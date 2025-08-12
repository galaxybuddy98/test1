from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import os
from .user_repository import UserRepository
from .user_entitiy import UserEntity
from .user_model import UserCreate, UserLogin, UserResponse, TokenResponse

# 비밀번호 해싱 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT 설정
SECRET_KEY = os.getenv("SECRET_KEY") or os.getenv("JWT_SECRET", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def hash_password(self, password: str) -> str:
        """비밀번호 해싱"""
        return pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """비밀번호 검증"""
        return pwd_context.verify(plain_password, hashed_password)
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        """JWT 토큰 생성"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[dict]:
        """JWT 토큰 검증"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                return None
            return payload
        except JWTError:
            return None
    
    async def register_user(self, user_data: UserCreate) -> Optional[UserResponse]:
        """사용자 회원가입"""
        # 사용자명 중복 확인
        existing_user = await self.user_repository.get_user_by_username(user_data.username)
        if existing_user:
            return None
        
        # 이메일 중복 확인
        existing_email = await self.user_repository.get_user_by_email(user_data.email)
        if existing_email:
            return None
        
        # 비밀번호 해싱
        hashed_password = self.hash_password(user_data.password)
        
        # UserEntity 생성
        user_entity = UserEntity(
            username=user_data.username,
            email=user_data.email,
            password_hash=hashed_password,
            company_id=user_data.company_id,
            role=user_data.role
        )
        
        # DB에 저장
        db_user = await self.user_repository.create_user(user_entity)
        if db_user:
            return UserResponse.model_validate(db_user)
        return None
    
    async def authenticate_user(self, login_data: UserLogin) -> Optional[UserResponse]:
        """사용자 로그인 인증"""
        # 사용자 조회
        user = await self.user_repository.get_user_by_username(login_data.username)
        if not user:
            return None
        
        # 비밀번호 검증
        if not self.verify_password(login_data.password, user.password_hash):
            return None
        
        return UserResponse.model_validate(user)
    
    async def login_user(self, login_data: UserLogin) -> Optional[TokenResponse]:
        """사용자 로그인 (토큰 생성 포함)"""
        user = await self.authenticate_user(login_data)
        if not user:
            return None
        
        # JWT 토큰 생성
        access_token = self.create_access_token(
            data={"sub": user.username, "user_id": user.id, "role": user.role}
        )
        
        return TokenResponse(
            access_token=access_token,
            user=user
        )
    
    async def get_current_user(self, token: str) -> Optional[UserResponse]:
        """토큰으로 현재 사용자 조회"""
        payload = self.verify_token(token)
        if not payload:
            return None
        
        username = payload.get("sub")
        if not username:
            return None
        
        user = await self.user_repository.get_user_by_username(username)
        if user:
            return UserResponse.model_validate(user)
        return None