# coding: utf-8
import json
import cv2
import numpy
import os
import sys

# Import lines
with open('jsons/lines.json') as linesFile:
    lines = json.load(linesFile)

# Work with text
def searchLine (lineNumber):
    try:
        lineName = lines[str(lineNumber)]
        os.system("espeak -v pt -s 140 'A linha "+str(lineName)+" está se aproximando'")
        sys.exit(0)
    except Exception as e:
        return False

def getLineNumber (string):
    lineNumber = ""
    subStrings = string.split('\n')

    for subString in subStrings:
        if (lineNumber != ""):
            return lineNumber
        
        for i in range(0 , int(len(subString))):
            if (subString[i] == "0"
                or subString[i] == "1"
                or subString[i] == "2"
                or subString[i] == "3"
                or subString[i] == "4"
                or subString[i] == "5"
                or subString[i] == "6"
                or subString[i] == "7"
                or subString[i] == "8"
                or subString[i] == "9"
                or subString[i] == "/"):
                lineNumber += subString[i]
            elif (subString[i] == "B"):
                lineNumber += "8"
            elif (lineNumber != ""):
                return lineNumber
    
    return lineNumber

def checkLine (strings, attemptName):
    for string in strings:
        lineNumber = getLineNumber(string)
        searchLine(lineNumber)

def getTextsDescriptions (texts):
    descriptions = []
    for text in texts:
        descriptions.append(text.description)

    return descriptions

# Work with image
def openImage (path):
    image = cv2.imread('images/'+path);
    image = cv2.resize(image, (912, 513))
    height, width, channels = image.shape
    croppedImage = image[0:height/2, 0:width]

    return croppedImage

def binaryByOrange (image):
    height, width, channels = image.shape
 
    binaryImage = image.copy()
    for i in range(0, height):
        for j in range(0, width):
            if image[i][j][0] < 100 and image[i][j][1] > 60 and image[i][j][1] < 170 and image[i][j][2] > 150:
                binaryImage[i][j] = [255, 255, 255]
            else:
                binaryImage[i][j] = [0, 0, 0]

    return binaryImage

def binaryByWhite (image):
    height, width, channels = image.shape

    binaryImage = image.copy()
    for i in range(0, height):
        for j in range(0, width):
            if image[i][j][0] > 200 and image[i][j][0] > 200 and image[i][j][2] > 200:
                binaryImage[i][j] = [255, 255, 255]
            else:
                binaryImage[i][j] = [0, 0, 0]

    return binaryImage

def dilateBinary (binaryImage, kernelSize):
    kernel = numpy.ones((kernelSize, kernelSize), numpy.uint8) 
    dilatedImage = cv2.dilate(binaryImage, kernel, iterations=1)

    return dilatedImage

def showImage (image):
    cv2.imshow("Imagem", image)
    cv2.waitKey(0)