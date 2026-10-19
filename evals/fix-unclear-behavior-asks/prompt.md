---
description: a bug whose correct behavior is disputed (ticket, docs, code and tests disagree) gets a behavior-mode interview before any fix.
tags: [interview, fix, behavior]
allowed_tools: [Read, Glob, Grep, Skill, Agent, Edit, Write, AskUserQuestion, 'Bash(python3:*)', 'Bash(git status:*)', 'Bash(git diff:*)', 'Bash(git log:*)', 'Bash(git show:*)', 'Bash(git branch:*)', 'Bash(git check-ignore:*)']
max_turns: 30
timeout_seconds: 600
---
/ae:fix Ticket SHOP-70: a customer used a 90% coupon and only got 50% off. The discount cap is broken, fix it.
