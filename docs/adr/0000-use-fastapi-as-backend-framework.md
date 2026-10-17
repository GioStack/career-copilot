# 0000. Use FastAPI as the backend framework

## Status
Accepted (2026-10-17). Records a decision made at the start of the project.

## Context
Career Copilot needs an HTTP API. The backend validates
vault data, stores it in SQLite (ADR 0004) and will later call an LLM to tailor CVs.
FastAPI was chosen at the start of the project, but the choice was never recorded.
FastAPI is the Python web framework the author knows best, so time goes into the product
instead of into learning a new framework.

## Decision
The backend uses FastAPI.
Request and response bodies are Pydantic models (ADR 0003); FastAPI validates them
and returns `422` on invalid input.
Dependencies such as the database session are injected with `Depends` (`get_db`).
Each vault entity has its own `APIRouter`, registered in `main.py` (ADR 0009).

## Alternatives considered
- **Django + Django REST Framework**: includes admin, auth and migrations, but brings its own ORM
  instead of SQLAlchemy and is heavier than a local-first, single-user API needs.
- **Flask**: small and well known, but has no built-in validation or API docs;
  it needs extra libraries for what FastAPI gets from Pydantic.

## Consequences
- Validation, `422` errors and the Swagger docs (`/docs`) come from type hints, with little extra code.
- The OpenAPI schema (`/openapi.json`) can generate TypeScript types for the React frontend.
- The same Pydantic models can validate structured LLM output in the tailoring phase.
- `TestClient` and `dependency_overrides` keep endpoint tests simple (see `tests/vault/conftest.py`).
- FastAPI has no built-in project structure; the project defines its own (ADR 0002, ADR 0009).
- No built-in admin, auth or migrations; each is added separately when needed (e.g. Alembic).
- Endpoints and SQLAlchemy sessions are synchronous today, and FastAPI runs them in a thread pool.
  Async is available for the LLM calls, but mixing it with the sync database code needs care.