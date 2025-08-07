from enum import Enum

class ServiceType(str, Enum):
    """
    마이크로서비스 타입 정의
    """
    USER = "user"
    AUTH = "auth"
    PAYMENT = "payment"
    NOTIFICATION = "notification"
    FILE = "file"
    REPORT = "report"
    
    @classmethod
    def get_all_services(cls):
        """모든 서비스 타입 반환"""
        return [service.value for service in cls]
    
    def __str__(self):
        return self.value

