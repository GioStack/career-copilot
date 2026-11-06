# 0016. Store achievements in their own table

## Status

Accepted (2026-11-06).

## Context

A CV lists achievements under each work experience. The user must be able to pick them one by one for each application. The planned AI features will embed each achievement and cite it, so each one needs its own id.

## Decision

Store achievements in an `achievements` table:

- `id`: UUID.
- `experience_id`: required foreign key with `ON DELETE CASCADE`, enforced by PostgreSQL.
- `text`: required, at least 1 character.
- `position`: set by the API to the next number, unique per experience.

Create and list them under their experience (`POST` and `GET /experiences/{id}/achievements`), ordered by `position`. Get, update and delete one by its own id (`/achievements/{id}`).

## Alternatives considered

- A JSON list on the experience: achievements would have no id, so they could not be selected or cited one by one.
- Lines inside `description`: same problem, and the text would need parsing.
- Order by creation time: rows created in the same transaction get the same `now()`, so the order is not reliable.
- Fully nested URLs (`/experiences/{id}/achievements/{id}`): the achievement id is already unique, so the extra id adds nothing.

## Consequences

- Each achievement can be selected, edited, embedded and cited.
- One more table, created with a migration.
- Achievements are not part of the experience response.
- Reordering needs its own endpoint later.
