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
print(watermark.shape)
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
################################################
def zigZag(block):
    lines=[[] for i in range(8+8-1)] 
    for y in range(8): 
        for x in range(8): 
            i=y+x 
            if(i%2 ==0): 
                lines[i].insert(0,block[y][x]) 
            else:  
                lines[i].append(block[y][x]) 
    # print(lines)
    return np.asarray([coefficient for line in lines for coefficient in line])


def TruncateEndZeros(zigzagAC):
    index = len(zigzagAC) - 1
    truncated = []
    while index >= 0:
        if zigzagAC[index] != 0:
            # print("FOUND: ",index)
            break
        index -= 1
    for i in range(index+1):
        truncated.append(zigzagAC[i])
    return truncated

def CollectSymbols(qDctBlocks):
    symbols = []
    for i in range(row_8):
        for j in range(col_8):
            subSym = TruncateEndZeros(zigZag(qDctBlocks[i][j])[1:])
            for s in subSym:
                if s != 0:
                    symbols.append(s)
    return symbols

symbols = CollectSymbols(qDctBlocks)
# print(symbols)
print(len(symbols))
def EncodeWatermark(originImg, watermark, alpha):
    row, col, _ = originImg.shape
    yChannel = originImg[:,:,0]
    # print(row,col)
    wrow,wcol = watermark.shape
    print(wrow,wcol)

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
    with open('coordinates.txt', 'w') as f:
        for item in kLargestIndices:
            f.write("%d," % item)
    return encryptedImg,kLargestIndices

# testarray = np.asarray([[10,10,7,6,5],[4,3,3,1,0]])
# testmatrix = np.asarray([[10,2,3,4,3],[2,10,7,6,0],[10,7,6,5,3],[1,1,1,0,0],[4,4,2,3,10]])
# # testmatrix = np.asarray([[10,10,10,10,10],[10,10,10,10,10],[10,10,10,10,10],[10,10,10,10,10],[10,10,10,10,10]])
# encryptedImg, positionDict = EncodeWatermark(testmatrix, testarray,2)
# print(encryptedImg)
# print(positionDict)

encryptedImg, positionDict = EncodeWatermark(ycbcr, watermark,0.2)
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

extractedWM = DecodeWatermark(ycbcr,encryptedImg,positionDict,wrow,wcol,0.2)

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
extractedWM = cv2.resize(extractedWM,(wcol*ratio,wrow*ratio))
cv2.imshow("ExtractedWm",extractedWM.astype(np.uint8))
cv2.waitKey(0)
cv2.destroyAllWindows()
