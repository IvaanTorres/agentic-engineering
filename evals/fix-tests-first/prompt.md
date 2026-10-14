---
description: /ae routes a bug ticket to ae:fix, writes a failing regression test first, fixes, and maps acceptance criteria.
tags: [routing, testing, fix]
allowed_tools: [Read, Glob, Grep, Skill, Agent, Edit, Write, 'Bash(python3:*)', 'Bash(git status:*)', 'Bash(git diff:*)', 'Bash(git log:*)', 'Bash(git show:*)', 'Bash(git branch:*)', 'Bash(git check-ignore:*)', 'Bash(git stash:*)']
max_turns: 40
timeout_seconds: 600
append_system_prompt: "There is no human available. Do not ask questions; finish the task. Do not commit."
---
/ae Ticket SHOP-42: Negative discounts increase the order total. apply_discount(100, -0.1) returns 110. Acceptance criteria: (1) a discount below 0 raises ValueError; (2) a discount of 0 leaves the total unchanged; (3) the existing 50% cap still applies. Fix it.
