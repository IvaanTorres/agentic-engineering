---
type: llm
focus: { source: file, path: tests/test_checkout.py }
---
PASS if the tests check outcomes for each of the four acceptance criteria: the returned order's status, total and payment id, what the repository holds afterwards, how many charges and refunds the payment double recorded (or equivalent), and that the save error is raised. Using a fake or stub gateway, or a mock whose calls are checked alongside those outcomes, is fine.
FAIL if any acceptance criterion is checked only through mock calls (for example `charge.assert_called_once()`) with no check of the returned order or the stored state, or if an acceptance criterion has no test.
