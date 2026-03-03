# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with
code in this repository.

**Project**: MagLogic -- Nanomagnetic Logic Simulation Suite
**Domain**: Computational magnetism (based on Alawein et al., IEEE Magnetics Letters 2019)
**Status**: Active research library

## Commands

### Development

- `pip install -e ".[dev]"` - Install with dev dependencies
- `conda env create -f environment.yml` - Create conda environment
- `conda activate maglogic` - Activate conda environment
- `docker-compose up --build` - Run via Docker
- `python -m pytest python/tests/` - Run test suite
- `python -m pytest python/tests/ --cov=maglogic` - Run tests with coverage
- `python -m pytest python/tests/ -m "not slow"` - Skip slow tests
- `ruff check .` - Lint code
- `mypy python/maglogic/` - Type checking
- `black python/` - Format code

### Testing

- Test directory: `python/tests/`
- Markers: `slow`, `gpu`, `oommf`, `mumax3`, `integration`
- Coverage reports: term-missing, HTML, XML

### Installation

- `pip install -e ".[dev]"` - Editable install with dev tools
- `pip install -e ".[ml]"` - Include ML dependencies (PyTorch, scikit-learn, TensorFlow)
- `pip install -e ".[hpc]"` - Include HPC dependencies (mpi4py, dask, zarr)
- `pip install -e ".[gui]"` - Include GUI dependencies (PyQt5, pyqtgraph)

## Architecture Overview

**MagLogic** is a **Python + MATLAB** library for micromagnetic simulations via
OOMMF and MuMax3 backends. Implements reconfigurable logic gate analysis
(NAND/NOR, majority gates) for triangular element geometries.

### Tech Stack

- **Language**: Python 3.8+, MATLAB
- **Core Dependencies**: NumPy, SciPy, Matplotlib, Pandas, h5py
- **Optional ML**: PyTorch, scikit-learn, TensorFlow, XGBoost, LightGBM
- **Simulation Backends**: OOMMF, MuMax3
- **Build System**: setuptools (pyproject.toml)
- **Environment**: Conda or Docker Compose
- **Linting**: ruff, flake8
- **Type Checking**: mypy (strict mode)
- **Formatting**: black (line-length 88)

### Project Structure

- `/python/maglogic/` - Core Python package
  - `/python/maglogic/core/` - Core simulation primitives
  - `/python/maglogic/simulation/` - Simulation runners and wrappers
  - `/python/maglogic/parsers/` - Output file parsers (OOMMF, MuMax3 formats)
  - `/python/maglogic/analysis/` - Analysis tools (magnetization, energy, truth tables)
  - `/python/maglogic/visualization/` - Plotting and visualization
  - `/python/maglogic/demos/` - Demo and example scripts
- `/python/tests/` - Test suite (pytest)
- `/matlab/` - MATLAB reference implementations
- `/oommf/` - OOMMF simulation input files
- `/mumax3/` - MuMax3 simulation input files
- `/examples/` - Demo scripts and Jupyter notebooks
- `/docker/` - Docker configuration
- `/docs/` - Documentation

### Key Configuration

- **pyproject.toml**: Package metadata, dependencies, tool configs (pytest, mypy, black, isort, flake8)
- **environment.yml**: Conda environment specification
- **pytest markers**: `slow`, `gpu`, `oommf`, `mumax3`, `integration`
- **CLI entry points**: `maglogic`, `maglogic-convert`, `maglogic-analyze`, `maglogic-gui`

### Important Notes

- **Heavy imports**: SciPy and PyTorch are used extensively -- import times can be significant
- **CFL condition**: Simulations must respect the Courant-Friedrichs-Lewy stability condition; time steps that violate CFL will produce non-physical results
- Support both OOMMF and MuMax3 backends where applicable
- GPU code must include CPU fallback paths
- Do not modify simulation output files in `oommf/` or `mumax3/` directly
- Update `CITATION.cff` for releases
- Governance: Has `AGENTS.md` from Morphism framework
