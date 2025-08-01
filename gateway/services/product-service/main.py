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
    title="Product Service",
    description="상품 관리 마이크로서비스",
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

# 임시 상품 데이터 (실제로는 데이터베이스 사용)
products_db = {
    "1": {
        "id": "1",
        "name": "노트북",
        "description": "고성능 노트북",
        "price": 999.99,
        "category": "electronics",
        "stock": 50,
        "image_url": "https://example.com/laptop.jpg",
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z",
        "status": "active"
    },
    "2": {
        "id": "2",
        "name": "스마트폰",
        "description": "최신 스마트폰",
        "price": 699.99,
        "category": "electronics",
        "stock": 100,
        "image_url": "https://example.com/smartphone.jpg",
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z",
        "status": "active"
    },
    "3": {
        "id": "3",
        "name": "책상",
        "description": "편안한 책상",
        "price": 199.99,
        "category": "furniture",
        "stock": 25,
        "image_url": "https://example.com/desk.jpg",
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z",
        "status": "active"
    }
}

@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "service": "product-service",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {
        "status": "healthy",
        "service": "product-service",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/products")
async def get_products():
    """모든 상품 조회"""
    return {
        "products": list(products_db.values()),
        "count": len(products_db),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/products/{product_id}")
async def get_product(product_id: str):
    """특정 상품 조회"""
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다.")
    
    return products_db[product_id]

@app.post("/products")
async def create_product(product_data: Dict):
    """새 상품 생성"""
    product_id = str(uuid.uuid4())
    
    new_product = {
        "id": product_id,
        "name": product_data.get("name"),
        "description": product_data.get("description"),
        "price": product_data.get("price", 0.0),
        "category": product_data.get("category"),
        "stock": product_data.get("stock", 0),
        "image_url": product_data.get("image_url"),
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "status": "active"
    }
    
    products_db[product_id] = new_product
    
    return {
        "message": "상품이 성공적으로 생성되었습니다.",
        "product": new_product
    }

@app.put("/products/{product_id}")
async def update_product(product_id: str, product_data: Dict):
    """상품 정보 업데이트"""
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다.")
    
    # 기존 상품 정보 업데이트
    products_db[product_id].update(product_data)
    products_db[product_id]["updated_at"] = datetime.now().isoformat()
    
    return {
        "message": "상품 정보가 성공적으로 업데이트되었습니다.",
        "product": products_db[product_id]
    }

@app.delete("/products/{product_id}")
async def delete_product(product_id: str):
    """상품 삭제"""
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다.")
    
    deleted_product = products_db.pop(product_id)
    
    return {
        "message": "상품이 성공적으로 삭제되었습니다.",
        "product": deleted_product
    }

@app.get("/products/category/{category}")
async def get_products_by_category(category: str):
    """카테고리별 상품 조회"""
    category_products = [
        product for product in products_db.values()
        if product["category"] == category
    ]
    
    return {
        "products": category_products,
        "count": len(category_products),
        "category": category
    }

@app.get("/products/search/{keyword}")
async def search_products(keyword: str):
    """상품 검색"""
    matching_products = [
        product for product in products_db.values()
        if keyword.lower() in product["name"].lower() or 
           keyword.lower() in product["description"].lower()
    ]
    
    return {
        "products": matching_products,
        "count": len(matching_products),
        "search_term": keyword
    }

@app.put("/products/{product_id}/stock")
async def update_stock(product_id: str, stock_data: Dict):
    """재고 업데이트"""
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다.")
    
    new_stock = stock_data.get("stock", 0)
    if new_stock < 0:
        raise HTTPException(status_code=400, detail="재고는 0 이상이어야 합니다.")
    
    products_db[product_id]["stock"] = new_stock
    products_db[product_id]["updated_at"] = datetime.now().isoformat()
    
    return {
        "message": f"재고가 {new_stock}로 업데이트되었습니다.",
        "product": products_db[product_id]
    }

@app.get("/products/price-range")
async def get_products_by_price_range(min_price: float = 0, max_price: float = 999999):
    """가격 범위별 상품 조회"""
    price_range_products = [
        product for product in products_db.values()
        if min_price <= product["price"] <= max_price
    ]
    
    return {
        "products": price_range_products,
        "count": len(price_range_products),
        "price_range": {"min": min_price, "max": max_price}
    }

@app.get("/categories")
async def get_categories():
    """모든 카테고리 조회"""
    categories = list(set(product["category"] for product in products_db.values()))
    
    return {
        "categories": categories,
        "count": len(categories)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003) 