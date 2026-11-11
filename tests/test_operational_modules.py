from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_assets_frameworks_analytics_and_jobs_routes_are_registered():
    asset_response = client.post(
        "/api/v1/assets",
        json={
            "name": "Primary Database",
            "asset_type": "Database",
            "environment": "production",
            "owner": "platform",
            "status": "active",
            "metadata": {"region": "us-east"},
        },
    )
    assert asset_response.status_code == 201
    asset_id = asset_response.json()["id"]

    framework_response = client.post(
        "/api/v1/frameworks",
        json={
            "name": "ISO 27001",
            "abbreviation": "ISO27001",
            "version": "2022",
            "status": "active",
            "description": "Information security management",
        },
    )
    assert framework_response.status_code == 201

    analytics_response = client.get("/api/v1/analytics/dashboard")
    assert analytics_response.status_code == 200
    payload = analytics_response.json()
    assert "overall_compliance_score" in payload

    job_response = client.post("/api/v1/jobs", params={"name": "evidence-collection"})
    assert job_response.status_code == 201
    assert job_response.json()["name"] == "evidence-collection"

    asset_lookup = client.get(f"/api/v1/assets/{asset_id}")
    assert asset_lookup.status_code == 200
    assert asset_lookup.json()["name"] == "Primary Database"
