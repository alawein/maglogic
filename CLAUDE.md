---
type: guide
authority: canonical
audience: [ai-agents, contributors]
last-verified: 2026-03-09
---

# CLAUDE.md

This file provides repo-specific guidance for agent work in `maglogic`.

## Repository Context

**Project:** MagLogic
**Domain:** computational magnetism, based on Alawein et al., IEEE Magnetics
Letters 2019
**Status:** active research library and simulation suite

## Layout Truth

MagLogic is a polyglot scientific suite, not a Python-only library.

- `python/maglogic/` is the canonical Python package
- `python/tests/` is the canonical Python test surface
- `oommf/` and `mumax3/` are first-class simulation asset surfaces
- `matlab/` is a maintained reference-implementation surface
- `docs/` and `scripts/` are repo-local support surfaces

Do not introduce a parallel `src/` tree without an explicit migration decision.

## Commands

### Setup

- `pip install -e ".[dev]"` — install development dependencies
- `conda env create -f environment.yml` — create the conda environment
- `docker compose up --build` — run the Dockerized environment

### Validation

- `python scripts/validate-structure.py` — verify repo layout
- `PYTHONPATH=python python -c "import maglogic"` — verify package importability
- `PYTHONPATH=python python -m pytest -s python/tests/test_constants.py python/tests/test_analysis.py` — representative tests when dependencies are installed

### Tooling

- `black python/` — format Python code
- `flake8 python/` — lint Python code
- `ruff check python/` — run Ruff if configured locally
- `mypy python/maglogic/` — type-check Python package

## Important Notes

- Heavy scientific dependencies are optional in some environments
- GPU-related work must keep CPU fallback paths
- Do not casually modify reference simulation assets in `oommf/` and `mumax3/`
- `pyproject.toml` is the packaging authority for the Python surface

## Governance

See [AGENTS.md](AGENTS.md) for rules and [SSOT.md](SSOT.md) for the current
state.
