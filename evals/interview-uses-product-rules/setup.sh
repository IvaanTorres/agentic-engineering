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


mkdir -p docs
cat > docs/product-rules.md <<'MD'
# Product rules

## Checkout

### Gift cards are applied after percentage discounts
- Why: finance books discounts before gift card redemptions.
- Decided by / date: product owner, 2026-03-02
- Source: SHOP-12
- Status: active

### A gift card never makes the amount to pay negative; the unused balance stays on the card
- Why: gift cards are stored value, not a discount.
- Decided by / date: product owner, 2026-03-02
- Source: SHOP-12
- Status: active
MD
cat >> CLAUDE.md <<'MD'

## Interviews
- Interviews: always
- Product rules: docs/product-rules.md
MD
git add -A && git -c user.name=eval -c user.email=eval@example.invalid commit -qm "docs: product rules"
