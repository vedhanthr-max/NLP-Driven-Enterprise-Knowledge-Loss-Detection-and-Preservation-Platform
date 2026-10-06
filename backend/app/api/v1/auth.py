from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.auth_service import AuthService, get_current_user
from app.models.entities import User, AuditLog
from app.schemas.auth import (
    UserRegisterRequest, UserRegisterResponse, UserLoginRequest,
    TokenResponse, UserOut, RefreshTokenRequest
)
from app.core.security import decode_token, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserRegisterResponse, status_code=status.HTTP_201_CREATED)
def register(req: UserRegisterRequest, db: Session = Depends(get_db)):
    """Register a new enterprise user and organization."""
    res = AuthService.register_user(db, req)
    db.add(AuditLog(
        organization_id=res.organization_id,
        user_id=res.user_id,
        action_type="register",
        resource_type="user",
        resource_id=res.user_id,
        status="success"
    ))
    db.commit()
    return res

@router.post("/login", response_model=TokenResponse)
def login(req: UserLoginRequest, db: Session = Depends(get_db)):
    """Authenticate with email and password to receive JWT bearer tokens."""
    user = AuthService.authenticate_user(db, req.email, req.password)
    tokens = AuthService.create_user_tokens(user)
    db.add(AuditLog(
        organization_id=user.organization_id,
        user_id=user.user_id,
        action_type="login",
        resource_type="user",
        resource_id=user.user_id,
        status="success"
    ))
    db.commit()
    return tokens

@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    """Retrieve authenticated user's profile and organization info."""
    return current_user

@router.post("/refresh")
def refresh_token(req: RefreshTokenRequest, db: Session = Depends(get_db)):
    """Generate new access token from valid refresh token."""
    payload = decode_token(req.refresh_token)
    if payload.get("type") != "refresh":
        from app.core.exceptions import InvalidTokenException
        raise InvalidTokenException("Supplied token is not a refresh token")

    user_id = payload.get("sub")
    user = db.query(User).filter(User.user_id == int(user_id)).first()
    if not user or not user.is_active:
        from app.core.exceptions import InvalidTokenException
        raise InvalidTokenException("User is inactive or not found")

    new_token_data = {
        "sub": str(user.user_id),
        "email": user.email,
        "role": user.role,
        "org_id": user.organization_id
    }
    new_access_token = create_access_token(new_token_data)
    return {
        "access_token": new_access_token,
        "token_type": "bearer",
        "expires_in": 3600
    }

@router.post("/logout")
def logout(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Log out user and record audit log."""
    db.add(AuditLog(
        organization_id=current_user.organization_id,
        user_id=current_user.user_id,
        action_type="logout",
        resource_type="user",
        resource_id=current_user.user_id,
        status="success"
    ))
    db.commit()
    return {"message": "Logged out successfully"}
