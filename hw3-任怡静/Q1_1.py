import maxflow
import cv2
import numpy as np

drawing = False
mode = 1

default = 0.5
MAXIMUM = 114514

foreground = 1
background = 0

def ListContain(elemet, list):
    for i in list:
        if elemet == i:
            return True
    return False
def AddSeed(event, x,y,flags,param):
    global drawing, mode
    row,col = param[2],param[3]
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            if mode == 1:
                if not ListContain((x,y),param[0]):
                    if(x >=0 and x < col) and (y>=0 and y<row):
                        param[0].append((x, y))
                    cv2.circle(image,(x,y),1,(0,255,0),-1)
            else:
                if not ListContain((x,y),param[1]):
                    if(x >=0 and x < col) and (y>=0 and y<row):
                        param[1].append((x, y))
                    cv2.circle(image,(x,y),1,(0,0,255),-1)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        if mode == True:
            cv2.circle(image,(x,y),1,(0,255,0),-1)
        else:
            cv2.circle(image,(x,y),1,(0,0,255),-1)

def GetFlattenCoord(x,y,num_col):
    return y*num_col + x

def CreateGraph(col, fore_seeds, back_seeds):
    nodes = []
    edges = []
    graph = np.ones((row, col)) * default
    for x,y in back_seeds:
        graph[y - 1, x - 1] = 0
    for x,y in fore_seeds:
        graph[y - 1, x - 1] = 1
    
    for (y,x),value in np.ndenumerate(graph):
        if value == 1.0:
            nodes.append((GetFlattenCoord(x, y, col), 0, MAXIMUM))
        elif value == 0.0:
                nodes.append((GetFlattenCoord(x, y, col), MAXIMUM, 0))
        else:
            nodes.append((GetFlattenCoord(x, y, col), 0, 0))

    for (y, x), value in np.ndenumerate(graph):
        if y == row - 1 or x == col - 1:
            continue
        my_index = GetFlattenCoord(x, y, col)

        neighbor_index = GetFlattenCoord(x+1, y, col)
        g = 1 / (1 + np.sum(np.power(image[y, x] - image[y, x+1], 2)))
        edges.append((my_index, neighbor_index, g))

        neighbor_index = GetFlattenCoord(x, y+1, col)
        g = 1 / (1 + np.sum(np.power(image[y, x] - image[y+1, x], 2)))
        edges.append((my_index, neighbor_index, g))
    
    return nodes, edges
        
def Get2DCoord(index, num_col):
    return (index % num_col), (index // num_col)

def CutGraph(row, col, nodes, edges):
    segment_mask = np.zeros((row, col, 3))
    g = maxflow.Graph[float](len(nodes), len(edges))
    nodelist = g.add_nodes(len(nodes))

    for n in nodes:
        v,c1,c2 = n
        g.add_tedge(nodelist[v], c1, c2)
    for e in edges:
        v1,v2,c = e
        g.add_edge(v1, v2, c, c)
    flow = g.maxflow()

    for index in range(len(nodes)):
        if g.get_segment(index) == 1:
            x,y = Get2DCoord(index, col)
            segment_mask[y, x] = (0, 0, 255)
    return segment_mask
def ImageResize(img, ratio):
    row = img.shape[0]
    col = img.shape[1]
    ret = cv2.resize(img,(int(col*ratio),int(row*ratio)))
    return ret

if __name__ == "__main__":
    image = cv2.imread('images/q1_2.jpeg')
    ratio = 0.3
    image = ImageResize(image, ratio)
    showboard = image.copy()
    row, col, _ = image.shape

    
    seed_overlay = np.zeros((row, col))

    background_seeds = []
    foreground_seeds = []
    mouse_param = [foreground_seeds,background_seeds,row,col]

    cv2.namedWindow('image')
    cv2.setMouseCallback('image',AddSeed, mouse_param)

    while(1):
        cv2.imshow('image',image)

        k = cv2.waitKey(1) & 0xFF
        if k == ord('o'):
            mode = 1
        elif k == ord('b'):
            mode = 0
        elif k == 27:
            break
    nds, eds = CreateGraph(col,foreground_seeds,background_seeds)
    ovlay = CutGraph(row, col, nds, eds)
    result = cv2.addWeighted(np.uint8(showboard), 0.5, np.uint8(ovlay), 0.5, 0.1)

    cv2.imshow("aha", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()