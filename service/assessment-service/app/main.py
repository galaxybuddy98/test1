import os, logging, sys, traceback
import httpx
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from dotenv import load_dotenv



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

@app.middleware("http")
async def log_requests(request: Request, call_next):
    client_host = request.client.host if request.client else "unknown"
    logger.info(f"📥 {request.method} {request.url.path} (client: {client_host})")
    try:
        response = await call_next(request)
        logger.info(f"📤 {response.status_code} {request.url.path}")
        return response
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        logger.error(traceback.format_exc())
        raise

@app.get("/", include_in_schema=False)
async def root():
    return {"service": "Assessment Service", "version": "1.0.0", "status": "running"}

# Router import
from .router.assessment_router import router as assessment_router

# Router 등록
app.include_router(assessment_router)

@app.get("/health", include_in_schema=False)
async def health_check():
    return {"status": "healthy", "service": "Assessment Service", "version": "1.0.0"}

# __main__ 블록은 로컬 실행용(배포에 영향 없음)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8001)))
