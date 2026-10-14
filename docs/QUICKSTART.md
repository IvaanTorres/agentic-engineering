# Quickstart: use the lightest safe workflow

## Start with the outcome, not the command name

| You want to… | Start here | Expected path |
|---|---|---|
| Understand code or an error | `/ae:retrospect` | Read-only explanation grounded in files/tests |
| Fix a bug | `/ae:bugfix` | Reproduce → root cause → regression test → verify → review |
| Make a small, clear change | `/ae:triage` or direct request | Narrow edit → targeted check → diff scan |
| Build a feature | `/ae:feature` | Investigate → proportional plan → implement slices → verify → review |
| Test feasibility | `/ae:spike` | Time-boxed experiment → recommendation → cleanup status |
| Restructure without behavior changes | `/ae:refactor` | Baseline → small steps → regression checks |
| Review a local diff | `/ae:review` | Evidence-based findings; report-only by default |
| Review a pull request | `/ae:pr-review` | Exact base/head and CI freshness; read-only |
| Resolve PR feedback | `/ae:pr-feedback` | Disposition each comment → patch → verify; no posting/push by default |
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
- known risks, uncertainty, and next action.

## Approval is action-specific

Approval for implementation is not approval to push, merge, publish, deploy, run destructive migrations, change credentials, or alter permissions. Before a high-impact action, the agent must identify the exact target, action, impact, verification, and rollback/mitigation plan, then wait for explicit approval. Platform permissions and CI/environment controls remain authoritative.

## A simple rule

If the task is clear, local, and reversible, keep the process short. If uncertainty, scope, security, data integrity, or external side effects increase, add investigation, planning, verification, and human checkpoints. Never use the number of artifacts as a proxy for quality.
