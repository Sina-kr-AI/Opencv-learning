import cv2

cap = cv2.VideoCapture("videos/mixkit-pedestrian-walk-in-tokyo-4231-hd-ready.mp4")

ret,frame=cap.read()

while True:
    frame_gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    cv2.imshow("video",frame_gray)

    key = cv2.waitKey(15) & 0xFF

    if key==ord('q'):
        break

    ret,frame=cap.read()

cap.release()
cv2.destroyAllWindows()