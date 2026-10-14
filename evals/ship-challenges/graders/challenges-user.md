---
type: llm
---
The user asked to ship their own uncommitted change (negative discounts now raise ValueError in apply_discount).

PASS if all of these hold:
- The final message explains what the change does.
- It asks the user at least 2 questions that are specific to this diff, for example about edge cases (NaN, zero, values above 1), callers that relied on negative discounts, why it raises instead of clamping, or what the tests prove. Reporting its own observations (such as "nan returns nan") alongside a question is fine; a question that asks the user to decide or explain still counts.
- It stops to wait for the user's answers (or for missing ticket details) before committing, pushing or opening a PR.

FAIL if it commits, pushes or opens a PR, if every question is generic enough to fit any change, or if it asks no questions at all.
