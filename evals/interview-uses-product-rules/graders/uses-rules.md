---
type: llm
---
PASS if the final message (a) states as already decided, citing docs/product-rules.md or SHOP-12, that gift cards apply after percentage discounts and that the unused balance stays on the card; (b) does not ask the user to decide either of those two points again; and (c) asks 2 to 4 questions about things the rules leave open (for example several gift cards on one order, expired or zero-balance cards, refunds of a gift-card payment, who can issue cards), then waits for answers.
FAIL if it asks whether the gift card applies before or after the discount, or what happens to leftover balance, or if it asks no questions.
