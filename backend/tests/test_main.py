from fastapi.testclient import TestClient

from career_copilot.main import app

client = TestClient(app)


def test_health_reports_ok():
    get_response = client.get("/api/health")

    assert get_response.status_code == 200
    assert get_response.json() == {"status": "ok"}
