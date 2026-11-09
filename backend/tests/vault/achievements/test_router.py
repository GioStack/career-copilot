import uuid

from fastapi.testclient import TestClient

from career_copilot.main import app

client = TestClient(app)

VALID_EXPERIENCE = {
    "title": "Backend Developer",
    "company": "Example Co",
    "start_date": "2024-03-01",
}

VALID_ACHIEVEMENT = {"text": "Reduced API response time by 40%"}


# --- POST /experiences/{experience_id}/achievements ---
def test_create_achievement_with_valid_data():
    create_response = client.post("/experiences", json=VALID_EXPERIENCE)

    assert create_response.status_code == 201

    experience_id = create_response.json()["id"]

    achievement_response = client.post(
        f"/experiences/{experience_id}/achievements", json=VALID_ACHIEVEMENT
    )

    assert achievement_response.status_code == 201

    data = achievement_response.json()

    assert data["text"] == VALID_ACHIEVEMENT["text"]
    assert data["experience_id"] == experience_id
    assert data["position"] == 1
    assert "id" in data


def test_create_achievement_sets_the_next_position():
    create_response = client.post("/experiences", json=VALID_EXPERIENCE)

    assert create_response.status_code == 201
    experience_id = create_response.json()["id"]

    first_response = client.post(
        f"/experiences/{experience_id}/achievements", json=VALID_ACHIEVEMENT
    )

    assert first_response.status_code == 201

    achievement_response = client.post(
        f"/experiences/{experience_id}/achievements", json=VALID_ACHIEVEMENT
    )

    assert achievement_response.status_code == 201
    assert achievement_response.json()["position"] == 2


def test_create_achievement_starts_at_position_1_for_each_experience():
    # First Experience+Achievement
    first_experience_response = client.post("/experiences", json=VALID_EXPERIENCE)

    assert first_experience_response.status_code == 201
    first_experience_id = first_experience_response.json()["id"]

    first_response = client.post(
        f"/experiences/{first_experience_id}/achievements", json=VALID_ACHIEVEMENT
    )

    assert first_response.status_code == 201

    # Second Experience+Achievement
    second_experience_response = client.post("/experiences", json=VALID_EXPERIENCE)

    assert second_experience_response.status_code == 201
    second_experience_id = second_experience_response.json()["id"]

    achievement_response = client.post(
        f"/experiences/{second_experience_id}/achievements", json=VALID_ACHIEVEMENT
    )

    assert achievement_response.status_code == 201
    assert achievement_response.json()["position"] == 1


def test_create_achievement_with_empty_text_returns_422():
    create_response = client.post("/experiences", json=VALID_EXPERIENCE)

    assert create_response.status_code == 201
    experience_id = create_response.json()["id"]

    achievement_response = client.post(
        f"/experiences/{experience_id}/achievements", json={**VALID_ACHIEVEMENT, "text": ""}
    )

    assert achievement_response.status_code == 422


def test_create_achievement_returns_404_when_experience_not_found():
    experience_id = uuid.uuid4()
    achievement_response = client.post(
        f"/experiences/{experience_id}/achievements", json=VALID_ACHIEVEMENT
    )

    assert achievement_response.status_code == 404
    assert achievement_response.json()["detail"] == "Experience not found"


def test_create_achievement_with_invalid_experience_id_returns_422():
    achievement_response = client.post("/experiences/abc/achievements", json=VALID_ACHIEVEMENT)

    assert achievement_response.status_code == 422


# --- GET /experiences/{experience_id}/achievements ---
def test_list_achievements_returns_them_in_position_order():
    create_response = client.post("/experiences", json=VALID_EXPERIENCE)

    assert create_response.status_code == 201
    experience_id = create_response.json()["id"]

    first_response = client.post(
        f"/experiences/{experience_id}/achievements",
        json={**VALID_ACHIEVEMENT, "text": "First Achievement"},
    )

    assert first_response.status_code == 201

    second_response = client.post(
        f"/experiences/{experience_id}/achievements",
        json={**VALID_ACHIEVEMENT, "text": "Second Achievement"},
    )

    assert second_response.status_code == 201

    get_response = client.get(f"/experiences/{experience_id}/achievements")

    assert get_response.status_code == 200
    assert [achievement["text"] for achievement in get_response.json()] == [
        "First Achievement",
        "Second Achievement",
    ]


def test_list_achievements_returns_only_those_of_the_experience():
    # Experience A + achievement
    first_experience_response = client.post("/experiences", json=VALID_EXPERIENCE)

    assert first_experience_response.status_code == 201
    first_experience_id = first_experience_response.json()["id"]

    first_response = client.post(
        f"/experiences/{first_experience_id}/achievements",
        json={**VALID_ACHIEVEMENT, "text": "A Experience Achievement"},
    )

    assert first_response.status_code == 201

    # Experience B + achievement
    second_experience_response = client.post("/experiences", json=VALID_EXPERIENCE)

    assert second_experience_response.status_code == 201
    second_experience_id = second_experience_response.json()["id"]

    second_response = client.post(
        f"/experiences/{second_experience_id}/achievements",
        json={**VALID_ACHIEVEMENT, "text": "B Experience Achievement"},
    )

    assert second_response.status_code == 201

    # List of Experience A
    get_response = client.get(f"/experiences/{first_experience_id}/achievements")

    assert get_response.status_code == 200
    assert [achievement["text"] for achievement in get_response.json()] == [
        "A Experience Achievement"
    ]


def test_list_achievements_returns_404_when_experience_not_found():

    experience_id = uuid.uuid4()

    get_response = client.get(f"/experiences/{experience_id}/achievements")

    assert get_response.status_code == 404
    assert get_response.json()["detail"] == "Experience not found"


def test_list_achievements_with_invalid_experience_id_returns_422():
    get_response = client.get("/experiences/abc/achievements")

    assert get_response.status_code == 422


# --- DELETE /experiences/{experience_id} ---
def test_delete_experience_with_achievements_returns_204():
    create_response = client.post("/experiences", json=VALID_EXPERIENCE)

    assert create_response.status_code == 201
    experience_id = create_response.json()["id"]

    achievement_response = client.post(
        f"/experiences/{experience_id}/achievements", json=VALID_ACHIEVEMENT
    )

    assert achievement_response.status_code == 201

    delete_response = client.delete(f"/experiences/{experience_id}")

    # Without ON DELETE CASCADE, the foreign key would block this delete.
    assert delete_response.status_code == 204
