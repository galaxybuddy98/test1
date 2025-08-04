# MSA Gateway

마이크로서비스 아키텍처(MSA) 게이트웨이 시스템입니다.

## 🏗️ 아키텍처

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Client        │    │   Nginx         │    │   Gateway       │
│   (Browser)     │───▶│   (Load Balancer)│───▶│   (API Gateway) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
                       ┌─────────────────┐            │
                       │   Redis         │            │
                       │   (Cache)       │            │
                       └─────────────────┘            │
                                                       │
                       ┌─────────────────┐            │
                       │   User Service  │◀───────────┘
                       │   (Port 8001)   │
                       └─────────────────┘
                                                       │
                       ┌─────────────────┐            │
                       │   Order Service │◀───────────┘
                       │   (Port 8002)   │
                       └─────────────────┘
                                                       │
                       ┌─────────────────┐            │
                       │   Product       │◀───────────┘
                       │   Service       │
                       │   (Port 8003)   │
                       └─────────────────┘
```

## 🚀 빠른 시작

### 1. 환경 설정

#### Windows
```bash
# 설치 스크립트 실행
install.bat

# 또는 수동 설치
python -m pip install -r requirements.txt
```

#### Linux/Mac
```bash
# 설치 스크립트 실행
chmod +x install.sh
./install.sh

# 또는 수동 설치
pip install -r requirements.txt
```

### 2. Docker로 실행

```bash
# 개발 환경 실행
docker-compose up -d

# 프로덕션 환경 실행
docker-compose -f docker-compose.prod.yml up -d

# 상태 확인
docker-compose ps

# 로그 확인
docker-compose logs -f
```

### 3. 직접 실행

```bash
# 게이트웨이 실행
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 사용자 서비스 실행
cd services/user-service
python -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload

# 주문 서비스 실행
cd services/order-service
python -m uvicorn main:app --host 0.0.0.0 --port 8002 --reload

# 상품 서비스 실행
cd services/product-service
python -m uvicorn main:app --host 0.0.0.0 --port 8003 --reload
```

## 📋 API 엔드포인트

### 게이트웨이 API

| 엔드포인트 | 메서드 | 설명 |
|-----------|--------|------|
| `/` | GET | 루트 페이지 |
| `/health` | GET | 헬스 체크 |
| `/metrics` | GET | 서비스 메트릭 |
| `/services` | GET | 등록된 서비스 목록 |
| `/api/{service}/{path}` | GET/POST/PUT/DELETE | 서비스 프록시 |

### 서비스 디스커버리 API

| 엔드포인트 | 메서드 | 설명 |
|-----------|--------|------|
| `/discovery/register` | POST | 서비스 등록 |
| `/discovery/unregister/{id}` | DELETE | 서비스 등록 해제 |
| `/discovery/services` | GET | 모든 서비스 조회 |
| `/discovery/services/{id}` | GET | 특정 서비스 조회 |
| `/discovery/heartbeat/{id}` | POST | 하트비트 업데이트 |
| `/discovery/cleanup` | POST | 비활성 서비스 정리 |

### 사용자 서비스 API

| 엔드포인트 | 메서드 | 설명 |
|-----------|--------|------|
| `/users` | GET | 모든 사용자 조회 |
| `/users/{id}` | GET | 특정 사용자 조회 |
| `/users` | POST | 새 사용자 생성 |
| `/users/{id}` | PUT | 사용자 정보 업데이트 |
| `/users/{id}` | DELETE | 사용자 삭제 |

### 주문 서비스 API

| 엔드포인트 | 메서드 | 설명 |
|-----------|--------|------|
| `/orders` | GET | 모든 주문 조회 |
| `/orders/{id}` | GET | 특정 주문 조회 |
| `/orders` | POST | 새 주문 생성 |
| `/orders/{id}` | PUT | 주문 정보 업데이트 |
| `/orders/{id}` | DELETE | 주문 삭제 |
| `/orders/user/{user_id}` | GET | 사용자별 주문 조회 |

### 상품 서비스 API

| 엔드포인트 | 메서드 | 설명 |
|-----------|--------|------|
| `/products` | GET | 모든 상품 조회 |
| `/products/{id}` | GET | 특정 상품 조회 |
| `/products` | POST | 새 상품 생성 |
| `/products/{id}` | PUT | 상품 정보 업데이트 |
| `/products/{id}` | DELETE | 상품 삭제 |
| `/products/category/{category}` | GET | 카테고리별 상품 조회 |

## 🧪 테스트

### 게이트웨이 테스트

```bash
# 전체 테스트 실행
python test_gateway.py

# 특정 URL로 테스트
python test_gateway.py http://localhost:8000
```

### API 테스트

```bash
# 게이트웨이 헬스 체크
curl http://localhost:8000/health

# 서비스 목록 조회
curl http://localhost:8000/discovery/services

# 사용자 목록 조회
curl http://localhost:8000/api/user-service/users

# 상품 목록 조회
curl http://localhost:8000/api/product-service/products
```

## 🛠️ 개발

### 프로젝트 구조

```
gateway/
├── app/
│   ├── main.py                 # 메인 애플리케이션
│   └── domain/
│       └── discovery/
│           ├── controller/
│           │   └── discovery_controller.py
│           └── model/
│               └── service_registry.py
├── services/
│   ├── user-service/
│   │   ├── main.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   ├── order-service/
│   │   ├── main.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   └── product-service/
│       ├── main.py
│       ├── Dockerfile
│       └── requirements.txt
├── nginx/
│   └── nginx.conf
├── docker-compose.yml
├── docker-compose.prod.yml
├── Dockerfile
├── Dockerfile.dev
├── requirements.txt
├── test_gateway.py
└── README.md
```

### 환경 변수

| 변수명 | 기본값 | 설명 |
|--------|--------|------|
| `GATEWAY_HOST` | `0.0.0.0` | 게이트웨이 호스트 |
| `GATEWAY_PORT` | `8000` | 게이트웨이 포트 |
| `ENVIRONMENT` | `development` | 실행 환경 |
| `LOG_LEVEL` | `INFO` | 로그 레벨 |

## 📊 모니터링

### 헬스 체크

```bash
# 게이트웨이 헬스 체크
curl http://localhost:8000/health

# 개별 서비스 헬스 체크
curl http://localhost:8001/health  # 사용자 서비스
curl http://localhost:8002/health  # 주문 서비스
curl http://localhost:8003/health  # 상품 서비스
```

### 메트릭

```bash
# 서비스 메트릭 조회
curl http://localhost:8000/metrics
```

### 로그 확인

```bash
# Docker 로그
docker-compose logs -f gateway
docker-compose logs -f user-service
docker-compose logs -f order-service
docker-compose logs -f product-service

# 또는 스크립트 사용
./docker-commands.sh logs
```

## 🔧 문제 해결

### 일반적인 문제들

1. **포트 충돌**
   ```bash
   # 포트 사용 확인
   netstat -tulpn | grep 8000
   
   # 프로세스 종료
   kill -9 <PID>
   ```

2. **Docker 컨테이너 문제**
   ```bash
   # 컨테이너 재시작
   docker-compose restart
   
   # 컨테이너 재빌드
   docker-compose build --no-cache
   ```

3. **서비스 연결 문제**
   ```bash
   # 네트워크 확인
   docker network ls
   docker network inspect msa-network
   ```

### 로그 레벨 변경

```bash
# 환경 변수로 로그 레벨 설정
export LOG_LEVEL=DEBUG
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 📝 라이센스

이 프로젝트는 MIT 라이센스 하에 배포됩니다.

## 🤝 기여

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 지원

문제가 있거나 질문이 있으시면 이슈를 생성해주세요. 