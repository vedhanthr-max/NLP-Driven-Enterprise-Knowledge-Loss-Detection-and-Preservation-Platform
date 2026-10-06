# System Requirements Specification (SRS)

## NLP-Driven SaaS Platform for Enterprise Knowledge Loss Detection and Preservation

**Document Version**: 1.0.0  
**Status**: Approved Specification  
**Reference Document**: `project-docs/ENHANCED_PROJECT_DOCUMENTATION.md`

---

## 1. Executive Overview & Purpose

The **NLP-Driven SaaS Platform for Enterprise Knowledge Loss Detection and Preservation** is designed to mitigate enterprise vulnerability caused by employee departures, retirements, and siloed expertise. The platform systematically extracts organizational knowledge from enterprise documents (PDF, DOCX, TXT), structures that knowledge via an NLP pipeline, quantifies knowledge loss risk using a deterministic 5-factor scoring model and a multi-class Machine Learning classification engine, generates actionable preservation strategies, and provides vector-based semantic search.

---

## 2. Functional Requirements (FR)

### FR-1: Authentication, Authorization & Multi-Tenancy
* **FR-1.1**: User registration with email, password, full name, organization name, and organization size.
* **FR-1.2**: Secure authentication using JSON Web Tokens (JWT) with PyJWT and bcrypt (12 rounds) password hashing.
* **FR-1.3**: Role-Based Access Control (RBAC) with three distinct roles:
  * `admin`: Complete organization administration, user management, audit log access, ML model lifecycle management.
  * `manager`: Document uploads, risk assessment triggering, preservation action assignments, report access.
  * `employee`: Knowledge exploration, assigned preservation task execution, document submission, personal expertise management.
* **FR-1.4**: Strict multi-tenant data isolation guaranteeing that all database queries, uploads, knowledge items, and risk analyses are strictly isolated by `organization_id`.
* **FR-1.5**: Audit logging of all security events, authentication attempts, document access, and modifications.

### FR-2: Document Ingestion & Preprocessing
* **FR-2.1**: Support upload of PDF (`.pdf`), Microsoft Word (`.docx`), Plain Text (`.txt`), and Markdown (`.md`).
* **FR-2.2**: Strict file validation: maximum file size 50 MB, MIME-type verification, safe filename sanitization, and SHA-256 deduplication hashing.
* **FR-2.3**: Text extraction using PyMuPDF (`fitz`) for PDF and `python-docx` for DOCX files.
* **FR-2.4**: Document metadata extraction: title, page count, word count, author, and timestamp.
* **FR-2.5**: Text cleaning: whitespace normalization, character encoding repair, punctuation handling, and line-break normalization.
* **FR-2.6**: Chunking strategy: split documents into sliding chunks of 512 tokens with 50 tokens of overlap, preserving sentence boundaries and metadata.

### FR-3: NLP Processing Engine
* **FR-3.1**: Text Preprocessing: lowercasing, tokenization, stopword removal, lemmatization, and POS tagging via spaCy (`en_core_web_md` / fallback `en_core_web_sm`).
* **FR-3.2**: Named Entity Recognition (NER): extraction of PERSON, ORGANIZATION, TECHNOLOGY, PRODUCT, GPE, DATE, EVENT, and PROCESS entities with confidence scoring (threshold >= 0.5) and regex pattern matching for technical domains.
* **FR-3.3**: Keyword Extraction: hybrid extraction combining TF-IDF scoring, TextRank graph centrality, and noun/adjective part-of-speech filtering.
* **FR-3.4**: Topic Modeling: automated identification of dominant technical/business topics (Cloud Infrastructure, Database Administration, DevOps, Security, Application Development).
* **FR-3.5**: Vector Embeddings: generation of 384-dimensional dense semantic vectors using Sentence Transformers (`all-MiniLM-L6-v2`) with L2 normalization.

### FR-4: Knowledge Management & Centralized Repository
* **FR-4.1**: Structured knowledge record generation linked to source documents, chunks, extracted entities, keywords, and topics.
* **FR-4.2**: Knowledge metadata management: category, tags, status (`draft`, `active`, `archived`, `obsolete`), verification flag, and access tracking.
* **FR-4.3**: Expert identification and mapping: link extracted personnel entities to registered organization employees with confidence scores and primary/secondary designations.
* **FR-4.4**: CRUD operations for knowledge records with audit logging and cascading dependencies.

### FR-5: Knowledge Loss Risk Detection (Core Algorithm)
* **FR-5.1**: Evaluate knowledge vulnerability using five normalized factors (0 to 100 scale):
  1. **Knowledge Criticality ($C$) - Weight: 30% ($0.30$)**:
     $$C = (\text{Business Impact} \times 0.40) + (\text{System Dependencies} \times 0.30) + (\text{Revenue Impact} \times 0.30)$$
  2. **Knowledge Uniqueness ($U$) - Weight: 25% ($0.25$)**:
     $$U = \left(1 - \frac{\min(N_{\text{experts}}, 6)}{6}\right) \times 100$$
     *(Discrete scale: 1 expert $\to 95$, 2 experts $\to 75$, 3 experts $\to 60$, 4-5 experts $\to 45$, 6+ experts $\to 20$)*
  3. **Organizational Dependency ($D$) - Weight: 20% ($0.20$)**:
     $$D = \min(100, (N_{\text{systems}} \times 20) + (N_{\text{processes}} \times 15) + \text{BusinessUnitDep})$$
     *(Company $\to 100$, Multi-Dept $\to 80$, Single-Dept $\to 50$, Team $\to 30$)*
  4. **Documentation Gap ($G$) - Weight: 15% ($0.15$)**:
     $$G = 100 - \text{Quality Score}$$
     *(Quality Score evaluated on introduction, prerequisites, step-by-step procedures, examples, troubleshooting, contact info, update recency)*
  5. **Expert Availability Risk ($A$) - Weight: 10% ($0.10$)**:
     $$A = (\text{Turnover Risk} \times 0.50) + (\text{Retirement/Age Risk} \times 0.30) + (\text{Skill Transition Risk} \times 0.20)$$
* **FR-5.2**: Composite Risk Calculation:
  $$\text{RISK SCORE} = (C \times 0.30) + (U \times 0.25) + (D \times 0.20) + (G \times 0.15) + (A \times 0.10)$$
* **FR-5.3**: Deterministic Risk Level Classification:
  * `0.00` – `30.00`: **LOW** (Green)
  * `30.01` – `60.00`: **MEDIUM** (Yellow)
  * `60.01` – `80.00`: **HIGH** (Orange)
  * `80.01` – `100.00`: **CRITICAL** (Red)
* **FR-5.4**: Detailed explainability engine generating human-readable contributing factor breakdowns and mitigation priority alerts.

### FR-6: Machine Learning Risk Classification
* **FR-6.1**: Supervised multi-class classification pipeline predicting risk level (`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`).
* **FR-6.2**: Feature engineering pipeline processing the 5 risk factors plus auxiliary features (expert count, system count, documentation length).
* **FR-6.3**: Implementation, training, cross-validation (5-fold), and comparative benchmarking of:
  1. Random Forest Classifier (`n_estimators=100`, `max_depth=10`, `class_weight='balanced'`)
  2. Gradient Boosting / XGBoost Classifier (`n_estimators=100`, `max_depth=6`, `learning_rate=0.1`)
  3. Multinomial Logistic Regression (`solver='lbfgs'`, `max_iter=1000`)
* **FR-6.4**: Real metrics computation on unseen test set: Accuracy, Precision, Recall, Macro F1-score, and Confusion Matrix. Target: Accuracy $\ge 80\%$, Critical Recall $\ge 90\%$, Macro F1 $\ge 0.75$.
* **FR-6.5**: Model persistence (`joblib`/pickle) and model registry metadata tracking in database.

### FR-7: Semantic Search Engine
* **FR-7.1**: Natural language query input (e.g., "How do I troubleshoot legacy payment database connections?").
* **FR-7.2**: Real-time query encoding using Sentence Transformers `all-MiniLM-L6-v2`.
* **FR-7.3**: Vector similarity ranking against stored document chunk embeddings (Cosine Similarity / Cosine Distance).
* **FR-7.4**: pgvector `<=>` index integration for PostgreSQL with fallback in-memory Cosine search for local SQLite dev environment.
* **FR-7.5**: Result highlighting with relevance score ($0.0 - 1.0$), matched chunk snippet, and link to parent knowledge item.

### FR-8: Knowledge Preservation Engine
* **FR-8.1**: Automated recommendation generation triggered by risk thresholds:
  * Uniqueness $> 75 \implies$ "Assign secondary expert" & "Schedule knowledge transfer sessions"
  * Documentation Gap $> 50 \implies$ "Draft technical runbook" & "Record video walkthroughs"
  * Criticality $> 70 \implies$ "Establish disaster recovery failover"
* **FR-8.2**: Action item lifecycle management: `recommended` $\to$ `planned` $\to$ `in_progress` $\to$ `completed` / `cancelled`.
* **FR-8.3**: Task assignment to users, deadline tracking, estimated hours vs actual hours tracking.

### FR-9: Interactive Web Frontend (React.js)
* **FR-9.1**: Responsive modern dashboard featuring KPI cards, risk distribution charts, critical alerts, and recent activities.
* **FR-9.2**: Document upload portal with drag-and-drop, upload status, chunk preview, and NLP extraction review.
* **FR-9.3**: Knowledge catalog with multifaceted filtering (category, risk level, status, tags) and search.
* **FR-9.4**: Knowledge detail page displaying structured metadata, extracted entities, identified experts, and risk breakdown.
* **FR-9.5**: Interactive Risk Assessment Calculator with real-time sliders and instant factor recalculation.
* **FR-9.6**: Semantic search page with instantaneous vector ranking and snippet visualization.
* **FR-9.7**: Preservation action management board for assigning and updating mitigation tasks.
* **FR-9.8**: ML model analytics dashboard displaying real accuracy, confusion matrix, and feature importances.
* **FR-9.9**: User management and audit log viewer.

---

## 3. Non-Functional Requirements (NFR)

### NFR-1: Performance & Latency
* **NFR-1.1**: API response time ($p95$) $< 500\text{ ms}$ for standard CRUD endpoints.
* **NFR-1.2**: Semantic search latency $< 200\text{ ms}$ for top-10 retrieval.
* **NFR-1.3**: Document processing throughput $< 30\text{ s}$ for a 20-page document.

### NFR-2: Security & Privacy
* **NFR-2.1**: Passwords hashed using bcrypt with salt work factor 12.
* **NFR-2.2**: Bearer token authentication via JWT with expiration and signature verification.
* **NFR-2.3**: Input validation and sanitization using Pydantic models to prevent injection and malformed payloads.
* **NFR-2.4**: Safe file storage preventing path traversal (`os.path.basename` enforcement).
* **NFR-2.5**: Secure HTTP response headers and CORS origin restrictions.

### NFR-3: Reliability & Data Integrity
* **NFR-3.1**: Foreign key constraints, unique constraints, and check constraints enforced at database layer.
* **NFR-3.2**: Transactional atomicity: document upload, extraction, and chunk storage wrapped in database transactions.
* **NFR-3.3**: Graceful degradation: in the absence of pgvector or PostgreSQL, the application seamlessly defaults to SQLite with NumPy vector similarity without crash.

### NFR-4: Usability & Accessibility
* **NFR-4.1**: WCAG 2.1 Level AA compliant color contrast and semantic HTML elements.
* **NFR-4.2**: Intuitive status indicators with color-coded risk levels (Green, Yellow, Orange, Red).
* **NFR-4.3**: Informative error messages mapped to the `ERR-MODULE-XXX` standard.

---

## 4. Error Code Specification

| Category | Code | Description | HTTP Status |
|---|---|---|---|
| Auth | `ERR-AUTH-001` | Email already registered | 400 |
| Auth | `ERR-AUTH-002` | Invalid credentials | 401 |
| Auth | `ERR-AUTH-005` | Token expired | 401 |
| Auth | `ERR-AUTH-006` | Invalid token | 401 |
| Doc | `ERR-DOC-001` | Document not found | 404 |
| Doc | `ERR-DOC-002` | Invalid file format | 400 |
| Doc | `ERR-DOC-003` | File too large (>50MB) | 413 |
| Doc | `ERR-DOC-004` | Document processing failed | 500 |
| Knowledge | `ERR-KNOW-001` | Knowledge item not found | 404 |
| Knowledge | `ERR-KNOW-002` | Invalid knowledge data | 422 |
| Risk | `ERR-RISK-001` | Risk calculation failed | 500 |
| Risk | `ERR-RISK-003` | Invalid risk factors (must be 0-100) | 400 |
| Search | `ERR-SEARCH-001` | Empty or invalid search query | 400 |
| Perm | `ERR-PERM-001` | Insufficient permissions for action | 403 |
