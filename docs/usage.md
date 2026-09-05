---
type: canonical
source: none
sync: none
sla: none
---

# Usage Guide

## Running a Truth Table

```bash
PYTHONPATH=python python examples/run_basic_triangle.py
```

## Programmatic API

```python
from maglogic.demos.demo_nand_nor import NANDNORDemo

# Running the full demo requires a local OOMMF installation.
demo = NANDNORDemo(output_dir="nand_nor_demo")
result = demo.run_complete_demo()
print(result["nand_gate_results"])
```

## Simulation Backends

- **OOMMF**: install OOMMF locally and use configs under `oommf/`; MagLogic does not bundle or execute a solver in its analysis-only example.
- **MuMax3**: requires GPU-enabled build; samples under `mumax3/`.

## Tips

- Keep `PYTHONPATH=python` when running examples/tests.
- For Docker, copy `docker/.env.example` to `docker/.env`, set unique local credentials, then use `docker compose --env-file .env up`.
- Large simulation assets are not committed; fetch or mount as needed.
