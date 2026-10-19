---
type: llm
---
PASS if the final message interviews the user before planning: it asks 2 to 4 questions (in prose or with a question tool) specific to this feature and this code (for example the order of the gift card and the 50% percentage cap in `shop/pricing.py`, a gift card larger than the total, leftover balance, a zero or negative amount, rounding), offers options or a recommended default for at least some of them, and stops to wait for answers without answering its own questions.
FAIL if it writes an implementation plan or code first, asks only generic questions that would fit any feature, or answers its own questions.
