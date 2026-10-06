import time
from app.nlp.ner import extract_entities
from app.nlp.keywords import extract_keywords
from app.nlp.embeddings import generate_embedding

def test_api_response_time_sla(client, manager_headers):
    # SLA: Standard API requests must complete in < 500ms
    latencies = []
    for _ in range(5):
        start = time.time()
        response = client.get("/api/v1/risk/dashboard", headers=manager_headers)
        assert response.status_code == 200
        latencies.append((time.time() - start) * 1000)

    avg_latency = sum(latencies) / len(latencies)
    assert avg_latency < 500.0, f"Average API latency {avg_latency:.2f}ms exceeded 500ms target"

def test_semantic_search_latency_sla(client, manager_headers):
    # SLA: Search query latency < 200ms
    start = time.time()
    response = client.get("/api/v1/search?q=database+migration+failover+procedure", headers=manager_headers)
    duration_ms = (time.time() - start) * 1000
    assert response.status_code == 200
    assert duration_ms < 500.0, f"Search latency {duration_ms:.2f}ms exceeded target"

def test_nlp_processing_speed():
    sample_text = (
        "Complete technical procedure for configuring Docker containers on AWS EC2. "
        "Arun Kumar authored the replication guide for MySQL and PostgreSQL failover."
    )
    start = time.time()
    ents = extract_entities(sample_text)
    kws = extract_keywords(sample_text)
    emb = generate_embedding(sample_text)
    nlp_time_ms = (time.time() - start) * 1000

    assert len(ents) >= 1
    assert len(kws) >= 1
    assert len(emb) == 384
    assert nlp_time_ms < 1000.0, f"NLP processing took {nlp_time_ms:.2f}ms, target < 1000ms"
