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
cv2.createTrackbar(
    "epsilon",
    "Threshold Trackbar",
    0,
    100,
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
cv2.setTrackbarPos(
    "epsilon",
    "Threshold Trackbar",
    20
)

canvas = np.zeros((1,1,3),np.uint8)

cam = cv2.VideoCapture(1)

shape = None

while True:
    ret,frame = cam.read()

    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray,(5,5),0)

    threshold1 = cv2.getTrackbarPos("Threshold 1","Threshold Trackbar")
    threshold2 = cv2.getTrackbarPos("Threshold 2","Threshold Trackbar")

    edges = cv2.Canny(blur,threshold1,threshold2)
    contours,_ = cv2.findContours(
        edges,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    cv2.drawContours(
        frame,
        contours,
        -1,
        (0,255,0),
        2
    )

    for contour in contours:
        area = cv2.contourArea(contour)
        if area < 1000:
            continue
        x,y,w,h = cv2.boundingRect(contour)
        perimeter = cv2.arcLength(
            contour,
            True
        )

        e = cv2.getTrackbarPos("epsilon","Threshold Trackbar")
        epsilon = (e/1000)*perimeter

        approx = cv2.approxPolyDP(
            contour,
            epsilon,
            True
        )

        corners = len(approx)

        ratio = w/h

        if corners==3:
            shape = "Triangle"
        elif corners==4:
            if 0.9<=ratio<=1.2:
                shape = "Square"
            else:
                shape = "Rectangle"
        elif corners==5:
            shape = "Pentagon"
        elif corners==6:
            shape = "Hexagon"
        else:
            shape = "Unknown"

        if shape is not None:
            cv2.putText(
                frame,
                shape,
                (10,30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,255,235),
                2
            )

        cv2.drawContours(
            frame,
            [approx],
            -1,
            (255,0,0),
            2
        )

    cv2.imshow("webcam",frame)
    cv2.imshow("edges",edges)
    cv2.imshow("Threshold Trackbar",canvas)

    key = cv2.waitKey(1) & 0xFF

    if key==ord('q'):
        break

cam.release()
cv2.destroyAllWindows()