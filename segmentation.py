from skimage.color import rgb2gray
import numpy as np
import cv2
import matplotlib.pyplot as plt
from scipy import ndimage

image = plt.imread('letreiro-pequeno-distorcido.jpg')
image.shape

gray = rgb2gray(image)

gray_r = gray.reshape(gray.shape[0]*gray.shape[1])
print(len(gray_r))
for i in range(gray_r.shape[0]):
    if gray_r[i] > gray_r.mean():
        gray_r[i] = 3
    elif gray_r[i] > 0.5:
        gray_r[i] = 2
    elif gray_r[i] > 0.25:
        gray_r[i] = 1
    else:
        gray_r[i] = 0
gray_reshape = gray_r.reshape(gray.shape[0],gray.shape[1])


#detecting edges

# defining the sobel filters
sobel_horizontal = np.array([np.array([1, 2, 1]), np.array([0, 0, 0]), np.array([-1, -2, -1])])
#print(sobel_horizontal, 'is a kernel for detecting horizontal edges')
 
sobel_vertical = np.array([np.array([-1, 0, 1]), np.array([-2, 0, 2]), np.array([-1, 0, 1])])
#print(sobel_vertical, 'is a kernel for detecting vertical edges')

kernel_laplace = np.array([np.array([1, 1, 1]), np.array([1, -8, 1]), np.array([1, 1, 1])])
#print(kernel_laplace, 'is a laplacian kernel')

out_h = ndimage.convolve(gray, sobel_horizontal, mode='reflect')
out_v = ndimage.convolve(gray, sobel_vertical, mode='reflect')
out_l = ndimage.convolve(gray, kernel_laplace, mode='reflect')

plt.imsave("laplace.jpg", out_l)
plt.imsave("reshape.jpg", gray_reshape)