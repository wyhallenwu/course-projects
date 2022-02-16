# from PIL import Image
# image = Image.open('./NoNoise/1.png')
# print(len(image.split()))

import cv2 as cv
import numpy as np
img = cv.imread('./NoNoise/1.png')
print(img.shape)
image_color = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow("origin", img)
print(image_color.shape)
vec = np.array(img).flatten()
print(vec.shape)
print(vec)
cv.imshow("gray",image_color)
vec = np.array(image_color).reshape(1, -1)
print(vec.shape)
arr = np.array([1, 2, 3])
print(arr.shape)
cv.waitKey(0)
cv.destroyAllWindows()
