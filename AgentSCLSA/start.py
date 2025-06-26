#!/usr/bin/env python3
"""
校园生活服务智能助手启动脚本
"""

import subprocess
import sys
import os
import time
import requests
from pathlib import Path

def check_dependencies():
    """检查依赖是否安装"""
    try:
        import fastapi
        import streamlit
        import openai
        import uvicorn
        print("✅ 所有依赖已安装")
        return True
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请运行: pip install -r requirements.txt")
        return False

def check_config():
    """检查配置文件"""
    try:
        from config import validate_config
        if validate_config():
            print("✅ 配置检查通过")
            return True
        else:
            print("❌ 配置检查失败，请先设置API密钥")
            return False
    except Exception as e:
        print(f"❌ 配置检查出错: {e}")
        return False

def start_backend():
    """启动后端服务"""
    print("🚀 启动后端服务...")
    try:
        # 启动FastAPI服务
        process = subprocess.Popen([
            sys.executable, "main.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # 等待服务启动
        time.sleep(3)
        
        # 检查服务是否启动成功
        try:
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                print("✅ 后端服务启动成功 (http://localhost:8000)")
                return process
            else:
                print("❌ 后端服务启动失败")
                return None
        except requests.exceptions.RequestException:
            print("❌ 后端服务启动失败")
            return None
            
    except Exception as e:
        print(f"❌ 启动后端服务时出错: {e}")
        return None

def start_frontend():
    """启动前端服务"""
    print("🎨 启动前端服务...")
    try:
        # 启动Streamlit服务
        process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "frontend/app.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # 等待服务启动
        time.sleep(5)
        
        try:
            response = requests.get("http://localhost:8501", timeout=5)
            if response.status_code == 200:
                print("✅ 前端服务启动成功 (http://localhost:8501)")
                return process
            else:
                print("❌ 前端服务启动失败")
                return None
        except requests.exceptions.RequestException:
            print("❌ 前端服务启动失败")
            return None
            
    except Exception as e:
        print(f"❌ 启动前端服务时出错: {e}")
        return None

def main():
    """主函数"""
    print("🎓 校园生活服务智能助手")
    print("=" * 50)
    
    # 检查依赖
    if not check_dependencies():
        return
    
    # 检查配置
    if not check_config():
        print("\n📝 配置说明:")
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
        print("❌ 无法启动后端服务，退出")
        return
    
    # 启动前端
    frontend_process = start_frontend()
    if not frontend_process:
        print("❌ 无法启动前端服务，退出")
        backend_process.terminate()
        return
    
    print("\n🎉 系统启动成功！")
    print("📱 前端界面: http://localhost:8501")
    print("🔧 后端API: http://localhost:8000")
    print("📚 API文档: http://localhost:8000/docs")
    print("\n按 Ctrl+C 停止服务")
    
    try:
        # 保持服务运行
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 正在停止服务...")
        backend_process.terminate()
        frontend_process.terminate()
        print("✅ 服务已停止")

if __name__ == "__main__":
    main() 