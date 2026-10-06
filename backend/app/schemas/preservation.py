from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict

class PreservationActionCreate(BaseModel):
    knowledge_id: int
    action_type: str  # documentation, secondary_expert, knowledge_transfer, training, automation
    action_description: str
    priority: str = "high"  # low, medium, high, critical
    assigned_to: Optional[int] = None
    deadline: Optional[date] = None
    estimated_hours: int = 20

class PreservationActionUpdate(BaseModel):
    status: Optional[str] = None  # recommended, planned, in_progress, completed, cancelled
    priority: Optional[str] = None
    assigned_to: Optional[int] = None
    deadline: Optional[date] = None
    completion_notes: Optional[str] = None
    actual_hours: Optional[int] = None

class PreservationActionOut(BaseModel):
    action_id: int
    organization_id: int
    knowledge_id: int
    knowledge_title: Optional[str] = None
    action_type: str
    action_description: str
    priority: str
    status: str
    assigned_to: Optional[int] = None
    assigned_name: Optional[str] = None
    deadline: Optional[date] = None
    completion_date: Optional[date] = None
    completion_notes: Optional[str] = None
    estimated_hours: int
    actual_hours: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
