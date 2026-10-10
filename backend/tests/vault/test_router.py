from fastapi.testclient import TestClient

from career_copilot.main import app

client = TestClient(app)


def test_create_skill_with_valid_data():
    response = client.post("/skills", json={"name": "Python", "level": 4, "years": 3.5})

    assert response.status_code == 201
    assert response.json() == {"name": "Python", "level": 4, "years": 3.5}


def test_create_skill_with_invalid_level_returns_422():

    response = client.post("/skills", json={"name": "Python", "level": 999})

    assert response.status_code == 422
