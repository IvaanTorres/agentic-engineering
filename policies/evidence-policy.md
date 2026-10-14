# Evidence Policy

- Every claim about tests/build/release must be tied to actual observed output.
- Distinguish PASS, FAIL, BLOCKED, NOT RUN, and NOT APPLICABLE.
- Preserve command and exit status; summarize output rather than copying sensitive logs.
- A successful unit test suite does not prove integration, security, or product acceptance.
- Review reports should point to concrete code and plausible failure scenarios.
- Do not treat another agent's confidence as verification.
- Record environmental limitations and pre-existing failures.
