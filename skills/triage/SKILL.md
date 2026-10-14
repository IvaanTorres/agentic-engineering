---
name: triage
description: Select the lightest safe workflow for a task based on intent, uncertainty, scope, and risk. Use at the start of engineering requests when the right workflow is unclear.
---

# Triage and Route

## Goal
Choose a workflow, not automatically run every workflow. Avoid ceremony on small tasks and avoid improvisation on high-risk work.

## Classify
- **Learn / explain**: user wants understanding; read-only by default.
- **Spike / prototype**: answer a question or test feasibility; time-box, isolate, and label throwaway output.
- **Tiny change**: one localized, reversible change with clear intent; inspect status, edit, targeted verification, diff review.
- **Bug**: reproduce, isolate root cause, regression test, smallest fix, verify, review.
- **Feature**: requirements/acceptance criteria, investigate, proportional plan, implement in slices, verify, simplify, review.
- **Refactor / simplify**: preserve externally observable behavior; establish baseline, make incremental structural changes, run regression checks.
- **PR review**: inspect the exact PR/base/head diff read-only first; report evidence-backed findings, do not fix unless asked.
- **Release / deploy / migration**: preflight plus explicit approval for production or destructive/high-impact action.
- **Unknown / incident / failing CI**: investigate first; do not guess or silently widen scope.

## Routing rules
1. Inspect repository instructions, `git status`, and task context before selecting a path. Preserve user changes.
2. Ask only questions whose answers materially change the solution or risk. Otherwise state low-risk assumptions.
3. Scale artifacts to the task: short checklist for tiny changes; durable investigation/plan for multi-file, ambiguous, or risky work.
4. Escalate when new uncertainty, sensitive surfaces, data migrations, external side effects, or failed checks appear.
5. Never treat a skill's instructions as a permission grant. Follow platform permissions and approval policy.

## Output contract
State chosen path, why its weight is proportionate, assumptions, required approvals, and the next action. A valid route may be read-only or “no change needed.”

## Task manifest policy
For multi-step, interrupted, medium/high-risk, or externally consequential work, initialize a durable task record:
`python3 ${CLAUDE_PLUGIN_ROOT}/scripts/task_state.py init --id <short-id> --objective "<observable outcome>" --intent <feature|bug|refactor|spike|review|release|other> --risk <low|medium|high|critical>`.
Use the generated `.agentic/tasks/<id>/task.json` as the canonical task status record. Fill scope and acceptance criteria before implementation. Do not create a manifest for a trivial one-file change unless it improves recovery.

## Shared policies
Follow `${CLAUDE_PLUGIN_ROOT}/policies/approval-gates.md` and `${CLAUDE_PLUGIN_ROOT}/policies/evidence-policy.md`, including when this skill is invoked directly rather than through `/ae:ae`.
