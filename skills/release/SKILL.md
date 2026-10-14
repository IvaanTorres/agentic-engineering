---
name: release
description: Prepare a release candidate, verify release readiness, and coordinate an explicitly approved deployment. Use when preparing a versioned release or production rollout.
---

# Release Workflow

1. Confirm requested version, target environment, release scope, and deployment owner.
2. Review merged changes, release notes, CI, tests, build artifact, migrations, feature flags, compatibility, and rollback.
3. Use `/ae:verify` and `/ae:review` against the release candidate.
4. Produce a release checklist and unresolved-risk list. Any blocker or required check failure blocks release.
5. Stop and hand off. Only the user can start `/ae:deploy`, so give them the checklist and ask them to run `/ae:deploy <target>` for preflight and approval. Do not deploy from this skill or bypass the deploy approval gate.
6. After authorized deployment, verify health and smoke tests; record results.
7. If rollout is unhealthy, stop and follow the pre-approved mitigation/rollback path.
8. Produce a release record using `${CLAUDE_PLUGIN_ROOT}/templates/release-record.md` (add `${CLAUDE_PLUGIN_ROOT}/templates/incident-and-rollback.md` if the rollout had an incident or rollback), check it with `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/validate_artifact.py <path>`, and document lessons from incidents or unusual failures.

## Shared policies
Follow `${CLAUDE_PLUGIN_ROOT}/policies/approval-gates.md` and `${CLAUDE_PLUGIN_ROOT}/policies/evidence-policy.md`, including when this skill is invoked directly rather than through `/ae:ae`. When the skill changed, reviewed, or explained something non-trivial, end with the debrief from `${CLAUDE_PLUGIN_ROOT}/policies/knowledge-transfer.md`.
