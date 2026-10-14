#!/usr/bin/env python3
"""Claude Code PreToolUse hook: require an interactive permission decision for high-impact shell commands.

This is a conservative prompt-enforcement layer, NOT a complete security boundary.
Use platform permissions, least-privilege credentials, branch protections, and deployment approvals too.
"""
import json
import re
import sys

PATTERNS = [
    (r"\bgit\s+push\b.*(--force|-f\b|--force-with-lease)", "force-push / shared-history rewrite"),
    (r"\bgit\s+push\b", "external Git push"),
    (r"\b(kubectl|helm)\s+(delete|upgrade|uninstall)\b", "cluster mutation"),
    (r"\bterraform\s+(apply|destroy)\b", "infrastructure mutation"),
    (r"\b(terraform|pulumi)\s+destroy\b", "infrastructure destruction"),
    (r"\b(drop|truncate)\s+(database|table|schema)\b", "destructive database operation"),
    (r"\b(alembic|prisma|knex|sequelize)\b.*\b(migrate|deploy|reset)\b", "database migration"),
    (r"\b(npm|pnpm|yarn)\s+publish\b", "package publication"),
    (r"\bdocker\s+push\b", "container publication"),
    (r"\baws\s+.*\b(delete|put|update|create|modify)\b", "cloud resource mutation"),
    (r"\bgcloud\s+.*\b(delete|deploy|create|update)\b", "cloud resource mutation"),
    (r"\baz\s+.*\b(delete|deploy|create|update)\b", "cloud resource mutation"),
    (r"\brm\s(?=(?:[^;&|\n]*\s)?(?:-[a-z]*r|--recursive\b))(?=(?:[^;&|\n]*\s)?(?:-[a-z]*f|--force\b))", "recursive forced deletion"),
]

def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        # Fail open here to avoid breaking unrelated tool calls; platform permissions remain authoritative.
        return 0
    tool_input = payload.get("tool_input") or {}
    command = tool_input.get("command", "")
    if not isinstance(command, str):
        return 0
    matched = next(((label, pattern) for pattern, label in PATTERNS if re.search(pattern, command, re.IGNORECASE)), None)
    if not matched:
        return 0
    label, _ = matched
    response = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason": (
                f"Agentic Engineering safety check: command may perform {label}. "
                "Inspect the exact target, scope, impact, and rollback plan. "
                "Approval must be explicit and action-specific; do not approve if the command or target is unclear."
            )
        }
    }
    print(json.dumps(response))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
