from typing import Dict, List, Optional
from datetime import datetime
import json


class ServiceInfo:
    """서비스 정보를 담는 클래스"""
    
    def __init__(self, service_id: str, service_name: str, service_url: str, 
                 health_check_url: str = None, metadata: Dict = None):
        self.service_id = service_id
        self.service_name = service_name
        self.service_url = service_url
        self.health_check_url = health_check_url or f"{service_url}/health"
        self.metadata = metadata or {}
        self.registered_at = datetime.now()
        self.last_heartbeat = datetime.now()
        self.is_active = True
    
    def to_dict(self) -> Dict:
        """서비스 정보를 딕셔너리로 변환"""
        return {
            "service_id": self.service_id,
            "service_name": self.service_name,
            "service_url": self.service_url,
            "health_check_url": self.health_check_url,
            "metadata": self.metadata,
            "registered_at": self.registered_at.isoformat(),
            "last_heartbeat": self.last_heartbeat.isoformat(),
            "is_active": self.is_active
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ServiceInfo':
        """딕셔너리에서 서비스 정보 객체 생성"""
        service_info = cls(
            service_id=data["service_id"],
            service_name=data["service_name"],
            service_url=data["service_url"],
            health_check_url=data.get("health_check_url"),
            metadata=data.get("metadata", {})
        )
        service_info.registered_at = datetime.fromisoformat(data["registered_at"])
        service_info.last_heartbeat = datetime.fromisoformat(data["last_heartbeat"])
        service_info.is_active = data.get("is_active", True)
        return service_info


class ServiceRegistry:
    """서비스 레지스트리 클래스"""
    
    def __init__(self):
        self._services: Dict[str, ServiceInfo] = {}
    
    def register_service(self, service_info: ServiceInfo) -> bool:
        """서비스 등록"""
        if service_info.service_id in self._services:
            return False
        
        self._services[service_info.service_id] = service_info
        return True
    
    def unregister_service(self, service_id: str) -> bool:
        """서비스 등록 해제"""
        if service_id in self._services:
            del self._services[service_id]
            return True
        return False
    
    def get_service(self, service_id: str) -> Optional[ServiceInfo]:
        """서비스 ID로 서비스 정보 조회"""
        return self._services.get(service_id)
    
    def get_service_by_name(self, service_name: str) -> List[ServiceInfo]:
        """서비스 이름으로 서비스 정보 조회"""
        return [service for service in self._services.values() 
                if service.service_name == service_name]
    
    def get_all_services(self) -> List[ServiceInfo]:
        """모든 서비스 정보 조회"""
        return list(self._services.values())
    
    def get_active_services(self) -> List[ServiceInfo]:
        """활성 서비스만 조회"""
        return [service for service in self._services.values() 
                if service.is_active]
    
    def update_heartbeat(self, service_id: str) -> bool:
        """서비스 하트비트 업데이트"""
        if service_id in self._services:
            self._services[service_id].last_heartbeat = datetime.now()
            self._services[service_id].is_active = True
            return True
        return False
    
    def mark_service_inactive(self, service_id: str) -> bool:
        """서비스를 비활성으로 표시"""
        if service_id in self._services:
            self._services[service_id].is_active = False
            return True
        return False
    
    def cleanup_inactive_services(self, timeout_seconds: int = 30) -> List[str]:
        """비활성 서비스 정리"""
        current_time = datetime.now()
        inactive_services = []
        
        for service_id, service in self._services.items():
            time_diff = (current_time - service.last_heartbeat).total_seconds()
            if time_diff > timeout_seconds:
                service.is_active = False
                inactive_services.append(service_id)
        
        return inactive_services
    
    def to_dict(self) -> Dict:
        """레지스트리 전체를 딕셔너리로 변환"""
        return {
            "services": {service_id: service.to_dict() 
                        for service_id, service in self._services.items()}
        }
    
    def from_dict(self, data: Dict):
        """딕셔너리에서 레지스트리 복원"""
        self._services.clear()
        for service_id, service_data in data.get("services", {}).items():
            self._services[service_id] = ServiceInfo.from_dict(service_data)
