from fastapi.testclient import TestClient

from career_copilot.main import app

client = TestClient(app)

VALID_LANGUAGE = {"name": "English", "level": "C1"}


# --- POST /languages ---
def test_create_language_with_valid_data():
    create_response = client.post("/languages", json=VALID_LANGUAGE)

    assert create_response.status_code == 201

    data = create_response.json()

    assert data["name"] == VALID_LANGUAGE["name"]
    assert data["level"] == VALID_LANGUAGE["level"]
    assert "id" in data


def test_create_language_with_native_level_returns_201():
    create_response = client.post("/languages", json={**VALID_LANGUAGE, "level": "Native"})

    assert create_response.status_code == 201
    assert create_response.json()["level"] == "Native"


def test_create_language_with_unknown_level_returns_422():
    create_response = client.post("/languages", json={**VALID_LANGUAGE, "level": "Fluent"})

    assert create_response.status_code == 422


def test_create_language_without_level_returns_422():
    language = VALID_LANGUAGE.copy()
    del language["level"]

    create_response = client.post("/languages", json=language)

    assert create_response.status_code == 422


def test_create_language_with_empty_name_returns_422():
    create_response = client.post("/languages", json={**VALID_LANGUAGE, "name": ""})

    assert create_response.status_code == 422


# --- GET /languages ---
def test_list_languages_returns_created_languages():
    create_response = client.post("/languages", json=VALID_LANGUAGE)

    assert create_response.status_code == 201

    get_response = client.get("/languages")

    assert get_response.status_code == 200
    assert [language["name"] for language in get_response.json()] == [VALID_LANGUAGE["name"]]
