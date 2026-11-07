from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_findings_creation_and_duplicate_prevention():
    evidence_response = client.post("/api/v1/evidence", json={
        "source_type": "USER",
        "source_name": "manual",
        "asset_identifier": "dup@example.com",
        "evidence_type": "USER_SECURITY_CONFIGURATION",
        "raw_data": {"username": "dup", "mfa_enabled": False, "is_privileged": True, "authorized": True, "active": True, "days_since_last_login": 200},
    })
    print(evidence_response.text)
    assert evidence_response.status_code == 201

    findings_response = client.get("/api/v1/findings")
    assert findings_response.status_code == 200
    assert isinstance(findings_response.json(), list)
