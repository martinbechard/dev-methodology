# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Verifies complete workspace mutation evidence and owned-artifact cleanup behavior.
# Governing design: evals/agent-tests/implementation-plan.md

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import workspace_inventory


class WorkspaceInventoryTests(unittest.TestCase):
    def _repository(self, root: Path) -> Path:
        repository = root / "candidate"
        repository.mkdir()
        subprocess.run(["git", "init", "--quiet", str(repository)], check=True)
        (repository / ".gitignore").write_text("__pycache__/\n*.pyc\n", encoding="utf-8")
        (repository / "tracked.py").write_text("VALUE = 1\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(repository), "add", ".gitignore", "tracked.py"], check=True)
        return repository

    def test_ignored_bytecode_is_detected_cleaned_and_retained_as_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repository = self._repository(root)
            baseline_path = root / "baseline.json"
            workspace_inventory._write_json(baseline_path, workspace_inventory._inventory(repository))

            cache = repository / "__pycache__"
            cache.mkdir()
            bytecode = cache / "tracked.cpython-311.pyc"
            bytecode.write_bytes(b"generated-bytecode")
            evidence = workspace_inventory._mutation_evidence(repository, baseline_path, True)

        self.assertEqual("side-effects-detected", evidence["derivedMutationClaim"])
        self.assertEqual(
            ["__pycache__", "__pycache__/tracked.cpython-311.pyc"],
            [entry["path"] for entry in evidence["detected"]["created"]],
        )
        self.assertEqual(
            ["__pycache__", "__pycache__/tracked.cpython-311.pyc"],
            evidence["cleanup"]["removed"],
        )
        self.assertTrue(evidence["finalMatchesBaseline"])

    def test_suppressed_python_review_preserves_exact_fixture_inventory_repeatably(self) -> None:
        fixture_source = Path(__file__).parent / "dev-code-reviewer" / "fixtures" / "incomplete-review-evidence"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture = root / "incomplete-review-evidence"
            shutil.copytree(fixture_source, fixture)
            subprocess.run(["git", "init", "--quiet", str(fixture)], check=True)
            subprocess.run(["git", "-C", str(fixture), "add", "."], check=True)
            baseline_path = root / "baseline.json"
            workspace_inventory._write_json(baseline_path, workspace_inventory._inventory(fixture))
            environment = dict(os.environ)
            environment["PYTHONDONTWRITEBYTECODE"] = "1"

            for _ in range(2):
                completed = subprocess.run(
                    [sys.executable, "-m", "unittest", "test_migration.py"],
                    cwd=fixture,
                    env=environment,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)
                evidence = workspace_inventory._mutation_evidence(fixture, baseline_path, True)
                self.assertEqual("no-changes-detected", evidence["derivedMutationClaim"])
                self.assertTrue(evidence["finalMatchesBaseline"])

    def test_preexisting_ignored_and_untracked_files_are_preserved_and_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repository = self._repository(root)
            (repository / "existing.pyc").write_bytes(b"preexisting")
            (repository / "notes.txt").write_text("keep\n", encoding="utf-8")
            baseline_path = root / "baseline.json"
            workspace_inventory._write_json(baseline_path, workspace_inventory._inventory(repository))

            (repository / "generated.pyc").write_bytes(b"owned")
            evidence = workspace_inventory._mutation_evidence(repository, baseline_path, True)

            self.assertTrue((repository / "existing.pyc").is_file())
            self.assertTrue((repository / "notes.txt").is_file())

        self.assertEqual(["existing.pyc"], evidence["preExisting"]["ignored"])
        self.assertEqual(["notes.txt"], evidence["preExisting"]["untracked"])
        self.assertEqual(["generated.pyc"], evidence["cleanup"]["removed"])
        self.assertTrue(evidence["finalMatchesBaseline"])

    def test_modified_or_deleted_baseline_files_are_never_cleaned(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repository = self._repository(root)
            baseline_path = root / "baseline.json"
            workspace_inventory._write_json(baseline_path, workspace_inventory._inventory(repository))

            (repository / "tracked.py").write_text("VALUE = 2\n", encoding="utf-8")
            (repository / ".gitignore").unlink()
            evidence = workspace_inventory._mutation_evidence(repository, baseline_path, True)

            self.assertEqual("VALUE = 2\n", (repository / "tracked.py").read_text(encoding="utf-8"))
            self.assertFalse((repository / ".gitignore").exists())

        self.assertFalse(evidence["finalMatchesBaseline"])
        self.assertEqual([], evidence["cleanup"]["removed"])
        self.assertEqual(["tracked.py"], [entry["path"] for entry in evidence["detected"]["modified"]])
        self.assertEqual([".gitignore"], [entry["path"] for entry in evidence["detected"]["deleted"]])


if __name__ == "__main__":
    unittest.main()
