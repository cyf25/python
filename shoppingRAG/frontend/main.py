import streamlit as st
from streamlit_chat import message
import requests
import uuid

st.set_page_config(page_title="电商智能客服助手", page_icon="🛒")

# 自定义CSS让输入区尽量靠近底部
st.markdown('''
    <style>
    .main-title {
        width: 700px;
        max-width: 90vw;
        margin-left: auto;
        margin-right: auto;
        margin-top: 2.5rem;
        margin-bottom: 2.5rem;
        font-size: 2.2rem;
        font-weight: bold;
        text-align: left;
        display: block;
    }
    .input-row {
        width: 700px;
        max-width: 90vw;
        margin-left: auto;
        margin-right: auto;
        margin-bottom: 1.5rem;
    }
    .block-container { padding-bottom: 10rem; }
    </style>
''', unsafe_allow_html=True)

if 'session_id' not in st.session_state:
    st.session_state['session_id'] = str(uuid.uuid4())
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'input_text' not in st.session_state:
    st.session_state['input_text'] = ''

# 标题左对齐且宽度与输入区一致
st.markdown('<div class="main-title">🛒 电商智能客服助手 (RAG + DeepSeek)</div>', unsafe_allow_html=True)

API_URL = "http://localhost:8000/rag/query"
API_CHAT_URL = "http://localhost:8000/rag/chat"

st.sidebar.header("管理员功能")
with st.sidebar.expander("📤 知识库文件上传", expanded=False):
    uploaded_files = st.file_uploader("选择文件上传 (txt, docx, pdf, csv, xlsx)", type=["txt", "docx", "pdf", "csv", "xlsx"], accept_multiple_files=True)
    if st.button("上传文件") and uploaded_files:
        files = [("files", (f.name, f.read())) for f in uploaded_files]
        try:
            resp = requests.post("http://localhost:8000/admin/upload", files=files)
            if resp.status_code == 200:
                st.success(resp.json()["msg"])
            else:
                st.error("上传失败：" + resp.text)
        except Exception as e:
            st.error(f"请求失败: {e}")
    # 上传历史
    st.markdown("---")
    st.markdown("#### 上传历史记录")
    try:
        log_resp = requests.get("http://localhost:8000/admin/upload_log")
        if log_resp.status_code == 200:
            logs = log_resp.json()
            for log in reversed(logs):
                st.write(f"{log['time']} 上传: {', '.join(log['files'])}，新增片段: {log['added_chunks']}")
        else:
            st.info("暂无上传历史。")
    except Exception:
        st.info("暂无上传历史。")

# 聊天气泡展示
for i, turn in enumerate(st.session_state['chat_history']):
    message(turn['question'], is_user=True, key=f"user_{i}")
    message(turn['answer'], is_user=False, key=f"bot_{i}")

def send_message():
    user_input = st.session_state['input_text']
    if user_input.strip():
        with st.spinner("正在生成回复..."):
            try:
                resp = requests.post(API_CHAT_URL, json={
                    "question": user_input,
                    "session_id": st.session_state['session_id']
                })
                if resp.status_code == 200:
                    data = resp.json()
                    st.session_state['session_id'] = data["session_id"]
                    st.session_state['chat_history'].append({"question": user_input, "answer": data["answer"]})
                    st.session_state['input_text'] = ''
                else:
                    st.error(f"后端错误: {resp.text}")
            except Exception as e:
                st.error(f"请求失败: {e}")

# 输入区靠近底部，按钮在右，支持回车发送
with st.container():
    st.markdown('<div class="input-row">', unsafe_allow_html=True)
    col1, col2 = st.columns([8, 2])
    with col1:
        st.text_input(
            "请输入您的问题：",
            key="input_text",
            label_visibility="collapsed",
            on_change=send_message
        )
    with col2:
        st.button("发送", key="send_btn", on_click=send_message)
    st.markdown('</div>', unsafe_allow_html=True) 