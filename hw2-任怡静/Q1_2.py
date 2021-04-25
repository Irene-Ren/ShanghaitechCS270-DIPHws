import cv2
import numpy as np
from scipy.fftpack import dct, idct
from scipy.io import loadmat

img = cv2.imread("hw2_files\Q1\lena.tiff")
watermarkData = loadmat("hw2_files\Q1\LOGO_CS270.mat")

watermark = watermarkData["LOGO_CS270"]
watermark = watermark[50:100,40:200]
wrow,wcol = watermark.shape
ratio = 1
watermark = cv2.resize(watermark,(int(wcol/ratio),int(wrow/ratio)))
wrow,wcol = int(wrow/ratio),int(wcol/ratio)
cv2.imshow("watermark",watermark.astype(np.uint8))
cv2.waitKey(0)
for i in range(watermark.shape[0]):
    for j in range(watermark.shape[1]):
        watermark[i, j] /= 255

ycbcr = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
row, col, _ = img.shape
row_8,col_8 =row//8,col//8
Y_table = [[16, 11, 10, 16, 24, 40, 51, 61],
           [12, 12, 14, 19, 26, 58, 60, 55],
           [14, 13, 16, 24, 40, 57, 69, 56],
           [14, 17, 22, 29, 51, 87, 80, 62],
           [18, 22, 37, 56, 68 ,109 ,103 ,77],
           [24, 35, 55, 64, 81 ,104 ,113 ,92],
           [49, 64, 78, 87, 103, 121, 120, 101],
           [72, 92, 95, 98, 112, 100, 103, 99]]
def Cut_Y64Blocks(yChannel):
    blocks = np.zeros((row_8, col_8, 8, 8),dtype = np.int16)
    for i in range (row_8):
        for j in range (col_8):
            blocks[i][j] = yChannel[i*8:(i+1)*8,j*8:(j+1)*8]
    return np.asarray(blocks)

def DCTOnBlocks(blocks):
    dctBlocks = np.zeros((row_8,col_8,8,8))
    for i in range(row_8):
        for j in range(col_8):
            dct_b = np.zeros((8,8))
            b = blocks[i][j][:,:]
            dct_b[:,:] = dct(dct(b.T, norm = 'ortho').T,norm = 'ortho')
            dctBlocks[i][j] = dct_b
    return dctBlocks

blocks = Cut_Y64Blocks(ycbcr[:,:,0])
dctBlocks = DCTOnBlocks(blocks)

qDctBlocks = (dctBlocks/Y_table).round().astype(np.int16)
# positives = []
# for i in range(row_8):
#     for j in range(col_8):
#         for s in range(8):
#             for t in range(8):
#                 if qDctBlocks[i,j,s,t] != 0:
#                     if not (s == 0 and t == 0):
#                         positives.append(qDctBlocks[i,j,s,t])
# print(positives)
# print(len(positives))
                
def EncodeWatermarkBlocks(originYchannel, watermark, alpha):
    wrow,wcol = watermark.shape
    print(wrow,wcol)

    blocks = Cut_Y64Blocks(originYchannel)
    dctBlocks = DCTOnBlocks(blocks)
    qDctBlocks = (dctBlocks/Y_table).round().astype(np.int16)

    # TODO: Need to make sure the value won't exceed, get all the non zero values and calculate the length, truncate k in range
    copyDCT = qDctBlocks
    k = 0
    for i in range(row_8):
        for j in range(col_8):
            for s in range(8):
                for t in range(8):
                    if k >= wrow*wcol:
                        return copyDCT
                    if s >= 5 and t >= 4:
                        break
                    if qDctBlocks[i,j,s,t] != 0:
                        if not (s == 0 and t == 0):
                            copyDCT[i,j,s,t] = qDctBlocks[i,j,s,t] * (1 + alpha * watermark[k//wcol][k%wcol])
                            k += 1
    return None
watermarkedBlocks = EncodeWatermarkBlocks(ycbcr[:,:,0],watermark,2)

def RebuildPicture(watermarkBlocks,YCbCrlayers):
    row = row_8 * 8
    col = col_8 * 8
    blocks = np.zeros((row_8,col_8,8,8))
    img = np.zeros((row,col,3))
    for i in range(row_8):
        for j in range(col_8):
            dct_b = watermarkBlocks[i][j] * Y_table
            blocks[i][j] = idct(idct(dct_b.T,norm = 'ortho').T,norm = 'ortho')
    for i in range(row_8):
        for j in range(col_8):
            img[i*8:(i+1)*8,j*8:(j+1)*8,0] = blocks[i,j]
    img[:,:,1] = YCbCrlayers[:,:,1]
    img[:,:,2] = YCbCrlayers[:,:,2]
    return img

encryptedImg = RebuildPicture(watermarkedBlocks, ycbcr)

cv2.imshow("Origin",ycbcr.astype(np.uint8))
cv2.waitKey(0)
cv2.imshow("Encrypted image",encryptedImg.astype(np.uint8))
cv2.waitKey(0)

def DecodeWatermark(originYchannel, encryptedYchannel,wrow,wcol,alpha):
    watermark = np.zeros((wrow,wcol))

    blocks_o = Cut_Y64Blocks(originYchannel)
    dctBlocks_o = DCTOnBlocks(blocks_o)
    qDctBlocks_o = (dctBlocks_o/Y_table).round().astype(np.int16)

    blocks_e = Cut_Y64Blocks(encryptedYchannel)
    dctBlocks_e = DCTOnBlocks(blocks_e)
    qDctBlocks_e = (dctBlocks_e/Y_table).round().astype(np.int16)

    k = 0
    for i in range(row_8):
        for j in range(col_8):
            for s in range(8):
                for t in range(8):
                    if k >= wrow*wcol:
                        return watermark
                    if s >= 5 and t >= 4:
                        break
                    if qDctBlocks_e[i,j,s,t] != 0:
                        if not (s == 0 and t == 0):
                            watermark[k//wcol][k%wcol] = (qDctBlocks_e[i,j,s,t] / qDctBlocks_o[i,j,s,t] - 1) / alpha
                            k += 1
    return None

extractedWM = DecodeWatermark(ycbcr[:,:,0],encryptedImg[:,:,0],wrow,wcol,2)

# encryptimg = cv2.imread("DecompressedImage.tiff")
# encryptycbcr = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
# my_file= open("coordinates.txt", "r")
# content = my_file.read()
# positionDict = content.split(",")
# my_file.close()
# positionDict.pop()
# print(len(positionDict))
# kLargestIndices = []
# for i in positionDict:
#     kLargestIndices.append(int(i))

# extractedWM = DecodeWatermark(ycbcr,encryptycbcr,kLargestIndices,wrow,wcol,0.2)

for i in range(extractedWM.shape[0]):
    for j in range(extractedWM.shape[1]):
        extractedWM[i,j] *= 255
        if extractedWM[i,j] > 255:
            extractedWM[i,j] = 255
extractedWM = cv2.resize(extractedWM,(wcol*ratio,wrow*ratio))
cv2.imshow("ExtractedWm",extractedWM.astype(np.uint8))
cv2.waitKey(0)
cv2.destroyAllWindows()
