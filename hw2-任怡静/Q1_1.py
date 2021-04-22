import cv2
from scipy.fftpack import dct, idct
import scipy
import numpy as np
import os
import matplotlib.pyplot as plt
from collections import Counter, OrderedDict

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

# cv2.imshow("Original Image",img)
# cv2.waitKey(0)

ycbcr = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
cv2.imshow("YCBCR Image",ycbcr.astype(np.uint8))
cv2.waitKey(0)

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

# testTrun = TruncateEndZeros(zigZag(qDctBlocks[0][0]))
# print("Truncated :",testTrun)

def CollectSymbols(qDctBlocks):
    symbols = []
    for i in range(row_8):
        for j in range(col_8):
            subSym = TruncateEndZeros(zigZag(qDctBlocks[i][j])[1:])
            symbols += [str(s) for s in subSym]
            symbols += "E"
    return symbols

symbols = CollectSymbols(qDctBlocks)
# print(symbols)

def CalculateProbabilities(symbols):
    counts = dict(Counter(symbols))
    probDict = dict(sorted(counts.items(), key=lambda item: item[1]))
    for key in probDict:
        probDict[key] /= float(len(symbols))
    return probDict

probDict = CalculateProbabilities(symbols)
# print(probDict)
# print(len(probDict))
# print(sum(probDict.values()))

def GenHuffmanDict(p):
    '''Return a Huffman code for an ensemble with distribution p.'''
    # print(sum(p.values()))
    # print(p)

    # Base case of only two symbols, assign 0 or 1 arbitrarily
    if(len(p) == 2):
        return dict(zip(p.keys(), ['0', '1']))

    # Create a new distribution by merging lowest prob. pair
    p_prime = p.copy()
    a1, a2 = lowest_prob_pair(p)
    p1, p2 = p_prime.pop(a1), p_prime.pop(a2)
    p_prime[a1 + a2] = p1 + p2

    # Recurse and construct code on new distribution
    c = GenHuffmanDict(p_prime)
    ca1a2 = c.pop(a1 + a2)
    c[a1], c[a2] = ca1a2 + '0', ca1a2 + '1'

    return c

def lowest_prob_pair(p):
    '''Return pair of symbols from distribution p with lowest probabilities.'''
    assert(len(p) >= 2) # Ensure there are at least 2 symbols in the dist.

    sorted_p = sorted(p.items(), key=lambda item: item[1])
    return sorted_p[0][0], sorted_p[1][0]

huffmanCodeDict = GenHuffmanDict(probDict)
# print(huffmanCodeDict)
# print(len(huffmanCodeDict))

def HuffmanEncode(huffmanCodeDict, qDctBlocks, endCode): 
    #TODO: NEED to determine one that is unique, also the DC part need some considerations
    codeWords = ''
    code_dc = ''
    
    for i in range(row_8):
        for j in range(col_8):
            tmp = TruncateEndZeros(zigZag(qDctBlocks[i][j]))
            # print(tmp)
            dc = tmp.pop(0)
            # print(tmp)

            code_dc += '{0:08b}'.format(dc)
            
            code = ''
            for t in tmp:
                # print(t)
                code += huffmanCodeDict[str(t)]
            codeWords += code + endCode
    codeWords = code_dc+codeWords
    return codeWords

huffmanEncodeMatrix = HuffmanEncode(huffmanCodeDict, qDctBlocks, huffmanCodeDict['E'])
# print(huffmanEncodeMatrix)

def DCDecode(dc_text):
    decoded_text_dc = []
    for i in range(len(dc_text)//8):
        character = int('0b'+dc_text[i*8:(i+1)*8],2)
        decoded_text_dc.append(character)
    return decoded_text_dc

def huffmanDecode (dictionary, ac_text):
    huffmanDecodeDict = {v: k for k, v in dictionary.items()}
    print(huffmanDecodeDict)
    current_code = ""
    decode_block = []
    decode_all = []
    
    counter = 0
    for bit in ac_text:
        current_code += bit
        if(current_code in huffmanDecodeDict):
            if huffmanDecodeDict[current_code] == 'E':
                zero_len = 63 - counter
                assert(zero_len <= 63)
                for i in range(zero_len):
                    decode_block.append(0)
                counter = 0
                current_code = ""
                decode_all.append(decode_block)
                decode_block = []
            else:
                character = huffmanDecodeDict[current_code]
                # print(character)
                decode_block.append(int(character))
                current_code = ""
                counter += 1

    return decode_all

dcDecodetest = DCDecode(huffmanEncodeMatrix[0:8*64*64])
# print (dcDecodetest)

huffmanDecodetest = huffmanDecode(huffmanCodeDict,huffmanEncodeMatrix[8*64*64:])
# print(huffmanDecodetest)
# print(huffmanDecodetest[0])

def dezigzag(List):
    n = int((len(List))**0.5)
    matrix = np.zeros([n,n],dtype=np.int16)
    index = 0
    for i in range(2*(n-1)): #Sum of row idx and columnx
        if i%2 ==0:
            for x in range(i,-1,-1): #逆序
                if (x <= n-1) and (i-x <= n-1):
                    #print("i=",i,x,i-x)
                    matrix[x,i-x] = List[index]
                    index=index + 1
        else:
            for x in range(0,i+1):
                if (x <= n-1) and (i-x <= n-1):
                    #print("i=",i,x,i-x)
                    matrix[x,i-x] = List[index]
                    index = index +1
    return matrix
# array = [dcDecodetest[0]] + huffmanDecodetest[0]
# print(array)
# testblock = dezigzag(array)
# print(testblock)
# print(qDctBlocks[0,0])
# print(type(testblock))
# print(type(qDctBlocks[0,0]))

# for i in range(row_8):
#     for j in range(col_8):
#         # print(dcDecodeList[i+j],acDecodeList[i+j])
#         zigzag = [dcDecodetest[i*row_8+j]] + huffmanDecodetest[i*row_8+j]
#         tmp = dezigzag(zigzag)
#         dct = qDctBlocks[i,j]
#         for s in range(8):
#             for t in range(8):
#                 if tmp[s,t] != dct[s,t]:
#                     print("ERROR at " + str((i,j)))


def RebuildBlocks(dcDecodeList, acDecodeList):
    blocks = np.zeros((row_8,col_8,8,8))
    for i in range(row_8):
        for j in range(col_8):
            # print(dcDecodeList[i+j],acDecodeList[i+j])
            zigzag = [dcDecodeList[i*row_8+j]] + acDecodeList[i*row_8+j]
            dct_b = dezigzag(zigzag) * Y_table
            blocks[i][j] = idct(idct(dct_b.T,norm = 'ortho').T,norm = 'ortho')
    return blocks

rebuiltBlocks = RebuildBlocks(dcDecodetest, huffmanDecodetest)



def RebuildPicture(rebuiltBlocks, YCbCrlayers):
    row = row_8 * 8
    col = col_8 * 8
    img = np.zeros((row,col,3))
    for i in range(row_8):
        for j in range(col_8):
            img[i*8:(i+1)*8,j*8:(j+1)*8,0] = rebuiltBlocks[i,j]
    img[:,:,1] = YCbCrlayers[:,:,1]
    img[:,:,2] = YCbCrlayers[:,:,2]
    return img

recoverd = RebuildPicture(rebuiltBlocks, ycbcr).astype(np.uint8)

cv2.imshow("recoverd YCbCr",recoverd)
cv2.waitKey(0)

# test code to see if the image converting to YCRCB is broken
bgr = cv2.cvtColor(recoverd, cv2.COLOR_YCrCb2BGR)
cv2.imshow("Restored RGB Image",bgr)
cv2.waitKey(0)
cv2.destroyAllWindows()