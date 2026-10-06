import React, { useState } from 'react';
import { authAPI } from '../services/api';
import { Sparkles, Shield, Lock, Mail, Building, UserPlus, LogIn, AlertCircle } from 'lucide-react';

export default function Login({ onLoginSuccess }) {
  const [isRegister, setIsRegister] = useState(false);
  const [email, setEmail] = useState('manager@techcorp.com');
  const [password, setPassword] = useState('Manager123!');
  const [fullName, setFullName] = useState('');
  const [orgName, setOrgName] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      if (isRegister) {
        await authAPI.register({
          email,
          password,
          full_name: fullName,
          organization_name: orgName,
          organization_size: 100
        });
        // Auto login after register
        const res = await authAPI.login(email, password);
        localStorage.setItem('access_token', res.data.access_token);
        localStorage.setItem('refresh_token', res.data.refresh_token);
        localStorage.setItem('user_info', JSON.stringify(res.data));
        onLoginSuccess(res.data);
      } else {
        const res = await authAPI.login(email, password);
        localStorage.setItem('access_token', res.data.access_token);
        localStorage.setItem('refresh_token', res.data.refresh_token);
        localStorage.setItem('user_info', JSON.stringify(res.data));
        onLoginSuccess(res.data);
      }
    } catch (err) {
      const msg = err.response?.data?.message || err.response?.data?.detail?.message || 'Authentication failed. Please check credentials.';
      const code = err.response?.data?.error_code || err.response?.data?.detail?.error_code || '';
      setError(code ? `[${code}] ${msg}` : msg);
    } finally {
      setLoading(false);
    }
  };

  const fillCredentials = (demoEmail, demoRole) => {
    setEmail(demoEmail);
    setPassword('Manager123!');
    setIsRegister(false);
  };

  return (
    <div style={{
      minHeight: '100vh', display: 'flex', alignItems: 'center',
      justifyContent: 'center', padding: '24px'
    }}>
      <div className="glass-card" style={{ width: '100%', maxWidth: '460px', padding: '36px 32px' }}>
        {/* Header */}
        <div style={{ textAlign: 'center', marginBottom: '28px' }}>
          <div style={{
            width: '48px', height: '48px', borderRadius: '14px',
            background: 'var(--accent-gradient)', display: 'inline-flex',
            alignItems: 'center', justifyContent: 'center', color: '#fff',
            marginBottom: '14px', boxShadow: 'var(--shadow-glow)'
          }}>
            <Sparkles size={26} />
          </div>
          <h2 style={{ fontSize: '1.6rem', fontWeight: '800', letterSpacing: '-0.02em', marginBottom: '6px' }}>
            {isRegister ? 'Create Enterprise Account' : 'Enterprise Knowledge Portal'}
          </h2>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
            {isRegister
              ? 'Register your organization to detect and preserve at-risk knowledge'
              : 'Sign in to monitor knowledge vulnerability, NLP extraction & risk analytics'}
          </p>
        </div>

        {/* Quick-Fill Demo Pills */}
        {!isRegister && (
          <div style={{ marginBottom: '20px' }}>
            <div style={{ fontSize: '0.75rem', fontWeight: '600', color: 'var(--text-muted)', marginBottom: '8px', textTransform: 'uppercase' }}>
              Quick Demo Logins:
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '6px' }}>
              <button
                type="button"
                onClick={() => fillCredentials('admin@techcorp.com', 'Admin')}
                className="btn btn-secondary"
                style={{ fontSize: '0.75rem', padding: '6px 4px', border: email === 'admin@techcorp.com' ? '1px solid var(--accent-primary)' : undefined }}
              >
                Admin
              </button>
              <button
                type="button"
                onClick={() => fillCredentials('manager@techcorp.com', 'Manager')}
                className="btn btn-secondary"
                style={{ fontSize: '0.75rem', padding: '6px 4px', border: email === 'manager@techcorp.com' ? '1px solid var(--accent-primary)' : undefined }}
              >
                Manager
              </button>
              <button
                type="button"
                onClick={() => fillCredentials('rajesh@techcorp.com', 'Rajesh (Sole Expert)')}
                className="btn btn-secondary"
                style={{ fontSize: '0.75rem', padding: '6px 4px', border: email === 'rajesh@techcorp.com' ? '1px solid var(--accent-primary)' : undefined }}
              >
                Rajesh (Expert)
              </button>
            </div>
          </div>
        )}

        {/* Error Alert */}
        {error && (
          <div style={{
            background: 'var(--risk-critical-bg)', border: '1px solid rgba(239, 68, 68, 0.3)',
            borderRadius: 'var(--radius-md)', padding: '12px 14px', color: '#fca5a5',
            fontSize: '0.85rem', marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '8px'
          }}>
            <AlertCircle size={16} />
            <div>{error}</div>
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {isRegister && (
            <>
              <div>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: '600', color: 'var(--text-secondary)', marginBottom: '6px' }}>
                  Full Name
                </label>
                <input
                  type="text"
                  required
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  placeholder="e.g. John Doe"
                  className="input"
                />
              </div>
              <div>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: '600', color: 'var(--text-secondary)', marginBottom: '6px' }}>
                  Organization Name
                </label>
                <input
                  type="text"
                  required
                  value={orgName}
                  onChange={(e) => setOrgName(e.target.value)}
                  placeholder="e.g. Acme Financial"
                  className="input"
                />
              </div>
            </>
          )}

          <div>
            <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: '600', color: 'var(--text-secondary)', marginBottom: '6px' }}>
              Work Email
            </label>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="name@company.com"
              className="input"
            />
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: '600', color: 'var(--text-secondary)', marginBottom: '6px' }}>
              Password
            </label>
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              className="input"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="btn btn-primary"
            style={{ width: '100%', padding: '12px', marginTop: '8px' }}
          >
            {loading ? 'Authenticating...' : isRegister ? (
              <><UserPlus size={18} /> Register Organization</>
            ) : (
              <><LogIn size={18} /> Enter Platform</>
            )}
          </button>
        </form>

        {/* Toggle Mode */}
        <div style={{ textAlign: 'center', marginTop: '20px', paddingTop: '16px', borderTop: '1px solid var(--border-subtle)' }}>
          <button
            type="button"
            onClick={() => { setIsRegister(!isRegister); setError(null); }}
            style={{ background: 'none', border: 'none', color: 'var(--accent-primary)', cursor: 'pointer', fontSize: '0.85rem', fontWeight: '600' }}
          >
            {isRegister ? 'Already have an account? Sign In' : "Don't have an enterprise account? Register"}
          </button>
        </div>
      </div>
    </div>
  );
}
