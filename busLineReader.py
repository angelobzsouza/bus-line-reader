# coding: utf-8
# Aux imports
import sys
import numpy as np

# Imports to manipulate images
import cv2
import pytesseract as pythonOcr

# Personal imports
import utils

# LOCAL ATTEMPTS
# Open Image
image = cv2.imread('images/'+sys.argv[1]);
image = cv2.resize(image, (912, 513))

# Get entire image proprieties
height, width, channels = image.shape

# crop image upper half
croppedImage = image[0:height/2, 0:width]

# Get croped image proprieties
croppedHeight, croppedWidth, croppedchannels = croppedImage.shape

# BINARY WITH ORANGE ATTEMPT
# Binarize image using orange pixels as parameter
binaryByOrangeImage = croppedImage
for i in range(0, croppedHeight):
    for j in range(0, croppedWidth):
        if croppedImage[i][j][0] < 200 and (croppedImage[i][j][1] > 10 or croppedImage[i][j][1] < 255) and croppedImage[i][j][2] > 200:
            binaryByOrangeImage[i][j] = [255, 255, 255]
        else:
            binaryByOrangeImage[i][j] = [0, 0, 0]

# Get line number
firstTryText = pythonOcr.image_to_string(binaryByOrangeImage)
lineNumber = utils.getLineNumber(firstTryText)

# Try to get line name
utils.trySpeakLineName(lineNumber, 'Binarização com laranja', False)

# BINARY WITH ORANGE AND OPEN ATTEMPT
# Morphologic transformations
kernel = np.ones((5, 5), np.uint8) 
dilatedBinaryByOrangeImage = cv2.dilate(binaryByOrangeImage, kernel, iterations=1)

# Get line number
secondTryText = pythonOcr.image_to_string(dilatedBinaryByOrangeImage)
lineNumber = utils.getLineNumber(secondTryText)

# Try to get line name
utils.trySpeakLineName(lineNumber, 'Expadir a imagem binaria com laranja', False)

# CLOUD ATTEMPTS
# BINARY WITH ORANGE ATTEMPT
# BINARY WITH ORANGE AND OPEN ATTEMPT
# BINARY WITH WHITE ATTEMPT
# BINARY WITH WHITE AND OPEN ATTEMPT
# NORMAL IMAGE ATTEMPT
