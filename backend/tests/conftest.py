import pytest
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from career_copilot.core.config import settings
from career_copilot.core.database import Base, get_db
from career_copilot.main import app


class DatabaseTestSettings(BaseSettings):
    """Reads TEST_DATABASE_URL from env vars, then .env, like the app settings."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    test_database_url: str


test_settings = DatabaseTestSettings()

# The tests drop every table after each test, so they must never use the app database.
if test_settings.test_database_url == settings.database_url:
    raise RuntimeError("TEST_DATABASE_URL must point to a different database than DATABASE_URL")

test_engine = create_engine(test_settings.test_database_url)
TestSessionLocal = sessionmaker(bind=test_engine)


def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def test_db():
    Base.metadata.create_all(test_engine)
    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()
    Base.metadata.drop_all(test_engine)


@pytest.fixture
def db_engine():
    """The test database engine, for tests that need it directly."""
    return test_engine
