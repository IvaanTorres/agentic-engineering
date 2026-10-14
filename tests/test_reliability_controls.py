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




class WorkflowGateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name)
        subprocess.run(["git", "init", "-q"], cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=self.repo, check=True)
        (self.repo / "README.md").write_text("test\n", encoding="utf-8")
        subprocess.run(["git", "add", "README.md"], cwd=self.repo, check=True)
        subprocess.run(["git", "commit", "-qm", "fixture"], cwd=self.repo, check=True)
        sys.path.insert(0, str(ROOT / "scripts"))
        import workflow_gate
        self.gate = workflow_gate
        self.head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=self.repo, text=True, capture_output=True, check=True).stdout.strip()

    def tearDown(self):
        self.temp.cleanup()

    def manifest(self, risk="low", intent="bug"):
        return {
            "schema_version": 1, "task_id": "gate-test", "intent": intent,
            "status": "ready_to_ship", "risk": risk, "objective": "Test readiness",
            "scope": {"in_scope": ["src"], "out_of_scope": []},
            "repository": {"branch": "main", "base_sha": self.head, "head_sha": self.head},
            "acceptance_criteria": ["expected behavior passes"], "dependencies": [],
            "evidence": [{"name": "unit tests", "result": "PASS", "command": "python -m unittest",
                          "head_sha": self.head, "timestamp": "2026-01-01T00:00:00Z",
                          "environment": "test", "summary": "passed"}],
            "approvals": [], "blockers": [], "updated_at": "2026-01-01T00:00:00Z"
        }

    def test_low_risk_passes_with_current_test_evidence(self):
        data = self.manifest()
        self.assertEqual(self.gate.readiness(data, self.head), [])

    def test_stale_evidence_blocks(self):
        data = self.manifest()
        data["evidence"][0]["head_sha"] = "old-sha"
        self.assertTrue(any("current-HEAD test/check" in b for b in self.gate.readiness(data, self.head)))

    def test_medium_risk_requires_review(self):
        data = self.manifest(risk="medium")
        self.assertTrue(any("review/audit evidence" in b for b in self.gate.readiness(data, self.head)))
        data["evidence"].append({"name": "review", "result": "PASS", "command": "review diff",
                                 "head_sha": self.head, "timestamp": "2026-01-01T00:00:00Z",
                                 "environment": "test", "summary": "no findings"})
        self.assertEqual(self.gate.readiness(data, self.head), [])

    def test_high_risk_requires_security_evidence(self):
        data = self.manifest(risk="high")
        data["evidence"].append({"name": "review", "result": "PASS", "command": "review diff",
                                 "head_sha": self.head, "timestamp": "2026-01-01T00:00:00Z",
                                 "environment": "test", "summary": "reviewed"})
        self.assertTrue(any("security/threat evidence" in b for b in self.gate.readiness(data, self.head)))

    def test_unresolved_blocker_prevents_readiness(self):
        data = self.manifest()
        data["blockers"] = ["dependency unavailable"]
        self.assertTrue(any("unresolved blocker" in b for b in self.gate.readiness(data, self.head)))

    def test_non_ship_ready_status_prevents_readiness(self):
        data = self.manifest()
        data["status"] = "in_progress"
        self.assertTrue(any("expected 'ready_to_ship'" in b for b in self.gate.readiness(data, self.head)))

    def test_critical_risk_requires_release_evidence(self):
        data = self.manifest(risk="critical")
        data["evidence"].extend([
            {"name": "review", "result": "PASS", "command": "review diff", "head_sha": self.head,
             "timestamp": "2026-01-01T00:00:00Z", "environment": "test", "summary": "reviewed"},
            {"name": "security threat model", "result": "PASS", "command": "threat model", "head_sha": self.head,
             "timestamp": "2026-01-01T00:00:00Z", "environment": "test", "summary": "reviewed"}
        ])
        self.assertTrue(any("release/rollback/preflight" in b for b in self.gate.readiness(data, self.head)))


if __name__ == "__main__":
    unittest.main()
