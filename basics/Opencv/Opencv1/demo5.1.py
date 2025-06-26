import numpy as np
import matplotlib.pyplot as plt
import cv2

# 设置中文显示
plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题

def load_image(image_path):
    """加载图像并返回BGR格式的图像数组"""
    # 使用OpenCV读取图像
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"无法加载图像: {image_path}")
    return image

def calculate_1d_histogram(image, channels=None, bins=256, ranges=[0, 256]):
 
    if channels is None:
        # 默认处理所有通道
        if len(image.shape) == 3:  # 彩色图像
            channels = [0, 1, 2]  # B, G, R
        else:  # 灰度图像
            channels = [0]
    
    histograms = {}
    channel_names = ['蓝色', '绿色', '红色', '灰度']
    
    for channel in channels:
        # 计算单通道直方图
        hist = cv2.calcHist([image], [channel], None, [bins], ranges)
        
        # 存储结果
        histograms[channel_names[channel]] = hist
    
    return histograms

def calculate_2d_histogram(image, channels=[0, 1], bins=[64, 64], ranges=[0, 256, 0, 256]):
 
    if len(channels) != 2:
        raise ValueError("二维直方图需要指定两个通道")
    
    # 计算二维直方图
    hist = cv2.calcHist([image], channels, None, bins, ranges)
    
    # 获取通道名称
    channel_names = ['蓝色', '绿色', '红色']
    channel_names = [channel_names[i] for i in channels]
    
    return hist, channel_names

def plot_1d_histograms(histograms, title="一维直方图"):
    """绘制一维直方图"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    colors = {'蓝色': 'b', '绿色': 'g', '红色': 'r', '灰度': 'gray'}
    
    for channel_name, hist in histograms.items():
        ax.plot(hist, color=colors.get(channel_name, 'black'), label=channel_name)
    
    ax.set_title(title)
    ax.set_xlabel('像素值')
    ax.set_ylabel('频数')
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    return fig

def plot_2d_histogram(hist, channel_names, title="二维直方图"):
    """绘制二维直方图"""
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # 绘制热力图
    im = ax.imshow(hist, cmap='viridis', origin='lower')
    
    # 添加颜色条
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label('频数')
    
    # 设置标题和轴标签
    ax.set_title(f"{channel_names[0]}与{channel_names[1]}通道的二维直方图")
    ax.set_xlabel(f"{channel_names[0]}通道bin索引")
    ax.set_ylabel(f"{channel_names[1]}通道bin索引")
    
    # 添加刻度标签
    ticks = np.linspace(0, hist.shape[0]-1, 5).astype(int)
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)
    
    plt.tight_layout()
    return fig

def main():
    # 示例：加载图像并计算直方图
    image_path = "example.jpg"  # 请替换为实际图像路径
    
    try:
        # 加载图像
        image = load_image( r"D:\BaiduNetdiskDownload\day4\1.jpg")
        
        # 显示原始图像
        plt.figure(figsize=(6, 6))
        # 转换为RGB格式显示
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        plt.title("原始图像")
        plt.axis('off')
        plt.show()
        
        # 计算一维直方图
        print("正在计算一维直方图...")
        histograms_1d = calculate_1d_histogram(image)
        fig_1d = plot_1d_histograms(histograms_1d, "使用OpenCV计算的一维直方图")
        plt.show()
        
        # 计算二维直方图 (蓝色和绿色通道)
        print("正在计算二维直方图...")
        hist_2d, channel_names = calculate_2d_histogram(image, channels=[0, 1])
        fig_2d = plot_2d_histogram(hist_2d, channel_names, "使用OpenCV计算的二维直方图")
        plt.show()
        
        print("直方图计算完成！")
        
    except Exception as e:
        print(f"程序运行出错: {e}")

if __name__ == "__main__":
    main()