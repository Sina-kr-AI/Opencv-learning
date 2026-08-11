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
    print("Cam not found!!")

while True:
    ret,frame = cam.read()
    if not ret:
        print("Frame not available!!!")
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
        threshold1=threshold1,
        threshold2=threshold2
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
        x,y,w,h = cv2.boundingRect(contour)
        width = w
        height = h
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"]/M["m00"])
            cy = int(M["m01"]/M["m00"])
        else:
            continue
        cv2.rectangle(
            frame,
            (x,y),
            (x+w,y+h),
            (0,255,0),
            1
        )
        cv2.putText(
            frame,
            f"W: {width} | H: {height}",
            (x,y+10),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1,
            color=(0,0,255),
            thickness=1
        )
        cv2.putText(
            frame,
            f"Area: {area}",
            (x,y-10),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1,
            color=(0,0,255),
            thickness=1
        )
        cv2.putText(
            frame,
            f"({x},{y})",
            (x-10,y),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1,
            color=(0,0,255),
            thickness=1
        )
        cv2.putText(
            frame,
            f"({x+w},{y+h})",
            (x+w+10,y+h),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1,
            color=(0, 0, 255),
            thickness=1
        )
        cv2.putText(
            frame,
            f"({cx},{cy})",
            (x + w,y-20),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1,
            color=(0, 0, 255),
            thickness=1
        )
        cv2.circle(
            frame,
            (cx,cy),
            radius=2,
            color=(255,0,0),
            thickness=-1
        )

    cv2.imshow("Webcam",frame)
    cv2.imshow("edges",edges)
    cv2.imshow("Threshold",canvas)

    key = cv2.waitKey(1) & 0xFF

    if key==ord('q'):
        print("Cam stopped")
        break

cam.release()
cv2.destroyAllWindows()