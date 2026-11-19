# 0020. Build the frontend with React and Vite

## Status

Accepted (2026-11-19).

## Context

The vault and the AI features need a user interface: viewing and editing the vault, checking a CV extracted by the LLM before it is saved, and working on a tailored CV. The backend is a FastAPI API that publishes an OpenAPI schema (`/openapi.json`). The frontend should use the same types as the API, show the API's validation errors (`422`) next to the right field, and keep its data in sync after every change.

## Decision

Build a single-page app in `frontend/` with React, TypeScript and Vite.

- **API client:** generated from the backend's OpenAPI schema with Hey API (`@hey-api/openapi-ts`), so the types and request functions always match the API. The backend gives each route a clear operation id, so the generated functions have short names (for example `createEducation`).
- **Server data:** TanStack Query handles fetching, caching, loading and error states, and refreshes the data after a create, update or delete.
- **Pages:** TanStack Router, with type-checked links and route parameters.
- **Components and styling:** Tailwind CSS with shadcn/ui components, which are copied into the project.
- **Quality:** Biome for linting and formatting, Vitest for tests, and the TypeScript compiler for type checks.
- **Packages:** npm.
- **Commands and CI:** `just` recipes run the frontend like the backend (ADR 0017), and CI runs lint, type checks, tests and the build on every pull request (ADR 0012).

## Alternatives considered

- **Next.js**: adds its own server, which the app does not need because FastAPI is the backend.
- **Writing the API types and requests by hand**: no generator, but every change to the API would have to be copied to the frontend, and mistakes would show up only at runtime.
- **openapi-typescript**: generates only types; every request would be written by hand.
- **Orval**: generates query hooks too, but creates many files and does not throw on error responses by default.
- **React Router**: more widely known, but links and route parameters are not checked by the compiler.
- **ESLint and Prettier**: the most common choice, but two tools with separate configuration instead of one.

## Consequences

- The project needs Node.js next to Python.
- After an API change, the client is generated again; a type error then shows every place in the frontend that must change.
- The backend must allow requests from the frontend's address (CORS).
- CI takes longer, with a second job for the frontend.
