import cv2
import numpy as np

image = cv2.imread('images/q2.jpeg')
cv2.imshow("origin",image)
cv2.waitKey(0)
image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
ret, th3 = cv2.threshold(image_gray,127,255,cv2.THRESH_BINARY_INV)
kernelSizes = [(3, 3), (4, 4)]
for kernelSize in kernelSizes:
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernelSize)
    th3 = cv2.morphologyEx(th3, cv2.MORPH_CLOSE, kernel)

def EightNeighbors(layer, coordinate):
    row,col = layer.shape
    directions = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    eight_neighbors = []
    x,y = coordinate
    for dx,dy in directions:
        i = x+dx
        j = y+dy
        if i >= 0 and i < row and j >= 0 and j < col:
            if layer[i,j] > 0:
                eight_neighbors.append((i,j))
    return eight_neighbors
def BFSConnected(connected_list):
    if len(connected_list) == 0:
        return
    else:
        neigbor_list = []
        for coord in connected_list:
            x,y = coord
            layer[x,y] = 0 
            area.append((x,y))
            neigbors = EightNeighbors(layer, coord)
            for n in neigbors:
                if not neigbor_list.__contains__(n):
                    neigbor_list.append(n)
        BFSConnected(neigbor_list)

segments = []
area = []
layer = th3.copy()
row, col = layer.shape
layer_background = np.zeros((row, col, 3))
for i in range(row):
    for j in range(col):
        if layer[i, j] > 0:
            area = []
            connected_list = [(i,j)]
            BFSConnected(connected_list)
            segments.append(area)
        if th3[i,j] == 0:
            layer_background[i,j] = image[i,j]

layer_large = np.zeros((row, col, 3))   
layer_small = np.zeros((row, col, 3))     
for s in segments:
    if len(s) > 50:
        for coord in s:
            x,y = coord
            layer_large[x,y] = image[x,y]
    else:
        for coord in s:
            x,y = coord
            layer_small[x,y] = image[x,y]

layer_large = layer_large + layer_background
layer_small = layer_small + layer_background

cv2.imshow("background", np.uint8(layer_background))
cv2.waitKey(0)
cv2.imshow("large", np.uint8(layer_large))
cv2.waitKey(0)
cv2.imshow("small", np.uint8(layer_small))
cv2.waitKey(0)
layer_epsilon = np.uint8(layer_large) + np.uint8(layer_small) - np.uint8(layer_background) - np.uint8(image)

cv2.imshow("Epsilon", layer_epsilon)
cv2.waitKey(0)

print("the summation of I_epsilon is: ", np.sum(layer_epsilon))
cv2.destroyAllWindows()