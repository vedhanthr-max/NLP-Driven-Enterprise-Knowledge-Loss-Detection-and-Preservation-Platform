import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Documents from './pages/Documents';
import KnowledgeCatalog from './pages/KnowledgeCatalog';
import KnowledgeDetail from './pages/KnowledgeDetail';
import RiskStudio from './pages/RiskStudio';
import MLAnalytics from './pages/MLAnalytics';
import SemanticSearch from './pages/SemanticSearch';
import PreservationBoard from './pages/PreservationBoard';
import Employees from './pages/Employees';
import AuditLogs from './pages/AuditLogs';
import { authAPI } from './services/api';

export default function App() {
  const [currentUser, setCurrentUser] = useState(null);
  const [currentView, setCurrentView] = useState('dashboard');
  const [selectedKnowledgeId, setSelectedKnowledgeId] = useState(null);
  const [checkingAuth, setCheckingAuth] = useState(true);

  useEffect(() => {
    // Check local storage for session
    const token = localStorage.getItem('access_token');
    const userStr = localStorage.getItem('user_info');
    if (token && userStr) {
      try {
        setCurrentUser(JSON.parse(userStr));
      } catch (e) {
        localStorage.clear();
      }
    }
    setCheckingAuth(false);
  }, []);

  const handleLoginSuccess = (user) => {
    setCurrentUser(user);
    setCurrentView('dashboard');
  };

  const handleLogout = async () => {
    try {
      await authAPI.logout();
    } catch (e) {
      // Ignore network errors during logout
    }
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user_info');
    setCurrentUser(null);
    setCurrentView('dashboard');
    setSelectedKnowledgeId(null);
  };

  const handleSelectKnowledge = (id) => {
    setSelectedKnowledgeId(id);
    setCurrentView('knowledge_detail');
  };

  if (checkingAuth) {
    return (
      <div style={{
        display: 'flex', justifyContent: 'center', alignItems: 'center',
        height: '100vh', background: 'var(--bg-main)', color: 'var(--text-secondary)'
      }}>
        Initializing Enterprise Session...
      </div>
    );
  }

  // Not logged in -> Show Login Page
  if (!currentUser) {
    return <Login onLoginSuccess={handleLoginSuccess} />;
  }

  // Render view
  const renderView = () => {
    switch (currentView) {
      case 'dashboard':
        return <Dashboard onSelectKnowledge={handleSelectKnowledge} />;
      case 'documents':
        return <Documents />;
      case 'knowledge':
        return <KnowledgeCatalog onSelectKnowledge={handleSelectKnowledge} />;
      case 'knowledge_detail':
        return (
          <KnowledgeDetail
            knowledgeId={selectedKnowledgeId}
            onBack={() => setCurrentView('knowledge')}
          />
        );
      case 'risk_studio':
        return <RiskStudio />;
      case 'ml_analytics':
        return <MLAnalytics />;
      case 'search':
        return <SemanticSearch onSelectKnowledge={handleSelectKnowledge} />;
      case 'preservation':
        return <PreservationBoard />;
      case 'employees':
        return <Employees />;
      case 'audit':
        return <AuditLogs />;
      default:
        return <Dashboard onSelectKnowledge={handleSelectKnowledge} />;
    }
  };

  return (
    <div className="app-shell">
      <Sidebar
        currentView={currentView}
        setCurrentView={setCurrentView}
        currentUser={currentUser}
        onLogout={handleLogout}
      />
      <main className="main-content">
        {renderView()}
      </main>
    </div>
  );
}
