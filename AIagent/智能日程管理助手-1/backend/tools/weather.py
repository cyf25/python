import json
import os
from datetime import datetime, timedelta

# 模拟数据库（实际项目中使用真实数据库）
DB_FILE = "data/weather_cache.json"
os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
CACHE_EXPIRATION = 3600  # 1小时

# 模拟天气数据（实际项目中调用真实API）
weather_data = {
    "北京": {
        "2025-06-08": "多云转晴，23℃~31℃，微风",
        "2025-06-09": "雷阵雨转晴，20℃~28℃，南风3-4级",
        "2025-06-10": "晴，25℃~32℃，东风2级"
    },
    "上海": {
        "2025-06-08": "小雨，22℃~26℃，北风2级",
        "2025-06-09": "中雨转多云，21℃~27℃，西北风3级",
        "2025-06-10": "多云，23℃~29℃，东北风2级"
    },
    "广州": {
        "2025-06-08": "晴，26℃~33℃，微风",
        "2025-06-09": "多云，25℃~32℃，南风2级",
        "2025-06-10": "雷阵雨，24℃~30℃，西南风3级"
    }
}

def load_cache():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"cache": {}}

def save_cache(cache_data):
    with open(DB_FILE, "w") as f:
        json.dump(cache_data, f, indent=2)

def parse_date(date_str):
    today = datetime.now()
    if not date_str or "今天" in date_str:
        return today.strftime("%Y-%m-%d")
    elif "明天" in date_str:
        return (today + timedelta(days=1)).strftime("%Y-%m-%d")
    elif "后天" in date_str:
        return (today + timedelta(days=2)).strftime("%Y-%m-%d")
    return date_str

def weather_tool(query):
    # 解析查询参数（城市和日期）
    parts = query.strip().split()
    if len(parts) == 1:
        city, date_str = parts[0], "今天"
    elif len(parts) == 2:
        city, date_str = parts[0], parts[1]
    else:
        return "❌ 请使用格式'[城市] [日期]'，如'北京 明天'"
    
    date = parse_date(date_str)
    
    # 检查缓存
    cache = load_cache()
    cache_key = f"{city}_{date}"
    cached_data = cache["cache"].get(cache_key)
    
    if cached_data and (datetime.now().timestamp() - cached_data["timestamp"] < CACHE_EXPIRATION):
        return f"🌦️ {city} {date_str} 的天气：{cached_data['weather']}（缓存）"
    
    # 从模拟数据获取天气
    city_weather = weather_data.get(city)
    if not city_weather:
        return f"❌ 未找到 {city} 的天气数据"
    
    weather = city_weather.get(date)
    if not weather:
        return f"❌ 未找到 {city} {date_str} 的天气数据"
    
    # 更新缓存
    cache["cache"][cache_key] = {
        "weather": weather,
        "timestamp": datetime.now().timestamp()
    }
    save_cache(cache)
    
    return f"🌦️ {city} {date_str} 的天气：{weather}"    