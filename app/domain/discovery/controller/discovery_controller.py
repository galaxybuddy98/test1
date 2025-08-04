from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List, Optional
import uuid
from datetime import datetime

from ..model.service_registry import ServiceRegistry, ServiceInfo


class DiscoveryController:
    """서비스 디스커버리 컨트롤러"""
    
    def __init__(self, service_registry: ServiceRegistry):
        self.service_registry = service_registry
        self.router = APIRouter(prefix="/discovery", tags=["discovery"])
        self._setup_routes()
    
    def _setup_routes(self):
        """라우터 설정"""
        
        @self.router.post("/register")
        async def register_service(service_data: Dict):
            """서비스 등록"""
            try:
                service_id = service_data.get("service_id") or str(uuid.uuid4())
                service_name = service_data.get("service_name")
                service_url = service_data.get("service_url")
                health_check_url = service_data.get("health_check_url")
                metadata = service_data.get("metadata", {})
                
                if not service_name or not service_url:
                    raise HTTPException(
                        status_code=400, 
                        detail="service_name과 service_url은 필수입니다."
                    )
                
                service_info = ServiceInfo(
                    service_id=service_id,
                    service_name=service_name,
                    service_url=service_url,
                    health_check_url=health_check_url,
                    metadata=metadata
                )
                
                success = self.service_registry.register_service(service_info)
                if not success:
                    raise HTTPException(
                        status_code=409,
                        detail=f"서비스 ID '{service_id}'가 이미 등록되어 있습니다."
                    )
                
                return {
                    "success": True,
                    "service_id": service_id,
                    "message": "서비스가 성공적으로 등록되었습니다.",
                    "service_info": service_info.to_dict()
                }
                
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"서비스 등록 중 오류가 발생했습니다: {str(e)}"
                )
        
        @self.router.delete("/unregister/{service_id}")
        async def unregister_service(service_id: str):
            """서비스 등록 해제"""
            try:
                success = self.service_registry.unregister_service(service_id)
                if not success:
                    raise HTTPException(
                        status_code=404,
                        detail=f"서비스 ID '{service_id}'를 찾을 수 없습니다."
                    )
                
                return {
                    "success": True,
                    "message": f"서비스 '{service_id}'가 성공적으로 등록 해제되었습니다."
                }
                
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"서비스 등록 해제 중 오류가 발생했습니다: {str(e)}"
                )
        
        @self.router.get("/services")
        async def get_all_services(active_only: bool = False):
            """모든 서비스 조회"""
            try:
                if active_only:
                    services = self.service_registry.get_active_services()
                else:
                    services = self.service_registry.get_all_services()
                
                return {
                    "success": True,
                    "services": [service.to_dict() for service in services],
                    "count": len(services)
                }
                
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"서비스 조회 중 오류가 발생했습니다: {str(e)}"
                )
        
        @self.router.get("/services/{service_id}")
        async def get_service(service_id: str):
            """특정 서비스 조회"""
            try:
                service = self.service_registry.get_service(service_id)
                if not service:
                    raise HTTPException(
                        status_code=404,
                        detail=f"서비스 ID '{service_id}'를 찾을 수 없습니다."
                    )
                
                return {
                    "success": True,
                    "service": service.to_dict()
                }
                
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"서비스 조회 중 오류가 발생했습니다: {str(e)}"
                )
        
        @self.router.get("/services/name/{service_name}")
        async def get_services_by_name(service_name: str):
            """서비스 이름으로 서비스 조회"""
            try:
                services = self.service_registry.get_service_by_name(service_name)
                
                return {
                    "success": True,
                    "services": [service.to_dict() for service in services],
                    "count": len(services)
                }
                
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"서비스 조회 중 오류가 발생했습니다: {str(e)}"
                )
        
        @self.router.post("/heartbeat/{service_id}")
        async def update_heartbeat(service_id: str):
            """서비스 하트비트 업데이트"""
            try:
                success = self.service_registry.update_heartbeat(service_id)
                if not success:
                    raise HTTPException(
                        status_code=404,
                        detail=f"서비스 ID '{service_id}'를 찾을 수 없습니다."
                    )
                
                return {
                    "success": True,
                    "message": f"서비스 '{service_id}'의 하트비트가 업데이트되었습니다.",
                    "timestamp": datetime.now().isoformat()
                }
                
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"하트비트 업데이트 중 오류가 발생했습니다: {str(e)}"
                )
        
        @self.router.post("/cleanup")
        async def cleanup_inactive_services(timeout_seconds: int = 30):
            """비활성 서비스 정리"""
            try:
                inactive_services = self.service_registry.cleanup_inactive_services(timeout_seconds)
                
                return {
                    "success": True,
                    "message": f"{len(inactive_services)}개의 비활성 서비스가 정리되었습니다.",
                    "inactive_services": inactive_services,
                    "timeout_seconds": timeout_seconds
                }
                
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"서비스 정리 중 오류가 발생했습니다: {str(e)}"
                )
        
        @self.router.get("/health")
        async def health_check():
            """헬스 체크"""
            try:
                active_services = self.service_registry.get_active_services()
                total_services = len(self.service_registry.get_all_services())
                
                return {
                    "status": "healthy",
                    "active_services": len(active_services),
                    "total_services": total_services,
                    "timestamp": datetime.now().isoformat()
                }
                
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"헬스 체크 중 오류가 발생했습니다: {str(e)}"
                )
    
    def get_router(self) -> APIRouter:
        """라우터 반환"""
        return self.router
