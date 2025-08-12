from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from .user_model import UserCreate, UserLogin, UserResponse, TokenResponse
from .user_Service import UserService
from .user_repository import UserRepository

# JWT Bearer 토큰 스키마
security = HTTPBearer()

# 의존성 주입을 위한 함수들 (main.py에서 DB 세션 설정 후 사용)
async def get_user_service(db: AsyncSession) -> UserService:
    """UserService 의존성 주입"""
    user_repository = UserRepository(db)
    return UserService(user_repository)

def create_auth_router() -> APIRouter:
    """인증 라우터 생성 함수"""
    router = APIRouter(prefix="/auth", tags=["Authentication"])
    
    @router.post("/register", response_model=UserResponse, summary="회원가입")
    async def register(
        user_data: UserCreate,
        user_service: UserService = Depends(get_user_service)
    ):
        """
        새 사용자를 등록합니다.
        - username: 사용자명 (중복 불가)
        - email: 이메일 (중복 불가)
        - password: 비밀번호 (자동으로 해싱됨)
        - company_id: 회사 ID (선택)
        - role: 역할 (기본값: user)
        """
        user = await user_service.register_user(user_data)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="사용자명 또는 이메일이 이미 존재합니다."
            )
        return user

    @router.post("/login", response_model=TokenResponse, summary="로그인")
    async def login(
        login_data: UserLogin,
        user_service: UserService = Depends(get_user_service)
    ):
        """
        사용자명과 비밀번호로 로그인합니다.
        성공 시 JWT 토큰과 사용자 정보를 반환합니다.
        """
        token_response = await user_service.login_user(login_data)
        if not token_response:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="사용자명 또는 비밀번호가 잘못되었습니다.",
                headers={"WWW-Authenticate": "Bearer"}
            )
        return token_response

    @router.get("/verify", response_model=UserResponse, summary="토큰 검증")
    async def verify_token(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        user_service: UserService = Depends(get_user_service)
    ):
        """
        JWT 토큰을 검증하고 현재 사용자 정보를 반환합니다.
        Authorization 헤더에 Bearer 토큰을 포함해야 합니다.
        """
        user = await user_service.get_current_user(credentials.credentials)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="유효하지 않은 토큰입니다.",
                headers={"WWW-Authenticate": "Bearer"}
            )
        return user

    @router.get("/me", response_model=UserResponse, summary="내 정보 조회")
    async def get_current_user_info(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        user_service: UserService = Depends(get_user_service)
    ):
        """
        현재 로그인한 사용자의 정보를 조회합니다.
        """
        user = await user_service.get_current_user(credentials.credentials)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="인증이 필요합니다.",
                headers={"WWW-Authenticate": "Bearer"}
            )
        return user

    @router.post("/logout", summary="로그아웃")
    async def logout():
        """
        사용자를 로그아웃합니다.
        (JWT는 stateless이므로 클라이언트에서 토큰을 삭제하면 됨)
        """
        return {
            "success": True,
            "message": "로그아웃되었습니다. 클라이언트에서 토큰을 삭제해주세요."
        }
    
    return router

# 라우터 생성
auth_router = create_auth_router()

# UserController 클래스 (구조적 정리용, 실제 라우팅은 위의 함수들 사용)
class UserController:
    """사용자 인증 및 관리 컨트롤러 (참조용)"""
    
    def __init__(self):
        self.router = auth_router
    
    @staticmethod
    def get_router():
        return auth_router
