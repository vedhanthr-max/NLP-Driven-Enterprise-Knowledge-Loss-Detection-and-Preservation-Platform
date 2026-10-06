from typing import Optional, List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.auth_service import get_current_user
from app.services.preservation_service import PreservationService
from app.models.entities import User, AuditLog
from app.schemas.preservation import (
    PreservationActionCreate, PreservationActionUpdate, PreservationActionOut
)

router = APIRouter(prefix="/preservation-actions", tags=["Preservation Engine"])

@router.get("", response_model=List[PreservationActionOut])
def get_preservation_actions(
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    assigned_to: Optional[int] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List preservation recommendations and tasks for current organization."""
    return PreservationService.list_actions(
        db=db,
        organization_id=current_user.organization_id,
        status=status,
        priority=priority,
        assigned_to=assigned_to
    )

@router.post("", response_model=PreservationActionOut, status_code=status.HTTP_201_CREATED)
def create_preservation_action(
    req: PreservationActionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new knowledge preservation action."""
    action = PreservationService.create_action(
        db=db,
        organization_id=current_user.organization_id,
        req=req,
        created_by_user_id=current_user.user_id
    )
    db.add(AuditLog(
        organization_id=current_user.organization_id,
        user_id=current_user.user_id,
        action_type="create",
        resource_type="preservation_action",
        resource_id=action.action_id,
        resource_name=action.action_description[:100],
        status="success"
    ))
    db.commit()
    actions = PreservationService.list_actions(db, current_user.organization_id)
    return [a for a in actions if a.action_id == action.action_id][0]

@router.put("/{action_id}", response_model=PreservationActionOut)
def update_preservation_action(
    action_id: int,
    req: PreservationActionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update status, assignment, or completion details of a preservation action."""
    action = PreservationService.update_action(
        db=db,
        action_id=action_id,
        organization_id=current_user.organization_id,
        req=req
    )
    db.add(AuditLog(
        organization_id=current_user.organization_id,
        user_id=current_user.user_id,
        action_type="update",
        resource_type="preservation_action",
        resource_id=action_id,
        resource_name=f"Status: {action.status}",
        status="success"
    ))
    db.commit()
    actions = PreservationService.list_actions(db, current_user.organization_id)
    return [a for a in actions if a.action_id == action.action_id][0]
