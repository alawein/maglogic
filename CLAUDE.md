# Claude AI Assistant Guide

## Repository Context

**Name:** MagLogic  
**Type:** research-library  
**Purpose:** Nanomagnetic logic simulation suite — micromagnetic simulations via OOMMF and MuMax3 backends. Implements reconfigurable logic gate analysis (NAND/NOR, majority gates) from Alawein et al., IEEE Magnetics Letters 2019.

## Tech Stack

- **Language:** Python 3.8+, MATLAB
- **Core deps:** NumPy, SciPy, Matplotlib, h5py
- **Optional:** PyTorch, scikit-learn
- **Build:** setuptools (`pyproject.toml` + legacy `setup.py`)
- **Environment:** Conda (`environment.yml`) or Docker Compose
- **Backends:** OOMMF, MuMax3

## Key Files

- `README.md` — Main documentation
- `pyproject.toml` — Package configuration
- `python/` — Core Python package (simulations, parsers, analysis, visualization)
- `matlab/` — MATLAB implementations
- `oommf/` — OOMMF simulation files
- `mumax3/` — MuMax3 simulation files
- `examples/` — Demo scripts and notebooks
- `docker/` — Docker configuration
- `docs/` — Detailed documentation

## Development Guidelines

1. Follow existing code style — use `ruff` for linting, `mypy` for type checking
2. Add tests for new features (`pytest`)
3. Update documentation for any API changes
4. Use conventional commits
5. Support both OOMMF and MuMax3 backends where applicable

## Common Tasks

### Running Tests
```bash
pytest
pytest --cov=maglogic
```

### Building
```bash
pip install -e ".[dev]"
# or via Conda
conda env create -f environment.yml
conda activate maglogic
```

### Docker
```bash
docker-compose up --build
```

## Architecture

Multi-backend simulation framework: Python core wraps OOMMF and MuMax3 for micromagnetic calculations. MATLAB implementations provide parallel reference code. Analysis pipeline handles magnetization patterns, domain structures, energy landscapes, and truth table verification for nanomagnetic logic gates.
