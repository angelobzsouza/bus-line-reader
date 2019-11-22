# coding: utf-8
from PIL import Image
import pytesseract as ocr
import numpy as np
import cv2
import sys
import os
import espeak

# Open image
image = cv2.imread(sys.argv[1]);

image = cv2.resize(image, (1080, 720))

# Get image infos
height, width, channels = image.shape

# Cut image and get the superior part
cropedImage = image[0:height/2, 0:width]

# Get image infos
height, width, channels = cropedImage.shape

# Create binary image selecting orange pixels
for i in range(0, height):
    for j in range(0, width):
        if cropedImage[i][j][0] < 200 and (cropedImage[i][j][1] > 10 or cropedImage[i][j][1] < 255) and cropedImage[i][j][2] > 200:
            cropedImage[i][j] = [255, 255, 255]
        else:
            cropedImage[i][j] = [0, 0, 0]

# Morphologic transformations
kernel = np.ones((5, 5), np.uint8) 
dilatedImage = cv2.dilate(cropedImage, kernel, iterations=1) 


# cv2.imshow("binary Image", dilatedImage)
# cv2.waitKey(0)

# Read text
lineName = ocr.image_to_string(dilatedImage)
print(lineName)
os.system("espeak -v pt -s 120 'A linha "+str(lineName)+" está se aproximando'")
sys.exit(0)
