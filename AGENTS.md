---
type: canonical
source: none
sync: none
sla: none
authority: canonical
audience: [agents, contributors, maintainers]
last_updated: 2026-04-15
last-verified: 2026-04-15
---

# AGENTS — MagLogic

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

## Governance rules

1. Keep the Python package rooted at `python/maglogic/`.
2. Do not add a parallel `src/` tree.
3. Treat OOMMF and MuMax3 inputs as reference assets, not casual scratch files.
4. Preserve both solver backends where a feature claims to support them.
5. Comments and docs should explain solver assumptions and geometry choices.

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
