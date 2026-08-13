import cv2
import numpy as np

cv2.namedWindow("Threshold",cv2.WINDOW_NORMAL)
cv2.resizeWindow("Threshold",(500,300))
cv2.createTrackbar(
    "Threshold 1",
    "Threshold",
    0,
    255,
    lambda x: None
)
cv2.createTrackbar(
    "Threshold 2",
    "Threshold",
    0,
    255,
    lambda x: None
)
cv2.setTrackbarPos(
    "Threshold 1",
    "Threshold",
    100
)
cv2.setTrackbarPos(
    "Threshold 2",
    "Threshold",
    200
)

canvas = np.zeros((1,1,3),np.uint8)

cam = cv2.VideoCapture(1)

if not cam.isOpened():
    print("Cam not found")

while True:
    ret,frame = cam.read()

    if not ret:
        print("Frame not found")
        break

    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )

    blur = cv2.GaussianBlur(
        gray,
        (5,5),
        0
    )

    threshold1 = cv2.getTrackbarPos("Threshold 1","Threshold")
    threshold2 = cv2.getTrackbarPos("Threshold 2", "Threshold")

    edges = cv2.Canny(
        blur,
        threshold1,
        threshold2
    )

    contours,_ = cv2.findContours(
        edges,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    for contour in contours:
        area = cv2.contourArea(contour)
        if area < 1000:
            continue
        rect = cv2.minAreaRect(contour)
        (x,y),(w,h),angle = rect
        box = cv2.boxPoints(rect)
        box = np.intp(box)

        cv2.drawContours(
            frame,
            [box],
            0,
            (255,0,0),
            2
        )

    cv2.imshow("cam",frame)
    cv2.imshow("canny",edges)
    cv2.imshow("Threshold",canvas)

    key = cv2.waitKey(1) & 0xFF

    if key==ord('q'):
        print("stopped")
        break

cam.release()
cv2.destroyAllWindows()