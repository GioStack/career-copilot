# Recipes run in PowerShell on Windows and in sh elsewhere (ADR 0017).
set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]

# List the recipes.
default:
    @just --list

# Start the database and apply the migrations.
[working-directory('backend')]
up: db
    uv run alembic upgrade head

# Format, lint and test the backend.
[working-directory('backend')]
check:
    uv run ruff format .
    uv run ruff check --fix .
    uv run pytest

# Run the API with auto-reload.
[working-directory('backend')]
dev:
    uv run uvicorn career_copilot.main:app --reload

# Start the database and wait until it is healthy.
[private]
db:
    docker compose up -d --wait
