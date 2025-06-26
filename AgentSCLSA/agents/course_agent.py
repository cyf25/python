from agents.base_agent import BaseAgent
from models.base import AIResponse, ServiceType
from services.course_service import CourseService
from typing import List, Dict, Any
import json

class CourseAgent(BaseAgent):
    """课程管理AI Agent"""
    
    def __init__(self):
        super().__init__()
        self.course_service = CourseService()
    
    def get_service_type(self) -> ServiceType:
        return ServiceType.COURSE
    
    def get_system_prompt(self) -> str:
        return """你是一个专业的课程管理助手，专门帮助学生处理课程相关的问题。

你的主要职责包括：
1. 课程查询和推荐
2. 选课建议
3. 学习计划制定
4. 课程时间安排
5. 学分管理

请用友好、专业的语气回答学生的问题，并提供实用的建议。"""
    
    def process_response(self, response: str) -> AIResponse:
        # 尝试从响应中提取课程信息
        courses = self.course_service.search_courses_by_keywords(response)
        
        metadata = {
            "courses": [course.dict() for course in courses[:3]] if courses else [],
            "total_courses": len(courses) if courses else 0
        }
        
        suggestions = [
            "查看所有可用课程",
            "获取选课建议",
            "制定学习计划",
            "查看课程时间表"
        ]
        
        return AIResponse(
            content=response,
            service_type=self.get_service_type(),
            confidence=0.85,
            metadata=metadata,
            suggestions=suggestions
        )
    
    async def find_course_info(self, course_name: str) -> AIResponse:
        """查找特定课程的信息"""
        try:
            # 使用服务层按关键词搜索，因为用户可能只输入部分名称
            courses = self.course_service.search_courses_by_keywords(course_name)
            
            if courses:
                # 假设我们只关注最匹配的第一个结果
                course = courses[0]
                
                prompt = f"""
                你是一个课程查询助手。
                你的任务是根据我提供的精确数据，为用户提供课程的详细信息。
                **你必须且只能使用下面 "=====" 分隔符内的数据来回答，严禁使用任何外部知识或自己数据库里的信息。**

                =====
                课程代码: {course.code}
                课程名称: {course.name}
                学分: {course.credits}
                授课教师: {course.instructor}
                上课时间: {course.schedule}
                上课地点: {course.location}
                课程描述: {course.description}
                =====

                请根据以上信息，清晰地回答用户关于"{course_name}"这门课的问题。
                例如，如果用户问上课时间，你就只回答上课时间。如果用户问授课老师，就回答老师信息。
                直接、准确地从提供的数据中提取并呈现信息。
                """
                response = await self.generate_response(prompt)
                response.metadata = {"course": course.dict()}
            else:
                response = AIResponse(
                    content=f'抱歉，没有在课程列表中找到名为"{course_name}"的课程。请检查课程名称是否正确。',
                    service_type=self.get_service_type(),
                    confidence=0.0
                )
            
            return response
            
        except Exception as e:
            self.logger.error(f"查找课程信息时出错: {str(e)}")
            return AIResponse(
                content="抱歉，查找课程信息时出现错误，请稍后再试。",
                service_type=self.get_service_type(),
                confidence=0.0
            )
    
    async def get_course_recommendations(self, user_profile: Dict[str, Any]) -> AIResponse:
        """获取课程推荐"""
        try:
            prompt = f"""
            基于以下学生信息，推荐合适的课程：
            
            专业：{user_profile.get('major', '未知')}
            年级：{user_profile.get('grade', '未知')}
            兴趣：{user_profile.get('interests', [])}
            已修学分：{user_profile.get('credits_earned', 0)}
            
            请推荐3-5门课程，并说明推荐理由。
            """
            
            response = await self.generate_response(prompt)
            
            # 获取推荐课程的具体信息
            recommended_courses = self.course_service.get_recommended_courses(user_profile)
            
            response.metadata = {
                "recommended_courses": [course.dict() for course in recommended_courses],
                "user_profile": user_profile
            }
            
            return response
            
        except Exception as e:
            self.logger.error(f"获取课程推荐时出错: {str(e)}")
            return AIResponse(
                content="抱歉，无法获取课程推荐，请稍后再试。",
                service_type=self.get_service_type(),
                confidence=0.0
            )
    
    async def create_study_plan(self, user_id: str, goals: List[str]) -> AIResponse:
        """制定学习计划"""
        try:
            prompt = f"""
            为学生制定一个详细的学习计划：
            
            学习目标：{', '.join(goals)}
            
            请制定一个包含以下内容的计划：
            1. 短期目标（1-2个月）
            2. 中期目标（3-6个月）
            3. 长期目标（1年）
            4. 具体的学习任务和时间安排
            5. 学习方法和建议
            """
            
            response = await self.generate_response(prompt)
            
            # 创建学习计划
            study_plan = self.course_service.create_study_plan(user_id, goals)
            
            response.metadata = {
                "study_plan": study_plan.dict() if study_plan else None
            }
            
            return response
            
        except Exception as e:
            self.logger.error(f"制定学习计划时出错: {str(e)}")
            return AIResponse(
                content="抱歉，无法制定学习计划，请稍后再试。",
                service_type=self.get_service_type(),
                confidence=0.0
            ) 