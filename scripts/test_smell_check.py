#!/usr/bin/env python3
"""Claude Code PostToolUse hook: point out false-green patterns in test code Claude just wrote.

Runs after Edit, Write and MultiEdit on test files. It never blocks: when it finds a
pattern on a line that the edit added, it returns the findings as additional context
so Claude can fix the test or keep it deliberately. See policies/testing.md.

Pattern matching gives false positives by nature; the message says so.
"""
import json
import re
import sys
from pathlib import Path

TEST_PATH = re.compile(
    r"(^|/)(tests?|__tests__|spec)/|(^|/)test_[^/]+\.py$|_test\.(py|go)$|\.(test|spec)\.[cm]?[jt]sx?$"
)

SWALLOWED = "swallows an exception, so a failure can pass silently"

# (pattern, explanation). Each one matches a single line.
LINE_SMELLS = [
    (r"\bassertIsNotNone\(|\bassert\s+[\w.\[\]]+\s+is\s+not\s+None\s*$",
     "asserts only that a value exists, not what it is"),
    (r"\bassertTrue\(\s*[\w.\[\]]+\s*\)|\bassert\s+[\w.\[\]]+\s*$",
     "asserts only that a value is truthy"),
    (r"\.toBeDefined\(\)|\.toBeTruthy\(\)|\.not\.toBeNull\(\)",
     "asserts only that a value exists or is truthy"),
    (r"expect\((true|1)\)\.toBe\((true|1)\)|\bassertTrue\(\s*True\s*\)|\bassert\s+True\b",
     "an assertion that can never fail"),
    (r"\.toMatchSnapshot\(\)",
     "a snapshot only protects behavior if someone checks it is correct"),
    (r"@(unittest\.)?skip|pytest\.mark\.(skip|xfail)|\b(it|test|describe)\.(skip|only)\(|\bx(it|describe)\(",
     "skips tests or runs only some of them"),
    (r"except(\s+\w+(\s+as\s+\w+)?)?\s*:\s*pass\b|catch\s*(\(\w*\))?\s*\{\s*\}",
     SWALLOWED),
    (r"\btime\.sleep\(|\bsetTimeout\(|\bawait\s+new\s+Promise\(\s*\w*\s*=>\s*setTimeout",
     "waits on time, which makes the test slow or flaky"),
]
MOCK_ASSERTION = re.compile(r"\.assert_(called|not_called|any_call|has_calls)\w*\(|\.toHaveBeenCalled\w*\(")
OUTCOME_ASSERTION = re.compile(
    r"\bassert(Equal|NotEqual|Raises|In|NotIn|AlmostEqual|Greater|Less|Count|Dict|List|Regex)\w*\(|"
    r"\bassert\s+.+(==|!=|<|>|\bin\b)|pytest\.raises\(|"
    r"\.to(Be|Equal|StrictEqual|Throw|Contain|HaveLength|HaveProperty|Match)\w*\("
)


def added_text(tool_name: str, tool_input: dict) -> str:
    if tool_name == "Write":
        return tool_input.get("content", "")
    if tool_name == "Edit":
        return tool_input.get("new_string", "")
    if tool_name == "MultiEdit":
        return "\n".join(edit.get("new_string", "") for edit in tool_input.get("edits", []))
    return ""


EXCEPT_LINE = re.compile(r"^\s*except(\s+[\w.]+(\s+as\s+\w+)?)?\s*:\s*$")

def line_findings(file_text: str, new_lines: set[str]) -> list[str]:
    findings = []
    previous = ""
    for number, line in enumerate(file_text.splitlines(), start=1):
        if line.strip() in new_lines:
            findings += _smells_on_line(number, line, previous)
        if line.strip():
            previous = line
    return findings


def _smells_on_line(number: int, line: str, previous: str) -> list[str]:
    if line.strip() == "pass" and EXCEPT_LINE.match(previous):
        return [f"line {number}: `{previous.strip()} pass` {SWALLOWED}"]
    for pattern, why in LINE_SMELLS:
        if re.search(pattern, line):
            return [f"line {number}: `{line.strip()[:80]}` {why}"]
    return []


def mock_only_finding(file_text: str, added: str) -> list[str]:
    if not MOCK_ASSERTION.search(added) or OUTCOME_ASSERTION.search(file_text):
        return []
    return ["the file checks only that mocks were called; no assertion checks a result, stored state or error"]


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0
    tool_input = payload.get("tool_input") or {}
    path = tool_input.get("file_path", "")
    if not TEST_PATH.search(path.replace("\\", "/")):
        return 0
    added = added_text(payload.get("tool_name", ""), tool_input)
    try:
        file_text = Path(path).read_text(encoding="utf-8")
    except OSError:
        file_text = added
    new_lines = {line.strip() for line in added.splitlines() if line.strip()}
    findings = line_findings(file_text, new_lines) + mock_only_finding(file_text, added)
    if not findings:
        return 0
    message = (
        f"Test smell check on {path} (pattern-based, may be a false positive): "
        + "; ".join(findings)
        + ". policies/testing.md in the ae plugin lists these as false-green patterns: a test that keeps "
        "passing when the behavior breaks. Either change the assertion to check the exact expected outcome, "
        "or keep it and say why."
    )
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": message}}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
