import cv2

class ImageProcessing(object):
    def __init__(self,window_name:str,image_path:str):
        self.window_name=window_name
        self.image=cv2.imread(image_path)
    def show(self,title=None,image=None):
        if image is None:
            image=self.image
        if title is None:
            title=self.window_name
        cv2.imshow(title,image)
    def resize(self,percent,image=None):
        if image is None:
            image=self.image
        h,w=image.shape[:2]
        width=int(w*percent/100)
        height=int(h*percent/100)
        resized_image=cv2.resize(image,(width,height))

        return resized_image
    def crop(self,pt_frst,pt_sec,image=None):
        if image is None:
            image=self.image
        x_tl,y_tl=pt_frst
        x_br,y_br=pt_sec

        if x_br < x_tl:
            x_br,x_tl=x_tl,x_br
        if y_br < y_tl:
            y_br,y_tl=y_tl,y_br
        croped_image=image[y_tl:y_br,x_tl:x_br]

        return croped_image
    def rotate(self,angle,image=None,scale=1.0):
        if image is None:
            image=self.image
        (h,w)=image.shape[:2]
        center=(w/2,h/2)
        rot_mat=cv2.getRotationMatrix2D(center,angle,scale)
        rotated_image=cv2.warpAffine(image,rot_mat,(w,h))

        return rotated_image 

ip = ImageProcessing("Process","pictures/3448137209640473.jfif")

ip.show()

resized_image=ip.resize(50)

ip.show(title="resized image",image=resized_image)

cv2.waitKey(0)
cv2.destroyAllWindows()