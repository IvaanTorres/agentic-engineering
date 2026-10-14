# Contextual expert mode in `/ae`

`/ae` is the single user-facing entry point. Before routing a task, it infers the relevant engineering discipline from the task and repository evidence. It then uses that discipline's quality bar to decide what to inspect, what trade-offs to consider, and which checks matter.

## Persistent task context

The expert lens is not a disposable label chosen at routing time. For non-trivial work, `/ae` establishes a compact context capsule containing the objective, primary/secondary lenses, repository conventions, quality bar, acceptance criteria, decisions, evidence, open risks, and next action. This frame follows the task through specialist skills and all lifecycle stages. A handoff should inherit it; a resume must reconcile it with the actual repository and fresh evidence. Reclassify only when the facts or user goal materially change. See `../policies/context-and-persona-continuity.md` for the contract and template.

## Examples

- `/ae Improve the mobile navigation menu` → frontend/UI lens: accessibility, responsive states, keyboard behavior, loading/error states, and UI regression tests.
- `/ae Add a rate-limited endpoint for exporting invoices` → backend/API lens with security and data-consistency secondary lenses: authorization, validation, limits, idempotency, auditability, and failure cases.
- `/ae Design a multi-agent research workflow` → architecture + AI systems lenses: task decomposition, evals, tool permissions, prompt injection boundaries, traceability, failure recovery, latency/cost, and human escalation.
- `/ae Add an online schema migration` → database/platform lens: expand-contract compatibility, locks, backfill strategy, rollback, and explicit approval for destructive steps.

## Behavior rules

1. Infer from code and project instructions, not just wording.
2. Select one primary lens; add secondary lenses only when relevant.
3. Use project conventions before generic preferences.
4. Ask a focused question only if ambiguity materially changes design, risk, or acceptance criteria.
5. Preserve the standard workflow, evidence, and approval gates.
6. State checks as passed only when they actually ran.
7. The lens is an operating mode, not a claim of human credentials.

## Limitation

This is instruction-level orchestration. It guides Claude Code's reasoning and routing but cannot guarantee perfect classification or execution. For higher assurance, add repository-specific eval cases and deterministic checks for critical requirements.
