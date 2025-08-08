from typing import Optional, Any

# SQLAlchemy import (linter 무시)
# type: ignore를 사용하여 linter 경고 억제
try:
    from sqlalchemy.ext.asyncio import AsyncSession  # type: ignore
except ImportError:
    AsyncSession = Any

class UserRepository:
    def __init__(self, session: Any = None):
        """
        사용자 데이터 액세스를 담당하는 Repository 클래스
        
        Args:
            session: SQLAlchemy AsyncSession 인스턴스
        """
        self.session = session
    
    async def create_user(self, user_data: dict):
        """새 사용자 생성"""
        # 실제 구현 시 SQLAlchemy ORM 사용
        print(f"사용자 생성: {user_data}")
        return {"id": 1, **user_data}
    
    async def get_user_by_id(self, user_id: int):
        """ID로 사용자 조회"""
        # 실제 구현 시 데이터베이스 쿼리
        print(f"사용자 조회: {user_id}")
        return {"id": user_id, "username": "test_user"}
    
    async def get_user_by_username(self, username: str):
        """사용자명으로 사용자 조회"""
        # 실제 구현 시 데이터베이스 쿼리
        print(f"사용자명으로 조회: {username}")
        return {"id": 1, "username": username}
    
    async def update_user(self, user_id: int, user_data: dict):
        """사용자 정보 업데이트"""
        # 실제 구현 시 SQLAlchemy ORM 사용
        print(f"사용자 업데이트: {user_id}, {user_data}")
        return {"id": user_id, **user_data}
    
    async def delete_user(self, user_id: int):
        """사용자 삭제"""
        # 실제 구현 시 SQLAlchemy ORM 사용
        print(f"사용자 삭제: {user_id}")
        return True