from datetime import datetime
from typing import Optional

class UserEntity:
    """사용자 엔티티 클래스 - 간단한 데이터 모델"""
    
    def __init__(self, username: str, email: str, password_hash: str, 
                 company_id: Optional[str] = None, role: str = 'user', user_id: Optional[int] = None):
        """UserEntity 초기화"""
        self.id = user_id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.company_id = company_id
        self.role = role
        self.is_active = True
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def __repr__(self):
        return f"<UserEntity(id={self.id}, username='{self.username}', email='{self.email}')>"
    
    def to_dict(self):
        """엔티티를 딕셔너리로 변환"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'company_id': self.company_id,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def update_from_dict(self, data: dict):
        """딕셔너리 데이터로 엔티티 업데이트"""
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'created_at']:
                setattr(self, key, value)
        self.updated_at = datetime.now()
    
    @classmethod
    def from_dict(cls, data: dict):
        """딕셔너리에서 UserEntity 인스턴스 생성"""
        return cls(
            username=data.get('username', ''),
            email=data.get('email', ''),
            password_hash=data.get('password_hash', ''),
            company_id=data.get('company_id'),
            role=data.get('role', 'user'),
            user_id=data.get('id')
        )
    
    def validate(self):
        """엔티티 데이터 유효성 검증"""
        errors = []
        
        if not self.username or len(self.username) < 3:
            errors.append("사용자명은 3자 이상이어야 합니다.")
        
        if not self.email or '@' not in self.email:
            errors.append("올바른 이메일 형식이 아닙니다.")
        
        if not self.password_hash:
            errors.append("비밀번호 해시가 필요합니다.")
        
        return errors