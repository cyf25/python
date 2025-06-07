# 智能日程管理助手/backend/agent.py

import os
import requests
from langchain.llms.base import LLM
from langchain.agents import AgentType, initialize_agent, Tool
from langchain.memory import ConversationBufferMemory
from typing import Optional, List, Mapping, Any
from tools.reminder import reminder_tool
from tools.weather import weather_tool
from tools.calendar import calendar_tool
from config import DEEPSEEK_API_KEY, DEEPSEEK_API_URL

class DeepSeekLLM(LLM):
    @property
    def _llm_type(self) -> str:
        return "deepseek"
    
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0,
            "max_tokens": 2000
        }
        
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

llm = DeepSeekLLM(api_key=DEEPSEEK_API_KEY)

tools = [
    Tool(
        name="Calendar",
        func=calendar_tool,
        description="用于管理日程，支持创建日程（格式：创建日程 [时间] - [描述]）、查询日程（格式：查询日程 [时间]）、列出所有日程"
    ),
    Tool(
        name="Weather",
        func=weather_tool,
        description="用于查询天气，格式：[城市] [日期]，如'北京 明天'"
    ),
    Tool(
        name="Reminder",
        func=reminder_tool,
        description="用于设置和查询提醒，支持'设置提醒 [内容]'和'列出提醒'"
    )
]

memory = ConversationBufferMemory(memory_key="chat_history")
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    memory=memory
)