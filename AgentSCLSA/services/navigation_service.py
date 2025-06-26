from models.base import Location
from typing import List, Dict, Any, Optional
import sqlite3
import os
import math
import csv

class NavigationService:
    """导航服务类"""
    
    def __init__(self):
        self.db_path = "data/campus_assistant.db"
        self.init_database()
        self.load_sample_data()
    
    def init_database(self):
        """初始化数据库"""
        os.makedirs("data", exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建地点表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS locations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                coordinates TEXT,
                address TEXT NOT NULL,
                opening_hours TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def load_sample_data(self):
        """加载示例数据"""
        csv_file = os.path.join("data", "locations.csv")
        if not os.path.exists(csv_file):
            print(f"警告: {csv_file} 文件未找到，无法加载地点数据。")
            return

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 检查表中是否已有数据
        cursor.execute("SELECT COUNT(*) FROM locations")
        if cursor.fetchone()[0] > 0:
            conn.close()
            return

        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    # 对于坐标中的双引号，CSV阅读器会自动处理，无需特殊操作
                    coordinates = row["coordinates"] if row["coordinates"] else None
                    cursor.execute('''
                        INSERT OR IGNORE INTO locations
                        (name, category, description, coordinates, address, opening_hours)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        row["name"], row["category"], row["description"],
                        coordinates, row["address"], row["opening_hours"]
                    ))
                except KeyError as e:
                    print(f"警告: 处理地点CSV文件行时出错: {row}. 错误: {e}")

        conn.commit()
        conn.close()
    
    def get_all_locations(self) -> List[Location]:
        """获取所有地点"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM locations')
        rows = cursor.fetchall()
        
        locations = []
        for row in rows:
            location = Location(
                id=str(row[0]),
                name=row[1],
                category=row[2],
                description=row[3],
                coordinates=eval(row[4]) if row[4] else None,
                address=row[5],
                opening_hours=row[6]
            )
            locations.append(location)
        
        conn.close()
        return locations
    
    def get_location_by_name(self, name: str) -> Optional[Location]:
        """根据名称获取地点"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM locations WHERE name = ?', (name,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return Location(
                id=str(row[0]),
                name=row[1],
                category=row[2],
                description=row[3],
                coordinates=eval(row[4]) if row[4] else None,
                address=row[5],
                opening_hours=row[6]
            )
        return None
    
    def search_locations_by_keywords(self, keywords: str) -> List[Location]:
        """根据关键词搜索地点"""
        all_locations = self.get_all_locations()
        keywords_lower = keywords.lower()
        
        matched_locations = []
        for location in all_locations:
            if (location.name.lower() in keywords_lower or
                location.category.lower() in keywords_lower or
                location.address.lower() in keywords_lower):
                matched_locations.append(location)
        
        return matched_locations
    
    def get_locations_by_category(self, category: str) -> List[Location]:
        """根据类别获取地点"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM locations WHERE category = ?', (category,))
        rows = cursor.fetchall()
        
        locations = []
        for row in rows:
            location = Location(
                id=str(row[0]),
                name=row[1],
                category=row[2],
                description=row[3],
                coordinates=eval(row[4]) if row[4] else None,
                address=row[5],
                opening_hours=row[6]
            )
            locations.append(location)
        
        conn.close()
        return locations
    
    def calculate_distance(self, loc1: Location, loc2: Location) -> float:
        """计算两个地点之间的距离（简化版，使用欧几里得距离）"""
        if not loc1.coordinates or not loc2.coordinates:
            return float('inf')
        
        lat1, lng1 = loc1.coordinates['lat'], loc1.coordinates['lng']
        lat2, lng2 = loc2.coordinates['lat'], loc2.coordinates['lng']
        
        # 简化的距离计算（实际应用中应使用更精确的公式）
        distance = math.sqrt((lat2 - lat1) ** 2 + (lng2 - lng1) ** 2)
        return distance * 111000  # 转换为米（粗略估算）
    
    def get_route(self, start_location: Location, end_location: Location) -> Dict[str, Any]:
        """获取路线信息"""
        distance = self.calculate_distance(start_location, end_location)
        
        # 简化的路线规划
        route_info = {
            "start": start_location.name,
            "end": end_location.name,
            "distance": f"{distance:.0f}米",
            "estimated_time": f"{int(distance / 80)}分钟",  # 假设步行速度80米/分钟
            "route_type": "步行",
            "steps": [
                f"从{start_location.name}出发",
                f"沿着校园道路前往{end_location.name}",
                f"到达{end_location.name}"
            ]
        }
        
        return route_info
    
    def get_nearby_facilities(self, center_location: Location, facility_type: str = None) -> List[Location]:
        """获取附近设施"""
        all_locations = self.get_all_locations()
        nearby_facilities = []
        
        for location in all_locations:
            if location.id == center_location.id:
                continue
            
            if facility_type and location.category != facility_type:
                continue
            
            distance = self.calculate_distance(center_location, location)
            if distance <= 500:  # 500米范围内
                nearby_facilities.append(location)
        
        # 按距离排序
        nearby_facilities.sort(key=lambda x: self.calculate_distance(center_location, x))
        return nearby_facilities[:5]  # 返回最近的5个设施 