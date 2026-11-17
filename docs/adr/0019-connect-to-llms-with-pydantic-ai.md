# 0019. Connect to LLMs with Pydantic AI

## Status

Accepted (2026-11-17).

## Context

The AI features (tailored CV, cover letter, ATS check, LinkedIn, mock interviews) need an LLM. The README promises "bring your own LLM key", so users choose their provider: a hosted one such as Claude or Gemini, or a local one through Ollama. The app works with structured data (Pydantic schemas), so the LLM's answers should come back in the same form. Tests must not call a real LLM, which is slow, costs money and gives a different answer each time.

## Decision

Use Pydantic AI (v1, pinned below 2) to call the LLM.

- The provider and model come from `LLM_MODEL` in `.env` (for example `anthropic:<model>` or `google-gla:<model>`), and the provider's API key from its own variable. Both are read by the settings (ADR 0006) and never committed.
- Every LLM call returns a Pydantic model. If the answer does not match the schema, Pydantic AI asks the model to correct it.
- Tests use Pydantic AI's test model instead of a real one. The real model is checked by evals, separately from the tests.

## Alternatives considered

- **A provider's own SDK** (for example `anthropic`): supports structured output, but only for that provider, so users could not bring a different key.
- **LiteLLM**: one API for many providers, but it returns plain text or JSON with no validation against a schema.
- **Calling the providers' HTTP APIs directly**: no dependency, but every provider's request and response format would have to be written and kept up to date by hand.

## Consequences

- Switching provider is a change to `.env`, not to the code.
- The AI code depends on Pydantic AI. Version 2 is in beta, so a major-version upgrade is expected later.
- Features are limited to what Pydantic AI supports across providers.
- Every AI feature needs evals, because the tests do not check the real model's answers.
