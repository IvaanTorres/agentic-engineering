# Using `/ae` in Claude Code

Install the package's `.claude/` directory into your project root (merge rather than overwrite existing project configuration), then start or restart Claude Code in that project.

## Examples

```text
/ae Fix the discount cap bug and add a regression test
/ae Add pagination to the customer API; plan first because this spans several layers
/ae Investigate why CI is flaky; do not modify files yet
/ae Verify the current changes and report evidence
/ae Resume the interrupted task in .agentic/tasks
```

`/ae` is a router and workflow contract, not a replacement for specialist skills. It reads the relevant specialist `SKILL.md` and follows that procedure. You can still call `/bugfix`, `/feature`, `/verify`, `/review`, etc. directly.

## Install

From the extracted package directory, copy `.claude/` into the target repository root. Review and merge existing `.claude/` content rather than overwriting it. Merge `CLAUDE.md` guidance as documented in the main README.

## Notes

- Claude Code must discover the skill in the current project's `.claude/skills/` directory (or a supported user-level skills location).
- `$ARGUMENTS` carries the text following `/ae`.
- This is instruction-level orchestration. Use Claude Code permissions, hooks, CI, protected branches, and deployment approvals for enforcement.
- Inspect `python scripts/task_state.py --help` for the installed script's exact CLI syntax.
