import cv2 
import numpy as np

color_dict={
    "red":[[0,120,70],[10,255,255],[170,120,70],[180,255,255]],
    "green":[[35,50,50],[85,255,255]],
    "blue":[[100,155,50],[140,255,255]],
    "yellow":[[20,100,100],[35,255,255]],
    "orange":[[10,100,100],[20,255,255]],
    "purple":[[140,50,50],[170,255,255]]
}

def_color = "red"

cam = cv2.VideoCapture(1)

if not cam.isOpened():
    print("Cam not found!!!!")

w = cam.get(cv2.CAP_PROP_FRAME_WIDTH)
h = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
fps = cam.get(cv2.CAP_PROP_FPS)

print(f"Width: {w} | Height: {h} | FPS: {fps}")
print("Def color is red.\nPress keyboard for change color\nRed: r | Green: g | Blue: b | Yellow: y | Orange: o | Purple: p")

ret,frame = cam.read()

while ret:

    flip_frame=cv2.flip(frame,0)
    hsv = cv2.cvtColor(flip_frame,cv2.COLOR_BGR2HSV)

    if def_color=="red":
        lower_1 = np.array(color_dict[def_color][0])
        upper_1 = np.array(color_dict[def_color][1])
        lower_2 = np.array(color_dict[def_color][2])
        upper_2 = np.array(color_dict[def_color][3])
        mask_1 = cv2.inRange(hsv,lower_1,upper_1)
        mask_2 = cv2.inRange(hsv,lower_2,upper_2)
        mask = mask_1+mask_2
    else:
        lower = np.array(color_dict[def_color][0])
        upper = np.array(color_dict[def_color][1])
        mask = cv2.inRange(hsv,lower,upper)

    kernel = np.ones((5,5),np.uint8)
    mask = cv2.erode(mask,kernel,iterations=1)
    mask = cv2.dilate(mask,kernel,iterations=2)

    opening = cv2.morphologyEx(
        mask,
        cv2.MORPH_OPEN,
        kernel
    )

    contours,_=cv2.findContours(
        opening,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    ) 
    for contour in contours:
        area=cv2.contourArea(contour)
        if area<1000:
            continue
        x,y,w,h= cv2.boundingRect(contour)
        cv2.rectangle(
            flip_frame,
            (x,y),
            (x+w,y+h),
            (255,0,0),
            2
        )
        cx = int(x+w/2)
        cy = int(y+h/2)
        cv2.circle(
            flip_frame,
            (cx,cy),
            6,
            (0,0,255),
            -1
        )

    cv2.imshow("Cam 1",flip_frame)
    cv2.imshow("mask",mask)

    key = cv2.waitKey(1) & 0xFF 

    if key==ord('q'):
        print("Cam stoped!!")
        break

    if key==ord('r'):
        def_color="red"
        print("Color target: Red")

    if key==ord('g'):
        def_color="green"
        print("Color target: Green")

    if key==ord('b'):
        def_color="blue"
        print("Color target: Blue")

    if key==ord('y'):
        def_color="yellow"
        print("Color target: Yellow")

    if key==ord('o'):
        def_color="orange"
        print("Color target: Orange")

    if key==ord('p'):
        def_color="purple"
        print("Color target: Purple")
        
    ret,frame=cam.read()

cam.release()
cv2.destroyAllWindows()