---
name: refactor
description: Improve internal structure while preserving externally observable behavior. Use for restructuring, extraction, renaming, deduplication, or architectural cleanup.
---

# Refactor Safely

1. State the structural goal and explicit non-goals; identify behavior and interfaces that must remain unchanged.
2. Inspect call sites, public APIs, data contracts, persistence, concurrency, and feature flags. Check `git status` and preserve unrelated changes.
3. Establish a baseline: relevant tests, build/typecheck, representative behavior, or characterization tests. If coverage is weak, call out the risk and add characterization coverage where practical.
4. Plan small, reversible steps. Avoid combining behavior changes with structural cleanup unless explicitly requested.
5. Make one coherent change at a time and run targeted regression checks after each meaningful step.
6. Compare behavior and public interfaces before/after; inspect the full diff for accidental scope expansion.
7. Run `/ae:simplify` only if it adds value, then `/ae:verify` and `/ae:review` proportionate to risk.
8. Stop if the refactor requires an unapproved behavior, schema, public API, or migration change. Escalate rather than smuggling it in.

## Output contract
Structural goal; behavior invariants; baseline; steps; checks/results; compatibility risks; remaining debt; evidence that behavior is preserved.
