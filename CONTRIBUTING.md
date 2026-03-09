# Contributing to MagLogic

This project follows the [alawein org contributing standards](https://github.com/alawein/alawein/blob/main/CONTRIBUTING.md)
and the local repository rules in [AGENTS.md](AGENTS.md).

## Quick Start

```bash
git clone https://github.com/alawein/maglogic.git
cd maglogic
pip install -e ".[dev]"
python scripts/validate-structure.py
PYTHONPATH=python python -c "import maglogic"
```

If you prefer Conda:

```bash
conda env create -f environment.yml
conda activate maglogic
```

## Workflow

1. Branch from `main`.
2. Make the smallest coherent change.
3. Update docs when layout, simulation workflow, or package boundaries change.
4. Run the repo validation commands before proposing the change.

## Validation

```bash
python scripts/validate-structure.py
PYTHONPATH=python python -c "import maglogic"
```

Representative tests, when dependencies are installed:

```bash
PYTHONPATH=python python -m pytest -s python/tests/test_constants.py python/tests/test_analysis.py
```

## Structure Rules

- Keep the Python package under `python/maglogic/`.
- Keep Python tests under `python/tests/`.
- Keep OOMMF assets under `oommf/`.
- Keep MuMax3 assets under `mumax3/`.
- Keep MATLAB reference implementations under `matlab/`.
- Do not introduce `src/` without an explicit migration decision.

## Documentation

See:

- [README.md](README.md)
- [SSOT.md](SSOT.md)
- [docs/README.md](docs/README.md)
- [docs/architecture/STRUCTURE_DECISION.md](docs/architecture/STRUCTURE_DECISION.md)
