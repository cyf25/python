import json
import os
from datetime import datetime

# 笔记数据存储文件
DB_FILE = "data/notes.json"
os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)

def load_db():
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"notes": []}

def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def notes_tool(query):
    db = load_db()
    
    if query.startswith("添加笔记"):
        try:
            _, content = query.split("添加笔记", 1)
            content = content.strip()
            
            note = {
                "id": len(db["notes"]) + 1,
                "content": content,
                "created_at": datetime.now().isoformat(),
                "tags": []
            }
            
            db["notes"].append(note)
            save_db(db)
            return f"📝 已添加笔记：{content}"
            
        except Exception as e:
            return f"❌ 添加笔记失败：{str(e)}。请使用格式'添加笔记 [内容]'"
    
    elif query.startswith("搜索笔记"):
        try:
            _, keyword = query.split("搜索笔记", 1)
            keyword = keyword.strip().lower()
            
            matching_notes = [
                f"{note['id']}. {note['content']}"
                for note in db["notes"]
                if keyword in note["content"].lower()
            ]
            
            if not matching_notes:
                return f"🔍 未找到包含'{keyword}'的笔记"
                
            return "找到的笔记：\n" + "\n".join(matching_notes)
            
        except Exception as e:
            return f"❌ 搜索笔记失败：{str(e)}。请使用格式'搜索笔记 [关键词]'"
    
    elif query == "列出所有笔记":
        if not db["notes"]:
            return "📚 暂无任何笔记"
            
        return "\n".join([
            f"{note['id']}. {note['content']}"
            for note in db["notes"]
        ])
    
    elif query.startswith("删除笔记"):
        try:
            _, note_id = query.split("删除笔记", 1)
            note_id = int(note_id.strip())
            
            for i, note in enumerate(db["notes"]):
                if note["id"] == note_id:
                    db["notes"].pop(i)
                    save_db(db)
                    return f"🗑️ 已删除笔记ID {note_id}"
            
            return f"❌ 未找到ID为{note_id}的笔记"
            
        except Exception as e:
            return f"❌ 删除笔记失败：{str(e)}。请使用格式'删除笔记 [ID]'"
    
    else:
        return "❌ 不支持的命令。支持：添加笔记、搜索笔记、列出所有笔记、删除笔记"