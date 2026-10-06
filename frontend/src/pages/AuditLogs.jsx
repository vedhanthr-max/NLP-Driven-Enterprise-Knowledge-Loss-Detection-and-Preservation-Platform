import React, { useState, useEffect } from 'react';
import { auditAPI } from '../services/api';
import { History, RefreshCw, Shield, Filter, Search, Terminal } from 'lucide-react';

export default function AuditLogs() {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filterAction, setFilterAction] = useState('');
  const [search, setSearch] = useState('');

  useEffect(() => {
    loadLogs();
  }, [filterAction]);

  const loadLogs = async () => {
    setLoading(true);
    try {
      const res = await auditAPI.getLogs(100, filterAction || null);
      setLogs(res.data.items || res.data || []);
    } catch (err) {
      console.error('Failed to load audit logs', err);
    } finally {
      setLoading(false);
    }
  };

  const filtered = logs.filter((log) => {
    const text = `${log.action_type} ${log.user_email || ''} ${log.details || ''} ${log.ip_address || ''}`.toLowerCase();
    return text.includes(search.toLowerCase());
  });

  const getActionBadgeColor = (action) => {
    const act = (action || '').toUpperCase();
    if (act.includes('LOGIN') || act.includes('AUTH')) return '#38bdf8';
    if (act.includes('DOCUMENT') || act.includes('UPLOAD')) return '#10b981';
    if (act.includes('RISK') || act.includes('ALERT')) return '#f59e0b';
    if (act.includes('ML') || act.includes('PREDICT')) return '#a855f7';
    if (act.includes('DELETE') || act.includes('FAIL')) return '#ef4444';
    return '#94a3b8';
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div>
          <h2 style={{ fontSize: '1.75rem', fontWeight: '800', letterSpacing: '-0.02em', display: 'flex', alignItems: 'center', gap: '10px' }}>
            <History style={{ color: 'var(--accent-primary)' }} />
            Enterprise Compliance & Audit Trail
          </h2>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginTop: '4px' }}>
            Immutable logging of data uploads, risk calculations, ML inferences, and user access.
          </p>
        </div>

        <button
          onClick={loadLogs}
          disabled={loading}
          className="btn btn-secondary"
          style={{ display: 'flex', alignItems: 'center', gap: '8px' }}
        >
          <RefreshCw size={15} className={loading ? 'spin' : ''} />
          Refresh Logs
        </button>
      </div>

      {/* Filter Bar */}
      <div className="card" style={{ padding: '16px 20px', display: 'flex', gap: '16px', alignItems: 'center', flexWrap: 'wrap' }}>
        <div style={{ position: 'relative', flex: 1, minWidth: '240px' }}>
          <Search size={16} style={{ position: 'absolute', left: '12px', top: '12px', color: 'var(--text-muted)' }} />
          <input
            type="text"
            className="input-field"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search by action, user, or IP address..."
            style={{ width: '100%', paddingLeft: '38px', height: '40px' }}
          />
        </div>

        <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
          <Filter size={16} style={{ color: 'var(--text-muted)' }} />
          <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: '600' }}>ACTION TYPE:</span>
          <select
            value={filterAction}
            onChange={(e) => setFilterAction(e.target.value)}
            className="input-field"
            style={{ height: '40px' }}
          >
            <option value="">All Actions</option>
            <option value="USER_LOGIN">USER_LOGIN</option>
            <option value="DOCUMENT_UPLOAD">DOCUMENT_UPLOAD</option>
            <option value="KNOWLEDGE_CREATE">KNOWLEDGE_CREATE</option>
            <option value="RISK_CALCULATION">RISK_CALCULATION</option>
            <option value="ML_PREDICTION">ML_PREDICTION</option>
            <option value="PRESERVATION_ACTION_CREATED">PRESERVATION_ACTION_CREATED</option>
          </select>
        </div>
      </div>

      {/* Logs Table */}
      <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.85rem' }}>
            <thead>
              <tr style={{ background: 'rgba(255,255,255,0.03)', borderBottom: '1px solid var(--border-subtle)', textAlign: 'left' }}>
                <th style={{ padding: '14px 16px', color: 'var(--text-muted)', fontWeight: '600' }}>TIMESTAMP</th>
                <th style={{ padding: '14px 16px', color: 'var(--text-muted)', fontWeight: '600' }}>ACTION</th>
                <th style={{ padding: '14px 16px', color: 'var(--text-muted)', fontWeight: '600' }}>USER / ACTOR</th>
                <th style={{ padding: '14px 16px', color: 'var(--text-muted)', fontWeight: '600' }}>IP ADDRESS</th>
                <th style={{ padding: '14px 16px', color: 'var(--text-muted)', fontWeight: '600' }}>DETAILS / ENTITY</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((log) => {
                const color = getActionBadgeColor(log.action_type);
                return (
                  <tr key={log.id} style={{ borderBottom: '1px solid var(--border-subtle)' }}>
                    <td style={{ padding: '12px 16px', whiteSpace: 'nowrap', color: 'var(--text-secondary)' }}>
                      {new Date(log.timestamp || log.created_at).toLocaleString()}
                    </td>

                    <td style={{ padding: '12px 16px', whiteSpace: 'nowrap' }}>
                      <span style={{
                        fontSize: '0.72rem', fontWeight: '700',
                        padding: '2px 8px', borderRadius: '4px',
                        background: `${color}20`, color: color, border: `1px solid ${color}40`
                      }}>
                        {log.action_type}
                      </span>
                    </td>

                    <td style={{ padding: '12px 16px', fontWeight: '600', color: 'var(--text-primary)' }}>
                      {log.user_email || log.user_name || 'System / Batch'}
                    </td>

                    <td style={{ padding: '12px 16px', fontFamily: 'monospace', fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                      {log.ip_address || '127.0.0.1'}
                    </td>

                    <td style={{ padding: '12px 16px', color: 'var(--text-secondary)', maxWidth: '350px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                      {typeof log.details === 'object' ? JSON.stringify(log.details) : (log.details || log.target_entity || '-')}
                    </td>
                  </tr>
                );
              })}

              {filtered.length === 0 && !loading && (
                <tr>
                  <td colSpan="5" style={{ textAlign: 'center', padding: '40px', color: 'var(--text-secondary)' }}>
                    No audit records match your query.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
