# 멀티스테이지 빌드 - 프로덕션용
FROM python:3.11-slim as builder

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 업데이트 및 필요한 패키지 설치
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 파일 복사
COPY requirements.txt .

# Python 패키지 설치
RUN pip install --no-cache-dir --user -r requirements.txt

# 프로덕션 이미지
FROM python:3.11-slim

# 보안을 위한 비root 사용자 생성
RUN groupadd -r appuser && useradd -r -g appuser appuser

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# builder 스테이지에서 Python 패키지 복사
COPY --from=builder /root/.local /root/.local

# PATH에 Python 패키지 경로 추가
ENV PATH=/root/.local/bin:$PATH

# 애플리케이션 코드 복사
COPY app/ ./app/

# 포트 노출
EXPOSE 8080

# 헬스체크 설정
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# 비root 사용자로 전환
USER appuser

# 애플리케이션 실행
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
