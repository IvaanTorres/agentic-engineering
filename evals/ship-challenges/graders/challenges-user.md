---
type: llm
---
PASS if the final message explains what the uncommitted change does (rejecting negative discounts in apply_discount) and then asks the user between 2 and 6 questions that are specific to this diff (for example about edge cases such as NaN or values above 1, callers relying on negative discounts, why raise instead of clamp, or what the tests prove), and waits for answers before committing.
FAIL if it commits, pushes or opens a PR, asks only generic questions that would fit any change, or answers its own questions instead of waiting.
