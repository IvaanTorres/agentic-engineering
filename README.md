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

Everything is namespaced under `ae:`.

| Command | Use it for |
|---|---|
| `/ae:ae <request>` | Single entry point: routes to the right specialist skill |
| `/ae:triage` | Unclear intent, size or risk |
| `/ae:learn` | Read-only explanation of code, a branch or a concept |
| `/ae:investigate`, `/ae:plan`, `/ae:execute` | Understand, plan and implement a change |
| `/ae:feature`, `/ae:bugfix` | End-to-end workflows |
| `/ae:debug`, `/ae:spike`, `/ae:refactor`, `/ae:simplify` | Focused engineering work |
| `/ae:verify`, `/ae:review`, `/ae:pr-review`, `/ae:pr-feedback` | Evidence and review |
| `/ae:resume` | Continue interrupted work |
| `/ae:release`, `/ae:deploy` | Release preparation; deploy stops at approval gates (user-invoked only) |
| `/ae:document-solution` | Record a reusable fix or decision |

The `ae:verification-auditor` subagent gives an independent, read-only PASS/FAIL/BLOCKED verdict on whether a change is backed by fresh evidence.

## What's in the repo

```text
.claude-plugin/   plugin.json and marketplace.json
skills/           20 skills (ae entry point + 19 specialists)
agents/           verification-auditor subagent
hooks/hooks.json  PreToolUse guard for high-impact Bash commands
scripts/          task_state.py, workflow_gate.py, validate_artifact.py, guard_high_impact.py
policies/         approval gates, evidence, lifecycle, safety and continuity policies
templates/        task artifacts, plus CLAUDE.working-agreement.md to merge into a project's CLAUDE.md
docs/             toolkit design docs, audits, quickstart and release notes
evals/            evaluation cases and scorecard
tests/            unit tests for the scripts
```

Skills read shared files through `${CLAUDE_PLUGIN_ROOT}`, which Claude Code replaces with the plugin's install path. Task artifacts are written to `.agentic/tasks/<task-id>/` in the repository you are working in; add `.agentic/` to that repo's `.gitignore` if you don't want them committed.

## Guard hook

`hooks/hooks.json` runs `scripts/guard_high_impact.py` before every Bash command in every session where the plugin is enabled. It asks for confirmation before commands that look high-impact: `git push` (including force pushes), `terraform apply/destroy`, `kubectl/helm delete|upgrade`, database drops and migrations, package or container publishing, cloud CLI mutations, and `rm -rf`. It's a prompt, not a security boundary. To turn it off, disable the plugin or remove the hook from `hooks/hooks.json`.

## Development

```bash
python3 -m unittest discover -s tests   # script tests
claude plugin validate .                # plugin + marketplace manifests
```

## Differences from the account-upload kit

- The `learn` skill is named `learn`. The upload kit had it as `retrospect` (folder `ae-learn/`), so `/ae` routed to a skill name that didn't exist.
- Skills point to policies, scripts and templates under `${CLAUDE_PLUGIN_ROOT}` instead of assuming they were copied into each repo.
- Cross-references between skills use the `/ae:<name>` form.

If you also uploaded the skills to claude.ai (Customize → Skills), remove those copies after installing the plugin, or you'll have two of every skill.
