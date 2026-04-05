---
type: canonical
source: none
sync: none
sla: none
---

# Usage Guide

## Running a Truth Table

```bash
PYTHONPATH=python python examples/demo_truth_table.py
```

## Programmatic API

```python
from maglogic.demos import demo_nand_nor
result = demo_nand_nor.generate_truth_table()
print(result["truth_table"])
```

## Simulation Backends

- **OOMMF**: place OOMMF binaries on PATH; use configs under `oommf/`.
- **MuMax3**: requires GPU-enabled build; samples under `mumax3/`.

## Tips

- Keep `PYTHONPATH=python` when running examples/tests.
- Use Docker (`docker compose up`) for an isolated, reproducible environment.
- Large simulation assets are not committed; fetch or mount as needed.
