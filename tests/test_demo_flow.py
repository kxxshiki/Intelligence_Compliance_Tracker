from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_demo_seed_and_collect():
    seed_response = client.post("/api/v1/demo/seed")
    assert seed_response.status_code == 200
    assert seed_response.json()["count"] >= 10

    collect_response = client.post("/api/v1/demo/collect-evidence")
    assert collect_response.status_code == 200
    assert "count" in collect_response.json()
