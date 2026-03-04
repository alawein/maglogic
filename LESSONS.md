---
type: lessons
authority: observed
audience: [ai-agents, contributors, future-self]
last-updated: 2026-03-04
---

# LESSONS — MagLogic

> Observed patterns only. Minimal initial entry — update as lessons accumulate.

## Patterns That Work

- **Grounding implementations in published work**: Anchoring the simulation suite to Alawein et al. (IEEE Magnetics Letters 2019) gives a clear correctness benchmark — results should reproduce the paper's figures before extending.
- **Separating physics kernels from I/O and plotting**: Keeping the core nanomagnetic logic solvers free of visualization code makes the library easier to test and reuse in other contexts.

## Anti-Patterns

- **Mixing single-cell and multi-cell simulation logic**: Single nanomagnetic element behavior and coupled array behavior have different governing equations; conflating them in one function creates subtle correctness bugs.
- **Floating-point defaults without unit documentation**: Physical simulation parameters (field strength, damping constants) must always carry explicit units in docstrings; unit confusion is the most common source of wrong results.

## Pitfalls

- **Numerical instability at extreme parameter ranges**: LLG-based solvers diverge with large time steps or extreme field values; always validate step size convergence before running parameter sweeps.
- **Comparing results across different discretization schemes without noting it**: Finite-difference and finite-element results for the same geometry can differ; document which scheme each result uses.
