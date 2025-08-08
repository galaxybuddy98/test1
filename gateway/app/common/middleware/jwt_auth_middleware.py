# app/common/middleware/jwt_auth_middleware.py
from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import logging

logger = logging.getLogger("jwt_auth_middleware")

class AuthMiddleware(BaseHTTPMiddleware):
    """
    JWT 인증 미들웨어
    - /, /health, /api/v1/health, /docs, /openapi.json 등은 인증 제외
    - 트레일링 슬래시 허용 (/health/ == /health)
    - OPTIONS/HEAD 요청은 패스(프리플라이트 포함)
    """

    def __init__(self, app):
        super().__init__(app)

        # 인증이 필요하지 않은 '정확 일치' 경로들
        self.excluded_paths = {
            "/",
            "/docs",
            "/openapi.json",
            "/redoc",
            "/health",               # 메인 앱 health
            "/login",
            "/signup",
            "/user/login",
            "/user/signup",
            "/auth/login",
            "/auth/register",
        }

        # 인증이 필요하지 않은 '접두사' 경로들(문서 정적 리소스 등)
        self.excluded_prefixes = (
            "/docs/",                # e.g., /docs/oauth2-redirect
            "/static/",              # 문서 정적파일이 여기에 매핑된 경우
        )

    async def dispatch(self, request: Request, call_next):
        try:
            raw_path = request.url.path
            method = request.method.upper()

            # 디버깅 로그
            logger.info(f"🔍 요청 경로: {raw_path} | 메서드: {method}")

            # 1) 프리플라이트/HEAD는 통과
            if method in ("OPTIONS", "HEAD"):
                return await call_next(request)

            # 2) 경로 정규화: 트레일링 슬래시 제거 (빈 문자열이면 "/")
            path = raw_path.rstrip("/") or "/"

            # 3) 인증 제외 경로/접두사면 통과
            if path in self.excluded_paths or any(path.startswith(p) for p in self.excluded_prefixes):
                logger.info(f"✅ 인증 제외 경로: {path}")
                return await call_next(request)

            # 4) 이하부터는 인증 필요
            authorization = request.headers.get("Authorization")
            if not authorization:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Authorization header가 필요합니다."},
                )

            if not authorization.startswith("Bearer "):
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Bearer 토큰이 필요합니다."},
                )

            token = authorization.split(" ", 1)[1]

            # TODO: 실제 환경에서는 JWT 디코드/검증 로직으로 교체
            if token != "mock_jwt_token_123":
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "유효하지 않은 토큰입니다."},
                )

            # 5) 다운스트림 서비스용 사용자 헤더 부착 (starlette 내부 구조 이용)
            try:
                request.headers.__dict__["_list"].append((b"x-user-id", b"test_user"))
            except Exception:  # 방어적 처리
                pass

            # 6) 다음 미들웨어/엔드포인트로
            return await call_next(request)

        except Exception as e:
            logger.error(f"JWT 미들웨어 오류: {e}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "인증 처리 중 서버 오류가 발생했습니다."},
            )
