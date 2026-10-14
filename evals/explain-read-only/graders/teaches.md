---
type: llm
---
PASS if the final message explains apply_discount with reference to shop/pricing.py, traces at least one concrete call (for example apply_discount(100, 0.9) returning 50), points out that negative discounts are not rejected and increase the total, and separates what the code shows from inference.
FAIL if it misses the negative-discount problem, invents behavior not in the code, or modifies files.
