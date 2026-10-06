from app.ml.classifier import predict_risk_level

def test_ml_metrics_endpoint(client, manager_headers):
    response = client.get("/api/v1/ml/metrics", headers=manager_headers)
    assert response.status_code == 200
    data = response.json()
    assert "metrics" in data or "models_evaluated" in data
    metrics = data.get("metrics") or data["models_evaluated"][0]
    
    # Target SLA: Accuracy >= 80%
    assert metrics["accuracy"] >= 0.80
    assert metrics["f1_score"] >= 0.75
    assert len(metrics["confusion_matrix"]) == 4
    assert "feature_importances" in metrics
    assert len(metrics["feature_importances"]) >= 5

def test_ml_predict_critical_scenario(client, manager_headers):
    response = client.post("/api/v1/ml/predict", headers=manager_headers, json={
        "criticality": 95.0,
        "uniqueness": 98.0,
        "dependency": 92.0,
        "documentation_gap": 85.0,
        "availability_risk": 90.0,
        "num_experts": 1,
        "num_systems": 5,
        "doc_length": 500
    })
    assert response.status_code == 200
    data = response.json()
    assert data["predicted_level"] in ("critical", "high")
    assert 0.0 <= data["confidence"] <= 1.0
    assert "class_probabilities" in data

def test_ml_predict_low_scenario(client, manager_headers):
    response = client.post("/api/v1/ml/predict", headers=manager_headers, json={
        "criticality": 30.0,
        "uniqueness": 15.0,
        "dependency": 25.0,
        "documentation_gap": 10.0,
        "availability_risk": 15.0,
        "num_experts": 8,
        "num_systems": 1,
        "doc_length": 5000
    })
    assert response.status_code == 200
    data = response.json()
    assert data["predicted_level"] in ("low", "medium")
    assert 0.0 <= data["confidence"] <= 1.0
