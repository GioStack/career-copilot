import pytest

from career_copilot.vault.router import skills_db


@pytest.fixture(autouse=True)
def clear_skills_db():
    skills_db.clear()
