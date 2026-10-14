#!/usr/bin/env python3
"""Create and validate durable Agentic Engineering task manifests (stdlib only)."""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

STATES = {
    "proposed", "ready", "in_progress", "blocked", "verifying",
    "reviewing", "ready_to_ship", "completed", "abandoned"
}
RISKS = {"low", "medium", "high", "critical"}
INTENTS = {"feature", "bug", "refactor", "spike", "review", "release", "other"}
RESULTS = {"PASS", "FAIL", "BLOCKED", "NOT RUN", "NOT APPLICABLE"}
REQUIRED = {
    "schema_version", "task_id", "intent", "status", "risk", "objective",
    "scope", "repository", "acceptance_criteria", "dependencies",
    "evidence", "approvals", "blockers", "updated_at"
}
EVIDENCE_REQUIRED = {"name", "result", "command", "head_sha", "timestamp", "environment", "summary"}

def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

def git_head(cwd: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=cwd, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=True
        )
        return result.stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None

def task_path(task_id: str, repo: Path) -> Path:
    if not task_id or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for c in task_id):
        raise ValueError("task-id may contain only letters, numbers, hyphens, and underscores")
    return repo / ".agentic" / "tasks" / task_id / "task.json"

def validate(data: object) -> list[str]:
    errors = []
    if not isinstance(data, dict):
        return ["manifest must be a JSON object"]
    missing = sorted(REQUIRED - set(data))
    if missing:
        errors.append("missing fields: " + ", ".join(missing))
    if data.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if data.get("status") not in STATES:
        errors.append(f"status must be one of: {', '.join(sorted(STATES))}")
    if data.get("risk") not in RISKS:
        errors.append(f"risk must be one of: {', '.join(sorted(RISKS))}")
    if data.get("intent") not in INTENTS:
        errors.append(f"intent must be one of: {', '.join(sorted(INTENTS))}")
    for key in ("task_id", "objective", "updated_at"):
        if not isinstance(data.get(key), str) or not data[key].strip():
            errors.append(f"{key} must be a non-empty string")
    for key in ("acceptance_criteria", "dependencies", "evidence", "approvals", "blockers"):
        if not isinstance(data.get(key), list):
            errors.append(f"{key} must be an array")
    if not isinstance(data.get("scope"), dict):
        errors.append("scope must be an object")
    if not isinstance(data.get("repository"), dict):
        errors.append("repository must be an object")
    for i, record in enumerate(data.get("evidence", []) if isinstance(data.get("evidence"), list) else []):
        if not isinstance(record, dict):
            errors.append(f"evidence[{i}] must be an object")
            continue
        missing_evidence = sorted(EVIDENCE_REQUIRED - set(record))
        if missing_evidence:
            errors.append(f"evidence[{i}] missing fields: " + ", ".join(missing_evidence))
        if record.get("result") not in RESULTS:
            errors.append(f"evidence[{i}].result must be one of: {', '.join(sorted(RESULTS))}")
    return errors

def load_manifest(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except FileNotFoundError:
        return None, f"file not found: {path}"
    except json.JSONDecodeError as exc:
        return None, f"invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}"

def cmd_init(args):
    repo = args.repo.resolve()
    path = task_path(args.task_id, repo)
    if path.exists() and not args.force:
        print(f"ERROR: task already exists: {path}; use --force only if you intend to replace it", file=sys.stderr)
        return 2
    head = git_head(repo) or ""
    data = {
        "schema_version": 1,
        "task_id": args.task_id,
        "intent": args.intent,
        "status": "proposed",
        "risk": args.risk,
        "objective": args.objective,
        "scope": {"in_scope": [], "out_of_scope": []},
        "repository": {"branch": "", "base_sha": head, "head_sha": head},
        "acceptance_criteria": [],
        "dependencies": [],
        "evidence": [],
        "approvals": [],
        "blockers": [],
        "updated_at": now()
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"CREATED {path}")
    print("State: proposed. Add scope and acceptance criteria before implementation.")
    return 0

def cmd_validate(args):
    path = args.manifest
    data, error = load_manifest(path)
    if error:
        print("FAIL: " + error, file=sys.stderr)
        return 2
    errors = validate(data)
    if errors:
        print("FAIL: manifest schema validation failed")
        for err in errors:
            print("- " + err)
        return 1
    print(f"PASS: {path} matches task manifest schema v1")
    if args.check_freshness:
        repo = args.repo.resolve()
        current = git_head(repo)
        if not current:
            print("UNKNOWN: not inside a Git repository; commit freshness not checked")
            return 0
        stale = [i for i, e in enumerate(data["evidence"]) if e.get("head_sha") and e.get("head_sha") != current]
        if stale:
            print(f"STALE: {len(stale)} evidence record(s) reference a different HEAD than {current[:12]}")
            for i in stale:
                print(f"- evidence[{i}] {data['evidence'][i].get('name', '(unnamed)')}: {data['evidence'][i]['head_sha'][:12]}")
            return 3
        print(f"FRESH-HEAD: evidence records match current HEAD {current[:12]} (this does not prove all relevant files were covered)")
    return 0

def cmd_status(args):
    data, error = load_manifest(args.manifest)
    if error:
        print("ERROR: " + error, file=sys.stderr)
        return 2
    errors = validate(data)
    if errors:
        print("INVALID")
        for err in errors: print("- " + err)
        return 1
    print(f"{data['task_id']}  [{data['status']}]  risk={data['risk']}  intent={data['intent']}")
    print(f"Objective: {data['objective']}")
    print(f"Acceptance criteria: {len(data['acceptance_criteria'])}; evidence records: {len(data['evidence'])}; blockers: {len(data['blockers'])}; approvals: {len(data['approvals'])}")
    return 0

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init", help="create a new task manifest")
    init.add_argument("--id", dest="task_id", required=True)
    init.add_argument("--objective", required=True)
    init.add_argument("--intent", choices=sorted(INTENTS), default="other")
    init.add_argument("--risk", choices=sorted(RISKS), default="low")
    init.add_argument("--repo", type=Path, default=Path.cwd())
    init.add_argument("--force", action="store_true", help="replace an existing manifest (destructive)")
    init.set_defaults(func=cmd_init)
    val = sub.add_parser("validate", help="validate a task manifest")
    val.add_argument("manifest", type=Path)
    val.add_argument("--check-freshness", action="store_true", help="compare evidence head_sha values with current Git HEAD")
    val.add_argument("--repo", type=Path, default=Path.cwd())
    val.set_defaults(func=cmd_validate)
    status = sub.add_parser("status", help="show concise task status")
    status.add_argument("manifest", type=Path)
    status.set_defaults(func=cmd_status)
    args = parser.parse_args()
    try:
        return args.func(args)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
