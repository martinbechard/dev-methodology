# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies exact-path manifests and path-limited Git commits for file-backed backlog records.
# Design: design/work-item-provider-and-completion-contracts.md

from __future__ import annotations

import subprocess
import tempfile
import unittest
from dataclasses import dataclass
from pathlib import Path, PurePosixPath


class _InvalidManifest(ValueError):
    """Report an invalid exact provider-path manifest."""


@dataclass(frozen=True)
class _ProviderPathManifest:
    """Describe the explicit provider paths for one backlog operation."""

    operation: str
    paths: tuple[str, ...] | None
    scope_source: str = "explicit"
    source_path: str | None = None
    destination_path: str | None = None
    current_paths: tuple[str, ...] = ()
    created_paths: tuple[str, ...] = ()
    atomic_rationale: str | None = None


def _validated_manifest_paths(manifest: _ProviderPathManifest) -> tuple[str, ...]:
    """Return canonical manifest paths after validating the operation shape."""
    if manifest.scope_source != "explicit":
        raise _InvalidManifest("provider paths must be explicit")
    if not manifest.paths:
        raise _InvalidManifest("provider-path manifest is missing")

    paths = manifest.paths
    if len(set(paths)) != len(paths):
        raise _InvalidManifest("provider-path manifest contains duplicates")
    for path in paths:
        candidate = PurePosixPath(path)
        if (
            candidate.is_absolute()
            or ".." in candidate.parts
            or "." in candidate.parts
            or "\\" in path
            or any(token in path for token in ("*", "?", "[", "]"))
            or len(candidate.parts) < 3
            or candidate.parts[0] != "backlog"
            or candidate.suffix != ".md"
        ):
            raise _InvalidManifest(f"non-canonical provider path: {path}")

    if manifest.operation in {"create", "update"}:
        if len(paths) != 1:
            raise _InvalidManifest(
                f"{manifest.operation} requires exactly one path"
            )
    elif manifest.operation in {"move", "archive"}:
        if len(paths) != 2:
            raise _InvalidManifest("move or archive requires exactly two paths")
        if not manifest.source_path or not manifest.destination_path:
            raise _InvalidManifest("move or archive endpoint is missing")
        if (manifest.source_path, manifest.destination_path) != paths:
            raise _InvalidManifest("move or archive endpoints differ from manifest")
    elif manifest.operation == "atomic":
        if len(paths) < 2:
            raise _InvalidManifest("atomic operation requires at least two paths")
        if not manifest.atomic_rationale or not manifest.atomic_rationale.strip():
            raise _InvalidManifest("atomic rationale is missing")
        roles = (*manifest.current_paths, *manifest.created_paths)
        if (
            set(manifest.current_paths).intersection(manifest.created_paths)
            or roles != paths
        ):
            raise _InvalidManifest("atomic path roles differ from manifest")
    else:
        raise _InvalidManifest(f"unknown operation: {manifest.operation}")
    return paths


def _mutating_argv(
    manifest: _ProviderPathManifest, message: str
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """Build exact path-limited add and commit argument vectors."""
    paths = _validated_manifest_paths(manifest)
    return (
        ("git", "add", "--", *paths),
        ("git", "commit", "--only", "-m", message, "--", *paths),
    )


class PathLimitedBacklogGitTests(unittest.TestCase):
    """Exercise the file-provider contract without modeling coordination or races."""

    def setUp(self) -> None:
        self._temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self._temporary_directory.cleanup)
        self.repository = Path(self._temporary_directory.name)
        self._git("init", "-q")
        self._git("config", "user.name", "Contract Test")
        self._git("config", "user.email", "contract@example.invalid")

        self._write("README.md", b"base\n")
        self._write("notes.txt", b"clean\n")
        self._write(
            "backlog/defect-backlog/update.md",
            self._work_item("backlog/defect-backlog/update.md"),
        )
        self._write(
            "backlog/feature-backlog/move.md",
            self._work_item("backlog/feature-backlog/move.md"),
        )
        self._git("add", "--", "README.md", "notes.txt", "backlog")
        self._git("commit", "-m", "Initial fixture")

    def test_allowed_manifest_shapes_build_exact_path_limited_argv(self) -> None:
        cases = (
            _ProviderPathManifest(
                "create", ("backlog/feature-backlog/create.md",)
            ),
            _ProviderPathManifest(
                "update", ("backlog/defect-backlog/update.md",)
            ),
            _ProviderPathManifest(
                "move",
                (
                    "backlog/feature-backlog/move.md",
                    "backlog/completed-backlog/features/move.md",
                ),
                source_path="backlog/feature-backlog/move.md",
                destination_path="backlog/completed-backlog/features/move.md",
            ),
            _ProviderPathManifest(
                "archive",
                (
                    "backlog/defect-backlog/update.md",
                    "backlog/completed-backlog/defects/update.md",
                ),
                source_path="backlog/defect-backlog/update.md",
                destination_path="backlog/completed-backlog/defects/update.md",
            ),
            _ProviderPathManifest(
                "atomic",
                (
                    "backlog/future-ideas/idea.md",
                    "backlog/feature-backlog/promoted.md",
                ),
                current_paths=("backlog/future-ideas/idea.md",),
                created_paths=("backlog/feature-backlog/promoted.md",),
                atomic_rationale="Keep reciprocal promotion links together.",
            ),
        )

        for manifest in cases:
            with self.subTest(operation=manifest.operation):
                add_argv, commit_argv = _mutating_argv(manifest, "Exact paths")
                self.assertEqual(("git", "add", "--", *manifest.paths), add_argv)
                self.assertEqual(
                    (
                        "git",
                        "commit",
                        "--only",
                        "-m",
                        "Exact paths",
                        "--",
                        *manifest.paths,
                    ),
                    commit_argv,
                )

    def test_invalid_manifest_shapes_are_rejected(self) -> None:
        invalid = (
            _ProviderPathManifest("create", None),
            _ProviderPathManifest(
                "create",
                ("backlog/feature-backlog/inferred.md",),
                scope_source="title-derived",
            ),
            _ProviderPathManifest("create", ("backlog/*/item.md",)),
            _ProviderPathManifest("create", ("backlog/feature-backlog",)),
            _ProviderPathManifest(
                "create",
                (
                    "backlog/feature-backlog/one.md",
                    "backlog/feature-backlog/two.md",
                ),
            ),
            _ProviderPathManifest(
                "move",
                (
                    "backlog/feature-backlog/source.md",
                    "backlog/completed-backlog/features/destination.md",
                ),
                source_path="backlog/feature-backlog/source.md",
            ),
            _ProviderPathManifest(
                "move",
                (
                    "backlog/feature-backlog/source.md",
                    "backlog/completed-backlog/features/destination.md",
                ),
                source_path="backlog/feature-backlog/other.md",
                destination_path="backlog/completed-backlog/features/destination.md",
            ),
            _ProviderPathManifest(
                "atomic",
                (
                    "backlog/future-ideas/idea.md",
                    "backlog/feature-backlog/promoted.md",
                ),
                current_paths=("backlog/future-ideas/idea.md",),
                created_paths=("backlog/feature-backlog/promoted.md",),
            ),
        )

        for manifest in invalid:
            with self.subTest(manifest=manifest):
                with self.assertRaises(_InvalidManifest):
                    _validated_manifest_paths(manifest)

    def test_one_file_creation_preserves_unrelated_staged_and_dirty_state(self) -> None:
        self._seed_unrelated_state()
        path = "backlog/feature-backlog/create.md"
        content = self._work_item(path)
        self._write(path, content)

        commit_oid = self._commit_exact(
            _ProviderPathManifest("create", (path,)), "Create work item"
        )

        self._assert_immutable_commit(commit_oid, {path: content})
        self._assert_unrelated_state()

    def test_one_file_update_preserves_unrelated_staged_and_dirty_state(self) -> None:
        self._seed_unrelated_state()
        path = "backlog/defect-backlog/update.md"
        content = self._work_item(path, status="Running")
        self._write(path, content)

        commit_oid = self._commit_exact(
            _ProviderPathManifest("update", (path,)), "Update work item"
        )

        self._assert_immutable_commit(commit_oid, {path: content})
        self._assert_unrelated_state()

    def test_source_destination_move_preserves_state_and_work_item_id(self) -> None:
        self._seed_unrelated_state()
        source = "backlog/feature-backlog/move.md"
        destination = "backlog/completed-backlog/features/move.md"
        content = self._work_item(destination, status="Completed")
        (self.repository / source).unlink()
        self._write(destination, content)
        manifest = _ProviderPathManifest(
            "move",
            (source, destination),
            source_path=source,
            destination_path=destination,
        )

        commit_oid = self._commit_exact(manifest, "Move work item")

        self._assert_immutable_commit(
            commit_oid, {source: None, destination: content}
        )
        self.assertIn(
            b"Work Item ID: move",
            self._git_bytes("show", f"{commit_oid}:{destination}"),
        )
        self._assert_unrelated_state()

    def _commit_exact(
        self, manifest: _ProviderPathManifest, message: str
    ) -> str:
        add_argv, commit_argv = _mutating_argv(manifest, message)
        subprocess.run(
            add_argv, cwd=self.repository, check=True, capture_output=True
        )
        subprocess.run(
            commit_argv, cwd=self.repository, check=True, capture_output=True
        )
        return self._git("rev-parse", "HEAD").stdout.strip()

    def _assert_immutable_commit(
        self, commit_oid: str, expected: dict[str, bytes | None]
    ) -> None:
        changed = self._nul_paths(
            self._git_bytes(
                "diff-tree",
                "--root",
                "--no-commit-id",
                "--name-only",
                "-z",
                "-r",
                commit_oid,
                "--",
            )
        )
        self.assertEqual(frozenset(expected), changed)
        for path, content in expected.items():
            observed = subprocess.run(
                ["git", "show", f"{commit_oid}:{path}"],
                cwd=self.repository,
                check=False,
                capture_output=True,
            )
            if content is None:
                self.assertNotEqual(0, observed.returncode)
            else:
                self.assertEqual(0, observed.returncode)
                self.assertEqual(content, observed.stdout)
                self.assertEqual([Path(path).stem], self._work_item_ids(content))

    def _seed_unrelated_state(self) -> None:
        self._write("README.md", b"staged\n")
        self._git("add", "--", "README.md")
        self._write("notes.txt", b"tracked dirty\n")
        self._write("scratch.txt", b"untracked dirty\n")

    def _assert_unrelated_state(self) -> None:
        self.assertEqual(
            b"staged\n", self._git_bytes("show", ":README.md")
        )
        self.assertEqual(b"tracked dirty\n", (self.repository / "notes.txt").read_bytes())
        self.assertEqual(
            b"untracked dirty\n", (self.repository / "scratch.txt").read_bytes()
        )
        self.assertEqual("M  README.md", self._status_line("README.md"))
        self.assertEqual(" M notes.txt", self._status_line("notes.txt"))
        self.assertEqual("?? scratch.txt", self._status_line("scratch.txt"))

    @staticmethod
    def _work_item_ids(content: bytes) -> list[str]:
        return [
            line.removeprefix("Work Item ID: ").strip()
            for line in content.decode().splitlines()
            if line.startswith("Work Item ID: ")
        ]

    @staticmethod
    def _work_item(reference: str, *, status: str = "Ready") -> bytes:
        return (
            "# Contract fixture\n\n"
            f"Status: {status}\n\n"
            "Type: Feature\n\n"
            "Provider: file\n\n"
            f"Work Item ID: {Path(reference).stem}\n\n"
            "Completion: direct-main\n\n"
            "## Summary\n\nFixture.\n\n"
            "## Context\n\nFixture.\n\n"
            "## Source Evidence\n\nFixture.\n\n"
            "## Requirements\n\n- Fixture.\n\n"
            "## Acceptance Criteria\n\n- Fixture.\n\n"
            "## Dependencies\n\nNone\n\n"
            "## Verification\n\nFocused test.\n\n"
            "## Open Questions\n\nNone\n"
        ).encode()

    def _status_line(self, path: str) -> str:
        return self._git("status", "--short", "--", path).stdout.rstrip()

    def _write(self, path: str, content: bytes) -> None:
        destination = self.repository / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(content)

    def _git_bytes(self, *arguments: str) -> bytes:
        return subprocess.run(
            ["git", *arguments],
            cwd=self.repository,
            check=True,
            capture_output=True,
        ).stdout

    def _git(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", *arguments],
            cwd=self.repository,
            check=True,
            capture_output=True,
            text=True,
        )

    @staticmethod
    def _nul_paths(output: bytes) -> frozenset[str]:
        return frozenset(
            path.decode() for path in output.split(b"\0") if path
        )


if __name__ == "__main__":
    unittest.main()
