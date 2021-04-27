import numpy as np
import scipy
import cv2
from scipy import ndimage
import matplotlib.pyplot as plt


img = cv2.imread("hw2_files/Q3/1/1.png")
# img = cv2.imread("EncryptedImage.tiff")
row, col, _ = img.shape
print(row, col)

cv2.imshow("Original Image",img)
cv2.waitKey(0)

ycbcr = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
gray = ycbcr[:,:,0]

f = np.fft.fft2(gray)

fshift = np.fft.fftshift(f)
magnitude_spectrum = 15*np.log(np.abs(fshift))

cv2.imshow("fft transform",magnitude_spectrum.astype(np.uint8))
cv2.waitKey(0)


test = magnitude_spectrum

# threshold
thresh = cv2.adaptiveThreshold(test.astype(np.uint8), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 13, 3)
thresh = 255 - thresh

# apply close to connect the white areas
kernel = np.ones((3,3), np.uint8)
morph = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
kernel = np.ones((1,9), np.uint8)
morph = cv2.morphologyEx(morph, cv2.MORPH_CLOSE, kernel)

# apply canny edge detection
edges = cv2.Canny(morph, 150, 200)

# get hough lines
result = img.copy()
lines = cv2.HoughLines(edges, 1, np.pi/180, 50)
# Draw line on the image
rho,theta = lines[0].flatten()[0],lines[0].flatten()[1]
print(rho,theta)
a = np.cos(theta)
b = np.sin(theta)
x0 = a*rho
y0 = b*rho
x1 = int(x0 + 1000*(-b))
y1 = int(y0 + 1000*(a))
x2 = int(x0 - 1000*(-b))
y2 = int(y0 - 1000*(a))
cv2.line(result, (x1, y1), (x2, y2), (0, 0, 255), 1)
# show thresh and result    

#rotation angle in degree
rotated = ndimage.rotate(test.astype(np.uint8), theta * 180 /np.pi)
# rotated = ndimage.rotate(result, theta * 180 /np.pi)
cv2.imshow("thresh", thresh)
cv2.imshow("morph", morph)
cv2.imshow("edges", edges)
cv2.imshow("result", result)
cv2.imshow("rotated", rotated)
cv2.waitKey(0)
cv2.destroyAllWindows()

proj = np.sum(rotated,axis = 0)
xaxis = [i for i in range(proj.shape[0])]
print(proj.shape)
maxValue = max(proj)
maxIndex = 0
for i in range(proj.shape[0]):
    if proj[i] == maxValue:
        maxIndex = i
        break
print(maxIndex)
index_1, index_2 = 0,0
for i in range(100):
    currV = proj[maxIndex - i]
    nextV = proj[maxIndex - i - 1]
    if currV < nextV:
        index_1 = i
        break

for i in range(100):
    currV = proj[maxIndex + i]
    nextV = proj[maxIndex + i + 1]
    if currV < nextV:
        index_2 = i
        break
print(index_1, index_2)
L = 2 * row / (index_1+index_2)
print(L)
plt.plot(xaxis,proj)
plt.show()
# print(proj)
