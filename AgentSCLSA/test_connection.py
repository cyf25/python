import requests
import time

def test_connection():
    """测试服务器连接"""
    print("测试服务器连接...")
    
    try:
        # 测试根路径
        print("测试根路径...")
        response = requests.get("http://localhost:8000/", timeout=5)
        print(f"根路径响应: {response.status_code}")
        print(f"响应内容: {response.json()}")
        
        # 测试健康检查
        print("\n测试健康检查...")
        response = requests.get("http://localhost:8000/health", timeout=5)
        print(f"健康检查响应: {response.status_code}")
        print(f"响应内容: {response.json()}")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"连接失败: {e}")
        return False

if __name__ == "__main__":
    success = test_connection()
    if success:
        print("\n✓ 连接测试成功")
    else:
        print("\n✗ 连接测试失败") 