---
type: canonical
source: _devkit/templates
sync: propagated
sla: none
---

# Contributing to maglogic

Nanomagnetic logic simulation suite -- Python, MATLAB, OOMMF, MuMax3.

This project follows the [alawein org contributing standards](https://github.com/alawein/alawein/blob/main/CONTRIBUTING.md).

## Getting Started

```bash
git clone https://github.com/alawein/maglogic.git
cd maglogic
pip install -e ".[dev]"
```

## Development Workflow

1. Branch off `main` using prefix: `feat/`, `fix/`, `docs/`, `chore/`, `test/`
2. Make your changes — keep PRs focused on a single concern
3. Run `PYTHONPATH=python python -m pytest -s python/tests/` to validate your changes before committing
4. Commit using [Conventional Commits](https://www.conventionalcommits.org/) — `type(scope): subject`
5. Open a Pull Request to `main`

## Code Standards

- Python package at `python/maglogic/` (not `src/`)
- Guard heavy scientific dependencies with conditional imports
- Do not modify reference simulation assets in `oommf/` and `mumax3/`

## Pull Request Checklist

- [ ] CI passes (no failing checks)
- [ ] Tests added or updated for new functionality
- [ ] `python scripts/validate-structure.py && PYTHONPATH=python python -m pytest -s python/tests/` passes
- [ ] `CHANGELOG.md` updated under `[Unreleased]`
- [ ] No breaking changes without a version bump plan

## Reporting Issues

Open an issue on the [GitHub repository](https://github.com/alawein/maglogic/issues) with steps to reproduce and relevant context.

## License

By contributing, you agree that your contributions will be licensed under [MIT](LICENSE).
