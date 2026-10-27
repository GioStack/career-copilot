from fastapi.testclient import TestClient

from career_copilot.main import app

client = TestClient(app)

VALID_EXPERIENCE = {
    "title": "Backend Developer",
    "company": "Example Co",
    "location": "Thessaloniki, Greece",
    "start_date": "2024-03-01",
    "end_date": "2025-06-30",
    "description": "Built REST APIs with FastAPI.",
}


# --- POST /experiences ---
def test_create_experience_with_valid_data():
    create_response = client.post("/experiences", json=VALID_EXPERIENCE)

    assert create_response.status_code == 201

    data = create_response.json()

    assert data["title"] == VALID_EXPERIENCE["title"]
    assert data["start_date"] == VALID_EXPERIENCE["start_date"]
    assert data["end_date"] == VALID_EXPERIENCE["end_date"]
    assert "id" in data


def test_create_experience_without_end_date_returns_201():
    create_response = client.post("/experiences", json={**VALID_EXPERIENCE, "end_date": None})

    assert create_response.status_code == 201
    assert create_response.json()["end_date"] is None


def test_create_experience_with_end_date_equal_to_start_date_returns_201():
    start_date = VALID_EXPERIENCE["start_date"]
    create_response = client.post("/experiences", json={**VALID_EXPERIENCE, "end_date": start_date})

    assert create_response.status_code == 201
    assert create_response.json()["end_date"] == start_date


def test_create_experience_with_empty_title_returns_422():
    create_response = client.post("/experiences", json={**VALID_EXPERIENCE, "title": ""})

    assert create_response.status_code == 422


def test_create_experience_without_start_date_returns_422():
    experience = VALID_EXPERIENCE.copy()
    del experience["start_date"]

    create_response = client.post("/experiences", json=experience)

    assert create_response.status_code == 422


def test_create_experience_with_end_date_before_start_date_returns_422():
    create_response = client.post(
        "/experiences", json={**VALID_EXPERIENCE, "end_date": "2024-02-01"}
    )

    assert create_response.status_code == 422
