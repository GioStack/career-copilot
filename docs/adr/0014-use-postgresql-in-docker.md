# 0014. Use PostgreSQL in Docker

## Status
Accepted (2026-11-01). Supersedes ADR 0004.

## Context
ADR 0004 chose SQLite for zero setup. The plans have changed since:
- The planned AI features (retrieval over the vault) need vector search.
  PostgreSQL has `pgvector`, a widely used extension; the SQLite options are less mature.
- Achievements will reference experiences with a foreign key and be deleted with them.
  SQLite does not enforce foreign keys unless every connection turns them on.
- PostgreSQL is the database used in most backend projects and job postings.
The app stays local-first and single-user: the data must stay on the user's machine.

## Decision
The backend uses PostgreSQL, run locally with Docker Compose (`docker-compose.yml`
at the repository root). SQLAlchemy connects with the `psycopg` driver,
and the connection is set with `DATABASE_URL` (ADR 0006).
Credentials live in `.env`, which is not committed; `.env.example` lists the variables
with placeholder values.
Tests run against a separate PostgreSQL test database, locally and in CI.
SQLite is no longer supported.

## Alternatives considered
- **Keep SQLite**: zero setup and fast tests, but no mature vector search,
  and foreign keys are off by default.
- **SQLite for tests, PostgreSQL for the app**: fast tests, but they would not test the database
  the app runs on; foreign keys, types and SQL behave differently.
- **PostgreSQL installed directly on the machine**: no Docker, but installation and version
  differ per machine (Windows, Linux); Docker gives the same version everywhere, also in CI.

## Consequences
- Running the app or the tests needs Docker running.
- Development, tests and CI use the same database.
- `pgvector` can be added later by changing the Docker image, with its own ADR.
- Data stays on the user's machine, in a Docker volume. Backup needs a database dump
  instead of copying one file.
- Existing SQLite data is not migrated; it was test data only.
- Tests are slower than with in-memory SQLite.
- Tables are still created with `create_all` (ADR 0007) until migrations are added.
