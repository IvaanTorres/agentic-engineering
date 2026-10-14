---
name: deploy
description: Prepare and carry out an explicitly authorized release or deployment, including preflight checks, rollout verification, and rollback readiness. Use only when a deployment is requested; production-impacting actions always require fresh explicit human approval.
disable-model-invocation: true
---

# Deploy

## Default mode
Preparation only. This skill must not deploy to production, publish a release, run a destructive migration, or change production infrastructure until the user explicitly approves the exact action after seeing the preflight summary.

## Procedure
1. Establish target environment, release/version, commit, deployment mechanism, operator permissions, and scope. If any are unclear, stop and ask.
2. Read release documentation and inspect CI status, tests, build artifacts, pending migrations, configuration changes, dependency changes, and known incidents.
3. Confirm the candidate commit and working tree. Do not deploy uncommitted or unreviewed changes unless the user explicitly requests and policy allows it.
4. Prepare a preflight report: target, exact commands/actions, expected impact, downtime/data risks, monitoring, rollback procedure (use `${CLAUDE_PLUGIN_ROOT}/templates/incident-and-rollback.md`), and who/what approves.
5. Stop and request explicit approval. Approval must identify the target and action. A generic "ship it" earlier in the conversation is insufficient if the target or action changed.
6. After approval, perform only the approved action using the repository's documented tooling. Do not bypass platform permission prompts or CI protections.
7. Verify rollout with health checks, smoke tests, logs/metrics, and the agreed success criteria.
8. If health checks fail, stop further rollout. Follow the documented rollback or mitigation plan only if that action was authorized; otherwise ask for approval.
9. Write a release record using `${CLAUDE_PLUGIN_ROOT}/templates/release-record.md`, saved as `.agentic/tasks/<task-id>/release-record.md` and checked with `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/validate_artifact.py .agentic/tasks/<task-id>/release-record.md`, with commit, environment, approver, timestamps, commands, verification results, and any incident/rollback.

## Output contract
Before approval: preflight report and a clear approval request. After authorized execution: actions performed, evidence, health status, and remaining risks.

## Guardrails
- Never print or store secrets.
- Never infer production approval from a request to implement a feature.
- Never disable required checks, bypass review, or broaden the approved scope.
- If rollback is not understood or safe, state that as a blocker before deployment.

## Deterministic control reminder
The `/ae:deploy` skill and hook prompts are defense-in-depth, not authorization mechanisms. Confirm the platform permission prompt, deployment-environment approval, protected branch/CI policy, and least-privilege identity independently. If any required control is missing, remain in preparation-only mode and report the blocker. Never treat an approval record or previous conversational approval as a reusable credential.

## Shared policies
Follow `${CLAUDE_PLUGIN_ROOT}/policies/approval-gates.md` and `${CLAUDE_PLUGIN_ROOT}/policies/evidence-policy.md`, including when this skill is invoked directly rather than through `/ae:ae`. When the skill changed, reviewed, or explained something non-trivial, end with the debrief from `${CLAUDE_PLUGIN_ROOT}/policies/knowledge-transfer.md`, unless another skill invoked this one; then the outermost skill gives the single debrief. If you were invoked directly rather than through `/ae:ae` or another skill, and the work is non-trivial, first pick the expert lens and working frame from `${CLAUDE_PLUGIN_ROOT}/policies/lifecycle.md` and apply that lens's checklist throughout.
