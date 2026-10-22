# 0004. Use SQLite as a local-first database

## Status
Accepted (2026-10-10).

## Context
Career Copilot is a local-first app: it runs on the user's own machine, for a single user,
and stores personal career data. It is not a hosted multi-user (SaaS) product for now.
Setup should be as simple as possible.

## Decision
Use SQLite, stored as a single file (`career_copilot.db`), accessed through SQLAlchemy.
The location is configured with `DATABASE_URL`.

## Alternatives considered
- **PostgreSQL / MySQL**: require a separate database server to install, run and configure.
  Their strengths (many concurrent users, network access) are not needed for a single local user.

## Consequences
- Zero setup: SQLite is built into Python, and the file is created automatically.
- Privacy: personal data never leaves the user's machine.
- Easy backup: copy one file.
- Only one write at a time; acceptable for a single user.
- Moving to a SaaS model would require migrating to a server database such as PostgreSQL.
  SQLAlchemy reduces the effort, but some adjustments would still be needed.