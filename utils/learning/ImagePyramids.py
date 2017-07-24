import cv2
import numpy as np

A = cv2.imread("..\\files\\apple.jpg")
B = cv2.imread("..\\files\\orange.jpg")

# generate Gaussian pyramid for A
G = A.copy()
gpA = [G]
for i in xrange(6):
    G = cv2.pyrDown(G)
    gpA.append(G)

# generate Gaussian pyramid for B
G = B.copy()
gpB = [G]
for i in xrange(6):
    G = cv2.pyrDown(G)
    gpB.append(G)

# generate Laplacian Pyramid for A
lpA = [gpA[5]]
for i in xrange(5, 0, -1):
    GE = cv2.pyrUp(gpA[i])
    print gpA[i]
    # L = cv2.subtract(gpA[i-1], GE)
    # lpA.append(L)

# generate Laplacian Pyramid for B
lpB = [gpB[5]]
for i in xrange(5,0,-1):
    GE = cv2.pyrUp(gpB[i])
#     L = cv2.subtract(gpB[i-1],GE)
#     lpB.append(L)

# cv2.imshow('image', gpA[0])
# cv2.waitKey(0)
# cv2.destroyAllWindows()