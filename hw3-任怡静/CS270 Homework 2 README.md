### CS270 Homework 2 README

任怡静 2018533144

#### Question 1

- **Environment**: Python 3.7 in Anaconda
- **Packages**: 
  - **OpenCv**, install by using `pip install opencv-contrib-python`
  - **Collections**: install by using `pip install collection`
  - **Scipy**: install by using `pip install scipy`
- **Execution and Operations**
  - **For Question 1.1, which is to compress lena.tiff and show the codewords and compressed image, do the following: **
    - Run code `python Q1_1.py "..\material\hw2_files\Q1\lena.tiff" "..\result\Q1\"`
      - The program will first pop out the original picture of lena.tiff, press **Enter** on keyboard to proceed the compression process, and the compressed and recovered image will appear, press **Enter** to close two pictures and see the compression ratios and other output information in the console. 
      - The program will output 3 files:
        - **code.txt**: the compressed image stored in bytes
        - **code_binary.txt**: the compressed image stored in bits
        - **DecompressedImage.tiff**: the recovered image from compressed codewords
  - **For Question 1.2, which is to add the watermark LOGO_CS270.mat to lena.tiff and compress the image, later extract watermark from compressed picture, do the following: **
    - Run code `python Q1_2.py -e "..\material\hw2_files\Q1\lena.tiff" "..\material\hw2_files\Q1\LOGO_CS270.mat" "..\result\Q1\"  `
      - The program will first pop out the original mat of the watermark, press **Enter** on keyboard to proceed the Encryption process, the Origin image and Encrypted image will appear successively when pressing **Enter**. Press **Enter** to end the encryption process.
      - The program will output 1 file:
        -  **EncrypetedImage.tiff**: the encrypted image with watermark
    - Run code `python Q1_1.py "..\result\Q1\EncryptedImage.tiff" "..\result\Q1\e-"` for the compression, the image is `e-DecompressedImage.tiff`
    - Run code `python Q1_2.py -d "..\material\hw2_files\Q1\lena.tiff" "..\result\Q1\e-DecompressedImage.tiff" "..\result\Q1\"     `
      - The program will pop out the extracted watermark
      - The program will output 1 file:
        - **ExtractedWatermark.jpg**: the extracted watermark

#### Question 2

- There are two sets of results in the result folder, the default one is the pre-defined matrix method
- **Environment**: Python 3.7 Anaconda
- **Packages**: 
  - **OpenCv**, install by using `pip install opencv-contrib-python`
  - **Scipy**: install by using `pip install scipy`
- **Executions and operations**
  - **For question 2.1**
    - Run code `python Q2_1.py`, if there are errors,check if the filepath in the file consistent with the system and file structure, change them manually.
    - If want to see the result of code matching picture, uncomment line 82 - line 86 and comment line 89, also remember to change line 106's name to `RegisterationResult_m.jpg` and line 135 's name to `BlendedImage_m.jpg`
  - **For question 2.2**
    - Run code `python Q2_2.py "..\material\hw2_files\Q2\target.jpeg" "..\material\hw2_files\Q2\source_background.JPG" "..\material\hw2_files\Q2\mask.jpg" "..\result\Q2\"`
    - If there is an error, check if the filepath in the file consistent with the system and file structure

#### Question 3

- Open `Q3.mlx` in the `code` folder
- Start the code to see the result on the right
- **Make sure the file path is correct**

