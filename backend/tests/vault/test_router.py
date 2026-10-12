from fastapi.testclient import TestClient

from career_copilot.main import app

client = TestClient(app)


def test_create_skill_with_valid_data():
    response = client.post("/skills", json={"name": "Python", "level": 4, "years": 3.5})

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Python"
    assert data["level"] == 4
    assert data["years"] == 3.5
    assert "id" in data


def test_create_skill_with_invalid_level_returns_422():
    response = client.post("/skills", json={"name": "Python", "level": 999})

    assert response.status_code == 422


def test_list_skills_returns_created_skill():
    create_response = client.post("/skills", json={"name": "Docker", "level": 4})

    assert create_response.status_code == 201

    list_response = client.get("/skills")

    assert list_response.status_code == 200
    data = list_response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Docker"
