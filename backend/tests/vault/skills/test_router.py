import uuid

from fastapi.testclient import TestClient

from career_copilot.main import app

client = TestClient(app)


# --- POST /skills ---
def test_create_skill_with_valid_data():
    response = client.post("/skills", json={"name": "Python", "level": 4, "years": 3.5})

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Python"
    assert data["level"] == 4
    assert data["years"] == 3.5
    assert "id" in data


def test_create_skill_with_level_1_returns_201():
    response = client.post("/skills", json={"name": "Python", "level": 1})

    assert response.status_code == 201
    assert response.json()["level"] == 1


def test_create_skill_with_level_5_returns_201():
    response = client.post("/skills", json={"name": "Python", "level": 5})

    assert response.status_code == 201
    assert response.json()["level"] == 5


def test_create_skill_with_empty_name_returns_422():
    response = client.post("/skills", json={"name": "", "level": 3})

    assert response.status_code == 422


def test_create_skill_with_invalid_level_returns_422():
    response = client.post("/skills", json={"name": "Python", "level": 999})

    assert response.status_code == 422


def test_create_skill_with_level_below_1_returns_422():
    response = client.post("/skills", json={"name": "Python", "level": 0})

    assert response.status_code == 422


def test_create_skill_with_negative_years_returns_422():
    response = client.post("/skills", json={"name": "Python", "level": 3, "years": -1})

    assert response.status_code == 422


def test_create_skill_with_years_above_50_returns_422():
    response = client.post("/skills", json={"name": "Python", "level": 3, "years": 51})

    assert response.status_code == 422


# --- GET /skills ---
def test_list_skills_returns_created_skill():
    create_response = client.post("/skills", json={"name": "Docker", "level": 4})

    assert create_response.status_code == 201

    list_response = client.get("/skills")

    assert list_response.status_code == 200
    data = list_response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Docker"


def test_list_skills_returns_empty_list_when_no_skills():
    list_response = client.get("/skills")

    assert list_response.status_code == 200
    data = list_response.json()
    assert data == []


# --- GET /skills/{id} ---
def test_get_skill_by_id_returns_skill():
    create_response = client.post("/skills", json={"name": "Python", "level": 4, "years": 3})

    assert create_response.status_code == 201

    skill_id = create_response.json()["id"]
    get_response = client.get(f"/skills/{skill_id}")
    assert get_response.status_code == 200
    name = get_response.json()["name"]
    assert name == "Python"


def test_get_skill_by_id_returns_404_when_not_found():
    skill_id = uuid.uuid4()
    get_response = client.get(f"/skills/{skill_id}")
    assert get_response.status_code == 404
    assert get_response.json()["detail"] == "Skill not found"


def test_get_skill_by_id_returns_422_when_id_is_invalid():
    get_response = client.get("/skills/abc")
    assert get_response.status_code == 422


# --- PUT /skills/{id} ---
def test_update_skill_returns_updated_skill():
    create_response = client.post("/skills", json={"name": "Docker", "level": 3})

    assert create_response.status_code == 201

    skill_id = create_response.json()["id"]

    update_response = client.put(
        f"/skills/{skill_id}", json={"name": "Docker", "level": 5, "years": 2}
    )

    assert update_response.status_code == 200

    assert update_response.json()["id"] == skill_id
    assert update_response.json()["level"] == 5
    assert update_response.json()["years"] == 2

    get_response = client.get(f"/skills/{skill_id}")

    assert get_response.json()["level"] == 5
    assert get_response.json()["years"] == 2


def test_update_skill_returns_404_when_not_found():
    skill_id = uuid.uuid4()

    update_response = client.put(f"/skills/{skill_id}", json={"name": "Docker", "level": 5})
    assert update_response.status_code == 404
    assert update_response.json()["detail"] == "Skill not found"


def test_update_skill_returns_422_when_body_is_invalid():
    create_response = client.post("/skills", json={"name": "Docker", "level": 3})

    assert create_response.status_code == 201

    skill_id = create_response.json()["id"]

    update_response = client.put(f"/skills/{skill_id}", json={"name": "Docker", "level": 999})
    assert update_response.status_code == 422


# --- DELETE /skills/{id} ---
def test_delete_skill_returns_204():
    create_response = client.post("/skills", json={"name": "Python", "level": 3})

    assert create_response.status_code == 201

    skill_id = create_response.json()["id"]

    delete_response = client.delete(f"/skills/{skill_id}")

    assert delete_response.status_code == 204
    assert delete_response.content == b""


def test_delete_skill_returns_404_when_not_found():
    skill_id = uuid.uuid4()

    delete_response = client.delete(f"/skills/{skill_id}")
    assert delete_response.status_code == 404
    assert delete_response.json()["detail"] == "Skill not found"


def test_deleted_skill_is_no_longer_found():
    create_response = client.post("/skills", json={"name": "Docker", "level": 3})

    assert create_response.status_code == 201

    skill_id = create_response.json()["id"]

    delete_response = client.delete(f"/skills/{skill_id}")

    assert delete_response.status_code == 204

    get_response = client.get(f"/skills/{skill_id}")

    assert get_response.status_code == 404
