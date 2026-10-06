from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict

class DocumentUploadResponse(BaseModel):
    document_id: int
    title: str
    file_name: str
    file_type: str
    file_size: int
    status: str
    message: str
    chunks_created: int = 0
    entities_extracted: int = 0
    keywords_extracted: int = 0
    knowledge_item_id: Optional[int] = None

class DocumentChunkOut(BaseModel):
    chunk_id: int
    chunk_index: int
    chunk_text: str
    token_count: int
    page_number: int

    model_config = ConfigDict(from_attributes=True)

class DocumentDetailOut(BaseModel):
    document_id: int
    title: str
    description: Optional[str] = None
    file_name: str
    file_type: str
    file_size: int
    pages: int
    language: str
    extraction_status: str
    extraction_error: Optional[str] = None
    created_at: datetime
    processed_at: Optional[datetime] = None
    chunks_created: int = 0
    entities_extracted: int = 0
    keywords_extracted: int = 0
    knowledge_items_count: int = 0
    chunks: List[DocumentChunkOut] = []

    model_config = ConfigDict(from_attributes=True)

class DocumentListItem(BaseModel):
    document_id: int
    title: str
    file_name: str
    file_type: str
    file_size: int
    pages: int
    status: str
    created_at: datetime
    chunks_count: int = 0
    knowledge_items_count: int = 0

class DocumentListResponse(BaseModel):
    total: int
    page: int
    limit: int
    documents: List[DocumentListItem]
