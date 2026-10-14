---
name: pr-feedback
description: Triage and resolve review comments or CI feedback on a pull request. Use after a reviewer requests changes or CI fails.
---

# Resolve PR Feedback

1. Read the exact review comments, CI failure, PR diff, and current working tree. Map each item to a concrete requested outcome.
2. Classify each as valid defect, valid suggestion, question, disagreement, duplicate, or already resolved. Do not dismiss or apply feedback blindly.
3. For valid changes, implement the smallest correction, preserving unrelated work. Ask the user before material scope or behavior changes.
4. Add/update tests where appropriate; run the narrowest relevant checks, then broader checks based on risk.
5. Re-check each comment against the resulting diff and provide a response draft with evidence. Do not post replies, push commits, or force-push unless explicitly authorized.
6. If CI is flaky/environmental, report evidence and do not alter code to fake green status. If feedback conflicts, surface the tradeoff and ask.

## Output contract
Comment/CI item; disposition and rationale; files changed; checks/results; response draft; remaining blockers; external actions still requiring approval.
