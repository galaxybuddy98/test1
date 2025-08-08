import os, logging, sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from app.router.auth_router import auth_router
from app.domain.sme.controller.assessment_controller import assessment_router

if os.getenv("PORT") is None:  # 로컬 개발 때만 .env 로드
    load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("assessment_service")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Assessment Service 시작")
    logger.info(f"🔧 PORT={os.getenv('PORT')}  RAILWAY={os.getenv('RAILWAY')}")
    yield
    logger.info("🛑 Assessment Service 종료")

app = FastAPI(
    title="Assessment Service",
    description="중소기업 진단 평가 서비스",
    version="1.0.0",
    docs_url="/docs",
    lifespan=lifespan,
)

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

# Prefix 통일
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(assessment_router, prefix="/api/v1/assessments", tags=["assessments"])

@app.get("/", include_in_schema=False)
async def root():
    return {"service": "Assessment Service", "version": "1.0.0", "status": "running"}

@app.get("/health", include_in_schema=False)
async def health_check():
    return {"status": "healthy", "service": "Assessment Service", "version": "1.0.0"}

# __main__ 블록은 로컬 실행용(배포에 영향 없음)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8001)))
