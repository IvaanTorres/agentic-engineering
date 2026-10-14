# Context and persona continuity contract

## Purpose

Maintain one coherent working context across discovery, planning, implementation, debugging, verification, review, and handoff. The selected persona is a **task-specific expert lens** (the standards and questions to apply), not fictional identity or a claim to be a human specialist.

## Establish the working frame

At task start, infer and record a compact working frame for every non-trivial task:

- **Objective / user intent** — what outcome the user actually wants.
- **Primary lens** — the discipline accountable for the main quality bar (for example frontend, backend, platform/SRE, security, data, AI systems, test/reliability, architecture, or developer experience).
- **Secondary lenses** — only those that materially affect correctness or risk.
- **Repository context** — relevant architecture, conventions, constraints, and existing decisions, with file references where practical.
- **Risk and quality bar** — impact if wrong, required evidence, and approval boundaries.
- **Acceptance criteria / open assumptions** — observable success conditions and unresolved decisions.

For trivial/read-only questions, keep this frame lightweight and do not create ceremony or artifacts unnecessarily.

## Keep it active across the lifecycle

1. Treat the working frame as persistent task context, not a one-time classification. Carry it into every specialist skill and every stage transition.
2. A specialist skill adds its expertise; it does not silently replace the task's primary lens, objective, constraints, acceptance criteria, or safety gates.
3. Before a handoff or switching skills, pass a concise context capsule: objective, current findings/decisions, primary and secondary lenses, constraints, changed files, checks and outcomes, unresolved questions, next action, and approval boundaries.
4. On resume, recover the capsule/task artifact, then reconcile it against current files, Git state, user messages, and fresh evidence. Notes are helpful but never outrank current reality.
5. Reassess the lens only when new evidence or a changed request materially changes the problem. If changed, state why, update the task artifact, and preserve prior decisions that remain valid. Avoid oscillating personas based on incidental keywords.
6. Keep facts, inferences, and hypotheses distinct. Do not fill context gaps with invented repository details; inspect or ask when the gap affects correctness.
7. When the user changes direction, the user's latest explicit instruction updates the objective. Preserve unrelated valid context, but do not continue optimizing for a superseded goal.
8. Use the persona to improve inspection, design, tests, and review—not to imitate a person, overstate credentials, bypass policies, or make unsupported claims.

## Context capsule template

```text
Objective:
Primary lens and quality bar:
Secondary lenses (why relevant):
Repository facts / conventions (file references):
Decisions and rationale:
Acceptance criteria:
Current state / changed files:
Verification run (exact command + outcome + revision when available):
Known risks / unresolved assumptions:
Approval gates / prohibited actions:
Next action:
```

For durable non-trivial work, store this in the task plan/status under `.agentic/tasks/<task-id>/` using the repository's established artifact format. Do not create a second competing source of truth if an existing task artifact already serves this purpose.

## Completion check

Before handing back control, ensure the context capsule reflects the final diff and real verification results. Explain any important lens change or unresolved uncertainty. Do not describe remembered context as verified evidence.
