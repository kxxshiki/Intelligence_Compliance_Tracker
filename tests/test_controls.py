from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_control_crud_flow():
    response = client.post("/api/v1/controls", json={
        "control_id": "TEST-001",
        "name": "Test Control",
        "description": "Test description",
        "framework": "NIST",
        "category": "USER",
        "severity": "high",
        "rule_definition": {"field": "mfa_enabled", "operator": "equals", "expected": True},
        "active": True,
    })
    assert response.status_code == 201
    control_id = response.json()["id"]

    list_response = client.get("/api/v1/controls")
    assert list_response.status_code == 200
    assert any(item["control_id"] == "TEST-001" for item in list_response.json())

    get_response = client.get(f"/api/v1/controls/{control_id}")
    assert get_response.status_code == 200

    patched = client.put(f"/api/v1/controls/{control_id}", json={"name": "Updated Test Control"})
    assert patched.status_code == 200
    assert patched.json()["name"] == "Updated Test Control"

    deleted = client.delete(f"/api/v1/controls/{control_id}")
    assert deleted.status_code == 200
