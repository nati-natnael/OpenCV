import cv2
import numpy as np

# cap = cv2.VideoCapture()
#
# while True:
#     try:
#         # get each frame
#         ret, frame = cap.read()
#
#         # Convert BGR to HSV
#         hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#
#         # Define range of blue color in HSV
#         lower_blue = np.array([110, 50, 50])
#         upper_blue = np.array([130, 255, 255])
#
#         # Threshold the HSV image to get only blue colors
#         mask = cv2.inRange(hsv, lower_blue, upper_blue)
#
#         # Bitwise-AND mask and original image
#         res = cv2.bitwise_and(frame, frame, mask=mask)
#
#         cv2.imshow('frame', frame)
#         cv2.imshow('mask', mask)
#         cv2.imshow('res', res)
#
#         key = cv2.waitKey(5) & 0xFF
#         if key == 27:
#             break
#     except Exception:
#         print("Oops!")
#         break

img = cv2.imread("C:\Users\Public\Pictures\Sample Pictures\\threshold.jpg", 0)

# img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# img = cv2.medianBlur(img, 5)

# ret,th = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

blur = cv2.GaussianBlur(img, (5, 5), 0)
th = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 25, 2)

# ret2, th2 = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#
# blur = cv2.GaussianBlur(img, (5, 5), 0)
# ret3, th3 = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

cv2.imshow('image', th)
cv2.waitKey(0)
cv2.destroyAllWindows()
