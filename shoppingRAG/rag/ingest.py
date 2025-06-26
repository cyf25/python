import os
import json
from docx import Document
import PyPDF2
import pandas as pd

def read_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def read_docx(file_path):
    doc = Document(file_path)
    return '\n'.join([para.text for para in doc.paragraphs])

def read_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def read_csv(file_path):
    df = pd.read_csv(file_path)
    return '\n'.join(df.astype(str).apply(' '.join, axis=1))

def read_xlsx(file_path):
    df = pd.read_excel(file_path)
    return '\n'.join(df.astype(str).apply(' '.join, axis=1))

def extract_chunks(text, chunk_size=200):
    paras = [p.strip() for p in text.split('\n') if p.strip()]
    chunks = []
    chunk = ""
    for para in paras:
        if len(chunk) + len(para) < chunk_size:
            chunk += para + " "
        else:
            chunks.append(chunk.strip())
            chunk = para + " "
    if chunk:
        chunks.append(chunk.strip())
    return chunks

def ingest_folder(folder, output_json):
    kb = []
    for fname in os.listdir(folder):
        fpath = os.path.join(folder, fname)
        if fname.endswith('.txt'):
            text = read_txt(fpath)
        elif fname.endswith('.docx'):
            text = read_docx(fpath)
        elif fname.endswith('.pdf'):
            text = read_pdf(fpath)
        elif fname.endswith('.csv'):
            text = read_csv(fpath)
        elif fname.endswith('.xlsx'):
            text = read_xlsx(fpath)
        else:
            continue
        for chunk in extract_chunks(text):
            kb.append({"content": chunk})
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(kb, f, ensure_ascii=False, indent=2)
    print(f"已导入知识库，共{len(kb)}条。")

if __name__ == '__main__':
    raw_folder = os.path.join(os.path.dirname(__file__), 'data', 'raw_docs')
    output_json = os.path.join(os.path.dirname(__file__), 'data', 'knowledge_base.json')
    ingest_folder(raw_folder, output_json) 