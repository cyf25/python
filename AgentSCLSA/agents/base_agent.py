from config import config

from models.base import AIResponse, ServiceType, Message
from typing import List, Dict, Any
import logging
from openai import OpenAI
import json

class BaseAgent:
    """AI Agent基类"""
    
    def __init__(self):
        self.client = OpenAI(
            api_key=config.DEEPSEEK_API_KEY,
            base_url=config.DEEPSEEK_BASE_URL
        )
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def get_service_type(self) -> ServiceType:
        """获取服务类型"""
        raise NotImplementedError
    
    def get_system_prompt(self) -> str:
        """获取系统提示"""
        raise NotImplementedError
    
    def process_response(self, response: str) -> AIResponse:
        """处理LLM的响应"""
        return AIResponse(
            content=response,
            service_type=self.get_service_type().value,  # 确保返回枚举值
            confidence=0.85
        )
    
    async def generate_response(self, user_message: str, context: List[Message] = None) -> AIResponse:
        """生成AI响应"""
        try:
            messages = [{"role": "system", "content": self.get_system_prompt()}]
            
            if context:
                for msg in context:
                    messages.append({"role": msg.message_type.value, "content": msg.content})
            
            messages.append({"role": "user", "content": user_message})
            
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                stream=False
            )
            
            ai_message = response.choices[0].message.content
            return self.process_response(ai_message)
            
        except Exception as e:
            self.logger.error(f"生成响应时出错: {str(e)}")
            return AIResponse(
                content="抱歉，处理您的请求时出现错误，请稍后再试。",
                service_type=self.get_service_type().value,  # 确保返回枚举值
                confidence=0.0
            )
    
    def extract_intent(self, user_message: str) -> Dict[str, Any]:
        """提取用户意图"""
        try:
            intent_prompt = f"""
            分析以下用户消息的意图，返回JSON格式：
            用户消息：{user_message}
            
            请返回以下格式的JSON：
            {{
                "intent": "主要意图",
                "entities": ["实体1", "实体2"],
                "confidence": 0.95
            }}
            """
            
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": intent_prompt}],
                temperature=0.3,
                max_tokens=200
            )
            
            intent_text = response.choices[0].message.content
            return json.loads(intent_text)
            
        except Exception as e:
            self.logger.error(f"提取意图时出错: {str(e)}")
            return {
                "intent": "unknown",
                "entities": [],
                "confidence": 0.0
            } 