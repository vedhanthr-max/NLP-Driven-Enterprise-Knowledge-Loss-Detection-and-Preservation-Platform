import React, { useState, useEffect } from 'react';
import { knowledgeAPI } from '../services/api';
import RiskBadge from '../components/RiskBadge';
import {
  ArrowLeft, Users, Tag, Cpu,
  Calendar, CheckCircle
} from 'lucide-react';

export default function KnowledgeDetail({ knowledgeId, onBack, onOpenRiskStudio }) {
  const [detail, setDetail] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDetail = async () => {
      setLoading(true);
      try {
        const res = await knowledgeAPI.getDetails(knowledgeId);
        setDetail(res.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    if (knowledgeId) {
      fetchDetail();
    }
  }, [knowledgeId]);

  if (loading) {
    return <div style={{ padding: '40px', textAlign: 'center', color: 'var(--text-muted)' }}>Loading knowledge profile...</div>;
  }

  if (!detail) {
    return (
      <div className="glass-card" style={{ padding: '32px', textAlign: 'center' }}>
        <div>Knowledge record not found.</div>
        <button onClick={onBack} className="btn btn-secondary" style={{ marginTop: '16px' }}>Back to Catalog</button>
      </div>
    );
  }

  return (
    <div>
      {/* Back button */}
      <button onClick={onBack} className="btn btn-secondary" style={{ marginBottom: '20px', padding: '6px 12px', fontSize: '0.82rem' }}>
        <ArrowLeft size={16} /> Back to Catalog
      </button>

      {/* Main Header Card */}
      <div className="glass-card" style={{ padding: '28px', marginBottom: '24px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '14px' }}>
          <div>
            <span style={{ fontSize: '0.78rem', fontWeight: '700', color: 'var(--accent-primary)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              {detail.category} {detail.subcategory ? `• ${detail.subcategory}` : ''}
            </span>
            <h2 style={{ fontSize: '1.6rem', fontWeight: '800', marginTop: '4px', lineHeight: 1.3 }}>
              {detail.title}
            </h2>
          </div>
          <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
            <RiskBadge level={detail.risk_level} score={detail.risk_score} />
            <button
              onClick={() => onOpenRiskStudio(detail)}
              className="btn btn-primary"
              style={{ fontSize: '0.82rem', padding: '6px 12px' }}
            >
              Analyze in Risk Studio
            </button>
          </div>
        </div>

        <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', lineHeight: 1.7, marginBottom: '20px' }}>
          {detail.description || 'No detailed description available.'}
        </p>

        {/* Metadata Badges */}
        <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap', fontSize: '0.8rem', color: 'var(--text-muted)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <Calendar size={14} /> Created: {new Date(detail.created_at).toLocaleDateString()}
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <CheckCircle size={14} color="var(--risk-low)" /> Status: {detail.status.toUpperCase()}
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <Cpu size={14} /> Extraction Confidence: {(detail.confidence_score * 100).toFixed(0)}%
          </div>
        </div>
      </div>

      {/* Two Column Layout: Experts & Entities */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px', marginBottom: '24px' }}>
        {/* Identified Experts */}
        <div className="glass-card" style={{ padding: '24px' }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: '700', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Users size={18} color="var(--accent-primary)" />
            Associated Subject Matter Experts ({detail.experts.length})
          </h3>

          {detail.experts.length === 0 ? (
            <div style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>No individual experts identified yet.</div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {detail.experts.map((exp, idx) => (
                <div key={idx} style={{
                  display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                  padding: '12px 14px', background: 'rgba(255, 255, 255, 0.03)',
                  border: '1px solid var(--border-subtle)', borderRadius: 'var(--radius-md)'
                }}>
                  <div>
                    <div style={{ fontWeight: '600', fontSize: '0.9rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
                      {exp.full_name}
                      {exp.is_primary_expert && (
                        <span style={{ fontSize: '0.7rem', padding: '2px 6px', borderRadius: '4px', background: 'rgba(99, 102, 241, 0.2)', color: 'var(--accent-primary)', fontWeight: '700' }}>
                          PRIMARY
                        </span>
                      )}
                    </div>
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                      Tenure/Experience: {exp.years_of_experience} years
                    </div>
                  </div>
                  <span className="badge" style={{ background: '#1e293b', color: 'var(--text-primary)' }}>
                    {exp.expertise_level.toUpperCase()}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* NLP Entities */}
        <div className="glass-card" style={{ padding: '24px' }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: '700', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Cpu size={18} color="var(--accent-secondary)" />
            Extracted Named Entities ({detail.entities.length})
          </h3>

          {detail.entities.length === 0 ? (
            <div style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>No entities extracted.</div>
          ) : (
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
              {detail.entities.map((ent, idx) => {
                const colorMap = {
                  TECHNOLOGY: '#818cf8',
                  PRODUCT: '#38bdf8',
                  PERSON: '#f472b6',
                  ORGANIZATION: '#34d399',
                  PROCESS: '#fbbf24'
                };
                const c = colorMap[ent.entity_type] || '#94a3b8';
                return (
                  <span key={idx} style={{
                    display: 'inline-flex', alignItems: 'center', gap: '6px',
                    padding: '4px 10px', borderRadius: '6px',
                    background: 'rgba(255, 255, 255, 0.04)', border: `1px solid ${c}33`,
                    fontSize: '0.78rem'
                  }}>
                    <span style={{ width: '6px', height: '6px', borderRadius: '50%', background: c }} />
                    <span style={{ fontWeight: '600', color: '#fff' }}>{ent.entity_name}</span>
                    <span style={{ fontSize: '0.68rem', color: 'var(--text-muted)' }}>({ent.entity_type})</span>
                  </span>
                );
              })}
            </div>
          )}
        </div>
      </div>

      {/* Keywords Section */}
      <div className="glass-card" style={{ padding: '24px' }}>
        <h3 style={{ fontSize: '1.1rem', fontWeight: '700', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Tag size={18} color="var(--risk-medium)" />
          TF-IDF Technical Keywords ({detail.keywords.length})
        </h3>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
          {detail.keywords.map((kw, idx) => (
            <span key={idx} style={{
              padding: '4px 10px', borderRadius: 'var(--radius-md)',
              background: '#131b2e', border: '1px solid var(--border-subtle)',
              fontSize: '0.8rem', display: 'inline-flex', alignItems: 'center', gap: '6px'
            }}>
              <span style={{ fontWeight: '600' }}>#{kw.keyword}</span>
              <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>TF-IDF: {kw.tf_idf_score.toFixed(2)}</span>
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}
