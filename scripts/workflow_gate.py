#!/usr/bin/env python3
"""Deterministic readiness gate for Agentic Engineering task manifests.

This checks manifest structure and evidence metadata; it does not prove that
commands were honestly run or that tests are adequate. CI and platform controls
remain authoritative for release/deployment authorization.
"""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import task_state


def git_head(repo: Path) -> str | None:
    try:
        p = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, text=True,
                           stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=True)
        return p.stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def readiness(data: dict, current_head: str | None) -> list[str]:
    blockers: list[str] = []
    schema_errors = task_state.validate(data)
    blockers.extend(f"invalid manifest: {e}" for e in schema_errors)
    if schema_errors:
        return blockers
    if data.get("status") not in {"ready_to_ship", "completed"}:
        blockers.append(f"status is {data.get('status')!r}; expected 'ready_to_ship' or 'completed'")
    criteria = data.get("acceptance_criteria", [])
    if not criteria or not all(isinstance(c, str) and c.strip() for c in criteria):
        blockers.append("acceptance criteria are missing or contain empty entries")
    if data.get("blockers"):
        blockers.append(f"task has {len(data['blockers'])} unresolved blocker(s)")
    if not current_head:
        blockers.append("current Git HEAD unavailable; evidence freshness cannot be established")
    evidence = data.get("evidence", [])
    passing = []
    for item in evidence:
        if not isinstance(item, dict) or item.get("result") != "PASS":
            continue
        sha = item.get("head_sha", "")
        if not sha or not current_head or sha != current_head:
            continue
        passing.append(item)
    def has_token(tokens):
        return any(any(t in str(e.get("name", "")).lower() for t in tokens) for e in passing)
    if not has_token(("test", "check", "ci", "build")):
        blockers.append("no passing, current-HEAD test/check/CI/build evidence")
    risk = data.get("risk", "low")
    if risk in {"medium", "high", "critical"} and not has_token(("review", "audit")):
        blockers.append("no passing, current-HEAD review/audit evidence for medium-or-higher risk")
    if risk in {"high", "critical"} and not has_token(("security", "threat")):
        blockers.append("no passing, current-HEAD security/threat evidence for high-or-critical risk")
    if data.get("intent") == "release" or risk == "critical":
        if not has_token(("release", "rollback", "deployment preflight")):
            blockers.append("no passing, current-HEAD release/rollback/preflight evidence")
    return blockers


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    args = parser.parse_args()
    manifest, error = task_state.load_manifest(args.manifest)
    if error:
        print("BLOCKED: " + error)
        return 2
    blockers = readiness(manifest, git_head(args.repo.resolve()))
    if blockers:
        print("NOT READY")
        for b in blockers:
            print(f"- {b}")
        print("Note: metadata checks do not independently prove evidence authenticity or adequacy.")
        return 1
    print("READY: manifest meets configured evidence metadata gates for the current Git HEAD")
    print("Note: this is not deployment authorization and does not prove evidence authenticity or adequacy.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
