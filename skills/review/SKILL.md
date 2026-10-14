---
name: review
description: Review a proposed code change for correctness, regressions, security, maintainability, and alignment with requirements. Use after implementation and verification, especially before merging or releasing.
---

# Review

## Review stance
Act as a skeptical reviewer. Prioritize real defects over style preferences. Do not assume the implementer is correct.

## Procedure
1. Read the request, acceptance criteria, plan, verification evidence, and full diff. Inspect surrounding code when necessary.
2. Look for:
   - incorrect behavior and edge cases;
   - regressions and compatibility breaks;
   - security, privacy, authorization, and input-validation defects;
   - data integrity, concurrency, and failure-handling problems;
   - missing or misleading tests;
   - unnecessary complexity, duplicated logic, and scope creep;
   - configuration, migration, observability, and rollout risks.
3. For each finding, provide severity, file/line or symbol, a concrete failure scenario, and a suggested correction.
4. Verify that each finding is supported by the diff or repository evidence. Label uncertain concerns as questions, not confirmed defects.
5. Check whether the verification report accurately represents actual command results.
6. Save findings to `.agentic/tasks/<task-id>/review.md`.

## Severity
- **Blocker:** likely data loss, security compromise, severe outage, or fundamental failure.
- **High:** important functionality broken or significant exploitable risk.
- **Medium:** meaningful defect with limited scope or a significant missing safeguard.
- **Low:** minor defect or maintainability concern.
- **Question:** clarification needed; not yet a confirmed defect.

## Output contract
Start with findings ordered by severity. If no findings are identified, say "No findings identified in this review" and state what was and was not examined. Never imply that absence of findings proves absence of bugs.

## Guardrails
- Review only; do not silently modify files. Propose fixes and hand them to `/ae:execute`.
- Do not block a change for subjective preferences without a concrete benefit.
- Never approve a production action; review and deployment authorization are separate.
