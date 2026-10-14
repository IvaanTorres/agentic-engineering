---
name: pr-review
description: Review a pull request or proposed branch against its actual base/head diff, focusing on actionable defects. Default to read-only findings; use for PR review requests.
---

# Pull Request Review

## Scope and safety
1. Identify PR/branch, base SHA, head SHA, and whether local files match the reviewed head. If unclear, ask or state the limitation.
2. Review the exact diff and relevant surrounding code; do not assume the current checkout equals the PR.
3. Read-only by default. Do not push, approve, merge, rebase, or modify the PR unless separately requested and authorized.

## Review method
1. Read PR description, acceptance criteria, linked issue, CI status, and prior review discussion if available.
2. Inspect changes by risk surface: correctness, security/auth, data integrity/migrations, concurrency, compatibility, error paths, observability, tests, docs, rollout.
3. For each finding, provide severity, file/line, concrete triggering scenario, impact, and a fix direction. Do not report style preferences as defects.
4. Validate findings against code/tests; deduplicate and calibrate confidence. Ask a question when evidence is insufficient.
5. Note coverage: files/surfaces inspected, checks observed, inaccessible context, and whether CI results are current for the head SHA.
6. If no findings, say no findings were identified and state limitations; never imply proof of correctness.
7. Save `.agentic/tasks/<task-id>/review.md` using `${CLAUDE_PLUGIN_ROOT}/templates/review.md` when durable tracking is useful, and check it with `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/validate_artifact.py .agentic/tasks/<task-id>/review.md`.

## Output contract
PR identity/base/head; prioritized findings; CI/test evidence; questions; review coverage and limitations. No mutation by default.

## Shared policies
Follow `${CLAUDE_PLUGIN_ROOT}/policies/approval-gates.md` and `${CLAUDE_PLUGIN_ROOT}/policies/evidence-policy.md`, including when this skill is invoked directly rather than through `/ae:ae`.
