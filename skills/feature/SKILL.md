---
name: feature
description: Run the standard end-to-end workflow for a nontrivial feature: investigate, interview the user, plan, implement in bounded tasks, verify, review, and capture useful lessons. Use for new user-facing behavior or multi-file changes.
---

# Feature Workflow

1. Read the ticket and its acceptance criteria if there is one (`${CLAUDE_PLUGIN_ROOT}/policies/team-workflow.md`). Classify risk and scope. Inspect repository instructions and existing changes.
2. Use `/ae:explore` and save the findings.
3. Use `/ae:interview` on the findings: question the user in short rounds about paths, edge cases, failures, data, permissions and rollout, explain what each answer implies, and agree the scenarios. Skip it only under the conditions that skill lists, and say why.
4. Use `/ae:plan` with the interview record; ensure acceptance criteria, PR slicing, and the test strategy (`${CLAUDE_PLUGIN_ROOT}/policies/testing.md`) are concrete.
5. Present the plan, the reviewer's critique of it, material assumptions and decisions to the user, with the options and their trade-offs for anything they should choose. Get clarification before implementation if needed.
6. Use `/ae:implement` on bounded tasks, logging decisions in the execution log. Parallelize only independent tasks with clear file ownership and integration points.
7. Do a simplification pass over the diff (see the simplify pass in `/ae:refactor`) when the implementation grew more complex than needed.
8. Use `/ae:verify`; failures route to `/ae:debug` or `/ae:implement`, then verify again. After two failed rounds, stop and report instead of looping.
9. Use `/ae:review`; address blocker/high findings and document any consciously accepted lower-severity risks.
10. Use `/ae:record` only if a durable lesson or decision emerged.
11. When the user wants it shipped, use `/ae:ship` to commit and open the PR.
12. Report changed files, acceptance criteria evidence, checks, review status, remaining risks, and the debrief from `${CLAUDE_PLUGIN_ROOT}/policies/knowledge-transfer.md`.
13. Do not deploy as part of this workflow unless the user separately requests it and `/ae:deploy` obtains the required approval.

Keep the process proportional. For trivial tasks, skip this composed workflow and use the smallest appropriate skill.

## Shared policies
Follow `${CLAUDE_PLUGIN_ROOT}/policies/approval-gates.md` and `${CLAUDE_PLUGIN_ROOT}/policies/evidence-policy.md`, including when this skill is invoked directly rather than through `/ae:ae`. When the skill changed, reviewed, or explained something non-trivial, end with the debrief from `${CLAUDE_PLUGIN_ROOT}/policies/knowledge-transfer.md`, unless another skill invoked this one; then the outermost skill gives the single debrief. If you were invoked directly rather than through `/ae:ae` or another skill, and the work is non-trivial, first pick the expert lens and working frame from `${CLAUDE_PLUGIN_ROOT}/policies/lifecycle.md` and apply that lens's checklist throughout.
