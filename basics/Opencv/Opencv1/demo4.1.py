import cv2
import numpy as np
import matplotlib.pyplot as plt

# 设置matplotlib中文字体
plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]

def find_and_draw_contours(image_path, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE):
    """
    查找并绘制图像中的轮廓
    
    参数:
    image_path (str): 图像文件路径
    mode (int): 轮廓检索模式
    method (int): 轮廓近似方法
    
    返回:
    原始图像和轮廓绘制结果的numpy数组
    """
    # 读取图像
    image = cv2.imread(image_path)
    
    # 检查图像是否成功加载
    if image is None:
        print(f"无法加载图像: {image_path}")
        return None, None
    
    # 创建用于绘制轮廓的副本
    contour_image = image.copy()
    
    # 将图像转换为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 应用Canny边缘检测
    edges = cv2.Canny(gray, 100, 200)
    
    # 查找轮廓
    contours, hierarchy = cv2.findContours(edges, mode, method)
    
    # 绘制轮廓
    cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 2)
    
    # 将BGR转换为RGB(matplotlib使用RGB格式)
    original_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    contour_rgb = cv2.cvtColor(contour_image, cv2.COLOR_BGR2RGB)
    
    return original_rgb, contour_rgb

def display_results(original, contour, image_path):
    """
    显示原始图像和轮廓绘制结果
    
    参数:
    original (numpy.ndarray): 原始图像
    contour (numpy.ndarray): 轮廓绘制结果
    image_path (str): 图像文件路径
    """
    if original is None or contour is None:
        return
    
    # 创建一个2x1的子图布局
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    
    # 显示原始图像
    ax1.imshow(original)
    ax1.set_title('原始图像')
    ax1.axis('off')
    
    # 显示轮廓绘制结果
    ax2.imshow(contour)
    ax2.set_title('轮廓绘制结果')
    ax2.axis('off')
    
    # 设置主标题为图像路径
    fig.suptitle(f'图像路径: {image_path}', fontsize=14)
    
    # 调整布局
    plt.tight_layout()
    
    # 显示图像
    plt.show()

if __name__ == "__main__":
    # 请替换为你的图像路径
    image_path = r"D:\BaiduNetdiskDownload\day4\1.jpg"
    
    # 执行轮廓查找和绘制
    original, contour = find_and_draw_contours(image_path)
    
    # 显示结果
    display_results(original, contour, image_path)