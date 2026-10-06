def test_login_success(client):
    response = client.post("/api/v1/auth/login", json={
        "email": "admin@techcorp.com",
        "password": "Manager123!"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["role"] == "admin"
    assert data["email"] == "admin@techcorp.com"

def test_login_invalid_password(client):
    response = client.post("/api/v1/auth/login", json={
        "email": "admin@techcorp.com",
        "password": "WrongPassword999!"
    })
    assert response.status_code == 401
    data = response.json()
    assert data["error_code"] == "ERR-AUTH-002"

def test_login_nonexistent_user(client):
    response = client.post("/api/v1/auth/login", json={
        "email": "nonexistent_user_999@domain.com",
        "password": "Password123!"
    })
    assert response.status_code == 401
    assert response.json()["error_code"] == "ERR-AUTH-002"

def test_get_me_authorized(client, admin_headers):
    response = client.get("/api/v1/auth/me", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "admin@techcorp.com"
    assert data["role"] == "admin"

def test_get_me_unauthorized(client):
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401
    assert response.json()["error_code"] == "ERR-AUTH-007"

def test_get_me_invalid_token(client):
    response = client.get("/api/v1/auth/me", headers={"Authorization": "Bearer invalid_garbage_token"})
    assert response.status_code == 401
    assert response.json()["error_code"] == "ERR-AUTH-006"

def test_register_user_duplicate_email(client):
    response = client.post("/api/v1/auth/register", json={
        "email": "admin@techcorp.com",
        "password": "Password123!",
        "full_name": "Duplicate Admin",
        "organization_name": "TechCorp Enterprise"
    })
    assert response.status_code == 400
    assert response.json()["error_code"] == "ERR-AUTH-001"
