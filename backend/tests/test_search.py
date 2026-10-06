def test_semantic_search_legacy_payment(client, manager_headers):
    response = client.get("/api/v1/search?q=legacy+payment+system+failover+procedure", headers=manager_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total_results"] >= 1
    assert data["search_time_ms"] < 500.0  # Search SLA < 500ms
    top_result = data["results"][0]
    assert "payment" in top_result["title"].lower() or "payment" in top_result["snippet"].lower()
    assert top_result["relevance_score"] > 0.3

def test_semantic_search_kubernetes_deployment(client, manager_headers):
    response = client.get("/api/v1/search?q=how+to+deploy+microservices+with+docker+and+helm", headers=manager_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total_results"] >= 1
    titles = [r["title"].lower() for r in data["results"]]
    assert any("kubernetes" in t or "docker" in t for t in titles)

def test_semantic_search_empty_query(client, manager_headers):
    response = client.get("/api/v1/search?q=", headers=manager_headers)
    assert response.status_code == 422 or response.status_code == 400
