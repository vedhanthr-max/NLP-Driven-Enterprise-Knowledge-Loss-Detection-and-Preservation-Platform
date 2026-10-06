import React, { useState, useEffect } from 'react';
import { employeeAPI } from '../services/api';
import { Users, Search, Briefcase, Calendar, ShieldAlert, Award, ArrowUpRight } from 'lucide-react';

export default function Employees({ onSelectEmployee }) {
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [deptFilter, setDeptFilter] = useState('ALL');

  useEffect(() => {
    loadEmployees();
  }, []);

  const loadEmployees = async () => {
    setLoading(true);
    try {
      const res = await employeeAPI.getAll();
      setEmployees(res.data.items || res.data || []);
    } catch (err) {
      console.error('Failed to load employees', err);
    } finally {
      setLoading(false);
    }
  };

  const filtered = employees.filter((emp) => {
    const matchesSearch =
      (emp.full_name || '').toLowerCase().includes(search.toLowerCase()) ||
      (emp.job_title || '').toLowerCase().includes(search.toLowerCase()) ||
      (emp.skills || []).some(s => s.toLowerCase().includes(search.toLowerCase()));
    const matchesDept = deptFilter === 'ALL' || (emp.department_name || '') === deptFilter;
    return matchesSearch && matchesDept;
  });

  const departments = ['ALL', ...new Set(employees.map(e => e.department_name).filter(Boolean))];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* Header */}
      <div>
        <h2 style={{ fontSize: '1.75rem', fontWeight: '800', letterSpacing: '-0.02em', display: 'flex', alignItems: 'center', gap: '10px' }}>
          <Users style={{ color: 'var(--accent-primary)' }} />
          Expert Directory & Attrition Watchlist
        </h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginTop: '4px' }}>
          Monitor key subject matter experts, single-points-of-failure, and domain coverage.
        </p>
      </div>

      {/* Filters Bar */}
      <div className="card" style={{ padding: '16px 20px', display: 'flex', gap: '16px', alignItems: 'center', flexWrap: 'wrap' }}>
        <div style={{ position: 'relative', flex: 1, minWidth: '240px' }}>
          <Search size={16} style={{ position: 'absolute', left: '12px', top: '12px', color: 'var(--text-muted)' }} />
          <input
            type="text"
            className="input-field"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search by expert name, title, or tech skill..."
            style={{ width: '100%', paddingLeft: '38px', height: '40px' }}
          />
        </div>

        <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: '600' }}>DEPARTMENT:</span>
          <select
            value={deptFilter}
            onChange={(e) => setDeptFilter(e.target.value)}
            className="input-field"
            style={{ height: '40px' }}
          >
            {departments.map((d) => (
              <option key={d} value={d}>{d}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Employee Grid */}
      <div className="grid-3">
        {filtered.map((emp) => {
          const flightRisk = emp.flight_risk || (emp.tenure_years > 7 ? 'High' : (emp.tenure_years > 3 ? 'Medium' : 'Low'));
          const flightColor = flightRisk === 'High' ? '#ef4444' : (flightRisk === 'Medium' ? '#f59e0b' : '#10b981');

          return (
            <div
              key={emp.id}
              className="card"
              style={{
                display: 'flex', flexDirection: 'column', gap: '14px',
                borderTop: `4px solid ${flightColor}`
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
                  <div style={{
                    width: '42px', height: '42px', borderRadius: '50%',
                    background: '#1e293b', border: '1px solid var(--border-subtle)',
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    fontWeight: '700', fontSize: '1rem', color: 'var(--accent-primary)'
                  }}>
                    {emp.full_name ? emp.full_name[0] : 'E'}
                  </div>
                  <div>
                    <h3 style={{ fontSize: '1rem', fontWeight: '700' }}>{emp.full_name}</h3>
                    <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>{emp.email}</div>
                  </div>
                </div>

                <span style={{
                  fontSize: '0.68rem', fontWeight: '700',
                  padding: '2px 8px', borderRadius: '12px',
                  background: `${flightColor}20`, color: flightColor, border: `1px solid ${flightColor}50`
                }}>
                  {flightRisk} Flight Risk
                </span>
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <Briefcase size={14} style={{ color: 'var(--text-muted)' }} />
                  <span>{emp.job_title || 'Domain Specialist'} • {emp.department_name || 'Engineering'}</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <Calendar size={14} style={{ color: 'var(--text-muted)' }} />
                  <span>Tenure: {emp.tenure_years || 5} years in organization</span>
                </div>
              </div>

              {/* Skills badges */}
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                {(emp.skills || ['Distributed Systems', 'Cloud Architecture']).map((skill, idx) => (
                  <span
                    key={idx}
                    style={{
                      fontSize: '0.7rem', background: 'rgba(255,255,255,0.05)',
                      color: 'var(--text-secondary)', padding: '2px 8px', borderRadius: '4px'
                    }}
                  >
                    {skill}
                  </span>
                ))}
              </div>

              <div style={{
                marginTop: 'auto', paddingTop: '10px',
                borderTop: '1px solid var(--border-subtle)',
                display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                fontSize: '0.75rem', color: 'var(--text-muted)'
              }}>
                <span>Linked Assets: <strong style={{ color: 'var(--text-primary)' }}>{emp.knowledge_count || 3}</strong></span>
                <span style={{ color: 'var(--accent-primary)', fontWeight: '600' }}>Active SME</span>
              </div>
            </div>
          );
        })}

        {filtered.length === 0 && !loading && (
          <div className="card" style={{ gridColumn: 'span 3', textAlign: 'center', padding: '40px' }}>
            <p style={{ color: 'var(--text-secondary)' }}>No personnel matched your criteria.</p>
          </div>
        )}
      </div>
    </div>
  );
}
