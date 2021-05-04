### CS270 Homework 2 README

任怡静 2018533144

#### Question 1

- Open `Q1_1.py` in the `Codes` folder
- **Environment**: Python 3.7 in Anaconda
- **Packages**: 
  - **OpenCv**, install by using `pip install opencv-contrib-python`
  - **Collections**: install by using `pip install collection`
  - **Scipy**: install by using `pip install scipy`
- **Execution and Operations**
  - **For Question 1.1, which is to compress lena.tiff and show the codewords and compressed image, do the following: **
    - Run code `python Q1_1.py "hw2_files/Q1/lena.tiff"`
      - The program will first pop out the original picture of lena.tiff, press **Enter** on keyboard to proceed the compression process, and the compressed and recovered image will appear, press **Enter** to close two pictures and see the compression ratios and other output information in the console. 
      - The program will output 3 files:
        - **code.txt**: the compressed image stored in bytes
        - **code_binary.txt**: the compressed image stored in bits
        - **DecompressedImage.tiff**: the recovered image from compressed codewords
  - **For Question 1.2, which is to add the watermark LOGO_CS270.mat to lena.tiff and compress the image, later extract watermark from compressed picture, do the following: **
    - Run code `python Q1_2.py -e "hw2_files\Q1\lena.tiff" "hw2_files\Q1\LOGO_CS270.mat"  `
      - The program will first pop out the original mat of the watermark, press **Enter** on keyboard to proceed the Encryption process, the Origin image and Encrypted image will appear successively when pressing **Enter**. Press **Enter** to end the encryption process.
      - The program will output 1 file:
        -  **EncrypetedImage.tiff**: the encrypted image with watermark
    - Run code `python Q1_1.py "EncryptedImage.tiff"` for the compression
    - Run code `python Q1_2.py -d "hw2_files\Q1\lena.tiff" "EncryptedImage.tiff"     `
      - The program will pop out the extracted watermark
      - The program will output 1 file:
        - **ExtractedWatermark.jpg**: the extracted watermark

#### Question 2

- There is an unfinished matlab version of stitching in `hw1_main.mlx` 
- Open `stitch_images.py` in the `Codes` folder
- **Environment**: Python 3.7
- **Packages**: OpenCv, install by using `pip install opencv-contrib-python==3.4.2.16`
- Run code `python stitch_images.py <NAME_OF_PIC_1> <NAME_OF_PIC_2>`
  - example: `python stitch_images.py "Homework1_images\q2\mc1\1.png"  "Homework1_images\q2\mc1\2.png"` to see picture result in **mc1**

#### Question 3

- Open `Q3.mlx` in the `Codes` folder
- Start the code to see the result on the right
- **Make sure the file path is correct**

