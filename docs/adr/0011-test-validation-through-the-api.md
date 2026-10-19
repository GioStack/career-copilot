# 0011. Test validation through the API

## Status
Accepted (2026-10-19).

## Context
Vault entities validate input with Pydantic schemas (ADR 0003).
Skills validation was tested in two places: `test_schemas.py` tested the `Skill` schema directly,
and `test_router.py` tested the API.
Profile validation was tested only through the API.
The two entities followed different test strategies; some rules were tested twice,
and two rules were tested only in the schema tests.

## Decision
Validation rules are tested through the API: each rule has a router test that sends
an invalid body and expects `422`.
Vault entities have no separate schema test files (`test_schemas.py`).
The skills schema tests were moved to the router tests (Issue #18).

## Alternatives considered
- **Schema tests and router tests for every entity**: schema tests are faster and point straight
  at the schema, but every rule is tested twice.
- **Schema tests only**: fast, but they do not check that the client actually receives `422`.

## Consequences
- One test strategy for every vault entity; each rule is tested once.
- Tests check what the client receives, not only what the schema does.
- A failing validation test may come from the schema, the router or the test database,
  so finding the cause can take a little longer. The status code that came back
  (e.g. `404` instead of `422`) usually shows which part to check.
- Router tests are slower than schema tests, because each request goes through FastAPI
  and the test database; this is acceptable at the current size.
- If a schema gets logic that the API cannot reach, that logic can get its own unit test.