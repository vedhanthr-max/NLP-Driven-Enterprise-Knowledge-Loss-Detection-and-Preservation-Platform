# NLP-DRIVEN SAAS PLATFORM FOR ENTERPRISE KNOWLEDGE LOSS DETECTION AND PRESERVATION

## COMPREHENSIVE PROJECT DOCUMENTATION (ENHANCED)

**Version**: 2.0  
**Status**: Final Year Project Specification  
**Last Updated**: September 2026  
**Document Classification**: Project Specification & Implementation Guide

---

# ABSTRACT

Organizations possess valuable knowledge through their employees, documents, project records, procedures, and internal processes. When experienced employees leave, important organizational knowledge can be lost. 

This project proposes an **NLP-Driven SaaS Platform for Enterprise Knowledge Loss Detection and Preservation**. The system uses Natural Language Processing, Machine Learning, semantic embeddings, and a centralized repository to identify and preserve organizational knowledge at risk of being lost.

Users upload enterprise documents (PDF, DOCX, TXT). The system extracts text and applies NLP techniques (Named Entity Recognition, keyword extraction, topic identification) to create structured knowledge records. The system evaluates knowledge-loss risk using five critical factors: knowledge criticality, uniqueness, organizational dependency, documentation gap, and expert availability.

For high-risk knowledge, the system generates preservation recommendations (documentation creation, assigning secondary experts, knowledge-transfer sessions). Semantic search using Sentence Transformers and PostgreSQL pgvector enables retrieval based on meaning rather than exact keywords.

The platform combines **NLP + Machine Learning + Knowledge Management + Risk Detection + Semantic Search + Multi-Tenant SaaS Architecture** into a unified enterprise knowledge-preservation system.

---

# TABLE OF CONTENTS

1. Introduction
2. Background
3. Problem Statement
4. Existing System
5. Limitations of Existing System
6. Proposed System
7. Objectives
8. Scope
9. System Requirements
10. Technology Stack
11. System Architecture
12. System Modules
13. System Workflow
14. NLP Processing Pipeline
15. Knowledge Extraction
16. Knowledge Loss Detection
17. Risk Calculation Algorithm
18. Machine Learning Component
19. Semantic Search
20. Knowledge Preservation
21. Knowledge Repository
22. Knowledge Graph
23. SaaS / Multi-Tenant Architecture
24. Database Design
25. User Roles & Permissions
26. Security Implementation (NEW)
27. API Design & Specifications (NEW)
28. Error Handling Strategy (NEW)
29. Monitoring, Logging & Alerting (NEW)
30. Performance Requirements (NEW)
31. Caching & Optimization (NEW)
32. Configuration Management (NEW)
33. Frontend Design
34. Backend Design
35. Project Folder Structure
36. Implementation Workflow
37. Testing Strategy (ENHANCED)
38. Deployment & DevOps (NEW)
39. Disaster Recovery & Backup (NEW)
40. Data Management & Retention (NEW)
41. Accessibility & UX Standards (NEW)
42. Expected Results
43. Advantages
44. Limitations
45. Future Enhancements
46. Cost Analysis (NEW)
47. Risk Management Plan (NEW)
48. Success Metrics & KPIs (NEW)
49. Documentation Standards (NEW)
50. Conclusion

---

# 1. INTRODUCTION

## 1.1 Overview

Knowledge is a critical organizational asset. Employees acquire knowledge through years of experience, problem-solving, customer interaction, and technical work.

Some knowledge is formally documented; other knowledge exists only in employee experience:
- How to troubleshoot legacy systems
- Database recovery procedures
- Server configuration knowledge
- Handling of specific customer issues
- Understanding of complex business processes
- Solutions to uncommon technical problems

When only one or few employees possess this knowledge and they leave, the organization faces significant knowledge loss.

Organizations require mechanisms to:
1. Identify important knowledge
2. Determine which knowledge is vulnerable
3. Estimate knowledge-loss risk
4. Recommend preservation actions
5. Store knowledge in centralized repository
6. Make preserved knowledge searchable

This project addresses these requirements through an NLP-driven SaaS platform.

---

# 2. BACKGROUND

## 2.1 Enterprise Knowledge

Enterprise knowledge encompasses:
- Technical expertise
- Project documentation
- Customer insights
- Process procedures
- Operational knowledge
- Troubleshooting guides
- Infrastructure understanding
- Business logic and rules

## 2.2 Knowledge Loss Causes

- Employee resignation
- Retirement
- Departmental transfer
- Lack of documentation
- Poor knowledge sharing practices
- Single-person expertise dependency
- Inadequate knowledge management

## 2.3 Natural Language Processing

NLP enables computers to process and analyze human language. In this project:
- Text preprocessing and cleaning
- Named Entity Recognition (NER)
- Keyword extraction
- Topic identification
- Semantic representation
- Similarity analysis

## 2.4 SaaS Architecture

Software as a Service (SaaS) provides web-based platform supporting multiple organizations. Each organization's data (employees, documents, knowledge, departments) is logically separated using organization identifiers while sharing the same application infrastructure.

---

# 3. PROBLEM STATEMENT

Organizations contain valuable knowledge distributed among employees and documents. Existing knowledge-management approaches store information but may not adequately identify vulnerable knowledge.

**Primary Problem**:
> **How can an organization automatically identify important knowledge at risk of being lost and recommend appropriate preservation actions using NLP and Machine Learning?**

The system should analyze organizational knowledge, determine importance and dependency, estimate knowledge-loss risk, and help organizations preserve critical knowledge.

---

# 4. EXISTING SYSTEM

Traditional knowledge management:
- Manual documentation
- Shared folders and drive systems
- Internal wikis
- Document management systems
- Employee-created knowledge bases
- Manual knowledge-transfer sessions

**Limitation**: Identification of knowledge-loss risk requires significant human effort.

---

# 5. LIMITATIONS OF EXISTING SYSTEM

1. **Manual Identification**: Important knowledge requires human identification
2. **Undocumented Knowledge**: Difficult to identify knowledge not formally documented
3. **No Automated Risk Analysis**: Risk identification lacks automation
4. **Single-Person Dependency**: Hard to identify who holds unique knowledge
5. **Limited Semantic Understanding**: Basic document processing without semantic meaning
6. **Keyword-Based Search**: Limited to exact keyword matching
7. **No Automated Recommendations**: Preservation recommendations require manual effort
8. **Distributed Knowledge**: Knowledge exists across multiple unconnected locations

The proposed system addresses these through NLP, risk analysis, semantic search, and preservation workflows.

---

# 6. PROPOSED SYSTEM

Web-based SaaS platform analyzing enterprise knowledge and identifying knowledge-loss risks.

## Main Workflow

```
Employee / Manager
    ↓
Upload Knowledge / Documents
    ↓
Text Extraction
    ↓
Text Preprocessing
    ↓
NLP Processing
    ↓
Knowledge Extraction
    ↓
Knowledge Analysis
    ↓
Risk Feature Generation
    ↓
Risk Score Calculation
    ↓
Risk Classification (Rule-based + ML)
    ↓
Preservation Recommendation
    ↓
Knowledge Repository
    ↓
Semantic Search
    ↓
Dashboard & Monitoring
```

## Core Technologies

- **Frontend**: React.js with TypeScript
- **Backend**: FastAPI (Python 3.10+)
- **Database**: PostgreSQL 14+
- **Vector Storage**: pgvector extension
- **NLP Framework**: spaCy 3.x
- **Machine Learning**: Scikit-learn 1.x
- **Embeddings**: Sentence Transformers
- **Authentication**: JWT (JSON Web Tokens)
- **Document Processing**: PyMuPDF + python-docx
- **Containerization**: Docker + Docker Compose
- **CI/CD**: GitHub Actions
- **Monitoring**: ELK Stack (Elasticsearch, Logstash, Kibana)
- **Caching**: Redis
- **API Documentation**: FastAPI Swagger/OpenAPI

---

# 7. OBJECTIVES

### Primary Objectives

1. **Web Platform Development**: Build full-stack web-based knowledge management platform
2. **Document Management**: Enable upload and management of knowledge documents
3. **NLP Processing**: Automatically extract information using NLP techniques
4. **Entity & Keyword Extraction**: Identify important entities, keywords, and topics
5. **Knowledge Structuring**: Represent organizational knowledge as structured records
6. **Expertise Mapping**: Identify knowledge dependencies on specific experts
7. **Risk Scoring**: Calculate knowledge-loss risk using transparent methodology
8. **Risk Classification**: Categorize knowledge into risk levels (LOW, MEDIUM, HIGH, CRITICAL)
9. **Preservation Actions**: Generate actionable preservation recommendations
10. **Semantic Search**: Implement semantic search for knowledge retrieval
11. **Risk Dashboard**: Provide visual monitoring of knowledge risks
12. **Multi-Tenancy**: Support multiple organizations through SaaS architecture

### Secondary Objectives

13. Implement Machine Learning for risk prediction (after rule-based baseline)
14. Create knowledge graph visualizations
15. Automated knowledge-transfer task generation
16. Advanced analytics and trend analysis
17. Integration with external knowledge sources

---

# 8. SCOPE OF THE PROJECT

## Document Formats Supported

- PDF (via PyMuPDF)
- DOCX/DOCM (via python-docx)
- TXT (plain text)
- FAQs (structured text)
- Knowledge articles
- Internal reports
- Project documentation
- Support information

## MVP (Minimum Viable Product) Scope

```
✓ Authentication & Authorization
✓ Document Upload & Management
✓ Text Extraction
✓ NLP Processing (NER, Keywords, Topics)
✓ Knowledge Extraction & Structuring
✓ Rule-Based Risk Scoring
✓ Risk Dashboard
✓ Knowledge Repository
✓ Basic Search
✓ User Management
✓ Organization Management
✓ Basic Security
```

## Advanced Features (Phase 2)

```
+ Semantic Search with pgvector
+ Machine Learning Risk Prediction
+ Knowledge Graph
+ Preservation Recommendations
+ Knowledge-Transfer Workflows
+ Multi-Tenancy Optimization
+ Advanced Analytics
+ Audit Logging
+ Notifications
+ API Rate Limiting
```

## Optional Enhancements (Phase 3)

```
~ LLM Integration for Summarization
~ Knowledge Trend Analysis
~ Department-Level Analytics
~ Integration with Calendar/Email
~ Mobile Application
~ Advanced Graph Visualizations
~ Predictive Expert Turnover
~ Knowledge Sustainability Scoring
```

---

# 9. SYSTEM REQUIREMENTS

## 9.1 Hardware Requirements

### Development Environment
- Laptop/Desktop computer
- **Minimum**: 8 GB RAM, 50 GB storage
- **Recommended**: 16 GB RAM, 100 GB storage
- Multi-core processor (4+ cores)
- Internet connection for dependency installation

### Staging/Production
- **Server**: Cloud VM (AWS EC2, GCP, Azure, or similar)
- **CPU**: 4-8 vCPU cores
- **RAM**: 16-32 GB (16 GB minimum)
- **Storage**: 500 GB - 2 TB (depends on document volume)
- **Network**: Minimum 50 Mbps connection
- **Backup Storage**: Equal to main storage capacity

## 9.2 Software Requirements

### Development Tools
- **OS**: Windows 10+ / macOS 10.15+ / Linux (Ubuntu 20.04+)
- **IDE**: VS Code, PyCharm, or JetBrains WebStorm
- **Version Control**: Git 2.30+
- **Package Manager**: npm 8+, pip 21+

### Runtime & Database
- **Python**: 3.10 or 3.11
- **Node.js**: 16 LTS or 18 LTS
- **PostgreSQL**: 14.x or 15.x
- **Redis**: 7.x (for caching)

### Development Dependencies
- Docker & Docker Compose
- Postman (API testing)
- pgAdmin (database management)
- DBeaver (database exploration)
- Git GUI (SourceTree or GitKraken)

---

# 10. TECHNOLOGY STACK

| Layer | Component | Technology | Version |
|-------|-----------|-----------|---------|
| **Frontend** | Framework | React.js | 18.x |
| | Language | TypeScript | 5.x |
| | State Management | Redux Toolkit | 1.9.x |
| | HTTP Client | Axios | 1.x |
| | UI Components | Material-UI | 5.x |
| | Charting | Recharts | 2.x |
| | Form Handling | React Hook Form | 7.x |
| **Backend** | Framework | FastAPI | 0.104+ |
| | Language | Python | 3.10+ |
| | Server | Uvicorn | 0.24+ |
| | Async | asyncio/ASGI | Built-in |
| **Database** | Primary DB | PostgreSQL | 14+ |
| | Vector Search | pgvector | 0.5+ |
| | ORM | SQLAlchemy | 2.0+ |
| | Migrations | Alembic | 1.13+ |
| **NLP** | Framework | spaCy | 3.7.x |
| | Model | en_core_web_md | 3.7.x |
| | Embeddings | Sentence Transformers | 2.2.x |
| | Model | all-MiniLM-L6-v2 | Latest |
| **ML** | Framework | Scikit-learn | 1.3.x |
| | Data Processing | Pandas | 2.x |
| | Numerical Computing | NumPy | 1.26.x |
| **Authentication** | Method | JWT | PyJWT 2.x |
| | Password Hashing | bcrypt | 4.x |
| | Session | Sessions/Cookies | - |
| **Document Processing** | PDF | PyMuPDF (fitz) | 1.23.x |
| | DOCX | python-docx | 0.8.x |
| **Caching** | Cache Store | Redis | 7.x |
| | Python Client | redis-py | 5.x |
| **Monitoring** | Logs | ELK Stack | 8.x |
| | Metrics | Prometheus | 2.x |
| | Visualization | Grafana | 10.x |
| **DevOps** | Containerization | Docker | 24.x |
| | Orchestration | Docker Compose | 2.x |
| | CI/CD | GitHub Actions | - |
| **Testing** | Backend | pytest | 7.x |
| | Mocking | unittest.mock | Built-in |
| | Coverage | coverage.py | 7.x |
| | Frontend | Jest | 29.x |
| | E2E | Cypress | 13.x |
| **API Documentation** | Format | OpenAPI 3.0 | - |
| | Tool | Swagger UI | Built-in FastAPI |
| **Security** | HTTPS | Let's Encrypt | Latest |
| | WAF | Optional | - |
| **Utilities** | Logging | Python logging | Built-in |
| | Config Management | python-dotenv | 1.x |
| | Data Validation | Pydantic | 2.x |

---

# 11. SYSTEM ARCHITECTURE

## 11.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      ENTERPRISE USERS                        │
│              (Managers, Employees, Admins)                   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
        ┌────────────────────────────────────┐
        │     React.js Frontend (SPA)        │
        │  ┌──────────────────────────────┐  │
        │  │  Auth │ Dashboard │ Documents│  │
        │  │  Risk │ Knowledge │ Search   │  │
        │  └──────────────────────────────┘  │
        └────────────────────┬───────────────┘
                             │ HTTPS/REST API
                             ▼
        ┌────────────────────────────────────┐
        │   FastAPI Backend Layer            │
        │  ┌──────────────────────────────┐  │
        │  │ Auth Service │ API Gateway  │  │
        │  │ Request Validation & Auth    │  │
        │  └──────────────────────────────┘  │
        └────────────────────┬───────────────┘
                             │
        ┌────────────────────┴────────────────┬────────────────┐
        ▼                                     ▼                ▼
   ┌─────────────┐                  ┌──────────────────┐  ┌──────────┐
   │Auth Service │                  │Knowledge Service │  │ Risk     │
   │             │                  │                  │  │ Engine   │
   │- Login      │                  │- Upload Docs     │  │          │
   │- Register   │                  │- Extract Text    │  │- Score   │
   │- Tokens     │                  │- Parse Metadata  │  │- Classify│
   │- Permissions│                  │- Store Knowledge │  │- Recommend
   └─────────────┘                  └────────┬─────────┘  └────┬─────┘
        │                                    │                 │
        └────────────────┬──────────────────┴─────────────────┘
                         │
        ┌────────────────┴─────────────────┐
        │   NLP & ML Processing Layer      │
        │  ┌───────────────────────────┐   │
        │  │ Text Preprocessing        │   │
        │  │ - Cleaning & Tokenization │   │
        │  │ - Lemmatization           │   │
        │  │ - Stopword Handling       │   │
        │  └───────────────────────────┘   │
        │  ┌───────────────────────────┐   │
        │  │ NLP Processing (spaCy)    │   │
        │  │ - Named Entity Recognition│   │
        │  │ - POS Tagging             │   │
        │  │ - Dependency Parsing      │   │
        │  └───────────────────────────┘   │
        │  ┌───────────────────────────┐   │
        │  │ Feature Extraction        │   │
        │  │ - Keywords                │   │
        │  │ - Topics                  │   │
        │  │ - Entities                │   │
        │  └───────────────────────────┘   │
        │  ┌───────────────────────────┐   │
        │  │ Embeddings (SentTransfm)  │   │
        │  │ - Generate Vectors        │   │
        │  │ - Normalize               │   │
        │  │ - Store in pgvector       │   │
        │  └───────────────────────────┘   │
        │  ┌───────────────────────────┐   │
        │  │ ML Risk Prediction        │   │
        │  │ - Feature Engineering     │   │
        │  │ - Model Inference         │   │
        │  │ - Confidence Scores       │   │
        │  └───────────────────────────┘   │
        └────────────────┬───────────────────┘
                         │
        ┌────────────────┴──────────────────────────┐
        │     Data Persistence Layer               │
        │  ┌────────────────────────────────────┐  │
        │  │     PostgreSQL Database             │  │
        │  │  ┌─────────────────────────────┐   │  │
        │  │  │ Organization                │   │  │
        │  │  │ Users & Departments         │   │  │
        │  │  │ Documents & Knowledge       │   │  │
        │  │  │ Risk Scores                 │   │  │
        │  │  │ Entities & Keywords         │   │  │
        │  │  │ Audit Logs                  │   │  │
        │  │  └─────────────────────────────┘   │  │
        │  │  ┌─────────────────────────────┐   │  │
        │  │  │ pgvector Extension          │   │  │
        │  │  │ - Embeddings Table          │   │  │
        │  │  │ - Vector Indexes (IVFFLAT)  │   │  │
        │  │  └─────────────────────────────┘   │  │
        │  └────────────────────────────────────┘  │
        │  ┌────────────────────────────────────┐  │
        │  │     Redis Cache Layer               │  │
        │  │  - Search Results Cache             │  │
        │  │  - User Session Cache               │  │
        │  │  - Rate Limiting Counters           │  │
        │  └────────────────────────────────────┘  │
        └────────────────┬──────────────────────────┘
                         │
        ┌────────────────┴──────────────────┐
        ▼                                   ▼
   ┌──────────────────┐           ┌───────────────────┐
   │Semantic Search   │           │Monitoring & Logging
   │                  │           │                   │
   │- Query Vector    │           │- ELK Stack        │
   │- Similarity Match│           │- Prometheus       │
   │- Ranking         │           │- Grafana          │
   │- Results Return  │           │- Audit Logging    │
   └──────────────────┘           └───────────────────┘
        │                                   │
        ▼                                   ▼
   ┌──────────────────────────────────────────────┐
   │    Dashboard & Analytics                     │
   │  - Risk Overview                              │
   │  - Knowledge Metrics                          │
   │  - Preservation Progress                      │
   │  - System Health                              │
   └──────────────────────────────────────────────┘
```

## 11.2 System Components

1. **Frontend (React.js)**
   - Single Page Application
   - Component-based architecture
   - Redux for state management
   - Responsive design

2. **API Gateway (FastAPI)**
   - Request routing
   - Authentication middleware
   - Rate limiting
   - CORS handling
   - Request/response validation

3. **Business Logic Layer**
   - Auth Service
   - Document Service
   - Knowledge Service
   - Risk Engine
   - Search Service

4. **NLP & ML Layer**
   - Text preprocessing
   - Entity extraction
   - Embedding generation
   - ML model inference

5. **Data Layer**
   - PostgreSQL database
   - pgvector for vector search
   - Redis for caching

6. **Monitoring & Observability**
   - Centralized logging (ELK)
   - Metrics collection (Prometheus)
   - Visualization (Grafana)
   - Alerting

---

# 12. SYSTEM MODULES

## Module 1: Authentication & Authorization

**Responsibilities**:
- User registration (email verification)
- Login with JWT tokens
- Password hashing (bcrypt, 12 rounds)
- Role-based access control (RBAC)
- Token refresh mechanisms
- Logout and session management
- Multi-factor authentication support (Phase 2)
- Audit trail of login attempts

**Key Functions**:
- `register_user()`
- `login_user()`
- `verify_email()`
- `refresh_token()`
- `verify_token()`
- `check_permission()`

---

## Module 2: Organization Management

**Responsibilities**:
- Create and manage organizations
- Manage organization users
- Manage departments
- Organization-specific configuration
- Data isolation (ensure org-level data separation)
- Subscription/licensing management

**Database Tables**:
- organizations
- organization_settings
- departments
- user_organization_mappings

---

## Module 3: Employee Management

**Responsibilities**:
- Maintain employee profiles
- Track expertise areas
- Manage department assignments
- Track employee status (active/inactive)
- Expertise level tracking
- Knowledge associations

**Data Stored**:
```
employee_id
user_id
organization_id
department_id
expertise_areas (JSON)
expertise_level (beginner/intermediate/expert)
status (active/inactive/left)
joined_date
last_active_date
```

---

## Module 4: Knowledge Collection

**Responsibilities**:
- Accept knowledge submissions
- Support multiple file formats (PDF, DOCX, TXT)
- Validate file types and sizes
- Virus/malware scanning (optional)
- Metadata extraction
- Document versioning
- Manual knowledge entry

**Constraints**:
- Maximum file size: 50 MB
- Maximum documents per month: 1000 (per org)
- Supported formats: .pdf, .docx, .txt, .md
- Allowed MIME types:
  - application/pdf
  - application/vnd.openxmlformats-officedocument.wordprocessingml.document
  - text/plain
  - text/markdown

---

## Module 5: Document Processing

**Workflow**:
```
Uploaded Document
    ↓
Format Validation
    ↓
File Scanning (optional)
    ↓
Text Extraction
    ├─ PDF: PyMuPDF (fitz)
    ├─ DOCX: python-docx
    └─ TXT: Direct read
    ↓
Metadata Extraction
    ├─ Title
    ├─ Created date
    ├─ Author
    ├─ Modification date
    ├─ Page count
    └─ Language detection
    ↓
Text Cleaning
    ├─ Remove extra whitespace
    ├─ Fix encoding issues
    ├─ Remove special characters
    └─ Normalize line breaks
    ↓
Text Chunking
    ├─ Split by sentences
    ├─ Create overlapping chunks (512 tokens, 50 token overlap)
    └─ Maintain chunk metadata
    ↓
Store in PostgreSQL
    ├─ Document record
    ├─ Text chunks
    └─ Metadata
```

**Key Libraries**:
- `PyMuPDF` (fitz): PDF extraction
- `python-docx`: DOCX processing
- `python-pptx`: Optional PowerPoint support (Phase 2)
- `langdetect`: Language detection

---

## Module 6: NLP Processing Engine

### 6.1 Text Preprocessing

**Operations**:
1. **Lowercasing**: Convert to lowercase for consistency
2. **Tokenization**: Split text into tokens
3. **Stopword Removal**: Remove common words (the, is, and, etc.)
4. **Lemmatization**: Convert words to base form
   - "running", "runs", "ran" → "run"
   - "better" → "good"
5. **POS Tagging**: Identify parts of speech
6. **Named Entity Recognition**: Identify entities

**Configuration**:
```python
# Stopwords to remove (customizable per language)
STOPWORDS = {'the', 'is', 'and', 'or', 'a', 'an', 'in', 'on', 'at', 'to', 'for', ...}

# Lemmatization rules
LEMMATIZATION_ENABLED = True

# NER models
NER_MODEL = "en_core_web_md"

# Min token length to keep
MIN_TOKEN_LENGTH = 2
```

### 6.2 Named Entity Recognition (NER)

**Entity Types Extracted**:
```
PERSON        - Employee names, team members
ORGANIZATION  - Company names, departments
TECHNOLOGY    - Programming languages, tools, frameworks
PRODUCT       - Software names, systems
GPE           - Geographic locations
DATE          - Important dates
EVENT         - Project names, milestones
FAC           - Infrastructure, facilities
LANGUAGE      - Programming languages
SKILLSET      - Technical skills
PROCESS       - Business processes
```

**spaCy Configuration**:
```python
# Model selection
MODEL_NAME = "en_core_web_md"  # Medium model with word vectors
MODEL_SIZE = ~45 MB
VECTOR_DIMENSION = 300

# Entity confidence threshold
NER_CONFIDENCE_THRESHOLD = 0.5

# Custom entity patterns (regex-based additions)
CUSTOM_PATTERNS = [
    ("AWS", "TECHNOLOGY"),
    ("Docker", "TECHNOLOGY"),
    ("Kubernetes", "TECHNOLOGY"),
    ("PostgreSQL", "TECHNOLOGY"),
    # Add domain-specific patterns
]
```

### 6.3 Keyword Extraction

**Methods**:
1. **TF-IDF Based**: Identify high-value terms
2. **TextRank**: Graph-based keyword extraction
3. **YAKE**: Unsupervised keyword extraction
4. **spaCy POS Filtering**: Extract nouns, proper nouns, adjectives

**Configuration**:
```python
# Keyword extraction settings
TOP_N_KEYWORDS = 15
MIN_KEYWORD_LENGTH = 2
KEYWORD_ALGORITHMS = ["tfidf", "textrank", "spacy_pos"]

# TF-IDF settings
TFIDF_MAX_FEATURES = 5000
TFIDF_MIN_DF = 2
TFIDF_MAX_DF = 0.8

# TextRank settings
TEXTRANK_WINDOW = 2
TEXTRANK_DAMPING = 0.85

# POS patterns for keyword extraction
KEYWORD_POS_PATTERNS = [
    "NOUN",
    "PROPN",  # Proper noun
    "ADJ",    # Adjective (technical terms)
    "VERB"    # Important verbs
]
```

### 6.4 Topic Identification

**Approach**:
- LDA (Latent Dirichlet Allocation) for topic modeling
- Or: Use document embeddings to find similar documents and their topics

**Configuration**:
```python
# LDA Parameters
NUM_TOPICS = 5  # Dynamically determined if needed
NUM_WORDS_PER_TOPIC = 10
PASSES = 10  # Number of passes over corpus
WORKERS = 4  # Parallel processing

# Topic names mapping
TOPIC_NAMES = {
    0: "Cloud Infrastructure",
    1: "Database Administration",
    2: "DevOps & Deployment",
    3: "Security & Compliance",
    4: "Application Development"
}
```

### 6.5 Embedding Generation

**Technology**: Sentence Transformers

**Model Selection**:
```python
# Recommended models (various sizes/speeds)

EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Recommended for MVP
# - Vector size: 384
# - Model size: ~80 MB
# - Inference speed: ~3000 sentences/sec on CPU
# - Memory: ~400 MB

# Alternative models:
# "all-mpnet-base-v2"
#   - Vector size: 768
#   - Model size: ~420 MB
#   - Best quality but slower
#
# "all-small-v2"
#   - Vector size: 384
#   - Model size: ~27 MB
#   - Smallest/fastest option

VECTOR_DIMENSION = 384
NORMALIZE_EMBEDDINGS = True
BATCH_SIZE = 32
```

---

## Module 7: Knowledge Extraction

**Process**:
```
NLP Output
    ├─ Entities
    ├─ Keywords
    ├─ Topics
    └─ Embeddings
    ↓
Structured Knowledge Record
    ├─ Knowledge ID
    ├─ Title
    ├─ Description
    ├─ Category
    ├─ Tags (keywords)
    ├─ Entities (structured)
    ├─ Topics
    ├─ Source Document
    ├─ Extracted Experts
    ├─ Embeddings
    ├─ Confidence Scores
    ├─ Created Date
    └─ Last Modified Date
```

**Knowledge Object Structure**:
```json
{
  "knowledge_id": "know_12345",
  "title": "AWS Production Deployment Guide",
  "description": "Complete guide for deploying applications to AWS production environment",
  "category": "Infrastructure",
  "tags": ["AWS", "deployment", "EC2", "production"],
  "entities": {
    "technologies": ["AWS", "Docker", "Jenkins"],
    "people": ["Arun Kumar"],
    "processes": ["Deployment", "Testing"],
    "systems": ["EC2", "RDS", "S3"]
  },
  "topics": ["Cloud Infrastructure", "DevOps"],
  "source_document_id": "doc_999",
  "identified_experts": [
    {"employee_id": "emp_001", "confidence": 0.95}
  ],
  "embedding": [0.234, -0.123, ...],
  "confidence_scores": {
    "entity_extraction": 0.92,
    "keyword_extraction": 0.88,
    "topic_identification": 0.85
  },
  "organization_id": "org_001",
  "created_by": "mgr_001",
  "created_at": "2024-01-15T10:30:00Z",
  "last_modified_at": "2024-01-15T10:30:00Z"
}
```

---

# 13. KNOWLEDGE LOSS DETECTION (CORE ALGORITHM)

## 13.1 Risk Factor Definitions & Calculation

### Factor 1: Knowledge Criticality (Weight: 30%)

**Definition**: How important is this knowledge to organizational operations?

**Calculation Method**:
```
Criticality Score = (Business Impact × 40%) + (System Dependencies × 30%) + (Revenue Impact × 30%)

Business Impact Scoring:
  - Affects core business process (system down) → 95
  - Affects important business process → 80
  - Affects supporting process → 60
  - Affects non-critical process → 40
  - Informational only → 20

System Dependencies:
  - Depends on legacy system (hard to replace) → 90
  - Depends on critical system → 80
  - Depends on important system → 60
  - Depends on supporting system → 40

Revenue Impact:
  - Direct revenue impact (>100K daily loss) → 95
  - Significant revenue impact (>10K daily loss) → 80
  - Moderate revenue impact (>1K daily loss) → 60
  - Minor revenue impact → 40
  - No direct revenue impact → 20
```

**Input Method**:
- Automatic detection from dependencies (if available)
- Manager assessment (survey/form)
- Historical incident data
- System criticality ratings

### Factor 2: Knowledge Uniqueness (Weight: 25%)

**Definition**: How many people possess this knowledge?

**Calculation Method**:
```
Uniqueness Score = (100 - (Number of Experts / Total Employees × 100)) × 1.25

Or:

Number of Experts:
  - 1 expert (only one person knows) → 95
  - 2 experts → 75
  - 3 experts → 60
  - 4-5 experts → 45
  - 6+ experts → 20

Formula: Uniqueness = (1 - min(num_experts, 6) / 6) × 100
```

**Data Collection**:
- NER extraction identifies mentioned persons
- Survey current employees about knowledge
- Document assignment tracking
- Project participation history

### Factor 3: Organizational Dependency (Weight: 20%)

**Definition**: How dependent is the organization on this knowledge?

**Calculation Method**:
```
Dependency Score = (Number of Dependent Systems × 20) + (Number of Dependent Processes × 15) + (Business Unit Dependency × 25)

Dependent Systems:
  - Each system/application that depends → +20 points (max 100)

Dependent Processes:
  - Each business process that requires → +15 points (max 100)

Business Unit Dependency:
  - Entire company depends → 100
  - Multiple departments depend → 80
  - Single department depends → 50
  - Small team depends → 30

Final Score = min(sum, 100)
```

**Data Sources**:
- System dependency mapping
- Process documentation
- Organizational structure analysis
- Impact assessment questionnaires

### Factor 4: Documentation Gap (Weight: 15%)

**Definition**: How well is the knowledge currently documented?

**Calculation Method**:
```
Documentation Gap Score = (100 - Documentation Quality Score)

Documentation Quality Scoring:
  - No documentation → 0 (Gap = 100)
  - Minimal documentation (< 25% coverage) → 25 (Gap = 75)
  - Partial documentation (25-50%) → 50 (Gap = 50)
  - Good documentation (50-75%) → 75 (Gap = 25)
  - Excellent documentation (75-100%) → 100 (Gap = 0)

Quality Indicators:
  - Procedure completeness
  - Clarity and understandability
  - Up-to-date status
  - Include examples/screenshots
  - Include troubleshooting
  - Include common mistakes
  - Include contact information

Assessment:
  - Automated: Check document length, structure, keywords
  - Manual: Manager/expert review
  - Combined: Weighted average
```

**Assessment Method**:
```python
def calculate_documentation_gap(document):
    # Automated assessment
    completeness = 0.0
    
    # Check for sections
    if has_introduction: completeness += 15
    if has_prerequisites: completeness += 10
    if has_step_by_step: completeness += 25
    if has_examples: completeness += 20
    if has_troubleshooting: completeness += 15
    if has_contact_info: completeness += 10
    if is_regularly_updated: completeness += 5
    
    # Document length assessment
    if word_count > 2000: completeness = min(completeness + 10, 100)
    
    gap_score = 100 - completeness
    return gap_score
```

### Factor 5: Expert Availability Risk (Weight: 10%)

**Definition**: How likely are the experts to leave or become unavailable?

**Calculation Method**:
```
Availability Risk = (Turnover Risk × 50%) + (Age/Retirement Risk × 30%) + (Skill Transition Risk × 20%)

Turnover Risk Scoring:
  - High (employee expressing intent to leave) → 95
  - Medium-High (in role < 2 years, junior) → 70
  - Medium (standard tenure, satisfaction unknown) → 50
  - Low (senior, long tenure) → 30
  - Very Low (leadership role, critical) → 10

Age/Retirement Risk:
  - Near retirement age (60+) → 80
  - Mid-career (40-59) → 40
  - Early-career (< 40) → 15

Skill Transition Risk:
  - Outdated technology → 60
  - Niche/specialized skill → 70
  - Broad skills → 20

Data Sources:
  - HR systems (if available)
  - Employee survey
  - Tenure tracking
  - Role criticality assessment
```

---

## 13.2 Risk Score Calculation Formula

### Weighted Formula

```
RISK SCORE = 
  (Criticality × 0.30) +
  (Uniqueness × 0.25) +
  (Dependency × 0.20) +
  (Documentation_Gap × 0.15) +
  (Availability_Risk × 0.10)

Where each factor is normalized to 0-100 scale
```

### Normalization

```
Normalized_Score = (Raw_Score - Min_Value) / (Max_Value - Min_Value) × 100

If any component cannot be calculated:
  - Use default/neutral value (50)
  - Mark as "Incomplete Assessment"
  - Highlight to manager for completion
```

### Risk Classification

```
0-30:       LOW Risk
  - Green indicator
  - Documented knowledge
  - Multiple experts
  - Good availability

31-60:      MEDIUM Risk
  - Yellow indicator
  - Some documentation gaps
  - Limited experts
  - Monitor availability

61-80:      HIGH Risk
  - Orange indicator
  - Poor documentation
  - Few experts
  - Action recommended

81-100:     CRITICAL Risk
  - Red indicator
  - Minimal/no documentation
  - Single expert
  - Urgent action required
```

---

## 13.3 Risk Score Calculation Examples

### Example 1: Legacy System Knowledge

```
Knowledge: Legacy Payment System Administration

Inputs:
  Criticality = 92
    (Core business system, direct revenue impact)
  Uniqueness = 95
    (Only 1 expert knows this system)
  Dependency = 85
    (4 dependent systems, multiple departments)
  Documentation_Gap = 80
    (Minimal documentation, 10-year-old system)
  Availability_Risk = 90
    (Expert near retirement, no backup)

Calculation:
  Risk Score = (92 × 0.30) + (95 × 0.25) + (85 × 0.20) + (80 × 0.15) + (90 × 0.10)
            = 27.6 + 23.75 + 17 + 12 + 9
            = 89.35

Risk Level: CRITICAL ✓

Recommendations:
  1. Create detailed documentation immediately
  2. Assign second expert for knowledge transfer
  3. Schedule knowledge-transfer sessions
  4. Record video procedures
  5. Create automation scripts where possible
```

### Example 2: General Framework Knowledge

```
Knowledge: Angular Framework Best Practices

Inputs:
  Criticality = 65
    (Important but not critical, widely available info)
  Uniqueness = 35
    (8 team members know Angular)
  Dependency = 45
    (Used in 2 applications)
  Documentation_Gap = 40
    (Some internal documentation exists)
  Availability_Risk = 20
    (Young team, low turnover risk)

Calculation:
  Risk Score = (65 × 0.30) + (35 × 0.25) + (45 × 0.20) + (40 × 0.15) + (20 × 0.10)
            = 19.5 + 8.75 + 9 + 6 + 2
            = 45.25

Risk Level: MEDIUM ✓

Recommendations:
  1. Update/enhance documentation
  2. Consider pairing newer developers
  3. Annual knowledge sharing session
  4. Monitor team composition
```

### Example 3: Well-Documented Process

```
Knowledge: Standard Deployment Process

Inputs:
  Criticality = 75
    (Important process, used regularly)
  Uniqueness = 20
    (12+ people can do this)
  Dependency = 50
    (Used by multiple teams)
  Documentation_Gap = 10
    (Comprehensive documentation with screenshots, videos)
  Availability_Risk = 15
    (Process documented, not dependent on individuals)

Calculation:
  Risk Score = (75 × 0.30) + (20 × 0.25) + (50 × 0.20) + (10 × 0.15) + (15 × 0.10)
            = 22.5 + 5 + 10 + 1.5 + 1.5
            = 40.5

Risk Level: MEDIUM (borderline LOW) ✓

Recommendations:
  1. Annual documentation review
  2. Update screenshots/videos if technology changes
  3. Maintain training for new team members
  4. Consider process automation
```

---

# 14. MACHINE LEARNING COMPONENT (PHASE 2)

## 14.1 ML Task Definition

**Problem Type**: Multi-class Classification

**Objective**: Predict knowledge-loss risk category (LOW, MEDIUM, HIGH, CRITICAL)

**Approach**: Supervised learning with trained models

## 14.2 Feature Engineering

### Input Features

```
1. Knowledge Criticality (0-100)
2. Knowledge Uniqueness (0-100)
3. Organizational Dependency (0-100)
4. Documentation Gap (0-100)
5. Expert Availability Risk (0-100)

Optional Additional Features:
6. Number of Experts
7. Average Expert Tenure (years)
8. Average Expert Age
9. Knowledge Age (years since created)
10. Document Length
11. Number of Referenced Systems
12. Industry/Domain Type
13. Regulatory Requirement Flag
14. Compliance Criticality
```

### Feature Preprocessing

```python
# Normalization
features_normalized = (features - min) / (max - min)

# Handle missing values
features_imputed = impute_with_median(features)

# Feature scaling
features_scaled = StandardScaler().fit_transform(features)
```

## 14.3 Dataset Strategy

### Data Collection

```
For MVP (Rule-Based Model):
  - Use rule-based scores as training data
  - Collect real assessments from managers
  - Blend synthetic + real data

For ML Model (After MVP):
  - Collect 500+ real risk assessments
  - Get expert validation
  - Track actual knowledge loss incidents
  - Collect feedback from managers
```

### Train/Test Split

```
Training Set: 70%
Validation Set: 15%
Test Set: 15%

Time-based split recommended:
  - Train: Historical data (months 1-6)
  - Validation: Data (months 7-8)
  - Test: Recent data (months 9-10)
```

## 14.4 Model Selection

### Recommended Models

**Model 1: Random Forest Classifier** (Recommended for MVP)
```python
RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1,
    class_weight='balanced'  # Handle class imbalance
)

Advantages:
  - Handles non-linear relationships
  - Feature importance interpretability
  - Robust to outliers
  - Good baseline performance

Disadvantages:
  - Can be slow with many features
  - May overfit
```

**Model 2: Gradient Boosting (XGBoost)**
```python
XGBClassifier(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    objective='multi:softmax',
    num_class=4,
    scale_pos_weight=1
)

Advantages:
  - Better predictive performance
  - Handle class imbalance well
  - Fast training

Disadvantages:
  - More complex to tune
  - Less interpretable
```

**Model 3: Logistic Regression (Baseline)**
```python
LogisticRegression(
    C=0.1,
    solver='lbfgs',
    max_iter=1000,
    multi_class='multinomial'
)

Advantages:
  - Interpretable
  - Fast training and prediction
  - Good baseline

Disadvantages:
  - Assumes linear relationships
  - May not capture complexity
```

## 14.5 Model Training Workflow

```
1. Data Preparation
   - Load training data
   - Handle missing values
   - Normalize features
   
2. Train/Test Split
   - 70/15/15 split
   - Stratified split for balanced classes
   
3. Model Training
   - Cross-validation (5-fold recommended)
   - Hyperparameter tuning (GridSearchCV)
   - Track training metrics
   
4. Evaluation
   - Calculate accuracy, precision, recall, F1
   - Confusion matrix analysis
   - ROC-AUC curves
   
5. Model Selection
   - Select best model
   - Final test set evaluation
   
6. Model Persistence
   - Save model as .pkl file
   - Save scaler/preprocessor
   - Version model (v1.0, v1.1, etc.)
   
7. Integration
   - Load model in FastAPI
   - Create prediction endpoint
   - Handle inference errors
   
8. Monitoring
   - Track prediction accuracy
   - Monitor model drift
   - Plan retraining schedule
```

## 14.6 Evaluation Metrics

### Classification Metrics

```
Accuracy = (TP + TN) / (TP + TN + FP + FN)
  - Overall correctness
  - Useful when classes balanced

Precision = TP / (TP + FP)
  - Of predicted HIGH/CRITICAL, how many correct?
  - Important: False alarms waste resources

Recall = TP / (TP + FN)
  - Of actual HIGH/CRITICAL, how many caught?
  - Important: Missing critical risks is bad

F1 Score = 2 × (Precision × Recall) / (Precision + Recall)
  - Harmonic mean of precision & recall
  - Balanced metric

Macro F1 = Average F1 across all classes
  - Treats all classes equally

Weighted F1 = Class-weighted F1
  - Accounts for class imbalance
```

### Target Metrics

```
Overall Accuracy: ≥ 80%
CRITICAL Class Recall: ≥ 90% (don't miss critical items)
CRITICAL Class Precision: ≥ 75% (limit false alarms)
Macro F1 Score: ≥ 0.75
```

---

# 15. SEMANTIC SEARCH IMPLEMENTATION

## 15.1 Embedding Strategy

### Generation Process

```
User Document
    ↓
Text Chunking (512 tokens, 50 token overlap)
    ↓
Generate Embeddings (SentenceTransformers)
    ↓
Normalize Embeddings (L2 norm)
    ↓
Store in pgvector
    ↓
Create Vector Indexes
    ↓
Ready for Search
```

### Configuration

```python
# Chunk parameters
CHUNK_SIZE = 512  # tokens
CHUNK_OVERLAP = 50  # tokens
MIN_CHUNK_LENGTH = 50  # characters

# Embedding model
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
VECTOR_DIMENSION = 384
NORMALIZE_EMBEDDINGS = True

# Batch processing
BATCH_SIZE = 32
POOL_STRATEGY = "mean"  # Mean pooling for sentence embeddings
```

## 15.2 Vector Storage (pgvector)

### Table Structure

```sql
CREATE TABLE embeddings (
    embedding_id SERIAL PRIMARY KEY,
    knowledge_id INT REFERENCES knowledge_items(knowledge_id),
    document_chunk_id INT,
    chunk_text TEXT,
    chunk_embedding vector(384),
    chunk_index INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for fast search
CREATE INDEX ON embeddings USING ivfflat (chunk_embedding vector_cosine_ops) 
WITH (lists = 100);

-- Alternative: HNSW index (faster, higher memory)
CREATE INDEX ON embeddings USING hnsw (chunk_embedding vector_cosine_ops) 
WITH (m = 16, ef_construction = 64);
```

### Index Configuration

```
IVFFlat Index:
  - lists: 100 (number of clusters)
  - ops: vector_cosine_ops
  - Trade-off: Memory vs speed
  - Recommended for < 1M vectors

HNSW Index:
  - m: 16 (connections per node)
  - ef_construction: 64 (search width)
  - Better for large datasets
  - Faster search, more memory
```

## 15.3 Search Workflow

```python
def semantic_search(query: str, top_k: int = 5) -> List[Dict]:
    """
    1. Convert query to embedding
    2. Search pgvector for similar embeddings
    3. Retrieve corresponding knowledge items
    4. Rank and return results
    """
    
    # Step 1: Embed query
    query_embedding = embedder.encode(query, normalize_embeddings=True)
    
    # Step 2: Search vector database
    similar_chunks = db.query("""
        SELECT embedding_id, knowledge_id, chunk_text, 
               1 - (chunk_embedding <=> %s) as similarity
        FROM embeddings
        WHERE (1 - (chunk_embedding <=> %s)) > 0.5  -- similarity threshold
        ORDER BY similarity DESC
        LIMIT %s
    """, (query_embedding, query_embedding, top_k))
    
    # Step 3: Aggregate results by knowledge_id
    # Step 4: Fetch full knowledge details
    # Step 5: Return ranked results
    
    return results
```

## 15.4 Search Performance Optimization

```
Query Optimization:
  - Cache popular searches
  - Use connection pooling
  - Async database queries
  - Batch similarity computations

Vector Index Optimization:
  - Proper index configuration
  - Regular index maintenance
  - Partition large indexes
  - Monitor index health

Caching Strategy:
  - Redis cache for search results
  - TTL: 1 hour for popular queries
  - Invalidate on document updates
```

---

# 16. DATABASE DESIGN (DETAILED)

## 16.1 Complete Schema

### Organizations Table

```sql
CREATE TABLE organizations (
    organization_id SERIAL PRIMARY KEY,
    organization_name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    industry VARCHAR(100),
    size INT CHECK (size > 0),  -- number of employees
    subscription_tier VARCHAR(50),  -- free, basic, pro, enterprise
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    
    CONSTRAINT org_name_length CHECK (LENGTH(organization_name) >= 3)
);

CREATE INDEX idx_org_active ON organizations(is_active);
```

### Users Table

```sql
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    organization_id INT NOT NULL REFERENCES organizations(organization_id) ON DELETE CASCADE,
    email VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,  -- bcrypt, 12 rounds
    full_name VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('admin', 'manager', 'employee')),
    department_id INT REFERENCES departments(department_id),
    is_active BOOLEAN DEFAULT TRUE,
    email_verified BOOLEAN DEFAULT FALSE,
    verification_token VARCHAR(255),
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(organization_id, email),
    CONSTRAINT email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$')
);

CREATE INDEX idx_user_org_email ON users(organization_id, email);
CREATE INDEX idx_user_is_active ON users(is_active);
```

### Departments Table

```sql
CREATE TABLE departments (
    department_id SERIAL PRIMARY KEY,
    organization_id INT NOT NULL REFERENCES organizations(organization_id) ON DELETE CASCADE,
    department_name VARCHAR(255) NOT NULL,
    description TEXT,
    parent_department_id INT REFERENCES departments(department_id),  -- for hierarchies
    manager_id INT REFERENCES users(user_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(organization_id, department_name),
    CHECK (parent_department_id IS NULL OR parent_department_id != department_id)
);

CREATE INDEX idx_dept_org ON departments(organization_id);
```

### Employees Table

```sql
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL UNIQUE REFERENCES users(user_id) ON DELETE CASCADE,
    organization_id INT NOT NULL REFERENCES organizations(organization_id) ON DELETE CASCADE,
    department_id INT REFERENCES departments(department_id),
    expertise_areas JSONB DEFAULT '[]',  -- ["Python", "AWS", "Docker"]
    expertise_level VARCHAR(50) CHECK (expertise_level IN ('beginner', 'intermediate', 'expert')),
    job_title VARCHAR(255),
    status VARCHAR(50) CHECK (status IN ('active', 'on_leave', 'inactive', 'left')),
    joined_date DATE,
    last_active_date TIMESTAMP,
    bio TEXT,
    skill_summary TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_emp_org ON employees(organization_id);
CREATE INDEX idx_emp_status ON employees(status);
CREATE INDEX idx_emp_expertise ON employees USING GIN (expertise_areas);
```

### Documents Table

```sql
CREATE TABLE documents (
    document_id SERIAL PRIMARY KEY,
    organization_id INT NOT NULL REFERENCES organizations(organization_id) ON DELETE CASCADE,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    file_name VARCHAR(500),
    file_path VARCHAR(1000),  -- encrypted storage path
    file_size INT,  -- bytes
    file_type VARCHAR(20) CHECK (file_type IN ('pdf', 'docx', 'txt')),
    mime_type VARCHAR(100),
    content_hash VARCHAR(64),  -- SHA-256 for dedup
    language VARCHAR(10) DEFAULT 'en',
    pages INT,  -- for PDF
    uploaded_by INT REFERENCES users(user_id),
    source_type VARCHAR(50),  -- manual_upload, email, api, etc.
    extraction_status VARCHAR(50) CHECK (extraction_status IN ('pending', 'processing', 'completed', 'failed')),
    extraction_error TEXT,
    processed_at TIMESTAMP,
    is_verified BOOLEAN DEFAULT FALSE,
    is_archived BOOLEAN DEFAULT FALSE,
    retention_date DATE,  -- when to delete
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP,  -- soft delete
    
    UNIQUE(organization_id, content_hash)
);

CREATE INDEX idx_doc_org ON documents(organization_id);
CREATE INDEX idx_doc_status ON documents(extraction_status);
CREATE INDEX idx_doc_archived ON documents(is_archived);
```

### Document Chunks Table

```sql
CREATE TABLE document_chunks (
    chunk_id SERIAL PRIMARY KEY,
    document_id INT NOT NULL REFERENCES documents(document_id) ON DELETE CASCADE,
    chunk_index INT NOT NULL,
    chunk_text TEXT NOT NULL,
    token_count INT,
    start_position INT,  -- character position in original
    end_position INT,
    page_number INT,  -- for PDF
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_chunk_doc ON document_chunks(document_id);
```

### Knowledge Items Table

```sql
CREATE TABLE knowledge_items (
    knowledge_id SERIAL PRIMARY KEY,
    organization_id INT NOT NULL REFERENCES organizations(organization_id) ON DELETE CASCADE,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    subcategory VARCHAR(100),
    tags JSONB DEFAULT '[]',
    source_document_id INT REFERENCES documents(document_id),
    knowledge_type VARCHAR(50),  -- procedure, troubleshooting, architecture, etc.
    status VARCHAR(50) CHECK (status IN ('draft', 'active', 'archived', 'obsolete')),
    is_verified BOOLEAN DEFAULT FALSE,
    verified_by INT REFERENCES users(user_id),
    verified_at TIMESTAMP,
    confidence_score DECIMAL(3,2),  -- 0.00 to 1.00
    extraction_method VARCHAR(50),  -- manual, nlp_extracted, ai_generated
    created_by INT REFERENCES users(user_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_accessed TIMESTAMP,
    access_count INT DEFAULT 0
);

CREATE INDEX idx_knowledge_org ON knowledge_items(organization_id);
CREATE INDEX idx_knowledge_category ON knowledge_items(category);
CREATE INDEX idx_knowledge_status ON knowledge_items(status);
CREATE INDEX idx_knowledge_tags ON knowledge_items USING GIN (tags);
```

### Entities Table

```sql
CREATE TABLE entities (
    entity_id SERIAL PRIMARY KEY,
    knowledge_id INT REFERENCES knowledge_items(knowledge_id) ON DELETE CASCADE,
    document_id INT REFERENCES documents(document_id) ON DELETE CASCADE,
    entity_name VARCHAR(500) NOT NULL,
    entity_type VARCHAR(50) NOT NULL,  -- person, technology, organization, etc.
    confidence DECIMAL(3,2),
    context TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(knowledge_id, entity_name, entity_type)
);

CREATE INDEX idx_entity_type ON entities(entity_type);
CREATE INDEX idx_entity_name ON entities(entity_name);
```

### Keywords Table

```sql
CREATE TABLE keywords (
    keyword_id SERIAL PRIMARY KEY,
    knowledge_id INT REFERENCES knowledge_items(knowledge_id) ON DELETE CASCADE,
    keyword VARCHAR(255) NOT NULL,
    frequency INT,  -- how many times appears
    tf_idf_score DECIMAL(5,4),
    extraction_method VARCHAR(50),  -- tfidf, textrank, nlp, manual
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(knowledge_id, keyword)
);

CREATE INDEX idx_keyword_knowledge ON keywords(knowledge_id);
CREATE INDEX idx_keyword_text ON keywords(keyword);
```

### Knowledge Experts Table

```sql
CREATE TABLE knowledge_experts (
    id SERIAL PRIMARY KEY,
    knowledge_id INT NOT NULL REFERENCES knowledge_items(knowledge_id) ON DELETE CASCADE,
    employee_id INT NOT NULL REFERENCES employees(employee_id) ON DELETE CASCADE,
    expertise_level VARCHAR(50) CHECK (expertise_level IN ('beginner', 'intermediate', 'expert')),
    is_primary_expert BOOLEAN DEFAULT FALSE,
    years_of_experience INT,
    confidence_score DECIMAL(3,2),
    identified_by VARCHAR(50),  -- nlp_extracted, manual, survey
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(knowledge_id, employee_id)
);

CREATE INDEX idx_kexp_knowledge ON knowledge_experts(knowledge_id);
CREATE INDEX idx_kexp_employee ON knowledge_experts(employee_id);
CREATE INDEX idx_kexp_primary ON knowledge_experts(is_primary_expert);
```

### Risk Scores Table

```sql
CREATE TABLE risk_scores (
    risk_id SERIAL PRIMARY KEY,
    organization_id INT NOT NULL REFERENCES organizations(organization_id) ON DELETE CASCADE,
    knowledge_id INT NOT NULL REFERENCES knowledge_items(knowledge_id) ON DELETE CASCADE,
    
    -- Individual risk factors (0-100)
    criticality DECIMAL(5,2),
    uniqueness DECIMAL(5,2),
    dependency DECIMAL(5,2),
    documentation_gap DECIMAL(5,2),
    availability_risk DECIMAL(5,2),
    
    -- Overall score (0-100)
    risk_score DECIMAL(5,2),
    risk_level VARCHAR(50) CHECK (risk_level IN ('low', 'medium', 'high', 'critical')),
    
    -- ML prediction (if applicable)
    ml_predicted_level VARCHAR(50),
    ml_confidence DECIMAL(3,2),
    prediction_model_version VARCHAR(50),
    
    -- Assessment details
    assessment_method VARCHAR(50),  -- rule_based, ml, hybrid
    assessed_by INT REFERENCES users(user_id),
    assessment_notes TEXT,
    
    -- Tracking
    is_latest BOOLEAN DEFAULT TRUE,
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    next_review_date DATE
);

CREATE INDEX idx_risk_org ON risk_scores(organization_id);
CREATE INDEX idx_risk_knowledge ON risk_scores(knowledge_id);
CREATE INDEX idx_risk_level ON risk_scores(risk_level);
CREATE INDEX idx_risk_latest ON risk_scores(is_latest);
```

### Embeddings Table

```sql
CREATE TABLE embeddings (
    embedding_id SERIAL PRIMARY KEY,
    knowledge_id INT REFERENCES knowledge_items(knowledge_id) ON DELETE CASCADE,
    document_chunk_id INT REFERENCES document_chunks(chunk_id) ON DELETE CASCADE,
    embedding vector(384),  -- 384-dim vector from all-MiniLM-L6-v2
    embedding_model VARCHAR(100) DEFAULT 'all-MiniLM-L6-v2',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Vector similarity index (IVFFlat - good for < 1M vectors)
CREATE INDEX idx_embedding_vector ON embeddings USING ivfflat (embedding vector_cosine_ops) 
WITH (lists = 100);

-- Alternative HNSW index (faster but more memory)
-- CREATE INDEX idx_embedding_vector ON embeddings USING hnsw (embedding vector_cosine_ops);

-- Regular indexes for retrieval
CREATE INDEX idx_embedding_knowledge ON embeddings(knowledge_id);
CREATE INDEX idx_embedding_chunk ON embeddings(document_chunk_id);
```

### Preservation Actions Table

```sql
CREATE TABLE preservation_actions (
    action_id SERIAL PRIMARY KEY,
    organization_id INT NOT NULL REFERENCES organizations(organization_id) ON DELETE CASCADE,
    knowledge_id INT NOT NULL REFERENCES knowledge_items(knowledge_id) ON DELETE CASCADE,
    action_type VARCHAR(100),  -- documentation, knowledge_transfer, secondary_expert, etc.
    action_description TEXT,
    priority VARCHAR(50) CHECK (priority IN ('low', 'medium', 'high', 'critical')),
    status VARCHAR(50) CHECK (status IN ('recommended', 'planned', 'in_progress', 'completed', 'cancelled')),
    assigned_to INT REFERENCES users(user_id),
    assigned_at TIMESTAMP,
    deadline DATE,
    completion_date DATE,
    completion_notes TEXT,
    estimated_hours INT,
    actual_hours INT,
    created_by INT REFERENCES users(user_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_action_org ON preservation_actions(organization_id);
CREATE INDEX idx_action_knowledge ON preservation_actions(knowledge_id);
CREATE INDEX idx_action_status ON preservation_actions(status);
CREATE INDEX idx_action_assigned_to ON preservation_actions(assigned_to);
```

### Audit Logs Table

```sql
CREATE TABLE audit_logs (
    log_id SERIAL PRIMARY KEY,
    organization_id INT REFERENCES organizations(organization_id) ON DELETE SET NULL,
    user_id INT REFERENCES users(user_id) ON DELETE SET NULL,
    action_type VARCHAR(100),  -- create, read, update, delete, export, etc.
    resource_type VARCHAR(100),  -- document, knowledge, risk, user, etc.
    resource_id INT,
    resource_name VARCHAR(500),
    old_value JSONB,  -- Previous state (for updates)
    new_value JSONB,  -- New state (for updates)
    ip_address INET,
    user_agent TEXT,
    status VARCHAR(50),  -- success, failure
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_org ON audit_logs(organization_id);
CREATE INDEX idx_audit_user ON audit_logs(user_id);
CREATE INDEX idx_audit_resource ON audit_logs(resource_type, resource_id);
CREATE INDEX idx_audit_timestamp ON audit_logs(created_at);
CREATE INDEX idx_audit_action ON audit_logs(action_type);
```

### ML Models Table (For Model Versioning)

```sql
CREATE TABLE ml_models (
    model_id SERIAL PRIMARY KEY,
    organization_id INT NOT NULL REFERENCES organizations(organization_id),
    model_name VARCHAR(255),
    model_type VARCHAR(100),  -- random_forest, xgboost, etc.
    version VARCHAR(50),
    model_path VARCHAR(500),  -- path to saved model file
    scaler_path VARCHAR(500),  -- path to feature scaler
    
    -- Performance metrics
    accuracy DECIMAL(5,4),
    precision DECIMAL(5,4),
    recall DECIMAL(5,4),
    f1_score DECIMAL(5,4),
    
    -- Training info
    training_data_size INT,
    training_samples INT,
    features_used JSONB,
    hyperparameters JSONB,
    
    is_active BOOLEAN DEFAULT FALSE,  -- current production model
    trained_at TIMESTAMP,
    deployed_at TIMESTAMP,
    performance_notes TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_model_org ON ml_models(organization_id);
CREATE INDEX idx_model_active ON ml_models(is_active);
```

---

# 17. API SPECIFICATIONS (DETAILED)

## 17.1 API Overview

- **Base URL**: `https://api.knowledgeloss.com/v1`
- **Authentication**: JWT Bearer Token
- **Content-Type**: `application/json`
- **Response Format**: JSON
- **API Version**: 1.0
- **Rate Limit**: 100 requests/minute per user

## 17.2 Authentication Endpoints

### Register User
```
POST /auth/register

Request:
{
  "email": "user@company.com",
  "password": "SecurePassword123!",
  "full_name": "John Doe",
  "organization_name": "Acme Corp",
  "organization_size": 100
}

Response (201 Created):
{
  "user_id": 123,
  "email": "user@company.com",
  "organization_id": 456,
  "message": "Verification email sent",
  "verification_pending": true
}

Error Response (400 Bad Request):
{
  "error_code": "ERR-AUTH-001",
  "message": "Email already registered",
  "details": "user@company.com is already registered"
}
```

### Verify Email
```
POST /auth/verify-email

Request:
{
  "email": "user@company.com",
  "verification_code": "ABC123DEF456"
}

Response (200 OK):
{
  "verified": true,
  "message": "Email verified successfully"
}
```

### Login
```
POST /auth/login

Request:
{
  "email": "user@company.com",
  "password": "SecurePassword123!"
}

Response (200 OK):
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user_id": 123,
  "role": "manager"
}
```

### Refresh Token
```
POST /auth/refresh

Request Headers:
Authorization: Bearer {refresh_token}

Response (200 OK):
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 3600
}
```

### Logout
```
POST /auth/logout

Request Headers:
Authorization: Bearer {access_token}

Response (200 OK):
{
  "message": "Logged out successfully"
}
```

---

## 17.3 Document Endpoints

### Upload Document
```
POST /documents/upload

Request:
Content-Type: multipart/form-data

Parameters:
  file: (File) The document to upload
  title: (string) Document title
  description: (string) Optional description

Response (202 Accepted):
{
  "document_id": 999,
  "status": "processing",
  "message": "Document uploaded and queued for processing",
  "estimated_time": "30 seconds"
}
```

### Get All Documents
```
GET /documents?page=1&limit=20&status=completed

Response (200 OK):
{
  "total": 142,
  "page": 1,
  "limit": 20,
  "documents": [
    {
      "document_id": 999,
      "title": "AWS Deployment Guide",
      "file_type": "pdf",
      "uploaded_by": "John Doe",
      "uploaded_at": "2024-01-15T10:30:00Z",
      "status": "completed",
      "knowledge_items_count": 5
    }
  ]
}
```

### Get Document Details
```
GET /documents/{document_id}

Response (200 OK):
{
  "document_id": 999,
  "title": "AWS Deployment Guide",
  "description": "...",
  "file_type": "pdf",
  "pages": 45,
  "file_size": 2048000,
  "uploaded_by": "John Doe",
  "uploaded_at": "2024-01-15T10:30:00Z",
  "status": "completed",
  "processed_at": "2024-01-15T10:35:00Z",
  "chunks_created": 12,
  "entities_extracted": 28,
  "keywords_extracted": 45,
  "language": "en",
  "knowledge_items": [
    {
      "knowledge_id": 123,
      "title": "AWS EC2 Deployment",
      "risk_level": "high"
    }
  ]
}
```

### Delete Document
```
DELETE /documents/{document_id}

Response (204 No Content):
(empty body)

Error Response (404 Not Found):
{
  "error_code": "ERR-DOC-001",
  "message": "Document not found",
  "document_id": 999
}
```

---

## 17.4 Knowledge Endpoints

### Create Knowledge Item
```
POST /knowledge

Request:
{
  "title": "AWS Production Deployment",
  "description": "Step-by-step guide for deploying...",
  "category": "Infrastructure",
  "tags": ["AWS", "deployment", "production"],
  "source_document_id": 999,
  "experts": [
    {
      "employee_id": 1,
      "expertise_level": "expert",
      "is_primary": true
    }
  ]
}

Response (201 Created):
{
  "knowledge_id": 123,
  "title": "AWS Production Deployment",
  "created_at": "2024-01-15T10:30:00Z",
  "status": "active"
}
```

### Get All Knowledge
```
GET /knowledge?category=Infrastructure&risk_level=high&page=1&limit=20

Response (200 OK):
{
  "total": 456,
  "page": 1,
  "limit": 20,
  "knowledge_items": [
    {
      "knowledge_id": 123,
      "title": "AWS Production Deployment",
      "category": "Infrastructure",
      "risk_level": "high",
      "risk_score": 82,
      "experts_count": 2,
      "documentation_status": "partial"
    }
  ]
}
```

### Get Knowledge Details
```
GET /knowledge/{knowledge_id}

Response (200 OK):
{
  "knowledge_id": 123,
  "title": "AWS Production Deployment",
  "description": "...",
  "category": "Infrastructure",
  "tags": ["AWS", "deployment", "production"],
  "status": "active",
  "access_count": 145,
  "last_accessed": "2024-01-15T14:30:00Z",
  "experts": [
    {
      "employee_id": 1,
      "name": "Arun Kumar",
      "expertise_level": "expert",
      "is_primary": true
    }
  ],
  "risk_analysis": {
    "risk_score": 82,
    "risk_level": "high",
    "criticality": 92,
    "uniqueness": 95,
    "dependency": 85,
    "documentation_gap": 80,
    "availability_risk": 90
  },
  "preservation_actions": [
    {
      "action_id": 456,
      "action_type": "documentation",
      "status": "in_progress"
    }
  ]
}
```

### Update Knowledge
```
PUT /knowledge/{knowledge_id}

Request:
{
  "title": "AWS Production Deployment - Updated",
  "description": "...",
  "tags": ["AWS", "deployment", "production", "2024"]
}

Response (200 OK):
{
  "knowledge_id": 123,
  "updated_at": "2024-01-15T15:45:00Z",
  "message": "Knowledge item updated successfully"
}
```

---

## 17.5 Risk Analysis Endpoints

### Analyze Risk
```
POST /risk/analyze/{knowledge_id}

Request:
{
  "force_recalculate": true,
  "assessment_method": "manual",
  "factors": {
    "criticality": 92,
    "uniqueness": 95,
    "dependency": 85,
    "documentation_gap": 80,
    "availability_risk": 90
  }
}

Response (200 OK):
{
  "risk_id": 789,
  "knowledge_id": 123,
  "risk_score": 87.35,
  "risk_level": "critical",
  "factors": {
    "criticality": 92,
    "uniqueness": 95,
    "dependency": 85,
    "documentation_gap": 80,
    "availability_risk": 90
  },
  "recommendations": [
    "Create detailed documentation",
    "Assign secondary expert",
    "Conduct knowledge transfer sessions"
  ],
  "calculated_at": "2024-01-15T15:45:00Z"
}
```

### Get Risk Dashboard
```
GET /risk/dashboard?organization_id=456

Response (200 OK):
{
  "summary": {
    "total_knowledge_items": 256,
    "critical_risk_count": 12,
    "high_risk_count": 34,
    "medium_risk_count": 78,
    "low_risk_count": 132,
    "average_risk_score": 45.2
  },
  "risk_distribution": {
    "critical": 4.7,
    "high": 13.3,
    "medium": 30.5,
    "low": 51.5
  },
  "top_critical_items": [
    {
      "knowledge_id": 123,
      "title": "Legacy Payment System",
      "risk_score": 95,
      "experts": 1
    }
  ],
  "preservation_progress": {
    "recommended": 45,
    "planned": 12,
    "in_progress": 8,
    "completed": 3
  }
}
```

---

## 17.6 Search Endpoints

### Semantic Search
```
GET /search?q=how+to+deploy+aws+application&limit=10

Response (200 OK):
{
  "query": "how to deploy aws application",
  "total_results": 23,
  "results": [
    {
      "knowledge_id": 123,
      "title": "AWS Production Deployment Guide",
      "description": "...",
      "relevance_score": 0.94,
      "snippet": "...step-by-step process for deploying applications to AWS production environment...",
      "category": "Infrastructure",
      "risk_level": "high"
    },
    {
      "knowledge_id": 124,
      "title": "Docker Deployment Procedure",
      "relevance_score": 0.82,
      "snippet": "...deployment using Docker containers...",
      "category": "DevOps"
    }
  ],
  "search_time_ms": 45
}
```

---

## 17.7 Preservation Actions Endpoints

### Create Preservation Action
```
POST /preservation-actions

Request:
{
  "knowledge_id": 123,
  "action_type": "documentation",
  "action_description": "Create comprehensive documentation for legacy system",
  "priority": "critical",
  "assigned_to": 2,
  "deadline": "2024-02-15"
}

Response (201 Created):
{
  "action_id": 456,
  "knowledge_id": 123,
  "status": "planned",
  "created_at": "2024-01-15T16:00:00Z"
}
```

### Get Preservation Actions
```
GET /preservation-actions?status=in_progress&assigned_to=2

Response (200 OK):
{
  "actions": [
    {
      "action_id": 456,
      "knowledge_id": 123,
      "action_type": "documentation",
      "status": "in_progress",
      "priority": "critical",
      "deadline": "2024-02-15",
      "assigned_to": "John Doe",
      "completion_percentage": 45
    }
  ]
}
```

---

# 18. ERROR HANDLING STRATEGY

## 18.1 Error Code System

All errors follow the pattern: `ERR-MODULE-XXX`

### Authentication Errors (ERR-AUTH-xxx)
```
ERR-AUTH-001: Email already registered
ERR-AUTH-002: Invalid credentials
ERR-AUTH-003: Email not verified
ERR-AUTH-004: Account locked (too many login attempts)
ERR-AUTH-005: Token expired
ERR-AUTH-006: Invalid token
ERR-AUTH-007: Missing required authentication
```

### Document Errors (ERR-DOC-xxx)
```
ERR-DOC-001: Document not found
ERR-DOC-002: Invalid file format
ERR-DOC-003: File too large (max 50 MB)
ERR-DOC-004: Document processing failed
ERR-DOC-005: Insufficient storage quota
ERR-DOC-006: Malware detected in file
```

### Knowledge Errors (ERR-KNOW-xxx)
```
ERR-KNOW-001: Knowledge item not found
ERR-KNOW-002: Invalid knowledge data
ERR-KNOW-003: Duplicate knowledge item
ERR-KNOW-004: Cannot delete knowledge with active dependencies
```

### Risk Analysis Errors (ERR-RISK-xxx)
```
ERR-RISK-001: Risk calculation failed
ERR-RISK-002: Insufficient data for risk assessment
ERR-RISK-003: Invalid risk factors provided
```

### Search Errors (ERR-SEARCH-xxx)
```
ERR-SEARCH-001: Search query too long
ERR-SEARCH-002: Search service unavailable
ERR-SEARCH-003: Invalid search filters
```

### Permission Errors (ERR-PERM-xxx)
```
ERR-PERM-001: Insufficient permissions
ERR-PERM-002: Access denied to resource
ERR-PERM-003: Organization access denied
```

### Validation Errors (ERR-VAL-xxx)
```
ERR-VAL-001: Required field missing
ERR-VAL-002: Invalid field format
ERR-VAL-003: Invalid enum value
ERR-VAL-004: Constraint violation
```

### Server Errors (ERR-SRV-xxx)
```
ERR-SRV-001: Internal server error
ERR-SRV-002: Database connection error
ERR-SRV-003: External service unavailable
ERR-SRV-004: Rate limit exceeded
```

## 18.2 Error Response Format

```json
{
  "error_code": "ERR-DOC-002",
  "message": "Invalid file format",
  "http_status": 400,
  "details": {
    "allowed_formats": ["pdf", "docx", "txt"],
    "received_format": "xlsx"
  },
  "timestamp": "2024-01-15T16:30:00Z",
  "request_id": "req_abc123def456",
  "user_message": "Only PDF, DOCX, and TXT files are supported. Please try again.",
  "suggestions": [
    "Convert your file to PDF or DOCX format",
    "Check file extension matches actual format"
  ]
}
```

## 18.3 HTTP Status Codes

```
200 OK - Request successful
201 Created - Resource created
202 Accepted - Request accepted for processing
204 No Content - Successful, no content to return

400 Bad Request - Invalid input
401 Unauthorized - Authentication required
403 Forbidden - Permission denied
404 Not Found - Resource not found
409 Conflict - Resource conflict (e.g., duplicate)
413 Payload Too Large - File/request too large
429 Too Many Requests - Rate limit exceeded
500 Internal Server Error - Server error
502 Bad Gateway - External service error
503 Service Unavailable - Maintenance/down
```

---

# 19. MONITORING, LOGGING & ALERTING

## 19.1 Logging Strategy

### Log Levels

```
DEBUG   - Detailed information for debugging
INFO    - General informational messages
WARNING - Warning about potential issues
ERROR   - Error conditions
CRITICAL - Critical system failures
```

### Structured Logging Format

```json
{
  "timestamp": "2024-01-15T16:30:45.123Z",
  "level": "INFO",
  "logger": "app.services.knowledge",
  "request_id": "req_abc123def456",
  "user_id": 123,
  "organization_id": 456,
  "message": "Knowledge item created successfully",
  "action": "create_knowledge",
  "resource_type": "knowledge",
  "resource_id": 789,
  "duration_ms": 234,
  "status": "success",
  "metadata": {
    "knowledge_title": "AWS Deployment",
    "category": "Infrastructure",
    "source": "document_upload"
  }
}
```

### Log Collection (ELK Stack)

```yaml
# Logstash Configuration
input:
  beats:
    port: 5000

filter:
  grok:
    match: { "message" => "%{TIMESTAMP_ISO8601:timestamp} %{LOGLEVEL:level} %{DATA:logger} %{GREEDYDATA:message}" }

output:
  elasticsearch:
    hosts: ["elasticsearch:9200"]
    index: "application-logs-%{+YYYY.MM.dd}"

# Retention: 30 days for hot index, 90 days archive
```

### Key Metrics to Log

1. **API Performance**
   - Request/response time
   - Request size
   - Response status code
   - Endpoint path
   - Method (GET, POST, etc.)

2. **NLP Processing**
   - Document processing time
   - NER extraction results
   - Keyword extraction count
   - Embedding generation time
   - Confidence scores

3. **Database Operations**
   - Query execution time
   - Slow query identification (> 1000ms)
   - Connection pool status
   - Transaction duration

4. **System Health**
   - CPU usage
   - Memory usage
   - Disk space
   - Database connections
   - Cache hit/miss rates

5. **Business Events**
   - Document uploaded
   - Knowledge item created
   - Risk score calculated
   - Preservation action assigned
   - Search performed

## 19.2 Metrics & Monitoring (Prometheus)

### Application Metrics

```python
# Prometheus metrics
from prometheus_client import Counter, Histogram, Gauge

# Request metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint'],
    buckets=(0.1, 0.5, 1.0, 2.5, 5.0)
)

# NLP metrics
nlp_processing_duration_seconds = Histogram(
    'nlp_processing_duration_seconds',
    'NLP processing time',
    ['operation'],  # ner, keywords, embeddings
    buckets=(1, 5, 10, 30, 60)
)

# Business metrics
knowledge_items_total = Counter(
    'knowledge_items_total',
    'Total knowledge items created',
    ['category', 'risk_level']
)

# Resource metrics
active_users_gauge = Gauge(
    'active_users_gauge',
    'Number of active users'
)

database_connection_pool_gauge = Gauge(
    'database_connection_pool_gauge',
    'Database connection pool size',
    ['status']  # available, in_use
)
```

## 19.3 Alerting Rules

### Critical Alerts

```yaml
# Alert: API Response Time High
- alert: APIResponseTimeHigh
  expr: histogram_quantile(0.95, http_request_duration_seconds) > 2
  for: 5m
  annotations:
    summary: "API response time is high"
    description: "95th percentile response time > 2s"

# Alert: Document Processing Failed
- alert: DocumentProcessingError
  expr: rate(document_processing_errors_total[5m]) > 0.1
  for: 5m
  annotations:
    summary: "High document processing error rate"
    description: "Error rate > 10% over last 5 minutes"

# Alert: Database Connection Pool Exhausted
- alert: DBConnectionPoolLow
  expr: database_connection_pool_gauge{status="available"} < 5
  for: 2m
  annotations:
    summary: "Database connection pool low"
    description: "Available connections < 5"

# Alert: Search Service Unavailable
- alert: SearchServiceDown
  expr: up{job="elasticsearch"} == 0
  for: 1m
  annotations:
    summary: "Elasticsearch service down"
    description: "Search service unavailable"

# Alert: Error Rate High
- alert: ErrorRateHigh
  expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.01
  for: 5m
  annotations:
    summary: "High error rate detected"
    description: "5xx error rate > 1%"
```

## 19.4 Visualization (Grafana Dashboards)

```
Dashboard 1: System Health
  - API response time (p50, p95, p99)
  - Error rate (by endpoint)
  - Request rate (by method)
  - Database performance
  - Cache hit rate

Dashboard 2: NLP Processing
  - Document processing time
  - NER extraction metrics
  - Keyword extraction count
  - Embedding generation time
  - Model inference latency

Dashboard 3: Business Metrics
  - Total documents processed
  - Knowledge items created
  - Risk assessments completed
  - Preservation actions assigned
  - Active users

Dashboard 4: Infrastructure
  - CPU usage
  - Memory usage
  - Disk space
  - Network bandwidth
  - Database connections
```

---

# 20. SECURITY IMPLEMENTATION

## 20.1 Authentication & Authorization

### Password Security
```python
import bcrypt

# Password hashing
PASSWORD_HASH_ROUNDS = 12

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=PASSWORD_HASH_ROUNDS)
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

# Password policy
PASSWORD_MIN_LENGTH = 12
PASSWORD_REQUIRE_UPPERCASE = True
PASSWORD_REQUIRE_LOWERCASE = True
PASSWORD_REQUIRE_NUMBERS = True
PASSWORD_REQUIRE_SPECIAL = True  # @#$%^&*
PASSWORD_EXPIRY_DAYS = 90
PASSWORD_HISTORY = 5  # Can't reuse last 5 passwords
```

### JWT Token Management
```python
# JWT Configuration
JWT_ALGORITHM = "HS256"
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")  # Stored in environment
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 hour
JWT_REFRESH_TOKEN_EXPIRE_DAYS = 7
JWT_ALGORITHM_CHOICES = ["HS256"]  # Only allow HS256

# Token Structure
{
  "sub": "user_id",
  "org": "organization_id",
  "role": "manager",
  "exp": 1234567890,
  "iat": 1234567890,
  "jti": "unique_token_id"  # JWT Token Identifier
}

# Token Revocation List (maintain in Redis)
# When user logs out or password changes, add token JTI to revocation list
```

### Role-Based Access Control (RBAC)

```python
ROLES = {
    "admin": {
        "permissions": [
            "manage_users",
            "manage_organizations",
            "view_audit_logs",
            "system_configuration"
        ]
    },
    "manager": {
        "permissions": [
            "upload_documents",
            "create_knowledge",
            "view_risk_analysis",
            "assign_preservation_tasks",
            "view_team_knowledge"
        ]
    },
    "employee": {
        "permissions": [
            "submit_knowledge",
            "view_knowledge",
            "participate_in_knowledge_transfer"
        ]
    }
}

# Decorator for permission checking
def require_permission(permission: str):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            current_user = get_current_user()
            if not has_permission(current_user.role, permission):
                raise HTTPException(status_code=403, detail="Permission denied")
            return await func(*args, **kwargs)
        return wrapper
    return decorator
```

## 20.2 Data Security

### Encryption at Rest
```python
# Database encryption
# - Use PostgreSQL built-in encryption
# - Enable pg_crypto extension for column-level encryption

# File storage encryption
from cryptography.fernet import Fernet

ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
cipher_suite = Fernet(ENCRYPTION_KEY)

def encrypt_file(file_path: str) -> str:
    with open(file_path, 'rb') as f:
        plaintext = f.read()
    encrypted = cipher_suite.encrypt(plaintext)
    # Save encrypted file
    return encrypted_path

def decrypt_file(encrypted_path: str) -> bytes:
    with open(encrypted_path, 'rb') as f:
        encrypted = f.read()
    plaintext = cipher_suite.decrypt(encrypted)
    return plaintext
```

### Encryption in Transit
```
# HTTPS/TLS Configuration
- Minimum TLS version: 1.2
- Recommended: TLS 1.3
- Certificate: Let's Encrypt (auto-renewal)
- Cipher suites: Only strong ciphers
- HSTS: Enable HTTP Strict Transport Security
  - max-age: 31536000 (1 year)
  - includeSubDomains: true
  - preload: true
```

## 20.3 Input Validation & Sanitization

```python
from pydantic import BaseModel, Field, EmailStr, validator

# Pydantic models for validation
class RegisterUserRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=12, max_length=128)
    full_name: str = Field(min_length=2, max_length=255)
    organization_name: str = Field(min_length=3, max_length=255)
    
    @validator('password')
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain uppercase')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain lowercase')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain numbers')
        # Check special characters
        special_chars = set("!@#$%^&*()_+-=[]{}|;:',.<>?/`~")
        if not any(c in special_chars for c in v):
            raise ValueError('Password must contain special characters')
        return v

# File upload validation
ALLOWED_FILE_TYPES = ['pdf', 'docx', 'txt']
ALLOWED_MIME_TYPES = [
    'application/pdf',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'text/plain'
]
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB

def validate_upload(file: UploadFile) -> bool:
    # Check file size
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large")
    
    # Check MIME type
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    # Check file extension (verify it matches MIME type)
    file_ext = file.filename.split('.')[-1].lower()
    if file_ext not in ALLOWED_FILE_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file extension")
    
    return True

# SQL Injection prevention (use ORM/parameterized queries)
# ✓ GOOD: SQLAlchemy ORM automatically parameterizes
query = db.query(Knowledge).filter(Knowledge.title == title)

# ✗ BAD: String interpolation (vulnerable)
query = db.query(f"SELECT * FROM knowledge WHERE title = '{title}'")
```

## 20.4 Rate Limiting & DDoS Protection

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

# Global rate limit
@app.get("/api/documents")
@limiter.limit("100/minute")
async def list_documents(request: Request):
    pass

# Per-user rate limit
@app.post("/auth/login")
@limiter.limit("5/minute")
async def login(request: Request, credentials: LoginRequest):
    pass

# DDoS Protection
# - Use CloudFlare or similar
# - Implement request throttling
# - Monitor traffic patterns
# - Implement CAPTCHA for suspicious activity
```

## 20.5 Audit Logging

```python
# Log all security-relevant actions
async def create_audit_log(
    user_id: int,
    action_type: str,
    resource_type: str,
    resource_id: int,
    old_value: dict = None,
    new_value: dict = None,
    status: str = "success",
    error_message: str = None
):
    log = AuditLog(
        user_id=user_id,
        action_type=action_type,  # create, read, update, delete, export
        resource_type=resource_type,
        resource_id=resource_id,
        old_value=old_value,
        new_value=new_value,
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent"),
        status=status,
        error_message=error_message,
        created_at=datetime.now(timezone.utc)
    )
    db.add(log)
    await db.commit()
```

## 20.6 Security Headers

```python
# Add security headers to all responses
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    
    # Content Security Policy
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'"
    
    # X-Content-Type-Options
    response.headers["X-Content-Type-Options"] = "nosniff"
    
    # X-Frame-Options
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    
    # X-XSS-Protection
    response.headers["X-XSS-Protection"] = "1; mode=block"
    
    # HSTS
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
    
    # Referrer-Policy
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    
    return response
```

---

# 21. PERFORMANCE OPTIMIZATION

## 21.1 Caching Strategy

### Redis Caching

```python
import redis
import json

redis_client = redis.Redis(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True,
    socket_connect_timeout=5
)

# Cache configuration
CACHE_TTL_SECONDS = {
    'search_results': 3600,      # 1 hour
    'user_session': 86400,       # 24 hours
    'knowledge_item': 1800,      # 30 minutes
    'risk_score': 3600,          # 1 hour
    'organization_config': 86400 # 24 hours
}

# Cache decorator
def cache_result(ttl_key: str):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{args}:{kwargs}"
            
            # Try to get from cache
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
            
            # Compute result
            result = await func(*args, **kwargs)
            
            # Store in cache
            ttl = CACHE_TTL_SECONDS.get(ttl_key, 3600)
            redis_client.setex(
                cache_key,
                ttl,
                json.dumps(result)
            )
            
            return result
        return wrapper
    return decorator
```

### Database Query Optimization

```python
# Use eager loading to prevent N+1 queries
# BAD: N+1 query problem
knowledge_items = db.query(Knowledge).all()
for item in knowledge_items:
    experts = item.experts  # Queries database for each item!

# GOOD: Eager load relationships
from sqlalchemy.orm import joinedload
knowledge_items = db.query(Knowledge).options(
    joinedload(Knowledge.experts),
    joinedload(Knowledge.risk_scores),
    joinedload(Knowledge.entities)
).all()

# Use pagination
@app.get("/knowledge")
async def list_knowledge(skip: int = 0, limit: int = 20):
    # GOOD: Paginate results
    items = db.query(Knowledge).offset(skip).limit(limit).all()
    total = db.query(Knowledge).count()
    return {"items": items, "total": total}
```

### Connection Pooling

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,           # Initial connections
    max_overflow=40,        # Additional connections under load
    pool_recycle=3600,      # Recycle connections every hour
    pool_pre_ping=True,     # Verify connections before use
    echo=False              # Disable SQL logging in production
)
```

---

# 22. TESTING STRATEGY (COMPREHENSIVE)

## 22.1 Unit Tests

```python
# tests/test_nlp_processing.py

import pytest
from app.nlp.preprocessing import preprocess_text

def test_preprocess_text_removes_stopwords():
    text = "The quick brown fox jumps over the lazy dog"
    result = preprocess_text(text)
    assert "the" not in result.lower()
    assert "brown" in result.lower()

def test_preprocess_text_handles_special_characters():
    text = "Hello, World! @#$%"
    result = preprocess_text(text)
    assert "@#$%" not in result

@pytest.mark.asyncio
async def test_ner_extraction():
    from app.nlp.ner import extract_entities
    text = "John works at Amazon in Seattle"
    entities = await extract_entities(text)
    assert any(e['type'] == 'PERSON' and e['text'] == 'John' for e in entities)
    assert any(e['type'] == 'ORG' and e['text'] == 'Amazon' for e in entities)

def test_risk_score_calculation():
    from app.risk.scoring import calculate_risk_score
    score = calculate_risk_score(
        criticality=92,
        uniqueness=95,
        dependency=85,
        documentation_gap=80,
        availability_risk=90
    )
    assert 81 <= score <= 100  # Should be in CRITICAL range
    assert isinstance(score, (int, float))

# Test coverage target: 80%+ for all modules
pytest --cov=app --cov-report=html
```

## 22.2 Integration Tests

```python
# tests/test_integration_document_workflow.py

@pytest.mark.asyncio
async def test_document_upload_and_nlp_processing():
    # 1. Upload document
    with open("sample.pdf", "rb") as f:
        response = await client.post(
            "/documents/upload",
            files={"file": f},
            data={"title": "Test Document"}
        )
    assert response.status_code == 202
    doc_id = response.json()["document_id"]
    
    # 2. Wait for processing
    await asyncio.sleep(2)
    
    # 3. Verify document processed
    response = await client.get(f"/documents/{doc_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "completed"
    assert response.json()["chunks_created"] > 0
    
    # 4. Verify knowledge extracted
    assert response.json()["entities_extracted"] > 0
    assert response.json()["keywords_extracted"] > 0
```

## 22.3 API/End-to-End Tests

```python
# tests/test_api_endpoints.py

@pytest.mark.asyncio
async def test_create_and_search_knowledge():
    # Create knowledge
    response = await client.post(
        "/knowledge",
        json={
            "title": "AWS Deployment",
            "description": "How to deploy on AWS",
            "category": "Infrastructure"
        }
    )
    assert response.status_code == 201
    knowledge_id = response.json()["knowledge_id"]
    
    # Search for knowledge
    response = await client.get(
        "/search?q=aws+deployment"
    )
    assert response.status_code == 200
    results = response.json()["results"]
    assert any(r["knowledge_id"] == knowledge_id for r in results)
```

## 22.4 Performance Tests

```python
# tests/test_performance.py

@pytest.mark.asyncio
async def test_search_performance():
    # Ensure search completes within SLA
    start_time = time.time()
    response = await client.get("/search?q=aws+deployment&limit=20")
    end_time = time.time()
    
    duration_ms = (end_time - start_time) * 1000
    assert duration_ms < 500, f"Search took {duration_ms}ms, target < 500ms"
    assert response.json()["search_time_ms"] < 200  # DB query time

@pytest.mark.asyncio
async def test_nlp_processing_speed():
    # Document processing should complete in reasonable time
    import time
    start = time.time()
    
    # Process document
    with open("large_document.pdf", "rb") as f:
        response = await client.post(
            "/documents/upload",
            files={"file": f}
        )
    
    # Wait for completion
    doc_id = response.json()["document_id"]
    while True:
        resp = await client.get(f"/documents/{doc_id}")
        if resp.json()["status"] == "completed":
            break
        await asyncio.sleep(1)
    
    duration = time.time() - start
    assert duration < 60, f"Document processing took {duration}s, target < 60s"
```

## 22.5 Security Tests

```python
# tests/test_security.py

@pytest.mark.asyncio
async def test_sql_injection_prevention():
    # Try SQL injection in search query
    response = await client.get(
        "/search?q=test'; DROP TABLE knowledge; --"
    )
    assert response.status_code == 200
    # Should not actually execute DROP TABLE

@pytest.mark.asyncio
async def test_cross_site_scripting_prevention():
    # Try XSS in knowledge title
    response = await client.post(
        "/knowledge",
        json={
            "title": "<script>alert('xss')</script>",
            "description": "Test"
        }
    )
    # Should sanitize or reject

@pytest.mark.asyncio
async def test_cross_organization_access_prevention():
    # Create knowledge in org1
    # Try to access from org2 user
    response = await client.get(
        f"/knowledge/{org1_knowledge_id}",
        headers={"Authorization": f"Bearer {org2_token}"}
    )
    assert response.status_code == 403  # Forbidden

@pytest.mark.asyncio
async def test_unauthorized_access():
    response = await client.get("/documents/123")
    assert response.status_code == 401  # Unauthorized
```

---

# 23. DEPLOYMENT & DEVOPS

## 23.1 Containerization (Docker)

### Dockerfile (Backend)

```dockerfile
# Multi-stage build for production
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Create wheels
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy wheels from builder
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

# Install Python packages
RUN pip install --no-cache /wheels/*

# Copy application
COPY ./app ./app
COPY ./config ./config

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: ${DB_NAME}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init-scripts/init-pgvector.sql:/docker-entrypoint-initdb.d/01-pgvector.sql
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build: ./backend
    environment:
      DATABASE_URL: "postgresql://${DB_USER}:${DB_PASSWORD}@db:5432/${DB_NAME}"
      REDIS_URL: "redis://redis:6379/0"
      JWT_SECRET_KEY: ${JWT_SECRET_KEY}
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ./backend:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    environment:
      REACT_APP_API_URL: "http://localhost:8000"

  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.10.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
    ports:
      - "9200:9200"
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data

  kibana:
    image: docker.elastic.co/kibana/kibana:8.10.0
    ports:
      - "5601:5601"
    environment:
      ELASTICSEARCH_HOSTS: "http://elasticsearch:9200"

volumes:
  postgres_data:
  redis_data:
  elasticsearch_data:
```

## 23.2 CI/CD Pipeline (GitHub Actions)

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        cache: 'pip'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt pytest pytest-cov
    
    - name: Run unit tests
      run: pytest tests/unit --cov=app --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
    
    - name: Run integration tests
      env:
        DATABASE_URL: "postgresql://postgres:postgres@localhost:5432/test"
      run: pytest tests/integration
    
    - name: Set up Node
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        cache: 'npm'
        cache-dependency-path: frontend/package-lock.json
    
    - name: Frontend build and test
      run: |
        cd frontend
        npm install
        npm run build
        npm test

  security:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Run Bandit (Python security)
      run: |
        pip install bandit
        bandit -r app/ -f json -o bandit-report.json || true
    
    - name: Run npm audit (JavaScript)
      run: |
        cd frontend
        npm audit --audit-level=moderate

  deploy:
    needs: [test, security]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Build and push Docker images
      uses: docker/build-push-action@v4
      with:
        context: ./backend
        push: true
        tags: ${{ secrets.DOCKER_REGISTRY }}/knowledge-loss-backend:latest
    
    - name: Deploy to production
      run: |
        # SSH into production server and pull latest images
        ssh -i ${{ secrets.SSH_KEY }} ${{ secrets.SERVER_USER }}@${{ secrets.SERVER_IP }} <<'EOF'
        cd /opt/knowledge-platform
        docker-compose pull
        docker-compose up -d
        EOF
```

---

# 24. DISASTER RECOVERY & BACKUP

## 24.1 Backup Strategy

### Database Backups

```bash
#!/bin/bash
# backup-database.sh

BACKUP_DIR="/backups/database"
RETENTION_DAYS=30
DB_NAME="knowledge_platform"
DB_USER="postgres"
DB_HOST="localhost"

# Daily full backup
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/full_backup_$DATE.sql.gz"

pg_dump -h $DB_HOST -U $DB_USER -d $DB_NAME | gzip > $BACKUP_FILE

# Upload to S3
aws s3 cp $BACKUP_FILE s3://knowledge-platform-backups/database/

# Cleanup old backups (older than RETENTION_DAYS)
find $BACKUP_DIR -type f -name "full_backup_*.sql.gz" -mtime +$RETENTION_DAYS -delete

# Test backup integrity
gunzip -t $BACKUP_FILE
if [ $? -eq 0 ]; then
    echo "Backup integrity check passed"
else
    echo "Backup integrity check failed"
    exit 1
fi
```

### File Storage Backups

```bash
#!/bin/bash
# backup-files.sh

STORAGE_DIR="/var/knowledge-platform/storage"
S3_BUCKET="knowledge-platform-backups"

# Daily incremental backup to S3
aws s3 sync $STORAGE_DIR s3://$S3_BUCKET/storage/ \
    --delete \
    --storage-class GLACIER_IR \
    --sse AES256

# Keep versioning enabled in S3 for point-in-time recovery
```

### Backup Schedule

```
Hourly: Application logs
Daily: Database full backup
Weekly: Database backup + file backup to S3
Monthly: Archive to cold storage (Glacier)

Retention Policy:
- Daily backups: 7 days
- Weekly backups: 4 weeks
- Monthly archives: 1 year
- Point-in-time recovery: Last 24 hours
```

## 24.2 Disaster Recovery Plan

### Recovery Time Objectives (RTO)

```
Critical Systems (RTO: 1 hour)
- Authentication service
- Knowledge repository
- Search functionality

Important Systems (RTO: 4 hours)
- Risk analysis engine
- Document processing

Non-critical Systems (RTO: 24 hours)
- Reporting
- Analytics
- Knowledge graph
```

### Recovery Point Objectives (RPO)

```
Database: RPO = 1 hour (hourly incremental backups)
Files: RPO = 1 day (daily backups)
Configuration: RPO = 0 (version controlled in Git)
```

### Recovery Procedures

```yaml
Database Failure Recovery:
  1. Stop application servers
  2. Restore database from latest backup
  3. Apply transaction logs if available (for point-in-time)
  4. Run integrity checks
  5. Restart application servers
  6. Verify data consistency
  Estimated time: 30 minutes

File Storage Failure Recovery:
  1. Restore files from S3 backup
  2. Verify file integrity (checksum validation)
  3. Restart application
  Estimated time: 15 minutes

Complete Infrastructure Failure:
  1. Provision new infrastructure from IaC (Terraform)
  2. Restore database from backup
  3. Restore files from S3
  4. Deploy application via CI/CD
  5. Update DNS to point to new infrastructure
  Estimated time: 2 hours

Testing:
  - Monthly backup restoration test
  - Quarterly full disaster recovery drill
  - Document lessons learned
  - Update procedures based on test results
```

---

# 25. DATA MANAGEMENT & RETENTION

## 25.1 Data Retention Policy

```
Active Data (Production):
- User accounts: Retained while active
- Documents: Retained per organization policy (default 2 years)
- Knowledge items: Retained while not obsolete
- Risk assessments: Retained for 18 months
- Audit logs: Retained for 12 months
- Session logs: Retained for 90 days

Archived Data (Cold Storage):
- Documents older than 2 years: Move to S3 Glacier
- Audit logs older than 1 year: Archive and compress
- Preserve for 7 years for compliance

Deleted Data:
- User initiated deletion: Soft delete (30-day grace period)
- After 30 days: Hard delete from production
- After 1 year: Delete from backups
```

## 25.2 Data Deletion Procedures (GDPR Right to be Forgotten)

```python
async def delete_user_data(user_id: int):
    """
    Delete all personal data associated with a user.
    Complies with GDPR Article 17.
    """
    
    # 1. Mark user as deleted (soft delete)
    user = await db.query(Users).filter(Users.user_id == user_id).first()
    user.deleted_at = datetime.now(timezone.utc)
    
    # 2. Anonymize user-specific data
    await db.query(AuditLogs).filter(
        AuditLogs.user_id == user_id
    ).update({
        'user_id': None,
        'user_agent': '[REDACTED]',
        'ip_address': None
    })
    
    # 3. Remove user from knowledge expert relationships
    await db.query(KnowledgeExperts).filter(
        KnowledgeExperts.employee_id == user_id
    ).delete()
    
    # 4. Remove from preservation action assignments
    await db.query(PreservationActions).filter(
        PreservationActions.assigned_to == user_id
    ).update({'assigned_to': None})
    
    # 5. Schedule deletion of soft-deleted user after 30 days
    schedule_permanent_deletion(user_id, delay_days=30)
    
    # 6. Log the deletion
    await create_audit_log(
        action_type='user_deletion',
        resource_type='user',
        resource_id=user_id,
        status='success'
    )
```

---

# 26. ACCESSIBILITY & UX STANDARDS

## 26.1 WCAG 2.1 Level AA Compliance

```
✓ Color Contrast: Minimum 4.5:1 for normal text, 3:1 for large text
✓ Keyboard Navigation: All features accessible via keyboard
✓ Screen Reader: Compatible with NVDA, JAWS, VoiceOver
✓ Focus Indicators: Clear focus states on all interactive elements
✓ Form Labels: All form fields labeled properly
✓ Alt Text: All images have descriptive alt text
✓ Language: HTML lang attribute set correctly
✓ Error Messages: Clear, descriptive error messages
✓ Motion: Respect prefers-reduced-motion setting
✓ Font Size: Adjustable to at least 200%
```

### Implementation

```jsx
// React accessibility example
function SearchComponent() {
  const [query, setQuery] = useState('');
  
  return (
    <section aria-labelledby="search-heading">
      <h2 id="search-heading">Knowledge Search</h2>
      
      <label htmlFor="search-input" className="sr-only">
        Search knowledge items
      </label>
      <input
        id="search-input"
        type="search"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search by keyword, technology, or process"
        aria-describedby="search-tips"
        aria-label="Search knowledge items"
      />
      
      <p id="search-tips" className="search-tips">
        Tip: Use quotes for exact phrases, e.g. "AWS deployment"
      </p>
      
      <button
        type="submit"
        onClick={handleSearch}
        aria-busy={isLoading}
      >
        {isLoading ? 'Searching...' : 'Search'}
      </button>
      
      {error && (
        <div role="alert" className="error-message">
          {error}
        </div>
      )}
    </section>
  );
}
```

## 26.2 Responsive Design

```
Mobile (< 768px):
  - Single column layout
  - Touch-friendly buttons (min 48x48px)
  - Stacked navigation

Tablet (768px - 1024px):
  - Two column layout
  - Adjusted spacing
  - Optimized for touch and mouse

Desktop (> 1024px):
  - Full multi-column layout
  - Sidebar navigation
  - Hover states for interactions
```

---

# 27. SUCCESS METRICS & KPIS

## 27.1 Technical Metrics

```
API Performance:
- Response time (p95): < 500ms
- Error rate: < 0.1%
- Uptime: > 99.9% (4.3 hours/month allowed)

NLP Processing:
- Document processing time: < 30 seconds (per 50 pages)
- NER accuracy: > 85%
- Entity extraction confidence: > 0.8

Search:
- Query response time: < 200ms
- Results relevance: > 80% precision
- Search throughput: > 1000 queries/second

Database:
- Query response time (p95): < 100ms
- Connection pool utilization: 40-80%
- Backup success rate: 100%
```

## 27.2 Business Metrics

```
User Adoption:
- Active users per month
- User registration growth rate
- Feature adoption rate

Knowledge Management:
- Documents uploaded per month
- Knowledge items created per month
- Knowledge update frequency

Risk Management:
- Risk assessments completed
- Critical knowledge identified
- Preservation actions assigned vs. completed
- Knowledge retention improvement

ROI Metrics:
- Average time to recover knowledge
- Knowledge loss incidents prevented
- Cost savings from preserved knowledge
```

## 27.3 Monitoring Dashboard Queries

```sql
-- Daily active users
SELECT DATE(last_active_date) as date, COUNT(DISTINCT user_id) as active_users
FROM users
WHERE deleted_at IS NULL
GROUP BY DATE(last_active_date)
ORDER BY date DESC;

-- Knowledge items by risk level (daily)
SELECT 
    DATE(rs.calculated_at) as date,
    rs.risk_level,
    COUNT(*) as count
FROM risk_scores rs
WHERE rs.is_latest = true
GROUP BY DATE(rs.calculated_at), rs.risk_level
ORDER BY date DESC;

-- Document processing metrics
SELECT
    DATE(d.created_at) as date,
    COUNT(*) as total_documents,
    COUNT(CASE WHEN d.extraction_status = 'completed' THEN 1 END) as completed,
    AVG(EXTRACT(EPOCH FROM (d.processed_at - d.created_at))) as avg_processing_time_seconds
FROM documents d
WHERE d.organization_id = %s
GROUP BY DATE(d.created_at)
ORDER BY date DESC;
```

---

# 28. DOCUMENTATION STANDARDS

## 28.1 Code Documentation

### Python Docstrings (Google Style)

```python
def calculate_risk_score(
    criticality: float,
    uniqueness: float,
    dependency: float,
    documentation_gap: float,
    availability_risk: float
) -> float:
    """
    Calculate knowledge-loss risk score using weighted formula.
    
    Implements the core risk assessment algorithm combining five risk factors
    using pre-determined weights to produce a normalized 0-100 score.
    
    Args:
        criticality: Business criticality score (0-100).
            Measure of how essential the knowledge is to operations.
        uniqueness: Knowledge uniqueness score (0-100).
            Inverse measure of number of people who possess the knowledge.
        dependency: Organizational dependency score (0-100).
            Measure of how many systems/processes depend on this knowledge.
        documentation_gap: Documentation gap score (0-100).
            Measure of how poorly the knowledge is documented (100 = not documented).
        availability_risk: Expert availability risk (0-100).
            Risk that experts may become unavailable (retirement, turnover).
    
    Returns:
        float: Calculated risk score (0-100).
            0-30: LOW risk
            31-60: MEDIUM risk
            61-80: HIGH risk
            81-100: CRITICAL risk
    
    Raises:
        ValueError: If any factor is outside 0-100 range.
        TypeError: If factors are not numeric.
    
    Example:
        >>> score = calculate_risk_score(92, 95, 85, 80, 90)
        >>> print(score)
        89.35
    
    Note:
        Weights are:
        - Criticality: 30%
        - Uniqueness: 25%
        - Dependency: 20%
        - Documentation Gap: 15%
        - Availability Risk: 10%
    """
    # Validate inputs
    for factor in [criticality, uniqueness, dependency, documentation_gap, availability_risk]:
        if not isinstance(factor, (int, float)):
            raise TypeError(f"Factor must be numeric, got {type(factor)}")
        if not 0 <= factor <= 100:
            raise ValueError(f"Factor must be between 0-100, got {factor}")
    
    # Calculate weighted sum
    risk_score = (
        criticality * 0.30 +
        uniqueness * 0.25 +
        dependency * 0.20 +
        documentation_gap * 0.15 +
        availability_risk * 0.10
    )
    
    return round(risk_score, 2)
```

### React Component Documentation

```jsx
/**
 * RiskDashboard - Displays comprehensive knowledge-loss risk overview
 * 
 * This component provides a high-level summary of organizational knowledge risks,
 * including risk distribution, top critical items, and preservation progress.
 * 
 * @component
 * @param {Object} props - Component props
 * @param {number} props.organizationId - Organization ID for data filtering
 * @param {boolean} [props.autoRefresh=true] - Auto-refresh data every 5 minutes
 * @param {function} [props.onCriticalItemClick] - Callback when critical item is clicked
 * 
 * @returns {React.ReactNode} Rendered risk dashboard
 * 
 * @example
 * <RiskDashboard 
 *   organizationId={456}
 *   autoRefresh={true}
 *   onCriticalItemClick={(itemId) => navigate(`/knowledge/${itemId}`)}
 * />
 * 
 * @throws {Error} If organizationId is invalid
 * 
 * @dependencies
 * - useQuery (React Query) for data fetching
 * - Chart.js for visualization
 * - Material-UI for components
 */
function RiskDashboard({ organizationId, autoRefresh = true, onCriticalItemClick }) {
  // Implementation...
}
```

## 28.2 API Documentation (OpenAPI/Swagger)

```python
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

app = FastAPI(
    title="Enterprise Knowledge Platform",
    description="NLP-driven platform for knowledge loss detection and preservation",
    version="1.0.0"
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Knowledge Platform API",
        version="1.0.0",
        description="Complete API documentation",
        routes=app.routes,
    )
    # Add custom metadata
    openapi_schema["info"]["x-logo"] = {
        "url": "https://example.com/logo.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/knowledge/{knowledge_id}")
async def get_knowledge(knowledge_id: int):
    """
    Retrieve detailed information about a specific knowledge item.
    
    This endpoint returns comprehensive details about a knowledge item including:
    - Basic information (title, description, category)
    - Associated entities and keywords
    - Risk assessment details
    - Assigned experts
    - Preservation actions
    - Access history
    
    **Requires**: Authentication token with at least 'employee' role
    
    **Rate limit**: 100 requests/minute
    
    Args:
        knowledge_id: Unique identifier of the knowledge item
    
    Returns:
        KnowledgeDetailResponse: Complete knowledge item details
    
    Raises:
        401: Unauthorized (missing or invalid token)
        403: Forbidden (no access to this organization's knowledge)
        404: Knowledge item not found
        429: Rate limit exceeded
    """
```

---

# 29. COST ANALYSIS

## 29.1 Infrastructure Costs (Monthly, for 100 organizations)

```
Compute:
  - API Server (AWS EC2 t3.large): $70/month
  - Background Workers: $50/month
  - Subtotal: $120/month

Database:
  - PostgreSQL RDS (db.t3.medium): $150/month
  - Backup storage (100GB): $5/month
  - Subtotal: $155/month

Storage:
  - Application data (S3): $50/month
  - Document backups (S3): $30/month
  - Archive storage (Glacier): $10/month
  - Subtotal: $90/month

Services:
  - CloudFlare CDN/DDoS: $20/month
  - Email service (SendGrid): $10/month
  - Monitoring (DataDog): $50/month
  - Subtotal: $80/month

Total Infrastructure: $445/month ($5,340/year)
```

## 29.2 Development Costs

```
Initial Development (MVP):
  - Team of 4 developers × 3 months
  - Average salary: $80,000/year
  - Cost: 4 × $80,000 × 0.25 = $80,000

Maintenance & Enhancement (Year 1):
  - 1 FTE: $80,000
  - 50% additional support: $40,000
  - Total: $120,000/year

Infrastructure Operations:
  - 0.5 FTE DevOps: $50,000/year
```

## 29.3 ROI Calculation

```
Annual Revenue (SaaS Model):
  - Free Tier: Limited organizations
  - Pro Tier: $500/month × 50 orgs = $30,000/month = $360,000/year
  - Enterprise: $2,000/month × 10 orgs = $20,000/month = $240,000/year
  - Total: $600,000/year

Annual Costs:
  - Infrastructure: $5,340
  - Development: $120,000
  - Ops: $50,000
  - Total: $175,340/year

Net Profit (Year 1): $424,660 (71% margin)
Payback Period: ~3 months
```

---

# 30. RISK MANAGEMENT PLAN

## 30.1 Technical Risks

```
Risk: NLP Model Accuracy Degradation
  Probability: Medium
  Impact: High
  Mitigation:
    - Regular model retraining on new data
    - Continuous accuracy monitoring
    - Fallback to rule-based system if accuracy drops
    - Version all models with rollback capability

Risk: Vector Similarity Search False Positives
  Probability: Medium
  Impact: Medium
  Mitigation:
    - Adjust similarity threshold based on testing
    - Hybrid search (semantic + keyword)
    - Manual verification for critical searches
    - User feedback loop for result quality

Risk: Database Performance Degradation
  Probability: Low
  Impact: High
  Mitigation:
    - Regular index optimization
    - Query performance monitoring
    - Archive old data periodically
    - Capacity planning for growth
    - Read replicas for high-volume searches

Risk: Security Breach / Data Leak
  Probability: Low
  Impact: Critical
  Mitigation:
    - Regular penetration testing
    - Bug bounty program
    - Security headers and encryption
    - Access control and audit logging
    - Incident response plan
    - Cyber insurance
```

## 30.2 Schedule Risks

```
Risk: Underestimated Development Effort
  Probability: Medium
  Impact: Medium
  Mitigation:
    - Agile methodology with 2-week sprints
    - Regular progress tracking
    - Clear MVP definition
    - Buffer time (20%) in estimates

Risk: Scope Creep
  Probability: High
  Impact: High
  Mitigation:
    - Define MVP features strictly
    - Phase 2/3 features planned separately
    - Change control process
    - Stakeholder approval for scope changes
```

## 30.3 Resource Risks

```
Risk: Key Team Member Departure
  Probability: Low
  Impact: High
  Mitigation:
    - Knowledge documentation
    - Pair programming
    - Cross-training team members
    - Clear code/documentation standards
    - Competitive compensation

Risk: Insufficient Budget
  Probability: Low
  Impact: High
  Mitigation:
    - Clear cost tracking
    - Regular budget reviews
    - Prioritize MVP features
    - Consider cloud cost optimization
```

---

# 31. EXAMPLE USE CASES WITH DATA

## Use Case 1: Legacy System Knowledge (High Risk)

```
Scenario:
  Organization: TechCorp (500 employees)
  System: Legacy Payment Processing (built 2005, Java)
  Sole Expert: Rajesh Kumar (15 years tenure, age 57)

Current State:
  - Documentation: Minimal (50-page word doc, outdated)
  - Other Knowledge: Only Rajesh knows the system
  - Business Impact: Processes $5M daily transactions
  - System Age: 19 years old
  - Maintenance: Critical bug fixes only

Risk Assessment:
  Criticality: 95
    - Direct revenue: $5M daily = $1.8B annually
    - System failure would stop transactions
    - No backup system exists
  
  Uniqueness: 98
    - Rajesh is the only expert
    - Documentation is outdated
    - Younger employees avoid this "legacy" work
  
  Dependency: 92
    - Used by 8 business processes
    - Connected to 5 critical systems
    - Finance team depends entirely on it
  
  Documentation Gap: 85
    - Design documentation outdated
    - No troubleshooting guide
    - No runbook for common issues
  
  Availability Risk: 90
    - Rajesh approaching retirement (2-3 years)
    - Has expressed desire to mentor
    - High job satisfaction though

Risk Score: (95×0.30) + (98×0.25) + (92×0.20) + (85×0.15) + (90×0.10)
          = 28.5 + 24.5 + 18.4 + 12.75 + 9
          = 93.15 → CRITICAL

Recommended Actions:
  1. URGENT: Create comprehensive documentation
     - Architecture & design diagrams
     - Database schema documentation
     - Key algorithms & business logic
     - Common troubleshooting procedures
     Assigned to: Rajesh + 2 junior developers
     Deadline: 30 days
     Est. 120 hours

  2. URGENT: Designate 2 Secondary Experts
     - Identify 2 junior/mid-level developers
     - Pair them with Rajesh for intensive training
     Assigned to: Rajesh + HR
     Deadline: 60 days
     Est. 200 hours (training time)

  3. HIGH: Record Video Procedures
     - Deployment procedures
     - Emergency procedures
     - Bug fix workflows
     Assigned to: Rajesh
     Deadline: 45 days
     Est. 40 hours

  4. MEDIUM: Create Modernization Plan
     - Assess feasibility of system replacement
     - Plan for gradual migration if needed
     Assigned to: Architecture team
     Deadline: 90 days

Preservation Progress:
  Week 1: Documentation started
  Week 2: Secondary experts identified
  Week 3: Documentation 30% complete, training begins
  Week 4: Video recording started
  Week 8: Documentation 80% complete
  Week 12: All actions complete, knowledge preserved
  
Impact:
  - Knowledge loss risk reduced from 93 → 25 (LOW)
  - Rajesh retirement can be planned smoothly
  - Organization has knowledge continuity
  - Faster onboarding for new developers
```

## Use Case 2: Well-Managed Knowledge (Low Risk)

```
Scenario:
  Organization: ModernSoft (200 employees)
  Knowledge: Kubernetes Deployment Pipeline
  Experts: 8 engineers (ages 30-45)

Current State:
  - Documentation: Comprehensive (wiki + runbooks + videos)
  - Team Knowledge: 8 experts, regularly updated
  - Business Impact: Important but not critical
  - System Age: 3 years
  - Automation: 95% automated

Risk Assessment:
  Criticality: 60
    - Supports development but not customer-facing
    - Deployment failures delay releases (not revenue impact)
    - Can manually deploy if system fails
  
  Uniqueness: 25
    - 8 different engineers know the pipeline
    - New engineers learn in 2 weeks
    - Knowledge is well-distributed
  
  Dependency: 45
    - Used by 1 team for deployments
    - Can fall back to manual process
  
  Documentation Gap: 15
    - Comprehensive wiki documentation
    - Video tutorials available
    - Runbooks for all scenarios
    - Regular updates (monthly)
  
  Availability Risk: 20
    - Young, stable team
    - Low turnover history
    - Knowledge transferable
    - Easily replaceable expertise

Risk Score: (60×0.30) + (25×0.25) + (45×0.20) + (15×0.15) + (20×0.10)
          = 18 + 6.25 + 9 + 2.25 + 2
          = 37.5 → MEDIUM (borderline LOW)

Recommended Actions:
  1. ROUTINE: Update documentation quarterly
     Assigned to: Any team member
     Effort: 4 hours/quarter

  2. ROUTINE: Annual knowledge sharing session
     Assigned to: Team lead
     Effort: 2 hours/year

  3. OPTIONAL: Consider automation expansion
     Assigned to: Interested team member
     Effort: Exploratory

Monitoring:
  - Review quarterly if still current
  - Monitor team composition changes
  - Trigger HIGH risk if team changes significantly
```

---

# 32. COMPREHENSIVE EXAMPLE: COMPLETE WORKFLOW

## Complete Scenario: From Upload to Risk Mitigation

### Step 1: Document Upload

```
User (Manager): John Doe
Date: 2024-01-20 14:30 UTC
File: "AWS_Database_Migration_Procedure.pdf" (45 pages, 2.3 MB)
Title: "Database Migration to AWS RDS"
Description: "Complete procedure for migrating on-premises databases to AWS"
Organization: GlobalTech Inc. (org_id: 789)
```

### Step 2: Automatic Processing

```
Processing Timeline:
14:30 - Document uploaded
14:31 - File validation passed
14:32 - Text extraction started (PyMuPDF)
14:35 - Text extraction completed (12,450 words extracted)
14:36 - Text preprocessing started
14:37 - Preprocessing completed
14:38 - NLP analysis started

NLP Results:
  NER Extraction:
    - PERSON: ["Arun Kumar", "Priya Sharma", "David Chen"] (Confidence: 0.92)
    - TECHNOLOGY: ["AWS RDS", "MySQL", "PostgreSQL", "DMS", "Oracle"] (Confidence: 0.95)
    - ORGANIZATION: ["GlobalTech", "AWS"] (Confidence: 0.94)
    - PROCESS: ["Migration", "Backup", "Testing", "Failover"] (Confidence: 0.88)
    - LOCATION: ["us-east-1", "us-west-2"] (Confidence: 0.91)
    Total entities: 28

  Keyword Extraction (TF-IDF):
    Top 15: ["RDS", "database", "migration", "backup", "AWS", "MySQL", "schema", 
             "failover", "replication", "testing", "performance", "security", 
             "monitoring", "automation", "compliance"]
    
  Topic Identification:
    Primary Topic: "Database Administration" (Confidence: 0.93)
    Secondary Topics: "Cloud Migration" (0.87), "DevOps" (0.81)
    
  Embeddings: Generated 24 chunk embeddings (512 tokens each, 50 token overlap)
  
14:40 - NLP processing completed
14:41 - Knowledge item creation started
14:42 - Knowledge item created successfully
```

### Step 3: Knowledge Creation

```json
{
  "knowledge_id": 5678,
  "title": "AWS Database Migration Procedure",
  "description": "Complete step-by-step procedure for migrating on-premises databases to AWS RDS with backup, testing, and failover procedures",
  "category": "Database Administration",
  "tags": ["AWS", "RDS", "database", "migration", "backup", "high-availability"],
  "source_document_id": 4567,
  "identified_experts": [
    {
      "employee_id": 123,
      "name": "Arun Kumar",
      "confidence": 0.92,
      "expertise_level": "expert",
      "is_primary": true
    },
    {
      "employee_id": 124,
      "name": "Priya Sharma",
      "confidence": 0.78,
      "expertise_level": "intermediate"
    }
  ],
  "entities": [
    {"type": "TECHNOLOGY", "name": "AWS RDS", "context": "Primary cloud database service"},
    {"type": "TECHNOLOGY", "name": "MySQL", "context": "Source database engine"},
    {"type": "PROCESS", "name": "Migration", "context": "Main process described"}
  ],
  "keywords": 15,
  "entities_count": 28,
  "confidence_scores": {
    "entity_extraction": 0.92,
    "keyword_extraction": 0.87,
    "topic_identification": 0.90
  },
  "status": "active",
  "created_at": "2024-01-20T14:42:00Z"
}
```

### Step 4: Risk Assessment

```
Risk Factor Analysis:

Criticality Assessment:
  - Affects 4 critical systems (score: 20 pts)
  - Direct revenue impact: $200K per hour downtime (score: 25 pts)
  - Regulatory requirement: Yes (score: 20 pts)
  - Frequency of use: Daily (score: 15 pts)
  - Impact severity: Very High (score: 15 pts)
  → Criticality Score: 95

Uniqueness Assessment:
  - Identified experts: 2 (Arun Kumar, Priya Sharma)
  - Expertise level: 1 expert + 1 intermediate
  - Cross-training status: Limited
  - Document mention: Limited (score: 90)
  → Uniqueness Score: 90

Dependency Assessment:
  - Dependent systems: 4 (Oracle, MySQL, PostgreSQL backends)
  - Business processes: 3 (data warehousing, analytics, reporting)
  - Critical for operations: Yes
  → Dependency Score: 85

Documentation Assessment:
  - Current documentation: This document (good)
  - Completeness: 80% (has procedures, examples, troubleshooting)
  - Update frequency: First upload (score: 80)
  - Accessibility: Stored in knowledge platform
  → Documentation Gap Score: 20 (good documentation)

Availability Risk Assessment:
  - Arun Kumar: 12 years tenure, age 42, low turnover risk (score: 30)
  - Priya Sharma: 5 years tenure, age 38, low turnover risk (score: 35)
  - Overall team: Stable (score: 35)
  → Availability Risk Score: 33

Final Risk Calculation:
  Risk Score = (95×0.30) + (90×0.25) + (85×0.20) + (20×0.15) + (33×0.10)
            = 28.5 + 22.5 + 17 + 3 + 3.3
            = 74.3 → HIGH RISK
```

### Step 5: Automated Recommendations

```
Risk Level: HIGH (74.3/100)

The system recommends the following preservation actions:

PRIORITY 1 - ASSIGN SECONDARY EXPERT
  - Current Experts: 1 (Arun Kumar) expert, 1 intermediate
  - Recommendation: Assign 2 additional team members for knowledge transfer
  - Duration: 4-6 weeks of intensive training
  - Success Criteria: Can independently perform database migration
  - Assigned To: Arun Kumar (trainer), HR (recruitment if needed)
  - Deadline: 2024-02-20

PRIORITY 1 - SCHEDULE KNOWLEDGE TRANSFER SESSIONS
  - Format: Weekly 2-hour sessions for 6 weeks
  - Content: 
    1. Architecture & design overview
    2. Pre-migration assessment
    3. Schema migration procedures
    4. Data migration & validation
    5. Cutover & failover procedures
    6. Post-migration monitoring
  - Participants: Arun Kumar, Priya Sharma, 2 new trainees
  - Start Date: 2024-01-27
  - Completion: 2024-03-09

PRIORITY 2 - ENHANCE DOCUMENTATION
  - Current gaps:
    1. Video walkthroughs missing
    2. Common error scenarios incomplete
    3. Performance tuning guide needed
    4. Disaster recovery procedures needed
  - Effort: 40 hours
  - Assigned To: Priya Sharma (document lead)
  - Deadline: 2024-03-20

PRIORITY 2 - CREATE RUNBOOK
  - Develop step-by-step runbook for:
    1. Pre-migration checklist
    2. Emergency rollback procedures
    3. Post-migration validation steps
  - Format: Wiki + PDF + Video
  - Assigned To: Arun Kumar
  - Deadline: 2024-02-15

PRIORITY 3 - RECORD VIDEO PROCEDURES
  - Record 3 main procedures:
    1. Standard database migration (20 minutes)
    2. Rollback procedure (10 minutes)
    3. Troubleshooting common issues (15 minutes)
  - Format: Screen recording + narration
  - Equipment: Screen recorder, microphone
  - Assigned To: Arun Kumar + videographer
  - Deadline: 2024-03-01
```

### Step 6: Preservation Actions Created

```sql
INSERT INTO preservation_actions (
  organization_id, knowledge_id, action_type, priority, status, 
  assigned_to, deadline, created_by, created_at
) VALUES
(789, 5678, 'secondary_expert_assignment', 'critical', 'planned', 
 23, '2024-02-20', 1, NOW()),
 
(789, 5678, 'knowledge_transfer_sessions', 'critical', 'planned', 
 23, '2024-03-09', 1, NOW()),
 
(789, 5678, 'documentation_enhancement', 'high', 'planned', 
 124, '2024-03-20', 1, NOW()),
 
(789, 5678, 'runbook_creation', 'high', 'planned', 
 123, '2024-02-15', 1, NOW()),
 
(789, 5678, 'video_recording', 'high', 'planned', 
 123, '2024-03-01', 1, NOW());
```

### Step 7: Dashboard View

```
Enterprise Knowledge Dashboard - GlobalTech Inc.

┌─────────────────────────────────────────┐
│      KNOWLEDGE RISK OVERVIEW            │
├─────────────────────────────────────────┤
│                                         │
│ Total Knowledge Areas:        247       │
│ Critical Risk:                  8 (3%)  │
│ High Risk:                     24 (10%) │ ◄── Database Migration (NEW)
│ Medium Risk:                   68 (27%) │
│ Low Risk:                    147 (60%)  │
│                                         │
│ Average Risk Score:          42.5       │
│                                         │
├─────────────────────────────────────────┤
│ TOP CRITICAL KNOWLEDGE ITEMS            │
├─────────────────────────────────────────┤
│ 1. Legacy Payment System        95.2    │ 🔴
│ 2. Database Migration (NEW)     74.3    │ 🟠
│ 3. Security Compliance          82.1    │ 🔴
│ 4. Disaster Recovery Plan       79.8    │ 🟠
│ 5. Network Infrastructure       76.5    │ 🟠
│                                         │
├─────────────────────────────────────────┤
│ PRESERVATION PROGRESS                   │
├─────────────────────────────────────────┤
│ Recommended Actions:     23              │
│ Planned Actions:          8              │
│ In Progress:              5              │
│ Completed This Month:     3              │
│                                         │
└─────────────────────────────────────────┘
```

### Step 8: Preservation Actions Executed (Over 8 weeks)

```
Week 1-2: Knowledge Transfer Starts
  - First training session scheduled
  - 2 new trainees assigned: Rajesh (backend), Lisa (frontend)
  - Arun Kumar begins preparation

Week 3: Runbook Created
  - Emergency procedures documented
  - Step-by-step guides prepared
  - PDF generated and stored

Week 4: First Video Recorded
  - "Standard Database Migration" (25 min, 850 MB)
  - Uploaded to knowledge platform
  - Accessible to all employees

Week 5: Documentation Enhanced
  - Common error scenarios documented
  - Performance tuning guide created
  - Known issues & solutions compiled

Week 6-8: Knowledge Transfer Continues
  - Weekly 2-hour sessions completed (6/6)
  - Trainees gain hands-on experience
  - Competency assessments passed
  - New experts ready for independent work

Month 3: Final Assessment
  - All preservation actions marked "Completed"
  - Risk re-assessment: 74.3 → 35.2 (MEDIUM)
  - Knowledge successfully preserved
  - 4 people now knowledgeable instead of 2
```

### Step 9: Re-assessment After Preservation

```
Updated Risk Scores After Preservation:

Criticality: 95 (unchanged - business need is same)
Uniqueness: 45 (improved - 4 experts now instead of 2)
Dependency: 85 (unchanged - still critical)
Documentation Gap: 10 (improved - comprehensive documentation + videos)
Availability Risk: 20 (improved - multiple experts, lower turnover risk)

New Risk Score = (95×0.30) + (45×0.25) + (85×0.20) + (10×0.15) + (20×0.10)
              = 28.5 + 11.25 + 17 + 1.5 + 2
              = 60.25 → MEDIUM ✓

From HIGH (74.3) to MEDIUM (60.25) - 23% reduction!
```

---

# CONCLUSION

This comprehensive project documentation provides a complete specification for an **NLP-Driven SaaS Platform for Enterprise Knowledge Loss Detection and Preservation**. The system combines:

- **Advanced NLP Processing**: Entity extraction, keyword identification, topic modeling
- **Intelligent Risk Assessment**: Five-factor weighted risk scoring with ML enhancement
- **Knowledge Preservation**: Automated recommendations and preservation workflows
- **Semantic Search**: Vector-based search using Sentence Transformers and pgvector
- **SaaS Architecture**: Multi-tenant design supporting multiple organizations
- **Enterprise-Grade Security**: Authentication, encryption, audit logging, RBAC
- **Production Readiness**: Monitoring, logging, disaster recovery, backup strategies

## Key Deliverables:

✅ Complete system architecture
✅ Detailed database schema with 20+ tables
✅ Comprehensive API specifications with examples
✅ NLP processing pipeline with concrete algorithms
✅ Risk calculation methodology with real examples
✅ Security implementation details
✅ Testing strategy with coverage targets
✅ Deployment & DevOps procedures
✅ Disaster recovery & backup plans
✅ Performance optimization strategies
✅ Accessibility & UX standards
✅ Success metrics & monitoring
✅ Cost analysis & ROI
✅ Risk management plan
✅ Complete workflow examples

## Development Roadmap:

**Phase 1 (Weeks 1-6): MVP**
- Authentication & database
- Document upload & text extraction
- NLP processing pipeline
- Rule-based risk scoring
- Dashboard & search
- Estimated: 30 days

**Phase 2 (Weeks 7-12): Enhancement**
- Machine Learning risk prediction
- Semantic search with pgvector
- Preservation recommendations
- Knowledge graph
- Advanced analytics
- Estimated: 30-45 days

**Phase 3+: Advanced Features**
- LLM integration
- Mobile application
- Advanced visualizations
- External integrations

---

**Document Prepared For**: Final Year Project Submission
**Suitable For**: Full-stack development team of 4+ members
**Estimated Development Time**: 45-90 days (depending on team size and dedication)
**Technology Stack**: React.js, FastAPI, PostgreSQL, spaCy, Scikit-learn, Sentence Transformers

---

**END OF COMPREHENSIVE PROJECT DOCUMENTATION**

