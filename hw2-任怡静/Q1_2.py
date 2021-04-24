import cv2
import numpy as np
from scipy.fftpack import dct, idct
from scipy.io import loadmat

img = cv2.imread("hw2_files\Q1\lena.tiff")
watermarkData = loadmat("hw2_files\Q1\LOGO_CS270.mat")

watermark = watermarkData["LOGO_CS270"]
cv2.imshow("watermark",watermark.astype(np.uint8))
cv2.waitKey(0)
for i in range(watermark.shape[0]):
    for j in range(watermark.shape[1]):
        watermark[i, j] /= 255

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


def EncodeWatermark(originImg, watermark, alpha):
    row, col, _ = originImg.shape
    yChannel = originImg[:,:,0]
    # print(row,col)
    wrow,wcol = watermark.shape
    # print(wrow,wcol)

    oriDCT = np.zeros((row,col))
    oriDCT[:,:] = dct(dct(yChannel.T, norm = 'ortho').T,norm = 'ortho')

    # oriDCT = yChannel # test code

    acDCTlist = oriDCT.flatten()[1:]
    kLargestIndices = np.argsort(acDCTlist,axis=None)[row*col-wrow*wcol-1 :][::-1]
    # print(kLargestIndices)
    # print(acDCTlist[kLargestIndices])
    # print(len(kLargestIndices))

    copyDCT = oriDCT
    for k in range(len(kLargestIndices)):
        kvalue = kLargestIndices[k]+1
        # print("DCT transform",kvalue//col,kvalue%col)
        # print("watermark index",k//wrow,k%wcol)
        copyDCT[kvalue//col][kvalue%col] = oriDCT[kvalue//col][kvalue%col] * (1 + alpha * watermark[k//wcol][k%wcol])

    encryptedImg = np.zeros((row,col,3))
    encryptedImg[:,:,0] = idct(idct(copyDCT.T, norm = 'ortho').T,norm = 'ortho')
    encryptedImg[:,:,1] = originImg[:,:,1]
    encryptedImg[:,:,2] = originImg[:,:,2]
    
    # print(np.max(encryptedImg))

    # encryptedImg = copyDCT # test code

    bgr = cv2.cvtColor(encryptedImg.astype(np.uint8), cv2.COLOR_YCrCb2BGR)
    cv2.imwrite("EncryptedImage.tiff", bgr)

    return encryptedImg,kLargestIndices

# testarray = np.asarray([[10,10,7,6,5],[4,3,3,1,0]])
# testmatrix = np.asarray([[10,2,3,4,3],[2,10,7,6,0],[10,7,6,5,3],[1,1,1,0,0],[4,4,2,3,10]])
# # testmatrix = np.asarray([[10,10,10,10,10],[10,10,10,10,10],[10,10,10,10,10],[10,10,10,10,10],[10,10,10,10,10]])
# encryptedImg, positionDict = EncodeWatermark(testmatrix, testarray,2)
# print(encryptedImg)
# print(positionDict)

encryptedImg, positionDict = EncodeWatermark(ycbcr, watermark,0.25)
print(encryptedImg.shape)


cv2.imshow("Origin",ycbcr.astype(np.uint8))
cv2.waitKey(0)
cv2.imshow("Encrypted image",encryptedImg.astype(np.uint8))
cv2.waitKey(0)

def DecodeWatermark(originImg, encryptedImg,kLargestIndices,wrow,wcol,alpha):
    row, col, _ = encryptedImg.shape
    yChannel_e = encryptedImg[:,:,0]
    yChannel_o = originImg[:,:,0]
    # print(row,col)
    watermark = np.zeros((wrow,wcol))

    oriDCT = np.zeros((row,col))
    oriDCT[:,:] = dct(dct(yChannel_o.T, norm = 'ortho').T,norm = 'ortho')
    encryptDCT = np.zeros((row,col))
    encryptDCT[:,:] = dct(dct(yChannel_e.T, norm = 'ortho').T,norm = 'ortho')
    for k in range(len(kLargestIndices)):
        kvalue = kLargestIndices[k]+1
        # print("DCT transform",kvalue//col,kvalue%col)
        # print("watermark index",k//wrow,k%wcol)
        watermark[k//wcol][k%wcol] = (encryptDCT[kvalue//col][kvalue%col] / oriDCT[kvalue//col][kvalue%col] - 1) / alpha
    return watermark

extractedWM = DecodeWatermark(ycbcr,encryptedImg,positionDict,wrow,wcol,0.25)
for i in range(extractedWM.shape[0]):
    for j in range(extractedWM.shape[1]):
        extractedWM[i,j] *= 255
cv2.imshow("ExtractedWm",extractedWM.astype(np.uint8))
cv2.waitKey(0)
cv2.destroyAllWindows()

