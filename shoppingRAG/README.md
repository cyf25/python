# 电商智能客服助手（RAG + DeepSeek）

本项目包含两个前端：
- **frontend/**：管理端（基于 Streamlit，支持知识库管理、文件上传等）
- **chat-frontend/**：用户端（基于 React，专业聊天体验，适合终端用户）

---

## 一键启动

在项目根目录下运行：
```bash
python start_all.py
```
- 会自动分别启动 FastAPI 后端和 React 用户前端
- 管理端和用户端可同时访问

---

## 1. 管理端（frontend/，Streamlit）

- 依赖安装：
  ```bash
  pip install streamlit requests
  ```
- 启动方式：
  ```bash
  cd frontend
  streamlit run main.py
  ```
- 访问地址： [http://localhost:8501](http://localhost:8501)
- 功能：知识库文件上传、管理、历史记录等

---

## 2. 用户端（chat-frontend/，React）

- 依赖安装：
  ```bash
  cd chat-frontend
  npm install
  ```
- 启动方式：
  ```bash
  npm start
  ```
- 访问地址： [http://localhost:3000](http://localhost:3000)
- 功能：专业气泡式聊天体验，支持多轮对话、Markdown排版

---

## 3. 后端（FastAPI）

- 依赖安装：
  ```bash
  pip install -r requirements.txt
  ```
- 启动方式：
  ```bash
  uvicorn app:app --reload
  ```
- 访问地址： [http://localhost:8000/docs](http://localhost:8000/docs)

---

如需更多功能或定制，欢迎随时联系开发者！

## 功能简介
- 支持电商常见问题自动回复
- 检索知识库相关内容，结合大模型生成高质量答案

## 环境变量
- `DEEPSEEK_API_KEY`：你的DeepSeek大模型API Key

## API使用
- 路径：`POST /rag/query`
- 请求体：
```json
{
  "question": "我的订单什么时候发货？"
}
```
- 返回：
```json
{
  "answer": "订单发货后一般1-3天内可送达，节假日顺延。"
}
```

## 知识库扩展
编辑 `rag/data/knowledge_base.json`，添加更多电商知识内容。 