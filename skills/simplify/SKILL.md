---
name: simplify
description: Reduce unnecessary complexity in a proposed or existing change without altering intended behavior. Use after implementation and before final review, or when asked to simplify code.
---

# Simplify

1. Read the task intent, acceptance criteria, current diff, and tests. Identify what must not change.
2. Look for unnecessary abstractions, duplicated logic, dead code, excessive indirection, needless dependencies, broad error handling, over-configurability, and tests that duplicate rather than protect behavior.
3. Prefer deleting complexity over adding a framework. Follow local conventions and YAGNI.
4. Make only changes with a clear readability/maintenance benefit. Do not reformat unrelated files or change public behavior under the label of simplification.
5. Run targeted tests after edits. If the simplification is not obviously semantics-preserving, do not apply it without tests or explicit user agreement.
6. Report what was simplified, what was intentionally retained, and checks run. Then hand off to `/ae:verify` and `/ae:review` as appropriate.

## Output contract
Candidate complexity; changes made (or why none were warranted); behavior-preservation evidence; test results; residual tradeoffs.

## Shared policies
Follow `${CLAUDE_PLUGIN_ROOT}/policies/approval-gates.md` and `${CLAUDE_PLUGIN_ROOT}/policies/evidence-policy.md`, including when this skill is invoked directly rather than through `/ae:ae`.
