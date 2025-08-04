from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List, Optional
import logging
from datetime import datetime
import uuid

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI 앱 생성
app = FastAPI(
    title="User Service",
    description="사용자 관리 마이크로서비스",
    version="1.0.0"
)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 임시 사용자 데이터 (실제로는 데이터베이스 사용)
users_db = {
    "1": {
        "id": "1",
        "username": "john_doe",
        "email": "john@example.com",
        "full_name": "John Doe",
        "created_at": "2024-01-01T00:00:00Z",
        "status": "active"
    },
    "2": {
        "id": "2", 
        "username": "jane_smith",
        "email": "jane@example.com",
        "full_name": "Jane Smith",
        "created_at": "2024-01-02T00:00:00Z",
        "status": "active"
    }
}

@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "service": "user-service",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {
        "status": "healthy",
        "service": "user-service",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/users")
async def get_users():
    """모든 사용자 조회"""
    return {
        "users": list(users_db.values()),
        "count": len(users_db),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/users/{user_id}")
async def get_user(user_id: str):
    """특정 사용자 조회"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    
    return users_db[user_id]

@app.post("/users")
async def create_user(user_data: Dict):
    """새 사용자 생성"""
    user_id = str(uuid.uuid4())
    
    new_user = {
        "id": user_id,
        "username": user_data.get("username"),
        "email": user_data.get("email"),
        "full_name": user_data.get("full_name"),
        "created_at": datetime.now().isoformat(),
        "status": "active"
    }
    
    users_db[user_id] = new_user
    
    return {
        "message": "사용자가 성공적으로 생성되었습니다.",
        "user": new_user
    }

@app.put("/users/{user_id}")
async def update_user(user_id: str, user_data: Dict):
    """사용자 정보 업데이트"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    
    # 기존 사용자 정보 업데이트
    users_db[user_id].update(user_data)
    
    return {
        "message": "사용자 정보가 성공적으로 업데이트되었습니다.",
        "user": users_db[user_id]
    }

@app.delete("/users/{user_id}")
async def delete_user(user_id: str):
    """사용자 삭제"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    
    deleted_user = users_db.pop(user_id)
    
    return {
        "message": "사용자가 성공적으로 삭제되었습니다.",
        "user": deleted_user
    }

@app.get("/users/search/{username}")
async def search_users_by_username(username: str):
    """사용자명으로 사용자 검색"""
    matching_users = [
        user for user in users_db.values()
        if username.lower() in user["username"].lower()
    ]
    
    return {
        "users": matching_users,
        "count": len(matching_users),
        "search_term": username
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 