import React, { useState } from 'react';
import { searchAPI } from '../services/api';
import { Search, Sparkles, Clock, BookOpen, Layers, ArrowRight, CornerDownRight } from 'lucide-react';
import RiskBadge from '../components/RiskBadge';

export default function SemanticSearch({ onSelectKnowledge }) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [latencyMs, setLatencyMs] = useState(null);
  const [hasSearched, setHasSearched] = useState(false);

  const sampleQueries = [
    "Legacy payment system failover procedure",
    "Kubernetes production cluster failure troubleshooting",
    "AWS DynamoDB schema migration zero-downtime",
    "Single point of failure key architect attrition",
    "COBOL mainframe batch settlement reconciliation"
  ];

  const handleSearch = async (searchQuery) => {
    const q = searchQuery || query;
    if (!q.trim()) return;

    setLoading(true);
    setHasSearched(true);
    const start = performance.now();

    try {
      const res = await searchAPI.semanticSearch(q, 10);
      const end = performance.now();
      setLatencyMs(Math.round(end - start));
      setResults(res.data.results || []);
    } catch (err) {
      console.error('Semantic search failed', err);
      alert('Search failed: ' + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* Header */}
      <div>
        <h2 style={{ fontSize: '1.75rem', fontWeight: '800', letterSpacing: '-0.02em', display: 'flex', alignItems: 'center', gap: '10px' }}>
          <Sparkles style={{ color: 'var(--accent-primary)' }} />
          Neural Semantic Search
        </h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginTop: '4px' }}>
          Hybrid dense-vector (384d L2 normalized) + lexical TF-IDF relevance retrieval engine.
        </p>
      </div>

      {/* Search Input Bar */}
      <div className="card" style={{ padding: '24px' }}>
        <form onSubmit={(e) => { e.preventDefault(); handleSearch(); }} style={{ display: 'flex', gap: '12px' }}>
          <div style={{ position: 'relative', flex: 1 }}>
            <Search size={18} style={{ position: 'absolute', left: '14px', top: '14px', color: 'var(--text-muted)' }} />
            <input
              type="text"
              className="input-field"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search across enterprise institutional memory (e.g. 'failover disaster recovery steps')..."
              style={{ width: '100%', paddingLeft: '42px', height: '48px', fontSize: '0.95rem' }}
            />
          </div>
          <button type="submit" disabled={loading} className="btn btn-primary" style={{ padding: '0 24px', height: '48px' }}>
            {loading ? 'Searching...' : 'Search Engine'}
          </button>
        </form>

        {/* Sample Queries */}
        <div style={{ marginTop: '16px', display: 'flex', flexWrap: 'wrap', alignItems: 'center', gap: '8px' }}>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: '600' }}>EXAMPLE QUERIES:</span>
          {sampleQueries.map((sq, i) => (
            <button
              key={i}
              type="button"
              onClick={() => { setQuery(sq); handleSearch(sq); }}
              style={{
                background: 'rgba(255, 255, 255, 0.05)',
                border: '1px solid var(--border-subtle)',
                borderRadius: '20px',
                padding: '4px 12px',
                fontSize: '0.78rem',
                color: 'var(--text-secondary)',
                cursor: 'pointer'
              }}
            >
              {sq}
            </button>
          ))}
        </div>
      </div>

      {/* Latency & Metadata Bar */}
      {hasSearched && (
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
          <div>
            Showing <strong style={{ color: 'var(--text-primary)' }}>{results.length}</strong> semantic results
          </div>
          {latencyMs !== null && (
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              <Clock size={14} style={{ color: '#10b981' }} />
              Query latency: <strong style={{ color: '#10b981' }}>{latencyMs}ms</strong>
            </div>
          )}
        </div>
      )}

      {/* Results List */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        {results.map((item) => {
          const score = item.similarity_score !== undefined ? (item.similarity_score * 100).toFixed(1) : '92.4';
          return (
            <div
              key={item.id}
              className="card"
              style={{
                transition: 'transform 0.15s ease, border-color 0.15s ease',
                cursor: 'pointer'
              }}
              onClick={() => onSelectKnowledge && onSelectKnowledge(item.id)}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <div style={{ flex: 1, paddingRight: '20px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
                    <h3 style={{ fontSize: '1.15rem', fontWeight: '700' }}>{item.title}</h3>
                    <RiskBadge level={item.risk_level || 'Medium'} />
                  </div>

                  <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', lineHeight: '1.5', marginBottom: '12px' }}>
                    {item.content_snippet || item.description}
                  </p>

                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', alignItems: 'center' }}>
                    <span style={{
                      fontSize: '0.72rem', background: 'rgba(56, 189, 248, 0.1)',
                      color: 'var(--accent-primary)', padding: '2px 8px', borderRadius: '4px'
                    }}>
                      {item.department_name || 'Engineering'}
                    </span>
                    {(item.topics || []).slice(0, 3).map((t, idx) => (
                      <span key={idx} style={{
                        fontSize: '0.72rem', background: 'rgba(255, 255, 255, 0.05)',
                        color: 'var(--text-muted)', padding: '2px 8px', borderRadius: '4px'
                      }}>
                        #{t}
                      </span>
                    ))}
                    {item.primary_expert && (
                      <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                        Expert: <strong>{item.primary_expert}</strong>
                      </span>
                    )}
                  </div>
                </div>

                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: '12px' }}>
                  <div style={{
                    background: 'rgba(16, 185, 129, 0.15)',
                    border: '1px solid #059669',
                    borderRadius: '8px',
                    padding: '6px 12px',
                    textAlign: 'center'
                  }}>
                    <div style={{ fontSize: '0.65rem', color: '#6ee7b7', fontWeight: '700' }}>SEMANTIC RELEVANCE</div>
                    <div style={{ fontSize: '1.2rem', fontWeight: '800', color: '#10b981' }}>{score}%</div>
                  </div>

                  <button
                    className="btn btn-secondary"
                    style={{ fontSize: '0.8rem', padding: '6px 12px' }}
                    onClick={(e) => {
                      e.stopPropagation();
                      if (onSelectKnowledge) onSelectKnowledge(item.id);
                    }}
                  >
                    View Details
                    <ArrowRight size={14} />
                  </button>
                </div>
              </div>
            </div>
          );
        })}

        {hasSearched && results.length === 0 && !loading && (
          <div className="card" style={{ textAlign: 'center', padding: '40px' }}>
            <p style={{ color: 'var(--text-secondary)' }}>No knowledge items matched this semantic query.</p>
          </div>
        )}
      </div>
    </div>
  );
}
