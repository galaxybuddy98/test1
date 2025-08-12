import os
import logging
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Union

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# 환경 설정 로드
if os.getenv("RAILWAY_ENVIRONMENT") != "true":
    load_dotenv()

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("chatbot_service")

# FastAPI 앱 생성
app = FastAPI(
    title="Chatbot Service",
    description="LangChain을 사용한 AI 채팅 서비스",
    version="1.0.0",
    docs_url="/docs"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        os.getenv("FRONTEND_ORIGIN", "http://localhost:3000"),
        os.getenv("GATEWAY_ORIGIN", "http://localhost:8080"),
    ],
    allow_origin_regex=r"https://.*\.railway\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# JWT Bearer 토큰 스키마  
security = HTTPBearer()

# ===== Pydantic 모델들 =====
class ChatMessageRequest(BaseModel):
    message: str
    session_id: Optional[int] = None
    context: Optional[dict] = None

class LangChainResponse(BaseModel):
    response: str
    session_id: int
    message_id: int
    tokens_used: Optional[int] = None
    processing_time: Optional[float] = None

class ChatSessionResponse(BaseModel):
    id: int
    user_id: int
    session_title: Optional[str]
    created_at: datetime
    is_active: bool

# ===== 간단한 LangChain 서비스 =====
class SimpleLangChainService:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        logger.info(f"🔑 OpenAI API Key: {'설정됨' if self.openai_api_key else '설정 안됨 (더미 모드)'}")
    
    async def generate_response(self, message: str, chat_history: Optional[List] = None, context: Optional[Dict] = None) -> Dict:
        """AI 응답 생성"""
        start_time = time.time()
        
        try:
            if self.openai_api_key:
                # TODO: 실제 OpenAI API 호출
                response = await self._generate_openai_response(message, chat_history, context)
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
    
    async def _generate_openai_response(self, message: str, chat_history: Optional[List] = None, context: Optional[Dict] = None) -> str:
        """OpenAI API를 사용한 응답 생성 (향후 구현)"""
        # TODO: 실제 OpenAI API 호출 구현
        return "실제 OpenAI API 응답 (구현 예정)"

# LangChain 서비스 인스턴스
langchain_service = SimpleLangChainService()

# ===== API 엔드포인트들 =====

@app.post("/api/v1/chat/send", response_model=LangChainResponse, summary="메시지 전송")
async def send_message(
    message_request: ChatMessageRequest
    # credentials: HTTPAuthorizationCredentials = Depends(security)  # 임시 비활성화
):
    """AI 채팅봇에게 메시지를 전송하고 응답을 받습니다."""
    try:
        logger.info(f"🤖 메시지 수신: {message_request.message}")
        
        # 간단한 사용자 ID (실제로는 JWT에서 추출)
        user_id = 1
        
        # 세션 ID 생성 또는 사용
        session_id = message_request.session_id or int(time.time())
        
        # 더미 응답으로 테스트
        dummy_response = f"테스트 응답: '{message_request.message}'에 대한 답변입니다."
        
        logger.info(f"✅ 더미 응답 생성 완료: {dummy_response}")
        
        return LangChainResponse(
            response=dummy_response,
            session_id=session_id,
            message_id=int(time.time()),  # 임시 message_id
            tokens_used=0,
            processing_time=0.1
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ 메시지 처리 오류: {e}")
        logger.error(f"❌ 에러 타입: {type(e)}")
        logger.error(f"❌ 에러 상세: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"메시지 처리 중 오류가 발생했습니다: {str(e)}"
        )

@app.get("/api/v1/chat/sessions", response_model=List[ChatSessionResponse], summary="채팅 세션 목록")
async def get_chat_sessions(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """사용자의 채팅 세션 목록을 조회합니다."""
    # TODO: 실제 DB에서 세션 목록 조회
    return [
        ChatSessionResponse(
            id=1,
            user_id=1,
            session_title="기업 진단 상담",
            created_at=datetime.now(),
            is_active=True
        )
    ]

@app.delete("/api/v1/chat/sessions/{session_id}", summary="채팅 세션 삭제")
async def delete_chat_session(
    session_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """채팅 세션을 삭제합니다."""
    logger.info(f"🗑️ 세션 삭제 요청: {session_id}")
    return {"message": "세션이 삭제되었습니다", "session_id": session_id}

# ===== 기본 엔드포인트들 =====

@app.get("/", include_in_schema=False)
async def root():
    return {
        "service": "Chatbot Service",
        "version": "1.0.0",
        "status": "running",
        "features": ["LangChain", "AI Chat", "Enterprise Diagnosis"],
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "send_message": "/api/v1/chat/send",
            "sessions": "/api/v1/chat/sessions"
        }
    }

@app.get("/health", include_in_schema=False)
async def health_check():
    """헬스 체크"""
    openai_status = "configured" if os.getenv("OPENAI_API_KEY") else "dummy_mode"
    database_status = "configured" if os.getenv("DATABASE_URL") else "not_configured"
    
    return {
        "status": "healthy",
        "service": "Chatbot Service",
        "version": "1.0.0",
        "openai": openai_status,
        "database": database_status,
        "features": {
            "langchain": True,
            "chat_responses": True,
            "dummy_responses": True,
            "enterprise_diagnosis": True
        }
    }

# 로컬 실행용
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8003))
    logger.info(f"🚀 Chatbot Service 시작 (포트: {port})")
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)