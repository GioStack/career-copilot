import uuid

from fastapi.testclient import TestClient

from career_copilot.main import app

client = TestClient(app)

VALID_EDUCATION = {
    "institution": "Example University",
    "degree": "Diploma in Computer Engineering",
    "location": "Thessaloniki, Greece",
    "start_date": "2018-10-01",
    "end_date": "2024-07-01",
    "grade": 8.5,
    "description": "5-year programme, 300 ECTS.",
}


# --- POST /education ---
def test_create_education_with_valid_data():
    create_response = client.post("/api/education", json=VALID_EDUCATION)

    assert create_response.status_code == 201

    data = create_response.json()

    assert data["institution"] == VALID_EDUCATION["institution"]
    assert data["degree"] == VALID_EDUCATION["degree"]
    assert data["location"] == VALID_EDUCATION["location"]
    assert data["start_date"] == VALID_EDUCATION["start_date"]
    assert data["end_date"] == VALID_EDUCATION["end_date"]
    assert data["grade"] == VALID_EDUCATION["grade"]
    assert data["description"] == VALID_EDUCATION["description"]
    assert "id" in data


def test_create_education_without_optional_fields_returns_201():
    education = VALID_EDUCATION.copy()
    del education["location"]
    del education["end_date"]
    del education["grade"]
    del education["description"]

    create_response = client.post("/api/education", json=education)

    assert create_response.status_code == 201

    data = create_response.json()

    assert data["location"] is None
    assert data["end_date"] is None
    assert data["grade"] is None
    assert data["description"] is None


def test_create_education_with_empty_institution_returns_422():
    create_response = client.post("/api/education", json={**VALID_EDUCATION, "institution": ""})

    assert create_response.status_code == 422


def test_create_education_with_empty_degree_returns_422():
    create_response = client.post("/api/education", json={**VALID_EDUCATION, "degree": ""})

    assert create_response.status_code == 422


def test_create_education_without_start_date_returns_422():
    education = VALID_EDUCATION.copy()
    del education["start_date"]

    create_response = client.post("/api/education", json=education)

    assert create_response.status_code == 422


def test_create_education_with_end_date_before_start_date_returns_422():
    create_response = client.post(
        "/api/education", json={**VALID_EDUCATION, "end_date": "2018-09-01"}
    )

    assert create_response.status_code == 422


def test_create_education_with_grade_0_returns_201():
    create_response = client.post("/api/education", json={**VALID_EDUCATION, "grade": 0})

    assert create_response.status_code == 201
    assert create_response.json()["grade"] == 0


def test_create_education_with_grade_10_returns_201():
    create_response = client.post("/api/education", json={**VALID_EDUCATION, "grade": 10})

    assert create_response.status_code == 201
    assert create_response.json()["grade"] == 10


def test_create_education_with_negative_grade_returns_422():
    create_response = client.post("/api/education", json={**VALID_EDUCATION, "grade": -0.1})

    assert create_response.status_code == 422


def test_create_education_with_grade_above_10_returns_422():
    create_response = client.post("/api/education", json={**VALID_EDUCATION, "grade": 10.1})

    assert create_response.status_code == 422


# --- GET /education ---
def test_list_education_returns_most_recent_first():
    older = {**VALID_EDUCATION, "start_date": "2012-10-01", "end_date": "2016-07-01"}
    newer = VALID_EDUCATION

    # Create the older entry first, so the test fails if the list is not sorted.
    assert client.post("/api/education", json=older).status_code == 201
    assert client.post("/api/education", json=newer).status_code == 201

    get_response = client.get("/api/education")

    assert get_response.status_code == 200

    data = get_response.json()

    assert len(data) == 2
    assert data[0]["start_date"] == newer["start_date"]
    assert data[1]["start_date"] == older["start_date"]


# --- GET /education/{id} ---
def test_get_education_by_id_returns_education():
    create_response = client.post("/api/education", json=VALID_EDUCATION)

    assert create_response.status_code == 201

    education_id = create_response.json()["id"]

    get_response = client.get(f"/api/education/{education_id}")

    assert get_response.status_code == 200

    data = get_response.json()

    assert data["id"] == education_id
    assert data["institution"] == VALID_EDUCATION["institution"]
    assert data["degree"] == VALID_EDUCATION["degree"]
    assert data["location"] == VALID_EDUCATION["location"]
    assert data["start_date"] == VALID_EDUCATION["start_date"]
    assert data["end_date"] == VALID_EDUCATION["end_date"]
    assert data["grade"] == VALID_EDUCATION["grade"]
    assert data["description"] == VALID_EDUCATION["description"]


def test_get_education_by_id_returns_404_when_not_found():
    education_id = uuid.uuid4()

    get_response = client.get(f"/api/education/{education_id}")

    assert get_response.status_code == 404
    assert get_response.json()["detail"] == "Education not found"


def test_get_education_by_id_returns_422_when_id_is_invalid():
    get_response = client.get("/api/education/abc")

    assert get_response.status_code == 422


# --- PUT /education/{id} ---
def test_update_education_returns_updated_education():
    create_response = client.post("/api/education", json=VALID_EDUCATION)

    assert create_response.status_code == 201

    education_id = create_response.json()["id"]

    update_response = client.put(
        f"/api/education/{education_id}",
        json={**VALID_EDUCATION, "degree": "MSc in Computer Engineering"},
    )

    assert update_response.status_code == 200

    data = update_response.json()

    assert data["id"] == education_id
    assert data["degree"] == "MSc in Computer Engineering"

    get_response = client.get(f"/api/education/{education_id}")

    assert get_response.json()["degree"] == "MSc in Computer Engineering"


def test_update_education_sets_grade_to_none_when_not_sent():
    create_response = client.post("/api/education", json=VALID_EDUCATION)

    assert create_response.status_code == 201

    education_id = create_response.json()["id"]

    education = VALID_EDUCATION.copy()
    del education["grade"]

    update_response = client.put(f"/api/education/{education_id}", json=education)

    assert update_response.status_code == 200
    assert update_response.json()["grade"] is None

    get_response = client.get(f"/api/education/{education_id}")

    assert get_response.json()["grade"] is None


def test_update_education_returns_404_when_not_found():
    education_id = uuid.uuid4()

    update_response = client.put(f"/api/education/{education_id}", json=VALID_EDUCATION)

    assert update_response.status_code == 404
    assert update_response.json()["detail"] == "Education not found"


def test_update_education_returns_422_when_id_is_invalid():
    update_response = client.put("/api/education/abc", json=VALID_EDUCATION)

    assert update_response.status_code == 422


def test_update_education_returns_422_when_body_is_invalid():
    create_response = client.post("/api/education", json=VALID_EDUCATION)

    assert create_response.status_code == 201

    education_id = create_response.json()["id"]

    update_response = client.put(
        f"/api/education/{education_id}", json={**VALID_EDUCATION, "end_date": "2018-09-01"}
    )

    assert update_response.status_code == 422


# --- DELETE /education/{id} ---
def test_delete_education_returns_204():
    create_response = client.post("/api/education", json=VALID_EDUCATION)

    assert create_response.status_code == 201

    education_id = create_response.json()["id"]

    delete_response = client.delete(f"/api/education/{education_id}")

    assert delete_response.status_code == 204
    assert delete_response.content == b""

    get_response = client.get(f"/api/education/{education_id}")

    assert get_response.status_code == 404


def test_delete_education_returns_404_when_not_found():
    education_id = uuid.uuid4()

    delete_response = client.delete(f"/api/education/{education_id}")

    assert delete_response.status_code == 404
    assert delete_response.json()["detail"] == "Education not found"


def test_delete_education_returns_422_when_id_is_invalid():
    delete_response = client.delete("/api/education/abc")

    assert delete_response.status_code == 422
