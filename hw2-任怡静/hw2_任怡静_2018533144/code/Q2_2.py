import scipy.sparse
import numpy as np
import cv2
from scipy.sparse.linalg import spsolve
import sys
def MaskIndicies(mask):
    nonzeros = np.nonzero(mask)
    indices = []
    for i in range(len(nonzeros[0])):
        indices.append((nonzeros[0][i], nonzeros[1][i]))
    return indices
def GetSurrounding(index, pic_col):
    i,j = index
    return [(i,j+pic_col),(i,j-pic_col),(i,j+1),(i,j-1)]

def CommonLaplacianMatrix(bg_row, bg_col):
    laplacianDiagPart = scipy.sparse.lil_matrix((bg_col, bg_col))
    laplacianDiagPart.setdiag(4)
    laplacianDiagPart.setdiag(-1, -1)
    laplacianDiagPart.setdiag(-1, 1)
        
    laplacianMatrix = scipy.sparse.block_diag([laplacianDiagPart] * bg_row).tolil()
    
    laplacianMatrix.setdiag(-1, bg_col)
    laplacianMatrix.setdiag(-1, -1*bg_col)
    
    return laplacianMatrix

def PossionBlending(source, target, mask, offset):
    # shape of mask and source is same as shape of background.
    bg_row, bg_col, _ = target.shape
    
    mat_A = CommonLaplacianMatrix(bg_row, bg_col)
    laplacian = mat_A.tocsc()

    # The regions that the not in the mask, we reset the laplacian
    # if taking the laplacian, the point will have a 4 in this position and four -1 in the same row at k+1,k-1,k+col,k-col
    # If do not take laplacian, set 4 back to 1 and others to 0
    for r in range(1, bg_row - 1):
        for c in range(1, bg_col - 1):
            if mask[r, c] == 0:
                k = c + r * bg_col
                mat_A[k, k] = 1
                for s in GetSurrounding((k,k), bg_col):
                    mat_A[s[0],s[1]] = 0

    mat_A = mat_A.tocsc()

    mask_flat = mask.flatten()
    for alpha in range(3):
        source_flat = source[:, :, alpha].flatten()
        target_flat = target[:, :, alpha].flatten()        
        
        # inside the mask
        # print(laplacian.shape)
        mat_b = laplacian.dot(source_flat)
        # print(mat_b.shape)

        # outside the mask:
        for i in range(len(mask_flat)):
            if mask_flat[i] == 0:
                mat_b[i] = target_flat[i]
        
        blendedSource = spsolve(mat_A, mat_b)
        blendedSource = blendedSource.reshape((bg_row, bg_col))

        for i in range(bg_row):
            for j in range(bg_col):
                if blendedSource[i, j] > 255:
                    blendedSource[i, j] = 255
                if blendedSource[i, j] < 0:
                    blendedSource[i, j] = 0
        blendedSource = np.uint8(blendedSource)

        target[0:bg_row, 0:bg_col, alpha] = blendedSource

    return target
def ImageResize(img, ratio):
    row = img.shape[0]
    col = img.shape[1]
    ret = cv2.resize(img,(int(col*ratio),int(row*ratio)))
    return ret
if __name__ == "__main__":
    src_path = sys.argv[1]
    tgt_path = sys.argv[2]
    mask_path = sys.argv[3]
    result_path = sys.argv[4]
    
    source = cv2.imread(src_path)
    target = cv2.imread(tgt_path)
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE) 

    ratio = 0.2
    source = ImageResize(source, ratio)
    target = ImageResize(target, ratio)
    mask = ImageResize(mask, ratio)
    
    bg_row,bg_col, _ = target.shape
    offset = (100,400)
    
     # position mask and source to the offset position
    M = np.float32([[1,0,offset[0]],[0,1,offset[1]]])
    source = cv2.warpAffine(source,M,(bg_col,bg_row))
    mask = cv2.warpAffine(mask,M,(bg_col,bg_row))
    cv2.imshow("SetPosition",source)
    cv2.imwrite(result_path + "SetPosition.jpg", ImageResize(source, 1/ratio))
    print("PRESS ENTER TO PROCEED")
    cv2.waitKey(0)

    unblendedImg = target
    for i in range(bg_row):
        for j in range(bg_col):
            if mask[i,j] != 0:
                unblendedImg[i,j] = source[i,j]
    cv2.imshow("NonBlended", unblendedImg)
    cv2.imwrite(result_path + "NonBlended.jpg", ImageResize(unblendedImg, 1/ratio))
    print("PRESS ENTER TO PROCEED")
    cv2.waitKey(0)

    result = PossionBlending(source, target, mask, offset)

    cv2.imshow("PossionBlending", result)
    cv2.imwrite(result_path + "PossionBlending.jpg", ImageResize(result,1/ratio))
    print("PRESS ENTER TO PROCEED")
    cv2.waitKey(0)
    cv2.destroyAllWindows()