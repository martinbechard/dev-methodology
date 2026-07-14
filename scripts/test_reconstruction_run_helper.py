# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies reconstruction seed isolation, hashing, archive sealing, and retention.
# Governing design: skills/documentation-reverse-engineer/SKILL.md

from __future__ import annotations

import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path
from types import ModuleType


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
HELPER_PATH = (
    REPOSITORY_ROOT
    / "skills"
    / "documentation-reverse-engineer"
    / "scripts"
    / "reconstruction_run.py"
)
HELPER_MODULE_NAME = "documentation_reconstruction_run"


def load_helper() -> ModuleType:
    """Load the portable reconstruction helper from its distributed skill package."""
    specification = importlib.util.spec_from_file_location(
        HELPER_MODULE_NAME,
        HELPER_PATH,
    )
    if specification is None or specification.loader is None:
        raise RuntimeError(f"Unable to load reconstruction helper from {HELPER_PATH}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


class ReconstructionRunHelperTests(unittest.TestCase):
    """Exercise the helper at filesystem boundaries using disposable repositories."""

    @classmethod
    def setUpClass(cls) -> None:
        """Load the helper once so each test exercises the same public module surface."""
        cls.helper = load_helper()

    def setUp(self) -> None:
        """Create a temporary source project with a closed documentation link graph."""
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.workspace = Path(self.temporary_directory.name)
        self.source = self.workspace / "source-project"
        self.build_root = self.workspace / "reconstructed-project"
        self.archive_root = self.workspace / "archives"
        self._write(
            self.source / "docs" / "wiki" / "index.md",
            "# Wiki\n\n[Architecture](../architecture/system.md)\n",
        )
        self._write(
            self.source / "docs" / "architecture" / "system.md",
            "# Architecture\n\n[Workflow](../functional/workflow.md)\n",
        )
        self._write(
            self.source / "docs" / "functional" / "workflow.md",
            "# Workflow\n",
        )
        self._write(
            self.source / "docs" / "modules" / "unlinked.md",
            "# Unlinked module\n",
        )
        self._write(self.source / "PROJECT.yaml", "project: fixture\n")
        self._write(self.source / "AGENTS.md", "# Fixture guidance\n")
        self._write(
            self.source / "src" / "feature" / "AGENTS.md",
            "# Nested fixture guidance\n",
        )

    def _write(self, path: Path, content: str) -> None:
        """Write one UTF-8 fixture file after creating its parent directory."""
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def _initialize(self) -> dict[str, object]:
        """Initialize the standard fixture run through the helper's public API."""
        return self.helper.initialize_run(
            source_project=self.source,
            build_root=self.build_root,
            run_id="run-004",
            source_baseline="abc123",
        )

    def _create_archive_fixture(self, run_id: str) -> Path:
        """Create one complete but unsealed archive candidate for retention tests."""
        archive = self.archive_root / run_id
        required_files = {
            "RUN.json": json.dumps({"runId": run_id}),
            "reset/source-baseline.json": "{}\n",
            "configuration/PROJECT.yaml": "project: fixture\n",
            "configuration/AGENTS.md": "# Guidance\n",
            "documentation/docs/wiki/index.md": "# Wiki\n",
            (
                "reviews/reconstruction-readiness."
                "review-checklist-reconstruction-readiness.md"
            ): "# Review\n",
            "seed/seed-manifest.json": "{}\n",
            "oracle/original-baseline.json": "{}\n",
            "reconstruction/README.md": "# Reconstructed project\n",
            "parity/cases.json": "[]\n",
            "parity/reconciliation.json": "[]\n",
            "generators/delta-ledger.json": "[]\n",
            "contamination/ledger.json": "[]\n",
            "execution/commands.jsonl": "{}\n",
            "execution/results.json": "{}\n",
            "metrics/usage.json": "{}\n",
        }
        for relative_path, content in required_files.items():
            self._write(archive / relative_path, content)
        return archive

    def test_initialize_copies_wiki_first_then_linked_docs_and_configuration(self) -> None:
        """A valid run records wiki-first copy order and complete seed hashes."""
        result = self._initialize()

        manifest_path = self.build_root / ".reconstruction" / "seed-manifest.json"
        run_metadata_path = self.build_root / ".reconstruction" / "run-metadata.json"
        contamination_path = (
            self.build_root / ".reconstruction" / "contamination-ledger.json"
        )
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        run_metadata = json.loads(run_metadata_path.read_text(encoding="utf-8"))
        contamination = json.loads(contamination_path.read_text(encoding="utf-8"))

        self.assertEqual("PASS", result["validationStatus"])
        self.assertEqual(
            ["wiki-first", "linked-docs-and-config"],
            [phase["name"] for phase in manifest["copyPhases"]],
        )
        copied_paths = {entry["path"] for entry in manifest["files"]}
        self.assertEqual(
            {
                "AGENTS.md",
                "PROJECT.yaml",
                "docs/architecture/system.md",
                "docs/functional/workflow.md",
                "docs/modules/unlinked.md",
                "docs/wiki/index.md",
                "src/feature/AGENTS.md",
            },
            copied_paths,
        )
        self.assertTrue(all(len(entry["sha256"]) == 64 for entry in manifest["files"]))
        self.assertEqual("SEED_VALIDATED", run_metadata["status"])
        self.assertEqual("PASS", contamination["status"])
        self.assertEqual(
            {
                "absolute-source-paths",
                "hard-links",
                "symbolic-links",
                "workstation-home-paths",
            },
            {check["name"] for check in contamination["checks"]},
        )
        self.assertNotIn(str(self.source), manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(
            "PASS",
            self.helper.validate_seed(self.build_root, exact=True)["status"],
        )

    def test_validate_seed_detects_post_copy_tampering(self) -> None:
        """Independent validation fails when a copied input changes after initialization."""
        self._initialize()
        self._write(
            self.build_root / "docs" / "functional" / "workflow.md",
            "# Workfl0w\n",
        )

        with self.assertRaisesRegex(
            self.helper.ReconstructionRunError,
            "hash mismatch",
        ):
            self.helper.validate_seed(self.build_root, exact=True)

    def test_initialize_rejects_an_existing_build_root(self) -> None:
        """Initialization never overlays an existing destination."""
        self.build_root.mkdir()

        with self.assertRaisesRegex(
            self.helper.ReconstructionRunError,
            "brand-new build root",
        ):
            self._initialize()

    def test_initialize_records_source_evidence_links_without_copying_source(self) -> None:
        """Relative source links remain path-ledger references and never become seed files."""
        self._write(
            self.source / "docs" / "wiki" / "index.md",
            "# Wiki\n\n[Application source](../../src/main.py)\n",
        )
        self._write(self.source / "src" / "main.py", "print('source')\n")

        self._initialize()

        manifest = json.loads(
            (
                self.build_root / ".reconstruction" / "seed-manifest.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(
            [
                {
                    "document": "docs/wiki/index.md",
                    "kind": "source-evidence",
                    "target": "src/main.py",
                }
            ],
            manifest["evidenceReferences"],
        )
        self.assertFalse((self.build_root / "src" / "main.py").exists())

    def test_initialize_rejects_an_unresolved_local_link(self) -> None:
        """A missing local target is neither a valid seed dependency nor source evidence."""
        self._write(
            self.source / "docs" / "wiki" / "index.md",
            "# Wiki\n\n[Missing](../missing.md)\n",
        )

        with self.assertRaisesRegex(
            self.helper.ReconstructionRunError,
            "Unresolved local documentation link",
        ):
            self._initialize()

    @unittest.skipUnless(hasattr(os, "symlink"), "symbolic links are unavailable")
    def test_initialize_rejects_symbolic_links(self) -> None:
        """No seed file may alias source content through a symbolic link."""
        target = self.source / "docs" / "functional" / "workflow.md"
        target.unlink()
        target.symlink_to(self.source / "PROJECT.yaml")

        with self.assertRaisesRegex(
            self.helper.ReconstructionRunError,
            "symbolic link",
        ):
            self._initialize()

    @unittest.skipUnless(hasattr(os, "link"), "hard links are unavailable")
    def test_initialize_rejects_hard_links(self) -> None:
        """No seed file may retain inode identity with another source path."""
        workflow = self.source / "docs" / "functional" / "workflow.md"
        linked_copy = self.source / "docs" / "functional" / "linked-copy.md"
        os.link(workflow, linked_copy)
        self._write(
            self.source / "docs" / "architecture" / "system.md",
            "# Architecture\n\n[Workflow](../functional/linked-copy.md)\n",
        )

        with self.assertRaisesRegex(
            self.helper.ReconstructionRunError,
            "hard link",
        ):
            self._initialize()

    def test_initialize_rejects_absolute_source_paths(self) -> None:
        """Portable seed text cannot disclose or depend on the original project path."""
        self._write(
            self.source / "docs" / "functional" / "workflow.md",
            f"# Workflow\n\nOriginal source: {self.source}/src/main.py\n",
        )

        with self.assertRaisesRegex(
            self.helper.ReconstructionRunError,
            "absolute source path",
        ):
            self._initialize()

    def test_initialize_rejects_unrelated_posix_workstation_paths(self) -> None:
        """Portable configuration cannot retain another checkout's user-home path."""
        self._write(
            self.source / "PROJECT.yaml",
            "project: fixture\nevidence: /Users/example/dev/other-repo/pom.xml\n",
        )

        with self.assertRaisesRegex(
            self.helper.ReconstructionRunError,
            "workstation-specific path",
        ):
            self._initialize()

    def test_initialize_rejects_windows_workstation_paths(self) -> None:
        """Windows user-home paths are as non-portable as POSIX user-home paths."""
        self._write(
            self.source / "PROJECT.yaml",
            "project: fixture\nevidence: C:\\Users\\example\\dev\\repo\\pom.xml\n",
        )

        with self.assertRaisesRegex(
            self.helper.ReconstructionRunError,
            "workstation-specific path",
        ):
            self._initialize()

    def test_initialize_rejects_linux_workstation_paths(self) -> None:
        """Common Linux checkout roots cannot leak from an unrelated workstation."""
        self._write(
            self.source / "PROJECT.yaml",
            "project: fixture\nevidence: /home/example/dev/other-repo/pom.xml\n",
        )

        with self.assertRaisesRegex(
            self.helper.ReconstructionRunError,
            "workstation-specific path",
        ):
            self._initialize()

    def test_initialize_allows_declared_runtime_absolute_paths(self) -> None:
        """Runtime routes and portable container paths are not workstation leakage."""
        self._write(
            self.source / "PROJECT.yaml",
            (
                "project: fixture\n"
                "api_route: /management/health\n"
                "container_root: /workspace\n"
                "generator_root: /home/jhipster/app\n"
                "portable_home: ${HOME}/.cache\n"
                "scanner_pattern: '/Users/|/home/|C:\\\\Users\\\\'\n"
            ),
        )

        self.assertEqual("PASS", self._initialize()["validationStatus"])

    def test_invalid_new_archive_never_triggers_retention_pruning(self) -> None:
        """An incomplete new archive leaves every existing run untouched."""
        for index in range(1, 4):
            archive = self._create_archive_fixture(f"run-00{index}")
            self.helper.seal_archive_and_prune(
                new_archive=archive,
                archive_root=self.archive_root,
                retain=10,
                completed_at=f"2026-07-14T00:0{index}:00Z",
            )
        invalid_archive = self._create_archive_fixture("run-004")
        (invalid_archive / "parity" / "reconciliation.json").unlink()

        with self.assertRaisesRegex(
            self.helper.ReconstructionRunError,
            "required archive entry",
        ):
            self.helper.seal_archive_and_prune(
                new_archive=invalid_archive,
                archive_root=self.archive_root,
                retain=3,
                completed_at="2026-07-14T00:04:00Z",
            )

        self.assertEqual(
            {"run-001", "run-002", "run-003", "run-004"},
            {path.name for path in self.archive_root.iterdir()},
        )

    def test_valid_new_archive_is_sealed_before_newest_three_are_retained(self) -> None:
        """A verified exact-content manifest gates deletion of the oldest valid run."""
        for index in range(1, 5):
            archive = self._create_archive_fixture(f"run-00{index}")
            result = self.helper.seal_archive_and_prune(
                new_archive=archive,
                archive_root=self.archive_root,
                retain=10 if index < 4 else 3,
                completed_at=f"2026-07-14T00:0{index}:00Z",
            )

        self.assertEqual(["run-001"], result["prunedArchives"])
        self.assertEqual(
            {"run-002", "run-003", "run-004"},
            {path.name for path in self.archive_root.iterdir()},
        )
        archive_manifest = json.loads(
            (
                self.archive_root / "run-004" / "archive-manifest.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual("VALID", archive_manifest["status"])
        self.assertTrue(archive_manifest["files"])

    def test_unsealed_existing_run_blocks_retention_pruning(self) -> None:
        """Retention never ignores an incomplete sibling run in the archive root."""
        for index in range(1, 4):
            archive = self._create_archive_fixture(f"run-00{index}")
            self.helper.seal_archive_and_prune(
                new_archive=archive,
                archive_root=self.archive_root,
                retain=10,
                completed_at=f"2026-07-14T00:0{index}:00Z",
            )
        self._write(self.archive_root / "run-unsealed" / "failure.txt", "partial\n")
        new_archive = self._create_archive_fixture("run-004")

        with self.assertRaisesRegex(
            self.helper.ReconstructionRunError,
            "unsealed run",
        ):
            self.helper.seal_archive_and_prune(
                new_archive=new_archive,
                archive_root=self.archive_root,
                retain=3,
                completed_at="2026-07-14T00:04:00Z",
            )

        self.assertTrue((self.archive_root / "run-001").is_dir())
        self.assertFalse((new_archive / "archive-manifest.json").exists())


if __name__ == "__main__":
    unittest.main()
