---
description: capability eval. Tests for a service with a repository and an HTTP payment gateway must catch realistic broken versions (double charge on retry, no refund, wrong status), which tests that only check mock calls miss.
tags: [testing, implement, false-green, capability]
allowed_tools: [Read, Glob, Grep, Skill, Agent, Edit, Write, 'Bash(python3:*)', 'Bash(git status:*)', 'Bash(git diff:*)', 'Bash(git log:*)', 'Bash(git show:*)']
max_turns: 50
timeout_seconds: 900
append_system_prompt: "There is no human available. Do not ask questions; make reasonable assumptions, state them, and finish. Do not commit."
---
/ae:implement Ticket SHOP-81: add `CheckoutService(orders, payments)` in shop/checkout.py with `place_order(order_id, subtotal, discount) -> Order`. `orders` is an `OrderRepository` (shop/orders.py) and `payments` is a payment gateway like `HttpPaymentGateway` (shop/payments.py). Acceptance criteria: (1) it charges the discounted total from `apply_discount`, using the order id as the idempotency key, and saves the order as "paid" with the payment id; (2) placing an order id that already exists returns the stored order without charging again; (3) if the charge is declined, the order is saved and returned with status "declined" and no payment id, and no exception is raised; (4) if saving a paid order fails, the payment is refunded and the error is raised. Put the tests in tests/test_checkout.py and run them. When you are done, run `python3 tools/mutation_check.py` once as a final check and include its output in your report; don't edit or read anything under tools/.
