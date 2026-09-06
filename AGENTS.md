---
type: canonical
source: none
sync: none
sla: none
authority: canonical
audience: [agents, contributors, maintainers]
last_updated: 2026-09-06
last-verified: 2026-09-06
---

# AGENTS: MagLogic

## Workspace identity

MagLogic is a research-library repo for nanomagnetic logic simulations across
Python, OOMMF, MuMax3, and MATLAB.

## Directory structure

- `python/maglogic/`: primary Python source
- `python/tests/`: required verification
- `oommf/`: OOMMF assets
- `mumax3/`: MuMax3 assets
- `matlab/`: reference implementation surface
- `examples/`: runnable demos

- `docker/`: reproducible environment definitions

- `docs/`: repo-local theory, API, and structure documentation

## Governance rules

1. Keep the Python package rooted at `python/maglogic/`.
2. Do not add a parallel `src/` tree.
3. Treat OOMMF and MuMax3 inputs as reference assets, not casual scratch files.
4. Preserve both solver backends where a feature claims to support them.
5. Comments and docs should explain solver assumptions and geometry choices.

6. GPU-oriented workflows must still document or preserve CPU fallback paths.

7. When Python behavior changes, keep examples and reference implementations from drifting silently.

8. Update citation metadata for release-grade scientific changes.

9. Do not casually modify reference `.mif` or `.mx3` inputs.

## Simplicity defaults

- Make the smallest change that satisfies the acceptance criteria.
- Prefer direct functions and plain data structures.
- No class when a function suffices. No framework for one implementation.
- No shared abstraction before real duplication exists.
- Prefer the standard library or an existing dependency.
- Avoid factories, registries, adapters, plugins, and config layers without multiple real consumers.
- Keep control flow direct. Use early returns when clearer. Keep errors explicit.
- Comments explain invariants, assumptions, and failure modes. Delete dead code instead of commenting it out.
- Keep pull requests single-purpose. Stop when tests and acceptance criteria pass. Do not rewrite adjacent working code without a stated need.

## Code conventions

- Type hints and accurate docstrings on public Python surfaces
- Conventional commits only
- Add or adjust tests when Python behavior changes

## Build and test commands

```bash
pip install -e ".[dev]"
python scripts/validate-structure.py
PYTHONPATH=python python -m pytest -s python/tests/test_constants.py python/tests/test_analysis.py
black python/
flake8 python/
ruff check python/
mypy python/maglogic/
```
