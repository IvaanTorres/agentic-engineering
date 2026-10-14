---
type: llm
---
PASS if the final message reports, as a finding of Medium severity or higher, that shop/checkout.py (checkout_total) still divides the coupon by 100 before calling apply_discount, so after this change a 20% coupon only takes 0.2% off; and notes that no test covers checkout_total.
FAIL if the checkout.py caller is not identified as broken.
