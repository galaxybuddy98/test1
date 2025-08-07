@echo off
echo 🚀 ERIpotter Gateway API 서버를 시작합니다...
echo.

REM 현재 디렉토리 확인
echo 📁 현재 위치: %cd%
echo.

REM 가상환경 활성화
echo 🔄 가상환경 활성화 중...
call venv\Scripts\activate.bat

REM Python 버전 확인
echo 🐍 Python 버전:
python --version
echo.

REM 패키지 설치 상태 확인
echo 📦 설치된 패키지 확인:
pip list | findstr -i "fastapi uvicorn"
echo.

REM 서버 시작
echo 🌟 서버 시작 중...
echo 📍 접속 주소: http://localhost:8080
echo 📍 API 문서: http://localhost:8080/docs
echo 📍 Health Check: http://localhost:8080/health
echo.
echo ⚠️  서버를 중지하려면 Ctrl+C를 누르세요
echo.

echo 🔄 서버 시작 시도 중...
python start.py
if %errorlevel% neq 0 (
    echo 🔄 대체 방법으로 시도...
    python -m uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
)
