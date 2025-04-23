import cv2
import numpy as np

# 加载图像（lena.jpg）
image = cv2.imread(r'D:\python\basics\Opencv\lena.jpg')

# 检查图像是否成功加载
if image is None:
    print("错误：无法加载图像，请检查文件路径。")
    exit()

# 创建掩模（与图像大小相同）
mask = np.zeros(image.shape[:2], dtype=np.uint8)  # 单通道掩模

# 在掩模上绘制一个白色小正方形
start_point = (100, 150)  # 正方形左上角坐标
end_point = (800, 800)    # 正方形右下角坐标
cv2.rectangle(mask, start_point, end_point, 255, -1)  # 255 表示白色，-1 表示填充

# 使用掩模提取图像中的正方形区域
masked_image = cv2.bitwise_and(image, image, mask=mask)

# 显示结果
cv2.namedWindow('Original Image',cv2.WINDOW_NORMAL)
cv2.imshow('Original Image', image)
cv2.namedWindow('Mask',cv2.WINDOW_NORMAL)
cv2.imshow('Mask', mask)
cv2.namedWindow('Masked Image',cv2.WINDOW_NORMAL)
cv2.imshow('Masked Image', masked_image)

# 等待按键按下
cv2.waitKey(0)

# 关闭所有窗口
cv2.destroyAllWindows()