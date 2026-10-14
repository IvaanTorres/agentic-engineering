---
name: record
description: Record a verified engineering solution, architectural decision, or recurring failure pattern so future work can reuse it. Use after a nontrivial fix, surprising discovery, or repeated project-specific issue.
---

# Record

## Procedure
1. Confirm the lesson is supported by evidence and likely to be useful again.
2. Prefer updating an existing source of truth over creating duplicate documentation.
3. Record the symptom/context, root cause, resolution, verification evidence, and prevention guidance.
4. Separate general rules from one-off details. Include relevant file paths and commands but never secrets or sensitive logs.
5. For architectural choices, use `${CLAUDE_PLUGIN_ROOT}/templates/decision-record.md` (context, decision, alternatives, consequences).
6. Keep the entry concise, searchable, and dated where useful.
7. Ask before changing widely used policy or automatically applying a new rule across the codebase.

## Output contract
State what was recorded, where it was recorded, evidence supporting it, and when the lesson should be reused.

## Guardrails
Do not record speculative explanations as facts. Do not preserve tokens, credentials, personal data, or unredacted production data.

## Shared policies
Follow `${CLAUDE_PLUGIN_ROOT}/policies/approval-gates.md` and `${CLAUDE_PLUGIN_ROOT}/policies/evidence-policy.md`, including when this skill is invoked directly rather than through `/ae:ae`. When the skill changed, reviewed, or explained something non-trivial, end with the debrief from `${CLAUDE_PLUGIN_ROOT}/policies/knowledge-transfer.md`.
