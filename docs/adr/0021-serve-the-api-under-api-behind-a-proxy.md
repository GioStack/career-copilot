# 0021. Serve the API under /api behind a proxy

## Status

Accepted (2026-11-20). Refines ADR 0020.

## Context

The frontend runs on `http://localhost:5173` (Vite) and the API on `http://127.0.0.1:8000` (FastAPI). A different port is a different origin, so the browser blocks the frontend's requests to the API unless the API allows them. ADR 0020 expected the API to allow them with CORS. The frontend will also have its own page URLs (for example `/skills`), which must not clash with the API's URLs.

## Decision

The browser talks to one origin, and a proxy forwards API requests to the backend.

- **One prefix for the API:** every route is served under `/api`, set once in `main.py` with a shared `APIRouter(prefix="/api")`. The routers keep their own prefixes, so `/projects` becomes `/api/projects`. `/docs` stays at `/docs`.
- **Development:** the Vite dev server forwards every request under `/api` to `http://127.0.0.1:8000` (`server.proxy` in `vite.config.ts`), without changing the path.
- **Production:** a reverse proxy (for example Nginx) serves the built frontend (`dist/`) and forwards `/api` to the backend. HTTPS ends at the proxy.
- **No CORS:** the API does not allow other origins.

## Alternatives considered

- **CORS in FastAPI**: works, but the browser often sends an extra preflight request, every deployment needs the right list of origins, and `allow_origins=["*"]` would let any site call the API.
- **The proxy removes `/api`, and the routes stay without it**: no backend change, but the same route would have two URLs (`/api/projects` in the browser, `/projects` in the API, the docs and the tests).
- **A proxy rule for each route** (`/projects`, `/skills`, ...): every new router needs a new rule, and the API's URLs would clash with the frontend's page URLs.

## Consequences

- The browser sees one origin, in development and in production.
- Page URLs (`/skills`) and API URLs (`/api/skills`) never clash.
- The same URL is used everywhere: browser, `/docs`, tests and proxy.
- In development, the frontend needs the backend running (`just dev`); otherwise Vite logs `http proxy error`.
- A production deployment needs a reverse proxy in front of the backend.
