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
    create_response = client.post("/education", json=VALID_EDUCATION)

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

    create_response = client.post("/education", json=education)

    assert create_response.status_code == 201

    data = create_response.json()

    assert data["location"] is None
    assert data["end_date"] is None
    assert data["grade"] is None
    assert data["description"] is None


def test_create_education_with_empty_institution_returns_422():
    create_response = client.post("/education", json={**VALID_EDUCATION, "institution": ""})

    assert create_response.status_code == 422


def test_create_education_with_empty_degree_returns_422():
    create_response = client.post("/education", json={**VALID_EDUCATION, "degree": ""})

    assert create_response.status_code == 422


def test_create_education_without_start_date_returns_422():
    education = VALID_EDUCATION.copy()
    del education["start_date"]

    create_response = client.post("/education", json=education)

    assert create_response.status_code == 422


def test_create_education_with_end_date_before_start_date_returns_422():
    create_response = client.post("/education", json={**VALID_EDUCATION, "end_date": "2018-09-01"})

    assert create_response.status_code == 422


def test_create_education_with_grade_0_returns_201():
    create_response = client.post("/education", json={**VALID_EDUCATION, "grade": 0})

    assert create_response.status_code == 201
    assert create_response.json()["grade"] == 0


def test_create_education_with_grade_10_returns_201():
    create_response = client.post("/education", json={**VALID_EDUCATION, "grade": 10})

    assert create_response.status_code == 201
    assert create_response.json()["grade"] == 10


def test_create_education_with_negative_grade_returns_422():
    create_response = client.post("/education", json={**VALID_EDUCATION, "grade": -0.1})

    assert create_response.status_code == 422


def test_create_education_with_grade_above_10_returns_422():
    create_response = client.post("/education", json={**VALID_EDUCATION, "grade": 10.1})

    assert create_response.status_code == 422
