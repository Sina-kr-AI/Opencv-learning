import cv2

cap = cv2.VideoCapture("videos/mixkit-street-with-people-walking-at-dusk-3428-hd-ready.mp4")

ret,frame=cap.read()
frame_gray2=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
print(f"shape org frame: {frame.shape}")
print(f"shape gray frame: {frame_gray2.shape}")

while True:

    frame_gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    chanel1=frame[:,:,0]
    chanel2=frame[:,:,1]
    chanel3=frame[:,:,2]
    cv2.imshow('frame1',chanel1)
    cv2.imshow('frame2',chanel2)
    cv2.imshow('frame3',chanel3)

    key = cv2.waitKey(15) & 0xFF

    if key==ord('q'):
        break

    ret,frame=cap.read()


cap.release()
cv2.destroyAllWindows()