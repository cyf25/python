#!/usr/bin/env python3
"""
校园生活服务智能助手简化启动脚本
"""

import subprocess
import sys
import os
import time
import requests
from pathlib import Path
import threading

def check_dependencies():
    """检查依赖是否安装"""
    try:
        import fastapi
        import uvicorn
        import openai
        print("核心依赖已安装")
        return True
    except ImportError as e:
        print(f"缺少依赖: {e}")
        print("请运行: python install_deps.py")
        return False

def check_config():
    """检查配置文件"""
    try:
        from config import validate_config
        if validate_config():
            print("配置检查通过")
            return True
        else:
            print("配置检查失败，请先设置API密钥")
            return False
    except Exception as e:
        print(f"配置检查出错: {e}")
        return False

def start_backend():
    """启动后端服务"""
    print("启动后端服务...")
    backend_log_file = "logs/backend.log"
    try:
        # 确保日志目录存在
        os.makedirs("logs", exist_ok=True)
        
        # 打开日志文件
        with open(backend_log_file, 'w') as log_file:
            # 启动FastAPI服务，将输出重定向到日志文件
            process = subprocess.Popen([
                sys.executable, "main.py"
            ], stdout=log_file, stderr=subprocess.STDOUT)
        
        # 等待服务启动 - 增加等待时间
        print(f"等待服务启动... 后端日志请查看: {backend_log_file}")
        time.sleep(12)  # 增加等待时间到12秒
        
        # 检查进程是否意外退出
        if process.poll() is not None:
            print("后端进程已意外退出。请检查日志获取错误信息。")
            return None
        
        # 检查服务是否启动成功
        print("检查服务状态...")
        max_retries = 5  # 增加重试次数
        for i in range(max_retries):
            try:
                # 尝试多个健康检查端点
                health_urls = [
                    "http://127.0.0.1:8000/health",
                    "http://localhost:8000/health",
                    "http://127.0.0.1:8000/",
                    "http://localhost:8000/"
                ]
                
                for url in health_urls:
                    try:
                        response = requests.get(url, timeout=10)  # 增加超时时间
                        if response.status_code == 200:
                            print(f"后端服务启动成功 ({url})")
                            return process
                    except requests.exceptions.RequestException:
                        continue
                
                print(f"尝试 {i+1}/{max_retries}: 无法连接到后端服务...")
                if i < max_retries - 1:
                    time.sleep(5)  # 增加重试间隔
                continue
                
            except Exception as e:
                print(f"尝试 {i+1}/{max_retries}: 连接错误: {e}")
                if i < max_retries - 1:
                    time.sleep(5)
                continue
        
        print("所有重试都失败了。请检查 `logs/backend.log` 文件获取详细错误信息。")
        process.terminate()
        return None
            
    except Exception as e:
        print(f"启动后端服务时出错: {e}")
        return None

def start_frontend():
    """启动前端服务"""
    print("启动前端服务...")
    try:
        # 使用更稳定的Streamlit前端
        process = subprocess.Popen([
            "streamlit", "run", "frontend/app.py",
            "--server.port", "8501",
            "--server.headless", "true"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # 增加等待时间，让Streamlit有足够的时间启动
        print("等待前端服务启动...")
        time.sleep(20)  # 增加等待时间到20秒
        
        # 检查进程是否意外退出
        if process.poll() is not None:
            print("前端进程已意外退出。请检查终端输出获取错误信息。")
            return None
        
        # 检查服务是否启动成功
        print("检查服务状态...")
        max_retries = 5
        for i in range(max_retries):
            try:
                response = requests.get("http://localhost:8501", timeout=15)  # 增加超时时间
                if response.status_code == 200:
                    print("前端服务启动成功 (http://localhost:8501)")
                    return process
                else:
                    print(f"前端服务检查失败，状态码: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"尝试 {i+1}/{max_retries}: 无法连接到前端服务: {e}")
                if i < max_retries - 1:
                    time.sleep(5)  # 增加等待时间
                continue
        
        print("所有重试都失败了")
        process.terminate()
        return None
            
    except Exception as e:
        print(f"启动前端服务时出错: {e}")
        return None

def main():
    """主函数"""
    print("校园生活服务智能助手 - 简化版")
    print("=" * 50)
    
    # 检查依赖
    if not check_dependencies():
        return
    
    # 检查配置
    if not check_config():
        print("\n配置说明:")
        print("1. 打开 config.py 文件")
        print("2. 找到 DEEPSEEK_API_KEY = 'your_deepseek_api_key_here' 这一行")
        print("3. 将 'your_deepseek_api_key_here' 替换为你的实际DeepSeek API密钥")
        print("4. 保存文件后重新运行此脚本")
        return
    
    # 创建必要的目录
    os.makedirs("data", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    # 启动后端
    backend_process = start_backend()
    if not backend_process:
        print("无法启动后端服务，退出")
        return
    
    # 启动前端
    frontend_process = start_frontend()
    if not frontend_process:
        print("无法启动前端服务，退出")
        backend_process.terminate()
        return
    
    print("\n系统启动成功！")
    print("前端界面: http://localhost:8501")
    print("后端API: http://127.0.0.1:8000")
    print("API文档: http://127.0.0.1:8000/docs")
    print("\n按 Ctrl+C 停止服务")
    
    try:
        # 保持服务运行
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n正在停止服务...")
        backend_process.terminate()
        frontend_process.terminate()
        print("服务已停止")

if __name__ == "__main__":
    main() 