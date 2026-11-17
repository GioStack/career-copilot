# 0018. Group skills in the prompt, not in the database

## Status

Accepted (2026-11-17).

## Context

A CV shows skills in groups such as Frameworks, AI and Tools. The CV text will be written by an LLM, which can group skills on its own, and the best grouping and order can change with the job ad. Storing a category for each skill would need a new column and a migration that fills in the existing skills.

## Decision

Do not store a category for skills. The prompt that writes the CV lists the groups and their order (for example Frameworks, AI, Tools), and the LLM puts each skill in a group.

## Alternatives considered

- **A fixed list of categories in the database**: the same groups in every CV, but they cannot change with the job ad, and the existing skills need a value such as `Other`.
- **Free-text categories in the database**: no fixed list, but `AI`, `ai` and `A.I.` would become three different groups.

## Consequences

- No column or migration for categories.
- Changing the groups or their order is a change to the prompt.
- The grouping is checked with evals in the AI phase; if it is wrong or changes between CVs, a `category` column with a fixed list is added then.
