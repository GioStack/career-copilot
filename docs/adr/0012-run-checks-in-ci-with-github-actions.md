# 0012. Run checks in CI with GitHub Actions

## Status
Accepted (2026-10-23). Refines ADR 0008.

## Context
Formatting, linting and tests ran only on my machine, as part of the ADR 0008 workflow.
Nothing checked a pull request automatically, so a PR could be merged with a skipped check,
or with code that only works on one machine (e.g. Windows but not Linux).
The repository is now public, and every PR showed "Checks 0".

## Decision
A GitHub Actions workflow (`.github/workflows/ci.yml`) runs on every pull request to `main`
and on every push to `main`. On a clean Ubuntu machine, from `backend/`, it runs
`uv sync --locked`, `ruff format --check`, `ruff check` and `pytest`.
A pull request is merged only when the CI check is green.
Tooling changes like this one use the `chore/` branch prefix and the `chore:` commit type,
which ADR 0008 did not list.

## Alternatives considered
- **Local checks only**: no setup, but they depend on remembering to run them,
  and they only prove the code works on one machine.
- **Pre-commit hooks**: catch problems before each commit, but they run only on the developer's
  machine, can be skipped, and do not show results on the pull request.
- **Another CI service** (e.g. CircleCI): needs a separate account and setup;
  GitHub Actions is built into the repository and free for public repositories.

## Consequences
- Every pull request shows whether formatting, linting and tests pass on a clean machine.
- `uv sync --locked` fails if `uv.lock` is out of date with `pyproject.toml`.
- CI checks formatting but does not fix it; `ruff format` still runs locally before each commit.
- "Green before merge" is followed by hand: branch protection is not enabled,
  so GitHub does not block a merge.
- Docs-only commits pushed directly to `main` (ADR 0008) also run the workflow.