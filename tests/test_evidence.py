from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_evidence_ingestion_and_hash():
    payload = {
        "source_type": "USER",
        "source_name": "manual",
        "asset_identifier": "demo-user@example.com",
        "evidence_type": "USER_SECURITY_CONFIGURATION",
        "raw_data": {"username": "demo-user", "mfa_enabled": False, "is_privileged": True, "authorized": True},
    }
    response = client.post("/api/v1/evidence", json=payload)
    assert response.status_code == 201, response.text
    body = response.json()
    assert body["evidence_hash"]
    evidence_id = body["id"]

    get_response = client.get(f"/api/v1/evidence/{evidence_id}")
    assert get_response.status_code == 200
    assert get_response.json()["asset_identifier"] == "demo-user@example.com"
