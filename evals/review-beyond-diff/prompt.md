---
description: review looks beyond the diff and finds a caller broken by a changed function contract.
tags: [review, side-effects]
allowed_tools: [Read, Glob, Grep, Skill, Agent, Edit, Write, 'Bash(python3:*)', 'Bash(git status:*)', 'Bash(git diff:*)', 'Bash(git log:*)', 'Bash(git show:*)', 'Bash(git branch:*)', 'Bash(git check-ignore:*)', 'Bash(git stash:*)']
max_turns: 30
timeout_seconds: 600
append_system_prompt: "There is no human available. Do not ask questions; give findings directly."
---
/ae:review the uncommitted changes. Acceptance criterion: apply_discount takes the discount as a percentage (0-100) instead of a fraction.

Note: `git` cannot run in this sandbox. My uncommitted diff against the last commit is saved in CHANGE.diff (an untracked helper file, not part of the change).
