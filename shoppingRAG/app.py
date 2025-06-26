from fastapi import FastAPI, HTTPException, UploadFile, File, Request
from pydantic import BaseModel
from rag.retriever import retrieve_relevant_docs, reload_vector_store
from rag.generator import generate_answer
from rag.ingest import read_txt, read_docx, read_pdf, extract_chunks
import shutil
import json
import os
import datetime
import pandas as pd
import io
import uuid
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 添加CORS中间件，允许所有来源
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str

class ChatRequest(BaseModel):
    question: str
    session_id: str = None

class ChatResponse(BaseModel):
    answer: str
    session_id: str

session_history = {}

@app.post("/rag/query", response_model=QueryResponse)
async def rag_query(request: QueryRequest):
    try:
        # 1. 检索相关文档
        docs = retrieve_relevant_docs(request.question)
        # 2. 生成答案
        answer = generate_answer(request.question, docs)
        return QueryResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/admin/upload")
async def upload_files(files: list[UploadFile] = File(...)):
    kb_path = "rag/data/knowledge_base.json"
    log_path = "rag/upload_log.json"
    # 读取现有知识库
    if os.path.exists(kb_path):
        with open(kb_path, "r", encoding="utf-8") as f:
            kb = json.load(f)
    else:
        kb = []
    new_chunks = []
    for file in files:
        content = None
        if file.filename.endswith(".txt"):
            content = (await file.read()).decode("utf-8")
        elif file.filename.endswith(".docx"):
            temp_path = "temp_upload.docx"
            with open(temp_path, "wb") as tempf:
                tempf.write(await file.read())
            content = read_docx(temp_path)
            os.remove(temp_path)
        elif file.filename.endswith(".pdf"):
            temp_path = "temp_upload.pdf"
            with open(temp_path, "wb") as tempf:
                tempf.write(await file.read())
            content = read_pdf(temp_path)
            os.remove(temp_path)
        elif file.filename.endswith(".csv"):
            df = pd.read_csv(io.BytesIO(await file.read()))
            content = '\n'.join(df.astype(str).apply(' '.join, axis=1))
        elif file.filename.endswith(".xlsx"):
            df = pd.read_excel(io.BytesIO(await file.read()))
            content = '\n'.join(df.astype(str).apply(' '.join, axis=1))
        if content:
            for chunk in extract_chunks(content):
                new_chunks.append({"content": chunk})
    # 去重
    all_contents = set(item["content"] for item in kb)
    added = 0
    for chunk in new_chunks:
        if chunk["content"] not in all_contents:
            kb.append(chunk)
            all_contents.add(chunk["content"])
            added += 1
    with open(kb_path, "w", encoding="utf-8") as f:
        json.dump(kb, f, ensure_ascii=False, indent=2)
    reload_vector_store()  # 自动重载向量库
    # 记录上传日志
    log_entry = {
        "time": datetime.datetime.now().isoformat(),
        "files": [file.filename for file in files],
        "added_chunks": added
    }
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            logs = json.load(f)
    else:
        logs = []
    logs.append(log_entry)
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)
    return {"msg": f"成功追加{added}条知识片段"}

@app.get("/admin/upload_log")
def get_upload_log():
    log_path = "rag/upload_log.json"
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            logs = json.load(f)
        return logs
    else:
        return []

@app.post("/rag/chat", response_model=ChatResponse)
async def rag_chat(request: ChatRequest):
    session_id = request.session_id or str(uuid.uuid4())
    history = session_history.get(session_id, [])
    # 检索相关文档
    docs = retrieve_relevant_docs(request.question)
    # 构建多轮对话prompt
    context = ""
    for turn in history[-4:]:  # 取最近4轮
        context += f"用户：{turn['question']}\n客服：{turn['answer']}\n"
    context += f"用户：{request.question}\n客服："
    # 生成答案
    answer = generate_answer(context, docs)
    # 存储历史
    history.append({"question": request.question, "answer": answer})
    session_history[session_id] = history
    return ChatResponse(answer=answer, session_id=session_id) 