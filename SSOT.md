---
type: normative
authority: canonical
audience: [ai-agents, contributors]
last-verified: 2026-03-09
---

# SSOT — maglogic

**Status:** Active research

## Purpose

MagLogic is the canonical nanomagnetic logic simulation suite for the Alawein
2019 IEEE Magnetics Letters workflow and follow-on analysis.

## Current State

- Python research library: active
- MATLAB reference surface: active
- OOMMF and MuMax3 assets: active
- Docker and environment setup: active

## Canonical Layout

MagLogic uses a language-boundary repo layout.

| Surface | Role |
|---------|------|
| `python/maglogic/` | Canonical Python package |
| `python/tests/` | Canonical Python test surface |
| `matlab/` | MATLAB reference implementations |
| `oommf/` | OOMMF simulation inputs and assets |
| `mumax3/` | MuMax3 simulation inputs and assets |
| `examples/` | Demo and exploratory usage |
| `docker/` | Containerization surface |
| `docs/` | Repo-local documentation |
| `scripts/` | Repo-local validation and maintenance helpers |

This repository does **not** use `src/` as its Python package boundary.

See [docs/architecture/STRUCTURE_DECISION.md](docs/architecture/STRUCTURE_DECISION.md)
for the explicit structure decision.

## Governance Documents

| Document | Purpose |
|----------|---------|
| [AGENTS.md](AGENTS.md) | Root contributor and agent rules |
| [CLAUDE.md](CLAUDE.md) | Repo-specific engineering guidance |
| [README.md](README.md) | User-facing overview and usage |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contribution workflow |

See [CLAUDE.md](CLAUDE.md) | [AGENTS.md](AGENTS.md)
