from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Dict, Any

from ..domain.discovery.controller.chatbot_controller import ChatbotController
from ..domain.discovery.service.chatbot_service import ChatbotService
from ..domain.discovery.repository.chatbot_repository import ChatbotRepository
from ..domain.discovery.model.chatbot_model import (
    ChatMessageRequest, 
    LangChainResponse, 
    ChatSessionResponse
)

router = APIRouter(prefix="/api/v1/chat", tags=["chatbot"])

# JWT Bearer 토큰 스키마
security = HTTPBearer()

# 의존성 주입
def get_chatbot_service() -> ChatbotService:
    """ChatbotService 의존성 주입"""
    repository = ChatbotRepository()
    return ChatbotService(repository)

def get_chatbot_controller() -> ChatbotController:
    """ChatbotController 의존성 주입"""
    service = get_chatbot_service()
    return ChatbotController(service)

@router.post("/send", response_model=LangChainResponse, summary="메시지 전송")
async def send_message(
    message_request: ChatMessageRequest,
    controller: ChatbotController = Depends(get_chatbot_controller)
    # credentials: HTTPAuthorizationCredentials = Depends(security)  # 임시 비활성화
):
    """AI 채팅봇에게 메시지를 전송하고 응답을 받습니다."""
    return await controller.send_message(message_request)

@router.get("/sessions", response_model=List[ChatSessionResponse], summary="채팅 세션 목록")
async def get_chat_sessions(
    controller: ChatbotController = Depends(get_chatbot_controller),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """사용자의 채팅 세션 목록을 조회합니다."""
    # TODO: JWT에서 user_id 추출
    user_id = 1
    return await controller.get_chat_sessions(user_id)

@router.delete("/sessions/{session_id}", summary="채팅 세션 삭제")
async def delete_chat_session(
    session_id: int,
    controller: ChatbotController = Depends(get_chatbot_controller),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """채팅 세션을 삭제합니다."""
    # TODO: JWT에서 user_id 추출
    user_id = 1
    return await controller.delete_chat_session(session_id, user_id)
