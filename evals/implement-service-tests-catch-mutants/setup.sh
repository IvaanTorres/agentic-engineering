#!/usr/bin/env bash
set -euo pipefail
mkdir -p shop tests
cat > shop/__init__.py <<'EOF'
EOF
cat > tests/__init__.py <<'EOF'
EOF
cat > shop/pricing.py <<'EOF'
"""Order pricing."""

MAX_DISCOUNT = 0.5


def apply_discount(subtotal: float, discount: float) -> float:
    """Return the total after applying a fractional discount, capped at MAX_DISCOUNT."""
    if subtotal < 0:
        raise ValueError("subtotal must be non-negative")
    if discount > MAX_DISCOUNT:
        discount = MAX_DISCOUNT
    return round(subtotal * (1 - discount), 2)
EOF
cat > tests/test_pricing.py <<'EOF'
import unittest

from shop.pricing import apply_discount


class ApplyDiscountTests(unittest.TestCase):
    def test_applies_discount(self):
        self.assertEqual(apply_discount(100, 0.2), 80)

    def test_caps_discount(self):
        self.assertEqual(apply_discount(100, 0.9), 50)
EOF
cat > CLAUDE.md <<'EOF'
# Shop

Run tests with `python3 -m unittest discover -s tests -t .`.
Commit messages follow Conventional Commits with the ticket id, e.g. `fix(SHOP-42): ...`.
EOF
printf ".agentic/\n__pycache__/\n" > .gitignore
git init -q -b main .
git add -A
git -c user.name=eval -c user.email=eval@example.invalid commit -qm "chore: initial shop pricing"


cat > shop/orders.py <<'EOF'
"""Orders and their storage."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Order:
    id: str
    total: float
    status: str  # "paid" or "declined"
    payment_id: str | None = None


class OrderRepository:
    """In-memory store; production uses the same interface over Postgres."""

    def __init__(self) -> None:
        self._orders: dict[str, Order] = {}

    def get(self, order_id: str) -> Order | None:
        return self._orders.get(order_id)

    def save(self, order: Order) -> None:
        self._orders[order.id] = order
EOF
cat > shop/payments.py <<'EOF'
"""Payment provider client."""
from __future__ import annotations

import json
import urllib.request


class PaymentDeclined(Exception):
    """The provider refused the charge."""


class HttpPaymentGateway:
    """Talks to the payment provider over HTTPS. Never call it from tests."""

    def __init__(self, base_url: str, api_key: str) -> None:
        self.base_url = base_url
        self.api_key = api_key

    def charge(self, amount: float, idempotency_key: str) -> str:
        """Charge the amount once per idempotency key and return the payment id. Raises PaymentDeclined."""
        body = self._post("/charges", {"amount": amount, "idempotency_key": idempotency_key})
        if body["status"] == "declined":
            raise PaymentDeclined(body.get("reason", ""))
        return body["payment_id"]

    def refund(self, payment_id: str) -> None:
        self._post(f"/charges/{payment_id}/refund", {})

    def _post(self, path: str, data: dict) -> dict:
        request = urllib.request.Request(
            self.base_url + path, data=json.dumps(data).encode(),
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"})
        with urllib.request.urlopen(request, timeout=10) as response:
            return json.loads(response.read())
EOF
mkdir -p tools
cat > tools/mutation_check.py <<'EOF'
"""Run the checkout tests against the real code and against realistic broken versions of it.

Writes mutation-report.txt. A mutant SURVIVED means the tests stayed green on broken code.
"""
import pathlib
import subprocess
import sys

BASE = '''
import shop.checkout as c
from shop.orders import Order
from shop.payments import PaymentDeclined
from shop.pricing import apply_discount

class Mutant:
    def __init__(self, orders, payments):
        self.orders = orders
        self.payments = payments

    def place_order(self, order_id, subtotal, discount):
        existing = self.orders.get(order_id)
        if existing is not None and IDEMPOTENT:
            return existing
        total = apply_discount(subtotal, discount) if DISCOUNTED else subtotal
        try:
            payment_id = self.payments.charge(total, idempotency_key=KEY)
        except PaymentDeclined:
            if SAVE_DECLINED:
                self.orders.save(Order(order_id, total, DECLINED_STATUS))
            return Order(order_id, total, DECLINED_STATUS)
        order = Order(order_id, total, "paid", payment_id)
        try:
            self.orders.save(order)
        except Exception:
            if REFUND:
                self.payments.refund(payment_id)
            if RERAISE:
                raise
            return None
        return order

c.CheckoutService = Mutant
'''
CORRECT = dict(IDEMPOTENT=True, DISCOUNTED=True, KEY="order_id", SAVE_DECLINED=True,
               DECLINED_STATUS='"declined"', REFUND=True, RERAISE=True)
MUTANTS = {
    "charges_undiscounted_subtotal": dict(DISCOUNTED=False),
    "charges_again_on_retry": dict(IDEMPOTENT=False),
    "idempotency_key_not_order_id": dict(KEY='"key-" + str(id(self))'),
    "declined_order_not_saved": dict(SAVE_DECLINED=False),
    "declined_marked_paid": dict(DECLINED_STATUS='"paid"'),
    "no_refund_when_save_fails": dict(REFUND=False),
    "save_failure_swallowed": dict(RERAISE=False),
}
RUN = (
    "{patch}\n"
    "import unittest\n"
    "suite = unittest.defaultTestLoader.discover('tests', pattern='test_checkout*.py', top_level_dir='.')\n"
    "r = unittest.TextTestRunner(verbosity=0).run(suite)\n"
    "raise SystemExit(0 if r.wasSuccessful() and r.testsRun else 1)\n"
)


def patch(overrides: dict) -> str:
    code = BASE
    for placeholder, value in {**CORRECT, **overrides}.items():
        code = code.replace(placeholder, str(value))
    return code


def passes(code: str) -> bool:
    return subprocess.run([sys.executable, "-c", RUN.format(patch=code)], capture_output=True).returncode == 0


lines = ["BASELINE " + ("PASS" if passes("") else "FAIL")]
lines.append("REFERENCE " + ("PASS" if passes(patch({})) else "FAIL"))
for name, overrides in MUTANTS.items():
    lines.append(f"{name} " + ("SURVIVED" if passes(patch(overrides)) else "KILLED"))
pathlib.Path("mutation-report.txt").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
EOF
git add -A && git -c user.name=eval -c user.email=eval@example.invalid commit -qm "feat: orders, payment gateway, mutation tool"
