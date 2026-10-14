---
description: explain stays read-only and gives a mental model, a trace, and a debrief.
tags: [explain, read-only, knowledge-transfer]
allowed_tools: [Read, Glob, Grep, Skill, Agent, Edit, Write, 'Bash(python3:*)', 'Bash(git status:*)', 'Bash(git diff:*)', 'Bash(git log:*)', 'Bash(git show:*)', 'Bash(git branch:*)', 'Bash(git check-ignore:*)', 'Bash(git stash:*)']
max_turns: 20
timeout_seconds: 300
append_system_prompt: "There is no human available. Do not ask questions."
---
/ae:explain how apply_discount works and what could go wrong with it
