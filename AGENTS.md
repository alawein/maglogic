<!-- Template: research-library v1.0.0 -->
<!-- Generated from _pkos governance templates. Do not edit the template sections -->
<!-- directly in consuming projects — update the template and re-sync instead.    -->
---
type: normative
authority: canonical
audience: [agents, contributors, maintainers]
last-verified: 2026-03-09
---

# AGENTS — maglogic

> **Status: Normative.** Do not modify without maintainer review.

This repository is governed by clear engineering and documentation standards
aligned with the **Morphism Categorical Governance Framework** principles.

## Governance Source

| Authority | Location |
|-----------|----------|
| Root governance | [AGENTS.md](AGENTS.md) (this file) |
| Contributing guide | [CONTRIBUTING.md](CONTRIBUTING.md) |
| Changelog | [CHANGELOG.md](CHANGELOG.md) |

## Repository Scope

Polyglot research suite for nanomagnetic logic simulations across Python,
MATLAB, OOMMF, and MuMax3 surfaces. The canonical Python package lives under
`python/maglogic/`, alongside domain assets and reference implementations at the
repo root. Based on Alawein et al., IEEE Magnetics Letters 2019.

## Directory Layout

| Directory | Purpose | Governance Level |
|-----------|---------|-----------------|
| `python/maglogic/` | Canonical Python package | **Primary** -- all changes require tests |
| `python/tests/` | Python test suite | **Required** -- never delete without replacement |
| `matlab/` | MATLAB reference implementations | **Primary** -- maintained parity |
| `oommf/` | OOMMF simulation inputs and assets | **Domain asset** -- do not modify casually |
| `mumax3/` | MuMax3 simulation inputs and assets | **Domain asset** -- do not modify casually |
| `examples/` | Demo scripts and exploratory usage | **Illustrative** -- must stay runnable |
| `docker/` | Container definitions | **Infrastructure** |
| `docs/` | Theory, API, development, and structure docs | **Supplementary** |
| `scripts/` | Repo-local validation and maintenance helpers | **Tooling** -- document changes |

## Invariants (Must Always Hold)

<!-- STANDARD INVARIANTS — do not remove or weaken these -->

1. **Tests pass**: All tests must pass before merging to main
2. **Lint clean**: Linter must exit 0 on the primary source directories
3. **Imports work**: The package must be importable after install
4. **No secrets**: API keys or credentials must never appear in source
5. **Reproducibility**: Experiment and benchmark results must be deterministic (fixed seeds)
6. **README accurate**: README code examples must match actual API signatures

<!-- EXTENSION SLOT: Additional Invariants
     Add project-specific invariants here.
-->
7. **Canonical package location**: Python package must remain at `python/maglogic/`, not `src/`
8. **Simulation asset integrity**: OOMMF and MuMax3 reference inputs must not be casually modified

## Agent Rules

When this repository is modified by an AI agent or automated tool:

<!-- STANDARD AGENT RULES — do not remove or weaken these -->

- **Read** `AGENTS.md` and `CONTRIBUTING.md` before making changes
- **Never** skip the test suite -- run tests before committing
- **Always** update `CHANGELOG.md` when changing public API or behavior
- **Always** keep docstrings and type hints accurate
- **Prefer** small, focused commits with conventional commit messages
- **Never** modify validated benchmark results or reference data

### Research-Specific Agent Rules

- **Data integrity**: Do not modify, rename, or delete files in immutable data
  directories (e.g., `data/`, `archive/`). Populate data directories via
  provided scripts; treat them as read-only afterward.
- **Numerical precision**: When comparing floating-point results, use tolerance-based
  comparisons. Do not tighten tolerances without verifying against known reference
  values. Document the precision requirements of any new numerical method.
- **Citation / attribution**: Update `CITATION.cff` for release-grade changes.
  Preserve author attribution in file headers. Reference the originating paper
  when implementing published algorithms.
- **Reproducibility**: All experiments, benchmarks, and simulations must be
  reproducible. Use fixed random seeds, pin dependency versions for published
  results, and record full parameter provenance for simulation outputs.

<!-- EXTENSION SLOT: Project-Specific Agent Rules
     Add rules unique to this project's domain.
-->
- Keep the canonical Python package under `python/maglogic/`
- Keep tests under `python/tests/`
- Do not introduce a parallel `src/` tree without an explicit migration decision
- Support both OOMMF and MuMax3 backends where applicable
- Do not modify simulation output or reference input assets in `oommf/` or `mumax3/` casually
- Add tests for new Python features when dependencies permit
- Use `black` for formatting, `flake8` and `ruff` for linting, and `mypy` for typing
- GPU code must include CPU fallback
- Update `CITATION.cff` for release-grade changes

## Naming Conventions

- **Modules**: `snake_case.py`
- **Classes**: `PascalCase`
- **Functions**: `snake_case`
- **Constants**: `UPPER_SNAKE_CASE`

## Commit Message Format

```
type(scope): short description

feat(python): add domain wall propagation analysis
fix(oommf): correct exchange coupling parameter
docs(readme): update simulation workflow guide
test(analysis): add magnetization curve edge case
refactor(core): extract constants to shared module
```

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `ci`, `chore`

## Dependency Policy

- **Core deps**: Keep minimal -- NumPy, SciPy, Matplotlib for Python surface
- **Optional deps**: Heavy scientific deps guarded with conditional imports
- **Dev deps**: pytest, black, flake8, ruff, mypy -- no production code may import dev deps
- **Version pins**: Minimum versions only (no upper bounds unless proven necessary)

---

*Aligned with Morphism Systems governance principles.*

See [CLAUDE.md](CLAUDE.md) | [SSOT.md](SSOT.md)
