import pytest
from pydantic import SecretStr

from career_copilot.core.config import settings
from career_copilot.llm.model import LLMNotConfiguredError, get_model


# --- get_model ---
def test_get_model_raises_when_llm_is_not_configured(monkeypatch):
    monkeypatch.setattr(settings, "llm_provider", None)

    with pytest.raises(LLMNotConfiguredError):
        get_model()


def test_get_model_raises_when_llm_model_is_not_set(monkeypatch):
    monkeypatch.setattr(settings, "llm_provider", "google")
    monkeypatch.setattr(settings, "llm_model", None)
    monkeypatch.setattr(settings, "llm_api_key", SecretStr("test-key"))

    with pytest.raises(LLMNotConfiguredError):
        get_model()


def test_get_model_raises_when_the_provider_needs_a_missing_setting(monkeypatch):
    monkeypatch.setattr(settings, "llm_provider", "google")
    monkeypatch.setattr(settings, "llm_model", "gemini-test")
    monkeypatch.setattr(settings, "llm_api_key", None)
    # The provider falls back to its own variables, so they must not be set either.
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    with pytest.raises(LLMNotConfiguredError):
        get_model()


def test_get_model_builds_the_model_from_settings(monkeypatch):
    monkeypatch.setattr(settings, "llm_provider", "google")
    monkeypatch.setattr(settings, "llm_model", "gemini-test")
    monkeypatch.setattr(settings, "llm_api_key", SecretStr("test-key"))

    model = get_model()

    assert model.system == "google"
    assert model.model_name == "gemini-test"
