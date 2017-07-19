import cv2
import numpy as np

img = cv2.imread("..\\files\\apple.jpg", cv2.IMREAD_UNCHANGED)
img = cv2.pyrDown(img)
img = cv2.pyrDown(img)

edges = cv2.Canny(img, 100, 200)

cv2.imshow('image', edges)
cv2.waitKey(0)
cv2.destroyAllWindows()