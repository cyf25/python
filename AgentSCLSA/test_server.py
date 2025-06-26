#!/usr/bin/env python3
"""
简单的服务器测试脚本
"""

import subprocess
import time
import requests
import sys
import os

def test_server_startup():
    """测试服务器启动"""
    print("测试服务器启动...")
    
    # 检查依赖
    try:
        import fastapi
        import uvicorn
        import openai
        print("✓ 核心依赖已安装")
    except ImportError as e:
        print(f"✗ 缺少依赖: {e}")
        return False
    
    # 检查配置
    try:
        from config import config
        print(f"✓ 配置加载成功，API密钥: {config.DEEPSEEK_API_KEY[:10]}...")
    except Exception as e:
        print(f"✗ 配置加载失败: {e}")
        return False
    
    # 启动服务器
    print("启动服务器...")
    try:
        process = subprocess.Popen([
            sys.executable, "main.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # 等待服务器启动
        print("等待服务器启动...")
        time.sleep(8)  # 增加等待时间
        
        # 检查进程状态
        if process.poll() is not None:
            stdout, stderr = process.communicate()
            print(f"✗ 服务器进程已退出")
            print(f"stdout: {stdout.decode()}")
            print(f"stderr: {stderr.decode()}")
            return False
        
        # 测试健康检查
        print("测试健康检查...")
        try:
            response = requests.get("http://localhost:8000/health", timeout=15)
            if response.status_code == 200:
                print("✓ 服务器启动成功")
                process.terminate()
                return True
            else:
                print(f"✗ 健康检查失败，状态码: {response.status_code}")
                process.terminate()
                return False
        except requests.exceptions.RequestException as e:
            print(f"✗ 无法连接到服务器: {e}")
            process.terminate()
            return False
            
    except Exception as e:
        print(f"✗ 启动服务器时出错: {e}")
        return False

if __name__ == "__main__":
    success = test_server_startup()
    if success:
        print("\n✓ 服务器测试通过")
    else:
        print("\n✗ 服务器测试失败")
        sys.exit(1) 