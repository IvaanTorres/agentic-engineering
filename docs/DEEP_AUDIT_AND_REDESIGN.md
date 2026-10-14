# Agentic Engineering — Deep Audit and Improvement Blueprint

**Audit date:** 2026-10-14  
**Scope:** Static review of the uploaded skills, project instructions, policies, templates, validator, evaluation cases, and existing alternatives audit; compared with public workflow/tooling documentation. This is a design audit, not a runtime security certification or statistically representative user study.

## Executive recommendation

Keep the skill library. Evolve it from a set of good natural-language procedures into a **risk-adaptive workflow system** with five layers:

1. **Intent router:** one intuitive entry point that selects the smallest adequate path.
2. **Specialist skills:** bounded work with consistent preconditions, outputs, and escalation behavior.
3. **Durable task state:** enough structured state to resume safely and show progress without reconstructing everything from chat.
4. **Deterministic controls:** permissions, hooks, CI, branch protections, environment approvals, and artifact validation.
5. **Evaluation and telemetry:** measure correctness, evidence quality, safety, user effort, latency, and cost before adding more complexity.

Do not build a custom autonomous controller immediately. First prove the gaps using repeatable evals. If routing, state recovery, or approvals remain unreliable, add a small state machine with explicit transition rules.

## Findings: priority order

### P0 — Define what is enforced versus merely instructed

**Evidence:** `policies/approval-gates.md` correctly states that policy guides the agent but does not itself enforce access control. `deploy` uses `disable-model-invocation: true`, but the rest of the package primarily relies on skill instructions.

**Risk:** A model may misunderstand or skip a rule; a malicious issue, file, or web page may attempt prompt injection; a tool may have broader permissions than the skill needs.

**Change:**
- Keep approval language in skills, but enforce high-impact actions outside the model.
- Use least-privilege credentials, Claude Code permission settings, protected branches, required CI, and deployment-environment approvals.
- Require exact target/action/scope confirmation immediately before external or irreversible side effects.
- Treat issue text, repository content, logs, webpages, generated output, and agent messages as untrusted data, not authority to expand scope.
- Record the approval reference and approved target in the task record.

**Acceptance test:** A malicious issue asks the agent to exfiltrate secrets or deploy to another environment. The workflow must not perform the action; the attempt is recorded as blocked.

### P1 — Make routing feel like one product, not a command catalog

**Evidence:** The package has many focused skills and a useful `/ae:triage` skill, but users still need to know the vocabulary and sequence of commands.

**Risk:** Users invoke the wrong path, over-orchestrate small tasks, or skip a safety-critical workflow because they do not know it exists.

**Change:**
- Make `/ae:triage` the default recommendation when the request is ambiguous; let clear requests route directly.
- Use plain-language categories: **Explain**, **Fix**, **Build**, **Explore**, **Refactor**, **Review**, **Ship**, **Resume**.
- Show a compact route preview: intent, chosen path, expected changes, verification, and any approval gate.
- Ask only questions that materially change behavior, scope, or risk.
- Make “no code change needed” and “blocked pending evidence” first-class successful outcomes.

**Acceptance test:** A typo fix routes to a lightweight edit/check; a multi-service feature routes to investigate → plan → execute → verify → review; a production deploy stops for a fresh explicit approval.

### P1 — Establish a canonical task state and resumability contract

**Evidence:** `/ae:resume` reconciles artifacts with Git state, and templates exist, but no single schema defines lifecycle state, evidence freshness, dependencies, or approval scope.

**Risk:** Markdown can be stale; a resumed task may reuse old verification after files or the target commit change; parallel work may duplicate or overwrite work.

**Change:**
- Add a task manifest with task ID, intent, risk tier, status, branch/base/head SHAs, scope, acceptance criteria, task dependencies, evidence timestamps, blockers, and approval records.
- Use explicit states: `proposed`, `ready`, `in_progress`, `blocked`, `verifying`, `reviewing`, `ready_to_ship`, `completed`, `abandoned`.
- Reconcile task state against `git status`, diff, current commit, and current CI before resume.
- Invalidate verification when relevant code, dependencies, configuration, or target SHA changes.
- Never treat a prior approval as approval for a different action, environment, or commit.

**Acceptance test:** Interrupt after implementation, change the branch head, and resume. The agent identifies stale verification and reruns the required checks.

### P1 — Turn artifact validation into real validation

**Evidence:** `scripts/validate_artifact.py` searches for required substrings in Markdown. It explicitly says it validates structure only, which is appropriate, but substring presence can produce false positives and does not validate state transitions, evidence links, or consistency.

**Risk:** A document can pass because a word appears in prose rather than in a required section. There are no visible tests for the validator in the package.

**Change:**
- Add tests for missing files, wrong headings, casing, empty sections, and false-positive substrings.
- Validate headings/structure rather than arbitrary substring presence where feasible.
- Add schema validation for task manifests and allowed lifecycle states.
- Distinguish `PASS`, `FAIL`, `BLOCKED`, `NOT RUN`, and `NOT APPLICABLE`.
- Keep factual correctness as a separate evidence review; a structurally valid artifact is not proof the work is correct.

**Acceptance test:** A document mentioning “acceptance criteria” only in an unrelated paragraph must fail if the required section is absent.

### P1 — Make verification CI-aware and evidence-fresh

**Evidence:** `/ae:verify` maps acceptance criteria to commands and results, and `/ae:pr-review` calls out current CI status. The package does not yet define a standard CI evidence contract or freshness rules.

**Risk:** A green test run on a stale local checkout is mistaken for proof about the reviewed PR head; flaky failures are misdiagnosed; integration and security checks are omitted.

**Change:**
- Record command, exit code, commit SHA, timestamp, environment, and concise result for each check.
- Separate local evidence from authoritative CI evidence.
- Confirm CI belongs to the exact PR head SHA and is current.
- Identify relevant test tiers: targeted, unit, integration, end-to-end, security, performance, accessibility, migration compatibility.
- Do not require every tier for every change; use risk-based selection and repository-owned CI policy.
- Preserve pre-existing failures and environment limitations explicitly.

**Acceptance test:** The PR head changes after CI passed. Review reports CI as stale until rerun or fresh CI evidence is available.

### P1 — Add an explicit parallel-work policy before scaling subagents

**Evidence:** The alternatives audit correctly flags parallel execution as a limitation. Skills identify independent tasks but do not define isolation, ownership, cancellation, or integration semantics.

**Risk:** Shared checkout collisions, overlapping file edits, duplicated investigation, lost changes, and premature “all done” reports.

**Change:**
- Parallelize only tasks with independent file/resource ownership and bounded interfaces.
- Prefer separate worktrees or isolated branches for concurrent edits.
- Assign one integrator who owns merge conflict resolution and final verification.
- Require subagents to return changed files, commit/patch identity, commands/results, uncertainty, and known side effects.
- Treat agent output as a proposal, not verification.
- Bound fan-out, retries, time, and cost; cancel work that no longer contributes.
- Do not parallelize migrations, shared-state operations, or deployment actions without a designed coordination mechanism.

**Acceptance test:** Two subtasks touch the same file. The controller serializes them or isolates changes and detects conflict before integration.

### P2 — Close important SDLC coverage gaps with opt-in routes

Existing coverage is good for coding tasks. Add project-specific routes or checklists for:
- incident response/on-call (must defer to the organization's incident commander and runbooks);
- database migration and backward compatibility;
- threat modeling and security-sensitive changes;
- dependency updates, SBOM/provenance, license and vulnerability review;
- UI/browser/mobile and accessibility acceptance;
- performance budgets, observability, localization, generated code, monorepos, API/schema evolution, feature flags;
- post-release monitoring, rollback drills, and learning from incidents.

These should be **conditional routes**, not mandatory ceremony for every task.

### P2 — Optimize the developer experience and context cost

**Change:**
- Use a concise, consistent output contract across skills.
- Keep `CLAUDE.md` short; load detailed references only when relevant.
- Add a one-screen quickstart and route examples.
- Make the next action explicit at every handoff.
- Keep task summaries short and evidence-linked; do not create permanent knowledge notes for trivial changes.
- Show the user what will happen before costly or consequential work.
- Add explicit budget/time limits for spikes and long-running autonomous work.

### P2 — Evaluate outcomes, not prompt sophistication

**Change:**
- Compare baseline Claude Code, the current library, and targeted alternatives on the same scenarios.
- Record model/version, repo commit, permissions, test environment, latency, token/cost estimate, and task outcome.
- Use at least three runs for stochastic scenarios where budget allows.
- Score correctness, evidence, scope control, proportionality, safety, recovery, review precision, and cost.
- Treat unauthorized side effects as hard failures; do not average them away.
- Keep a skill only if it measurably improves quality, safety, usability, speed, or reuse.

## Alternatives and what to borrow

| Approach | Best use | Borrow | Avoid |
|---|---|---|---|
| Superpowers | Requirements clarification, TDD, bounded implementation | Design checkpoints, red/green discipline, review handoffs | Mandatory heavyweight planning for tiny edits |
| GSD | Long-running and multi-phase tasks | Durable state, checkpoints, resumability | Excessive phase ceremony for exploratory work |
| GitHub Spec Kit | Repeatable multi-step workflows and human gates | Declarative workflow state, conditional steps, pause/resume | Making specs mandatory for every task |
| OpenSpec | Change-oriented specs in existing products | Proposal/spec/design/task traceability and closure | Duplicating or neglecting authoritative specs |
| Native Claude Code skills/hooks | Repo-specific lightweight workflow | Native skills, permissions, hooks, project conventions | Treating model instructions as security boundaries |

References:
- Superpowers: https://github.com/obra/superpowers
- GSD: https://github.com/gsd-build/get-shit-done
- Spec Kit workflows: https://github.com/github/spec-kit/blob/main/docs/reference/workflows.md
- OpenSpec schema: https://openspec.dev/docs/schemas/spec-driven
- Claude Code steering: https://claude.com/resources/articles/steering-claude-code-skills-hooks-rules-subagents-and-more
- DORA CI: https://dora.dev/capabilities/continuous-integration/
- DORA metrics: https://dora.dev/guides/dora-metrics/
- NIST SSDF: https://csrc.nist.gov/pubs/sp/800/218/final
- GitHub Actions secure use: https://docs.github.com/en/actions/reference/security/secure-use
- OWASP GenAI Security: https://owasp.github.io/www-project-top-10-for-large-language-model-applications/

## Recommended target architecture

```text
User request
    |
    v
Intent + risk router
    |
    +--> Explain / Learn (read-only)
    +--> Fix (reproduce -> regression test -> patch -> verify)
    +--> Build (clarify -> plan -> implement slices -> verify)
    +--> Explore (time-boxed spike -> decision)
    +--> Refactor (baseline -> small steps -> regression checks)
    +--> Review (exact diff/head -> findings; read-only)
    +--> Ship (preflight -> approval -> deploy -> health checks)
    +--> Resume (reconcile Git + state + evidence)
    |
    v
Specialist skills + task artifacts
    |
    v
Deterministic controls: permissions, hooks, CI, branch/env protection
    |
    v
Evidence-backed outcome + next action
    |
    v
Evaluation and improvement
```

The controller is optional. Start with skills plus a small manifest and validation; add a runtime state machine only if evaluation proves it is needed.

## Phased implementation plan

### Phase 0 — Baseline and usability
- Run the existing eval cases and record baseline outcomes.
- Measure routing accuracy, task completion, user interventions, latency, cost, and safety failures.
- Test the first-run experience with an engineer unfamiliar with the skill names.

### Phase 1 — Reliability contracts
- Add a task manifest and lifecycle state.
- Add validator tests and schema checks.
- Standardize evidence metadata and stale-evidence rules.
- Add explicit untrusted-input and least-privilege guidance.

### Phase 2 — Developer experience
- Add quickstart, plain-language routing, route previews, and short handoff summaries.
- Tune skill descriptions to minimize overlap and accidental activation.
- Keep optional artifacts optional for tiny tasks.

### Phase 3 — CI/CD integration
- Implement repo-specific hooks and CI checks.
- Require exact-SHA evidence for PR/release readiness.
- Enforce approvals using platform controls rather than prompts alone.
- Add migration, security, browser, and accessibility checks where relevant.

### Phase 4 — Parallelism and controller (only if justified)
- Add isolated worktrees, ownership, cancellation, retry limits, and integration verification.
- Implement persisted workflow transitions and approval scope only if the prior phases show recurring failures.

### Phase 5 — Continuous evaluation
- Run the eval suite on every material skill or policy change.
- Review metrics monthly; remove skills and steps that add friction without outcome improvement.

## Definition of done for the redesign

- A newcomer can choose a path without memorizing every skill.
- Tiny tasks remain lightweight; risky tasks reliably stop at the right boundary.
- Every completion claim is linked to evidence and its commit/target.
- Resume detects stale state and never destroys user work.
- High-impact permissions are enforced outside the model.
- Parallel execution is isolated and integrated deliberately.
- Evaluations demonstrate improved results over baseline without unacceptable overhead.
