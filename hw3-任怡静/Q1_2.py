import maxflow
import cv2
import numpy as np

drawing = False
mode = 0

default = 0.5
MAXIMUM = 114514

foreground = 1
background = 0

back_colors = [(138,80,58),(139,143,31),(97,200,92),(0,255,255)]
colors = [(255,20,0),(0,255,0),(0,0,255),(0,255,255)]

def ListContain(elemet, list):
    for i in list:
        if elemet == i:
            return True
    return False
def AddSeed(event, x,y,flags,param):
    global drawing, mode
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            if not ListContain((x,y),param[mode]):
                if(x >=0 and x < col) and (y>=0 and y<row):
                    param[mode].append((x, y))
                cv2.circle(image,(x,y),1,colors[mode],-1)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.circle(image,(x,y),1,colors[mode],-1)

def GetFlattenCoord(x,y,num_col):
    return y*num_col + x
def ProduceForeBackList(param, i):
    foreground_seeds = param[i]
    background_seeds = []
    for s in range(len(param)):
        if s != i:
            for t in param[s]:
                if not ListContain(t,background_seeds):
                    background_seeds.append(t)
    return foreground_seeds, background_seeds

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

def CutGraph(row, col, nodes, edges, colorType):
    
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
            if segment_mask[y,x] == 0:
                segment_mask[y, x] = colorType
def ImageResize(img, ratio):
    row = img.shape[0]
    col = img.shape[1]
    ret = cv2.resize(img,(int(col*ratio),int(row*ratio)))
    return ret

if __name__ == "__main__":
    image = cv2.imread('images/q1_1.jpeg')
    ratio = 2
    image = ImageResize(image, ratio)
    showboard = image.copy()
    row, col, _ = image.shape

    
    seed_overlay = np.zeros((row, col))

    seeds_pack0 = []
    seeds_pack1 = []
    seeds_pack2 = []
    seeds_pack3 = []
    mouse_param = [seeds_pack0,seeds_pack1,seeds_pack2,seeds_pack3]
    cv2.namedWindow('image')
    cv2.setMouseCallback('image',AddSeed, mouse_param)

    while(1):
        cv2.imshow('image',image)

        k = cv2.waitKey(1) & 0xFF
        if k >= ord('1') and k <= ord('4'):
            mode = k-ord('1')
            print("marker ",mode)
        elif k == 27:
            break
    segment_mask = np.zeros((row, col), dtype=int)
    for i in range(len(colors)):
        foreground_seeds, background_seeds = ProduceForeBackList(mouse_param, i)
        nds, eds = CreateGraph(col, foreground_seeds, background_seeds)
        CutGraph(row, col, nds, eds, i)
    ovlay = np.zeros((row, col, 3))
    mask = np.zeros((row, col, 3))
    for i in range(row):
        for j in range(col):
            ovlay[i,j] = colors[segment_mask[i,j]]
            mask[i,j] = back_colors[segment_mask[i,j]]
    
    mask = ImageResize(mask, 1.0/ratio)
    cv2.imshow("Segmented mask", np.uint8(mask))
    cv2.imwrite("segmented_mask.jpg", np.uint8(mask))
    result = cv2.addWeighted(np.uint8(showboard), 0.5, np.uint8(ovlay), 0.5, 0.1)
    result = ImageResize(result, 1.0 / ratio)
    cv2.imshow("Overlayed result", result)
    cv2.imwrite("overlayed_result.jpg", np.uint8(result))
    cv2.waitKey(0)
    cv2.destroyAllWindows()