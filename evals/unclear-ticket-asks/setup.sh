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

