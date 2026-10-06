from typing import Optional, List
from pydantic import BaseModel

class SearchResultItem(BaseModel):
    knowledge_id: int
    title: str
    description: Optional[str] = None
    category: str
    risk_level: Optional[str] = None
    risk_score: Optional[float] = None
    relevance_score: float  # 0.0 to 1.0
    snippet: str
    matched_chunk_id: Optional[int] = None
    source_document_id: Optional[int] = None

class SearchResponse(BaseModel):
    query: str
    total_results: int
    search_time_ms: float
    results: List[SearchResultItem]
