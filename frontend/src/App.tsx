import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { Layout } from './components/Layout';
import { Home } from './pages/Home';
import { Results } from './pages/Results';
import { Login } from './pages/Login';
import { Dashboard } from './pages/Dashboard';
import { CompanyStatus } from './pages/CompanyStatus';
import { KakaoCallback } from './pages/KakaoCallback';
import { GoogleCallback } from './pages/GoogleCallback';
import './index.css';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Layout>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/company-status" element={<CompanyStatus />} />
            <Route path="/results" element={<Results />} />
            <Route path="/auth/kakao/callback" element={<KakaoCallback />} />
            <Route path="/auth/google/callback" element={<GoogleCallback />} />
          </Routes>
        </Layout>
      </Router>
    </AuthProvider>
  );
}

export default App;
