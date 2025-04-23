import cv2
import numpy as np
vc=cv2.VideoCapture(0)
fps=30
size=(int(vc.get(cv2.CAP_PROP_FRAME_WIDTH)),int(vc.get(cv2.CAP_PROP_FRAME_HEIGHT)))
vm=cv2.VideoWriter('捕获视频.avi',cv2.VideoWriter_fourcc(*'XVID'),fps,size)
success,frame=vc.read()
while success:
    vm.write(frame)
    cv2.imshow('Myframe',frame)
    key=cv2.waitKey()
    if key==27:
        break
    success,frame=vc.read()
vc.release