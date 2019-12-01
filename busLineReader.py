# coding: utf-8
import sys
import os
import signal
import thread
import time
import io
import cv2
import numpy
import json
import pytesseract as pythonOcr
from google.cloud import vision
from google.cloud.vision import types

enableCloud = False

attemptsFail = 0
listnerLineFound = False
listnerLineWarned = False
running = True

#######################################################
##                      attempts                     ##
#######################################################

# Create google vision client
if (enableCloud):
	client = vision.ImageAnnotatorClient()
	print 'Cloud is enabled!'

def localAttempt (image, attemptName):
    imageString = pythonOcr.image_to_string(image)
    imageStrings = []
    imageStrings.append(imageString)
    checkLine(imageStrings, attemptName)
    print 'Fail attempt: '+attemptName
    setFail()

def cloudAttempt (image, imageName, attemptName):
    if (enableCloud):
        cv2.imwrite('tempImages/temp'+imageName+'.jpg', image)
        with io.open('tempImages/temp'+imageName+'.jpg', 'rb') as image_file:
            content = image_file.read()

        imageCloud = vision.types.Image(content=content)
        response = client.text_detection(image=imageCloud)
        imageStrings = getTextsDescriptions(response.text_annotations)
        checkLine(imageStrings, attemptName)
        print 'Fail attempt: '+attemptName
        setFail()

#######################################################
##                      utills                       ##
#######################################################

# Import lines
with open('jsons/lines.json') as linesFile:
    lines = json.load(linesFile)

# Work with text
def searchLine (lineNumber):
    try:
        lineName = lines[str(lineNumber)]
        if not checkLineAlredyFound():
            setLineFound()
            os.system("espeak -v pt -s 140 'A linha "+str(lineName)+" está se aproximando'")
            setLineWarned()
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

# Working with image
def openImage (path):
    image = cv2.imread('images/'+path);
    # Cut
    height, width, channels = image.shape
    croppedImage = image[0:height/2, 0:width]

    # Resize
    scalePercent = 40
    x = int(croppedImage.shape[1] * scalePercent / 100)
    y = int(croppedImage.shape[0] * scalePercent / 100)
    resizedImage = cv2.resize(croppedImage, (x, y))

    return resizedImage

def smoothingImage (image):
	kernel = numpy.ones((5,5),numpy.float32)/25
	# funcoes para suavização, usar 1 por vez
	image = cv2.filter2D(image,-1,kernel)
	#image = cv2.GaussianBlur(image,(5,5),0)
	#image = cv2.medianBlur(image,5)
	#image = cv2.bilateralFilter(image,9,75,75)
	return image

def unshiningImage (image):
	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	h, s, v = cv2.split(hsv)

	v[v < 50] = 0
	v[v >= 50] -= 50

	final_hsv = cv2.merge((h, s, v))
	image = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
	return image

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

# Work with threads
def listner():
    global attemptsFail
    while True:
        time.sleep(1)
        if listnerLineFound:
            finish()
            print attemptsFail

        if attemptsFail == 33:
            os.system("espeak -v pt -s 140 'Não foi possível identificar a linha'")
            finish()

def finish():
	global running
	running = False
	thread.exit()

def setFail():
	global attemptsFail
	attemptsFail = attemptsFail + 1

def setLineFound():
	global listnerLineFound
	listnerLineFound = True

def setLineWarned():
	global listnerLineWarned
	listnerLineWarned = True

def checkLineAlredyFound():
	return listnerLineFound


#######################################################
##                   busLineReader                   ##
#######################################################

def main():
    thread.start_new_thread(listner, ())

    # Abre a imagem
    image = openImage(sys.argv[1])
    # normal suavizada
    smoothedImage = smoothingImage(image)	
    # normal sem brilho
    unshinedImage = unshiningImage(image)
    # normal sem brilho suavisada
    unshinedSmoothedImage = smoothingImage(unshinedImage)

    ## ORANGE ##
    # binarizada normal 
    binaryOrange = binaryByOrange(image)
    # binarizada normal suavisada
    binaryOrangeSmoothed = binaryByOrange(smoothedImage)
    # binarizada normal dilatada
    binaryOrangeDilated = dilateBinary(binaryOrange, 5)
    # binarizada normal suavisada dilatada
    binaryOrangeSmoothedDilated = dilateBinary(binaryOrangeSmoothed, 5)

    # binarizada sem brilho
    unshinedBinaryOrange = binaryByOrange(unshinedImage)
    # binarizada sem brilho suavisada
    unshinedBinaryOrangeSmoothed = binaryByOrange(unshinedSmoothedImage)
    # binarizada sem brilho dilatada
    unshinedBinaryOrangeDilated = dilateBinary(unshinedBinaryOrange, 5)
    # binarizada sem brilho suavisada dilatada
    unshinedBinaryOrangeSmoothedDilated = dilateBinary(unshinedBinaryOrangeSmoothed, 5)

    ## WHITE ##
    # binarizada normal
    binaryWhite = binaryByWhite(image)
    # binarizada normal suavisada
    binaryWhiteSmoothed = binaryByWhite(smoothedImage)
    # binarizada normal dilatada
    binaryWhiteDilated = dilateBinary(binaryWhite, 5)
    # binarizada normal suavisada dilatada
    binaryWhiteSmoothedDilated = dilateBinary(binaryWhiteSmoothed, 5)

    # binarizada sem brilho
    unshinedBinaryWhite = binaryByWhite(unshinedImage)
    # binarizada sem brilho suavisada
    unshinedBinaryWhiteSmoothed = binaryByWhite(unshinedSmoothedImage)
    # binarizada sem brilho dilatada
    unshinedBinaryWhiteDilated = dilateBinary(unshinedBinaryWhite, 5)
    # binarizada sem brilho suavisada dilatada
    unshinedBinaryWhiteSmoothedDilated = dilateBinary(unshinedBinaryWhiteSmoothed, 5)

    ## LOCAL ATTEMPTS ##
    thread.start_new_thread(localAttempt,(binaryOrange, 'LOCAL: binarizada normal laranja'))
    thread.start_new_thread(localAttempt,(binaryOrangeSmoothed, 'LOCAL: binarizada normal suavisada laranja'))
    thread.start_new_thread(localAttempt,(binaryOrangeDilated, 'LOCAL: binarizada normal dilatada laranja'))
    thread.start_new_thread(localAttempt,(binaryOrangeSmoothedDilated, 'LOCAL: binarizada normal suavisada dilatada laranja'))
    thread.start_new_thread(localAttempt,(unshinedBinaryOrange, 'LOCAL: binarizada sem brilho laranja'))
    thread.start_new_thread(localAttempt,(unshinedBinaryOrangeSmoothed, 'LOCAL: binarizada sem brilho suavisada laranja'))
    thread.start_new_thread(localAttempt,(unshinedBinaryOrangeDilated, 'LOCAL: binarizada sem brilho dilatada laranja'))
    thread.start_new_thread(localAttempt,(unshinedBinaryOrangeSmoothedDilated, 'LOCAL: binarizada sem brilho suavisada dilatada laranja'))
    thread.start_new_thread(localAttempt,(binaryWhite, 'LOCAL: binarizada normal branca'))
    thread.start_new_thread(localAttempt,(binaryWhiteSmoothed, 'LOCAL: binarizada normal suavisada branca'))
    thread.start_new_thread(localAttempt,(binaryWhiteDilated, 'LOCAL: binarizada normal dilatada branca'))
    thread.start_new_thread(localAttempt,(binaryWhiteSmoothedDilated, 'LOCAL: binarizada normal suavisada dilatada branca'))
    thread.start_new_thread(localAttempt,(unshinedBinaryWhite, 'LOCAL: binarizada sem brilho branca'))
    thread.start_new_thread(localAttempt,(unshinedBinaryWhiteSmoothed, 'LOCAL: binarizada sem brilho suavisada branca'))
    thread.start_new_thread(localAttempt,(unshinedBinaryWhiteDilated, 'LOCAL: binarizada sem brilho dilatada branca'))
    thread.start_new_thread(localAttempt,(unshinedBinaryWhiteSmoothedDilated, 'LOCAL: binarizada sem brilho suavisada dilatada branca'))

    ## CLOUD ATTEMPTS ##
    if (enableCloud):
        thread.start_new_thread(cloudAttempt,(binaryOrange,'binaryOrange', 'CLOUD: binarizada normal laranja'))
        thread.start_new_thread(cloudAttempt,(binaryOrangeSmoothed,'binaryOrangeSmoothed', 'CLOUD: binarizada normal suavisada laranja'))
        thread.start_new_thread(cloudAttempt,(binaryOrangeDilated,'binaryOrangeDilated', 'CLOUD: binarizada normal dilatada laranja'))
        thread.start_new_thread(cloudAttempt,(binaryOrangeSmoothedDilated,'binaryOrangeSmoothedDilated', 'CLOUD: binarizada normal suavisada dilatada laranja'))
        thread.start_new_thread(cloudAttempt,(unshinedBinaryOrange,'unshinedBinaryOrange', 'CLOUD: binarizada sem brilho laranja'))
        thread.start_new_thread(cloudAttempt,(unshinedBinaryOrangeSmoothed,'unshinedBinaryOrangeSmoothed', 'CLOUD: binarizada sem brilho suavisada laranja'))
        thread.start_new_thread(cloudAttempt,(unshinedBinaryOrangeDilated,'unshinedBinaryOrangeDilated', 'CLOUD: binarizada sem brilho dilatada laranja'))
        thread.start_new_thread(cloudAttempt,(unshinedBinaryOrangeSmoothedDilated,'unshinedBinaryOrangeSmoothedDilated', 'CLOUD: binarizada sem brilho suavisada dilatada laranja'))
        thread.start_new_thread(cloudAttempt,(binaryWhite,'binaryWhite', 'CLOUD: binarizada normal branca'))
        thread.start_new_thread(cloudAttempt,(binaryWhiteSmoothed,'binaryWhiteSmoothed', 'CLOUD: binarizada normal suavisada branca'))
        thread.start_new_thread(cloudAttempt,(binaryWhiteDilated,'binaryWhiteDilated', 'CLOUD: binarizada normal dilatada branca'))
        thread.start_new_thread(cloudAttempt,(binaryWhiteSmoothedDilated,'binaryWhiteSmoothedDilated', 'CLOUD: binarizada normal suavisada dilatada branca'))
        thread.start_new_thread(cloudAttempt,(unshinedBinaryWhite,'unshinedBinaryWhite', 'CLOUD: binarizada sem brilho branca'))
        thread.start_new_thread(cloudAttempt,(unshinedBinaryWhiteSmoothed,'unshinedBinaryWhiteSmoothed', 'CLOUD: binarizada sem brilho suavisada branca'))
        thread.start_new_thread(cloudAttempt,(unshinedBinaryWhiteDilated,'unshinedBinaryWhiteDilated', 'CLOUD: binarizada sem brilho dilatada branca'))
        thread.start_new_thread(cloudAttempt,(unshinedBinaryWhiteSmoothedDilated,'unshinedBinaryWhiteSmoothedDilated', 'CLOUD: binarizada sem brilho suavisada dilatada branca'))
        thread.start_new_thread(cloudAttempt,(image, 'NormalImage', 'CLOUD: Imagem normal na cloud'))

    while True:
        if not running:
            time.sleep(2)
            sys.exit(0)

if __name__ == "__main__":
	sys.exit(main())
