import cv2 

image = cv2.imread("pictures/422281209644530.jfif")
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
rgb=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)

cv2.imshow("rgb",rgb)
cv2.imshow("gray",gray)
cv2.imshow("hsv",hsv)

cv2.waitKey(0)
cv2.destroyAllWindows()