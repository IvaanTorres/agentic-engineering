---
name: ship
description: Turn a verified change into a clean commit and a pull request whose description explains the decisions, evidence, and risks. Use after verify and review pass, when the user wants the work committed and a PR opened.
argument-hint: <optional base branch or PR title>
---

# Ship

## Preconditions
- Verification and review have run for the current changes, or the user explicitly accepts shipping without them (record that in the PR).
- Know the target base branch. Read the repository's contribution rules: `CONTRIBUTING`, PR templates (`.github/pull_request_template.md`, `.github/PULL_REQUEST_TEMPLATE/`), commit conventions visible in `git log`, and branch naming.

## Procedure
1. Inspect `git status`, the branch, and the full diff against the base. Exclude unrelated changes, generated churn, secrets, `.agentic/` artifacts, and local config from the commit. If unrelated changes are mixed in, ask before staging selectively.
2. If on the default branch, create a feature branch named to the repository's convention (include the ticket id when there is one).
3. Commit with a message that follows the repository's convention and explains why, not only what. Prefer one coherent commit per logical change; do not rewrite history that has already been pushed.
4. Draft the PR description from the evidence, following the repository's template when one exists:
   - **What and why**: the problem and the approach, linked to the issue or ticket.
   - **Decisions**: material choices and rejected alternatives (from the plan and the execution log's decisions table).
   - **How to review**: the reading order for the diff and the riskiest parts.
   - **Testing**: commands run and results at the current HEAD, plus what was not tested and why.
   - **Risks and follow-ups**: known gaps, rollout notes, feature flags, migrations.
5. Show the user the branch name, commit message, and PR description, and ask for approval before `git push` or `gh pr create`. Pushing and opening a PR are outward-facing actions.
6. After approval, push and open the PR (`gh pr create`, as a draft if the user prefers). Report the PR URL and the CI checks that started.

## Output contract
Branch, commit(s), PR URL (or the drafted description if not yet approved), checks triggered, and the debrief from `${CLAUDE_PLUGIN_ROOT}/policies/knowledge-transfer.md`. The PR description is itself the main knowledge-transfer artifact for reviewers; keep it accurate and concise.

## Guardrails
- Never force-push, rebase shared branches, or bypass hooks or CI without explicit approval.
- Never claim tests passed in the PR description unless they ran at the current HEAD.
- Do not merge; merging is a separate, explicitly requested action.

## Shared policies
Follow `${CLAUDE_PLUGIN_ROOT}/policies/approval-gates.md` and `${CLAUDE_PLUGIN_ROOT}/policies/evidence-policy.md`, including when this skill is invoked directly rather than through `/ae:ae`. When the skill changed, reviewed, or explained something non-trivial, end with the debrief from `${CLAUDE_PLUGIN_ROOT}/policies/knowledge-transfer.md`.
