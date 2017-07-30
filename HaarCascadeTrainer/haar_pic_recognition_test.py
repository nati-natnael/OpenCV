import cv2

cascade = 'hand_cascade.xml'
face = cv2.CascadeClassifier('haar_cascades/haarcascades_xml/' + cascade)

img = cv2.imread('C:/Users/Natnael/Desktop/FunnyPic_HAND.jpg')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face.detectMultiScale(gray, 1.3, 5)
for (x, y, w, h) in faces:
    img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)

cv2.imshow('image', img)
# When everything done, release the capture
cv2.waitKey(0)
cv2.destroyAllWindows()
