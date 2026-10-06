from app.core.security import verify_password, hash_password

def test_password_hashing_bcrypt():
    pwd = "SecurePassword123!"
    hashed = hash_password(pwd)
    assert hashed != pwd
    assert hashed.startswith("$2b$")  # bcrypt prefix
    assert verify_password(pwd, hashed) is True
    assert verify_password("WrongPassword!", hashed) is False

def test_sql_injection_prevention_search(client, manager_headers):
    sqli_query = "' OR '1'='1'; DROP TABLE users; --"
    response = client.get(f"/api/v1/search?q={sqli_query}", headers=manager_headers)
    assert response.status_code == 200  # Safely parameterized query

def test_sql_injection_prevention_knowledge_filter(client, manager_headers):
    sqli_category = "General' OR '1'='1"
    response = client.get(f"/api/v1/knowledge?category={sqli_category}", headers=manager_headers)
    assert response.status_code == 200

def test_role_restriction_employee_forbidden_admin_audit(client, employee_headers):
    # Employee should NOT be able to view audit logs (requires admin or manager)
    # rajesh is an employee
    response = client.get("/api/v1/audit/logs", headers=employee_headers)
    assert response.status_code == 403
    assert response.json()["error_code"] == "ERR-PERM-001"

def test_role_restriction_employee_forbidden_train_endpoint(client, employee_headers):
    response = client.post("/api/v1/ml/train", headers=employee_headers)
    assert response.status_code == 403
    assert response.json()["error_code"] == "ERR-PERM-001"

def test_xss_prevention_in_knowledge_creation(client, manager_headers):
    xss_payload = "<script>alert('XSS-ATTACK')</script>"
    response = client.post("/api/v1/knowledge", headers=manager_headers, json={
        "title": f"Test Knowledge {xss_payload}",
        "description": "Safe test description",
        "category": "General",
        "tags": ["test"]
    })
    assert response.status_code == 201
    data = response.json()
    assert data["knowledge_id"] > 0
