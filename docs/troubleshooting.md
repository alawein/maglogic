---
type: canonical
owner: platform-engineering
last-reviewed: 2026-03-31
---

# Troubleshooting -- maglogic

## Common Issues

**`import maglogic` fails after installation**

The Python package root is `python/maglogic/`, not the repo root. Run all
Python commands with `PYTHONPATH=python` set, or install the package in
editable mode:

```bash
pip install -e ".[dev]"
```

**`python scripts/validate-structure.py` reports missing directories**

The expected layout requires `python/maglogic/`, `python/tests/`, `oommf/`,
`mumax3/`, `matlab/`, `examples/`, `docker/`, and `docs/` to exist. If any
were accidentally removed, restore from git. The validate-structure script is
the canonical check.

**Docker build fails**

Confirm Docker Desktop is running and `docker compose` (V2 syntax) is
available. The `docker/` directory contains the environment definitions; check
that solver base images are accessible from your network.

**OOMMF or MuMax3 binary not found**

These are external solvers that are not bundled with the repo. Install them
separately, or use the Docker image which includes them. The Python package
falls back to pre-computed reference data for demo mode when solvers are
absent.

**Tests fail with `ModuleNotFoundError`**

Ensure the conda environment is active (`conda activate maglogic`) and that
the editable install completed successfully (`pip install -e ".[dev]"`). The
test suite requires `PYTHONPATH=python` or the editable install to resolve
`maglogic`.

## Diagnostic Steps

1. Confirm environment: `conda activate maglogic && python -c "import maglogic"`.
2. Run structure validation: `python scripts/validate-structure.py`.
3. Run the minimal test subset:
   `PYTHONPATH=python python -m pytest -s python/tests/test_constants.py python/tests/test_analysis.py`.
4. If using Docker, inspect compose logs: `docker compose logs`.

## Known Failure Modes

No additional failure modes are recorded at this time. If you encounter a
repeatable failure not covered above, open an issue at
<https://github.com/alawein/maglogic/issues> with the full error output, your
OS, Python version, and whether you are using Docker or a local conda
environment.
