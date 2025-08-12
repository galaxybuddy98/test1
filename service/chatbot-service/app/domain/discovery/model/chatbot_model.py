from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class ChatMessageRequest(BaseModel):
    """채팅 메시지 요청 모델"""
    message: str
    session_id: Optional[int] = None
    context: Optional[dict] = None

class LangChainResponse(BaseModel):
    """LangChain 응답 모델"""
    response: str
    session_id: int
    message_id: int
    tokens_used: Optional[int] = None
    processing_time: Optional[float] = None

class ChatSessionResponse(BaseModel):
    """채팅 세션 응답 모델"""
    id: int
    user_id: int
    session_title: Optional[str]
    created_at: datetime
    is_active: bool

class ChatMessageResponse(BaseModel):
    """채팅 메시지 응답 모델"""
    id: int
    message: str
    user_id: int
    session_id: int
    message_type: str
    response: Optional[str] = None
    tokens_used: Optional[int] = None
    processing_time: Optional[float] = None
    created_at: datetime

class ChatSessionCreateRequest(BaseModel):
    """채팅 세션 생성 요청 모델"""
    user_id: int
    session_title: Optional[str] = None

class ChatSessionUpdateRequest(BaseModel):
    """채팅 세션 수정 요청 모델"""
    session_title: Optional[str] = None
    is_active: Optional[bool] = None
