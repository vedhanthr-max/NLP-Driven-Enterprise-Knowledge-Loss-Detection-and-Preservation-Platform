# Enterprise API Audit & Specification Matrix

**Project:** NLP-Driven SaaS Platform for Enterprise Knowledge Loss Detection and Preservation  
**Classification:** Complete REST API Interface Audit  
**Base URL:** `http://127.0.0.1:8000/api/v1`  
**Interactive Docs:** `http://127.0.0.1:8000/docs` (OpenAPI 3.0)  

---

## 1. Executive Summary

This document provides a comprehensive audit of all **31 REST endpoints** exposed by the FastAPI backend across 9 resource routers, verifying request schemas, response formats, authentication requirements, role authorization constraints, error hierarchies, and frontend consumer mapping.

---

## 2. API Endpoint Audit Table

| # | Method | Path | Purpose | Auth Required | Role Required | Request Format | Response Format | Error Codes | Test Status |
| :-: | :---: | :--- | :--- | :---: | :---: | :--- | :--- | :--- | :---: |
| 1 | `GET` | `/health` | Service health status | No | Any | None | 200 `{status, service, version}` | 500 | **VERIFIED** |
| 2 | `GET` | `/` | Root service metadata | No | Any | None | 200 `{name, version, docs}` | 500 | **VERIFIED** |
| 3 | `POST` | `/api/v1/auth/register` | Register new organization user | No | Any | `RegisterRequest` (JSON) | 201 `UserOut` | `ERR-AUTH-003`, 409 | **VERIFIED** |
| 4 | `POST` | `/api/v1/auth/login` | Authenticate & issue JWT | No | Any | `LoginRequest` (JSON) | 200 `TokenResponse` | `ERR-AUTH-001`, 401 | **VERIFIED** |
| 5 | `POST` | `/api/v1/auth/refresh` | Issue new access token | No | Any | `RefreshRequest` (JSON) | 200 `TokenResponse` | `ERR-AUTH-002`, 401 | **VERIFIED** |
| 6 | `GET` | `/api/v1/auth/me` | Current authenticated user profile | Bearer JWT | Any | None | 200 `UserOut` | `ERR-AUTH-002`, 401 | **VERIFIED** |
| 7 | `POST` | `/api/v1/auth/logout` | Terminate session | Bearer JWT | Any | None | 200 `{status: success}` | `ERR-AUTH-002`, 401 | **VERIFIED** |
| 8 | `POST` | `/api/v1/documents/upload` | Ingest PDF, DOCX, TXT, MD | Bearer JWT | Any | Multipart `UploadFile` | 202 `DocumentDetailOut` | `ERR-DOC-001`, `ERR-DOC-004`, `ERR-DOC-005`, 413 | **VERIFIED** |
| 9 | `GET` | `/api/v1/documents` | List organization documents | Bearer JWT | Any | Query `page`, `limit` | 200 `DocumentListResponse` | `ERR-AUTH-002`, 401 | **VERIFIED** |
| 10 | `GET` | `/api/v1/documents/{id}` | Get document metadata & chunks | Bearer JWT | Any | Path `id` | 200 `DocumentDetailOut` | `ERR-DOC-002`, 404 | **VERIFIED** |
| 11 | `DELETE`| `/api/v1/documents/{id}` | Soft-delete document | Bearer JWT | `admin`, `manager` | Path `id` | 200 `{status: success}` | `ERR-DOC-002`, `ERR-PERM-001`, 403 | **VERIFIED** |
| 12 | `GET` | `/api/v1/knowledge` | List knowledge items | Bearer JWT | Any | Query `category`, `status` | 200 `KnowledgeListResponse` | `ERR-AUTH-002`, 401 | **VERIFIED** |
| 13 | `GET` | `/api/v1/knowledge/{id}` | Detailed knowledge item inspector | Bearer JWT | Any | Path `id` | 200 `KnowledgeDetailOut` | `ERR-KNOW-001`, 404 | **VERIFIED** |
| 14 | `POST` | `/api/v1/knowledge` | Create structured knowledge record | Bearer JWT | Any | `KnowledgeCreate` (JSON) | 201 `KnowledgeDetailOut` | `ERR-VALID-001`, 422 | **VERIFIED** |
| 15 | `PUT` | `/api/v1/knowledge/{id}` | Update knowledge record | Bearer JWT | Any | `KnowledgeUpdate` (JSON) | 200 `KnowledgeDetailOut` | `ERR-KNOW-001`, 404 | **VERIFIED** |
| 16 | `DELETE`| `/api/v1/knowledge/{id}` | Remove knowledge record | Bearer JWT | `admin`, `manager` | Path `id` | 200 `{status: success}` | `ERR-PERM-001`, 403 | **VERIFIED** |
| 17 | `POST` | `/api/v1/risk/analyze/{id}` | Calculate 5-factor risk & ML inference | Bearer JWT | Any | `RiskAssessmentRequest` | 200 `RiskScoreOut` | `ERR-KNOW-001`, 404 | **VERIFIED** |
| 18 | `POST` | `/api/v1/risk/simulate` | Dynamic risk studio simulation | Bearer JWT | Any | `FactorSimulationRequest` | 200 `FactorSimulationResponse` | `ERR-VALID-001`, 422 | **VERIFIED** |
| 19 | `GET` | `/api/v1/risk/dashboard` | Executive KPI scorecard & distributions | Bearer JWT | Any | None | 200 `DashboardMetricsOut` | `ERR-AUTH-002`, 401 | **VERIFIED** |
| 20 | `GET` | `/api/v1/risk/history/{id}` | Historical risk assessment log | Bearer JWT | Any | Path `id` | 200 `List[RiskScoreOut]` | `ERR-KNOW-001`, 404 | **VERIFIED** |
| 21 | `GET` | `/api/v1/ml/metrics` | Model benchmarking metrics & CV | Bearer JWT | Any | None | 200 `dict` | `ERR-AUTH-002`, 401 | **VERIFIED** |
| 22 | `POST` | `/api/v1/ml/predict` | Real-time ML risk classification | Bearer JWT | Any | `MLPredictRequest` (JSON) | 200 `MLPredictResponse` | `ERR-VALID-001`, 422 | **VERIFIED** |
| 23 | `POST` | `/api/v1/ml/train` | Trigger 4-algorithm retraining & CV | Bearer JWT | `admin`, `manager` | None | 200 `MLTrainingResponse` | `ERR-PERM-001`, 403 | **VERIFIED** |
| 24 | `GET` | `/api/v1/search` | Hybrid vector + lexical search | Bearer JWT | Any | Query `q`, `limit` | 200 `SearchResponse` | `ERR-AUTH-002`, 401 | **VERIFIED** |
| 25 | `GET` | `/api/v1/preservation-actions`| List preservation action items | Bearer JWT | Any | Query `status`, `priority` | 200 `List[PreservationActionOut]` | `ERR-AUTH-002`, 401 | **VERIFIED** |
| 26 | `POST` | `/api/v1/preservation-actions`| Create manual preservation task | Bearer JWT | Any | `PreservationActionCreate` | 201 `PreservationActionOut` | `ERR-KNOW-001`, 404 | **VERIFIED** |
| 27 | `PUT` | `/api/v1/preservation-actions/{id}`| Update Kanban stage, hours, notes | Bearer JWT | Any | `PreservationActionUpdate` | 200 `PreservationActionOut` | `ERR-ACT-001`, 404 | **VERIFIED** |
| 28 | `GET` | `/api/v1/employees` | Organization employee directory | Bearer JWT | Any | None | 200 `List[EmployeeOut]` | `ERR-AUTH-002`, 401 | **VERIFIED** |
| 29 | `GET` | `/api/v1/audit/logs` | Comprehensive compliance audit logs | Bearer JWT | `admin` only | Query `limit`, `action_type` | 200 `List[AuditLogOut]` | `ERR-PERM-001`, 403 | **VERIFIED** |
| 30 | `GET` | `/docs` | Swagger OpenAPI UI | No | Any | None | 200 HTML | — | **VERIFIED** |
| 31 | `GET` | `/openapi.json` | OpenAPI 3.0 specification JSON | No | Any | None | 200 JSON | — | **VERIFIED** |

---

## 3. Frontend-Backend Contract Verification

All consumer calls in `frontend/src/services/api.js` were audited against backend route definitions:

| Frontend API Module | Function Call | Targeted Backend Endpoint | Contract Alignment |
| :--- | :--- | :--- | :---: |
| `authAPI` | `login(email, password)` | `POST /api/v1/auth/login` | **100% MATCH** |
| `authAPI` | `register(data)` | `POST /api/v1/auth/register` | **100% MATCH** |
| `authAPI` | `getMe()` | `GET /api/v1/auth/me` | **100% MATCH** |
| `authAPI` | `logout()` | `POST /api/v1/auth/logout` | **100% MATCH** |
| `documentAPI` | `upload(formData)` | `POST /api/v1/documents/upload` | **100% MATCH** |
| `documentAPI` | `getAll(page, limit)` | `GET /api/v1/documents` | **100% MATCH** |
| `documentAPI` | `getDetails(id)` | `GET /api/v1/documents/{id}` | **100% MATCH** |
| `documentAPI` | `delete(id)` | `DELETE /api/v1/documents/{id}` | **100% MATCH** |
| `knowledgeAPI` | `getAll(params)` | `GET /api/v1/knowledge` | **100% MATCH** |
| `knowledgeAPI` | `getDetails(id)` | `GET /api/v1/knowledge/{id}` | **100% MATCH** |
| `knowledgeAPI` | `create(data)` | `POST /api/v1/knowledge` | **100% MATCH** |
| `knowledgeAPI` | `update(id, data)` | `PUT /api/v1/knowledge/{id}` | **100% MATCH** |
| `riskAPI` | `getDashboard()` | `GET /api/v1/risk/dashboard` | **100% MATCH** |
| `riskAPI` | `analyze(id, data)` | `POST /api/v1/risk/analyze/{id}` | **100% MATCH** |
| `riskAPI` | `simulate(factors)` | `POST /api/v1/risk/simulate` | **100% MATCH** |
| `riskAPI` | `getHistory(id)` | `GET /api/v1/risk/history/{id}` | **100% MATCH** |
| `mlAPI` | `getMetrics()` | `GET /api/v1/ml/metrics` | **100% MATCH** |
| `mlAPI` | `predict(data)` | `POST /api/v1/ml/predict` | **100% MATCH** |
| `mlAPI` | `train()` | `POST /api/v1/ml/train` | **100% MATCH** |
| `searchAPI` | `semanticSearch(q, limit)` | `GET /api/v1/search` | **100% MATCH** |
| `preservationAPI` | `getAll(params)` | `GET /api/v1/preservation-actions` | **100% MATCH** |
| `preservationAPI` | `create(data)` | `POST /api/v1/preservation-actions` | **100% MATCH** |
| `preservationAPI` | `update(id, data)` | `PUT /api/v1/preservation-actions/{id}` | **100% MATCH** |
| `employeeAPI` | `getAll()` | `GET /api/v1/employees` | **100% MATCH** |
| `auditAPI` | `getLogs(limit, action_type)` | `GET /api/v1/audit/logs` | **100% MATCH** |

**Discrepancies Found:** 0 mismatches. All parameter names, URL query structures, and HTTP verbs match seamlessly.
