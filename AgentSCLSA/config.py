import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """应用配置类"""
    
    # DeepSeek API配置 - 请在这里直接设置你的API密钥
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "key")  # 请替换为你的实际API密钥
    DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
    
    # 应用配置
    APP_NAME = os.getenv("APP_NAME", "校园生活服务智能助手")
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    HOST = os.getenv("HOST", "127.0.0.1")
    PORT = int(os.getenv("PORT", "8000"))
    
    # 数据库配置
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./campus_assistant.db")
    
    # 日志配置
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "logs/app.log")
    
    # 安全配置
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key_here")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# 创建配置实例
config = Config()

# 配置验证
def validate_config():
    """验证配置是否正确"""
    if config.DEEPSEEK_API_KEY == "your_deepseek_api_key_here":
        print("⚠️  警告: 请先在config.py中设置你的DeepSeek API密钥")
        print("   找到 DEEPSEEK_API_KEY = 'your_deepseek_api_key_here' 这一行")
        print("   将其替换为你的实际API密钥")
        return False
    return True 