# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies Dev Backlog Steward blocked-work resumption and Future Ideas evaluation contracts.
# Governing design: evals/agent-tests/dev-backlog-steward/skills/dev-backlog-steward-suite-contract/SKILL.md
# Governing test plan: evals/agent-tests/dev-backlog-steward/scenarios.yaml

from __future__ import annotations

import importlib.util
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any, Callable

import yaml


SUITE_ROOT = Path(__file__).resolve().parent
_PROMOTION_FIXTURE = yaml.safe_load(
    (SUITE_ROOT / "fixtures" / "cases.yaml").read_text(encoding="utf-8")
)["cases"]["future-ideas-capture-and-promotion"]
_IDEA_CLAIM_PATH = _PROMOTION_FIXTURE["ideaPath"]
_TARGET_CLAIM_PATH = _PROMOTION_FIXTURE["promotedWorkItemPath"]
_PROMOTED_WORK_ITEM_ID = Path(_TARGET_CLAIM_PATH).stem
_PROMOTION_CLAIM_MANIFEST = (_IDEA_CLAIM_PATH, _TARGET_CLAIM_PATH)
_ATOMIC_PROMOTION_ACQUIRE = f"acquire:{'|'.join(_PROMOTION_CLAIM_MANIFEST)}"
_RELEASED_PROMOTION_CLAIMS = (
    _ATOMIC_PROMOTION_ACQUIRE,
    f"release:{'|'.join(_PROMOTION_CLAIM_MANIFEST)}",
)
_RETAINED_PROMOTION_CLAIMS = (
    _ATOMIC_PROMOTION_ACQUIRE,
    f"retain:{'|'.join(_PROMOTION_CLAIM_MANIFEST)}",
)
_IDEA_BEFORE_BYTES = _PROMOTION_FIXTURE["ideaBefore"].encode("utf-8")
_PROMOTED_IDEA_BYTES = _PROMOTION_FIXTURE["ideaAfter"].encode("utf-8")
_PROMOTED_ITEM_BYTES = _PROMOTION_FIXTURE["promotedWorkItem"].encode("utf-8")
_HARNESS_PATH = SUITE_ROOT / "contract_harness.py"
_SPEC = importlib.util.spec_from_file_location(
    "dev_backlog_steward_contract_harness", _HARNESS_PATH
)
assert _SPEC is not None and _SPEC.loader is not None
contract_harness = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = contract_harness
_SPEC.loader.exec_module(contract_harness)


def _restore_snapshot(path: Path, existed: bool, content: bytes) -> None:
    """Restore one path to its exact pre-attempt bytes or absence."""
    if existed:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    else:
        path.unlink(missing_ok=True)


def _unrelated_worktree_state(
    repository: Path,
    manifest: tuple[str, ...],
) -> dict[str, tuple[str, int, bytes | str]]:
    """Capture exact non-manifest worktree entries without entering .git."""
    state: dict[str, tuple[str, int, bytes | str]] = {}
    excluded = set(manifest)
    for path in repository.rglob("*"):
        relative = path.relative_to(repository).as_posix()
        if relative == ".git" or relative.startswith(".git/"):
            continue
        if relative in excluded:
            continue
        mode = stat.S_IMODE(path.lstat().st_mode)
        if path.is_symlink():
            state[relative] = ("symlink", mode, os.readlink(path))
        elif path.is_dir():
            continue
        else:
            state[relative] = ("regular", mode, path.read_bytes())
    return state


def _index_entries(repository: Path) -> dict[str, tuple[str, str, int]]:
    """Return mode, object ID, and stage for every Git index entry."""
    output = subprocess.run(
        ["git", "-C", str(repository), "ls-files", "--stage", "-z"],
        check=True,
        capture_output=True,
    ).stdout
    entries: dict[str, tuple[str, str, int]] = {}
    for record in output.split(b"\0"):
        if not record:
            continue
        metadata, separator, path_bytes = record.partition(b"\t")
        if not separator:
            raise RuntimeError("Git returned a malformed index entry")
        mode, object_id, stage = metadata.decode("ascii").split()
        path = path_bytes.decode("utf-8", errors="surrogateescape")
        entries[path] = (mode, object_id, int(stage))
    return entries


def _validate_promoted_records(
    idea_before: bytes,
    idea_after: bytes,
    target_after: bytes,
    *,
    idea_relative: str,
    target_relative: str,
) -> None:
    """Require intact source content and a complete typed destination record."""
    work_item_id = Path(target_relative).stem
    promoted_to = f"Promoted To: {work_item_id}\n".encode("utf-8")
    if idea_after.count(promoted_to) != 1:
        raise ValueError("idea requires one exact promoted Work Item ID")
    if idea_after.replace(promoted_to, b"", 1) != idea_before:
        raise ValueError("promoted idea does not preserve its complete source record")

    try:
        target_text = target_after.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError("target is not valid UTF-8") from error
    title_lines = [line for line in target_text.splitlines() if line.startswith("# ")]
    if len(title_lines) != 1 or not title_lines[0].removeprefix("# ").strip():
        raise ValueError("target requires one nonempty title")
    required_fields = {
        "Status": "Ready",
        "Type": "Feature",
        "Provider": "file",
        "Provider Reference": target_relative,
        "Work Item ID": work_item_id,
        "Completion": "main-branch",
    }
    lines = target_text.splitlines()
    for field, expected in required_fields.items():
        prefix = f"{field}: "
        values = [
            line.removeprefix(prefix).strip()
            for line in lines
            if line.startswith(prefix)
        ]
        if len(values) != 1 or not values[0]:
            raise ValueError(f"target requires one nonempty {field} field")
        if values[0] != expected:
            raise ValueError(f"target {field} does not match its governed identity")

    required_sections = (
        "Summary",
        "Context",
        "Source Evidence",
        "Requirements",
        "Acceptance Criteria",
        "Dependencies",
        "Verification",
        "Open Questions",
    )
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for line in lines:
        if line.startswith("## "):
            current = line.removeprefix("## ").strip()
            sections[current] = []
        elif current is not None:
            sections[current].append(line)
    for section in required_sections:
        if section not in sections or not "\n".join(sections[section]).strip():
            raise ValueError(f"target requires a nonempty {section} section")
    if idea_relative not in "\n".join(sections["Source Evidence"]):
        raise ValueError("target lacks reciprocal idea provenance")


def _inventory_future_ideas(
    future_ideas_root: Path,
    *,
    explicitly_requested: bool,
) -> dict[str, Any]:
    """Exercise read-only Future Ideas inventory against real test files."""
    if not explicitly_requested:
        return {
            "status": "BLOCKED",
            "ideas": [],
            "invalidRecords": [],
            "ordinaryLifecycleCount": 0,
            "mutations": [],
        }

    canonical_root = future_ideas_root.resolve(strict=True)
    ideas: list[dict[str, str]] = []
    invalid_records: list[dict[str, Any]] = []
    identities: dict[tuple[str, str, str], str] = {}

    for entry in sorted(future_ideas_root.iterdir(), key=lambda path: path.name):
        record_path = f"backlog/future-ideas/{entry.name}"
        try:
            resolved = entry.resolve(strict=True)
        except OSError as error:
            invalid_records.append(
                {"path": record_path, "issues": [f"unreadable: {error}"]}
            )
            continue
        if (
            entry.is_symlink()
            or canonical_root not in resolved.parents
            or not resolved.is_file()
        ):
            invalid_records.append(
                {"path": record_path, "issues": ["not a canonical regular file"]}
            )
            continue

        try:
            content = resolved.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            invalid_records.append(
                {"path": record_path, "issues": [f"unreadable: {error}"]}
            )
            continue

        title_lines = [
            line.removeprefix("# ").strip()
            for line in content.splitlines()
            if line.startswith("# ")
        ]
        issues: list[str] = []
        if len(title_lines) != 1 or not title_lines[0]:
            issues.append("requires exactly one nonempty title")

        sections: dict[str, str] = {}
        current_section: str | None = None
        section_lines: list[str] = []
        for line in content.splitlines():
            if line.startswith("## "):
                if current_section is not None:
                    sections[current_section] = "\n".join(section_lines).strip()
                current_section = line.removeprefix("## ").strip()
                section_lines = []
            elif current_section is not None:
                section_lines.append(line)
        if current_section is not None:
            sections[current_section] = "\n".join(section_lines).strip()

        for section in ("Synopsis", "Origin or Rationale"):
            if not sections.get(section):
                issues.append(f"missing or empty {section}")

        if issues:
            invalid_records.append({"path": record_path, "issues": issues})
            continue

        title = title_lines[0]
        identity = (
            title.casefold(),
            sections["Synopsis"].casefold(),
            sections["Origin or Rationale"].casefold(),
        )
        if identity in identities:
            invalid_records.append(
                {
                    "path": record_path,
                    "issues": [f"duplicates {identities[identity]}"],
                }
            )
            continue
        identities[identity] = record_path
        ideas.append(
            {
                "path": record_path,
                "title": title,
                "synopsis": sections["Synopsis"],
                "originOrRationale": sections["Origin or Rationale"],
            }
        )

    return {
        "status": "PASS",
        "ideas": ideas,
        "invalidRecords": invalid_records,
        "ordinaryLifecycleCount": 0,
        "mutations": [],
    }


def _execute_capture_transaction(
    repository: Path,
    idea: Path,
    idea_bytes: bytes,
) -> dict[str, object]:
    """Create and commit one Future Idea through real exclusive file and Git operations."""
    idea_relative = idea.relative_to(repository).as_posix()
    if os.path.lexists(idea):
        return {"status": "BLOCKED", "reason": "target collision"}
    descriptor = os.open(idea, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o666)
    try:
        pending = memoryview(idea_bytes)
        while pending:
            written = os.write(descriptor, pending)
            if written == 0:
                raise OSError("exclusive idea write made no progress")
            pending = pending[written:]
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    subprocess.run(
        ["git", "-C", str(repository), "add", "--", idea_relative],
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        [
            "git",
            "-C",
            str(repository),
            "commit",
            "--quiet",
            "--only",
            "-m",
            "Capture Future Idea",
            "--",
            idea_relative,
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    commit_oid = subprocess.run(
        ["git", "-C", str(repository), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    committed_paths = subprocess.run(
        [
            "git",
            "-C",
            str(repository),
            "diff-tree",
            "--no-commit-id",
            "--name-only",
            "-r",
            commit_oid,
        ],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    committed_bytes = subprocess.run(
        ["git", "-C", str(repository), "show", f"{commit_oid}:{idea_relative}"],
        check=True,
        capture_output=True,
    ).stdout
    return {
        "status": "READY",
        "commitOid": commit_oid,
        "committedPaths": tuple(committed_paths),
        "committedBytes": committed_bytes,
    }


class _FakeClaimRegistry:
    """Record exact-path promotion claims exercised by contract tests."""

    def __init__(self, *, conflicting_paths: set[str] | None = None) -> None:
        """Create an empty path-aware registry with optional existing conflicts."""
        self.active_paths: set[str] = set()
        self.conflicting_paths = set(conflicting_paths or ())
        self.last_conflicts: set[str] = set()
        self.calls: list[str] = []

    @property
    def active(self) -> bool:
        """Report whether any exact-path promotion claim remains active."""
        return bool(self.active_paths)

    def acquire(self, paths: tuple[str, ...]) -> bool:
        """Acquire one exact multi-path manifest atomically or acquire nothing."""
        if self.active_paths:
            raise RuntimeError("a promotion manifest claim is already active")
        if not paths or len(set(paths)) != len(paths):
            raise ValueError("claim manifest requires unique exact paths")
        self.calls.append(f"acquire:{'|'.join(paths)}")
        self.last_conflicts = set(paths) & self.conflicting_paths
        if self.last_conflicts:
            return False
        self.active_paths.update(paths)
        return True

    def retain_all(self) -> None:
        """Record retained exact-path ownership after unsafe recovery."""
        if not self.active_paths:
            raise RuntimeError("no active claims to retain")
        self.calls.append(f"retain:{'|'.join(_PROMOTION_CLAIM_MANIFEST)}")

    def release_all(self) -> None:
        """Release every exact-path claim after success or a safe stop."""
        if not self.active_paths:
            raise RuntimeError("no active claims to release")
        self.calls.append(f"release:{'|'.join(_PROMOTION_CLAIM_MANIFEST)}")
        self.active_paths.clear()


def _execute_promotion_transaction(
    repository: Path,
    idea: Path,
    target: Path,
    idea_after: bytes,
    target_after: bytes,
    *,
    resource_coordination: str,
    claim_registry: _FakeClaimRegistry | None = None,
    after_claims: Callable[[], None] | None = None,
    after_commit: Callable[[str], None] | None = None,
    fail_boundary: str | None = None,
    fail_staging: bool = False,
    fail_commit: bool = False,
    fail_postcommit_verification: bool = False,
    fail_rollback_verification: bool = False,
) -> dict[str, object]:
    """Exercise the promotion contract against a real temporary Git index.

    The transaction snapshots exact worktree and index bytes, stages only the
    reciprocal records, commits only those paths, and verifies the captured
    commit object. Resource-claim coordination records acquire, retain, and release
    calls; none performs the same Git transaction without claim operations or
    claim evidence.
    """
    if resource_coordination not in {"resource-claim", "none"}:
        raise ValueError("unsupported resource coordination selection")
    if resource_coordination == "resource-claim" and claim_registry is None:
        raise ValueError("resource-claim requires a claim registry")
    if fail_rollback_verification:
        if fail_staging or fail_postcommit_verification:
            raise ValueError("rollback verification requires a commit failure")
        legacy_boundaries = ["rollback-verification"]
    else:
        legacy_boundaries = [
            boundary
            for enabled, boundary in (
                (fail_staging, "staging"),
                (fail_commit, "commit"),
                (fail_postcommit_verification, "post-commit-verification"),
            )
            if enabled
        ]
    if fail_boundary is not None and legacy_boundaries:
        raise ValueError("use one failure injection interface")
    if len(legacy_boundaries) > 1:
        raise ValueError("only one failure boundary may be injected")
    injected_boundary = fail_boundary or (legacy_boundaries[0] if legacy_boundaries else None)
    allowed_boundaries = {
        None,
        "target-write",
        "idea-write",
        "validation",
        "staging",
        "commit",
        "post-commit-verification",
        "rollback-verification",
    }
    if injected_boundary not in allowed_boundaries:
        raise ValueError(f"unsupported failure boundary: {injected_boundary}")

    def result_with_claim_evidence(
        result: dict[str, object],
        *,
        retain: bool = False,
        release: bool = False,
    ) -> dict[str, object]:
        """Apply the selected coordination lifecycle to one transaction result."""
        if resource_coordination == "resource-claim":
            assert claim_registry is not None
            if retain:
                claim_registry.retain_all()
            if release:
                claim_registry.release_all()
            result["claimRetained"] = claim_registry.active
            result["claimCalls"] = tuple(claim_registry.calls)
        return result

    idea_relative = idea.relative_to(repository).as_posix()
    target_relative = target.relative_to(repository).as_posix()
    repository_root = repository.resolve(strict=True)

    def path_state(path: Path) -> tuple[bool, str, str, bool, bytes | None]:
        """Capture existence, type, resolved authority, containment, and bytes."""
        exists = os.path.lexists(path)
        if exists:
            try:
                resolved = path.resolve(strict=True)
            except OSError:
                resolved = path.absolute()
            mode = path.lstat().st_mode
            file_type = "regular" if stat.S_ISREG(mode) else "other"
            contained = resolved == repository_root or repository_root in resolved.parents
            content = path.read_bytes() if file_type == "regular" and contained else None
            return exists, file_type, str(resolved), contained, content
        parent = path.parent.resolve(strict=True)
        resolved = parent / path.name
        contained = resolved == repository_root or repository_root in resolved.parents
        return False, "absent", str(resolved), contained, None

    idea_state_before = path_state(idea)
    target_state_before = path_state(target)
    if idea_state_before[1] != "regular" or not idea_state_before[3]:
        return result_with_claim_evidence(
            {"status": "BLOCKED", "zeroMutation": True, "reason": "invalid source"}
        )
    if not target_state_before[3]:
        return result_with_claim_evidence(
            {
                "status": "BLOCKED",
                "zeroMutation": True,
                "commitCreated": False,
                "reason": "invalid destination authority",
            }
        )
    if target_state_before[0]:
        return result_with_claim_evidence(
            {
                "status": "BLOCKED",
                "zeroMutation": True,
                "rollbackVerified": True,
                "reason": "target collision",
            }
        )

    idea_existed = idea_state_before[0]
    idea_before = idea_state_before[4] or b""
    target_existed = target_state_before[0]
    target_before = target_state_before[4] or b""
    index_location = subprocess.run(
        ["git", "-C", str(repository), "rev-parse", "--git-path", "index"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    index_path = Path(index_location)
    if not index_path.is_absolute():
        index_path = repository / index_path
    index_existed = index_path.exists()
    index_before = index_path.read_bytes() if index_existed else b""
    head_before = subprocess.run(
        ["git", "-C", str(repository), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    manifest = (idea_relative, target_relative)
    index_entries_before = _index_entries(repository)
    unrelated_worktree_before = _unrelated_worktree_state(repository, manifest)

    if resource_coordination == "resource-claim":
        assert claim_registry is not None
        if not claim_registry.acquire((idea_relative, target_relative)):
            return result_with_claim_evidence(
                {
                    "status": "BLOCKED",
                    "zeroMutation": True,
                    "commitCreated": False,
                    "claimOutcome": "CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED",
                    "conflictingPaths": tuple(sorted(claim_registry.last_conflicts)),
                }
            )
    if after_claims is not None:
        after_claims()

    index_exists_after_claims = index_path.exists()
    index_after_claims = index_path.read_bytes() if index_exists_after_claims else b""
    head_after_claims = subprocess.run(
        ["git", "-C", str(repository), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    unrelated_worktree_after_claims = _unrelated_worktree_state(
        repository, manifest
    )
    drift = []
    if path_state(idea) != idea_state_before:
        drift.append("source")
    target_state_after_claims = path_state(target)
    if not target_state_after_claims[3]:
        drift.append("destination authority")
    elif target_state_after_claims != target_state_before:
        drift.append("destination")
    if head_after_claims != head_before:
        drift.append("HEAD")
    if (index_exists_after_claims, index_after_claims) != (index_existed, index_before):
        drift.append("index")
    if unrelated_worktree_after_claims != unrelated_worktree_before:
        drift.append("unrelated worktree or staged state")
    if drift:
        return result_with_claim_evidence(
            {
                "status": "BLOCKED",
                "zeroMutation": True,
                "drift": tuple(drift),
                "commitCreated": False,
            },
            release=True,
        )

    recovery = (
        repository
        / ".git"
        / "future-idea-promotion-recovery"
        / "contract-attempt"
    )
    recovery.mkdir(parents=True)
    (recovery / "idea.bin").write_bytes(idea_before)
    (recovery / "target.bin").write_bytes(target_before)
    (recovery / "target-state").write_bytes(
        b"present\n" if target_existed else b"absent\n"
    )
    (recovery / "index.bin").write_bytes(index_before)
    (recovery / "index-state").write_bytes(
        b"present\n" if index_existed else b"absent\n"
    )

    commit_oid: str | None = None
    try:
        target_descriptor = os.open(
            target,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL,
            0o666,
        )
        try:
            pending = memoryview(target_after)
            while pending:
                written = os.write(target_descriptor, pending)
                if written == 0:
                    raise OSError("exclusive target write made no progress")
                pending = pending[written:]
            os.fsync(target_descriptor)
        finally:
            os.close(target_descriptor)
        if injected_boundary == "target-write":
            raise OSError("injected target-write failure")
        idea.write_bytes(idea_after)
        if injected_boundary == "idea-write":
            raise OSError("injected idea-write failure")
        if injected_boundary == "validation":
            raise ValueError("injected validation failure")
        _validate_promoted_records(
            idea_before,
            idea_after,
            target_after,
            idea_relative=idea_relative,
            target_relative=target_relative,
        )
        add_arguments = [
            "git",
            "-C",
            str(repository),
            "add",
        ]
        if injected_boundary == "staging":
            add_arguments.append("--invalid-option")
        add_arguments.extend(
            [
                "--",
                idea_relative,
                target_relative,
            ]
        )
        subprocess.run(
            add_arguments,
            check=True,
            capture_output=True,
            text=True,
        )
        commit_arguments = [
            "git",
            "-C",
            str(repository),
            "commit",
            "--quiet",
            "--only",
        ]
        if injected_boundary in {"commit", "rollback-verification"}:
            commit_arguments.append("--cleanup=invalid")
        commit_arguments.extend(
            [
                "-m",
                "Promote Future Idea",
                "--",
                idea_relative,
                target_relative,
            ]
        )
        subprocess.run(
            commit_arguments,
            check=True,
            capture_output=True,
            text=True,
        )
        commit_oid = subprocess.run(
            ["git", "-C", str(repository), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        if after_commit is not None:
            after_commit(commit_oid)
        commit_parent = subprocess.run(
            ["git", "-C", str(repository), "rev-parse", f"{commit_oid}^"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        if commit_parent != head_before:
            raise RuntimeError("confirmed commit parent does not match captured HEAD")
        committed_paths = set(
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(repository),
                    "diff-tree",
                    "--no-commit-id",
                    "--name-only",
                    "-r",
                    commit_oid,
                ],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.splitlines()
        )
        if committed_paths != {idea_relative, target_relative}:
            raise RuntimeError("confirmed commit does not contain exactly the pair")
        for relative_path, expected_content in (
            (idea_relative, idea_after),
            (target_relative, target_after),
        ):
            verification_expected = expected_content
            if (
                injected_boundary == "post-commit-verification"
                and relative_path == target_relative
            ):
                verification_expected += b"injected verification mismatch\n"
            committed_content = subprocess.run(
                [
                    "git",
                    "-C",
                    str(repository),
                    "show",
                    f"{commit_oid}:{relative_path}",
                ],
                check=True,
                capture_output=True,
            ).stdout
            if committed_content != verification_expected:
                raise RuntimeError(
                    "confirmed reciprocal record bytes do not match"
                )
        if (
            _unrelated_worktree_state(repository, manifest)
            != unrelated_worktree_before
        ):
            raise RuntimeError("unrelated worktree bytes or modes changed")
        index_entries_after = _index_entries(repository)
        unrelated_index_before = {
            path: entry
            for path, entry in index_entries_before.items()
            if path not in manifest
        }
        unrelated_index_after = {
            path: entry
            for path, entry in index_entries_after.items()
            if path not in manifest
        }
        if unrelated_index_after != unrelated_index_before:
            raise RuntimeError("unrelated index entries changed")
        for relative_path in manifest:
            committed_object = subprocess.run(
                [
                    "git",
                    "-C",
                    str(repository),
                    "rev-parse",
                    f"{commit_oid}:{relative_path}",
                ],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            index_entry = index_entries_after.get(relative_path)
            if index_entry is None or index_entry[1:] != (committed_object, 0):
                raise RuntimeError("promotion index entry does not match commit")
    except (OSError, subprocess.CalledProcessError, ValueError, RuntimeError) as exc:
        if commit_oid is not None:
            return result_with_claim_evidence(
                {
                    "status": "BLOCKED",
                    "rollbackVerified": False,
                    "recoveryOwner": "Dev Backlog Steward",
                    "preservedEvidence": recovery,
                    "commitOid": commit_oid,
                    "failureBoundary": injected_boundary,
                    "failure": str(exc),
                },
                retain=True,
            )
        try:
            _restore_snapshot(idea, idea_existed, idea_before)
            _restore_snapshot(target, target_existed, target_before)
            _restore_snapshot(index_path, index_existed, index_before)
            if injected_boundary == "rollback-verification":
                idea.write_bytes(idea_before + b"injected rollback divergence\n")
            if (
                idea.exists() != idea_existed
                or target.exists() != target_existed
                or index_path.exists() != index_existed
                or (idea_existed and idea.read_bytes() != idea_before)
                or (target_existed and target.read_bytes() != target_before)
                or (index_existed and index_path.read_bytes() != index_before)
            ):
                raise OSError("rollback verification failed")
            if _index_entries(repository) != index_entries_before:
                raise OSError("rollback did not restore exact index entries")
            if (
                _unrelated_worktree_state(repository, manifest)
                != unrelated_worktree_before
            ):
                raise OSError("rollback changed unrelated worktree bytes or modes")
        except (OSError, RuntimeError, subprocess.CalledProcessError) as rollback_error:
            return result_with_claim_evidence(
                {
                    "status": "BLOCKED",
                    "rollbackVerified": False,
                    "recoveryOwner": "Dev Backlog Steward",
                    "preservedEvidence": recovery,
                    "failureBoundary": injected_boundary,
                    "failure": str(rollback_error),
                },
                retain=True,
            )
        shutil.rmtree(recovery)
        return result_with_claim_evidence(
            {
                "status": "BLOCKED",
                "rollbackVerified": True,
                "indexVerified": True,
                "unrelatedStateVerified": True,
                "failureBoundary": injected_boundary,
                "failure": str(exc),
            },
            release=True,
        )
    shutil.rmtree(recovery)
    return result_with_claim_evidence(
        {
            "status": "READY",
            "commitVerified": True,
            "commitOid": commit_oid,
            "capturedHead": head_before,
            "commitParent": commit_parent,
            "indexVerified": True,
            "unrelatedStateVerified": True,
        },
        release=True,
    )


class DevBacklogStewardContractTests(unittest.TestCase):
    """Protect explicit claim acquisition and evidence preservation during resumption."""

    def _git(self, repository: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
        """Run one checked Git command in a disposable contract repository."""
        return subprocess.run(
            ["git", "-C", str(repository), *arguments],
            check=True,
            capture_output=True,
            text=True,
        )

    def _promotion_repository(
        self,
    ) -> tuple[tempfile.TemporaryDirectory[str], Path, Path, Path, Path, Path]:
        """Create a repository with complete idea and varied unrelated dirty state."""
        temporary = tempfile.TemporaryDirectory()
        repository = Path(temporary.name)
        self._git(repository, "init", "--quiet")
        self._git(repository, "config", "user.name", "Contract Test")
        self._git(repository, "config", "user.email", "contract@example.invalid")
        idea = repository / "backlog/future-ideas/retry-dashboard.md"
        target = repository / "backlog/feature-backlog/retry-dashboard.md"
        unrelated = repository / "unrelated.txt"
        tracked_dirty = repository / "tracked-dirty.txt"
        untracked_dirty = repository / "untracked-dirty.txt"
        idea.parent.mkdir(parents=True)
        target.parent.mkdir(parents=True)
        idea.write_bytes(_IDEA_BEFORE_BYTES)
        unrelated.write_bytes(b"base unrelated bytes\n")
        tracked_dirty.write_bytes(b"base tracked bytes\n")
        self._git(repository, "add", "--", idea.relative_to(repository).as_posix())
        self._git(
            repository,
            "add",
            "--",
            unrelated.relative_to(repository).as_posix(),
            tracked_dirty.relative_to(repository).as_posix(),
        )
        self._git(repository, "commit", "--quiet", "-m", "Initial state")
        unrelated.write_bytes(b"unrelated staged bytes\n")
        unrelated.chmod(0o640)
        self._git(
            repository,
            "add",
            "--",
            unrelated.relative_to(repository).as_posix(),
        )
        tracked_dirty.write_bytes(b"tracked dirty bytes\n")
        tracked_dirty.chmod(0o744)
        untracked_dirty.write_bytes(b"untracked dirty bytes\n")
        untracked_dirty.chmod(0o600)
        index_location = self._git(
            repository, "rev-parse", "--git-path", "index"
        ).stdout.strip()
        index_path = Path(index_location)
        if not index_path.is_absolute():
            index_path = repository / index_path
        return temporary, repository, idea, target, unrelated, index_path

    def test_blocked_handoff_releases_prior_ownership_and_preserves_evidence(self) -> None:
        """A blocked handoff ends the prior claim without losing durable evidence."""
        fixture = yaml.safe_load(
            (SUITE_ROOT / "fixtures" / "cases.yaml").read_text(encoding="utf-8")
        )["cases"]["blocked-state-transition"]
        before = fixture["itemBefore"].encode("utf-8")

        after, transitions = contract_harness.block_for_handoff(before)

        self.assertEqual(("running", "blocked", "released"), transitions)
        expected = before.replace(b"Status: Running", b"Status: Blocked", 1)
        expected = expected.replace(b"Owner: dev-coder", b"Owner: Unowned", 1)
        expected = expected.replace(
            b"Claim: schema-migration-active", b"Claim: None", 1
        )
        self.assertEqual(expected, after)
        for preserved_line in (
            b"Blocker: External schema decision is unavailable.",
            b"Unblock Condition: Approved schema decision is recorded.",
            b"Evidence: Existing schema analysis and verification log.",
            (
                b"Acceptance Criteria: Schema decision remains traceable; "
                b"existing verification remains required."
            ),
        ):
            with self.subTest(preserved_line=preserved_line):
                self.assertIn(preserved_line, after)

    def test_future_ideas_case_and_output_contract_are_aligned(self) -> None:
        """Every suite surface exposes a meaningful Future Idea output contract."""
        fixture = yaml.safe_load(
            (SUITE_ROOT / "fixtures" / "cases.yaml").read_text(encoding="utf-8")
        )["cases"]["future-ideas-capture-and-promotion"]
        scenarios = yaml.safe_load(
            (SUITE_ROOT / "scenarios.yaml").read_text(encoding="utf-8")
        )["scenarios"]
        scenario = next(
            entry
            for entry in scenarios
            if entry["id"] == "future-ideas-capture-and-promotion"
        )
        suite = yaml.safe_load(
            (SUITE_ROOT / "suite.yaml").read_text(encoding="utf-8")
        )
        role = yaml.safe_load(
            (
                SUITE_ROOT.parent.parent.parent
                / "agents"
                / "roles"
                / "dev-activities"
                / "dev-backlog-steward.role.yaml"
            ).read_text(encoding="utf-8")
        )
        expected_output = "backlog item, Future Idea, or status update"

        self.assertEqual("file", fixture["provider"])
        self.assertEqual("github", fixture["nonFileProviderWithoutOverride"])
        self.assertIn("BLOCKED", fixture["nonFileProviderResult"])
        self.assertFalse(fixture["ordinaryScanIncludesIdea"])
        self.assertNotIn("Status:", fixture["ideaBefore"])
        self.assertEqual(_IDEA_BEFORE_BYTES, fixture["ideaBefore"].encode("utf-8"))
        self.assertEqual(
            _PROMOTED_IDEA_BYTES,
            fixture["ideaAfter"].encode("utf-8"),
        )
        self.assertEqual(
            _PROMOTED_ITEM_BYTES,
            fixture["promotedWorkItem"].encode("utf-8"),
        )
        self.assertEqual(
            _IDEA_BEFORE_BYTES,
            _PROMOTED_IDEA_BYTES.replace(
                f"Promoted To: {_PROMOTED_WORK_ITEM_ID}\n".encode("utf-8"),
                b"",
                1,
            ),
        )
        for retained_section in (
            "## Synopsis",
            "## Origin or Rationale",
            "## Revisit Trigger",
        ):
            with self.subTest(retained_section=retained_section):
                self.assertIn(retained_section, fixture["ideaAfter"])
        self.assertIn(
            f"Promoted To: {_PROMOTED_WORK_ITEM_ID}", fixture["ideaAfter"]
        )
        self.assertNotIn(f"Promoted To: {fixture['promotedWorkItemPath']}", fixture["ideaAfter"])
        self.assertIn(
            f"Work Item ID: {_PROMOTED_WORK_ITEM_ID}", fixture["promotedWorkItem"]
        )
        self.assertEqual(
            _PROMOTED_WORK_ITEM_ID,
            Path(fixture["promotedWorkItemPath"]).stem,
        )
        self.assertIn("Completion: main-branch", fixture["promotedWorkItem"])
        for required_section in (
            "## Summary",
            "## Context",
            "## Source Evidence",
            "## Requirements",
            "## Acceptance Criteria",
            "## Dependencies",
            "## Verification",
            "## Open Questions",
        ):
            with self.subTest(required_section=required_section):
                self.assertIn(required_section, fixture["promotedWorkItem"])
        self.assertEqual(expected_output, fixture["expectedOutput"])
        self.assertIn(expected_output, scenario["expectedOutputs"])
        self.assertIn(expected_output, suite["target"]["requiredOutputs"])
        self.assertIn(
            expected_output,
            [next(iter(entry)) for entry in role["outputContract"]],
        )
        self.assertIn(
            "Return the Future Idea output contract", scenario["requiredBehaviors"]
        )

    def test_future_idea_capture_uses_real_exclusive_file_and_git_operations(
        self,
    ) -> None:
        """Capture creates one immutable idea commit and preserves unrelated staging."""
        fixture = yaml.safe_load(
            (SUITE_ROOT / "fixtures" / "cases.yaml").read_text(encoding="utf-8")
        )["cases"]["future-ideas-capture-and-promotion"]
        with tempfile.TemporaryDirectory() as temporary_name:
            repository = Path(temporary_name)
            self._git(repository, "init", "--quiet")
            self._git(repository, "config", "user.name", "Contract Test")
            self._git(
                repository,
                "config",
                "user.email",
                "contract@example.invalid",
            )
            unrelated = repository / "unrelated.txt"
            unrelated.write_bytes(b"base unrelated bytes\n")
            self._git(repository, "add", "--", unrelated.name)
            self._git(repository, "commit", "--quiet", "-m", "Initial state")
            unrelated.write_bytes(b"unrelated staged bytes\n")
            self._git(repository, "add", "--", unrelated.name)
            staged_before = self._git(
                repository, "show", f":{unrelated.name}"
            ).stdout
            idea = repository / fixture["ideaPath"]
            idea.parent.mkdir(parents=True)
            idea_bytes = fixture["ideaBefore"].encode("utf-8")

            result = _execute_capture_transaction(repository, idea, idea_bytes)

            self.assertEqual("READY", result["status"])
            self.assertEqual((fixture["ideaPath"],), result["committedPaths"])
            self.assertEqual(idea_bytes, result["committedBytes"])
            self.assertEqual(idea_bytes, idea.read_bytes())
            self.assertEqual(
                unrelated.name,
                self._git(
                    repository, "diff", "--cached", "--name-only"
                ).stdout.strip(),
            )
            self.assertEqual(
                staged_before, self._git(repository, "show", f":{unrelated.name}").stdout
            )

    def test_future_ideas_inventory_reads_real_files_and_reports_invalid_entries(
        self,
    ) -> None:
        """Inventory validates filesystem records without lifecycle or mutation effects."""
        fixture = yaml.safe_load(
            (SUITE_ROOT / "fixtures" / "cases.yaml").read_text(encoding="utf-8")
        )["cases"]["future-ideas-inventory-and-validation"]
        scenario = next(
            entry
            for entry in yaml.safe_load(
                (SUITE_ROOT / "scenarios.yaml").read_text(encoding="utf-8")
            )["scenarios"]
            if entry["id"] == "future-ideas-inventory-and-validation"
        )
        blocked_without_request = _inventory_future_ideas(
            SUITE_ROOT / "does-not-exist",
            explicitly_requested=False,
        )
        self.assertEqual("BLOCKED", blocked_without_request["status"])
        self.assertEqual([], blocked_without_request["mutations"])
        with tempfile.TemporaryDirectory() as temporary_name:
            repository = Path(temporary_name)
            ideas_root = repository / "backlog" / "future-ideas"
            ideas_root.mkdir(parents=True)
            for name, content in fixture["records"].items():
                (ideas_root / name).write_text(content, encoding="utf-8")
            external = repository.parent / f"{repository.name}-external-idea.md"
            external.write_text(
                fixture["authorityEscape"]["externalBytes"], encoding="utf-8"
            )
            self.addCleanup(external.unlink, missing_ok=True)
            (ideas_root / fixture["authorityEscape"]["path"]).symlink_to(external)

            def directory_state() -> dict[str, tuple[str, bytes | str]]:
                """Capture entries without dereferencing the authority-escaping link."""
                return {
                    path.name: (
                        ("symlink", os.readlink(path))
                        if path.is_symlink()
                        else ("regular", path.read_bytes())
                    )
                    for path in ideas_root.iterdir()
                }

            state_before = directory_state()
            result = _inventory_future_ideas(
                ideas_root,
                explicitly_requested=fixture["explicitlyRequested"],
            )

            self.assertEqual("executable", scenario["status"])
            self.assertEqual("fixtures/cases.yaml", scenario["executableCase"])
            self.assertNotIn("requiresWorkspaceInventory", scenario)
            self.assertNotIn("requiresNoDetectedMutation", scenario)
            self.assertEqual("PASS", result["status"])
            self.assertEqual(
                fixture["expectedValidPaths"],
                [record["path"] for record in result["ideas"]],
            )
            self.assertEqual(
                set(fixture["expectedInvalidPaths"]),
                {record["path"] for record in result["invalidRecords"]},
            )
            escaping_result = next(
                record
                for record in result["invalidRecords"]
                if record["path"].endswith(fixture["authorityEscape"]["path"])
            )
            self.assertEqual(
                ["not a canonical regular file"], escaping_result["issues"]
            )
            self.assertNotIn(
                fixture["authorityEscape"]["externalBytes"], repr(result)
            )
            self.assertEqual(fixture["ordinaryLifecycleCount"], 0)
            self.assertEqual(0, result["ordinaryLifecycleCount"])
            self.assertEqual([], result["mutations"])
            self.assertEqual(state_before, directory_state())

    def test_future_idea_promotion_is_failure_atomic_at_every_boundary(self) -> None:
        """Collision and injected failures restore exact pre-attempt promotion state."""
        fixture = yaml.safe_load(
            (SUITE_ROOT / "fixtures" / "cases.yaml").read_text(encoding="utf-8")
        )["cases"]["future-ideas-capture-and-promotion"]
        scenario = next(
            entry
            for entry in yaml.safe_load(
                (SUITE_ROOT / "scenarios.yaml").read_text(encoding="utf-8")
            )["scenarios"]
            if entry["id"] == "future-ideas-capture-and-promotion"
        )
        contract_text = (
            SUITE_ROOT
            / "skills"
            / "dev-backlog-steward-suite-contract"
            / "SKILL.md"
        ).read_text(encoding="utf-8")
        role = yaml.safe_load(
            (
                SUITE_ROOT.parent.parent.parent
                / "agents"
                / "roles"
                / "dev-activities"
                / "dev-backlog-steward.role.yaml"
            ).read_text(encoding="utf-8")
        )
        transaction = fixture["promotionTransaction"]
        collision = transaction["collision"]
        git_index = transaction["gitIndex"]

        self.assertEqual("BLOCKED", collision["result"])
        self.assertFalse(collision["writesAttempted"])
        self.assertEqual(collision["ideaBefore"], collision["ideaAfter"])
        self.assertEqual(collision["targetBefore"], collision["targetAfter"])
        self.assertEqual(
            {"target-write", "idea-write", "validation", "staging", "commit"},
            {
                failure["boundary"]
                for failure in transaction["injectedFailures"]
            },
        )
        for failure in transaction["injectedFailures"]:
            with self.subTest(boundary=failure["boundary"]):
                self.assertEqual(failure["ideaBefore"], failure["ideaAfter"])
                if failure["targetExistedBefore"]:
                    self.assertEqual(failure["targetBefore"], failure["targetAfter"])
                else:
                    self.assertEqual("absent", failure["targetAfter"])
                self.assertEqual(
                    "remove only a target created by this attempt",
                    failure["cleanupScope"],
                )

        self.assertEqual(
            "exact full file bytes and existence",
            git_index["preAttemptSnapshot"],
        )
        self.assertEqual(
            [fixture["ideaPath"], fixture["promotedWorkItemPath"]],
            git_index["stagedPaths"],
        )
        self.assertEqual("path-limited", git_index["commitMode"])
        self.assertTrue(git_index["preserveUnrelatedStagedState"])
        self.assertEqual(
            [fixture["ideaPath"], fixture["promotedWorkItemPath"]],
            git_index["verifiedCommitPaths"],
        )
        self.assertEqual(
            "captured immutable commit OID",
            git_index["verifiedCommitReference"],
        )
        self.assertEqual(
            "restore exact bytes and existence then verify",
            git_index["failureRestoration"],
        )
        self.assertEqual("BLOCKED", git_index["rollbackFailure"]["status"])
        self.assertEqual(
            "Dev Backlog Steward",
            git_index["rollbackFailure"]["recoveryOwner"],
        )
        coordination = transaction["resourceCoordination"]
        expected_paths = [fixture["ideaPath"], fixture["promotedWorkItemPath"]]
        self.assertEqual(
            expected_paths,
            coordination["resource-claim"]["claimPaths"],
        )
        self.assertEqual(
            [
                "acquire both exact paths together in one operation before mutation",
                "revalidate transaction snapshots after claims",
                "release after success or safe verified rollback",
                "retain after unsafe rollback or postcommit verification failure",
            ],
            coordination["resource-claim"]["claimLifecycle"],
        )
        self.assertEqual([], coordination["none"]["claimCalls"])
        self.assertEqual("absent", coordination["none"]["claimEvidence"])
        for behavior in (
            "Preflight target collisions before any promotion write",
            "Snapshot exact idea bytes target bytes and target existence",
            "Restore exact pre-attempt state after target-write idea-write validation staging or commit failure",
            "Snapshot exact full Git index file bytes and existence before mutation",
            "Revalidate source destination HEAD index and unrelated state immediately before mutation",
            "Return zero-mutation BLOCKED on pre-mutation drift",
            "Set Promoted To to the destination Work Item ID",
            "Set destination Work Item ID to its filename stem",
            "Add reciprocal Source Evidence with the exact idea path",
            "Stage and path-limit commit to exactly the idea and target while preserving unrelated staged state",
            "Capture the new commit OID and verify that exact object contains exactly the reciprocal idea and target pair",
            "Restore and verify exact pre-attempt index bytes and existence on failure",
        ):
            with self.subTest(required_behavior=behavior):
                self.assertIn(behavior, scenario["requiredBehaviors"])
        common_behavior_text = "\n".join(scenario["requiredBehaviors"]).casefold()
        for claim_only_fragment in (
            "acquire exact source and destination path claims",
            "claim conflict",
            "after claims",
            "post-claim drift",
        ):
            with self.subTest(claim_only_fragment=claim_only_fragment):
                self.assertNotIn(claim_only_fragment, common_behavior_text)
        scenario_coordination = scenario["resourceCoordinationCases"]
        resource_claim = scenario_coordination["resource-claim"]
        none = scenario_coordination["none"]
        self.assertEqual(["resource-claim"], resource_claim["targetSkills"])
        self.assertEqual(["claim-lifecycle"], resource_claim["deterministicChecks"])
        self.assertTrue(resource_claim["claimCalls"])
        self.assertEqual("required", resource_claim["claimEvidence"])
        self.assertIn(
            "Retain ownership after unsafe rollback or postcommit verification failure",
            resource_claim["claimLifecycle"],
        )
        self.assertIn(
            "Release after success or safe verified rollback",
            resource_claim["claimLifecycle"],
        )
        self.assertIn(
            "Acquire both exact paths together in one operation before promotion mutation",
            resource_claim["claimLifecycle"],
        )
        self.assertIn(
            "Stop with no retained new ownership on any path conflict",
            resource_claim["claimLifecycle"],
        )
        self.assertIn(
            "Revalidate transaction snapshots after claims",
            resource_claim["claimLifecycle"],
        )
        self.assertEqual([], none["targetSkills"])
        self.assertEqual([], none["deterministicChecks"])
        self.assertEqual([], none["claimCalls"])
        self.assertEqual([], none["registryMutations"])
        self.assertEqual([], none["journalWrites"])
        self.assertEqual([], none["claimReleases"])
        self.assertEqual("absent", none["claimEvidence"])
        self.assertEqual(resource_claim["providerLifecycle"], none["providerLifecycle"])
        self.assertIn("transaction as failure-atomic", contract_text)
        self.assertIn(
            "target-write, idea-write, validation, staging, or commit",
            contract_text,
        )
        self.assertIn("exact full Git index file", contract_text)
        self.assertIn("path-limited commit", contract_text)
        self.assertIn("captured immutable commit OID", contract_text)
        self.assertIn("one atomic acquire", contract_text)
        self.assertIn("Promoted To to equal the destination Work Item ID", contract_text)
        self.assertIn("Work Item ID to equal the destination filename stem", contract_text)
        self.assertIn("A conflict on either path acquires nothing", contract_text)
        self.assertIn("return zero-mutation BLOCKED on drift", contract_text)
        self.assertIn("peer commit-file-provider-transaction skill", contract_text)
        self.assertIn(
            "When resource_coordination selects resource-claim", contract_text
        )
        self.assertIn(
            "When resource_coordination selects none", contract_text
        )
        supervisor_text = (SUITE_ROOT / "agents" / "supervisor.toml").read_text(
            encoding="utf-8"
        )
        judge_text = (SUITE_ROOT / "agents" / "judge.toml").read_text(
            encoding="utf-8"
        )
        for expected_prompt_contract in (
            "one atomic source-and-destination promotion claim operation",
            "zero-mutation claim conflict and post-claim drift handling",
            "peer-transaction recovery evidence",
        ):
            self.assertIn(expected_prompt_contract, supervisor_text)
        for expected_prompt_contract in (
            "observable reads of canonical regular files",
            "one atomic acquire operation containing both exact paths",
            "Do not require the Steward role itself to own transaction rollback mechanics",
        ):
            self.assertIn(expected_prompt_contract, judge_text)
        self.assertNotIn(
            "commit-file-provider-transaction",
            yaml.safe_dump(role, sort_keys=False),
        )
        self.assertTrue(
            any(
                "Unsafe Future Ideas recovery is BLOCKED" in step
                for step in role["instructions"]["completion"]
            )
        )

    def test_each_precommit_failure_boundary_executes_and_restores_real_state(
        self,
    ) -> None:
        """Target, source, validation, staging, and commit failures restore snapshots."""
        fixture = yaml.safe_load(
            (SUITE_ROOT / "fixtures" / "cases.yaml").read_text(encoding="utf-8")
        )["cases"]["future-ideas-capture-and-promotion"]["promotionTransaction"]
        boundaries = [failure["boundary"] for failure in fixture["injectedFailures"]]
        self.assertEqual(
            ["target-write", "idea-write", "validation", "staging", "commit"],
            boundaries,
        )

        for boundary in boundaries:
            with self.subTest(boundary=boundary):
                temporary, repository, idea, target, unrelated, index_path = (
                    self._promotion_repository()
                )
                self.addCleanup(temporary.cleanup)
                registry = _FakeClaimRegistry()
                idea_before = idea.read_bytes()
                index_before = index_path.read_bytes()
                unrelated_before = unrelated.read_bytes()
                unrelated_staged_before = self._git(
                    repository, "show", ":unrelated.txt"
                ).stdout
                head_before = self._git(
                    repository, "rev-parse", "HEAD"
                ).stdout.strip()

                result = _execute_promotion_transaction(
                    repository,
                    idea,
                    target,
                    _PROMOTED_IDEA_BYTES,
                    _PROMOTED_ITEM_BYTES,
                    resource_coordination="resource-claim",
                    claim_registry=registry,
                    fail_boundary=boundary,
                )

                self.assertEqual("BLOCKED", result["status"])
                self.assertEqual(boundary, result["failureBoundary"])
                self.assertTrue(result["rollbackVerified"])
                self.assertTrue(result["indexVerified"])
                self.assertTrue(result["unrelatedStateVerified"])
                self.assertEqual(_RELEASED_PROMOTION_CLAIMS, result["claimCalls"])
                self.assertFalse(registry.active)
                self.assertEqual(idea_before, idea.read_bytes())
                self.assertFalse(target.exists())
                self.assertEqual(unrelated_before, unrelated.read_bytes())
                self.assertEqual(index_before, index_path.read_bytes())
                self.assertEqual(
                    unrelated_staged_before,
                    self._git(repository, "show", ":unrelated.txt").stdout,
                )
                self.assertEqual(
                    head_before,
                    self._git(repository, "rev-parse", "HEAD").stdout.strip(),
                )

    def test_failed_promotion_commit_restores_worktree_and_exact_index(self) -> None:
        """A failed path-limited commit restores bytes and unrelated staged state."""
        temporary, repository, idea, target, _, index_path = (
            self._promotion_repository()
        )
        self.addCleanup(temporary.cleanup)
        idea_before = idea.read_bytes()
        index_before = index_path.read_bytes()
        registry = _FakeClaimRegistry()

        result = _execute_promotion_transaction(
            repository,
            idea,
            target,
            _PROMOTED_IDEA_BYTES,
            _PROMOTED_ITEM_BYTES,
            resource_coordination="resource-claim",
            claim_registry=registry,
            fail_commit=True,
        )

        self.assertEqual("BLOCKED", result["status"])
        self.assertTrue(result["rollbackVerified"])
        self.assertFalse(result["claimRetained"])
        self.assertEqual(_RELEASED_PROMOTION_CLAIMS, result["claimCalls"])
        self.assertFalse(registry.active)
        self.assertEqual(idea_before, idea.read_bytes())
        self.assertFalse(target.exists())
        self.assertEqual(index_before, index_path.read_bytes())
        self.assertEqual(
            "unrelated.txt",
            self._git(
                repository, "diff", "--cached", "--name-only"
            ).stdout.strip(),
        )

    def test_successful_promotion_commits_only_pair_and_preserves_staged_state(
        self,
    ) -> None:
        """A successful path-limited commit contains only reciprocal records."""
        temporary, repository, idea, target, _, _ = self._promotion_repository()
        self.addCleanup(temporary.cleanup)
        registry = _FakeClaimRegistry()
        head_before = self._git(repository, "rev-parse", "HEAD").stdout.strip()
        unrelated_staged_before = self._git(
            repository, "diff", "--cached", "--", "unrelated.txt"
        ).stdout

        result = _execute_promotion_transaction(
            repository,
            idea,
            target,
            _PROMOTED_IDEA_BYTES,
            _PROMOTED_ITEM_BYTES,
            resource_coordination="resource-claim",
            claim_registry=registry,
        )

        self.assertEqual("READY", result["status"])
        self.assertTrue(result["commitVerified"])
        self.assertTrue(result["indexVerified"])
        self.assertTrue(result["unrelatedStateVerified"])
        self.assertEqual(head_before, result["capturedHead"])
        self.assertEqual(head_before, result["commitParent"])
        self.assertEqual(_RELEASED_PROMOTION_CLAIMS, result["claimCalls"])
        self.assertFalse(registry.active)
        commit_oid = str(result["commitOid"])
        self.assertEqual(
            {
                "backlog/future-ideas/retry-dashboard.md",
                "backlog/feature-backlog/retry-dashboard.md",
            },
            set(
                self._git(
                    repository,
                    "diff-tree",
                    "--no-commit-id",
                    "--name-only",
                    "-r",
                    commit_oid,
                ).stdout.splitlines()
            ),
        )
        self.assertEqual(
            _PROMOTED_IDEA_BYTES,
            subprocess.run(
                ["git", "-C", str(repository), "show", f"{commit_oid}:{_IDEA_CLAIM_PATH}"],
                check=True,
                capture_output=True,
            ).stdout,
        )
        committed_item = subprocess.run(
            ["git", "-C", str(repository), "show", f"{commit_oid}:{_TARGET_CLAIM_PATH}"],
            check=True,
            capture_output=True,
        ).stdout
        self.assertEqual(_PROMOTED_ITEM_BYTES, committed_item)
        self.assertIn(
            f"Work Item ID: {Path(_TARGET_CLAIM_PATH).stem}\n".encode("utf-8"),
            committed_item,
        )
        self.assertEqual(
            "unrelated.txt",
            self._git(
                repository, "diff", "--cached", "--name-only"
            ).stdout.strip(),
        )
        self.assertEqual(
            unrelated_staged_before,
            self._git(
                repository, "diff", "--cached", "--", "unrelated.txt"
            ).stdout,
        )

    def test_success_and_safe_rollback_preserve_dirty_bytes_modes_and_index(
        self,
    ) -> None:
        """Release follows exact verification of unrelated dirty and index state."""
        for failure_boundary in (None, "validation"):
            with self.subTest(failure_boundary=failure_boundary):
                temporary, repository, idea, target, _, index_path = (
                    self._promotion_repository()
                )
                self.addCleanup(temporary.cleanup)
                manifest = (
                    idea.relative_to(repository).as_posix(),
                    target.relative_to(repository).as_posix(),
                )
                unrelated_before = _unrelated_worktree_state(repository, manifest)
                self.assertEqual(0o640, unrelated_before["unrelated.txt"][1])
                self.assertEqual(0o744, unrelated_before["tracked-dirty.txt"][1])
                self.assertEqual(0o600, unrelated_before["untracked-dirty.txt"][1])
                index_before = index_path.read_bytes()
                index_entries_before = _index_entries(repository)
                registry = _FakeClaimRegistry()

                result = _execute_promotion_transaction(
                    repository,
                    idea,
                    target,
                    _PROMOTED_IDEA_BYTES,
                    _PROMOTED_ITEM_BYTES,
                    resource_coordination="resource-claim",
                    claim_registry=registry,
                    fail_boundary=failure_boundary,
                )

                self.assertTrue(result["indexVerified"])
                self.assertTrue(result["unrelatedStateVerified"])
                self.assertEqual(
                    unrelated_before,
                    _unrelated_worktree_state(repository, manifest),
                )
                self.assertEqual(_RELEASED_PROMOTION_CLAIMS, result["claimCalls"])
                self.assertFalse(registry.active)
                if failure_boundary is None:
                    index_entries_after = _index_entries(repository)
                    self.assertEqual(
                        {
                            path: entry
                            for path, entry in index_entries_before.items()
                            if path not in manifest
                        },
                        {
                            path: entry
                            for path, entry in index_entries_after.items()
                            if path not in manifest
                        },
                    )
                else:
                    self.assertEqual(index_before, index_path.read_bytes())
                    self.assertEqual(index_entries_before, _index_entries(repository))

    def test_post_claim_transaction_drift_stops_before_every_promotion_mutation(
        self,
    ) -> None:
        """Real repository drift after both claims returns zero-mutation BLOCKED."""
        fixture = yaml.safe_load(
            (SUITE_ROOT / "fixtures" / "cases.yaml").read_text(encoding="utf-8")
        )["cases"]["future-ideas-capture-and-promotion"]["promotionTransaction"]
        expected_markers = {
            "source-bytes": "source",
            "source-type-and-authority": "source",
            "destination-appears": "destination",
            "head": "HEAD",
            "index": "index",
            "unrelated-worktree": "unrelated worktree or staged state",
        }
        self.assertEqual(
            set(expected_markers), set(fixture["postClaimDrift"]["injectedKinds"])
        )

        for drift_kind, expected_marker in expected_markers.items():
            with self.subTest(drift_kind=drift_kind):
                temporary, repository, idea, target, _, _ = (
                    self._promotion_repository()
                )
                self.addCleanup(temporary.cleanup)
                registry = _FakeClaimRegistry()
                commit_count_before = int(
                    self._git(repository, "rev-list", "--count", "HEAD").stdout
                )
                external = repository.parent / f"{repository.name}-external.md"

                def inject_drift() -> None:
                    """Apply one independently owned change after both path claims."""
                    if drift_kind == "source-bytes":
                        idea.write_bytes(idea.read_bytes() + b"post-claim drift\n")
                    elif drift_kind == "source-type-and-authority":
                        external.write_bytes(b"external bytes must remain external\n")
                        idea.unlink()
                        idea.symlink_to(external)
                    elif drift_kind == "destination-appears":
                        target.write_bytes(b"external collision\n")
                    elif drift_kind == "head":
                        self._git(repository, "commit", "--quiet", "-m", "Claim drift")
                    elif drift_kind == "index":
                        drift_path = repository / "claim-drift.txt"
                        drift_path.write_bytes(b"index drift\n")
                        self._git(repository, "add", "--", drift_path.name)
                    elif drift_kind == "unrelated-worktree":
                        (repository / "claim-drift.txt").write_bytes(
                            b"untracked drift\n"
                        )
                    else:  # pragma: no cover - fixture and mapping are asserted above.
                        raise AssertionError(f"unsupported drift kind: {drift_kind}")

                result = _execute_promotion_transaction(
                    repository,
                    idea,
                    target,
                    _PROMOTED_IDEA_BYTES,
                    _PROMOTED_ITEM_BYTES,
                    resource_coordination="resource-claim",
                    claim_registry=registry,
                    after_claims=inject_drift,
                )

                self.assertEqual("BLOCKED", result["status"])
                self.assertTrue(result["zeroMutation"])
                self.assertFalse(result["commitCreated"])
                self.assertIn(expected_marker, result["drift"])
                self.assertEqual(_RELEASED_PROMOTION_CLAIMS, result["claimCalls"])
                self.assertFalse(registry.active)
                expected_commit_count = commit_count_before + (
                    1 if drift_kind == "head" else 0
                )
                self.assertEqual(
                    expected_commit_count,
                    int(self._git(repository, "rev-list", "--count", "HEAD").stdout),
                )
                self.assertFalse(
                    (
                        repository
                        / ".git"
                        / "future-idea-promotion-recovery"
                        / "contract-attempt"
                    ).exists()
                )
                external.unlink(missing_ok=True)

    def test_destination_claim_conflict_acquires_nothing_and_mutates_nothing(
        self,
    ) -> None:
        """One atomic two-path claim conflict leaves repository and ownership unchanged."""
        fixture = yaml.safe_load(
            (SUITE_ROOT / "fixtures" / "cases.yaml").read_text(encoding="utf-8")
        )["cases"]["future-ideas-capture-and-promotion"]["promotionTransaction"]
        conflict = fixture["destinationClaimConflict"]
        temporary, repository, idea, target, unrelated, index_path = (
            self._promotion_repository()
        )
        self.addCleanup(temporary.cleanup)
        registry = _FakeClaimRegistry(
            conflicting_paths={conflict["conflictingPath"]}
        )
        idea_before = idea.read_bytes()
        unrelated_before = unrelated.read_bytes()
        index_before = index_path.read_bytes()
        head_before = self._git(repository, "rev-parse", "HEAD").stdout.strip()

        result = _execute_promotion_transaction(
            repository,
            idea,
            target,
            _PROMOTED_IDEA_BYTES,
            _PROMOTED_ITEM_BYTES,
            resource_coordination="resource-claim",
            claim_registry=registry,
        )

        self.assertEqual("BLOCKED", result["status"])
        self.assertTrue(result["zeroMutation"])
        self.assertFalse(result["commitCreated"])
        self.assertEqual(conflict["outcome"], result["claimOutcome"])
        self.assertEqual(
            (conflict["conflictingPath"],), result["conflictingPaths"]
        )
        self.assertEqual((_ATOMIC_PROMOTION_ACQUIRE,), result["claimCalls"])
        self.assertFalse(result["claimRetained"])
        self.assertFalse(registry.active)
        self.assertEqual(set(), registry.active_paths)
        self.assertEqual(idea_before, idea.read_bytes())
        self.assertFalse(target.exists())
        self.assertEqual(unrelated_before, unrelated.read_bytes())
        self.assertEqual(index_before, index_path.read_bytes())
        self.assertEqual(
            head_before, self._git(repository, "rev-parse", "HEAD").stdout.strip()
        )
        self.assertFalse(
            (repository / ".git" / "future-idea-promotion-recovery").exists()
        )

    def test_absent_destination_with_external_parent_stops_before_claims(
        self,
    ) -> None:
        """Preflight rejects an absent destination resolved outside authority."""
        temporary, repository, idea, target, _, index_path = (
            self._promotion_repository()
        )
        self.addCleanup(temporary.cleanup)
        external_temporary = tempfile.TemporaryDirectory()
        self.addCleanup(external_temporary.cleanup)
        external_root = Path(external_temporary.name)
        target.parent.rmdir()
        target.parent.symlink_to(external_root, target_is_directory=True)
        registry = _FakeClaimRegistry()
        idea_before = idea.read_bytes()
        index_before = index_path.read_bytes()
        head_before = self._git(repository, "rev-parse", "HEAD").stdout.strip()

        result = _execute_promotion_transaction(
            repository,
            idea,
            target,
            _PROMOTED_IDEA_BYTES,
            _PROMOTED_ITEM_BYTES,
            resource_coordination="resource-claim",
            claim_registry=registry,
        )

        self.assertEqual("BLOCKED", result["status"])
        self.assertTrue(result["zeroMutation"])
        self.assertFalse(result["commitCreated"])
        self.assertEqual("invalid destination authority", result["reason"])
        self.assertEqual((), result["claimCalls"])
        self.assertFalse(result["claimRetained"])
        self.assertFalse(registry.active)
        self.assertEqual(idea_before, idea.read_bytes())
        self.assertFalse(target.exists())
        self.assertFalse((external_root / target.name).exists())
        self.assertEqual(index_before, index_path.read_bytes())
        self.assertEqual(
            head_before, self._git(repository, "rev-parse", "HEAD").stdout.strip()
        )

    def test_post_claim_destination_authority_escape_releases_claims(
        self,
    ) -> None:
        """Post-claim authority escape stops before mutation and releases the pair."""
        temporary, repository, idea, target, _, index_path = (
            self._promotion_repository()
        )
        self.addCleanup(temporary.cleanup)
        external_temporary = tempfile.TemporaryDirectory()
        self.addCleanup(external_temporary.cleanup)
        external_root = Path(external_temporary.name)
        registry = _FakeClaimRegistry()
        idea_before = idea.read_bytes()
        index_before = index_path.read_bytes()
        head_before = self._git(repository, "rev-parse", "HEAD").stdout.strip()

        def escape_destination_authority() -> None:
            """Replace the empty governed parent with an external directory link."""
            target.parent.rmdir()
            target.parent.symlink_to(external_root, target_is_directory=True)

        result = _execute_promotion_transaction(
            repository,
            idea,
            target,
            _PROMOTED_IDEA_BYTES,
            _PROMOTED_ITEM_BYTES,
            resource_coordination="resource-claim",
            claim_registry=registry,
            after_claims=escape_destination_authority,
        )

        self.assertEqual("BLOCKED", result["status"])
        self.assertTrue(result["zeroMutation"])
        self.assertFalse(result["commitCreated"])
        self.assertIn("destination authority", result["drift"])
        self.assertEqual(_RELEASED_PROMOTION_CLAIMS, result["claimCalls"])
        self.assertFalse(result["claimRetained"])
        self.assertFalse(registry.active)
        self.assertEqual(idea_before, idea.read_bytes())
        self.assertFalse(target.exists())
        self.assertFalse((external_root / target.name).exists())
        self.assertEqual(index_before, index_path.read_bytes())
        self.assertEqual(
            head_before, self._git(repository, "rev-parse", "HEAD").stdout.strip()
        )
        self.assertFalse(
            (repository / ".git" / "future-idea-promotion-recovery").exists()
        )

    def test_promotion_rollback_failure_retains_claim_and_recovery_evidence(
        self,
    ) -> None:
        """Rollback failure returns truthful BLOCKED ownership and durable evidence."""
        temporary, repository, idea, target, _, index_path = (
            self._promotion_repository()
        )
        self.addCleanup(temporary.cleanup)
        idea_before = idea.read_bytes()
        index_before = index_path.read_bytes()
        unrelated_staged_before = self._git(
            repository, "show", ":unrelated.txt"
        ).stdout
        registry = _FakeClaimRegistry()

        result = _execute_promotion_transaction(
            repository,
            idea,
            target,
            _PROMOTED_IDEA_BYTES,
            _PROMOTED_ITEM_BYTES,
            resource_coordination="resource-claim",
            claim_registry=registry,
            fail_boundary="rollback-verification",
        )

        evidence = Path(str(result["preservedEvidence"]))
        self.assertEqual("BLOCKED", result["status"])
        self.assertEqual("rollback-verification", result["failureBoundary"])
        self.assertFalse(result["rollbackVerified"])
        self.assertTrue(result["claimRetained"])
        self.assertEqual(_RETAINED_PROMOTION_CLAIMS, result["claimCalls"])
        self.assertTrue(registry.active)
        self.assertEqual("Dev Backlog Steward", result["recoveryOwner"])
        self.assertEqual(idea_before, (evidence / "idea.bin").read_bytes())
        self.assertEqual(index_before, (evidence / "index.bin").read_bytes())
        self.assertEqual(b"absent\n", (evidence / "target-state").read_bytes())
        self.assertEqual(
            unrelated_staged_before,
            self._git(repository, "show", ":unrelated.txt").stdout,
        )

    def test_promotion_staging_failure_restores_and_releases_safe_claim(
        self,
    ) -> None:
        """A staging failure restores exact state before releasing enabled ownership."""
        temporary, repository, idea, target, _, index_path = (
            self._promotion_repository()
        )
        self.addCleanup(temporary.cleanup)
        idea_before = idea.read_bytes()
        index_before = index_path.read_bytes()
        unrelated_staged_before = self._git(
            repository, "show", ":unrelated.txt"
        ).stdout
        registry = _FakeClaimRegistry()

        result = _execute_promotion_transaction(
            repository,
            idea,
            target,
            _PROMOTED_IDEA_BYTES,
            _PROMOTED_ITEM_BYTES,
            resource_coordination="resource-claim",
            claim_registry=registry,
            fail_staging=True,
        )

        self.assertEqual("BLOCKED", result["status"])
        self.assertTrue(result["rollbackVerified"])
        self.assertEqual(_RELEASED_PROMOTION_CLAIMS, result["claimCalls"])
        self.assertFalse(registry.active)
        self.assertEqual(idea_before, idea.read_bytes())
        self.assertFalse(target.exists())
        self.assertEqual(index_before, index_path.read_bytes())
        self.assertEqual(
            unrelated_staged_before,
            self._git(repository, "show", ":unrelated.txt").stdout,
        )

    def test_postcommit_verification_failure_retains_claim_and_exact_oid(
        self,
    ) -> None:
        """A reciprocal verification failure preserves its exact commit and ownership."""
        temporary, repository, idea, target, _, _ = self._promotion_repository()
        self.addCleanup(temporary.cleanup)
        unrelated_staged_before = self._git(
            repository, "show", ":unrelated.txt"
        ).stdout
        registry = _FakeClaimRegistry()

        result = _execute_promotion_transaction(
            repository,
            idea,
            target,
            _PROMOTED_IDEA_BYTES,
            _PROMOTED_ITEM_BYTES,
            resource_coordination="resource-claim",
            claim_registry=registry,
            fail_boundary="post-commit-verification",
        )

        self.assertEqual("BLOCKED", result["status"])
        self.assertEqual("post-commit-verification", result["failureBoundary"])
        self.assertFalse(result["rollbackVerified"])
        self.assertEqual(_RETAINED_PROMOTION_CLAIMS, result["claimCalls"])
        self.assertTrue(registry.active)
        self.assertEqual(
            str(result["commitOid"]),
            self._git(repository, "rev-parse", "HEAD").stdout.strip(),
        )
        self.assertEqual(
            unrelated_staged_before,
            self._git(repository, "show", ":unrelated.txt").stdout,
        )

    def test_promotion_verifies_captured_commit_oid_after_head_moves(self) -> None:
        """Commit verification remains bound to the captured object when HEAD moves."""
        temporary, repository, idea, target, _, _ = self._promotion_repository()
        self.addCleanup(temporary.cleanup)
        registry = _FakeClaimRegistry()
        head_before = self._git(repository, "rev-parse", "HEAD").stdout.strip()

        def move_head(commit_oid: str) -> None:
            tree_oid = self._git(repository, "rev-parse", f"{commit_oid}^{{tree}}")
            moved_oid = subprocess.run(
                [
                    "git",
                    "-C",
                    str(repository),
                    "commit-tree",
                    tree_oid.stdout.strip(),
                    "-p",
                    commit_oid,
                ],
                check=True,
                capture_output=True,
                text=True,
                input="Move mutable HEAD\n",
            ).stdout.strip()
            self._git(repository, "update-ref", "HEAD", moved_oid, commit_oid)

        result = _execute_promotion_transaction(
            repository,
            idea,
            target,
            _PROMOTED_IDEA_BYTES,
            _PROMOTED_ITEM_BYTES,
            resource_coordination="resource-claim",
            claim_registry=registry,
            after_commit=move_head,
        )

        self.assertEqual("READY", result["status"])
        self.assertEqual(head_before, result["capturedHead"])
        self.assertEqual(head_before, result["commitParent"])
        self.assertEqual(
            head_before,
            self._git(
                repository, "rev-parse", f"{result['commitOid']}^"
            ).stdout.strip(),
        )
        self.assertNotEqual(
            str(result["commitOid"]),
            self._git(repository, "rev-parse", "HEAD").stdout.strip(),
        )
        self.assertTrue(result["indexVerified"])
        self.assertTrue(result["unrelatedStateVerified"])
        self.assertEqual(_RELEASED_PROMOTION_CLAIMS, result["claimCalls"])

    def test_none_coordination_uses_no_claim_calls_or_evidence(self) -> None:
        """Coordination none preserves success and failure semantics without claims."""
        for fail_staging, expected_status in ((False, "READY"), (True, "BLOCKED")):
            with self.subTest(fail_staging=fail_staging):
                temporary, repository, idea, target, _, index_path = (
                    self._promotion_repository()
                )
                self.addCleanup(temporary.cleanup)
                idea_before = idea.read_bytes()
                index_before = index_path.read_bytes()
                unrelated_staged_before = self._git(
                    repository, "show", ":unrelated.txt"
                ).stdout
                registry = _FakeClaimRegistry()

                result = _execute_promotion_transaction(
                    repository,
                    idea,
                    target,
                    _PROMOTED_IDEA_BYTES,
                    _PROMOTED_ITEM_BYTES,
                    resource_coordination="none",
                    claim_registry=registry,
                    fail_staging=fail_staging,
                )

                self.assertEqual(expected_status, result["status"])
                self.assertEqual([], registry.calls)
                self.assertFalse(registry.active)
                self.assertNotIn("claimCalls", result)
                self.assertNotIn("claimRetained", result)
                self.assertEqual(
                    unrelated_staged_before,
                    self._git(repository, "show", ":unrelated.txt").stdout,
                )
                if fail_staging:
                    self.assertTrue(result["rollbackVerified"])
                    self.assertEqual(idea_before, idea.read_bytes())
                    self.assertFalse(target.exists())
                    self.assertEqual(index_before, index_path.read_bytes())
                else:
                    self.assertTrue(result["commitVerified"])

    def test_blocked_resumption_has_negative_and_positive_scenarios(self) -> None:
        """The suite keeps provider outcomes neutral and claim behavior conditional."""
        scenarios = yaml.safe_load(
            (SUITE_ROOT / "scenarios.yaml").read_text(encoding="utf-8")
        )["scenarios"]
        by_id = {scenario["id"]: scenario for scenario in scenarios}

        shortcut = by_id["blocked-unowned-running-shortcut"]
        self.assertEqual("BLOCKED", shortcut["expectedTerminalStatus"])
        self.assertIn("Leave the backlog item unchanged", shortcut["requiredBehaviors"])
        self.assertIn(
            "Reject because no provider owner exists",
            shortcut["requiredBehaviors"],
        )
        self.assertTrue(
            shortcut["resourceCoordinationCases"]["resource-claim"]["claimCalls"]
        )
        self.assertEqual(
            [],
            shortcut["resourceCoordinationCases"]["none"]["claimCalls"],
        )

        resumption = by_id["blocked-claimed-resumption"]
        self.assertEqual("PASS", resumption["expectedTerminalStatus"])
        self.assertIn(
            "Record Ready then a new provider owner before Running",
            resumption["requiredBehaviors"],
        )
        self.assertTrue(
            resumption["resourceCoordinationCases"]["resource-claim"]["claimCalls"]
        )

        failed_claim = by_id["blocked-failed-claim-resumption"]
        self.assertEqual("BLOCKED", failed_claim["expectedTerminalStatus"])
        self.assertIn(
            "CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED",
            failed_claim["resourceCoordinationCases"]["resource-claim"][
                "claimLifecycle"
            ][1],
        )
        self.assertEqual(
            [],
            failed_claim["resourceCoordinationCases"]["none"]["claimCalls"],
        )
        self.assertIn("project-hash-policy", failed_claim["deterministicChecks"])

    def test_failed_or_missing_claim_leaves_the_item_unchanged(self) -> None:
        """Missing and conflict-wait claim outcomes keep exact blocked bytes and evidence."""
        cases = yaml.safe_load(
            (SUITE_ROOT / "fixtures" / "cases.yaml").read_text(encoding="utf-8")
        )["cases"]

        expected_transitions = {
            "blocked-unowned-running-shortcut": ("blocked", "rejected-unowned"),
            "blocked-failed-claim-resumption": (
                "blocked",
                "ready",
                "claim-failed",
                "blocked",
            ),
        }
        for case_id, transitions_expected in expected_transitions.items():
            fixture = cases[case_id]
            before = fixture["itemBefore"].encode("utf-8")
            claim_outcomes = [fixture["claimOutcome"]]
            claim_outcomes.extend(fixture.get("otherFailedClaimOutcomes", []))
            for claim_outcome in claim_outcomes:
                after, transitions = contract_harness.attempt_resumption(
                    before,
                    unblock_condition_satisfied=fixture["unblockConditionSatisfied"],
                    claim_outcome=claim_outcome,
                )

                with self.subTest(case_id=case_id, claim_outcome=claim_outcome):
                    self.assertEqual(before, after)
                    self.assertEqual(transitions_expected, transitions)
                    self.assertIn(b"Status: Blocked", after)
                    self.assertIn(b"Owner: Unowned", after)
                    self.assertIn(b"Claim: None", after)
                    self.assertNotIn(b"Status: Running", after)

    def test_successful_claim_resumes_in_order_and_preserves_evidence(self) -> None:
        """A new claim and owner precede Running without rewriting prior evidence."""
        fixture = yaml.safe_load(
            (SUITE_ROOT / "fixtures" / "cases.yaml").read_text(encoding="utf-8")
        )["cases"]["blocked-claimed-resumption"]
        before = fixture["itemBefore"].encode("utf-8")

        after, transitions = contract_harness.attempt_resumption(
            before,
            unblock_condition_satisfied=fixture["unblockConditionSatisfied"],
            claim_outcome=fixture["claimOutcome"],
            new_owner=fixture["newOwner"],
            new_claim=fixture["newClaim"],
        )

        self.assertEqual(("blocked", "ready", "claimed", "running"), transitions)
        self.assertLess(transitions.index("ready"), transitions.index("claimed"))
        self.assertLess(transitions.index("claimed"), transitions.index("running"))
        expected = before.replace(b"Status: Blocked", b"Status: Running", 1)
        expected = expected.replace(b"Owner: Unowned", b"Owner: dev-coder", 1)
        expected = expected.replace(
            b"Claim: None", b"Claim: schema-migration-resumption", 1
        )
        self.assertEqual(expected, after)
        for preserved_line in (
            b"Blocker: External schema decision is unavailable.",
            b"Unblock Condition: Approved schema decision is recorded.",
            b"Evidence: Existing schema analysis and verification log.",
            (
                b"Acceptance Criteria: Schema decision remains traceable; "
                b"existing verification remains required."
            ),
        ):
            with self.subTest(preserved_line=preserved_line):
                self.assertIn(preserved_line, after)


if __name__ == "__main__":
    unittest.main()
