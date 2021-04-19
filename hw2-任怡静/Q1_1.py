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

def DctAndQuantization(img_source_64):
    part_8 = np.zeros((8,8))
    b = np.zeros((8,8))

    for i in range(8):
        for j in range(8):
            b[i][j] = img_source_64[i][j] - 128
    c = dct(dct(b, axis = 0,norm = 'ortho'),axis = 1,norm='ortho')

    for i in range(8):
        for j in range(8):
            part_8 = np.fix(c[i][j]/Y_table[i][j])

    return part_8

