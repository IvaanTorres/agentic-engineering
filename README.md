# Agentic Engineering (`ae`) — Claude Code plugin

A personal Claude Code plugin that packages the Agentic Engineering v5 toolkit: an evidence-led, human-governed software lifecycle. This repo is both the plugin and its own marketplace.

## Install on a computer

Requires Claude Code, `git` access to this repo, and `python3` (for the scripts and the guard hook).

```text
/plugin marketplace add IvaanTorres/agentic-engineering
/plugin install ae@agentic-engineering
```

Or from a shell:

```bash
claude plugin marketplace add IvaanTorres/agentic-engineering
claude plugin install ae@agentic-engineering
```

If the repo is private, Claude Code uses your existing git credentials: an SSH key loaded in `ssh-agent`, or HTTPS after `gh auth login && gh auth setup-git`. Set `CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1` if you don't use SSH.

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
| `/ae:ship` | Self-review your change against the ticket, walk you through it and challenge you on it, then commit and draft the PR (asks before pushing) |
| `/ae:pr-review` | Review a PR against its ticket and beyond the diff, challenge you with questions, draft comments without posting (`quick` skips the questions) |
| `/ae:pr-fix` | Work through review comments or CI failures, explaining each reviewer's concern |
| `/ae:resume` | Continue interrupted work |
| `/ae:release`, `/ae:deploy` | Release preparation; deploy stops at approval gates (user-invoked only) |
| `/ae:record` | Record a reusable fix or decision |

Two read-only subagents back up the skills: `ae:reviewer` gives a fresh-context second opinion as the task's expert lens (for example a frontend specialist on a UI change). It checks plans before implementation (`plan`, medium risk and up) and diffs after it (`review`, `ship`, `pr-review`). And `ae:verification-auditor` gives a PASS/FAIL/BLOCKED verdict on whether a change is backed by fresh evidence.

### How it works with a sprint team

- **Tickets first:** give `/ae` a ticket ID or URL and it reads the acceptance criteria before doing anything, flags unclear ones, and keeps out-of-scope findings as follow-ups (`policies/team-workflow.md`).
- **Expert lens everywhere:** each task gets a primary lens (frontend, backend, data, security, ...) from the code it touches, whether you start with `/ae` or call a skill directly, and the lens is passed to the reviewer subagent.
- **Tests by default:** behavior changes and bug fixes get tests (a failing regression test first for bugs); skipping one needs a stated reason (`policies/testing.md`).
- **Challenge questions:** `/ae:pr-review` and `/ae:ship` ask you 3–5 questions about the specific change (edge cases, side effects, decisions, tests) and wait for your answers, so you can defend what you approve or deliver (`policies/challenge.md`). Say `quick` to skip.
- **Reactive work:** hotfix mode in `/ae:fix`, review feedback and CI failures in `/ae:pr-fix`.
- **UI changes are checked in a browser** by `/ae:verify` (states, viewports, console, accessibility, screenshots), or marked NOT RUN with a manual checklist.

### Learning from the work

Every skill that changes, reviews or explains something non-trivial ends with a **debrief** (`policies/knowledge-transfer.md`): the decisions and the alternatives rejected, a reading order for the diff, assumptions and gaps, what to check yourself, and the key concepts. `implement` records decisions as it goes in the execution log's decisions table, so the debrief, `explain` and the PR description work from a real record instead of reconstructing reasons afterwards.

## What's in the repo

```text
.claude-plugin/   plugin.json and marketplace.json
skills/           19 skills (ae entry point + 18 specialists)
agents/           reviewer and verification-auditor subagents
hooks/hooks.json  PreToolUse guard for high-impact Bash commands
scripts/          task_state.py (opt-in task records), validate_artifact.py, guard_high_impact.py (the hook)
policies/         lifecycle, approval gates, evidence, testing, challenge questions, team/sprint workflow, knowledge transfer, safety
templates/        task artifacts, plus CLAUDE.working-agreement.md to merge into a project's CLAUDE.md
docs/             quickstart and /ae usage; docs/history/ holds the original toolkit's design docs and audits
evals/            plugin eval cases (one folder each); scenarios.json is the original toolkit's scenario list
tests/            unit tests for the scripts
```

Skills read shared files through `${CLAUDE_PLUGIN_ROOT}`, which Claude Code replaces with the plugin's install path. Task artifacts are written to `.agentic/tasks/<task-id>/` in the repository you are working in; `/ae:ae` checks whether `.agentic/` is ignored there and suggests adding it to `.gitignore` if not.

## Guard hook

`hooks/hooks.json` runs `scripts/guard_high_impact.py` before every Bash command and every connector (MCP) tool call, in every session where the plugin is enabled. It asks for confirmation before:

- **Team-visible actions:** `git push`, `gh pr|issue create/merge/comment/review/edit/close`, `gh api` writes, and connector tools whose names describe a write (for example Linear `save_issue`, GitHub `create_pull_request`, Slack `send_message`). Reads such as `gh pr view` or Linear `get_issue` pass through.
- **Discarding local work:** `git reset --hard`, `git clean -f`, `git checkout -- .`, `git restore <path>`, `git branch -D`, `git stash drop|clear`, and recursive forced `rm`.
- **Infrastructure, data and publishing:** `terraform apply/destroy`, `kubectl/helm delete|upgrade`, database drops and migrations, package or container publishing, cloud CLI mutations.

It's a prompt, not a security boundary; `policies/approval-gates.md` is the rule the skills follow. To turn the hook off, disable the plugin or edit `hooks/hooks.json`.

## Development

```bash
python3 -m unittest discover -s tests   # script tests
claude plugin validate .                # plugin + marketplace manifests
claude plugin eval . --scaffold --ablation none --allow-tools Edit Write Agent "Bash(python3:*)" "Bash(git status:*)" "Bash(git diff:*)" "Bash(git log:*)" "Bash(git show:*)" "Bash(git branch:*)" "Bash(git check-ignore:*)" "Bash(git stash:*)"
```

The eval suite runs each case in a throwaway sandbox repo (a tiny Python shop package) and checks the behaviors that matter most: `/ae` routes a bug ticket to `fix` and writes a failing test first, `ship` challenges you instead of committing, `explain` stays read-only, an unclear ticket gets questions instead of code, `review` finds a caller broken outside the diff, and `plan` gets the reviewer's critique before implementation. Each case runs once by default; pass `--runs 3` for a steadier score. Drop `--ablation none` to compare against Claude without the plugin. Results go to `evals/results/` (git-ignored).

When adding or changing a skill, follow `policies/skill-contract.md`.

## Differences from the account-upload kit

- Skills have short names: `explain` (the toolkit's `learn`, `retrospect` in the upload kit), `explore` (was `investigate`), `implement` (`execute`), `fix` (`bugfix`), `pr-fix` (`pr-feedback`) and `record` (`document-solution`). In the upload kit the explanation skill's name and the router disagreed, so routing failed.
- Skills point to policies, scripts and templates under `${CLAUDE_PLUGIN_ROOT}` instead of assuming they were copied into each repo.
- Cross-references between skills use the `/ae:<name>` form.
- `/ae:release` and `/ae:ae` hand deployment back to you, because only you can start `/ae:deploy`.
- Every template, `validate_artifact.py`, the `verification-auditor` subagent and every policy is now used by at least one skill. Each specialist links the approval-gate and evidence policies, so they still apply when you call it directly.
- The guard hook no longer prompts for harmless commands like `rm -i report.pdf`.
- `triage` is folded into `/ae:ae` and `simplify` into `/ae:refactor`; four overlapping lifecycle, continuity, expert-lens and task-state policies are merged into one short `policies/lifecycle.md`, task records are opt-in, and the metadata readiness gate (`workflow_gate.py`) was removed because nothing could ever satisfy it.
- Added `/ae:ship`, the knowledge-transfer debrief, the execution-log decisions table, and the PR/branch and agent-task modes of `/ae:explain`.

If you also uploaded the skills to claude.ai (Customize → Skills), remove those copies after installing the plugin, or you'll have two of every skill.
