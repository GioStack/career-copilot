# Testing

How tests are written in this project. Older tests may not follow every naming rule yet;
names are fixed when a test is changed for another reason.

## Running the tests
Before every commit, from any folder in the repo:

    just check

It runs `ruff check --fix`, `ruff format` and `pytest` in `backend/` (see the `justfile`).
CI runs the same checks without fixing anything (ADR 0012).

## What to test
Every test must catch a realistic mistake that no other test catches.
A test that only repeats what another test already covers is not added.

Validation is tested through the API, not on the schema directly (ADR 0011).
The test database is built with the migrations once per test run, and each test runs
inside a transaction that is rolled back at the end, so every test starts with empty tables
(`tests/conftest.py`, ADR 0015).
Test data is fake: `example.com` emails, "Example Co" companies.

## Tests for each endpoint
- **Success:** the expected status and the fields that matter.
- **Not found:** `404`, and the `detail` message, so it is our 404 and not the framework's.
- **Invalid id:** `422` for an id that is not a UUID (e.g. `/experiences/abc`).
- **Invalid body:** one `422` test per validation rule, on POST.
  PUT uses the same schema, so one invalid-body test is enough there.
- **Boundaries:** both the valid limits (e.g. `level` 1 and 5) and the invalid ones (0 and 6+).
- **PUT replaces:** an optional field that is not sent becomes `null`.
- **Changes are saved:** PUT and DELETE are checked with a separate GET in the same test.
  POST is checked by the GET tests.

## Structure of a test
1. **Setup:** create what the test needs, and assert the status (e.g. `201`),
   so a broken setup is not mistaken for a broken feature.
2. **Action:** the request under test. Assert the status first, then the body.
3. **Check:** the final GET asserts only the field that changed, without its status.

Leave a blank line between a request and its asserts.

## Expected values
- Compare with what was sent: `VALID_EXPERIENCE["title"]`, or the literal written in the test.
  Never compare one response with another.
- To check that a change was saved, assert a field that changed; a field that did not change
  passes either way.

## Names
- Tests start with the router function: `test_update_experience_...`,
  then the case and the result: `..._returns_404_when_not_found`,
  `..._sets_location_to_none_when_not_sent`.
- Responses are named by their role: `create_response`, `get_response`, `update_response`,
  `delete_response`. A setup request is `create_response` even when it is a PUT.
- Valid data lives in one constant per file, e.g. `VALID_EXPERIENCE`.
  Change a field with `{**VALID_EXPERIENCE, "title": ""}`;
  remove one with `.copy()` and `del`.

## Tests for code that already exists
A new test for existing code passes at once, so it has never been seen to fail.
Check it with a temporary bug:
1. Break the code the way the test should catch (e.g. `ge=0` → `gt=0`).
2. Run the tests: only the new test must fail.
3. Revert with `git restore <file>`. The temporary bug is never committed.

If other tests also fail, the mistake is already covered and the new test is not needed.
