import numpy as np
import cv2

img = np.zeros((512, 512, 3), np.uint8)  # 创建一个512*512的黑色图像
font = cv2.FONT_HERSHEY_PLAIN  # 设置字体

xys = []  # 初始化xys列表

def draw(event, x, y, flags, param):
    global xys
    if event == cv2.EVENT_LBUTTONDOWN:
        xy = f'({x},{y})'
        cv2.putText(img, xy, (x, y), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
        xys.append([x, y])  # 添加坐标到xys列表
        cv2.circle(img, (x, y), 5, (0, 255, 0), -1)
    elif event == cv2.EVENT_RBUTTONDOWN:
        if xys:  # 确保xys列表不为空
            pts = np.array(xys, np.int32)
            cv2.polylines(img, [pts], True, (0, 255, 255), 3)
            xys = []  # 清空xys列表
    cv2.imshow('image', img)

cv2.namedWindow('image')
cv2.setMouseCallback('image', draw)
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
