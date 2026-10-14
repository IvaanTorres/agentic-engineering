> **Historical:** this is the original toolkit README, kept for reference. Its install steps (copying `.claude/` into each project) don't apply to the plugin; see the repository `README.md` instead.

# Agentic Engineering — Claude Code

A modular, human-governed, evidence-led software lifecycle workflow for Claude Code.

## Design principles

1. Skills do specialist work; workflows compose skills; deterministic scripts validate artifacts.
2. Prefer the smallest workflow that can safely satisfy the task.
3. Treat test output, diffs, CI results, and health checks as evidence; never accept a self-reported "done".
4. Require explicit human approval before production deployments, destructive data operations, secret/permission changes, or other irreversible/high-impact actions.
5. Keep durable knowledge concise and actionable.

## Install

Copy this repository's `.claude/` directory into your project root. Merge `CLAUDE.md` guidance into your existing `CLAUDE.md` rather than replacing project-specific instructions.

```bash
cp -R .claude /path/to/your-project/
```

Then open Claude Code in the target project. Use `/ae:ae <task>` as the single entry point to route work to the appropriate specialist skill. Specialist skills are also available directly. Skills are available as `/ae:ae`, `/ae:triage`, `/ae:retrospect`, `/ae:investigate`, `/ae:plan`, `/ae:execute`, `/ae:verify`, `/ae:review`, `/ae:pr-review`, `/ae:pr-feedback`, `/ae:debug`, `/ae:spike`, `/ae:refactor`, `/ae:simplify`, `/ae:resume`, `/ae:deploy`, `/ae:document-solution`, `/ae:feature`, `/ae:bugfix`, and `/ae:release`.

Review all skill instructions and example settings before use. This starter kit does not grant permissions, configure credentials, or deploy anything by itself.

## What's included

- `.claude/skills/`: core capabilities and composed workflows, including `/ae:ae` as the single natural-language entry point
- `templates/`: standard artifacts
- `policies/`: approval and evidence requirements
- `evals/`: task scenarios for evaluating skill quality
- `docs/ALTERNATIVES_AND_COMPLETENESS_AUDIT.md`: public alternatives comparison, workflow routing matrix, gaps, and evaluation strategy
- `scripts/validate_artifact.py`: deterministic validator for required artifact sections
- `scripts/workflow_gate.py`: risk-aware readiness metadata gate for current-revision evidence (not deployment authorization)
- `policies/lifecycle-contract.md`: stage transitions, proportionality, evidence, and recovery contract
- `templates/threat-model.md`, `templates/test-strategy.md`, and `templates/incident-and-rollback.md`: lifecycle artifacts for higher-risk changes
- `IMPLEMENTATION_PLAN.md`: staged rollout


## Quickstart

For the route by intent, expected workflow, and completion contract, see [`docs/QUICKSTART.md`](docs/QUICKSTART.md). For the detailed findings and phased redesign, see [`docs/DEEP_AUDIT_AND_REDESIGN.md`](docs/DEEP_AUDIT_AND_REDESIGN.md).

## Safety and task continuity

- [`policies/agent-safety-and-tool-boundaries.md`](policies/agent-safety-and-tool-boundaries.md) describes trust boundaries and tool-use constraints.
- [`policies/task-state-and-evidence.md`](policies/task-state-and-evidence.md) defines a suggested durable task manifest, lifecycle, evidence freshness, and recovery contract.
- [`evals/scorecard.json`](evals/scorecard.json) adds a reusable evaluation rubric and scenario set.

**Important:** skills and policy documents are guidance, not access-control enforcement. Enforce high-impact actions using platform permissions, least-privilege credentials, protected branches, required CI, and deployment-environment approvals.

## Recommended first run

1. Start with `/ae:triage` or use `/ae:retrospect` for a read-only explanation.
2. For a small reversible change, keep the path light; for a multi-file feature, use `/ae:feature`; for a bug, use `/ae:bugfix`.
3. Use `/ae:spike` for time-boxed feasibility work and `/ae:refactor` for behavior-preserving structural work.
4. Before final review, consider `/ae:simplify`, then run `/ae:verify` and `/ae:review` or `/ae:pr-review` as appropriate.
5. Use `/ae:resume` after interruption and `/ae:pr-feedback` to resolve review/CI comments.
6. Compare results with `evals/cases.json` before adopting the system for important work.

## Artifact location

By default, create project artifacts in `.agentic/` in the target repository:

```text
.agentic/
  tasks/<task-id>/
    investigation.md
    plan.md
    execution-log.md
    verification.md
    review.md
    decision-record.md
    release-record.md
```

Do not store secrets, tokens, private keys, production data, or raw sensitive logs in these artifacts.

## Safety note

Skills are instructions, not a security boundary. Enforce tool permissions in Claude Code settings and CI/CD permissions separately. A prompt saying "ask first" is not equivalent to a technical access control. Never use `--dangerously-skip-permissions` for this workflow.


## Reliability controls (v2)

- `scripts/task_state.py` initializes and validates a durable task manifest and can flag evidence whose recorded Git HEAD differs from the current HEAD.
- `scripts/guard_high_impact.py` is a heuristic Claude Code `PreToolUse` hook that asks for interactive permission on recognized risky Bash commands. It is not comprehensive and is not a security boundary.
- `.claude/settings.example.json` is an opt-in hook example. Review it before copying to `.claude/settings.json`.
- `.claude/agents/verification-auditor.md` defines a read-only independent verification role.
- `tests/` contains standard-library tests for task manifest validation and the guard's representative cases.
- `docs/CLAUDE_CODE_IMPLEMENTATION_ARCHITECTURE.md` describes components, authority boundaries, and rollout.

Run the local tests with:

```bash
python3 -m unittest discover -s tests -v
python3 -m py_compile scripts/task_state.py scripts/guard_high_impact.py
```


## Context-aware expert orchestration

Use `/ae:ae <task>` as the default entry point. The orchestrator first infers the relevant engineering discipline from the request and repository, then applies that discipline's quality bar while routing into the appropriate workflow. For example, UI work gets frontend concerns (accessibility, states, responsive behavior); backend work gets contract, security, consistency, and failure-mode checks; AI/agent work gets evaluation, grounding, tool-boundary, and cost/latency checks. Cross-disciplinary tasks use a primary lens and only the secondary lenses that materially affect the result.

The expert lens is a reasoning and verification policy, not a claim of human credentials or a guarantee of correctness. Existing evidence, approval, and safety requirements always remain in force. See `.claude/skills/ae/SKILL.md` for the routing and quality bars.


## Lifecycle readiness gate (v5)

After recording evidence in `.agentic/tasks/<task-id>/task.json`, run:

```bash
python3 scripts/workflow_gate.py .agentic/tasks/<task-id>/task.json --repo .
```

The gate requires a ship-ready/completed manifest, non-empty acceptance criteria, no blockers, passing evidence tied to the current Git HEAD, and risk-appropriate evidence labels (tests/checks, review, security, and release/rollback where applicable). See `policies/lifecycle-contract.md`. A passing result validates metadata only; it cannot prove a command was honestly executed, that tests are adequate, or that a deployment is authorized.

Run all package tests with `python3 -m unittest discover -s tests -v`. The included evaluation cases are scenarios for live Claude Code assessment; they are not automatically passing benchmarks unless an evaluation runner actually executes them.


## Context and persona continuity

For non-trivial tasks, `/ae:ae` maintains a task-specific expert lens and context capsule across specialist skills and lifecycle stages. This preserves the objective, repository conventions, decisions, acceptance criteria, verification evidence, open risks, and next action through handoffs and resumes. See `policies/context-and-persona-continuity.md` and `docs/CONTEXTUAL_EXPERT_MODE.md`. This is instruction-level guidance, not a guarantee that an AI will never lose context; durable task artifacts and reconciliation against current repository state are the recovery mechanism.
