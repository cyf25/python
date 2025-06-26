from datetime import datetime
import json
import os
from .calendar import parse_date  # 复用日历的日期解析

# 会议数据库文件
DB_FILE = "data/meetings.json"
os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)

def load_db():
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"meetings": []}

def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def meeting_tool(query):
    db = load_db()
    
    if query.startswith("创建会议"):
        try:
            _, content = query.split("创建会议", 1)
            content = content.strip()
            
            # 解析格式: [时间] [地点] - [描述] @[参与人]
            parts = content.split(" - ")
            if len(parts) != 2:
                raise ValueError("缺少描述部分")
                
            time_place, description = parts
            time_place_parts = time_place.split(" ")
            if len(time_place_parts) < 2:
                raise ValueError("缺少地点信息")
                
            time_part = " ".join(time_place_parts[:-1])
            place = time_place_parts[-1]
            
            # 解析参与人
            participants = []
            if "@" in description:
                desc_part, people_part = description.split("@", 1)
                description = desc_part.strip()
                participants = [p.strip() for p in people_part.split(",")]
            
            # 解析时间
            parsed_time = parse_date(time_part)
            
            meeting = {
                "id": len(db["meetings"]) + 1,
                "time": parsed_time,
                "place": place,
                "description": description,
                "participants": participants,
                "status": "已安排",
                "created_at": datetime.now().isoformat()
            }
            db["meetings"].append(meeting)
            save_db(db)
            
            return (f"✅ 已创建会议(ID:{meeting['id']}):\n"
                   f"时间: {parsed_time}\n"
                   f"地点: {place}\n"
                   f"描述: {description}\n"
                   f"参与人: {', '.join(participants) if participants else '无'}")
                   
        except Exception as e:
            return f"❌ 创建会议失败: {str(e)}。格式: '创建会议 [时间] [地点] - [描述] @[参与人1,参与人2]'"
            
    elif query.startswith("取消会议"):
        try:
            _, meeting_id = query.split("取消会议", 1)
            meeting_id = int(meeting_id.strip())
            
            for meeting in db["meetings"]:
                if meeting["id"] == meeting_id:
                    meeting["status"] = "已取消"
                    meeting["canceled_at"] = datetime.now().isoformat()
                    save_db(db)
                    return f"✅ 已取消会议(ID:{meeting_id}): {meeting['description']}"
                    
            return f"❌ 未找到会议ID: {meeting_id}"
            
        except Exception as e:
            return f"❌ 取消会议失败: {str(e)}。格式: '取消会议 [ID]'"
            
    elif query.startswith("查询会议"):
        try:
            _, date_part = query.split("查询会议", 1)
            date_part = date_part.strip() or "今天"
            parsed_date = parse_date(date_part)
            
            meetings = [
                m for m in db["meetings"] 
                if parsed_date in m["time"] and m["status"] == "已安排"
            ]
            
            if not meetings:
                return f"📅 {parsed_date} 暂无会议安排"
                
            return "\n".join([
                f"✅ {m['id']}. {m['time']} {m['place']} - {m['description']} "
                f"(参与人: {', '.join(m['participants']) if m['participants'] else '无'})"
                for m in meetings
            ])
            
        except Exception as e:
            return f"❌ 查询会议失败: {str(e)}。格式: '查询会议 [日期]'"
            
    elif query == "列出所有会议":
        if not db["meetings"]:
            return "📅 暂无任何会议安排"
            
        return "\n".join([
            f"✅ {m['id']}. [{m['status']}] {m['time']} {m['place']} - {m['description']}"
            for m in db["meetings"]
        ])
        
    else:
        return "❌ 不支持的命令。支持: 创建会议, 取消会议, 查询会议, 列出所有会议"