# 0017. Use just as the command runner

## Status

Accepted (2026-11-11).

## Context

The daily commands are long and depend on the current folder: `pytest` and `alembic` must run from `backend/`, where `.env` and `alembic.ini` are. Starting the database and applying the migrations takes several commands. The project is developed on both Windows (PowerShell) and Linux, and a frontend will be added later.

## Decision

Keep the daily commands as recipes in a `justfile` at the repo root:

- `just up`: start the database, wait until it is healthy, apply the migrations.
- `just check`: format, lint and test the backend.
- `just dev`: run the API with auto-reload.

`just` is installed with `uv tool install rust-just`, the same way on Windows and Linux. Recipes run in PowerShell on Windows and in `sh` on Linux, and set their working folder, so they work from any folder in the repo.

## Alternatives considered

- **Make**: widely known, but not installed on Windows by default, and its syntax (tabs, `.PHONY`) is easy to get wrong.
- **Shell and PowerShell scripts**: every command would be written twice, once per platform.
- **A Python task runner in `pyproject.toml`** (for example poethepoet): no extra install, but it lives in `backend/` and is tied to Python, while the frontend will need its own commands.
- **Only documenting the commands**: no new tool, but the commands stay long and easy to run from the wrong folder.

## Consequences

- One command per daily task, the same on Windows and Linux.
- Each machine needs `just` installed once.
- The `justfile` also documents the commands: `just --list` shows them, and anyone without `just` can still read and run them by hand.
- CI keeps its own steps for now and does not use `just`.
