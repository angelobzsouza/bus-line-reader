# coding: utf-8
import sys
import attempts
import os
import signal
import socket
import thread
import time
import utils
import io

attemptsFail = 0
listnerLineFound = False
listnerLineWarned = False
running = True

def listner():
	global attemptsFail
	while True:
		time.sleep(1)
		print 'ouvindo'
		if listnerLineFound:
			finish()
		print attemptsFail
		if attemptsFail == 7:
			os.system("espeak -v pt -s 140 'Não foi possível identificar a linha'")
			finish()

def finish():
	global running
	running = False
	thread.exit()

def setFail():
	global attemptsFail
	attemptsFail = attemptsFail + 1
	print attemptsFail	

def setLineFound():
	global listnerLineFound
	listnerLineFound = True

def setLineWarned():
	global listnerLineWarned
	listnerLineWarned = True

def checkLineAlredyFound():
	return listnerLineFound

def main():
	thread.start_new_thread(listner, ())

	image = utils.openImage(sys.argv[1])
	binaryOrangeImage = utils.binaryByOrange(image)
	binaryOrangeDilatedImage = utils.dilateBinary(binaryOrangeImage, 5)
	binaryWhiteImage = utils.binaryByWhite(image)
	binaryWhiteDilatedImage = utils.dilateBinary(binaryWhiteImage, 3)

	thread.start_new_thread(attempts.localAttempt,(binaryOrangeImage, 'Binarização com laranja'))
	thread.start_new_thread(attempts.localAttempt,(binaryOrangeDilatedImage, 'Dilatação e binarização por laranja'))
	thread.start_new_thread(attempts.cloudAttempt,(binaryOrangeImage, 'BinaryOrangeImage', 'Binarização com laranja na cloud'))
	thread.start_new_thread(attempts.cloudAttempt,(binaryOrangeDilatedImage, 'BinaryOrangeDilatedImage', 'Dilatação e binarização com laranja na cloud'))
	thread.start_new_thread(attempts.cloudAttempt,(binaryWhiteImage, 'BinaryWhiteImage', 'Binarização com branco na cloud'))
	thread.start_new_thread(attempts.cloudAttempt,(binaryWhiteDilatedImage, 'BinaryWhiteDiletedImage', 'Dilatação e binarização com branco na cloud'))
	thread.start_new_thread(attempts.cloudAttempt,(image, 'NormalImage', 'Imagem normal na cloud'))

	while True:
		if not running:
			time.sleep(2)
			sys.exit(0)

if __name__ == "__main__":
	sys.exit(main())


	