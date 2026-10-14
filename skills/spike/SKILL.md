---
name: spike
description: Time-box a technical investigation or prototype to answer a specific feasibility or design question. Use when learning by experiment is more valuable than a full implementation plan.
---

# Spike / Prototype

1. Write the question, decision it will inform, time/effort budget, and success/failure criteria.
2. Inspect repository state and isolate experiments in a branch, worktree, temporary directory, or clearly marked files.
3. Prefer the smallest experiment that distinguishes alternatives. Avoid production credentials/data and irreversible side effects.
4. Record commands, environment assumptions, observations, and limitations; distinguish measured results from speculation.
5. Compare options against explicit criteria (correctness, complexity, integration cost, performance, security, operability).
6. End at the budget or when the decision is clear. Do not let a spike silently become production implementation.
7. Summarize recommendation, evidence, unresolved risks, and next step: discard, repeat, plan implementation, or promote a clearly scoped prototype.
8. Clean up temporary artifacts only when safe; never discard user changes. Ask before deleting valuable work or changing shared state.

## Output contract
Question; timebox; setup; experiments; results; tradeoffs; recommendation; limitations; cleanup status; implementation follow-up. Mark code as experimental and unverified unless it passes the normal verification workflow.
