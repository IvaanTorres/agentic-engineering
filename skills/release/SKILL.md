---
name: release
description: Prepare a release candidate, verify release readiness, and coordinate an explicitly approved deployment. Use when preparing a versioned release or production rollout.
---

# Release Workflow

1. Confirm requested version, target environment, release scope, and deployment owner.
2. Review merged changes, release notes, CI, tests, build artifact, migrations, feature flags, compatibility, and rollback.
3. Use `/ae:verify` and `/ae:review` against the release candidate.
4. Produce a release checklist and unresolved-risk list. Any blocker or required check failure blocks release.
5. Invoke `/ae:deploy` for preflight and approval. Do not bypass its approval gate.
6. After authorized deployment, verify health and smoke tests; record results.
7. If rollout is unhealthy, stop and follow the pre-approved mitigation/rollback path.
8. Produce a release record and document lessons from incidents or unusual failures.
