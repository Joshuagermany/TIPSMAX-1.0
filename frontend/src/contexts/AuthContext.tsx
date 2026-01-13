import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

interface User {
  id: string | number;
  nickname: string;
  email?: string;
  profile_image?: string;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  login: (user: User, accessToken: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    // localStorage에서 사용자 정보 로드
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      try {
        setUser(JSON.parse(storedUser));
      } catch (e) {
        console.error('사용자 정보 파싱 오류:', e);
        localStorage.removeItem('user');
        localStorage.removeItem('access_token');
      }
    }
  }, []);

  const login = (userData: User, accessToken: string) => {
    console.log('AuthContext login 호출:', userData);
    setUser(userData);
    localStorage.setItem('user', JSON.stringify(userData));
    localStorage.setItem('access_token', accessToken);
    console.log('AuthContext login 완료, user 상태 업데이트됨');
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('user');
    localStorage.removeItem('access_token');
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user,
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
