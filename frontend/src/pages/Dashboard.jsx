import React, { useState, useEffect } from 'react';
import { riskAPI } from '../services/api';
import RiskBadge from '../components/RiskBadge';
import {
  ShieldAlert, AlertTriangle, ShieldCheck, Flame, BookOpen,
  ArrowUpRight, RefreshCw, Layers, CheckCircle2, Clock
} from 'lucide-react';

export default function Dashboard({ onNavigateToKnowledge, onNavigate }) {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchDashboard = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await riskAPI.getDashboard();
      setDashboardData(res.data);
    } catch (err) {
      setError('Unable to load dashboard data. Ensure backend is running.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboard();
  }, []);

  if (loading) {
    return (
      <div style={{ padding: '40px', textAlign: 'center', color: 'var(--text-secondary)' }}>
        <RefreshCw size={28} className="animate-spin" style={{ marginBottom: '12px', animation: 'spin 1s linear infinite' }} />
        <div>Loading Executive Risk Dashboard...</div>
      </div>
    );
  }

  if (error || !dashboardData) {
    return (
      <div className="glass-card" style={{ padding: '32px', textAlign: 'center' }}>
        <AlertTriangle size={36} color="var(--risk-critical)" style={{ marginBottom: '12px' }} />
        <h3>{error || 'No data available'}</h3>
        <button onClick={fetchDashboard} className="btn btn-primary" style={{ marginTop: '16px' }}>
          Retry
        </button>
      </div>
    );
  }

  const { summary, risk_distribution, top_critical_items, preservation_progress } = dashboardData;

  return (
    <div>
      {/* Top Banner / Title */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '28px' }}>
        <div>
          <h2 style={{ fontSize: '1.75rem', fontWeight: '800', letterSpacing: '-0.02em', marginBottom: '4px' }}>
            Enterprise Knowledge Loss Overview
          </h2>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
            Continuous NLP extraction, single-expert dependency detection & automated preservation monitoring
          </p>
        </div>
        <div style={{ display: 'flex', gap: '10px' }}>
          <button onClick={fetchDashboard} className="btn btn-secondary">
            <RefreshCw size={15} /> Refresh Data
          </button>
          <button onClick={() => onNavigate('documents')} className="btn btn-primary">
            + Ingest Document
          </button>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '18px', marginBottom: '28px' }}>
        {/* Total Knowledge */}
        <div className="glass-card" style={{ padding: '22px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <div>
              <div style={{ fontSize: '0.8rem', fontWeight: '600', color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '6px' }}>
                Total Knowledge Items
              </div>
              <div style={{ fontSize: '2rem', fontWeight: '800' }}>
                {summary.total_knowledge_items}
              </div>
            </div>
            <div style={{ padding: '10px', borderRadius: '12px', background: 'rgba(99, 102, 241, 0.12)', color: 'var(--accent-primary)' }}>
              <BookOpen size={22} />
            </div>
          </div>
          <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', marginTop: '10px' }}>
            Extracted from verified runbooks & architecture docs
          </div>
        </div>

        {/* Critical Risk */}
        <div className="glass-card" style={{ padding: '22px', borderLeft: '4px solid var(--risk-critical)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <div>
              <div style={{ fontSize: '0.8rem', fontWeight: '600', color: 'var(--risk-critical)', textTransform: 'uppercase', marginBottom: '6px' }}>
                Critical Vulnerability
              </div>
              <div style={{ fontSize: '2rem', fontWeight: '800', color: 'var(--risk-critical)' }}>
                {summary.critical_risk_count}
              </div>
            </div>
            <div style={{ padding: '10px', borderRadius: '12px', background: 'var(--risk-critical-bg)', color: 'var(--risk-critical)' }}>
              <Flame size={22} />
            </div>
          </div>
          <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', marginTop: '10px' }}>
            Immediate loss risk (single expert + high dependency)
          </div>
        </div>

        {/* High Risk */}
        <div className="glass-card" style={{ padding: '22px', borderLeft: '4px solid var(--risk-high)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <div>
              <div style={{ fontSize: '0.8rem', fontWeight: '600', color: 'var(--risk-high)', textTransform: 'uppercase', marginBottom: '6px' }}>
                High Priority Risk
              </div>
              <div style={{ fontSize: '2rem', fontWeight: '800', color: 'var(--risk-high)' }}>
                {summary.high_risk_count}
              </div>
            </div>
            <div style={{ padding: '10px', borderRadius: '12px', background: 'var(--risk-high-bg)', color: 'var(--risk-high)' }}>
              <AlertTriangle size={22} />
            </div>
          </div>
          <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', marginTop: '10px' }}>
            Mitigation action required within 30 days
          </div>
        </div>

        {/* Avg Risk Score */}
        <div className="glass-card" style={{ padding: '22px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <div>
              <div style={{ fontSize: '0.8rem', fontWeight: '600', color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '6px' }}>
                Avg Risk Index
              </div>
              <div style={{ fontSize: '2rem', fontWeight: '800' }}>
                {summary.average_risk_score}
                <span style={{ fontSize: '1rem', color: 'var(--text-muted)', fontWeight: '500' }}>/100</span>
              </div>
            </div>
            <div style={{ padding: '10px', borderRadius: '12px', background: 'rgba(245, 158, 11, 0.12)', color: 'var(--risk-medium)' }}>
              <ShieldAlert size={22} />
            </div>
          </div>
          <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', marginTop: '10px' }}>
            Organization composite risk rating
          </div>
        </div>
      </div>

      {/* Middle Row: Risk Distribution & Preservation Status */}
      <div style={{ display: 'grid', gridTemplateColumns: '1.3fr 1fr', gap: '20px', marginBottom: '28px' }}>
        {/* Risk Distribution Chart */}
        <div className="glass-card" style={{ padding: '24px' }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: '700', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Layers size={18} color="var(--accent-primary)" />
            Organizational Knowledge Risk Distribution
          </h3>

          {/* Segmented Progress Bar */}
          <div style={{ height: '24px', borderRadius: '12px', display: 'flex', overflow: 'hidden', background: '#1e293b', marginBottom: '20px' }}>
            <div style={{ width: `${risk_distribution.critical}%`, background: 'var(--risk-critical)' }} title={`Critical: ${risk_distribution.critical}%`} />
            <div style={{ width: `${risk_distribution.high}%`, background: 'var(--risk-high)' }} title={`High: ${risk_distribution.high}%`} />
            <div style={{ width: `${risk_distribution.medium}%`, background: 'var(--risk-medium)' }} title={`Medium: ${risk_distribution.medium}%`} />
            <div style={{ width: `${risk_distribution.low}%`, background: 'var(--risk-low)' }} title={`Low: ${risk_distribution.low}%`} />
          </div>

          {/* Legend Grid */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '12px' }}>
            <div style={{ padding: '12px', borderRadius: 'var(--radius-md)', background: 'var(--risk-critical-bg)', border: '1px solid rgba(239, 68, 68, 0.2)' }}>
              <div style={{ fontSize: '0.75rem', fontWeight: '700', color: 'var(--risk-critical)' }}>CRITICAL (81-100)</div>
              <div style={{ fontSize: '1.25rem', fontWeight: '800' }}>{risk_distribution.critical}%</div>
            </div>
            <div style={{ padding: '12px', borderRadius: 'var(--radius-md)', background: 'var(--risk-high-bg)', border: '1px solid rgba(249, 115, 22, 0.2)' }}>
              <div style={{ fontSize: '0.75rem', fontWeight: '700', color: 'var(--risk-high)' }}>HIGH (61-80)</div>
              <div style={{ fontSize: '1.25rem', fontWeight: '800' }}>{risk_distribution.high}%</div>
            </div>
            <div style={{ padding: '12px', borderRadius: 'var(--radius-md)', background: 'var(--risk-medium-bg)', border: '1px solid rgba(245, 158, 11, 0.2)' }}>
              <div style={{ fontSize: '0.75rem', fontWeight: '700', color: 'var(--risk-medium)' }}>MEDIUM (31-60)</div>
              <div style={{ fontSize: '1.25rem', fontWeight: '800' }}>{risk_distribution.medium}%</div>
            </div>
            <div style={{ padding: '12px', borderRadius: 'var(--radius-md)', background: 'var(--risk-low-bg)', border: '1px solid rgba(16, 185, 129, 0.2)' }}>
              <div style={{ fontSize: '0.75rem', fontWeight: '700', color: 'var(--risk-low)' }}>LOW (0-30)</div>
              <div style={{ fontSize: '1.25rem', fontWeight: '800' }}>{risk_distribution.low}%</div>
            </div>
          </div>
        </div>

        {/* Preservation Progress Tracker */}
        <div className="glass-card" style={{ padding: '24px' }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: '700', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <ShieldCheck size={18} color="var(--risk-low)" />
            Preservation Action Lifecycle
          </h3>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '10px 14px', background: 'rgba(255, 255, 255, 0.03)', borderRadius: 'var(--radius-md)' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <Clock size={16} color="var(--risk-high)" />
                <span style={{ fontSize: '0.9rem', fontWeight: '500' }}>Recommended Actions</span>
              </div>
              <span className="badge badge-high">{preservation_progress.recommended}</span>
            </div>

            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '10px 14px', background: 'rgba(255, 255, 255, 0.03)', borderRadius: 'var(--radius-md)' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <Layers size={16} color="var(--risk-medium)" />
                <span style={{ fontSize: '0.9rem', fontWeight: '500' }}>Planned for Handover</span>
              </div>
              <span className="badge badge-medium">{preservation_progress.planned}</span>
            </div>

            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '10px 14px', background: 'rgba(255, 255, 255, 0.03)', borderRadius: 'var(--radius-md)' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <RefreshCw size={16} color="var(--accent-primary)" />
                <span style={{ fontSize: '0.9rem', fontWeight: '500' }}>In Progress / Cross-Training</span>
              </div>
              <span className="badge" style={{ background: 'rgba(99, 102, 241, 0.15)', color: 'var(--accent-primary)', border: '1px solid rgba(99, 102, 241, 0.3)' }}>
                {preservation_progress.in_progress}
              </span>
            </div>

            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '10px 14px', background: 'rgba(255, 255, 255, 0.03)', borderRadius: 'var(--radius-md)' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <CheckCircle2 size={16} color="var(--risk-low)" />
                <span style={{ fontSize: '0.9rem', fontWeight: '500' }}>Completed / Preserved</span>
              </div>
              <span className="badge badge-low">{preservation_progress.completed}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Top Critical Knowledge Watchlist */}
      <div className="glass-card" style={{ padding: '24px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '18px' }}>
          <div>
            <h3 style={{ fontSize: '1.15rem', fontWeight: '700' }}>Critical Knowledge Watchlist</h3>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.82rem' }}>
              Highest risk assets based on single expert dependency, documentation gaps, and revenue impact
            </p>
          </div>
          <button onClick={() => onNavigate('knowledge')} className="btn btn-secondary" style={{ fontSize: '0.8rem' }}>
            View Full Repository <ArrowUpRight size={14} />
          </button>
        </div>

        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.88rem' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid var(--border-subtle)', color: 'var(--text-muted)' }}>
                <th style={{ padding: '12px 14px' }}>KNOWLEDGE ITEM</th>
                <th style={{ padding: '12px 14px' }}>CATEGORY</th>
                <th style={{ padding: '12px 14px' }}>EXPERTS</th>
                <th style={{ padding: '12px 14px' }}>PRIMARY FACTOR</th>
                <th style={{ padding: '12px 14px' }}>RISK SCORE</th>
                <th style={{ padding: '12px 14px', textAlign: 'right' }}>ACTION</th>
              </tr>
            </thead>
            <tbody>
              {top_critical_items.map((item) => (
                <tr key={item.knowledge_id} style={{ borderBottom: '1px solid var(--border-subtle)' }}>
                  <td style={{ padding: '14px', fontWeight: '600' }}>
                    <div style={{ color: 'var(--text-primary)' }}>{item.title}</div>
                  </td>
                  <td style={{ padding: '14px', color: 'var(--text-secondary)' }}>
                    {item.category}
                  </td>
                  <td style={{ padding: '14px' }}>
                    <span style={{ padding: '2px 8px', borderRadius: '6px', background: '#1e293b', fontSize: '0.8rem' }}>
                      {item.experts_count} {item.experts_count === 1 ? 'Expert (Sole)' : 'Experts'}
                    </span>
                  </td>
                  <td style={{ padding: '14px', color: 'var(--text-muted)' }}>
                    {item.primary_factor}
                  </td>
                  <td style={{ padding: '14px' }}>
                    <RiskBadge level={item.risk_level} score={item.risk_score} />
                  </td>
                  <td style={{ padding: '14px', textAlign: 'right' }}>
                    <button
                      onClick={() => onNavigateToKnowledge(item.knowledge_id)}
                      className="btn btn-secondary"
                      style={{ padding: '4px 10px', fontSize: '0.78rem' }}
                    >
                      Inspect
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
