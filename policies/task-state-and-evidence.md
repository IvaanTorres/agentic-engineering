# Task State and Evidence Contract

This policy defines the minimum durable state for multi-step or risky work. Tiny edits may use a short summary instead of creating a full task directory.

## Task manifest

Store one manifest at `.agentic/tasks/<task-id>/task.json` for tasks that need resumability. Keep secrets, credentials, tokens, private production data, and raw sensitive logs out of the manifest.

Minimum fields:

```json
{
  "schema_version": 1,
  "task_id": "short-stable-id",
  "intent": "feature | bug | refactor | spike | review | release | other",
  "status": "proposed",
  "risk": "low | medium | high | critical",
  "objective": "observable desired outcome",
  "scope": {
    "in_scope": [],
    "out_of_scope": []
  },
  "repository": {
    "branch": "",
    "base_sha": "",
    "head_sha": ""
  },
  "acceptance_criteria": [],
  "dependencies": [],
  "evidence": [],
  "approvals": [],
  "blockers": [],
  "updated_at": ""
}
```

This is a template, not a promise that every field is known at task creation. Unknown values must remain explicit rather than guessed.

## Lifecycle states

- `proposed`: request understood enough to frame; not yet ready to execute.
- `ready`: scope, acceptance criteria, and required decisions are clear.
- `in_progress`: bounded implementation or investigation is active.
- `blocked`: a missing decision, failed prerequisite, permission, or external dependency prevents safe progress.
- `verifying`: implementation is paused while required checks/evidence are collected.
- `reviewing`: diff and evidence are being independently inspected.
- `ready_to_ship`: required checks and review are satisfied; any ship action still needs its own approval.
- `completed`: requested outcome is complete and evidence is recorded.
- `abandoned`: work was intentionally stopped; preserve relevant state and user changes.

Do not skip a state just to make the artifact look complete. Record why a transition was made.

## Evidence record

Each important check should record:
- check name and exact command or CI job;
- result: `PASS`, `FAIL`, `BLOCKED`, `NOT RUN`, or `NOT APPLICABLE`;
- exit code when applicable;
- commit SHA or tree identity checked;
- timestamp and environment;
- concise result and link/path to non-sensitive details.

## Freshness rules

Re-run relevant checks when any of the following changes after evidence was collected:
- source files or tests covered by the check;
- dependency lockfiles, build/test configuration, compiler/runtime version, or relevant environment;
- base/head SHA of the reviewed change;
- migration, API/schema, authorization, or deployment configuration.

A task summary or previous agent statement is not evidence. Reconcile state against the real working tree and authoritative CI.

## Approval records

Record action, target, environment/resource, approved scope, approver/reference, timestamp, and conditions. Approval must not be inferred from a generic instruction or transferred to a different target, commit, environment, or action. Do not store secrets or credentials in approval records.

## Recovery

On resume:
1. Inspect Git status, diff, branch, and current commit.
2. Read the manifest and task artifacts, treating them as possibly stale.
3. Compare current code/target SHA to the evidence records.
4. Identify completed, incomplete, blocked, and uncertain work.
5. Re-run cheap checks needed to establish state.
6. Continue only within the original scope and approvals; ask before material scope changes or external side effects.
