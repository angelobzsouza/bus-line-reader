# coding: utf-8
import os
import sys
import json
import cv2

# Import lines
with open('lines.json') as linesFile:
    lines = json.load(linesFile)

def trySpeakLineName (lineNumber, attemptName, lastAttempt):
    try:
        lineName = lines[str(lineNumber)]
        os.system("espeak -v pt -s 140 'A linha "+str(lineName)+" está se aproximando'")
        sys.exit(0)
    except Exception as e:
        if (not lastAttempt):
            os.system("espeak -v pt -s 140 'A tentativa "+str(attemptName)+" falhou, continuando processamento'")
        else: 
            os.system("espeak -v pt -s 140 'Infelizmente, não foi possível obter o nome da linha'")
            sys.exit(0)

def getLineNumber (strings):
    lineNumber = ""
    lineStrings = strings.split('\n')

    for lineString in lineStrings:
        if (lineNumber != ""):
            return lineNumber
        
        for i in range(0 , int(len(lineString))):
            if (lineString[i] == "0"
                or lineString[i] == "1"
                or lineString[i] == "2"
                or lineString[i] == "3"
                or lineString[i] == "4"
                or lineString[i] == "5"
                or lineString[i] == "6"
                or lineString[i] == "7"
                or lineString[i] == "8"
                or lineString[i] == "9"
                or lineString[i] == "/"):
                lineNumber += lineString[i]
            elif (lineNumber != ""):
                return lineNumber
    
    return lineNumber

def showImage (image):
    cv2.imshow("Imagem", image)
    cv2.waitKey(0)