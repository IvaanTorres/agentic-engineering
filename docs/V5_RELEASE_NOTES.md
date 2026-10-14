# v5 — Reliability and Lifecycle Edition

## What changed

- Added a lifecycle contract for discovery, specification, design, planning, implementation, verification, review, delivery, and operation. The contract is risk-adaptive rather than forcing every stage on every task.
- Strengthened `/ae` so it remains accountable for state reconciliation, risk escalation, current-revision evidence, and final completion reporting even when specialist skills are consulted.
- Added `scripts/workflow_gate.py`, a deterministic metadata gate for ship-ready task manifests. It requires current-HEAD passing evidence and adds review/security/release evidence requirements based on risk.
- Added threat-model, test-strategy, and incident/rollback templates.
- Added evaluation scenarios for stale evidence, conflicting resume state, release authorization, and cross-disciplinary expert routing.
- Added seven unit tests for readiness gates, bringing the package suite to 21 tests.

## Run checks

```bash
python3 -m unittest discover -s tests -v
python3 -m py_compile scripts/task_state.py scripts/guard_high_impact.py scripts/validate_artifact.py scripts/workflow_gate.py
python3 scripts/workflow_gate.py .agentic/tasks/<task-id>/task.json --repo .
```

## Limitations

- The workflow gate validates manifest structure and evidence metadata; it cannot authenticate command execution, assess whether tests are adequate, or prevent a determined actor from editing the manifest.
- Evidence freshness is checked by exact Git HEAD equality. This is conservative and may require rerunning checks after any commit, even if unrelated; matching HEAD does not prove relevant-file coverage.
- The high-impact Bash hook remains heuristic and is not a security boundary. Use Claude Code permission controls, least-privilege credentials, branch protections, CI policy, and deployment approvals.
- The evaluation scenarios are a test plan, not benchmark results. Live Claude Code end-to-end evaluation is still required.
- No production deployment, real external service, or live Paseo integration was exercised in package tests.
