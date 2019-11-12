import pytesseract as ocr
from PIL import Image
import cv2
import numpy as np
 
img = cv2.imread('teste-basico.jpg',0)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# img = cv2.resize(img, (1000, 1000))
# size = np.size(img)
# skel = np.zeros(img.shape,np.uint8)
cv2.imshow("test", img)
cv2.waitKey(0)
#ret,img = cv2.threshold(img,150,255,cv2.THRESH_BINARY)

# element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
# done = False
 
# while( not done):
#     eroded = cv2.erode(img,element)
#     temp = cv2.dilate(eroded,element)
#     temp = cv2.subtract(img,temp)
#     skel = cv2.bitwise_or(skel,temp)
#     img = eroded.copy()
 
#     zeros = size - cv2.countNonZero(img)
#     if zeros==size:
#         done = True
 
#cv2.imshow("skel",skel)
#cv2.waitKey(0)

phrase = ocr.image_to_string(img, config='por')
print(phrase)