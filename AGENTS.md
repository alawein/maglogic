---
type: normative
authority: canonical
audience: [agents, contributors, maintainers]
last-verified: 2026-03-01
---

# AGENTS -- maglogic

> Nanomagnetic logic simulation suite. Based on Alawein et al., IEEE Magnetics Letters 2019.

## Repository Scope

Python + MATLAB library for micromagnetic simulations via OOMMF and MuMax3
backends. Implements reconfigurable logic gate analysis (NAND/NOR, majority
gates) for triangular element geometries.

## Key Directories

| Directory | Purpose |
|-----------|---------|
| `python/` | Core Python package (simulations, parsers, analysis, visualization) |
| `matlab/` | MATLAB implementations |
| `oommf/` | OOMMF simulation files |
| `mumax3/` | MuMax3 simulation files |
| `examples/` | Demo scripts and notebooks |
| `docker/` | Docker configuration |
| `tests/` | Test suite |
| `docs/` | Documentation |

## Commands

- `pip install -e ".[dev]"` -- install with dev dependencies
- `conda env create -f environment.yml` -- create conda environment
- `docker-compose up --build` -- run via Docker
- `pytest` -- run tests
- `pytest --cov=maglogic` -- run tests with coverage

## Agent Rules

- Read this file before making changes
- Support both OOMMF and MuMax3 backends where applicable
- Add tests for new features (`pytest`)
- Use `ruff` for linting and `mypy` for type checking
- GPU code must include CPU fallback
- Do not modify simulation output files in `oommf/` or `mumax3/` directly
- Update `CITATION.cff` for releases
- Use conventional commit messages: `feat(scope):`, `fix(scope):`, etc.

## Naming Conventions

- Python modules: `snake_case.py`
- Classes: `PascalCase`
- Functions: `snake_case`
- Constants: `UPPER_SNAKE_CASE`

See [CLAUDE.md](CLAUDE.md) | [SSOT.md](SSOT.md)