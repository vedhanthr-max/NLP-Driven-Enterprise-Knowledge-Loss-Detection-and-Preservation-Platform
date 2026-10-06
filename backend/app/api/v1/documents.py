from typing import Optional
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, UploadFile, File, Form, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.auth_service import get_current_user
from app.services.document_service import DocumentService
from app.models.entities import User, Document, DocumentChunk, AuditLog
from app.schemas.documents import DocumentUploadResponse, DocumentDetailOut, DocumentListResponse, DocumentListItem
from app.core.exceptions import DocumentNotFoundException

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post("/upload", response_model=DocumentUploadResponse, status_code=status.HTTP_202_ACCEPTED)
async def upload_document(
    file: UploadFile = File(...),
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload and parse an enterprise document (PDF, DOCX, TXT, MD)."""
    doc = await DocumentService.process_document_upload(
        db=db,
        file=file,
        title=title or file.filename,
        description=description,
        current_user=current_user
    )

    db.add(AuditLog(
        organization_id=current_user.organization_id,
        user_id=current_user.user_id,
        action_type="upload",
        resource_type="document",
        resource_id=doc.document_id,
        resource_name=doc.title,
        status="success"
    ))
    db.commit()

    knowledge_item = doc.knowledge_items[0] if doc.knowledge_items else None
    entities_count = len(knowledge_item.entities) if knowledge_item else 0
    keywords_count = len(knowledge_item.keywords) if knowledge_item else 0

    return DocumentUploadResponse(
        document_id=doc.document_id,
        title=doc.title,
        file_name=doc.file_name,
        file_type=doc.file_type,
        file_size=doc.file_size,
        status=doc.extraction_status,
        message="Document uploaded, parsed, and indexed into knowledge repository successfully",
        chunks_created=len(doc.chunks),
        entities_extracted=entities_count,
        keywords_extracted=keywords_count,
        knowledge_item_id=knowledge_item.knowledge_id if knowledge_item else None
    )

@router.get("", response_model=DocumentListResponse)
def get_documents(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all documents belonging to current user's organization."""
    query = db.query(Document).filter(
        Document.organization_id == current_user.organization_id,
        Document.deleted_at.is_(None)
    )
    total = query.count()
    docs = query.order_by(Document.created_at.desc()).offset((page - 1) * limit).limit(limit).all()

    items = []
    for d in docs:
        items.append(DocumentListItem(
            document_id=d.document_id,
            title=d.title,
            file_name=d.file_name,
            file_type=d.file_type,
            file_size=d.file_size,
            pages=d.pages or 1,
            status=d.extraction_status,
            created_at=d.created_at,
            chunks_count=len(d.chunks),
            knowledge_items_count=len(d.knowledge_items)
        ))

    return DocumentListResponse(
        total=total,
        page=page,
        limit=limit,
        documents=items
    )

@router.get("/{document_id}", response_model=DocumentDetailOut)
def get_document_details(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve detailed document metadata, text chunks, and NLP stats."""
    doc = db.query(Document).filter(
        Document.document_id == document_id,
        Document.organization_id == current_user.organization_id,
        Document.deleted_at.is_(None)
    ).first()
    if not doc:
        raise DocumentNotFoundException(document_id)

    knowledge_item = doc.knowledge_items[0] if doc.knowledge_items else None
    entities_count = len(knowledge_item.entities) if knowledge_item else 0
    keywords_count = len(knowledge_item.keywords) if knowledge_item else 0

    return DocumentDetailOut(
        document_id=doc.document_id,
        title=doc.title,
        description=doc.description,
        file_name=doc.file_name,
        file_type=doc.file_type,
        file_size=doc.file_size,
        pages=doc.pages or 1,
        language=doc.language or "en",
        extraction_status=doc.extraction_status,
        extraction_error=doc.extraction_error,
        created_at=doc.created_at,
        processed_at=doc.processed_at,
        chunks_created=len(doc.chunks),
        entities_extracted=entities_count,
        keywords_extracted=keywords_count,
        knowledge_items_count=len(doc.knowledge_items),
        chunks=[{
            "chunk_id": c.chunk_id,
            "chunk_index": c.chunk_index,
            "chunk_text": c.chunk_text,
            "token_count": c.token_count,
            "page_number": c.page_number
        } for c in doc.chunks]
    )

@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Soft delete document record."""
    doc = db.query(Document).filter(
        Document.document_id == document_id,
        Document.organization_id == current_user.organization_id
    ).first()
    if not doc:
        raise DocumentNotFoundException(document_id)

    doc.deleted_at = datetime.now(timezone.utc)
    db.add(AuditLog(
        organization_id=current_user.organization_id,
        user_id=current_user.user_id,
        action_type="delete",
        resource_type="document",
        resource_id=document_id,
        resource_name=doc.title,
        status="success"
    ))
    db.commit()
    return None
