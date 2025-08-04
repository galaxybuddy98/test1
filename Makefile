# 모든 명령어 앞에 'make' 를 붙여서 실행해야 함
# 🔧 공통 명령어
up:
	docker-compose up -d --build

down:
	docker-compose down

logs:
	docker-compose logs -f

restart:
	docker-compose down && docker-compose up -d --build

ps:
	docker-compose ps

# 🚀 마이크로서비스별 명령어

## gateway
build-gateway:
	docker-compose build gateway

up-gateway:
	docker-compose up -d gateway

down-gateway:
	docker-compose stop gateway

logs-gateway:
	docker-compose logs -f gateway

restart-gateway:
	docker-compose stop gateway && docker-compose up -d gateway

## assessment-service
build-assessment:
	docker-compose build assessment-service

up-assessment:
	docker-compose up -d assessment-service

down-assessment:
	docker-compose stop assessment-service

logs-assessment:
	docker-compose logs -f assessment-service

restart-assessment:
	docker-compose stop assessment-service && docker-compose up -d assessment-service

## chatbot-service
build-chatbot:
	docker-compose build chatbot-service

up-chatbot:
	docker-compose up -d chatbot-service

down-chatbot:
	docker-compose stop chatbot-service

logs-chatbot:
	docker-compose logs -f chatbot-service

restart-chatbot:
	docker-compose stop chatbot-service && docker-compose up -d chatbot-service

## monitoring-service
build-monitoring:
	docker-compose build monitoring-service

up-monitoring:
	docker-compose up -d monitoring-service

down-monitoring:
	docker-compose stop monitoring-service

logs-monitoring:
	docker-compose logs -f monitoring-service

restart-monitoring:
	docker-compose stop monitoring-service && docker-compose up -d monitoring-service

## report-service
build-report:
	docker-compose build report-service

up-report:
	docker-compose up -d report-service

down-report:
	docker-compose stop report-service

logs-report:
	docker-compose logs -f report-service

restart-report:
	docker-compose stop report-service && docker-compose up -d report-service

## request-service
build-request:
	docker-compose build request-service

up-request:
	docker-compose up -d request-service

down-request:
	docker-compose stop request-service

logs-request:
	docker-compose logs -f request-service

restart-request:
	docker-compose stop request-service && docker-compose up -d request-service

## response-service
build-response:
	docker-compose build response-service

up-response:
	docker-compose up -d response-service

down-response:
	docker-compose stop response-service

logs-response:
	docker-compose logs -f response-service

restart-response:
	docker-compose stop response-service && docker-compose up -d response-service

## frontend
build-frontend:
	docker-compose build frontend

up-frontend:
	docker-compose up -d frontend

down-frontend:
	docker-compose stop frontend

logs-frontend:
	docker-compose logs -f frontend

restart-frontend:
	docker-compose stop frontend && docker-compose up -d frontend

## redis
build-redis:
	docker-compose build redis

up-redis:
	docker-compose up -d redis

down-redis:
	docker-compose stop redis

logs-redis:
	docker-compose logs -f redis

restart-redis:
	docker-compose stop redis && docker-compose up -d redis

## n8n
build-n8n:
	docker-compose build n8n

up-n8n:
	docker-compose up -d n8n

down-n8n:
	docker-compose stop n8n

logs-n8n:
	docker-compose logs -f n8n

restart-n8n:
	docker-compose stop n8n && docker-compose up -d n8n

## nginx
build-nginx:
	docker-compose build nginx

up-nginx:
	docker-compose up -d nginx

down-nginx:
	docker-compose stop nginx

logs-nginx:
	docker-compose logs -f nginx

restart-nginx:
	docker-compose stop nginx && docker-compose up -d nginx

# 🔧 개발 도구 명령어
clean:
	docker-compose down -v --remove-orphans
	docker system prune -f

clean-all:
	docker-compose down -v --remove-orphans
	docker system prune -af
	docker volume prune -f

# 📊 상태 확인 명령어
status:
	docker-compose ps
	docker-compose top

health:
	docker-compose exec gateway curl -f http://localhost:8080/health || echo "Gateway health check failed"
	docker-compose exec assessment-service curl -f http://localhost:8001/health || echo "Assessment service health check failed"
	docker-compose exec chatbot-service curl -f http://localhost:8002/health || echo "Chatbot service health check failed"
	docker-compose exec monitoring-service curl -f http://localhost:8003/health || echo "Monitoring service health check failed"
	docker-compose exec report-service curl -f http://localhost:8004/health || echo "Report service health check failed"
	docker-compose exec request-service curl -f http://localhost:8005/health || echo "Request service health check failed"
	docker-compose exec response-service curl -f http://localhost:8006/health || echo "Response service health check failed"

# 🚀 배포 명령어
deploy:
	make down
	make clean
	make up
	make health

deploy-gateway:
	make down-gateway
	make build-gateway
	make up-gateway

deploy-frontend:
	make down-frontend
	make build-frontend
	make up-frontend

# 📝 로그 명령어
logs-all:
	docker-compose logs -f gateway assessment-service chatbot-service monitoring-service report-service request-service response-service frontend redis n8n nginx

logs-services:
	docker-compose logs -f assessment-service chatbot-service monitoring-service report-service request-service response-service

logs-infrastructure:
	docker-compose logs -f gateway frontend redis n8n nginx
