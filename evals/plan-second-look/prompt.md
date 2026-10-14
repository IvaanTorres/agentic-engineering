---
description: plan for a medium-risk ticket gets an independent reviewer critique before implementation, and the plan changes because of it.
tags: [plan, reviewer, rubber-duck]
allowed_tools: [Read, Glob, Grep, Skill, Agent, Edit, Write, 'Bash(python3:*)', 'Bash(git status:*)', 'Bash(git diff:*)', 'Bash(git log:*)', 'Bash(git show:*)', 'Bash(git check-ignore:*)']
max_turns: 40
timeout_seconds: 600
append_system_prompt: "There is no human available. Do not ask questions; make reasonable assumptions, state them, and finish the plan. Do not implement anything."
---
/ae:plan Ticket SHOP-50 (medium risk): customers can stack a percentage coupon with a fixed-amount coupon at checkout. Acceptance criteria: (1) apply the percentage coupon first, then the fixed amount; (2) the total never goes below 0; (3) the existing 50% cap on percentage discounts still applies. Plan it only.
