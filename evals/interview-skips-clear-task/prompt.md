---
description: should-not-trigger case. A small, fully specified, low-risk feature is implemented without an interview, so the interview doesn't over-trigger.
tags: [interview, over-trigger]
allowed_tools: [Read, Glob, Grep, Skill, Agent, Edit, Write, AskUserQuestion, 'Bash(python3:*)', 'Bash(git status:*)', 'Bash(git diff:*)', 'Bash(git log:*)', 'Bash(git show:*)', 'Bash(git branch:*)', 'Bash(git check-ignore:*)']
max_turns: 40
timeout_seconds: 600
---
/ae Ticket SHOP-91: add `format_price(amount: float) -> str` to shop/pricing.py for receipts. Acceptance criteria: (1) `format_price(12.5)` returns "€12.50"; (2) `format_price(0)` returns "€0.00"; (3) `format_price(1234.5)` returns "€1234.50" (no thousands separator); (4) a negative amount raises ValueError. Implement it with tests and run them. Don't commit.
