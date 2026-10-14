from fastapi.testclient import TestClient
from sqlalchemy import create_engine, inspect
from sqlalchemy.pool import StaticPool

from career_copilot.main import app


def test_lifespan_creates_tables(monkeypatch):
    test_engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    monkeypatch.setattr("career_copilot.main.engine", test_engine)
    assert "skills" not in inspect(test_engine).get_table_names()

    with TestClient(app):
        pass

    assert "skills" in inspect(test_engine).get_table_names()
