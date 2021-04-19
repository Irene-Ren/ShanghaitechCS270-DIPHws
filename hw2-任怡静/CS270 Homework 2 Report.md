### CS270 Homework 1 Report

任怡静 2018533144

#### Question 1 Defogging and Fogging

- How do you implement your algorithm? Describe it by flow charts or words. (6 pts)

  - For Picture Defogging: 
    - First I use the CLAHE method, which will select a small unit to adjust locally rather than adjust the picture as a whole.
    - Then I use a white balance color correction to adjust a bit to make the picture's color not too over-saturated.
  - For Picture Fogging:
    - To implement the fogging effect, I use a line positioned at **m**, and calculate the distance between every points to this line, the nearer to **m**, the heavier the fog is and vice versa. 

- Describe implement details of your code. (6 pts)

  - For CLAHE:

    - Step 1: I pick a small unit of 32 * 32 pixels.
    - Step 2: Count the histogram in this unit, change the histogram to PDF of the intensity of this unit. And for the histogram bars that goes over **up bound**, I trim it to bound, and collect all the trimmed bars to integral them, then add the average of this integral to all bars. (see the figure below)
    - Step 3: Then I transform the PDF in step 2 into CDF.
    - Step 4: The output of this intensity is 255 * CDF.
    - Apply this to the R, G, B layers and iterate the unit through the whole picture.
    - <img src="D:\Rigin_Rain\Classes\CS270\hws\hw1\CLAHE.png" style="zoom:50%;" />

  - For white balance:

    - Step 1: Calculate the mean for R, G, B, gray layers' values individually, note them as **R_bar**, **G_bar**, **B_bar**, **I_bar**, which gray = 0.299 .* R + 0.587 .* G + 0.114 .* B

    - Step 2: Form a matrix as follows:

    - $$
      k \_ matrix = \left[ \matrix{  \frac{I \_ bar}{R \_ bar} & 0 & 0\\   0 & \frac{I \_ bar}{G \_ bar} & 0\\  0 & 0 & \frac{I \_ bar}{B \_ bar}  } \right]
      $$

    - Step 3: Calculate the cross product of **k_matrix** and the 1 * 3 [R, G, B] vector at all points on the picture, return the calculated picture matrix.

  - For  Fogging:

    - Input **m** indicate a focus, the intensity of the fog is only depending on the vertical distance of the picture pixel position **I(i, j, alpha)** and line **m**. **β** and **A** are coefficients that adjust the final effect of fog, making the fog look whiter and so on.

    - Step 1: Loop through the whole picture, use the calculations below to indicate ratio in specific positions, which the ratio will be deciding how much original value of the picture is saved at its position:

    - $$
      ratio = e^{-\beta * (-0.05 * |j-m| + 13)}
      $$

    - Step 2: Calculate the **output** by timing the ratio to the input picture matrix, to prevent the value overflows, we divide the original input matrix by 255. And then since the picture is now at a very low intensity (ratio < 1), we add a constant to make the fog white:

    - $$
      A * (1 - ratio(row, col))
      $$

    - Step 3: Output the result

- Results of defogging processing (like Fig. 1(b)). (9 pts)

  - ![](D:\Rigin_Rain\Classes\CS270\hws\hw1\Defogging_Result.png)

- Results of fogging processing (like Fig 2(b)). (9 pts)

  - ![](D:\Rigin_Rain\Classes\CS270\hws\hw1\Fogging_Result.png)

#### Question 2 Image stitching

- How do you extract features from the images? (3 pts) How do you match the features? (3 pts)
  - I use SIFT to extract features from images. 
  - The matching is pretty simple, just check for two sets of descriptors, for each points in one set, match it with the nearest Euclidean-distance point in the other set, and if the two sets contains the same matches, we save this match as a rough valid match.
- How do you detect the mismatches? (6 pts)
  - I use RANSAC like method for mismatch filtering. 
    - It will loop for 1000 times to see all the matched points whether their geometry distance is small enough to be fitful for a more delicate match. And it will break within 1000 times when the ratio of **thresh** matches are found.
    - When changing the picked matches, the algorithm will also change the homographic matrix correspondingly.
- Which transformation method do you use? How does it work? (8 pts)
  - I use Homography for transformations.
  - We need to find **h** to minimize the sum of the pair-points' distance after the transformation is applied. For selected pair points (at least four), substitute them into the equation below:
  - <img src="D:\Rigin_Rain\Classes\CS270\hws\hw1\Eq_homography_fitting.png" style="zoom:50%;" />
  - By the linear regression method, **h** is found to be the eigenvector of $A^TA$  corresponding to the smallest eigenvalue. 
  - The calculated result of a 3*3 matrix will be the transformation the image needs, this matrix includes scaling, distortion and rotation, apply it onto the image matrix, then we have two transformed pieces.
- Your matched features (like Fig 5). (4*2 pts)
  - This is the matching of the rough match process, I don't have the data structure after filtering with RANSAC, thus this may not be accurate for the final result
  - ![](D:\Rigin_Rain\Classes\CS270\hws\hw1\match_1.png)
  - ![](D:\Rigin_Rain\Classes\CS270\hws\hw1\match_2.png)
  - ![](D:\Rigin_Rain\Classes\CS270\hws\hw1\match_3.png)
  - ![](D:\Rigin_Rain\Classes\CS270\hws\hw1\match_4.png)
- Your matched result (like Fig 6 & Fig 7). (4*3pts)
  - run `python stitch_images.py <NAME_OF_PIC_1>  <NAME_OF_PIC_2>` to see the result
  - <img src="D:\Rigin_Rain\Classes\CS270\hws\hw1\stitch_1.png" style="zoom:80%;" />
  - <img src="D:\Rigin_Rain\Classes\CS270\hws\hw1\stitch_2.png" style="zoom:36%;" />
  - <img src="D:\Rigin_Rain\Classes\CS270\hws\hw1\stitch_3.png" style="zoom:46%;" />
  - <img src="D:\Rigin_Rain\Classes\CS270\hws\hw1\stitch_4.png" style="zoom:41%;" />

#### Question 3 Color Transfer Between Images

- Explain the transformation steps, and your coding implementation. (7 pts)

  - Explain transformation steps:

    - lαβ space's axes has rare correlations, thus transforming in lαβ space is safer than in RGB space
    - First transformation transform the RGB color space to LMS color space using specified matrices
    - The second transformation is to take the log values of LMS color space and transform it to lαβ space using specified matrices
    - Then the color correction:
      - First extract the "special" parts of the **source** image (doing this by subtracting each color axes in lαβ by each mean value in **source**), so that the shapes in **source** is reserved.
      - Transform each color axes in lαβ by timing the ratio of lαβ of **target** and lαβ of **source**. By doing this, the "special" parts of **source** has been transformed into the style of **target**
      - Add the mean value in **target** of lαβ axes to each color axis, at this time the new picture will contains the "special" parts of **source** and the color style of **target**
    - Then use the inverse specified matrix operation to revert to LMS, then RGB space to recover the new image in RGB space.

  - Coding implementation

    - For RGB transform lαβ space:

      - Step 1: initialize the following matrices

      - $$
        rgb2xyz = \left[ \matrix{ 0.5141 & 0.3239 & 0.1604\\   0.2651 & 0.6702 & 0.0641\\  0.0241 & 0.1288 & 0.8444  } \right] \\
        xyz2lms = \left[ \matrix{ 0.3897 & 0.6890 & -0.0787\\  -0.2298 & 1.1834 & 0.0464\\  0.0000 & 0.0000 & 1.0000  } \right]\\
        lms2lab \_1 = \left[ \matrix{ \frac{1}{\sqrt{3}} & 0 & 0\\  0 & \frac{1}{\sqrt{6}} & 0\\  0 & 0 & \frac{1}{\sqrt{2}} } \right]\\
        lms2lab \_2 = \left[ \matrix{ 1 & 1 & 1\\  1 & 1 & -2\\  1 & -1 & 0  } \right]\\
        $$

      - Step 2: Iterate through all the 1*3 RGB vectors at each position of the picture. Calculate the vector **temp** = xyz2lms * (rgb2xyz * rgb), and if one of the vector **temp** is 0, assign 0 to that dimension rather than assign it with log10(**temp(s)**)

    - For  Color Correction:

      - The inputs are: **input**, **reference**, and they are both lαβ space matrices, and **input** indicates **source**, **reference** indicates **target**
      - Step 1: First calculate the mean and deviation of three channels (l, α, β) for **input** and **reference**, mark them as L_bar, A_bar, B_bar, L_sdev, A_sdev, B_sdev; L_tbar, A_tbar, B_tbar, L_tdev, A_tdev, B_tdev
      - Step 2: For each layer of lαβ, calculate each positions' value **correction(row,col,lαβ)** = (L_tdev/L_sdev) .* (lαβ(i,j) - L_bar) + L_tbar;
      - Step 3: After the loop, return the **correction** as output.

    - For lαβ transform RGB space:

      - Step 1: initialize the following matrices

      - $$
        lms2rgb = \left[ \matrix{ 4.4679 & -3.5873 & 0.1193\\   -1.2186 & 2.3809 & -0.1624\\  0.0497 & -0.2439 & 1.2045  } \right] \\
        lms2lab \_1 = \left[ \matrix{ \frac{1}{\sqrt{3}} & 0 & 0\\  0 & \frac{1}{\sqrt{6}} & 0\\  0 & 0 & \frac{1}{\sqrt{2}} } \right]\\
        lms2lab \_2 = \left[ \matrix{ 1 & 1 & 1\\  1 & 1 & -2\\  1 & -1 & 0  } \right]\\
        $$

      - Step 2: Iterate through all the 1*3 lαβ vectors at each position of the picture. Calculate the vector rgb(row, col, RGB) = lms2rgb * 10^(lms2lab_2 * lms2lab_1 * lαβ(row, col, lαβ)) for all positions and get the result of RGB picture matrix

- The improvements you made to the algorithm. (3 pts)

  - There is a small modification in dealing with **temp** being 0, in the documentation, the hint suggested to add a small value to 0s in input RGB vectors, but it will cause some errors in the picture, causing some place to have purple dots. A better way is to judge after calculation, that is to say, to check after doing **temp** = xyz2lms * (rgb2xyz * rgb), assign 0 directly rather than doing logarithm calculation, it can avoid errors of infinity and make the pictures looks better. (Transfer result)
  - The color transfer result seems satisfying, not too bright or dark

- LAB color space image (like Fig 9). (2*2 pts)

  - ![](D:\Rigin_Rain\Classes\CS270\hws\hw1\Rgb2lab_Result.png)

- Component image of LAB (like Fig 10). (2*2 pts)

  - ![](D:\Rigin_Rain\Classes\CS270\hws\hw1\lab_Result.png)

- Result of your color transformation (like Fig 11). (2*2 pts)

  - ![](D:\Rigin_Rain\Classes\CS270\hws\hw1\ColorTransformation_Result.png)

- Result of your color transformation (like Fig 12). (2*2 pts)

  - ![](D:\Rigin_Rain\Classes\CS270\hws\hw1\ColorTransTwo_Result.png)

- Your selected images and color transfer results (4 pts). 

  - ![](D:\Rigin_Rain\Classes\CS270\hws\hw1\ColorTransSelf_Result.png)
  - Explanation
    - As we can see, the pictures (**source**) all changes to the color style of the other picture (**target**)
    - The **source** and **target** are all transformed to lαβ color space because there are barely correlation between the axes. Thus it is safer to do transform between two pictures and then revert **transformed source** back to RGB color space.
    - The main Idea is to find out the trait of the **source** picture and the color axes' value ratio between two pictures. The trait will leave the picture hold its shapes in place, and the ratio will adjust the **source** picture's color towards **target**. Thus the pictures(**source**) can transform to similar color style of other pictures(**target**).

