---
name: pr-fix
description: Work through review comments and CI failures on a pull request, and keep its branch up to date with its base. Explains the concern behind each comment, fixes what is valid with tests, adds new commits, drafts a reply per thread, and resolves merge conflicts with an explanation of both sides. Pushes and posts only after approval.
argument-hint: <PR number or URL> [sync]
---

# PR Fix

## 1. Gather the feedback
1. Identify the PR, its base, head SHA, and whether it is stacked. Check out its branch only if the working tree is clean or the user agrees; never discard local work.
2. Read all feedback: the review summaries and conversation (`gh pr view <n> --comments`), the **inline review comments** (`gh api repos/{owner}/{repo}/pulls/<n>/comments`), unresolved threads, and failing CI checks with their logs (`gh pr checks <n>`, `gh run view <run-id> --log-failed`).
3. Map each item to a concrete requested outcome.

## 2. Decide and explain
1. Classify each item: valid defect, valid suggestion, question, disagreement, duplicate, out of scope (becomes a follow-up), or already resolved. Don't dismiss or apply feedback blindly.
2. Explain the concern behind each comment so the user understands why the reviewer raised it, and say what you propose. Ask the user before material scope or behavior changes, and on disagreements surface the trade-off instead of picking a side.

## 3. Fix
1. Implement the smallest correction for each accepted item, preserving unrelated work and staying within the PR's scope.
2. Add or update tests per `${CLAUDE_PLUGIN_ROOT}/policies/testing.md`; a comment that exposes a bug gets a regression test.
3. For CI failures, reproduce locally when possible and fix the cause. If the failure is flaky or environmental, report the evidence; never change code or skip tests to fake a green result.
4. Run the narrowest relevant checks, then broader checks based on risk.
5. Commit the fixes as **new commits** on the PR branch (one per logical fix, messages following the repository's convention). Don't squash, amend, or rebase commits that reviewers have already seen unless the user asks.

## 4. Keep the branch current (when the base moved, there are conflicts, or the user says `sync`)
1. Show how far the branch is behind its base and which files overlap. For stacked PRs, check whether the parent was merged or squashed and the base needs retargeting.
2. Follow the repository's convention (merge the base in, or rebase). A rebase rewrites pushed history, so propose it and get approval first.
3. For each conflict, explain what each side changed and why, propose the resolution, and ask when the intent is unclear. Never resolve a conflict by silently dropping either side.
4. Rerun the relevant tests after updating.

## 5. Reply and hand off
1. Re-check each comment against the resulting diff, then draft a reply per thread with the evidence (commit, test, or reason for not changing).
2. Show the commits, any history rewrite, and the reply drafts. Ask for approval before `git push` (a force-push needs explicit approval of its own), before posting replies, and before re-requesting review.
3. After approval, push, post the approved replies, and re-request review.

## Output contract
Per item: disposition, rationale, and the reviewer's underlying concern; files changed and commits; checks and results; conflicts resolved and how; reply drafts; follow-ups; external actions still awaiting approval; then the debrief from `${CLAUDE_PLUGIN_ROOT}/policies/knowledge-transfer.md`.

## Shared policies
Follow `${CLAUDE_PLUGIN_ROOT}/policies/approval-gates.md` and `${CLAUDE_PLUGIN_ROOT}/policies/evidence-policy.md`, including when this skill is invoked directly rather than through `/ae:ae`. When the skill changed, reviewed, or explained something non-trivial, end with the debrief from `${CLAUDE_PLUGIN_ROOT}/policies/knowledge-transfer.md`, unless another skill invoked this one; then the outermost skill gives the single debrief. If you were invoked directly rather than through `/ae:ae` or another skill, and the work is non-trivial, first pick the expert lens and working frame from `${CLAUDE_PLUGIN_ROOT}/policies/lifecycle.md` and apply that lens's checklist throughout.
