from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
import logging

from ..model.user_model import UserModel
from ..entity.user_entity import UserEntity

logger = logging.getLogger("account_service")

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_user(self, user_entity: UserEntity) -> Optional[UserModel]:
        """새 사용자 생성"""
        try:
            db_user = UserModel(
                username=user_entity.username,
                email=user_entity.email,
                password_hash=user_entity.password_hash,
                company_id=user_entity.company_id,
                role=user_entity.role
            )
            self.session.add(db_user)
            await self.session.commit()
            await self.session.refresh(db_user)
            return db_user
        except Exception as e:
            logger.error(f"사용자 생성 오류: {e}")
            await self.session.rollback()
            return None
    
    async def get_user_by_username(self, username: str) -> Optional[UserModel]:
        """사용자명으로 사용자 조회"""
        try:
            result = await self.session.execute(
                select(UserModel).where(UserModel.username == username)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"사용자명 조회 오류: {e}")
            return None
    
    async def get_user_by_email(self, email: str) -> Optional[UserModel]:
        """이메일로 사용자 조회"""
        try:
            result = await self.session.execute(
                select(UserModel).where(UserModel.email == email)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"이메일 조회 오류: {e}")
            return None
    
    async def get_user_by_id(self, user_id: int) -> Optional[UserModel]:
        """ID로 사용자 조회"""
        try:
            result = await self.session.execute(
                select(UserModel).where(UserModel.id == user_id)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"ID 조회 오류: {e}")
            return None
    
    async def verify_user_credentials(self, username: str, password_hash: str) -> Optional[UserModel]:
        """사용자 인증 정보 확인"""
        try:
            result = await self.session.execute(
                select(UserModel).where(
                    UserModel.username == username,
                    UserModel.password_hash == password_hash,
                    UserModel.is_active == True
                )
            )
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"인증 정보 확인 오류: {e}")
            return None
    
    async def update_user(self, user_id: int, update_data: dict) -> Optional[UserModel]:
        """사용자 정보 업데이트"""
        try:
            result = await self.session.execute(
                select(UserModel).where(UserModel.id == user_id)
            )
            user = result.scalar_one_or_none()
            if user:
                for key, value in update_data.items():
                    if hasattr(user, key):
                        setattr(user, key, value)
                await self.session.commit()
                await self.session.refresh(user)
                return user
            return None
        except Exception as e:
            logger.error(f"사용자 업데이트 오류: {e}")
            await self.session.rollback()
            return None
