# Agentic Engineering (`ae`) — Claude Code plugin

A personal Claude Code plugin that packages the Agentic Engineering v5 toolkit: an evidence-led, human-governed software lifecycle. This repo is both the plugin and its own marketplace.

## Install on a computer

Requires Claude Code, `git` access to this repo, and `python3` (for the scripts and the guard hook).

```text
/plugin marketplace add <owner>/<repo>
/plugin install ae@agentic-engineering
```

Or from a shell:

```bash
claude plugin marketplace add <owner>/<repo>
claude plugin install ae@agentic-engineering
```

For a private GitHub repo, Claude Code uses your existing git credentials: an SSH key loaded in `ssh-agent`, or HTTPS after `gh auth login && gh auth setup-git`. Set `CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1` if you don't use SSH.

To try it without installing, from a clone: `claude --plugin-dir /path/to/this/repo`.

## Updates

The plugin has no `version` field, so installs follow the latest commit.

- Turn on auto-update once per computer: `/plugin` → **Marketplaces** → `agentic-engineering` → **Enable auto-update**.
- Or update by hand: `/plugin marketplace update agentic-engineering`, then `claude plugin update ae@agentic-engineering`.
- Running sessions keep the version they loaded; run `/reload-plugins` to pick up an update.

## Usage

Everything is namespaced under `ae:`. Skills whose names don't clash with a built-in command also work without the prefix (`/ae`, `/explain`, `/fix`), but `/review`, `/plan`, `/resume` and similar built-in names need the `ae:` prefix.

| Command | Use it for |
|---|---|
| `/ae <request>` | Entry point: classifies the request and routes to the lightest suitable skill |
| `/ae:explain` | Learn: explain code or a concept, walk through a PR/branch as a story of decisions, or review what an agent did in a task |
| `/ae:explore`, `/ae:plan`, `/ae:implement` | Understand, plan and implement a change |
| `/ae:feature`, `/ae:fix` | End-to-end workflows, ending in `/ae:ship` |
| `/ae:debug`, `/ae:spike`, `/ae:refactor` | Focused work; `refactor` includes a simplify pass |
| `/ae:verify`, `/ae:review` | Evidence and review of local changes |
| `/ae:ship` | Commit, write the PR description from decisions and evidence, open the PR (asks before pushing) |
| `/ae:pr-review`, `/ae:pr-fix` | Review a PR; work through review comments or CI feedback |
| `/ae:resume` | Continue interrupted work |
| `/ae:release`, `/ae:deploy` | Release preparation; deploy stops at approval gates (user-invoked only) |
| `/ae:record` | Record a reusable fix or decision |

The `ae:verification-auditor` subagent gives an independent, read-only PASS/FAIL/BLOCKED verdict on whether a change is backed by fresh evidence.

### Learning from the work

Every skill that changes, reviews or explains something non-trivial ends with a **debrief** (`policies/knowledge-transfer.md`): the decisions and the alternatives rejected, a reading order for the diff, assumptions and gaps, what to check yourself, and the key concepts. `implement` records decisions as it goes in the execution log's decisions table, so the debrief, `explain` and the PR description work from a real record instead of reconstructing reasons afterwards.

## What's in the repo

```text
.claude-plugin/   plugin.json and marketplace.json
skills/           19 skills (ae entry point + 18 specialists)
agents/           verification-auditor subagent
hooks/hooks.json  PreToolUse guard for high-impact Bash commands
scripts/          task_state.py, workflow_gate.py, validate_artifact.py, guard_high_impact.py
policies/         approval gates, evidence, knowledge transfer, expert lenses, lifecycle, safety and continuity
templates/        task artifacts, plus CLAUDE.working-agreement.md to merge into a project's CLAUDE.md
docs/             quickstart and /ae usage; docs/history/ holds the original toolkit's design docs and audits
evals/            evaluation cases and scorecard
tests/            unit tests for the scripts
```

Skills read shared files through `${CLAUDE_PLUGIN_ROOT}`, which Claude Code replaces with the plugin's install path. Task artifacts are written to `.agentic/tasks/<task-id>/` in the repository you are working in; `/ae:ae` checks whether `.agentic/` is ignored there and suggests adding it to `.gitignore` if not.

## Guard hook

`hooks/hooks.json` runs `scripts/guard_high_impact.py` before every Bash command in every session where the plugin is enabled. It asks for confirmation before commands that look high-impact: `git push` (including force pushes), `terraform apply/destroy`, `kubectl/helm delete|upgrade`, database drops and migrations, package or container publishing, cloud CLI mutations, and recursive forced deletes (`rm` with both a recursive and a force flag, such as `rm -rf` or `rm -r -f`). It's a prompt, not a security boundary. To turn it off, disable the plugin or remove the hook from `hooks/hooks.json`.

## Development

```bash
python3 -m unittest discover -s tests   # script tests
claude plugin validate .                # plugin + marketplace manifests
```

When adding or changing a skill, follow `policies/skill-contract.md`.

## Differences from the account-upload kit

- Skills have short names: `explain` (the toolkit's `learn`, `retrospect` in the upload kit), `explore` (was `investigate`), `implement` (`execute`), `fix` (`bugfix`), `pr-fix` (`pr-feedback`) and `record` (`document-solution`). In the upload kit the explanation skill's name and the router disagreed, so routing failed.
- Skills point to policies, scripts and templates under `${CLAUDE_PLUGIN_ROOT}` instead of assuming they were copied into each repo.
- Cross-references between skills use the `/ae:<name>` form.
- `/ae:release` and `/ae:ae` hand deployment back to you, because only you can start `/ae:deploy`.
- Every template, `validate_artifact.py`, the `verification-auditor` subagent and every policy is now used by at least one skill. Each specialist links the approval-gate and evidence policies, so they still apply when you call it directly.
- The guard hook no longer prompts for harmless commands like `rm -i report.pdf`.
- `triage` is folded into `/ae:ae` and `simplify` into `/ae:refactor`; the expert-role descriptions moved to `policies/expert-lenses.md` so `/ae:ae` loads less on every call.
- Added `/ae:ship`, the knowledge-transfer debrief, the execution-log decisions table, and the PR/branch and agent-task modes of `/ae:explain`.

If you also uploaded the skills to claude.ai (Customize → Skills), remove those copies after installing the plugin, or you'll have two of every skill.
