from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.user.controller.user_controller import UserController
from app.domain.user.model.user_model import UserCreate, UserLogin, UserResponse, TokenResponse
from app.main import get_database

router = APIRouter(prefix="/api/account", tags=["account"])

# JWT 토큰 검증을 위한 security
security = HTTPBearer()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate, db: AsyncSession = Depends(get_database)):
    """사용자 회원가입"""
    controller = UserController()
    return await controller.register_user(user_data)

@router.post("/login", response_model=TokenResponse)
async def login_user(login_data: UserLogin, db: AsyncSession = Depends(get_database)):
    """사용자 로그인"""
    controller = UserController()
    return await controller.login_user(login_data)

@router.get("/me", response_model=UserResponse)
async def get_current_user(credentials = Depends(security), db: AsyncSession = Depends(get_database)):
    """현재 사용자 정보 조회"""
    controller = UserController()
    return await controller.get_current_user(credentials)
