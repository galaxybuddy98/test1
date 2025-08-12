import os
import logging
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from dotenv import load_dotenv

# 도메인 임포트
from app.domain.user.user_controller import create_auth_router, get_user_service
from app.domain.user.user_model import Base
from app.domain.user.user_Service import UserService
from app.domain.user.user_repository import UserRepository

# 환경 설정 로드
if os.getenv("RAILWAY_ENVIRONMENT") != "true":
    load_dotenv()

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("auth_service")

# 데이터베이스 설정
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://user:password@localhost:5432/eripotter_db"
)

# Railway 환경에서 postgres://를 postgresql+asyncpg://로 변경 (sslmode 제거)
if DATABASE_URL and ("railway" in DATABASE_URL or "postgres://" in DATABASE_URL):
    # postgres://를 postgresql+asyncpg://로 변경
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://")
    # sslmode가 있으면 제거 (asyncpg는 sslmode를 지원하지 않음)
    if "sslmode=" in DATABASE_URL:
        DATABASE_URL = DATABASE_URL.split("?")[0]  # 쿼리 파라미터 모두 제거

# asyncpg 드라이버 강제 설정
if DATABASE_URL and not DATABASE_URL.startswith("postgresql+asyncpg://"):
    if DATABASE_URL.startswith("postgresql://"):
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
    
logger.info(f"🔧 최종 DATABASE_URL: {DATABASE_URL[:50]}...")

# 비동기 데이터베이스 엔진 생성
engine = create_async_engine(
    DATABASE_URL,
    poolclass=NullPool,  # Railway에서 연결 풀 문제 방지
    echo=False  # 운영 환경에서는 False
)

# 세션 메이커
AsyncSessionLocal = async_sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """앱 시작/종료 시 실행되는 함수"""
    logger.info("🚀 Auth Service 시작")
    logger.info(f"🔧 PORT={os.getenv('PORT')}  RAILWAY={os.getenv('RAILWAY')}")
    
    # DB 연결은 필요할 때만 (user_controller에서 직접 처리)
    logger.info("📦 Auth Service 준비 완료")
    
    yield
    
    logger.info("🛑 Auth Service 종료")

# FastAPI 앱 생성
app = FastAPI(
    title="Auth Service",
    description="사용자 인증 및 권한 관리 서비스",
    version="1.0.0",
    docs_url="/docs",
    lifespan=lifespan,
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

# 데이터베이스 세션 의존성
async def get_database():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# UserService 의존성을 위한 오버라이드
async def get_user_service_dependency(db: AsyncSession = Depends(get_database)) -> UserService:
    user_repository = UserRepository(db)
    return UserService(user_repository)

# 의존성 오버라이드 (user_controller의 get_user_service를 실제 DB 세션으로 대체)
app.dependency_overrides[get_user_service] = get_user_service_dependency

# 라우터 등록
auth_router = create_auth_router()
app.include_router(auth_router, prefix="/api/v1")

# 기본 엔드포인트들
@app.get("/", include_in_schema=False)
async def root():
    return {
        "service": "Auth Service",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "docs": "/docs",
            "auth": "/api/v1/auth"
        }
    }

@app.get("/health", include_in_schema=False)
async def health_check():
    return {
        "status": "healthy",
        "service": "Auth Service",
        "version": "1.0.0",
        "database": "connected" if engine else "disconnected"
    }

# 로컬 실행용
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8002))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)