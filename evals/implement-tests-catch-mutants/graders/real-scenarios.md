---
type: llm
focus: { source: file, path: tests/test_gift_card.py }
---
PASS if every test checks a concrete scenario with exact expected values for both elements of the returned tuple (or the raised ValueError), the expected values are literal numbers worked out from the requirement rather than computed by calling apply_gift_card or copying its logic, and together the tests cover a card smaller than the total, a card larger than the total, and a negative balance.
FAIL if any test only checks types, truthiness or that no error is raised, computes its expected value with the code under test, or if one of those three scenarios is missing.
