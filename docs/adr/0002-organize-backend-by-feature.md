# 0002. Organize the backend by feature

## Status
Accepted (2026-10-08). Refined by ADR 0009.

## Context
The backend will grow into several independent modules (Career Vault, Job Tailoring,
LinkedIn Brand Studio, Settings). We need a structure that keeps each module
easy to find, change and test.

## Decision
Organize code by feature (vertical slices). Each feature has its own package with
its own `models.py`, `schemas.py` and `router.py`. Shared infrastructure
(settings, database setup) lives in `core/`. Tests mirror the same structure
(e.g. `tests/vault/`).

Current layout:
- `core/`: configuration and database setup
- `vault/`: the user's career data (skills for now)

## Alternatives considered
- **Organize by layer** (`models/`, `schemas/`, `routers/`): a single feature change
  touches many folders, and each folder mixes unrelated features as the app grows.

## Consequences
- Adding, changing or removing a feature mostly affects one folder.
- Each feature is easier to understand and test in isolation.
- Dependencies between features must stay one-directional
  (e.g. tailoring may read from vault, not the other way around).
- Shared logic must be moved to `core/` deliberately, to avoid duplication.