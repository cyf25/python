from datetime import datetime
import json
import os

# 任务数据库文件
DB_FILE = "data/tasks.json"
os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)

def load_db():
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"tasks": []}

def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def task_tool(query):
    db = load_db()
    
    if query.startswith("创建任务"):
        try:
            _, content = query.split("创建任务", 1)
            content = content.strip()
            
            # 解析优先级 (高/中/低)
            priority = "中"
            if "优先级高" in content:
                priority = "高"
                content = content.replace("优先级高", "").strip()
            elif "优先级低" in content:
                priority = "低" 
                content = content.replace("优先级低", "").strip()
                
            task = {
                "id": len(db["tasks"]) + 1,
                "content": content,
                "priority": priority,
                "completed": False,
                "created_at": datetime.now().isoformat()
            }
            db["tasks"].append(task)
            save_db(db)
            
            return f"✅ 已创建任务(ID:{task['id']}): {content} (优先级:{priority})"
            
        except Exception as e:
            return f"❌ 创建任务失败: {str(e)}。格式: '创建任务 [内容] [优先级高/低]'"
            
    elif query.startswith("完成任务"):
        try:
            _, task_id = query.split("完成任务", 1)
            task_id = int(task_id.strip())
            
            for task in db["tasks"]:
                if task["id"] == task_id:
                    task["completed"] = True
                    task["completed_at"] = datetime.now().isoformat()
                    save_db(db)
                    return f"✅ 已完成任务(ID:{task_id}): {task['content']}"
                    
            return f"❌ 未找到任务ID: {task_id}"
            
        except Exception as e:
            return f"❌ 完成任务失败: {str(e)}。格式: '完成任务 [ID]'"
            
    elif query.startswith("列出任务"):
        filter_type = "全部"
        if "未完成" in query:
            filter_type = "未完成"
        elif "已完成" in query:
            filter_type = "已完成"
        elif "优先级高" in query:
            filter_type = "高优先级"
            
        tasks = []
        if filter_type == "全部":
            tasks = db["tasks"]
        elif filter_type == "未完成":
            tasks = [t for t in db["tasks"] if not t["completed"]]
        elif filter_type == "已完成":
            tasks = [t for t in db["tasks"] if t["completed"]]
        elif filter_type == "高优先级":
            tasks = [t for t in db["tasks"] if t["priority"] == "高"]
            
        if not tasks:
            return f"📝 无{filter_type}任务"
            
        return "\n".join([
            f"✅ {t['id']}. [{'✓' if t['completed'] else ' '}] {t['content']} (优先级:{t['priority']})"
            for t in sorted(tasks, key=lambda x: x["id"])
        ])
        
    else:
        return "❌ 不支持的命令。支持: 创建任务, 完成任务, 列出任务"