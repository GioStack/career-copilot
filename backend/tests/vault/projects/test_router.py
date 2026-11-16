from fastapi.testclient import TestClient

from career_copilot.main import app

client = TestClient(app)

VALID_PROJECT = {
    "name": "Example Project",
    "description": "A tool that tailors CVs to job postings.",
    "url": "https://github.com/example/project",
    "start_date": "2025-01-01",
    "end_date": "2025-06-30",
}


# --- POST /projects ---
def test_create_project_with_valid_data():
    create_response = client.post("/projects", json=VALID_PROJECT)

    assert create_response.status_code == 201

    data = create_response.json()

    assert data["name"] == VALID_PROJECT["name"]
    assert data["description"] == VALID_PROJECT["description"]
    assert data["url"] == VALID_PROJECT["url"]
    assert data["start_date"] == VALID_PROJECT["start_date"]
    assert data["end_date"] == VALID_PROJECT["end_date"]
    assert "id" in data


def test_create_project_with_only_name_returns_201():
    create_response = client.post("/projects", json={"name": "Career Copilot"})

    assert create_response.status_code == 201

    data = create_response.json()

    assert data["description"] is None
    assert data["url"] is None
    assert data["start_date"] is None
    assert data["end_date"] is None


def test_create_project_with_empty_name_returns_422():
    create_response = client.post("/projects", json={**VALID_PROJECT, "name": ""})

    assert create_response.status_code == 422


def test_create_project_with_description_of_501_characters_returns_422():
    create_response = client.post("/projects", json={**VALID_PROJECT, "description": "a" * 501})

    assert create_response.status_code == 422


def test_create_project_with_description_of_500_characters_returns_201():
    create_response = client.post("/projects", json={**VALID_PROJECT, "description": "a" * 500})

    assert create_response.status_code == 201


def test_create_project_with_invalid_url_returns_422():
    create_response = client.post("/projects", json={**VALID_PROJECT, "url": "not a url"})

    assert create_response.status_code == 422


def test_create_project_with_end_date_before_start_date_returns_422():
    create_response = client.post(
        "/projects", json={**VALID_PROJECT, "start_date": "2025-06-30", "end_date": "2025-01-01"}
    )

    assert create_response.status_code == 422


def test_create_project_with_end_date_equal_to_start_date_returns_201():
    create_response = client.post(
        "/projects", json={**VALID_PROJECT, "start_date": "2025-06-30", "end_date": "2025-06-30"}
    )

    assert create_response.status_code == 201


def test_create_project_with_only_end_date_returns_201():
    project = VALID_PROJECT.copy()
    del project["start_date"]

    create_response = client.post("/projects", json=project)

    assert create_response.status_code == 201


def test_create_project_with_only_start_date_returns_201():
    project = VALID_PROJECT.copy()
    del project["end_date"]

    create_response = client.post("/projects", json=project)

    assert create_response.status_code == 201
