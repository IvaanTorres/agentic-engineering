# Agentic Engineering v5 — Independent Completeness, Security, and Workflow Audit

**Audit date:** 2026-10-14  
**Scope:** Static inspection of the supplied ZIP, its Claude Code skills/instructions, policy documents, templates, scripts, tests, and evaluation fixtures. This is not a full adversarial security review or a run in a real target repository.

## Executive verdict

**Promising engineering workflow library; not yet production-assured or demonstrably complete.** The package has a useful risk-adaptive lifecycle, 18 specialist skills, policy contracts, durable task-state helpers, templates, a hook example, tests, and evaluation scenarios. The existing automated suite passes (21 tests). That is meaningful baseline evidence, but it does not establish that the workflow is enforced, the hook catches all dangerous operations, the skills are consistently invoked, or the evaluations improve outcomes.

**Important packaging distinction:** the archive contains Claude Code project-level skills under `.claude/skills/`, but no `.claude-plugin/plugin.json` manifest. As supplied, it is a repository kit / project configuration, not a self-contained distributable Claude Code plugin in the standard plugin package shape. Either add a plugin manifest and validate installation from a test marketplace, or clearly document that users must copy/install it as project configuration.

## What is present

- Project-level `CLAUDE.md` plus `/ae` orchestration and specialist skills for triage, investigation, planning, execution, bug fixing/debugging, features, refactoring/simplification, verification/review, PR review/feedback, resume, release/deploy, spikes, learning, and solution capture.
- Lifecycle, evidence, task-state, approval, skill-contract, and tool-boundary policies.
- Markdown artifact templates; task-manifest, artifact-validation, workflow-gate, and high-impact-command scripts.
- A Claude Code hook settings example, a verification-auditor agent, 21 reliability-control tests, and JSON eval cases/scorecard.
- Documentation describing architecture, quick start, workflow usage, release notes, and known alternatives/gaps.

## Verification performed

- `pytest -q`: **21 passed**.
- The package's Python test suite executes successfully in this environment. A non-fatal Python startup warning from the environment's spreadsheet warmup appeared after pytest; it was not a test failure.
- Static review of core lifecycle/policy documents, the task-state and artifact scripts, the command guard, settings example, the main `/ae` skill, and the completeness audit document.
- This did **not** include installing the package into Claude Code, exercising live hooks, testing against real repositories/CI, or performing a comprehensive shell-command bypass campaign.

## Findings (priority order)

### P0 — Clarify package/install contract

**Finding:** no `.claude-plugin/plugin.json` is present. The package's layout is suitable for project-level configuration but is not a complete standard Claude Code plugin bundle as delivered.

**Impact:** users may expect `/plugin install` / marketplace installation behavior that the archive does not provide.

**Action:** choose and document one supported distribution model:
1. **Project kit:** keep `.claude/` and instruct users to copy/merge the files into their repository, with a safe merge/backup procedure; or
2. **Distributable plugin:** add `.claude-plugin/plugin.json`, ensure plugin-relative paths and skill discovery work after installation, and test installation/uninstallation from a fixture marketplace. Avoid silently overwriting user settings.

### P1 — The high-impact command hook is a warning layer, not a security boundary

**Finding:** `guard_high_impact.py` explicitly fails open on malformed hook input. Its regexes inspect a raw command string and cannot reliably parse shell syntax, wrappers, aliases, scripts, encoded commands, or all equivalent CLI forms. Several dangerous operations may be expressed in ways the regexes do not match. The script itself correctly warns that platform permissions are authoritative, but users could still overestimate coverage.

**Impact:** regex matching can create a false sense of safety. A matching hook is not a general shell policy engine.

**Action:**
- Keep the disclaimer prominent in install docs and never describe the guard as complete prevention.
- Configure Claude Code's native permission deny/ask rules for known risky tools/commands, and enforce deployments/publishing/database changes with platform IAM, CI/CD environment approvals, protected branches, and separate credentials.
- Decide deliberately whether malformed hook input should block or fail open. If fail-open is retained for availability, log a sanitized diagnostic to stderr and explicitly state that the native permission layer must still deny unsafe operations.
- Add adversarial tests for shell chaining, environment assignments, `sudo`, `git -C`, command wrappers, quoting, newlines, CLI aliases, and alternative destructive command forms. Prefer tool-specific structured controls where possible over trying to solve shell parsing with regex.

### P1 — Workflow gates validate evidence metadata, not evidence authenticity or adequacy

**Finding:** `workflow_gate.py` checks for named passing evidence records and a matching HEAD. Names containing tokens such as `test`, `review`, `security`, or `release` can satisfy broad categories; the gate cannot establish that the command ran, that output is genuine, that the reviewer was independent, or that the check covers the change. Matching HEAD also does not prove a clean working tree or complete coverage.

**Impact:** a manifest can pass while the actual work is unverified or evidence is weak.

**Action:**
- Keep the current disclaimer and label output **“metadata gate passed”**, not “verified” or “safe to ship.”
- Where practical, capture evidence directly from trusted CI or wrapper commands, including command, exit status, commit/tree identity, environment, timestamp, and artifact location.
- Require explicit check identifiers / structured evidence types rather than substring matching on human-authored names.
- Add tests for dirty trees, malformed evidence, duplicate/conflicting records, missing acceptance criteria, wrong repo path, and stale evidence after changes.
- Never use this gate as deployment authorization.

### P1 — No demonstrated CI/release enforcement in the supplied tree

**Finding:** there is no CI workflow configuration in the archive. The scripts and tests exist, but the package does not itself show that they are run on every change or that distribution is blocked on failure.

**Impact:** controls can silently regress after the package is adopted.

**Action:** add a CI workflow for supported Python versions that runs unit tests, `compileall`, JSON parsing/schema checks, skill frontmatter/path checks, shell/hook fixtures, and packaging validation. Pin third-party actions by full commit SHA if used. Add release artifact validation and a smoke test that confirms skill discovery in the chosen install mode.

### P1 — Task manifest validation is permissive in important nested fields

**Finding:** `task_state.py` validates many top-level types but does not fully validate nested `scope` and `repository` shapes, timestamp format, SHA format, approval record shape, dependency element types, or status-transition legality. `--force` can replace an existing manifest, and the init path does not appear to use atomic write semantics.

**Impact:** malformed or inconsistent state can survive validation, and a partial write or careless `--force` can damage durable task state.

**Action:** implement a versioned JSON Schema or equivalent complete nested validation; validate UTC timestamps and SHA formats where applicable; define legal state transitions; make writes atomic (temporary file + replace); make force replacement require a backup or stronger explicit confirmation; add tests for malformed nested structures, interrupted writes, and invalid transitions. Preserve forward compatibility deliberately.

### P2 — Eval fixtures are not an executable evaluation harness

**Finding:** `evals/cases.json` and `scorecard.json` document scenarios and scoring, but no runner or baseline-comparison report is included.

**Impact:** the library's quality and overhead claims cannot be measured repeatably from this archive alone.

**Action:** provide a runner or a clearly documented manual protocol that records model/version, skill revision, repo commit, tool permissions, prompts, outcomes, safety violations, latency, and cost. Include baseline-vs-skills comparisons and deterministic assertions for safety-critical cases. Treat unauthorized side effects as hard failures, not an averaged score.

### P2 — The skill inventory is broad; routing overlap needs regression tests

**Finding:** there are many useful specialist skills and the `/ae` router describes intent routing, but natural-language descriptions overlap (for example bugfix/debug/investigate; release/deploy; review/pr-review; feature/execute/plan). Documentation acknowledges proportionality, but no automated tests establish routing consistency or that all skills obey shared safety/evidence contracts.

**Action:**
- Define a compact skill contract for every skill: trigger, preconditions, permitted actions, required outputs/evidence, stop conditions, handoff target, and prohibited side effects.
- Add one routing fixture per skill plus ambiguous/overlapping cases; assert the selected path and safety invariants.
- Check every `SKILL.md` has valid frontmatter, unique name, a concise description, valid local links, and no contradictory defaults.
- Consider whether `bugfix` should explicitly say when to route to `/debug` vs `/investigate`; similarly distinguish release preparation from deployment execution.

### P2 — Project-specific engineering quality gates remain intentionally external

The docs correctly acknowledge that generic skills cannot substitute for project controls. Before using this in a real engineering team, explicitly map these to repository/organization tooling:
- unit, integration, contract, end-to-end, and regression tests;
- formatting, lint, type checking, static analysis, dependency/license/SBOM and secret scanning;
- authorization/security tests and threat-model ownership for sensitive changes;
- migration expand/contract, backup/restore, compatibility and rollback/forward-fix checks;
- accessibility, localization, performance budgets, observability and browser/device checks where relevant;
- branch protection, required CI, code-owner approval, release signing/provenance, environment protection and deployment health checks.

These are not all defects in a generic skill pack; they are explicit adoption requirements and must not be implied to be covered automatically.

### P3 — Documentation/readability improvements

- The root README should start with a short “what this is / what it is not,” install mode, supported prerequisites, first command, and limitations.
- State whether paths assume repository root, and provide copy/paste commands for Windows/macOS/Linux where support is intended.
- Include a one-page lifecycle diagram or concise stage table, plus a troubleshooting section for hooks and skill discovery.
- Mark normative policies (“MUST/NEVER”) consistently and keep detailed rationale in docs, not repeated across every skill.
- Add a changelog/release process and compatibility policy for manifest/schema changes.
- Add a clear “known limitations / threat model” section next to installation instructions.

## Recommended acceptance criteria before calling this production-ready

- [ ] Distribution model is explicit and smoke-tested (project kit or installable plugin).
- [ ] All skills pass automated frontmatter, name, link, and contract checks.
- [ ] CI runs unit, static, packaging, and hook adversarial tests on every PR.
- [ ] Dangerous actions are constrained by native permissions/platform controls, not regex alone.
- [ ] Manifest schema and legal state transitions are validated; writes are atomic.
- [ ] Evidence gate uses structured evidence types and is documented as metadata-only.
- [ ] Eval harness measures baseline comparison, routing, safety, recovery, and overhead.
- [ ] A fixture repo validates install, routing, task creation/resume, verification, and release-preflight behavior.
- [ ] Team-specific quality/security/release checks are mapped to real CI and owner approvals.
- [ ] Final diff, test output, known limitations, and versioned release artifact are recorded.

## Final assessment

The v5 package has a strong foundation and is substantially more disciplined than a loose collection of prompts. Its most valuable design choice is the risk-adaptive lifecycle combined with explicit evidence semantics and approval boundaries. The largest remaining risk is the gap between **instructions and enforceable controls**: skills route and guide work, but they do not guarantee execution; the command hook is incomplete by construction; and metadata gates do not authenticate evidence. Address packaging, CI, structured validation, adversarial testing, and repeatable evaluations before presenting it as complete or production-secure.
