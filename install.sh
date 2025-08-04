#!/bin/bash

# MSA Gateway 설치 스크립트

set -e

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 로그 함수
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Python 설치 확인
check_python() {
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3가 설치되지 않았습니다."
        log_info "Python 3를 설치해주세요: https://www.python.org/downloads/"
        exit 1
    fi
    
    log_success "Python 3가 설치되어 있습니다."
}

# pip 설치 확인
check_pip() {
    if ! command -v pip3 &> /dev/null; then
        log_error "pip3가 설치되지 않았습니다."
        log_info "pip3를 설치해주세요."
        exit 1
    fi
    
    log_success "pip3가 설치되어 있습니다."
}

# 가상환경 생성
create_venv() {
    log_info "Python 가상환경을 생성합니다..."
    
    if [ -d "venv" ]; then
        log_warning "가상환경이 이미 존재합니다."
        read -p "기존 가상환경을 삭제하고 새로 생성하시겠습니까? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf venv
        else
            log_info "기존 가상환경을 사용합니다."
            return
        fi
    fi
    
    python3 -m venv venv
    log_success "가상환경이 생성되었습니다."
}

# 가상환경 활성화
activate_venv() {
    log_info "가상환경을 활성화합니다..."
    source venv/bin/activate
    log_success "가상환경이 활성화되었습니다."
}

# Python 패키지 설치
install_packages() {
    log_info "Python 패키지를 설치합니다..."
    pip install --upgrade pip
    pip install -r requirements.txt
    log_success "Python 패키지 설치가 완료되었습니다."
}

# Docker 설치 확인
check_docker() {
    if ! command -v docker &> /dev/null; then
        log_warning "Docker가 설치되지 않았습니다."
        log_info "Docker를 설치해주세요: https://docs.docker.com/get-docker/"
        return 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        log_warning "Docker Compose가 설치되지 않았습니다."
        log_info "Docker Compose를 설치해주세요: https://docs.docker.com/compose/install/"
        return 1
    fi
    
    log_success "Docker 및 Docker Compose가 설치되어 있습니다."
    return 0
}

# 프로젝트 구조 생성
create_project_structure() {
    log_info "프로젝트 구조를 생성합니다..."
    
    # 디렉토리 생성
    mkdir -p services/user-service
    mkdir -p services/order-service
    mkdir -p services/product-service
    mkdir -p nginx/conf.d
    mkdir -p logs
    
    log_success "프로젝트 구조가 생성되었습니다."
}

# 스크립트 권한 설정
set_permissions() {
    log_info "스크립트 권한을 설정합니다..."
    chmod +x docker-commands.sh
    chmod +x install.sh
    log_success "스크립트 권한이 설정되었습니다."
}

# 설치 완료 메시지
show_completion() {
    echo ""
    log_success "=== 설치가 완료되었습니다! ==="
    echo ""
    echo "다음 명령어로 서비스를 시작할 수 있습니다:"
    echo "  ./docker-commands.sh start"
    echo ""
    echo "또는 직접 실행:"
    echo "  python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
    echo ""
    echo "도움말:"
    echo "  ./docker-commands.sh help"
    echo ""
}

# 메인 설치 로직
main() {
    log_info "MSA Gateway 설치를 시작합니다..."
    
    # 시스템 요구사항 확인
    check_python
    check_pip
    
    # 프로젝트 구조 생성
    create_project_structure
    
    # 가상환경 생성 및 활성화
    create_venv
    activate_venv
    
    # Python 패키지 설치
    install_packages
    
    # Docker 확인
    if check_docker; then
        log_success "Docker 환경이 준비되었습니다."
    else
        log_warning "Docker가 설치되지 않아 컨테이너 실행이 불가능합니다."
    fi
    
    # 스크립트 권한 설정
    set_permissions
    
    # 설치 완료
    show_completion
}

# 스크립트 실행
main "$@"
