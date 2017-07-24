import cv2
import numpy as np

img = cv2.imread("C:\Users\Public\Pictures\Sample Pictures\\threshold.png", 0)

laplacian = cv2.Laplacian(img, cv2.CV_64F)
sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)

cv2.imshow('image', laplacian)
cv2.waitKey(0)
cv2.destroyAllWindows()

