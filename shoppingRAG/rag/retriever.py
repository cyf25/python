import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import re

# 加载嵌入模型
EMBEDDING_MODEL = SentenceTransformer('all-MiniLM-L6-v2')

DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'knowledge_base.json')

# 全局变量
KB = []#知识库
DOCS = []#文档
DOC_EMBEDS = None#文档嵌入
INDEX = None#索引

def load_knowledge_base():
    global KB, DOCS, DOC_EMBEDS, INDEX
    
    # 确保data目录存在
    data_dir = os.path.dirname(DATA_PATH)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"✓ 创建数据目录: {data_dir}")
    
    # 检查知识库文件是否存在
    if os.path.exists(DATA_PATH):
        try:
            with open(DATA_PATH, 'r', encoding='utf-8') as f:
                KB = json.load(f)
            print(f"✓ 加载知识库: {len(KB)} 条记录")
        except Exception as e:
            print(f"⚠ 加载知识库失败: {e}")
            KB = []
    else:
        # 文件不存在，创建空的知识库
        KB = []
        try:
            with open(DATA_PATH, 'w', encoding='utf-8') as f:
                json.dump(KB, f, ensure_ascii=False, indent=2)
            print(f"✓ 创建空知识库文件: {DATA_PATH}")
        except Exception as e:
            print(f"⚠ 创建知识库文件失败: {e}")
    
    DOCS = [item['content'] for item in KB]
    if DOCS:
        DOC_EMBEDS = EMBEDDING_MODEL.encode(DOCS, convert_to_numpy=True)
        INDEX = faiss.IndexFlatL2(DOC_EMBEDS.shape[1])
        INDEX.add(DOC_EMBEDS)
        print(f"✓ 构建向量索引: {len(DOCS)} 个文档")
    else:
        DOC_EMBEDS = None
        INDEX = None
        print("ℹ 知识库为空，向量索引未构建")

# 初始化加载
load_knowledge_base()

def reload_vector_store():
    load_knowledge_base()

def keyword_search(query, docs):
    # 支持字母+数字的快递单号/订单号（长度6位及以上）
    order_pattern = re.compile(r'\b[A-Za-z0-9]{6,}\b')
    keywords = order_pattern.findall(query)
    if not keywords:
        return []
    results = []
    for doc in docs:
        if any(k in doc for k in keywords):
            results.append(doc)
    return results

def retrieve_relevant_docs(query, top_k=10):
    # 先关键词精确查找
    keyword_hits = keyword_search(query, DOCS)
    if keyword_hits:
        return keyword_hits[:top_k]
    # 再语义检索
    if not INDEX or not DOCS:
        return []
    query_vec = EMBEDDING_MODEL.encode([query], convert_to_numpy=True)
    D, I = INDEX.search(query_vec, top_k)
    return [DOCS[i] for i in I[0]] 