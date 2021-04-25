import cv2
import numpy as np
from scipy.fftpack import dct, idct
from scipy.io import loadmat
import sys
import getopt
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
                    if qDctBlocks_o[i,j,s,t] != 0:
                        if not (s == 0 and t == 0):
                            watermark[k//wcol][k%wcol] = (qDctBlocks_e[i,j,s,t] / qDctBlocks_o[i,j,s,t] - 1) / alpha
                            k += 1
    return None

if __name__ == "__main__":
    ratio = 1
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ed")
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        sys.exit(2)
    for o, a in opts:
        if o == "-e":
            imgPath = args[0]
            wmPath = args[1]
            img = cv2.imread(imgPath)
            watermarkData = loadmat(wmPath)

            watermark = watermarkData["LOGO_CS270"]
            cv2.imshow("watermark",watermark.astype(np.uint8))
            cv2.waitKey(0)
            watermark = watermark[50:100,40:200]
            wrow,wcol = watermark.shape
            watermark = cv2.resize(watermark,(int(wcol/ratio),int(wrow/ratio)))
            wrow,wcol = int(wrow/ratio),int(wcol/ratio)
            
            for i in range(watermark.shape[0]):
                for j in range(watermark.shape[1]):
                    watermark[i, j] /= 255

            ycbcr = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
            row, col, _ = img.shape
            row_8,col_8 =row//8,col//8
            watermarkedBlocks = EncodeWatermarkBlocks(ycbcr[:,:,0],watermark,2)
            encryptedImg = RebuildPicture(watermarkedBlocks, ycbcr).astype(np.uint8)
            bgr = cv2.cvtColor(encryptedImg, cv2.COLOR_YCrCb2BGR)
            cv2.imwrite("EncryptedImage.tiff", bgr)

            cv2.imshow("Origin",img.astype(np.uint8))
            cv2.waitKey(0)
            cv2.imshow("Encrypted image",bgr)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        elif o == "-d":
            imgPath = args[0]
            enimgPath = args[1]
            img = cv2.imread(imgPath)
            encrypted = cv2.imread(enimgPath)
            ycbcr = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
            encryptedImg = cv2.cvtColor(encrypted, cv2.COLOR_BGR2YCR_CB)
            row, col, _ = img.shape
            row_8,col_8 =row//8,col//8
            wrow,wcol = 50,160

            extractedWM = DecodeWatermark(ycbcr[:,:,0],encryptedImg[:,:,0],wrow,wcol,2)
            for i in range(extractedWM.shape[0]):
                for j in range(extractedWM.shape[1]):
                    extractedWM[i,j] *= 255
                    if extractedWM[i,j] > 255:
                        extractedWM[i,j] = 255
            
            extractedWM = cv2.resize(extractedWM,(wcol*ratio,wrow*ratio))
            realWm = np.ones((150,240)) * 255
            realWm[50:100,40:200] = extractedWM
            invertedWM = 255 - realWm
            kernel = np.ones((2,2),np.uint8)
            erosionWM = cv2.erode(invertedWM,kernel,iterations = 2)
            kernel3 = np.ones((3,3),np.uint8)
            kernel3[0][0] = 0
            kernel3[2][0] = 0
            kernel3[0][2] = 0
            kernel3[2][2] = 0
            dilation = cv2.dilate(erosionWM,kernel3,iterations = 1)
            realWm = 255 - dilation
            cv2.imshow("ExtractedWm",realWm.astype(np.uint8))
            cv2.imwrite("ExtractedWatermark.jpg", realWm.astype(np.uint8))
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            assert False, "unhandled option"