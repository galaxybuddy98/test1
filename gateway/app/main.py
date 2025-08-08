from typing import Optional, List
from fastapi import APIRouter, FastAPI, Request, UploadFile, File, Query, HTTPException, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import logging
import sys
from dotenv import load_dotenv
from contextlib import asynccontextmanager
import httpx  # ✅ 추가: 프록시 요청 릴레이용

from app.router.auth_router import auth_router
from app.common.middleware.jwt_auth_middleware import AuthMiddleware
# ⛔ ServiceDiscovery / ServiceType 불필요
# from app.domain.discovery.model.service_discovery import ServiceDiscovery
# from app.domain.discovery.model.service_type import ServiceType
from app.common.utility.constant.settings import Settings
from app.common.utility.factory.response_factory import ResponseFactory

# ===== 환경 설정 =====
if os.getenv("RAILWAY_ENVIRONMENT") != "true":
    load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("gateway_api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Gateway API 서비스 시작")
    # Settings 초기화 방어
    try:
        app.state.settings = Settings()
        logger.info("✅ Settings 초기화 완료")
    except Exception as e:
        logger.warning(f"⚠️ Settings 초기화 실패, 계속 진행합니다: {e}")
        app.state.settings = None
    yield
    logger.info("🛑 Gateway API 서비스 종료")


app = FastAPI(
    title="ERIpotter Gateway API", 
    description="Gateway API for lme.eripotter.com",
    version="0.1.0",
    docs_url="/docs",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://lme.eripotter.com",  # 실제 프론트 도메인
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_origin_regex=r"https://.*\.railway\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(AuthMiddleware)

gateway_router = APIRouter(tags=["Gateway API"])
gateway_router.include_router(auth_router)
app.include_router(gateway_router)

# 🪡 파일이 필요한 서비스 목록 (현재는 없음)
FILE_REQUIRED_SERVICES = set()

# ===== 내부 헬퍼 =====
def _get_base_url(service: str) -> str:
    """
    서비스명 → ENV 매핑
    필요한 서비스만 여기 추가하면 됨.
    """
    if service == "assessment":
        url = os.getenv("ASSESSMENT_SERVICE_URL")
        if not url:
            raise RuntimeError("ENV ASSESSMENT_SERVICE_URL 가 설정되지 않았습니다.")
        return url.rstrip("/")

    # 필요시 다른 서비스들도 여기에 추가:
    # if service == "report":
    #     url = os.getenv("REPORT_SERVICE_URL")

    raise HTTPException(status_code=404, detail=f"Unknown service: {service}")


async def _relay(method: str, base_url: str, path: str, headers=None, body=None, files=None, params=None, data=None):
    """
    실제 마이크로서비스로 요청을 릴레이.
    원본 프록시 설계와 동일하게 content(body)/files/params/data를 그대로 전달.
    """
    url = f"{base_url}/{path.lstrip('/')}"
    timeout = httpx.Timeout(30.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        resp = await client.request(
            method=method,
            url=url,
            headers=headers,
            content=body,   # JSON이면 원요청이 JSON 형태로 들어오기 때문에 content 그대로 전달
            files=files,
            params=params,
            data=data
        )
        return resp


# ===== 헬스 및 기본 =====
@gateway_router.get("/health", summary="API v1 헬스 체크")
async def api_v1_health_check():
    return {"status": "healthy!", "version": "v1"}


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": "요청한 리소스를 찾을 수 없습니다."}
    )


@app.get("/")
async def root():
    return {
        "message": "Gateway API", 
        "version": "0.1.1",
        "port": os.getenv("PORT", "8080"),
        "status": "running",
        "timestamp": "2024-01-01"
    }

@app.get("/test")
async def test_endpoint():
    """간단한 테스트 엔드포인트"""
    return {"message": "Hello from Railway!", "status": "OK"}


@app.post("/health")
async def simple_health_check_post():
    return {"status": "healthy!", "service": "Gateway API", "method": "POST"}


# ===== 인증(예시) =====
@gateway_router.post("/login", summary="로그인")
async def login():
    print("로그인 요청 받음", {})
    return {"message": "로그인 요청 받음"}


@gateway_router.post("/signup", summary="회원가입")
async def signup(request: Request):
    try:
        body = await request.body()
        if body:
            import json
            data = json.loads(body)
            print("🎉 회원가입 요청 받음:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print("📭 빈 요청 받음")
            data = {}
        return {"message": "회원가입성공", "received_data": data}
    except Exception as e:
        print(f"❌ 회원가입 요청 처리 중 오류: {str(e)}")
        return {"message": "회원가입 실패", "error": str(e)}


# ===== 동적 프록시 라우팅 =====
@gateway_router.get("/{service}/{path:path}", summary="GET 프록시")
async def proxy_get(service: str, path: str, request: Request):
    try:
        headers = dict(request.headers)
        base_url = _get_base_url(service)
        response = await _relay("GET", base_url, path, headers=headers)
        return ResponseFactory.create_response(response)
    except Exception as e:
        logger.error(f"Error in GET proxy: {str(e)}")
        return JSONResponse(
            content={"detail": f"Error processing request: {str(e)}"},
            status_code=500
        )


@gateway_router.post("/{service}/{path:path}", summary="POST 프록시")
async def proxy_post(
    service: str,
    path: str,
    request: Request,
    file: Optional[UploadFile] = None,
    sheet_names: Optional[List[str]] = Query(None, alias="sheet_name")
):
    try:
        logger.info(f"🌈 POST 요청 받음: 서비스={service}, 경로={path}")
        if file:
            logger.info(f"파일명: {file.filename}, 시트 이름: {sheet_names if sheet_names else '없음'}")

        # 요청 파라미터 초기화
        files = None
        params = None
        body = None
        data = None

        # 헤더 전달 (JWT 및 사용자 ID - 미들웨어에서 이미 X-User-Id 헤더가 추가됨)
        headers = dict(request.headers)

        # 파일이 필요한 서비스 처리
        if service in FILE_REQUIRED_SERVICES:
            if "upload" in path and not file:
                raise HTTPException(status_code=400, detail=f"서비스 {service}에는 파일 업로드가 필요합니다.")
            if file:
                file_content = await file.read()
                files = {'file': (file.filename, file_content, file.content_type)}
                await file.seek(0)
            if sheet_names:
                params = {'sheet_name': sheet_names}
        else:
            try:
                body = await request.body()
                if not body:
                    logger.info("요청 본문이 비어 있습니다.")
            except Exception as e:
                logger.warning(f"요청 본문 읽기 실패: {str(e)}")

        base_url = _get_base_url(service)
        response = await _relay("POST", base_url, path, headers=headers, body=body, files=files, params=params, data=data)
        return ResponseFactory.create_response(response)

    except HTTPException as he:
        return JSONResponse(content={"detail": he.detail}, status_code=he.status_code)
    except Exception as e:
        logger.error(f"POST 요청 처리 중 오류 발생: {str(e)}")
        return JSONResponse(
            content={"detail": f"Gateway error: {str(e)}"},
            status_code=500
        )


@gateway_router.put("/{service}/{path:path}", summary="PUT 프록시")
async def proxy_put(service: str, path: str, request: Request):
    try:
        headers = dict(request.headers)
        body = await request.body()
        base_url = _get_base_url(service)
        response = await _relay("PUT", base_url, path, headers=headers, body=body)
        return ResponseFactory.create_response(response)
    except Exception as e:
        logger.error(f"Error in PUT proxy: {str(e)}")
        return JSONResponse(
            content={"detail": f"Error processing request: {str(e)}"},
            status_code=500
        )


@gateway_router.delete("/{service}/{path:path}", summary="DELETE 프록시")
async def proxy_delete(service: str, path: str, request: Request):
    try:
        headers = dict(request.headers)
        body = await request.body()
        base_url = _get_base_url(service)
        response = await _relay("DELETE", base_url, path, headers=headers, body=body)
        return ResponseFactory.create_response(response)
    except Exception as e:
        logger.error(f"Error in DELETE proxy: {str(e)}")
        return JSONResponse(
            content={"detail": f"Error processing request: {str(e)}"},
            status_code=500
        )


@gateway_router.patch("/{service}/{path:path}", summary="PATCH 프록시")
async def proxy_patch(service: str, path: str, request: Request):
    try:
        headers = dict(request.headers)
        body = await request.body()
        base_url = _get_base_url(service)
        response = await _relay("PATCH", base_url, path, headers=headers, body=body)
        return ResponseFactory.create_response(response)
    except Exception as e:
        logger.error(f"Error in PATCH proxy: {str(e)}")
        return JSONResponse(
            content={"detail": f"Error processing request: {str(e)}"},
            status_code=500
        )

# 루트 레벨 Health Check (prefix 없이)
@app.get("/health")
async def root_health_check():
    """루트 레벨 헬스 체크 - 프론트엔드 프록시용"""
    return {"status": "ok"}

# API 레벨 Health Check (프론트엔드 프록시 /api/health용)
@app.get("/api/health")
async def frontend_proxy_health_check():
    """API 레벨 헬스 체크 - 프론트엔드 /api/health 프록시용"""
    return {"status": "ok"}

# ===== 로컬 실행 =====
if __name__ == "__main__":
    import uvicorn
    # Railway PORT 환경변수 사용
    port = int(os.getenv("PORT", os.getenv("SERVICE_PORT", 8080)))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
