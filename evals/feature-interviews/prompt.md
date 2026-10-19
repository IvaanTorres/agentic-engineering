---
description: a feature request is interviewed before planning, with codebase-grounded questions and recommended defaults, and no code or plan is written before the user answers.
tags: [feature, interview, knowledge-transfer]
allowed_tools: [Read, Glob, Grep, Skill, Agent, Edit, Write, AskUserQuestion, 'Bash(python3:*)', 'Bash(git status:*)', 'Bash(git diff:*)', 'Bash(git log:*)', 'Bash(git show:*)', 'Bash(git branch:*)', 'Bash(git check-ignore:*)']
max_turns: 30
timeout_seconds: 600
---
/ae:feature Ticket SHOP-60: customers can apply a fixed-amount gift card at checkout, on top of the existing percentage discount. Acceptance criteria: (1) the gift card amount is subtracted from the total.
