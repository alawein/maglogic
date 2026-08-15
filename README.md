# MagLogic

Status:      frozen
Category:    research
Owner:       alawein
Visibility:  public
Purpose:     Magnetic logic gates and device simulation research.
Next action: continue

## Abstract

MagLogic simulates nanomagnetic logic devices using OOMMF and MuMax3 backends.
It implements triangular-element logic gates and cellular automata from Alawein
et al., IEEE Magnetics Letters 2019, with automated truth-table verification and
energy-landscape analysis for teaching and reproducible research.

## Status

- Lifecycle: frozen
- Verification date: 2026-06-29
- Scope: Python package under `python/maglogic/`, OOMMF/MuMax3 assets, MATLAB references

## Runtime requirements

- Python 3.8+ with `conda env create -f environment.yml` or Docker via `docker compose up --build`
- OOMMF and/or MuMax3 for full micromagnetic runs (`oommf/`, `mumax3/`)
- Set `PYTHONPATH=python` when running outside an editable install

## Reproducibility

```bash
git clone https://github.com/alawein/maglogic.git
cd maglogic
conda env create -f environment.yml
conda activate maglogic
pip install -e ".[dev]"
python scripts/validate-structure.py
PYTHONPATH=python python -m pytest python/tests/ -v
```

Quick demo:

```bash
PYTHONPATH=python python examples/run_basic_triangle.py
```

See [docs/architecture/STRUCTURE_DECISION.md](docs/architecture/STRUCTURE_DECISION.md) for the language-boundary layout (`python/maglogic/` is canonical; this repo does not use `src/<package>`).

## Datasets

- Simulation inputs and reference outputs live under `oommf/` and `mumax3/`
- No external dataset download required for bundled demos
- Regenerate figures from documented scripts before citing numerical results


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
