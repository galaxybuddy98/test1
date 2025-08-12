from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import logging
import asyncpg
import os

from ..service.user_service import UserService
from ..repository.user_repository import UserRepository
from ..model.user_model import UserCreate, UserLogin, UserResponse, TokenResponse

logger = logging.getLogger("account_service")

# JWT Bearer 토큰 스키마
security = HTTPBearer()

class UserController:
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL", "")
        if "postgres://" in self.database_url:
            self.database_url = self.database_url.replace("postgres://", "postgresql://")
        self.conn_str = self.database_url.split("?")[0]  # 쿼리 파라미터 제거
    
    async def _get_db_connection(self):
        """데이터베이스 연결 생성"""
        try:
            # 여러 SSL 옵션 시도해서 연결
            for ssl_option in ['require', True, False, None]:
                try:
                    if ssl_option is None:
                        conn = await asyncpg.connect(self.conn_str)
                    else:
                        conn = await asyncpg.connect(self.conn_str, ssl=ssl_option)
                    return conn
                except Exception as e:
                    logger.warning(f"DB 연결 실패 (SSL: {ssl_option}): {e}")
                    continue
            raise Exception("모든 연결 방법 실패")
        except Exception as e:
            logger.error(f"데이터베이스 연결 오류: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="데이터베이스 연결 실패"
            )
    
    async def register_user(self, user_data: UserCreate) -> UserResponse:
        """사용자 회원가입"""
        try:
            conn = await self._get_db_connection()
            
            # 사용자명 중복 체크
            existing = await conn.fetchval(
                "SELECT id FROM users WHERE username = $1 OR email = $2",
                user_data.username, user_data.email
            )
            
            if existing:
                await conn.close()
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="사용자명 또는 이메일이 이미 존재합니다."
                )
            
            # 비밀번호 해싱
            from passlib.context import CryptContext
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            hashed_password = pwd_context.hash(user_data.password)
            
            # 사용자 생성
            result = await conn.fetchrow("""
                INSERT INTO users (username, email, password_hash, company_id, role)
                VALUES ($1, $2, $3, $4, $5)
                RETURNING id, username, email, company_id, role, is_active, created_at, updated_at
            """, user_data.username, user_data.email, hashed_password, 
                user_data.company_id, user_data.role)
            
            await conn.close()
            
            return UserResponse(
                id=result['id'],
                username=result['username'],
                email=result['email'],
                company_id=result['company_id'],
                role=result['role'],
                is_active=result['is_active'],
                created_at=result['created_at'],
                updated_at=result['updated_at']
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"회원가입 오류: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="회원가입 중 오류가 발생했습니다."
            )
    
    async def login_user(self, login_data: UserLogin) -> TokenResponse:
        """사용자 로그인"""
        try:
            conn = await self._get_db_connection()
            
            # 사용자 조회
            user = await conn.fetchrow(
                "SELECT * FROM users WHERE username = $1 AND is_active = true",
                login_data.username
            )
            
            if not user:
                await conn.close()
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="잘못된 사용자명 또는 비밀번호입니다."
                )
            
            # 비밀번호 검증
            from passlib.context import CryptContext
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            
            if not pwd_context.verify(login_data.password, user['password_hash']):
                await conn.close()
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="잘못된 사용자명 또는 비밀번호입니다."
                )
            
            # JWT 토큰 생성
            from jose import jwt
            from datetime import datetime, timedelta
            
            SECRET_KEY = os.getenv("SECRET_KEY") or os.getenv("JWT_SECRET", "your-secret-key-here")
            ALGORITHM = "HS256"
            ACCESS_TOKEN_EXPIRE_MINUTES = 30
            
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            expire = datetime.utcnow() + access_token_expires
            
            to_encode = {"sub": user['username'], "exp": expire}
            access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
            
            await conn.close()
            
            user_response = UserResponse(
                id=user['id'],
                username=user['username'],
                email=user['email'],
                company_id=user['company_id'],
                role=user['role'],
                is_active=user['is_active'],
                created_at=user['created_at'],
                updated_at=user['updated_at']
            )
            
            return TokenResponse(
                access_token=access_token,
                token_type="bearer",
                user=user_response
            )
            
        except HTTPException:
            raise
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
            
            # JWT 토큰 검증
            from jose import JWTError, jwt
            
            SECRET_KEY = os.getenv("SECRET_KEY") or os.getenv("JWT_SECRET", "your-secret-key-here")
            ALGORITHM = "HS256"
            
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                username: str = payload.get("sub")
                if username is None:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="유효하지 않은 토큰입니다."
                    )
            except JWTError:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="유효하지 않은 토큰입니다."
                )
            
            # 사용자 정보 조회
            conn = await self._get_db_connection()
            user = await conn.fetchrow(
                "SELECT * FROM users WHERE username = $1 AND is_active = true",
                username
            )
            
            await conn.close()
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="사용자를 찾을 수 없습니다."
                )
            
            return UserResponse(
                id=user['id'],
                username=user['username'],
                email=user['email'],
                company_id=user['company_id'],
                role=user['role'],
                is_active=user['is_active'],
                created_at=user['created_at'],
                updated_at=user['updated_at']
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"사용자 정보 조회 오류: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="인증에 실패했습니다."
            )
