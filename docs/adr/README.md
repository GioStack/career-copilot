# Architecture Decision Records

Each ADR records one technical decision, why it was made, and its trade-offs.
ADRs are not edited after they are accepted; a new ADR refines or replaces an older one.

| ADR | Decision | Status |
|---|---|---|
| [0000](0000-use-fastapi-as-backend-framework.md) | Use FastAPI as the backend framework | Accepted |
| [0001](0001-use-uv-for-dependency-management.md) | Use uv for dependency management | Accepted |
| [0002](0002-organize-backend-by-feature.md) | Organize the backend by feature | Accepted, refined by 0009 |
| [0003](0003-use-sqlalchemy-with-pydantic-schemas.md) | Use SQLAlchemy models with separate Pydantic schemas | Accepted |
| [0004](0004-use-sqlite-as-local-first-database.md) | Use SQLite as a local-first database | Accepted |
| [0005](0005-use-uuids-as-primary-keys.md) | Use UUIDs as primary keys | Accepted |
| [0006](0006-load-configuration-from-env.md) | Load configuration from environment variables and .env | Accepted |
| [0007](0007-create-tables-on-startup.md) | Create database tables on startup with create_all (no migrations yet) | Accepted |
| [0008](0008-issue-branch-pr-workflow.md) | Use an issue, branch and pull request workflow | Accepted, refined by 0012 |
| [0009](0009-split-vault-into-sub-packages.md) | Split the vault into one sub-package per entity | Accepted |
| [0010](0010-use-a-single-profile-resource.md) | Use a single profile resource with GET and PUT | Accepted |
| [0011](0011-test-validation-through-the-api.md) | Test validation through the API | Accepted |
| [0012](0012-run-checks-in-ci-with-github-actions.md) | Run checks in CI with GitHub Actions | Accepted |