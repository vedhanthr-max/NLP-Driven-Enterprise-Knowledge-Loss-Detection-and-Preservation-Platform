import React, { useState, useEffect } from 'react';
import { documentAPI } from '../services/api';
import { UploadCloud, FileText, CheckCircle, AlertCircle, RefreshCw, Eye, Trash2, X } from 'lucide-react';

export default function Documents({ onNavigateToKnowledge }) {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);
  const [successMsg, setSuccessMsg] = useState(null);

  // Form states
  const [selectedFile, setSelectedFile] = useState(null);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');

  // Inspection modal
  const [inspectDoc, setInspectDoc] = useState(null);
  const [inspectLoading, setInspectLoading] = useState(false);

  const fetchDocuments = async () => {
    setLoading(true);
    try {
      const res = await documentAPI.getAll();
      setDocuments(res.data.documents || []);
    } catch (err) {
      setError('Failed to fetch document repository.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
      if (!title) {
        setTitle(file.name.replace(/\.[^/.]+$/, ''));
      }
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!selectedFile) {
      setError('Please select a file to upload (PDF, DOCX, TXT).');
      return;
    }

    setUploading(true);
    setError(null);
    setSuccessMsg(null);

    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('title', title);
    if (description) formData.append('description', description);

    try {
      const res = await documentAPI.upload(formData);
      setSuccessMsg(`Successfully uploaded and indexed "${res.data.title}"! Extracted ${res.data.chunks_created} chunks and ${res.data.entities_extracted} entities.`);
      setSelectedFile(null);
      setTitle('');
      setDescription('');
      fetchDocuments();
    } catch (err) {
      const msg = err.response?.data?.message || err.response?.data?.detail?.message || 'Document processing failed.';
      setError(msg);
    } finally {
      setUploading(false);
    }
  };

  const handleInspect = async (docId) => {
    setInspectLoading(true);
    try {
      const res = await documentAPI.getDetails(docId);
      setInspectDoc(res.data);
    } catch (err) {
      alert('Failed to load document chunks');
    } finally {
      setInspectLoading(false);
    }
  };

  return (
    <div>
      <div style={{ marginBottom: '24px' }}>
        <h2 style={{ fontSize: '1.75rem', fontWeight: '800', letterSpacing: '-0.02em', marginBottom: '4px' }}>
          Document Ingestion & Text Processing Hub
        </h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
          Upload PDF, DOCX, or TXT documents for PyMuPDF text extraction, 512-token sliding chunking, and spaCy NER indexing.
        </p>
      </div>

      {/* Upload Box Card */}
      <div className="glass-card" style={{ padding: '24px', marginBottom: '32px' }}>
        <h3 style={{ fontSize: '1.1rem', fontWeight: '700', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <UploadCloud size={20} color="var(--accent-primary)" />
          Ingest New Enterprise Document
        </h3>

        {error && (
          <div style={{
            background: 'var(--risk-critical-bg)', border: '1px solid rgba(239, 68, 68, 0.3)',
            borderRadius: 'var(--radius-md)', padding: '12px', color: '#fca5a5',
            fontSize: '0.85rem', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px'
          }}>
            <AlertCircle size={16} />
            <div>{error}</div>
          </div>
        )}

        {successMsg && (
          <div style={{
            background: 'var(--risk-low-bg)', border: '1px solid rgba(16, 185, 129, 0.3)',
            borderRadius: 'var(--radius-md)', padding: '12px', color: '#6ee7b7',
            fontSize: '0.85rem', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px'
          }}>
            <CheckCircle size={16} />
            <div>{successMsg}</div>
          </div>
        )}

        <form onSubmit={handleUpload}>
          <div style={{ display: 'grid', gridTemplateColumns: '1.5fr 1fr 1fr', gap: '16px', marginBottom: '16px' }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: '600', color: 'var(--text-secondary)', marginBottom: '6px' }}>
                Select File (PDF, DOCX, TXT, MD - Max 50MB)
              </label>
              <input
                type="file"
                accept=".pdf,.docx,.txt,.md"
                onChange={handleFileChange}
                className="input"
                style={{ padding: '7px 12px' }}
              />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: '600', color: 'var(--text-secondary)', marginBottom: '6px' }}>
                Document Title
              </label>
              <input
                type="text"
                required
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="e.g. AWS Migration Runbook"
                className="input"
              />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: '600', color: 'var(--text-secondary)', marginBottom: '6px' }}>
                Description (Optional)
              </label>
              <input
                type="text"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Operational context..."
                className="input"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={uploading || !selectedFile}
            className="btn btn-primary"
            style={{ padding: '10px 20px' }}
          >
            {uploading ? (
              <><RefreshCw size={16} className="animate-spin" /> Processing & Extracting NLP...</>
            ) : (
              <><UploadCloud size={16} /> Process & Index Document</>
            )}
          </button>
        </form>
      </div>

      {/* Documents Repository Table */}
      <div className="glass-card" style={{ padding: '24px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '18px' }}>
          <h3 style={{ fontSize: '1.15rem', fontWeight: '700' }}>Ingested Documents Repository</h3>
          <button onClick={fetchDocuments} className="btn btn-secondary" style={{ fontSize: '0.8rem' }}>
            <RefreshCw size={14} /> Refresh
          </button>
        </div>

        {loading ? (
          <div style={{ textAlign: 'center', padding: '30px', color: 'var(--text-muted)' }}>Loading documents...</div>
        ) : documents.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '40px', color: 'var(--text-muted)' }}>
            <FileText size={40} style={{ opacity: 0.3, marginBottom: '10px' }} />
            <div>No documents uploaded yet. Upload a sample document above to test text extraction.</div>
          </div>
        ) : (
          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.88rem' }}>
              <thead>
                <tr style={{ borderBottom: '1px solid var(--border-subtle)', color: 'var(--text-muted)' }}>
                  <th style={{ padding: '12px 14px' }}>TITLE / FILE</th>
                  <th style={{ padding: '12px 14px' }}>FORMAT</th>
                  <th style={{ padding: '12px 14px' }}>SIZE</th>
                  <th style={{ padding: '12px 14px' }}>PAGES</th>
                  <th style={{ padding: '12px 14px' }}>CHUNKS</th>
                  <th style={{ padding: '12px 14px' }}>STATUS</th>
                  <th style={{ padding: '12px 14px', textAlign: 'right' }}>ACTIONS</th>
                </tr>
              </thead>
              <tbody>
                {documents.map((doc) => (
                  <tr key={doc.document_id} style={{ borderBottom: '1px solid var(--border-subtle)' }}>
                    <td style={{ padding: '14px', fontWeight: '600' }}>
                      <div style={{ color: 'var(--text-primary)' }}>{doc.title}</div>
                      <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{doc.file_name}</div>
                    </td>
                    <td style={{ padding: '14px' }}>
                      <span style={{ textTransform: 'uppercase', padding: '3px 8px', borderRadius: '4px', background: '#1e293b', fontSize: '0.75rem', fontWeight: '700' }}>
                        {doc.file_type}
                      </span>
                    </td>
                    <td style={{ padding: '14px', color: 'var(--text-secondary)' }}>
                      {(doc.file_size / 1024).toFixed(1)} KB
                    </td>
                    <td style={{ padding: '14px', color: 'var(--text-secondary)' }}>
                      {doc.pages}
                    </td>
                    <td style={{ padding: '14px' }}>
                      <span style={{ padding: '2px 8px', borderRadius: '6px', background: 'rgba(99, 102, 241, 0.12)', color: 'var(--accent-primary)', fontWeight: '600' }}>
                        {doc.chunks_count} chunks
                      </span>
                    </td>
                    <td style={{ padding: '14px' }}>
                      <span className="badge badge-low">
                        <CheckCircle size={12} /> {doc.status}
                      </span>
                    </td>
                    <td style={{ padding: '14px', textAlign: 'right' }}>
                      <button
                        onClick={() => handleInspect(doc.document_id)}
                        className="btn btn-secondary"
                        style={{ padding: '5px 12px', fontSize: '0.8rem' }}
                      >
                        <Eye size={14} /> Chunks & NLP
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Chunks & Extraction Inspector Modal */}
      {inspectDoc && (
        <div style={{
          position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
          background: 'rgba(0, 0, 0, 0.75)', backdropFilter: 'blur(6px)',
          display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 100, padding: '20px'
        }}>
          <div className="glass-card" style={{ width: '100%', maxWidth: '800px', maxHeight: '85vh', display: 'flex', flexDirection: 'column', padding: '28px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px', borderBottom: '1px solid var(--border-subtle)', paddingBottom: '12px' }}>
              <div>
                <h3 style={{ fontSize: '1.2rem', fontWeight: '700' }}>{inspectDoc.title}</h3>
                <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                  {inspectDoc.chunks_created} Chunks • {inspectDoc.entities_extracted} Entities Extracted • {inspectDoc.keywords_extracted} Keywords
                </div>
              </div>
              <button
                onClick={() => setInspectDoc(null)}
                style={{ background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}
              >
                <X size={22} />
              </button>
            </div>

            <div style={{ overflowY: 'auto', flex: 1, display: 'flex', flexDirection: 'column', gap: '14px', paddingRight: '6px' }}>
              <div style={{ fontSize: '0.85rem', fontWeight: '700', color: 'var(--accent-primary)', textTransform: 'uppercase' }}>
                Extracted 512-Token Sliding Chunks:
              </div>
              {inspectDoc.chunks.map((c) => (
                <div key={c.chunk_id} style={{ background: '#0a0d14', border: '1px solid var(--border-subtle)', borderRadius: 'var(--radius-md)', padding: '14px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '6px' }}>
                    <span>CHUNK #{c.chunk_index + 1}</span>
                    <span>{c.token_count} TOKENS • PAGE {c.page_number}</span>
                  </div>
                  <div style={{ fontSize: '0.85rem', color: 'var(--text-primary)', whiteHeight: 1.6 }}>
                    {c.chunk_text}
                  </div>
                </div>
              ))}
            </div>

            <div style={{ marginTop: '16px', paddingTop: '14px', borderTop: '1px solid var(--border-subtle)', textAlign: 'right' }}>
              <button onClick={() => setInspectDoc(null)} className="btn btn-secondary">
                Close Inspector
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
