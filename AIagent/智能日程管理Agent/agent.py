import os
import requests
from langchain.llms.base import LLM
from langchain.agents import AgentType, initialize_agent, Tool
from langchain.memory import ConversationBufferMemory
from typing import Optional, List, Mapping, Any
from tools.reminder import reminder_tool
from tools.weather import weather_tool
from tools.calendar import calendar_tool
from tools.task import task_tool
from tools.meeting import meeting_tool
from tools.notes import notes_tool
from tools.email import email_tool
from config import DEEPSEEK_API_KEY, DEEPSEEK_API_URL
from langchain.agents import AgentExecutor
# 自定义DeepSeek LLM类
class DeepSeekLLM(LLM):
    api_key: str
    model_name: str = "deepseek-chat"
    
    @property
    def _llm_type(self) -> str:
        # 返回一个字符串，表示LLM的类型
        return "deepseek"
    
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        # 设置请求头
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        # 设置请求体
        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0,
            "max_tokens": 2000
        }
        
        # 发送POST请求
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)
        # 检查响应状态码
        response.raise_for_status()
        # 返回响应内容
        return response.json()["choices"][0]["message"]["content"]
    
    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        return {"model_name": self.model_name}

# 初始化DeepSeek模型
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
    ),
    Tool(
        name="Task",
        func=task_tool,
        description="用于管理任务，支持创建任务（格式：创建任务 [内容] [优先级高/低]）、完成任务（格式：完成任务 [ID]）、列出任务（格式：列出任务 [未完成/已完成/高优先级]）"
    ),
    Tool(
        name="Meeting",
        func=meeting_tool,
        description="用于管理会议，支持创建会议（格式：创建会议 [时间] [地点] - [描述] @[参与人]）、取消会议（格式：取消会议 [ID]）、查询会议（格式：查询会议 [日期]）、列出所有会议"
    ),
    Tool(
        name="Notes",
        func=notes_tool,
        description="用于管理笔记，支持添加笔记（格式：添加笔记 [内容]）、搜索笔记（格式：搜索笔记 [关键词]）、列出所有笔记、删除笔记（格式：删除笔记 [ID]）"
    )
]
# 初始化记忆
memory = ConversationBufferMemory(memory_key="chat_history")

# 先初始化 agent
base_agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    memory=memory,
    agent_kwargs={
        "prefix": "你是一个智能助手，严格按照以下格式输出：\n"
                  "- 如果需要调用工具，只输出 Thought、Action、Action Input。\n"
                  "- 如果已经得到最终答案，只输出 Final Answer。\n"
                  "不要在同一次回复中同时输出 Action 和 Final Answer。\n"
    }
)
# 确保在全局作用域
agent = AgentExecutor.from_agent_and_tools(
    agent=base_agent.agent,
    tools=tools,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True
)