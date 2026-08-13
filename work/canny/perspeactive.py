import cv2
import numpy as np

points = []

def mouse_event(event,x,y,flags,param):
    global points
    if event==cv2.EVENT_LBUTTONDOWN:
        if len(points) < 4:
            points.append((x,y))
            print(f"Points: {points}")

def order_points(points):

    pts = np.array(points,dtype=np.float32)
    result = np.zeros((4,2),dtype=np.float32)

    result[0] = pts[np.argmin(pts.sum(axis=1))]
    result[2] = pts[np.argmax(pts.sum(axis=1))]
    result[1] = pts[np.argmin(np.diff(pts,axis=1))]
    result[3] = pts[np.argmax(np.diff(pts,axis=1))]

    return result

cam = cv2.VideoCapture(1)

if not cam.isOpened():
    print("Cam not found")

cv2.namedWindow("Webcam")
cv2.setMouseCallback(
    "Webcam",
    mouse_event
)

while True:
    ret,frame = cam.read()
    if not ret:
        print("Frame not found")
        break

    display = frame.copy()

    for i,point in enumerate(points):
        cv2.circle(
            display,
            point,
            6,
            (0,0,255),
            -1
        )
        cv2.putText(
            display,
            str(i+1),
            (point[0]+10,point[1]),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.8,
            color=(0,255,0),
            thickness=2
        )

    if len(points)==4:
        src = order_points(points)

        width = 500
        height = 300

        dst = np.array([
            [0,0],
            [width,0],
            [width,height],
            [0,height]
        ],
        dtype=np.float32
        )

        matrix = cv2.getPerspectiveTransform(src,dst)
        warped = cv2.warpPerspective(
            frame,
            matrix,
            (width,height)
        )

        cv2.imshow("Warped",warped)

    cv2.imshow("Webcam",display)

    key = cv2.waitKey(1) & 0xFF

    if key==ord('q'):
        break
    if key==ord('r'):
        points = []
        cv2.destroyWindow("Warped")
        print("Points resset")

cam.release()
cv2.destroyAllWindows()