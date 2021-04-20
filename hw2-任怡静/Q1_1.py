import cv2
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

cv2.imshow("Original Image",img)
cv2.waitKey(0)

ycbcr = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
bgr = cv2.cvtColor(ycbcr, cv2.COLOR_YCrCb2BGR)
cv2.imshow("YCBCR Image",ycbcr.astype(np.uint8))
cv2.waitKey(0)

# test code to see if the image converting to YCRCB is broken
cv2.imshow("Restored RGB Image",bgr)
cv2.waitKey(0)
cv2.destroyAllWindows()

# def Cut_64Blocks(img):
