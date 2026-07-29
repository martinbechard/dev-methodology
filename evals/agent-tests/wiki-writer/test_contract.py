# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies Wiki Writer interruption handling through a deterministic offline verifier seam.

from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path

import yaml


SUITE_ROOT = Path(__file__).resolve().parent
REPOSITORY_ROOT = SUITE_ROOT.parents[2]
HARNESS_PATH = SUITE_ROOT / "executable_harness.py"
ROLE_PATH = (
    REPOSITORY_ROOT
    / "agents"
    / "roles"
    / "wiki-activities"
    / "wiki-writer.role.yaml"
)
NATIVE_ADAPTER_PATH = (
    REPOSITORY_ROOT
    / "generated"
    / "adapters"
    / "codex"
    / "agents"
    / "wiki-writer.toml"
)
VERIFIER_ADAPTER_PATH = (
    REPOSITORY_ROOT
    / "generated"
    / "adapters"
    / "codex"
    / "agents"
    / "wiki-topic-verifier.toml"
)


def _load_harness():
    """Load the offline harness from the hyphenated suite directory."""
    specification = importlib.util.spec_from_file_location(
        "wiki_writer_offline_harness",
        HARNESS_PATH,
    )
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot load Wiki Writer harness: {HARNESS_PATH}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


class WikiWriterOfflineInterruptionTests(unittest.TestCase):
    """Exercise role-owned interruption evidence without a live model."""

    @classmethod
    def setUpClass(cls) -> None:
        """Load the deterministic harness once for all interruption cases."""
        cls.harness = _load_harness()

    def test_interruption_preserves_writer_scope_and_returns_complete_packet(
        self,
    ) -> None:
        """An interrupted verifier preserves edits and yields BLOCKED evidence."""
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary)
            pages = self.harness.stage_writer_state(repository)
            result = self.harness.run_interruption_control(
                repository,
                pages,
                "interrupted",
                validation_results={
                    "lint": "PASS",
                    "okf": "PASS",
                    "leafLink": "PASS",
                },
                completed_attempts=1,
                attempt_cap=2,
            )

            self.assertEqual("BLOCKED", result["status"])
            self.assertEqual("wiki-writer", result["owner"])
            self.assertEqual(list(pages), result["pageInventory"])
            self.assertEqual(
                {"lint": "PASS", "okf": "PASS", "leafLink": "PASS"},
                result["validationResults"],
            )
            self.assertEqual(
                {
                    "agent": "wiki-topic-verifier",
                    "invocation": 2,
                    "outcome": "INTERRUPTED",
                    "boundary": "OFFLINE_PYTHON_AUDIT_MODEL",
                    "interruption": (
                        "wiki-topic-verifier became unavailable before returning a verdict"
                    ),
                },
                result["invocationReceipt"],
            )
            self.assertEqual(
                {"completed": 1, "cap": 2},
                result["correctionAttempts"],
            )
            self.assertEqual(
                result["invocationReceipt"]["interruption"],
                result["exactInterruption"],
            )
            self.assertEqual(
                result["writerState"]["before"],
                result["writerState"]["after"],
            )
            self.assertFalse(result["verifierMutatedWriterScope"])
            role_text = " ".join(
                ROLE_PATH.read_text(encoding="utf-8").split()
            )
            self.assertIn("explicit no-findings marker", role_text)
            self.assertEqual(
                {
                    "status": "NOT_RETURNED",
                    "reason": "verifier interrupted before returning a verdict",
                },
                result["verifierFindings"],
            )
            self.assertIn("exact status and diff", role_text)
            expected_status = (
                " M docs/wiki/deployment/deployment-policy.md\n"
                " M docs/wiki/deployment/index.md"
            )
            preserved = result["preservedWriterState"]
            self.assertEqual(expected_status, preserved["worktreeStatus"])
            self.assertEqual(sorted(pages), preserved["paths"])
            self.assertRegex(
                preserved["diffDigest"],
                re.compile(r"^[0-9a-f]{64}$"),
            )
            self.assertIn(
                "Rollback requires an operator-confirmed checkpoint.",
                (
                    repository
                    / "docs"
                    / "wiki"
                    / "deployment"
                    / "deployment-policy.md"
                ).read_text(encoding="utf-8"),
            )

    def test_mutating_verifier_is_rejected(self) -> None:
        """A real direct file write is rejected by the verifier process boundary."""
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary)
            pages = self.harness.stage_writer_state(repository)
            target = (
                repository
                / "docs"
                / "wiki"
                / "deployment"
                / "deployment-policy.md"
            )
            original = target.read_text(encoding="utf-8")
            with self.assertRaises(self.harness.VerifierMutationError) as captured:
                self.harness.run_interruption_control(
                    repository,
                    pages,
                    "direct-write",
                    validation_results={"lint": "PASS"},
                    completed_attempts=0,
                    attempt_cap=2,
                )
            self.assertIn(target.as_posix(), str(captured.exception))
            self.assertEqual(original, target.read_text(encoding="utf-8"))

    def test_write_then_restore_attempt_is_rejected(self) -> None:
        """Direct write-and-restore attempts are both blocked and recorded."""
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary)
            pages = self.harness.stage_writer_state(repository)
            target = (
                repository
                / "docs"
                / "wiki"
                / "deployment"
                / "deployment-policy.md"
            )
            original = target.read_text(encoding="utf-8")
            with self.assertRaises(self.harness.VerifierMutationError) as captured:
                self.harness.run_interruption_control(
                    repository,
                    pages,
                    "direct-write-restore",
                    validation_results={"lint": "PASS"},
                    completed_attempts=1,
                    attempt_cap=2,
                )
            self.assertEqual(2, str(captured.exception).count(target.as_posix()))
            self.assertEqual(original, target.read_text(encoding="utf-8"))

    def test_dir_fd_write_then_restore_attempt_is_rejected(self) -> None:
        """Relative os.open attempts through a wiki directory fd are recorded."""
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary)
            pages = self.harness.stage_writer_state(repository)
            target = repository / pages[0]
            original = target.read_bytes()

            with self.assertRaises(self.harness.VerifierMutationError) as captured:
                self.harness.run_interruption_control(
                    repository,
                    pages,
                    "dir-fd-write-restore",
                    validation_results={"lint": "PASS"},
                    completed_attempts=1,
                    attempt_cap=2,
                )

            self.assertEqual(2, str(captured.exception).count(target.as_posix()))
            self.assertEqual(original, target.read_bytes())

    def test_replace_then_restore_attempt_is_rejected(self) -> None:
        """Rename-family mutation and restore attempts are blocked and recorded."""
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary)
            pages = self.harness.stage_writer_state(repository)
            target = repository / pages[0]
            original = target.read_bytes()

            with self.assertRaises(self.harness.VerifierMutationError) as captured:
                self.harness.run_interruption_control(
                    repository,
                    pages,
                    "replace-restore",
                    validation_results={"lint": "PASS"},
                    completed_attempts=1,
                    attempt_cap=2,
                )

            self.assertEqual(2, str(captured.exception).count(target.as_posix()))
            self.assertEqual(original, target.read_bytes())

    def test_subprocess_write_attempt_is_rejected(self) -> None:
        """A process escape that could write the writer scope is blocked."""
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary)
            pages = self.harness.stage_writer_state(repository)
            target = repository / pages[0]
            original = target.read_bytes()

            with self.assertRaises(self.harness.VerifierMutationError) as captured:
                self.harness.run_interruption_control(
                    repository,
                    pages,
                    "subprocess-write",
                    validation_results={"lint": "PASS"},
                    completed_attempts=0,
                    attempt_cap=2,
                )

            self.assertIn("process:subprocess.Popen", str(captured.exception))
            self.assertEqual(original, target.read_bytes())

    def test_omitted_dirty_page_is_rejected(self) -> None:
        """The reviewed inventory must equal the complete dirty docs/wiki scope."""
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary)
            pages = self.harness.stage_writer_state(repository)
            omitted = "docs/wiki/deployment/omitted.md"
            (repository / omitted).write_text("unreviewed\n", encoding="utf-8")

            with self.assertRaises(ValueError) as captured:
                self.harness.run_interruption_control(
                    repository,
                    pages,
                    "interrupted",
                    validation_results={"lint": "PASS"},
                    completed_attempts=0,
                    attempt_cap=2,
                )

            self.assertIn(omitted, str(captured.exception))

    def test_staged_and_unstaged_pages_have_exact_git_status(self) -> None:
        """The evidence includes both index and worktree dirty states."""
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary)
            pages = self.harness.stage_writer_state(repository)
            subprocess.run(
                ["git", "add", "--", pages[0]],
                cwd=repository,
                check=True,
            )

            result = self.harness.run_interruption_control(
                repository,
                pages,
                "interrupted",
                validation_results={"lint": "PASS"},
                completed_attempts=0,
                attempt_cap=2,
            )
            (repository / pages[0]).write_text(
                "# Deployment Policy\n\nA second staged version.\n",
                encoding="utf-8",
            )
            subprocess.run(
                ["git", "add", "--", pages[0]],
                cwd=repository,
                check=True,
            )
            changed_index = self.harness.run_interruption_control(
                repository,
                pages,
                "interrupted",
                validation_results={"lint": "PASS"},
                completed_attempts=0,
                attempt_cap=2,
            )

            self.assertEqual(
                (
                    f"M  {pages[0]}\n"
                    f" M {pages[1]}"
                ),
                result["preservedWriterState"]["worktreeStatus"],
            )
            self.assertEqual(
                sorted(pages),
                result["preservedWriterState"]["paths"],
            )
            self.assertNotEqual(
                result["preservedWriterState"]["diffDigest"],
                changed_index["preservedWriterState"]["diffDigest"],
            )

    def test_untracked_bytes_change_preserved_state_digest(self) -> None:
        """Untracked page bytes contribute to the canonical SHA-256 evidence."""
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary)
            pages = self.harness.stage_writer_state(repository)
            untracked = "docs/wiki/deployment/new-leaf.md"
            target = repository / untracked
            target.write_bytes(b"first untracked bytes\n")
            inventory = (*pages, untracked)

            first = self.harness.run_interruption_control(
                repository,
                inventory,
                "interrupted",
                validation_results={"lint": "PASS"},
                completed_attempts=0,
                attempt_cap=2,
            )
            target.write_bytes(b"second untracked bytes\x00\n")
            second = self.harness.run_interruption_control(
                repository,
                inventory,
                "interrupted",
                validation_results={"lint": "PASS"},
                completed_attempts=0,
                attempt_cap=2,
            )

            self.assertIn(
                f"?? {untracked}",
                first["preservedWriterState"]["worktreeStatus"],
            )
            self.assertNotEqual(
                first["preservedWriterState"]["diffDigest"],
                second["preservedWriterState"]["diffDigest"],
            )

    def test_mode_only_change_updates_preserved_state_digest(self) -> None:
        """Git and lstat mode evidence makes a mode-only change observable."""
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary)
            pages = self.harness.stage_writer_state(repository)
            target = repository / pages[0]
            original_bytes = target.read_bytes()
            first = self.harness.run_interruption_control(
                repository,
                pages,
                "interrupted",
                validation_results={"lint": "PASS"},
                completed_attempts=0,
                attempt_cap=2,
            )

            original_mode = target.stat().st_mode & 0o777
            target.chmod(original_mode ^ 0o100)
            second = self.harness.run_interruption_control(
                repository,
                pages,
                "interrupted",
                validation_results={"lint": "PASS"},
                completed_attempts=0,
                attempt_cap=2,
            )

            self.assertEqual(original_bytes, target.read_bytes())
            self.assertNotEqual(
                first["preservedWriterState"]["diffDigest"],
                second["preservedWriterState"]["diffDigest"],
            )

    def test_deletion_is_included_in_preserved_state(self) -> None:
        """A deleted tracked page remains part of the complete dirty inventory."""
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary)
            pages = self.harness.stage_writer_state(repository)
            (repository / pages[0]).unlink()
            subprocess.run(
                ["git", "add", "--", pages[0]],
                cwd=repository,
                check=True,
            )

            result = self.harness.run_interruption_control(
                repository,
                pages,
                "interrupted",
                validation_results={"lint": "PASS"},
                completed_attempts=0,
                attempt_cap=2,
            )

            self.assertIn(
                f"D  {pages[0]}",
                result["preservedWriterState"]["worktreeStatus"],
            )
            self.assertEqual(
                sorted(pages),
                result["preservedWriterState"]["paths"],
            )

    def test_rename_and_binary_bytes_are_included_in_digest(self) -> None:
        """Rename endpoints and binary worktree bytes are preserved as evidence."""
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary)
            pages = self.harness.stage_writer_state(repository)
            renamed = "docs/wiki/deployment/renamed-policy.md"
            subprocess.run(
                ["git", "mv", "--", pages[0], renamed],
                cwd=repository,
                check=True,
            )
            target = repository / renamed
            target.write_bytes(b"\x00first binary version\xff")
            inventory = (*pages, renamed)

            first = self.harness.run_interruption_control(
                repository,
                inventory,
                "interrupted",
                validation_results={"lint": "PASS"},
                completed_attempts=0,
                attempt_cap=2,
            )
            target.write_bytes(b"\x00second binary version\xfe")
            second = self.harness.run_interruption_control(
                repository,
                inventory,
                "interrupted",
                validation_results={"lint": "PASS"},
                completed_attempts=0,
                attempt_cap=2,
            )

            preserved = first["preservedWriterState"]
            self.assertIn(pages[0], preserved["worktreeStatus"])
            self.assertIn(renamed, preserved["worktreeStatus"])
            self.assertEqual(sorted(inventory), preserved["paths"])
            self.assertNotEqual(
                preserved["diffDigest"],
                second["preservedWriterState"]["diffDigest"],
            )

    def test_production_verifier_adapter_is_read_only(self) -> None:
        """The generated production verifier uses the Codex read-only sandbox."""
        adapter = tomllib.loads(VERIFIER_ADAPTER_PATH.read_text(encoding="utf-8"))

        self.assertEqual("read-only", adapter["sandbox_mode"])
        self.assertIn(
            "fresh read-only context",
            adapter["developer_instructions"],
        )

    def test_role_and_generated_adapter_own_existing_interruption_guarantees(
        self,
    ) -> None:
        """Canonical and generated role instructions retain the exercised boundary."""
        role = yaml.safe_load(ROLE_PATH.read_text(encoding="utf-8"))
        adapter = tomllib.loads(NATIVE_ADAPTER_PATH.read_text(encoding="utf-8"))
        source_instructions = role["instructions"]
        source_text = " ".join(
            " ".join(source_instructions[section])
            for section in (
                "boundaries",
                "delegation",
                "failureHandling",
                "completion",
            )
        )
        generated_text = adapter["developer_instructions"]

        for phrase in (
            "Keep wiki-topic-verifier read-only",
            "Invoke wiki-topic-verifier",
            "Report BLOCKED when wiki-topic-verifier is unavailable",
            "Capture the verifier invocation and returned receipt",
            "writer-owned page scope immediately before and after",
            "Preserve the current unverified writer edits",
            "do not invent verifier findings",
            "intentionally leave the worktree dirty",
            "exact status and diff digest",
            "explicit no-findings marker",
            "attempted verifier write",
            "reviewed page inventory",
            "validation results",
            "completed correction attempts",
            "exact unresolved condition",
        ):
            with self.subTest(source_role_contract=phrase):
                self.assertIn(phrase, source_text)
        for phrase in (
            "Keep wiki_topic_verifier read-only",
            "Invoke wiki_topic_verifier",
            "Report BLOCKED when wiki_topic_verifier is unavailable",
            "Capture the verifier invocation and returned receipt",
            "writer-owned page scope immediately before and after",
            "Preserve the current unverified writer edits",
            "do not invent verifier findings",
            "intentionally leave the worktree dirty",
            "exact status and diff digest",
            "explicit no-findings marker",
            "attempted verifier write",
            "reviewed page inventory",
            "validation results",
            "completed correction attempts",
            "exact unresolved condition",
        ):
            with self.subTest(generated_role_contract=phrase):
                self.assertIn(phrase, generated_text)


if __name__ == "__main__":
    unittest.main()
