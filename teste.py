from PIL import Image
import pytesseract as ocr
import cv2
import sys
 
# Read image
img = cv2.imread('inteiro-distorcido.jpg')

# Get dimensions
height, width, channels = img.shape

# Binarizy image
for i in range(0, height):
    for j in range(0, width):
        if img[i][j][0] < 190 and (img[i][j][1] > 10 or img[i][j][1] < 255) and img[i][j][2] > 210:
            img[i][j] = [255, 255, 255]
        else:
            img[i][j] = [0, 0, 0]

cv2.imshow("binary Image", img)
cv2.waitKey(0)

# Try to read text
phrase = ocr.image_to_string(img)
print(phrase)
sys.exit(0)
