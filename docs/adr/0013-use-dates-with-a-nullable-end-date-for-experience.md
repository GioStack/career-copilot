# 0013. Use dates with a nullable end date for work experience

## Status
Accepted (2026-10-30).

## Context
Each work experience in the vault has a start and an end.
A CV shows the period of each role, marks the current one, and lists roles from most recent.
Two choices had to be made: how to mark the current position, and how precise the dates are.

## Decision
`start_date` and `end_date` are `date` values (`YYYY-MM-DD`), in the schema and in the database.
`start_date` is required. `end_date` is optional; `null` means the current position.
The `Experience` schema rejects an `end_date` before the `start_date` with `422`;
equal dates are allowed.
`GET /experiences` returns experiences sorted by `start_date`, most recent first.

## Alternatives considered
- **An `is_current` boolean next to `end_date`**: common, but the two fields can contradict
  each other (`is_current: true` with an end date), which needs an extra validator and tests.
- **Separate year and month fields**: closer to how CVs show dates, but four fields
  instead of two, and comparing or sorting them needs custom code.
- **Dates as free text** (e.g. "March 2024"): flexible, but cannot be validated,
  compared or sorted.

## Consequences
- One field decides whether a position is current, so it cannot be inconsistent.
- Dates are compared and sorted directly, in Python and in SQL.
- The user must enter a day even when only the month is known (e.g. `2024-03-01`);
  a generated CV can still show only the month and year.
- Several experiences can have `end_date: null`; holding two positions at once is valid.
- Changing this later changes the API and the database columns, which needs a migration;
  the project has no migrations yet (ADR 0007).