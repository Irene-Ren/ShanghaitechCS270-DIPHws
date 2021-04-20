from scipy.fftpack import dct, idct
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

temporary = {}
keys_nominees = []
g = 0

def DctAndQuantization(img_source_64):
    part_8 = np.zeros((8,8))
    b = np.zeros((8,8))

    for i in range(8):
        for j in range(8):
            b[i][j] = img_source_64[i][j] - 128
    c = scipy.fftpack.dct(scipy.fftpack.dct(b, axis = 0,norm = 'ortho'),axis = 1,norm='ortho')
    # print(type(c))

    for i in range(8):
        for j in range(8):
            part_8[i][j] = np.fix(c[i][j]/Y_table[i][j])
    # print(type(part_8))
    return part_8

def ZigZag(matrix, row, col):
    global g
    
    matrix = np.array(matrix)
    aux = np.zeros(row*col)

    solution = [[] for i in range(row+col-1)]

    for i in range(row):
        for j in range(col):
            sum = i+j
            if sum % 2 == 0:
                solution[sum].insert(0,matrix[i][j])
            else:
                solution[sum].append(matrix[i][j])
    # solution = solution.reverse()
    # print("Solution: ", solution) 

    # Strip out the non-zero value from the zigzag form
    count = 0
    
    for i in solution:
        for j in i:
            if j == -0.0:
                aux[count] = 0
            else:
                aux[count] = j
            count += 1
    # index = 0
    # for i in range(row*col):
    #     if aux[i] != 0:
    #         index = i
    #         break
    for i in range(0, row*col):
        temporary[g] = aux[i]
        if aux[i] in keys_nominees:
            continue
        else:
            keys_nominees.append(aux[i])
        g += 1
    

img = cv2.imread("hw2_files\Q1\lena.tiff")
cv2.imshow("Original Image",img)
cv2.waitKey(0)
cv2.destroyAllWindows()

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
row, col = img_gray.shape
# print(row,col)
# print(img_gray)

ori_matrix = np.asarray(img_gray,dtype=np.float32)
dct_matrix = np.zeros((row,col))
for i in range(0,row,8):
    for j in range(0,col,8):
        dct_matrix[i:(i+8),j:(j+8)] = DctAndQuantization(ori_matrix[i:(i+8),j:(j+8)])
dct_img = dct_matrix.astype(np.uint8)
# print(dct_matrix)
cv2.imshow("DCT Image",dct_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
for i in range(0,row,8):
        for j in range(0,col,8):
            ZigZag(dct_matrix[i:(i+8),j:(j+8)],8,8)
print(temporary)
elements = list(temporary.values())

probabilities = {}
for i in keys_nominees:
    t_element = float(elements.count(i))
    probabilities[i] = t_element/float(len(elements))

"""save the probability dictionary into .txt file"""
pos = 0
file = open("result.txt","w")
for i in probabilities:
    file.write(str(keys_nominees[pos]) +"\t"+ str(probabilities.get(i))+"\n")
    pos+= 1