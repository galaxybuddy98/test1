FROM python:3.11-slim

# 1) 빌드 도구 + libpq (psycopg2용) + curl(헬스체크용)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev pkg-config curl \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2) 의존성 설치 (requirements.txt가 이 디렉토리에 있다고 가정)
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# 3) 앱 소스
COPY app/ /app/app

# 4) 로컬에서도 바로 뜨게 기본 포트 지정(로컬 전용), Railway에선 ${PORT} 사용
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# 5) (선택) 헬스체크: /health 엔드포인트 구현해두었을 때
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD curl -fsS http://127.0.0.1:${PORT}/health || exit 1

# 6) 실행
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
