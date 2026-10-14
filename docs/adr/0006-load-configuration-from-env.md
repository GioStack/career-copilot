# 0006. Load configuration from environment variables and .env

## Status
Accepted (2026-10-10)

## Context
Some values change between machines or must stay secret
(e.g. the database location now, LLM API keys later).
They should not be hard-coded or committed to Git.

## Decision
Use pydantic-settings (`Settings` in `core/config.py`) to load configuration.
Priority: environment variable → `.env` file → default value in code.
`.env` is listed in `.gitignore`. `.env.example` is committed and shows
which settings exist, with safe placeholder values.

## Alternatives considered
- **Hard-coded values**: changing them requires editing code, and secrets would end up in Git.
- **Reading `os.environ` manually**: no type validation and no defaults in one place.

## Consequences
- Settings change per machine without changing code.
- Secrets never reach the repository.
- Values are validated by Pydantic (e.g. `database_url: str`).
- Users must copy `.env.example` to `.env` before running the app.
- `.env` and relative paths like `./career_copilot.db` are resolved from the current
  working directory, so the server must be started from `backend/`. To be fixed later.