from agents.base_agent import BaseAgent
from models.base import AIResponse, ServiceType

class LifeServiceAgent(BaseAgent):
    """生活服务AI Agent"""

    def get_service_type(self) -> ServiceType:
        return ServiceType.LIFE_SERVICE

    def get_system_prompt(self) -> str:
        return """你是一个校园生活服务助手，帮助学生了解和使用校园内的生活服务。

你的职责包括：
1. 提供食堂餐饮信息、营业时间和推荐菜品。
2. 解答关于宿舍住宿、维修和管理规定。
3. 提供校园内购物、快递、医疗等服务信息。"""

    def process_response(self, response: str) -> AIResponse:
        """处理LLM的响应"""
        return AIResponse(
            content=response,
            service_type=self.get_service_type().value,
            confidence=0.85,
            suggestions=[
                "食堂今天有什么特色菜？",
                "宿舍晚上几点关门？",
                "最近的快递点在哪里？"
            ]
        ) 