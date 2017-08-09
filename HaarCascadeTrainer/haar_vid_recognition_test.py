import cv2

cascade_dir = 'C:/Users/uc212807/PycharmProjects/OpenCV/HaarCascadeTrainer/haar_cascades/haarcascade_xml/'
cascade = 'cascade.xml'
face = cv2.CascadeClassifier(cascade_dir + cascade)

cap = cv2.VideoCapture('C:/Users/uc212807/Desktop/test_2.mp4')

while cap.isOpened():
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face.detectMultiScale(gray, 1.3, 30, 1, (25, 25))
    for (x, y, w, h) in faces:
        img = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]

    # Display the resulting frame
    frame = cv2.resize(frame, (500, 500))
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
