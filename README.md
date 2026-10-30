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

- **Local-first**: your data lives in a local SQLite database on your machine.
- **BYOK (Bring Your Own Key)**: you use your own LLM API key; no keys or data go through our servers.

## Tech stack

- **Backend**: Python 3.12, FastAPI, Pydantic v2, SQLAlchemy 2, SQLite
- **Tooling**: uv, pytest, ruff, GitHub Actions CI
- **Frontend** *(planned)*: React + TypeScript

## Status

Early development. Currently working:

- Career Vault API:
  - Profile: a single user profile (`GET /profile`, `PUT /profile`)
  - Skills: full CRUD (`POST /skills`, `GET /skills`, `GET /skills/{id}`, `PUT /skills/{id}`, `DELETE /skills/{id}`)
  - Experience: full CRUD (`POST /experiences`, `GET /experiences`, `GET /experiences/{id}`, `PUT /experiences/{id}`, `DELETE /experiences/{id}`)
- Input validation with Pydantic (e.g. emails, URLs, value ranges, required fields)
- Persistence in SQLite
- Automated tests with an isolated in-memory test database
- CI on every pull request: formatting, linting and tests with GitHub Actions

Next: education, projects and languages in the vault.

## Architecture decisions

Key technical decisions and their trade-offs are recorded as ADRs in [`docs/adr/`](docs/adr/).
