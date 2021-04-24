import cv2
import numpy as np
from scipy.fftpack import dct, idct
from scipy.io import loadmat

img = cv2.imread("hw2_files\Q1\lena.tiff")
watermarkData = loadmat("hw2_files\Q1\LOGO_CS270.mat")

watermark = watermarkData["LOGO_CS270"]

ycbcr = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
row, col, _ = img.shape

# oriDCT = np.zeros((row,col))
# gray = ycbcr[:,:,0]
# oriDCT[:,:] = dct(dct(gray.T, norm = 'ortho').T,norm = 'ortho')
# acDCTlist = oriDCT.flatten()[1:]
# k = 10
# kLargest = list(acDCTlist[np.argsort(acDCTlist,axis=None)])[row*col-k-1:][::-1]
# print(kLargest)

# recovered = np.zeros((row,col))
# recovered[:,:] = idct(idct(oriDCT.T,norm = 'ortho').T,norm = 'ortho')
# cv2.imshow("Recovered",recovered.astype(np.uint8))
wrow, wcol = watermark.shape
print("You are to expect finding", wrow*wcol, "numbers, PLEASE BE PATIENT,press any key to start")
cv2.imshow("watermark",watermark.astype(np.uint8))
cv2.waitKey(0)
cv2.destroyAllWindows()

def EncodeWatermark(origin, watermark, alpha):
    row, col = origin.shape
    print(row,col)
    wrow,wcol = watermark.shape
    print(wrow,wcol)

    oriDCT = np.zeros((row,col))
    oriDCT[:,:] = dct(dct(origin.T, norm = 'ortho').T,norm = 'ortho')

    oriDCT = origin # test code

    acDCTlist = oriDCT.flatten()[1:]
    kLargest = list(acDCTlist[np.argsort(acDCTlist,axis=None)])[row*col-wrow*wcol-1 :][::-1]

    encryptPosDict = {}
    for k in range(len(kLargest)):
        found = False
        for i in range(0,row):
            if found:
                break
            for j in range(0,col):
                if i == 0 and j == 0:
                    continue
                if found:
                    break
                if oriDCT[i][j] == kLargest[k]:
                    # print(encryptPosDict)
                    if (i,j) not in encryptPosDict.keys():
                        print("position",(i,j),"occupied by index ",k,kLargest[k],"in watermark list")
                        oriDCT[i][j] = oriDCT[i][j] * (1+alpha*watermark[k//wcol][k%wcol])
                        encryptPosDict[(i,j)] = k
                        found = True
                    else:
                        # print("position",(i,j),"been taken by ",k,kLargest[k],"in watermark list")
                        continue

    encryptedImg = np.zeros((row,col))
    encryptedImg[:,:] = idct(idct(oriDCT.T, norm = 'ortho').T,norm = 'ortho')
    return encryptedImg,encryptPosDict

# testarray = np.asarray([[10,10,7,6,5],[4,3,3,1,0]])
# testmatrix = np.asarray([[10,2,3,4,3],[2,10,7,6,0],[10,7,6,5,3],[1,1,1,0,0],[4,4,2,3,10]])
# testmatrix = np.asarray([[10,10,10,10,10],[10,10,10,10,10],[10,10,10,10,10],[10,10,10,10,10],[10,10,10,10,10]])
encryptedImg, positionDict = EncodeWatermark(ycbcr[:,:,0], watermark,2)
cv2.imshow("Encrypted image",encryptedImg.astype(np.uint8))
cv2.waitKey(0)
cv2.destroyAllWindows()
# print(dctResult)
# print(positions)