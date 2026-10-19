#!/usr/bin/env python3
"""Validate required headings/table headers in Agentic Engineering Markdown artifacts.

This checks document structure only. It does not prove that claims are true.
"""
from pathlib import Path
import argparse
import re
import sys

# Required headings are matched against Markdown heading lines, not arbitrary prose.
REQUIRED_HEADINGS = {
    "investigation.md": [
        "Observed facts", "Hypotheses (not confirmed facts)", "Risks and constraints",
        "Recommended next step"
    ],
    "plan.md": [
        "Objective", "Acceptance criteria", "Tasks", "Test and verification strategy",
        "Human approval gates"
    ],
    "verification.md": [
        "Commands run", "Checks not run and why", "Coverage gaps and residual risks",
        "Recommended next step"
    ],
    "review.md": ["Findings (highest severity first)", "Checks performed", "Verdict"],
    "execution-log.md": ["Decisions", "Steps", "Deviations from plan"],
    "interview.md": ["Feature map", "Decisions", "Scenarios and edge cases", "Assumptions", "Changes for the plan", "End-to-end verification"],
}
REQUIRED_LABELS = {
    "release-record.md": ["Environment", "Explicit approver and approval reference", "Smoke tests / health checks", "Result"]
}
REQUIRED_TABLE_HEADERS = {
    "verification.md": ["Acceptance criterion", "Evidence / command", "Result (PASS/FAIL/BLOCKED)"],
    "execution-log.md": ["Decision", "Alternatives considered", "Why this one"],
    "interview.md": ["Question", "Answer", "Implication", "Scenario", "Given / When", "Expected behavior"],
}

def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().casefold())

def extract_headings(content: str) -> set[str]:
    headings = set()
    for line in content.splitlines():
        match = re.match(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$", line)
        if match:
            headings.add(normalize(match.group(1)))
    return headings

def extract_table_headers(content: str) -> set[str]:
    headers = set()
    lines = content.splitlines()
    for index, line in enumerate(lines[:-1]):
        line = line.strip()
        next_line = lines[index + 1].strip()
        if not line.startswith("|") or line.count("|") < 2:
            continue
        if not next_line.startswith("|"):
            continue
        cells = [normalize(cell.strip().strip("`")) for cell in line.strip("|").split("|")]
        separators = [cell.strip() for cell in next_line.strip("|").split("|")]
        if cells and len(cells) == len(separators) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in separators):
            headers.update(cells)
    return headers

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact", type=Path, help="Markdown artifact to validate")
    args = parser.parse_args()
    path = args.artifact
    if not path.is_file():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 2
    content = path.read_text(encoding="utf-8")
    headings_required = REQUIRED_HEADINGS.get(path.name)
    tables_required = REQUIRED_TABLE_HEADERS.get(path.name, [])
    labels_required = REQUIRED_LABELS.get(path.name, [])
    if headings_required is None and not tables_required and not labels_required:
        print(f"INFO: no required-section rules for {path.name}")
        return 0
    headings = extract_headings(content)
    table_headers = extract_table_headers(content)
    normalized_content = normalize(content)
    missing_headings = [h for h in headings_required or [] if normalize(h) not in headings]
    missing_tables = [h for h in tables_required if normalize(h) not in table_headers]
    missing_labels = [h for h in labels_required if normalize(h) not in normalized_content]
    if missing_headings or missing_tables or missing_labels:
        print("FAIL: missing required headings/table headers/field labels:")
        for term in missing_headings:
            print(f"- heading: {term}")
        for term in missing_tables:
            print(f"- table header: {term}")
        for term in missing_labels:
            print(f"- field label: {term}")
        return 1
    print(f"PASS: required headings/table headers found in {path}")
    print("Note: this checks structure only; it does not validate factual correctness.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
