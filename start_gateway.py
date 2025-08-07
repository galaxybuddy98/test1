#!/usr/bin/env python3
"""
프로젝트 루트에서 Gateway API 서버를 시작하는 스크립트
"""
import os
import sys
import subprocess

def main():
    # 프로젝트 루트에서 gateway 폴더로 이동해서 실행
    project_root = os.path.dirname(os.path.abspath(__file__))
    gateway_dir = os.path.join(project_root, "gateway")
    
    if not os.path.exists(gateway_dir):
        print(f"❌ gateway 폴더를 찾을 수 없습니다: {gateway_dir}")
        sys.exit(1)
    
    print("🚀 ERIpotter Gateway API 서버를 시작합니다...")
    print(f"📁 프로젝트 루트: {project_root}")
    print(f"📁 Gateway 디렉토리: {gateway_dir}")
    print("📍 서버 주소: http://localhost:8080")
    print("📍 API 문서: http://localhost:8080/docs")
    print("📍 Health Check: http://localhost:8080/health")
    print("-" * 50)
    
    try:
        # gateway 폴더에서 uvicorn 실행
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
        print(f"작업 디렉토리: {gateway_dir}")
        
        # 작업 디렉토리를 gateway로 변경해서 실행
        subprocess.run(cmd, cwd=gateway_dir)
        
    except KeyboardInterrupt:
        print("\n🛑 서버가 중지되었습니다.")
    except Exception as e:
        print(f"❌ 서버 실행 중 오류: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
