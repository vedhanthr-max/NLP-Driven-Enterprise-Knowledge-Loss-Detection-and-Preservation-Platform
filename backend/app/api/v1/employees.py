from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict

from app.core.database import get_db
from app.services.auth_service import get_current_user
from app.models.entities import User, Employee, KnowledgeExpert, KnowledgeItem

router = APIRouter(prefix="/employees", tags=["Employees"])

class EmployeeOut(BaseModel):
    employee_id: int
    user_id: int
    full_name: str
    email: str
    job_title: Optional[str] = None
    expertise_level: str
    expertise_areas: List[str] = []
    status: str
    associated_knowledge_count: int = 0

    model_config = ConfigDict(from_attributes=True)

@router.get("", response_model=List[EmployeeOut])
def get_employees(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List organization employees with their technical expertise areas and knowledge items."""
    employees = db.query(Employee).filter(
        Employee.organization_id == current_user.organization_id
    ).all()

    out = []
    for emp in employees:
        u = emp.user
        knowledge_count = db.query(KnowledgeExpert).filter(
            KnowledgeExpert.employee_id == emp.employee_id
        ).count()
        out.append(EmployeeOut(
            employee_id=emp.employee_id,
            user_id=emp.user_id,
            full_name=u.full_name if u else f"Employee {emp.employee_id}",
            email=u.email if u else "",
            job_title=emp.job_title,
            expertise_level=emp.expertise_level or "intermediate",
            expertise_areas=emp.expertise_areas or [],
            status=emp.status or "active",
            associated_knowledge_count=knowledge_count
        ))
    return out
