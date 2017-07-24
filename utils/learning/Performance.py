import cv2
import sys

img = cv2.imread("C:\Users\Public\Pictures\Sample Pictures\Desert.jpg", cv2.IMREAD_UNCHANGED)

# t1 = cv2.getTickCount()
# for i in xrange(5, 49, 2):
#     img = cv2.medianBlur(img, i)
# t2 = cv2.getTickCount()
#
# et = (t2 - t1) / cv2.getTickFrequency()
# print et


