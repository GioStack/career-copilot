from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings from env vars, then .env, then defaults (see ADR 0006)."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Required: there is no default database (see ADR 0014).
    database_url: str


# Created once at import; other modules import this instance.
settings = Settings()
