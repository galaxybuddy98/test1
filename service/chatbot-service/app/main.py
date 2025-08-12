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

# Router import
from .router.chatbot_router import router as chatbot_router

# Router 등록
app.include_router(chatbot_router)

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