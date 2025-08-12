from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from typing import Optional
from .user_model import UserModel
from .user_entitiy import UserEntity

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
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
            self.db.add(db_user)
            await self.db.commit()
            await self.db.refresh(db_user)
            return db_user
        except IntegrityError:
            await self.db.rollback()
            return None
    
    async def get_user_by_username(self, username: str) -> Optional[UserModel]:
        """사용자명으로 사용자 조회"""
        result = await self.db.execute(
            select(UserModel).where(UserModel.username == username)
        )
        return result.scalar_one_or_none()
    
    async def get_user_by_email(self, email: str) -> Optional[UserModel]:
        """이메일로 사용자 조회"""
        result = await self.db.execute(
            select(UserModel).where(UserModel.email == email)
        )
        return result.scalar_one_or_none()
    
    async def get_user_by_id(self, user_id: int) -> Optional[UserModel]:
        """ID로 사용자 조회"""
        result = await self.db.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def verify_user_credentials(self, username: str, password_hash: str) -> Optional[UserModel]:
        """사용자 인증 (사용자명과 비밀번호 해시로 확인)"""
        result = await self.db.execute(
            select(UserModel).where(
                UserModel.username == username,
                UserModel.password_hash == password_hash,
                UserModel.is_active == True
            )
        )
        return result.scalar_one_or_none()
    
    async def update_user(self, user_id: int, update_data: dict) -> Optional[UserModel]:
        """사용자 정보 업데이트"""
        user = await self.get_user_by_id(user_id)
        if user:
            for key, value in update_data.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            await self.db.commit()
            await self.db.refresh(user)
        return user