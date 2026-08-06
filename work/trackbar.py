import cv2
import numpy as np

cv2.namedWindow("Trackbars",cv2.WINDOW_NORMAL)
cv2.resizeWindow("Trackbars",500,300)
cv2.createTrackbar(
    "Hue min",
    "Trackbars",
    0,
    180,
    lambda x:None
)
cv2.createTrackbar(
    "Hue max",
    "Trackbars",
    0,
    180,
    lambda x:None
)
cv2.createTrackbar(
    "Sat min",
    "Trackbars",
    0,
    255,
    lambda x:None
)
cv2.createTrackbar(
    "Sat max",
    "Trackbars",
    0,
    255,
    lambda x:None
)
cv2.createTrackbar(
    "Val min",
    "Trackbars",
    0,
    255,
    lambda x:None
)
cv2.createTrackbar(
    "Val max",
    "Trackbars",
    0,
    255,
    lambda x:None
)

canvas = np.zeros((1,1,3),np.uint8)
canvas[:]=235,235,235

while True:
    cv2.imshow("Trackbars",canvas)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
cv2.destroyAllWindows()