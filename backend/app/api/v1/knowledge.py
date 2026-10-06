from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.auth_service import get_current_user
from app.services.knowledge_service import KnowledgeService
from app.models.entities import User, KnowledgeItem, AuditLog
from app.schemas.knowledge import (
    KnowledgeListResponse, KnowledgeDetailOut, KnowledgeCreateRequest, KnowledgeUpdateRequest
)
from app.core.exceptions import KnowledgeNotFoundException

router = APIRouter(prefix="/knowledge", tags=["Knowledge"])

@router.get("", response_model=KnowledgeListResponse)
def get_knowledge(
    category: Optional[str] = Query(None),
    risk_level: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve filterable knowledge items for organization."""
    return KnowledgeService.get_knowledge_list(
        db=db,
        organization_id=current_user.organization_id,
        category=category,
        risk_level=risk_level,
        status=status,
        search=search,
        page=page,
        limit=limit
    )

@router.get("/{knowledge_id}", response_model=KnowledgeDetailOut)
def get_knowledge_item(
    knowledge_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve full knowledge item details, entities, keywords, and expert links."""
    return KnowledgeService.get_knowledge_detail(
        db=db,
        knowledge_id=knowledge_id,
        organization_id=current_user.organization_id
    )

@router.post("", response_model=KnowledgeDetailOut, status_code=status.HTTP_201_CREATED)
def create_knowledge_item(
    req: KnowledgeCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a structured knowledge item with linked experts."""
    item = KnowledgeService.create_knowledge_item(
        db=db,
        organization_id=current_user.organization_id,
        req=req,
        created_by_user_id=current_user.user_id
    )
    db.add(AuditLog(
        organization_id=current_user.organization_id,
        user_id=current_user.user_id,
        action_type="create",
        resource_type="knowledge",
        resource_id=item.knowledge_id,
        resource_name=item.title,
        status="success"
    ))
    db.commit()
    return KnowledgeService.get_knowledge_detail(db, item.knowledge_id, current_user.organization_id)

@router.put("/{knowledge_id}", response_model=KnowledgeDetailOut)
def update_knowledge_item(
    knowledge_id: int,
    req: KnowledgeUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update metadata and properties of a knowledge item."""
    item = db.query(KnowledgeItem).filter(
        KnowledgeItem.knowledge_id == knowledge_id,
        KnowledgeItem.organization_id == current_user.organization_id
    ).first()
    if not item:
        raise KnowledgeNotFoundException(knowledge_id)

    if req.title:
        item.title = req.title
    if req.description:
        item.description = req.description
    if req.category:
        item.category = req.category
    if req.subcategory:
        item.subcategory = req.subcategory
    if req.tags is not None:
        item.tags = req.tags
    if req.status:
        item.status = req.status

    db.add(AuditLog(
        organization_id=current_user.organization_id,
        user_id=current_user.user_id,
        action_type="update",
        resource_type="knowledge",
        resource_id=knowledge_id,
        resource_name=item.title,
        status="success"
    ))
    db.commit()
    return KnowledgeService.get_knowledge_detail(db, knowledge_id, current_user.organization_id)
