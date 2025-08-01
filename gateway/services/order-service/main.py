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
    title="Order Service",
    description="주문 관리 마이크로서비스",
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

# 임시 주문 데이터 (실제로는 데이터베이스 사용)
orders_db = {
    "1": {
        "id": "1",
        "user_id": "1",
        "items": [
            {"product_id": "1", "quantity": 2, "price": 29.99},
            {"product_id": "2", "quantity": 1, "price": 49.99}
        ],
        "total_amount": 109.97,
        "status": "pending",
        "created_at": "2024-01-01T10:00:00Z",
        "updated_at": "2024-01-01T10:00:00Z"
    },
    "2": {
        "id": "2",
        "user_id": "2",
        "items": [
            {"product_id": "3", "quantity": 1, "price": 19.99}
        ],
        "total_amount": 19.99,
        "status": "completed",
        "created_at": "2024-01-02T14:30:00Z",
        "updated_at": "2024-01-02T15:00:00Z"
    }
}

@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "service": "order-service",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {
        "status": "healthy",
        "service": "order-service",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/orders")
async def get_orders():
    """모든 주문 조회"""
    return {
        "orders": list(orders_db.values()),
        "count": len(orders_db),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/orders/{order_id}")
async def get_order(order_id: str):
    """특정 주문 조회"""
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="주문을 찾을 수 없습니다.")
    
    return orders_db[order_id]

@app.post("/orders")
async def create_order(order_data: Dict):
    """새 주문 생성"""
    order_id = str(uuid.uuid4())
    
    # 총 금액 계산
    total_amount = sum(item["price"] * item["quantity"] for item in order_data.get("items", []))
    
    new_order = {
        "id": order_id,
        "user_id": order_data.get("user_id"),
        "items": order_data.get("items", []),
        "total_amount": total_amount,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    orders_db[order_id] = new_order
    
    return {
        "message": "주문이 성공적으로 생성되었습니다.",
        "order": new_order
    }

@app.put("/orders/{order_id}")
async def update_order(order_id: str, order_data: Dict):
    """주문 정보 업데이트"""
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="주문을 찾을 수 없습니다.")
    
    # 기존 주문 정보 업데이트
    orders_db[order_id].update(order_data)
    orders_db[order_id]["updated_at"] = datetime.now().isoformat()
    
    return {
        "message": "주문 정보가 성공적으로 업데이트되었습니다.",
        "order": orders_db[order_id]
    }

@app.delete("/orders/{order_id}")
async def delete_order(order_id: str):
    """주문 삭제"""
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="주문을 찾을 수 없습니다.")
    
    deleted_order = orders_db.pop(order_id)
    
    return {
        "message": "주문이 성공적으로 삭제되었습니다.",
        "order": deleted_order
    }

@app.get("/orders/user/{user_id}")
async def get_orders_by_user(user_id: str):
    """사용자별 주문 조회"""
    user_orders = [
        order for order in orders_db.values()
        if order["user_id"] == user_id
    ]
    
    return {
        "orders": user_orders,
        "count": len(user_orders),
        "user_id": user_id
    }

@app.put("/orders/{order_id}/status")
async def update_order_status(order_id: str, status_data: Dict):
    """주문 상태 업데이트"""
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="주문을 찾을 수 없습니다.")
    
    new_status = status_data.get("status")
    valid_statuses = ["pending", "processing", "shipped", "delivered", "cancelled", "completed"]
    
    if new_status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"유효하지 않은 상태입니다. 가능한 상태: {valid_statuses}")
    
    orders_db[order_id]["status"] = new_status
    orders_db[order_id]["updated_at"] = datetime.now().isoformat()
    
    return {
        "message": f"주문 상태가 '{new_status}'로 업데이트되었습니다.",
        "order": orders_db[order_id]
    }

@app.get("/orders/status/{status}")
async def get_orders_by_status(status: str):
    """상태별 주문 조회"""
    status_orders = [
        order for order in orders_db.values()
        if order["status"] == status
    ]
    
    return {
        "orders": status_orders,
        "count": len(status_orders),
        "status": status
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002) 