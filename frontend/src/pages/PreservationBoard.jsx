import React, { useState, useEffect } from 'react';
import { preservationAPI, knowledgeAPI } from '../services/api';
import { ShieldCheck, Plus, CheckCircle2, Clock, AlertCircle, PlayCircle, ArrowRight, UserCheck } from 'lucide-react';
import RiskBadge from '../components/RiskBadge';

const STAGES = [
  { id: 'recommended', label: 'AI Recommended', color: '#f59e0b', border: '#b45309' },
  { id: 'planned', label: 'Planned & Scheduled', color: '#38bdf8', border: '#0284c7' },
  { id: 'in_progress', label: 'In Progress', color: '#a855f7', border: '#7e22ce' },
  { id: 'completed', label: 'Preserved & Verified', color: '#10b981', border: '#059669' }
];

export default function PreservationBoard() {
  const [actions, setActions] = useState([]);
  const [knowledgeList, setKnowledgeList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [newAction, setNewAction] = useState({
    title: '',
    description: '',
    action_type: 'documentation',
    priority: 'high',
    knowledge_item_id: '',
    due_date: ''
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [resActions, resKnowledge] = await Promise.all([
        preservationAPI.getAll(),
        knowledgeAPI.getAll()
      ]);
      const rawActions = Array.isArray(resActions.data) ? resActions.data : (resActions.data.items || []);
      const rawKnowledge = Array.isArray(resKnowledge.data) ? resKnowledge.data : (resKnowledge.data.items || []);
      setActions(rawActions);
      setKnowledgeList(rawKnowledge);
    } catch (err) {
      console.error('Failed to load preservation data', err);
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateStatus = async (actionId, newStatus) => {
    try {
      await preservationAPI.update(actionId, { status: newStatus });
      setActions(actions.map(a => (a.action_id === actionId || a.id === actionId) ? { ...a, status: newStatus } : a));
    } catch (err) {
      console.error('Failed to update status', err);
      alert('Failed to update status: ' + (err.response?.data?.detail || err.message));
    }
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    if (!newAction.title || !newAction.knowledge_item_id) {
      alert('Please fill in title and select a knowledge asset.');
      return;
    }

    try {
      const payload = {
        knowledge_id: parseInt(newAction.knowledge_item_id),
        action_type: newAction.action_type,
        action_description: `${newAction.title}${newAction.description ? ': ' + newAction.description : ''}`,
        priority: newAction.priority,
        deadline: newAction.due_date || null
      };
      const res = await preservationAPI.create(payload);
      setActions([res.data, ...actions]);
      setShowModal(false);
      setNewAction({
        title: '',
        description: '',
        action_type: 'documentation',
        priority: 'high',
        knowledge_item_id: '',
        due_date: ''
      });
    } catch (err) {
      console.error('Create action failed', err);
      alert('Failed to create action: ' + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div>
          <h2 style={{ fontSize: '1.75rem', fontWeight: '800', letterSpacing: '-0.02em', display: 'flex', alignItems: 'center', gap: '10px' }}>
            <ShieldCheck style={{ color: 'var(--accent-primary)' }} />
            Preservation Action Board
          </h2>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginTop: '4px' }}>
            Orchestrate knowledge transfer workflows, pair shadowing, and archival documentation.
          </p>
        </div>

        <button
          onClick={() => setShowModal(true)}
          className="btn btn-primary"
          style={{ display: 'flex', alignItems: 'center', gap: '8px' }}
        >
          <Plus size={16} />
          Plan Preservation Action
        </button>
      </div>

      {/* Kanban Stages Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px', alignItems: 'start' }}>
        {STAGES.map((stage) => {
          const stageActions = actions.filter(a => (a.status || 'recommended').toLowerCase() === stage.id);
          return (
            <div
              key={stage.id}
              style={{
                background: 'var(--bg-card)',
                border: '1px solid var(--border-subtle)',
                borderRadius: 'var(--radius-lg)',
                padding: '16px',
                display: 'flex',
                flexDirection: 'column',
                gap: '12px',
                minHeight: '500px'
              }}
            >
              <div style={{
                display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                paddingBottom: '12px', borderBottom: `2px solid ${stage.color}`
              }}>
                <span style={{ fontWeight: '700', fontSize: '0.9rem', color: stage.color }}>
                  {stage.label}
                </span>
                <span style={{
                  fontSize: '0.75rem', background: 'rgba(255,255,255,0.08)',
                  padding: '2px 8px', borderRadius: '10px', fontWeight: '700'
                }}>
                  {stageActions.length}
                </span>
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', flex: 1 }}>
                {stageActions.map((action) => {
                  const actionId = action.action_id || action.id;
                  const actionTitle = action.action_description || action.title || 'Preservation Task';
                  const kTitle = action.knowledge_title || action.knowledge_item_title;
                  const dueDate = action.deadline || action.due_date;

                  return (
                    <div
                      key={actionId}
                      style={{
                        background: 'rgba(255,255,255,0.02)',
                        border: '1px solid var(--border-subtle)',
                        borderRadius: 'var(--radius-md)',
                        padding: '14px',
                        display: 'flex',
                        flexDirection: 'column',
                        gap: '8px'
                      }}
                    >
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                        <span style={{
                          fontSize: '0.7rem', textTransform: 'uppercase',
                          color: 'var(--accent-primary)', fontWeight: '700'
                        }}>
                          {action.action_type ? action.action_type.replace('_', ' ') : 'Action'}
                        </span>
                        <span style={{
                          fontSize: '0.65rem',
                          fontWeight: '700',
                          padding: '1px 6px',
                          borderRadius: '4px',
                          background: action.priority === 'critical' ? '#7f1d1d' : (action.priority === 'high' ? '#7c2d12' : '#14532d'),
                          color: action.priority === 'critical' ? '#fecaca' : (action.priority === 'high' ? '#fed7aa' : '#bbf7d0')
                        }}>
                          {action.priority?.toUpperCase()}
                        </span>
                      </div>

                      <h4 style={{ fontSize: '0.9rem', fontWeight: '700', lineHeight: '1.3' }}>{actionTitle}</h4>

                      {kTitle && (
                        <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>
                          Asset: <span style={{ color: 'var(--text-primary)' }}>{kTitle}</span>
                        </div>
                      )}

                      {/* Progress / Transition Buttons */}
                      <div style={{
                        marginTop: '6px', paddingTop: '8px',
                        borderTop: '1px solid var(--border-subtle)',
                        display: 'flex', justifyContent: 'space-between', alignItems: 'center'
                      }}>
                        <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>
                          {dueDate ? `Due: ${new Date(dueDate).toLocaleDateString()}` : 'No deadline'}
                        </span>

                        <div style={{ display: 'flex', gap: '4px' }}>
                          {stage.id === 'recommended' && (
                            <button
                              onClick={() => handleUpdateStatus(actionId, 'planned')}
                              className="btn btn-secondary"
                              style={{ fontSize: '0.7rem', padding: '3px 8px' }}
                            >
                              Accept
                            </button>
                          )}
                          {stage.id === 'planned' && (
                            <button
                              onClick={() => handleUpdateStatus(actionId, 'in_progress')}
                              className="btn btn-secondary"
                              style={{ fontSize: '0.7rem', padding: '3px 8px' }}
                            >
                              Start
                            </button>
                          )}
                          {stage.id === 'in_progress' && (
                            <button
                              onClick={() => handleUpdateStatus(actionId, 'completed')}
                              className="btn btn-primary"
                              style={{ fontSize: '0.7rem', padding: '3px 8px' }}
                            >
                              Complete
                            </button>
                          )}
                          {stage.id === 'completed' && (
                            <CheckCircle2 size={16} style={{ color: '#10b981' }} />
                          )}
                        </div>
                      </div>
                    </div>
                  );
                })}

                {stageActions.length === 0 && (
                  <div style={{ textAlign: 'center', padding: '24px 0', color: 'var(--text-muted)', fontSize: '0.8rem' }}>
                    No actions in this phase
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Modal for creating action */}
      {showModal && (
        <div style={{
          position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
          background: 'rgba(0,0,0,0.75)', backdropFilter: 'blur(4px)',
          display: 'flex', justifyContent: 'center', alignItems: 'center', zIndex: 1000
        }}>
          <div className="card" style={{ width: '540px', maxHeight: '90vh', overflowY: 'auto' }}>
            <h3 style={{ fontSize: '1.25rem', fontWeight: '800', marginBottom: '16px' }}>
              Plan Preservation Initiative
            </h3>

            <form onSubmit={handleCreate} style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
              <div>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: '600', marginBottom: '6px' }}>Action Title *</label>
                <input
                  type="text"
                  required
                  value={newAction.title}
                  onChange={(e) => setNewAction({ ...newAction, title: e.target.value })}
                  placeholder="e.g. Video Archival of Mainframe Failover Routine"
                  className="input-field"
                  style={{ width: '100%' }}
                />
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: '600', marginBottom: '6px' }}>Associated Knowledge Item *</label>
                <select
                  required
                  value={newAction.knowledge_item_id}
                  onChange={(e) => setNewAction({ ...newAction, knowledge_item_id: e.target.value })}
                  className="input-field"
                  style={{ width: '100%' }}
                >
                  <option value="">-- Select Knowledge Asset --</option>
                  {knowledgeList.map((k) => (
                    <option key={k.id} value={k.id}>{k.title}</option>
                  ))}
                </select>
              </div>

              <div className="grid-2">
                <div>
                  <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: '600', marginBottom: '6px' }}>Action Format</label>
                  <select
                    value={newAction.action_type}
                    onChange={(e) => setNewAction({ ...newAction, action_type: e.target.value })}
                    className="input-field"
                    style={{ width: '100%' }}
                  >
                    <option value="documentation">Documentation Sprint</option>
                    <option value="expert_interview">Structured Expert Interview</option>
                    <option value="shadowing">Pair Mentorship / Shadowing</option>
                    <option value="video_recording">Screen & Walkthrough Recording</option>
                    <option value="cross_training">Team Cross-Training Workshop</option>
                  </select>
                </div>

                <div>
                  <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: '600', marginBottom: '6px' }}>Priority Level</label>
                  <select
                    value={newAction.priority}
                    onChange={(e) => setNewAction({ ...newAction, priority: e.target.value })}
                    className="input-field"
                    style={{ width: '100%' }}
                  >
                    <option value="critical">Critical</option>
                    <option value="high">High</option>
                    <option value="medium">Medium</option>
                    <option value="low">Low</option>
                  </select>
                </div>
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: '600', marginBottom: '6px' }}>Preservation Scope & Steps</label>
                <textarea
                  rows="3"
                  value={newAction.description}
                  onChange={(e) => setNewAction({ ...newAction, description: e.target.value })}
                  placeholder="Detail the deliverables, questions to capture, or cross-training agenda..."
                  className="input-field"
                  style={{ width: '100%' }}
                />
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: '600', marginBottom: '6px' }}>Target Due Date</label>
                <input
                  type="date"
                  value={newAction.due_date}
                  onChange={(e) => setNewAction({ ...newAction, due_date: e.target.value })}
                  className="input-field"
                  style={{ width: '100%' }}
                />
              </div>

              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px', marginTop: '10px' }}>
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="btn btn-secondary"
                >
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">
                  Save Action
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
