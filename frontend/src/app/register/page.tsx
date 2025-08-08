'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

// 맨 위쪽 import 아래에 타입 선언
type Company = {
  company_id: string;
  company_name: string | null;
  industry: string;
  company_category: string;
  admin_username: string;
  registeredAt: string;
};

type User = {
  username: string;
  password: string;
  email: string;
  company_id: string;
  role: 'admin' | 'user';
  registeredAt: string;
};

export default function RegisterPage() {
  const router = useRouter();
  
  // Form state management
  const [registerData, setRegisterData] = useState({
    company_id: '',
    company_name: '',
    industry: '',
    company_category: '',
    admin_username: '',
    admin_password: '',
    confirm_password: '',
    admin_email: ''
  });
  
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [errors, setErrors] = useState({
    company_id: '',
    company_name: '',
    industry: '',
    company_category: '',
    admin_username: '',
    admin_password: '',
    confirm_password: '',
    admin_email: '',
    general: ''
  });

  const validateForm = () => {
    const newErrors = {
      company_id: '',
      company_name: '',
      industry: '',
      company_category: '',
      admin_username: '',
      admin_password: '',
      confirm_password: '',
      admin_email: '',
      general: ''
    };
    
    // 회사 ID 검증
    if (!registerData.company_id.trim()) {
      newErrors.company_id = '회사 ID를 입력해주세요.';
    } else if (registerData.company_id.length < 3) {
      newErrors.company_id = '회사 ID는 최소 3자 이상이어야 합니다.';
    } else if (!/^[a-zA-Z0-9_-]+$/.test(registerData.company_id)) {
      newErrors.company_id = '회사 ID는 영문, 숫자, 하이픈, 언더스코어만 사용 가능합니다.';
    }
    
    // 회사명 검증 (선택사항)
    if (registerData.company_name.trim() && registerData.company_name.length < 2) {
      newErrors.company_name = '회사명은 최소 2자 이상이어야 합니다.';
    }
    
    // 산업분야 검증
    if (!registerData.industry.trim()) {
      newErrors.industry = '산업분야를 입력해주세요.';
    }
    
    // 회사 카테고리 검증
    if (!registerData.company_category.trim()) {
      newErrors.company_category = '회사 카테고리를 선택해주세요.';
    }

    // 관리자 사용자명 검증
    if (!registerData.admin_username.trim()) {
      newErrors.admin_username = '관리자 사용자명을 입력해주세요.';
    } else if (registerData.admin_username.length < 4) {
      newErrors.admin_username = '사용자명은 최소 4자 이상이어야 합니다.';
    } else if (!/^[a-zA-Z0-9_]+$/.test(registerData.admin_username)) {
      newErrors.admin_username = '사용자명은 영문, 숫자, 언더스코어만 사용 가능합니다.';
    }

    // 관리자 이메일 검증
    if (!registerData.admin_email.trim()) {
      newErrors.admin_email = '관리자 이메일을 입력해주세요.';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(registerData.admin_email)) {
      newErrors.admin_email = '올바른 이메일 형식을 입력해주세요.';
    }

    // 관리자 비밀번호 검증
    if (!registerData.admin_password.trim()) {
      newErrors.admin_password = '관리자 비밀번호를 입력해주세요.';
    } else if (registerData.admin_password.length < 6) {
      newErrors.admin_password = '비밀번호는 최소 6자 이상이어야 합니다.';
    } else if (!/(?=.*[a-zA-Z])(?=.*\d)/.test(registerData.admin_password)) {
      newErrors.admin_password = '비밀번호는 영문과 숫자를 포함해야 합니다.';
    }

    // 비밀번호 확인 검증
    if (!registerData.confirm_password.trim()) {
      newErrors.confirm_password = '비밀번호 확인을 입력해주세요.';
    } else if (registerData.admin_password !== registerData.confirm_password) {
      newErrors.confirm_password = '비밀번호가 일치하지 않습니다.';
    }
    
    setErrors(newErrors);
    return !Object.values(newErrors).some(error => error !== '');
  };

  // Form input handler
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setRegisterData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) return;
    
    setIsLoading(true);
    setErrors({
      company_id: '',
      company_name: '',
      industry: '',
      company_category: '',
      admin_username: '',
      admin_password: '',
      confirm_password: '',
      admin_email: '',
      general: ''
    });

    try {
      // 백엔드로 전송할 데이터 준비
      const requestData = {
        company: {
          company_id: registerData.company_id,
          company_name: registerData.company_name || null,
          industry: registerData.industry,
          company_category: registerData.company_category
        },
        admin: {
          username: registerData.admin_username,
          email: registerData.admin_email,
          password: registerData.admin_password
        },
        timestamp: new Date().toISOString()
      };

      // 실제 백엔드 API 호출
      const response = await fetch('/api/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData)
      });

      const result = await response.json();
      console.log('백엔드 응답:', result);

      if (!response.ok) {
        throw new Error(result.message || '회사 등록에 실패했습니다.');
      }

      // 로컬 저장소에도 저장 (기존 로직 유지)
      const existingCompanies = localStorage.getItem('companies');
      const companies: Company[] = existingCompanies ? (JSON.parse(existingCompanies) as Company[]) : [];
      
      // 🔧 any 제거
      if (companies.find((company: Company) => company.company_id === registerData.company_id)) {
        setErrors({ 
          company_id: '', 
          company_name: '', 
          industry: '', 
          company_category: '', 
          admin_username: '',
          admin_password: '',
          confirm_password: '',
          admin_email: '',
          general: '이미 존재하는 회사 ID입니다.' 
        });
        setIsLoading(false);
        return;
      }

      // 기존 사용자 확인
      const existingUser = localStorage.getItem('user');
      if (existingUser) {
        const { username } = JSON.parse(existingUser) as User;
        if (username === registerData.admin_username) {
          setErrors({ 
            company_id: '', 
            company_name: '', 
            industry: '', 
            company_category: '', 
            admin_username: '',
            admin_password: '',
            confirm_password: '',
            admin_email: '',
            general: '이미 존재하는 사용자명입니다.' 
          });
          setIsLoading(false);
          return;
        }
      }

      // 회사 등록 데이터 저장
      const companyData = {
        company_id: registerData.company_id,
        company_name: registerData.company_name || null,
        industry: registerData.industry,
        company_category: registerData.company_category,
        admin_username: registerData.admin_username,
        registeredAt: new Date().toISOString()
      };
      
      companies.push(companyData);
      localStorage.setItem('companies', JSON.stringify(companies));

      // 관리자 사용자 계정 저장
      const userData = {
        username: registerData.admin_username,
        password: registerData.admin_password,
        email: registerData.admin_email,
        company_id: registerData.company_id,
        role: 'admin',
        registeredAt: new Date().toISOString()
      };
      
      localStorage.setItem('user', JSON.stringify(userData));
      
      // 성공 메시지 표시 후 로그인 페이지로 이동
      alert('🎉 회사 등록이 완료되었습니다!\n관리자 계정이 생성되었습니다.\n백엔드에 데이터가 전송되었습니다.\n로그인 페이지로 이동합니다.');
      router.push('/login');
      
    } catch (error: unknown) {  // 🔧 any → unknown
      console.error('회사 등록 오류:', error);
      const message = error instanceof Error ? error.message : '회사 등록 중 오류가 발생했습니다. 백엔드 연결을 확인해주세요.';
      setErrors({
        company_id: '',
        company_name: '',
        industry: '',
        company_category: '',
        admin_username: '',
        admin_password: '',
        confirm_password: '',
        admin_email: '',
        general: message
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="register-container">
      <div className="register-background">
        <div className="register-card">
          <div className="register-header">
            <div className="company-logo">
              <div className="logo-icon">🏢</div>
              <h1 className="company-name">ERIpotter</h1>
            </div>
            <p className="register-subtitle">회사 등록</p>
          </div>

          <form onSubmit={handleSubmit} className="register-form">
            {errors.general && (
              <div className="error-banner">
                <span className="error-icon">⚠️</span>
                {errors.general}
              </div>
            )}

            {/* 회사 ID */}
            <div className="form-group">
              <label htmlFor="company_id" className="form-label">회사 ID <span className="required">*</span></label>
              <div className="input-container">
                <span className="input-icon">🏢</span>
                <input
                  id="company_id"
                  name="company_id"
                  type="text"
                  placeholder="회사 고유 ID를 입력하세요"
                  value={registerData.company_id}
                  onChange={handleInputChange}
                  className={`form-input ${errors.company_id ? 'error' : ''}`}
                  disabled={isLoading}
                />
              </div>
              {errors.company_id && <span className="error-text">{errors.company_id}</span>}
            </div>

            {/* 회사명 */}
            <div className="form-group">
              <label htmlFor="company_name" className="form-label">회사명</label>
              <div className="input-container">
                <span className="input-icon">🏛️</span>
                <input
                  id="company_name"
                  name="company_name"
                  type="text"
                  placeholder="회사명을 입력하세요 (선택사항)"
                  value={registerData.company_name}
                  onChange={handleInputChange}
                  className={`form-input ${errors.company_name ? 'error' : ''}`}
                  disabled={isLoading}
                />
              </div>
              {errors.company_name && <span className="error-text">{errors.company_name}</span>}
            </div>

            {/* 산업분야 */}
            <div className="form-group">
              <label htmlFor="industry" className="form-label">산업분야 <span className="required">*</span></label>
              <div className="input-container">
                <span className="input-icon">🏭</span>
                <input
                  id="industry"
                  name="industry"
                  type="text"
                  placeholder="예: IT, 제조업, 금융, 서비스업 등"
                  value={registerData.industry}
                  onChange={handleInputChange}
                  className={`form-input ${errors.industry ? 'error' : ''}`}
                  disabled={isLoading}
                />
              </div>
              {errors.industry && <span className="error-text">{errors.industry}</span>}
            </div>

            {/* 회사 카테고리 */}
            <div className="form-group">
              <label htmlFor="company_category" className="form-label">회사 카테고리 <span className="required">*</span></label>
              <div className="input-container">
                <span className="input-icon">📊</span>
                <select
                  id="company_category"
                  name="company_category"
                  value={registerData.company_category}
                  onChange={handleInputChange}
                  className={`form-select ${errors.company_category ? 'error' : ''}`}
                  disabled={isLoading}
                >
                  <option value="">회사 카테고리를 선택하세요</option>
                  <option value="startup">스타트업</option>
                  <option value="sme">중소기업</option>
                  <option value="mid-cap">중견기업</option>
                  <option value="large">대기업</option>
                  <option value="public">공기업</option>
                  <option value="ngo">비영리기관</option>
                  <option value="government">정부기관</option>
                  <option value="other">기타</option>
                </select>
              </div>
              {errors.company_category && <span className="error-text">{errors.company_category}</span>}
            </div>

            {/* 구분선 */}
            <div className="section-divider">
              <span>관리자 계정 정보</span>
            </div>

            {/* 관리자 사용자명 */}
            <div className="form-group">
              <label htmlFor="admin_username" className="form-label">관리자 사용자명 <span className="required">*</span></label>
              <div className="input-container">
                <span className="input-icon">👤</span>
                <input
                  id="admin_username"
                  name="admin_username"
                  type="text"
                  placeholder="관리자 사용자명을 입력하세요"
                  value={registerData.admin_username}
                  onChange={handleInputChange}
                  className={`form-input ${errors.admin_username ? 'error' : ''}`}
                  disabled={isLoading}
                />
              </div>
              {errors.admin_username && <span className="error-text">{errors.admin_username}</span>}
            </div>

            {/* 관리자 이메일 */}
            <div className="form-group">
              <label htmlFor="admin_email" className="form-label">관리자 이메일 <span className="required">*</span></label>
              <div className="input-container">
                <span className="input-icon">📧</span>
                <input
                  id="admin_email"
                  name="admin_email"
                  type="email"
                  placeholder="관리자 이메일을 입력하세요"
                  value={registerData.admin_email}
                  onChange={handleInputChange}
                  className={`form-input ${errors.admin_email ? 'error' : ''}`}
                  disabled={isLoading}
                />
              </div>
              {errors.admin_email && <span className="error-text">{errors.admin_email}</span>}
            </div>

            {/* 관리자 비밀번호 */}
            <div className="form-group">
              <label htmlFor="admin_password" className="form-label">관리자 비밀번호 <span className="required">*</span></label>
              <div className="input-container">
                <span className="input-icon">🔒</span>
                <input
                  id="admin_password"
                  name="admin_password"
                  type={showPassword ? "text" : "password"}
                  placeholder="관리자 비밀번호를 입력하세요"
                  value={registerData.admin_password}
                  onChange={handleInputChange}
                  className={`form-input ${errors.admin_password ? 'error' : ''}`}
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
              {errors.admin_password && <span className="error-text">{errors.admin_password}</span>}
            </div>

            {/* 비밀번호 확인 */}
            <div className="form-group">
              <label htmlFor="confirm_password" className="form-label">비밀번호 확인 <span className="required">*</span></label>
              <div className="input-container">
                <span className="input-icon">🔐</span>
                <input
                  id="confirm_password"
                  name="confirm_password"
                  type={showConfirmPassword ? "text" : "password"}
                  placeholder="비밀번호를 다시 입력하세요"
                  value={registerData.confirm_password}
                  onChange={handleInputChange}
                  className={`form-input ${errors.confirm_password ? 'error' : ''}`}
                  disabled={isLoading}
                />
                <button
                  type="button"
                  className="password-toggle"
                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  disabled={isLoading}
                >
                  {showConfirmPassword ? '🙈' : '👁️'}
                </button>
              </div>
              {errors.confirm_password && <span className="error-text">{errors.confirm_password}</span>}
            </div>

            <button type="submit" className={`register-button ${isLoading ? 'loading' : ''}`} disabled={isLoading}>
              {isLoading ? (
                <>
                  <span className="spinner"></span>
                  회사 등록 중...
                </>
              ) : (
                '회사 등록'
              )}
            </button>

            <div className="divider">
              <span>또는</span>
            </div>

            <div className="login-section">
              <p>이미 등록된 회사가 있으신가요?</p>
              <div className="nav-buttons">
                <button 
                  type="button"
                  onClick={() => router.push('/')}
                  className="nav-link-button"
                  disabled={isLoading}
                >
                  홈으로 이동
                </button>
                <button 
                  type="button"
                  onClick={() => router.push('/login')}
                  className="nav-link-button primary"
                  disabled={isLoading}
                >
                  로그인하기
                </button>
              </div>
            </div>
          </form>

          <div className="register-footer">
            <p>© 2025 ERIpotter. 모든 권리 보유.</p>
            <div className="footer-links">
              <a href="#">개인정보처리방침</a>
              <span>|</span>
              <a href="#">이용약관</a>
            </div>
          </div>
        </div>
      </div>

      <style jsx>{`
        .register-container {
          min-height: 100vh;
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 20px;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
        }

        .register-background {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          min-height: 100vh;
          width: 100%;
          display: flex;
          align-items: center;
          justify-content: center;
          position: relative;
        }

        .register-background::before {
          content: '';
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: url('data:image/svg+xml,<svg width="60" height="60" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg"><g fill="none" fill-rule="evenodd"><g fill="%23ffffff" fill-opacity="0.1"><circle cx="30" cy="30" r="2"/></g></svg>');
          opacity: 0.3;
        }

        .register-card {
          background: white;
          border-radius: 16px;
          box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
          padding: 40px;
          width: 100%;
          max-width: 520px;
          position: relative;
          z-index: 1;
          backdrop-filter: blur(10px);
        }

        .register-header {
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

        .register-subtitle {
          color: #718096;
          font-size: 18px;
          margin: 0;
          font-weight: 600;
        }

        .register-form {
          display: flex;
          flex-direction: column;
          gap: 20px;
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
          gap: 6px;
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
          padding: 14px 16px 14px 48px;
          border: 2px solid #e2e8f0;
          border-radius: 12px;
          font-size: 15px;
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

        .form-select {
          width: 100%;
          padding: 14px 16px 14px 48px;
          border: 2px solid #e2e8f0;
          border-radius: 12px;
          font-size: 15px;
          transition: all 0.2s ease;
          background: #fafafa;
          box-sizing: border-box;
          appearance: none;
          background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12"><path fill="%23666" d="M6 9l3-3H3z"/></svg>');
          background-repeat: no-repeat;
          background-position: right 16px center;
          background-size: 12px;
        }

        .form-select:focus {
          outline: none;
          border-color: #667eea;
          background: white;
          box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        .form-select.error {
          border-color: #e53e3e;
          background: #fef5f5;
        }

        .form-select:disabled {
          opacity: 0.6;
          cursor: not-allowed;
        }

        .required {
          color: #e53e3e;
          font-weight: 600;
        }

        .section-divider {
          text-align: center;
          position: relative;
          margin: 32px 0 24px 0;
          color: #4a5568;
          font-size: 14px;
          font-weight: 600;
        }

        .section-divider::before {
          content: '';
          position: absolute;
          top: 50%;
          left: 0;
          right: 0;
          height: 1px;
          background: #e2e8f0;
        }

        .section-divider span {
          background: white;
          padding: 0 16px;
          position: relative;
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

        .register-button {
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
          margin-top: 8px;
        }

        .register-button:hover:not(:disabled) {
          transform: translateY(-2px);
          box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
        }

        .register-button:disabled {
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
          margin: 20px 0;
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

        .login-section {
          text-align: center;
        }

        .login-section p {
          color: #718096;
          margin: 0 0 16px 0;
          font-size: 14px;
        }

        .nav-buttons {
          display: flex;
          gap: 12px;
          flex-wrap: wrap;
        }

        .nav-link-button {
          background: white;
          color: #667eea;
          border: 2px solid #667eea;
          padding: 12px 20px;
          border-radius: 12px;
          font-weight: 600;
          font-size: 14px;
          cursor: pointer;
          transition: all 0.2s ease;
          flex: 1;
          min-width: 120px;
        }

        .nav-link-button:hover:not(:disabled) {
          background: #667eea;
          color: white;
          transform: translateY(-1px);
        }

        .nav-link-button.primary {
          background: #667eea;
          color: white;
        }

        .nav-link-button.primary:hover:not(:disabled) {
          background: #5a67d8;
          transform: translateY(-1px);
        }

        .nav-link-button:disabled {
          opacity: 0.6;
          cursor: not-allowed;
        }

        .register-footer {
          margin-top: 32px;
          text-align: center;
          padding-top: 24px;
          border-top: 1px solid #e2e8f0;
        }

        .register-footer p {
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
          .register-card {
            padding: 24px;
            margin: 16px;
          }

          .company-name {
            font-size: 24px;
          }

          .register-form {
            gap: 16px;
          }

          .form-group {
            gap: 4px;
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
