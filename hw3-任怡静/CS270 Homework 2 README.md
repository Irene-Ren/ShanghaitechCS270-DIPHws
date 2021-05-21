### CS270 Homework 3 README

任怡静 2018533144

#### Question 1

- **Environment**: Python 3.7 in Anaconda
- **Packages**: 
  - **OpenCv (4.5.1.48)**, install by using `pip install opencv-contrib-python`
  - **Maxflow (1.2.13)**: install by using `pip install PyMaxflow`
  - **Numpy**: install by using `pip install numpy`
- **Execution and Operations**
  - **For Question 1.1 the binary partition: **
    - Run code `python Q1_1.py "..\material\images\q1_2.jpeg" "..\result\Q1\"`, if there are errors,check if the filepath in the file consistent with the system and file structure, change them manually.
      - The program will pop out the 1/3* size (the image is too large for screen, the result will be recovered to original size before saving) of the original image as the seed collecting drawboard, **press 'o' on keyboard for selection of foreground, press 'b' for selection of background**, once mode selected, drag on image to sketch the seeds. 
      - The program will output 3 files:
        - **SeedsOverlayed.jpeg**: the record of your seed sketch on the original image
        - **Mask.jpeg**: the mask of foreground and background, foreground in red and background in black
        - **PartitionOverlayed.jpeg**: the overlay of the original image and the mask
  - **For Question 1.2 the multi-region partition: **
    - Run code `python Q1_2.py "..\material\images\q1_1.jpeg" "..\result\Q1\"`, if there are errors,check if the filepath in the file consistent with the system and file structure, change them manually.
      - The program will pop out the 2* size (for better drawing accuracy, the result will be recovered to original size before saving) of the original image as the seed collecting drawboard, **press '1' to '4' on keyboard for selection of different regions**, once mode selected, drag on image to sketch the seeds. 
      - The program will output 3 files:
        - **Multi_SeedsOverlayed.jpeg**: the record of your seed sketch on the original image
        - **Multi_Masks.jpeg**: the mask of each region, dark blue for region **'1'**, greenish-blue for region **'2'**, green for region **'3'**, and yellow for region **'4'** (for color harmony the colors are different from the overlay masks' colors)
        - **Multi_PartitionsOverlayed.jpeg**: the overlay of the original image and the masks

#### Question 2

- **Environment**: Python 3.7 Anaconda
- **Packages**: 
  - **OpenCv (4.5.1.48)**, install by using `pip install opencv-contrib-python`
  - **Numpy**: install by using `pip install numpy`
- **Executions and operations**
  - Run code `python Q2.py "..\material\images\q2.jpeg" "..\result\Q2\"`, if there are errors,check if the filepath in the file consistent with the system and file structure, change them manually.
    - The program will pop out the original image, press **Enter** to continue. Then the program will output the **illustrations of large canals and small canals** that has green and red marks to canals (this will not be saved, just for visual understanding), at this time the actual $I_b$ will be shown. Press **Enter** to close the two illustrations and get the two actual $I_l$ and $I_s$ along with the $I_b$ in last step, press **Enter** to close the rest images and get the element-wised summation $\sum_{i\in {I_\epsilon}}I_{\epsilon}(i)$ in the console
    - The program will output 3 files:
      - **Background.jpeg**: the extracted background image, the canal places are black
      - **Large.jpeg**: the extracted large canals along with background image, the small canal places are black
      - **Small.jpeg**: the extracted small canals along with background image, the large canal places are black

