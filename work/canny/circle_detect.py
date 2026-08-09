import cv2

cam = cv2.VideoCapture(1)

if not cam.isOpened():
    print("Cam not found")

while True:

    ret,frame = cam.read()

    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)

    circles = cv2.HoughCircles(
        blur,
        cv2.HOUGH_GRADIENT,
        dp=1,
        minDist=50,
        param1=100,
        param2=30,
        minRadius=10,
        maxRadius=200
    )

    if circles is not None:
        circles = circles[0]
        for circle in circles:
            x,y,r = circle
            x = int(x)
            y = int(y)
            r = int(r)
            cv2.circle(
                frame,
                (x,y),
                r,
                (255,235,10),
                2
            )
            cv2.circle(
                frame,
                (x,y),
                3,
                (0,0,255),
                -1
            )

    cv2.imshow("cam",frame)

    key = cv2.waitKey(1) & 0xFF

    if key==ord('q'):
        print("cam stopped")
        break

cam.release()
cv2.destroyAllWindows()