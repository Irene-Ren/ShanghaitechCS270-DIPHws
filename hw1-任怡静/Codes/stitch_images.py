import sys
import cv2
import numpy as np
import random

MAX = 9999999
min_matches = 8
ERROR = 0.1

# stitch the images
def GetStitchedImage(img1, img2, M):
	r1,c1 = img1.shape[0:2]
	r2,c2 = img2.shape[0:2]

	img2_dims_temp = np.float32([ [0,0], [0,r2], [c2, r2], [c2,0] ]).reshape(-1,1,2)
	img2_dims = cv2.perspectiveTransform(img2_dims_temp, M)

	img1_dims = np.float32([ [0,0], [0,r1], [c1, r1], [c1,0] ]).reshape(-1,1,2)
	result_dims = np.concatenate( (img1_dims, img2_dims), axis = 0)

	[x_min, y_min] = np.int32(result_dims.min(axis=0).ravel() - 0.5)
	[x_max, y_max] = np.int32(result_dims.max(axis=0).ravel() + 0.5)
	
	# Create output array after affine transformation 
	transform_dist = [-x_min,-y_min]
	transform_array = np.array([[1, 0, transform_dist[0]], 
								[0, 1, transform_dist[1]], 
								[0,0,1]]) 

	# Warp images to get the resulting image
	output_img = cv2.warpPerspective(img2, transform_array.dot(M), 
									(x_max-x_min, y_max-y_min))
	output_img[transform_dist[1]:r1+transform_dist[1], 
				transform_dist[0]:c1+transform_dist[0]] = img1

	# Return the result
	return output_img
def FeatureMatcher(set_1, set_2):
	matchList_1to2 = []
	for i in range(len(set_1)):
		dist = MAX
		set2_1stNear_idx = 0
		set2_2ndNear_idx = 0
		for j in range(len(set_2)):
			tmp = np.linalg.norm(set_1[i]-set_2[j])
			if tmp < dist:
				dist = tmp
				set2_2ndNear_idx = set2_1stNear_idx
				set2_1stNear_idx = j
		matchList_1to2.append((i,set2_1stNear_idx))
	
	matchList_2to1 = []
	for i in range(len(set_2)):
		dist = MAX
		set1_1stNear_idx = 0
		set1_2ndNear_idx = 0
		for j in range(len(set_1)):
			tmp = np.linalg.norm(set_2[i]-set_1[j])
			if tmp < dist:
				dist = tmp
				set1_2ndNear_idx = set1_1stNear_idx
				set1_1stNear_idx = j
		matchList_2to1.append((i,set1_1stNear_idx))

	matches = []
	for set1_idx, set2_idx in matchList_1to2:
		if matchList_2to1[set2_idx][1] == set1_idx:
			matches.append((set1_idx, set2_idx))
	return matches
# Find SIFT and return Homography Matrix
def GetSiftHomography(img1, img2, verify_ratio):
	sift = cv2.xfeatures2d.SIFT_create()

	k1, d1 = sift.detectAndCompute(img1, None)
	k2, d2 = sift.detectAndCompute(img2, None)

	bf = cv2.BFMatcher()
	matches = bf.knnMatch(d1,d2, k=2)

	# More delicate matches filtered
	verified_matches = []
	for m1,m2 in matches:
		if m1.distance < verify_ratio * m2.distance:
			verified_matches.append(m1)

	# IMPORTANT: Uncomment this block of code to add the matching graphs
	# imgMatch = cv2.drawMatches(img1,k1,img2,k2,verified_matches, None, flags = 2)
	# cv2.imshow ('Result', imgMatch)
	# cv2.waitKey()
	
	# Got enough matching pairs
	if len(verified_matches) > min_matches:
		img1_pts = []
		img2_pts = []

		# Add matching points to array
		for match in verified_matches:
			img1_pts.append(k1[match.queryIdx].pt)
			img2_pts.append(k2[match.trainIdx].pt)
		img1_pts = np.float32(img1_pts).reshape(-1,1,2)
		img2_pts = np.float32(img2_pts).reshape(-1,1,2)
		
		# Compute homography matrix
		M, mask = cv2.findHomography(img1_pts, img2_pts, cv2.RANSAC, 5.0)
		return M
	else:
		print ('Error: Not enough matches')
		return None

def calculateHomography(correspondences):
    #loop through correspondences and create assemble matrix
    aList = []
    for corr in correspondences:
        p1 = np.matrix([corr.item(0), corr.item(1), 1])
        p2 = np.matrix([corr.item(2), corr.item(3), 1])

        a2 = [0, 0, 0, -p2.item(2) * p1.item(0), -p2.item(2) * p1.item(1), -p2.item(2) * p1.item(2),
              p2.item(1) * p1.item(0), p2.item(1) * p1.item(1), p2.item(1) * p1.item(2)]
        a1 = [-p2.item(2) * p1.item(0), -p2.item(2) * p1.item(1), -p2.item(2) * p1.item(2), 0, 0, 0,
              p2.item(0) * p1.item(0), p2.item(0) * p1.item(1), p2.item(0) * p1.item(2)]
        aList.append(a1)
        aList.append(a2)

    matrixA = np.matrix(aList)

    #svd composition
    u, s, v = np.linalg.svd(matrixA)

    #reshape the min singular value into a 3 by 3 matrix
    h = np.reshape(v[8], (3, 3))

    #normalize and now we have h
    h = np.squeeze(np.asarray((1/h.item(8)) * h))
    return h

def geometricDistance(correspondence, h):

    p1 = np.transpose(np.matrix([correspondence[0].item(0), correspondence[0].item(1), 1]))
    estimatep2 = np.dot(h, p1)
    estimatep2 = (1/estimatep2.item(2))*estimatep2

    p2 = np.transpose(np.matrix([correspondence[0].item(2), correspondence[0].item(3), 1]))
    error = p2 - estimatep2
    return np.linalg.norm(error)

def ransac(corr, thresh, confidence, Npairs, distance):
    maxInliers = []
    finalH = None
	# m = ceil(log(1 - confidence) / log(1 - thresh^Npairs))
    for i in range(1000):
        #find 4 random points to calculate a homography
        c1 = corr[random.randrange(0, len(corr))]
        c2 = corr[random.randrange(0, len(corr))]
        randomFour = np.vstack((c1, c2))
        c3 = corr[random.randrange(0, len(corr))]
        randomFour = np.vstack((randomFour, c3))
        c4 = corr[random.randrange(0, len(corr))]
        randomFour = np.vstack((randomFour, c4))

        #call the homography function on those points
        h = calculateHomography(randomFour) 
        inliers = []

        for i in range(len(corr)):
            d = geometricDistance(corr[i], h)
            if d < distance:
                inliers.append(corr[i])

        if len(inliers) > len(maxInliers):
            maxInliers = inliers
            finalH = h
        print ("Corr size: ", len(corr), " NumInliers: ", len(inliers), "Max inliers: ", len(maxInliers))

        if len(maxInliers) > (len(corr)*thresh):
            break
    return finalH, maxInliers

# Call main function
if __name__=='__main__':
	# Get input set of images
	img1 = cv2.imread(sys.argv[1])
	img2 = cv2.imread(sys.argv[2])

	# Initialize SIFT 
	sift = cv2.xfeatures2d.SIFT_create()

	# Extract keypoints and descriptors
	k1, d1 = sift.detectAndCompute(img1, None)
	k2, d2 = sift.detectAndCompute(img2, None)
	
	correspondenceList = []
	keypoints = [k1, k2]
	bf = cv2.BFMatcher()
	matches = bf.knnMatch(d1,d2, k=1)
	for match in matches:
		(x1, y1) = keypoints[0][match[0].queryIdx].pt
		(x2, y2) = keypoints[1][match[0].trainIdx].pt
		correspondenceList.append([x1, y1, x2, y2])

	corrs = np.matrix(correspondenceList)
	finalH, inliers = ransac(corrs, 0.60, 0.99, len(corrs),5)
	M =  GetSiftHomography(img1, img2, 0.8)
	if M is not None:
		for i in range(len(finalH)):
			for j in range(len(finalH)):
				if abs(finalH[i][j] - M[i][j]) > ERROR:
					finalH = M
					break

	# Stitch the images together using homography matrix
	result_image = GetStitchedImage(img2, img1, finalH)

	# Show the resulting image
	cv2.imshow ('Result', result_image)
	cv2.waitKey()