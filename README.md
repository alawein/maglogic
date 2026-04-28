# MagLogic

MagLogic is a nanomagnetic logic simulation suite built around the actual
research surfaces that matter in this domain: the Python package, OOMMF input
decks, MuMax3 input decks, and MATLAB reference implementations. The point is
not to hide the simulator boundary. The point is to make it explicit and
repeatable.

This repository follows the triangular-logic and cellular-automata work from
the 2019 IEEE Magnetics Letters paper and keeps both CPU and GPU micromagnetic
backends in scope.

## Core surfaces

- `python/maglogic/`: canonical Python package
- `python/tests/`: required Python verification
- `oommf/`: OOMMF simulation inputs and reference assets
- `mumax3/`: MuMax3 simulation inputs and reference assets
- `matlab/`: MATLAB reference implementations
- `examples/`: runnable demos and exploratory usage

## Quick start

### Local

```bash
conda env create -f environment.yml
conda activate maglogic
pip install -e ".[dev]"
python scripts/validate-structure.py
PYTHONPATH=python python -c "import maglogic"
```

### Docker

```bash
docker compose up --build
```

## CLI and Python usage

```bash
maglogic --help
maglogic-analyze --help
```

```python
from maglogic.demos import demo_nand_nor

truth_table = demo_nand_nor.generate_truth_table()
print(truth_table)
```

## Development

```bash
PYTHONPATH=python python -m pytest -s python/tests/test_constants.py python/tests/test_analysis.py
black python/
flake8 python/
ruff check python/
mypy python/maglogic/
```

## Documentation

Start with [docs/README.md](docs/README.md) for API, theory, usage, and the
structure decision that keeps `python/maglogic/` as the canonical package
boundary.
