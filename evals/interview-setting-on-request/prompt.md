---
description: with "Interviews - on-request" in CLAUDE.md, a feature goes straight to a plan with stated assumptions instead of an interview.
tags: [interview, settings]
allowed_tools: [Read, Glob, Grep, Skill, Agent, Edit, Write, AskUserQuestion, 'Bash(python3:*)', 'Bash(git status:*)', 'Bash(git diff:*)', 'Bash(git log:*)', 'Bash(git show:*)', 'Bash(git branch:*)', 'Bash(git check-ignore:*)']
max_turns: 40
timeout_seconds: 600
---
/ae:feature Ticket SHOP-61: customers can apply a fixed-amount gift card at checkout, on top of the existing percentage discount. Acceptance criteria: (1) the gift card amount is subtracted from the total. Plan it only; don't implement yet.
