# 0010. Use a single profile resource with GET and PUT

## Status
Accepted (2026-10-16).

## Context
The vault stores the user's profile: name, headline, contact details and links,
shown at the top of every generated CV.
Career Copilot is local-first with a single user (ADR 0004), so there is exactly one profile.
Skills use an id in the URL (`/skills/{id}`), because the user has many skills.
For the profile, an id in the URL would make the client store an id for data that exists once,
and POST would allow creating a second profile.

## Decision
The profile is a single resource at `/profile`, with no id in the URL.
`GET /profile` returns the profile, or `404` with "Profile not found" if it does not exist yet.
`PUT /profile` creates the profile the first time and replaces it afterwards, always with `200`.
There is no POST and no DELETE; the user edits the profile with PUT.
The table keeps a UUID primary key (ADR 0005), so responses still include an `id`.

## Alternatives considered
- **Full CRUD like skills** (`POST /profile`, `GET/PUT/DELETE /profile/{id}`):
  consistent with skills, but allows several profiles and needs an id the client has no use for.
- **POST to create, PUT to update**: two endpoints for one action;
  the client must check whether the profile exists before saving.

## Consequences
- The client saves the profile with one call and never needs the id.
- Only the API keeps the profile single; nothing in the database prevents a second row.
- `PUT` returns `200` also when it creates the profile, not `201`.
- If Career Copilot becomes multi-user, the profile will need a user id and this decision
  will be revisited.