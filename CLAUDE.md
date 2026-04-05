---
type: canonical
source: none
sync: none
sla: none
authority: canonical
audience: [ai-agents, contributors]
last-verified: 2026-03-09
---

<!-- Domain-Specific Rules -->
- **Build:** setuptools via `pyproject.toml`
- **Conda:** `environment.yml` for conda-based setup
- **Core deps:** NumPy, SciPy, Matplotlib (Python surface)
- **Do not modify simulation reference assets casually**: OOMMF `.mif` and MuMax3 `.mx3` input files are reference data
- **Docker:** Container definitions available for reproducible environments
- **GPU code must include CPU fallback**: Never assume GPU availability
- **Language:** Python 3.9+ (canonical package), MATLAB, OOMMF, MuMax3
- **Linting:** black, flake8, ruff, mypy
- **Micromagnetic engines:** OOMMF (CPU), MuMax3 (GPU)
- **No parallel `src/` tree**: Canonical Python package lives at `python/maglogic/`; do not restructure without explicit migration decision
- **OOMMF and MuMax3 are first-class surfaces**: Simulation assets in `oommf/` and `mumax3/` are not secondary to Python
- **Support both OOMMF and MuMax3 backends**: Where applicable, features should work with both micromagnetic engines
- **Testing:** pytest (Python), MATLAB `runtests`

<!-- Template: research-library v1.0.0 -->
<!-- Generated from _pkos governance templates. Do not edit the template sections -->
<!-- directly in consuming projects — update the template and re-sync instead.    -->

# CLAUDE.md — MagLogic

## Repository Context

**Name:** MagLogic
**Type:** research-library
**Purpose:** Nanomagnetic logic simulation suite for computational magnetism. Polyglot
scientific suite spanning Python, MATLAB, OOMMF, and MuMax3 surfaces. Based on Alawein
et al., IEEE Magnetics Letters 2019.


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
