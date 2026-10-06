import React from 'react';
import {
  LayoutDashboard, FileText, BookOpen, AlertOctagon,
  Cpu, Search, ShieldCheck, Users, History, LogOut, Sparkles
} from 'lucide-react';

export default function Sidebar({ currentView, setCurrentView, currentUser, onLogout }) {
  const navItems = [
    { id: 'dashboard', label: 'Executive Dashboard', icon: <LayoutDashboard size={18} /> },
    { id: 'documents', label: 'Document Hub', icon: <FileText size={18} /> },
    { id: 'knowledge', label: 'Knowledge Catalog', icon: <BookOpen size={18} /> },
    { id: 'risk_studio', label: 'Risk Studio', icon: <AlertOctagon size={18} /> },
    { id: 'ml_analytics', label: 'ML Analytics', icon: <Cpu size={18} /> },
    { id: 'search', label: 'Semantic Search', icon: <Search size={18} /> },
    { id: 'preservation', label: 'Preservation Board', icon: <ShieldCheck size={18} /> },
    { id: 'employees', label: 'Expert Directory', icon: <Users size={18} /> },
    { id: 'audit', label: 'Audit Trail', icon: <History size={18} />, adminOnly: true },
  ];

  return (
    <aside className="sidebar">
      {/* Brand Header */}
      <div style={{ paddingBottom: '24px', borderBottom: '1px solid var(--border-subtle)', marginBottom: '16px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div style={{
            width: '36px', height: '36px', borderRadius: '10px',
            background: 'var(--accent-gradient)', display: 'flex',
            alignItems: 'center', justifyContent: 'center', color: '#fff'
          }}>
            <Sparkles size={20} />
          </div>
          <div>
            <h1 style={{ fontSize: '1.05rem', fontWeight: '700', letterSpacing: '-0.02em' }}>KnowledgeLoss</h1>
            <span style={{ fontSize: '0.7rem', color: 'var(--accent-primary)', fontWeight: '600' }}>AI SAAS PLATFORM</span>
          </div>
        </div>
      </div>

      {/* Navigation Links */}
      <nav style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '2px', overflowY: 'auto' }}>
        {navItems.map((item) => {
          if (item.adminOnly && currentUser?.role === 'employee') return null;
          const isActive = currentView === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setCurrentView(item.id)}
              className={`nav-link ${isActive ? 'active' : ''}`}
              style={{ background: isActive ? undefined : 'transparent', border: 'none', width: '100%', textAlign: 'left' }}
            >
              {item.icon}
              <span>{item.label}</span>
            </button>
          );
        })}
      </nav>

      {/* User Info & Logout Footer */}
      <div style={{ paddingTop: '16px', borderTop: '1px solid var(--border-subtle)', display: 'flex', flexDirection: 'column', gap: '12px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div style={{
            width: '34px', height: '34px', borderRadius: '50%',
            background: '#1e293b', border: '1px solid var(--border-subtle)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontWeight: '700', fontSize: '0.85rem', color: 'var(--accent-primary)'
          }}>
            {currentUser?.full_name ? currentUser.full_name[0].toUpperCase() : 'U'}
          </div>
          <div style={{ overflow: 'hidden' }}>
            <div style={{ fontSize: '0.85rem', fontWeight: '600', textOverflow: 'ellipsis', whiteSpace: 'nowrap', overflow: 'hidden' }}>
              {currentUser?.full_name || 'Enterprise User'}
            </div>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'capitalize' }}>
              {currentUser?.role || 'User'} • {currentUser?.organization_name || 'TechCorp'}
            </div>
          </div>
        </div>

        <button
          onClick={onLogout}
          className="btn btn-secondary"
          style={{ width: '100%', justifyContent: 'center', fontSize: '0.8rem', padding: '6px 12px' }}
        >
          <LogOut size={15} />
          Sign Out
        </button>
      </div>
    </aside>
  );
}
