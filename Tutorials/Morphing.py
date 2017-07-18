import cv2
import numpy as np

img = cv2.imread("C:\Users\Public\Pictures\Sample Pictures\\j.png", cv2.IMREAD_UNCHANGED)

kernel = np.ones((5, 5), np.uint8)

# erosion = cv2.erode(img, kernel, iterations=1)

# dilation = cv2.dilate(img, kernel, iterations=1)

# opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

# closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

# gradient = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)

# top_hat = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)

black_hat = cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, kernel)

# Rectangular Kernel
cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

# Elliptical Kernel
cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

# Cross-shaped Kernel
cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))

cv2.imshow('image', black_hat)
cv2.waitKey(0)
cv2.destroyAllWindows()
