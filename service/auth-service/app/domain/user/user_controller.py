from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

# 간단한 요청 모델들
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    company_id: str = None
    role: str = "user"

class UserLogin(BaseModel):
    username: str
    password: str

# JWT Bearer 토큰 스키마
security = HTTPBearer()

def create_auth_router() -> APIRouter:
    """인증 라우터 생성 함수"""
    router = APIRouter(prefix="/auth", tags=["Authentication"])
    
    @router.post("/register", summary="회원가입")
    async def register(user_data: UserCreate):
        """
        새 사용자를 등록합니다.
        """
        try:
            # 간단한 더미 응답
            return {
                "success": True,
                "message": "회원가입 완료",
                "user": {
                    "username": user_data.username,
                    "email": user_data.email,
                    "role": user_data.role
                }
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"회원가입 실패: {str(e)}"
            )

    @router.post("/login", summary="로그인")
    async def login(login_data: UserLogin):
        """
        사용자명과 비밀번호로 로그인합니다.
        """
        try:
            # 간단한 더미 로그인
            if login_data.username == "admin" and login_data.password == "password":
                return {
                    "success": True,
                    "message": "로그인 성공",
                    "access_token": "mock_jwt_token_123",
                    "token_type": "bearer",
                    "user": {
                        "username": login_data.username,
                        "role": "admin"
                    }
                }
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="사용자명 또는 비밀번호가 잘못되었습니다."
                )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"로그인 처리 중 오류: {str(e)}"
            )

    @router.get("/verify", summary="토큰 검증")
    async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
        """
        JWT 토큰을 검증합니다.
        """
        try:
            token = credentials.credentials
            if token == "mock_jwt_token_123":
                return {
                    "valid": True,
                    "user": {
                        "username": "admin",
                        "role": "admin"
                    }
                }
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="유효하지 않은 토큰입니다."
                )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"토큰 검증 중 오류: {str(e)}"
            )

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

# UserController 클래스 (구조적 정리용, 실제 라우팅은 위의 함수들 사용)
class UserController:
    """사용자 인증 및 관리 컨트롤러 (참조용)"""
    
    def __init__(self):
        self.router = create_auth_router()
    
    @staticmethod
    def get_router():
        return create_auth_router()
