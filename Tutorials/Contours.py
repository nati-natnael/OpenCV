import cv2
import numpy as np

img = cv2.imread("..\\files\\white_square.jpg", cv2.COLOR_BGR2GRAY)
ret, th = cv2.threshold(img, 127, 255, 0)
image, contours, hierarcy = cv2.findContours(th, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

img = cv2.drawContours(img, contours, 0, (0,255,0), 3)

cv2.imshow('image', th)
cv2.waitKey(0)
cv2.destroyAllWindows()

