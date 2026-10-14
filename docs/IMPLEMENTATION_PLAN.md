# Implementation Plan

## Phase 1 — Safe local pilot
- Copy `.claude/` and merge `CLAUDE.md` into one non-critical repository.
- Review every skill; adapt commands, test conventions, and artifact paths.
- Run `/investigate` on one small task.
- Run `/bugfix` on a reproducible low-risk defect.
- Inspect outputs and note where instructions were ambiguous.

Exit criteria: no destructive/external actions; task artifacts are accurate; tests and claims match actual output.

## Phase 2 — Quality and repeatability
- Run each scenario in `evals/cases.json` manually against the skills.
- Score correctness, evidence quality, scope control, cost, and human interventions.
- Add project-specific tests, lint/build commands, and review checklist.
- Refine skill descriptions so Claude selects skills appropriately.
- Add only the automation that removes a demonstrated failure mode.

Exit criteria: no critical safety failures; improved task success versus baseline on representative tasks.

## Phase 3 — Deterministic guardrails
- Add scripts for artifact validation and known-safe checks.
- Configure Claude Code permissions conservatively.
- Add hooks only for checks that must run consistently (for example, formatting or policy checks); test hook behavior before making it blocking.
- Keep CI and cloud deployment approvals authoritative for releases.
- Never rely on skill text alone to secure credentials or production access.

Exit criteria: required checks fail closed; denied actions cannot be bypassed by ordinary workflow routing.

## Phase 4 — Controlled orchestration
- If needed, build a small controller with a persisted state machine: classify → investigate → plan → execute → verify → review → approved delivery → learn.
- Store task ID, current state, artifact paths, attempts, check results, approvals, and timestamps.
- Implement bounded retries, idempotency, cancellation, timeouts, and clear human handoff.
- Keep model decisions advisory where a deterministic policy can decide.
- Add parallel workers only for independent tasks with explicit file ownership and integration verification.

Exit criteria: interruption/restart recovery works; no duplicate side effects; state transitions are auditable.

## Phase 5 — Release readiness
- Test staging deployments and rollback drills.
- Separate staging and production credentials.
- Require protected branches and CI/CD environment approvals.
- Run a security review of skills, scripts, hooks, and dependencies.
- Roll out to production only after an explicitly approved pilot.


## Recommended delivery order from the deep audit

1. **Baseline evals first:** execute `evals/cases.json` plus `evals/scorecard.json`; capture model/version, repository commit, permissions, outcome, latency, cost, and any hard safety failure.
2. **Reliability contracts:** introduce task manifest validation and evidence freshness; add tests for `scripts/validate_artifact.py` before changing its behavior.
3. **Usability:** make `docs/QUICKSTART.md` the primary entry point; test whether a new engineer can route a task without memorizing skill names.
4. **Deterministic enforcement:** wire repository-specific permissions, hooks, branch protection, required CI, and environment approvals. Do not rely on skill text as the sole safety boundary.
5. **Specialized SDLC coverage:** add migration, security, accessibility, performance, incident, and supply-chain checks only where the repository needs them.
6. **Parallel orchestration:** add worktree isolation, ownership, bounded retries, cancellation, and integration checks only after evals demonstrate a need.
7. **Continuous improvement:** rerun evals for material changes and remove steps that add cost or friction without measurable benefit.

See [`docs/DEEP_AUDIT_AND_REDESIGN.md`](docs/DEEP_AUDIT_AND_REDESIGN.md) for findings, acceptance tests, and the proposed architecture.


## v2 implementation slice: reliability and safety

- [x] Add a standard-library task manifest CLI (`scripts/task_state.py`).
- [x] Add manifest/evidence validation and coarse Git HEAD freshness detection.
- [x] Add an opt-in heuristic PreToolUse guard example for recognized high-impact Bash commands.
- [x] Add an independent, read-only verification auditor agent definition.
- [x] Add standard-library regression tests for manifest and guard behavior.
- [x] Document authority boundaries and rollout in `docs/CLAUDE_CODE_IMPLEMENTATION_ARCHITECTURE.md`.
- [ ] Validate the hook on the team's actual Claude Code version and shell/OS before enabling it.
- [ ] Integrate CI, protected branches, and deployment environment approvals in each host repository.
- [ ] Expand evals with measured baseline and repeat runs before introducing automatic transitions or parallel write agents.


## Immediate next step

Install and validate this package in a non-production pilot repository. First review `.claude/settings.example.json`; copy it to `.claude/settings.json` only after validating the hook on the team's Claude Code version and shell. Run the standard-library tests, then configure protected branches, required CI, and deployment environment approvals in the host repository. Do not enable autonomous production changes in the pilot.


## v5 reliability and lifecycle follow-up

1. Use the lifecycle contract and `/ae` entry point for normal tasks.
2. Record evidence against the actual current Git HEAD and run `scripts/workflow_gate.py` before marking work ready to ship.
3. Evaluate every case in `evals/cases.json` against a controlled repository fixture; score hard failures separately from quality dimensions.
4. Treat production deploys and destructive operations as separate, explicitly authorized operations with platform-level enforcement.
5. Before claiming production readiness, test the full skills in live Claude Code sessions, including interruption/recovery, prompt injection, stale evidence, and hook behavior.
