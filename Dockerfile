# ERIpotter MSA Project - Root Dockerfile
# Gateway를 중심으로 한 마이크로서비스 통합 컨테이너

FROM python:3.11-slim

WORKDIR /app

# 시스템 패키지 업데이트 및 필요한 패키지 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Gateway 의존성 설치
COPY gateway/requirements.txt ./gateway/
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r gateway/requirements.txt

# 프로젝트 전체 복사
COPY . .

# 환경 변수 설정
ENV PYTHONPATH=/app/gateway
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Gateway 포트 노출
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -fsS "http://localhost:${PORT}/health" || exit 1

# 비루트 사용자 생성 및 전환
RUN groupadd -r appuser && useradd -r -g appuser appuser \
    && chown -R appuser:appuser /app
USER appuser

# Gateway 실행 (직접 실행)
WORKDIR /app/gateway
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
