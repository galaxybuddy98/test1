@echo off
echo 🚀 FastAPI 서버를 시작합니다...

REM 가상환경 활성화
call venv\Scripts\activate.bat

REM 패키지 설치 확인
pip list | findstr uvicorn
if %errorlevel% neq 0 (
    echo ❌ uvicorn이 설치되지 않았습니다. 설치 중...
    pip install uvicorn fastapi python-dotenv httpx
)

REM 서버 시작 (여러 방법 시도)
echo 방법 1: Python 모듈로 실행
python -m uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload

if %errorlevel% neq 0 (
    echo 방법 2: 직접 실행파일 사용
    .\venv\Scripts\uvicorn.exe app.main:app --host 0.0.0.0 --port 8080 --reload
)

if %errorlevel% neq 0 (
    echo 방법 3: Python 스크립트 직접 실행
    python app\main.py
)

if %errorlevel% neq 0 (
    echo 방법 4: 사용자 정의 스크립트 실행
    python start_server.py
)

pause
