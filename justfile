# Recipes run in PowerShell on Windows and in sh elsewhere (ADR 0017).
set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]

# List the recipes.
default:
    @just --list

# Start the database and apply the migrations.
[working-directory('backend')]
up: db
    uv run alembic upgrade head

# Fix, format and check the backend code.
[working-directory('backend')]
lint:
    uv run ruff check --fix --exit-zero .
    uv run ruff format .
    uv run ruff check .

# Run the backend tests; pass a path to run only some of them.
[working-directory('backend')]
test *args:
    uv run pytest {{args}}

# Lint and test the backend.
check: lint test

# Run the API with auto-reload.
[working-directory('backend')]
dev:
    uv run uvicorn career_copilot.main:app --reload

# Install the frontend packages exactly as locked.
[working-directory('frontend')]
web-install:
    npm ci

# Run the frontend with hot reload.
[working-directory('frontend')]
web:
    npm run dev

# Fix, format, check and build the frontend.
[working-directory('frontend')]
web-check:
    npm run format
    npm run lint
    npm run build

# Start the database and wait until it is healthy.
[private]
db:
    docker compose up -d --wait
