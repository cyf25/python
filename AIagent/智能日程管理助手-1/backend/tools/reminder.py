import json
import os
from datetime import datetime

# 模拟数据库（实际项目中使用真实数据库）
DB_FILE = "data/reminders.json"
os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)

def load_db():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"reminders": []}

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def reminder_tool(query):
    db = load_db()
    
    if query.startswith("设置提醒"):
        try:
            _, content = query.split("设置提醒", 1)
            content = content.strip()
            
            # 创建提醒
            reminder = {
                "id": len(db["reminders"]) + 1,
                "content": content,
                "created_at": datetime.now().isoformat(),
                "status": "active"
            }
            db["reminders"].append(reminder)
            save_db(db)
            
            return f"⏰ 已设置提醒：{content}"
        except Exception as e:
            return f"❌ 设置提醒失败：{str(e)}。请使用格式'设置提醒 [内容]'"
    
    elif query == "列出提醒":
        active_reminders = [r for r in db["reminders"] if r["status"] == "active"]
        
        if not active_reminders:
            return "⏰ 暂无活跃提醒"
        
        return "\n".join([
            f"✅ {i+1}. {reminder['content']}（创建于{datetime.fromisoformat(reminder['created_at']).strftime('%Y-%m-%d %H:%M')}）"
            for i, reminder in enumerate(active_reminders)
        ])
    
    else:
        return "❌ 不支持的命令。支持：设置提醒、列出提醒"    