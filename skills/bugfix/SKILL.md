---
name: bugfix
description: Run an evidence-led bug-fix workflow: investigate, reproduce, debug, implement a regression test, verify, and review. Use when correcting incorrect or unstable behavior.
---

# Bug Fix Workflow

1. Use `/ae:investigate` to map the failure and relevant code.
2. Reproduce the issue or state explicitly why it cannot be reproduced.
3. Use `/ae:debug` to test hypotheses and identify root cause.
4. Implement the smallest fix and add a regression test where practical.
5. Use `/ae:verify` to run the regression test and relevant neighboring checks.
6. Use `/ae:review` to inspect the diff for side effects and whether the test actually protects the behavior.
7. Use `/ae:document-solution` if the root cause or prevention lesson is likely to recur.
8. Report root cause, fix, evidence, and remaining uncertainty. Do not deploy without a separate approved release workflow.

## Shared policies
Follow `${CLAUDE_PLUGIN_ROOT}/policies/approval-gates.md` and `${CLAUDE_PLUGIN_ROOT}/policies/evidence-policy.md`, including when this skill is invoked directly rather than through `/ae:ae`.
