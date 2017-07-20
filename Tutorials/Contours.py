import cv2
import numpy as np

# img = cv2.imread("..\\files\\square.jpg")

''' Finding contours of an image '''
# imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# ret, th = cv2.threshold(imgray, 127, 255, 0)
# image, contours, hierarchy = cv2.findContours(th, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# img = cv2.drawContours(img, contours, -1, (255, 0, 0), 5)

''' Calculating image properties '''
# cnt = contours[0]
# M = cv2.moments(cnt)
# print M
# print M['m00']  # Area

# perimeter = cv2.arcLength(cnt, True)
# print perimeter

# img = cv2.imread("..\\files\\star.png")

# imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# ret, th = cv2.threshold(imgray, 127, 255, 0)
# image, contours, hierarchy = cv2.findContours(th, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

# epsilon = 0.01 * cv2.arcLength(contours[1], True)
# approx = cv2.approxPolyDP(contours[1], epsilon, True)

# hull = cv2.convexHull(contours[1], returnPoints=True)
# k = cv2.isContourConvex(contours[1])
# print k

# img = cv2.drawContours(img, hull, -1, (255, 0, 0), 5)

img = cv2.imread("..\\files\\flash.png")

imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, th = cv2.threshold(imgray, 127, 255, 0)
image, contours, hierarchy = cv2.findContours(th, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

''' Fitting a rect on an image with no consideration to orientation of image '''
# x, y, w, h = cv2.boundingRect(contours[1])
# img = cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

''' Fiting Rect on an image considering the rotation '''
# rect = cv2.minAreaRect(contours[1])
# box = cv2.boxPoints(rect)
# box = np.int0(box)
# img = cv2.drawContours(img, [box], 0, (0, 255, 0), 2)

''' Fitting Circle on an image '''
# (x, y), r = cv2.minEnclosingCircle(contours[1])
# center = (int(x), int(y))
# radius = int(r)
# img = cv2.circle(img, center, radius, (255, 0, 0), 2)

''' Fitting an ellipse on an image '''
# ellipse = cv2.fitEllipse(contours[1])
# img = cv2.ellipse(img, ellipse, (0, 255, 0), 2)

''' Fitting a line on an image '''
rows, cols = img.shape[:2]
[vx, vy, x, y] = cv2.fitLine(contours[1], cv2.DIST_L2, 0, 0.01, 0.01)
lefty = int((-x*vy/vx) + y)
righty = int(((cols-x)*vy/vx) + y)
img = cv2.line(img, (cols-1, righty), (0, lefty), (0, 255, 0), 2)

'''Contour Properties'''


cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

