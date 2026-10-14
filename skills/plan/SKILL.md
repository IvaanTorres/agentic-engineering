---
name: plan
description: Create a bounded, testable implementation plan for a feature, bug fix, refactor, or technical change. Use after requirements and relevant code have been investigated, especially for multi-file or risky work.
---

# Plan

## Goal
Create a plan that another execution pass can follow without re-discovering the task.

## Procedure
1. Read the request, project instructions, relevant investigation, current git status, and existing plans.
2. State the problem, intended outcome, explicit non-goals, assumptions, and acceptance criteria, taken from the ticket when there is one (`${CLAUDE_PLUGIN_ROOT}/policies/team-workflow.md`).
3. Identify affected files/components, interfaces, data changes, dependencies, and migration/compatibility needs.
4. Break work into small, ordered tasks. Mark dependencies and identify tasks that are genuinely independent. If the change is too big for one reviewable PR, group tasks into PR-sized slices that each ship on their own, behind a feature flag when behavior is incomplete.
5. For each task specify: intended change, files/area, the tests it needs per `${CLAUDE_PLUGIN_ROOT}/policies/testing.md` (or why none), and completion evidence.
6. Include failure modes, security/privacy implications, observability, and rollback considerations where relevant.
7. Prefer existing libraries and project patterns. Explain any new dependency or architectural abstraction.
8. Identify decisions that need user input. Never assume approval for a risky action.
9. If a task record exists, save to `.agentic/tasks/<task-id>/plan.md` using `${CLAUDE_PLUGIN_ROOT}/templates/plan.md`, and check it with `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/validate_artifact.py .agentic/tasks/<task-id>/plan.md`.
10. For high or critical risk, add a threat model (`${CLAUDE_PLUGIN_ROOT}/templates/threat-model.md`) and a test strategy (`${CLAUDE_PLUGIN_ROOT}/templates/test-strategy.md`) next to the plan.

11. **Second look (medium risk and above):** before implementation starts, run the `ae:reviewer` subagent in plan-review mode. Give it the plan, the acceptance criteria, the relevant findings from exploration, and the primary expert lens with its checklist line from `${CLAUDE_PLUGIN_ROOT}/policies/lifecycle.md`. Fix the plan for every valid point, and show the user the critique with what you changed and what you deliberately left out.

## Output contract
A plan must include:
- objective and non-goals;
- acceptance criteria that can be checked;
- ordered tasks and dependencies;
- test/verification strategy;
- risk and rollback notes;
- explicit approval gates;
- unresolved questions and assumptions;
- for medium risk and above, the reviewer's critique and how the plan changed.

## Quality bar
The plan must be proportional to the task. A one-line configuration change does not need a multi-phase project plan. Avoid vague steps such as "implement backend"; name the behavior and evidence required.

## Shared policies
Follow `${CLAUDE_PLUGIN_ROOT}/policies/approval-gates.md` and `${CLAUDE_PLUGIN_ROOT}/policies/evidence-policy.md`, including when this skill is invoked directly rather than through `/ae:ae`. When the skill changed, reviewed, or explained something non-trivial, end with the debrief from `${CLAUDE_PLUGIN_ROOT}/policies/knowledge-transfer.md`, unless another skill invoked this one; then the outermost skill gives the single debrief. If you were invoked directly rather than through `/ae:ae` or another skill, and the work is non-trivial, first pick the expert lens and working frame from `${CLAUDE_PLUGIN_ROOT}/policies/lifecycle.md` and apply that lens's checklist throughout.
