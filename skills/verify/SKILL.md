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
5. Map every acceptance criterion to evidence: test name/output, build result, manual observation, or an explicit gap.
6. Check for untested paths, regressions, accidental file changes, flaky/environment-dependent results, and missing migrations.
7. If checks fail, report the failure and route to `/ae:debug` or `/ae:execute`. Do not approve completion while required checks are failing or unknown.
8. Write `.agentic/tasks/<task-id>/verification.md` using the verification template.

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
