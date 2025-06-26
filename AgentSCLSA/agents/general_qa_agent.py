from agents.base_agent import BaseAgent
from models.base import AIResponse, ServiceType
from typing import List, Dict, Any
import json

class GeneralQAAgent(BaseAgent):
    """通用问答AI Agent"""
    
    def __init__(self):
        super().__init__()
    
    def get_service_type(self) -> ServiceType:
        return ServiceType.GENERAL_QA
    
    def get_system_prompt(self) -> str:
        return """你是一个专业的校园生活服务智能助手，专门帮助大学生解决各种校园生活问题。

你的主要职责包括：
1. 校园政策咨询和解答
2. 学术问题指导
3. 生活常识问答
4. 心理健康支持
5. 职业规划建议
6. 社交关系指导

请用友好、耐心、专业的语气回答学生的问题，提供实用的建议和解决方案。
注意保护学生隐私，对于敏感问题要谨慎处理。"""
    
    def process_response(self, response: str) -> AIResponse:
        suggestions = [
            "查看校园政策",
            "获取学习建议",
            "生活服务咨询",
            "心理健康支持",
            "职业规划指导"
        ]
        
        return AIResponse(
            content=response,
            service_type=self.get_service_type().value,
            confidence=0.80,
            suggestions=suggestions
        )
    
    async def answer_academic_question(self, question: str, subject: str = None) -> AIResponse:
        """回答学术问题"""
        try:
            prompt = f"""
            请回答以下学术问题：
            
            问题：{question}
            学科：{subject or '通用'}
            
            请提供：
            1. 详细的解答
            2. 相关的知识点
            3. 学习建议
            4. 参考资料（如果有）
            """
            
            return await self.generate_response(prompt)
            
        except Exception as e:
            self.logger.error(f"回答学术问题时出错: {str(e)}")
            return AIResponse(
                content="抱歉，无法回答您的学术问题，请稍后再试。",
                service_type=self.get_service_type(),
                confidence=0.0
            )
    
    async def provide_life_advice(self, situation: str, category: str = "general") -> AIResponse:
        """提供生活建议"""
        try:
            prompt = f"""
            请为以下生活情况提供建议：
            
            情况描述：{situation}
            建议类别：{category}
            
            请提供：
            1. 问题分析
            2. 具体建议
            3. 注意事项
            4. 相关资源
            """
            
            return await self.generate_response(prompt)
            
        except Exception as e:
            self.logger.error(f"提供生活建议时出错: {str(e)}")
            return AIResponse(
                content="抱歉，无法提供生活建议，请稍后再试。",
                service_type=self.get_service_type(),
                confidence=0.0
            )
    
    async def mental_health_support(self, concern: str) -> AIResponse:
        """心理健康支持"""
        try:
            prompt = f"""
            请为以下心理健康问题提供支持和建议：
            
            问题描述：{concern}
            
            请提供：
            1. 情感支持
            2. 应对策略
            3. 专业资源推荐
            4. 注意事项
            
            注意：如果问题严重，请建议寻求专业心理咨询师的帮助。
            """
            
            response = await self.generate_response(prompt)
            
            # 添加心理健康资源
            response.metadata = {
                "mental_health_resources": [
                    "校园心理咨询中心",
                    "心理健康热线",
                    "专业心理咨询师"
                ]
            }
            
            return response
            
        except Exception as e:
            self.logger.error(f"心理健康支持时出错: {str(e)}")
            return AIResponse(
                content="如果您正在经历心理健康问题，建议您联系校园心理咨询中心或寻求专业帮助。",
                service_type=self.get_service_type(),
                confidence=0.0
            )
    
    async def career_guidance(self, interests: List[str], skills: List[str], goals: str) -> AIResponse:
        """职业规划指导"""
        try:
            prompt = f"""
            请为以下学生提供职业规划指导：
            
            兴趣：{', '.join(interests)}
            技能：{', '.join(skills)}
            职业目标：{goals}
            
            请提供：
            1. 职业方向分析
            2. 技能发展建议
            3. 学习路径规划
            4. 实习和就业建议
            5. 行业发展趋势
            """
            
            response = await self.generate_response(prompt)
            
            # 添加职业发展资源
            response.metadata = {
                "career_resources": [
                    "职业发展中心",
                    "实习机会平台",
                    "技能培训课程",
                    "行业交流活动"
                ]
            }
            
            return response
            
        except Exception as e:
            self.logger.error(f"职业规划指导时出错: {str(e)}")
            return AIResponse(
                content="抱歉，无法提供职业规划指导，请稍后再试。",
                service_type=self.get_service_type(),
                confidence=0.0
            ) 