from LearningOpenCV import opencv_logo
import cv2


img = cv2.imread("C:\Users\Public\Pictures\Sample Pictures\Desert.jpg", cv2.IMREAD_UNCHANGED)
opencv_logo(img, 350, 250)
cv2.imshow('image', img)
key_stroke = cv2.waitKey(0)
