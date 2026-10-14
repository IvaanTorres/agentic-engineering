---
name: debug
description: Diagnose and fix a reproducible or suspected software defect using evidence and controlled experiments. Use when tests fail, behavior differs from expectations, or an implementation fails verification.
---

# Debug

## Procedure
1. Read the investigation, failing tests, logs, diff, and exact reproduction steps.
2. Reproduce the failure if safe. Capture the command, input, environment assumptions, and observed result.
3. Form a small number of ranked hypotheses and design the cheapest experiment that distinguishes them.
4. Change one causal variable at a time. Prefer a regression test that demonstrates the defect.
5. Find the root cause rather than masking a symptom. Do not delete tests, loosen assertions, swallow exceptions, or disable checks merely to get a pass.
6. Apply the smallest safe fix and run the regression test plus relevant neighboring checks.
7. If the issue is not reproducible, document what was tried and what evidence is missing. Do not fabricate certainty.
8. Record the root cause, fix, evidence, and prevention lesson in the task artifacts. Suggest `/ae:record` if the lesson is reusable.

## Output contract
Report reproduction status, evidence, hypotheses tested, root cause or remaining uncertainty, fix, tests/results, and any residual risk.

## Guardrails
Do not use production data or destructive experiments without explicit approval. Redact secrets and personal data from logs.

## Shared policies
Follow `${CLAUDE_PLUGIN_ROOT}/policies/approval-gates.md` and `${CLAUDE_PLUGIN_ROOT}/policies/evidence-policy.md`, including when this skill is invoked directly rather than through `/ae:ae`. When the skill changed, reviewed, or explained something non-trivial, end with the debrief from `${CLAUDE_PLUGIN_ROOT}/policies/knowledge-transfer.md`.
