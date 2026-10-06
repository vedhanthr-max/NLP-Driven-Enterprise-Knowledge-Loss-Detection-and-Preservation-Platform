from app.risk.scoring import calculate_risk_score, classify_risk_level

def test_risk_score_documented_example_1():
    # Example 1: Legacy Payment System
    # (92 × 0.30) + (95 × 0.25) + (85 × 0.20) + (80 × 0.15) + (90 × 0.10) = 89.35
    score = calculate_risk_score(92, 95, 85, 80, 90)
    assert score == 89.35
    assert classify_risk_level(score) == "critical"

def test_risk_score_documented_example_2():
    # Example 2: General Framework Knowledge
    # (65 × 0.30) + (35 × 0.25) + (45 × 0.20) + (40 × 0.15) + (20 × 0.10) = 45.25
    score = calculate_risk_score(65, 35, 45, 40, 20)
    assert score == 45.25
    assert classify_risk_level(score) == "medium"

def test_risk_score_documented_example_3():
    # Example 3: Well-Documented Process
    # (75 × 0.30) + (20 × 0.25) + (50 × 0.20) + (10 × 0.15) + (15 × 0.10) = 40.50
    score = calculate_risk_score(75, 20, 50, 10, 15)
    assert score == 40.50
    assert classify_risk_level(score) == "medium"

def test_risk_score_use_case_1():
    # Use Case 1: Legacy Banking System
    # (95 × 0.30) + (98 × 0.25) + (92 × 0.20) + (85 × 0.15) + (90 × 0.10) = 93.15
    score = calculate_risk_score(95, 98, 92, 85, 90)
    assert score == 93.15
    assert classify_risk_level(score) == "critical"

def test_risk_score_use_case_2():
    # Use Case 2: Kubernetes Pipeline
    # (60 × 0.30) + (25 × 0.25) + (45 × 0.20) + (15 × 0.15) + (20 × 0.10) = 37.50
    score = calculate_risk_score(60, 25, 45, 15, 20)
    assert score == 37.50
    assert classify_risk_level(score) == "medium"

def test_risk_score_use_case_3():
    # Use Case 3: AWS Database Migration
    # (95 × 0.30) + (90 × 0.25) + (85 × 0.20) + (20 × 0.15) + (33 × 0.10) = 74.30
    score = calculate_risk_score(95, 90, 85, 20, 33)
    assert score == 74.30
    assert classify_risk_level(score) == "high"

def test_risk_simulation_endpoint(client):
    response = client.post("/api/v1/risk/simulate", json={
        "criticality": 95.0,
        "uniqueness": 98.0,
        "dependency": 92.0,
        "documentation_gap": 85.0,
        "availability_risk": 90.0
    })
    assert response.status_code == 200
    data = response.json()
    assert data["risk_score"] == 93.15
    assert data["risk_level"] == "critical"
    assert len(data["factor_breakdown"]) == 5
    assert len(data["recommendations"]) >= 1

def test_risk_dashboard_endpoint(client, manager_headers):
    response = client.get("/api/v1/risk/dashboard", headers=manager_headers)
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert "risk_distribution" in data
    assert data["summary"]["total_knowledge_items"] >= 1
    assert data["summary"]["average_risk_score"] > 0
