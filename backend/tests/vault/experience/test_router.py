import uuid

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


# --- GET /experiences ---
def test_list_experiences_returns_most_recent_first():
    older = {**VALID_EXPERIENCE, "start_date": "2020-01-01", "end_date": "2021-12-31"}
    newer = VALID_EXPERIENCE

    # Create the older entry first, so the test fails if the list is not sorted.
    assert client.post("/experiences", json=older).status_code == 201
    assert client.post("/experiences", json=newer).status_code == 201

    get_response = client.get("/experiences")

    assert get_response.status_code == 200
    data = get_response.json()
    assert len(data) == 2
    assert data[0]["start_date"] == newer["start_date"]
    assert data[1]["start_date"] == older["start_date"]


def test_list_experiences_returns_empty_list_when_no_experiences():
    get_response = client.get("/experiences")
    assert get_response.status_code == 200
    assert get_response.json() == []


# --- GET /experiences/{id} ---
def test_get_experience_by_id_returns_experience():
    create_response = client.post("/experiences", json=VALID_EXPERIENCE)

    assert create_response.status_code == 201

    experience_id = create_response.json()["id"]
    get_response = client.get(f"/experiences/{experience_id}")
    assert get_response.status_code == 200

    data = get_response.json()
    assert data["id"] == experience_id
    assert data["title"] == VALID_EXPERIENCE["title"]


def test_get_experience_by_id_returns_404_when_not_found():
    experience_uuid = uuid.uuid4()
    get_response = client.get(f"/experiences/{experience_uuid}")
    assert get_response.status_code == 404
    assert get_response.json()["detail"] == "Experience not found"


def test_get_experience_by_id_returns_422_when_id_is_invalid():
    get_response = client.get("/experiences/abc")

    assert get_response.status_code == 422


# --- PUT /experiences/{id} ---
def test_update_experience_returns_updated_experience():
    create_response = client.post("/experiences", json=VALID_EXPERIENCE)

    assert create_response.status_code == 201

    experience_id = create_response.json()["id"]

    update_response = client.put(
        f"/experiences/{experience_id}",
        json={**VALID_EXPERIENCE, "title": "Senior Backend Developer"},
    )

    assert update_response.status_code == 200

    data = update_response.json()

    assert data["id"] == experience_id
    assert data["title"] == "Senior Backend Developer"

    get_response = client.get(f"/experiences/{experience_id}")

    assert get_response.json()["title"] == "Senior Backend Developer"


def test_update_experience_returns_404_when_not_found():
    experience_id = uuid.uuid4()
    update_response = client.put(f"/experiences/{experience_id}", json=VALID_EXPERIENCE)

    assert update_response.status_code == 404
    assert update_response.json()["detail"] == "Experience not found"


def test_update_experience_returns_422_when_id_is_invalid():
    update_response = client.put("/experiences/abc", json=VALID_EXPERIENCE)

    assert update_response.status_code == 422


def test_update_experience_returns_422_when_body_is_invalid():
    create_response = client.post("/experiences", json=VALID_EXPERIENCE)

    assert create_response.status_code == 201

    experience_id = create_response.json()["id"]

    update_response = client.put(
        f"/experiences/{experience_id}", json={**VALID_EXPERIENCE, "end_date": "2024-02-01"}
    )

    assert update_response.status_code == 422
