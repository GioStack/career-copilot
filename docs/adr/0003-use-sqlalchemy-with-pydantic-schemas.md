# 0003. Use SQLAlchemy models with separate Pydantic schemas

## Status
Accepted (2026-10-10)

## Context
The backend needs to store data in a database and expose it through an API.
The database shape and the API shape are related but not always the same
(e.g. the client does not send an `id`, but every response includes one).

## Decision
Use two kinds of classes per entity:
- **SQLAlchemy ORM models** (e.g. `SkillORM` in `models.py`) describe database tables.
- **Pydantic schemas** (in `schemas.py`) describe and validate API input and output:
  - `Skill`: input sent by the client (no `id`).
  - `SkillRead`: output returned by the API (inherits `Skill`, adds `id`).

Conversion happens explicitly: `SkillORM(**skill.model_dump())` for input and
`SkillRead.model_validate(skill_orm)` (with `from_attributes=True`) for output.

## Alternatives considered
- **SQLModel**: one class that is both a table and a Pydantic model. Less code,
  but it mixes two responsibilities, and once the database and API shapes diverge,
  several classes are needed anyway. It also hides how SQLAlchemy and Pydantic work.

## Consequences
- The database and the API can change independently.
- Each class has one clear responsibility.
- More code: fields are declared twice and must be kept in sync.
- Explicit conversion is needed between ORM models and schemas.