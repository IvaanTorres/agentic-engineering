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


cat > shop/permissions.py <<'EOF'
"""Who may do what with an order."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class User:
    id: str
    role: str  # "customer", "support" or "admin"


@dataclass
class Order:
    id: str
    owner_id: str
    total: float


def can_refund(user: User, order: Order) -> bool:
    """Admins can refund any order; nobody else can."""
    return user.role == "admin"
EOF
cat > tests/test_permissions.py <<'EOF'
import unittest

from shop.permissions import Order, User, can_refund


class CanRefundTests(unittest.TestCase):
    def test_admin_can_refund_any_order(self):
        self.assertTrue(can_refund(User("a1", "admin"), Order("o1", "c1", 40.0)))

    def test_customer_cannot_refund_own_order(self):
        self.assertFalse(can_refund(User("c1", "customer"), Order("o1", "c1", 40.0)))
EOF
git add -A && git -c user.name=eval -c user.email=eval@example.invalid commit -qm "feat: refund permissions"
