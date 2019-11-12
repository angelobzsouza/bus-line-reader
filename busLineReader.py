from PIL import Image
import pytesseract as ocr
import cv2

# Open image
image = cv2.imread('teste-basico.jpg');

# Get image infos
height, width, channels = image.shape

# Cut image and get the superior part
cropedImage = image[0:height/2, 0:width]

# Try to read text
phrase = ocr.image_to_string(cropedImage, config='por')
print(phrase)