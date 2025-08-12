from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
import asyncio
from typing import Dict, List, Optional
import logging
from datetime import datetime

from .domain.discovery.model.service_registry import ServiceRegistry, ServiceInfo
from .domain.discovery.controller.discovery_controller import DiscoveryController

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI 앱 생성
app = FastAPI(
    title="MSA Gateway",
    description="마이크로서비스 아키텍처 게이트웨이",
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

# 서비스 레지스트리 초기화
service_registry = ServiceRegistry()

# 디스커버리 컨트롤러 초기화
discovery_controller = DiscoveryController(service_registry)

# 디스커버리 라우터 등록
app.include_router(discovery_controller.get_router())

# HTTP 클라이언트 설정
http_client = httpx.AsyncClient(timeout=30.0)

@app.on_event("startup")
async def startup_event():
    """애플리케이션 시작 시 실행"""
    logger.info("MSA Gateway가 시작되었습니다.")
    
    # 기본 서비스 등록 (개발용)
    default_services = [
        {
            "service_id": "user-service-1",
            "service_name": "user-service",
            "service_url": "http://user-service:8001",
            "metadata": {"version": "1.0.0", "environment": "development"}
        },
        {
            "service_id": "order-service-1", 
            "service_name": "order-service",
            "service_url": "http://order-service:8002",
            "metadata": {"version": "1.0.0", "environment": "development"}
        },
        {
            "service_id": "product-service-1",
            "service_name": "product-service", 
            "service_url": "http://product-service:8003",
            "metadata": {"version": "1.0.0", "environment": "development"}
        }
    ]
    
    for service_data in default_services:
        service_info = ServiceInfo(**service_data)
        service_registry.register_service(service_info)
        logger.info(f"서비스 등록: {service_info.service_name}")

@app.on_event("shutdown")
async def shutdown_event():
    """애플리케이션 종료 시 실행"""
    logger.info("MSA Gateway가 종료되었습니다.")
    await http_client.aclose()

@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "message": "MSA Gateway에 오신 것을 환영합니다!",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "discovery": "/discovery",
            "health": "/health",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    try:
        active_services = service_registry.get_active_services()
        total_services = len(service_registry.get_all_services())
        
        return {
            "status": "healthy",
            "gateway": "running",
            "active_services": len(active_services),
            "total_services": total_services,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"헬스 체크 오류: {e}")
        raise HTTPException(status_code=500, detail="서비스 상태 확인 실패")

@app.get("/api/{service_name}/{path:path}")
async def proxy_request(service_name: str, path: str, request_method: str = "GET"):
    """서비스 프록시 요청"""
    try:
        # 서비스 조회
        services = service_registry.get_service_by_name(service_name)
        if not services:
            raise HTTPException(status_code=404, detail=f"서비스 '{service_name}'를 찾을 수 없습니다.")
        
        # 활성 서비스 중 첫 번째 선택 (로드 밸런싱은 향후 구현)
        service = services[0]
        if not service.is_active:
            raise HTTPException(status_code=503, detail=f"서비스 '{service_name}'가 비활성 상태입니다.")
        
        # 프록시 URL 구성
        target_url = f"{service.service_url}/{path}"
        
        # 요청 전달
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=request_method,
                url=target_url,
                timeout=30.0
            )
            
            return JSONResponse(
                content=response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
            
    except httpx.RequestError as e:
        logger.error(f"서비스 요청 오류: {e}")
        raise HTTPException(status_code=503, detail="서비스에 연결할 수 없습니다.")
    except Exception as e:
        logger.error(f"프록시 요청 오류: {e}")
        raise HTTPException(status_code=500, detail="요청 처리 중 오류가 발생했습니다.")

@app.post("/api/{service_name}/{path:path}")
async def proxy_post_request(service_name: str, path: str, data: Dict):
    """POST 요청 프록시"""
    return await proxy_request(service_name, path, "POST")

@app.put("/api/{service_name}/{path:path}")
async def proxy_put_request(service_name: str, path: str, data: Dict):
    """PUT 요청 프록시"""
    return await proxy_request(service_name, path, "PUT")

@app.delete("/api/{service_name}/{path:path}")
async def proxy_delete_request(service_name: str, path: str):
    """DELETE 요청 프록시"""
    return await proxy_request(service_name, path, "DELETE")

@app.get("/services")
async def list_services():
    """등록된 모든 서비스 목록"""
    services = service_registry.get_all_services()
    return {
        "services": [service.to_dict() for service in services],
        "count": len(services),
        "active_count": len([s for s in services if s.is_active])
    }

@app.get("/metrics")
async def get_metrics():
    """서비스 메트릭"""
    services = service_registry.get_all_services()
    active_services = [s for s in services if s.is_active]
    
    return {
        "total_services": len(services),
        "active_services": len(active_services),
        "inactive_services": len(services) - len(active_services),
        "service_types": list(set(s.service_name for s in services)),
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8006))
    uvicorn.run(app, host="0.0.0.0", port=port)
