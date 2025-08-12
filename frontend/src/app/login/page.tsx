'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';

export default function LoginPage() {
  const router = useRouter();

  // Form state management
  const [userData, setUserData] = useState({
    user_id: '',
    user_pw: ''
  });
  
  const [rememberMe, setRememberMe] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [errors, setErrors] = useState({ user_id: '', user_pw: '', general: '' });

  const validateForm = () => {
    const newErrors = { user_id: '', user_pw: '', general: '' };
    
    if (!userData.user_id.trim()) {
      newErrors.user_id = '사용자명을 입력해주세요.';
    } else if (userData.user_id.length < 3) {
      newErrors.user_id = '사용자명은 최소 3자 이상이어야 합니다.';
    }
    
    if (!userData.user_pw.trim()) {
      newErrors.user_pw = '비밀번호를 입력해주세요.';
    } else if (userData.user_pw.length < 6) {
      newErrors.user_pw = '비밀번호는 최소 6자 이상이어야 합니다.';
    }
    
    setErrors(newErrors);
    return !newErrors.user_id && !newErrors.user_pw;
  };

  // Form input handler
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setUserData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // JSON 형태로 alert 창 표시
    // alert(JSON.stringify(userData, null, 2));
    
    // axios가 들어갈 자리

    if (!validateForm()) return;
    
    setIsLoading(true);
    setErrors({ user_id: '', user_pw: '', general: '' });

    try {
      // axios를 사용한 로그인 API 호출 (예시)
      console.log('Axios를 사용하여 로그인 요청 준비 중...');
      
      // 실제 auth-service API 호출
              const response = await axios.post('/api/account/login', {
        username: userData.user_id,
        password: userData.user_pw
      });

      // 로그인 성공 처리
      if (response.data && response.data.access_token) {
        // JWT 토큰 저장
        localStorage.setItem('auth_token', response.data.access_token);
        localStorage.setItem('loggedIn', 'true');
        
        // Remember Me 처리
        if (rememberMe) {
          localStorage.setItem('rememberUser', userData.user_id);
        } else {
          localStorage.removeItem('rememberUser');
        }
        
        console.log('로그인 성공:', response.data);
        router.push('/about');
      } else {
        setErrors({ user_id: '', user_pw: '', general: '로그인 응답이 올바르지 않습니다.' });
      }
    } catch (error) {
      console.error('Axios 로그인 요청 중 오류 발생:', error);
      
      // axios 에러 처리
      if (axios.isAxiosError(error)) {
        if (error.response) {
          // 서버에서 응답을 받았지만 에러 상태코드
          setErrors({ user_id: '', user_pw: '', general: `서버 오류: ${error.response.status}` });
        } else if (error.request) {
          // 요청이 만들어졌지만 응답을 받지 못함
          setErrors({ user_id: '', user_pw: '', general: '서버와 연결할 수 없습니다.' });
        } else {
          // 요청을 설정하는 중에 오류 발생
          setErrors({ user_id: '', user_pw: '', general: '요청 처리 중 오류가 발생했습니다.' });
        }
    } else {
        setErrors({ user_id: '', user_pw: '', general: '알 수 없는 오류가 발생했습니다.' });
      }
    } finally {
      setIsLoading(false);
    }
  };

  // 컴포넌트 초기화 및 axios 설정
  useEffect(() => {
    // axios 기본 설정 - 환경변수 사용
    const apiBaseURL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080';
    axios.defaults.baseURL = apiBaseURL;
    axios.defaults.timeout = 10000; // 10초 타임아웃
    axios.defaults.headers.common['Content-Type'] = 'application/json';
    
    // 요청 인터셉터 설정
    axios.interceptors.request.use(
      (config) => {
        console.log('API 요청:', config.method?.toUpperCase(), config.url);
        return config;
      },
      (error) => {
        console.error('요청 에러:', error);
        return Promise.reject(error);
      }
    );

    // 응답 인터셉터 설정
    axios.interceptors.response.use(
      (response) => {
        console.log('API 응답:', response.status, response.data);
        return response;
      },
      (error) => {
        console.error('응답 에러:', error);
        return Promise.reject(error);
      }
    );

    // 로그인된 상태라면 대시보드로 리디렉션
    const loggedIn = localStorage.getItem('loggedIn');
    if (loggedIn === 'true') {
      router.push('/about');
    }
    
    // Remember Me 기능
    const rememberedUser = localStorage.getItem('rememberUser');
    if (rememberedUser) {
      setUserData(prev => ({
        ...prev,
        user_id: rememberedUser
      }));
      setRememberMe(true);
    }
  }, [router]);

  return (
    <div className="login-container">
      <div className="login-background">
        <div className="login-card">
          <div className="login-header">
            <div className="company-logo">
              <div className="logo-icon">🏢</div>
              <h1 className="company-name">ERIpotter</h1>
            </div>
            <p className="login-subtitle">원청사 로그인 포털</p>
          </div>

          <form onSubmit={handleSubmit} className="login-form">
            {errors.general && (
              <div className="error-banner">
                <span className="error-icon">⚠️</span>
                {errors.general}
              </div>
            )}

            <div className="form-group">
              <label htmlFor="user_id" className="form-label">사용자명</label>
              <div className="input-container">
                <span className="input-icon">👤</span>
          <input
                  id="user_id"
                  name="user_id"
            type="text"
                  placeholder="사용자명을 입력하세요"
                  value={userData.user_id}
                  onChange={handleInputChange}
                  className={`form-input ${errors.user_id ? 'error' : ''}`}
                  disabled={isLoading}
          />
        </div>
              {errors.user_id && <span className="error-text">{errors.user_id}</span>}
            </div>

            <div className="form-group">
              <label htmlFor="user_pw" className="form-label">비밀번호</label>
              <div className="input-container">
                <span className="input-icon">🔒</span>
                <input
                  id="user_pw"
                  name="user_pw"
                  type={showPassword ? "text" : "password"}
                  placeholder="비밀번호를 입력하세요"
                  value={userData.user_pw}
                  onChange={handleInputChange}
                  className={`form-input ${errors.user_pw ? 'error' : ''}`}
                  disabled={isLoading}
                />
                <button
                  type="button"
                  className="password-toggle"
                  onClick={() => setShowPassword(!showPassword)}
                  disabled={isLoading}
                >
                  {showPassword ? '🙈' : '👁️'}
                </button>
              </div>
              {errors.user_pw && <span className="error-text">{errors.user_pw}</span>}
            </div>

            <div className="form-options">
              <label className="checkbox-container">
          <input
                  type="checkbox"
                  checked={rememberMe}
                  onChange={(e) => setRememberMe(e.target.checked)}
                  disabled={isLoading}
                />
                <span className="checkmark"></span>
                로그인 상태 유지
              </label>
              <a href="#" className="forgot-password">비밀번호를 잊으셨나요?</a>
            </div>

            <button type="submit" className={`login-button ${isLoading ? 'loading' : ''}`} disabled={isLoading}>
              {isLoading ? (
                <>
                  <span className="spinner"></span>
                  로그인 중...
                </>
              ) : (
                '로그인'
              )}
            </button>

            <div className="divider">
              <span>또는</span>
            </div>

            <div className="register-section">
              <p>아직 등록된 회사가 없으신가요?</p>
              <a href="/register" className="register-link">회사 등록하기</a>
            </div>
          </form>

          <div className="login-footer">
            <p>© 2025 ERIpotter. 모든 권리 보유.</p>
            <div className="footer-links">
              <a href="#">개인정보처리방침</a>
              <span>|</span>
              <a href="#">이용약관</a>
              <span>|</span>
              <a href="#">고객지원</a>
            </div>
          </div>
        </div>
      </div>

      <style jsx>{`
        .login-container {
          min-height: 100vh;
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 20px;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
        }

        .login-background {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          min-height: 100vh;
          width: 100%;
          display: flex;
          align-items: center;
          justify-content: center;
          position: relative;
        }

        .login-background::before {
          content: '';
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: url('data:image/svg+xml,<svg width="60" height="60" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg"><g fill="none" fill-rule="evenodd"><g fill="%23ffffff" fill-opacity="0.1"><circle cx="30" cy="30" r="2"/></g></svg>');
          opacity: 0.3;
        }

        .login-card {
          background: white;
          border-radius: 16px;
          box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
          padding: 40px;
          width: 100%;
          max-width: 480px;
          position: relative;
          z-index: 1;
          backdrop-filter: blur(10px);
        }

        .login-header {
          text-align: center;
          margin-bottom: 32px;
        }

        .company-logo {
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 12px;
          margin-bottom: 16px;
        }

        .logo-icon {
          font-size: 32px;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          width: 56px;
          height: 56px;
          border-radius: 12px;
          display: flex;
          align-items: center;
          justify-content: center;
          box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
        }

        .company-name {
          font-size: 28px;
          font-weight: 700;
          color: #1a202c;
          margin: 0;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }

        .login-subtitle {
          color: #718096;
          font-size: 16px;
          margin: 0;
          font-weight: 500;
        }

        .login-form {
          display: flex;
          flex-direction: column;
          gap: 24px;
        }

        .error-banner {
          background: #fed7d7;
          border: 1px solid #feb2b2;
          color: #c53030;
          padding: 12px 16px;
          border-radius: 8px;
          display: flex;
          align-items: center;
          gap: 8px;
          font-size: 14px;
          font-weight: 500;
        }

        .error-icon {
          font-size: 16px;
        }

        .form-group {
          display: flex;
          flex-direction: column;
          gap: 8px;
        }

        .form-label {
          font-weight: 600;
          color: #2d3748;
          font-size: 14px;
        }

        .input-container {
          position: relative;
          display: flex;
          align-items: center;
        }

        .input-icon {
          position: absolute;
          left: 16px;
          font-size: 16px;
          z-index: 2;
        }

        .form-input {
          width: 100%;
          padding: 16px 16px 16px 48px;
          border: 2px solid #e2e8f0;
          border-radius: 12px;
          font-size: 16px;
          transition: all 0.2s ease;
          background: #fafafa;
          box-sizing: border-box;
        }

        .form-input:focus {
          outline: none;
          border-color: #667eea;
          background: white;
          box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        .form-input.error {
          border-color: #e53e3e;
          background: #fef5f5;
        }

        .form-input:disabled {
          opacity: 0.6;
          cursor: not-allowed;
        }

        .password-toggle {
          position: absolute;
          right: 16px;
          background: none;
          border: none;
          cursor: pointer;
          font-size: 16px;
          padding: 4px;
          border-radius: 4px;
          transition: background-color 0.2s ease;
        }

        .password-toggle:hover {
          background-color: #f0f0f0;
        }

        .password-toggle:disabled {
          opacity: 0.6;
          cursor: not-allowed;
        }

        .error-text {
          color: #e53e3e;
          font-size: 12px;
          font-weight: 500;
        }

        .form-options {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin: 8px 0;
        }

        .checkbox-container {
          display: flex;
          align-items: center;
          cursor: pointer;
          font-size: 14px;
          color: #4a5568;
          position: relative;
        }

        .checkbox-container input {
          position: absolute;
          opacity: 0;
          cursor: pointer;
        }

        .checkmark {
          width: 18px;
          height: 18px;
          border: 2px solid #cbd5e0;
          border-radius: 4px;
          margin-right: 8px;
          position: relative;
          transition: all 0.2s ease;
        }

        .checkbox-container input:checked ~ .checkmark {
          background-color: #667eea;
          border-color: #667eea;
        }

        .checkbox-container input:checked ~ .checkmark::after {
          content: '✓';
          position: absolute;
          color: white;
          font-size: 12px;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
        }

        .forgot-password {
          color: #667eea;
          text-decoration: none;
          font-size: 14px;
          font-weight: 500;
          transition: color 0.2s ease;
        }

        .forgot-password:hover {
          color: #5a67d8;
          text-decoration: underline;
        }

        .login-button {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          border: none;
          padding: 16px 24px;
          border-radius: 12px;
          font-size: 16px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.2s ease;
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 8px;
          box-shadow: 0 4px 14px rgba(102, 126, 234, 0.4);
        }

        .login-button:hover:not(:disabled) {
          transform: translateY(-2px);
          box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
        }

        .login-button:disabled {
          opacity: 0.7;
          cursor: not-allowed;
          transform: none;
        }

        .spinner {
          width: 16px;
          height: 16px;
          border: 2px solid transparent;
          border-top: 2px solid white;
          border-radius: 50%;
          animation: spin 1s linear infinite;
        }

        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }

        .divider {
          text-align: center;
          position: relative;
          margin: 24px 0;
          color: #a0aec0;
          font-size: 14px;
        }

        .divider::before {
          content: '';
          position: absolute;
          top: 50%;
          left: 0;
          right: 0;
          height: 1px;
          background: #e2e8f0;
        }

        .divider span {
          background: white;
          padding: 0 16px;
          position: relative;
        }

        .register-section {
          text-align: center;
        }

        .register-section p {
          color: #718096;
          margin: 0 0 8px 0;
          font-size: 14px;
        }

        .register-link {
          color: #667eea;
          text-decoration: none;
          font-weight: 600;
          font-size: 14px;
          transition: color 0.2s ease;
        }

        .register-link:hover {
          color: #5a67d8;
          text-decoration: underline;
        }

        .login-footer {
          margin-top: 32px;
          text-align: center;
          padding-top: 24px;
          border-top: 1px solid #e2e8f0;
        }

        .login-footer p {
          color: #a0aec0;
          font-size: 12px;
          margin: 0 0 8px 0;
        }

        .footer-links {
          display: flex;
          justify-content: center;
          align-items: center;
          gap: 8px;
          font-size: 12px;
        }

        .footer-links a {
          color: #667eea;
          text-decoration: none;
          transition: color 0.2s ease;
        }

        .footer-links a:hover {
          color: #5a67d8;
          text-decoration: underline;
        }

        .footer-links span {
          color: #cbd5e0;
        }

        @media (max-width: 640px) {
          .login-card {
            padding: 24px;
            margin: 16px;
          }

          .company-name {
            font-size: 24px;
          }

          .form-options {
            flex-direction: column;
            gap: 12px;
            align-items: flex-start;
          }

          .footer-links {
            flex-direction: column;
            gap: 4px;
          }

          .footer-links span {
            display: none;
          }
        }
      `}</style>
    </div>
  );
}
