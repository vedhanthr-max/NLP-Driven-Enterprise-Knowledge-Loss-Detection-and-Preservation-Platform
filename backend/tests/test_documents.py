import io

def test_upload_text_document(client, manager_headers):
    content = (
        "AWS Cloud Infrastructure and Microservices Deployment Guide.\n"
        "This document details the configuration for Amazon Web Services EC2 and RDS instances.\n"
        "Written by Arun Kumar and maintained by the DevOps SRE team.\n"
        "Step 1: Authenticate with IAM credentials.\n"
        "Step 2: Deploy container images using Docker and Kubernetes.\n"
        "Step 3: Verify PostgreSQL database connectivity."
    )
    file_bytes = content.encode("utf-8")
    
    response = client.post(
        "/api/v1/documents/upload",
        headers=manager_headers,
        data={"title": "AWS SRE Operations Manual", "description": "Cloud infrastructure instructions"},
        files={"file": ("aws_sre_manual.txt", io.BytesIO(file_bytes), "text/plain")}
    )
    assert response.status_code == 202
    data = response.json()
    assert data["document_id"] > 0
    assert data["status"] == "completed"
    assert data["chunks_created"] >= 1
    assert data["knowledge_item_id"] is not None

def test_upload_invalid_file_extension(client, manager_headers):
    file_bytes = b"echo 'malicious script'"
    response = client.post(
        "/api/v1/documents/upload",
        headers=manager_headers,
        data={"title": "Executable File"},
        files={"file": ("malware.exe", io.BytesIO(file_bytes), "application/octet-stream")}
    )
    assert response.status_code == 400
    assert response.json()["error_code"] == "ERR-DOC-002"

def test_get_document_list(client, manager_headers):
    response = client.get("/api/v1/documents", headers=manager_headers)
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "documents" in data
    assert len(data["documents"]) >= 1

def test_get_document_details(client, manager_headers):
    # Fetch first document from list
    list_res = client.get("/api/v1/documents", headers=manager_headers)
    doc_id = list_res.json()["documents"][0]["document_id"]

    response = client.get(f"/api/v1/documents/{doc_id}", headers=manager_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["document_id"] == doc_id
    assert "chunks" in data
    assert len(data["chunks"]) >= 1

def test_get_nonexistent_document(client, manager_headers):
    response = client.get("/api/v1/documents/99999", headers=manager_headers)
    assert response.status_code == 404
    assert response.json()["error_code"] == "ERR-DOC-001"
