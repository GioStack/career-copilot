# 0019. Connect to LLMs with Pydantic AI

## Status

Accepted (2026-11-17).

## Context

The AI features (tailored CV, cover letter, ATS check, LinkedIn, mock interviews) need an LLM. The README promises "bring your own LLM key", so users choose their provider: a hosted one such as Claude or Gemini, or a local one through Ollama. The app works with structured data (Pydantic schemas), so the LLM's answers should come back in the same form. Tests must not call a real LLM, which is slow, costs money and gives a different answer each time.

## Decision

Use Pydantic AI (v1, pinned below 2) to call the LLM.

- The provider comes from `LLM_PROVIDER` in `.env`, which must be one of a fixed list of providers that Pydantic AI supports (for example `anthropic`, `google`, `openai`, `ollama`). A provider outside the list stops the app at startup. The model comes from `LLM_MODEL`.
- The API key comes from `LLM_API_KEY`, one variable for every provider, and an optional `LLM_BASE_URL` sets the server address (for example for a local Ollama). Both are read by the settings (ADR 0006) and passed to the provider, so all the code reads configuration from the settings and there is no code for each provider. Keys are never committed.
- Every LLM call returns a Pydantic model. If the answer does not match the schema, Pydantic AI asks the model to correct it.
- Tests use Pydantic AI's test model instead of a real one, and real model requests are blocked in tests. The real model is checked by evals, separately from the tests.

## Alternatives considered

- **A provider's own SDK** (for example `anthropic`): supports structured output, but only for that provider, so users could not bring a different key.
- **LiteLLM**: one API for many providers, but it returns plain text or JSON with no validation against a schema.
- **Calling the providers' HTTP APIs directly**: no dependency, but every provider's request and response format would have to be written and kept up to date by hand.
- **Any provider as free text in `LLM_MODEL`** (`provider:model`): no list to maintain, but a typo in the provider name is found only at the first LLM call, not at startup.
- **Each provider's own key variable** (`GOOGLE_API_KEY`, `ANTHROPIC_API_KEY`), loaded from `.env` into the environment: Pydantic AI finds the key by itself, but the configuration would be read from two places (the settings and the environment), and a key typed into the app later could not be passed the same way.

## Consequences

- Switching provider is a change to `.env`, not to the code.
- Adding a provider that Pydantic AI supports is one word in the list.
- A key entered in the app later can be passed to the provider in the same way.
- The full `pydantic-ai` package installs the libraries of every provider, so the install is larger.
- The AI code depends on Pydantic AI. Version 2 is in beta, so a major-version upgrade is expected later.
- Every AI feature needs evals, because the tests do not check the real model's answers.
