from agents.base_agent import BaseAgent
from models.base import AIResponse, ServiceType

class StudyAssistantAgent(BaseAgent):
    """学习助手AI Agent"""

    def get_service_type(self) -> ServiceType:
        return ServiceType.STUDY_ASSISTANT

    def get_system_prompt(self) -> str:
        return """你是一个学习助手，帮助学生规划学习、准备考试和提高效率。

你的职责包括：
1. 帮助制定学习计划和复习时间表。
2. 提供学习方法和时间管理技巧。
3. 解答关于作业、论文和研究的问题。"""

    def process_response(self, response: str) -> AIResponse:
        """处理LLM的响应"""
        return AIResponse(
            content=response,
            service_type=self.get_service_type().value,
            confidence=0.85,
            suggestions=[
                "帮我制定一个期末复习计划",
                "如何提高专注力？",
                "写论文需要注意什么？"
            ]
        ) 