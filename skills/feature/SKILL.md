---
name: feature
description: Run the standard end-to-end workflow for a nontrivial feature: investigate, plan, implement in bounded tasks, verify, review, and capture useful lessons. Use for new user-facing behavior or multi-file changes.
---

# Feature Workflow

1. Classify risk and scope. Inspect repository instructions and existing changes.
2. Use `/ae:investigate` and save the findings.
3. Use `/ae:plan`; ensure acceptance criteria and test strategy are concrete.
4. Present material assumptions and decisions to the user. Get clarification before implementation if needed.
5. Use `/ae:execute` on bounded tasks. Parallelize only independent tasks with clear file ownership and integration points.
6. Use `/ae:verify`; failures route to `/ae:debug` or `/ae:execute`, then verify again.
7. Use `/ae:review`; address blocker/high findings and document any consciously accepted lower-severity risks.
8. Use `/ae:document-solution` only if a durable lesson or decision emerged.
9. Report changed files, acceptance criteria evidence, checks, review status, and remaining risks.
10. Do not deploy as part of this workflow unless the user separately requests it and `/ae:deploy` obtains the required approval.

Keep the process proportional. For trivial tasks, skip this composed workflow and use the smallest appropriate skill.
