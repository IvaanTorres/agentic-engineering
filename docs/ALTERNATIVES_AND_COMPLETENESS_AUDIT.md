# Alternatives and Workflow Completeness Audit

**Date:** 2026-10-14  
**Scope:** Public project documentation and a sample of public user discussions; not a statistically representative survey. Product features evolve quickly, so re-check upstream docs before adopting their mechanics.

## Executive decision

Keep the custom library, but do not treat the first 11 skills as complete. The strongest approach is a **risk-adaptive hybrid**: a small router selects a task-shaped workflow; specialist skills do bounded work; repository tests/CI/platform permissions provide deterministic enforcement; task artifacts support handoffs and recovery. Do not reproduce a large framework wholesale until local evaluations show a gap.

The initial kit had core implementation and safety paths, but lacked explicit first-class routes for **task triage, spikes/prototypes, behavior-preserving refactors, simplification, learning/explanation, exact PR review, PR feedback/CI repair, and interruption recovery**. These are added in this revision. Remaining limitations are listed below; a skill library is not itself a durable controller, a security boundary, or a guarantee that a workflow was followed.

## Real alternatives: strengths and costs

### Superpowers

**Model:** workflow methodology built around brainstorming, user-approved design, detailed plans, TDD, and task-level implementation/review, with skills intended to activate automatically. Source: [project README](https://github.com/obra/superpowers).

- **Fits:** unclear requirements; users who want the agent to ask questions before coding; disciplined test-first implementation; breaking larger work into reviewed tasks.
- **Likes evidenced in public discussions:** the structured brainstorming and planning can surface requirements people had not considered; one user reported it improved their workflow and task execution ([discussion](https://www.reddit.com/r/ClaudeAI/comments/1sn27yu/claude_code_workflow_tips_after_6_months_of_daily/)).
- **Tradeoffs reported:** verbosity/overhead for smaller work; users question whether every plan stage adds value; a public discussion also reports long-running tasks with limited visibility, frequent permission prompts, and PR creation at a time the user did not want ([discussion](https://www.reddit.com/r/ClaudeAI/comments/1qj1zjg/using_claude_code_obrasuperpowers_how_do_you/)). These are individual experiences, not universal properties.
- **Borrow:** explicit design checkpoints, TDD discipline, bounded implementation tasks, user-visible handoffs.
- **Avoid copying blindly:** a mandatory heavy path for every tiny task; assume that a natural-language skill is a security control.

### GSD (Get Shit Done)

**Model:** context/project management plus phases, plans, execution, verification, and checkpoints. Its execution workflow supports interactive execution that pauses after tasks and lowers subagent/token overhead ([execution workflow](https://github.com/gsd-build/get-shit-done/blob/main/get-shit-done/workflows/execute-phase.md)).

- **Fits:** larger, multi-phase projects; users who want progress artifacts and explicit phase-level verification; work that benefits from context being carried between sessions.
- **Likes evidenced in public discussions:** users praise asking questions, planning, parallel execution, phase verification, and reduced context loss ([GSD usage discussion](https://www.reddit.com/r/ClaudeCode/comments/1qh24np/gsd_get_shit_done_usage/)).
- **Tradeoffs reported:** other users find it slow, too detailed, or token-intensive for exploratory work and small tasks ([workflow comparison discussion](https://www.reddit.com/r/ClaudeCode/comments/1rtorur/some_claude_workflow_options_ive_tried_whats_your/)).
- **Borrow:** persistent task state, task-sized execution, explicit checkpoints, resumability.
- **Avoid copying blindly:** phase ceremony for small fixes; assuming a plan is accurate merely because it is detailed.

### Compound Engineering

**Model:** brainstorm → plan → work → simplify → code review → capture reusable learning; includes optional debugging, explain, optimization, PR, browser testing, and autonomous orchestration paths ([project README](https://github.com/EveryInc/compound-engineering-plugin)).

- **Fits:** teams that want each change to improve future work; projects with recurring architectural patterns; code review that needs severity/confidence calibration; users who want a reusable solution library.
- **Borrow:** a dedicated simplification pass, a learning-compounding step, review findings with evidence, and task-size-aware review depth. The upstream review skill explicitly distinguishes report-only review from authorized local fixes ([review guide](https://github.com/EveryInc/compound-engineering-plugin/blob/main/skills/guides/ce-code-review.md)).
- **Tradeoffs:** more skills and conventions mean more setup, maintenance, and possible routing ambiguity; durable notes can become stale or duplicate source-of-truth documentation. The “planning-heavy” philosophy is not ideal for every task.
- **Avoid copying blindly:** automatically writing a knowledge note after every trivial change; multiple overlapping review passes with no measurable improvement.

### OpenSpec

**Model:** change-oriented artifacts and a propose/apply/sync/archive lifecycle, with optional exploration and verification ([getting started](https://github.com/Fission-AI/OpenSpec/blob/main/docs/getting-started.md), [commands](https://github.com/Fission-AI/OpenSpec/blob/main/docs/commands.md)).

- **Fits:** existing products with evolving requirements/specifications; changes that need a traceable proposal and an update to maintained specs; teams that want to distinguish exploration from committed work.
- **Borrow:** an explicit explore-before-commit path, change-scoped artifacts, a sync/archive closure step.
- **Tradeoffs:** spec artifacts can become bureaucracy for trivial edits; teams must decide which specs are authoritative and keep them synchronized.

### GitHub Spec Kit

**Model:** spec-driven development with specify → plan → tasks → implement and explicit review gates between stages ([workflow reference](https://github.com/github/spec-kit/blob/main/docs/reference/workflows.md)).

- **Fits:** feature work where requirements, architecture, task breakdown, and approval gates must be visible and auditable.
- **Borrow:** explicit artifact gates and machine-readable workflow definitions for high-assurance paths.
- **Tradeoffs:** greater artifact overhead; a sequential gate can slow learning when a quick prototype would answer the key question sooner.

### Native Claude Code + custom skills

**Model:** use platform-native capabilities and project instructions, adding skills only where they improve repeated outcomes. Anthropic describes skills as filesystem-based instruction bundles with optional resources/scripts; they can access tools and code, so contents should be audited ([official skills overview](https://docs.anthropic.com/en/docs/claude-code/skills), [Claude Code docs](https://docs.anthropic.com/en/docs/claude-code/overview)).

- **Fits:** users who want control, low setup, repository-specific conventions, and no dependency on a large opinionated workflow.
- **Tradeoffs:** orchestration is less deterministic unless reinforced by hooks, permissions, scripts, CI, and persisted state; skill activation and model compliance must be evaluated.
- **Borrow:** minimal primitives, clear skill contracts, deterministic checks for requirements that must not be optional.

## What public user feedback suggests people actually optimize for

These are recurring themes in a small sample, not universal consensus:

1. **Less time managing the agent.** Small work should not take days because it passed through every planning/review stage ([task-size workflow discussion](https://www.reddit.com/r/ClaudeCode/comments/1wmax2u/whats_your_actual_claude_code_workflow_by_task/)).
2. **Enough planning to prevent wild guesses.** Users value plans for complex tasks and incremental steps, but disagree on how much planning is worth it ([daily workflow discussion](https://www.reddit.com/r/ClaudeAI/comments/1sn27yu/claude_code_workflow_tips_after_6_months_of_daily/)).
3. **Visible progress and recoverable context.** Task logs, checkpoints, small slices, and resuming in a fresh session help manage long jobs ([GSD discussion](https://www.reddit.com/r/ClaudeCode/comments/1qh24np/gsd_get_shit_done_usage/)).
4. **Trustworthy verification, not confident summaries.** TDD, real command output, independent diff review, and CI status matter more than “done” claims.
5. **Control over side effects.** Users want to course-correct before a PR is created, pushed, merged, or deployed; explicit approvals should be action- and target-specific ([Superpowers review workflow discussion](https://www.reddit.com/r/ClaudeAI/comments/1qj1zjg/using_claude_code_obrasuperpowers_how_do_you/)).
6. **Cost and latency awareness.** Parallel agents and multi-pass reviews can improve coverage but consume more tokens and create synthesis noise. Escalate depth based on risk and measured value.
7. **Learning that compounds without documentation spam.** Capture reusable root causes, project-specific constraints, and architectural decisions; do not create notes for every trivial edit.

## Workflow selection matrix

| Intent / scale | Recommended path | Required evidence | Approval posture |
|---|---|---|---|
| Explain, learn, code tour | `/learn` (read-only) | File/symbol trace; uncertainty called out | No changes by default |
| Ambiguous request / unknown system | `/triage` → `/investigate` | Facts, hypotheses, unknowns | Ask only material questions |
| Tiny, clear, reversible change | `/triage` → edit directly or `/execute` → targeted `/verify` → diff scan | Focused check + diff | No deployment/push implied |
| Bug | `/bugfix` → reproduce → `/debug` → regression test → `/verify` → `/review` | Repro, root cause, regression evidence | Escalate if data/security impact |
| Medium feature | `/feature` → investigation → proportional plan → bounded execute → simplify → verify → review | Acceptance criteria mapped to checks | Approval for material design/risk choices |
| Large/multi-phase feature | `/investigate` → `/plan` → task slices → per-slice verify/review → integration verify → simplify/review → release path | Dependency plan, durable artifacts, integration evidence | Checkpoints at design and risky boundaries |
| Spike / feasibility | `/spike` | Timebox, experiment results, recommendation | No production side effects; cleanup carefully |
| Refactor | `/refactor` → baseline/characterization tests → small steps → verify/review | Behavior invariants and regression checks | Approval for public behavior/schema changes |
| Simplification | `/simplify` → verify → review as needed | Evidence behavior preserved | No unrelated cleanup |
| Review local diff | `/review` | Findings anchored to current diff | Report-only unless fixes requested |
| Review PR | `/pr-review` | Exact base/head, CI freshness, findings and coverage | Read-only; no approval/merge implied |
| Resolve review / CI feedback | `/pr-feedback` → verify → review | Each comment disposition and checks | No posting/pushing unless authorized |
| Interrupted task | `/resume` | Actual git state reconciled with artifacts | Prior approval does not expand scope |
| Release/deploy | `/release` → `/deploy` | Preflight, CI, health checks, rollback | Fresh explicit approval for exact target/action |
| Reusable lesson | `/document-solution` or `/learn` follow-up | Verified root cause/decision | Ask before broad policy changes |

## Coverage and gap closure

### Added in this revision

- `/triage`: routes by intent, uncertainty, risk, and task size; explicitly permits read-only or no-op outcomes.
- `/spike`: timebox and isolate experiments; prevents prototype code silently becoming production code.
- `/refactor`: establishes behavior invariants and baseline checks; separates structural change from behavior change.
- `/simplify`: dedicated complexity-reduction pass before final review.
- `/learn`: explanation-only path, read-only by default.
- `/pr-review`: identifies the exact PR/base/head and remains read-only by default.
- `/pr-feedback`: handles review comments and CI repair without blindly applying or posting responses.
- `/resume`: reconciles task artifacts with real repository state after interruption.

### Still needs project-specific validation

- **Incidents/on-call:** no dedicated incident commander workflow. For production incidents, use the organization's incident runbook and human incident lead; do not improvise production operations from a coding skill.
- **Data migrations:** approval policy exists, but each project needs expand/contract strategy, backup/restore evidence, compatibility windows, and rollback/forward-fix policy.
- **Security-sensitive changes:** add project-specific threat-model, dependency/SBOM, secret scanning, authorization tests, and security-owner approval as applicable.
- **UI/browser/mobile behavior:** generic verification is not enough; wire the project's browser/device test tooling and visual acceptance criteria.
- **Accessibility, performance, localization, observability:** invoke checks when the changed surface warrants them; define budgets and required CI jobs in the repo.
- **Generated code, dependency upgrades, monorepos, API/schema changes, feature flags:** tune routing and test selection for local build topology and compatibility requirements.
- **Git hosting integrations:** skills do not themselves guarantee correct PR metadata, posting comments, branch protection, or CI state. Validate connector/CLI behavior separately and require explicit authorization for external writes.
- **Parallel execution:** only add subagent orchestration when file ownership, shared checkout safety, integration tests, and failure recovery are solved.

## Architecture recommendations

1. **Layer 1 — Router:** `/triage` chooses a path; don't force every task through every skill.
2. **Layer 2 — Specialist skills:** investigation, planning, execution, debugging, simplification, verification, review, learning, PR feedback, delivery.
3. **Layer 3 — Shared contracts/artifacts:** task ID, objective, scope, risk, acceptance criteria, plan, execution log, verification, review, approvals, release record. Artifacts are evidence aids, not unquestioned truth; reconcile them against git and actual command output.
4. **Layer 4 — Deterministic controls:** Claude Code permissions, protected branches, CI required checks, environment approvals, secret boundaries, migration controls, and scripts/hooks for mechanical validation.
5. **Layer 5 — Optional controller:** add a state machine only when evals show that routing, restart recovery, retries, or side-effect tracking are unreliable. Persist state transitions and approval scope. Skills alone do not provide reliable orchestration guarantees.

## Evaluation plan

For each scenario, compare (A) baseline Claude Code with project instructions, (B) current custom skills, and (C) one relevant alternative only when useful. Run at least 3 repetitions for stochastic scenarios where budget allows; record model/version, repo commit, tool permissions, context, and cost/time.

Score 0–4 on: task correctness, evidence quality, scope control, proportionality/overhead, safety, recovery, review precision, and cost/latency. Track hard safety violations separately; any unauthorized external/destructive action is an automatic failure, not averaged away.

Required scenario families:
- tiny edit and typo; ambiguous investigation; reproducible and non-reproducible bug;
- small/medium/large feature; changing requirements mid-plan; task interruption/resume;
- spike that should be discarded; prototype promoted to production plan;
- behavior-preserving refactor with weak tests; simplification where no change is better;
- local diff review vs PR review where local checkout differs from PR head;
- contradictory review feedback; stale/failing/flaky CI; PR feedback that requires a scope change;
- dependency update, generated code, public API/schema change, data migration;
- secrets/auth/security-sensitive change; production deployment; rollback/health-check failure;
- docs-only change, learning-only request, accessibility/performance-sensitive UI change;
- malicious instructions in issue text, logs, repository docs, or web content;
- pre-existing dirty tree and unrelated user edits.

Success means better outcomes than baseline **without unacceptable overhead**. Keep a skill only if it improves measurable quality, reliability, safety, or future reuse. Delete or merge overlapping skills when they add routing ambiguity without value.
