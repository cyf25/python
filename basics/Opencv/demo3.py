import cv2
import numpy as np

# 读取图像
image = cv2.imread(r'D:\python\basics\Opencv\lena.jpg')
if image is None:
    print("无法读取图像，请检查图像路径。")
else:
    height, width = image.shape[:2]
    center = (width // 2, height // 2)
    scale = 1.0
    scale_step = 0.01
    scale_direction = -1  # -1 表示缩小，1 表示放大
    angle = 0
    angle_step = 1

    while True:
        # 计算旋转矩阵
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale)

        # 应用旋转和缩放变换
        rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))

        # 显示图像
        cv2.imshow('Rotated and Scaled Image', rotated_image)

        # 更新角度
        angle = (angle + angle_step) % 360

        # 更新缩放比例
        scale += scale_step * scale_direction
        if scale <= 0.1:
            scale_direction = 1
        elif scale >= 1.0:
            scale_direction = -1

        # 按 'q' 键退出循环
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    # 关闭所有窗口
    cv2.destroyAllWindows()
    