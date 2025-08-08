import { create } from 'zustand';

interface AppState {
  // Loading states
  isLoading: boolean;
  
  // Error states
  error: string | null;
  
  // User authentication
  isLoggedIn: boolean;
  user: { name: string; email: string } | null;
  
  // Actions
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

export const useStore = create<AppState>((set) => ({
  // Initial states
  isLoading: false,
  error: null,
  isLoggedIn: false,
  user: null,
  
  // Basic actions
  setLoading: (loading: boolean) => set({ isLoading: loading }),
  setError: (error: string | null) => set({ error }),
  
  // Authentication
  login: async (email: string, password: string) => {
    set({ isLoading: true, error: null });
    try {
      // 실제 Gateway API 호출 (lme.eripotter.com/api/login)
      const response = await fetch('/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        throw new Error(`로그인 실패: ${response.status}`);
      }

      const data = await response.json();
      
      set({ 
        isLoggedIn: true, 
        user: { name: '사용자', email },
        isLoading: false 
      });
      
      // JWT 토큰이 있다면 저장
      if (data.token) {
        localStorage.setItem('auth_token', data.token);
      }
      localStorage.setItem('loggedIn', 'true');
      
    } catch (error) {
      set({ 
        error: error instanceof Error ? error.message : '로그인에 실패했습니다', 
        isLoading: false 
      });
    }
  },
  
  logout: () => {
    set({ isLoggedIn: false, user: null });
    localStorage.removeItem('loggedIn');
    localStorage.removeItem('auth_token');
  },
})); 