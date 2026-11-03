# Career Copilot

![Career Copilot](assets/cover.jpg)

Store your career data once. Tailor your CV, summary and cover letter to every job posting.

**Open source · Local-first · Bring your own LLM key · In progress**

## The problem

Job seekers rewrite the same experience for every application. The facts stay the same; only the angle changes for each role.

## How it works

```mermaid
flowchart LR
    A["Your career data<br/>profile, skills, experience"] --> B[("Career Vault<br/>PostgreSQL")]
    J["Job posting"] --> C["LLM<br/>your own API key"]
    B --> C
    C --> D["Tailored CV"]
    C --> E["Summary"]
    C --> F["Cover letter"]

    classDef done fill:#0F172A,stroke:#14B8A6,color:#fff
    classDef next fill:#fff,stroke:#94A3B8,color:#334155,stroke-dasharray: 5 5
    class A,B done
    class J,C,D,E,F next
```

Solid boxes work today. Dashed boxes are next.

## Status

| Works today | Coming next |
|---|---|
| Career Vault API: profile, skills, experience | Database migrations (Alembic) |
| Input validation (Pydantic) | Achievements, projects, education |
| 50+ tests on a separate test database | **Tailoring engine**: CV, summary, cover letter |
| CI on every pull request (GitHub Actions) | React frontend |
| | Interview preparation |

## Key decisions

| Decision | Why | Trade-off |
|---|---|---|
| **FastAPI** | Validation and API docs come from type hints | No built-in auth or migrations |
| **PostgreSQL in Docker** | Vector search (`pgvector`) for the AI features, real foreign keys | Docker must be running |
| **UUID ids** | Data can move between machines without id clashes | Harder to read while debugging |
| **Tests through the API** | Tests check what the client actually receives | Slower than testing schemas directly |

Every decision is explained in [`docs/adr/`](docs/adr/).

## How it evolved

```mermaid
flowchart LR
    A["SQLite<br/>skills API"] --> B["Profile &<br/>experience"] --> C["CI with<br/>GitHub Actions"] --> D["PostgreSQL<br/>in Docker"]
```

I started with SQLite for zero setup, then moved to PostgreSQL once the AI plans needed vector search ([ADR 0014](docs/adr/0014-use-postgresql-in-docker.md)).

## Limitations

- API only for now: try it at `/docs`.
- No AI features yet.
- Single user, no login, by design for a local app.

## Run it locally

Requires Docker and [uv](https://docs.astral.sh/uv/).

```bash
cp backend/.env.example backend/.env    # then set your own password
docker compose up -d
docker compose exec db psql -U career_copilot -d career_copilot -c "CREATE DATABASE career_copilot_test;"
cd backend
uv run uvicorn career_copilot.main:app --reload    # API docs at http://127.0.0.1:8000/docs
uv run pytest
```

How tests are written: [`docs/testing.md`](docs/testing.md)

## Tech stack

Python 3.12 · FastAPI · Pydantic v2 · SQLAlchemy 2 · PostgreSQL · Docker Compose · uv · pytest · ruff · GitHub Actions
