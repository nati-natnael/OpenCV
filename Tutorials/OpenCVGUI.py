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

    ellipse_thickness = size / 4

    # First Triangle co-ordinates
    Vi_o = [start_x, start_y]
    Vi_i = [int(Vi_o[0] - (size * np.cos(np.pi / 3))), int(Vi_o[1] + (size * np.sin(np.pi / 3)))]
    Vi_ii = [int(Vi_o[0] + (size * np.cos(np.pi / 3))), int(Vi_o[1] + (size * np.sin(np.pi / 3)))]

    first_pts = np.array([[Vi_o], [Vi_i], [Vi_ii]], np.int32)

    # Second Triangle co-ordinates
    Vii_o = [start_x + size, start_y]
    half_x = Vi_o[0] + (size - ((size * np.sin(np.pi / 3)) * np.cos(np.pi / 6)))
    half_y = Vi_o[1] + ((size * np.sin(np.pi / 3)) * np.sin(np.pi / 6))
    Vii_i = [int(half_x), int(half_y)]
    second_pts = np.array([[Vii_o], [Vi_ii], [Vii_i]], np.int32)

    # Drawing Circles
    elli_tuple = (ellipse_major, ellipse_minor)

    font = cv2.FONT_HERSHEY_SIMPLEX
    txt_start_x = (Vi_i[0] - (size + ellipse_thickness) / 3)
    txt_start_y = (Vi_i[1] + (size / 2) + gap * 2 + ellipse_thickness)

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


size = 1
clicked = False


# Mouse Callbacks
def draw_circle(event, x, y, flags, param):
    global size
    global clicked
    size = cv2.getTrackbarPos('Radius', 'image')

    r = cv2.getTrackbarPos('R', 'image')
    g = cv2.getTrackbarPos('G', 'image')
    b = cv2.getTrackbarPos('B', 'image')

    color = (b, g, r)

    if event == cv2.EVENT_LBUTTONDOWN:
        clicked = True
        cv2.circle(img, (x, y), size, color, -1)

    if event == cv2.EVENT_LBUTTONUP:
        clicked = False

    if event == cv2.EVENT_MOUSEMOVE and clicked:
        cv2.circle(img, (x, y), size, color, -1)


def nothing(x):
    pass


img = np.zeros((512, 512, 3), np.uint8)
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_circle)

cv2.createTrackbar('Radius', 'image', 1, 100, nothing)

cv2.createTrackbar('R', 'image', 0, 255, nothing)
cv2.createTrackbar('G', 'image', 0, 255, nothing)
cv2.createTrackbar('B', 'image', 0, 255, nothing)

while (True):
    cv2.imshow('image', img)
    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()
