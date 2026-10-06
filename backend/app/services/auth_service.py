from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import Depends, Header, status
from fastapi.security import OAuth2PasswordBearer

from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from app.core.exceptions import (
    AppException, InvalidCredentialsException, TokenExpiredException,
    InvalidTokenException, PermissionDeniedException
)
from app.models.entities import User, Organization, Employee
from app.schemas.auth import UserRegisterRequest, UserRegisterResponse, TokenResponse

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)

class AuthService:
    @staticmethod
    def register_user(db: Session, req: UserRegisterRequest) -> UserRegisterResponse:
        # Check if email is already taken
        existing_user = db.query(User).filter(User.email == req.email.lower()).first()
        if existing_user:
            raise AppException(
                status_code=status.HTTP_400_BAD_REQUEST,
                error_code="ERR-AUTH-001",
                message="Email already registered",
                details={"email": req.email}
            )

        # Check or create organization
        org = db.query(Organization).filter(Organization.organization_name == req.organization_name).first()
        if not org:
            org = Organization(
                organization_name=req.organization_name,
                size=req.organization_size,
                subscription_tier="enterprise"
            )
            db.add(org)
            db.flush()

        # Hash password and create user
        hashed_pwd = hash_password(req.password)
        user = User(
            organization_id=org.organization_id,
            email=req.email.lower(),
            password_hash=hashed_pwd,
            full_name=req.full_name,
            role=req.role if req.role in ("admin", "manager", "employee") else "employee",
            is_active=True,
            email_verified=True
        )
        db.add(user)
        db.flush()

        # Create linked employee record
        emp = Employee(
            user_id=user.user_id,
            organization_id=org.organization_id,
            job_title="Knowledge Contributor",
            expertise_level="intermediate",
            status="active"
        )
        db.add(emp)
        db.commit()
        db.refresh(user)

        return UserRegisterResponse(
            user_id=user.user_id,
            email=user.email,
            organization_id=org.organization_id,
            organization_name=org.organization_name,
            role=user.role,
            message="User registered successfully"
        )

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> User:
        user = db.query(User).filter(User.email == email.lower()).first()
        if not user or not verify_password(password, user.password_hash):
            raise InvalidCredentialsException()
        if not user.is_active:
            raise AppException(
                status_code=status.HTTP_403_FORBIDDEN,
                error_code="ERR-AUTH-004",
                message="User account is deactivated"
            )
        # Update last login
        user.last_login = datetime.now(timezone.utc)
        db.commit()
        return user

    @staticmethod
    def create_user_tokens(user: User) -> TokenResponse:
        token_data = {
            "sub": str(user.user_id),
            "email": user.email,
            "role": user.role,
            "org_id": user.organization_id
        }
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=3600,
            user_id=user.user_id,
            email=user.email,
            full_name=user.full_name,
            role=user.role,
            organization_id=user.organization_id,
            organization_name=user.organization.organization_name if user.organization else ""
        )

def get_current_user(token: Optional[str] = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """Dependency extracting and validating authenticated user from JWT bearer token."""
    if not token:
        raise AppException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="ERR-AUTH-007",
            message="Missing or invalid authentication token"
        )
    payload = decode_token(token)
    user_id = payload.get("sub")
    if not user_id:
        raise InvalidTokenException("Missing user identifier in token")
    
    user = db.query(User).filter(User.user_id == int(user_id)).first()
    if not user:
        raise InvalidTokenException("User associated with token no longer exists")
    if not user.is_active:
        raise AppException(
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="ERR-AUTH-004",
            message="User account is deactivated"
        )
    return user

def require_role(allowed_roles: List[str]):
    """Role-Based Access Control decorator/dependency."""
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise PermissionDeniedException(
                f"Action requires one of the following roles: {', '.join(allowed_roles)}"
            )
        return current_user
    return role_checker
