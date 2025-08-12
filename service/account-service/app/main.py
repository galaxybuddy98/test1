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
from app.domain.user.model.user_model import Base

# 환경 설정 로드
if os.getenv("RAILWAY_ENVIRONMENT") != "true":
    load_dotenv()

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("account_service")

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
    logger.info("🚀 Account Service 시작")
    logger.info(f"🔧 PORT={os.getenv('PORT')}  RAILWAY={os.getenv('RAILWAY')}")
    
    # 앱 시작 시 users 테이블 생성
    try:
        import asyncpg
        DATABASE_URL = os.getenv("DATABASE_URL", "")
        if DATABASE_URL:
            # asyncpg 연결용 URL 정리
            conn_str = DATABASE_URL.replace("postgres://", "postgresql://").split("?")[0]
            
            # 여러 SSL 옵션 시도해서 연결
            conn = None
            for ssl_option in ['require', True, False, None]:
                try:
                    if ssl_option is None:
                        conn = await asyncpg.connect(conn_str)
                    else:
                        conn = await asyncpg.connect(conn_str, ssl=ssl_option)
                    logger.info(f"✅ 시작 시 DB 연결 성공 (SSL: {ssl_option})")
                    break
                except Exception as e:
                    logger.warning(f"❌ 시작 시 DB 연결 실패 (SSL: {ssl_option}): {e}")
                    continue
            
            if conn:
                # users 테이블 생성
                await conn.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(50) UNIQUE NOT NULL,
                        email VARCHAR(100) UNIQUE NOT NULL,
                        password_hash VARCHAR(255) NOT NULL,
                        company_id VARCHAR(100),
                        role VARCHAR(20) DEFAULT 'user',
                        is_active BOOLEAN DEFAULT true,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                    );
                """)
                logger.info("✅ users 테이블 생성 완료")
                await conn.close()
            else:
                logger.error("❌ 모든 DB 연결 방법 실패")
        else:
            logger.warning("⚠️ DATABASE_URL이 설정되지 않음")
    except Exception as e:
        logger.error(f"❌ DB 테이블 생성 실패: {e}")
        logger.info("⚠️ 서비스는 계속 진행됩니다")
    
    logger.info("📦 Account Service 준비 완료")
    
    yield
    
    logger.info("🛑 Account Service 종료")

# FastAPI 앱 생성
app = FastAPI(
    title="Account Service",
    description="사용자 계정 관리 서비스",
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

# Router import
from app.router.user_router import router as user_router

# 의존성 오버라이드 제거 - Controller에서 직접 DB 연결 처리

# Router 등록
app.include_router(user_router, prefix="/api/v1")

# 기본 엔드포인트들
@app.get("/", include_in_schema=False)
async def root():
    return {
        "service": "Account Service",
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
        "service": "Account Service",
        "version": "1.0.0",
        "database": "connected" if engine else "disconnected"
    }

# 로컬 실행용
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8002))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)