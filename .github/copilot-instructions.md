# Repo instructions for GitHub Copilot

GitHub Copilot reads this file from `.github/copilot-instructions.md`. The prompts live in
`.github/prompts/` as `.prompt.md` files. Read this at the start of a session.

## What this project is

Magnetic logic gates and device simulation research.

## Prompts

Use the one that fits the step you are on.

- `plan-change` before a non-trivial edit.
- `implement-change` to make the change in small steps.
- `write-tests` for behavior and expected contracts.
- `debug-failure` when a check fails.
- `refactor-safely` to change structure without changing behavior.
- `code-review` for a structured review.
- `prepare-pr` to draft the commit and PR and run checks.
- `handoff-session` to leave a short handoff for the next session.

## Working agreement

- Plan before a non-trivial edit.
- Make the smallest change that solves the problem.
- Add or update a test when behavior changes.
- Run the required checks before you call the work done: `ruff check . && mypy . && pytest`.
- Stage explicit paths. Keep `.env` and secrets out of git.
- Imperative commit subject, one concern per commit or PR.

## Final report

End with what changed, what you ran, and the results. Say what is verified and what is still open. Do not claim work you did not run.
