from contextlib import closing

import cv2
import numpy as np

cv2.namedWindow("Trackbar")
cv2.resizeWindow("Trackbar",(500,300))
cv2.createTrackbar(
    "Hue min",
    "Trackbar",
    0,
    255,
    lambda x: None
)
cv2.createTrackbar(
    "Hue max",
    "Trackbar",
    0,
    255,
    lambda x: None
)
cv2.createTrackbar(
    "Sat min",
    "Trackbar",
    0,
    255,
    lambda x: None
)
cv2.createTrackbar(
    "Sat max",
    "Trackbar",
    0,
    255,
    lambda x: None
)
cv2.createTrackbar(
    "Val min",
    "Trackbar",
    0,
    255,
    lambda x: None
)
cv2.createTrackbar(
    "Val max",
    "Trackbar",
    0,
    255,
    lambda x: None
)
cv2.setTrackbarPos("Sat max","Trackbar",255)
cv2.setTrackbarPos("Val max","Trackbar",255)

canvas = np.zeros((1,1,3),np.uint8)

cam = cv2.VideoCapture(1)

if not cam.isOpened():
    print("Cam not found")

cam_width = cam.get(cv2.CAP_PROP_FRAME_WIDTH)
cam_height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)

alarm_zone_x1 = int(cam_width-(cam_width*0.8))
alarm_zone_x2 = int(cam_width*0.8)
alarm_zone_y1 = int(cam_height-(cam_height*0.8))
alarm_zone_y2 = int(cam_height*0.8)

in_zone = False

print(f"Width: {cam_width} | Height: {cam_height}\nx1: {alarm_zone_x1} x2: {alarm_zone_x2} | y1: {alarm_zone_y1} y2: {alarm_zone_y2}")

kernel = np.ones((5,5),np.uint8)

while True:
    ret,frame = cam.read()
    if not ret:
        print("Frame not found")
        break

    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    h_min = cv2.getTrackbarPos("Hue min","Trackbar")
    h_max = cv2.getTrackbarPos("Hue max", "Trackbar")
    s_min = cv2.getTrackbarPos("Sat min", "Trackbar")
    s_max = cv2.getTrackbarPos("Sat max", "Trackbar")
    v_min = cv2.getTrackbarPos("Val min", "Trackbar")
    v_max = cv2.getTrackbarPos("Val max", "Trackbar")

    lower = np.array([h_min,s_min,v_min])
    upper = np.array([h_max,s_max,v_max])

    mask = cv2.inRange(hsv,lower,upper)

    mask = cv2.erode(mask,kernel,iterations=1)
    mask = cv2.dilate(mask,kernel,iterations=2)

    opening = cv2.morphologyEx(
        mask,
        cv2.MORPH_OPEN,
        kernel
    )

    closing = cv2.morphologyEx(
        opening,
        cv2.MORPH_CLOSE,
        kernel
    )

    contours,_ = cv2.findContours(
        closing,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    for contour in contours:
        area = cv2.contourArea(contour)
        if area<1000:
            continue
        x,y,w,h = cv2.boundingRect(contour)
        cx = int(x+w/2)
        cy = int(y+h/2)
        cv2.rectangle(
            frame,
            (x,y),
            (x+w,y+h),
            (255,0,0),
            2
        )
        cv2.circle(
            frame,
            (cx,cy),
            3,
            (0,0,255),
            -1
        )
        if alarm_zone_x1<=cx<=alarm_zone_x2 and alarm_zone_y1<=cy<=alarm_zone_y2:
            in_zone = True
        else:
            in_zone = False
        if in_zone:
            cv2.rectangle(
                frame,
                (10,10),
                (50,50),
                (0,0,255),
                -1
            )
        else:
            cv2.rectangle(
                frame,
                (10,10),
                (50,50),
                (0,255,0),
                -1
            )

    cv2.rectangle(
        frame,
        (alarm_zone_x1, alarm_zone_y1),
        (alarm_zone_x2, alarm_zone_y2),
        (235, 255, 10),
        2
    )

    cv2.imshow("Webcam",frame)
    cv2.imshow("Mask",closing)

    key = cv2.waitKey(1) & 0xFF

    if key==ord('q'):
        break
    if key==ord('s'):
        print(f"Hue min: {h_min} | Sat min: {s_min} | Val min: {v_min}\nHue max: {h_max} | Sat max: {s_max} | Val max: {v_max}")

cam.release()
cv2.destroyAllWindows()