from PIL import Image, ImageDraw, ImageFont
import math

def draw_rounded_rectangle(draw, x1, y1, x2, y2, radius, fill, outline, width=1):
    """绘制带圆角的矩形"""
    # 填充内部
    draw.rectangle([(x1 + radius, y1), (x2 - radius, y2)], fill=fill)
    draw.rectangle([(x1, y1 + radius), (x2, y2 - radius)], fill=fill)
    draw.arc([(x1, y1), (x1 + 2 * radius, y1 + 2 * radius)], 180, 270, fill=fill)
    draw.arc([(x2 - 2 * radius, y1), (x2, y1 + 2 * radius)], 270, 360, fill=fill)
    draw.arc([(x1, y2 - 2 * radius), (x1 + 2 * radius, y2)], 90, 180, fill=fill)
    draw.arc([(x2 - 2 * radius, y2 - 2 * radius), (x2, y2)], 0, 99, fill=fill)
    
    # 绘制边框（使用 fill 替代 outline）
    if width > 0:
        # 顶边和底边
        draw.line([(x1 + radius, y1), (x2 - radius, y1)], fill=outline, width=width)
        draw.line([(x1 + radius, y2), (x2 - radius, y2)], fill=outline, width=width)
        # 左边和右边
        draw.line([(x1, y1 + radius), (x1, y2 - radius)], fill=outline, width=width)
        draw.line([(x2, y1 + radius), (x2, y2 - radius)], fill=outline, width=width)
        # 四个角
        draw.arc([(x1, y1), (x1 + 2 * radius, y1 + 2 * radius)], 180, 270, fill=outline, width=width)
        draw.arc([(x2 - 2 * radius, y1), (x2, y1 + 2 * radius)], 270, 360, fill=outline, width=width)
        draw.arc([(x1, y2 - 2 * radius), (x1 + 2 * radius, y2)], 90, 180, fill=outline, width=width)
        draw.arc([(x2 - 2 * radius, y2 - 2 * radius), (x2, y2)], 0, 90, fill=outline, width=width)

def draw_arrow(draw, x1, y1, x2, y2, head_width=8, head_length=10, width=2):
    """绘制带箭头的线条"""
    draw.line([(x1, y1), (x2, y2)], fill="black", width=width)
    
    # 计算箭头角度
    angle = math.atan2(y2 - y1, x2 - x1)
    
    # 绘制箭头头部
    arrow_x1 = x2 - head_length * math.cos(angle - math.pi / 6)
    arrow_y1 = y2 - head_length * math.sin(angle - math.pi / 6)
    arrow_x2 = x2 - head_length * math.cos(angle + math.pi / 6)
    arrow_y2 = y2 - head_length * math.sin(angle + math.pi / 6)
    
    draw.polygon([(x2, y2), (arrow_x1, arrow_y1), (arrow_x2, arrow_y2)], fill="black")

def generate_login_flowchart(output_path="login_flowchart.png"):
    """生成教务系统登录流程图"""
    # 创建图像
    width, height = 800, 600
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    
    # 定义颜色
    COLOR_START_END = (246, 255, 237)  # 淡绿色
    COLOR_PROCESS = (230, 247, 255)    # 淡蓝色
    COLOR_DECISION = (255, 247, 230)   # 淡黄色
    COLOR_BORDER_START_END = (82, 196, 26)    # 绿色边框
    COLOR_BORDER_PROCESS = (24, 144, 255)     # 蓝色边框
    COLOR_BORDER_DECISION = (250, 140, 22)    # 橙色边框
    
    # 定义字体
    try:
        font = ImageFont.truetype("Arial.ttf", 14)
    except IOError:
        # 如果找不到Arial字体，使用默认字体
        font = ImageFont.load_default()
    
    # 开始节点
    draw.ellipse((350, 50, 450, 110), fill=COLOR_START_END, outline=COLOR_BORDER_START_END, width=2)
    draw.text((400, 75), "开始", fill="black", font=font, anchor="mm")
    
    # 初始化尝试次数
    draw_rounded_rectangle(draw, 330, 130, 470, 180, 5, COLOR_PROCESS, COLOR_BORDER_PROCESS, 2)
    draw.text((400, 155), "尝试次数 = 0", fill="black", font=font, anchor="mm")
    
    # 判断尝试次数
    points = [(400, 210), (460, 250), (400, 290), (340, 250)]
    draw.polygon(points, fill=COLOR_DECISION)
    draw.line(points + [points[0]], fill=COLOR_BORDER_DECISION, width=2)
    draw.text((400, 250), "尝试次数 < 3?", fill="black", font=font, anchor="mm")
    
    # 是分支 - 登录界面
    draw_rounded_rectangle(draw, 330, 320, 470, 370, 5, COLOR_PROCESS, COLOR_BORDER_PROCESS, 2)
    draw.text((400, 345), "显示登录界面", fill="black", font=font, anchor="mm")
    
    # 输入用户名密码
    draw_rounded_rectangle(draw, 330, 390, 470, 440, 5, COLOR_PROCESS, COLOR_BORDER_PROCESS, 2)
    draw.text((400, 415), "输入用户名和密码", fill="black", font=font, anchor="mm")
    
    # 判断用户名密码
    points = [(400, 470), (460, 510), (400, 550), (340, 510)]
    draw.polygon(points, fill=COLOR_DECISION)
    draw.line(points + [points[0]], fill=COLOR_BORDER_DECISION, width=2)
    draw.text((400, 510), "用户名和密码是否正确?", fill="black", font=font, anchor="mm")
    
    # 是分支 - 登录成功
    draw_rounded_rectangle(draw, 530, 470, 670, 520, 5, COLOR_PROCESS, COLOR_BORDER_PROCESS, 2)
    draw.text((600, 495), "显示登录成功", fill="black", font=font, anchor="mm")
    
    # 进入系统
    draw_rounded_rectangle(draw, 530, 540, 670, 590, 5, COLOR_PROCESS, COLOR_BORDER_PROCESS, 2)
    draw.text((600, 565), "进入系统", fill="black", font=font, anchor="mm")
    
    # 结束节点
    draw.ellipse((550, 610, 650, 670), fill=COLOR_START_END, outline=COLOR_BORDER_START_END, width=2)
    draw.text((600, 640), "结束", fill="black", font=font, anchor="mm")
    
    # 否分支 - 增加尝试次数
    draw_rounded_rectangle(draw, 130, 470, 270, 520, 5, COLOR_PROCESS, COLOR_BORDER_PROCESS, 2)
    draw.text((200, 495), "尝试次数 +1", fill="black", font=font, anchor="mm")
    
    # 显示错误提示
    draw_rounded_rectangle(draw, 130, 540, 270, 590, 5, COLOR_PROCESS, COLOR_BORDER_PROCESS, 2)
    draw.text((200, 565), "显示错误提示\n(剩余尝试次数)", fill="black", font=font, anchor="mm")
    
    # 否分支 - 登录失败
    draw_rounded_rectangle(draw, 130, 210, 270, 260, 5, COLOR_PROCESS, COLOR_BORDER_PROCESS, 2)
    draw.text((200, 235), "登录失败，账号已锁定", fill="black", font=font, anchor="mm")
    
    # 连接线
    draw_arrow(draw, 400, 110, 400, 130)  # 开始 -> 初始化
    draw_arrow(draw, 400, 180, 400, 210)  # 初始化 -> 判断尝试次数
    draw_arrow(draw, 400, 290, 400, 320)  # 判断尝试次数(是) -> 登录界面
    draw_arrow(draw, 400, 370, 400, 390)  # 登录界面 -> 输入用户名密码
    draw_arrow(draw, 400, 440, 400, 470)  # 输入用户名密码 -> 判断用户名密码
    draw_arrow(draw, 460, 510, 530, 510)  # 判断用户名密码(是) -> 登录成功
    draw_arrow(draw, 530, 520, 530, 540)  # 登录成功 -> 进入系统
    draw_arrow(draw, 530, 590, 600, 610)  # 进入系统 -> 结束
    draw_arrow(draw, 340, 510, 270, 510)  # 判断用户名密码(否) -> 增加尝试次数
    draw_arrow(draw, 270, 510, 270, 540)  # 增加尝试次数 -> 显示错误提示
    draw_arrow(draw, 270, 590, 330, 320)  # 显示错误提示 -> 登录界面
    draw_arrow(draw, 340, 250, 270, 250)  # 判断尝试次数(否) -> 登录失败
    draw_arrow(draw, 270, 260, 270, 610)  # 登录失败 -> 结束
    
    # 标注"是"和"否"
    draw.text((430, 230), "是", fill="black", font=font, anchor="mm")
    draw.text((370, 230), "否", fill="black", font=font, anchor="mm")
    draw.text((490, 490), "是", fill="black", font=font, anchor="mm")
    draw.text((310, 490), "否", fill="black", font=font, anchor="mm")
    
    # 保存图像
    image.save(output_path)
    print(f"流程图已保存至 {output_path}")
    
    # 返回图像对象
    return image

if __name__ == "__main__":
    generate_login_flowchart()