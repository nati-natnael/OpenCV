import cv2

img = cv2.imread("C:\Users\Public\Pictures\Sample Pictures\Desert.jpg", cv2.IMREAD_UNCHANGED)
cv2.imshow('image', img)
key_stroke = cv2.waitKey(0)

if key_stroke == ord('Q'):
    cv2.destroyAllWindows()
elif key_stroke == ord('s'):
    img = cv2.imread("C:\Users\Public\Pictures\Sample Pictures\Penguins.jpg", cv2.IMREAD_UNCHANGED)
    cv2.imshow('image', img)
    cv2.waitKey(1000)
    cv2.destroyAllWindows()