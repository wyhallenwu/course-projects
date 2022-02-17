import cv2

img = cv2.imread('./NoNoise/1.png')
cv2.imshow('test', img)
cv2.waitKey(0)
cv2.destroyAllWindows()