import json
import logging
from typing import Any, Dict
from fastapi.responses import JSONResponse
import httpx

logger = logging.getLogger("response_factory")

class ResponseFactory:
    """
    HTTP 응답을 생성하는 팩토리 클래스
    """
    
    @staticmethod
    def create_response(response: httpx.Response) -> JSONResponse:
        """
        httpx.Response를 FastAPI JSONResponse로 변환
        """
        try:
            # 응답 헤더 처리
            headers = dict(response.headers)
            
            # Content-Type이 없으면 기본값 설정
            if "content-type" not in headers:
                headers["content-type"] = "application/json"
            
            # 응답 본문 처리
            try:
                # JSON 응답인 경우
                if "application/json" in headers.get("content-type", ""):
                    content = response.json()
                else:
                    # 텍스트 응답인 경우
                    content = {"data": response.text}
            except json.JSONDecodeError:
                # JSON 파싱 실패시 텍스트로 처리
                content = {"data": response.text}
            except Exception:
                # 기타 오류시 기본 응답
                content = {"message": "응답 처리 중 오류가 발생했습니다."}
            
            return JSONResponse(
                content=content,
                status_code=response.status_code,
                headers=headers
            )
            
        except Exception as e:
            logger.error(f"응답 생성 중 오류: {str(e)}")
            return ResponseFactory.create_error_response(
                message="응답 처리 중 내부 오류가 발생했습니다.",
                status_code=500
            )
    
    @staticmethod
    def create_success_response(
        data: Any = None, 
        message: str = "성공", 
        status_code: int = 200
    ) -> JSONResponse:
        """
        성공 응답 생성
        """
        content = {
            "success": True,
            "message": message
        }
        
        if data is not None:
            content["data"] = data
        
        return JSONResponse(
            content=content,
            status_code=status_code
        )
    
    @staticmethod
    def create_error_response(
        message: str = "오류가 발생했습니다.", 
        error_code: str = None,
        details: Dict[str, Any] = None,
        status_code: int = 400
    ) -> JSONResponse:
        """
        에러 응답 생성
        """
        content = {
            "success": False,
            "message": message
        }
        
        if error_code:
            content["error_code"] = error_code
            
        if details:
            content["details"] = details
        
        return JSONResponse(
            content=content,
            status_code=status_code
        )
    
    @staticmethod
    def create_validation_error_response(
        errors: Dict[str, Any],
        message: str = "입력값 검증에 실패했습니다."
    ) -> JSONResponse:
        """
        유효성 검증 실패 응답 생성
        """
        return ResponseFactory.create_error_response(
            message=message,
            error_code="VALIDATION_ERROR",
            details={"validation_errors": errors},
            status_code=422
        )
    
    @staticmethod
    def create_not_found_response(
        resource: str = "리소스"
    ) -> JSONResponse:
        """
        404 Not Found 응답 생성
        """
        return ResponseFactory.create_error_response(
            message=f"요청한 {resource}를 찾을 수 없습니다.",
            error_code="NOT_FOUND",
            status_code=404
        )
    
    @staticmethod
    def create_unauthorized_response(
        message: str = "인증이 필요합니다."
    ) -> JSONResponse:
        """
        401 Unauthorized 응답 생성
        """
        return ResponseFactory.create_error_response(
            message=message,
            error_code="UNAUTHORIZED",
            status_code=401
        )
    
    @staticmethod
    def create_forbidden_response(
        message: str = "접근 권한이 없습니다."
    ) -> JSONResponse:
        """
        403 Forbidden 응답 생성
        """
        return ResponseFactory.create_error_response(
            message=message,
            error_code="FORBIDDEN",
            status_code=403
        )

