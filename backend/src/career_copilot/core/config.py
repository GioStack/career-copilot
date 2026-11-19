from typing import Literal

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

# Providers supported by Pydantic AI that the app accepts (ADR 0019).
LLMProvider = Literal["anthropic", "google", "groq", "mistral", "ollama", "openai", "openrouter"]


class Settings(BaseSettings):
    """Settings from env vars, then .env, then defaults (see ADR 0006)."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Required: there is no default database (see ADR 0014).
    database_url: SecretStr

    # Optional: the vault works without an LLM; only the AI features need it.
    llm_provider: LLMProvider | None = None
    llm_model: str | None = None
    # SecretStr hides the key when the settings are printed or logged.
    llm_api_key: SecretStr | None = None
    # Only for providers on your own server, such as a local Ollama.
    llm_base_url: str | None = None


# Created once at import; other modules import this instance.
settings = Settings()
