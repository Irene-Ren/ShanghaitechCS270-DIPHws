import cv2
import numpy as np
from scipy.fftpack import dct, idct
from scipy.io import loadmat

img = cv2.imread("hw2_files\Q1\lena.tiff")
watermark = loadmat("hw2_files\Q1\LOGO_CS270.mat")

print(type(watermark["LOGO_CS270"]))

ycbcr = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
row, col, _ = img.shape
oriDCT = np.zeros((row,col))
oriDCT[:,:] = dct(dct(ycbcr[:,:,0].T, norm = 'ortho').T,norm = 'ortho')
print(np.max(oriDCT))
k = 10
test = list(oriDCT.flatten()[np.argsort(oriDCT,axis=None)])[row*col - k :]
print(test)
print(len(test))



def EncodeWatermark(origin, watermark, alpha):
    row, col, _ = origin.shape
    wrow,wcol = watermark.shape
    oriDCT = np.zeros((row,col))
    oriDCT[:,:] = dct(dct(origin.T, norm = 'ortho').T,norm = 'ortho')
    kLargest = list(oriDCT.flatten()[np.argsort(oriDCT,axis=None)])[row*col-wrow*wcol :]
    encriptPosMap = np.zeros((row,col))
    lastStopDict = {}
    for k in range(len(kLargest)):
        found = False
        if lastStopDict[k]:
            start_r, start_c = lastStopDict[k][0], lastStopDict[k][1]
        else:
            start_r, start_c = 0, 0
        for i in range(start_r,row):
            if found:
                break
            for j in range(start_c,col):
                if found:
                    break
                if oriDCT[i][j] == kLargest[k]:
                    if encriptPosMap[i][j] == 0:
                        oriDCT[i][j] = oriDCT[i][j] * (1+alpha*watermark[k//wrow][k%wrow])
                        encriptPosMap[i][j] = 1
                        found = True
                        lastStopDict[k] = (i,j)
                    else:
                        continue


