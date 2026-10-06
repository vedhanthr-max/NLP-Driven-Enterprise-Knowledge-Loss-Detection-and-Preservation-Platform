from datetime import datetime, timezone
import json
from sqlalchemy import (
    Column, Integer, String, Float, Text, Boolean, DateTime, Date, ForeignKey, JSON
)
from sqlalchemy.orm import relationship
from app.core.database import Base

def utcnow():
    return datetime.now(timezone.utc)

class Organization(Base):
    __tablename__ = "organizations"

    organization_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    organization_name = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    industry = Column(String(100), nullable=True)
    size = Column(Integer, default=50)
    subscription_tier = Column(String(50), default="enterprise")
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)

    # Relationships
    users = relationship("User", back_populates="organization", cascade="all, delete-orphan")
    departments = relationship("Department", back_populates="organization", cascade="all, delete-orphan")
    employees = relationship("Employee", back_populates="organization", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="organization", cascade="all, delete-orphan")
    knowledge_items = relationship("KnowledgeItem", back_populates="organization", cascade="all, delete-orphan")
    risk_scores = relationship("RiskScore", back_populates="organization", cascade="all, delete-orphan")
    preservation_actions = relationship("PreservationAction", back_populates="organization", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="organization")
    ml_models = relationship("MLModel", back_populates="organization")

class Department(Base):
    __tablename__ = "departments"

    department_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    organization_id = Column(Integer, ForeignKey("organizations.organization_id", ondelete="CASCADE"), nullable=False, index=True)
    department_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    parent_department_id = Column(Integer, ForeignKey("departments.department_id"), nullable=True)
    manager_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)

    # Relationships
    organization = relationship("Organization", back_populates="departments")
    users = relationship("User", back_populates="department")
    employees = relationship("Employee", back_populates="department")

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    organization_id = Column(Integer, ForeignKey("organizations.organization_id", ondelete="CASCADE"), nullable=False, index=True)
    email = Column(String(255), nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="employee")  # admin, manager, employee
    department_id = Column(Integer, ForeignKey("departments.department_id"), nullable=True)
    is_active = Column(Boolean, default=True, index=True)
    email_verified = Column(Boolean, default=True)
    verification_token = Column(String(255), nullable=True)
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)

    # Relationships
    organization = relationship("Organization", back_populates="users")
    department = relationship("Department", back_populates="users")
    employee = relationship("Employee", back_populates="user", uselist=False)

class Employee(Base):
    __tablename__ = "employees"

    employee_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), unique=True, nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.organization_id", ondelete="CASCADE"), nullable=False, index=True)
    department_id = Column(Integer, ForeignKey("departments.department_id"), nullable=True)
    expertise_areas = Column(JSON, default=list)  # e.g. ["Python", "AWS", "Legacy Banking"]
    expertise_level = Column(String(50), default="intermediate")  # beginner, intermediate, expert
    job_title = Column(String(255), nullable=True)
    status = Column(String(50), default="active", index=True)  # active, on_leave, inactive, left
    joined_date = Column(Date, nullable=True)
    last_active_date = Column(DateTime, nullable=True)
    bio = Column(Text, nullable=True)
    skill_summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)

    # Relationships
    user = relationship("User", back_populates="employee")
    organization = relationship("Organization", back_populates="employees")
    department = relationship("Department", back_populates="employees")
    expert_links = relationship("KnowledgeExpert", back_populates="employee", cascade="all, delete-orphan")

class Document(Base):
    __tablename__ = "documents"

    document_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    organization_id = Column(Integer, ForeignKey("organizations.organization_id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    file_name = Column(String(500), nullable=False)
    file_path = Column(String(1000), nullable=False)
    file_size = Column(Integer, default=0)
    file_type = Column(String(20), nullable=False)  # pdf, docx, txt, md
    mime_type = Column(String(100), nullable=True)
    content_hash = Column(String(64), nullable=False, index=True)  # SHA-256
    language = Column(String(10), default="en")
    pages = Column(Integer, default=1)
    uploaded_by = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    source_type = Column(String(50), default="manual_upload")
    extraction_status = Column(String(50), default="pending", index=True)  # pending, processing, completed, failed
    extraction_error = Column(Text, nullable=True)
    processed_at = Column(DateTime, nullable=True)
    is_verified = Column(Boolean, default=False)
    is_archived = Column(Boolean, default=False)
    retention_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)
    deleted_at = Column(DateTime, nullable=True)

    # Relationships
    organization = relationship("Organization", back_populates="documents")
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")
    knowledge_items = relationship("KnowledgeItem", back_populates="source_document")

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    chunk_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    document_id = Column(Integer, ForeignKey("documents.document_id", ondelete="CASCADE"), nullable=False, index=True)
    chunk_index = Column(Integer, nullable=False)
    chunk_text = Column(Text, nullable=False)
    token_count = Column(Integer, default=0)
    start_position = Column(Integer, default=0)
    end_position = Column(Integer, default=0)
    page_number = Column(Integer, default=1)
    created_at = Column(DateTime, default=utcnow)

    # Relationships
    document = relationship("Document", back_populates="chunks")
    embeddings = relationship("Embedding", back_populates="chunk", cascade="all, delete-orphan")

class KnowledgeItem(Base):
    __tablename__ = "knowledge_items"

    knowledge_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    organization_id = Column(Integer, ForeignKey("organizations.organization_id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(100), default="General", index=True)
    subcategory = Column(String(100), nullable=True)
    tags = Column(JSON, default=list)
    source_document_id = Column(Integer, ForeignKey("documents.document_id"), nullable=True)
    knowledge_type = Column(String(50), default="procedure")  # procedure, troubleshooting, architecture, policy
    status = Column(String(50), default="active", index=True)  # draft, active, archived, obsolete
    is_verified = Column(Boolean, default=False)
    verified_by = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    verified_at = Column(DateTime, nullable=True)
    confidence_score = Column(Float, default=1.0)
    extraction_method = Column(String(50), default="nlp_extracted")
    created_by = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    created_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)
    last_accessed = Column(DateTime, nullable=True)
    access_count = Column(Integer, default=0)

    # Relationships
    organization = relationship("Organization", back_populates="knowledge_items")
    source_document = relationship("Document", back_populates="knowledge_items")
    entities = relationship("Entity", back_populates="knowledge", cascade="all, delete-orphan")
    keywords = relationship("Keyword", back_populates="knowledge", cascade="all, delete-orphan")
    experts = relationship("KnowledgeExpert", back_populates="knowledge", cascade="all, delete-orphan")
    risk_scores = relationship("RiskScore", back_populates="knowledge", cascade="all, delete-orphan")
    preservation_actions = relationship("PreservationAction", back_populates="knowledge", cascade="all, delete-orphan")
    embeddings = relationship("Embedding", back_populates="knowledge", cascade="all, delete-orphan")

class Entity(Base):
    __tablename__ = "entities"

    entity_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    knowledge_id = Column(Integer, ForeignKey("knowledge_items.knowledge_id", ondelete="CASCADE"), nullable=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.document_id", ondelete="CASCADE"), nullable=True, index=True)
    entity_name = Column(String(500), nullable=False, index=True)
    entity_type = Column(String(50), nullable=False, index=True)  # PERSON, TECHNOLOGY, ORGANIZATION, PRODUCT, etc.
    confidence = Column(Float, default=0.90)
    context = Column(Text, nullable=True)
    created_at = Column(DateTime, default=utcnow)

    # Relationships
    knowledge = relationship("KnowledgeItem", back_populates="entities")

class Keyword(Base):
    __tablename__ = "keywords"

    keyword_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    knowledge_id = Column(Integer, ForeignKey("knowledge_items.knowledge_id", ondelete="CASCADE"), nullable=False, index=True)
    keyword = Column(String(255), nullable=False, index=True)
    frequency = Column(Integer, default=1)
    tf_idf_score = Column(Float, default=0.0)
    extraction_method = Column(String(50), default="tfidf")
    created_at = Column(DateTime, default=utcnow)

    # Relationships
    knowledge = relationship("KnowledgeItem", back_populates="keywords")

class KnowledgeExpert(Base):
    __tablename__ = "knowledge_experts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    knowledge_id = Column(Integer, ForeignKey("knowledge_items.knowledge_id", ondelete="CASCADE"), nullable=False, index=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id", ondelete="CASCADE"), nullable=False, index=True)
    expertise_level = Column(String(50), default="expert")  # beginner, intermediate, expert
    is_primary_expert = Column(Boolean, default=False, index=True)
    years_of_experience = Column(Integer, default=5)
    confidence_score = Column(Float, default=0.95)
    identified_by = Column(String(50), default="nlp_extracted")
    added_at = Column(DateTime, default=utcnow)

    # Relationships
    knowledge = relationship("KnowledgeItem", back_populates="experts")
    employee = relationship("Employee", back_populates="expert_links")

class RiskScore(Base):
    __tablename__ = "risk_scores"

    risk_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    organization_id = Column(Integer, ForeignKey("organizations.organization_id", ondelete="CASCADE"), nullable=False, index=True)
    knowledge_id = Column(Integer, ForeignKey("knowledge_items.knowledge_id", ondelete="CASCADE"), nullable=False, index=True)
    
    # 5 Factors (0 to 100)
    criticality = Column(Float, nullable=False)
    uniqueness = Column(Float, nullable=False)
    dependency = Column(Float, nullable=False)
    documentation_gap = Column(Float, nullable=False)
    availability_risk = Column(Float, nullable=False)
    
    # Composite Score & Level
    risk_score = Column(Float, nullable=False)
    risk_level = Column(String(50), nullable=False, index=True)  # low, medium, high, critical
    
    # ML Prediction
    ml_predicted_level = Column(String(50), nullable=True)
    ml_confidence = Column(Float, nullable=True)
    prediction_model_version = Column(String(50), nullable=True)
    
    # Metadata
    assessment_method = Column(String(50), default="rule_based")  # rule_based, ml, hybrid
    assessed_by = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    assessment_notes = Column(Text, nullable=True)
    is_latest = Column(Boolean, default=True, index=True)
    calculated_at = Column(DateTime, default=utcnow)
    next_review_date = Column(Date, nullable=True)

    # Relationships
    organization = relationship("Organization", back_populates="risk_scores")
    knowledge = relationship("KnowledgeItem", back_populates="risk_scores")

class Embedding(Base):
    __tablename__ = "embeddings"

    embedding_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    knowledge_id = Column(Integer, ForeignKey("knowledge_items.knowledge_id", ondelete="CASCADE"), nullable=True, index=True)
    document_chunk_id = Column(Integer, ForeignKey("document_chunks.chunk_id", ondelete="CASCADE"), nullable=True, index=True)
    embedding_vector = Column(Text, nullable=False)  # JSON serialized array of floats (384d)
    embedding_model = Column(String(100), default="all-MiniLM-L6-v2")
    created_at = Column(DateTime, default=utcnow)

    # Relationships
    knowledge = relationship("KnowledgeItem", back_populates="embeddings")
    chunk = relationship("DocumentChunk", back_populates="embeddings")

    def get_vector(self):
        """Parse vector into float list."""
        try:
            return json.loads(self.embedding_vector)
        except Exception:
            return []

    def set_vector(self, vec):
        """Set vector from float list."""
        self.embedding_vector = json.dumps([float(x) for x in vec])

class PreservationAction(Base):
    __tablename__ = "preservation_actions"

    action_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    organization_id = Column(Integer, ForeignKey("organizations.organization_id", ondelete="CASCADE"), nullable=False, index=True)
    knowledge_id = Column(Integer, ForeignKey("knowledge_items.knowledge_id", ondelete="CASCADE"), nullable=False, index=True)
    action_type = Column(String(100), nullable=False)  # documentation, secondary_expert, knowledge_transfer, training
    action_description = Column(Text, nullable=False)
    priority = Column(String(50), default="high")  # low, medium, high, critical
    status = Column(String(50), default="recommended", index=True)  # recommended, planned, in_progress, completed, cancelled
    assigned_to = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    assigned_at = Column(DateTime, nullable=True)
    deadline = Column(Date, nullable=True)
    completion_date = Column(Date, nullable=True)
    completion_notes = Column(Text, nullable=True)
    estimated_hours = Column(Integer, default=20)
    actual_hours = Column(Integer, default=0)
    created_by = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    created_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)

    # Relationships
    organization = relationship("Organization", back_populates="preservation_actions")
    knowledge = relationship("KnowledgeItem", back_populates="preservation_actions")

class AuditLog(Base):
    __tablename__ = "audit_logs"

    log_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    organization_id = Column(Integer, ForeignKey("organizations.organization_id", ondelete="SET NULL"), nullable=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="SET NULL"), nullable=True, index=True)
    action_type = Column(String(100), nullable=False, index=True)  # login, upload, create, update, delete, search, assess
    resource_type = Column(String(100), nullable=False)  # document, knowledge, risk, user, action
    resource_id = Column(Integer, nullable=True)
    resource_name = Column(String(500), nullable=True)
    old_value = Column(JSON, nullable=True)
    new_value = Column(JSON, nullable=True)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(Text, nullable=True)
    status = Column(String(50), default="success")  # success, failure
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=utcnow, index=True)

    # Relationships
    organization = relationship("Organization", back_populates="audit_logs")

class MLModel(Base):
    __tablename__ = "ml_models"

    model_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    organization_id = Column(Integer, ForeignKey("organizations.organization_id", ondelete="CASCADE"), nullable=False, index=True)
    model_name = Column(String(255), nullable=False)
    model_type = Column(String(100), nullable=False)  # random_forest, xgboost, logistic_regression
    version = Column(String(50), nullable=False)
    model_path = Column(String(500), nullable=False)
    scaler_path = Column(String(500), nullable=True)
    accuracy = Column(Float, default=0.0)
    precision = Column(Float, default=0.0)
    recall = Column(Float, default=0.0)
    f1_score = Column(Float, default=0.0)
    training_data_size = Column(Integer, default=0)
    training_samples = Column(Integer, default=0)
    features_used = Column(JSON, default=list)
    hyperparameters = Column(JSON, default=dict)
    is_active = Column(Boolean, default=False, index=True)
    trained_at = Column(DateTime, default=utcnow)
    deployed_at = Column(DateTime, nullable=True)
    performance_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=utcnow)

    # Relationships
    organization = relationship("Organization", back_populates="ml_models")
