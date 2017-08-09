import cv2

cascade_dir = 'C:/Users/uc212807/PycharmProjects/OpenCV/HaarCascadeTrainer/haar_cascades/haarcascade_xml/'
cascade = 'cascade.xml'
face = cv2.CascadeClassifier(cascade_dir + cascade)

img = cv2.imread('C:/Users/uc212807/Desktop/test.jpg')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face.detectMultiScale(gray, 1.3, 10, 1, (25, 25))
for (x, y, w, h) in faces:
    img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

cv2.imshow('image', img)
# When everything done, release the capture
cv2.waitKey(0)
cv2.destroyAllWindows()
