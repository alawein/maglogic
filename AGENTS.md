---
type: normative
authority: canonical
audience: [agents, contributors, maintainers]
last-verified: 2026-03-09
---

# AGENTS — maglogic

> Nanomagnetic logic simulation suite.
> Based on Alawein et al., IEEE Magnetics Letters 2019.

## Repository Scope

Polyglot research suite for nanomagnetic logic simulations across Python,
MATLAB, OOMMF, and MuMax3 surfaces. The canonical Python package lives under
`python/maglogic/`, alongside domain assets and reference implementations at the
repo root.

## Key Directories

| Directory | Purpose |
|-----------|---------|
| `python/maglogic/` | Canonical Python package |
| `python/tests/` | Python test suite |
| `matlab/` | MATLAB reference implementations |
| `oommf/` | OOMMF simulation inputs and assets |
| `mumax3/` | MuMax3 simulation inputs and assets |
| `examples/` | Demo scripts and exploratory usage |
| `docker/` | Container definitions |
| `docs/` | Theory, API, development, and structure docs |
| `scripts/` | Repo-local validation and maintenance helpers |

## Commands

- `pip install -e ".[dev]"` — install with development dependencies
- `conda env create -f environment.yml` — create the conda environment
- `python scripts/validate-structure.py` — verify the canonical repo layout
- `PYTHONPATH=python python -c "import maglogic"` — verify the package surface
- `PYTHONPATH=python python -m pytest -s python/tests/test_constants.py python/tests/test_analysis.py` — run representative tests when dependencies are installed

## Agent Rules

- Read this file before making changes
- Keep the canonical Python package under `python/maglogic/`
- Keep tests under `python/tests/`
- Do not introduce a parallel `src/` tree without an explicit migration decision
- Support both OOMMF and MuMax3 backends where applicable
- Do not modify simulation output or reference input assets in `oommf/` or
  `mumax3/` casually
- Add tests for new Python features when dependencies permit
- Use `black` for formatting, `flake8` and `ruff` for linting, and `mypy` for
  typing
- GPU code must include CPU fallback
- Update `CITATION.cff` for release-grade changes
- Use conventional commit messages: `feat(scope):`, `fix(scope):`, etc.

## Naming Conventions

- Python modules: `snake_case.py`
- Classes: `PascalCase`
- Functions: `snake_case`
- Constants: `UPPER_SNAKE_CASE`

See [CLAUDE.md](CLAUDE.md) | [SSOT.md](SSOT.md)
