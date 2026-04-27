# MagLogic

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## About

Python tools for simulating nanomagnetic logic devices using OOMMF and MuMax3 backends. Implements nanomagnetic logic simulations from Alawein et al. (IEEE Magnetics Letters, 2019) for triangular element logic gates and cellular automata—designed for reproducible research and teaching.

## Features

- Micromagnetic simulations via OOMMF and MuMax3
- Reconfigurable logic gate analysis (NAND/NOR, majority gates)
- Magnetization pattern analysis and domain structure detection
- Energy landscape calculation and topological feature detection
- Cross-platform Docker support
- Automated truth-table verification

## Installation

### Docker

```bash
git clone https://github.com/alawein/maglogic.git
cd maglogic
docker compose up --build
```

### Local

```bash
conda env create -f environment.yml
conda activate maglogic
pip install -e ".[dev]"
python scripts/validate-structure.py
PYTHONPATH=python python -c "import maglogic"
```

## Quick Usage

```bash
PYTHONPATH=python python examples/demo_truth_table.py
```

```python
from maglogic.demos import demo_nand_nor
result = demo_nand_nor.generate_truth_table()
print(result["truth_table"])
```

## Layout Model

MagLogic intentionally uses a **language-boundary layout**:

- `python/maglogic/` is the canonical Python package
- `python/tests/` is the canonical Python test surface
- `oommf/` and `mumax3/` hold simulation assets and reference inputs
- `matlab/` holds MATLAB reference implementations
- `docs/` holds repo-local documentation
- `scripts/` holds repo-local validation and maintenance helpers

This repo does **not** use `src/<package>` as its Python boundary.

See [docs/architecture/STRUCTURE_DECISION.md](docs/architecture/STRUCTURE_DECISION.md)
for the explicit structure decision.

## Roadmap

- **Near term:** modernize OOMMF/MuMax3 docker images, add reproducible seeds for demos.
- **Mid term:** expand majority-gate library and energy landscape visualizations.
- **Future:** add JAX-backed differentiable differentiable simulators and more CA examples.

## Usage

```python
from maglogic.demos import demo_nand_nor

# NAND mode (clock = +60 degrees)
result_nand = demo_nand_nor.run_simulation(clock_angle=60, input_A=1, input_B=1)
print(f"NAND(1,1) = {result_nand['logic_output']}")

# Generate a complete truth table
truth_table = demo_nand_nor.generate_truth_table()
```

## Project Structure

```text
maglogic/
├── python/
│   ├── maglogic/       # Canonical Python package
│   └── tests/          # Python test suite
├── matlab/             # MATLAB reference implementations
├── oommf/              # OOMMF simulation files
├── mumax3/             # MuMax3 simulation files
├── examples/           # Demo scripts and notebooks
├── docker/             # Docker configuration
├── docs/               # Documentation
│   └── architecture/   # Structure decisions
└── scripts/            # Repo-local validation and maintenance helpers
```

## Validation

```bash
python scripts/validate-structure.py
PYTHONPATH=python python -c "import maglogic"
```

Representative tests, when dependencies are installed:

```bash
PYTHONPATH=python python -m pytest -s python/tests/test_constants.py python/tests/test_analysis.py
```

## Documentation

- [docs/README.md](docs/README.md)
- [docs/api.md](docs/api.md)
- [docs/theory.md](docs/theory.md)
- [docs/architecture/STRUCTURE_DECISION.md](docs/architecture/STRUCTURE_DECISION.md)

## Citation

```bibtex
@article{alawein2019multistate,
  title={Multistate nanomagnetic logic using equilateral permalloy triangles},
  author={Alawein, Meshal and others},
  journal={IEEE Magnetics Letters},
  volume={10},
  pages={1--5},
  year={2019},
  doi={10.1109/LMAG.2019.2912398}
}
```

## License

MIT License. See [LICENSE](LICENSE).

## Ownership

- **Maintainer:** @alawein
- **Support:** [GitHub Issues](https://github.com/alawein/maglogic/issues)
