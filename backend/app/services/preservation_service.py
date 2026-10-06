from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.models.entities import PreservationAction, KnowledgeItem, User
from app.schemas.preservation import PreservationActionCreate, PreservationActionUpdate, PreservationActionOut

class PreservationService:
    @staticmethod
    def list_actions(
        db: Session,
        organization_id: int,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        assigned_to: Optional[int] = None
    ) -> List[PreservationActionOut]:
        query = db.query(PreservationAction).filter(PreservationAction.organization_id == organization_id)
        if status:
            query = query.filter(PreservationAction.status == status)
        if priority:
            query = query.filter(PreservationAction.priority == priority)
        if assigned_to:
            query = query.filter(PreservationAction.assigned_to == assigned_to)

        actions = query.order_by(PreservationAction.created_at.desc()).all()
        out = []
        for a in actions:
            assigned_user = db.query(User).filter(User.user_id == a.assigned_to).first() if a.assigned_to else None
            k = a.knowledge
            out.append(PreservationActionOut(
                action_id=a.action_id,
                organization_id=a.organization_id,
                knowledge_id=a.knowledge_id,
                knowledge_title=k.title if k else None,
                action_type=a.action_type,
                action_description=a.action_description,
                priority=a.priority,
                status=a.status,
                assigned_to=a.assigned_to,
                assigned_name=assigned_user.full_name if assigned_user else None,
                deadline=a.deadline,
                completion_date=a.completion_date,
                completion_notes=a.completion_notes,
                estimated_hours=a.estimated_hours or 0,
                actual_hours=a.actual_hours or 0,
                created_at=a.created_at,
                updated_at=a.updated_at
            ))
        return out

    @staticmethod
    def create_action(
        db: Session,
        organization_id: int,
        req: PreservationActionCreate,
        created_by_user_id: int
    ) -> PreservationAction:
        knowledge = db.query(KnowledgeItem).filter(
            KnowledgeItem.knowledge_id == req.knowledge_id,
            KnowledgeItem.organization_id == organization_id
        ).first()
        if not knowledge:
            raise AppException(404, "ERR-KNOW-001", "Knowledge item not found")

        action = PreservationAction(
            organization_id=organization_id,
            knowledge_id=req.knowledge_id,
            action_type=req.action_type,
            action_description=req.action_description,
            priority=req.priority,
            status="planned" if req.assigned_to else "recommended",
            assigned_to=req.assigned_to,
            assigned_at=datetime.now(timezone.utc) if req.assigned_to else None,
            deadline=req.deadline,
            estimated_hours=req.estimated_hours,
            created_by=created_by_user_id
        )
        db.add(action)
        db.commit()
        db.refresh(action)
        return action

    @staticmethod
    def update_action(
        db: Session,
        action_id: int,
        organization_id: int,
        req: PreservationActionUpdate
    ) -> PreservationAction:
        action = db.query(PreservationAction).filter(
            PreservationAction.action_id == action_id,
            PreservationAction.organization_id == organization_id
        ).first()
        if not action:
            raise AppException(404, "ERR-ACT-001", "Preservation action not found")

        if req.status:
            action.status = req.status
            if req.status == "completed":
                action.completion_date = datetime.now(timezone.utc).date()
        if req.priority:
            action.priority = req.priority
        if req.assigned_to is not None:
            action.assigned_to = req.assigned_to
            action.assigned_at = datetime.now(timezone.utc)
        if req.deadline:
            action.deadline = req.deadline
        if req.completion_notes:
            action.completion_notes = req.completion_notes
        if req.actual_hours is not None:
            action.actual_hours = req.actual_hours

        action.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(action)
        return action
