import numpy as np
import cv2

'''
Draw the openCV logo on provided image
'''


def opencv_logo(img, start_x, start_y):
    size = 200

    # gap between two circles
    gap = 10
    ellipse_major = int(size / 3)
    ellipse_minor = ellipse_major

    ellipse_thickness = 50

    # First Triangle co-ordinates
    Vi_o = [start_x, start_y]
    Vi_i = [int(Vi_o[0] - (size * np.cos(np.pi / 3))), int(Vi_o[1] + (size * np.sin(np.pi / 3)))]
    Vi_ii = [int(Vi_o[0] + (size * np.cos(np.pi / 3))), int(Vi_o[1] + (size * np.sin(np.pi / 3)))]

    first_pts = np.array([[Vi_o], [Vi_i], [Vi_ii]], np.int32)

    # Second Triangle co-ordinates
    Vii_o = [start_x+size, start_y]
    half_x = Vi_o[0] + (size - ((size * np.sin(np.pi / 3)) * np.cos(np.pi / 6)))
    half_y = Vi_o[1] + ((size * np.sin(np.pi / 3)) * np.sin(np.pi / 6))
    Vii_i = [int(half_x), int(half_y)]
    second_pts = np.array([[Vii_o], [Vi_ii], [Vii_i]], np.int32)

    # Drawing Circles
    elli_tuple = (ellipse_major, ellipse_minor)

    font = cv2.FONT_HERSHEY_SIMPLEX
    txt_start_x = (Vi_i[0] - (size + ellipse_thickness) / 3)
    txt_start_y = (Vi_i[1] + (size/2) + gap*2 + ellipse_thickness)

    # logo outer
    rect_start_x = Vi_i[0] - ellipse_major - ellipse_thickness
    rect_start_y = Vi_o[1] - ellipse_minor - ellipse_thickness

    rect_size_x = Vi_i[0] + size + ellipse_major + ellipse_thickness
    rect_size_y = Vi_i[1] + size + gap

    rect_start = (rect_start_x, rect_start_y)
    rect_size = (rect_size_x, rect_size_y)

    outer = cv2.rectangle(img, rect_start, rect_size, (185, 128, 41), cv2.FILLED)

    # Drawing outer circles
    cv2.ellipse(outer, (Vi_o[0], Vi_o[1]), elli_tuple, 0, 0, 360, (0, 0, 255), ellipse_thickness)
    cv2.ellipse(outer, (Vi_i[0], Vi_i[1]), elli_tuple, 0, 0, 360, (0, 255, 0), ellipse_thickness)

    cv2.fillPoly(outer, [first_pts], (185, 128, 41))

    # Drawing Circle with Different orientation
    cv2.ellipse(outer, (Vi_ii[0], Vi_ii[1]), elli_tuple, 0, 0, 360, (255, 0, 0), ellipse_thickness)
    cv2.fillPoly(outer, [second_pts], (185, 128, 41))

    # has to be dependant on params
    cv2.putText(outer, 'OpenCV', (int(txt_start_x), int(txt_start_y)), font, 3, (255, 255, 255), 8, cv2.LINE_AA)


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
