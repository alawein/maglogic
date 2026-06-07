---
type: canonical
owner: platform-engineering
last-reviewed: 2026-03-31
---

# Architecture Overview -- maglogic

MagLogic is a polyglot research library for nanomagnetic logic simulation,
grounded in Alawein et al. (IEEE Magnetics Letters, 2019). It is not a web
service or deployed application. The unit of work is a simulation run, not a
request-response cycle.

## Components

The repo uses a language-boundary layout. Each surface is first-class:

| Surface | Role |
|---------|------|
| `python/maglogic/` | Canonical Python package: simulation helpers, analysis, truth-table verification |
| `python/tests/` | Python test suite (pytest) |
| `matlab/` | MATLAB reference implementations of the same logic-gate models |
| `oommf/` | OOMMF simulation input files (`.mif`) and domain assets |
| `mumax3/` | MuMax3 simulation input files (`.mx3`) and domain assets |
| `examples/` | Runnable demo scripts and notebooks |
| `docker/` | Reproducible environment definitions (Docker Compose) |
| `scripts/` | Repo-local validation and maintenance helpers |
| `docs/` | Repo-local documentation |

The Python package does not use `src/` layout. See
[docs/architecture/STRUCTURE_DECISION.md](architecture/STRUCTURE_DECISION.md)
for the explicit rationale.

## Data Flow

A typical simulation run follows this path:

1. A researcher selects an input file from `oommf/` or `mumax3/`, or generates
   one via `python/maglogic/`.
2. The solver (OOMMF or MuMax3, running locally or in Docker) produces
   magnetization output data.
3. `python/maglogic/` analysis utilities read the solver output, detect domain
   patterns, and compute logic outputs.
4. Results are compared against expected truth-table entries via the automated
   verification helpers in `examples/` or `python/tests/`.

MATLAB implementations in `matlab/` follow the same conceptual flow as
reference cross-checks, not as the primary compute path.

## Dependencies

Runtime dependencies are declared in `environment.yml` (conda) and
`pyproject.toml` (pip extras). Key external dependencies:

- OOMMF and/or MuMax3: micromagnetic solvers (not bundled; install separately
  or use the Docker image).
- NumPy, SciPy: numerical computation.
- Matplotlib: figure generation.
- Docker (optional): reproducible solver environment via `docker/`.

See `environment.yml` and `pyproject.toml` for pinned versions.

## Constraints

- OOMMF and MuMax3 are external binaries. The Python package degrades
  gracefully when they are absent (demo mode uses pre-computed reference data).
- GPU acceleration is available through MuMax3's CUDA backend. CPU fallback
  paths must remain documented and functional.
- The repo does not expose a network API. All interaction is through scripts,
  notebooks, or the Python package import surface.
- Simulation inputs (`.mif`, `.mx3`) are reference artifacts; do not modify
  them casually without recording the change rationale.
