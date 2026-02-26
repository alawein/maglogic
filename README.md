# MagLogic

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

Python tools for simulating nanomagnetic logic devices using OOMMF and MuMax3 backends. Implements nanomagnetic logic simulations from Alawein et al. (IEEE Magnetics Letters, 2019) for triangular element logic gates and cellular automata.

## Features

- Micromagnetic simulations via OOMMF and MuMax3
- Reconfigurable logic gate analysis (NAND/NOR, majority gates)
- Magnetization pattern analysis and domain structure detection
- Energy landscape calculation and topological feature detection
- Cross-platform Docker support
- Automated truth table verification

## Installation

### Docker (Recommended)
```bash
git clone https://github.com/alawein/maglogic.git
cd maglogic
docker-compose up --build
```

### Local
```bash
conda env create -f environment.yml
conda activate maglogic
pip install -e .
python examples/run_basic_triangle.py
```

## Usage

```python
from maglogic.demos import demo_nand_nor

# NAND mode (clock = +60 degrees)
result_nand = demo_nand_nor.run_simulation(clock_angle=60, input_A=1, input_B=1)
print(f"NAND(1,1) = {result_nand['logic_output']}")  # Expected: 0

# Generate complete truth table
truth_table = demo_nand_nor.generate_truth_table()
```

## Project Structure

```
maglogic/
├── python/        # Python package (core, parsers, analysis, visualization)
├── matlab/        # MATLAB implementations
├── oommf/         # OOMMF simulation files
├── mumax3/        # MuMax3 simulation files
├── examples/      # Demo scripts and notebooks
├── docker/        # Docker configuration
└── docs/          # Documentation
```

## Testing

```bash
pytest --cov=maglogic --cov-report=html
```

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

MIT License -- see [LICENSE](LICENSE).

## Author

**Meshal Alawein**
- Email: [contact@meshal.ai](mailto:contact@meshal.ai)
- GitHub: [github.com/alawein](https://github.com/alawein)
- LinkedIn: [linkedin.com/in/alawein](https://linkedin.com/in/alawein)
