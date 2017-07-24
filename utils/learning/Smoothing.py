import cv2
import numpy as np

img = cv2.imread("C:\Users\Public\Pictures\Sample Pictures\\opencv.png", cv2.COLOR_RGBA2BGR)

# kernel = np.ones((5, 5), np.float32)/10
# dst = cv2.filter2D(img, -1, kernel)

# dst = cv2.blur(img, (5, 5))

# dst = cv2.GaussianBlur(img, (5, 5), 0)

# dst = cv2.medianBlur(img, 3)

dst = cv2.bilateralFilter(img, 9, 75, 75)

cv2.imshow('image', dst)
cv2.waitKey(0)
cv2.destroyAllWindows()