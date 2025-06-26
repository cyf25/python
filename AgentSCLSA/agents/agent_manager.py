from agents.course_agent import CourseAgent
from agents.navigation_agent import NavigationAgent
from agents.general_qa_agent import GeneralQAAgent
from agents.activity_agent import ActivityAgent
from agents.life_service_agent import LifeServiceAgent
from agents.study_assistant_agent import StudyAssistantAgent
from models.base import AIResponse, ServiceType, Message
from typing import Dict, List, Any
import logging

class AgentManager:
    """AI Agent管理器"""
    
    def __init__(self):
        self.agents = {
            ServiceType.COURSE: CourseAgent(),
            ServiceType.NAVIGATION: NavigationAgent(),
            ServiceType.GENERAL_QA: GeneralQAAgent(),
            ServiceType.ACTIVITY: ActivityAgent(),
            ServiceType.LIFE_SERVICE: LifeServiceAgent(),
            ServiceType.STUDY_ASSISTANT: StudyAssistantAgent()
        }
        self.logger = logging.getLogger(__name__)
    
    async def route_message(self, user_message: str, context: List[Message] = None) -> AIResponse:
        """路由消息到合适的Agent"""
        try:
            # 优先级1：实体查找。优先检查用户的消息是否能匹配到数据库中的具体实体。
            
            # 尝试查找课程实体
            course_agent = self.agents[ServiceType.COURSE]
            courses = course_agent.course_service.search_courses_by_keywords(user_message)
            if courses:
                return await course_agent.find_course_info(user_message)

            # 尝试查找地点实体
            nav_agent = self.agents[ServiceType.NAVIGATION]
            locations = nav_agent.navigation_service.search_locations_by_keywords(user_message)
            if locations:
                return await nav_agent.find_location(user_message)

            # 优先级2：意图关键字匹配。如果找不到具体实体，则根据关键字判断大致意图。
            intent = self.analyze_intent(user_message)
            agent = self.agents.get(intent.get('service_type'))
            if agent:
                return await agent.generate_response(user_message, context)
            
            # 优先级3：通用问答。如果以上都失败，则交由通用Agent处理。
            return await self.agents[ServiceType.GENERAL_QA].generate_response(user_message, context)
            
        except Exception as e:
            self.logger.error(f"路由消息时出错: {str(e)}")
            return AIResponse(
                content="抱歉，处理您的请求时出现错误，请稍后再试。",
                service_type=ServiceType.GENERAL_QA,
                confidence=0.0
            )
    
    def analyze_intent(self, user_message: str) -> Dict[str, Any]:
        """分析用户意图"""
        message_lower = user_message.lower()
        
        # 课程相关关键词
        course_keywords = [
            '课程', '选课', '学分', '学习', '考试', '作业', '教授', '老师',
            '课程表', '成绩', 'gpa', '选课建议', '学习计划'
        ]
        
        # 导航相关关键词
        navigation_keywords = [
            '在哪里', '怎么去', '路线', '导航', '地图', '位置', '地址',
            '教学楼', '图书馆', '食堂', '宿舍', '体育馆', '医院'
        ]
        
        # 活动相关关键词
        activity_keywords = [
            '活动', '社团', '讲座', '比赛', '演出', '节日', '庆典',
            '志愿者', '社会实践', '实习'
        ]
        
        # 生活服务相关关键词
        life_service_keywords = [
            '食堂', '吃饭', '住宿', '宿舍', '医疗', '银行', '购物',
            '快递', '维修', '服务'
        ]
        
        # 学习助手相关关键词
        study_assistant_keywords = [
            '学习计划', '复习', '考试', '作业', '论文', '研究',
            '学习方法', '时间管理', '效率'
        ]
        
        # 检查关键词匹配
        if any(keyword in message_lower for keyword in course_keywords):
            return {'service_type': ServiceType.COURSE, 'confidence': 0.9}
        
        if any(keyword in message_lower for keyword in navigation_keywords):
            return {'service_type': ServiceType.NAVIGATION, 'confidence': 0.9}
        
        if any(keyword in message_lower for keyword in activity_keywords):
            return {'service_type': ServiceType.ACTIVITY, 'confidence': 0.8}
        
        if any(keyword in message_lower for keyword in life_service_keywords):
            return {'service_type': ServiceType.LIFE_SERVICE, 'confidence': 0.8}
        
        if any(keyword in message_lower for keyword in study_assistant_keywords):
            return {'service_type': ServiceType.STUDY_ASSISTANT, 'confidence': 0.8}
        
        # 默认使用通用问答
        return {'service_type': ServiceType.GENERAL_QA, 'confidence': 0.5}
    
    async def get_course_recommendations(self, user_profile: Dict[str, Any]) -> AIResponse:
        """获取课程推荐"""
        course_agent = self.agents[ServiceType.COURSE]
        return await course_agent.get_course_recommendations(user_profile)
    
    async def find_location(self, location_name: str) -> AIResponse:
        """查找地点"""
        navigation_agent = self.agents[ServiceType.NAVIGATION]
        return await navigation_agent.find_location(location_name)
    
    async def plan_route(self, start_location: str, end_location: str) -> AIResponse:
        """规划路线"""
        navigation_agent = self.agents[ServiceType.NAVIGATION]
        return await navigation_agent.plan_route(start_location, end_location)
    
    async def answer_academic_question(self, question: str, subject: str = None) -> AIResponse:
        """回答学术问题"""
        qa_agent = self.agents[ServiceType.GENERAL_QA]
        return await qa_agent.answer_academic_question(question, subject)
    
    async def provide_life_advice(self, situation: str, category: str = "general") -> AIResponse:
        """提供生活建议"""
        qa_agent = self.agents[ServiceType.GENERAL_QA]
        return await qa_agent.provide_life_advice(situation, category)
    
    async def mental_health_support(self, concern: str) -> AIResponse:
        """心理健康支持"""
        qa_agent = self.agents[ServiceType.GENERAL_QA]
        return await qa_agent.mental_health_support(concern)
    
    async def career_guidance(self, interests: List[str], skills: List[str], goals: str) -> AIResponse:
        """职业规划指导"""
        qa_agent = self.agents[ServiceType.GENERAL_QA]
        return await qa_agent.career_guidance(interests, skills, goals)
    
    def get_available_services(self) -> List[Dict[str, Any]]:
        """获取可用服务列表"""
        services = []
        for service_type, agent in self.agents.items():
            services.append({
                'type': service_type.value,
                'name': self.get_service_name(service_type),
                'description': self.get_service_description(service_type)
            })
        return services
    
    def get_service_name(self, service_type: ServiceType) -> str:
        """获取服务名称"""
        names = {
            ServiceType.COURSE: "课程管理",
            ServiceType.NAVIGATION: "校园导航",
            ServiceType.ACTIVITY: "活动推荐",
            ServiceType.LIFE_SERVICE: "生活服务",
            ServiceType.STUDY_ASSISTANT: "学习助手",
            ServiceType.GENERAL_QA: "智能问答"
        }
        return names.get(service_type, "未知服务")
    
    def get_service_description(self, service_type: ServiceType) -> str:
        """获取服务描述"""
        descriptions = {
            ServiceType.COURSE: "课程查询、选课建议、学习计划制定",
            ServiceType.NAVIGATION: "地点查询、路线规划、校园导航",
            ServiceType.ACTIVITY: "校园活动信息、社团推荐、学术讲座",
            ServiceType.LIFE_SERVICE: "食堂信息、图书馆服务、宿舍管理",
            ServiceType.STUDY_ASSISTANT: "学习计划、复习提醒、进度跟踪",
            ServiceType.GENERAL_QA: "校园政策咨询、学术问题解答、生活建议"
        }
        return descriptions.get(service_type, "未知服务描述") 