import numpy as np
import scipy
import cv2
img = cv2.imread("hw2_files/Q3/1/1.png")
# img = cv2.imread("EncryptedImage.tiff")
row, col, _ = img.shape

cv2.imshow("Original Image",img)
cv2.waitKey(0)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

f = np.fft.fft2(gray)
fshift = np.fft.fftshift(f)
magnitude_spectrum = 20*np.log(np.abs(fshift))

cv2.imshow("fft transform",magnitude_spectrum.astype(np.uint8))
cv2.waitKey(0)
cv2.destroyAllWindows()
