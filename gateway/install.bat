@echo off
setlocal enabledelayedexpansion

REM MSA Gateway Windows 설치 스크립트

echo [INFO] MSA Gateway 설치를 시작합니다...

REM Python 설치 확인
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python이 설치되지 않았습니다.
    echo [INFO] Python을 설치해주세요: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [SUCCESS] Python이 설치되어 있습니다.

REM pip 설치 확인
pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip이 설치되지 않았습니다.
    echo [INFO] pip을 설치해주세요.
    pause
    exit /b 1
)
echo [SUCCESS] pip이 설치되어 있습니다.

REM 프로젝트 구조 생성
echo [INFO] 프로젝트 구조를 생성합니다...
if not exist "services" mkdir services
if not exist "services\user-service" mkdir services\user-service
if not exist "services\order-service" mkdir services\order-service
if not exist "services\product-service" mkdir services\product-service
if not exist "nginx" mkdir nginx
if not exist "nginx\conf.d" mkdir nginx\conf.d
if not exist "logs" mkdir logs
echo [SUCCESS] 프로젝트 구조가 생성되었습니다.

REM 가상환경 생성
echo [INFO] Python 가상환경을 생성합니다...
if exist "venv" (
    echo [WARNING] 가상환경이 이미 존재합니다.
    set /p choice="기존 가상환경을 삭제하고 새로 생성하시겠습니까? (y/N): "
    if /i "!choice!"=="y" (
        rmdir /s /q venv
        python -m venv venv
        echo [SUCCESS] 가상환경이 재생성되었습니다.
    ) else (
        echo [INFO] 기존 가상환경을 사용합니다.
    )
) else (
    python -m venv venv
    echo [SUCCESS] 가상환경이 생성되었습니다.
)

REM 가상환경 활성화
echo [INFO] 가상환경을 활성화합니다...
call venv\Scripts\activate.bat
echo [SUCCESS] 가상환경이 활성화되었습니다.

REM Python 패키지 설치
echo [INFO] Python 패키지를 설치합니다...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
echo [SUCCESS] Python 패키지 설치가 완료되었습니다.

REM Docker 설치 확인
docker --version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Docker가 설치되지 않았습니다.
    echo [INFO] Docker를 설치해주세요: https://docs.docker.com/get-docker/
) else (
    docker-compose --version >nul 2>&1
    if errorlevel 1 (
        echo [WARNING] Docker Compose가 설치되지 않았습니다.
        echo [INFO] Docker Compose를 설치해주세요: https://docs.docker.com/compose/install/
    ) else (
        echo [SUCCESS] Docker 및 Docker Compose가 설치되어 있습니다.
    )
)

echo.
echo [SUCCESS] === 설치가 완료되었습니다! ===
echo.
echo 다음 명령어로 서비스를 시작할 수 있습니다:
echo   docker-compose up -d
echo.
echo 또는 직접 실행:
echo   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
echo.
echo 도움말:
echo   docker-compose --help
echo.

pause
