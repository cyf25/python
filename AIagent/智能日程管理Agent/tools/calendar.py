from datetime import datetime,timedelta
import json
import os
#建立数据库存储日历数据
DB_FILE="data/calendar.json"
os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)#创建文件夹
#数据库操作-加载保存
def load_db():
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)#读取json文件
    except:
        return {"events": []}
#数据库操作-保存
def save_db(data):
    with open(DB_FILE,'W',encoding='utf-8')as f:
        json.dump(data,f,ensure_ascii=False,indent=2)#写入json文件
# 定义一个函数，用于解析日期字符串
def parse_date(date_str):
    today=datetime.now()
    if "今天"in date_str:
        return today.strftime("%Y-%m-%d")
    elif "明天" in date_str:
        return(today+timedelta(days=1)).strftime("%Y-%m-%d")#日期加一天
    elif "后天" in date_str:
        return(today+timedelta(days=2)).strftime("%Y-%m-%d")#日期加两天
    return date_str
#日程创建流程
def calendar_tool(query):
    db = load_db()  # 加载数据库
    if query.startswith("创建日程"):
        try:
            _, content = query.split("创建日程", 1)
            content = content.strip()
            time_part, desc_part = content.split(" - ", 1)
            
            # 解析时间
            parsed_time = parse_date(time_part)
            
            # 添加事件
            event = {
                "id": len(db["events"]) + 1,
                "time": parsed_time,
                "description": desc_part,
                "created_at": datetime.now().isoformat()
            }
            db["events"].append(event)
            save_db(db)
            
            return f"✅ 已创建日程：{parsed_time} - {desc_part}"
        except Exception as e:
            return f"❌ 创建日程失败：{str(e)}。请使用格式'创建日程 [时间] - [描述]'"
    elif query.startswith("查询日程"):
        try:
            _, date_part = query.split("查询日程", 1)
            date_part = date_part.strip() or "今天"
            parsed_date = parse_date(date_part)
            
            # 查找匹配的日程
            matching_events = [
                f"{event['time']} - {event['description']}"
                for event in db["events"]
                if parsed_date in event["time"]
            ]
            
            if not matching_events:
                return f"📅 {parsed_date} 暂无日程"
            
            return "\n".join([f"✅ {i+1}. {event}" for i, event in enumerate(matching_events)])
        except Exception as e:
            return f"❌ 查询日程失败：{str(e)}。请使用格式'查询日程 [时间]'"
    
    elif query == "列出所有日程":
        if not db["events"]:
            return "📅 暂无任何日程"
        
        return "\n".join([
            f"✅ {i+1}. {event['time']} - {event['description']}"
            for i, event in enumerate(db["events"])
        ])
    
    else:
        return "❌ 不支持的命令。支持：创建日程、查询日程、列出所有日程"    
