# Career Copilot

An open-source, local-first web app that helps you manage your career data and turn it into tailored CVs and LinkedIn content.

## Why

Job seekers keep rewriting the same experience for every application and every post.
Career Copilot stores your career data once, in a single structured "vault",
and reuses it to tailor applications and build your personal brand, without sending your data to a third-party platform.

## Modules

- **Career Vault**: a structured store of your skills, experience, projects and achievements.
- **Job Tailoring Engine** *(planned)*: matches your vault against a job description and drafts a tailored CV.
- **LinkedIn Brand Studio** *(planned)*: generates LinkedIn posts and profile content from your vault.
- **Settings** *(planned)*: choose your LLM provider and manage your own API keys.

## Principles

- **Local-first**: your data lives in a local SQLite database on your machine.
- **BYOK (Bring Your Own Key)**: you use your own LLM API key; no keys or data go through our servers.

## Tech stack

- **Backend**: Python 3.12, FastAPI, Pydantic v2, SQLAlchemy 2, SQLite
- **Tooling**: uv, pytest, ruff
- **Frontend** *(planned)*: React + TypeScript

## Status

Early development. Currently working:

- Career Vault **Skills API** (`POST /skills`, `GET /skills`)
- Input validation with Pydantic
- Persistence in SQLite
- Automated tests with an isolated in-memory test database

