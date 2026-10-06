def test_list_preservation_actions(client, manager_headers):
    response = client.get("/api/v1/preservation-actions", headers=manager_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    action = data[0]
    assert "action_description" in action
    assert "status" in action
    assert "priority" in action

def test_create_and_update_preservation_action(client, manager_headers):
    # Fetch first knowledge item
    know_res = client.get("/api/v1/knowledge", headers=manager_headers)
    knowledge_id = know_res.json()["items"][0]["knowledge_id"]

    # 1. Create Action
    create_res = client.post(
        "/api/v1/preservation-actions",
        headers=manager_headers,
        json={
            "knowledge_id": knowledge_id,
            "action_type": "documentation",
            "action_description": "Record comprehensive video walkthrough of incident recovery",
            "priority": "high",
            "estimated_hours": 30
        }
    )
    assert create_res.status_code == 201
    action_data = create_res.json()
    action_id = action_data["action_id"]
    assert action_data["status"] == "recommended"

    # 2. Update Action to in_progress
    update_res = client.put(
        f"/api/v1/preservation-actions/{action_id}",
        headers=manager_headers,
        json={
            "status": "in_progress",
            "actual_hours": 10,
            "completion_notes": "First 3 video modules recorded and stored in repository."
        }
    )
    assert update_res.status_code == 200
    updated_data = update_res.json()
    assert updated_data["status"] == "in_progress"
    assert updated_data["actual_hours"] == 10
