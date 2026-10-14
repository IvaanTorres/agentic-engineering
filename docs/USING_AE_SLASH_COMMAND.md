# Using `/ae:ae` in Claude Code

Install the `ae` plugin (see the repository README), then start or restart Claude Code. The skills are available in every project.

## Examples

```text
/ae:ae Fix the discount cap bug and add a regression test
/ae:ae Add pagination to the customer API; plan first because this spans several layers
/ae:ae Investigate why CI is flaky; do not modify files yet
/ae:ae Verify the current changes and report evidence
/ae:ae Resume the interrupted task in .agentic/tasks
```

`/ae:ae` is a router and workflow contract, not a replacement for specialist skills. It reads the relevant specialist `SKILL.md` and follows that procedure. You can still call `/ae:fix`, `/ae:feature`, `/ae:verify`, `/ae:review`, etc. directly.

## Install

```text
/plugin marketplace add IvaanTorres/agentic-engineering
/plugin install ae@agentic-engineering
```

Nothing is copied into your projects. To adopt the working agreement in a project, merge `templates/CLAUDE.working-agreement.md` into that project's `CLAUDE.md`.

## Notes

- The plugin must be installed and enabled; check with `/plugin`.
- `$ARGUMENTS` carries the text following `/ae:ae`.
- This is instruction-level orchestration. Use Claude Code permissions, hooks, CI, protected branches, and deployment approvals for enforcement.
- The skills call the scripts at `${CLAUDE_PLUGIN_ROOT}/scripts/`; run `python3 <plugin path>/scripts/task_state.py --help` for the exact CLI syntax.
