import pytest
from pydantic import ValidationError

from career_copilot.core.config import Settings


# --- Settings ---
def test_settings_reject_unknown_llm_provider():
    with pytest.raises(ValidationError):
        Settings(
            database_url="postgresql+psycopg://user:pass@localhost/db",
            llm_provider="gogle",
        )


def test_settings_hide_secrets_when_printed():
    settings = Settings(
        database_url="postgresql+psycopg://user:db-password@localhost/db",
        llm_api_key="llm-key",
    )

    assert "db-password" not in repr(settings)
    assert "llm-key" not in repr(settings)
