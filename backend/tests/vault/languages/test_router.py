import uuid

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


# --- GET /languages/{language_id} ---
def test_get_language_returns_200():
    create_response = client.post("/languages", json=VALID_LANGUAGE)

    assert create_response.status_code == 201
    language_id = create_response.json()["id"]

    get_response = client.get(f"/languages/{language_id}")

    assert get_response.status_code == 200
    assert get_response.json()["name"] == VALID_LANGUAGE["name"]
    assert get_response.json()["level"] == VALID_LANGUAGE["level"]


def test_get_language_returns_404_when_not_found():
    language_id = uuid.uuid4()
    get_response = client.get(f"/languages/{language_id}")

    assert get_response.status_code == 404
    assert get_response.json()["detail"] == "Language not found"


def test_get_language_with_invalid_id_returns_422():
    get_response = client.get("/languages/abc")

    assert get_response.status_code == 422


# --- PUT /languages/{language_id} ---
def test_update_language_returns_200():
    create_response = client.post("/languages", json=VALID_LANGUAGE)

    assert create_response.status_code == 201
    language_id = create_response.json()["id"]

    update_response = client.put(
        f"/languages/{language_id}", json={**VALID_LANGUAGE, "level": "C2"}
    )

    assert update_response.status_code == 200
    assert update_response.json()["level"] == "C2"

    get_response = client.get(f"/languages/{language_id}")

    assert get_response.json()["level"] == "C2"


def test_update_language_returns_404_when_not_found():
    language_id = uuid.uuid4()
    update_response = client.put(f"/languages/{language_id}", json=VALID_LANGUAGE)

    assert update_response.status_code == 404
    assert update_response.json()["detail"] == "Language not found"


def test_update_language_with_invalid_id_returns_422():
    update_response = client.put("/languages/abc", json=VALID_LANGUAGE)

    assert update_response.status_code == 422


def test_update_language_with_unknown_level_returns_422():
    create_response = client.post("/languages", json=VALID_LANGUAGE)

    assert create_response.status_code == 201
    language_id = create_response.json()["id"]

    update_response = client.put(
        f"/languages/{language_id}", json={**VALID_LANGUAGE, "level": "Fluent"}
    )

    assert update_response.status_code == 422
