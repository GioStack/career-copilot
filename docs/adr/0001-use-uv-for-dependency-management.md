# 0001. Use uv for dependency management

## Status
Accepted (2026-10-08)

## Context
The backend needs a reproducible Python environment: the same Python version
and the same package versions on every machine that runs the project.

## Decision
Use uv to manage the Python version, the virtual environment and dependencies.
Dependencies are declared in `pyproject.toml` and locked in `uv.lock`.
Commands are run with `uv run`.

## Alternatives considered
- **pip + venv**: two separate tools, slower, and no built-in lockfile;
  `requirements.txt` usually pins only direct dependencies, not their sub-dependencies.
- **Poetry**: has a lockfile, but is slower and uses its own configuration.

## Consequences
- Every machine installs exactly the same versions (`uv.lock`).
- One tool for Python version, environment and packages; installs are fast.
- Contributors must install uv first.
- Low lock-in risk: `pyproject.toml` is a Python standard.