<!-- Template: research-library v1.0.0 -->
<!-- Generated from _pkos governance templates. Do not edit the template sections -->
<!-- directly in consuming projects — update the template and re-sync instead.    -->
---
type: guide
authority: canonical
audience: [ai-agents, contributors]
last-verified: 2026-03-09
---

# CLAUDE.md — MagLogic

## Repository Context

**Name:** MagLogic
**Type:** research-library
**Purpose:** Nanomagnetic logic simulation suite for computational magnetism. Polyglot
scientific suite spanning Python, MATLAB, OOMMF, and MuMax3 surfaces. Based on Alawein
et al., IEEE Magnetics Letters 2019.

---

## Tech Stack

- **Language:** Python 3.9+ (canonical package), MATLAB, OOMMF, MuMax3
- **Core deps:** NumPy, SciPy, Matplotlib (Python surface)
- **Build:** setuptools via `pyproject.toml`
- **Testing:** pytest (Python), MATLAB `runtests`
- **Linting:** black, flake8, ruff, mypy

<!-- EXTENSION SLOT: Toolchain
     Add project-specific toolchain details here (HPC tools, simulation
     engines, external solvers, GPU frameworks, etc.)
-->
- **Micromagnetic engines:** OOMMF (CPU), MuMax3 (GPU)
- **Docker:** Container definitions available for reproducible environments
- **Conda:** `environment.yml` for conda-based setup

---

## Commands

### Setup

```bash
pip install -e ".[dev]"
conda env create -f environment.yml
docker compose up --build
```

### Test

```bash
PYTHONPATH=python python -m pytest -s python/tests/test_constants.py python/tests/test_analysis.py
```

### Lint / Format

```bash
black python/
flake8 python/
ruff check python/
mypy python/maglogic/
```

<!-- EXTENSION SLOT: Additional Commands
     Add project-specific command sections here (benchmarks, agents,
     SSOT, simulation workflows, HPC job submission, etc.)
-->

### Validation

```bash
python scripts/validate-structure.py
PYTHONPATH=python python -c "import maglogic"
```

---

## Architecture Overview

MagLogic is a polyglot scientific suite, not a Python-only library.

- `python/maglogic/` is the canonical Python package
- `python/tests/` is the canonical Python test surface
- `oommf/` and `mumax3/` are first-class simulation asset surfaces
- `matlab/` is a maintained reference-implementation surface
- `docs/` and `scripts/` are repo-local support surfaces

Do not introduce a parallel `src/` tree without an explicit migration decision.

---

## Project Structure

```
maglogic/
├── python/maglogic/       # Canonical Python package
├── python/tests/          # Python test suite
├── matlab/                # MATLAB reference implementations
├── oommf/                 # OOMMF simulation inputs and assets
├── mumax3/                # MuMax3 simulation inputs and assets
├── examples/              # Demo scripts and exploratory usage
├── docker/                # Container definitions
├── docs/                  # Theory, API, development, and structure docs
├── scripts/               # Repo-local validation and maintenance helpers
└── pyproject.toml         # Package configuration
```

---

## Key Configuration

| File | Purpose |
|------|---------|
| `pyproject.toml` | Build, deps, tool config |
| `AGENTS.md` | Governance invariants (normative) |
| `environment.yml` | Conda environment definition |

---

## Important Notes / Known Quirks

<!-- Standard research library notes -->

**Deterministic seeds** -- All benchmark and experiment runs must use fixed seeds.
Reproducibility is a governance invariant. Never remove seed arguments from benchmark
or test code.

**Archive is read-only** -- If an `archive/` directory exists, it contains historical
data and papers. Never modify its contents.

**API stability** -- Breaking changes to the public API require a version bump and a
`CHANGELOG.md` entry.

**Pre-commit / linting** -- Run the project's format command before committing.

<!-- EXTENSION SLOT: Domain-Specific Notes
     Add project-specific quirks, numerical issues, data handling rules,
     dependency caveats, etc.
-->

**Canonical root package** -- The Python package is rooted at `python/maglogic/`, not `src/`.
Do not introduce a parallel `src/` tree without an explicit migration decision.

**Heavy scientific dependencies are optional** -- Some environments may not have all
scientific deps installed. Guard imports accordingly.

**GPU code must keep CPU fallback paths** -- Never assume GPU availability.

**Simulation assets are reference data** -- Do not casually modify reference simulation
assets in `oommf/` and `mumax3/`.

---

## Domain-Specific Rules

<!-- EXTENSION SLOT: Domain-Specific Rules
     Each project fills this section with rules unique to its research domain.
-->

- **No parallel `src/` tree**: Canonical Python package lives at `python/maglogic/`; do not restructure without explicit migration decision
- **OOMMF and MuMax3 are first-class surfaces**: Simulation assets in `oommf/` and `mumax3/` are not secondary to Python
- **Do not modify simulation reference assets casually**: OOMMF `.mif` and MuMax3 `.mx3` input files are reference data
- **GPU code must include CPU fallback**: Never assume GPU availability
- **Support both OOMMF and MuMax3 backends**: Where applicable, features should work with both micromagnetic engines

---

## Data Integrity

<!-- EXTENSION SLOT: Data Integrity
     Define project-specific rules for data handling, reproducibility,
     and research artifact management.
-->

- **Simulation inputs are reference data**: OOMMF and MuMax3 input files should not be modified without verification against published results
- **Benchmark results must be reproducible**: Fixed seeds and documented simulation parameters for all published comparisons
- **Update CITATION.cff for release-grade changes**: Academic citation metadata must stay current

---

## Governance

See [AGENTS.md](AGENTS.md) for rules. See [SSOT.md](SSOT.md) for current state.
