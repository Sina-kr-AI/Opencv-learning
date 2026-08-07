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

cam = cv2.VideoCapture(1)

ret,frame=cam.read()

fps = cam.get(cv2.CAP_PROP_FPS)

kernel = np.ones((5,5),np.uint8)

while True:
    if not ret:
        break

    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    h_min = cv2.getTrackbarPos("Hue min","Trackbars")
    h_max = cv2.getTrackbarPos("Hue max","Trackbars")
    s_min = cv2.getTrackbarPos("Sat min","Trackbars")
    s_max = cv2.getTrackbarPos("Sat max","Trackbars")
    v_min = cv2.getTrackbarPos("Val min","Trackbars")
    v_max = cv2.getTrackbarPos("Val max","Trackbars")

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

    contours,_=cv2.findContours(
        closing,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    ) 
    for contour in contours:
        area=cv2.contourArea(contour)
        if area<1000:
            continue
        x,y,w,h= cv2.boundingRect(contour)
        cv2.rectangle(
            frame,
            (x,y),
            (x+w,y+h),
            (255,0,0),
            2
        )
        cx = int(x+w/2)
        cy = int(y+h/2)
        cv2.circle(
            frame,
            (cx,cy),
            6,
            (0,0,255),
            -1
        )
    cv2.putText(
        frame,
        f"FPS: {fps}",
        (10,30),
        cv2.FONT_HERSHEY_COMPLEX,
        fontScale=1,
        color=(255,255,255),
        thickness=1,
        lineType=cv2.LINE_AA
    )

    cv2.imshow("webcam",frame)
    cv2.imshow("mask",closing)
    cv2.imshow("Trackbars",canvas)

    key = cv2.waitKey(1) & 0xFF

    if key==ord('q'):
        break
    if key==ord('s'):
        print(f"Hue min: {h_min} | Sat min: {s_min} | Val: {v_min}\nHue max: {h_max} | Sat max: {s_max} | Val max: {v_max}")

    ret,frame = cam.read()

cam.release()
cv2.destroyAllWindows()