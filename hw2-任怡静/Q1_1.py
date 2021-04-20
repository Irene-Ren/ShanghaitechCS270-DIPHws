import cv2
from scipy.fftpack import dct, idct
import scipy
import numpy as np
import os
import matplotlib.pyplot as plt

Y_table = [[16, 11, 10, 16, 24, 40, 51, 61],
           [12, 12, 14, 19, 26, 58, 60, 55],
           [14, 13, 16, 24, 40, 57, 69, 56],
           [14, 17, 22, 29, 51, 87, 80, 62],
           [18, 22, 37, 56, 68 ,109 ,103 ,77],
           [24, 35, 55, 64, 81 ,104 ,113 ,92],
           [49, 64, 78, 87, 103, 121, 120, 101],
           [72, 92, 95, 98, 112, 100, 103, 99]]
# read the image and determine the row,col of the image (512x512)
img = cv2.imread("hw2_files\Q1\lena.tiff")
row, col, _ = img.shape
print("row: ",row, "col: ",col)

row_8,col_8 =row//8,col//8

cv2.imshow("Original Image",img)
cv2.waitKey(0)

ycbcr = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
cv2.imshow("YCBCR Image",ycbcr.astype(np.uint8))
cv2.waitKey(0)

# test code to see if the image converting to YCRCB is broken
bgr = cv2.cvtColor(ycbcr, cv2.COLOR_YCrCb2BGR)
cv2.imshow("Restored RGB Image",bgr)
cv2.waitKey(0)
cv2.destroyAllWindows()

def Cut_64Blocks(img):
    blocks = np.zeros((row, col, 8, 8, 3),dtype = np.int16)
    for i in range (row_8):
        for j in range (col_8):
            blocks[i][j] = img[i*8:(i+1)*8,j*8:(j+1)*8]
    return np.asarray(blocks)

def DCTOnBlocks(blocks):
    dctBlocks = np.zeros((row,col,8,8,3))
    for i in range(row_8):
        for j in range(col_8):
            dct_b = np.zeros((8,8,3))
            for alpha in range(3):
               b = blocks[i][j][:,:,alpha]
               dct_b[:,:,alpha] = dct(dct(b.T, norm = 'ortho').T,norm = 'ortho')
            dctBlocks[i][j] = dct_b
    return dctBlocks

blocks = Cut_64Blocks(ycbcr)
print(blocks[0][0][:,:,1])
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
  return np.asarray([coefficient for line in lines for coefficient in line])
print(qDctBlocks[0][0][:,:,0])
zigZag(qDctBlocks[0][0][:,:,0])