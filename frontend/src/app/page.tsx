'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function HomePage() {
  const router = useRouter();
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    // 로그인 상태 확인
    const loggedIn = localStorage.getItem('loggedIn');
    if (loggedIn === 'true') {
      setIsLoggedIn(true);
    }
  }, []);

  const handleGetStarted = () => {
    if (isLoggedIn) {
      router.push('/about');
    } else {
      router.push('/login');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('loggedIn');
    localStorage.removeItem('rememberUser');
    setIsLoggedIn(false);
  };

  return (
    <div className="home-container">
      <div className="home-background">
        {/* Navigation Header */}
        <nav className="navigation">
          <div className="nav-left">
            <div className="logo">
              <div className="logo-icon">🏢</div>
              <span className="logo-text">ERIpotter</span>
            </div>
          </div>
          <div className="nav-right">
            {isLoggedIn ? (
              <>
                <button 
                  onClick={() => router.push('/about')}
                  className="nav-link"
                >
                  대시보드
                </button>
                <button 
                  onClick={handleLogout}
                  className="nav-button secondary"
                >
                  로그아웃
                </button>
              </>
            ) : (
              <>
                <button 
                  onClick={() => router.push('/login')}
                  className="nav-link"
                >
                  로그인
                </button>
                <button 
                  onClick={() => router.push('/register')}
                  className="nav-button primary"
                >
                  회사등록
                </button>
              </>
            )}
          </div>
        </nav>

        {/* Hero Section */}
        <div className="hero-section">
          <div className="hero-content">
            <div className="hero-badge">
              <span>🚀 새로운 원청사 관리 시스템</span>
            </div>
            <h1 className="hero-title">
              효율적인 원청사 관리의
              <br />
              <span className="gradient-text">새로운 기준</span>
            </h1>
            <p className="hero-description">
              ERIpotter는 원청사와 협력업체 간의 효율적인 소통과 관리를 위한 
              통합 플랫폼입니다. 실시간 모니터링부터 리포트 관리까지, 
              모든 것을 한 곳에서 관리하세요.
            </p>
            <div className="hero-actions">
              <button 
                onClick={handleGetStarted}
                className="cta-button primary"
              >
                {isLoggedIn ? '대시보드로 이동' : '시작하기'}
              </button>
              <button 
                onClick={() => router.push('/register')}
                className="cta-button secondary"
              >
                회사 등록하기
              </button>
            </div>
          </div>
          <div className="hero-visual">
            <div className="visual-card">
              <div className="card-header">
                <div className="card-dots">
                  <span className="dot red"></span>
                  <span className="dot yellow"></span>
                  <span className="dot green"></span>
                </div>
                <span className="card-title">ERIpotter Dashboard</span>
              </div>
              <div className="card-content">
                <div className="stat-row">
                  <div className="stat-item">
                    <div className="stat-icon">📊</div>
                    <div className="stat-info">
                      <div className="stat-number">247</div>
                      <div className="stat-label">활성 사용자</div>
                    </div>
                  </div>
                  <div className="stat-item">
                    <div className="stat-icon">🏢</div>
                    <div className="stat-info">
                      <div className="stat-number">89</div>
                      <div className="stat-label">등록된 회사</div>
                    </div>
                  </div>
                </div>
                <div className="chart-placeholder">
                  <div className="chart-bar" style={{height: '60%'}}></div>
                  <div className="chart-bar" style={{height: '80%'}}></div>
                  <div className="chart-bar" style={{height: '45%'}}></div>
                  <div className="chart-bar" style={{height: '90%'}}></div>
                  <div className="chart-bar" style={{height: '70%'}}></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Features Section */}
        <div className="features-section">
          <div className="features-container">
            <div className="section-header">
              <h2 className="section-title">주요 기능</h2>
              <p className="section-description">
                원청사 관리에 필요한 모든 기능을 제공합니다
              </p>
            </div>
            <div className="features-grid">
              <div className="feature-card">
                <div className="feature-icon">📊</div>
                <h3>실시간 대시보드</h3>
                <p>모든 데이터를 한눈에 파악할 수 있는 직관적인 대시보드</p>
              </div>
              <div className="feature-card">
                <div className="feature-icon">👥</div>
                <h3>사용자 관리</h3>
                <p>협력업체 및 내부 직원의 체계적인 권한 관리</p>
              </div>
              <div className="feature-card">
                <div className="feature-icon">📈</div>
                <h3>상세 리포트</h3>
                <p>데이터 기반의 정확한 분석과 보고서 생성</p>
              </div>
              <div className="feature-card">
                <div className="feature-icon">🔒</div>
                <h3>보안 관리</h3>
                <p>기업급 보안 시스템으로 안전한 데이터 보호</p>
              </div>
            </div>
          </div>
        </div>

        {/* CTA Section */}
        <div className="cta-section">
          <div className="cta-container">
            <h2 className="cta-title">지금 바로 시작하세요</h2>
            <p className="cta-description">
              ERIpotter와 함께 더 효율적인 원청사 관리를 경험해보세요
            </p>
            <div className="cta-buttons">
              <button 
                onClick={handleGetStarted}
                className="cta-button primary large"
              >
                무료로 시작하기
              </button>
              <button 
                onClick={() => router.push('/register')}
                className="cta-button secondary large"
              >
                회사 등록하기
              </button>
            </div>
          </div>
        </div>

        {/* Footer */}
        <footer className="footer">
          <div className="footer-content">
            <div className="footer-left">
              <div className="footer-logo">
                <div className="logo-icon">🏢</div>
                <span className="logo-text">ERIpotter</span>
              </div>
              <p className="footer-description">
                효율적인 원청사 관리의 새로운 기준
              </p>
            </div>
            <div className="footer-right">
              <div className="footer-links">
                <a href="#" className="footer-link">개인정보처리방침</a>
                <a href="#" className="footer-link">이용약관</a>
                <a href="#" className="footer-link">고객지원</a>
              </div>
              <p className="footer-copyright">
                © 2025 ERIpotter. 모든 권리 보유.
              </p>
            </div>
          </div>
        </footer>
      </div>

      <style jsx>{`
        .home-container {
          min-height: 100vh;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
        }

        .home-background {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          min-height: 100vh;
          position: relative;
        }

        .home-background::before {
          content: '';
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: url('data:image/svg+xml,<svg width="60" height="60" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg"><g fill="none" fill-rule="evenodd"><g fill="%23ffffff" fill-opacity="0.1"><circle cx="30" cy="30" r="2"/></g></svg>');
          opacity: 0.3;
        }

        /* Navigation */
        .navigation {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 20px 40px;
          position: relative;
          z-index: 10;
        }

        .nav-left, .nav-right {
          display: flex;
          align-items: center;
          gap: 16px;
        }

        .logo {
          display: flex;
          align-items: center;
          gap: 12px;
        }

        .logo-icon {
          font-size: 24px;
          background: white;
          width: 40px;
          height: 40px;
          border-radius: 8px;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .logo-text {
          font-size: 24px;
          font-weight: 700;
          color: white;
        }

        .nav-link {
          color: white;
          text-decoration: none;
          font-weight: 500;
          background: none;
          border: none;
          cursor: pointer;
          padding: 8px 16px;
          border-radius: 6px;
          transition: background-color 0.2s ease;
        }

        .nav-link:hover {
          background-color: rgba(255, 255, 255, 0.1);
        }

        .nav-button {
          padding: 10px 20px;
          border-radius: 8px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.2s ease;
          border: none;
        }

        .nav-button.primary {
          background: white;
          color: #667eea;
        }

        .nav-button.primary:hover {
          transform: translateY(-1px);
          box-shadow: 0 4px 12px rgba(255, 255, 255, 0.3);
        }

        .nav-button.secondary {
          background: transparent;
          color: white;
          border: 2px solid white;
        }

        .nav-button.secondary:hover {
          background: white;
          color: #667eea;
        }

        /* Hero Section */
        .hero-section {
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 80px 40px;
          position: relative;
          z-index: 5;
          max-width: 1200px;
          margin: 0 auto;
          gap: 60px;
        }

        .hero-content {
          flex: 1;
          max-width: 600px;
        }

        .hero-badge {
          display: inline-block;
          background: rgba(255, 255, 255, 0.2);
          color: white;
          padding: 8px 16px;
          border-radius: 20px;
          font-size: 14px;
          font-weight: 500;
          margin-bottom: 24px;
          backdrop-filter: blur(10px);
        }

        .hero-title {
          font-size: 48px;
          font-weight: 700;
          color: white;
          margin: 0 0 24px 0;
          line-height: 1.2;
        }

        .gradient-text {
          background: linear-gradient(135deg, #ffd89b 0%, #19547b 100%);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }

        .hero-description {
          font-size: 18px;
          color: rgba(255, 255, 255, 0.9);
          line-height: 1.6;
          margin: 0 0 32px 0;
        }

        .hero-actions {
          display: flex;
          gap: 16px;
          flex-wrap: wrap;
        }

        .cta-button {
          padding: 16px 32px;
          border-radius: 12px;
          font-size: 16px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.2s ease;
          border: none;
        }

        .cta-button.primary {
          background: white;
          color: #667eea;
          box-shadow: 0 4px 14px rgba(255, 255, 255, 0.3);
        }

        .cta-button.primary:hover {
          transform: translateY(-2px);
          box-shadow: 0 6px 20px rgba(255, 255, 255, 0.4);
        }

        .cta-button.secondary {
          background: transparent;
          color: white;
          border: 2px solid white;
        }

        .cta-button.secondary:hover {
          background: white;
          color: #667eea;
        }

        .cta-button.large {
          padding: 20px 40px;
          font-size: 18px;
        }

        /* Hero Visual */
        .hero-visual {
          flex: 1;
          display: flex;
          justify-content: center;
        }

        .visual-card {
          background: white;
          border-radius: 16px;
          padding: 24px;
          box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
          width: 100%;
          max-width: 400px;
        }

        .card-header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          margin-bottom: 20px;
          padding-bottom: 16px;
          border-bottom: 1px solid #e2e8f0;
        }

        .card-dots {
          display: flex;
          gap: 6px;
        }

        .dot {
          width: 12px;
          height: 12px;
          border-radius: 50%;
        }

        .dot.red { background: #ff5f56; }
        .dot.yellow { background: #ffbd2e; }
        .dot.green { background: #27ca3f; }

        .card-title {
          font-size: 14px;
          font-weight: 600;
          color: #4a5568;
        }

        .stat-row {
          display: flex;
          gap: 16px;
          margin-bottom: 24px;
        }

        .stat-item {
          flex: 1;
          display: flex;
          align-items: center;
          gap: 12px;
          padding: 16px;
          background: #f7fafc;
          border-radius: 8px;
        }

        .stat-icon {
          font-size: 24px;
        }

        .stat-number {
          font-size: 20px;
          font-weight: 700;
          color: #2d3748;
        }

        .stat-label {
          font-size: 12px;
          color: #718096;
        }

        .chart-placeholder {
          display: flex;
          align-items: end;
          gap: 8px;
          height: 80px;
          padding: 16px;
          background: #f7fafc;
          border-radius: 8px;
        }

        .chart-bar {
          flex: 1;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          border-radius: 2px;
          min-height: 20px;
        }

        /* Features Section */
        .features-section {
          background: white;
          padding: 80px 40px;
          position: relative;
          z-index: 5;
        }

        .features-container {
          max-width: 1200px;
          margin: 0 auto;
        }

        .section-header {
          text-align: center;
          margin-bottom: 60px;
        }

        .section-title {
          font-size: 36px;
          font-weight: 700;
          color: #2d3748;
          margin: 0 0 16px 0;
        }

        .section-description {
          font-size: 18px;
          color: #718096;
          margin: 0;
        }

        .features-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
          gap: 32px;
        }

        .feature-card {
          text-align: center;
          padding: 32px 24px;
          background: #f7fafc;
          border-radius: 16px;
          transition: all 0.3s ease;
        }

        .feature-card:hover {
          transform: translateY(-4px);
          box-shadow: 0 12px 24px rgba(102, 126, 234, 0.15);
        }

        .feature-icon {
          font-size: 48px;
          margin-bottom: 20px;
        }

        .feature-card h3 {
          font-size: 20px;
          font-weight: 600;
          color: #2d3748;
          margin: 0 0 12px 0;
        }

        .feature-card p {
          font-size: 16px;
          color: #718096;
          margin: 0;
          line-height: 1.5;
        }

        /* CTA Section */
        .cta-section {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          padding: 80px 40px;
          position: relative;
          z-index: 5;
        }

        .cta-container {
          max-width: 800px;
          margin: 0 auto;
          text-align: center;
        }

        .cta-title {
          font-size: 36px;
          font-weight: 700;
          color: white;
          margin: 0 0 16px 0;
        }

        .cta-description {
          font-size: 18px;
          color: rgba(255, 255, 255, 0.9);
          margin: 0 0 32px 0;
        }

        .cta-buttons {
          display: flex;
          gap: 16px;
          justify-content: center;
          flex-wrap: wrap;
        }

        /* Footer */
        .footer {
          background: #2d3748;
          padding: 40px;
          position: relative;
          z-index: 5;
        }

        .footer-content {
          max-width: 1200px;
          margin: 0 auto;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }

        .footer-left {
          display: flex;
          flex-direction: column;
          gap: 8px;
        }

        .footer-logo {
          display: flex;
          align-items: center;
          gap: 12px;
        }

        .footer-logo .logo-icon {
          background: #667eea;
          color: white;
        }

        .footer-logo .logo-text {
          color: white;
        }

        .footer-description {
          color: #a0aec0;
          margin: 0;
          font-size: 14px;
        }

        .footer-right {
          display: flex;
          flex-direction: column;
          align-items: flex-end;
          gap: 8px;
        }

        .footer-links {
          display: flex;
          gap: 24px;
        }

        .footer-link {
          color: #a0aec0;
          text-decoration: none;
          font-size: 14px;
          transition: color 0.2s ease;
        }

        .footer-link:hover {
          color: white;
        }

        .footer-copyright {
          color: #718096;
          margin: 0;
          font-size: 12px;
        }

        /* Responsive */
        @media (max-width: 768px) {
          .navigation {
            padding: 16px 20px;
          }

          .nav-right {
            flex-direction: column;
            gap: 8px;
          }

          .hero-section {
            flex-direction: column;
            padding: 60px 20px;
            text-align: center;
            gap: 40px;
          }

          .hero-title {
            font-size: 36px;
          }

          .features-section {
            padding: 60px 20px;
          }

          .features-grid {
            grid-template-columns: 1fr;
          }

          .cta-section {
            padding: 60px 20px;
          }

          .cta-buttons {
            flex-direction: column;
            align-items: center;
          }

          .footer {
            padding: 32px 20px;
          }

          .footer-content {
            flex-direction: column;
            gap: 24px;
            text-align: center;
          }

          .footer-right {
            align-items: center;
          }

          .footer-links {
            flex-direction: column;
            gap: 12px;
          }
        }
      `}</style>
    </div>
  );
}
