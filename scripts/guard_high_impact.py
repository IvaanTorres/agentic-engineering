#!/usr/bin/env python3
"""Claude Code PreToolUse hook: require an interactive permission decision for high-impact actions.

Covers Bash commands (pushes, team-visible GitHub writes, destructive local Git,
infrastructure, data and publishing) and MCP connector tools whose names describe
a write (create, update, comment, merge, send, ...).

This is a conservative prompt-enforcement layer, NOT a complete security boundary.
Use platform permissions, least-privilege credentials, branch protections, and deployment approvals too.
"""
import json
import re
import sys

PATTERNS = [
    (r"\bgit\s+push\b.*(--force|-f\b|--force-with-lease)", "force-push / shared-history rewrite"),
    (r"\bgit\s+push\b", "external Git push"),
    (r"\bgh\s+(pr|issue|release)\s+(create|merge|comment|review|close|reopen|edit|ready|delete|lock|unlock|transfer)\b",
     "team-visible GitHub change"),
    (r"\bgh\s+repo\s+(create|delete|edit|rename|archive|fork)\b", "GitHub repository change"),
    (r"\bgh\s+api\b.*(-X|--method)\s*(POST|PUT|PATCH|DELETE)\b", "GitHub API write"),
    (r"\bgh\s+api\b.*\s(-f|-F|--field|--raw-field|--input)\b", "GitHub API write"),
    (r"\bgit\s+reset\b.*--hard\b", "discarding local work"),
    (r"\bgit\s+clean\b(?=[^;&|\n]*\s-[a-z]*f)", "deleting untracked files"),
    (r"\bgit\s+checkout\s+(--\s+)?\.(\s|$)", "discarding local changes"),
    (r"\bgit\s+restore\b(?![^;&|\n]*--staged)", "discarding local changes"),
    (r"\bgit\s+branch\s+((?-i:-D)\b|--delete\s+--force\b)", "deleting a branch"),
    (r"\bgit\s+stash\s+(drop|clear)\b", "deleting stashed work"),
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

# Words in an MCP tool's action name that mean it changes something other people can see.
MCP_WRITE_WORDS = {
    "create", "save", "update", "merge", "add", "submit", "delete", "push", "send", "post",
    "comment", "reply", "forward", "trash", "untrash", "label", "unlabel", "move", "archive",
    "publish", "share", "unshare", "write", "edit", "remove", "set", "mark", "unmark", "apply",
    "restore", "retire", "fork", "schedule", "upload", "assign", "close", "reopen", "transfer",
}


def ask(reason: str) -> None:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason": (
                f"Agentic Engineering safety check: this may perform {reason}. "
                "Inspect the exact target, scope, impact, and rollback plan. "
                "Approval must be explicit and action-specific; do not approve if the action or target is unclear."
            ),
        }
    }))


def mcp_write(tool_name: str) -> bool:
    action = tool_name.split("__")[-1].lower()
    return any(word in MCP_WRITE_WORDS for word in re.split(r"[_\-]+", action))


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        # Fail open here to avoid breaking unrelated tool calls; platform permissions remain authoritative.
        return 0
    tool_name = payload.get("tool_name") or ""
    if tool_name.startswith("mcp__"):
        if mcp_write(tool_name):
            ask(f"a write through a connector ({tool_name})")
        return 0
    tool_input = payload.get("tool_input") or {}
    command = tool_input.get("command", "")
    if not isinstance(command, str):
        return 0
    label = next((label for pattern, label in PATTERNS if re.search(pattern, command, re.IGNORECASE)), None)
    if label:
        ask(label)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
