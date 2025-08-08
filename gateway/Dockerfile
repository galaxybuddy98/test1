# ---- builder ----
    FROM python:3.11-slim AS builder
    WORKDIR /app
    RUN apt-get update && apt-get install -y --no-install-recommends gcc g++ && rm -rf /var/lib/apt/lists/*
    COPY requirements.txt .
    # 시스템 경로에 설치(--user 사용 안 함)
    RUN pip install --no-cache-dir -r requirements.txt
    
    # ---- runtime ----
    FROM python:3.11-slim
    ENV PYTHONUNBUFFERED=1 \
        PORT=8080
    WORKDIR /app
    
    # 런타임 최소 패키지
    RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
    
    # builder에서 site-packages / bin 복사
    # (python:3.11-slim 기본 경로: /usr/local)
    COPY --from=builder /usr/local /usr/local
    
    # 앱 코드 복사: /app/app/main.py 형태
    COPY app/ ./app/
    
    # (선택) 노출 — 플랫폼이 실제로 사용하진 않음
    EXPOSE 8080
    
    # HEALTHCHECK도 할당 포트 사용 (쉘 폼으로 env 확장)
    HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
      CMD curl -fsS "http://localhost:${PORT:-8080}/health" || exit 1
    
    # 비루트 사용자 (원하면 유지)
    RUN groupadd -r appuser && useradd -r -g appuser appuser
    USER appuser
    
    # ★ 중요: python -m uvicorn + 동적 포트
    CMD sh -c "python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}"
    