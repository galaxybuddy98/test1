#!/usr/bin/env python3
"""
MSA Gateway 테스트 스크립트
게이트웨이의 모든 기능을 테스트합니다.
"""

import asyncio
import httpx
import json
import time
from typing import Dict, List
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GatewayTester:
    """게이트웨이 테스트 클래스"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)
        self.test_results = []
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
    
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """테스트 결과 로깅"""
        status = "✅ PASS" if success else "❌ FAIL"
        logger.info(f"{status} - {test_name}")
        if details:
            logger.info(f"  {details}")
        
        self.test_results.append({
            "test": test_name,
            "success": success,
            "details": details
        })
    
    async def test_root_endpoint(self):
        """루트 엔드포인트 테스트"""
        try:
            response = await self.client.get(f"{self.base_url}/")
            if response.status_code == 200:
                data = response.json()
                self.log_test("루트 엔드포인트", True, f"버전: {data.get('version')}")
                return True
            else:
                self.log_test("루트 엔드포인트", False, f"상태 코드: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("루트 엔드포인트", False, f"오류: {str(e)}")
            return False
    
    async def test_health_check(self):
        """헬스 체크 테스트"""
        try:
            response = await self.client.get(f"{self.base_url}/health")
            if response.status_code == 200:
                data = response.json()
                self.log_test("헬스 체크", True, f"상태: {data.get('status')}")
                return True
            else:
                self.log_test("헬스 체크", False, f"상태 코드: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("헬스 체크", False, f"오류: {str(e)}")
            return False
    
    async def test_discovery_endpoints(self):
        """서비스 디스커버리 엔드포인트 테스트"""
        tests = [
            ("서비스 목록 조회", f"{self.base_url}/discovery/services"),
            ("헬스 체크", f"{self.base_url}/discovery/health"),
        ]
        
        results = []
        for test_name, url in tests:
            try:
                response = await self.client.get(url)
                if response.status_code == 200:
                    self.log_test(test_name, True)
                    results.append(True)
                else:
                    self.log_test(test_name, False, f"상태 코드: {response.status_code}")
                    results.append(False)
            except Exception as e:
                self.log_test(test_name, False, f"오류: {str(e)}")
                results.append(False)
        
        return all(results)
    
    async def test_service_registration(self):
        """서비스 등록 테스트"""
        test_service = {
            "service_name": "test-service",
            "service_url": "http://test-service:8000",
            "metadata": {"version": "1.0.0", "test": True}
        }
        
        try:
            # 서비스 등록
            response = await self.client.post(
                f"{self.base_url}/discovery/register",
                json=test_service
            )
            
            if response.status_code == 200:
                data = response.json()
                service_id = data.get("service_id")
                self.log_test("서비스 등록", True, f"서비스 ID: {service_id}")
                
                # 등록된 서비스 확인
                response = await self.client.get(f"{self.base_url}/discovery/services/{service_id}")
                if response.status_code == 200:
                    self.log_test("등록된 서비스 조회", True)
                    
                    # 서비스 등록 해제
                    response = await self.client.delete(f"{self.base_url}/discovery/unregister/{service_id}")
                    if response.status_code == 200:
                        self.log_test("서비스 등록 해제", True)
                        return True
                    else:
                        self.log_test("서비스 등록 해제", False, f"상태 코드: {response.status_code}")
                        return False
                else:
                    self.log_test("등록된 서비스 조회", False, f"상태 코드: {response.status_code}")
                    return False
            else:
                self.log_test("서비스 등록", False, f"상태 코드: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("서비스 등록 테스트", False, f"오류: {str(e)}")
            return False
    
    async def test_metrics_endpoint(self):
        """메트릭 엔드포인트 테스트"""
        try:
            response = await self.client.get(f"{self.base_url}/metrics")
            if response.status_code == 200:
                data = response.json()
                self.log_test("메트릭 조회", True, 
                            f"총 서비스: {data.get('total_services')}, "
                            f"활성 서비스: {data.get('active_services')}")
                return True
            else:
                self.log_test("메트릭 조회", False, f"상태 코드: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("메트릭 조회", False, f"오류: {str(e)}")
            return False
    
    async def test_proxy_routing(self):
        """프록시 라우팅 테스트"""
        # 실제 서비스가 없으므로 404 예상
        try:
            response = await self.client.get(f"{self.base_url}/api/user-service/users")
            if response.status_code == 404:
                self.log_test("프록시 라우팅", True, "서비스 없음 (예상된 동작)")
                return True
            else:
                self.log_test("프록시 라우팅", False, f"예상과 다른 상태 코드: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("프록시 라우팅", False, f"오류: {str(e)}")
            return False
    
    async def test_heartbeat(self):
        """하트비트 테스트"""
        # 먼저 서비스 등록
        test_service = {
            "service_name": "heartbeat-test",
            "service_url": "http://heartbeat-test:8000"
        }
        
        try:
            # 서비스 등록
            response = await self.client.post(
                f"{self.base_url}/discovery/register",
                json=test_service
            )
            
            if response.status_code == 200:
                data = response.json()
                service_id = data.get("service_id")
                
                # 하트비트 업데이트
                response = await self.client.post(f"{self.base_url}/discovery/heartbeat/{service_id}")
                if response.status_code == 200:
                    self.log_test("하트비트 업데이트", True)
                    
                    # 서비스 정리
                    await self.client.delete(f"{self.base_url}/discovery/unregister/{service_id}")
                    return True
                else:
                    self.log_test("하트비트 업데이트", False, f"상태 코드: {response.status_code}")
                    return False
            else:
                self.log_test("하트비트 테스트", False, "서비스 등록 실패")
                return False
        except Exception as e:
            self.log_test("하트비트 테스트", False, f"오류: {str(e)}")
            return False
    
    async def run_all_tests(self):
        """모든 테스트 실행"""
        logger.info("🚀 MSA Gateway 테스트를 시작합니다...")
        logger.info(f"테스트 대상: {self.base_url}")
        logger.info("=" * 50)
        
        tests = [
            ("루트 엔드포인트", self.test_root_endpoint),
            ("헬스 체크", self.test_health_check),
            ("서비스 디스커버리", self.test_discovery_endpoints),
            ("서비스 등록/해제", self.test_service_registration),
            ("메트릭 조회", self.test_metrics_endpoint),
            ("프록시 라우팅", self.test_proxy_routing),
            ("하트비트", self.test_heartbeat),
        ]
        
        results = []
        for test_name, test_func in tests:
            logger.info(f"\n📋 {test_name} 테스트 중...")
            try:
                result = await test_func()
                results.append(result)
            except Exception as e:
                logger.error(f"테스트 실행 중 오류: {e}")
                results.append(False)
        
        # 결과 요약
        logger.info("\n" + "=" * 50)
        logger.info("📊 테스트 결과 요약")
        logger.info("=" * 50)
        
        passed = sum(1 for result in results if result)
        total = len(results)
        
        logger.info(f"총 테스트: {total}")
        logger.info(f"성공: {passed}")
        logger.info(f"실패: {total - passed}")
        logger.info(f"성공률: {(passed/total)*100:.1f}%")
        
        if passed == total:
            logger.info("🎉 모든 테스트가 성공했습니다!")
        else:
            logger.info("⚠️  일부 테스트가 실패했습니다.")
        
        return passed == total

async def main():
    """메인 함수"""
    import sys
    
    # 명령행 인수 처리
    base_url = "http://localhost:8000"
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    
    async with GatewayTester(base_url) as tester:
        success = await tester.run_all_tests()
        return 0 if success else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code) 