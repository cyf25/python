#!/usr/bin/env python3
"""
配置检查脚本
"""

def check_config():
    """检查配置是否正确"""
    try:
        from config import config, validate_config
        
        print("🔍 检查系统配置...")
        print("=" * 40)
        
        # 检查API密钥
        if config.DEEPSEEK_API_KEY == "your_deepseek_api_key_here":
            print("❌ API密钥未设置")
            print("   请在 config.py 文件中设置你的DeepSeek API密钥")
            print("   找到: DEEPSEEK_API_KEY = 'your_deepseek_api_key_here'")
            print("   替换为: DEEPSEEK_API_KEY = '你的实际API密钥'")
            return False
        else:
            print("✅ API密钥已设置")
        
        # 检查其他配置
        print(f"✅ 应用名称: {config.APP_NAME}")
        print(f"✅ 调试模式: {config.DEBUG}")
        print(f"✅ 服务端口: {config.PORT}")
        print(f"✅ 数据库: {config.DATABASE_URL}")
        
        print("\n🎉 配置检查完成！")
        return True
        
    except Exception as e:
        print(f"❌ 配置检查出错: {e}")
        return False

def check_dependencies():
    """检查依赖是否安装"""
    print("\n🔍 检查依赖包...")
    print("=" * 40)
    
    dependencies = [
        ("fastapi", "FastAPI框架"),
        ("streamlit", "Streamlit前端"),
        ("openai", "OpenAI客户端"),
        ("uvicorn", "ASGI服务器"),
        ("pydantic", "数据验证"),
        ("requests", "HTTP客户端"),
        ("python-dotenv", "环境变量")
    ]
    
    missing = []
    
    for package, description in dependencies:
        try:
            __import__(package)
            print(f"✅ {description} ({package})")
        except ImportError:
            print(f"❌ {description} ({package}) - 未安装")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  缺少依赖包: {', '.join(missing)}")
        print("请运行: pip install -r requirements.txt")
        return False
    else:
        print("\n🎉 所有依赖包已安装！")
        return True

def main():
    """主函数"""
    print("🎓 校园生活服务智能助手 - 配置检查")
    print("=" * 50)
    
    # 检查依赖
    deps_ok = check_dependencies()
    
    # 检查配置
    config_ok = check_config()
    
    print("\n" + "=" * 50)
    if deps_ok and config_ok:
        print("🎉 系统配置正确，可以启动！")
        print("运行命令: python start.py")
    else:
        print("⚠️  请先解决上述问题，然后重新运行此脚本")
        
        if not config_ok:
            print("\n📝 配置说明:")
            print("1. 打开 config.py 文件")
            print("2. 找到 DEEPSEEK_API_KEY 设置")
            print("3. 替换为你的实际API密钥")
            print("4. 保存文件")

if __name__ == "__main__":
    main() 