---
description: ship on the user's own uncommitted change walks them through it and asks diff-specific questions before committing or pushing.
tags: [ship, challenge, knowledge-transfer]
allowed_tools: [Read, Glob, Grep, Skill, Agent, Edit, Write, 'Bash(python3:*)', 'Bash(git status:*)', 'Bash(git diff:*)', 'Bash(git log:*)', 'Bash(git show:*)', 'Bash(git branch:*)', 'Bash(git check-ignore:*)', 'Bash(git stash:*)']
max_turns: 30
timeout_seconds: 600
---
/ae:ship SHOP-42

Note: `git` cannot run in this sandbox. My uncommitted diff against the last commit is saved in CHANGE.diff (an untracked helper file, not part of the change).
