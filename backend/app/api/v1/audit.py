from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict

from app.core.database import get_db
from app.services.auth_service import get_current_user, require_role
from app.models.entities import User, AuditLog

router = APIRouter(prefix="/audit", tags=["Audit & Security"])

class AuditLogOut(BaseModel):
    log_id: int
    user_id: Optional[int] = None
    user_name: Optional[str] = None
    action_type: str
    resource_type: str
    resource_id: Optional[int] = None
    resource_name: Optional[str] = None
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

@router.get("/logs", response_model=List[AuditLogOut])
def get_audit_logs(
    limit: int = Query(50, ge=1, le=200),
    action_type: Optional[str] = Query(None),
    current_user: User = Depends(require_role(["admin", "manager"])),
    db: Session = Depends(get_db)
):
    """Retrieve audit trail logs for organizational security review."""
    query = db.query(AuditLog).filter(
        AuditLog.organization_id == current_user.organization_id
    )
    if action_type:
        query = query.filter(AuditLog.action_type == action_type)

    logs = query.order_by(AuditLog.created_at.desc()).limit(limit).all()
    out = []
    for l in logs:
        u = db.query(User).filter(User.user_id == l.user_id).first() if l.user_id else None
        out.append(AuditLogOut(
            log_id=l.log_id,
            user_id=l.user_id,
            user_name=u.full_name if u else "System",
            action_type=l.action_type,
            resource_type=l.resource_type,
            resource_id=l.resource_id,
            resource_name=l.resource_name,
            status=l.status or "success",
            created_at=l.created_at
        ))
    return out
