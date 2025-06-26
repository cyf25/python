from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class MessageType(str, Enum):
    """消息类型枚举"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class ServiceType(str, Enum):
    """服务类型枚举"""
    COURSE = "course"
    NAVIGATION = "navigation"
    ACTIVITY = "activity"
    LIFE_SERVICE = "life_service"
    STUDY_ASSISTANT = "study_assistant"
    GENERAL_QA = "general_qa"

class Message(BaseModel):
    """消息模型"""
    id: Optional[str] = None
    content: str
    message_type: MessageType
    timestamp: datetime = Field(default_factory=datetime.now)
    user_id: Optional[str] = None
    session_id: Optional[str] = None

class Conversation(BaseModel):
    """对话模型"""
    id: Optional[str] = None
    user_id: str
    title: str
    messages: List[Message] = []
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class User(BaseModel):
    """用户模型"""
    id: Optional[str] = None
    username: str
    email: Optional[str] = None
    student_id: Optional[str] = None
    major: Optional[str] = None
    grade: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

class Course(BaseModel):
    """课程模型"""
    id: Optional[str] = None
    code: str
    name: str
    credits: int
    instructor: str
    schedule: str
    location: str
    description: Optional[str] = None
    capacity: int
    enrolled: int = 0

class Activity(BaseModel):
    """活动模型"""
    id: Optional[str] = None
    title: str
    description: str
    start_time: datetime
    end_time: datetime
    location: str
    organizer: str
    category: str
    max_participants: Optional[int] = None
    current_participants: int = 0

class Location(BaseModel):
    """地点模型"""
    id: Optional[str] = None
    name: str
    category: str
    description: str
    coordinates: Optional[Dict[str, float]] = None
    address: str
    opening_hours: Optional[str] = None

class StudyPlan(BaseModel):
    """学习计划模型"""
    id: Optional[str] = None
    user_id: str
    title: str
    description: str
    tasks: List[Dict[str, Any]] = []
    start_date: datetime
    end_date: datetime
    progress: float = 0.0
    status: str = "active"

class AIResponse(BaseModel):
    """AI响应模型"""
    content: str
    service_type: ServiceType
    confidence: float = 0.0
    metadata: Optional[Dict[str, Any]] = None
    suggestions: Optional[List[str]] = None 