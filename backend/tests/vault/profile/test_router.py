from fastapi.testclient import TestClient

from career_copilot.main import app

client = TestClient(app)

VALID_PROFILE = {
    "full_name": "Giorgos Example",
    "headline": "Backend Developer",
    "birth_date": "2000-01-15",
    "email": "giorgos@example.com",
    "linkedin_url": "https://www.linkedin.com/in/example",
    "github_url": "https://github.com/example",
}


# --- GET /profile ---
def test_get_profile_returns_404_when_not_created():
    get_response = client.get("/profile")
    assert get_response.status_code == 404
    assert get_response.json()["detail"] == "Profile not found"


# --- PUT /profile ---
def test_put_profile_creates_profile():
    update_response = client.put("/profile", json=VALID_PROFILE)

    assert update_response.status_code == 200
    assert update_response.json()["full_name"] == VALID_PROFILE["full_name"]
    assert update_response.json()["email"] == VALID_PROFILE["email"]
    assert update_response.json()["birth_date"] == VALID_PROFILE["birth_date"]
    assert update_response.json()["linkedin_url"] == VALID_PROFILE["linkedin_url"]
    assert update_response.json()["phone"] is None

    get_response = client.get("/profile")

    assert get_response.status_code == 200
    assert get_response.json()["full_name"] == VALID_PROFILE["full_name"]


def test_put_profile_replaces_existing_profile():
    update_response = client.put("/profile", json=VALID_PROFILE)

    assert update_response.status_code == 200

    profile_id = update_response.json()["id"]

    new_response = client.put("/profile", json={**VALID_PROFILE, "headline": "Python Developer"})

    assert new_response.status_code == 200
    assert new_response.json()["headline"] == "Python Developer"
    assert new_response.json()["id"] == profile_id

    get_response = client.get("/profile")

    assert get_response.json()["headline"] == "Python Developer"
    assert get_response.json()["id"] == profile_id


def test_put_profile_returns_422_for_invalid_email():
    update_response = client.put("/profile", json={**VALID_PROFILE, "email": "not-an-email"})

    assert update_response.status_code == 422


def test_put_profile_returns_422_for_invalid_url():
    update_response = client.put("/profile", json={**VALID_PROFILE, "linkedin_url": "not-a-url"})

    assert update_response.status_code == 422


def test_put_profile_returns_422_when_required_field_is_missing():
    profile = VALID_PROFILE.copy()
    del profile["full_name"]

    update_response = client.put("/profile", json=profile)

    assert update_response.status_code == 422


def test_put_profile_returns_422_for_empty_full_name():
    update_response = client.put("/profile", json={**VALID_PROFILE, "full_name": ""})

    assert update_response.status_code == 422
