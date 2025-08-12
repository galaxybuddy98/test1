from datetime import datetime
from typing import Optional, Dict, Any

class ChatMessage:
    """채팅 메시지 엔티티 클래스"""
    
    def __init__(self, message: str, user_id: int, session_id: int, 
                 message_type: str = "user", response: Optional[str] = None,
                 tokens_used: Optional[int] = None, processing_time: Optional[float] = None,
                 message_id: Optional[int] = None):
        """ChatMessage 초기화"""
        self.id = message_id
        self.message = message
        self.user_id = user_id
        self.session_id = session_id
        self.message_type = message_type  # "user" 또는 "assistant"
        self.response = response
        self.tokens_used = tokens_used
        self.processing_time = processing_time
        self.created_at = datetime.now()
    
    def __repr__(self):
        return f"<ChatMessage(id={self.id}, user_id={self.user_id}, session_id={self.session_id}, type='{self.message_type}')>"
    
    def to_dict(self):
        """엔티티를 딕셔너리로 변환"""
        return {
            'id': self.id,
            'message': self.message,
            'user_id': self.user_id,
            'session_id': self.session_id,
            'message_type': self.message_type,
            'response': self.response,
            'tokens_used': self.tokens_used,
            'processing_time': self.processing_time,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """딕셔너리에서 ChatMessage 인스턴스 생성"""
        return cls(
            message=data.get('message', ''),
            user_id=data.get('user_id'),
            session_id=data.get('session_id'),
            message_type=data.get('message_type', 'user'),
            response=data.get('response'),
            tokens_used=data.get('tokens_used'),
            processing_time=data.get('processing_time'),
            message_id=data.get('id')
        )

class ChatSession:
    """채팅 세션 엔티티 클래스"""
    
    def __init__(self, user_id: int, session_title: Optional[str] = None,
                 session_id: Optional[int] = None):
        """ChatSession 초기화"""
        self.id = session_id
        self.user_id = user_id
        self.session_title = session_title or f"채팅 세션 {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        self.is_active = True
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def __repr__(self):
        return f"<ChatSession(id={self.id}, user_id={self.user_id}, title='{self.session_title}')>"
    
    def to_dict(self):
        """엔티티를 딕셔너리로 변환"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'session_title': self.session_title,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def update_title(self, new_title: str):
        """세션 제목 업데이트"""
        self.session_title = new_title
        self.updated_at = datetime.now()
    
    def deactivate(self):
        """세션 비활성화"""
        self.is_active = False
        self.updated_at = datetime.now()
    
    @classmethod
    def from_dict(cls, data: dict):
        """딕셔너리에서 ChatSession 인스턴스 생성"""
        return cls(
            user_id=data.get('user_id'),
            session_title=data.get('session_title'),
            session_id=data.get('id')
        )
