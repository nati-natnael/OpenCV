import cv2
import numpy as np

img = cv2.imread("C:\Users\Public\Pictures\Sample Pictures\Desert.jpg", cv2.IMREAD_UNCHANGED)
img2 = cv2.imread("C:\Users\Public\Pictures\Sample Pictures\Jellyfish.jpg", cv2.IMREAD_UNCHANGED)

img_cv_r = cv2.add(img, img2)
img_np_r = img + img2

# img[:,:,2] = 0
# border = 10
# b = cv2.copyMakeBorder(img, border, border, border, border, cv2.BORDER_CONSTANT)

cv2.imshow('image', img_np_r)
cv2.waitKey(0)
cv2.destroyAllWindows()