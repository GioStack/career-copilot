# 0007. Create database tables on startup with create_all (no migrations yet)

## Status
Accepted (2026-10-13)

## Context
The app must create its tables automatically; previously they were created
by a manual command, so a fresh install failed with `no such table: skills` (#1).
The data model is still changing often, and there are no real users with data yet.

## Decision
Call `Base.metadata.create_all(engine)` in the FastAPI `lifespan` handler,
so missing tables are created every time the server starts.
Database migrations are postponed.

## Alternatives considered
- **Manual setup command**: easy to forget; a fresh install breaks.
- **Migrations with Alembic now**: keeps data safe when the schema changes,
  but adds tooling and complexity while the model is still unstable.

## Consequences
- A fresh install works with no manual steps.
- Existing tables and data are never deleted.
- `create_all` does not change existing tables: when a model changes
  (e.g. a new column), the local database file must be deleted and recreated.
- Before real users store data, migrations (Alembic) must be introduced in a new ADR.