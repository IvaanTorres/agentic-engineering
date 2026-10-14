# Quickstart: use the lightest safe workflow

## Start with the outcome, not the command name

| You want to… | Start here | Expected path |
|---|---|---|
| Not sure where to start | `/ae <request>` | Classifies the request and picks the lightest route |
| Understand code, an error or a concept | `/ae:explain` | Read-only explanation grounded in files/tests |
| Learn from a PR, branch, or an agent's task | `/ae:explain <PR, branch, or task id>` | The change as a story of decisions, with a reading order |
| Fix a bug | `/ae:fix` | Reproduce → root cause → regression test → verify → review |
| Make a small, clear change | `/ae <request>` or `/ae:implement` | Narrow edit → targeted check → diff scan |
| Build a feature | `/ae:feature` | Investigate → proportional plan → implement slices → verify → review → ship |
| Test feasibility | `/ae:spike` | Time-boxed experiment → recommendation → cleanup status |
| Restructure or simplify without behavior changes | `/ae:refactor` | Baseline → small steps → regression checks |
| Review a local diff | `/ae:review` | Evidence-based findings; report-only by default |
| Review a pull request | `/ae:pr-review` | Exact base/head and CI freshness; read-only |
| Commit and open a PR | `/ae:ship` | Clean commit → PR description from decisions and evidence → approval → push |
| Resolve PR feedback | `/ae:pr-fix` | Disposition each comment → patch → verify; no posting/push by default |
| Prepare a release/deployment | `/ae:release`, then `/ae:deploy` | Preflight → explicit approval → execute authorized action → health checks |
| Continue after interruption | `/ae:resume` | Reconcile task artifacts against actual Git state |

## What the agent should show you

Before material work:
- the selected workflow and why it fits;
- important assumptions and acceptance criteria;
- likely files/surfaces and relevant risks;
- any decision or approval required before proceeding.

At completion:
- what changed and what did not;
- commands actually run, exit status, and relevant results;
- checks not run and why;
- known risks, uncertainty, and next action;
- a debrief: decisions and alternatives, reading order, assumptions and gaps, what to check yourself, and key concepts (see `policies/knowledge-transfer.md`).

## Approval is action-specific

Approval for implementation is not approval to push, merge, publish, deploy, run destructive migrations, change credentials, or alter permissions. Before a high-impact action, the agent must identify the exact target, action, impact, verification, and rollback/mitigation plan, then wait for explicit approval. Platform permissions and CI/environment controls remain authoritative.

## A simple rule

If the task is clear, local, and reversible, keep the process short. If uncertainty, scope, security, data integrity, or external side effects increase, add investigation, planning, verification, and human checkpoints. Never use the number of artifacts as a proxy for quality.
