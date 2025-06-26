from models.base import Course, StudyPlan
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import json
import sqlite3
import os
import csv

class CourseService:
    """课程服务类"""
    
    def __init__(self):
        self.db_path = "data/campus_assistant.db"
        self.init_database()
        self.load_sample_data()
    
    def init_database(self):
        """初始化数据库"""
        os.makedirs("data", exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建课程表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                credits INTEGER NOT NULL,
                instructor TEXT NOT NULL,
                schedule TEXT NOT NULL,
                location TEXT NOT NULL,
                description TEXT,
                capacity INTEGER NOT NULL,
                enrolled INTEGER DEFAULT 0
            )
        ''')
        
        # 创建学习计划表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS study_plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                tasks TEXT,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                progress REAL DEFAULT 0.0,
                status TEXT DEFAULT 'active'
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def load_sample_data(self):
        """加载示例数据"""
        csv_file = os.path.join("data", "courses.csv")
        if not os.path.exists(csv_file):
            print(f"警告: {csv_file} 文件未找到，无法加载课程数据。")
            return

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 检查表中是否已有数据
        cursor.execute("SELECT COUNT(*) FROM courses")
        if cursor.fetchone()[0] > 0:
            conn.close()
            return

        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    cursor.execute('''
                        INSERT OR IGNORE INTO courses
                        (code, name, credits, instructor, schedule, location, description, capacity, enrolled)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        row["code"], row["name"], int(row["credits"]), row["instructor"],
                        row["schedule"], row["location"], row["description"],
                        int(row["capacity"]), int(row["enrolled"])
                    ))
                except (KeyError, ValueError) as e:
                    print(f"警告: 处理课程CSV文件行时出错: {row}. 错误: {e}")

        conn.commit()
        conn.close()
    
    def get_all_courses(self) -> List[Course]:
        """获取所有课程"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM courses')
        rows = cursor.fetchall()
        
        courses = []
        for row in rows:
            course = Course(
                id=str(row[0]),
                code=row[1],
                name=row[2],
                credits=row[3],
                instructor=row[4],
                schedule=row[5],
                location=row[6],
                description=row[7],
                capacity=row[8],
                enrolled=row[9]
            )
            courses.append(course)
        
        conn.close()
        return courses
    
    def search_courses_by_keywords(self, keywords: str) -> List[Course]:
        """根据关键词搜索课程"""
        all_courses = self.get_all_courses()
        keywords_lower = keywords.lower()
        
        matched_courses = []
        for course in all_courses:
            if (course.name.lower() in keywords_lower or
                course.code.lower() in keywords_lower or
                course.instructor.lower() in keywords_lower):
                matched_courses.append(course)
        
        return matched_courses
    
    def get_course_by_code(self, code: str) -> Optional[Course]:
        """根据课程代码获取课程"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM courses WHERE code = ?', (code,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return Course(
                id=str(row[0]),
                code=row[1],
                name=row[2],
                credits=row[3],
                instructor=row[4],
                schedule=row[5],
                location=row[6],
                description=row[7],
                capacity=row[8],
                enrolled=row[9]
            )
        return None
    
    def get_recommended_courses(self, user_profile: Dict[str, Any]) -> List[Course]:
        """获取推荐课程"""
        all_courses = self.get_all_courses()
        major = user_profile.get('major', '').lower()
        interests = [interest.lower() for interest in user_profile.get('interests', [])]
        
        # 简单的推荐逻辑
        recommended = []
        for course in all_courses:
            score = 0
            
            # 根据专业匹配
            if major in course.name.lower() or major in course.description.lower():
                score += 3
            
            # 根据兴趣匹配
            for interest in interests:
                if interest in course.name.lower() or interest in course.description.lower():
                    score += 2
            
            # 根据课程容量
            if course.enrolled < course.capacity * 0.8:
                score += 1
            
            if score > 0:
                recommended.append((course, score))
        
        # 按分数排序
        recommended.sort(key=lambda x: x[1], reverse=True)
        return [course for course, score in recommended[:5]]
    
    def create_study_plan(self, user_id: str, goals: List[str]) -> Optional[StudyPlan]:
        """创建学习计划"""
        try:
            # 生成任务列表
            tasks = []
            for i, goal in enumerate(goals):
                tasks.append({
                    "id": i + 1,
                    "title": f"目标{i + 1}: {goal}",
                    "description": f"完成{goal}相关的学习和实践",
                    "status": "pending",
                    "deadline": (datetime.now() + timedelta(days=30 * (i + 1))).isoformat()
                })
            
            study_plan = StudyPlan(
                user_id=user_id,
                title=f"学习计划 - {datetime.now().strftime('%Y-%m-%d')}",
                description=f"基于目标: {', '.join(goals)}",
                tasks=tasks,
                start_date=datetime.now(),
                end_date=datetime.now() + timedelta(days=90),
                progress=0.0,
                status="active"
            )
            
            # 保存到数据库
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO study_plans 
                (user_id, title, description, tasks, start_date, end_date, progress, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                study_plan.user_id,
                study_plan.title,
                study_plan.description,
                json.dumps(study_plan.tasks),
                study_plan.start_date.isoformat(),
                study_plan.end_date.isoformat(),
                study_plan.progress,
                study_plan.status
            ))
            
            study_plan.id = str(cursor.lastrowid)
            conn.commit()
            conn.close()
            
            return study_plan
            
        except Exception as e:
            print(f"创建学习计划时出错: {str(e)}")
            return None
    
    def get_user_study_plans(self, user_id: str) -> List[StudyPlan]:
        """获取用户的学习计划"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM study_plans WHERE user_id = ?', (user_id,))
        rows = cursor.fetchall()
        
        study_plans = []
        for row in rows:
            study_plan = StudyPlan(
                id=str(row[0]),
                user_id=row[1],
                title=row[2],
                description=row[3],
                tasks=json.loads(row[4]) if row[4] else [],
                start_date=datetime.fromisoformat(row[5]),
                end_date=datetime.fromisoformat(row[6]),
                progress=row[7],
                status=row[8]
            )
            study_plans.append(study_plan)
        
        conn.close()
        return study_plans 