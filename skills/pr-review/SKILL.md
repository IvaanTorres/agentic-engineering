---
name: pr-review
description: Review a pull request against its exact base/head diff and its ticket, look beyond the diff for side effects, judge whether the tests protect the change, and challenge the reviewer with questions so they understand it. Read-only; drafts comments without posting. Use for any PR review.
argument-hint: <PR number or URL> [quick]
---

# Pull Request Review

## Scope and safety
1. Identify the PR, base branch and SHA, head SHA, whether it is stacked on another PR (and the merge order), and whether local refs match the head. Use `gh pr view` / `gh pr diff`. If anything is unclear, ask or state the limitation.
2. Review the exact diff; don't assume the current checkout equals the PR. To run code or tests, use a temporary worktree at the head SHA and remove it afterwards; never switch or modify the user's checkout.
3. Read-only. Don't push, approve, merge, rebase, comment, or change ticket status unless separately requested and authorized.

## Gather context
1. PR description, linked ticket and its acceptance criteria (see `${CLAUDE_PLUGIN_ROOT}/policies/team-workflow.md`), designs, prior review threads, bot reviews, and CI status for the head SHA (note checks that are skipped or disabled).
2. Repository conventions that apply: `CLAUDE.md`, contribution guide, PR template, nearby code style.

## Review
1. **Requirements:** map each acceptance criterion to the code and tests that satisfy it. Flag criteria that are unmet, partially met, or met differently than specified, and behavior the PR adds that the ticket didn't ask for.
2. **Correctness by risk surface:** logic and edge cases, error paths, security/auth, data integrity and migrations, concurrency and ordering, compatibility, performance, observability, accessibility for UI, rollout and feature flags.
3. **Beyond the diff:** find callers and consumers of every changed function, type, endpoint, schema, event, or config key, including other services and the frontend/backend counterpart. Check that contracts still hold and look for side effects the author may not have seen.
4. **Tests:** apply `${CLAUDE_PLUGIN_ROOT}/policies/testing.md`. Would the tests fail if the change were reverted? Which edge cases and failure paths are untested? Are mocks hiding the behavior that matters? Run the relevant tests in the temporary worktree when the environment allows; otherwise say they were not run and why.
5. **UI changes:** list the states and flows a reviewer should click through (from the acceptance criteria and the design). If the user asks, run the app from the temporary worktree and check them in a browser as in `/ae:verify`.
6. **Findings:** for each, give severity (Blocker, High, Medium, Low, Question), file/line, a concrete triggering scenario, impact, and a fix direction. Validate each against code or tests, deduplicate, and calibrate confidence; label uncertain concerns as questions. No style preferences as defects.

## Challenge the reviewer
Unless the user asked for a quick review, follow `${CLAUDE_PLUGIN_ROOT}/policies/challenge.md` before giving the verdict:
1. Give a short overview: what the PR does, the approach, and a reading order for the diff.
2. Ask 3 to 5 questions aimed at the riskiest parts and at any gap you suspect, then wait for the answers.
3. Respond to each answer with evidence. Add any gap the answers expose to the findings.

## Report
1. Prioritized findings and open questions for the author.
2. **Draft review comments** in the user's voice, each anchored to a file and line, ready to paste. Don't post them.
3. A suggested overall decision (approve, comment, request changes) with the reason; the user decides.
4. Coverage: files and surfaces inspected, checks run or observed, CI freshness for the head SHA, and what was not examined. If there are no findings, say so and state the limitations; never imply proof of correctness.
5. Save `.agentic/tasks/<task-id>/review.md` using `${CLAUDE_PLUGIN_ROOT}/templates/review.md` when durable tracking is useful, and check it with `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/validate_artifact.py .agentic/tasks/<task-id>/review.md`.

## Output contract
PR identity, base, head, and stack; acceptance-criteria coverage; findings; challenge outcome; draft comments; suggested decision; CI and test evidence; coverage and limitations; then the debrief from `${CLAUDE_PLUGIN_ROOT}/policies/knowledge-transfer.md`. No mutation by default.

## Shared policies
Follow `${CLAUDE_PLUGIN_ROOT}/policies/approval-gates.md` and `${CLAUDE_PLUGIN_ROOT}/policies/evidence-policy.md`, including when this skill is invoked directly rather than through `/ae:ae`. When the skill changed, reviewed, or explained something non-trivial, end with the debrief from `${CLAUDE_PLUGIN_ROOT}/policies/knowledge-transfer.md`.
