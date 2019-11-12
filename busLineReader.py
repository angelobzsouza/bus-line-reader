from PIL import Image
import pytesseract as ocr
import numpy as np
import cv2
import sys

# Open image
image = cv2.imread('letreiro-pequeno-distorcido.png');
#image = cv2.resize(image, (1920, 1080))
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Get image infos
height, width = image.shape

# Cut image and get the superior part
#cropedImage = image[0:height/2, 0:width]

# Filter
kernel = np.ones((7,7), np.float32)/25
filtredImage = cv2.filter2D(image, -1, kernel)

cv2.imshow("filtred Image", filtredImage)
cv2.waitKey(0)

# Create binary image
ret, binaryImage = cv2.threshold(filtredImage, 240, 255, cv2.THRESH_BINARY_INV)

cv2.imshow("binary Image", binaryImage)
cv2.waitKey(0)

# Trying otsu binary
#blur = cv2.GaussianBlur(cropedImage,(11,11),0)
#ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#cv2.imshow("otsu Image", th3)
#cv2.waitKey(0)

# Try to read text
phrase = ocr.image_to_string(binaryImage)
print(phrase)
sys.exit(0)
