from fastapi import HTTPException, Depends
from typing import Dict, List, Optional
from datetime import datetime
import time
import logging

from ..service.chatbot_service import ChatbotService
from ..model.chatbot_model import ChatMessageRequest, LangChainResponse, ChatSessionResponse

logger = logging.getLogger("chatbot_service")

class ChatbotController:
    def __init__(self, chatbot_service: ChatbotService):
        self.chatbot_service = chatbot_service
    
    async def send_message(self, message_request: ChatMessageRequest) -> LangChainResponse:
        """AI 채팅봇에게 메시지를 전송하고 응답을 받습니다."""
        try:
            logger.info(f"🤖 메시지 수신: {message_request.message}")
            
            # 간단한 사용자 ID (실제로는 JWT에서 추출)
            user_id = 1
            
            # 세션 ID 생성 또는 사용
            session_id = message_request.session_id or int(time.time())
            
            # 서비스를 통해 응답 생성
            response_data = await self.chatbot_service.generate_response(
                message_request.message, 
                message_request.context
            )
            
            logger.info(f"✅ 응답 생성 완료: {response_data['response']}")
            
            return LangChainResponse(
                response=response_data['response'],
                session_id=session_id,
                message_id=int(time.time()),  # 임시 message_id
                tokens_used=response_data.get('tokens_used', 0),
                processing_time=response_data.get('processing_time', 0.1)
            )
            
        except Exception as e:
            logger.error(f"❌ 메시지 처리 오류: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"메시지 처리 중 오류가 발생했습니다: {str(e)}"
            )
    
    async def get_chat_sessions(self, user_id: int) -> List[ChatSessionResponse]:
        """사용자의 채팅 세션 목록을 조회합니다."""
        try:
            sessions = await self.chatbot_service.get_chat_sessions(user_id)
            return sessions
        except Exception as e:
            logger.error(f"❌ 세션 목록 조회 오류: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"세션 목록 조회 중 오류가 발생했습니다: {str(e)}"
            )
    
    async def delete_chat_session(self, session_id: int, user_id: int) -> Dict:
        """채팅 세션을 삭제합니다."""
        try:
            logger.info(f"🗑️ 세션 삭제 요청: {session_id}")
            result = await self.chatbot_service.delete_chat_session(session_id, user_id)
            return {"message": "세션이 삭제되었습니다", "session_id": session_id}
        except Exception as e:
            logger.error(f"❌ 세션 삭제 오류: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"세션 삭제 중 오류가 발생했습니다: {str(e)}"
            )
