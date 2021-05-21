### CS270 Homework 3 Report

任怡静 2018533144

#### Question 1: Graph Cut for Image Segmentation (50 points)

- Please describe your algorithms in words or flowcharts. (15’)
  - **The Seed Collecting**
    - This part used the OpenCv built-in functions to catch mouse operations to append coordinates to seed lists ( **foreground_seeds** and **background_seeds **) and illustrate seeds on image
    - The image size is adjusted for drawboards so that user can draw accurately
  - **The Cut Graph Algorithm**
    - I first calculate a graph from seeds obtained in the previous step, which assign 0 to background_seeds' corresponding coordinates in **graph**, 1 to foreground_seeds' and 0.5 for the rest.
    - Then according to the **graph**, I can construct the node list and edge list for **maxflow graph**. I append **node** (node_flatcoord, capacity_towards_source, capacity_towards_sink) into the **nodeList**, and **edge** (curr_index, neighbor_index, capacity) into the **edgeList**. It follows the rule that if the point in the **graph** is 1 then I append (node_flatcoord, 0, MAXIMUM), 0 append (node_flatcoord, MAXIMUM, 0) and (node_flatcoord, 0, 0)  to the rest. I calculate and append two edges into **edgeList** for each points in the **graph**, whose capacity using $\frac{1}{1+Euclidean(I(x,y), I(x+1,y))}$ and $\frac{1}{1+Euclidean(I(x,y), I(x,y+1))}$
    - Then I use built-in maxflow package to construct the graph **g** that first connect all nodes to source and sink, then for nodes which has edges to each other (have edge in **edgeList**) add edges between them. And do the maxflow() algorithm.
    - Then I obtain the mask that the foreground is valued 1 and background 0, so that I can generate the mask and overlays based on **g**.get_segment(index)
  - **The multi-segments division**
    - I reuse the cut graph algorithm. And to divide multiple parts, I create 4 lists to collect four kinds of seeds, select one to be the foreground and others combined to be the background, loop this procedure for all four lists as they all become once the foreground. Then I check the mask before filling in color to see if it is occupied by other colors before and only fill in the non-occupied parts.
    - I modified the GUI to fit for four kinds of seeds by pressing '1', '2', '3', '4' in the keyboard

- As shown in figure 1 you need to perform graph cut method to segment the foreground and background of the given image q1_1.jpeg. (15’)

  - First original image, second seed record image, third mask image, fourth mask-origin overlayed image

    <figure class="half">
        <img src="hw3_任怡静_2018533144\material\images\q1_2.jpeg" style="zoom:12%;" /><img src="hw3_任怡静_2018533144\result\Q1\SeedsOverlayed.jpeg" style="zoom:12%;" /><img src="hw3_任怡静_2018533144\result\Q1\Mask.jpeg" style="zoom:12%;" /><img src="hw3_任怡静_2018533144\result\Q1\PartitionOverlayed.jpeg" style="zoom:12%;" />
    </figure>

- Modify your graph cut program for multi-class segmentation. You need to segment the given image q1_2.jpeg to four parts, and show the segmentation results via transparent painting overlayed with the origin image as shown in Figure 2. (20’)

  - First original image, second seed record image, third masks image, fourth masks-origin overlayed image

    <figure class="half">
        <img src="hw3_任怡静_2018533144\material\images\q1_1.jpeg" style="zoom:100%;" /><img src="hw3_任怡静_2018533144\result\Q1\Multi_SeedsOverlayed.jpeg" style="zoom:100%;" /><img src="hw3_任怡静_2018533144\result\Q1\Multi_Masks.jpg" style="zoom:100%;" /><img src="hw3_任怡静_2018533144\result\Q1\Multi_PartitionsOverlayed.jpg" style="zoom:100%;" />
    </figure>


#### Question 2 Image Blending

- Overall illustration of the process you designed. (5')

  - 

    <figure class="half">
        <img src="hw2_files/Q2/girl.jpeg" style="zoom:50%;" /><img src="hw2_files/Q2/man.jpg" style="zoom:50%;" />
    </figure>

    <figure class="half">
        <img src="Results/Q2/RegisterationResult_m.jpg" style="zoom:50%;" /><img src="Results/Q2/BlendedImage_m.jpg" style="zoom:50%;" /><img src="Results/Q2/RegisterationResult_p.jpg" style="zoom:50%;" /><img src="Results/Q2/BlendedImage_p.jpg" style="zoom:50%;" />
    </figure>


  <figure class="half">
      <img src="Results/Q2/SetPosition.jpg" style="zoom:7%;" /><img src="Results/Q2/NonBlended.jpg" style="zoom:7%;" /><img src="Results/Q2/PossionBlending.jpg" style="zoom:7%;" />
  </figure>

