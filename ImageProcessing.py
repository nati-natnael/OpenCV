import numpy as np
import cv2

'''
Draw the openCV logo on provided image
'''
def opencv_logo(img, start_x, start_y):
    size = 200

    # gap between two circles
    gap = 10
    ellipse_major = int(size/3)
    ellipse_minor = ellipse_major

    ellipse_thickness = 50
    padding = 30

    # Triangle co-ordinates
    Vo = [start_x, start_y]
    Vi = [int(Vo[0]-(size*np.cos(np.pi/3))), int(Vo[1]+(size*np.sin(np.pi/3)))]
    Vii = [int(Vo[0] + (size * np.cos(np.pi/3))), int(Vo[1] + (size * np.sin(np.pi/3)))]

    pts = np.array([Vo, Vi, Vii], np.int32)

    print pts
    pts = pts.reshape((-1, 1, 2))

    # Drawing Circles
    elli_tuple = (ellipse_major, ellipse_minor)

    font = cv2.FONT_HERSHEY_SIMPLEX
    txt_start_x = (Vi[0] - size/10)
    txt_start_y = (Vi[1] + (size/2 - gap/2) + gap + ellipse_thickness)

    # logo outer
    rect_start_x = Vi[0] - ellipse_major - ellipse_thickness
    rect_start_y = Vo[1] - ellipse_minor - ellipse_thickness

    rect_size_x = Vi[0] + size + ellipse_major + ellipse_thickness
    rect_size_y = Vi[1] + size

    rect_start = (rect_start_x, rect_start_y)
    rect_size = (rect_size_x, rect_size_y)

    outer = cv2.rectangle(img, rect_start, rect_size, (185, 128, 41), cv2.FILLED)

    cv2.ellipse(outer, (Vo[0], Vo[1]), elli_tuple, 0, 0, 360, (0, 0, 255), ellipse_thickness)
    cv2.ellipse(outer, (Vi[0], Vi[1]), elli_tuple, 0, 0, 360, (0, 255, 0), ellipse_thickness)
    cv2.ellipse(outer, (Vii[0], Vii[1]), elli_tuple, 0, 0, 360, (255, 0, 0), ellipse_thickness)

    cv2.fillPoly(outer, [pts], (185, 128, 41))

    # has to be dependant on params
    cv2.putText(outer, 'OpenCV', (int(txt_start_x), int(txt_start_y)), font, 2, (255, 255, 255), 8, cv2.LINE_AA)

img = cv2.imread("C:\Users\Public\Pictures\Sample Pictures\Desert.jpg", cv2.IMREAD_UNCHANGED)
opencv_logo(img, 350, 250)
cv2.imshow('image', img)
key_stroke = cv2.waitKey(0)
#
# if key_stroke == ord('Q'):
#     cv2.destroyAllWindows()
# elif key_stroke == ord('s'):
#     img = cv2.imread("C:\Users\Public\Pictures\Sample Pictures\Penguins.jpg", cv2.IMREAD_UNCHANGED)
#     cv2.imshow('image', img)
#     cv2.waitKey(1000)
#     cv2.destroyAllWindows()


