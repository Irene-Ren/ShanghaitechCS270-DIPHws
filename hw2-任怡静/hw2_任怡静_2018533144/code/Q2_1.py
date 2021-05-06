import cv2
import sys
import numpy as np
from scipy.io import loadmat
from scipy.signal import convolve2d

kernel = np.array([0.25-0.4/2.0, 0.25, 0.4, 0.25, 0.25-0.4/2.0])
gaussian = np.outer(kernel, kernel)

def Reduce(layer, gaussian):
    # return layer[::2, ::2]
    return convolve2d(layer, gaussian,'same')[::2, ::2]

def Expand(layer, gaussian):
    row, col = layer.shape
    expanded = np.zeros((row * 2,col * 2))
    expanded[::2,::2] = layer
    return convolve2d(expanded, gaussian, 'same') * 4

def GaussianPyramid(layer, levels):
    pyramid = []
    pyramid.append(layer)

    for i in range(levels):
        pyramid.append(Reduce(pyramid[i],gaussian))

    return pyramid

def LaplacianPyramid(gaussianPyr):
    lap_pyramid = []
    for i in range(len(gaussianPyr) - 1):
        row, col = gaussianPyr[i].shape
        lap_pyramid.append(gaussianPyr[i] - Expand(gaussianPyr[i+1], gaussian)[0:row, 0:col])
    lap_pyramid.append(gaussianPyr[len(gaussianPyr) - 1])
    return lap_pyramid

def Blend(lap_p1, lap_p2, gaussPyrMask):
    blend_pyramid = []
    for i in range(len(gaussPyrMask)):
        level = lap_p2[i] * (1-gaussPyrMask[i]) + lap_p1[i] * gaussPyrMask[i]
        blend_pyramid.append(level)
    return blend_pyramid

def Collapse(blend_pyramid):
    # test = []
    # for p in blend_pyramid:
    #     test.append(p.shape)
    # print(test)
    layer = blend_pyramid[len(blend_pyramid) - 1]
    for i in range(len(blend_pyramid)-2, -1, -1):
        row, col = blend_pyramid[i].shape
        layer = Expand(layer, gaussian)[0:row, 0:col] + blend_pyramid[i]
    return layer

def ImageResize(img, ratio):
    row = img.shape[0]
    col = img.shape[1]
    ret = cv2.resize(img,(int(col*ratio),int(row*ratio)))
    return ret

def reconstruct_lablacian(laplacian_pyramid):
    output = np.zeros(
        (laplacian_pyramid[0].shape[0], laplacian_pyramid[0].shape[1]), dtype=np.float64)
    for i in range(len(laplacian_pyramid) - 1, 0, -1):
        expanded_lap = Expand(laplacian_pyramid[i], gaussian)
        next_lap = laplacian_pyramid[i - 1]
        if expanded_lap.shape[0] > next_lap.shape[0]:
            expanded_lap = np.delete(expanded_lap, (-1), axis=0)
        if expanded_lap.shape[1] > next_lap.shape[1]:
            expanded_lap = np.delete(expanded_lap, (-1), axis=1)
        tmp = expanded_lap + next_lap
        laplacian_pyramid.pop()
        laplacian_pyramid.pop()
        laplacian_pyramid.append(tmp)
        output = tmp
    return output

girl_img = cv2.imread("..\material\hw2_files\Q2\girl.jpeg")
man_img = cv2.imread("..\material\hw2_files\Q2\man.jpg")

# Registeration Read from mat files
# girl_features = loadmat("..\material\hw2_files\Q2\girl_features.mat")["girl_features"]
# girl_features = np.float32(girl_features)
# man_features = loadmat("..\material\hw2_files\Q2\man_features.mat")["man_features"]
# man_features = np.float32(man_features)
# M = cv2.getAffineTransform(man_features, girl_features)

# Registeration predefined
M = np.array([[1.6909, -0.0104,-88.1811],[0.0104, 1.6909, -109.4904]])

#Not so good backups
# M = np.array([[1.6939, -0.0215,-87.1060],[0.0215, 1.6939, -111.8089]])
# M = np.array([[1.6327, -0.0219,-76.5426],[0.0219, 1.6327, -100.1675]])

# print(M)
man_trans = np.zeros(girl_img.shape)
grow,gcol,_ = girl_img.shape
for i in range(3):
    man_trans[:,:,i] = cv2.warpAffine(man_img[:,:,i], M, (gcol,grow))

mask = np.zeros((grow,gcol))
mask[:,0:int(gcol / 2)] = np.ones((grow,int(gcol/2)))

C = cv2.addWeighted(np.uint8(girl_img), 0.5, np.uint8(man_trans), 0.5, 0.0)
cv2.imshow("RegisterationResult",C)
cv2.imwrite("..\\result\Q2\RegisterationResult_p.jpg", C)
print("PRESS ENTER TO PROCEED")
cv2.waitKey(0)
cv2.destroyAllWindows()

levels = 100
maskPry = GaussianPyramid(mask,levels)
image = np.zeros(girl_img.shape)

for i in range(3):
    man_pyr = GaussianPyramid(man_trans[:,:,i], levels)
    girl_pyr = GaussianPyramid(girl_img[:,:,i], levels)

    man_LPyr = LaplacianPyramid(man_pyr)
    girl_LPyr = LaplacianPyramid(girl_pyr)

    blend_pyr = Blend(man_LPyr, girl_LPyr, maskPry)
    recovered = Collapse(blend_pyr)

    reco_r,reco_c = recovered.shape
    for s in range(reco_r):
        for t in range(reco_c):
            if recovered[s, t] > 255:
                recovered[s, t] = 255
            if recovered[s, t] < 0:
                recovered[s, t] = 0
    image[:,:,i] = recovered

cv2.imshow("Blended", np.uint8(image))
cv2.imwrite("..\\result\Q2\BlendedImage_p.jpg", np.uint8(image))
print("PRESS ENTER TO PROCEED")
cv2.waitKey(0)
cv2.destroyAllWindows()