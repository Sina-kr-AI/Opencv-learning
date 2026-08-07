import cv2 

cam = cv2.VideoCapture(1)

ret,frame=cam.read()

while ret:

    flip_frame=cv2.flip(frame,0)
    gray=cv2.cvtColor(flip_frame,cv2.COLOR_BGR2GRAY)
    blur=cv2.GaussianBlur(gray,(5,5),0)
    ret,thresh=cv2.threshold(
        blur,
        120,
        255,
        cv2.THRESH_BINARY
    )

    
    cv2.imshow("webcam",flip_frame)
    cv2.imshow("thresh",thresh)

    key = cv2.waitKey(1) & 0xFF

    if key==ord('q'):
        break

    ret,frame=cam.read()

cam.release()
cv2.destroyAllWindows()