from agents.base_agent import BaseAgent
from models.base import AIResponse, ServiceType

class ActivityAgent(BaseAgent):
    """校园活动AI Agent"""

    def get_service_type(self) -> ServiceType:
        return ServiceType.ACTIVITY

    def get_system_prompt(self) -> str:
        return """你是一个校园活动助手，帮助学生发现和参与校园活动。

你的职责包括：
1. 提供最新的校园活动信息（讲座、社团、比赛等）。
2. 根据学生的兴趣推荐活动。
3. 解答关于活动细节（时间、地点、报名方式）的问题。"""

    def process_response(self, response: str) -> AIResponse:
        """处理LLM的响应"""
        return AIResponse(
            content=response,
            service_type=self.get_service_type().value,
            confidence=0.85,
            suggestions=[
                "最近有什么讲座？",
                "推荐一些有趣的社团",
                "如何报名参加志愿者活动？"
            ]
        ) 