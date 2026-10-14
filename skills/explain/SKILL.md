---
name: explain
description: Explain and teach, read-only. Explains unfamiliar code, architecture, errors, libraries or concepts; walks through a pull request or branch as a story of decisions; or reconstructs what an agent did in a task. Use when the user wants to understand, learn from, or get a knowledge transfer on code or a change.
argument-hint: <code, concept, PR/branch, or task id>
---

# Explain and Learn

Read-only by default. Do not modify files unless explicitly asked; if the user wants changes, route through `/ae:ae`.

## Pick the mode
- **Code or concept**: how something works today.
- **Change (PR or branch)**: what a change does, how it evolved, and why.
- **Agent task**: what an agent did in a task under `.agentic/tasks/<task-id>/` or in a recent session's changes, and whether it holds up.

Clarify the question and desired depth only when it is genuinely ambiguous.

## Code or concept
1. Ground the explanation in repository evidence: paths, symbols, tests, configuration, call flow. Use external documentation when behavior is version-sensitive or the user asks.
2. Give the mental model first, then trace one concrete example through the code.

## Change (PR or branch)
1. Identify the change exactly: PR number or branch, base and head SHAs, and whether local refs are up to date. Use `gh pr view`/`gh pr diff` when it is a PR. Do not check out or modify anything without asking.
2. Read the description, linked issue and acceptance criteria, commit history, review threads, and CI status when available.
3. Map the diff by layer (for example backend, frontend, config, tests, docs) and find the entry points.
4. Tell the story: the initial approach, then what changed in later commits and why. Fix, refactor, and review-driven commits usually reveal decisions and problems that were hit; call those out.
5. Trace one concrete request or user flow end to end through the new code.
6. Offer to challenge the user on the change (`${CLAUDE_PLUGIN_ROOT}/policies/challenge.md`) so they can check their understanding; do it by default when they are about to review, approve, or take over the change.

## Agent task
1. Read the task artifacts (`task.json`, `plan.md`, `execution-log.md`, `verification.md`, `review.md`) and the actual diff. Treat artifacts as claims; check them against the repository and Git state.
2. Compare what was planned with what was done: deviations, decisions taken along the way, checks actually run versus claimed, and anything skipped.
3. Point out where the agent made a judgment call the user should agree with, and where evidence is thin.

## Always
- Separate what the code or evidence proves from inference, convention, and unknowns. Cite file paths, commits, or sources for key claims.
- Offer a small, non-destructive experiment when useful (for example a test to run or a request to try) and say what the user should observe.

## Output contract
Short answer; mental model; evidence and trace; then the debrief from `${CLAUDE_PLUGIN_ROOT}/policies/knowledge-transfer.md` (decisions, reading order, assumptions and gaps, check yourself, concepts); optional next learning step. No code changes by default.

## Shared policies
Follow `${CLAUDE_PLUGIN_ROOT}/policies/approval-gates.md` and `${CLAUDE_PLUGIN_ROOT}/policies/evidence-policy.md`, including when this skill is invoked directly rather than through `/ae:ae`. When the skill changed, reviewed, or explained something non-trivial, end with the debrief from `${CLAUDE_PLUGIN_ROOT}/policies/knowledge-transfer.md`, unless another skill invoked this one; then the outermost skill gives the single debrief.
