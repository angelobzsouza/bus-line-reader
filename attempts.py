# coding: utf-8
import pytesseract as pythonOcr
import utils
import cv2
import io

from google.cloud import vision
from google.cloud.vision import types

# Create google vision client
client = vision.ImageAnnotatorClient()

def localAttempt (image, attemptName):
    imageString = pythonOcr.image_to_string(image)
    imageStrings = []
    imageStrings.append(imageString)
    utils.checkLine(imageStrings, attemptName)
    print 'Fail attempt: '+attemptName

def cloudAttempt (image, imageName, attemptName):
    cv2.imwrite('tempImages/temp'+imageName+'.jpg', image)
    with io.open('tempImages/temp'+imageName+'.jpg', 'rb') as image_file:
        content = image_file.read()

    imageCloud = vision.types.Image(content=content)
    response = client.text_detection(image=imageCloud)
    imageStrings = utils.getTextsDescriptions(response.text_annotations)
    utils.checkLine(imageStrings, attemptName)
    print 'Fail attempt: '+attemptName
