---
name: resume
description: Safely resume an interrupted or long-running engineering task from repository state and task artifacts. Use after context loss, interruption, or a new session.
---

# Resume Work

1. Inspect `git status`, diff, recent relevant commits, and `.agentic/tasks/` artifacts. Never reset, clean, stash, or overwrite work to make state tidy.
2. Compare task plan, execution log, verification, review findings, and actual repository state. Treat artifacts as possibly stale.
3. Re-run cheap, safe checks needed to establish current state; verify commit/base/head if work relates to a PR.
4. Summarize completed, incomplete, blocked, and uncertain work; list uncommitted changes and risks.
5. Continue only from a safe, understood point. If task identity, user intent, or approval scope is unclear, ask before side effects.
6. Respect previous approval only for the exact action/scope/environment approved; approvals do not automatically carry over to changed targets or higher-risk actions.

## Output contract
Recovered task; state evidence; completed vs remaining; uncommitted/user changes; next safe step; approvals that are still needed.

## Reliability reconciliation
If a task manifest exists, run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/task_state.py status .agentic/tasks/<task-id>/task.json` and validate it. Then reconcile manifest claims with `git status --short`, the current branch/HEAD, uncommitted diff, and current CI. Never reset, clean, stash, or overwrite user changes to make the manifest agree with the checkout. Mark evidence stale when its recorded head SHA no longer matches; rerun relevant checks before completion.

## Shared policies
Follow `${CLAUDE_PLUGIN_ROOT}/policies/approval-gates.md` and `${CLAUDE_PLUGIN_ROOT}/policies/evidence-policy.md`, including when this skill is invoked directly rather than through `/ae:ae`.
