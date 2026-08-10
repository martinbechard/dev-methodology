# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies command claims, work-item lifecycles, resource deadlines, journaling, isolation, recovery, and reporting.
# Design: design/work-item-provider-and-completion-contracts.md

from __future__ import annotations

import ast
import gzip
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from collections.abc import Mapping
from contextlib import redirect_stdout
from datetime import date, timedelta
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
CLAIM_SCRIPT = ROOT / "skills" / "resource-claim-helper-command" / "scripts" / "claim.py"


def _symlinks_are_available() -> bool:
    """Return whether this host can create file-system symbolic links."""
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        target = root / "target"
        target.write_text("target\n", encoding="utf-8")
        try:
            (root / "link").symlink_to(target.name)
        except OSError:
            return False
        return True


SYMLINKS_AVAILABLE = _symlinks_are_available()


class ResourceClaimTests(unittest.TestCase):
    """Exercises the public claim command against temporary linked Git worktrees."""

    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.repository = Path(self.temporary_directory.name) / "repository"
        self.repository.mkdir()
        (self.repository / "src").mkdir()
        (self.repository / "docs").mkdir()
        (self.repository / "backlog" / "feature-backlog").mkdir(parents=True)
        (self.repository / ".gitignore").write_text(
            "/.worktrees/\n/.codex/agent-claim/\n",
            encoding="utf-8",
        )
        (self.repository / "README.md").write_text("baseline\n", encoding="utf-8")
        (self.repository / "src" / "one.py").write_text("one\n", encoding="utf-8")
        (self.repository / "docs" / "guide.md").write_text("guide\n", encoding="utf-8")
        (self.repository / "backlog" / "feature-backlog" / "queued.md").write_text(
            "queued\n",
            encoding="utf-8",
        )
        self.write_deadline_policy()
        self.git("init")
        self.git("config", "user.email", "test@example.invalid")
        self.git("config", "user.name", "Claim Test")
        self.git("add", ".")
        self.git("commit", "-m", "baseline")

    def test_claim_helper_has_no_unconditional_platform_lock_import(self) -> None:
        """Keep the command importable when either fcntl or msvcrt is unavailable."""

        tree = ast.parse(CLAIM_SCRIPT.read_text(encoding="utf-8"), filename=str(CLAIM_SCRIPT))
        imported_at_module_scope = {
            alias.name
            for node in tree.body
            if isinstance(node, ast.Import)
            for alias in node.names
        }

        self.assertNotIn("fcntl", imported_at_module_scope)
        self.assertNotIn("msvcrt", imported_at_module_scope)

    def git(self, *arguments: str, worktree: Path | None = None) -> subprocess.CompletedProcess[str]:
        """Run Git in the requested temporary worktree and require success."""
        return subprocess.run(
            ["git", "-C", str(worktree or self.repository), *arguments],
            check=True,
            text=True,
            capture_output=True,
        )

    def claim(
        self,
        *arguments: str,
        repo: Path | None = None,
        environment: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        """Run the bundled command with optional deterministic-clock and fault-injection variables."""
        command_environment = os.environ.copy()
        command_environment["PYTHONDONTWRITEBYTECODE"] = "1"
        command_environment.update(environment or {})
        return subprocess.run(
            [sys.executable, str(CLAIM_SCRIPT), "--repo", str(repo or self.repository), *arguments],
            check=False,
            text=True,
            capture_output=True,
            env=command_environment,
        )

    def claim_command(self, *arguments: str, repo: Path | None = None) -> list[str]:
        """Build a subprocess command for concurrency tests without executing it."""
        return [sys.executable, str(CLAIM_SCRIPT), "--repo", str(repo or self.repository), *arguments]

    def claim_with_denied_registry_path_read(
        self,
        denied_registry: Path,
        *arguments: str,
    ) -> tuple[int, dict[str, object]]:
        """Run the command while a Windows-style second registry open is denied."""
        module = self.load_claim_module("path_denial")
        denied_registry = denied_registry.resolve()
        original_read_text = Path.read_text

        def deny_registry_read(path: Path, *args: object, **kwargs: object) -> str:
            if path.resolve() == denied_registry:
                raise PermissionError("simulated Windows denial for a locked registry")
            return original_read_text(path, *args, **kwargs)

        with mock.patch.object(Path, "read_text", deny_registry_read):
            return self.claim_in_process(module, *arguments)

    def load_claim_module(self, label: str) -> object:
        """Load an isolated claim-helper module for one deterministic fault test."""
        module_name = f"resource_claim_{label}_{id(self)}"
        spec = importlib.util.spec_from_file_location(module_name, CLAIM_SCRIPT)
        if spec is None or spec.loader is None:
            raise RuntimeError("Unable to load the claim helper for fault testing.")
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        self.addCleanup(sys.modules.pop, module_name, None)
        spec.loader.exec_module(module)
        return module

    def claim_in_process(
        self,
        module: object,
        *arguments: str,
    ) -> tuple[int, dict[str, object]]:
        """Invoke one isolated helper module and decode its structured result."""
        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = module.main(["--repo", str(self.repository), *arguments])
        return exit_code, json.loads(output.getvalue())

    def claim_with_denied_canonical_path_read(
        self,
        *arguments: str,
    ) -> tuple[int, dict[str, object]]:
        """Deny a second pathname read of the canonical registry."""
        return self.claim_with_denied_registry_path_read(
            self.registry_path(),
            *arguments,
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

    def work_item_arguments(
        self,
        claim_id: str,
        work_item_id: str,
        activity: str = "work",
    ) -> list[str]:
        """Build an exact work-item acquisition without path or resource scope."""
        return [
            *self.acquire_arguments(claim_id),
            "--work-item-id",
            work_item_id,
            "--activity",
            activity,
        ]

    def isolated_arguments(self, claim_id: str, path_name: str | None = None) -> tuple[list[str], Path]:
        """Build a unique branch and the canonical worktree expected for a later writer."""
        isolated_path = (self.repository / ".worktrees" / (path_name or claim_id)).resolve()
        return ["--branch", f"codex/{claim_id}"], isolated_path

    def existing_linked_worktree(self, name: str = "private") -> Path:
        """Create an existing non-canonical linked checkout for caller-topology tests."""
        linked_path = (Path(self.temporary_directory.name) / f"{name}-checkout").resolve()
        self.git("worktree", "add", "-b", f"codex/{name}", str(linked_path), "HEAD")
        return linked_path

    def timed_resource_arguments(
        self,
        resource: str = "port:3000",
        resource_class: str = "database-port",
        resource_id: str | None = None,
        expected_duration_seconds: int = 300,
        requested_hard_stop_duration_seconds: int = 900,
    ) -> list[str]:
        """Build one complete deterministic deadline request for a named resource."""
        return [
            "--resource",
            resource,
            "--resource-class",
            resource_class,
            "--resource-id",
            resource if resource_id is None else resource_id,
            "--expected-duration-seconds",
            str(expected_duration_seconds),
            "--requested-hard-stop-duration-seconds",
            str(requested_hard_stop_duration_seconds),
        ]

    def deadline_policy(self) -> dict[str, object]:
        """Return the five configured class defaults used by command tests."""
        return {
            "resource_coordination": {
                "selected": "resource-claim",
                "deadline_policy": {
                    "resource_classes": {
                        "backlog-mutation": {
                            "maximum_duration_seconds": 600,
                            "cleanup_grace_seconds": 120,
                        },
                        "main-integration": {
                            "maximum_duration_seconds": 2700,
                            "cleanup_grace_seconds": 600,
                        },
                        "browser-server": {
                            "maximum_duration_seconds": 3600,
                            "cleanup_grace_seconds": 600,
                        },
                        "database-port": {
                            "maximum_duration_seconds": 1800,
                            "cleanup_grace_seconds": 300,
                        },
                        "live-model-evaluation": {
                            "maximum_duration_seconds": 14400,
                            "cleanup_grace_seconds": 1800,
                        },
                    },
                    "resource_overrides": {},
                },
            }
        }

    def write_deadline_policy(self, policy: dict[str, object] | None = None) -> None:
        """Write one YAML-compatible JSON project policy into the temporary repository."""
        (self.repository / "PROJECT.yaml").write_text(
            json.dumps(policy if policy is not None else self.deadline_policy(), indent=2) + "\n",
            encoding="utf-8",
        )

    def output(self, completed: subprocess.CompletedProcess[str]) -> dict[str, object]:
        """Decode one structured command result."""
        return json.loads(completed.stdout)

    def common_directory(self) -> Path:
        """Return the temporary repository's Git common directory."""
        raw = Path(self.git("rev-parse", "--git-common-dir").stdout.strip())
        return raw if raw.is_absolute() else self.repository / raw

    def registry_path(self) -> Path:
        """Return the repository-global live registry path."""
        return self.repository / ".codex" / "agent-claim" / "agent-claims.json"

    def write_registry_fixture(self, payload: dict[str, object]) -> None:
        """Write canonical versioned claim state for a stored-schema compatibility case."""
        self.state_root().mkdir(parents=True, exist_ok=True)
        self.registry_path().write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        (self.state_root() / "state.json").write_text(
            json.dumps(
                {
                    "migration_status": "complete",
                    "origin": "fresh",
                    "schema_version": 1,
                    "state_layout_version": 2,
                },
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )

    def legacy_registry_path(self) -> Path:
        """Return the pre-migration registry path in Git metadata."""
        return self.common_directory() / "agent-claims.json"

    def state_root(self) -> Path:
        """Return the canonical operational claim-state root."""
        return self.repository / ".codex" / "agent-claim"

    def rewrite_claim_paths_as_legacy(
        self,
        claim_id: str,
        *,
        files: list[str] | None = None,
        trees: list[str] | None = None,
    ) -> None:
        """Replace stored paths and remove current file-domain metadata for a legacy fixture."""
        registry = json.loads(self.registry_path().read_text(encoding="utf-8"))
        claim = next(item for item in registry["claims"] if item["claim_id"] == claim_id)
        if files is not None:
            claim["files"] = files
        if trees is not None:
            claim["trees"] = trees
        claim.pop("file_domain", None)
        claim.pop("project_files", None)
        claim.pop("backlog", None)
        self.registry_path().write_text(
            json.dumps(registry, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    def hot_directory(self) -> Path:
        """Return the repository-global hot journal directory."""
        return self.state_root() / "agent-claim-events" / "hot"

    def journal_events(self) -> list[dict[str, object]]:
        """Read all hot events for lifecycle and concurrency assertions."""
        events: list[dict[str, object]] = []
        for path in sorted(self.hot_directory().glob("*.jsonl")):
            events.extend(json.loads(line) for line in path.read_text(encoding="utf-8").splitlines())
        return events

    def write_daily_events(self, day: str, events: list[dict[str, object]]) -> Path:
        """Write a deterministic historical hot file for archive and report tests."""
        self.hot_directory().mkdir(parents=True, exist_ok=True)
        path = self.hot_directory() / f"{day}.jsonl"
        path.write_text("".join(json.dumps(event, sort_keys=True) + "\n" for event in events), encoding="utf-8")
        return path

    def synthetic_event(
        self,
        event_id: str,
        timestamp: str,
        action: str,
        outcome: str,
        claim_id: str,
        **values: object,
    ) -> dict[str, object]:
        """Build the minimum versioned event fixture accepted by reporting and archival."""
        event: dict[str, object] = {
            "schema_version": 1,
            "event_id": event_id,
            "timestamp": timestamp,
            "action": action,
            "outcome": outcome,
            "claim_id": claim_id,
            "journal_warnings": [],
        }
        event.update(values)
        return event

    def test_first_writer_claims_clean_primary_worktree(self) -> None:
        completed = self.claim(*self.acquire_arguments("first"), "--file", "README.md")

        self.assertEqual(0, completed.returncode, completed.stderr)
        result = self.output(completed)
        self.assertEqual(2, result["schema_version"])
        self.assertEqual("SHARED_CHECKOUT_ACQUIRED", result["outcome"])
        self.assertEqual("PRIMARY", result["legacy_outcome"])
        self.assertEqual(str(self.repository.resolve()), result["claim"]["worktree"])
        self.assertEqual("primary", result["claim"]["checkout_topology"])
        self.assertEqual("primary", result["target"]["mode"])
        self.assertEqual("primary", result["target"]["checkout_topology"])
        event = self.journal_events()[-1]
        self.assertEqual("primary", event["checkout_topology"])
        self.assertEqual("primary", event["worktree_id"])
        self.assertNotIn(str(self.temporary_directory.name), json.dumps(event))

    def test_primary_and_linked_worktrees_share_primary_operational_state(self) -> None:
        """Every checkout resolves the primary worktree's ignored claim-state root."""
        first_linked = self.existing_linked_worktree("first-linked")
        second_linked = self.existing_linked_worktree("second-linked")

        acquired = self.claim(
            *self.acquire_arguments("shared"),
            "--file",
            "README.md",
            repo=first_linked,
        )
        primary_status = self.claim("status")
        second_status = self.claim("status", repo=second_linked)

        self.assertEqual(0, acquired.returncode, acquired.stderr)
        expected_registry = str(self.registry_path().resolve())
        self.assertEqual(expected_registry, self.output(primary_status)["registry"])
        self.assertEqual(expected_registry, self.output(second_status)["registry"])
        self.assertEqual(
            ["shared"],
            [claim["claim_id"] for claim in self.output(second_status)["claims"]],
        )
        self.assertFalse((first_linked / ".codex" / "agent-claim").exists())
        self.assertFalse((second_linked / ".codex" / "agent-claim").exists())
        self.assertFalse(self.legacy_registry_path().exists())

    def test_claim_state_is_lazy_and_operational_paths_are_not_claimable(self) -> None:
        """Read access stays write-free; the first mutation creates canonical state."""
        self.assertFalse(self.state_root().exists())

        status = self.claim("status")
        self.assertEqual(0, status.returncode, status.stderr)
        self.assertEqual([], self.output(status)["claims"])
        self.assertFalse(self.state_root().exists())

        created = self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        rejected = self.claim(
            *self.acquire_arguments("operational"),
            "--file",
            ".codex/agent-claim/agent-claims.json",
        )

        self.assertEqual(0, created.returncode, created.stderr)
        self.assertEqual(
            ["first"],
            [claim["claim_id"] for claim in json.loads(self.registry_path().read_text(encoding="utf-8"))["claims"]],
        )
        self.assertFalse(self.legacy_registry_path().exists())
        self.assertFalse((self.common_directory() / "agent-claim-events").exists())
        self.assertEqual(1, rejected.returncode)
        self.assertEqual("INVALID_SCOPE", self.output(rejected)["outcome"])
        self.assertEqual(
            "operational_path_not_claimable",
            self.output(rejected)["rejection"]["reason"],
        )

    def test_empty_legacy_registry_and_history_migrate_with_incompatible_markers(self) -> None:
        """An empty legacy registry migrates history and blocks old helper path types."""
        legacy_registry = self.legacy_registry_path()
        legacy_registry.write_text('{"claims":[]}\n', encoding="utf-8")
        legacy_hot = self.common_directory() / "agent-claim-events" / "hot"
        legacy_hot.mkdir(parents=True)
        legacy_event = self.synthetic_event(
            "legacy-event",
            "2026-07-10T01:00:00Z",
            "release",
            "RELEASED",
            "legacy",
        )
        (legacy_hot / "2026-07-10.jsonl").write_text(
            json.dumps(legacy_event) + "\n",
            encoding="utf-8",
        )

        status = self.claim(*self.acquire_arguments("migrated"), "--file", "README.md")

        self.assertEqual(0, status.returncode, status.stderr)
        self.assertEqual(str(self.registry_path().resolve()), self.output(status)["registry"])
        self.assertTrue(legacy_registry.is_dir())
        self.assertTrue((legacy_registry / "state.json").is_file())
        legacy_events = self.common_directory() / "agent-claim-events"
        self.assertTrue(legacy_events.is_file())
        self.assertEqual(
            legacy_event,
            json.loads((self.hot_directory() / "2026-07-10.jsonl").read_text(encoding="utf-8")),
        )
        marker = json.loads((self.state_root() / "state.json").read_text(encoding="utf-8"))
        self.assertEqual("complete", marker["migration_status"])
        self.assertEqual("legacy", marker["origin"])

    def test_fresh_state_validation_uses_its_locked_canonical_descriptor(self) -> None:
        """Fresh setup succeeds when Windows denies reopening its locked registry path."""
        exit_code, result = self.claim_with_denied_canonical_path_read("reset")

        self.assertEqual(0, exit_code)
        self.assertEqual("RESET", result["outcome"])
        self.assertEqual([], result["claims"])
        marker = json.loads((self.state_root() / "state.json").read_text())
        self.assertEqual("complete", marker["migration_status"])
        self.assertEqual("fresh", marker["origin"])

    def test_legacy_migration_validation_uses_its_locked_canonical_descriptor(self) -> None:
        """Migration succeeds when Windows denies reopening its locked registry path."""
        self.legacy_registry_path().write_text('{"claims":[]}\n', encoding="utf-8")

        exit_code, result = self.claim_with_denied_canonical_path_read("reset")

        self.assertEqual(0, exit_code)
        self.assertEqual("RESET", result["outcome"])
        self.assertEqual([], result["claims"])
        marker = json.loads((self.state_root() / "state.json").read_text())
        self.assertEqual("complete", marker["migration_status"])
        self.assertEqual("legacy", marker["origin"])
        self.assertTrue(self.legacy_registry_path().is_dir())

    def test_legacy_migration_reuses_payload_from_its_locked_legacy_descriptor(self) -> None:
        """Migration succeeds when Windows denies reopening its locked legacy path."""
        legacy_registry = self.legacy_registry_path()
        legacy_registry.write_text('{"claims":[]}\n', encoding="utf-8")

        exit_code, result = self.claim_with_denied_registry_path_read(
            legacy_registry,
            "reset",
        )

        self.assertEqual(0, exit_code)
        self.assertEqual("RESET", result["outcome"])
        self.assertEqual([], result["claims"])
        marker = json.loads((self.state_root() / "state.json").read_text())
        self.assertEqual("complete", marker["migration_status"])
        self.assertEqual("legacy", marker["origin"])
        self.assertTrue(legacy_registry.is_dir())

    def test_windows_migration_tombstones_same_inode_before_moving_events(self) -> None:
        """Windows retires empty legacy state in place before event migration."""
        module = self.load_claim_module("windows_tombstone")
        legacy_registry = self.legacy_registry_path()
        legacy_events = self.common_directory() / "agent-claim-events"
        legacy_registry.write_text('{"claims":[]}\n', encoding="utf-8")
        (legacy_events / "hot").mkdir(parents=True)
        original_inode = legacy_registry.stat().st_ino
        operations: list[str] = []
        original_tombstone = module._write_locked_legacy_registry_tombstone
        original_move_events = module._move_legacy_events
        original_rename = os.rename
        original_unlink = Path.unlink
        original_read_bytes = Path.read_bytes
        original_write = os.write
        raw_writes: list[bytes] = []

        def track_tombstone(legacy_file: object, path: Path) -> None:
            original_tombstone(legacy_file, path)
            operations.append("tombstone")

        def track_events(repository: Path) -> None:
            operations.append("move-events")
            original_move_events(repository)

        def reject_legacy_rename(source: object, destination: object) -> None:
            if Path(source) == legacy_registry:
                raise AssertionError("Windows migration must not rename the legacy registry")
            original_rename(source, destination)

        def reject_legacy_unlink(path: Path, *args: object, **kwargs: object) -> None:
            if path == legacy_registry:
                raise AssertionError("Windows migration must not unlink the legacy registry")
            original_unlink(path, *args, **kwargs)

        def reject_locked_legacy_read(path: Path) -> bytes:
            if path == legacy_registry:
                raise PermissionError("simulated Windows locked-file reopen rejection")
            return original_read_bytes(path)

        def record_raw_write(descriptor: int, payload: bytes) -> int:
            raw_writes.append(bytes(payload))
            return original_write(descriptor, payload)

        with (
            mock.patch.object(module, "WINDOWS_LEGACY_REGISTRY_TOMBSTONE", True),
            mock.patch.object(
                module,
                "_write_locked_legacy_registry_tombstone",
                track_tombstone,
            ),
            mock.patch.object(module, "_move_legacy_events", track_events),
            mock.patch.object(module.os, "rename", reject_legacy_rename),
            mock.patch.object(Path, "unlink", reject_legacy_unlink),
            mock.patch.object(Path, "read_bytes", reject_locked_legacy_read),
            mock.patch.object(module.os, "write", record_raw_write),
        ):
            exit_code, result = self.claim_in_process(module, "reset")

        self.assertEqual(0, exit_code)
        self.assertEqual("RESET", result["outcome"])
        self.assertEqual(["tombstone", "move-events"], operations)
        self.assertEqual(original_inode, legacy_registry.stat().st_ino)
        self.assertEqual(
            module._legacy_marker_payload("registry"),
            legacy_registry.read_bytes(),
        )
        self.assertIn(module._legacy_marker_payload("registry"), raw_writes)
        self.assertTrue(legacy_events.is_file())
        marker = json.loads((self.state_root() / "state.json").read_text())
        self.assertEqual("complete", marker["migration_status"])

    def test_windows_tombstone_makes_old_registry_decoder_fail_closed(self) -> None:
        """The exact regular marker omits claims so an old helper rejects it."""
        module = self.load_claim_module("windows_old_helper_stop")
        legacy_registry = self.legacy_registry_path()
        legacy_registry.write_bytes(module._legacy_marker_payload("registry"))

        self.assertTrue(module._legacy_registry_is_marker(legacy_registry))
        with self.assertRaises(module._ClaimStateError) as raised:
            module._registry_payload(legacy_registry)

        self.assertEqual("invalid_registry", raised.exception.reason)
        self.assertNotIn("claims", json.loads(legacy_registry.read_text()))

    def test_windows_tombstone_migration_recovers_before_moving_events(self) -> None:
        """An interruption after tombstoning resumes without changing the retired inode."""
        module = self.load_claim_module("windows_tombstone_recovery")
        legacy_registry = self.legacy_registry_path()
        legacy_events = self.common_directory() / "agent-claim-events"
        legacy_registry.write_text('{"claims":[]}\n', encoding="utf-8")
        (legacy_events / "hot").mkdir(parents=True)
        original_inode = legacy_registry.stat().st_ino
        original_move_events = module._move_legacy_events
        move_attempts = 0

        def interrupt_first_event_move(repository: Path) -> None:
            nonlocal move_attempts
            move_attempts += 1
            if move_attempts == 1:
                raise OSError("simulated interruption after registry tombstone")
            original_move_events(repository)

        with (
            mock.patch.object(module, "WINDOWS_LEGACY_REGISTRY_TOMBSTONE", True),
            mock.patch.object(module, "_move_legacy_events", interrupt_first_event_move),
        ):
            blocked_code, blocked = self.claim_in_process(module, "reset")
            blocked_marker = json.loads((self.state_root() / "state.json").read_text())
            recovered_code, recovered = self.claim_in_process(module, "reset")

        self.assertEqual(3, blocked_code)
        self.assertEqual("migration_interrupted", blocked["reason"])
        self.assertEqual("in_progress", blocked_marker["migration_status"])
        self.assertEqual(0, recovered_code)
        self.assertEqual("RESET", recovered["outcome"])
        self.assertEqual(2, move_attempts)
        self.assertEqual(original_inode, legacy_registry.stat().st_ino)
        self.assertEqual(
            module._legacy_marker_payload("registry"),
            legacy_registry.read_bytes(),
        )
        self.assertTrue(legacy_events.is_file())

    def test_windows_tombstone_migration_preserves_live_legacy_state(self) -> None:
        """A live legacy registry remains byte-for-byte drain-only state."""
        module = self.load_claim_module("windows_live_registry")
        legacy_registry = self.legacy_registry_path()
        live_payload = b'{"claims":[{"claim_id":"live-owner"}]}\n'
        legacy_registry.write_bytes(live_payload)
        original_inode = legacy_registry.stat().st_ino

        with mock.patch.object(module, "WINDOWS_LEGACY_REGISTRY_TOMBSTONE", True):
            exit_code, result = self.claim_in_process(module, "reset")

        self.assertEqual(3, exit_code)
        self.assertEqual("live_legacy_claims_require_drain", result["reason"])
        self.assertEqual(original_inode, legacy_registry.stat().st_ino)
        self.assertEqual(live_payload, legacy_registry.read_bytes())
        self.assertFalse(self.state_root().exists())

    def test_windows_tombstone_rejects_nonempty_legacy_metadata(self) -> None:
        """Only the exact empty registry payload is eligible for retirement."""
        module = self.load_claim_module("windows_nonempty_metadata")
        legacy_registry = self.legacy_registry_path()
        legacy_payload = b'{"claims":[],"unexpected":"state"}\n'
        legacy_registry.write_bytes(legacy_payload)
        original_inode = legacy_registry.stat().st_ino

        with mock.patch.object(module, "WINDOWS_LEGACY_REGISTRY_TOMBSTONE", True):
            exit_code, result = self.claim_in_process(module, "reset")

        self.assertEqual(3, exit_code)
        self.assertEqual("contradictory_dual_state", result["reason"])
        self.assertEqual(original_inode, legacy_registry.stat().st_ino)
        self.assertEqual(legacy_payload, legacy_registry.read_bytes())
        self.assertFalse(self.state_root().exists())

    def test_windows_tombstone_rejects_legacy_identity_mismatch(self) -> None:
        """A descriptor that lost the legacy path never overwrites either inode."""
        module = self.load_claim_module("windows_identity_mismatch")
        legacy_registry = self.legacy_registry_path()
        legacy_payload = b'{"claims":[]}\n'
        legacy_registry.write_bytes(legacy_payload)
        original_inode = legacy_registry.stat().st_ino

        with (
            mock.patch.object(module, "WINDOWS_LEGACY_REGISTRY_TOMBSTONE", True),
            mock.patch.object(module, "_legacy_descriptor_matches_path", return_value=False),
        ):
            exit_code, result = self.claim_in_process(module, "reset")

        self.assertEqual(3, exit_code)
        self.assertEqual("contradictory_dual_state", result["reason"])
        self.assertEqual(original_inode, legacy_registry.stat().st_ino)
        self.assertEqual(legacy_payload, legacy_registry.read_bytes())

    def test_windows_in_progress_live_state_remains_release_only(self) -> None:
        """A legacy writer racing an interrupted migration can still be drained."""
        module = self.load_claim_module("windows_in_progress_live")
        self.state_root().mkdir(parents=True)
        self.registry_path().write_text('{"claims":[]}\n', encoding="utf-8")
        (self.state_root() / "state.json").write_text(
            json.dumps(
                {
                    "migration_status": "in_progress",
                    "origin": "legacy",
                    "schema_version": 1,
                    "state_layout_version": 2,
                }
            )
            + "\n",
            encoding="utf-8",
        )
        legacy_claim = {
            "claim_id": "late-writer",
            "agent": "late-writer",
            "task": "late writer",
            "root_task_id": "late-writer",
            "files": ["README.md"],
            "trees": [],
            "resources": [],
            "project_files": False,
            "backlog": False,
            "all_files": False,
            "mode": "primary",
            "checkout_topology": "primary",
            "worktree": str(self.repository),
            "branch": "main",
        }
        self.legacy_registry_path().write_text(
            json.dumps({"claims": [legacy_claim]}, indent=2) + "\n",
            encoding="utf-8",
        )
        legacy_before = self.legacy_registry_path().read_bytes()

        with mock.patch.object(module, "WINDOWS_LEGACY_REGISTRY_TOMBSTONE", True):
            blocked_code, blocked = self.claim_in_process(module, "reset")
            preserved_after_block = self.legacy_registry_path().read_bytes()
            release_code, released = self.claim_in_process(
                module,
                "release",
                "--claim-id",
                "late-writer",
            )
            recovered_code, recovered = self.claim_in_process(module, "reset")

        self.assertEqual(3, blocked_code)
        self.assertEqual("live_legacy_claims_require_drain", blocked["reason"])
        self.assertEqual(legacy_before, preserved_after_block)
        self.assertEqual(0, release_code)
        self.assertEqual("RELEASED", released["outcome"])
        self.assertEqual(0, recovered_code)
        self.assertEqual("RESET", recovered["outcome"])
        self.assertEqual(
            module._legacy_marker_payload("registry"),
            self.legacy_registry_path().read_bytes(),
        )
        marker = json.loads((self.state_root() / "state.json").read_text())
        self.assertEqual("complete", marker["migration_status"])

    def test_regular_tombstone_is_recognized_on_posix_recovery(self) -> None:
        """Every platform accepts the exact Windows tombstone after migration."""
        module = self.load_claim_module("cross_platform_tombstone")
        self.state_root().mkdir(parents=True)
        self.registry_path().write_text('{"claims":[]}\n', encoding="utf-8")
        (self.state_root() / "state.json").write_text(
            json.dumps(
                {
                    "migration_status": "complete",
                    "origin": "legacy",
                    "schema_version": 1,
                    "state_layout_version": 2,
                }
            )
            + "\n",
            encoding="utf-8",
        )
        self.legacy_registry_path().write_bytes(
            module._legacy_marker_payload("registry")
        )
        (self.common_directory() / "agent-claim-events").write_bytes(
            module._legacy_marker_payload("events")
        )

        exit_code, result = self.claim_in_process(module, "status")

        self.assertEqual(0, exit_code)
        self.assertEqual("STATUS", result["outcome"])
        self.assertEqual([], result["claims"])

    def test_live_legacy_registry_is_drain_only_before_migration(self) -> None:
        """The upgraded helper can release, but cannot otherwise mutate, a live legacy claim."""
        legacy_claim = {
            "claim_id": "integration",
            "incarnation_id": "legacy-incarnation",
            "agent": "merge-coordinator",
            "task": "integration",
            "root_task_id": "integration",
            "parent_claim_id": None,
            "claimed_at": "2026-08-05T23:00:00Z",
            "heartbeat": "2026-08-05T23:00:00Z",
            "files": ["README.md"],
            "trees": [],
            "resources": [],
            "project_files": False,
            "backlog": False,
            "all_files": False,
            "file_domain": "project_files",
            "scope_reasons": {},
            "mode": "primary",
            "checkout_topology": "primary",
            "worktree": str(self.repository),
            "branch": "main",
            "baseline_commit": self.git("rev-parse", "HEAD").stdout.strip(),
            "acquisition_outcome": "SHARED_CHECKOUT_ACQUIRED",
        }
        self.legacy_registry_path().write_text(
            json.dumps({"claims": [legacy_claim]}, indent=2) + "\n",
            encoding="utf-8",
        )
        legacy_before = self.legacy_registry_path().read_bytes()

        blocked_status = self.claim("status")
        blocked_heartbeat = self.claim("heartbeat", "--claim-id", "integration")
        blocked_acquire = self.claim(
            *self.acquire_arguments("other"),
            "--file",
            "src/one.py",
        )

        for completed in (blocked_status, blocked_heartbeat, blocked_acquire):
            self.assertEqual(3, completed.returncode)
            self.assertEqual(
                "CLAIM_STATE_MIGRATION_BLOCKED",
                self.output(completed)["outcome"],
            )
            self.assertEqual("live_legacy_claims_require_drain", self.output(completed)["reason"])
        self.assertEqual(legacy_before, self.legacy_registry_path().read_bytes())
        self.assertFalse(self.state_root().exists())

        released = self.claim("release", "--claim-id", "integration")
        read_only = self.claim("status")

        self.assertEqual(0, released.returncode, released.stderr)
        self.assertEqual("RELEASED", self.output(released)["outcome"])
        self.assertIn(
            "/.git/agent-claim-events/hot/",
            str(self.output(released)["journal"]["path"]),
        )
        self.assertEqual(0, read_only.returncode, read_only.stderr)
        self.assertFalse(self.state_root().exists())

        migrated = self.claim(*self.acquire_arguments("post-upgrade"), "--file", "src/one.py")

        self.assertEqual(0, migrated.returncode, migrated.stderr)
        self.assertTrue(self.legacy_registry_path().is_dir())
        self.assertEqual("SHARED_CHECKOUT_ACQUIRED", self.output(migrated)["outcome"])

    def test_concurrent_legacy_release_re_resolves_after_migration(self) -> None:
        """A stale legacy resolution follows migration instead of reopening its old path."""
        self.legacy_registry_path().write_text(
            json.dumps(
                {
                    "claims": [
                        {
                            "claim_id": "integration",
                            "agent": "merge-coordinator",
                            "root_task_id": "integration",
                            "files": ["README.md"],
                            "worktree": str(self.repository),
                            "branch": "main",
                            "mode": "primary",
                            "checkout_topology": "primary",
                        }
                    ]
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        barrier = Path(self.temporary_directory.name) / "release-resolution"
        command_environment = os.environ.copy()
        command_environment.update(
            {
                "PYTHONDONTWRITEBYTECODE": "1",
                "RESOURCE_CLAIM_TEST_RELEASE_RESOLVE_BARRIER": str(barrier),
            }
        )
        first_release = subprocess.Popen(
            self.claim_command("release", "--claim-id", "integration"),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=command_environment,
        )
        self.addCleanup(lambda: first_release.poll() is None and first_release.kill())
        ready = Path(f"{barrier}.ready")
        deadline = time.monotonic() + 5
        while not ready.exists() and time.monotonic() < deadline:
            time.sleep(0.01)
        self.assertTrue(ready.exists(), "first release did not reach the resolution barrier")

        second_release = self.claim("release", "--claim-id", "integration")
        migrated = self.claim("reset")
        Path(f"{barrier}.continue").write_text("continue\n", encoding="utf-8")
        stdout, stderr = first_release.communicate(timeout=5)

        self.assertEqual(0, second_release.returncode, second_release.stderr)
        self.assertEqual("RELEASED", self.output(second_release)["outcome"])
        self.assertEqual(0, migrated.returncode, migrated.stderr)
        self.assertEqual(1, first_release.returncode, stderr)
        self.assertEqual("CLAIM_NOT_FOUND", json.loads(stdout)["outcome"])
        self.assertNotIn("Traceback", stderr)
        self.assertTrue(self.legacy_registry_path().is_dir())
        self.assertTrue(self.registry_path().is_file())
        self.assertEqual([], json.loads(self.registry_path().read_text())["claims"])

    def test_legacy_resolution_rechecks_inode_after_its_first_lock(self) -> None:
        """A waiter never migrates through the stale descriptor it opened before locking."""
        self.legacy_registry_path().write_text(
            json.dumps(
                {
                    "claims": [
                        {
                            "claim_id": "integration",
                            "agent": "merge-coordinator",
                            "root_task_id": "integration",
                            "files": ["README.md"],
                            "worktree": str(self.repository),
                            "branch": "main",
                            "mode": "primary",
                            "checkout_topology": "primary",
                        }
                    ]
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        barrier = Path(self.temporary_directory.name) / "legacy-open"
        command_environment = os.environ.copy()
        command_environment.update(
            {
                "PYTHONDONTWRITEBYTECODE": "1",
                "RESOURCE_CLAIM_TEST_RELEASE_LEGACY_OPEN_BARRIER": str(barrier),
            }
        )
        first_release = subprocess.Popen(
            self.claim_command("release", "--claim-id", "integration"),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=command_environment,
        )
        self.addCleanup(lambda: first_release.poll() is None and first_release.kill())
        ready = Path(f"{barrier}.ready")
        deadline = time.monotonic() + 5
        while not ready.exists() and time.monotonic() < deadline:
            time.sleep(0.01)
        self.assertTrue(ready.exists(), "first release did not open the legacy registry")

        second_release = self.claim("release", "--claim-id", "integration")
        canonical_acquire = self.claim(
            *self.acquire_arguments("canonical-owner"),
            "--file",
            "src/one.py",
        )
        Path(f"{barrier}.continue").write_text("continue\n", encoding="utf-8")
        stdout, stderr = first_release.communicate(timeout=5)

        self.assertEqual(0, second_release.returncode, second_release.stderr)
        self.assertEqual(0, canonical_acquire.returncode, canonical_acquire.stderr)
        self.assertEqual(1, first_release.returncode, stderr)
        self.assertEqual("CLAIM_NOT_FOUND", json.loads(stdout)["outcome"])
        self.assertNotIn("Traceback", stderr)
        marker = json.loads((self.state_root() / "state.json").read_text())
        self.assertEqual("complete", marker["migration_status"])
        self.assertEqual("legacy", marker["origin"])
        self.assertTrue(self.legacy_registry_path().is_dir())
        self.assertEqual(
            ["canonical-owner"],
            [
                claim["claim_id"]
                for claim in json.loads(self.registry_path().read_text())["claims"]
            ],
        )

    def test_read_only_legacy_snapshot_rechecks_inode_after_its_first_lock(self) -> None:
        """A stale-open reader retries and observes the new canonical owner."""
        self.legacy_registry_path().write_text(
            json.dumps(
                {
                    "claims": [
                        {
                            "claim_id": "integration",
                            "agent": "merge-coordinator",
                            "root_task_id": "integration",
                            "files": ["README.md"],
                            "worktree": str(self.repository),
                            "branch": "main",
                            "mode": "primary",
                            "checkout_topology": "primary",
                        }
                    ]
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        barrier = Path(self.temporary_directory.name) / "read-only-legacy-open"
        command_environment = os.environ.copy()
        command_environment.update(
            {
                "PYTHONDONTWRITEBYTECODE": "1",
                "RESOURCE_CLAIM_TEST_READ_ONLY_LEGACY_OPEN_BARRIER": str(barrier),
            }
        )
        stale_status = subprocess.Popen(
            self.claim_command("status"),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=command_environment,
        )
        self.addCleanup(lambda: stale_status.poll() is None and stale_status.kill())
        ready = Path(f"{barrier}.ready")
        deadline = time.monotonic() + 5
        while not ready.exists() and time.monotonic() < deadline:
            time.sleep(0.01)
        self.assertTrue(ready.exists(), "status did not open the legacy registry")

        released = self.claim("release", "--claim-id", "integration")
        canonical_acquire = self.claim(
            *self.acquire_arguments("canonical-owner"),
            "--file",
            "src/one.py",
        )
        Path(f"{barrier}.continue").write_text("continue\n", encoding="utf-8")
        stdout, stderr = stale_status.communicate(timeout=5)

        self.assertEqual(0, released.returncode, released.stderr)
        self.assertEqual(0, canonical_acquire.returncode, canonical_acquire.stderr)
        self.assertEqual(0, stale_status.returncode, stderr)
        status = json.loads(stdout)
        self.assertEqual("STATUS", status["outcome"])
        self.assertEqual(
            ["canonical-owner"],
            [claim["claim_id"] for claim in status["claims"]],
        )
        self.assertNotIn("Traceback", stderr)
        marker = json.loads((self.state_root() / "state.json").read_text())
        self.assertEqual("complete", marker["migration_status"])
        self.assertEqual("legacy", marker["origin"])

    def test_contradictory_dual_registries_stop_without_mutation(self) -> None:
        """Two independently populated state locations are never reconciled by preference."""
        self.state_root().mkdir(parents=True)
        self.registry_path().write_text('{"claims":[]}\n', encoding="utf-8")
        self.legacy_registry_path().write_text(
            '{"claims":[{"claim_id":"legacy-live"}]}\n',
            encoding="utf-8",
        )
        new_before = self.registry_path().read_bytes()
        legacy_before = self.legacy_registry_path().read_bytes()

        completed = self.claim("status")

        self.assertEqual(3, completed.returncode)
        self.assertEqual("CLAIM_STATE_MIGRATION_BLOCKED", self.output(completed)["outcome"])
        self.assertEqual("contradictory_dual_state", self.output(completed)["reason"])
        self.assertEqual(new_before, self.registry_path().read_bytes())
        self.assertEqual(legacy_before, self.legacy_registry_path().read_bytes())

    def test_report_reads_legacy_history_before_first_mutation(self) -> None:
        """Read-only reporting preserves visible history until an empty legacy state migrates."""
        self.legacy_registry_path().write_text('{"claims":[]}\n', encoding="utf-8")
        legacy_hot = self.common_directory() / "agent-claim-events" / "hot"
        legacy_hot.mkdir(parents=True)
        event = self.synthetic_event(
            "legacy-visible",
            "2026-08-05T10:00:00Z",
            "acquire",
            "SHARED_CHECKOUT_ACQUIRED",
            "legacy-visible",
        )
        (legacy_hot / "2026-08-05.jsonl").write_text(
            json.dumps(event, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        completed = self.claim(
            "report",
            "--since",
            "1d",
            environment={"RESOURCE_CLAIM_TEST_NOW": "2026-08-05T12:00:00Z"},
        )

        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertEqual(1, self.output(completed)["event_count"])
        self.assertFalse(self.state_root().exists())
        self.assertTrue(self.legacy_registry_path().is_file())
        self.assertTrue(legacy_hot.is_dir())

    def test_fresh_state_rejects_legacy_state_created_after_rollout(self) -> None:
        """A completed fresh boundary still detects an older helper's later split registry."""
        first = self.claim("reset")
        self.assertEqual(0, first.returncode, first.stderr)
        self.legacy_registry_path().write_text('{"claims":[]}\n', encoding="utf-8")

        completed = self.claim("status")

        self.assertEqual(3, completed.returncode)
        self.assertEqual("CLAIM_STATE_MIGRATION_BLOCKED", self.output(completed)["outcome"])
        self.assertEqual("contradictory_dual_state", self.output(completed)["reason"])

    def test_migrated_state_requires_exact_legacy_marker_types(self) -> None:
        """A completed legacy boundary never trusts missing or replaced rollout markers."""
        self.legacy_registry_path().write_text('{"claims":[]}\n', encoding="utf-8")
        migrated = self.claim("reset")
        self.assertEqual(0, migrated.returncode, migrated.stderr)
        (self.legacy_registry_path() / "state.json").write_text("{}\n", encoding="utf-8")

        completed = self.claim("status")

        self.assertEqual(3, completed.returncode)
        self.assertEqual("CLAIM_STATE_MIGRATION_BLOCKED", self.output(completed)["outcome"])
        self.assertEqual("contradictory_dual_state", self.output(completed)["reason"])

    def test_interrupted_empty_legacy_migration_recovers_deterministically(self) -> None:
        """A migration stopped after moving history resumes from its versioned marker."""
        self.legacy_registry_path().write_text('{"claims":[]}\n', encoding="utf-8")
        legacy_hot = self.common_directory() / "agent-claim-events" / "hot"
        legacy_hot.mkdir(parents=True)
        (legacy_hot / "2026-08-05.jsonl").write_text("", encoding="utf-8")

        interrupted = self.claim(
            "reset",
            environment={"RESOURCE_CLAIM_TEST_FAIL_MIGRATION_AFTER_EVENTS": "1"},
        )
        recovered = self.claim("reset")

        self.assertEqual(3, interrupted.returncode)
        self.assertEqual("migration_interrupted", self.output(interrupted)["reason"])
        self.assertEqual(0, recovered.returncode, recovered.stderr)
        self.assertTrue(self.legacy_registry_path().is_dir())
        self.assertTrue((self.common_directory() / "agent-claim-events").is_file())
        marker = json.loads((self.state_root() / "state.json").read_text(encoding="utf-8"))
        self.assertEqual("complete", marker["migration_status"])

    def test_new_claim_events_share_one_immutable_incarnation_id(self) -> None:
        acquired = self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        heartbeat = self.claim("heartbeat", "--claim-id", "first")
        released = self.claim("release", "--claim-id", "first")

        self.assertEqual(0, acquired.returncode, acquired.stderr)
        self.assertEqual(0, heartbeat.returncode, heartbeat.stderr)
        self.assertEqual(0, released.returncode, released.stderr)
        incarnation_id = self.output(acquired)["claim"]["incarnation_id"]
        self.assertRegex(
            incarnation_id,
            r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$",
        )
        self.assertEqual(
            [incarnation_id, incarnation_id, incarnation_id],
            [event["incarnation_id"] for event in self.journal_events()],
        )

    def test_work_item_claims_contend_by_exact_id_and_distinct_ids_coexist(self) -> None:
        first = self.claim(*self.work_item_arguments("first", "opaque/item:42"))
        conflict = self.claim(
            *self.work_item_arguments("second", "opaque/item:42", "update")
        )
        distinct = self.claim(
            *self.work_item_arguments("third", "opaque/item:43", "update")
        )

        self.assertEqual(0, first.returncode, first.stderr)
        self.assertEqual(3, conflict.returncode)
        self.assertEqual(
            "CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED",
            self.output(conflict)["outcome"],
        )
        self.assertEqual(
            [
                {
                    "claim_id": "first",
                    "claimed": "opaque/item:42",
                    "claimed_kind": "work_item",
                    "requested": "opaque/item:42",
                    "requested_kind": "work_item",
                    "scope_kind": "work_item",
                }
            ],
            self.output(conflict)["overlaps"],
        )
        self.assertEqual(0, distinct.returncode, distinct.stderr)
        handed_off = self.claim(
            "release",
            "--claim-id",
            "first",
            "--disposition",
            "handoff",
        )
        successor = self.claim(
            *self.work_item_arguments("second", "opaque/item:42", "update")
        )
        self.assertEqual(0, handed_off.returncode, handed_off.stderr)
        self.assertEqual(0, successor.returncode, successor.stderr)
        registry = json.loads(self.registry_path().read_text(encoding="utf-8"))
        self.assertEqual(
            [("opaque/item:42", "update"), ("opaque/item:43", "update")],
            sorted(
                (claim["work_item_id"], claim["activity"])
                for claim in registry["claims"]
            ),
        )

    def test_work_item_claim_fields_are_preserved_in_status_and_journal(self) -> None:
        acquired = self.claim(
            *self.work_item_arguments("provider-update", "provider#17", "update")
        )
        status = self.claim("status")

        self.assertEqual(0, acquired.returncode, acquired.stderr)
        claim = self.output(status)["claims"][0]
        self.assertEqual("provider#17", claim["work_item_id"])
        self.assertEqual("update", claim["activity"])
        self.assertEqual("provider-update", claim["claim_id"])
        self.assertEqual("provider-update", claim["agent"])
        self.assertEqual("provider-update", claim["root_task_id"])
        self.assertEqual("SHARED_CHECKOUT_ACQUIRED", claim["acquisition_outcome"])
        self.assertIn("incarnation_id", claim)
        self.assertIn("claimed_at", claim)
        event = self.journal_events()[-1]
        expected_fields = {
            "work_item_id": claim["work_item_id"],
            "activity": claim["activity"],
            "claim_id": claim["claim_id"],
            "incarnation_id": claim["incarnation_id"],
            "agent": claim["agent"],
            "root_task_id": claim["root_task_id"],
        }
        for field, expected in expected_fields.items():
            with self.subTest(field=field):
                self.assertEqual(expected, event[field])
        self.assertIn("timestamp", event)
        self.assertEqual("PRIMARY", event["outcome"])

    def test_work_item_contention_is_independent_of_invalid_stored_path_metadata(self) -> None:
        self.claim(*self.work_item_arguments("first", "item-path-independent"))
        registry = json.loads(self.registry_path().read_text(encoding="utf-8"))
        registry["claims"][0]["files"] = ["../outside"]
        self.registry_path().write_text(
            json.dumps(registry, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        registry_before = self.registry_path().read_bytes()

        conflict = self.claim(
            *self.work_item_arguments(
                "second",
                "item-path-independent",
                "update",
            )
        )

        self.assertEqual(3, conflict.returncode)
        self.assertEqual(
            "work_item",
            self.output(conflict)["overlaps"][0]["scope_kind"],
        )
        if registry_before:
            self.assertEqual(registry_before, self.registry_path().read_bytes())
        else:
            self.assertFalse(self.registry_path().exists())

    def test_invalid_work_item_acquisition_preserves_registry_bytes(self) -> None:
        self.claim(*self.acquire_arguments("legacy"), "--file", "README.md")
        registry_before = self.registry_path().read_bytes()
        invalid_requests = (
            [*self.acquire_arguments("missing-activity"), "--work-item-id", "item-1"],
            [*self.acquire_arguments("missing-id"), "--activity", "work"],
            [*self.work_item_arguments("invalid-activity", "item-2", "review")],
            [
                *self.work_item_arguments("mixed-scope", "item-3"),
                "--file",
                "src/one.py",
            ],
            [*self.work_item_arguments("blank-id", " ")],
            [*self.work_item_arguments("multiline-id", "item\n3")],
        )

        for arguments in invalid_requests:
            with self.subTest(arguments=arguments):
                rejected = self.claim(*arguments)
                self.assertEqual(1, rejected.returncode)
                self.assertEqual(
                    "INVALID_WORK_ITEM_SCOPE",
                    self.output(rejected)["outcome"],
                )
                self.assertEqual(registry_before, self.registry_path().read_bytes())

    def test_work_item_release_requires_valid_disposition_and_blocker_pairing(self) -> None:
        invalid_cases = (
            ([], "disposition_required"),
            (["--disposition", "paused"], "invalid_disposition"),
            (
                ["--disposition", "blocked", "--blocker-reference", ""],
                "invalid_blocker_reference",
            ),
            (
                ["--disposition", "blocked", "--blocker-reference", " dependency-7"],
                "invalid_blocker_reference",
            ),
            (
                ["--disposition", "blocked", "--blocker-reference", "dependency\n7"],
                "invalid_blocker_reference",
            ),
            (
                ["--disposition", "blocked", "--blocker-reference", "x" * 201],
                "invalid_blocker_reference",
            ),
            (
                [
                    "--disposition",
                    "done",
                    "--blocker-reference",
                    "dependency-7",
                ],
                "blocker_reference_not_allowed",
            ),
        )
        for index, (release_arguments, reason) in enumerate(invalid_cases):
            claim_id = f"invalid-release-{index}"
            self.claim(*self.work_item_arguments(claim_id, f"item-{index}"))
            registry_before = self.registry_path().read_bytes()
            rejected = self.claim(
                "release",
                "--claim-id",
                claim_id,
                *release_arguments,
            )
            self.assertEqual(1, rejected.returncode)
            self.assertEqual("INVALID_WORK_ITEM_RELEASE", self.output(rejected)["outcome"])
            self.assertEqual(reason, self.output(rejected)["rejection"]["reason"])
            self.assertEqual(registry_before, self.registry_path().read_bytes())

        releases = (
            ("done", None),
            ("handoff", None),
            ("blocked", "dependency-9"),
        )
        for disposition, blocker_reference in releases:
            claim_id = f"release-{disposition}"
            self.claim(*self.work_item_arguments(claim_id, f"item-{disposition}"))
            arguments = ["release", "--claim-id", claim_id, "--disposition", disposition]
            if blocker_reference:
                arguments.extend(["--blocker-reference", blocker_reference])
            released = self.claim(*arguments)
            self.assertEqual(0, released.returncode, released.stderr)
            result = self.output(released)
            self.assertEqual(disposition, result["disposition"])
            self.assertEqual(blocker_reference, result["blocker_reference"])
            event = self.journal_events()[-1]
            self.assertEqual(disposition, event["disposition"])
            self.assertEqual(blocker_reference, event["blocker_reference"])

    def test_blocked_work_item_release_accepts_no_blocker_reference(self) -> None:
        acquired = self.claim(
            *self.work_item_arguments("blocked-no-reference", "item-blocked-no-reference")
        )
        released = self.claim(
            "release",
            "--claim-id",
            "blocked-no-reference",
            "--disposition",
            "blocked",
        )

        self.assertEqual(0, acquired.returncode, acquired.stderr)
        self.assertEqual(0, released.returncode, released.stderr)
        result = self.output(released)
        self.assertEqual("RELEASED", result["outcome"])
        self.assertEqual("blocked", result["disposition"])
        self.assertIsNone(result["blocker_reference"])
        registry = json.loads(self.registry_path().read_text(encoding="utf-8"))
        self.assertEqual([], registry["claims"])
        event = self.journal_events()[-1]
        self.assertEqual("RELEASED", event["outcome"])
        self.assertEqual("item-blocked-no-reference", event["work_item_id"])
        self.assertEqual("blocked", event["disposition"])
        self.assertIsNone(event["blocker_reference"])

        report = self.output(self.claim("report", "--since", "1d"))["work_items"]
        segment = report["items"][0]["segments"][0]
        self.assertEqual("blocked", segment["disposition"])
        self.assertIsNone(segment["blocker_reference"])
        self.assertEqual([], report["diagnostics"]["contradictory_event_ids"])

    def test_legacy_release_remains_disposition_free(self) -> None:
        self.claim(*self.acquire_arguments("legacy-release"), "--file", "README.md")
        released = self.claim("release", "--claim-id", "legacy-release")

        self.assertEqual(0, released.returncode, released.stderr)
        self.assertNotIn("disposition", self.output(released))

    def test_work_item_path_and_resource_claims_remain_independently_applicable(self) -> None:
        path_claim = self.claim(
            *self.acquire_arguments("path-owner"),
            "--file",
            "README.md",
        )
        resource_claim = self.claim(
            *self.acquire_arguments("resource-owner"),
            *self.timed_resource_arguments(),
        )
        work_item_claim = self.claim(
            *self.work_item_arguments("work-item-owner", "item-independent")
        )

        self.assertEqual(0, path_claim.returncode, path_claim.stderr)
        self.assertEqual(0, resource_claim.returncode, resource_claim.stderr)
        self.assertEqual(0, work_item_claim.returncode, work_item_claim.stderr)
        self.assertEqual(
            ["path-owner", "resource-owner", "work-item-owner"],
            sorted(
                claim["claim_id"]
                for claim in self.output(self.claim("status"))["claims"]
            ),
        )

    def test_work_item_claim_rejects_operational_scope_extensions_without_registry_mutation(
        self,
    ) -> None:
        extension_cases = (
            ("file", ["--file", "README.md"]),
            ("resource", self.timed_resource_arguments()),
        )
        for label, extension_arguments in extension_cases:
            with self.subTest(scope=label):
                claim_id = f"work-item-extend-{label}"
                acquired = self.claim(
                    *self.work_item_arguments(claim_id, f"item-extend-{label}")
                )
                self.assertEqual(0, acquired.returncode, acquired.stderr)
                registry_before = self.registry_path().read_bytes()

                rejected = self.claim(
                    "extend",
                    "--claim-id",
                    claim_id,
                    *extension_arguments,
                )

                self.assertEqual(1, rejected.returncode)
                result = self.output(rejected)
                self.assertEqual("INVALID_WORK_ITEM_SCOPE", result["outcome"])
                self.assertEqual(
                    "work_item_operational_extension",
                    result["rejection"]["reason"],
                )
                self.assertEqual(registry_before, self.registry_path().read_bytes())

    def test_report_groups_versioned_work_item_segments_and_diagnostics(self) -> None:
        acquire_time = {"RESOURCE_CLAIM_TEST_NOW": "2026-08-05T10:00:00Z"}
        release_time = {"RESOURCE_CLAIM_TEST_NOW": "2026-08-05T10:05:00Z"}
        open_time = {"RESOURCE_CLAIM_TEST_NOW": "2026-08-05T10:06:00Z"}
        self.claim(
            *self.work_item_arguments("claim-a", "item-a", "work"),
            environment=acquire_time,
        )
        self.claim(
            "release",
            "--claim-id",
            "claim-a",
            "--disposition",
            "done",
            environment=release_time,
        )
        self.claim(
            *self.work_item_arguments("claim-b", "item-b", "update"),
            environment=open_time,
        )
        existing = self.journal_events()
        synthetic = [
            self.synthetic_event(
                "duplicate-acquire",
                "2026-08-05T10:07:00Z",
                "acquire",
                "PRIMARY",
                "claim-b-duplicate",
                work_item_id="item-b",
                activity="work",
                incarnation_id="incarnation-b-duplicate",
                agent="owner-b-duplicate",
                root_task_id="root-b-duplicate",
            ),
            self.synthetic_event(
                "missing-release",
                "2026-08-05T10:08:00Z",
                "acquire",
                "PRIMARY",
                "claim-d",
                work_item_id="item-d",
                activity="work",
                incarnation_id="incarnation-d",
                agent="owner-d",
                root_task_id="root-d",
            ),
            self.synthetic_event(
                "release-only",
                "2026-08-05T10:09:00Z",
                "release",
                "RELEASED",
                "claim-c",
                work_item_id="item-c",
                activity="update",
                disposition="handoff",
                blocker_reference=None,
                incarnation_id="incarnation-c",
                agent="owner-c",
                root_task_id="root-c",
            ),
            self.synthetic_event(
                "legacy-event",
                "2026-08-05T10:10:00Z",
                "acquire",
                "PRIMARY",
                "legacy-claim",
            ),
        ]
        self.write_daily_events("2026-08-05", [*existing, *synthetic])

        completed = self.claim(
            "report",
            "--since",
            "1d",
            environment={"RESOURCE_CLAIM_TEST_NOW": "2026-08-05T12:00:00Z"},
        )

        self.assertEqual(0, completed.returncode, completed.stderr)
        report = self.output(completed)
        self.assertEqual("REPORT", report["outcome"])
        self.assertEqual(2, report["schema_version"])
        work_items = report["work_items"]
        self.assertEqual(1, work_items["schema_version"])
        self.assertEqual(
            ["item-a", "item-b", "item-d"],
            [item["work_item_id"] for item in work_items["items"]],
        )
        item_a = work_items["items"][0]["segments"][0]
        self.assertEqual("2026-08-05T10:00:00.000000Z", item_a["acquired_at"])
        self.assertEqual("2026-08-05T10:05:00.000000Z", item_a["released_at"])
        self.assertEqual(300.0, item_a["duration_seconds"])
        self.assertEqual("work", item_a["activity"])
        self.assertEqual("done", item_a["disposition"])
        self.assertFalse(item_a["open"])
        self.assertFalse(item_a["live"])
        item_b_segments = work_items["items"][1]["segments"]
        self.assertTrue(item_b_segments[0]["open"])
        self.assertTrue(item_b_segments[0]["live"])
        diagnostics = work_items["diagnostics"]
        self.assertEqual(["missing-release"], diagnostics["missing_release_event_ids"])
        self.assertEqual(["release-only"], diagnostics["release_without_acquisition_event_ids"])
        self.assertEqual(
            ["duplicate-acquire"],
            diagnostics["contradictory_event_ids"],
        )
        self.assertEqual(
            ["legacy-event"],
            diagnostics["historical_non_work_item_event_ids"],
        )

    def test_report_reconstructs_work_item_segments_across_window_boundary(self) -> None:
        before_window = {"RESOURCE_CLAIM_TEST_NOW": "2026-08-03T10:00:00Z"}
        inside_window = {"RESOURCE_CLAIM_TEST_NOW": "2026-08-05T10:00:00Z"}
        report_time = {"RESOURCE_CLAIM_TEST_NOW": "2026-08-05T12:00:00Z"}
        self.claim(
            *self.work_item_arguments("live-old", "item-live-old"),
            environment=before_window,
        )
        self.claim(
            *self.work_item_arguments("released-now", "item-released-now"),
            environment=before_window,
        )
        self.claim(
            "release",
            "--claim-id",
            "released-now",
            "--disposition",
            "done",
            environment=inside_window,
        )
        before_window_events = [
            json.loads(line)
            for line in (
                self.hot_directory() / "2026-08-03.jsonl"
            ).read_text(encoding="utf-8").splitlines()
        ]
        self.write_daily_events(
            "2026-08-03",
            [
                *before_window_events,
                self.synthetic_event(
                    "orphan-old-acquire",
                    "2026-08-03T11:00:00.000000Z",
                    "acquire",
                    "PRIMARY",
                    "orphan-old",
                    work_item_id="item-orphan-old",
                    activity="work",
                    incarnation_id="incarnation-orphan-old",
                    agent="owner-orphan-old",
                    root_task_id="root-orphan-old",
                ),
            ],
        )

        report = self.output(
            self.claim("report", "--since", "1d", environment=report_time)
        )["work_items"]

        self.assertEqual(
            ["item-live-old", "item-orphan-old", "item-released-now"],
            [item["work_item_id"] for item in report["items"]],
        )
        live_segment = report["items"][0]["segments"][0]
        orphan_segment = report["items"][1]["segments"][0]
        released_segment = report["items"][2]["segments"][0]
        self.assertTrue(live_segment["open"])
        self.assertTrue(live_segment["live"])
        self.assertTrue(orphan_segment["open"])
        self.assertFalse(orphan_segment["live"])
        self.assertFalse(released_segment["open"])
        self.assertEqual("done", released_segment["disposition"])
        self.assertEqual(
            ["orphan-old-acquire"],
            report["diagnostics"]["missing_release_event_ids"],
        )
        self.assertEqual([], report["diagnostics"]["release_without_acquisition_event_ids"])

    def test_release_cleans_only_the_exact_claim_without_git_or_delivery_validation(
        self,
    ) -> None:
        first = self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        second = self.claim(*self.acquire_arguments("second"), "--file", "docs/guide.md")
        tree = self.git("rev-parse", "HEAD^{tree}").stdout.strip()
        unrelated_head = self.git("commit-tree", tree, "-m", "unrelated primary").stdout.strip()
        self.git("reset", "--hard", unrelated_head)
        (self.repository / "README.md").write_text("dirty uncommitted work\n", encoding="utf-8")

        released = self.claim("release", "--claim-id", "first")

        self.assertEqual(0, first.returncode, first.stderr)
        self.assertEqual(0, second.returncode, second.stderr)
        self.assertEqual(0, released.returncode, released.stderr)
        result = self.output(released)
        self.assertEqual("RELEASED", result["outcome"])
        self.assertEqual("first", result["claim"]["claim_id"])
        self.assertEqual(
            ["second"],
            [claim["claim_id"] for claim in self.output(self.claim("status"))["claims"]],
        )
        release_events = [
            event
            for event in self.journal_events()
            if event["action"] == "release" and event["claim_id"] == "first"
        ]
        self.assertEqual(["RELEASED"], [event["outcome"] for event in release_events])
        self.assertIsNone(release_events[0]["resulting_commit"])
        self.assertNotIn("no_change", release_events[0])
        self.assertEqual("first", release_events[0]["claim_id"])
        self.assertEqual("first", release_events[0]["agent"])
        self.assertEqual("first", release_events[0]["root_task_id"])
        self.assertEqual(
            self.output(first)["claim"]["files"],
            release_events[0]["scopes"]["files"],
        )
        self.assertEqual(
            self.output(first)["claim"]["baseline_commit"],
            release_events[0]["baseline_commit"],
        )

    def test_reset_replaces_missing_valid_or_invalid_registry_with_empty_claims(
        self,
    ) -> None:
        cases = (
            ("missing", None, 0, True),
            ("valid", '{"claims":[{"claim_id":"stale"}]}\n', 1, True),
            ("malformed", '{"claims":[', None, False),
            ("non_object_null", "null\n", None, False),
            ("non_object_array", "[]\n", None, False),
            ("non_object_string", '"claims"\n', None, False),
            ("non_object_number", "1\n", None, False),
            ("non_object_boolean", "true\n", None, False),
            ("missing_claims", "{}\n", None, False),
            ("claims_not_list", '{"claims":{}}\n', None, False),
        )
        for name, content, removed_count, previous_valid in cases:
            with self.subTest(name=name):
                self.registry_path().unlink(missing_ok=True)
                if content is not None:
                    self.registry_path().write_text(content, encoding="utf-8")

                reset = self.claim("reset")

                self.assertEqual(0, reset.returncode, reset.stderr)
                self.assertEqual("RESET", self.output(reset)["outcome"])
                self.assertEqual(
                    {"claims": []},
                    json.loads(self.registry_path().read_text(encoding="utf-8")),
                )
                event = self.journal_events()[-1]
                self.assertEqual("RESET", event["outcome"])
                self.assertEqual(previous_valid, event["previous_registry_valid"])
                self.assertEqual(removed_count, event["removed_claim_count"])

    def test_release_rejects_removed_completion_and_reconciliation_flags_atomically(
        self,
    ) -> None:
        acquired = self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        self.assertEqual(0, acquired.returncode, acquired.stderr)
        registry_before = self.registry_path().read_bytes()
        events_before = self.journal_events()

        removed_options = (
            ("--no-change",),
            ("--reconcile-out-of-domain-commit", "f" * 40),
            ("--prior-rejected-release-reference", "prior-event"),
        )
        for option in removed_options:
            with self.subTest(option=option):
                rejected = self.claim("release", "--claim-id", "first", *option)
                self.assertEqual(2, rejected.returncode)
                self.assertIn("unrecognized arguments", rejected.stderr)
                self.assertEqual(registry_before, self.registry_path().read_bytes())
                self.assertEqual(events_before, self.journal_events())

    def test_release_claim_not_found_preserves_live_registry(self) -> None:
        acquired = self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        self.assertEqual(0, acquired.returncode, acquired.stderr)
        registry_before = self.registry_path().read_bytes()

        missing = self.claim("release", "--claim-id", "missing")

        self.assertEqual(1, missing.returncode)
        self.assertEqual("CLAIM_NOT_FOUND", self.output(missing)["outcome"])
        self.assertEqual(registry_before, self.registry_path().read_bytes())
        self.assertEqual(
            ["first"],
            [claim["claim_id"] for claim in self.output(self.claim("status"))["claims"]],
        )

    def test_registry_mutations_keep_the_directly_locked_inode(self) -> None:
        acquired = self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        self.assertEqual(0, acquired.returncode, acquired.stderr)
        registry_inode = self.registry_path().stat().st_ino

        heartbeat = self.claim("heartbeat", "--claim-id", "first")
        released = self.claim("release", "--claim-id", "first")

        self.assertEqual(0, heartbeat.returncode, heartbeat.stderr)
        self.assertEqual(0, released.returncode, released.stderr)
        self.assertEqual(registry_inode, self.registry_path().stat().st_ino)
        self.assertFalse((self.common_directory() / "resource-claims.lock").exists())

    @unittest.skipIf(os.name == "nt", "The fixture directly exercises POSIX fcntl crash cleanup.")
    def test_registry_os_lock_is_released_when_holder_process_crashes(self) -> None:
        acquired = self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        self.assertEqual(0, acquired.returncode, acquired.stderr)
        holder = subprocess.Popen(
            [
                sys.executable,
                "-c",
                (
                    "import fcntl, sys, time; "
                    "registry = open(sys.argv[1], 'r+', encoding='utf-8'); "
                    "fcntl.flock(registry.fileno(), fcntl.LOCK_EX); "
                    "print('locked', flush=True); "
                    "time.sleep(30)"
                ),
                str(self.registry_path()),
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.addCleanup(lambda: holder.poll() is None and holder.kill())
        self.assertIsNotNone(holder.stdout)
        self.assertEqual("locked", holder.stdout.readline().strip())
        waiting_status = subprocess.Popen(
            self.claim_command("status"),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.addCleanup(lambda: waiting_status.poll() is None and waiting_status.kill())
        time.sleep(0.2)
        self.assertIsNone(waiting_status.poll())

        holder.kill()
        holder.communicate(timeout=5)
        stdout, stderr = waiting_status.communicate(timeout=5)

        self.assertEqual(0, waiting_status.returncode, stderr)
        self.assertEqual("STATUS", json.loads(stdout)["outcome"])

    def test_first_writer_in_existing_linked_checkout_reports_linked_topology(self) -> None:
        linked_path = self.existing_linked_worktree()
        primary_head = self.git("rev-parse", "HEAD").stdout
        primary_status = self.git("status", "--porcelain=v1").stdout

        completed = self.claim(
            *self.acquire_arguments("private"),
            "--file",
            "README.md",
            repo=linked_path,
        )

        self.assertEqual(0, completed.returncode, completed.stderr)
        result = self.output(completed)
        self.assertEqual("SHARED_CHECKOUT_ACQUIRED", result["outcome"])
        self.assertEqual("PRIMARY", result["legacy_outcome"])
        self.assertEqual("primary", result["claim"]["mode"])
        self.assertEqual("linked", result["claim"]["checkout_topology"])
        self.assertEqual(str(linked_path), result["claim"]["worktree"])
        self.assertEqual("primary", result["target"]["mode"])
        self.assertEqual("linked", result["target"]["checkout_topology"])
        self.assertFalse((self.repository / ".worktrees" / "private").exists())
        self.assertEqual(primary_head, self.git("rev-parse", "HEAD").stdout)
        self.assertEqual(primary_status, self.git("status", "--porcelain=v1").stdout)
        event = self.journal_events()[-1]
        self.assertEqual("linked", event["checkout_topology"])
        self.assertEqual("codex/private", event["worktree_id"])
        self.assertEqual("codex/private", event["branch"])
        self.assertNotIn(str(self.temporary_directory.name), json.dumps(event))

    def test_linked_exact_file_claim_cannot_extend_to_project_files(self) -> None:
        linked_path = self.existing_linked_worktree()
        acquired = self.claim(
            *self.acquire_arguments("private"),
            "--file",
            "README.md",
            repo=linked_path,
        )
        self.assertEqual(0, acquired.returncode, acquired.stderr)
        acquired_claim = self.output(acquired)["claim"]
        registry_before = self.registry_path().read_bytes()

        extended = self.claim(
            "extend",
            "--claim-id",
            "private",
            "--project-files",
            "--scope-reason",
            "primary integration",
            repo=linked_path,
        )

        self.assertEqual(3, extended.returncode, extended.stderr)
        result = self.output(extended)
        self.assertEqual("SHARED_CHECKOUT_REQUIRED", result["outcome"])
        self.assertEqual("PRIMARY_REQUIRED", result["legacy_outcome"])
        self.assertEqual("project_files_requires_primary_worktree", result["reason"])
        self.assertEqual(registry_before, self.registry_path().read_bytes())
        stored = self.output(self.claim("status"))["claims"][0]
        self.assertEqual(acquired_claim["files"], stored["files"])
        self.assertIs(stored["project_files"], False)
        self.assertEqual("linked", stored["checkout_topology"])

    def test_primary_exact_file_claim_can_extend_to_project_files(self) -> None:
        acquired = self.claim(
            *self.acquire_arguments("primary"),
            "--file",
            "README.md",
        )
        self.assertEqual(0, acquired.returncode, acquired.stderr)

        extended = self.claim(
            "extend",
            "--claim-id",
            "primary",
            "--project-files",
            "--scope-reason",
            "primary integration",
        )

        self.assertEqual(0, extended.returncode, extended.stderr)
        claim = self.output(extended)["claim"]
        self.assertIs(claim["project_files"], True)
        self.assertEqual("primary", claim["checkout_topology"])

    def test_linked_project_files_extension_reports_conflict_before_location(self) -> None:
        primary = self.claim(
            *self.acquire_arguments("primary"),
            "--file",
            "docs/guide.md",
        )
        self.assertEqual(0, primary.returncode, primary.stderr)
        linked_path = self.existing_linked_worktree()
        linked = self.claim(
            *self.acquire_arguments("linked"),
            "--file",
            "README.md",
            repo=linked_path,
        )
        self.assertEqual(0, linked.returncode, linked.stderr)
        registry_before = self.registry_path().read_bytes()

        extended = self.claim(
            "extend",
            "--claim-id",
            "linked",
            "--project-files",
            "--scope-reason",
            "primary integration",
            repo=linked_path,
        )

        self.assertEqual(3, extended.returncode, extended.stderr)
        result = self.output(extended)
        self.assertEqual("CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED", result["outcome"])
        self.assertEqual(["primary"], result["conflicting_claim_ids"])
        self.assertEqual(registry_before, self.registry_path().read_bytes())

    def test_linked_project_files_require_primary_before_non_ancestral_integration(self) -> None:
        linked_path = self.existing_linked_worktree()
        baseline_commit = self.git("rev-parse", "HEAD").stdout.strip()

        linked_acquisition = self.claim(
            *self.acquire_arguments("project"),
            "--project-files",
            "--scope-reason",
            "primary integration",
            repo=linked_path,
        )

        self.assertEqual(3, linked_acquisition.returncode, linked_acquisition.stderr)
        linked_result = self.output(linked_acquisition)
        self.assertEqual("SHARED_CHECKOUT_REQUIRED", linked_result["outcome"])
        self.assertEqual("PRIMARY_REQUIRED", linked_result["legacy_outcome"])
        self.assertEqual("project_files_requires_primary_worktree", linked_result["reason"])
        self.assertEqual(
            "Project-files scope is available only from the primary worktree.",
            linked_result["message"],
        )
        self.assertEqual([], self.output(self.claim("status"))["claims"])
        linked_event = self.journal_events()[-1]
        self.assertEqual("PRIMARY_REQUIRED", linked_event["outcome"])
        self.assertEqual("project_files_requires_primary_worktree", linked_event["reason"])
        self.assertIs(linked_event["shared_checkout_claimed"], False)
        self.assertIs(linked_event["requested_scopes"]["project_files"], True)

        (linked_path / "src" / "one.py").write_text("integrated\n", encoding="utf-8")
        self.git("add", "src/one.py", worktree=linked_path)
        self.git("commit", "-m", "candidate project change", worktree=linked_path)
        linked_candidate = self.git("rev-parse", "HEAD", worktree=linked_path).stdout.strip()

        primary_acquisition = self.claim(
            *self.acquire_arguments("project"),
            "--project-files",
            "--scope-reason",
            "primary integration",
        )
        self.assertEqual(0, primary_acquisition.returncode, primary_acquisition.stderr)
        primary_claim = self.output(primary_acquisition)["claim"]
        self.assertEqual(str(self.repository.resolve()), primary_claim["worktree"])
        self.assertEqual("primary", primary_claim["checkout_topology"])

        (self.repository / "src" / "one.py").write_text("integrated\n", encoding="utf-8")
        self.git("add", "src/one.py")
        self.git("commit", "-m", "non-ancestral primary integration")
        primary_head = self.git("rev-parse", "HEAD").stdout.strip()
        ancestry = subprocess.run(
            [
                "git",
                "-C",
                str(self.repository),
                "merge-base",
                "--is-ancestor",
                linked_candidate,
                primary_head,
            ],
            check=False,
            text=True,
            capture_output=True,
        )

        self.assertEqual(1, ancestry.returncode, ancestry.stderr)
        self.assertEqual(
            baseline_commit,
            self.git("merge-base", primary_head, linked_candidate).stdout.strip(),
        )
        self.assertEqual(
            self.git("rev-parse", f"{linked_candidate}^{{tree}}").stdout.strip(),
            self.git("rev-parse", f"{primary_head}^{{tree}}").stdout.strip(),
        )

        released = self.claim("release", "--claim-id", "project")

        self.assertEqual(0, released.returncode, released.stderr)
        self.assertEqual("RELEASED", self.output(released)["outcome"])
        self.assertEqual([], self.output(self.claim("status"))["claims"])

    def test_timed_resource_acquisition_records_complete_deadline_evidence(self) -> None:
        acquired = self.claim(
            *self.acquire_arguments("timed"),
            *self.timed_resource_arguments(),
            environment={"RESOURCE_CLAIM_TEST_NOW": "2026-07-22T10:00:00Z"},
        )

        self.assertEqual(0, acquired.returncode, acquired.stderr)
        result = self.output(acquired)
        deadline = result["claim"]["deadline"]
        self.assertEqual("database-port", deadline["resource_class"])
        self.assertEqual("port:3000", deadline["resource_id"])
        self.assertEqual(300, deadline["expected_duration_seconds"])
        self.assertEqual(900, deadline["requested_hard_stop_duration_seconds"])
        self.assertEqual(1800, deadline["configured_maximum_duration_seconds"])
        self.assertEqual(300, deadline["cleanup_grace_seconds"])
        self.assertEqual("2026-07-22T10:05:00.000000Z", deadline["expected_release_at"])
        self.assertEqual("2026-07-22T10:15:00.000000Z", deadline["hard_stop_at"])
        self.assertEqual("2026-07-22T10:20:00.000000Z", deadline["cleanup_grace_ends_at"])
        self.assertEqual([], deadline["extensions"])
        event = self.journal_events()[-1]
        self.assertEqual(deadline, event["deadline"])

    def test_timed_resource_acquisition_rejects_incomplete_or_invalid_ordering(self) -> None:
        cases = (
            (
                ["--resource", "port:3000"],
                "Named resource acquisition requires complete timing evidence",
            ),
            (
                ["--resource", "port:3000", "--expected-duration-seconds", "300"],
                "timing arguments must be supplied together",
            ),
            (
                [
                    *self.timed_resource_arguments(),
                    "--expected-duration-seconds",
                    "901",
                ],
                "expected duration must not exceed requested hard stop",
            ),
            (
                [
                    *self.timed_resource_arguments(),
                    "--requested-hard-stop-duration-seconds",
                    "1801",
                ],
                "requested hard stop must not exceed configured maximum",
            ),
        )

        for index, (arguments, message) in enumerate(cases):
            with self.subTest(message=message):
                rejected = self.claim(
                    *self.acquire_arguments(f"invalid-{index}"),
                    *arguments,
                )
                self.assertEqual(1, rejected.returncode, rejected.stderr)
                result = self.output(rejected)
                self.assertEqual("INVALID_DEADLINE_POLICY", result["outcome"])
                self.assertIn(message, result["message"])

        status = self.output(self.claim("status"))
        self.assertEqual([], status["claims"])

    def test_timed_resource_rejects_missing_invalid_or_unselected_project_policy(self) -> None:
        cases: tuple[tuple[dict[str, object] | None, str], ...] = (
            (None, "PROJECT.yaml is required for named resource acquisition"),
            ({}, "resource_coordination must select resource-claim"),
            (
                {"resource_coordination": {"selected": "none"}},
                "resource_coordination must select resource-claim",
            ),
            (
                {
                    "resource_coordination": {
                        "selected": "resource-claim",
                        "deadline_policy": {"resource_classes": {}, "resource_overrides": {}},
                    }
                },
                "resource_classes keys must be exactly",
            ),
        )

        for index, (policy, message) in enumerate(cases):
            with self.subTest(message=message):
                if policy is None:
                    (self.repository / "PROJECT.yaml").unlink()
                else:
                    self.write_deadline_policy(policy)
                rejected = self.claim(
                    *self.acquire_arguments(f"policy-{index}"),
                    *self.timed_resource_arguments(),
                )
                self.assertEqual(1, rejected.returncode, rejected.stderr)
                self.assertEqual("INVALID_DEADLINE_POLICY", self.output(rejected)["outcome"])
                self.assertIn(message, self.output(rejected)["message"])
                self.write_deadline_policy()

    def test_exact_resource_override_replaces_class_default(self) -> None:
        policy = self.deadline_policy()
        policy["resource_coordination"]["deadline_policy"]["resource_overrides"] = {
            "port:3000": {
                "resource_class": "database-port",
                "maximum_duration_seconds": 1200,
                "cleanup_grace_seconds": 120,
            }
        }
        self.write_deadline_policy(policy)
        self.git("add", "PROJECT.yaml")
        self.git("commit", "-m", "configure exact resource override")

        acquired = self.claim(
            *self.acquire_arguments("override"),
            *self.timed_resource_arguments(requested_hard_stop_duration_seconds=1200),
        )

        self.assertEqual(0, acquired.returncode, acquired.stderr)
        deadline = self.output(acquired)["claim"]["deadline"]
        self.assertEqual(1200, deadline["configured_maximum_duration_seconds"])
        self.assertEqual(120, deadline["cleanup_grace_seconds"])

    def test_resource_class_and_exact_override_binding_must_be_configured(self) -> None:
        unknown_class = self.claim(
            *self.acquire_arguments("unknown-class"),
            *self.timed_resource_arguments(resource_class="unknown-class"),
        )
        self.assertEqual(1, unknown_class.returncode, unknown_class.stderr)
        self.assertIn("must name a configured PROJECT.yaml resource class", self.output(unknown_class)["message"])

        policy = self.deadline_policy()
        policy["resource_coordination"]["deadline_policy"]["resource_overrides"] = {
            "port:3000": {
                "resource_class": "browser-server",
                "maximum_duration_seconds": 1200,
                "cleanup_grace_seconds": 120,
            }
        }
        self.write_deadline_policy(policy)
        mismatch = self.claim(
            *self.acquire_arguments("override-mismatch"),
            *self.timed_resource_arguments(resource_class="database-port"),
        )

        self.assertEqual(1, mismatch.returncode, mismatch.stderr)
        self.assertIn("is configured for resource class browser-server", self.output(mismatch)["message"])

    def test_resource_id_is_canonicalized_before_policy_resolution_and_storage(self) -> None:
        acquired = self.claim(
            *self.acquire_arguments("normalized"),
            *self.timed_resource_arguments(
                resource="  port:3000  ",
                resource_id=" port:3000 ",
            ),
        )

        self.assertEqual(0, acquired.returncode, acquired.stderr)
        claim = self.output(acquired)["claim"]
        self.assertEqual(["port:3000"], claim["resources"])
        self.assertEqual("port:3000", claim["deadline"]["resource_id"])

    def test_resource_claim_rejects_multiple_resources_and_caller_asserted_policy(self) -> None:
        multiple = self.claim(
            *self.acquire_arguments("multiple"),
            *self.timed_resource_arguments(),
            "--resource",
            "database:secondary",
        )
        caller_maximum = self.claim(
            *self.acquire_arguments("caller-maximum"),
            *self.timed_resource_arguments(),
            "--configured-maximum-duration-seconds",
            "999999",
        )

        self.assertEqual(1, multiple.returncode, multiple.stderr)
        self.assertEqual("INVALID_DEADLINE_POLICY", self.output(multiple)["outcome"])
        self.assertIn("exactly one named resource", self.output(multiple)["message"])
        self.assertEqual(2, caller_maximum.returncode)
        self.assertIn("unrecognized arguments", caller_maximum.stderr)

    def test_file_claim_can_add_one_timed_resource_but_cannot_add_a_second(self) -> None:
        acquired = self.claim(*self.acquire_arguments("extend-resource"), "--file", "README.md")
        extended = self.claim(
            "extend",
            "--claim-id",
            "extend-resource",
            *self.timed_resource_arguments(),
            environment={"RESOURCE_CLAIM_TEST_NOW": "2026-07-22T11:00:00Z"},
        )
        registry_before_second = self.registry_path().read_bytes()
        second = self.claim(
            "extend",
            "--claim-id",
            "extend-resource",
            *self.timed_resource_arguments(
                resource="database:secondary",
                resource_class="database-port",
            ),
        )

        self.assertEqual(0, acquired.returncode, acquired.stderr)
        self.assertEqual(0, extended.returncode, extended.stderr)
        deadline = self.output(extended)["claim"]["deadline"]
        self.assertEqual("2026-07-22T11:00:00.000000Z", deadline["acquired_at"])
        self.assertEqual(["port:3000"], self.output(extended)["claim"]["resources"])
        self.assertEqual(1, second.returncode, second.stderr)
        self.assertEqual("INVALID_DEADLINE_POLICY", self.output(second)["outcome"])
        self.assertIn("cannot add a second named resource", self.output(second)["message"])
        self.assertEqual(registry_before_second, self.registry_path().read_bytes())

    def test_file_claim_rejects_untimed_resource_extension(self) -> None:
        acquired = self.claim(*self.acquire_arguments("extend-untimed"), "--file", "README.md")
        extended = self.claim(
            "extend",
            "--claim-id",
            "extend-untimed",
            "--resource",
            "port:3000",
        )

        self.assertEqual(0, acquired.returncode, acquired.stderr)
        self.assertEqual(1, extended.returncode, extended.stderr)
        self.assertEqual("INVALID_DEADLINE_POLICY", self.output(extended)["outcome"])

    def test_heartbeat_preserves_hard_stop_and_evidence_backed_extension_is_bounded(self) -> None:
        acquired = self.claim(
            *self.acquire_arguments("timed"),
            *self.timed_resource_arguments(),
            environment={"RESOURCE_CLAIM_TEST_NOW": "2026-07-22T10:00:00Z"},
        )
        extended = self.claim(
            "extend-deadline",
            "--claim-id",
            "timed",
            "--requested-hard-stop-duration-seconds",
            "1200",
            "--extension-evidence",
            "browser fixture needs one final deterministic assertion",
            environment={"RESOURCE_CLAIM_TEST_NOW": "2026-07-22T10:10:00Z"},
        )
        heartbeat = self.claim(
            "heartbeat",
            "--claim-id",
            "timed",
            environment={"RESOURCE_CLAIM_TEST_NOW": "2026-07-22T10:19:00Z"},
        )

        self.assertEqual(0, acquired.returncode, acquired.stderr)
        self.assertEqual(0, extended.returncode, extended.stderr)
        self.assertEqual(0, heartbeat.returncode, heartbeat.stderr)
        deadline = self.output(heartbeat)["claim"]["deadline"]
        self.assertEqual("2026-07-22T10:20:00.000000Z", deadline["hard_stop_at"])
        self.assertEqual(1200, deadline["requested_hard_stop_duration_seconds"])
        self.assertEqual(1, len(deadline["extensions"]))
        self.assertEqual(
            "browser fixture needs one final deterministic assertion",
            deadline["extensions"][0]["evidence"],
        )
        self.assertEqual("2026-07-22T10:19:00.000000Z", self.output(heartbeat)["claim"]["heartbeat"])
        extension_event = next(
            event
            for event in self.journal_events()
            if event["action"] == "extend-deadline" and event["outcome"] == "DEADLINE_EXTENDED"
        )
        self.assertEqual(900, extension_event["deadline_extension"]["previous_requested_hard_stop_duration_seconds"])
        self.assertEqual(1200, extension_event["deadline_extension"]["requested_hard_stop_duration_seconds"])
        self.assertEqual(1800, extension_event["deadline"]["configured_maximum_duration_seconds"])

        registry_before_rejection = self.registry_path().read_bytes()
        rejected = self.claim(
            "extend-deadline",
            "--claim-id",
            "timed",
            "--requested-hard-stop-duration-seconds",
            "1801",
            "--extension-evidence",
            "unsupported extra time",
        )
        self.assertEqual(1, rejected.returncode, rejected.stderr)
        self.assertEqual("INVALID_DEADLINE_EXTENSION", self.output(rejected)["outcome"])
        self.assertEqual(registry_before_rejection, self.registry_path().read_bytes())

    def test_status_keeps_overdue_claim_visible_without_delivery_inference_or_auto_release(self) -> None:
        acquired = self.claim(
            *self.acquire_arguments("timed"),
            *self.timed_resource_arguments(),
            environment={"RESOURCE_CLAIM_TEST_NOW": "2026-07-22T10:00:00Z"},
        )
        registry_before_status = self.registry_path().read_bytes()
        status = self.claim(
            "status",
            environment={"RESOURCE_CLAIM_TEST_NOW": "2026-07-22T10:17:00Z"},
        )

        self.assertEqual(0, acquired.returncode, acquired.stderr)
        self.assertEqual(0, status.returncode, status.stderr)
        claims = self.output(status)["claims"]
        self.assertEqual(1, len(claims))
        health = claims[0]["deadline_status"]
        self.assertTrue(health["overdue"])
        self.assertEqual(
            {
                "seconds": 300,
                "ends_at": "2026-07-22T10:20:00.000000Z",
                "active": True,
                "elapsed": False,
            },
            health["cleanup_grace"],
        )
        self.assertEqual(
            {
                "owner_stopped": None,
                "immediately_actionable_when_stopped": True,
            },
            health["stopped_owner_actionability_inputs"],
        )
        self.assertNotIn("delivery_status", health)
        self.assertNotIn("completion_ready", health)
        self.assertEqual(registry_before_status, self.registry_path().read_bytes())

    def test_second_independent_writer_gets_isolated_worktree(self) -> None:
        first = self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        isolated, isolated_path = self.isolated_arguments("second")
        second = self.claim(
            *self.acquire_arguments("second"),
            "--file",
            "src/one.py",
            *isolated,
        )

        self.assertEqual(0, first.returncode, first.stderr)
        self.assertEqual(0, second.returncode, second.stderr)
        result = self.output(second)
        self.assertEqual("ISOLATED_CHECKOUT_ACQUIRED", result["outcome"])
        self.assertEqual("ISOLATE", result["legacy_outcome"])
        self.assertEqual(str(isolated_path), result["target"]["worktree"])
        self.assertEqual("linked", result["claim"]["checkout_topology"])
        self.assertEqual("linked", result["target"]["checkout_topology"])
        self.assertTrue((isolated_path / ".git").is_file())
        self.assertTrue((isolated_path / "src" / "one.py").is_file())
        self.assertFalse((isolated_path / "backlog").exists())
        self.assertTrue((self.repository / "backlog" / "feature-backlog" / "queued.md").is_file())
        self.assertEqual("", self.git("status", "--porcelain").stdout)
        event = self.journal_events()[-1]
        self.assertEqual("linked", event["checkout_topology"])
        self.assertEqual("codex/second", event["worktree_id"])
        self.assertNotIn(str(self.temporary_directory.name), json.dumps(event))

    def test_existing_linked_checkout_with_active_peer_uses_canonical_isolation(self) -> None:
        linked_path = self.existing_linked_worktree()
        first = self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        isolated, isolated_path = self.isolated_arguments("second")
        primary_head = self.git("rev-parse", "HEAD").stdout
        primary_status = self.git("status", "--porcelain=v1").stdout
        linked_head = self.git("rev-parse", "HEAD", worktree=linked_path).stdout
        linked_status = self.git("status", "--porcelain=v1", worktree=linked_path).stdout

        second = self.claim(
            *self.acquire_arguments("second"),
            "--file",
            "src/one.py",
            *isolated,
            repo=linked_path,
        )

        self.assertEqual(0, first.returncode, first.stderr)
        self.assertEqual(0, second.returncode, second.stderr)
        result = self.output(second)
        self.assertEqual("ISOLATED_CHECKOUT_ACQUIRED", result["outcome"])
        self.assertEqual("ISOLATE", result["legacy_outcome"])
        self.assertEqual("isolated", result["claim"]["mode"])
        self.assertEqual("linked", result["claim"]["checkout_topology"])
        self.assertEqual(str(isolated_path), result["target"]["worktree"])
        self.assertEqual("linked", result["target"]["checkout_topology"])
        self.assertNotEqual(linked_path, isolated_path)
        self.assertEqual(primary_head, self.git("rev-parse", "HEAD").stdout)
        self.assertEqual(primary_status, self.git("status", "--porcelain=v1").stdout)
        self.assertEqual(linked_head, self.git("rev-parse", "HEAD", worktree=linked_path).stdout)
        self.assertEqual(linked_status, self.git("status", "--porcelain=v1", worktree=linked_path).stdout)
        event = self.journal_events()[-1]
        self.assertEqual("linked", event["checkout_topology"])
        self.assertEqual("codex/second", event["worktree_id"])
        self.assertNotIn(str(self.temporary_directory.name), json.dumps(event))

    def test_nonoverlapping_primary_claims_coexist_without_isolation(self) -> None:
        self.claim(*self.acquire_arguments("first"), "--file", "README.md")

        completed = self.claim(*self.acquire_arguments("second"), "--file", "src/one.py")

        self.assertEqual(0, completed.returncode, completed.stderr)
        result = self.output(completed)
        self.assertEqual("SHARED_CHECKOUT_ACQUIRED", result["outcome"])
        self.assertNotEqual("SHARED_CHECKOUT_RELEASE_REQUIRED", result["outcome"])
        self.assertEqual("primary", result["claim"]["checkout_topology"])
        self.assertEqual(
            ["first", "second"],
            [claim["claim_id"] for claim in self.output(self.claim("status"))["claims"]],
        )

    def test_explicit_worktree_path_must_match_the_canonical_target(self) -> None:
        self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        outside_path = Path(self.temporary_directory.name) / "outside"

        completed = self.claim(
            *self.acquire_arguments("second"),
            "--file",
            "src/one.py",
            "--branch",
            "codex/second",
            "--worktree-path",
            str(outside_path),
        )

        self.assertEqual(1, completed.returncode)
        result = self.output(completed)
        self.assertEqual(2, result["schema_version"])
        self.assertEqual("INVALID_WORKTREE_PATH", result["outcome"])
        self.assertNotIn("legacy_outcome", result)
        self.assertEqual(
            str((self.repository / ".worktrees" / "second").resolve()),
            result["expected_worktree"],
        )
        self.assertFalse(outside_path.exists())

    def test_compatible_caller_may_supply_the_exact_canonical_worktree_path(self) -> None:
        self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        canonical_path = (self.repository / ".worktrees" / "second").resolve()

        completed = self.claim(
            *self.acquire_arguments("second"),
            "--file",
            "src/one.py",
            "--branch",
            "codex/second",
            "--worktree-path",
            str(canonical_path),
        )

        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertEqual(str(canonical_path), self.output(completed)["target"]["worktree"])

    def test_isolation_requires_the_canonical_root_to_be_ignored(self) -> None:
        (self.repository / ".gitignore").write_text("", encoding="utf-8")
        self.git("add", ".gitignore")
        self.git("commit", "-m", "remove worktree ignore")
        self.claim(*self.acquire_arguments("first"), "--file", "README.md")

        completed = self.claim(
            *self.acquire_arguments("second"),
            "--file",
            "src/one.py",
            "--branch",
            "codex/second",
        )

        self.assertEqual(1, completed.returncode)
        result = self.output(completed)
        self.assertEqual("WORKTREE_ROOT_NOT_IGNORED", result["outcome"])
        self.assertEqual("/.worktrees/", result["required_ignore_pattern"])
        self.assertFalse((self.repository / ".worktrees").exists())

    def test_claim_id_cannot_create_a_recursive_worktree_path(self) -> None:
        self.claim(*self.acquire_arguments("first"), "--file", "README.md")

        completed = self.claim(
            *self.acquire_arguments("../recursive"),
            "--file",
            "src/one.py",
            "--branch",
            "codex/recursive",
        )

        self.assertEqual(1, completed.returncode)
        result = self.output(completed)
        self.assertEqual("INVALID_IDENTIFIER", result["outcome"])
        self.assertEqual("claim_id", result["field"])
        self.assertFalse((self.repository / "recursive").exists())

    def test_exact_backlog_scope_coexists_with_nonoverlapping_primary_project_claim(self) -> None:
        self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        isolated, isolated_path = self.isolated_arguments("backlog")

        completed = self.claim(
            *self.acquire_arguments("backlog"),
            "--file",
            "backlog/feature-backlog/queued.md",
            *isolated,
        )

        self.assertEqual(0, completed.returncode, completed.stderr)
        result = self.output(completed)
        self.assertEqual("SHARED_CHECKOUT_ACQUIRED", result["outcome"])
        self.assertEqual("primary", result["claim"]["checkout_topology"])
        self.assertFalse(isolated_path.exists())

    def test_backlog_scope_uses_available_primary_while_isolated_claim_remains(self) -> None:
        self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        isolated, _isolated_path = self.isolated_arguments("second")
        self.claim(
            *self.acquire_arguments("second"),
            "--file",
            "src/one.py",
            *isolated,
        )
        released = self.claim("release", "--claim-id", "first")

        completed = self.claim(
            *self.acquire_arguments("backlog"),
            "--file",
            "backlog/feature-backlog/queued.md",
            *self.timed_resource_arguments(
                resource="git-index:primary",
                resource_class="main-integration",
            ),
        )

        self.assertEqual(0, released.returncode, released.stderr)
        self.assertEqual(0, completed.returncode, completed.stderr)
        result = self.output(completed)
        self.assertEqual("SHARED_CHECKOUT_ACQUIRED", result["outcome"])
        self.assertEqual(str(self.repository.resolve()), result["target"]["worktree"])

    def test_primary_integration_scope_uses_available_primary_while_isolated_claim_remains(self) -> None:
        self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        isolated, _isolated_path = self.isolated_arguments("isolated")
        self.claim(
            *self.acquire_arguments("isolated"),
            "--file",
            "src/one.py",
            *isolated,
        )
        self.claim("release", "--claim-id", "first")

        completed = self.claim(
            *self.acquire_arguments("integration"),
            "--file",
            "skills/coordinate-work-items/SKILL.md",
            "--file",
            "design/generated/skill-definitions.js",
            *self.timed_resource_arguments(
                resource="merge:integration:main",
                resource_class="main-integration",
            ),
        )

        self.assertEqual(0, completed.returncode, completed.stderr)
        result = self.output(completed)
        self.assertEqual("SHARED_CHECKOUT_ACQUIRED", result["outcome"])
        self.assertEqual(str(self.repository.resolve()), result["target"]["worktree"])

    def test_resource_only_claim_does_not_force_unrelated_file_claim_into_isolation(self) -> None:
        resource = self.claim(
            *self.acquire_arguments("resource"),
            *self.timed_resource_arguments(),
        )

        completed = self.claim(
            *self.acquire_arguments("file"),
            "--file",
            "src/one.py",
        )

        self.assertEqual(0, resource.returncode, resource.stderr)
        self.assertEqual(0, completed.returncode, completed.stderr)
        result = self.output(completed)
        self.assertEqual("SHARED_CHECKOUT_ACQUIRED", result["outcome"])
        self.assertEqual(str(self.repository.resolve()), result["target"]["worktree"])

    def test_primary_resource_only_claim_can_extend_into_a_nonoverlapping_file_scope(self) -> None:
        self.claim(*self.acquire_arguments("file"), "--file", "README.md")
        resource = self.claim(
            *self.acquire_arguments("resource"),
            *self.timed_resource_arguments(),
        )

        extended = self.claim(
            "extend",
            "--claim-id",
            "resource",
            "--file",
            "src/one.py",
        )

        self.assertEqual(0, resource.returncode, resource.stderr)
        self.assertEqual(0, extended.returncode, extended.stderr)
        result = self.output(extended)
        self.assertEqual("EXTENDED", result["outcome"])
        status = self.output(self.claim("status"))["claims"]
        stored = next(claim for claim in status if claim["claim_id"] == "resource")
        self.assertEqual("project_files", stored["file_domain"])
        self.assertEqual(["src/one.py"], stored["files"])

    def test_resource_only_claim_does_not_block_unrelated_primary_integration(self) -> None:
        resource = self.claim(
            *self.acquire_arguments("resource"),
            *self.timed_resource_arguments(),
        )

        completed = self.claim(
            *self.acquire_arguments("integration"),
            "--file",
            "skills/coordinate-work-items/SKILL.md",
            "--file",
            "design/generated/skill-definitions.js",
            *self.timed_resource_arguments(
                resource="merge:integration:main",
                resource_class="main-integration",
            ),
        )

        self.assertEqual(0, resource.returncode, resource.stderr)
        self.assertEqual(0, completed.returncode, completed.stderr)
        result = self.output(completed)
        self.assertEqual("SHARED_CHECKOUT_ACQUIRED", result["outcome"])
        self.assertEqual(str(self.repository.resolve()), result["target"]["worktree"])

    def test_resource_only_claim_ignores_unrelated_dirty_files(self) -> None:
        source_path = self.repository / "src" / "one.py"
        source_path.write_text("private worktree edit\n", encoding="utf-8")

        acquired = self.claim(
            *self.acquire_arguments("resource"),
            *self.timed_resource_arguments(),
        )
        source_path.write_text("continued private worktree edit\n", encoding="utf-8")
        released = self.claim("release", "--claim-id", "resource")

        self.assertEqual(0, acquired.returncode, acquired.stderr)
        self.assertEqual(0, released.returncode, released.stderr)
        self.assertEqual("RELEASED", self.output(released)["outcome"])
        self.assertEqual(
            "continued private worktree edit\n",
            source_path.read_text(encoding="utf-8"),
        )

    def test_private_resource_only_claim_does_not_serialize_file_or_integration_claims(self) -> None:
        self.claim(*self.acquire_arguments("primary-file"), "--file", "README.md")
        isolated_arguments, isolated_path = self.isolated_arguments("isolated-file")
        isolated = self.claim(
            *self.acquire_arguments("isolated-file"),
            "--file",
            "src/one.py",
            *isolated_arguments,
        )
        self.assertEqual(0, isolated.returncode, isolated.stderr)
        self.claim("release", "--claim-id", "isolated-file")

        resource = self.claim(
            *self.acquire_arguments("private-resource"),
            *self.timed_resource_arguments(resource="test:e2e"),
            repo=isolated_path,
        )
        self.assertEqual(0, resource.returncode, resource.stderr)
        self.assertEqual(
            isolated_path.resolve(),
            Path(self.output(resource)["target"]["worktree"]).resolve(),
        )
        self.claim("release", "--claim-id", "primary-file")

        integration = self.claim(
            *self.acquire_arguments("five-file-integration"),
            "--file",
            "README.md",
            "--file",
            "src/one.py",
            "--file",
            "docs/guide.md",
            "--file",
            "docs/future.md",
            "--file",
            "src/future.py",
            *self.timed_resource_arguments(
                resource="merge:integration:main",
                resource_class="main-integration",
            ),
        )

        self.assertEqual(0, integration.returncode, integration.stderr)
        result = self.output(integration)
        self.assertEqual("SHARED_CHECKOUT_ACQUIRED", result["outcome"])
        self.assertEqual(str(self.repository.resolve()), result["target"]["worktree"])
        self.assertFalse((self.repository / ".worktrees" / "five-file-integration").exists())

    def test_primary_git_index_resource_uses_available_primary_while_isolated_claim_remains(self) -> None:
        self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        isolated, _isolated_path = self.isolated_arguments("isolated")
        self.claim(
            *self.acquire_arguments("isolated"),
            "--file",
            "src/one.py",
            *isolated,
        )
        self.claim("release", "--claim-id", "first")

        completed = self.claim(
            *self.acquire_arguments("git-index"),
            *self.timed_resource_arguments(
                resource="git-index:primary",
                resource_class="main-integration",
            ),
        )

        self.assertEqual(0, completed.returncode, completed.stderr)
        result = self.output(completed)
        self.assertEqual("SHARED_CHECKOUT_ACQUIRED", result["outcome"])
        self.assertEqual(str(self.repository.resolve()), result["target"]["worktree"])

    def test_primary_integration_scope_waits_for_overlapping_isolated_claim(self) -> None:
        self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        isolated, _isolated_path = self.isolated_arguments("isolated")
        self.claim(
            *self.acquire_arguments("isolated"),
            "--file",
            "skills/coordinate-work-items/SKILL.md",
            *isolated,
        )
        self.claim("release", "--claim-id", "first")

        completed = self.claim(
            *self.acquire_arguments("integration"),
            "--file",
            "skills/coordinate-work-items/SKILL.md",
            "--file",
            "design/generated/skill-definitions.js",
            *self.timed_resource_arguments(
                resource="merge:integration:main",
                resource_class="main-integration",
            ),
        )

        self.assertEqual(3, completed.returncode)
        result = self.output(completed)
        self.assertEqual("CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED", result["outcome"])
        self.assertEqual("WAIT", result["legacy_outcome"])
        self.assertEqual(["isolated"], result["conflicting_claim_ids"])

    def test_primary_integration_scope_coexists_with_nonoverlapping_primary_owner(self) -> None:
        self.claim(*self.acquire_arguments("first"), "--file", "README.md")

        completed = self.claim(
            *self.acquire_arguments("integration"),
            "--file",
            "design/generated/skill-definitions.js",
            *self.timed_resource_arguments(
                resource="merge:integration:main",
                resource_class="main-integration",
            ),
        )

        self.assertEqual(0, completed.returncode, completed.stderr)
        result = self.output(completed)
        self.assertEqual("SHARED_CHECKOUT_ACQUIRED", result["outcome"])
        self.assertEqual("primary", result["claim"]["checkout_topology"])

    def test_primary_integration_scope_ignores_worktree_status(self) -> None:
        self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        isolated, _isolated_path = self.isolated_arguments("isolated")
        self.claim(
            *self.acquire_arguments("isolated"),
            "--file",
            "src/one.py",
            *isolated,
        )
        self.claim("release", "--claim-id", "first")
        (self.repository / "docs" / "guide.md").write_text("dirty\n", encoding="utf-8")

        completed = self.claim(
            *self.acquire_arguments("integration"),
            "--file",
            "design/generated/skill-definitions.js",
            *self.timed_resource_arguments(
                resource="merge:integration:main",
                resource_class="main-integration",
            ),
        )

        self.assertEqual(0, completed.returncode, completed.stderr)
        result = self.output(completed)
        self.assertEqual("SHARED_CHECKOUT_ACQUIRED", result["outcome"])
        self.assertEqual("PRIMARY", result["legacy_outcome"])
        self.assertNotIn("dirty_status", result)

    def test_simultaneous_nonoverlapping_claims_can_both_use_primary(self) -> None:
        files_by_claim = {
            "first": "src/one.py",
            "second": "docs/guide.md",
        }
        commands = [
            self.claim_command(
                *self.acquire_arguments(claim_id),
                "--file",
                file_path,
            )
            for claim_id, file_path in files_by_claim.items()
        ]
        processes = [
            subprocess.Popen(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            for command in commands
        ]
        completed = [process.communicate() + (process.returncode,) for process in processes]
        outcomes = {json.loads(stdout)["outcome"] for stdout, _stderr, _code in completed}
        return_codes = sorted(code for _stdout, _stderr, code in completed)

        self.assertEqual([0, 0], return_codes)
        self.assertEqual({"SHARED_CHECKOUT_ACQUIRED"}, outcomes)

    def test_case_variant_exact_file_alias_conflicts_on_case_insensitive_filesystem(self) -> None:
        case_variant = self.repository / "readme.md"
        if not case_variant.exists():
            self.skipTest("requires a case-insensitive filesystem")

        first = self.claim(
            *self.acquire_arguments("canonical"),
            "--file",
            "README.md",
        )
        alias = self.claim(
            *self.acquire_arguments("alias"),
            "--file",
            "readme.md",
        )

        self.assertEqual(0, first.returncode, first.stderr)
        self.assertEqual(3, alias.returncode)
        result = self.output(alias)
        self.assertEqual("CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED", result["outcome"])
        self.assertEqual("readme.md", result["overlaps"][0]["requested"])
        self.assertEqual("readme.md", result["overlaps"][0]["claimed"])
        self.assertEqual(
            ["canonical"],
            [claim["claim_id"] for claim in self.output(self.claim("status"))["claims"]],
        )
        self.assertEqual(
            ["readme.md"],
            self.output(self.claim("status"))["claims"][0]["files"],
        )

    def test_future_case_variant_exact_file_alias_conflicts_on_case_insensitive_filesystem(self) -> None:
        case_variant = self.repository / "SRC"
        if not case_variant.exists():
            self.skipTest("requires a case-insensitive filesystem")

        first = self.claim(
            *self.acquire_arguments("canonical"),
            "--file",
            "src/FutureClaim.py",
        )
        alias = self.claim(
            *self.acquire_arguments("alias"),
            "--file",
            "SRC/futureclaim.py",
        )

        self.assertFalse((self.repository / "src" / "FutureClaim.py").exists())
        self.assertEqual(0, first.returncode, first.stderr)
        self.assertEqual(3, alias.returncode)
        self.assertEqual(
            "CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED",
            self.output(alias)["outcome"],
        )
        self.assertEqual(
            ["canonical"],
            [claim["claim_id"] for claim in self.output(self.claim("status"))["claims"]],
        )

    def test_legacy_case_variant_file_blocks_new_acquire_without_registry_mutation(self) -> None:
        if not (self.repository / "readme.md").exists():
            self.skipTest("requires a case-insensitive filesystem")

        owner = self.claim(
            *self.acquire_arguments("owner"),
            "--file",
            "README.md",
        )
        self.assertEqual(0, owner.returncode, owner.stderr)
        self.rewrite_claim_paths_as_legacy("owner", files=["README.md"])
        registry_before = self.registry_path().read_bytes()

        competitor = self.claim(
            *self.acquire_arguments("competitor"),
            "--file",
            "readme.md",
        )

        self.assertEqual(3, competitor.returncode)
        self.assertEqual(
            "CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED",
            self.output(competitor)["outcome"],
        )
        self.assertEqual(registry_before, self.registry_path().read_bytes())
        claims = self.output(self.claim("status"))["claims"]
        self.assertEqual(["owner"], [claim["claim_id"] for claim in claims])
        self.assertEqual(["README.md"], claims[0]["files"])

    def test_legacy_case_variant_file_blocks_new_extend_without_registry_mutation(self) -> None:
        if not (self.repository / "readme.md").exists():
            self.skipTest("requires a case-insensitive filesystem")

        owner = self.claim(
            *self.acquire_arguments("owner"),
            "--file",
            "README.md",
        )
        extender = self.claim(
            *self.acquire_arguments("extender"),
            "--file",
            "src/one.py",
        )
        self.assertEqual(0, owner.returncode, owner.stderr)
        self.assertEqual(0, extender.returncode, extender.stderr)
        self.rewrite_claim_paths_as_legacy("owner", files=["README.md"])
        registry_before = self.registry_path().read_bytes()

        extended = self.claim(
            "extend",
            "--claim-id",
            "extender",
            "--file",
            "readme.md",
        )

        self.assertEqual(3, extended.returncode)
        self.assertEqual(
            "CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED",
            self.output(extended)["outcome"],
        )
        self.assertEqual(registry_before, self.registry_path().read_bytes())
        claims = {
            claim["claim_id"]: claim["files"]
            for claim in self.output(self.claim("status"))["claims"]
        }
        self.assertEqual(
            {"owner": ["README.md"], "extender": ["src/one.py"]},
            claims,
        )

    def test_legacy_owner_extend_preserves_stored_case_variant(self) -> None:
        if not (self.repository / "readme.md").exists():
            self.skipTest("requires a case-insensitive filesystem")

        owner = self.claim(
            *self.acquire_arguments("owner"),
            "--file",
            "README.md",
        )
        self.assertEqual(0, owner.returncode, owner.stderr)
        self.rewrite_claim_paths_as_legacy("owner", files=["README.md"])
        registry_before = self.registry_path().read_bytes()

        extended = self.claim(
            "extend",
            "--claim-id",
            "owner",
            "--file",
            "readme.md",
        )

        self.assertEqual(0, extended.returncode, extended.stderr)
        result = self.output(extended)
        self.assertEqual([], result["added_scope"]["files"])
        self.assertEqual(["readme.md"], result["already_owned_scope"]["files"])
        self.assertEqual(["README.md"], result["claim"]["files"])
        self.assertEqual(registry_before, self.registry_path().read_bytes())

    def test_legacy_case_variant_tree_blocks_descendant_without_registry_mutation(self) -> None:
        if not (self.repository / "SRC").exists():
            self.skipTest("requires a case-insensitive filesystem")

        owner = self.claim(
            *self.acquire_arguments("owner"),
            "--tree",
            "src",
            "--scope-reason",
            "source ownership",
        )
        self.assertEqual(0, owner.returncode, owner.stderr)
        self.rewrite_claim_paths_as_legacy("owner", trees=["SRC"])
        registry_before = self.registry_path().read_bytes()

        competitor = self.claim(
            *self.acquire_arguments("competitor"),
            "--file",
            "src/one.py",
        )

        self.assertEqual(3, competitor.returncode)
        self.assertEqual(
            "CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED",
            self.output(competitor)["outcome"],
        )
        self.assertEqual(registry_before, self.registry_path().read_bytes())
        claims = self.output(self.claim("status"))["claims"]
        self.assertEqual(["owner"], [claim["claim_id"] for claim in claims])
        self.assertEqual(["SRC"], claims[0]["trees"])

    def test_unsafe_legacy_path_fails_closed_without_registry_mutation(self) -> None:
        owner = self.claim(
            *self.acquire_arguments("owner"),
            "--file",
            "README.md",
        )
        self.assertEqual(0, owner.returncode, owner.stderr)
        self.rewrite_claim_paths_as_legacy("owner", files=["../outside.py"])
        registry_before = self.registry_path().read_bytes()

        competitor = self.claim(
            *self.acquire_arguments("competitor"),
            "--file",
            "docs/guide.md",
        )

        self.assertEqual(3, competitor.returncode)
        self.assertEqual(
            "CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED",
            self.output(competitor)["outcome"],
        )
        self.assertEqual(registry_before, self.registry_path().read_bytes())
        self.assertEqual(
            ["owner"],
            [
                claim["claim_id"]
                for claim in self.output(self.claim("status"))["claims"]
            ],
        )

    @unittest.skipUnless(SYMLINKS_AVAILABLE, "Symbolic-link creation is unavailable.")
    def test_dangling_symlink_and_missing_target_remain_distinct_stable_paths(self) -> None:
        alias_path = self.repository / "src" / "future-alias.py"
        target_path = self.repository / "src" / "future-target.py"
        alias_path.symlink_to(target_path.name)
        self.git("add", "src/future-alias.py")
        self.git("commit", "-m", "add dangling symlink fixture")

        acquired = self.claim(
            *self.acquire_arguments("dangling"),
            "--file",
            "src/future-alias.py",
            "--file",
            "src/future-target.py",
        )

        self.assertFalse(target_path.exists())
        self.assertEqual(0, acquired.returncode, acquired.stderr)
        self.assertEqual(
            ["src/future-alias.py", "src/future-target.py"],
            self.output(acquired)["claim"]["files"],
        )

    @unittest.skipUnless(SYMLINKS_AVAILABLE, "Symbolic-link creation is unavailable.")
    def test_absolute_symlink_scope_preserves_lexical_path_without_following_target(self) -> None:
        alias_path = self.repository / "src" / "guide-alias.md"
        alias_path.symlink_to("../docs/guide.md")
        self.git("add", "src/guide-alias.md")
        self.git("commit", "-m", "add symlink fixture")

        alias = self.claim(
            *self.acquire_arguments("alias"),
            "--file",
            str(self.repository.resolve() / "src" / "guide-alias.md"),
        )
        target = self.claim(
            *self.acquire_arguments("target"),
            "--file",
            "docs/guide.md",
        )

        self.assertEqual(0, alias.returncode, alias.stderr)
        self.assertEqual(
            ["src/guide-alias.md"],
            self.output(alias)["claim"]["files"],
        )
        self.assertEqual(0, target.returncode, target.stderr)

    @unittest.skipUnless(SYMLINKS_AVAILABLE, "Symbolic-link creation is unavailable.")
    def test_exact_file_symlink_does_not_inherit_target_directory_kind(self) -> None:
        alias_path = self.repository / "src" / "docs-alias"
        alias_path.symlink_to("../docs")
        self.git("add", "src/docs-alias")
        self.git("commit", "-m", "add directory symlink fixture")

        acquired = self.claim(
            *self.acquire_arguments("alias"),
            "--file",
            "src/docs-alias",
        )

        self.assertEqual(0, acquired.returncode, acquired.stderr)
        self.assertEqual(
            ["src/docs-alias"],
            self.output(acquired)["claim"]["files"],
        )

    def test_distinct_hard_link_paths_can_be_claimed_concurrently(self) -> None:
        alias_path = self.repository / "README-alias.md"
        try:
            os.link(self.repository / "README.md", alias_path)
        except OSError as error:
            self.skipTest(f"hard links unavailable: {error}")
        self.git("add", "README-alias.md")
        self.git("commit", "-m", "add hard-link alias fixture")

        first = self.claim(
            *self.acquire_arguments("canonical"),
            "--file",
            "README.md",
        )
        alias = self.claim(
            *self.acquire_arguments("alias"),
            "--file",
            "README-alias.md",
        )

        self.assertEqual(0, first.returncode, first.stderr)
        self.assertEqual(0, alias.returncode, alias.stderr)

    def test_exact_files_do_not_use_ancestry_overlap(self) -> None:
        first = self.claim(*self.acquire_arguments("first"), "--file", "future")
        isolated, _isolated_path = self.isolated_arguments("second")
        second = self.claim(
            *self.acquire_arguments("second"),
            "--file",
            "future/child.py",
            *isolated,
        )

        self.assertEqual(0, first.returncode, first.stderr)
        self.assertEqual(0, second.returncode, second.stderr)
        self.assertEqual("ISOLATED_CHECKOUT_ACQUIRED", self.output(second)["outcome"])

    def test_tree_and_all_files_scopes_overlap_descendants(self) -> None:
        tree = self.claim(
            *self.acquire_arguments("tree"),
            "--tree",
            "src",
            "--scope-reason",
            "bounded source generation",
        )
        isolated, blocked_path = self.isolated_arguments("blocked")
        nested = self.claim(
            *self.acquire_arguments("blocked"),
            "--file",
            "src/one.py",
            *isolated,
        )

        self.assertEqual(0, tree.returncode, tree.stderr)
        self.assertEqual(3, nested.returncode)
        nested_result = self.output(nested)
        self.assertEqual("CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED", nested_result["outcome"])
        self.assertEqual("tree", nested_result["overlaps"][0]["claimed_kind"])
        self.assertFalse(blocked_path.exists())

        self.claim("release", "--claim-id", "tree")
        all_files = self.claim(
            *self.acquire_arguments("all"),
            "--all-files",
            "--scope-reason",
            "repository migration",
        )
        resource = self.claim(
            *self.acquire_arguments("other"),
            *self.timed_resource_arguments(),
        )
        exact = self.claim(*self.acquire_arguments("exact"), "--file", "docs/guide.md")
        self.assertEqual(0, all_files.returncode, all_files.stderr)
        self.assertEqual(0, resource.returncode, resource.stderr)
        self.assertEqual("SHARED_CHECKOUT_ACQUIRED", self.output(resource)["outcome"])
        self.assertEqual(3, exact.returncode)

    def test_project_files_and_backlog_are_separate_broad_domains(self) -> None:
        project = self.claim(
            *self.acquire_arguments("project"),
            "--project-files",
            "--scope-reason",
            "project delivery",
        )
        isolated, isolated_path = self.isolated_arguments("other-project")
        other_project = self.claim(
            *self.acquire_arguments("other-project"),
            "--file",
            "src/one.py",
            *isolated,
        )
        backlog = self.claim(
            *self.acquire_arguments("backlog"),
            "--file",
            "backlog/feature-backlog/queued.md",
        )

        self.assertEqual(0, project.returncode, project.stderr)
        self.assertEqual("project_files", self.output(project)["claim"]["file_domain"])
        self.assertEqual(3, other_project.returncode)
        self.assertFalse(isolated_path.exists())
        self.assertEqual(0, backlog.returncode, backlog.stderr)
        self.assertEqual("SHARED_CHECKOUT_ACQUIRED", self.output(backlog)["outcome"])
        self.assertEqual(
            ["project", "backlog"],
            [item["claim_id"] for item in self.output(self.claim("status"))["claims"]],
        )

    def test_different_exact_backlog_items_coexist(self) -> None:
        first = self.claim(
            *self.acquire_arguments("first-backlog"),
            "--file",
            "backlog/feature-backlog/queued.md",
        )
        second = self.claim(
            *self.acquire_arguments("second-backlog"),
            "--file",
            "backlog/feature-backlog/second.md",
        )

        self.assertEqual(0, first.returncode, first.stderr)
        self.assertEqual(0, second.returncode, second.stderr)
        self.assertEqual("SHARED_CHECKOUT_ACQUIRED", self.output(second)["outcome"])
        self.assertEqual(
            ["first-backlog", "second-backlog"],
            [item["claim_id"] for item in self.output(self.claim("status"))["claims"]],
        )

    def test_backlog_broad_scope_does_not_overlap_project_paths(self) -> None:
        backlog = self.claim(
            *self.acquire_arguments("backlog"),
            "--backlog",
            "--scope-reason",
            "backlog maintenance",
        )
        self.assertEqual(0, backlog.returncode, backlog.stderr)
        self.assertEqual("backlog", self.output(backlog)["claim"]["file_domain"])
        self.claim("release", "--claim-id", "backlog")

        project = self.claim(*self.acquire_arguments("project"), "--file", "src/one.py")
        self.assertEqual(0, project.returncode, project.stderr)

    def test_mixed_project_and_backlog_paths_are_rejected_atomically(self) -> None:
        completed = self.claim(
            *self.acquire_arguments("mixed"),
            "--file",
            "src/one.py",
            "--file",
            "backlog/feature-backlog/queued.md",
        )

        self.assertEqual(1, completed.returncode)
        result = self.output(completed)
        self.assertEqual("INVALID_SCOPE", result["outcome"])
        self.assertEqual("mixed_file_domains", result["rejection"]["reason"])
        self.assertEqual([], self.output(self.claim("status"))["claims"])

    def test_broad_file_domains_are_mutually_exclusive(self) -> None:
        for index, arguments in enumerate(
            (
                ("--project-files", "--backlog"),
                ("--project-files", "--all-files"),
                ("--backlog", "--all-files"),
            )
        ):
            with self.subTest(arguments=arguments):
                completed = self.claim(
                    *self.acquire_arguments(f"mixed-{index}"),
                    *arguments,
                    "--scope-reason",
                    "invalid broad combination",
                )
                self.assertEqual(1, completed.returncode)
                self.assertEqual("INVALID_SCOPE", self.output(completed)["outcome"])

    def test_compatibility_backlog_file_uses_backlog_domain_and_primary_rules(self) -> None:
        self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        completed = self.claim(
            *self.acquire_arguments("backlog"),
            "--file",
            "backlog/feature-backlog/queued.md",
        )

        self.assertEqual(0, completed.returncode, completed.stderr)
        result = self.output(completed)
        self.assertEqual("SHARED_CHECKOUT_ACQUIRED", result["outcome"])
        self.assertEqual("backlog", result["claim"]["file_domain"])
        self.assertEqual("compat_backlog_path", result["warnings"][0]["code"])

    def test_project_claim_ignores_unchanged_preexisting_backlog_dirtiness(self) -> None:
        backlog_path = self.repository / "backlog" / "feature-backlog" / "queued.md"
        backlog_path.write_text("preexisting\n", encoding="utf-8")

        acquired = self.claim(*self.acquire_arguments("project"), "--project-files", "--scope-reason", "project work")
        released = self.claim("release", "--claim-id", "project")

        self.assertEqual(0, acquired.returncode, acquired.stderr)
        self.assertEqual("SHARED_CHECKOUT_ACQUIRED", self.output(acquired)["outcome"])
        self.assertEqual(0, released.returncode, released.stderr)

    def test_nul_status_preserves_unchanged_backlog_rename_records(self) -> None:
        renamed_path = "backlog/feature-backlog/renamed café item.md"
        self.git("mv", "backlog/feature-backlog/queued.md", renamed_path)
        acquired = self.claim(
            *self.acquire_arguments("project"),
            "--project-files",
            "--scope-reason",
            "project work",
        )

        released = self.claim("release", "--claim-id", "project")

        self.assertEqual(0, acquired.returncode, acquired.stderr)
        self.assertEqual(0, released.returncode, released.stderr)

    def test_project_claim_release_does_not_audit_committed_backlog_history(self) -> None:
        acquired = self.claim(*self.acquire_arguments("project"), "--project-files", "--scope-reason", "project work")
        self.assertEqual(0, acquired.returncode, acquired.stderr)
        backlog_path = self.repository / "backlog" / "feature-backlog" / "queued.md"
        backlog_path.write_text("committed\n", encoding="utf-8")
        self.git("add", str(backlog_path))
        self.git("commit", "-m", "review-owned scope decision")

        released = self.claim("release", "--claim-id", "project")

        self.assertEqual(0, released.returncode, released.stderr)
        self.assertEqual("RELEASED", self.output(released)["outcome"])

    def test_project_claim_release_ignores_merge_parent_history(self) -> None:
        source_branch = "project-source"
        target_branch = self.git("branch", "--show-current").stdout.strip()
        self.git("branch", source_branch)
        backlog_path = self.repository / "backlog" / "feature-backlog" / "queued.md"
        backlog_path.write_text("completed before claim\n", encoding="utf-8")
        self.git("add", str(backlog_path))
        self.git("commit", "-m", "complete backlog work before claim")
        acquired = self.claim(*self.acquire_arguments("project"), "--project-files", "--scope-reason", "project work")
        self.assertEqual(0, acquired.returncode, acquired.stderr)

        self.git("checkout", source_branch)
        source_path = self.repository / "src" / "one.py"
        source_path.write_text("project change\n", encoding="utf-8")
        self.git("add", str(source_path))
        self.git("commit", "-m", "project source change")
        self.git("checkout", target_branch)
        self.git("merge", "--no-ff", source_branch, "-m", "integrate project source")

        released = self.claim("release", "--claim-id", "project")

        self.assertEqual(0, released.returncode, released.stderr)
        self.assertEqual("RELEASED", self.output(released)["outcome"])

    def test_status_and_extend_preserve_active_legacy_mixed_claim(self) -> None:
        legacy_claim = {
            "agent": "legacy",
            "all_files": False,
            "baseline_commit": self.git("rev-parse", "HEAD").stdout.strip(),
            "baseline_status": [],
            "branch": "main",
            "claim_id": "legacy-mixed",
            "claimed_at": "2026-07-12T10:00:00Z",
            "files": ["src/one.py", "backlog/feature-backlog/queued.md"],
            "heartbeat": "2026-07-12T10:00:00Z",
            "mode": "primary",
            "parent_claim_id": None,
            "resources": [],
            "root_task_id": "legacy-root",
            "scope_reasons": {},
            "task": "legacy mixed claim",
            "trees": [],
            "worktree": str(self.repository),
        }
        self.write_registry_fixture({"claims": [legacy_claim]})

        status = self.output(self.claim("status"))["claims"][0]
        extended = self.claim("extend", "--claim-id", "legacy-mixed", "--file", "docs/guide.md")
        stored = json.loads(self.registry_path().read_text(encoding="utf-8"))["claims"][0]

        self.assertEqual("legacy_mixed", status["file_domain"])
        self.assertTrue(status["compatibility"]["legacy_registry_claim"])
        self.assertEqual(1, extended.returncode)
        self.assertEqual("legacy_mixed_file_domains", self.output(extended)["rejection"]["reason"])
        self.assertNotIn("file_domain", stored)
        self.assertEqual(legacy_claim["files"], stored["files"])

    def test_legacy_claim_release_does_not_require_out_of_domain_baseline(self) -> None:
        acquired = self.claim(*self.acquire_arguments("project"), "--file", "src/one.py")
        self.assertEqual(0, acquired.returncode, acquired.stderr)
        registry = json.loads(self.registry_path().read_text(encoding="utf-8"))
        claim = registry["claims"][0]
        claim["baseline_out_of_domain_state"] = {"obsolete": "ignored"}
        claim["baseline_out_of_domain_status"] = [{"path": "obsolete"}]
        self.registry_path().write_text(json.dumps(registry), encoding="utf-8")
        (self.repository / "backlog" / "feature-backlog" / "queued.md").write_text(
            "changed\n",
            encoding="utf-8",
        )

        released = self.claim("release", "--claim-id", "project")

        self.assertEqual(0, released.returncode, released.stderr)
        self.assertEqual("RELEASED", self.output(released)["outcome"])

    def test_legacy_resource_only_claim_reports_none_and_accepts_project_domain(self) -> None:
        legacy_claim = {
            "agent": "legacy",
            "all_files": False,
            "baseline_commit": self.git("rev-parse", "HEAD").stdout.strip(),
            "baseline_status": [],
            "branch": "main",
            "claim_id": "legacy-resource",
            "claimed_at": "2026-07-12T10:00:00Z",
            "files": [],
            "heartbeat": "2026-07-12T10:00:00Z",
            "mode": "primary",
            "parent_claim_id": None,
            "resources": ["port:3000"],
            "root_task_id": "legacy-root",
            "scope_reasons": {},
            "task": "legacy resource claim",
            "trees": [],
            "worktree": str(self.repository),
        }
        self.write_registry_fixture({"claims": [legacy_claim]})

        status = self.output(self.claim("status"))["claims"][0]
        extended = self.claim(
            "extend",
            "--claim-id",
            "legacy-resource",
            "--file",
            "src/one.py",
        )

        self.assertEqual("none", status["file_domain"])
        self.assertTrue(status["compatibility"]["legacy_registry_claim"])
        self.assertEqual(0, extended.returncode, extended.stderr)
        claim = self.output(extended)["claim"]
        self.assertEqual("project_files", claim["file_domain"])
        self.assertEqual(["src/one.py"], claim["files"])
        self.assertEqual(["port:3000"], claim["resources"])

    def test_legacy_resource_only_claim_rejects_backlog_domain_without_mutation(self) -> None:
        legacy_claim = {
            "agent": "legacy",
            "all_files": False,
            "baseline_commit": self.git("rev-parse", "HEAD").stdout.strip(),
            "baseline_status": [],
            "branch": "main",
            "claim_id": "legacy-resource",
            "claimed_at": "2026-07-12T10:00:00Z",
            "files": [],
            "heartbeat": "2026-07-12T10:00:00Z",
            "mode": "primary",
            "parent_claim_id": None,
            "resources": ["database:seed"],
            "root_task_id": "legacy-root",
            "scope_reasons": {},
            "task": "legacy resource claim",
            "trees": [],
            "worktree": str(self.repository),
        }
        self.write_registry_fixture({"claims": [legacy_claim]})

        registry_before = self.registry_path().read_bytes()
        extended = self.claim(
            "extend",
            "--claim-id",
            "legacy-resource",
            "--backlog",
            "--scope-reason",
            "backlog maintenance",
        )

        self.assertEqual(1, extended.returncode)
        result = self.output(extended)
        self.assertEqual("INVALID_SCOPE", result["outcome"])
        self.assertEqual("resource_only_backlog_extension", result["rejection"]["reason"])
        self.assertEqual(registry_before, self.registry_path().read_bytes())

    def test_linked_resource_only_claim_rejects_exact_backlog_extension_without_mutation(self) -> None:
        linked = self.existing_linked_worktree("resource-owner")
        acquired = self.claim(
            *self.acquire_arguments("resource"),
            *self.timed_resource_arguments(),
            repo=linked,
        )
        registry_before = self.registry_path().read_bytes()

        extended = self.claim(
            "extend",
            "--claim-id",
            "resource",
            "--file",
            "backlog/feature-backlog/queued.md",
            repo=linked,
        )

        self.assertEqual(0, acquired.returncode, acquired.stderr)
        self.assertEqual(1, extended.returncode)
        result = self.output(extended)
        self.assertEqual("INVALID_SCOPE", result["outcome"])
        self.assertEqual("resource_only_backlog_extension", result["rejection"]["reason"])
        self.assertEqual(registry_before, self.registry_path().read_bytes())
        stored = self.output(self.claim("status"))["claims"][0]
        self.assertEqual("none", stored["file_domain"])
        self.assertEqual([], stored["files"])
        self.assertFalse(stored["backlog"])
        self.assertEqual(["port:3000"], stored["resources"])

    def test_legacy_complete_worktree_release_allows_opposite_domain_commit_after_extension(self) -> None:
        legacy_claim = {
            "agent": "legacy",
            "all_files": False,
            "baseline_commit": self.git("rev-parse", "HEAD").stdout.strip(),
            "baseline_status": [],
            "branch": "main",
            "claim_id": "legacy-resource",
            "claimed_at": "2026-07-12T10:00:00Z",
            "files": [],
            "heartbeat": "2026-07-12T10:00:00Z",
            "mode": "primary",
            "parent_claim_id": None,
            "resources": ["port:3000"],
            "root_task_id": "legacy-root",
            "scope_reasons": {},
            "task": "legacy resource claim",
            "trees": [],
            "worktree": str(self.repository),
        }
        self.write_registry_fixture({"claims": [legacy_claim]})
        extended = self.claim("extend", "--claim-id", "legacy-resource", "--file", "src/one.py")
        self.assertEqual(0, extended.returncode, extended.stderr)
        backlog_path = self.repository / "backlog" / "feature-backlog" / "queued.md"
        backlog_path.write_text("legacy committed\n", encoding="utf-8")
        self.git("add", str(backlog_path))
        self.git("commit", "-m", "legacy complete worktree commit")

        released = self.claim("release", "--claim-id", "legacy-resource")

        self.assertEqual(0, released.returncode, released.stderr)
        self.assertEqual("RELEASED", self.output(released)["outcome"])

    def test_backlog_claim_release_does_not_inspect_project_change(self) -> None:
        acquired = self.claim(
            *self.acquire_arguments("backlog"),
            "--backlog",
            "--scope-reason",
            "backlog maintenance",
        )
        self.assertEqual(0, acquired.returncode, acquired.stderr)
        (self.repository / "src" / "one.py").write_text("changed\n", encoding="utf-8")

        released = self.claim("release", "--claim-id", "backlog")

        self.assertEqual(0, released.returncode, released.stderr)
        self.assertEqual("RELEASED", self.output(released)["outcome"])

    def test_backlog_claim_ignores_unchanged_preexisting_project_dirtiness(self) -> None:
        project_path = self.repository / "src" / "one.py"
        project_path.write_text("preexisting\n", encoding="utf-8")

        acquired = self.claim(
            *self.acquire_arguments("backlog"),
            "--backlog",
            "--scope-reason",
            "backlog maintenance",
        )
        released = self.claim("release", "--claim-id", "backlog")

        self.assertEqual(0, acquired.returncode, acquired.stderr)
        self.assertEqual("SHARED_CHECKOUT_ACQUIRED", self.output(acquired)["outcome"])
        self.assertEqual(0, released.returncode, released.stderr)

    def test_operational_worktree_paths_are_not_claimable_as_project_files(self) -> None:
        completed = self.claim(
            *self.acquire_arguments("operational"),
            "--file",
            ".worktrees/internal-state",
        )

        self.assertEqual(1, completed.returncode)
        result = self.output(completed)
        self.assertEqual("INVALID_SCOPE", result["outcome"])
        self.assertEqual("operational_path_not_claimable", result["rejection"]["reason"])

    def test_extend_cannot_cross_from_project_into_backlog_domain(self) -> None:
        acquired = self.claim(*self.acquire_arguments("project"), "--file", "src/one.py")
        extended = self.claim(
            "extend",
            "--claim-id",
            "project",
            "--file",
            "backlog/feature-backlog/queued.md",
        )

        self.assertEqual(0, acquired.returncode, acquired.stderr)
        self.assertEqual(1, extended.returncode)
        self.assertEqual("INVALID_SCOPE", self.output(extended)["outcome"])
        claim = self.output(self.claim("status"))["claims"][0]
        self.assertEqual("project_files", claim["file_domain"])
        self.assertEqual(["src/one.py"], claim["files"])

    def test_broad_scope_guardrails_and_future_file_behavior(self) -> None:
        invalid_commands = (
            (["--file", "."], "use --all-files"),
            (["--file", "**"], "use --tree"),
            (["--file", "src"], "use --tree"),
            (["--tree", "README.md", "--scope-reason", "wrong kind"], "use --file"),
            (["--tree", ".", "--scope-reason", "too broad"], "use --all-files"),
            (["--tree", "src"], "add --scope-reason"),
        )
        for index, (scope_arguments, replacement) in enumerate(invalid_commands):
            with self.subTest(scope_arguments=scope_arguments):
                completed = self.claim(*self.acquire_arguments(f"invalid-{index}"), *scope_arguments)
                self.assertEqual(1, completed.returncode)
                result = self.output(completed)
                self.assertEqual("INVALID_SCOPE", result["outcome"])
                self.assertIn(replacement, result["replacement"])

        future = self.claim(*self.acquire_arguments("future"), "--file", "not-created-yet.py")
        self.assertEqual(0, future.returncode, future.stderr)

    def test_acquire_requires_scope_without_mutating_registry(self) -> None:
        completed = self.claim(*self.acquire_arguments("scope-less"))

        self.assertEqual(1, completed.returncode)
        result = self.output(completed)
        self.assertEqual("INVALID_SCOPE", result["outcome"])
        self.assertEqual("missing_scope", result["rejection"]["reason"])
        self.assertEqual([], self.output(self.claim("status"))["claims"])

    def test_broad_backlog_scope_requires_and_retains_reason(self) -> None:
        rejected = self.claim(
            *self.acquire_arguments("missing-reason"),
            "--backlog",
        )

        self.assertEqual(1, rejected.returncode)
        rejected_result = self.output(rejected)
        self.assertEqual("INVALID_SCOPE", rejected_result["outcome"])
        self.assertEqual("scope_reason_required", rejected_result["rejection"]["reason"])
        self.assertEqual([], self.output(self.claim("status"))["claims"])

        acquired = self.claim(
            *self.acquire_arguments("reasoned"),
            "--backlog",
            "--scope-reason",
            "bounded backlog maintenance",
        )

        self.assertEqual(0, acquired.returncode, acquired.stderr)
        self.assertEqual(
            {"backlog:backlog": "bounded backlog maintenance"},
            self.output(acquired)["claim"]["scope_reasons"],
        )
        event = next(
            event
            for event in self.journal_events()
            if event["claim_id"] == "reasoned" and event["outcome"] == "PRIMARY"
        )
        self.assertEqual(
            "bounded backlog maintenance",
            event["requested_scopes"]["scope_reason"],
        )
        self.assertEqual(
            {"backlog:backlog": "bounded backlog maintenance"},
            event["scopes"]["scope_reasons"],
        )

    def test_compatibility_mode_converts_directory_file_scope_with_warning(self) -> None:
        completed = self.claim(
            *self.acquire_arguments("legacy"),
            "--file",
            "src",
            "--compat-file-directories",
            "--scope-reason",
            "temporary legacy caller",
        )

        self.assertEqual(0, completed.returncode, completed.stderr)
        result = self.output(completed)
        self.assertEqual(["src"], result["claim"]["trees"])
        self.assertEqual("legacy_file_directory_scope", result["warnings"][0]["code"])

    def test_extend_adds_multiple_scopes_and_is_idempotent(self) -> None:
        acquired = self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        extended = self.claim(
            "extend",
            "--claim-id",
            "first",
            "--file",
            "future.py",
            *self.timed_resource_arguments(
                resource="generated:codegen",
                resource_class="live-model-evaluation",
            ),
        )
        repeated = self.claim(
            "extend",
            "--claim-id",
            "first",
            "--file",
            "future.py",
            *self.timed_resource_arguments(
                resource="generated:codegen",
                resource_class="live-model-evaluation",
            ),
        )

        self.assertEqual(0, acquired.returncode, acquired.stderr)
        self.assertEqual(0, extended.returncode, extended.stderr)
        added = self.output(extended)["added_scope"]
        self.assertEqual(["future.py"], added["files"])
        self.assertEqual(["generated:codegen"], added["resources"])
        repeated_result = self.output(repeated)
        self.assertEqual("EXTENDED", repeated_result["outcome"])
        self.assertEqual([], repeated_result["added_scope"]["files"])
        self.assertEqual(["future.py"], repeated_result["already_owned_scope"]["files"])

    def test_conflicting_extension_leaves_registry_byte_for_byte_unchanged(self) -> None:
        self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        isolated, _isolated_path = self.isolated_arguments("second")
        self.claim(*self.acquire_arguments("second"), "--file", "src/one.py", *isolated)
        before = self.registry_path().read_bytes()

        blocked = self.claim("extend", "--claim-id", "second", "--file", "README.md")

        self.assertEqual(3, blocked.returncode)
        self.assertEqual("CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED", self.output(blocked)["outcome"])
        self.assertEqual(before, self.registry_path().read_bytes())

    def test_isolated_extension_reports_primary_resource_overlap_before_location(self) -> None:
        self.claim(
            *self.acquire_arguments("first"),
            *self.timed_resource_arguments(
                resource="merge:integration:main",
                resource_class="main-integration",
            ),
        )
        isolated, _isolated_path = self.isolated_arguments("second")
        self.claim(*self.acquire_arguments("second"), "--file", "src/one.py", *isolated)
        before = self.registry_path().read_bytes()

        blocked = self.claim(
            "extend",
            "--claim-id",
            "second",
            *self.timed_resource_arguments(
                resource="merge:integration:main",
                resource_class="main-integration",
            ),
        )

        self.assertEqual(3, blocked.returncode)
        result = self.output(blocked)
        self.assertEqual("CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED", result["outcome"])
        self.assertEqual(["first"], result["conflicting_claim_ids"])
        self.assertEqual(before, self.registry_path().read_bytes())

    def test_simultaneous_extensions_cannot_both_acquire_same_file(self) -> None:
        self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        isolated, _isolated_path = self.isolated_arguments("second")
        self.claim(*self.acquire_arguments("second"), "--file", "src/one.py", *isolated)
        commands = [
            self.claim_command("extend", "--claim-id", claim_id, "--file", "shared-new.py")
            for claim_id in ("first", "second")
        ]
        processes = [
            subprocess.Popen(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            for command in commands
        ]
        completed = [process.communicate() + (process.returncode,) for process in processes]

        self.assertEqual([0, 3], sorted(code for _stdout, _stderr, code in completed))
        self.assertEqual(
            {"CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED", "EXTENDED"},
            {json.loads(stdout)["outcome"] for stdout, _stderr, _code in completed},
        )

    def test_extending_isolated_claim_preserves_worktree_metadata(self) -> None:
        self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        isolated, _isolated_path = self.isolated_arguments("second")
        acquired = self.claim(*self.acquire_arguments("second"), "--file", "src/one.py", *isolated)
        before = self.output(acquired)["claim"]

        extended = self.claim("extend", "--claim-id", "second", "--file", "future.py")
        after = self.output(extended)["claim"]

        for field in (
            "worktree",
            "branch",
            "checkout_topology",
            "baseline_commit",
            "claimed_at",
            "mode",
        ):
            self.assertEqual(before[field], after[field])

    def test_isolated_claim_hands_backlog_extension_to_primary_despite_unrelated_claim(self) -> None:
        self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        isolated, isolated_path = self.isolated_arguments("second")
        self.claim(*self.acquire_arguments("second"), "--file", "src/one.py", *isolated)
        before = self.registry_path().read_bytes()

        completed = self.claim(
            "extend",
            "--claim-id",
            "second",
            "--file",
            "backlog/feature-backlog/queued.md",
            repo=isolated_path,
        )
        report = self.claim("report", "--since", "2d")

        self.assertEqual(3, completed.returncode)
        result = self.output(completed)
        self.assertEqual("SHARED_CHECKOUT_REQUIRED", result["outcome"])
        self.assertEqual("PRIMARY_REQUIRED", result["legacy_outcome"])
        self.assertEqual(before, self.registry_path().read_bytes())
        event = next(
            event
            for event in self.journal_events()
            if event["claim_id"] == "second" and event["outcome"] == "PRIMARY_REQUIRED"
        )
        self.assertIs(event["shared_checkout_claimed"], False)
        self.assertEqual(0, report.returncode, report.stderr)
        metrics = self.output(report)["metrics"]
        self.assertEqual(1, metrics["outcome_counts"]["SHARED_CHECKOUT_REQUIRED"])
        self.assertEqual(1, metrics["raw_outcome_counts"]["PRIMARY_REQUIRED"])
        self.assertEqual([], metrics["outcome_normalization_gaps"])

    def test_isolated_backlog_extension_reports_available_shared_checkout(self) -> None:
        self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        isolated, isolated_path = self.isolated_arguments("second")
        self.claim(*self.acquire_arguments("second"), "--file", "src/one.py", *isolated)
        self.claim("release", "--claim-id", "first")

        completed = self.claim(
            "extend",
            "--claim-id",
            "second",
            "--file",
            "backlog/feature-backlog/queued.md",
            repo=isolated_path,
        )

        self.assertEqual(3, completed.returncode)
        self.assertEqual("SHARED_CHECKOUT_REQUIRED", self.output(completed)["outcome"])
        event = next(
            event
            for event in self.journal_events()
            if event["claim_id"] == "second" and event["outcome"] == "PRIMARY_REQUIRED"
        )
        self.assertIs(event["shared_checkout_claimed"], False)

    def test_isolated_named_resource_extension_ignores_unrelated_primary_claim(self) -> None:
        self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        isolated, isolated_path = self.isolated_arguments("second")
        self.claim(*self.acquire_arguments("second"), "--file", "src/one.py", *isolated)

        completed = self.claim(
            "extend",
            "--claim-id",
            "second",
            *self.timed_resource_arguments(
                resource="git-index:primary",
                resource_class="main-integration",
            ),
            repo=isolated_path,
        )

        self.assertEqual(0, completed.returncode, completed.stderr)
        result = self.output(completed)
        self.assertEqual("EXTENDED", result["outcome"])
        event = next(
            event
            for event in reversed(self.journal_events())
            if event["claim_id"] == "second" and event["outcome"] == "EXTENDED"
        )
        self.assertEqual(["git-index:primary"], event["added_scope"]["resources"])

    def test_report_uses_explicit_context_when_shared_checkout_is_available(self) -> None:
        self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        isolated, isolated_path = self.isolated_arguments("isolated")
        self.claim(*self.acquire_arguments("isolated"), "--file", "src/one.py", *isolated)
        self.claim("release", "--claim-id", "first")

        required = self.claim(
            *self.acquire_arguments("backlog"),
            "--backlog",
            "--scope-reason",
            "backlog maintenance",
            repo=isolated_path,
        )
        report = self.claim("report", "--since", "2d")

        self.assertEqual(3, required.returncode)
        event = next(event for event in self.journal_events() if event["claim_id"] == "backlog")
        self.assertIs(event["shared_checkout_claimed"], False)
        self.assertEqual(0, report.returncode, report.stderr)
        metrics = self.output(report)["metrics"]
        self.assertEqual(1, metrics["outcome_counts"]["SHARED_CHECKOUT_REQUIRED"])
        self.assertEqual(1, metrics["raw_outcome_counts"]["PRIMARY_REQUIRED"])
        self.assertEqual([], metrics["outcome_normalization_gaps"])

    def test_linked_worktrees_share_one_journal(self) -> None:
        self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        isolated, isolated_path = self.isolated_arguments("second")
        self.claim(*self.acquire_arguments("second"), "--file", "src/one.py", *isolated)
        third_arguments, third_path = self.isolated_arguments("third")
        third = self.claim(
            *self.acquire_arguments("third"),
            "--file",
            "docs/guide.md",
            *third_arguments,
            repo=isolated_path,
        )
        heartbeat = self.claim("heartbeat", "--claim-id", "second", repo=isolated_path)

        self.assertEqual(0, third.returncode, third.stderr)
        self.assertEqual(0, heartbeat.returncode, heartbeat.stderr)
        self.assertTrue(third_path.is_dir())
        self.assertFalse((isolated_path / ".worktrees" / "third").exists())
        events = self.journal_events()
        self.assertEqual(["first", "second", "third", "second"], [event["claim_id"] for event in events])
        self.assertEqual(1, len(list(self.hot_directory().glob("*.jsonl"))))
        linked_event = next(event for event in events if event["claim_id"] == "third")
        self.assertEqual("codex/third", linked_event["worktree_id"])
        self.assertNotIn(str(self.temporary_directory.name), json.dumps(linked_event))

    def test_legacy_linked_claim_without_topology_retains_accurate_journal_fallback(self) -> None:
        linked_path = self.existing_linked_worktree()
        acquired = self.claim(
            *self.acquire_arguments("private"),
            "--file",
            "README.md",
            repo=linked_path,
        )
        registry = json.loads(self.registry_path().read_text(encoding="utf-8"))
        registry["claims"][0].pop("checkout_topology")
        self.registry_path().write_text(
            json.dumps(registry, indent=2) + "\n",
            encoding="utf-8",
        )

        heartbeat = self.claim("heartbeat", "--claim-id", "private", repo=linked_path)

        self.assertEqual(0, acquired.returncode, acquired.stderr)
        self.assertEqual(0, heartbeat.returncode, heartbeat.stderr)
        event = self.journal_events()[-1]
        self.assertEqual("HEARTBEAT", event["outcome"])
        self.assertEqual("primary", event["mode"])
        self.assertEqual("linked", event["checkout_topology"])
        self.assertEqual("codex/private", event["worktree_id"])
        self.assertNotIn(str(self.temporary_directory.name), json.dumps(event))

    def test_concurrent_journal_events_are_complete_and_unique(self) -> None:
        self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        commands = [self.claim_command("heartbeat", "--claim-id", "first") for _index in range(12)]
        processes = [
            subprocess.Popen(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            for command in commands
        ]
        completed = [process.communicate() + (process.returncode,) for process in processes]

        self.assertTrue(all(code == 0 for _stdout, _stderr, code in completed))
        events = self.journal_events()
        self.assertEqual(13, len(events))
        self.assertEqual(13, len({event["event_id"] for event in events}))

    def test_journal_failure_warns_without_weakening_registry_safety(self) -> None:
        completed = self.claim(
            *self.acquire_arguments("first"),
            "--file",
            "README.md",
            environment={"RESOURCE_CLAIM_TEST_FAIL_JOURNAL_WRITE": "1"},
        )

        self.assertEqual(0, completed.returncode, completed.stderr)
        result = self.output(completed)
        self.assertEqual("journal_write_failed", result["warnings"][0]["code"])
        self.assertFalse(result["journal"]["persisted"])
        registry = json.loads(self.registry_path().read_text(encoding="utf-8"))
        self.assertEqual(["first"], [claim["claim_id"] for claim in registry["claims"]])
        report = self.claim("report", "--since", "2d")
        self.assertEqual(
            [{"detail": "live claim has no acquisition event", "source": "first"}],
            json.loads(report.stdout)["coverage_gaps"],
        )

    def test_released_claim_reconstructs_as_journal_lifecycle(self) -> None:
        self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        self.claim("heartbeat", "--claim-id", "first")
        (self.repository / "README.md").write_text("committed\n", encoding="utf-8")
        self.git("add", "README.md")
        self.git("commit", "-m", "change")
        released = self.claim("release", "--claim-id", "first")

        self.assertEqual(0, released.returncode, released.stderr)
        events = self.journal_events()
        self.assertTrue(all(event["schema_version"] == 1 for event in events))
        self.assertEqual(["PRIMARY", "HEARTBEAT", "RELEASED"], [event["outcome"] for event in events])
        self.assertIsNone(events[-1]["resulting_commit"])
        self.assertNotIn("no_change", events[-1])

    def test_release_journal_failure_restores_exact_claim(self) -> None:
        acquired = self.claim(
            *self.acquire_arguments("first"),
            "--file",
            "README.md",
        )
        registry_before = self.registry_path().read_bytes()
        rejected = self.claim(
            "release",
            "--claim-id",
            "first",
            environment={"RESOURCE_CLAIM_TEST_FAIL_JOURNAL_WRITE": "1"},
        )

        self.assertEqual(0, acquired.returncode, acquired.stderr)
        self.assertEqual(1, rejected.returncode)
        self.assertEqual("RELEASE_ERROR", self.output(rejected)["outcome"])
        self.assertEqual(registry_before, self.registry_path().read_bytes())
        self.assertFalse(
            any(event["outcome"] == "RELEASED" for event in self.journal_events())
        )

    def test_dirty_file_does_not_change_claim_acquisition_or_release(self) -> None:
        (self.repository / "README.md").write_text("dirty\n", encoding="utf-8")
        acquired = self.claim(
            *self.acquire_arguments("dirty-file"),
            "--file",
            "README.md",
        )
        released = self.claim("release", "--claim-id", "dirty-file")

        self.assertEqual(0, acquired.returncode, acquired.stderr)
        result = self.output(acquired)
        self.assertEqual("SHARED_CHECKOUT_ACQUIRED", result["outcome"])
        self.assertEqual("PRIMARY", result["legacy_outcome"])
        self.assertNotIn("baseline_status", result["claim"])
        self.assertEqual(0, released.returncode, released.stderr)

    def test_isolated_worktrees_commit_without_global_commit_resource(self) -> None:
        self.claim(*self.acquire_arguments("first"), "--file", "first.txt")
        isolated, isolated_path = self.isolated_arguments("second")
        self.claim(*self.acquire_arguments("second"), "--file", "second.txt", *isolated)
        (self.repository / "first.txt").write_text("first\n", encoding="utf-8")
        (isolated_path / "second.txt").write_text("second\n", encoding="utf-8")
        self.git("add", "first.txt")
        self.git("add", "second.txt", worktree=isolated_path)
        processes = [
            subprocess.Popen(
                ["git", "-C", str(worktree), "commit", "-m", message],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            for worktree, message in ((self.repository, "first"), (isolated_path, "second"))
        ]
        completed = [process.communicate() + (process.returncode,) for process in processes]

        self.assertTrue(all(code == 0 for _stdout, _stderr, code in completed), completed)

    def test_integration_resources_conflict_per_target_branch(self) -> None:
        main = self.claim(
            *self.acquire_arguments("main"),
            *self.timed_resource_arguments(
                resource="merge:integration:main",
                resource_class="main-integration",
            ),
        )
        same_target = self.claim(
            *self.acquire_arguments("same"),
            *self.timed_resource_arguments(
                resource="merge:integration:main",
                resource_class="main-integration",
            ),
        )
        isolated, _isolated_path = self.isolated_arguments("release")
        other_target = self.claim(
            *self.acquire_arguments("release"),
            *self.timed_resource_arguments(
                resource="merge:integration:release",
                resource_class="main-integration",
            ),
            *isolated,
        )

        self.assertEqual(0, main.returncode, main.stderr)
        self.assertEqual(3, same_target.returncode)
        self.assertEqual(0, other_target.returncode, other_target.stderr)

    def test_maintenance_keeps_two_hot_days_and_archives_older_days_losslessly(self) -> None:
        for day in ("2026-07-10", "2026-07-11", "2026-07-12", "2026-07-13"):
            event = self.synthetic_event(
                f"event-{day}",
                f"{day}T12:00:00Z",
                "acquire",
                "PRIMARY",
                f"claim-{day}",
            )
            self.write_daily_events(day, [event])
        environment = {"RESOURCE_CLAIM_TEST_NOW": "2026-07-13T15:00:00Z"}

        maintained = self.claim("maintain-journal", "--hot-days", "2", environment=environment)
        rerun = self.claim("maintain-journal", "--hot-days", "2", environment=environment)

        self.assertEqual(0, maintained.returncode, maintained.stderr)
        self.assertEqual(0, rerun.returncode, rerun.stderr)
        self.assertEqual(
            ["2026-07-12.jsonl", "2026-07-13.jsonl"],
            sorted(path.name for path in self.hot_directory().glob("*.jsonl")),
        )
        archive_root = self.state_root() / "agent-claim-events" / "archive" / "2026" / "07"
        summary_root = self.state_root() / "agent-claim-events" / "journal" / "2026" / "07"
        for day in ("2026-07-10", "2026-07-11"):
            archive = archive_root / f"{day}.jsonl.gz"
            summary = summary_root / f"{day}.json"
            events = [json.loads(line) for line in gzip.decompress(archive.read_bytes()).decode().splitlines()]
            self.assertEqual([f"event-{day}"], [event["event_id"] for event in events])
            self.assertEqual(1, json.loads(summary.read_text(encoding="utf-8"))["raw_event_count"])
        self.assertEqual([], self.output(rerun)["archived"])

    def test_archive_interruption_leaves_hot_file_for_safe_rerun(self) -> None:
        event = self.synthetic_event("old", "2026-07-10T12:00:00Z", "acquire", "PRIMARY", "old")
        hot = self.write_daily_events("2026-07-10", [event])
        environment = {
            "RESOURCE_CLAIM_TEST_NOW": "2026-07-13T15:00:00Z",
            "RESOURCE_CLAIM_TEST_FAIL_ARCHIVE_BEFORE_VALIDATE": "1",
        }

        interrupted = self.claim("maintain-journal", environment=environment)

        self.assertEqual(1, interrupted.returncode)
        self.assertTrue(hot.exists())
        archive = self.state_root() / "agent-claim-events" / "archive" / "2026" / "07" / "2026-07-10.jsonl.gz"
        self.assertFalse(archive.exists())
        completed = self.claim(
            "maintain-journal",
            environment={"RESOURCE_CLAIM_TEST_NOW": "2026-07-13T15:00:00Z"},
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertFalse(hot.exists())

    def test_archive_validation_failure_preserves_hot_source(self) -> None:
        event = self.synthetic_event("old", "2026-07-10T12:00:00Z", "acquire", "PRIMARY", "old")
        hot = self.write_daily_events("2026-07-10", [event])
        archive = self.state_root() / "agent-claim-events" / "archive" / "2026" / "07" / "2026-07-10.jsonl.gz"
        archive.parent.mkdir(parents=True)
        archive.write_bytes(gzip.compress(b'{"different":"event"}\n'))

        completed = self.claim(
            "maintain-journal",
            environment={"RESOURCE_CLAIM_TEST_NOW": "2026-07-13T15:00:00Z"},
        )

        self.assertEqual(1, completed.returncode)
        self.assertEqual("JOURNAL_MAINTENANCE_FAILED", self.output(completed)["outcome"])
        self.assertTrue(hot.exists())

    def test_report_groups_waits_and_distinguishes_contention_kinds(self) -> None:
        events = [
            self.synthetic_event(
                "wait-1",
                "2026-07-12T10:00:00Z",
                "acquire",
                "WAIT",
                "blocked",
                overlaps=[
                    {
                        "scope_kind": "path",
                        "requested_kind": "file",
                        "requested": "src/one.py",
                        "claimed_kind": "file",
                        "claimed": "src/one.py",
                    },
                    {
                        "scope_kind": "resource",
                        "requested_kind": "resource",
                        "requested": "port:3000",
                        "claimed_kind": "resource",
                        "claimed": "port:3000",
                    },
                ],
                journal_warnings=[{"code": "prior_journal_warning"}],
            ),
            self.synthetic_event(
                "wait-2",
                "2026-07-12T10:02:00Z",
                "acquire",
                "WAIT",
                "blocked",
                overlaps=[
                    {
                        "scope_kind": "path",
                        "requested_kind": "file",
                        "requested": "src/one.py",
                        "claimed_kind": "tree",
                        "claimed": "src",
                    }
                ],
            ),
            self.synthetic_event(
                "acquire",
                "2026-07-12T10:05:00Z",
                "acquire",
                "PRIMARY",
                "blocked",
                requested_scopes={
                    "files": [],
                    "trees": ["src"],
                    "project_files": False,
                    "backlog": False,
                    "all_files": False,
                    "file_domain": "project_files",
                    "resources": ["merge:integration:main"],
                    "scope_reason": "source migration",
                },
            ),
            self.synthetic_event(
                "backlog-domain",
                "2026-07-12T10:05:10Z",
                "extend",
                "EXTENDED",
                "backlog-domain",
                requested_scopes={
                    "files": [],
                    "trees": [],
                    "project_files": False,
                    "backlog": True,
                    "all_files": False,
                    "file_domain": "backlog",
                    "resources": [],
                    "scope_reason": None,
                },
            ),
            self.synthetic_event(
                "all-domain",
                "2026-07-12T10:05:20Z",
                "extend",
                "EXTENDED",
                "all-domain",
                requested_scopes={
                    "files": [],
                    "trees": [],
                    "project_files": False,
                    "backlog": False,
                    "all_files": True,
                    "file_domain": "all_files",
                    "resources": [],
                    "scope_reason": "source migration",
                },
            ),
            self.synthetic_event("release", "2026-07-12T10:06:00Z", "release", "RELEASED", "blocked"),
            self.synthetic_event(
                "isolate",
                "2026-07-12T10:10:00Z",
                "acquire",
                "ISOLATE",
                "isolated",
                mode="isolated",
            ),
            self.synthetic_event(
                "shared-required",
                "2026-07-12T10:10:30Z",
                "acquire",
                "PRIMARY_REQUIRED",
                "shared-required",
                active_claim_count=1,
                shared_checkout_claimed=False,
            ),
            self.synthetic_event("isolate-release", "2026-07-12T10:11:00Z", "release", "RELEASED", "isolated"),
            self.synthetic_event("recover", "2026-07-12T10:20:00Z", "acquire", "RECOVER", "recovery"),
            self.synthetic_event("recover-release", "2026-07-12T10:21:00Z", "release", "RELEASED", "recovery"),
        ]
        self.write_daily_events("2026-07-12", events)
        environment = {"RESOURCE_CLAIM_TEST_NOW": "2026-07-13T10:00:00Z"}
        registry_before = self.registry_path().read_bytes() if self.registry_path().exists() else b""
        journal_before = (self.hot_directory() / "2026-07-12.jsonl").read_bytes()

        completed = self.claim("report", "--since", "2d", environment=environment)

        self.assertEqual(0, completed.returncode, completed.stderr)
        report = json.loads(completed.stdout)
        self.assertEqual(2, report["schema_version"])
        metrics = report["metrics"]
        self.assertEqual(
            {"primary": 1, "isolated": 1, "recovery": 1},
            metrics["successful_acquisitions"],
        )
        self.assertEqual(2, metrics["wait_attempt_count"])
        self.assertEqual(2, metrics["outcome_counts"]["CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED"])
        self.assertEqual(2, metrics["raw_outcome_counts"]["WAIT"])
        self.assertEqual(1, metrics["outcome_counts"]["SHARED_CHECKOUT_REQUIRED"])
        self.assertEqual(1, metrics["raw_outcome_counts"]["PRIMARY_REQUIRED"])
        self.assertEqual(1, len(metrics["wait_episodes"]))
        self.assertEqual(300.0, metrics["wait_episodes"][0]["duration_seconds"])
        self.assertEqual("src/one.py", metrics["top_contention"]["exact_files"][0]["scope"])
        self.assertEqual("src/one.py", metrics["top_contention"]["trees"][0]["scope"])
        self.assertEqual("port:3000", metrics["top_contention"]["resources"][0]["scope"])
        self.assertEqual(60.0, metrics["claim_duration_seconds"]["median"])
        self.assertEqual("source migration", metrics["broad_scopes"]["reasons"][0]["scope"])
        self.assertEqual(
            {"all_files": 1, "backlog": 1, "project_files": 1},
            metrics["broad_scopes"]["file_domains"],
        )
        self.assertEqual("merge:integration:main", metrics["integration_resources"][0]["scope"])
        self.assertEqual(1, metrics["journal_warning_count"])
        if registry_before:
            self.assertEqual(registry_before, self.registry_path().read_bytes())
        else:
            self.assertFalse(self.registry_path().exists())
        self.assertEqual(journal_before, (self.hot_directory() / "2026-07-12.jsonl").read_bytes())

    def test_report_exposes_successful_exact_file_adoption_in_json_and_text(self) -> None:
        environment = {"RESOURCE_CLAIM_TEST_NOW": "2026-07-13T10:00:00Z"}
        acquired = self.claim(
            *self.acquire_arguments("exact-file"),
            "--file",
            "src/one.py",
            environment=environment,
        )
        released = self.claim(
            "release",
            "--claim-id",
            "exact-file",
            environment=environment,
        )

        json_report = self.claim(
            "report",
            "--since",
            "2d",
            environment=environment,
        )
        text_report = self.claim(
            "report",
            "--since",
            "2d",
            "--format",
            "text",
            environment=environment,
        )

        self.assertEqual(0, acquired.returncode, acquired.stderr)
        self.assertEqual(0, released.returncode, released.stderr)
        self.assertEqual(0, json_report.returncode, json_report.stderr)
        self.assertEqual(
            [{"count": 1, "scope": "src/one.py"}],
            self.output(json_report)["metrics"]["successful_scope_adoptions"]["exact_files"],
        )
        self.assertEqual(0, text_report.returncode, text_report.stderr)
        self.assertNotIn('"outcome"', text_report.stdout)
        self.assertIn(
            "Successful exact-file adoptions: src/one.py=1",
            text_report.stdout,
        )

    def test_report_keeps_ambiguous_legacy_primary_required_outcome_raw(self) -> None:
        event = self.synthetic_event(
            "ambiguous-primary-required",
            "2026-07-12T10:00:00Z",
            "acquire",
            "PRIMARY_REQUIRED",
            "ambiguous",
            active_claim_count=1,
        )
        self.write_daily_events("2026-07-12", [event])

        completed = self.claim(
            "report",
            "--since",
            "2d",
            environment={"RESOURCE_CLAIM_TEST_NOW": "2026-07-13T10:00:00Z"},
        )

        self.assertEqual(0, completed.returncode, completed.stderr)
        report = self.output(completed)
        self.assertEqual(1, report["metrics"]["outcome_counts"]["PRIMARY_REQUIRED"])
        self.assertEqual(
            "legacy PRIMARY_REQUIRED lacks deterministic shared-checkout ownership evidence",
            report["metrics"]["outcome_normalization_gaps"][0]["detail"],
        )

    def test_daily_boundaries_use_utc_not_local_daylight_saving(self) -> None:
        event = self.synthetic_event("old", "2026-11-01T23:30:00Z", "acquire", "PRIMARY", "old")
        old = self.write_daily_events("2026-11-01", [event])
        current = self.write_daily_events(
            "2026-11-03",
            [self.synthetic_event("current", "2026-11-03T00:01:00Z", "heartbeat", "HEARTBEAT", "current")],
        )

        completed = self.claim(
            "maintain-journal",
            "--hot-days",
            "2",
            environment={"RESOURCE_CLAIM_TEST_NOW": "2026-11-03T00:05:00Z", "TZ": "America/Toronto"},
        )

        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertFalse(old.exists())
        self.assertTrue(current.exists())


if __name__ == "__main__":
    unittest.main()
