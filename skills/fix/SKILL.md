---
name: fix
description: Run an evidence-led bug-fix workflow: investigate, reproduce, debug, implement a regression test, verify, and review. Use when correcting incorrect or unstable behavior.
---

# Bug Fix Workflow

1. Use `/ae:explore` to map the failure and relevant code.
2. Reproduce the issue or state explicitly why it cannot be reproduced.
3. Use `/ae:debug` to test hypotheses and identify root cause.
4. Write a regression test that fails before the fix (`${CLAUDE_PLUGIN_ROOT}/policies/testing.md`), then implement the smallest fix and show the test passing. If no test is feasible, record why.
   - **Hotfix mode** (urgent production bug): target the branch the team releases from, keep the diff minimal, note any backport, and put cleanup in a follow-up (`${CLAUDE_PLUGIN_ROOT}/policies/team-workflow.md`).
5. Use `/ae:verify` to run the regression test and relevant neighboring checks.
6. Use `/ae:review` to inspect the diff for side effects beyond the changed lines and whether the test actually protects the behavior.
7. Use `/ae:record` if the root cause or prevention lesson is likely to recur.
8. When the user wants it shipped, use `/ae:ship` to commit and open the PR.
9. Report root cause, fix, evidence, remaining uncertainty, and the debrief from `${CLAUDE_PLUGIN_ROOT}/policies/knowledge-transfer.md`. Do not deploy without a separate approved release workflow.

## Shared policies
Follow `${CLAUDE_PLUGIN_ROOT}/policies/approval-gates.md` and `${CLAUDE_PLUGIN_ROOT}/policies/evidence-policy.md`, including when this skill is invoked directly rather than through `/ae:ae`. When the skill changed, reviewed, or explained something non-trivial, end with the debrief from `${CLAUDE_PLUGIN_ROOT}/policies/knowledge-transfer.md`.
