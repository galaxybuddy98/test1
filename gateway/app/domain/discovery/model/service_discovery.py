import httpx
import logging
from typing import Optional, Dict, Any
from .service_type import ServiceType

logger = logging.getLogger("service_discovery")

class ServiceDiscovery:
    """
    서비스 디스커버리 및 요청 프록시 클래스
    """
    
    # 서비스별 기본 URL 매핑
    SERVICE_URLS = {
        ServiceType.USER: "http://localhost:8001",
        ServiceType.AUTH: "http://localhost:8002", 
        ServiceType.PAYMENT: "http://localhost:8003",
        ServiceType.NOTIFICATION: "http://localhost:8004",
        ServiceType.FILE: "http://localhost:8005",
        ServiceType.REPORT: "http://localhost:8006",
    }
    
    def __init__(self, service_type: ServiceType):
        self.service_type = service_type
        self.base_url = self.SERVICE_URLS.get(service_type)
        
        if not self.base_url:
            raise ValueError(f"지원되지 않는 서비스 타입: {service_type}")
    
    async def request(
        self,
        method: str,
        path: str,
        headers: Optional[Dict[str, Any]] = None,
        body: Optional[bytes] = None,
        files: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        timeout: int = 30
    ) -> httpx.Response:
        """
        대상 서비스로 HTTP 요청 전송
        """
        url = f"{self.base_url}/{path.lstrip('/')}"
        
        logger.info(f"요청 전송: {method} {url}")
        
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                if method.upper() == "GET":
                    response = await client.get(
                        url, 
                        headers=headers, 
                        params=params
                    )
                elif method.upper() == "POST":
                    if files:
                        response = await client.post(
                            url, 
                            headers=headers, 
                            files=files, 
                            params=params
                        )
                    else:
                        response = await client.post(
                            url, 
                            headers=headers, 
                            content=body, 
                            params=params,
                            data=data
                        )
                elif method.upper() == "PUT":
                    response = await client.put(
                        url, 
                        headers=headers, 
                        content=body, 
                        params=params
                    )
                elif method.upper() == "DELETE":
                    response = await client.delete(
                        url, 
                        headers=headers, 
                        content=body, 
                        params=params
                    )
                elif method.upper() == "PATCH":
                    response = await client.patch(
                        url, 
                        headers=headers, 
                        content=body, 
                        params=params
                    )
                else:
                    raise ValueError(f"지원되지 않는 HTTP 메서드: {method}")
                
                logger.info(f"응답 받음: {response.status_code}")
                return response
                
        except httpx.TimeoutException:
            logger.error(f"요청 타임아웃: {url}")
            raise
        except httpx.RequestError as e:
            logger.error(f"요청 오류: {url}, 에러: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"예상치 못한 오류: {url}, 에러: {str(e)}")
            raise

