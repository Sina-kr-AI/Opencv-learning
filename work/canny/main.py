import cv2
import numpy as np

cv2.namedWindow("Threshold Trackbar",cv2.WINDOW_NORMAL)
cv2.resizeWindow("Threshold Trackbar",500,20)
cv2.createTrackbar(
    "Threshold 1",
    "Threshold Trackbar",
    0,
    255,
    lambda x: None
)
cv2.createTrackbar(
    "Threshold 2",
    "Threshold Trackbar",
    0,
    255,
    lambda x: None
)

cv2.setTrackbarPos(
    "Threshold 1",
    "Threshold Trackbar",
    50
)

cv2.setTrackbarPos(
    "Threshold 2",
    "Threshold Trackbar",
    150
)

canvas = np.zeros((1,1,3),np.uint8)

cam = cv2.VideoCapture(1)

while True:
    ret,frame = cam.read()

    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray,(5,5),0)

    threshold1 = cv2.getTrackbarPos("Threshold 1","Threshold Trackbar")
    threshold2 = cv2.getTrackbarPos("Threshold 2","Threshold Trackbar")

    edges = cv2.Canny(blur,threshold1,threshold2)

    cv2.imshow("webcam",frame)
    cv2.imshow("edges",edges)
    cv2.imshow("Threshold Trackbar",canvas)

    key = cv2.waitKey(1) & 0xFF

    if key==ord('q'):
        break

cam.release()
cv2.destroyAllWindows()