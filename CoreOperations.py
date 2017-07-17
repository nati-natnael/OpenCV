import cv2
import numpy as np

img = cv2.imread("C:\Users\Public\Pictures\Sample Pictures\Desert.jpg", cv2.IMREAD_UNCHANGED)
# img2 = cv2.imread("C:\Users\Public\Pictures\Sample Pictures\Jellyfish.jpg", cv2.IMREAD_UNCHANGED)
logo = cv2.imread("C:\Users\Public\Pictures\Sample Pictures\opencv.png", cv2.IMREAD_UNCHANGED)

# img[:,:,2] = 0
# border = 10
# b = cv2.copyMakeBorder(img, border, border, border, border, cv2.BORDER_CONSTANT)

# img_cv_r = cv2.add(img, img2)
# img_np_r = img + img2

# res = cv2.addWeighted(img, 0.2, img2, 0.2, 0)

logo = cv2.cvtColor(logo, cv2.COLOR_RGBA2BGR)
rows, cols, channels = logo.shape
roi = img[0:rows, 0:cols]

roi_rows, roi_cols, roi_channels = roi.shape

img2gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
mask_inv = cv2.bitwise_not(mask)

img1_bg = cv2.bitwise_and(roi, roi, mask = mask_inv)
img2_fg = cv2.bitwise_and(logo, logo, mask = mask)

dst = cv2.add(img1_bg, img2_fg)
img[0:rows, 0:cols] = dst

cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()