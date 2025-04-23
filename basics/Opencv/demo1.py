import cv2
src1 = cv2.imread(r'D:\python\basics\Opencv\lena.jpg')
cv2.namedWindow('lena',cv2.WINDOW_NORMAL)
cv2.imshow('lena',src1)
cv2.namedWindow('src1',cv2.WINDOW_NORMAL)
src1[450:550,250:800]=0
#将100-200行，230-380列的像素值设为0
cv2.imshow('src1',src1) 
cv2.waitKey(0)
cv2.destroyAllWindows()