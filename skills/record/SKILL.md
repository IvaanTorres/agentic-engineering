---
name: record
description: Record a verified engineering solution, architectural decision, product rule, or recurring failure pattern so future work can reuse it. Use after a nontrivial fix, surprising discovery, repeated project-specific issue, or an interview answer that settles a durable product rule.
---

# Record

## Procedure
1. Confirm the lesson is supported by evidence and likely to be useful again.
2. Prefer updating an existing source of truth over creating duplicate documentation.
3. Record the symptom/context, root cause, resolution, verification evidence, and prevention guidance.
4. Separate general rules from one-off details. Include relevant file paths and commands but never secrets or sensitive logs.
5. For architectural choices, use `${CLAUDE_PLUGIN_ROOT}/templates/decision-record.md` (context, decision, alternatives, consequences).
6. Keep the entry concise, searchable, and dated where useful.
   - **Product rules** (durable answers from `/ae:interview`, such as "gift cards never combine with percentage discounts"): add them to the file named by `Product rules:` in `CLAUDE.md`, or `docs/product-rules.md`. If the file doesn't exist, propose creating it from `${CLAUDE_PLUGIN_ROOT}/templates/product-rules.md` and, with approval, add the one-line `Product rules: <path>` pointer to `CLAUDE.md`. Put the rules in that file, not in `CLAUDE.md`, which loads in every session and should stay short. Record who decided and where the rule is enforced; a rule nobody decided is an assumption, not a rule.
7. Ask before changing widely used policy or automatically applying a new rule across the codebase.

## Output contract
State what was recorded, where it was recorded, evidence supporting it, and when the lesson should be reused.

## Guardrails
Do not record speculative explanations as facts. Do not preserve tokens, credentials, personal data, or unredacted production data.

## Shared policies
Follow `${CLAUDE_PLUGIN_ROOT}/policies/approval-gates.md` and `${CLAUDE_PLUGIN_ROOT}/policies/evidence-policy.md`, including when this skill is invoked directly rather than through `/ae:ae`. When the skill changed, reviewed, or explained something non-trivial, end with the debrief from `${CLAUDE_PLUGIN_ROOT}/policies/knowledge-transfer.md`, unless another skill invoked this one; then the outermost skill gives the single debrief. If you were invoked directly rather than through `/ae:ae` or another skill, and the work is non-trivial, first pick the expert lens and working frame from `${CLAUDE_PLUGIN_ROOT}/policies/lifecycle.md` and apply that lens's checklist throughout.
