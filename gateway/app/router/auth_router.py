from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

# 여기에 인증 관련 라우터들을 추가할 수 있습니다
