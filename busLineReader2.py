from PIL import Image
import pytesseract as ocr
import numpy as np
import cv2
import sys

# Open image
image = cv2.imread('teste-basico.jpg');

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
        if cropedImage[i][j][0] < 190 and (cropedImage[i][j][1] > 10 or cropedImage[i][j][1] < 255) and cropedImage[i][j][2] > 210:
            cropedImage[i][j] = [255, 255, 255]
        else:
            cropedImage[i][j] = [0, 0, 0]

cv2.imshow("binary Image", cropedImage)
cv2.waitKey(0)

# Try to read text
phrase = ocr.image_to_string(cropedImage)
print(phrase)
sys.exit(0)
