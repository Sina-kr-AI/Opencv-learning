import cv2

cam = cv2.VideoCapture(0)

ret,frame=cam.read()
print(frame.shape)
while True:
    frame_1=frame[:,:,0]
    cv2.imshow("webcam",frame_1)

    key = cv2.waitKey(15) & 0xFF

    if key==ord('q'):
        break

    ret,frame=cam.read()

cam.release()
cv2.destroyAllWindows()