# 0009. Split the vault into one sub-package per entity

## Status
Accepted (2026-10-16). Refines ADR 0002.

## Context
ADR 0002 organizes the backend by feature. The vault started as one package with shared
`models.py`, `schemas.py` and `router.py`, because it only held skills.
The vault will hold six entities (skills, profile, experience, education, projects, languages).
In shared files, each file would grow past 300 lines and mix unrelated entities.
This should have been decided when the full list of vault entities was defined;
doing it now, with only one entity to move, keeps the refactor small.

## Decision
Each vault entity gets its own sub-package with its own `models.py`, `schemas.py`
and `router.py` (e.g. `vault/skills/`, `vault/profile/`).
Tests mirror the same structure (`tests/vault/skills/`); `tests/vault/conftest.py` stays shared.
In `main.py`, each router is named after its URL (`skills_router`, `profile_router`).

## Alternatives considered
- **Shared files for all entities**: no refactor, but large files that mix unrelated entities.
- **Organize by file type inside the vault** (`vault/routers/`, `vault/models/`):
  already rejected in ADR 0002.

## Consequences
- Each entity lives in one folder; adding an entity means adding one folder.
- Test files with the same name (e.g. `test_router.py`) are kept apart by `__init__.py` packages.
- More folders and `__init__.py` files.
- Imports between entities must stay one-directional, as in ADR 0002.