import os
import time
import logging
from typing import Dict, List, Optional
from datetime import datetime

from ..repository.chatbot_repository import ChatbotRepository
from ..entity.chatbot_entity import ChatMessage, ChatSession

logger = logging.getLogger("chatbot_service")

class ChatbotService:
    def __init__(self, repository: ChatbotRepository):
        self.repository = repository
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        logger.info(f"🔑 OpenAI API Key: {'설정됨' if self.openai_api_key else '설정 안됨 (더미 모드)'}")
    
    async def generate_response(self, message: str, context: Optional[Dict] = None) -> Dict:
        """AI 응답 생성"""
        start_time = time.time()
        
        try:
            if self.openai_api_key:
                # TODO: 실제 OpenAI API 호출
                response = await self._generate_openai_response(message, context)
            else:
                # 더미 응답
                response = self._generate_dummy_response(message)
            
            processing_time = time.time() - start_time
            
            return {
                "response": response,
                "tokens_used": 0,  # TODO: 실제 토큰 수 계산
                "processing_time": processing_time,
                "success": True
            }
            
        except Exception as e:
            logger.error(f"AI 응답 생성 오류: {e}")
            processing_time = time.time() - start_time
            
            return {
                "response": "죄송합니다. 현재 AI 서비스에 문제가 있습니다. 잠시 후 다시 시도해주세요.",
                "tokens_used": 0,
                "processing_time": processing_time,
                "success": False,
                "error": str(e)
            }
    
    def _generate_dummy_response(self, message: str) -> str:
        """더미 응답 생성 (개발/테스트용)"""
        dummy_responses = {
            "안녕": "안녕하세요! 중소기업 진단 AI 어시스턴트입니다. 어떤 도움이 필요하신가요?",
            "재무": "재무 상태를 분석해드리겠습니다. 매출, 비용, 현금흐름 등의 정보를 알려주시면 더 정확한 진단이 가능합니다.",
            "운영": "운영 효율성을 개선하기 위해 프로세스 최적화, 인력 관리, 기술 도입 등을 검토해보시기 바랍니다.",
            "마케팅": "마케팅 전략으로는 디지털 마케팅 강화, 고객 세분화, 브랜드 포지셔닝 등을 고려해보세요.",
            "평가": "기업 평가를 위해서는 재무제표, 사업계획서, 시장 분석 자료 등이 필요합니다. 어떤 부분을 중점적으로 살펴보고 싶으신가요?",
            "개선": "개선 방안을 제시하기 위해 현재 겪고 있는 문제점이나 목표를 구체적으로 말씀해 주세요."
        }
        
        for keyword, response in dummy_responses.items():
            if keyword in message:
                return response
        
        return f"'{message}'에 대해 분석해보겠습니다. 중소기업 진단 관련하여 재무, 운영, 마케팅, 인사 등 어떤 분야에 대해 더 자세히 알고 싶으신가요?"
    
    async def _generate_openai_response(self, message: str, context: Optional[Dict] = None) -> str:
        """OpenAI API를 사용한 응답 생성 (향후 구현)"""
        # TODO: 실제 OpenAI API 호출 구현
        return "실제 OpenAI API 응답 (구현 예정)"
    
    async def get_chat_sessions(self, user_id: int) -> List[Dict]:
        """사용자의 채팅 세션 목록을 조회합니다."""
        try:
            # TODO: 실제 DB에서 세션 목록 조회
            return [
                {
                    "id": 1,
                    "user_id": user_id,
                    "session_title": "기업 진단 상담",
                    "created_at": datetime.now(),
                    "is_active": True
                }
            ]
        except Exception as e:
            logger.error(f"세션 목록 조회 오류: {e}")
            return []
    
    async def delete_chat_session(self, session_id: int, user_id: int) -> bool:
        """채팅 세션을 삭제합니다."""
        try:
            # TODO: 실제 DB에서 세션 삭제
            logger.info(f"세션 삭제: {session_id}")
            return True
        except Exception as e:
            logger.error(f"세션 삭제 오류: {e}")
            return False
