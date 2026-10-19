import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import task_state

class TaskStateTests(unittest.TestCase):
    def valid_manifest(self):
        return {
            "schema_version": 1, "task_id": "task-1", "intent": "bug",
            "status": "in_progress", "risk": "medium", "objective": "Fix the bug",
            "scope": {"in_scope": ["src"], "out_of_scope": []},
            "repository": {"branch": "main", "base_sha": "abc", "head_sha": "abc"},
            "acceptance_criteria": ["regression test passes"], "dependencies": [],
            "evidence": [], "approvals": [], "blockers": [], "updated_at": "2026-01-01T00:00:00+00:00"
        }

    def test_valid_manifest(self):
        self.assertEqual(task_state.validate(self.valid_manifest()), [])

    def test_missing_required_field_fails(self):
        data = self.valid_manifest()
        del data["acceptance_criteria"]
        self.assertTrue(any("acceptance_criteria" in e for e in task_state.validate(data)))

    def test_unknown_state_fails(self):
        data = self.valid_manifest()
        data["status"] = "done-ish"
        self.assertTrue(any("status must be" in e for e in task_state.validate(data)))

    def test_evidence_requires_sha_and_result(self):
        data = self.valid_manifest()
        data["evidence"] = [{"name": "unit", "result": "PASS"}]
        errors = task_state.validate(data)
        self.assertTrue(any("evidence[0] missing fields" in e for e in errors))


    def test_init_refuses_to_overwrite_existing_manifest(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            target = task_state.task_path("task-1", repo)
            target.parent.mkdir(parents=True)
            target.write_text("preserve-me", encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "task_state.py"), "init",
                 "--id", "task-1", "--objective", "Example", "--repo", str(repo)],
                text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            self.assertEqual(proc.returncode, 2)
            self.assertEqual(target.read_text(encoding="utf-8"), "preserve-me")

    def test_invalid_json_is_reported(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "task.json"
            path.write_text("{broken", encoding="utf-8")
            data, error = task_state.load_manifest(path)
            self.assertIsNone(data)
            self.assertIn("invalid JSON", error)

class HighImpactGuardTests(unittest.TestCase):
    def run_guard(self, command):
        payload = json.dumps({"tool_name": "Bash", "tool_input": {"command": command}})
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "guard_high_impact.py")],
            input=payload, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        return proc.returncode, proc.stdout

    def test_force_push_requests_permission(self):
        code, output = self.run_guard("git push --force origin main")
        self.assertEqual(code, 0)
        self.assertIn('"permissionDecision": "ask"', output)

    def test_deploy_requests_permission(self):
        code, output = self.run_guard("terraform apply")
        self.assertIn('"permissionDecision": "ask"', output)


    def test_recursive_delete_requests_permission(self):
        code, output = self.run_guard("rm -rf ./build")
        self.assertEqual(code, 0)
        self.assertIn('"permissionDecision": "ask"', output)

    def test_split_recursive_force_flags_request_permission(self):
        for command in ("rm -r -f ./build", "rm -fr ./build", "rm --recursive --force ./build"):
            code, output = self.run_guard(command)
            self.assertIn('"permissionDecision": "ask"', output, command)

    def test_non_recursive_rm_does_not_prompt(self):
        for command in ("rm -i report.pdf", "rm -f notes.txt", "rm file-rf.txt"):
            code, output = self.run_guard(command)
            self.assertEqual(output, "", command)

    def test_team_visible_github_writes_request_permission(self):
        for command in ("gh pr create --fill", "gh pr merge 5", "gh pr comment 5 -b hi",
                        "gh api -X POST repos/o/r/issues/1/comments", "gh api repos/o/r/issues -f title=x"):
            code, output = self.run_guard(command)
            self.assertIn('"permissionDecision": "ask"', output, command)

    def test_github_reads_do_not_prompt(self):
        for command in ("gh pr view 5", "gh pr diff 5", "gh api repos/o/r/pulls/5/comments"):
            code, output = self.run_guard(command)
            self.assertEqual(output, "", command)

    def test_discarding_local_work_requests_permission(self):
        for command in ("git reset --hard HEAD~1", "git clean -fd", "git checkout -- .",
                        "git restore src/a.py", "git branch -D old", "git stash drop"):
            code, output = self.run_guard(command)
            self.assertIn('"permissionDecision": "ask"', output, command)

    def test_safe_local_git_does_not_prompt(self):
        for command in ("git reset HEAD a.py", "git clean -n", "git checkout main",
                        "git restore --staged a.py", "git branch -d merged", "git stash list"):
            code, output = self.run_guard(command)
            self.assertEqual(output, "", command)

    def run_mcp(self, tool_name):
        payload = json.dumps({"tool_name": tool_name, "tool_input": {}})
        return subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "guard_high_impact.py")],
            input=payload, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        ).stdout

    def test_connector_writes_request_permission(self):
        for tool in ("mcp__claude_ai_Linear__save_issue", "mcp__plugin_github_github__create_pull_request",
                     "mcp__plugin_github_github__pull_request_review_write", "mcp__claude_ai_Slack__slack_send_message"):
            self.assertIn('"permissionDecision": "ask"', self.run_mcp(tool), tool)

    def test_connector_reads_and_browser_do_not_prompt(self):
        for tool in ("mcp__claude_ai_Linear__get_issue", "mcp__plugin_github_github__list_pull_requests",
                     "mcp__plugin_chrome-devtools-mcp_chrome-devtools__click", "mcp__context7__resolve-library-id"):
            self.assertEqual(self.run_mcp(tool), "", tool)

    def test_read_only_command_does_not_prompt(self):
        code, output = self.run_guard("git status --short")
        self.assertEqual(code, 0)
        self.assertEqual(output, "")


class ArtifactValidatorTests(unittest.TestCase):
    def run_validator(self, content, filename="verification.md"):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / filename
            path.write_text(content, encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "validate_artifact.py"), str(path)],
                text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )

    def test_required_heading_in_prose_is_not_enough(self):
        proc = self.run_validator(
            "This paragraph mentions Commands run and Recommended next step.\n"
            "## Random heading\nSome text\n",
            "verification.md"
        )
        self.assertEqual(proc.returncode, 1)
        self.assertIn("heading: Commands run", proc.stdout)

    def test_verification_template_structure_passes(self):
        proc = self.run_validator((ROOT / "templates" / "verification.md").read_text(), "verification.md")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)


    def test_release_record_template_structure_passes(self):
        proc = self.run_validator((ROOT / "templates" / "release-record.md").read_text(), "release-record.md")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("PASS:", proc.stdout)

    def test_execution_log_template_structure_passes(self):
        proc = self.run_validator((ROOT / "templates" / "execution-log.md").read_text(), "execution-log.md")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_execution_log_requires_decisions_table(self):
        proc = self.run_validator("## Decisions\n## Steps\n## Deviations from plan\n", "execution-log.md")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("table header: Alternatives considered", proc.stdout)

    def test_review_template_structure_passes(self):
        proc = self.run_validator((ROOT / "templates" / "review.md").read_text(), "review.md")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_interview_template_structure_passes(self):
        proc = self.run_validator((ROOT / "templates" / "interview.md").read_text(), "interview.md")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_interview_requires_decisions_table(self):
        content = "## Feature map\n## Decisions\n## Scenarios and edge cases\n## Assumptions\n## Changes for the plan\n## End-to-end verification\n"
        proc = self.run_validator(content, "interview.md")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("table header: Implication", proc.stdout)


if __name__ == "__main__":
    unittest.main()
