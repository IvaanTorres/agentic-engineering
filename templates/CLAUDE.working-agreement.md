# Agentic Engineering Working Agreement

Use the project's existing conventions and tests. Prefer the smallest safe change that satisfies the acceptance criteria.

## Workflow routing

- Start with `/ae <request>` when intent, task size, or risk makes the right path unclear. Choose the lightest adequate workflow; a no-change or read-only outcome is valid.
- Learning/explanation: `/ae:explain` (read-only by default).
- Small, clear, reversible change: implement narrowly, run targeted verification, and inspect the diff; do not generate a heavyweight plan by default.
- Bug: reproduce, use `/ae:debug` to identify root cause, add a regression test where practical, then `/ae:verify` and `/ae:review`.
- Feature or cross-cutting change: `/ae:explore` → `/ae:interview` (per the setting below) → proportional `/ae:plan` → bounded `/ae:implement` tasks → simplify pass when useful → `/ae:verify` → `/ae:review` → `/ae:ship`.
- Spike/feasibility: `/ae:spike` with a timebox, isolated experiment, explicit recommendation, and cleanup status.
- Refactor: `/ae:refactor` with behavior invariants and a baseline before structural changes.
- PR review: `/ae:pr-review` against the exact base/head, read-only by default. PR comments or CI feedback: `/ae:pr-fix`.
- Interrupted work: `/ae:resume` and reconcile artifacts with actual repository state before continuing.
- Release or production change: `/ae:release` and `/ae:deploy`; do not perform production-impacting actions without explicit human approval.

## Interviews

- Interviews: risky
- Interview rounds: 3
- Product rules: docs/product-rules.md

`Interviews` decides when `/ae:interview` questions you before work is planned: `always`, `risky` (medium risk and up, or when a guess could change data, permissions, a public contract or what users see), or `on-request`. Saying "interview me" or "quick" in a request overrides it for that task.

## Task persona and context continuity

- For non-trivial work, maintain a persistent task-specific expert lens: one primary discipline, only materially relevant secondary lenses, repository facts/conventions, objective, acceptance criteria, risk/quality bar, and open assumptions.
- Carry this frame through planning, execution, debugging, tests, verification, review, and delivery. A specialist skill contributes a method; it does not reset the task context or override the user's goal.
- When switching skills or resuming, pass/recover a concise context capsule with decisions, file references, changed files, exact verification outcomes, unresolved risks, next action, and approval boundaries. Reconcile it against current repository/Git state before relying on it.
- Re-evaluate the persona only when new evidence or a material scope change justifies it. Keep facts distinct from hypotheses; never invent missing context or claim human credentials.
- The `ae` plugin's `lifecycle` policy describes the working frame and when to keep a task record. Reuse an existing task record instead of creating competing notes. Keep trivial tasks lightweight.

## Evidence and handoffs

- State assumptions and distinguish observed facts from hypotheses.
- Plans must include acceptance criteria, likely risks, and verification commands.
- Do not claim tests passed unless you ran them and inspected their results.
- Never hide, delete, or weaken a failing test merely to make the suite pass.
- Record commands run, results, and unresolved issues in the task artifact.
- If verification fails, diagnose and fix or report the blocker; do not mark the task complete.

## Human approval gates

Obtain explicit approval immediately before:
- deploying to production or publishing a release;
- destructive or irreversible data/schema operations;
- deleting user data or changing retention/access policies;
- changing secrets, credentials, permissions, billing, or security controls;
- force-pushing, rewriting shared history, or making other high-impact external changes.

Describe the exact action, target environment/resource, expected impact, and rollback path before asking. A general request to "finish the feature" is not approval for these actions.

## Repository hygiene

- Do not overwrite existing project instructions or workflows without inspecting them.
- Do not commit secrets or sensitive logs.
- Do not add dependencies unless justified.
- Keep reusable knowledge short, verified, and specific to this repository.
