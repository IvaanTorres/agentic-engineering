---
name: ae
description: Single entry point for Agentic Engineering. Classify a natural-language request, route it to the lightest suitable specialist skill, preserve task state, verify with evidence, stop at approval gates, and end with a debrief the user can learn from.
argument-hint: <task or goal>
user-invocable: true
---

# Agentic Engineering — Entry Point

The user's request is available as `$ARGUMENTS`. `/ae:ae` (or `/ae`) is the front door for this toolkit; specialist skills can also be called directly as `/ae:<name>`.

## Operating contract
1. If `$ARGUMENTS` is empty, ask what the user wants to accomplish and offer the routes below.
2. Inspect the current directory, project instructions, `git status --short` when Git is available, and existing `.agentic/tasks/` state. Preserve unrelated changes. If the request names a ticket, read it first and work to its acceptance criteria (`${CLAUDE_PLUGIN_ROOT}/policies/team-workflow.md`).
3. Classify the request (below), choose the lightest adequate route, and invoke that specialist skill (`ae:<name>`) before following it. Always use this plugin's `ae:` skills. Never substitute a built-in command, an account skill, or another plugin's skill with a similar name (for example a generic `review`, `plan`, `debug` or `simplify`). Ask only questions whose answers change the solution or risk; otherwise state low-risk assumptions.
4. For non-trivial work, read `${CLAUDE_PLUGIN_ROOT}/policies/expert-lenses.md` and `${CLAUDE_PLUGIN_ROOT}/policies/context-and-persona-continuity.md`, establish the working frame, and keep it across skill hand-offs. Specialist skills inherit it instead of starting from a blank context.
5. Work only within the requested scope. Run relevant checks and record exact commands and outcomes. Never claim a check ran or passed unless it did.
6. Follow `${CLAUDE_PLUGIN_ROOT}/policies/agent-safety-and-tool-boundaries.md` and `${CLAUDE_PLUGIN_ROOT}/policies/approval-gates.md`. Ask before deployment, publishing, destructive data changes, secret/permission changes, irreversible operations, or shared Git history rewrites. A prompt or guard script is not a complete security boundary.
7. Finish with outcome, changed files, verification evidence, approvals requested/obtained, unresolved risks, the next recommended action, and the debrief from `${CLAUDE_PLUGIN_ROOT}/policies/knowledge-transfer.md`.

## Classify and route
| Request | Route |
|---|---|
| Understand code, a concept, a PR/branch, or what an agent did | `ae:explain` (read-only) |
| Tiny, clear, reversible change | Do it directly: inspect status, edit, targeted check, diff review, debrief |
| Small bounded implementation with clear requirements | `ae:implement`, then `ae:verify` |
| Bug or regression | `ae:fix`; if the cause is unclear, `ae:explore` or `ae:debug` first |
| New behavior or multi-file change | `ae:feature`; for broad or ambiguous work, `ae:plan` first |
| Explicit plan/design request | `ae:plan` |
| Investigation, architecture question, root cause | `ae:explore` |
| Feasibility or uncertain technology | `ae:spike`, with a timebox and stop condition |
| Behavior-preserving restructuring or simplification | `ae:refactor` |
| Check evidence for a change | `ae:verify` |
| Review a local diff | `ae:review`; a pull request: `ae:pr-review` |
| Understand my own change, commit it, write the PR, open it | `ae:ship` |
| A ticket ID or URL | Read it, then route by what it asks: `ae:feature`, `ae:fix`, `ae:spike`, or `ae:explore` when it is unclear |
| Urgent production bug (hotfix) | `ae:fix` in hotfix mode (`${CLAUDE_PLUGIN_ROOT}/policies/team-workflow.md`) |
| PR review comments or CI feedback | `ae:pr-fix` |
| Continue interrupted work | `ae:resume` |
| Release preparation | `ae:release` |
| Deployment / production operation | `ae:deploy`. Only the user can start it: prepare what you can and ask them to run `/ae:deploy <target>`; never deploy without explicit approval |
| Durable lesson, runbook, or decision | `ae:record` |
| Unknown, incident, failing CI | `ae:explore` first; don't guess or silently widen scope |

For complex changes the default path is `ae:explore` → `ae:plan` → `ae:implement` → `ae:verify` → `ae:review` → `ae:ship`, skipping stages only when justified. Never run every skill mechanically. Escalate the route when new uncertainty, sensitive surfaces, migrations, external side effects, or failed checks appear. A read-only or "no change needed" outcome is valid.

## Task records
For multi-step, interrupted, medium/high-risk, or externally consequential work, create a task record:
`python3 ${CLAUDE_PLUGIN_ROOT}/scripts/task_state.py init --id <short-id> --objective "<observable outcome>" --intent <feature|bug|refactor|spike|review|release|other> --risk <low|medium|high|critical>`
- Check `--help` before using other subcommands; never invent flags or overwrite another task's record. The format is in `${CLAUDE_PLUGIN_ROOT}/policies/task-state-and-evidence.md`.
- Before creating `.agentic/` in a repository, run `git check-ignore -q .agentic`; if it is not ignored, tell the user and suggest adding it to `.gitignore` rather than editing that file without asking.
- Skip the record for a trivial one-file change unless it helps recovery. Fill scope and acceptance criteria before implementation.

## Lifecycle contract
Follow `${CLAUDE_PLUGIN_ROOT}/policies/lifecycle-contract.md`. `/ae:ae` stays accountable for the task when it hands off to specialist skills; skills are workflow guidance, not authorities that can skip safety or evidence requirements.
- Before reporting completion, inspect the final diff and run applicable verification against the current Git HEAD. Tests follow `${CLAUDE_PLUGIN_ROOT}/policies/testing.md`: required by default for behavior changes, skipped only with a stated reason.
- Evidence scales with risk: medium or higher needs review evidence; high/critical needs security/threat evidence; release/critical needs release, rollback, and preflight evidence.
- With a valid task manifest, run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/workflow_gate.py .agentic/tasks/<task-id>/task.json` before calling the task ready to ship. It checks evidence metadata only, not authenticity, test quality, or deployment authorization. If it fails, report the blockers instead of bypassing them.
- If requirements change materially, update scope and criteria and revisit risk. On resume, reconcile real files and Git state before trusting earlier notes.

## Status semantics
Distinguish **implemented** (code changed), **verified** (relevant checks actually passed and evidence recorded), **blocked** (decision, approval, dependency, or environment missing), and **not run** (check not executed). The artifact validator (`${CLAUDE_PLUGIN_ROOT}/scripts/validate_artifact.py`) checks structure, not whether evidence is true.
