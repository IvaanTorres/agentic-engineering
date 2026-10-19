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


mkdir -p tools
cat > tools/mutation_check.py <<'PY'
"""Run the gift card tests against the real code and against broken versions of it.

Writes mutation-report.txt. A mutant SURVIVED means the tests stayed green on broken code.
"""
import pathlib
import subprocess
import sys

MUTANTS = {
    "negative_amount_to_pay": "lambda t, b: (t - b, max(b - t, 0))",
    "balance_never_reduced": "lambda t, b: (max(t - b, 0), b)",
    "leftover_balance_lost": "lambda t, b: (max(t - b, 0), 0)",
    "no_negative_balance_check": "lambda t, b: (max(t - b, 0), b - (t - max(t - b, 0)))",
    "tuple_swapped": "lambda t, b: (b - (t - max(t - b, 0)), max(t - b, 0))",
}
RUN = (
    "import unittest, shop.pricing as p\n"
    "{patch}\n"
    "suite = unittest.defaultTestLoader.discover('tests', pattern='test_gift_card*.py', top_level_dir='.')\n"
    "r = unittest.TextTestRunner(verbosity=0).run(suite)\n"
    "raise SystemExit(0 if r.wasSuccessful() and r.testsRun else 1)\n"
)


def run(patch: str) -> bool:
    proc = subprocess.run([sys.executable, "-c", RUN.format(patch=patch)], capture_output=True, text=True)
    return proc.returncode == 0


lines = ["BASELINE " + ("PASS" if run("") else "FAIL")]
for name, body in MUTANTS.items():
    lines.append(f"{name} " + ("SURVIVED" if run(f"p.apply_gift_card = {body}") else "KILLED"))
pathlib.Path("mutation-report.txt").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
PY
git add -A && git -c user.name=eval -c user.email=eval@example.invalid commit -qm "chore: mutation check tool"
