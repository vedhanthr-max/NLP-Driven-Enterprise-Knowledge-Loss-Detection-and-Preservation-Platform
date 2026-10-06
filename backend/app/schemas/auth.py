from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict

class UserRegisterRequest(BaseModel):
    email: str = Field(..., min_length=5, description="User email address")
    password: str = Field(..., min_length=8)
    full_name: str = Field(..., min_length=2)
    organization_name: str = Field(..., min_length=2)
    organization_size: int = Field(default=50, ge=1)
    role: str = Field(default="employee")

class UserRegisterResponse(BaseModel):
    user_id: int
    email: str
    organization_id: int
    organization_name: str
    role: str
    message: str

class UserLoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user_id: int
    email: str
    full_name: str
    role: str
    organization_id: int
    organization_name: str

class UserOut(BaseModel):
    user_id: int
    email: str
    full_name: str
    role: str
    organization_id: int
    department_id: Optional[int] = None
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class RefreshTokenRequest(BaseModel):
    refresh_token: str
