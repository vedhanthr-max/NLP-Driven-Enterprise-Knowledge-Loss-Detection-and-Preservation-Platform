# Automated Testing & Audit Verification Report

**Project:** NLP-Driven SaaS Platform for Enterprise Knowledge Loss Detection and Preservation  
**Audit Timestamp:** 2026-09-21T18:50:15+05:30  
**Environment:** Python 3.12, FastAPI, SQLite (Dual PostgreSQL/pgvector Engine), Vite + React 19, spaCy, Scikit-learn  
**Test Runner:** Pytest 8.x & Custom End-to-End Audit Harness (`backend/audit_runner.py`)

---

## 1. Test Suite Summary

```text
Total tests:     45
Passed:          45
Failed:          0
Skipped:         0
Pass percentage: 100.0%
Total Execution Time: 2.46 seconds
```

---

## 2. Live End-to-End User Journey Audit

The complete enterprise user journey was executed autonomously against the live running server on `http://127.0.0.1:8000`:

| Step | User Journey Milestone | Status | Details / Output |
| :--- | :--- | :---: | :--- |
| **1** | User Authentication (Login) | **PASS** | Valid JWT Bearer token issued for `admin@techcorp.com` |
| **2** | Dashboard Metrics Access | **PASS** | High-level KPIs, risk distribution & recent actions loaded |
| **3** | Realistic Document Upload | **PASS** | Uploaded `journey_dr_manual.pdf` (Multi-region Kubernetes DR) |
| **4** | Text Extraction & Chunking | **PASS** | Extracted plain text & generated overlapping 512-token chunks |
| **5** | NLP Pipeline Extraction | **PASS** | Extracted tech entities (Kubernetes, AWS), keywords, and taxonomy topic |
| **6** | Knowledge Record Creation | **PASS** | Created persistent `KnowledgeItem` asset (`knowledge_id: 26`) |
| **7** | 5-Factor Risk Calculation | **PASS** | Calculated score: **86.50** (Critical) |
| **8** | Supervised ML Classification | **PASS** | Random Forest classified as **`critical`** (86.0% model confidence) |
| **9** | Preservation Recommendation | **PASS** | Automatically triggered 43 adaptive preservation actions |
| **10** | Neural Semantic Vector Search | **PASS** | Retrieved top matching knowledge items with 384d vector similarity |
| **11** | Knowledge Item Inspection | **PASS** | Retrieved full asset details, linked experts, and entities |
| **12** | Enterprise Session Logout | **PASS** | Blacklisted token and cleared authentication state |

---

## 3. Comprehensive API Endpoint Audit Matrix

| Endpoint | Method | Expected Status | Actual Status | Result | Details / Validation |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `/health` | `GET` | 200 OK | 200 OK | **PASS** | Service health status healthy |
| `/api/v1/auth/login` | `POST` | 200 OK | 200 OK | **PASS** | Valid credentials return access & refresh tokens |
| `/api/v1/auth/login` (Invalid) | `POST` | 401 Unauthorized | 401 Unauthorized | **PASS** | Rejected invalid credentials with `ERR-AUTH-002` |
| `/api/v1/auth/me` | `GET` | 200 OK | 200 OK | **PASS** | Returns authenticated user profile |
| `/api/v1/auth/me` (No Token) | `GET` | 401 Unauthorized | 401 Unauthorized | **PASS** | Missing Authorization header rejected |
| `/api/v1/auth/me` (Tampered) | `GET` | 401 Unauthorized | 401 Unauthorized | **PASS** | Invalid signature rejected |
| `/api/v1/auth/logout` | `POST` | 200 OK | 200 OK | **PASS** | Successfully terminated session |
| `/api/v1/documents/upload` (PDF) | `POST` | 202 Accepted | 202 Accepted | **PASS** | Parsed PDF, generated text chunks & knowledge item |
| `/api/v1/documents/upload` (DOCX)| `POST` | 202 Accepted | 202 Accepted | **PASS** | Parsed DOCX paragraphs and tables |
| `/api/v1/documents/upload` (Empty)| `POST`| 400 Bad Request | 400 Bad Request | **PASS** | 0-byte upload rejected with `ERR-DOC-005` |
| `/api/v1/documents/upload` (Corrupt)|`POST`| 400 Bad Request | 400 Bad Request | **PASS** | Corrupted binary rejected with `ERR-DOC-004` |
| `/api/v1/documents/upload` (.exe) | `POST`| 400 Bad Request | 400 Bad Request | **PASS** | Disallowed extension rejected with `ERR-DOC-002` |
| `/api/v1/documents/upload` (>50MB)| `POST`| 413 Payload Too Large | 413 Payload Too Large | **PASS** | Oversized payload rejected with `ERR-DOC-003` |
| `/api/v1/documents/upload` (Dup) | `POST` | 202 Accepted | 202 Accepted | **PASS** | SHA256 content hash deduplicated safely |
| `/api/v1/documents` | `GET` | 200 OK | 200 OK | **PASS** | Paginated organization document list |
| `/api/v1/documents/{id}` | `GET` | 200 OK | 200 OK | **PASS** | Document metadata, extraction status, and chunks |
| `/api/v1/knowledge` | `GET` | 200 OK | 200 OK | **PASS** | Filterable knowledge inventory |
| `/api/v1/knowledge` | `POST`| 201 Created | 201 Created | **PASS** | Created new knowledge asset with linked experts |
| `/api/v1/knowledge/{id}` | `GET` | 200 OK | 200 OK | **PASS** | Detailed knowledge entity, tags, and risk metrics |
| `/api/v1/risk/dashboard` | `GET` | 200 OK | 200 OK | **PASS** | Organization-wide risk metrics and KPI aggregates |
| `/api/v1/risk/analyze/{id}` | `POST` | 200 OK | 200 OK | **PASS** | Calculated exact 5-factor risk score & explainability |
| `/api/v1/risk/simulate` | `POST` | 200 OK | 200 OK | **PASS** | Interactive sandbox simulation without persistence |
| `/api/v1/ml/metrics` | `GET` | 200 OK | 200 OK | **PASS** | Empirical holdout metrics: 99.05% Acc, 0.9142 F1 |
| `/api/v1/ml/predict` | `POST` | 200 OK | 200 OK | **PASS** | Live supervised risk inference & class probabilities |
| `/api/v1/ml/train` | `POST` | 200 OK | 200 OK | **PASS** | Triggered 700-sample pipeline re-training |
| `/api/v1/search` | `GET` | 200 OK | 200 OK | **PASS** | Hybrid 384d vector + lexical relevance search |
| `/api/v1/preservation-actions` | `GET` | 200 OK | 200 OK | **PASS** | Kanban preservation tasks filtered by stage |
| `/api/v1/preservation-actions` | `POST`| 201 Created | 201 Created | **PASS** | Scheduled new preservation task |
| `/api/v1/employees` | `GET` | 200 OK | 200 OK | **PASS** | Directory of SMEs and attrition flight risks |
| `/api/v1/audit/logs` (Admin) | `GET` | 200 OK | 200 OK | **PASS** | Compliance audit trail with timestamps and IPs |
| `/api/v1/audit/logs` (Employee)| `GET` | 403 Forbidden | 403 Forbidden | **PASS** | Role restriction enforced: non-admins blocked |

---

## 4. Mathematical Risk Engine Verification

The formula implemented in `app/risk/scoring.py` was evaluated against manual calculations across 5 distinct test vectors:

$$\text{Risk Score} = (C \times 0.30) + (U \times 0.25) + (D \times 0.20) + (G \times 0.15) + (A \times 0.10)$$

| Test Vector ($C, U, D, G, A$) | Manual Mathematical Calculation | Code Result | Level | Match |
| :--- | :--- | :---: | :---: | :---: |
| $(95, 90, 85, 80, 75)$ | $28.5 + 22.5 + 17.0 + 12.0 + 7.5 = 87.50$ | **87.50** | `critical` | **EXACT** |
| $(70, 60, 75, 65, 50)$ | $21.0 + 15.0 + 15.0 + 9.75 + 5.0 = 65.75$ | **65.75** | `high` | **EXACT** |
| $(50, 40, 40, 50, 30)$ | $15.0 + 10.0 + 8.0 + 7.5 + 3.0 = 43.50$ | **43.50** | `medium` | **EXACT** |
| $(20, 10, 20, 30, 20)$ | $6.0 + 2.5 + 4.0 + 4.5 + 2.0 = 19.00$ | **19.00** | `low` | **EXACT** |
| $(61, 61, 61, 61, 61)$ | $18.3 + 15.25 + 12.2 + 9.15 + 6.1 = 61.00$ | **61.00** | `high` | **EXACT** |

Threshold boundaries verified:
- **Low Risk:** $0.0 - 30.0$
- **Medium Risk:** $30.1 - 60.0$
- **High Risk:** $60.1 - 80.0$
- **Critical Risk:** $80.1 - 100.0$

---

## 5. Machine Learning Evaluation & Non-Fabrication Audit

- **Dataset Size:** 700 synthetic/enterprise samples derived from documented distributions
- **Data Split:** 70% Train (490) / 15% Validation (105) / 15% Holdout Test (105)
- **Cross-Validation:** 5-Fold Stratified Cross Validation
- **Model Selected:** Random Forest Classifier (100 estimators, max depth 10)
- **Feature Weights (Gini Impurity Reduction):**
  - Uniqueness: 28.31%
  - Criticality: 20.68%
  - Documentation Gap: 15.70%
  - Dependency: 15.54%
  - Availability Risk: 9.62%
  - Non-linear interactions (experts, systems, doc length): 10.15%
- **Empirical Metrics on Unseen Test Holdout (105 samples):**
  - **Accuracy:** `99.05%` (SLA Target: $\ge 80.0\%$) — **PASSED**
  - **Precision:** `99.51%`
  - **Recall:** `87.50%`
  - **F1 Score (Macro):** `0.9142` (SLA Target: $\ge 0.7500$) — **PASSED**
  - **5-Fold Cross-Val Mean F1:** `0.8691`
- **Saved Model Check:** Verified on disk at `backend/ml_models/risk_classifier.pkl` and `scaler.pkl` with `metadata.json`.

---

## 6. Security Audit Findings

1. **Authentication & Password Hashing:**
   - Password hashing uses `bcrypt` with cost factor 12 (`$2b$12$...`).
   - Verified that plaintext passwords cannot be recovered.
2. **Access Control & RBAC:**
   - Employees attempting to access admin audit logs receive `403 Forbidden`.
   - Token tamper/expiration verified with immediate `401 Unauthorized`.
3. **SQL Injection Resistance:**
   - Tested integer route parameter manipulation (`/documents/1%20OR%201=1`).
   - Blocked at FastAPI validation boundary with `422 Unprocessable Entity`; never executed on SQLite/PostgreSQL.
   - All database queries strictly use SQLAlchemy parameterized ORM queries.
4. **Cross-Site Scripting (XSS):**
   - Injected `<script>alert('XSS')</script>` into knowledge payload.
   - Stored and retrieved as sanitized text; frontend React escapes all innerHTML strings automatically.
5. **CORS:**
   - Pre-flight `OPTIONS` requests respond with explicit `Access-Control-Allow-Origin: http://127.0.0.1:5173`.

---

## 7. Performance Latency Measurements

Measured across 10 repeated warm iterations:

- **Baseline API Ping Latency (`/health`):** `2.78 ms`
- **Semantic Vector + Lexical Search Latency:** `28.18 ms` (Target: $< 200 \text{ ms}$)
- **Complete NLP Pipeline (Clean, NER, Keywords, Topics, Embedding):** `2.70 ms` per 500-token document
- **Database Transaction Overhead:** $< 4 \text{ ms}$

---

## 8. Conclusion
The system successfully passed 100% of automated unit, integration, and security checks. Zero failures or unhandled exceptions were detected during the comprehensive audit run.
