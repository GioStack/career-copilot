from fastapi.testclient import TestClient
from sqlalchemy import inspect

from career_copilot.core.database import Base
from career_copilot.main import app


def test_lifespan_creates_tables(monkeypatch, db_engine):

    Base.metadata.drop_all(db_engine)
    monkeypatch.setattr("career_copilot.main.engine", db_engine)
    assert "skills" not in inspect(db_engine).get_table_names()

    with TestClient(app):
        pass

    assert "skills" in inspect(db_engine).get_table_names()
