from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import logging

logger = logging.getLogger("jwt_auth_middleware")

class AuthMiddleware(BaseHTTPMiddleware):
    """
    JWT 인증 미들웨어
    """
    
    def __init__(self, app):
        super().__init__(app)
        # 인증이 필요하지 않은 경로들
        self.excluded_paths = {
            "/",
            "/docs", 
            "/openapi.json",
            "/health",              # 메인 앱의 health check
            "/api/v1/health",       # gateway_router의 health check
            "/api/v1/login",        # gateway_router의 login
            "/api/v1/signup",       # gateway_router의 signup
            "/api/v1/auth/login",   # auth_router의 login
            "/api/v1/auth/register"
        }
    
    async def dispatch(self, request: Request, call_next):
        """
        요청을 처리하기 전 JWT 토큰 검증
        """
        try:
            # 디버깅: 요청 경로 로그
            logger.info(f"🔍 요청 경로: {request.url.path}")
            logger.info(f"🔍 제외 경로 목록: {self.excluded_paths}")
            
            # 인증이 필요하지 않은 경로는 건너뛰기
            if request.url.path in self.excluded_paths:
                logger.info(f"✅ 인증 제외 경로: {request.url.path}")
                response = await call_next(request)
                return response
            
            # JWT 토큰 검증 (현재는 간단한 테스트용)
            authorization = request.headers.get("Authorization")
            
            if not authorization:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Authorization header가 필요합니다."}
                )
            
            if not authorization.startswith("Bearer "):
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Bearer 토큰이 필요합니다."}
                )
            
            token = authorization.split(" ")[1]
            
            # 간단한 토큰 검증 (실제로는 JWT 디코딩 필요)
            if token != "mock_jwt_token_123":
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "유효하지 않은 토큰입니다."}
                )
            
            # 사용자 ID를 헤더에 추가 (다른 서비스에서 사용할 수 있도록)
            request.headers.__dict__["_list"].append(
                (b"x-user-id", b"test_user")
            )
            
            response = await call_next(request)
            return response
            
        except Exception as e:
            logger.error(f"JWT 미들웨어 오류: {str(e)}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "인증 처리 중 서버 오류가 발생했습니다."}
            )

