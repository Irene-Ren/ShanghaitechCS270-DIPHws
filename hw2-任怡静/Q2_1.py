import cv2
import sys
import numpy as np
from scipy.io import loadmat

girl_img = cv2.imread("hw2_files\Q2\girl.jpeg")
man_img = cv2.imread("hw2_files\Q2\man.jpg")
girl_features = loadmat("hw2_files\Q2\girl_features.mat")["girl_features"]
girl_features = np.float32(girl_features)
man_features = loadmat("hw2_files\Q2\man_features.mat")["man_features"]
man_features = np.float32(man_features)
M = cv2.getAffineTransform(man_features[0:3], girl_features[0:3])
man_trans = np.zeros(girl_img.shape)
grow,gcol,_ = girl_img.shape
for i in range(3):
    man_trans[:,:,i] = cv2.warpAffine(man_img[:,:,i], M, (gcol,grow))
cv2.imshow("Pic",np.uint8(man_trans))
cv2.waitKey(0)
C = cv2.addWeighted(np.uint8(girl_img), 0.5, np.uint8(man_trans), 0.5, 0.0)
cv2.imshow("Answer",C)
cv2.waitKey(0)
cv2.destroyAllWindows()