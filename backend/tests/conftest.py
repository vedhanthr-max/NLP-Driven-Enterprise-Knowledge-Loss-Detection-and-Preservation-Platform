import os
import sys
import pytest
from fastapi.testclient import TestClient

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app
from app.core.database import SessionLocal, engine, Base
from app.core.security import hash_password, create_access_token
from app.models.entities import Organization, User, Employee

@pytest.fixture(scope="session")
def client():
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="session")
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="session")
def admin_headers(db_session):
    user = db_session.query(User).filter(User.email == "admin@techcorp.com").first()
    if not user:
        # Create test admin
        org = db_session.query(Organization).first()
        user = User(
            organization_id=org.organization_id,
            email="admin@techcorp.com",
            password_hash=hash_password("Manager123!"),
            full_name="Admin Test",
            role="admin",
            is_active=True
        )
        db_session.add(user)
        db_session.commit()
    token = create_access_token({"sub": str(user.user_id), "email": user.email, "role": user.role, "org_id": user.organization_id})
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture(scope="session")
def manager_headers(db_session):
    user = db_session.query(User).filter(User.email == "manager@techcorp.com").first()
    token = create_access_token({"sub": str(user.user_id), "email": user.email, "role": user.role, "org_id": user.organization_id})
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture(scope="session")
def employee_headers(db_session):
    user = db_session.query(User).filter(User.email == "rajesh@techcorp.com").first()
    token = create_access_token({"sub": str(user.user_id), "email": user.email, "role": user.role, "org_id": user.organization_id})
    return {"Authorization": f"Bearer {token}"}
