import React, { useState, useEffect } from 'react';
import { riskAPI, knowledgeAPI } from '../services/api';
import RiskBadge from '../components/RiskBadge';
import {
  Sliders, Cpu, ShieldCheck, CheckCircle2,
  Save, Layers
} from 'lucide-react';

export default function RiskStudio({ initialKnowledge = null }) {
  const [knowledgeList, setKnowledgeList] = useState([]);
  const [selectedKnowledgeId, setSelectedKnowledgeId] = useState(initialKnowledge?.knowledge_id || '');

  // 5 Factors
  const [criticality, setCriticality] = useState(initialKnowledge?.risk_score ? 85 : 75);
  const [uniqueness, setUniqueness] = useState(initialKnowledge?.risk_score ? 90 : 80);
  const [dependency, setDependency] = useState(initialKnowledge?.risk_score ? 80 : 70);
  const [docGap, setDocGap] = useState(initialKnowledge?.risk_score ? 60 : 50);
  const [availRisk, setAvailRisk] = useState(initialKnowledge?.risk_score ? 70 : 60);

  // Result state
  const [simulationResult, setSimulationResult] = useState(null);
  const [saving, setSaving] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(null);

  useEffect(() => {
    const fetchKnowledgeOptions = async () => {
      try {
        const res = await knowledgeAPI.getAll({ limit: 50 });
        setKnowledgeList(res.data.items || []);
      } catch (err) {
        console.error(err);
      }
    };
    fetchKnowledgeOptions();
  }, []);

  // Recalculate simulation on factor change
  useEffect(() => {
    const runSimulation = async () => {
      try {
        const res = await riskAPI.simulate({
          criticality: Number(criticality),
          uniqueness: Number(uniqueness),
          dependency: Number(dependency),
          documentation_gap: Number(docGap),
          availability_risk: Number(availRisk)
        });
        setSimulationResult(res.data);
      } catch (err) {
        console.error(err);
      }
    };
    runSimulation();
  }, [criticality, uniqueness, dependency, docGap, availRisk]);

  const loadPreset = (c, u, d, g, a) => {
    setCriticality(c);
    setUniqueness(u);
    setDependency(d);
    setDocGap(g);
    setAvailRisk(a);
    setSaveSuccess(null);
  };

  const handleSaveAssessment = async () => {
    if (!selectedKnowledgeId) {
      alert('Please select a Knowledge Item to save this assessment to.');
      return;
    }
    setSaving(true);
    try {
      await riskAPI.analyze(selectedKnowledgeId, {
        factors: {
          criticality: Number(criticality),
          uniqueness: Number(uniqueness),
          dependency: Number(dependency),
          documentation_gap: Number(docGap),
          availability_risk: Number(availRisk)
        },
        assessment_method: 'hybrid',
        assessment_notes: 'Calculated and saved via Risk Studio'
      });
      setSaveSuccess('Assessment successfully saved to knowledge record!');
    } catch (err) {
      alert('Failed to save assessment');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div>
      <div style={{ marginBottom: '24px' }}>
        <h2 style={{ fontSize: '1.75rem', fontWeight: '800', letterSpacing: '-0.02em', marginBottom: '4px' }}>
          Knowledge Loss Risk Studio & Simulation Engine
        </h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
          Interactive risk parameter calibration, deterministic factor explainability & Scikit-learn ML classification.
        </p>
      </div>

      {/* Preset Buttons */}
      <div style={{ display: 'flex', gap: '10px', marginBottom: '24px', flexWrap: 'wrap' }}>
        <button
          onClick={() => loadPreset(95, 98, 92, 85, 90)}
          className="btn btn-secondary"
          style={{ fontSize: '0.8rem', border: '1px solid rgba(239, 68, 68, 0.4)', background: 'var(--risk-critical-bg)' }}
        >
          Preset: Legacy Banking (Critical 93.15)
        </button>
        <button
          onClick={() => loadPreset(95, 90, 85, 20, 33)}
          className="btn btn-secondary"
          style={{ fontSize: '0.8rem', border: '1px solid rgba(249, 115, 22, 0.4)', background: 'var(--risk-high-bg)' }}
        >
          Preset: AWS Migration (High 74.30)
        </button>
        <button
          onClick={() => loadPreset(65, 35, 45, 40, 20)}
          className="btn btn-secondary"
          style={{ fontSize: '0.8rem', border: '1px solid rgba(245, 158, 11, 0.4)', background: 'var(--risk-medium-bg)' }}
        >
          Preset: Angular Framework (Medium 45.25)
        </button>
        <button
          onClick={() => loadPreset(60, 25, 45, 15, 20)}
          className="btn btn-secondary"
          style={{ fontSize: '0.8rem', border: '1px solid rgba(16, 185, 129, 0.4)', background: 'var(--risk-low-bg)' }}
        >
          Preset: K8s DevOps (Medium/Low 37.50)
        </button>
      </div>

      {/* Two Column Grid: Sliders & Live Results */}
      <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1fr', gap: '24px', marginBottom: '28px' }}>
        {/* Left Column: Sliders */}
        <div className="glass-card" style={{ padding: '26px' }}>
          <h3 style={{ fontSize: '1.15rem', fontWeight: '700', marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Sliders size={18} color="var(--accent-primary)" />
            5-Factor Calibration Sliders
          </h3>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
            {/* Factor 1 */}
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                <span style={{ fontWeight: '600', fontSize: '0.88rem' }}>1. Knowledge Criticality (30% Weight)</span>
                <span style={{ fontWeight: '800', color: 'var(--accent-primary)' }}>{criticality} / 100</span>
              </div>
              <input
                type="range" min="0" max="100" value={criticality}
                onChange={(e) => setCriticality(e.target.value)}
              />
              <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '4px' }}>
                Impact on revenue, system uptime and business processes.
              </div>
            </div>

            {/* Factor 2 */}
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                <span style={{ fontWeight: '600', fontSize: '0.88rem' }}>2. Knowledge Uniqueness (25% Weight)</span>
                <span style={{ fontWeight: '800', color: 'var(--accent-primary)' }}>{uniqueness} / 100</span>
              </div>
              <input
                type="range" min="0" max="100" value={uniqueness}
                onChange={(e) => setUniqueness(e.target.value)}
              />
              <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '4px' }}>
                Inverse of expert count: 1 expert = 95, 2 experts = 75, 4+ experts = 45.
              </div>
            </div>

            {/* Factor 3 */}
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                <span style={{ fontWeight: '600', fontSize: '0.88rem' }}>3. Organizational Dependency (20% Weight)</span>
                <span style={{ fontWeight: '800', color: 'var(--accent-primary)' }}>{dependency} / 100</span>
              </div>
              <input
                type="range" min="0" max="100" value={dependency}
                onChange={(e) => setDependency(e.target.value)}
              />
              <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '4px' }}>
                Number of dependent software systems & departments relying on this knowledge.
              </div>
            </div>

            {/* Factor 4 */}
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                <span style={{ fontWeight: '600', fontSize: '0.88rem' }}>4. Documentation Gap (15% Weight)</span>
                <span style={{ fontWeight: '800', color: 'var(--accent-primary)' }}>{docGap} / 100</span>
              </div>
              <input
                type="range" min="0" max="100" value={docGap}
                onChange={(e) => setDocGap(e.target.value)}
              />
              <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '4px' }}>
                100 - Structural completeness score (runbooks, troubleshooting, step-by-step).
              </div>
            </div>

            {/* Factor 5 */}
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                <span style={{ fontWeight: '600', fontSize: '0.88rem' }}>5. Expert Availability Risk (10% Weight)</span>
                <span style={{ fontWeight: '800', color: 'var(--accent-primary)' }}>{availRisk} / 100</span>
              </div>
              <input
                type="range" min="0" max="100" value={availRisk}
                onChange={(e) => setAvailRisk(e.target.value)}
              />
              <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '4px' }}>
                Probability of expert attrition, retirement proximity, or role transition.
              </div>
            </div>
          </div>
        </div>

        {/* Right Column: Real-time Calculated Gauge & ML Inference */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          {/* Main Score Box */}
          <div className="glass-card" style={{ padding: '26px', textAlign: 'center' }}>
            <div style={{ fontSize: '0.8rem', fontWeight: '700', color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '8px' }}>
              Calculated Composite Risk Score
            </div>

            <div style={{ fontSize: '3.5rem', fontWeight: '900', letterSpacing: '-0.03em', lineHeight: 1.1, color: '#fff' }}>
              {simulationResult ? simulationResult.risk_score.toFixed(2) : '--'}
              <span style={{ fontSize: '1.4rem', color: 'var(--text-muted)', fontWeight: '600' }}>/100</span>
            </div>

            <div style={{ marginTop: '12px', marginBottom: '16px' }}>
              {simulationResult && (
                <RiskBadge level={simulationResult.risk_level} score={null} />
              )}
            </div>

            {/* Dual ML Model Prediction Badge */}
            <div style={{
              padding: '12px 16px', background: 'rgba(255, 255, 255, 0.04)',
              borderRadius: 'var(--radius-md)', border: '1px solid var(--border-subtle)',
              display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.85rem'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                <Cpu size={16} color="var(--accent-secondary)" />
                <span style={{ color: 'var(--text-secondary)' }}>Scikit-learn Model:</span>
              </div>
              <div style={{ fontWeight: '700', color: 'var(--text-primary)' }}>
                {simulationResult?.ml_predicted_level ? simulationResult.ml_predicted_level.toUpperCase() : 'ANALYZING...'}
                {simulationResult?.ml_confidence && (
                  <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginLeft: '6px' }}>
                    ({(simulationResult.ml_confidence * 100).toFixed(0)}% conf)
                  </span>
                )}
              </div>
            </div>
          </div>

          {/* Associate & Save to Knowledge Item */}
          <div className="glass-card" style={{ padding: '20px' }}>
            <div style={{ fontSize: '0.85rem', fontWeight: '700', marginBottom: '10px' }}>
              Save Assessment to Knowledge Record:
            </div>

            {saveSuccess && (
              <div style={{
                background: 'var(--risk-low-bg)', border: '1px solid rgba(16, 185, 129, 0.3)',
                borderRadius: 'var(--radius-md)', padding: '10px', color: '#6ee7b7',
                fontSize: '0.82rem', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '6px'
              }}>
                <CheckCircle2 size={14} />
                <div>{saveSuccess}</div>
              </div>
            )}

            <div style={{ display: 'flex', gap: '10px' }}>
              <select
                value={selectedKnowledgeId}
                onChange={(e) => setSelectedKnowledgeId(e.target.value)}
                className="select"
                style={{ fontSize: '0.85rem' }}
              >
                <option value="">Select Knowledge Item...</option>
                {knowledgeList.map((k) => (
                  <option key={k.knowledge_id} value={k.knowledge_id}>{k.title}</option>
                ))}
              </select>

              <button
                onClick={handleSaveAssessment}
                disabled={saving || !selectedKnowledgeId}
                className="btn btn-primary"
                style={{ whiteSpace: 'nowrap' }}
              >
                <Save size={15} /> {saving ? 'Saving...' : 'Persist'}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Factor Explainability Breakdown Table */}
      {simulationResult && (
        <div className="glass-card" style={{ padding: '26px', marginBottom: '28px' }}>
          <h3 style={{ fontSize: '1.15rem', fontWeight: '700', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Layers size={18} color="var(--accent-primary)" />
            Contributing Factor Explainability Breakdown
          </h3>

          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.88rem' }}>
              <thead>
                <tr style={{ borderBottom: '1px solid var(--border-subtle)', color: 'var(--text-muted)' }}>
                  <th style={{ padding: '12px 14px' }}>FACTOR NAME</th>
                  <th style={{ padding: '12px 14px' }}>RAW VALUE</th>
                  <th style={{ padding: '12px 14px' }}>WEIGHT</th>
                  <th style={{ padding: '12px 14px' }}>POINTS CONTRIBUTED</th>
                  <th style={{ padding: '12px 14px' }}>EXPLAINABILITY & IMPACT</th>
                </tr>
              </thead>
              <tbody>
                {simulationResult.factor_breakdown.map((fb, idx) => (
                  <tr key={idx} style={{ borderBottom: '1px solid var(--border-subtle)' }}>
                    <td style={{ padding: '14px', fontWeight: '600' }}>{fb.factor_name}</td>
                    <td style={{ padding: '14px', fontWeight: '700' }}>{fb.raw_score}</td>
                    <td style={{ padding: '14px', color: 'var(--text-muted)' }}>{(fb.weight * 100).toFixed(0)}%</td>
                    <td style={{ padding: '14px', fontWeight: '800', color: 'var(--accent-primary)' }}>
                      +{fb.weighted_score.toFixed(2)}
                    </td>
                    <td style={{ padding: '14px', color: 'var(--text-secondary)', fontSize: '0.82rem' }}>
                      {fb.interpretation}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Automated Preservation Recommendations */}
      {simulationResult && simulationResult.recommendations.length > 0 && (
        <div className="glass-card" style={{ padding: '24px' }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: '700', marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <ShieldCheck size={18} color="var(--risk-low)" />
            Automated Preservation Recommendations
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {simulationResult.recommendations.map((rec, idx) => (
              <div key={idx} style={{
                display: 'flex', alignItems: 'center', gap: '10px',
                padding: '12px 14px', background: 'rgba(255, 255, 255, 0.03)',
                borderRadius: 'var(--radius-md)', fontSize: '0.88rem'
              }}>
                <CheckCircle2 size={16} color="var(--accent-primary)" style={{ flexShrink: 0 }} />
                <span>{rec}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
