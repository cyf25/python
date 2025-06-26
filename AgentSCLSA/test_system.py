#!/usr/bin/env python3
"""
校园生活服务智能助手系统测试脚本
"""

import requests
import json
import time
from typing import Dict, Any

# API配置
API_BASE_URL = "http://localhost:8000"

def test_health_check():
    """测试健康检查"""
    print("🔍 测试健康检查...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            print("✅ 健康检查通过")
            return True
        else:
            print(f"❌ 健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 健康检查异常: {e}")
        return False

def test_services():
    """测试服务列表"""
    print("🔍 测试服务列表...")
    try:
        response = requests.get(f"{API_BASE_URL}/services")
        if response.status_code == 200:
            services = response.json()["services"]
            print(f"✅ 获取到 {len(services)} 个服务")
            for service in services:
                print(f"  - {service['name']}: {service['description']}")
            return True
        else:
            print(f"❌ 获取服务列表失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 获取服务列表异常: {e}")
        return False

def test_chat():
    """测试聊天功能"""
    print("🔍 测试聊天功能...")
    try:
        payload = {
            "message": "你好，我想了解计算机科学课程",
            "user_id": "test_user",
            "session_id": "test_session"
        }
        
        response = requests.post(f"{API_BASE_URL}/chat", json=payload)
        if response.status_code == 200:
            result = response.json()
            print("✅ 聊天功能正常")
            print(f"  AI回复: {result['response']['content'][:100]}...")
            return True
        else:
            print(f"❌ 聊天功能失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 聊天功能异常: {e}")
        return False

def test_course_recommendations():
    """测试课程推荐"""
    print("🔍 测试课程推荐...")
    try:
        payload = {
            "user_profile": {
                "major": "计算机科学",
                "grade": "大二",
                "interests": ["编程", "人工智能"],
                "credits_earned": 30
            }
        }
        
        response = requests.post(f"{API_BASE_URL}/course/recommendations", json=payload)
        if response.status_code == 200:
            result = response.json()
            print("✅ 课程推荐功能正常")
            print(f"  推荐内容: {result['response']['content'][:100]}...")
            return True
        else:
            print(f"❌ 课程推荐失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 课程推荐异常: {e}")
        return False

def test_navigation():
    """测试导航功能"""
    print("🔍 测试导航功能...")
    try:
        payload = {
            "location_name": "图书馆"
        }
        
        response = requests.post(f"{API_BASE_URL}/navigation/find", json=payload)
        if response.status_code == 200:
            result = response.json()
            print("✅ 导航功能正常")
            print(f"  地点信息: {result['response']['content'][:100]}...")
            return True
        else:
            print(f"❌ 导航功能失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 导航功能异常: {e}")
        return False

def test_route_planning():
    """测试路线规划"""
    print("🔍 测试路线规划...")
    try:
        payload = {
            "start_location": "教学楼A",
            "end_location": "图书馆"
        }
        
        response = requests.post(f"{API_BASE_URL}/navigation/route", json=payload)
        if response.status_code == 200:
            result = response.json()
            print("✅ 路线规划功能正常")
            print(f"  路线信息: {result['response']['content'][:100]}...")
            return True
        else:
            print(f"❌ 路线规划失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 路线规划异常: {e}")
        return False

def test_academic_qa():
    """测试学术问答"""
    print("🔍 测试学术问答...")
    try:
        payload = {
            "question": "什么是机器学习？",
            "subject": "计算机科学"
        }
        
        response = requests.post(f"{API_BASE_URL}/qa/academic", json=payload)
        if response.status_code == 200:
            result = response.json()
            print("✅ 学术问答功能正常")
            print(f"  回答内容: {result['response']['content'][:100]}...")
            return True
        else:
            print(f"❌ 学术问答失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 学术问答异常: {e}")
        return False

def test_life_advice():
    """测试生活建议"""
    print("🔍 测试生活建议...")
    try:
        payload = {
            "situation": "我最近学习压力很大，感觉很累",
            "category": "心理健康"
        }
        
        response = requests.post(f"{API_BASE_URL}/qa/life-advice", json=payload)
        if response.status_code == 200:
            result = response.json()
            print("✅ 生活建议功能正常")
            print(f"  建议内容: {result['response']['content'][:100]}...")
            return True
        else:
            print(f"❌ 生活建议失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 生活建议异常: {e}")
        return False

def main():
    """主测试函数"""
    print("🧪 校园生活服务智能助手系统测试")
    print("=" * 50)
    
    # 等待服务启动
    print("⏳ 等待服务启动...")
    time.sleep(3)
    
    # 测试列表
    tests = [
        ("健康检查", test_health_check),
        ("服务列表", test_services),
        ("聊天功能", test_chat),
        ("课程推荐", test_course_recommendations),
        ("导航功能", test_navigation),
        ("路线规划", test_route_planning),
        ("学术问答", test_academic_qa),
        ("生活建议", test_life_advice)
    ]
    
    # 执行测试
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        if test_func():
            passed += 1
        time.sleep(1)  # 避免请求过快
    
    # 输出测试结果
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！系统运行正常")
    else:
        print("⚠️  部分测试失败，请检查系统配置")
    
    print("\n💡 提示:")
    print("- 确保后端服务正在运行 (http://localhost:8000)")
    print("- 检查DeepSeek API配置是否正确")
    print("- 查看日志文件了解详细错误信息")

if __name__ == "__main__":
    main() 