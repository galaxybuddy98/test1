



from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

# Pydantic 모델 정의
class UserResponse(BaseModel):
    id: Optional[int] = None
    username: str
    email: str
    message: str = "Success"

class UserRegisterRequest(BaseModel):
    username: str
    email: str
    password: str

class UserLoginRequest(BaseModel):
    email: str
    password: str

class UserLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    username: str

# 라우터 생성 - prefix 없이 생성
router = APIRouter(tags=["User Authentication"])

@router.post("/api/auth/register", response_model=UserResponse, summary="회원가입")
async def register(user_data: UserRegisterRequest):
    """사용자 회원가입"""
    try:
        # 여기서 실제 회원가입 로직을 구현하거나
        # account-service로 프록시할 수 있습니다
        return UserResponse(
            username=user_data.username,
            email=user_data.email,
            message="회원가입이 완료되었습니다."
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/api/auth/login", response_model=UserLoginResponse, summary="로그인")
async def login(user_data: UserLoginRequest):
    """사용자 로그인"""
    try:
        # 여기서 실제 로그인 로직을 구현하거나
        # account-service로 프록시할 수 있습니다
        return UserLoginResponse(
            access_token="dummy_token",
            user_id=1,
            username=user_data.email.split('@')[0]
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/api/auth/me", response_model=UserResponse, summary="사용자 정보 조회")
async def get_user_info():
    """현재 로그인한 사용자 정보 조회"""
    try:
        return UserResponse(
            username="test_user",
            email="test@example.com",
            message="사용자 정보 조회 성공"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
