import cv2
import numpy as np

img = cv2.imread("..\\files\\square.jpg")

imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, th = cv2.threshold(imgray, 127, 255, 0)
image, contours, hierarchy = cv2.findContours(th, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

img = cv2.drawContours(img, contours, 1, (0, 255, 0), 5)
#
# cnt = contours[0]
# M = cv2.moments(cnt)
# print M
# print M['m00']  # Area

# perimeter = cv2.arcLength(cnt, True)
# print perimeter

cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

