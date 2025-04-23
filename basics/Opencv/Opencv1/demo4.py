import cv2
import numpy as np


# 创建一个空白的黑白图像
image = np.zeros((200, 400), dtype=np.uint8)

# 使用 cv2.putText 函数创建英文字符 AB
font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(image, 'AB', (50, 120), font, 5, (255, 255, 255), 2, cv2.LINE_AA)

# 使用 cv2.circle 函数创建白色噪音
num_noise_points = 100
for _ in range(num_noise_points):
    x = np.random.randint(0, image.shape[1])
    y = np.random.randint(0, image.shape[0])
    cv2.circle(image, (x, y), 1, (255, 255, 255), -1)

# 使用 cv2.line 函数创建直线
cv2.line(image, (0, 50), (image.shape[1], 50), (255, 255, 255), 1)
cv2.line(image, (100, 0), (100, image.shape[0]), (255, 255, 255), 1)

# 显示原始图像
cv2.imshow('Original Image', image)

# 定义形态操作的核
kernel = np.ones((3, 3), np.uint8)

# 开运算去除小的噪声和细线条
opened = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

# 闭运算填充字符内部可能的小孔洞
closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)

# 显示处理后的图像
cv2.imshow('Processed Image', closed)

# 等待按键退出
cv2.waitKey(0)
cv2.destroyAllWindows()
    