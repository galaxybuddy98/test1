from typing import Optional, List
from fastapi import APIRouter, FastAPI, Request, UploadFile, File, Query, HTTPException, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
import os
import logging
import sys
from dotenv import load_dotenv
from contextlib import asynccontextmanager
import httpx  # ✅ 추가: 프록시 요청 릴레이용

# from app.router.auth_router import auth_router  # 사용하지 않음
# from app.common.middleware.jwt_auth_middleware import AuthMiddleware  # 삭제됨
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

# app.add_middleware(AuthMiddleware)  # 임시 비활성화

gateway_router = APIRouter(tags=["Gateway API"])
# gateway_router.include_router(auth_router)  # 사용하지 않음
print("🔧 gateway_router 생성됨!")

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
    
    if service == "auth":
        url = os.getenv("AUTH_SERVICE_URL")
        if not url:
            raise RuntimeError("ENV AUTH_SERVICE_URL 가 설정되지 않았습니다.")
        return url.rstrip("/")
    
    if service == "chatbot":
        url = os.getenv("CHATBOT_SERVICE_URL")
        if not url:
            raise RuntimeError("ENV CHATBOT_SERVICE_URL 가 설정되지 않았습니다.")
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


# ===== Auth 서비스 프록시 =====
@gateway_router.api_route("/api/auth/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def auth_proxy(request: Request, path: str):
    """Auth 서비스로 모든 요청을 프록시 (/api/auth/*)"""
    try:
        logger.info(f"🔍 Auth 프록시 요청: {request.method} {request.url.path}")
        auth_url = os.getenv('AUTH_SERVICE_URL', 'NOT_SET')
        logger.info(f"🔍 AUTH_SERVICE_URL: {auth_url}")
        
        # 임시 fallback (Railway 환경변수 문제 시)
        if auth_url == 'NOT_SET':
            # auth-service의 실제 도메인
            auth_url = "https://auth-service-production-ce3c.up.railway.app"
            logger.info(f"🔧 임시 AUTH_SERVICE_URL 사용: {auth_url}")
            base_url = auth_url
        else:
            base_url = _get_base_url("auth")
        logger.info(f"🔍 Base URL: {base_url}")
        
        # 요청 본문 읽기
        body = await request.body()
        
        # 헤더에서 불필요한 것들 제거
        headers = dict(request.headers)
        headers.pop("host", None)
        headers.pop("content-length", None)
        
        # auth-service는 /api/v1/auth/* 경로를 사용하므로 경로 변환
        auth_service_path = f"api/v1/auth/{path}"
        
        response = await _relay(
            method=request.method,
            base_url=base_url,
            path=auth_service_path,
            headers=headers,
            body=body,
            params=dict(request.query_params)
        )
        
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers)
        )
        
    except Exception as e:
        logger.error(f"Auth 프록시 오류: {e}")
        raise HTTPException(status_code=500, detail=f"Auth 서비스 연결 실패: {str(e)}")

# ===== Chatbot 구체적인 라우트들 (app 레벨에 직접 등록) =====
@app.get("/api/chatbot/health")
async def chatbot_health_proxy(request: Request):
    """Chatbot health check 프록시"""
    logger.error("🚨🤖 CHATBOT HEALTH 호출됨!!!")
    print("🚨🤖 CHATBOT HEALTH 호출됨!!!")
    try:
        chatbot_url = os.getenv('CHATBOT_SERVICE_URL', 'NOT_SET')
        if chatbot_url == 'NOT_SET':
            chatbot_url = "https://chatbot-service-production-1d24.up.railway.app"
        
        import httpx
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{chatbot_url}/health")
            return response.json()
    except Exception as e:
        logger.error(f"Chatbot health 오류: {e}")
        return {"error": str(e)}

@app.post("/api/chatbot/send")
async def chatbot_send_proxy(request: Request):
    """Chatbot send message 프록시"""
    logger.error("🚨🤖 CHATBOT SEND 호출됨!!!")
    print("🚨🤖 CHATBOT SEND 호출됨!!!")
    try:
        chatbot_url = os.getenv('CHATBOT_SERVICE_URL', 'NOT_SET')
        if chatbot_url == 'NOT_SET':
            chatbot_url = "https://chatbot-service-production-1d24.up.railway.app"
        
        body = await request.body()
        headers = dict(request.headers)
        headers.pop("host", None)
        headers.pop("content-length", None)
        
        import httpx
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{chatbot_url}/api/v1/chat/send",
                content=body,
                headers=headers
            )
            return response.json()
    except Exception as e:
        logger.error(f"Chatbot send 오류: {e}")
        return {"error": str(e)}

# ===== 테스트용 간단한 chatbot 라우트 =====
@app.get("/api/chatbot/test")
async def chatbot_test():
    """chatbot 라우트 테스트"""
    logger.error("🚨 /api/chatbot/test 라우트 호출됨!!!")
    print("🚨 /api/chatbot/test 라우트 호출됨!!!")
    return {"message": "chatbot 라우트 작동 중!", "service": "gateway->chatbot"}

# ===== Chatbot 서비스 프록시 (일반용) =====
@gateway_router.api_route("/api/chatbot/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def chatbot_proxy(request: Request, full_path: str):
    """Chatbot 서비스로 모든 요청을 프록시 (/api/chatbot/*)"""
    try:
        logger.error(f"🚨🤖 CHATBOT PROXY 호출됨!!! - {request.method} {request.url.path} - full_path={full_path}")
        print(f"🚨🤖 CHATBOT PROXY 호출됨!!! - {request.method} {request.url.path} - full_path={full_path}")
        logger.info(f"🤖 Chatbot 프록시 요청: {request.method} {request.url.path}")
        chatbot_url = os.getenv('CHATBOT_SERVICE_URL', 'NOT_SET')
        logger.info(f"🔍 CHATBOT_SERVICE_URL: {chatbot_url}")
        
        # 임시 fallback (Railway 환경변수 문제 시)
        if chatbot_url == 'NOT_SET':
            chatbot_url = "https://chatbot-service-production-1d24.up.railway.app"
            logger.info(f"🔧 임시 CHATBOT_SERVICE_URL 사용: {chatbot_url}")
            base_url = chatbot_url
        else:
            base_url = _get_base_url("chatbot")
        logger.info(f"🔍 Base URL: {base_url}")
        
        # 요청 본문 읽기
        body = await request.body()
        
        # 헤더에서 불필요한 것들 제거
        headers = dict(request.headers)
        headers.pop("host", None)
        headers.pop("content-length", None)
        
        # chatbot-service는 /api/v1/chat/* 경로를 사용하므로 경로 변환
        chatbot_service_path = f"api/v1/chat/{full_path}"
        
        response = await _relay(
            method=request.method,
            base_url=base_url,
            path=chatbot_service_path,
            headers=headers,
            body=body,
            params=dict(request.query_params)
        )
        
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers)
        )
        
    except Exception as e:
        logger.error(f"Chatbot 프록시 오류: {e}")
        raise HTTPException(status_code=500, detail=f"Chatbot 서비스 연결 실패: {str(e)}")

# ===== gateway_router 등록 =====
app.include_router(gateway_router)
print("🔧 gateway_router가 app에 등록됨 (auth_proxy, chatbot_proxy 포함)!")

# 디버그: 등록된 라우트 확인
print("🔍 등록된 라우트 목록:")
for route in app.routes:
    try:
        methods = getattr(route, 'methods', None)
        path = getattr(route, 'path', None)
        
        if methods and path:
            print(f"  - {methods} {path}")
        elif path:
            print(f"  - [NO METHODS] {path}")
        else:
            print(f"  - [ROUTE] {type(route).__name__}")
    except Exception:
        print(f"  - [ROUTE] {type(route).__name__}")
print("🔍 라우트 확인 완료")

# 라우트 우선순위 경고
print("⚠️ 라우트 우선순위: 더 구체적인 라우트가 먼저 등록되어야 함")
print("   /api/chatbot/{path:path} vs /{service}/{path:path}")

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


# ===== 인증(예시) - 직접 app에 등록 =====
@app.post("/login", summary="로그인")
async def login():
    print("🚀 /login 엔드포인트 호출됨!")
    return {"message": "로그인 요청 받음"}

print("🔧 /login 라우트가 app에 직접 등록됨!")


@app.post("/signup", summary="회원가입")
async def signup(request: Request):
    try:
        print("🚀 /signup 엔드포인트 호출됨!")
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

print("🔧 /signup 라우트가 app에 직접 등록됨!")

# ===== 임시 테스트 - 직접 앱에 라우트 등록 =====
@app.post("/test-signup")
async def test_signup_direct():
    print("🚀 직접 등록된 /test-signup 호출됨!")
    return {"message": "직접 등록된 signup 성공!", "status": "OK"}

# ===== 라우트 디버깅 =====
print("🔍 앱 시작 시 라우트 디버깅 시작")

def debug_routes():
    print("🔍 등록된 모든 라우트:")
    for route in app.routes:
        try:
            # 안전한 속성 접근
            methods = getattr(route, 'methods', None)
            path = getattr(route, 'path', None)
            
            if methods and path:
                print(f"  - {methods} {path}")
            elif path:
                print(f"  - [NO METHODS] {path}")
            else:
                print(f"  - [ROUTE] {type(route).__name__}")
        except Exception:
            # 모든 예외를 무시하고 계속
            print(f"  - [ROUTE] {type(route).__name__}")
    
debug_routes()


# ===== 동적 프록시 라우팅 =====
# 임시 비활성화: 구체적인 라우트와 충돌 방지
# @gateway_router.get("/{service}/{path:path}", summary="GET 프록시")
async def proxy_get_disabled(service: str, path: str, request: Request):
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


# 임시 비활성화: 구체적인 라우트와 충돌 방지
# @gateway_router.post("/{service}/{path:path}", summary="POST 프록시")
async def proxy_post_disabled(
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


# 임시 비활성화: 구체적인 라우트와 충돌 방지
# @gateway_router.put("/{service}/{path:path}", summary="PUT 프록시")
async def proxy_put_disabled(service: str, path: str, request: Request):
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


# 임시 비활성화: 구체적인 라우트와 충돌 방지
# @gateway_router.delete("/{service}/{path:path}", summary="DELETE 프록시")
async def proxy_delete_disabled(service: str, path: str, request: Request):
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


# 임시 비활성화: 구체적인 라우트와 충돌 방지  
# @gateway_router.patch("/{service}/{path:path}", summary="PATCH 프록시")
async def proxy_patch_disabled(service: str, path: str, request: Request):
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

@app.get("/api/chatbot/direct-test")
async def direct_chatbot_test():
    """app 레벨 직접 chatbot 테스트"""
    logger.error("🚨 app 레벨 chatbot 테스트 호출됨!!!")
    print("🚨 app 레벨 chatbot 테스트 호출됨!!!")
    return {"message": "app 레벨 chatbot 라우트 작동!", "level": "app"}

# ===== 라우터 이미 등록 완료 =====
print("🔧 모든 라우터 등록 완료!")

# ===== 로컬 실행 =====
if __name__ == "__main__":
    import uvicorn
    # Railway PORT 환경변수 사용
    port = int(os.getenv("PORT", os.getenv("SERVICE_PORT", 8080)))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
