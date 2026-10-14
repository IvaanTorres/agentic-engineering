# Claude Code Implementation Architecture (v2)

## Decision

Use native Claude Code skills as the interaction layer, standard-library Python scripts as deterministic local controls, Git/CI as the source of truth for code state and checks, and platform permissions/environment approvals as the authority for consequential actions. Do not introduce a custom orchestrator or a mandatory multi-agent swarm in this iteration.

## Components and ownership

| Layer | Component | Responsibility | Must not be trusted to do |
|---|---|---|---|
| Intent UX | `/ae:triage`, `/ae:feature`, `/ae:bugfix`, `/ae:resume` | Choose proportional workflow and explain next step | Grant permissions |
| Specialist behavior | existing skills | Investigation, implementation, review, release preparation | Claim evidence they did not observe |
| Independent review | `.claude/agents/verification-auditor.md` | Audit the actual diff and freshness of evidence | Modify code or approve deployment |
| Durable state | `.agentic/tasks/<id>/task.json` | Status, scope, criteria, blockers, evidence references | Replace Git or CI as source of truth |
| Local validation | `scripts/task_state.py` | Validate manifest shape and compare evidence SHA to current HEAD | Prove correctness or all evidence coverage |
| Guardrail prompt | `scripts/guard_high_impact.py` + optional hook config | Surface interactive permission for recognized risky shell commands | Provide comprehensive command security |
| Authoritative gates | Claude Code permission rules, protected branches, required CI, deployment environments, least-privilege credentials | Enforce what the agent can actually do | Be replaced by prompt instructions |
| Evaluation | `evals/cases.json`, `evals/scorecard.json`, `tests/` | Catch regressions in routing, evidence, state, and obvious guard behavior | Guarantee production safety |

## Why the project hook is an example, not automatically enabled

`.claude/settings.example.json` demonstrates a `PreToolUse` Bash hook that requests an interactive permission decision for recognized high-impact commands. Review it before copying it into `.claude/settings.json`. Its command matcher is heuristic: shell aliases, wrappers, scripts, command chaining, and unfamiliar cloud CLIs can evade it, and harmless commands may trigger it. The hook therefore asks rather than silently approves or denies, and it is explicitly not a security boundary.

Install only after confirming the team's Python command, hook schema supported by its Claude Code version, and expected command patterns. For stronger enforcement, restrict the underlying credentials and use CI/deployment platform controls.

## Task lifecycle contract

The initial state machine is intentionally advisory:
`proposed -> ready -> in_progress -> verifying -> reviewing -> ready_to_ship -> completed`

`blocked` may be entered from any active state; `abandoned` is a terminal state. Do not automate state transitions yet. First collect evaluation data and decide whether state-transition scripts would reduce mistakes. The v1 validator checks allowed values and required fields, not whether a transition is semantically valid. Evidence freshness compares only the current local HEAD and recorded SHA; it does not query remote CI.

## Verification contract

A PASS requires:
- each acceptance criterion has a named evidence item;
- the command/CI job and exit status are recorded;
- evidence identifies the exact revision and environment;
- relevant test tiers were selected proportionately;
- the current diff has been inspected;
- failures, skipped checks, and environmental constraints remain visible.

The helper's SHA comparison is a coarse freshness check. A matching HEAD alone does not establish that a test covered a changed file, that a remote CI job is current, or that an environment matches production.

## Human approval contract

For production deploys, release publication, destructive migrations/data changes, secret/permission changes, force pushes, or material-cost external actions:
1. Prepare exact action, target, revision, impact, verification, rollback, and exclusions.
2. Stop and request fresh, action-specific approval.
3. Confirm platform permissions and environment/CI gates independently.
4. Execute only the approved scope.
5. Verify health and record results.
6. If target/scope changes, re-request approval.

## Recommended CI checks

- `python3 -m unittest discover -s tests -v`
- `python3 -m py_compile scripts/task_state.py scripts/guard_high_impact.py`
- JSON parse of `.claude/settings.example.json` and `evals/scorecard.json`
- validator behavior tests and safety-guard test cases
- existing project test/lint/typecheck/build commands, discovered from the host repository

The first three are runnable in this starter package. Host-project checks must be configured per repository; this package cannot infer the correct test suite generically.
