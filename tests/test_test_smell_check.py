import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / "scripts" / "test_smell_check.py"

WEAK_PY_TEST = '''import unittest
from shop.pricing import apply_gift_card


class GiftCardTests(unittest.TestCase):
    def test_returns_something(self):
        result = apply_gift_card(80, 30)
        self.assertIsNotNone(result)
'''

STRONG_PY_TEST = '''import unittest
from shop.pricing import apply_gift_card


class GiftCardTests(unittest.TestCase):
    def test_card_larger_than_total_keeps_leftover_balance(self):
        self.assertEqual(apply_gift_card(30, 50), (0, 20))

    def test_negative_balance_is_rejected(self):
        with self.assertRaises(ValueError):
            apply_gift_card(30, -5)
'''

MOCK_ONLY_PY_TEST = '''from unittest.mock import MagicMock
from shop.checkout import CheckoutService


def test_place_order_charges_card():
    payments = MagicMock()
    service = CheckoutService(MagicMock(), payments)
    service.place_order("o-1", 100, 0.2)
    payments.charge.assert_called_once()
'''


class TestSmellHookTests(unittest.TestCase):
    """Each test feeds the hook the JSON Claude Code sends after a real edit."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        (self.repo / "tests").mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def run_hook(self, payload):
        proc = subprocess.run([sys.executable, str(HOOK)], input=json.dumps(payload),
                              capture_output=True, text=True, timeout=10)
        self.assertEqual(proc.returncode, 0, "the hook must never fail or block the session")
        return json.loads(proc.stdout)["hookSpecificOutput"]["additionalContext"] if proc.stdout else None

    def write(self, relative, content):
        path = self.repo / relative
        path.write_text(content)
        return {"tool_name": "Write", "tool_input": {"file_path": str(path), "content": content}}

    def test_existence_only_assertion_is_reported_with_its_line(self):
        message = self.run_hook(self.write("tests/test_gift_card.py", WEAK_PY_TEST))
        self.assertIn("line 8: `self.assertIsNotNone(result)` asserts only that a value exists", message)

    def test_exact_outcome_assertions_produce_no_message(self):
        self.assertIsNone(self.run_hook(self.write("tests/test_gift_card.py", STRONG_PY_TEST)))

    def test_mock_call_without_any_outcome_assertion_is_reported(self):
        message = self.run_hook(self.write("tests/test_checkout.py", MOCK_ONLY_PY_TEST))
        self.assertIn("checks only that mocks were called", message)

    def test_mock_call_next_to_an_outcome_assertion_is_accepted(self):
        content = MOCK_ONLY_PY_TEST + '    assert service.orders.get("o-1").status == "paid"\n'
        self.assertIsNone(self.run_hook(self.write("tests/test_checkout.py", content)))

    def test_production_code_is_never_checked(self):
        self.assertIsNone(self.run_hook(self.write("shop_util.py", "def ok(x):\n    assert x\n")))

    def test_edit_reports_only_lines_it_added_not_older_ones(self):
        path = self.repo / "tests" / "test_gift_card.py"
        path.write_text(WEAK_PY_TEST + "\n    def test_focused(self):\n        self.assertTrue(flag)\n")
        payload = {"tool_name": "Edit", "tool_input": {
            "file_path": str(path), "old_string": "x", "new_string": "    def test_focused(self):\n        self.assertTrue(flag)"}}
        message = self.run_hook(payload)
        self.assertIn("`self.assertTrue(flag)` asserts only that a value is truthy", message)
        self.assertNotIn("assertIsNotNone", message)

    def test_focused_and_skipped_js_tests_are_reported(self):
        content = "it.only('pays with card', () => {\n  expect(pay(10)).toEqual({ status: 'paid' });\n});\n"
        message = self.run_hook(self.write("tests/checkout.test.ts", content))
        self.assertIn("line 1:", message)
        self.assertIn("skips tests or runs only some of them", message)

    def test_multiedit_swallowed_exception_on_two_lines_is_reported(self):
        path = self.repo / "tests" / "test_x.py"
        path.write_text("def test_x():\n    try:\n        run()\n    except Exception:\n        pass\n")
        payload = {"tool_name": "MultiEdit", "tool_input": {"file_path": str(path), "edits": [
            {"old_string": "a", "new_string": "    except Exception:\n        pass"}]}}
        message = self.run_hook(payload)
        self.assertIn("line 5: `except Exception: pass` swallows an exception", message)

    def test_same_line_swallowed_exception_is_reported(self):
        content = "def test_x():\n    try:\n        run()\n    except Exception: pass\n"
        message = self.run_hook(self.write("tests/test_x.py", content))
        self.assertIn("swallows an exception", message)

    def test_malformed_input_is_ignored(self):
        proc = subprocess.run([sys.executable, str(HOOK)], input="not json", capture_output=True, text=True)
        self.assertEqual((proc.returncode, proc.stdout), (0, ""))


if __name__ == "__main__":
    unittest.main()
