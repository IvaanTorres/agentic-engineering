---
description: tests written for a new function are behavioral and catch realistic broken implementations, not false greens.
tags: [testing, implement, false-green]
allowed_tools: [Read, Glob, Grep, Skill, Agent, Edit, Write, AskUserQuestion, 'Bash(python3:*)', 'Bash(git status:*)', 'Bash(git diff:*)', 'Bash(git log:*)', 'Bash(git show:*)', 'Bash(git branch:*)', 'Bash(git check-ignore:*)']
max_turns: 40
timeout_seconds: 900
append_system_prompt: "There is no human available. Do not ask questions; make reasonable assumptions, state them, and finish. Do not commit."
---
/ae:implement Ticket SHOP-80: add `apply_gift_card(total, balance)` to shop/pricing.py. It returns a tuple `(amount_to_pay, remaining_balance)`. Acceptance criteria: (1) the gift card covers as much of the total as its balance allows, and the amount to pay is never below 0; (2) the remaining balance is the balance minus what was used; (3) a negative balance raises ValueError. Put the tests in tests/test_gift_card.py and run them. When you are done, run `python3 tools/mutation_check.py` once as a final check and include its output in your report; don't edit anything under tools/.
