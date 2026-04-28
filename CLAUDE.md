---
type: canonical
source: none
sync: none
sla: none
authority: canonical
audience: [ai-agents, contributors]
last_updated: 2026-04-15
last-verified: 2026-04-15
---

# CLAUDE.md — MagLogic

## Workspace identity

MagLogic is a research-library repo for nanomagnetic logic simulations across
Python, OOMMF, MuMax3, and MATLAB. The repo should read like an operator-facing
scientific workspace, not like a generic Python wrapper around hidden solver
state.

Shared voice and research-writing contract:

- <https://github.com/alawein/alawein/blob/main/docs/style/VOICE.md>
- <https://github.com/alawein/alawein/blob/main/prompt-kits/AGENT.md>

## Directory structure

- `python/maglogic/`: canonical Python package
- `python/tests/`: required Python verification
- `oommf/`: OOMMF simulation inputs and domain assets
- `mumax3/`: MuMax3 simulation inputs and domain assets
- `matlab/`: MATLAB reference implementation surface
- `examples/`: runnable demos
- `docker/`: reproducible environment definitions
- `docs/`: repo-local theory, API, and structure documentation

## Governance rules

1. Keep the canonical Python package under `python/maglogic/`.
2. Do not introduce a parallel `src/` tree without an explicit migration
   decision.
3. OOMMF and MuMax3 are first-class surfaces, not secondary assets.
4. Do not casually modify reference `.mif` or `.mx3` inputs.
5. GPU-oriented workflows must still document or preserve CPU fallback paths.
6. When Python behavior changes, keep examples and reference implementations
   from drifting silently.
7. Update citation metadata for release-grade scientific changes.

## Code conventions

- Public Python imports resolve from `python/maglogic/`.
- Tests live under `python/tests/`.
- Comments explain physical assumptions, geometry constraints, or solver
  tradeoffs.
- Prefer the real engine boundary over fake abstraction when the solver details
  matter.

## Build and test commands

```bash
conda env create -f environment.yml
pip install -e ".[dev]"
python scripts/validate-structure.py
PYTHONPATH=python python -c "import maglogic"
PYTHONPATH=python python -m pytest -s python/tests/test_constants.py python/tests/test_analysis.py
black python/
flake8 python/
ruff check python/
mypy python/maglogic/
```
