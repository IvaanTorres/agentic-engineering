# Approval Gates

## Always require fresh explicit approval
- Production deployment, publishing, or release promotion.
- Destructive or irreversible database/schema/data operations.
- Deleting user data or changing retention policies.
- Modifying secrets, credentials, access permissions, security controls, or billing.
- Force-pushing, rewriting shared history, or changing protected branches.
- External actions with material cost, legal, privacy, or operational impact.
- Team-visible actions: pushing, opening, editing or merging pull requests, posting PR or issue comments and reviews, re-requesting review, changing ticket status or fields, and sending messages. Draft them; act only after approval of the exact content and target.
- Discarding local work: `git reset --hard`, `git clean -f`, `git checkout -- .`, `git restore <path>`, deleting branches or stashes.

## Approval request format
State:
1. Exact action and command/tool operation.
2. Target environment/resource and identity.
3. Expected impact and possible failure modes.
4. Verification and monitoring plan.
5. Rollback/mitigation path and whether it is safe.
6. What is not included in the approval.

Wait for explicit approval of that action and target. If scope changes, ask again.

## Implementation note
This document guides the agent; it does not enforce access control by itself. Use Claude Code permission settings, restricted credentials, branch protection, CI/CD approvals, and least-privilege cloud roles as independent controls.
