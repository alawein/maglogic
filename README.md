# MagLogic

Status:      frozen
Category:    lab
Owner:       alawein
Visibility:  public
Purpose:     Magnetic logic gates and device simulation research.
Next action: continue

## Abstract

MagLogic is a Python analysis layer for nanomagnetic logic simulations run in
OOMMF and MuMax3, implementing the triangular-element logic gates and cellular
automata from Alawein et al., IEEE Magnetics Letters 2019. It is for
researchers and students who need truth-table extraction and
energy-landscape analysis on top of raw solver output, rather than a general
micromagnetics package. It does not run micromagnetic simulations itself;
OOMMF and MuMax3 must be installed separately to produce the data this
package analyzes.

## Status

- Lifecycle: frozen
- Verification date: 2026-08-28
- Scope: Python package under `python/maglogic/`, OOMMF/MuMax3 assets, MATLAB references

## Runtime requirements

- Python 3.8+ with `conda env create -f environment.yml`, or `pip install -e ".[dev]"` when conda is not available
- OOMMF and/or MuMax3 for full micromagnetic runs (`oommf/`, `mumax3/`)
- Docker via `docker compose -f docker/docker-compose.yml up --build` (not run for this PR)
- Set `PYTHONPATH=python` when running outside an editable install

## Reproducibility

```bash
pip install -e ".[dev]"
python scripts/validate-structure.py
python -m pytest python/tests -q
```

conda was not available on the machine used to verify this pass, so pip
installed directly from `pyproject.toml`; `conda env create -f
environment.yml` is the documented alternative.

Quick demo (requires OOMMF on `PATH`; not run in this pass):

```bash
PYTHONPATH=python python examples/run_basic_triangle.py
```

See [docs/architecture/STRUCTURE_DECISION.md](docs/architecture/STRUCTURE_DECISION.md) for the language-boundary layout (`python/maglogic/` is canonical; this repo does not use `src/<package>`).

## Datasets

- Simulation inputs and reference outputs live under `oommf/` and `mumax3/`
- No external dataset download required for bundled demos

## Architecture

```text
maglogic/
├── python/maglogic/  # canonical Python package
├── python/tests/     # pytest suite
├── oommf/ mumax3/    # micromagnetic solver inputs
├── matlab/           # MATLAB reference implementations
├── examples/ docker/ # demos and reproducible environment
└── docs/             # theory, API, architecture decisions
```

Detail: [docs/architecture/topology.md](docs/architecture/topology.md), [docs/architecture/STRUCTURE_DECISION.md](docs/architecture/STRUCTURE_DECISION.md), and [docs/architecture.md](docs/architecture.md).

## Docs map

- [docs/README.md](docs/README.md)
- [SSOT.md](SSOT.md)
- [LESSONS.md](LESSONS.md)
