from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
import logging
import os

from agents.agent_manager import AgentManager
from models.base import Message, MessageType, AIResponse
from config import config

# 配置日志
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler()
    ]
)

# 创建FastAPI应用
app = FastAPI(
    title=config.APP_NAME,
    description="基于DeepSeek的校园生活服务智能助手API",
    version="1.0.0"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建Agent管理器
agent_manager = AgentManager()

# 请求模型
class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    context: Optional[List[Dict[str, Any]]] = None

class CourseRecommendationRequest(BaseModel):
    user_profile: Dict[str, Any]

class LocationRequest(BaseModel):
    location_name: str

class RouteRequest(BaseModel):
    start_location: str
    end_location: str

class AcademicQuestionRequest(BaseModel):
    question: str
    subject: Optional[str] = None

class LifeAdviceRequest(BaseModel):
    situation: str
    category: Optional[str] = "general"

class MentalHealthRequest(BaseModel):
    concern: str

class CareerGuidanceRequest(BaseModel):
    interests: List[str]
    skills: List[str]
    goals: str

# 响应模型
class ChatResponse(BaseModel):
    response: AIResponse
    session_id: str

class ServiceListResponse(BaseModel):
    services: List[Dict[str, Any]]

@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "校园生活服务智能助手API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """聊天接口"""
    try:
        # 转换上下文消息
        context = None
        if request.context:
            context = []
            for msg_data in request.context:
                context.append(Message(
                    content=msg_data["content"],
                    message_type=MessageType(msg_data["message_type"]),
                    user_id=msg_data.get("user_id"),
                    session_id=msg_data.get("session_id")
                ))
        
        # 获取AI响应
        response = await agent_manager.route_message(request.message, context)
        
        # 生成会话ID
        session_id = request.session_id or f"session_{request.user_id}_{hash(request.message)}"
        
        return ChatResponse(response=response, session_id=session_id)
        
    except Exception as e:
        logging.error(f"聊天接口出错: {str(e)}")
        raise HTTPException(status_code=500, detail="处理请求时出现错误")

@app.post("/course/recommendations")
async def get_course_recommendations(request: CourseRecommendationRequest):
    """获取课程推荐"""
    try:
        response = await agent_manager.get_course_recommendations(request.user_profile)
        return {"response": response}
    except Exception as e:
        logging.error(f"获取课程推荐时出错: {str(e)}")
        raise HTTPException(status_code=500, detail="获取课程推荐时出现错误")

@app.post("/navigation/find")
async def find_location(request: LocationRequest):
    """查找地点"""
    try:
        response = await agent_manager.find_location(request.location_name)
        return {"response": response}
    except Exception as e:
        logging.error(f"查找地点时出错: {str(e)}")
        raise HTTPException(status_code=500, detail="查找地点时出现错误")

@app.post("/navigation/route")
async def plan_route(request: RouteRequest):
    """规划路线"""
    try:
        response = await agent_manager.plan_route(request.start_location, request.end_location)
        return {"response": response}
    except Exception as e:
        logging.error(f"规划路线时出错: {str(e)}")
        raise HTTPException(status_code=500, detail="规划路线时出现错误")

@app.post("/qa/academic")
async def answer_academic_question(request: AcademicQuestionRequest):
    """回答学术问题"""
    try:
        response = await agent_manager.answer_academic_question(request.question, request.subject)
        return {"response": response}
    except Exception as e:
        logging.error(f"回答学术问题时出错: {str(e)}")
        raise HTTPException(status_code=500, detail="回答学术问题时出现错误")

@app.post("/qa/life-advice")
async def provide_life_advice(request: LifeAdviceRequest):
    """提供生活建议"""
    try:
        response = await agent_manager.provide_life_advice(request.situation, request.category)
        return {"response": response}
    except Exception as e:
        logging.error(f"提供生活建议时出错: {str(e)}")
        raise HTTPException(status_code=500, detail="提供生活建议时出现错误")

@app.post("/qa/mental-health")
async def mental_health_support(request: MentalHealthRequest):
    """心理健康支持"""
    try:
        response = await agent_manager.mental_health_support(request.concern)
        return {"response": response}
    except Exception as e:
        logging.error(f"心理健康支持时出错: {str(e)}")
        raise HTTPException(status_code=500, detail="心理健康支持时出现错误")

@app.post("/qa/career-guidance")
async def career_guidance(request: CareerGuidanceRequest):
    """职业规划指导"""
    try:
        response = await agent_manager.career_guidance(request.interests, request.skills, request.goals)
        return {"response": response}
    except Exception as e:
        logging.error(f"职业规划指导时出错: {str(e)}")
        raise HTTPException(status_code=500, detail="职业规划指导时出现错误")

@app.get("/services", response_model=ServiceListResponse)
async def get_services():
    """获取可用服务列表"""
    try:
        services = agent_manager.get_available_services()
        return ServiceListResponse(services=services)
    except Exception as e:
        logging.error(f"获取服务列表时出错: {str(e)}")
        raise HTTPException(status_code=500, detail="获取服务列表时出现错误")

if __name__ == "__main__":
    # 创建日志目录
    os.makedirs("logs", exist_ok=True)
    
    # 启动服务器
    uvicorn.run(
        "main:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.DEBUG,
        log_level=config.LOG_LEVEL.lower()
    ) 