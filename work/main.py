import cv2

cap = cv2.VideoCapture("videos/mixkit-pedestrian-walk-in-tokyo-4231-hd-ready.mp4")

ret,frame = cap.read()

if not ret:
    print("couldnt read the frame")

n = 1


while True:

    cv2.imshow("video",frame)

    key = cv2.waitKey(15) & 0xFF

    if key==ord('q'):
        print("video stoped")
        break
    if key==ord('s'):
        path = f"output/image{n}.jpg"
        cv2.imwrite(path,frame)
        print(path)
        n+=1

    ret,frame=cap.read()

cap.release()
cv2.destroyAllWindows()