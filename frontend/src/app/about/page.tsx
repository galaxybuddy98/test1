'use client';

import { useRouter } from 'next/navigation';

export default function AboutPage() {
  const router = useRouter();

  return (
    <div className="about-container">
      <div className="about-background">
        <div className="about-card">
          {/* Header Section */}
          <div className="about-header">
            <div className="logo-section">
              <div className="logo-icon">🏢</div>
              <h1 className="company-title">ERIpotter</h1>
              <p className="company-subtitle">원청사 관리 시스템</p>
            </div>
          </div>

          {/* Content Section */}
          <div className="about-content">
            <div className="welcome-section">
              <h2 className="welcome-title">로그인 성공!</h2>
              <p className="welcome-message">
                ERIpotter 원청사 관리 시스템에 오신 것을 환영합니다.
              </p>
            </div>

            <div className="features-section">
              <h3 className="features-title">주요 기능</h3>
              <div className="features-grid">
                <div className="feature-card">
                  <div className="feature-icon">📊</div>
                  <h4>대시보드</h4>
                  <p>실시간 데이터 모니터링</p>
                </div>
                <div className="feature-card">
                  <div className="feature-icon">👥</div>
                  <h4>사용자 관리</h4>
                  <p>팀원 및 권한 관리</p>
                </div>
                <div className="feature-card">
                  <div className="feature-icon">📈</div>
                  <h4>리포트</h4>
                  <p>상세 분석 및 보고서</p>
                </div>
                <div className="feature-card">
                  <div className="feature-icon">⚙️</div>
                  <h4>설정</h4>
                  <p>시스템 환경 설정</p>
                </div>
              </div>
            </div>

            <div className="stats-section">
              <h3 className="stats-title">현재 상태</h3>
              <div className="stats-grid">
                <div className="stat-item">
                  <div className="stat-number">247</div>
                  <div className="stat-label">활성 사용자</div>
                </div>
                <div className="stat-item">
                  <div className="stat-number">1,834</div>
                  <div className="stat-label">완료된 작업</div>
                </div>
                <div className="stat-item">
                  <div className="stat-number">98.5%</div>
                  <div className="stat-label">시스템 가동률</div>
                </div>
              </div>
            </div>
          </div>

          {/* Navigation Section */}
          <div className="navigation-section">
            <button 
              onClick={() => router.push('/')}
              className="nav-button primary"
            >
              홈으로 이동
            </button>
            <button 
              onClick={() => router.push('/login')}
              className="nav-button secondary"
            >
              로그인 페이지로
            </button>
            <button 
              onClick={() => alert('대시보드로 이동 예정')}
              className="nav-button secondary"
            >
              대시보드 바로가기
            </button>
          </div>

          {/* Footer */}
          <div className="about-footer">
            <p>© 2025 ERIpotter. 모든 권리 보유.</p>
            <div className="footer-info">
              <span>버전 1.0.0</span>
              <span>•</span>
              <span>최종 업데이트: 2025.01.27</span>
            </div>
          </div>
        </div>
      </div>

      <style jsx>{`
        .about-container {
          min-height: 100vh;
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 20px;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
        }

        .about-background {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          min-height: 100vh;
          width: 100%;
          display: flex;
          align-items: center;
          justify-content: center;
          position: relative;
        }

        .about-background::before {
          content: '';
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: url('data:image/svg+xml,<svg width="60" height="60" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg"><g fill="none" fill-rule="evenodd"><g fill="%23ffffff" fill-opacity="0.1"><circle cx="30" cy="30" r="2"/></g></svg>');
          opacity: 0.3;
        }

        .about-card {
          background: white;
          border-radius: 20px;
          box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
          padding: 40px;
          width: 100%;
          max-width: 800px;
          position: relative;
          z-index: 1;
          backdrop-filter: blur(10px);
        }

        .about-header {
          text-align: center;
          margin-bottom: 40px;
        }

        .logo-section {
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 8px;
        }

        .logo-icon {
          font-size: 48px;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          width: 80px;
          height: 80px;
          border-radius: 16px;
          display: flex;
          align-items: center;
          justify-content: center;
          box-shadow: 0 12px 24px rgba(102, 126, 234, 0.3);
          margin-bottom: 16px;
        }

        .company-title {
          font-size: 36px;
          font-weight: 700;
          color: #1a202c;
          margin: 0;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }

        .company-subtitle {
          color: #718096;
          font-size: 18px;
          margin: 8px 0 0 0;
          font-weight: 500;
        }

        .about-content {
          display: flex;
          flex-direction: column;
          gap: 40px;
        }

        .welcome-section {
          text-align: center;
          padding: 32px;
          background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
          border-radius: 16px;
          border: 1px solid #e2e8f0;
        }

        .welcome-title {
          font-size: 32px;
          font-weight: 700;
          color: #2d3748;
          margin: 0 0 16px 0;
        }

        .welcome-message {
          font-size: 18px;
          color: #4a5568;
          margin: 0;
          line-height: 1.6;
        }

        .features-section, .stats-section {
          text-align: center;
        }

        .features-title, .stats-title {
          font-size: 24px;
          font-weight: 600;
          color: #2d3748;
          margin: 0 0 24px 0;
        }

        .features-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
          gap: 20px;
          margin-top: 24px;
        }

        .feature-card {
          background: white;
          border: 2px solid #e2e8f0;
          border-radius: 12px;
          padding: 24px 16px;
          text-align: center;
          transition: all 0.3s ease;
          cursor: pointer;
        }

        .feature-card:hover {
          border-color: #667eea;
          box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
          transform: translateY(-2px);
        }

        .feature-icon {
          font-size: 32px;
          margin-bottom: 12px;
        }

        .feature-card h4 {
          font-size: 16px;
          font-weight: 600;
          color: #2d3748;
          margin: 0 0 8px 0;
        }

        .feature-card p {
          font-size: 14px;
          color: #718096;
          margin: 0;
        }

        .stats-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
          gap: 24px;
          margin-top: 24px;
        }

        .stat-item {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          border-radius: 12px;
          padding: 24px;
          text-align: center;
        }

        .stat-number {
          font-size: 28px;
          font-weight: 700;
          margin-bottom: 8px;
        }

        .stat-label {
          font-size: 14px;
          opacity: 0.9;
        }

        .navigation-section {
          display: flex;
          gap: 12px;
          justify-content: center;
          margin-top: 40px;
          flex-wrap: wrap;
        }

        .nav-button {
          padding: 14px 24px;
          border-radius: 12px;
          font-size: 14px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.2s ease;
          border: none;
          min-width: 160px;
        }

        .nav-button.primary {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          box-shadow: 0 4px 14px rgba(102, 126, 234, 0.4);
        }

        .nav-button.primary:hover {
          transform: translateY(-2px);
          box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
        }

        .nav-button.secondary {
          background: white;
          color: #667eea;
          border: 2px solid #667eea;
        }

        .nav-button.secondary:hover {
          background: #667eea;
          color: white;
          transform: translateY(-2px);
        }

        .about-footer {
          margin-top: 40px;
          text-align: center;
          padding-top: 24px;
          border-top: 1px solid #e2e8f0;
        }

        .about-footer p {
          color: #a0aec0;
          font-size: 14px;
          margin: 0 0 8px 0;
        }

        .footer-info {
          display: flex;
          justify-content: center;
          align-items: center;
          gap: 8px;
          font-size: 12px;
          color: #cbd5e0;
        }

        @media (max-width: 768px) {
          .about-card {
            padding: 24px;
            margin: 16px;
          }

          .company-title {
            font-size: 28px;
          }

          .welcome-title {
            font-size: 24px;
          }

          .features-grid {
            grid-template-columns: 1fr;
          }

          .navigation-section {
            flex-direction: column;
            align-items: center;
          }

          .nav-button {
            width: 100%;
            max-width: 300px;
          }
        }
      `}</style>
    </div>
  );
}
