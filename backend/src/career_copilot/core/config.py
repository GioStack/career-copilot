from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings from env vars, then .env, then defaults (see ADR 0006)."""

    model_config = SettingsConfigDict(env_file=".env")

    database_url: str = "sqlite:///./career_copilot.db"


# Created once at import; other modules import this instance.
settings = Settings()
