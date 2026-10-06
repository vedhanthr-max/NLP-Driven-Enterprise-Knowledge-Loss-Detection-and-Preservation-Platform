from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.auth_service import get_current_user
from app.services.search_service import SearchService
from app.models.entities import User, AuditLog
from app.schemas.search import SearchResponse

router = APIRouter(prefix="/search", tags=["Semantic Search"])

@router.get("", response_model=SearchResponse)
def semantic_search(
    q: str = Query(..., min_length=1, description="Natural language search query"),
    limit: int = Query(10, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Execute vector similarity search over organizational knowledge base."""
    res = SearchService.semantic_search(
        db=db,
        organization_id=current_user.organization_id,
        query=q,
        limit=limit
    )

    db.add(AuditLog(
        organization_id=current_user.organization_id,
        user_id=current_user.user_id,
        action_type="search",
        resource_type="query",
        resource_name=q[:100],
        status="success"
    ))
    db.commit()

    return res
