#!/usr/bin/env python3
"""
依赖安装脚本
"""

import subprocess
import sys
import os

def run_command(command, description):
    """运行命令并显示结果"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} 成功")
            return True
        else:
            print(f"❌ {description} 失败")
            print(f"错误信息: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} 异常: {e}")
        return False

def install_core_deps():
    """安装核心依赖"""
    print("📦 安装核心依赖...")
    
    # 升级pip
    run_command(f"{sys.executable} -m pip install --upgrade pip", "升级pip")
    
    # 安装核心包
    core_packages = [
        "fastapi",
        "uvicorn", 
        "pydantic",
        "python-dotenv",
        "requests",
        "openai",
        "streamlit"
    ]
    
    for package in core_packages:
        success = run_command(f"{sys.executable} -m pip install {package}", f"安装 {package}")
        if not success:
            print(f"⚠️  跳过 {package}，继续安装其他包")
    
    return True

def install_optional_deps():
    """安装可选依赖"""
    print("\n📦 安装可选依赖...")
    
    optional_packages = [
        "langchain",
        "langchain-community"
    ]
    
    for package in optional_packages:
        success = run_command(f"{sys.executable} -m pip install {package}", f"安装 {package}")
        if not success:
            print(f"⚠️  {package} 安装失败，但不影响核心功能")

def check_installation():
    """检查安装结果"""
    print("\n🔍 检查安装结果...")
    
    packages = [
        ("fastapi", "FastAPI框架"),
        ("uvicorn", "ASGI服务器"),
        ("pydantic", "数据验证"),
        ("python-dotenv", "环境变量"),
        ("requests", "HTTP客户端"),
        ("openai", "OpenAI客户端"),
        ("streamlit", "Streamlit前端")
    ]
    
    missing = []
    
    for package, description in packages:
        try:
            __import__(package)
            print(f"✅ {description} ({package})")
        except ImportError:
            print(f"❌ {description} ({package}) - 未安装")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  缺少包: {', '.join(missing)}")
        print("请手动安装: pip install " + " ".join(missing))
        return False
    else:
        print("\n🎉 所有核心依赖安装成功！")
        return True

def main():
    """主函数"""
    print("🎓 校园生活服务智能助手 - 依赖安装")
    print("=" * 50)
    
    # 安装核心依赖
    install_core_deps()
    
    # 安装可选依赖
    install_optional_deps()
    
    # 检查安装结果
    success = check_installation()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 依赖安装完成！")
        print("现在可以运行: python start.py")
    else:
        print("⚠️  部分依赖安装失败，请手动安装缺少的包")

if __name__ == "__main__":
    main() 