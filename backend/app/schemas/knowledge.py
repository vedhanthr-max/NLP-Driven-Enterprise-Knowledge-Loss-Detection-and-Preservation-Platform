from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

class EntityOut(BaseModel):
    entity_name: str
    entity_type: str
    confidence: float = 0.9
    context: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class KeywordOut(BaseModel):
    keyword: str
    frequency: int = 1
    tf_idf_score: float = 0.0

    model_config = ConfigDict(from_attributes=True)

class ExpertItem(BaseModel):
    employee_id: int
    expertise_level: str = "expert"  # beginner, intermediate, expert
    is_primary_expert: bool = False
    years_of_experience: int = 5
    confidence_score: float = 0.95

class ExpertOut(BaseModel):
    employee_id: int
    full_name: Optional[str] = None
    expertise_level: str
    is_primary_expert: bool
    years_of_experience: int
    confidence_score: float

    model_config = ConfigDict(from_attributes=True)

class KnowledgeCreateRequest(BaseModel):
    title: str = Field(..., min_length=3)
    description: Optional[str] = None
    category: str = "General"
    subcategory: Optional[str] = None
    tags: List[str] = []
    source_document_id: Optional[int] = None
    knowledge_type: str = "procedure"
    status: str = "active"
    experts: List[ExpertItem] = []

class KnowledgeUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    tags: Optional[List[str]] = None
    status: Optional[str] = None

class KnowledgeDetailOut(BaseModel):
    knowledge_id: int
    title: str
    description: Optional[str] = None
    category: str
    subcategory: Optional[str] = None
    tags: List[str] = []
    source_document_id: Optional[int] = None
    knowledge_type: str
    status: str
    is_verified: bool
    confidence_score: float
    created_at: datetime
    updated_at: datetime
    last_accessed: Optional[datetime] = None
    access_count: int = 0
    entities: List[EntityOut] = []
    keywords: List[KeywordOut] = []
    experts: List[ExpertOut] = []
    risk_score: Optional[float] = None
    risk_level: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class KnowledgeListItem(BaseModel):
    knowledge_id: int
    title: str
    category: str
    status: str
    risk_score: Optional[float] = None
    risk_level: Optional[str] = None
    experts_count: int = 0
    tags: List[str] = []
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class KnowledgeListResponse(BaseModel):
    total: int
    page: int
    limit: int
    items: List[KnowledgeListItem]
