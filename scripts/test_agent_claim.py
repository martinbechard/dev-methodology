# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies atomic claim selection, worktree isolation, recovery, and release invariants.

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLAIM_SCRIPT = ROOT / "skills" / "agent-claim" / "scripts" / "claim.py"


class AgentClaimTests(unittest.TestCase):
    """Exercises the public claim command against temporary linked Git worktrees."""

    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.repository = Path(self.temporary_directory.name) / "repository"
        self.repository.mkdir()
        self.git("init")
        self.git("config", "user.email", "test@example.invalid")
        self.git("config", "user.name", "Claim Test")
        (self.repository / "README.md").write_text("baseline\n", encoding="utf-8")
        self.git("add", "README.md")
        self.git("commit", "-m", "baseline")

    def git(self, *arguments: str, worktree: Path | None = None) -> subprocess.CompletedProcess[str]:
        """Run Git in the requested temporary worktree and require success."""
        return subprocess.run(
            ["git", "-C", str(worktree or self.repository), *arguments],
            check=True,
            text=True,
            capture_output=True,
        )

    def claim(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        """Run the bundled claim command and preserve its structured output for assertions."""
        return subprocess.run(
            [sys.executable, str(CLAIM_SCRIPT), "--repo", str(self.repository), *arguments],
            check=False,
            text=True,
            capture_output=True,
        )

    def acquire_arguments(self, claim_id: str) -> list[str]:
        """Build the common acquisition arguments for one independent test task."""
        return [
            "acquire",
            "--claim-id",
            claim_id,
            "--agent",
            claim_id,
            "--task",
            f"task {claim_id}",
            "--root-task-id",
            claim_id,
        ]

    def output(self, completed: subprocess.CompletedProcess[str]) -> dict[str, object]:
        """Decode one structured command result."""
        return json.loads(completed.stdout)

    def test_first_writer_claims_clean_primary_worktree(self) -> None:
        completed = self.claim(*self.acquire_arguments("first"))

        self.assertEqual(0, completed.returncode, completed.stderr)
        result = self.output(completed)
        self.assertEqual("PRIMARY", result["outcome"])
        self.assertEqual(str(self.repository.resolve()), result["claim"]["worktree"])

    def test_second_independent_writer_gets_isolated_worktree(self) -> None:
        first = self.claim(*self.acquire_arguments("first"))
        isolated_path = Path(self.temporary_directory.name) / "isolated"
        second_arguments = self.acquire_arguments("second") + [
            "--branch",
            "codex/second",
            "--worktree-path",
            str(isolated_path),
        ]

        second = self.claim(*second_arguments)

        self.assertEqual(0, first.returncode, first.stderr)
        self.assertEqual(0, second.returncode, second.stderr)
        self.assertEqual("ISOLATE", self.output(second)["outcome"])
        self.assertTrue((isolated_path / ".git").is_file())

    def test_simultaneous_writers_cannot_both_claim_primary(self) -> None:
        commands = [
            [
                sys.executable,
                str(CLAIM_SCRIPT),
                "--repo",
                str(self.repository),
                *self.acquire_arguments(claim_id),
            ]
            for claim_id in ("first", "second")
        ]
        processes = [
            subprocess.Popen(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            for command in commands
        ]
        completed = [process.communicate() + (process.returncode,) for process in processes]
        outcomes = {json.loads(stdout)["outcome"] for stdout, _stderr, _code in completed}
        return_codes = sorted(code for _stdout, _stderr, code in completed)

        self.assertEqual([0, 4], return_codes)
        self.assertEqual({"PRIMARY", "ISOLATE_REQUIRED"}, outcomes)

    def test_overlapping_claim_waits_instead_of_creating_worktree(self) -> None:
        first = self.claim(*self.acquire_arguments("first"), "--file", "skills")
        isolated_path = Path(self.temporary_directory.name) / "blocked"
        second = self.claim(
            *self.acquire_arguments("second"),
            "--file",
            "skills/agent-claim",
            "--branch",
            "codex/blocked",
            "--worktree-path",
            str(isolated_path),
        )

        self.assertEqual(0, first.returncode, first.stderr)
        self.assertEqual(3, second.returncode)
        self.assertEqual("WAIT", self.output(second)["outcome"])
        self.assertFalse(isolated_path.exists())

    def test_dirty_unclaimed_primary_requires_explicit_recovery(self) -> None:
        (self.repository / "README.md").write_text("dirty\n", encoding="utf-8")

        completed = self.claim(*self.acquire_arguments("recovery"))

        self.assertEqual(5, completed.returncode)
        self.assertEqual("RECOVERY_REQUIRED", self.output(completed)["outcome"])

    def test_release_requires_clean_commit_or_explicit_no_change(self) -> None:
        acquired = self.claim(*self.acquire_arguments("first"))
        rejected = self.claim("release", "--claim-id", "first")
        (self.repository / "README.md").write_text("committed\n", encoding="utf-8")
        self.git("add", "README.md")
        self.git("commit", "-m", "change")
        released = self.claim("release", "--claim-id", "first")

        self.assertEqual(0, acquired.returncode, acquired.stderr)
        self.assertEqual(1, rejected.returncode)
        self.assertEqual("RELEASE_REJECTED", self.output(rejected)["outcome"])
        self.assertEqual(0, released.returncode, released.stderr)
        self.assertEqual("RELEASED", self.output(released)["outcome"])

    def test_recovery_claim_preserves_dirty_baseline_until_checkpoint_commit(self) -> None:
        (self.repository / "README.md").write_text("recovery\n", encoding="utf-8")
        acquired = self.claim(*self.acquire_arguments("recovery"), "--allow-recovery")
        rejected = self.claim("release", "--claim-id", "recovery")
        self.git("add", "README.md")
        self.git("commit", "-m", "recovery checkpoint")
        released = self.claim("release", "--claim-id", "recovery")

        self.assertEqual(0, acquired.returncode, acquired.stderr)
        self.assertEqual("RECOVER", self.output(acquired)["outcome"])
        self.assertEqual(1, rejected.returncode)
        self.assertEqual(0, released.returncode, released.stderr)


if __name__ == "__main__":
    unittest.main()
