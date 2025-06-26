import cv2
import matplotlib.pyplot as plt

# 设置matplotlib中文字体
plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]

def canny_edge_detection(image_path, threshold1=100, threshold2=200):
    """
    使用Canny算法进行边缘检测
    
    参数:
    image_path (str): 图像文件路径
    threshold1 (int): Canny算法的第一个阈值
    threshold2 (int): Canny算法的第二个阈值
    
    返回:
    原始图像和边缘检测结果的numpy数组
    """
    # 读取图像
    image = cv2.imread(image_path)
    
    # 检查图像是否成功加载
    if image is None:
        print(f"无法加载图像: {image_path}")
        return None, None
    
    # 将图像从BGR转换为RGB(matplotlib使用RGB格式)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # 转换为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 应用Canny边缘检测
    edges = cv2.Canny(gray, threshold1, threshold2)
    
    return image_rgb, edges

def display_results(original, edges, image_path):
    """
    显示原始图像和边缘检测结果
    
    参数:
    original (numpy.ndarray): 原始图像
    edges (numpy.ndarray): 边缘检测结果
    image_path (str): 图像文件路径
    """
    if original is None or edges is None:
        return
    
    # 创建一个2x1的子图布局
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    
    # 显示原始图像
    ax1.imshow(original)
    ax1.set_title('原始图像')
    ax1.axis('off')
    
    # 显示边缘检测结果
    ax2.imshow(edges, cmap='gray')
    ax2.set_title('Canny边缘检测结果')
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
    
    # 执行Canny边缘检测
    original, edges = canny_edge_detection(image_path)
    
    # 显示结果
    display_results(original, edges, image_path)