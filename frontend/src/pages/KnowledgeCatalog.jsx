import React, { useState, useEffect } from 'react';
import { knowledgeAPI } from '../services/api';
import RiskBadge from '../components/RiskBadge';
import { BookOpen, Search, Filter, Tag, Users, ArrowRight, RefreshCw } from 'lucide-react';

export default function KnowledgeCatalog({ onSelectKnowledge }) {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('');
  const [riskLevel, setRiskLevel] = useState('');

  const categories = [
    'All Categories',
    'Legacy Systems',
    'Database Administration',
    'DevOps & Deployment',
    'Cloud Infrastructure',
    'Security & Compliance',
    'Application Development'
  ];

  const fetchKnowledge = async () => {
    setLoading(true);
    try {
      const params = {};
      if (search) params.search = search;
      if (category && category !== 'All Categories') params.category = category;
      if (riskLevel && riskLevel !== 'all') params.risk_level = riskLevel;

      const res = await knowledgeAPI.getAll(params);
      setItems(res.data.items || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchKnowledge();
  }, [category, riskLevel]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    fetchKnowledge();
  };

  return (
    <div>
      <div style={{ marginBottom: '24px' }}>
        <h2 style={{ fontSize: '1.75rem', fontWeight: '800', letterSpacing: '-0.02em', marginBottom: '4px' }}>
          Enterprise Knowledge Catalog
        </h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
          Structured organizational knowledge records linked to primary technical experts, extracted entities & risk assessments.
        </p>
      </div>

      {/* Filters Bar */}
      <div className="glass-card" style={{ padding: '18px 22px', marginBottom: '28px' }}>
        <form onSubmit={handleSearchSubmit} style={{ display: 'grid', gridTemplateColumns: '2fr 1.2fr 1fr auto', gap: '14px', alignItems: 'center' }}>
          <div style={{ position: 'relative' }}>
            <Search size={18} style={{ position: 'absolute', left: '12px', top: '11px', color: 'var(--text-muted)' }} />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search knowledge title or keywords..."
              className="input"
              style={{ paddingLeft: '38px' }}
            />
          </div>

          <div>
            <select
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="select"
            >
              {categories.map((c) => (
                <option key={c} value={c}>{c}</option>
              ))}
            </select>
          </div>

          <div>
            <select
              value={riskLevel}
              onChange={(e) => setRiskLevel(e.target.value)}
              className="select"
            >
              <option value="">All Risk Levels</option>
              <option value="critical">Critical (81-100)</option>
              <option value="high">High (61-80)</option>
              <option value="medium">Medium (31-60)</option>
              <option value="low">Low (0-30)</option>
            </select>
          </div>

          <button type="submit" className="btn btn-primary" style={{ padding: '10px 18px' }}>
            Filter
          </button>
        </form>
      </div>

      {/* Knowledge Grid */}
      {loading ? (
        <div style={{ textAlign: 'center', padding: '40px', color: 'var(--text-muted)' }}>
          <RefreshCw size={24} className="animate-spin" style={{ marginBottom: '10px' }} />
          <div>Loading knowledge records...</div>
        </div>
      ) : items.length === 0 ? (
        <div className="glass-card" style={{ padding: '40px', textAlign: 'center', color: 'var(--text-muted)' }}>
          <BookOpen size={42} style={{ opacity: 0.3, marginBottom: '12px' }} />
          <div>No knowledge records found matching the active filter criteria.</div>
        </div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(340px, 1fr))', gap: '20px' }}>
          {items.map((item) => (
            <div
              key={item.knowledge_id}
              className="glass-card"
              onClick={() => onSelectKnowledge(item.knowledge_id)}
              style={{
                padding: '22px', display: 'flex', flexDirection: 'column',
                justifyContent: 'space-between', cursor: 'pointer'
              }}
            >
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '10px' }}>
                  <span style={{ fontSize: '0.75rem', fontWeight: '700', color: 'var(--accent-primary)', textTransform: 'uppercase' }}>
                    {item.category}
                  </span>
                  <RiskBadge level={item.risk_level} score={item.risk_score} />
                </div>

                <h3 style={{ fontSize: '1.05rem', fontWeight: '700', marginBottom: '12px', lineHeight: 1.4 }}>
                  {item.title}
                </h3>

                {/* Tags */}
                {item.tags && item.tags.length > 0 && (
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', marginBottom: '16px' }}>
                    {item.tags.slice(0, 4).map((t, idx) => (
                      <span key={idx} style={{
                        fontSize: '0.72rem', padding: '2px 8px', borderRadius: '4px',
                        background: 'rgba(255, 255, 255, 0.05)', color: 'var(--text-secondary)'
                      }}>
                        #{t}
                      </span>
                    ))}
                  </div>
                )}
              </div>

              <div style={{
                display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                paddingTop: '14px', borderTop: '1px solid var(--border-subtle)',
                fontSize: '0.8rem', color: 'var(--text-muted)'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <Users size={15} />
                  <span>{item.experts_count} {item.experts_count === 1 ? 'Expert' : 'Experts'}</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '4px', color: 'var(--accent-primary)', fontWeight: '600' }}>
                  Inspect <ArrowRight size={14} />
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
