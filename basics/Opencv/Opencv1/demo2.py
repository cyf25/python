import numpy as np
import cv2
img=img2=cv2.imread(r'D:\python\basics\Opencv\lena.jpg')
def dochage(x):
    global img
    bgr=cv2.getTrackbarPos('BGR','image')
    if bgr==0:
        img=img2
    else:
        img= img2[:,:,bgr-1]
cv2.namedWindow('image',cv2.WINDOW_NORMAL)

cv2.createTrackbar('BGR','image',0,3,dochage)

while True:
    
    cv2.imshow('image',img)

    if cv2.waitKey(1)==27:
        break
cv2.destroyAllWindows()