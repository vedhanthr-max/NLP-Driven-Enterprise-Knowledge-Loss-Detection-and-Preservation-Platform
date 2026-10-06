# Enterprise Knowledge Loss Platform — Architecture Design Document

**Document Version**: 1.0.0  
**Status**: Architectural Baseline  
**Reference Document**: `project-docs/ENHANCED_PROJECT_DOCUMENTATION.md` (Sections 10, 11, 12, 16, 23, 24)

---

## 1. System Overview & Architectural Topology

The platform adopts a decoupled **Multi-Tier Micro-Modular Architecture** structured into five discrete tiers:
1. **Client Tier**: Single Page Application (SPA) built with React.js and modern component architecture.
2. **API Gateway / Controller Tier**: FastAPI asynchronous ASGI application exposing OpenAPI 3.0 REST endpoints.
3. **Application & Domain Services Tier**: Modular domain services encapsulating business logic (Auth, Documents, Knowledge, Risk, Preservation, Search).
4. **NLP & Machine Learning Engine Tier**: Modular pipeline hosting spaCy NER, TF-IDF/TextRank keyword extractors, Sentence Transformers embedding generator, and Scikit-learn classification models.
5. **Persistence & Vector Storage Tier**: Relational schema managed via SQLAlchemy 2.0 with PostgreSQL 14+ / pgvector (with transparent SQLite + NumPy vector search fallback for local stand-alone environments).

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           PRESENTATION TIER                             │
│                  React.js Single Page Application                       │
│  ┌───────────────┬─────────────────┬────────────────┬────────────────┐  │
│  │ Auth & Users  │ Dashboard & KPI │ Document Hub   │ Knowledge Hub  │  │
│  ├───────────────┼─────────────────┼────────────────┼────────────────┤  │
│  │ Risk Studio   │ ML Analytics    │ Semantic Search│ Preservation   │  │
│  └───────────────┴─────────────────┴────────────────┴────────────────┘  │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ HTTPS / JSON REST API
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                             BACKEND TIER                                │
│                     FastAPI Application (ASGI)                          │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │ Middlewares: CORS, Request Timing, Tenant Extraction, Error Handler│  │
│  └─────────────────────────────────┬─────────────────────────────────┘  │
│                                    ▼                                    │
│  ┌───────────────┬─────────────────┬────────────────┬────────────────┐  │
│  │ /api/v1/auth  │ /api/v1/docs    │ /api/v1/know   │ /api/v1/risk   │  │
│  ├───────────────┼─────────────────┼────────────────┼────────────────┤  │
│  │ /api/v1/search│ /api/v1/preserv │ /api/v1/ml     │ /api/v1/audit  │  │
│  └───────────────┴─────────────────┴────────────────┴────────────────┘  │
│                                    │                                    │
│  ┌─────────────────────────────────┴─────────────────────────────────┐  │
│  │                         DOMAIN SERVICES                           │  │
│  │  - AuthService        - DocumentProcessor    - KnowledgeService   │  │
│  │  - RiskEngine         - PreservationEngine   - SemanticSearchSvc  │  │
│  └─────────────────────────────────┬─────────────────────────────────┘  │
└────────────────────────────────────┼────────────────────────────────────┘
                                     │
                 ┌───────────────────┴───────────────────┐
                 ▼                                       ▼
┌─────────────────────────────────┐   ┌───────────────────────────────────┐
│          NLP & ML TIER          │   │         PERSISTENCE TIER          │
│  ┌───────────────────────────┐  │   │  ┌─────────────────────────────┐  │
│  │ spaCy NER & POS Tagging   │  │   │  │ PostgreSQL 14+ / pgvector   │  │
│  ├───────────────────────────┤  │   │  │ (or SQLite + NumPy fallback)│  │
│  │ TF-IDF / TextRank Keyword │  │   │  ├─────────────────────────────┤  │
│  ├───────────────────────────┤  │   │  │ 15 Relational Tables:       │  │
│  │ SentenceTransformers 384d │  │   │  │ - organizations, users      │  │
│  ├───────────────────────────┤  │   │  │ - employees, departments    │  │
│  │ Scikit-learn Classifiers: │  │   │  │ - documents, document_chunks│  │
│  │ - Random Forest           │  │   │  │ - knowledge_items, entities │  │
│  │ - Gradient Boosting       │  │   │  │ - keywords, risk_scores     │  │
│  │ - Logistic Regression     │  │   │  │ - preservation_actions      │  │
│  └───────────────────────────┘  │   │  │ - embeddings, ml_models     │  │
└─────────────────────────────────┘   │  │ - audit_logs                │  │
                                      │  └─────────────────────────────┘  │
                                      └───────────────────────────────────┘
```

---

## 2. Core Processing Pipelines

### 2.1 Document Ingestion & NLP Pipeline
```
[File Upload: PDF/DOCX/TXT]
      │
      ▼
[Security Validation: MIME type, Extension, Size < 50MB, SHA-256 Hash]
      │
      ▼
[Text Extraction: PyMuPDF fitz / python-docx]
      │
      ▼
[Text Normalization: Encoding cleanup, whitespace trim, paragraph split]
      │
      ▼
[Sliding Token Chunking: 512 tokens with 50-token overlap]
      │
      ▼
[NLP Processing Engine: spaCy en_core_web_md]
      ├── NER: Extract PERSON, ORG, TECH, PRODUCT, GPE (confidence >= 0.5)
      ├── Keywords: TF-IDF + TextRank + POS (Noun/Adj)
      └── Topic Modeling: Clustering & Category classification
      │
      ▼
[Dense Embeddings: Sentence Transformers all-MiniLM-L6-v2 (384d, L2 Norm)]
      │
      ▼
[Atomic Database Persistence: Document + Chunks + Knowledge Item + Vectors]
```

### 2.2 Risk Detection & Classification Pipeline
```
[Knowledge Item Record + Expert & Dependency Metadata]
      │
      ▼
[5-Factor Feature Extraction]
      ├── Criticality (C)       = (Business Impact × 0.40) + (System Dep × 0.30) + (Revenue Impact × 0.30)
      ├── Uniqueness (U)        = (1 - min(num_experts, 6)/6) × 100
      ├── Dependency (D)        = min(100, (Systems × 20) + (Processes × 15) + ScopeDep)
      ├── Documentation Gap (G) = 100 - Structural Quality Score
      └── Availability Risk (A) = (Turnover × 0.50) + (Retirement × 0.30) + (Skill Transition × 0.20)
      │
      ▼
[Deterministic Scoring Engine]
      Risk Score = (C × 0.30) + (U × 0.25) + (D × 0.20) + (G × 0.15) + (A × 0.10)
      │
      ├── 0-30:   LOW
      ├── 31-60:  MEDIUM
      ├── 61-80:  HIGH
      └── 81-100: CRITICAL
      │
      ▼
[ML Inference Engine]
      Features Vector: [C, U, D, G, A, num_experts, num_systems, doc_len]
      Model: Trained Random Forest / Gradient Boosting
      Output: Predicted Risk Level + Class Probabilities
      │
      ▼
[Preservation Recommendation Trigger]
      Generates targeted mitigation actions based on leading risk drivers
```

### 2.3 Semantic Search Pipeline
```
[User Natural Language Query]
      │
      ▼
[Query Vectorization: all-MiniLM-L6-v2 -> 384-dimensional vector]
      │
      ▼
[Vector Similarity Retrieval]
      PostgreSQL: SELECT 1 - (chunk_embedding <=> query_vec) AS sim ... ORDER BY sim DESC LIMIT 10
      SQLite Dev: Cosine similarity computation via NumPy/SciPy dot-product
      │
      ▼
[Relevance Ranking & Context Assembly]
      Filters results by similarity threshold (> 0.45)
      Aggregates best chunk per parent knowledge item
      Extracts matched snippet with keyword highlighting
      │
      ▼
[JSON Response: Results + Search Time in ms]
```

---

## 3. Database Architecture & Relational Schema

### Entity Relationship Mapping
* `organizations` (1) ── (N) `users`
* `organizations` (1) ── (N) `departments`
* `organizations` (1) ── (N) `employees`
* `organizations` (1) ── (N) `documents`
* `organizations` (1) ── (N) `knowledge_items`
* `documents` (1) ── (N) `document_chunks`
* `documents` (1) ── (N) `knowledge_items`
* `knowledge_items` (1) ── (N) `entities`
* `knowledge_items` (1) ── (N) `keywords`
* `knowledge_items` (1) ── (N) `knowledge_experts`
* `knowledge_items` (1) ── (N) `risk_scores`
* `knowledge_items` (1) ── (N) `preservation_actions`
* `knowledge_items` (1) ── (N) `embeddings`
* `document_chunks` (1) ── (N) `embeddings`
* `organizations` (1) ── (N) `audit_logs`
* `organizations` (1) ── (N) `ml_models`

---

## 4. Multi-Tenancy & Security Architecture

1. **Tenant Scoping**: Every database entity (excluding system constants) contains a mandatory `organization_id` foreign key. All repository queries require and filter on `organization_id`.
2. **Authentication Flow**:
   - Client sends credentials to `/api/v1/auth/login`.
   - Backend validates password with bcrypt (12 rounds).
   - Backend issues signed JWT containing `sub` (user_id), `org_id` (organization_id), and `role` (admin/manager/employee).
   - Client attaches JWT in `Authorization: Bearer <token>` on all requests.
   - FastApi dependency `get_current_active_user` extracts and validates the tenant context for every request.
3. **Role Authorization Matrix**:
   - `admin`: Full administrative control, organization settings, user role elevation, model management, audit log inspection.
   - `manager`: Document upload, risk assessment triggering, preservation action creation & assignment, analytics viewing.
   - `employee`: Knowledge search and browsing, document submission, personal preservation task updates.

---

## 5. Directory & Module Organization

```
d:/Final year project/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   │   ├── auth.py
│   │   │   │   ├── documents.py
│   │   │   │   ├── knowledge.py
│   │   │   │   ├── risk.py
│   │   │   │   ├── search.py
│   │   │   │   ├── preservation.py
│   │   │   │   ├── ml.py
│   │   │   │   └── audit.py
│   │   │   └── router.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   ├── database.py
│   │   │   └── exceptions.py
│   │   ├── models/
│   │   │   └── entities.py
│   │   ├── schemas/
│   │   │   ├── auth.py
│   │   │   ├── documents.py
│   │   │   ├── knowledge.py
│   │   │   ├── risk.py
│   │   │   ├── preservation.py
│   │   │   └── search.py
│   │   ├── services/
│   │   │   ├── auth_service.py
│   │   │   ├── document_service.py
│   │   │   ├── knowledge_service.py
│   │   │   ├── risk_service.py
│   │   │   ├── preservation_service.py
│   │   │   └── search_service.py
│   │   ├── nlp/
│   │   │   ├── preprocessor.py
│   │   │   ├── ner.py
│   │   │   ├── keywords.py
│   │   │   ├── topic_extractor.py
│   │   │   └── embeddings.py
│   │   ├── ml/
│   │   │   ├── feature_engineering.py
│   │   │   ├── trainer.py
│   │   │   ├── evaluator.py
│   │   │   ├── models/
│   │   │   └── classifier.py
│   │   └── main.py
│   ├── tests/
│   │   ├── test_auth.py
│   │   ├── test_documents.py
│   │   ├── test_nlp.py
│   │   ├── test_risk.py
│   │   ├── test_ml.py
│   │   ├── test_search.py
│   │   └── test_preservation.py
│   ├── requirements.txt
│   └── seed_data.py
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   │   ├── Login.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Documents.jsx
│   │   │   ├── KnowledgeCatalog.jsx
│   │   │   ├── KnowledgeDetail.jsx
│   │   │   ├── RiskStudio.jsx
│   │   │   ├── MLAnalytics.jsx
│   │   │   ├── SemanticSearch.jsx
│   │   │   ├── PreservationBoard.jsx
│   │   │   ├── Employees.jsx
│   │   │   └── AuditLogs.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
└── docs/
    ├── requirements.md
    ├── implementation-plan.md
    ├── feature-matrix.md
    ├── architecture.md
    ├── assumptions.md
    └── development-progress.md
```
