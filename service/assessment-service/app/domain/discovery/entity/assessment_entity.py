from datetime import datetime
from typing import Optional

class AssessmentEntity:
    """평가 엔티티 클래스 - 간단한 데이터 모델"""
    
    def __init__(self, title: str, description: str, assessment_type: str, 
                 company_id: Optional[str] = None, status: str = 'draft', assessment_id: Optional[int] = None):
        """AssessmentEntity 초기화"""
        self.id = assessment_id
        self.title = title
        self.description = description
        self.assessment_type = assessment_type
        self.company_id = company_id
        self.status = status
        self.is_active = True
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def __repr__(self):
        return f"<AssessmentEntity(id={self.id}, title='{self.title}', type='{self.assessment_type}')>"
    
    def to_dict(self):
        """엔티티를 딕셔너리로 변환"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'assessment_type': self.assessment_type,
            'company_id': self.company_id,
            'status': self.status,
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
        """딕셔너리에서 AssessmentEntity 인스턴스 생성"""
        return cls(
            title=data.get('title', ''),
            description=data.get('description', ''),
            assessment_type=data.get('assessment_type', ''),
            company_id=data.get('company_id'),
            status=data.get('status', 'draft'),
            assessment_id=data.get('id')
        )
    
    def validate(self):
        """엔티티 데이터 유효성 검증"""
        errors = []
        
        if not self.title or len(self.title) < 3:
            errors.append("평가 제목은 3자 이상이어야 합니다.")
        
        if not self.description or len(self.description) < 10:
            errors.append("평가 설명은 10자 이상이어야 합니다.")
        
        if not self.assessment_type:
            errors.append("평가 유형이 필요합니다.")
        
        return errors
