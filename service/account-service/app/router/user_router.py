from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any

from app.domain.user.controller.user_controller import UserController
from app.domain.user.service.user_service import UserService
from app.domain.user.repository.user_repository import UserRepository
from app.domain.user.model.user_model import UserCreate, UserLogin, UserResponse, TokenResponse

# JWT 토큰 검증을 위한 security
security = HTTPBearer()

router = APIRouter(prefix="/auth", tags=["Authentication"])

# 의존성 주입 함수들
def get_user_controller() -> UserController:
    return UserController()

@router.post("/register", response_model=UserResponse, summary="회원가입")
async def register(
    user_data: UserCreate,
    controller: UserController = Depends(get_user_controller)
):
    """새 사용자를 등록합니다."""
    return await controller.register_user(user_data)

@router.post("/login", response_model=TokenResponse, summary="로그인")
async def login(
    login_data: UserLogin,
    controller: UserController = Depends(get_user_controller)
):
    """사용자 로그인을 수행합니다."""
    return await controller.login_user(login_data)

@router.get("/me", response_model=UserResponse, summary="현재 사용자 정보")
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    controller: UserController = Depends(get_user_controller)
):
    """현재 로그인한 사용자의 정보를 조회합니다."""
    return await controller.get_current_user(credentials)

@router.get("/health", summary="서비스 상태 확인")
async def health_check():
    """서비스 상태를 확인합니다."""
    return {"service": "Account Service", "status": "healthy"}
