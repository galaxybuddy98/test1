from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

# 요청 모델 정의
class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    password: str
    email: str
    company_id: Optional[str] = None

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/login", summary="로그인")
async def login(request: LoginRequest):
    """
    사용자명과 비밀번호로 로그인합니다.
    """
    print(f"로그인 시도: {request.username}")
    
    # 임시 로그인 로직 (실제로는 데이터베이스 검증 필요)
    if request.username == "admin" and request.password == "password":
        return {
            "success": True,
            "message": "로그인 성공",
            "user": {
                "username": request.username,
                "role": "admin"
            },
            "token": "mock_jwt_token_123"
        }
    else:
        raise HTTPException(status_code=401, detail="사용자명 또는 비밀번호가 잘못되었습니다.")

@auth_router.post("/register", summary="회원가입")
async def register(request: RegisterRequest):
    """
    새 사용자를 등록합니다.
    """
    print(f"회원가입 시도: {request.username}, 이메일: {request.email}")
    
    # 임시 회원가입 로직 (실제로는 데이터베이스에 저장 필요)
    return {
        "success": True,
        "message": "회원가입 완료",
        "user": {
            "username": request.username,
            "email": request.email,
            "company_id": request.company_id
        }
    }

@auth_router.post("/logout", summary="로그아웃")
async def logout():
    """
    사용자를 로그아웃합니다.
    """
    return {
        "success": True,
        "message": "로그아웃되었습니다."
    }

@auth_router.get("/verify", summary="토큰 검증")
async def verify_token(token: str):
    """
    JWT 토큰을 검증합니다.
    """
    # 임시 토큰 검증 로직
    if token == "mock_jwt_token_123":
        return {
            "valid": True,
            "user": {
                "username": "admin",
                "role": "admin"
            }
        }
    else:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")