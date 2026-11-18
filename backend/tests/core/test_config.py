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
