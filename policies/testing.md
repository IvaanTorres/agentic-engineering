# Testing

Tests are the default for any change that alters behavior. Skipping them is allowed, but it is a decision that must be stated with a reason, never a silent omission.

## When a test is required

| Change | Default |
|---|---|
| Bug fix | Regression test that fails before the fix and passes after it. Show both runs when feasible. |
| New or changed behavior, branch, validation rule, or error path | Tests for the main path and the edge cases named in the acceptance criteria or found during review. |
| Public API, contract, schema, or serialization change | Test at the boundary (request/response, schema, consumer-facing type). |
| Refactor or simplification | Existing tests must cover the touched behavior; if they don't, add characterization tests first. |
| Config, copy, docs, styling-only, generated code, dependency bump | Usually no new test; run the existing suite or the relevant build/type check instead. |
| Spike or throwaway prototype | None, but label the code as unverified. |

When in doubt, write the test. If you skip one where the table says it is required, record why (for example "no test harness for this layer; covered by manual check X") in the execution log and the PR description.

## How

- Follow the repository's conventions: framework, file location, naming, fixtures, and test style. Look at neighboring tests before writing new ones.
- Test behavior through the public surface, not implementation details. One clear reason to fail per test.
- Cover the edge cases that matter for this change: empty/null/missing values, boundaries, error and permission paths, concurrency or ordering when relevant, and backward compatibility.
- A test that passes without the change protects nothing. For fixes and new behavior, confirm it fails without the change (temporarily reverting or reasoning explicitly from the code) when practical.
- Never delete, skip, or loosen an existing test to get green. If an existing test is wrong, say why and change it deliberately.
- Run the narrowest relevant tests first, then the broader suite in proportion to risk. If tests cannot run locally (missing dependencies, broken environment), report that as BLOCKED with the exact error; don't repair the environment without asking.
