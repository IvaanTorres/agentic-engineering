---
name: refactor
description: Improve internal structure or reduce unnecessary complexity while preserving externally observable behavior. Use for restructuring, extraction, renaming, deduplication, architectural cleanup, or simplifying a change before review.
---

# Refactor Safely

1. State the structural goal and explicit non-goals; identify behavior and interfaces that must remain unchanged.
2. Inspect call sites, public APIs, data contracts, persistence, concurrency, and feature flags. Check `git status` and preserve unrelated changes.
3. Establish a baseline: relevant tests, build/typecheck, representative behavior, or characterization tests. If coverage is weak, call out the risk and add characterization coverage where practical.
4. Plan small, reversible steps. Avoid combining behavior changes with structural cleanup unless explicitly requested.
5. Make one coherent change at a time and run targeted regression checks after each meaningful step.
6. Compare behavior and public interfaces before/after; inspect the full diff for accidental scope expansion.
7. Do the simplify pass below if it adds value, then `/ae:verify` and `/ae:review` proportionate to risk.
8. Stop if the refactor requires an unapproved behavior, schema, public API, or migration change. Escalate rather than smuggling it in.

## Simplify pass
Use on its own ("simplify this change") or as the last refactor step.
1. Read the intent, acceptance criteria, current diff, and tests; identify what must not change.
2. Look for unnecessary abstractions, duplicated logic, dead code, excessive indirection, needless dependencies, broad error handling, over-configurability, and tests that duplicate rather than protect behavior.
3. Prefer deleting complexity over adding a framework. Follow local conventions and YAGNI.
4. Make only changes with a clear readability or maintenance benefit. Don't reformat unrelated files or change public behavior under the label of simplification.
5. Run targeted tests after edits. If a simplification is not obviously semantics-preserving, don't apply it without tests or explicit user agreement.
6. Report what was simplified and what was intentionally kept.

## Output contract
Structural goal; behavior invariants; baseline; steps; checks/results; compatibility risks; remaining debt; evidence that behavior is preserved; and the debrief from `${CLAUDE_PLUGIN_ROOT}/policies/knowledge-transfer.md`.

## Shared policies
Follow `${CLAUDE_PLUGIN_ROOT}/policies/approval-gates.md` and `${CLAUDE_PLUGIN_ROOT}/policies/evidence-policy.md`, including when this skill is invoked directly rather than through `/ae:ae`. When the skill changed, reviewed, or explained something non-trivial, end with the debrief from `${CLAUDE_PLUGIN_ROOT}/policies/knowledge-transfer.md`, unless another skill invoked this one; then the outermost skill gives the single debrief.
