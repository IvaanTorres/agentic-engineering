---
name: ship
description: Prepare the user's change for review so they understand exactly what they are delivering. Self-reviews the diff against the ticket, walks the user through it and challenges them on edge cases and side effects, checks the definition of done, then makes a clean commit and drafts the PR; pushes and opens the PR only after approval. Works for changes written by the user or by an agent.
argument-hint: <optional ticket, base branch, or "quick">
---

# Ship

## 1. Establish the change
1. Inspect `git status`, the branch, and the full diff against the target base (including uncommitted work and existing local commits). Confirm the base branch; for stacked work, name the parent PR and merge order.
2. Find the ticket from the request, branch name, or commits and read its acceptance criteria (`${CLAUDE_PLUGIN_ROOT}/policies/team-workflow.md`). Read `.agentic/tasks/` artifacts if they exist; if the user wrote the change, reconstruct intent from the diff and commits instead, and ask where the intent is unclear.
3. Read the repository's contribution rules: `CONTRIBUTING`, PR templates (`.github/pull_request_template.md`, `.github/PULL_REQUEST_TEMPLATE/`), commit conventions visible in `git log`, branch naming, and any definition of done.

## 2. Self-review
1. Map each acceptance criterion to the code and tests that satisfy it; list anything unmet or done differently. If there is an interview record, check its decisions and scenarios too, and list any the change doesn't honor.
2. Look beyond the diff: callers and consumers of changed symbols, contracts, config, migrations, feature flags, and the other side of any API.
3. Check tests against `${CLAUDE_PLUGIN_ROOT}/policies/testing.md`. If a required test is missing, say so and offer to add it (via `/ae:implement`) before shipping.
4. Catch accidental content: debug output, commented-out code, stray TODOs, unrelated files, generated churn, secrets, local config, `.agentic/` artifacts.
5. Run the relevant checks (lint, types, tests) at the current HEAD unless `/ae:verify` already did for this exact HEAD. Report failures; don't ship on red without the user's explicit decision.
6. For medium-or-higher risk or a large diff, run `/ae:review` (which brings in the independent `ae:reviewer` subagent) if it hasn't run on this HEAD.
7. For UI changes, make sure the browser check in `/ae:verify` ran on this HEAD; otherwise run it or put manual QA steps in the PR.

## 3. Make sure the user understands it
Unless the user asked for a quick ship:
1. Walk the user through the change: what it does, the approach, the decisions (from the execution log or reconstructed, labelled as such), and a reading order.
2. Challenge them following `${CLAUDE_PLUGIN_ROOT}/policies/challenge.md`: edge cases, side effects, why this approach, what the tests do and don't prove, what a reviewer will ask. Wait for answers and respond with evidence.
3. Fold any gap the answers expose into a fix (before shipping) or into the PR's known risks, as the user decides.

## 4. Commit and draft the PR
1. If on the default branch, create a branch named to the repository's convention, including the ticket id.
2. Stage only the intended changes; if unrelated changes are mixed in, ask before staging selectively. Commit following the repository's convention, explaining why, not only what. Don't rewrite history that has been pushed.
3. Draft the PR description, following the repository template when there is one:
   - **What and why:** the problem, the approach, and the ticket link.
   - **Acceptance criteria:** each one and where it is satisfied.
   - **Decisions:** material choices and rejected alternatives, including product decisions agreed in the interview.
   - **How to review:** reading order and the riskiest parts.
   - **How to test:** commands run and results at the current HEAD; manual steps for QA; what was not tested and why.
   - **Risks and rollout:** side effects considered, migrations, feature flags, backward compatibility.
   - **Follow-ups:** out-of-scope items for new tickets.
4. Show the branch, commit message, and PR description. Ask for approval before `git push` and `gh pr create` (draft PR if the user prefers). Offer a ticket status update as a draft; don't change it without approval.
5. After approval, push and open the PR, then report the URL and the CI checks that started.

## Output contract
Acceptance-criteria coverage; self-review findings and how they were resolved; challenge outcome; checks and results; branch, commits, PR URL (or the draft if not approved); follow-ups; then the debrief from `${CLAUDE_PLUGIN_ROOT}/policies/knowledge-transfer.md`. The PR description is the reviewers' knowledge transfer; keep it accurate and concise.

## Guardrails
- Never force-push, rebase shared branches, or bypass hooks or CI without explicit approval.
- Never claim tests passed in the PR description unless they ran at the current HEAD.
- Don't merge; merging is a separate, explicitly requested action.

## Shared policies
Follow `${CLAUDE_PLUGIN_ROOT}/policies/approval-gates.md` and `${CLAUDE_PLUGIN_ROOT}/policies/evidence-policy.md`, including when this skill is invoked directly rather than through `/ae:ae`. When the skill changed, reviewed, or explained something non-trivial, end with the debrief from `${CLAUDE_PLUGIN_ROOT}/policies/knowledge-transfer.md`, unless another skill invoked this one; then the outermost skill gives the single debrief. If you were invoked directly rather than through `/ae:ae` or another skill, and the work is non-trivial, first pick the expert lens and working frame from `${CLAUDE_PLUGIN_ROOT}/policies/lifecycle.md` and apply that lens's checklist throughout.
