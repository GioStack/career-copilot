# Career Copilot

An open-source, local-first web app that stores your career data once and uses your own LLM API key to turn it into tailored CVs, LinkedIn content and mock interviews.

## Why

Job seekers rewrite the same experience for every CV, LinkedIn update and job application.
Career Copilot stores your career data once, in a single structured "vault",
and reuses it to tailor applications and build your personal brand, while your data stays on your own machine.

## Modules

- **Career Vault**: a structured store of your profile, skills, experience, projects and achievements.
- **Job Tailoring Engine** *(planned)*: matches your vault against a job description and drafts a tailored CV.
- **LinkedIn Brand Studio** *(planned)*: generates LinkedIn profile content and posts from your vault.
- **Interview Coach** *(planned)*: runs mock interviews based on your vault and a target role.
- **Settings** *(planned)*: choose your LLM provider and manage your own API keys.

## Principles

- **Local-first**: your data lives in a local PostgreSQL database, running in Docker on your machine.
- **BYOK (Bring Your Own Key)**: you use your own LLM API key; no keys or data go through our servers.

## Tech stack

- **Backend**: Python 3.12, FastAPI, Pydantic v2, SQLAlchemy 2, PostgreSQL
- **Tooling**: uv, Docker Compose, pytest, ruff, GitHub Actions CI
- **Frontend** *(planned)*: React + TypeScript

## Status

Early development. Currently working:

- Career Vault API:
  - Profile: a single user profile (`GET /profile`, `PUT /profile`)
  - Skills: full CRUD (`POST /skills`, `GET /skills`, `GET /skills/{id}`, `PUT /skills/{id}`, `DELETE /skills/{id}`)
  - Experience: full CRUD (`POST /experiences`, `GET /experiences`, `GET /experiences/{id}`, `PUT /experiences/{id}`, `DELETE /experiences/{id}`)
- Input validation with Pydantic (e.g. emails, URLs, value ranges, required fields)
- Persistence in PostgreSQL
- Automated tests on a separate PostgreSQL test database
- CI on every pull request: formatting, linting and tests with GitHub Actions

Next: database migrations with Alembic, then achievements, projects, education and languages in the vault.

## Running locally

Requirements: Docker and uv.

1. Copy `backend/.env.example` to `backend/.env` and set your own password.
2. Start PostgreSQL from the repository root:

       docker compose up -d

3. Create the test database (once):

       docker compose exec db psql -U career_copilot -d career_copilot -c "CREATE DATABASE career_copilot_test;"

4. From `backend/`, start the API at http://127.0.0.1:8000/docs:

       uv run uvicorn career_copilot.main:app --reload

5. From `backend/`, run the tests:

       uv run pytest

## Architecture decisions

Key technical decisions and their trade-offs are recorded as ADRs in [`docs/adr/`](docs/adr/).

## Testing

How tests are written and checked is described in [`docs/testing.md`](docs/testing.md).
