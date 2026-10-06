# Architectural Assumptions & Conflict Resolution Record

**Document Version**: 1.0.0  
**Project**: NLP-Driven SaaS Platform for Enterprise Knowledge Loss Detection and Preservation  
**Classification**: Architectural Decision Record (ADR)

---

## 1. Context & Purpose

In accordance with Section 2 and Section 6 of the project directives, this document records all identified ambiguities, conflicting specifications, environment adaptations, and architectural decisions made when synthesizing `project-docs/ENHANCED_PROJECT_DOCUMENTATION.md`, `project-docs/gap_analysis.md`, and `project-docs/IMPROVEMENTS_SUMMARY.md`.

---

## 2. Technical Decisions & Conflict Resolutions

### ADR-01: Database Engine & Vector Storage Strategy
* **Source Conflict / Environmental Constraint**:
  * `ENHANCED_PROJECT_DOCUMENTATION.md` specifies PostgreSQL 14+ with pgvector 0.5+ as the primary database.
  * The current execution environment is a local Windows developer machine without an active PostgreSQL service or Docker engine installed.
* **Resolution**:
  * The database layer is architected using SQLAlchemy 2.0 with dynamic dialect switching:
    1. **Production / PostgreSQL Mode**: When `DATABASE_URL` starts with `postgresql`, the application uses native PostgreSQL tables and pgvector (`vector(384)`) with IVFFlat cosine similarity indexing (`vector_cosine_ops`).
    2. **Local Standalone / Development Mode**: When `DATABASE_URL` is SQLite (or PostgreSQL is unreachable), the application defaults to `sqlite:///./knowledge_loss.db`. In this mode, embeddings are stored as JSON/binary float arrays, and vector similarity search is performed using high-performance NumPy/SciPy dot-product cosine similarity.
* **Rationale**: Guarantees that the complete application runs, tests, and demonstrates cleanly on any developer workstation without external service dependencies, while remaining 100% production-compatible with PostgreSQL and pgvector.

---

### ADR-02: Deterministic Risk Weights & Threshold Standard
* **Documentation Review**:
  * In Section 13 of `ENHANCED_PROJECT_DOCUMENTATION.md`:
    * Criticality Weight: $0.30$ (30%)
    * Uniqueness Weight: $0.25$ (25%)
    * Dependency Weight: $0.20$ (20%)
    * Documentation Gap Weight: $0.15$ (15%)
    * Availability Risk Weight: $0.10$ (10%)
    * Sum: $0.30 + 0.25 + 0.20 + 0.15 + 0.10 = 1.00$ (100%)
  * Classification Thresholds:
    * `0` – `30`: **LOW**
    * `31` – `60`: **MEDIUM**
    * `61` – `80`: **HIGH**
    * `81` – `100`: **CRITICAL**
* **Resolution**: The exact mathematical formula and thresholds from Section 13 are adopted across both the backend calculation service, the ML feature pipeline, and the frontend interactive studio. No deviating weights or arbitrary scaling factors shall be introduced.

---

### ADR-03: NLP Model Fallback & Offline Resilience
* **Documentation Review**:
  * `ENHANCED_PROJECT_DOCUMENTATION.md` specifies spaCy `en_core_web_md` and Sentence Transformers `all-MiniLM-L6-v2`.
* **Resolution**:
  * The NLP service attempts to load `en_core_web_md`. If unavailable, it falls back to `en_core_web_sm`. If spaCy models are not yet downloaded in the local environment, it utilizes an internal regex-driven rule-based entity recognizer (with the exact same entity taxonomy: PERSON, ORG, TECH, PRODUCT, GPE, DATE, PROCESS) so tests and offline runs never crash.
  * The embedding service attempts to load `all-MiniLM-L6-v2` from SentenceTransformers. If network connectivity limits the initial HuggingFace model download, a deterministic 384-dimensional dense projection embedder is provided as a zero-downtime fallback.

---

### ADR-04: Machine Learning Workflow & Metric Integrity
* **Documentation Review**:
  * ML component requires training, cross-validation, and evaluation across three algorithms: Random Forest, Gradient Boosting, and Logistic Regression.
  * Prohibition against fabricated metrics: "Calculate actual Accuracy, Precision, Recall, F1-score, Confusion Matrix. Never fabricate metrics."
* **Resolution**:
  * A dedicated synthetic dataset generator creates 600+ realistic enterprise knowledge loss scenarios based on the domain parameters described in Section 31 (e.g., legacy payment gateways, cloud migrations, database runbooks).
  * A true train/test split (70% train, 15% validation, 15% test) is executed.
  * The three models are trained, evaluated using Scikit-learn metrics (`accuracy_score`, `precision_recall_fscore_support`, `confusion_matrix`), and the top performing model is saved to disk (`app/ml/models/risk_classifier.pkl`) and registered in the `ml_models` database table with its real empirical scores.

---

### ADR-05: Frontend Build & UI Architecture
* **Documentation Review**:
  * Frontend specified as React.js.
  * System currently has Node.js v24.19.0 and npm 11.17.0 installed.
* **Resolution**:
  * Frontend is initialized using Vite + React.
  * The user interface will feature an executive SaaS design system: modern typography (Inter/Outfit), clean card layouts, crisp data density, interactive risk factor sliders, dynamic SVG/Canvas charts, and color-coded risk indicators adhering to WCAG 2.1 AA standards.
  * In PowerShell on Windows, `npm.cmd` will be used to invoke npm commands to prevent execution policy errors with `npm.ps1`.
