---
name: verify
description: Independently verify that a code change meets acceptance criteria and has adequate test evidence. Use after implementation, before review or completion, and after a bug fix.
---

# Verify

## Procedure
1. Read acceptance criteria, plan, execution log, and current diff.
2. Inspect project scripts and documentation to identify the correct test, lint, typecheck, build, and integration commands. Do not guess command names when the repository can tell you.
3. Run the narrowest meaningful checks first, then broader checks proportionate to risk.
4. Inspect exit codes and relevant output. A command being started is not evidence of passing.
5. Map every acceptance criterion (from the ticket when there is one) to evidence: test name/output, build result, manual observation, or an explicit gap.
6. Check test adequacy against `${CLAUDE_PLUGIN_ROOT}/policies/testing.md`: required tests present, tests that would fail without the change, edge cases and failure paths covered. Also check for regressions, accidental file changes, flaky or environment-dependent results, missing migrations, and the team's definition of done (`${CLAUDE_PLUGIN_ROOT}/policies/team-workflow.md`).
7. If checks fail, report the failure and route to `/ae:debug` or `/ae:implement`. Do not approve completion while required checks are failing or unknown.
8. Write `.agentic/tasks/<task-id>/verification.md` using `${CLAUDE_PLUGIN_ROOT}/templates/verification.md`, then check its structure with `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/validate_artifact.py .agentic/tasks/<task-id>/verification.md`.
9. For medium-or-higher risk tasks, also get an independent verdict from the `ae:verification-auditor` subagent and record it. It supplements your own checks; it does not replace them.

## Output contract
Return PASS / FAIL / BLOCKED per criterion; commands and outcomes; coverage gaps; environmental limitations; residual risks; and the next action.

## Guardrails
- Never change implementation merely to make verification look successful.
- Do not claim full correctness from unit tests alone.
- Do not access production or perform destructive actions to verify a change.

## Evidence freshness
For tasks with a manifest, validate it before reporting:
`python3 ${CLAUDE_PLUGIN_ROOT}/scripts/task_state.py validate .agentic/tasks/<task-id>/task.json --check-freshness`.
A stale-head result is a signal to reassess and rerun relevant checks, not proof that every check is stale or fresh. Confirm evidence covers the files/configuration under review. Record exact command, exit code, environment, timestamp, result, summary, and commit SHA. If a manifest is absent for a small task, include the same evidence fields in the final summary.

## Shared policies
Follow `${CLAUDE_PLUGIN_ROOT}/policies/approval-gates.md` and `${CLAUDE_PLUGIN_ROOT}/policies/evidence-policy.md`, including when this skill is invoked directly rather than through `/ae:ae`. When the skill changed, reviewed, or explained something non-trivial, end with the debrief from `${CLAUDE_PLUGIN_ROOT}/policies/knowledge-transfer.md`.
