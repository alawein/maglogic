# MagLogic Structure Decision

## Decision

MagLogic intentionally uses a **language-boundary layout**.

The canonical Python package surface is:

`python/maglogic/`

The canonical Python test surface is:

`python/tests/`

This repository does **not** use `src/<package>` as its Python boundary.

## Canonical Surfaces

- `python/maglogic/` — Python package
- `python/tests/` — Python tests
- `oommf/` — OOMMF assets and inputs
- `mumax3/` — MuMax3 assets and inputs
- `matlab/` — MATLAB reference implementations
- `examples/` — demos and exploratory usage
- `docker/` — container and environment surface
- `docs/` — repo-local documentation
- `scripts/` — repo-local validation and maintenance helpers

## Why This Is Intentional

MagLogic is a polyglot scientific suite. The Python package is only one of
several first-class runtime and asset surfaces. Keeping the Python code under a
dedicated `python/` boundary is clearer than pretending the repo is a pure
Python package.

## Rules

- Keep importable Python code under `python/maglogic/`.
- Keep Python tests under `python/tests/`.
- Do not create a parallel `src/` tree without an explicit migration plan.
- Keep OOMMF, MuMax3, and MATLAB surfaces separate and documented.
