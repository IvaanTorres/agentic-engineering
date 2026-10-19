# Interview question areas

A checklist for picking questions, not a script. Keep only the questions that are unknown or inferred and would change behavior, data, the API, security, scope or tests. Weight the areas by the primary expert lens. Feature mode uses the general areas below; the other modes start from their own section and borrow general areas only where they matter.

## Behavior mode (unclear bugs)
- What should happen here, according to whom (ticket, docs, the product owner, another client)? Is there a spec or a test that encodes it?
- Who relies on the current behavior, even if it's wrong (other services, reports, users' workarounds, integrations)? Does fixing it break them?
- Is data already wrong because of the bug? Repair it, leave it, or flag it?
- Fix only the reported path, or every path with the same root cause?
- Hotfix now and a fuller fix later, or one fix?

## Spike mode
- Which decision does this spike inform, and who makes it?
- Which options are in play, and which are already ruled out and why?
- What result would make you choose each option (a number, a working path, a known blocker)?
- What is the budget, and what do we do if it runs out without an answer?
- What is out of bounds (production data, paid services, changing shared configuration)?

## Intent mode (PRs without a ticket)
- What problem does this PR solve, and for whom? Where did the request come from?
- What should a reviewer treat as the acceptance criteria?
- What did the author deliberately leave out?
- Are there parts of the diff not related to that purpose (refactors, drive-by fixes)? Should they be split out?

## Rollout mode (releases and risky migrations)
- In which order do code, migrations, configuration and flags go out? Can old and new versions run side by side during the rollout?
- Which feature flags change, for whom, and who decides when to turn them on?
- What tells us within minutes that it's broken (metrics, logs, alerts, a smoke test)?
- What triggers a rollback, who decides, and is rollback actually possible after the migration runs?
- Who is around during and after the rollout? Are there freeze windows, customer communications or dependent teams?

## Purpose and scope
- What problem does this solve, and for whom? How will we know it worked (a metric, a support ticket that stops)?
- What is explicitly out of scope for this ticket? What is the smallest version worth shipping?

## Actors and permissions
- Who can trigger this: which roles, anonymous users, admins, background jobs, other services?
- What can each actor see or do? What happens when someone without permission tries?
- Does it act on behalf of a user, a team, a tenant? Can it cross those boundaries?

## Main and alternative paths
- Walk the main path step by step: inputs, what the user sees, what is stored, what is sent.
- What other ways into the feature exist (another screen, API, import, job, deep link)?
- Can the user cancel, go back, edit or undo midway? What is kept?

## Inputs and edge cases
- Empty, missing, zero, negative, very large, duplicated, malformed, unicode or locale-specific input.
- Boundaries: limits, quotas, pagination, time zones, currencies, rounding.
- The first use (no data yet) and the heavy user (a lot of data).

## States and lifecycle
- Which states can the entity be in, and which transitions are allowed? What about stale or expired states?
- What happens to existing records created before this feature? Do they need a default or a backfill?

## Failure and concurrency
- What happens when a dependency is slow, down, or returns an error? Retry, fall back, or fail visibly?
- Two users or two tabs doing this at once; the same request sent twice (idempotency).
- Partial failure: step 2 of 3 fails. What is rolled back, and what does the user see?

## Data and compatibility
- New fields, tables or events? Migration, backfill and their reversibility.
- Who else reads this data or calls this API (other services, mobile clients, reports, exports)? Do older clients keep working?

## User experience
- Loading, empty, error and success states; the messages shown and their wording owner.
- Accessibility, mobile and responsive behavior, translations.
- Notifications, emails, or audit trail the user expects.

## Security and privacy
- Personal or sensitive data involved? Who may see it, how long it is kept, is it logged?
- Abuse paths: rate limits, enumeration, injection, cost-driving misuse.

## Non-functional
- Expected volume and latency; anything that runs per request, per item, or on a schedule.
- Cost of third-party calls or storage growth.

## Rollout and operations
- Feature flag, gradual rollout, or all at once? Who decides when it's on?
- How do we know it's broken in production (logs, metrics, alerts)? How do we turn it off?

## Acceptance and testing
- Which scenarios would QA or the product owner try first?
- What must be tested automatically, and what manually?
