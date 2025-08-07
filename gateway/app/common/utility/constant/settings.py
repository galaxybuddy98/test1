import os
from typing import Optional

class Settings:
    """
    애플리케이션 설정 클래스
    """
    
    def __init__(self):
        # 환경 변수에서 설정값 로드
        self.environment = os.getenv("ENVIRONMENT", "development")
        self.debug = os.getenv("DEBUG", "true").lower() == "true"
        self.service_port = int(os.getenv("SERVICE_PORT", 8080))
        self.jwt_secret_key = os.getenv("JWT_SECRET_KEY", "your-secret-key-here")
        self.jwt_algorithm = os.getenv("JWT_ALGORITHM", "HS256")
        self.jwt_expire_minutes = int(os.getenv("JWT_EXPIRE_MINUTES", 1440))  # 24시간
        
        # 데이터베이스 설정
        self.database_url = os.getenv("DATABASE_URL", "sqlite:///./app.db")
        
        # CORS 설정
        self.cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
        
        # 로깅 레벨
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        
        # 외부 서비스 URL들
        self.user_service_url = os.getenv("USER_SERVICE_URL", "http://localhost:8001")
        self.auth_service_url = os.getenv("AUTH_SERVICE_URL", "http://localhost:8002")
        self.payment_service_url = os.getenv("PAYMENT_SERVICE_URL", "http://localhost:8003")
        self.notification_service_url = os.getenv("NOTIFICATION_SERVICE_URL", "http://localhost:8004")
        self.file_service_url = os.getenv("FILE_SERVICE_URL", "http://localhost:8005")
        self.report_service_url = os.getenv("REPORT_SERVICE_URL", "http://localhost:8006")
    
    def is_production(self) -> bool:
        """프로덕션 환경인지 확인"""
        return self.environment.lower() == "production"
    
    def is_development(self) -> bool:
        """개발 환경인지 확인"""
        return self.environment.lower() == "development"
    
    def get_service_url(self, service_name: str) -> Optional[str]:
        """서비스 이름으로 URL 조회"""
        service_urls = {
            "user": self.user_service_url,
            "auth": self.auth_service_url,
            "payment": self.payment_service_url,
            "notification": self.notification_service_url,
            "file": self.file_service_url,
            "report": self.report_service_url,
        }
        return service_urls.get(service_name.lower())
    
    def __str__(self):
        return f"Settings(environment={self.environment}, port={self.service_port}, debug={self.debug})"

