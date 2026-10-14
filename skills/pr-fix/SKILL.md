---
name: pr-fix
description: Triage and resolve review comments or CI feedback on a pull request. Use after a reviewer requests changes or CI fails.
---

# Resolve PR Feedback

1. Read the exact review comments, CI failure, PR diff, and current working tree. Map each item to a concrete requested outcome.
2. Classify each as valid defect, valid suggestion, question, disagreement, duplicate, out of scope (becomes a follow-up), or already resolved. Do not dismiss or apply feedback blindly. Explain the concern behind each comment so the user understands why the reviewer raised it.
3. For valid changes, implement the smallest correction, preserving unrelated work. Ask the user before material scope or behavior changes.
4. Add or update tests per `${CLAUDE_PLUGIN_ROOT}/policies/testing.md` (a comment that exposes a bug gets a regression test); run the narrowest relevant checks, then broader checks based on risk.
5. Re-check each comment against the resulting diff and draft a reply for each with evidence. Do not post replies, push commits, force-push, or re-request review unless explicitly authorized; when approved, push and re-request review.
6. If CI is flaky/environmental, report evidence and do not alter code to fake green status. If feedback conflicts, surface the tradeoff and ask.

## Output contract
Comment/CI item; disposition and rationale; files changed; checks/results; response draft; remaining blockers; external actions still requiring approval.

## Shared policies
Follow `${CLAUDE_PLUGIN_ROOT}/policies/approval-gates.md` and `${CLAUDE_PLUGIN_ROOT}/policies/evidence-policy.md`, including when this skill is invoked directly rather than through `/ae:ae`. When the skill changed, reviewed, or explained something non-trivial, end with the debrief from `${CLAUDE_PLUGIN_ROOT}/policies/knowledge-transfer.md`.
