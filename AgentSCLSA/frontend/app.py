import streamlit as st
import requests
import json
from datetime import datetime
from typing import List, Dict, Any
import time

# 配置页面
st.set_page_config(
    page_title="校园生活服务智能助手",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API配置
API_BASE_URL = "http://localhost:8000"

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid;
    }
    
    .user-message {
        background-color: #e3f2fd;
        border-left-color: #2196f3;
    }
    
    .assistant-message {
        background-color: #f3e5f5;
        border-left-color: #9c27b0;
    }
    
    .service-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border: 1px solid #dee2e6;
    }
    
    .suggestion-button {
        margin: 0.2rem;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        border: 1px solid #ddd;
        background-color: white;
        cursor: pointer;
    }
    
    .suggestion-button:hover {
        background-color: #f0f0f0;
    }
</style>
""", unsafe_allow_html=True)

# 初始化会话状态
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'session_id' not in st.session_state:
    st.session_state.session_id = f"session_{int(time.time())}"

def send_message_to_api(message: str) -> Dict:
    """发送消息到后端API"""
    try:
        context = [
            {"content": msg["content"], "message_type": msg["role"]}
            for msg in st.session_state.messages[-10:] if "role" in msg
        ]
        
        payload = {
            "message": message,
            "user_id": "streamlit_user",
            "session_id": st.session_state.session_id,
            "context": context
        }
        
        response = requests.post(f"{API_BASE_URL}/chat", json=payload, timeout=30)
        
        if response.status_code != 200:
            try:
                error_details = response.json()
                st.error(f"请求失败: {error_details.get('detail', response.text)}")
            except json.JSONDecodeError:
                st.error(f"请求失败，状态码: {response.status_code}, 内容: {response.text}")
            return None
            
        return response.json()

    except requests.exceptions.Timeout:
        st.error("请求超时，后端服务可能正在处理，请稍后再试。")
    except requests.exceptions.RequestException as e:
        st.error(f"请求失败: {e}，请确保后端服务正在运行并且网络连接正常。")
    return None

def get_services() -> List[Dict]:
    """获取可用服务列表"""
    try:
        response = requests.get(f"{API_BASE_URL}/services")
        response.raise_for_status()
        return response.json()["services"]
    except requests.exceptions.RequestException as e:
        st.error(f"获取服务列表失败: {str(e)}")
        return []

def handle_submission(input_text: str):
    """处理用户提交的逻辑"""
    if not input_text.strip():
        return

    # 添加用户消息
    st.session_state.messages.append({
        'content': input_text,
        'is_user': True,
        'role': 'user'
    })

    # 获取AI响应
    with st.spinner("AI正在思考中..."):
        response_data = send_message_to_api(input_text)

    if response_data and response_data.get("response"):
        ai_response = response_data["response"]
        st.session_state.messages.append({
            'content': ai_response["content"],
            'is_user': False,
            'suggestions': ai_response.get("suggestions", []),
            'role': 'assistant'
        })
    else:
        st.session_state.messages.append({
            'content': "抱歉，我暂时无法回答这个问题。",
            'is_user': False,
            'role': 'assistant'
        })
    
    # 清空建议和输入框，然后重新运行
    if 'user_input_from_suggestion' in st.session_state:
        st.session_state.user_input_from_suggestion = ""
    st.rerun()

def display_message(message: Dict):
    """显示消息"""
    is_user = message.get("is_user", False)
    role = "user" if is_user else "assistant"
    
    # 确保所有消息都有 'role'
    message['role'] = role
    
    if is_user:
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>你:</strong> {message['content']}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message assistant-message">
            <strong>AI助手:</strong> {message['content']}
        </div>
        """, unsafe_allow_html=True)
        
        # 显示建议按钮
        if 'suggestions' in message and message['suggestions']:
            # 使用唯一键来避免重复
            suggestion_key_base = f"suggestion_{int(time.time() * 1000)}"
            cols = st.columns(len(message['suggestions']))
            for i, suggestion in enumerate(message['suggestions']):
                if cols[i].button(suggestion, key=f"{suggestion_key_base}_{i}"):
                    # 当按钮被点击时，立即处理
                    handle_submission(suggestion)

def display_service_cards():
    """显示服务卡片"""
    services = get_services()
    
    st.subheader("🎯 可用服务")
    
    for service in services:
        with st.expander(f"📋 {service['name']}", expanded=False):
            st.write(f"**描述:** {service['description']}")
            st.write(f"**类型:** {service['type']}")

def user_profile_section():
    """用户资料设置"""
    st.sidebar.subheader("👤 用户资料")
    
    with st.sidebar.form("user_profile_form"):
        major = st.text_input("专业", value=st.session_state.user_profile.get('major', ''))
        grade = st.selectbox("年级", ["大一", "大二", "大三", "大四", "研究生"], 
                           index=["大一", "大二", "大三", "大四", "研究生"].index(st.session_state.user_profile.get('grade', '大一')))
        interests = st.multiselect("兴趣", ["计算机科学", "数学", "物理", "化学", "生物", "文学", "艺术", "体育", "音乐", "摄影"],
                                 default=st.session_state.user_profile.get('interests', []))
        credits_earned = st.number_input("已修学分", min_value=0, max_value=200, value=st.session_state.user_profile.get('credits_earned', 0))
        
        if st.form_submit_button("更新资料"):
            st.session_state.user_profile = {
                'major': major,
                'grade': grade,
                'interests': interests,
                'credits_earned': credits_earned
            }
            st.success("用户资料已更新！")

def quick_actions():
    """快速操作"""
    st.sidebar.subheader("⚡ 快速操作")
    
    if st.sidebar.button("📚 课程推荐"):
        if st.session_state.user_profile.get('major'):
            response = requests.post(f"{API_BASE_URL}/course/recommendations", 
                                   json={"user_profile": st.session_state.user_profile})
            if response.status_code == 200:
                result = response.json()
                st.session_state.messages.append({
                    'content': result['response']['content'],
                    'suggestions': result['response'].get('suggestions', [])
                })
                st.rerun()
        else:
            st.warning("请先设置用户资料")
    
    if st.sidebar.button("🗺️ 校园导航"):
        handle_submission("我想了解校园导航服务")
    
    if st.sidebar.button("🎓 学习建议"):
        handle_submission("我需要学习建议")
    
    if st.sidebar.button("💬 心理健康支持"):
        handle_submission("我需要心理健康支持")

def main():
    """主函数"""
    # 页面标题
    st.markdown('<h1 class="main-header">校园生活服务智能助手</h1>', unsafe_allow_html=True)
    
    # 初始化
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = {}
    if 'user_input_from_suggestion' not in st.session_state:
        st.session_state.user_input_from_suggestion = ""

    # 侧边栏
    with st.sidebar:
        user_profile_section()
        quick_actions()
        display_service_cards()
    
    # 主聊天区域
    st.subheader("智能对话")
    
    # 显示聊天历史
    if not st.session_state.messages:
        st.session_state.messages.append({
            "content": "你好！我是你的专属校园助手，有什么可以帮到你吗？",
            "is_user": False,
            "suggestions": ["课程推荐", "校园导航", "附近有什么好吃的？"]
        })

    for message in st.session_state.messages:
        display_message(message)
    
    # 输入区域
    user_input = st.text_input("请输入您的问题或需求:", key="user_input_area", placeholder="例如：我想了解计算机科学课程...")
    
    if st.button("发送", key="send_button"):
        handle_submission(user_input)

if __name__ == "__main__":
    main() 