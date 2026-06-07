---
type: canonical
owner: platform-engineering
last-reviewed: 2026-03-31
---

# Deployment and Release -- maglogic

MagLogic is a research library and simulation suite, not a web service or
long-running application. It is not deployed to a cloud environment. There is
no production instance, no staging environment, and no server-side rollback
procedure.

## Reproducing the Environment Locally

The primary method for running MagLogic is local reproduction, either via
Docker (recommended for solver isolation) or a conda environment.

**Docker (recommended):**

```bash
git clone https://github.com/alawein/maglogic.git
cd maglogic
docker compose up --build
```

**Conda (direct):**

```bash
conda env create -f environment.yml
conda activate maglogic
pip install -e ".[dev]"
python scripts/validate-structure.py
PYTHONPATH=python python -c "import maglogic"
```

After setup, confirm the environment is functional:

```bash
PYTHONPATH=python python -m pytest -s python/tests/test_constants.py python/tests/test_analysis.py
```

## Release Strategy

MagLogic follows research-cadence versioning. There is no automated release
pipeline. A release is a tagged commit on `main` that marks a reproducible
state of the simulation suite, typically aligned with a manuscript submission
or a significant analysis milestone.

Version numbers follow the format documented in `CHANGELOG.md`.

## Environment Configuration

No secrets or cloud credentials are required to run MagLogic. The only
environment-specific configuration is the path to OOMMF or MuMax3 binaries,
which is set via shell environment variables or Docker volume mounts as
documented in `docker/` and `environment.yml`.
