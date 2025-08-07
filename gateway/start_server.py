#!/usr/bin/env python3
"""
FastAPI 서버 시작 스크립트
"""
import os
import sys

# 현재 디렉토리를 Python path에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def main():
    try:
        import uvicorn
        print("✅ uvicorn 모듈을 성공적으로 import했습니다.")
        
        # FastAPI 앱 실행
        print("🚀 서버를 시작합니다...")
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0", 
            port=8080, 
            reload=True,
            log_level="info"
        )
        
    except ImportError as e:
        print(f"❌ uvicorn import 에러: {e}")
        print("💡 해결 방법: pip install uvicorn")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ 서버 시작 에러: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
