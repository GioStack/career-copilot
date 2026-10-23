# 0008. Use an issue, branch and pull request workflow

## Status
Accepted (2026-10-13). Refined by ADR 0012.

## Context
Changes should be traceable (what changed and why), reviewed before they reach `main`,
and should never leave `main` in a broken state.

## Decision
Every code or test change follows this flow:
1. Open a GitHub Issue describing the problem or feature.
2. Create a branch from an up-to-date `main` (`feat/...`, `fix/...`, `test/...`).
3. Write tests first, then the code.
4. Run `ruff format`, `ruff check --fix` and `pytest` before committing.
5. Push the branch and open a Pull Request with `Closes #N`.
6. Review the diff in "Files changed", then **Squash and merge** and delete the branch.
7. Sync locally: `git switch main`, `git pull`, `git branch -d ...`, `git fetch --prune`.

Changes that cannot break code (docs, ADRs, license, typos) may be committed directly to `main`.

## Alternatives considered
- **Commit directly to `main`**: faster, but untested or half-finished work can break `main`,
  and there is no place to review a change or link it to its reason.
- **Merge commit / rebase and merge**: keep every intermediate commit in `main`;
  squash keeps one clean commit per change, linked to its PR.

## Consequences
- `main` always works, and every change is linked: commit → PR → Issue.
- Each change is reviewed in isolation before it is merged.
- More steps per change, even for small code fixes.
- With squash merge, `git branch -d` warns about the deleted branch; this is expected.