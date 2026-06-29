---
type: canonical
last_updated: 2026-06-29
---

# Repository topology

Archetype: `python-research-package` with earned multi-language roots (fleet topology canon).

On-disk layout as of 2026-06-29. This repo does **not** use `src/<package>`; see [STRUCTURE_DECISION.md](STRUCTURE_DECISION.md).

## Tree

```text
maglogic/
├── python/
│   ├── maglogic/                # canonical Python package
│   │   ├── core/                # logic primitives, gate models
│   │   ├── simulation/          # solver orchestration helpers
│   │   ├── analysis/            # truth tables, energy landscapes
│   │   ├── visualization/       # figure and animation helpers
│   │   └── parsers/             # output parsers for OOMMF/MuMax3
│   └── tests/                   # pytest suite
├── oommf/                       # OOMMF input files (.mif) and domain assets
│   ├── basic/
│   └── triangles/
├── mumax3/                      # MuMax3 input files (.mx3) and domain assets
│   ├── basic/
│   └── triangles/
├── matlab/                      # MATLAB reference implementations
├── examples/                    # demo scripts (e.g. demo_truth_table.py)
├── docker/                      # Docker Compose reproducible environment
├── scripts/                     # validate-structure.py and maintenance helpers
├── reports/                     # exported report artifacts
└── docs/                        # theory, API, architecture decisions
```

## Surfaces

| Path | Role |
|------|------|
| `python/maglogic/` | Canonical Python package; set `PYTHONPATH=python` outside editable install |
| `python/tests/` | Python regression suite |
| `oommf/`, `mumax3/` | Micromagnetic solver inputs and reference outputs |
| `matlab/` | Reference implementations parallel to Python gate models |
| `examples/` | Runnable demos for teaching and verification |
| `docker/` | Full-stack environment for OOMMF/MuMax3 runs |

## Rules

From [STRUCTURE_DECISION.md](STRUCTURE_DECISION.md):

- Keep importable Python code under `python/maglogic/`.
- Keep Python tests under `python/tests/`.
- Do not create a parallel `src/` tree without an explicit migration plan.
- Keep OOMMF, MuMax3, and MATLAB surfaces separate and documented.

## Related docs

- [STRUCTURE_DECISION.md](STRUCTURE_DECISION.md) for the language-boundary rationale
- [architecture.md](../architecture.md) for simulation data flow
