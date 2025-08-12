from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from ..service.user_service import UserService
from ..model.user_model import UserCreate, UserLogin, UserResponse, TokenResponse

logger = logging.getLogger("account_service")

# JWT Bearer 토큰 스키마
security = HTTPBearer()

class UserController:
    def __init__(self, user_service: UserService):
        self.user_service = user_service
    
    async def register_user(self, user_data: UserCreate) -> UserResponse:
        """사용자 회원가입"""
        try:
            result = await self.user_service.register_user(user_data)
            if result:
                return result
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="사용자명 또는 이메일이 이미 존재합니다."
                )
        except Exception as e:
            logger.error(f"회원가입 오류: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="회원가입 중 오류가 발생했습니다."
            )
    
    async def login_user(self, login_data: UserLogin) -> TokenResponse:
        """사용자 로그인"""
        try:
            result = await self.user_service.login_user(login_data)
            if result:
                return result
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="잘못된 사용자명 또는 비밀번호입니다."
                )
        except Exception as e:
            logger.error(f"로그인 오류: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="로그인 중 오류가 발생했습니다."
            )
    
    async def get_current_user(self, credentials: HTTPAuthorizationCredentials = Depends(security)) -> UserResponse:
        """현재 사용자 정보 조회"""
        try:
            token = credentials.credentials
            user = await self.user_service.get_current_user(token)
            if user:
                return user
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="유효하지 않은 토큰입니다."
                )
        except Exception as e:
            logger.error(f"사용자 정보 조회 오류: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="인증에 실패했습니다."
            )
