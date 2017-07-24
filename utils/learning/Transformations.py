import cv2
import numpy as np

img = cv2.imread("C:\Users\Public\Pictures\Sample Pictures\\threshold.jpg", cv2.IMREAD_UNCHANGED)
rows, cols, channels = img.shape

# res = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

# M = np.float32([[1, 0, 0], [0, 1, 0]])
# res = cv2.warpAffine(img, M, (cols, rows))

# M = cv2.getRotationMatrix2D((cols/2, rows/2), 90, 1)
# res = cv2.warpAffine(img, M, (cols, rows))

# pts1 = np.float32([[50, 50], [200, 50], [50, 200]])
# pts2 = np.float32([[10, 100], [200, 50], [100, 250]])
# M = cv2.getAffineTransform(pts1, pts2)
# res = cv2.warpAffine(img, M, (cols, rows))

pts1 = np.float32([[36, 45], [262, 37], [20, 273], [275, 276]])
pts2 = np.float32([[0, 0], [cols, 0], [0, rows], [cols, rows]])

# cv2.line(img, (36, 45), (262, 37), (0, 255, 0), 2)
# cv2.line(img, (36, 45), (20, 273), (0, 255, 0), 2)
# cv2.line(img, (275, 276), (20, 273), (0, 255, 0), 2)
# cv2.line(img, (275, 276), (262, 37), (0, 255, 0), 2)

M = cv2.getPerspectiveTransform(pts1, pts2)
res = cv2.warpPerspective(img, M, (cols, rows))

cv2.imshow('image', res)
cv2.waitKey(0)
cv2.destroyAllWindows()
