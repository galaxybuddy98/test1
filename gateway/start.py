#!/usr/bin/env python3
"""
Gateway API 서버 시작 스크립트
"""
import os
import sys
import subprocess

def main():
    # 현재 디렉토리를 Python path에 추가
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    print("🚀 ERIpotter Gateway API 서버를 시작합니다...")
    print(f"📁 작업 디렉토리: {current_dir}")
    print("📍 서버 주소: http://localhost:8080")
    print("📍 API 문서: http://localhost:8080/docs")
    print("📍 Health Check: http://localhost:8080/health")
    print("📍 로그인: http://localhost:8080/api/v1/auth/login")
    print("-" * 50)
    
    try:
        # uvicorn으로 서버 실행
        cmd = [
            sys.executable, 
            "-m", 
            "uvicorn", 
            "app.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8080", 
            "--reload"
        ]
        
        print(f"실행 명령: {' '.join(cmd)}")
        subprocess.run(cmd, cwd=current_dir)
        
    except KeyboardInterrupt:
        print("\n🛑 서버가 중지되었습니다.")
    except Exception as e:
        print(f"❌ 서버 실행 중 오류: {e}")
        
        # 대체 방법으로 main.py 직접 실행
        print("🔄 대체 방법으로 서버를 시작합니다...")
        try:
            from app.main import app
            import uvicorn
            uvicorn.run(app, host="0.0.0.0", port=8080, reload=True)
        except Exception as e2:
            print(f"❌ 대체 방법도 실패: {e2}")
            sys.exit(1)

if __name__ == "__main__":
    main()
