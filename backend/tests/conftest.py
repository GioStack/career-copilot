import pytest
from alembic import command
from alembic.config import Config
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from career_copilot.core.config import settings
from career_copilot.core.database import get_db
from career_copilot.main import app


class TestSettings(BaseSettings):
    """Reads TEST_DATABASE_URL from env vars, then .env, like the app settings."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    test_database_url: str


test_settings = TestSettings()

# The tests drop every table after each test, so they must never use the app database.
if test_settings.test_database_url == settings.database_url:
    raise RuntimeError("TEST_DATABASE_URL must point to a different database than DATABASE_URL")

test_engine = create_engine(test_settings.test_database_url)


@pytest.fixture(scope="session", autouse=True)
def migrated_database():
    """Build the test database with the migrations, once per test run (ADR 0015)."""
    config = Config("alembic.ini")
    # "%" is special in Alembic's config, so it is escaped as "%%".
    config.set_main_option("sqlalchemy.url", test_settings.test_database_url.replace("%", "%%"))
    # Start from an empty schema, so the run always uses the current migrations.
    command.downgrade(config, "base")
    command.upgrade(config, "head")


@pytest.fixture(autouse=True)
def db_session(migrated_database):
    """Run each test inside a transaction that is rolled back at the end."""
    connection = test_engine.connect()
    transaction = connection.begin()
    # The app's commit() calls become savepoints inside this transaction.
    session = Session(bind=connection, join_transaction_mode="create_savepoint")

    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db
    yield session
    app.dependency_overrides.clear()
    session.close()
    transaction.rollback()
    connection.close()
