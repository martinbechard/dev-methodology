#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Implements the claim command-line interface and helper for registry, journal, deadline, recovery, and release operations.

from __future__ import annotations

import argparse
import base64
import binascii
import fcntl
import gzip
import hashlib
import json
import math
import os
import re
import stat
import subprocess
from collections import Counter
from contextlib import contextmanager
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from statistics import median
from typing import Any, Iterator, Sequence
from uuid import uuid4

import yaml


SUCCESS = 0
ERROR = 1
COORDINATION_REQUIRED_EXIT_CODE = 3
ISOLATION_SETUP_EXIT_CODE = 4
RECOVERY_AUTHORIZATION_EXIT_CODE = 5
BACKLOG_ROOT_DIRECTORY = "backlog"
WORKTREE_ROOT_DIRECTORY = ".worktrees"
WORKTREE_IGNORE_PATTERN = "/.worktrees/"
ISOLATED_SPARSE_CHECKOUT_PATTERNS = ("/*", "!/backlog/")
REGISTRY_FILE_NAME = "agent-claims.json"
LOCK_FILE_NAME = "agent-claims.lock"
RECONCILIATION_PENDING_FILE_NAME = "agent-claim-reconciliation-pending.json"
EVENT_DIRECTORY_NAME = "agent-claim-events"
EVENT_SCHEMA_VERSION = 1
RESULT_SCHEMA_VERSION = 2
SUMMARY_SCHEMA_VERSION = 2
REPORT_SCHEMA_VERSION = 2
DEFAULT_HOT_DAYS = 2
MAX_SCOPE_REASON_LENGTH = 200
MAX_IDENTIFIER_LENGTH = 200
MAX_EXTENSION_EVIDENCE_LENGTH = 1000
_RESOURCE_DEADLINE_CLASS_IDS = (
    "backlog-mutation",
    "main-integration",
    "browser-server",
    "database-port",
    "live-model-evaluation",
)
STALE_HEARTBEAT_HOURS = 24
UTC_DAY_PATTERN = re.compile(r"^(\d{4}-\d{2}-\d{2})\.jsonl$")
SINCE_PATTERN = re.compile(r"^(\d+)([dh])$")
FULL_COMMIT_SHA_PATTERN = re.compile(r"^[0-9a-fA-F]{40}$")
WORKTREE_COMPONENT_PATTERN = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9._-]{0,198}[A-Za-z0-9_-])?$")
LEGACY_OUTCOME_ALIASES = {
    "PRIMARY": "SHARED_CHECKOUT_ACQUIRED",
    "ISOLATE": "ISOLATED_CHECKOUT_ACQUIRED",
    "RECOVER": "DIRTY_CHECKOUT_RECOVERY_ACQUIRED",
    "WAIT": "CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED",
    "PRIMARY_REQUIRED": "SHARED_CHECKOUT_REQUIRED",
    "ISOLATE_REQUIRED": "ISOLATED_CHECKOUT_SETUP_REQUIRED",
    "RECOVERY_REQUIRED": "DIRTY_CHECKOUT_RECOVERY_AUTHORIZATION_REQUIRED",
}


class _ScopeError(ValueError):
    def __init__(
        self,
        message: str,
        offending_scope: str,
        replacement: str,
        reason: str = "invalid_scope",
    ) -> None:
        super().__init__(message)
        self.offending_scope = offending_scope
        self.replacement = replacement
        self.reason = reason


class _DeadlineError(ValueError):
    def __init__(self, message: str, field: str, reason: str) -> None:
        super().__init__(message)
        self.field = field
        self.reason = reason


class _ReleaseReconciliationError(ValueError):
    def __init__(self, message: str, reason: str, **details: Any) -> None:
        super().__init__(message)
        self.reason = reason
        self.details = details


class _PendingReconciliationError(RuntimeError):
    def __init__(self, message: str, claim_id: str, marker_path: Path) -> None:
        super().__init__(message)
        self.claim_id = claim_id
        self.marker_path = marker_path


def _git(worktree: Path, *arguments: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(worktree), *arguments],
        check=check,
        text=True,
        capture_output=True,
    )


def _repository_root(path: Path) -> Path:
    return Path(_git(path, "rev-parse", "--show-toplevel").stdout.strip()).resolve()


def _git_common_directory(repository: Path) -> Path:
    raw_path = Path(_git(repository, "rev-parse", "--git-common-dir").stdout.strip())
    if not raw_path.is_absolute():
        raw_path = repository / raw_path
    return raw_path.resolve()


def _primary_worktree(repository: Path) -> Path:
    fields = _git(repository, "worktree", "list", "--porcelain", "-z").stdout.split("\0")
    for field in fields:
        if field.startswith("worktree "):
            return Path(field.removeprefix("worktree ")).resolve()
    raise RuntimeError("Git did not report a primary worktree.")


def _canonical_worktree_root(repository: Path) -> Path:
    return (_primary_worktree(repository) / WORKTREE_ROOT_DIRECTORY).resolve()


def _canonical_worktree(repository: Path, claim_id: str) -> Path:
    return (_canonical_worktree_root(repository) / claim_id).resolve()


def _checkout_topology(claim: dict[str, Any]) -> str | None:
    topology = claim.get("checkout_topology")
    if topology in {"primary", "linked"}:
        return str(topology)
    worktree = claim.get("worktree")
    if isinstance(worktree, str):
        worktree_path = Path(worktree).resolve()
        try:
            return "primary" if worktree_path == _primary_worktree(worktree_path) else "linked"
        except (OSError, RuntimeError, subprocess.CalledProcessError):
            pass
    mode = claim.get("mode")
    if mode == "isolated":
        return "linked"
    if mode in {"primary", "recovery"}:
        return "primary"
    return None


def _worktree_root_is_ignored(repository: Path) -> bool:
    primary_worktree = _primary_worktree(repository)
    probe = f"{WORKTREE_ROOT_DIRECTORY}/.agent-claim-ignore-probe"
    ignored = _git(
        primary_worktree,
        "check-ignore",
        "--quiet",
        "--no-index",
        "--",
        probe,
        check=False,
    )
    return ignored.returncode == SUCCESS


def _claim_id_is_safe_worktree_component(claim_id: str) -> bool:
    return bool(WORKTREE_COMPONENT_PATTERN.fullmatch(claim_id))


def _registry_paths(repository: Path) -> tuple[Path, Path]:
    common_directory = _git_common_directory(repository)
    return common_directory / REGISTRY_FILE_NAME, common_directory / LOCK_FILE_NAME


def _journal_paths(common_directory: Path) -> tuple[Path, Path, Path, Path]:
    root = common_directory / EVENT_DIRECTORY_NAME
    return root, root / "hot", root / "archive", root / "journal"


def _fsync_directory(directory: Path) -> None:
    descriptor = os.open(directory, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _fault_enabled(faults: dict[str, str] | None, boundary: str) -> bool:
    environment_name = (faults or {}).get(boundary)
    return bool(environment_name and os.environ.get(environment_name) == "1")


def _durable_atomic_replace(
    path: Path,
    content: bytes,
    *,
    faults: dict[str, str] | None = None,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.{uuid4().hex}.tmp")
    target_mode = stat.S_IMODE(path.stat().st_mode) if path.exists() else 0o600
    descriptor: int | None = None
    replaced = False
    try:
        if _fault_enabled(faults, "write"):
            raise OSError("simulated durable replacement write failure")
        descriptor = os.open(
            temporary,
            os.O_CREAT | os.O_EXCL | os.O_WRONLY,
            0o600,
        )
        os.fchmod(descriptor, target_mode)
        offset = 0
        while offset < len(content):
            remaining = content[offset:]
            if _fault_enabled(faults, "short_write"):
                written = os.write(
                    descriptor,
                    remaining[: max(1, len(remaining) // 2)],
                )
                if written > 0:
                    offset += written
                raise OSError("simulated incomplete durable replacement write")
            written = os.write(descriptor, remaining)
            if written <= 0:
                raise OSError("durable replacement write made no progress")
            offset += written
        if _fault_enabled(faults, "after_write"):
            raise OSError("simulated failure after durable replacement write")
        if _fault_enabled(faults, "fsync"):
            raise OSError("simulated durable replacement file fsync failure")
        os.fsync(descriptor)
        os.close(descriptor)
        descriptor = None
        if _fault_enabled(faults, "replace"):
            raise OSError("simulated durable replacement rename failure")
        os.replace(temporary, path)
        replaced = True
        if _fault_enabled(faults, "directory_fsync"):
            raise OSError("simulated durable replacement directory fsync failure")
        _fsync_directory(path.parent)
    finally:
        if descriptor is not None:
            os.close(descriptor)
        if not replaced:
            temporary.unlink(missing_ok=True)


def _durable_remove(
    path: Path,
    *,
    fault_environment: str | None = None,
) -> None:
    if fault_environment and os.environ.get(fault_environment) == "1":
        raise OSError("simulated durable removal failure")
    if path.exists():
        path.unlink()
        _fsync_directory(path.parent)


def _pending_reconciliation_path(common_directory: Path) -> Path:
    return common_directory / RECONCILIATION_PENDING_FILE_NAME


def _encoded_snapshot(content: bytes, exists: bool = True) -> dict[str, Any]:
    return {
        "exists": exists,
        "sha256": hashlib.sha256(content).hexdigest(),
        "base64": base64.b64encode(content).decode("ascii"),
    }


def _decoded_snapshot(snapshot: dict[str, Any]) -> tuple[bool, bytes]:
    if not isinstance(snapshot, dict) or set(snapshot) != {
        "exists",
        "sha256",
        "base64",
    }:
        raise ValueError("Invalid reconciliation snapshot schema.")
    exists = snapshot.get("exists")
    encoded = snapshot.get("base64")
    digest = snapshot.get("sha256")
    if (
        not isinstance(exists, bool)
        or not isinstance(encoded, str)
        or not isinstance(digest, str)
    ):
        raise ValueError("Invalid reconciliation snapshot.")
    content = base64.b64decode(encoded, validate=True)
    if hashlib.sha256(content).hexdigest() != digest:
        raise ValueError("Reconciliation snapshot digest mismatch.")
    return exists, content


def _required_marker_string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"Invalid pending reconciliation {field}.")
    return value


def _safe_pending_target(
    common_directory: Path,
    relative_path: Any,
    expected_relative_path: str,
) -> Path:
    if relative_path != expected_relative_path:
        raise ValueError("Pending reconciliation target is not canonical.")
    candidate = common_directory / expected_relative_path
    current = common_directory
    for component in Path(expected_relative_path).parts:
        current = current / component
        try:
            mode = os.lstat(current).st_mode
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(mode):
            raise ValueError("Pending reconciliation target contains a symbolic link.")
    return candidate


def _snapshot_json(snapshot: dict[str, Any], field: str) -> dict[str, Any]:
    exists, content = _decoded_snapshot(snapshot)
    if not exists:
        raise ValueError(f"Pending reconciliation {field} snapshot must exist.")
    try:
        value = json.loads(content.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(
            f"Pending reconciliation {field} snapshot is not valid JSON."
        ) from error
    if not isinstance(value, dict):
        raise ValueError(f"Pending reconciliation {field} snapshot is not an object.")
    return value


def _appended_event(
    original: bytes,
    replacement: bytes,
    field: str,
) -> dict[str, Any]:
    if not replacement.startswith(original):
        raise ValueError(
            f"Pending reconciliation journal {field} does not preserve original bytes."
        )
    appended = replacement[len(original) :]
    if not appended or not appended.endswith(b"\n") or b"\n" in appended[:-1]:
        raise ValueError(
            f"Pending reconciliation journal {field} is not one appended event."
        )
    try:
        event = json.loads(appended.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(
            f"Pending reconciliation journal {field} event is invalid."
        ) from error
    if not isinstance(event, dict):
        raise ValueError(
            f"Pending reconciliation journal {field} event is not an object."
        )
    return event


def _validated_pending_reconciliation(
    common_directory: Path,
    pending: Any,
) -> dict[str, Any]:
    if not isinstance(pending, dict) or set(pending) != {
        "schema_version",
        "state",
        "claim_id",
        "event_id",
        "incarnation_id",
        "event_timestamp",
        "prior_rejected_release_reference",
        "registry",
        "journal",
    }:
        raise ValueError("Invalid pending reconciliation marker schema.")
    if type(pending["schema_version"]) is not int or pending["schema_version"] != 1:
        raise ValueError("Unsupported pending reconciliation marker schema version.")
    state = pending["state"]
    if state not in {"prepared", "committed"}:
        raise ValueError("Invalid pending reconciliation state.")
    claim_id = _required_marker_string(pending["claim_id"], "claim id")
    event_id = _required_marker_string(pending["event_id"], "event id")
    incarnation_id = _required_marker_string(
        pending["incarnation_id"],
        "incarnation id",
    )
    event_timestamp = _required_marker_string(
        pending["event_timestamp"],
        "event timestamp",
    )
    prior_reference = _required_marker_string(
        pending["prior_rejected_release_reference"],
        "prior rejected release reference",
    )
    try:
        journal_day = _parse_timestamp(event_timestamp).date().isoformat()
    except (TypeError, ValueError) as error:
        raise ValueError("Invalid pending reconciliation event timestamp.") from error

    registry = pending["registry"]
    journal = pending["journal"]
    if not isinstance(registry, dict) or set(registry) != {
        "path",
        "original",
        "released",
    }:
        raise ValueError("Invalid pending reconciliation registry schema.")
    if not isinstance(journal, dict) or set(journal) != {
        "path",
        "original",
        "prepared",
        "released",
    }:
        raise ValueError("Invalid pending reconciliation journal schema.")
    registry_path = _safe_pending_target(
        common_directory,
        registry["path"],
        REGISTRY_FILE_NAME,
    )
    journal_relative = (
        f"{EVENT_DIRECTORY_NAME}/hot/{journal_day}.jsonl"
    )
    journal_path = _safe_pending_target(
        common_directory,
        journal["path"],
        journal_relative,
    )
    if registry_path == journal_path:
        raise ValueError("Pending reconciliation targets must be distinct.")

    original_registry = _snapshot_json(registry["original"], "original registry")
    released_registry = _snapshot_json(registry["released"], "released registry")
    original_claims = original_registry.get("claims")
    released_claims = released_registry.get("claims")
    if not isinstance(original_claims, list) or not isinstance(released_claims, list):
        raise ValueError("Pending reconciliation registry claims are invalid.")
    matching_indexes = [
        index
        for index, claim in enumerate(original_claims)
        if isinstance(claim, dict) and claim.get("claim_id") == claim_id
    ]
    if len(matching_indexes) != 1:
        raise ValueError(
            "Pending reconciliation original registry must contain one target claim."
        )
    target_index = matching_indexes[0]
    expected_released_claims = (
        original_claims[:target_index] + original_claims[target_index + 1 :]
    )
    expected_released_registry = dict(original_registry)
    expected_released_registry["claims"] = expected_released_claims
    if released_registry != expected_released_registry:
        raise ValueError(
            "Pending reconciliation released registry is not target-only removal."
        )
    target_claim = original_claims[target_index]
    target_incarnation = target_claim.get("incarnation_id")
    if target_incarnation is not None and target_incarnation != incarnation_id:
        raise ValueError("Pending reconciliation claim incarnation is inconsistent.")

    original_exists, original_journal = _decoded_snapshot(journal["original"])
    if not original_exists and original_journal:
        raise ValueError(
            "Pending reconciliation absent original journal must have empty bytes."
        )
    prepared_exists, prepared_journal = _decoded_snapshot(journal["prepared"])
    released_exists, released_journal = _decoded_snapshot(journal["released"])
    if not prepared_exists or not released_exists:
        raise ValueError(
            "Pending reconciliation prepared and released journals must exist."
        )
    prepared_event = _appended_event(
        original_journal,
        prepared_journal,
        "prepared",
    )
    released_event = _appended_event(
        original_journal,
        released_journal,
        "released",
    )
    if prepared_event.get("outcome") != "RELEASE_PENDING":
        raise ValueError("Pending reconciliation prepared outcome is invalid.")
    if prepared_event.get("reconciliation_transaction_state") != "prepared":
        raise ValueError("Pending reconciliation prepared state is invalid.")
    if released_event.get("outcome") != "RELEASED":
        raise ValueError("Pending reconciliation released outcome is invalid.")
    if "reconciliation_transaction_state" in released_event:
        raise ValueError("Pending reconciliation released event retains pending state.")
    normalized_prepared = dict(prepared_event)
    normalized_prepared["outcome"] = "RELEASED"
    normalized_prepared.pop("reconciliation_transaction_state", None)
    if normalized_prepared != released_event:
        raise ValueError(
            "Pending reconciliation journal snapshots are not one event transformation."
        )
    reconciliation = released_event.get("reconciliation")
    if (
        released_event.get("event_id") != event_id
        or released_event.get("claim_id") != claim_id
        or released_event.get("incarnation_id") != incarnation_id
        or released_event.get("timestamp") != event_timestamp
        or not isinstance(reconciliation, dict)
        or reconciliation.get("prior_rejected_release_reference") != prior_reference
        or not isinstance(reconciliation.get("claim_incarnation"), dict)
        or reconciliation["claim_incarnation"].get("id") != incarnation_id
        or reconciliation.get("baseline_commit") != target_claim.get("baseline_commit")
        or not _claim_facts_match(released_event, target_claim)
    ):
        raise ValueError("Pending reconciliation event relationships are invalid.")

    registry_current = (
        registry_path.exists(),
        registry_path.read_bytes() if registry_path.exists() else b"",
    )
    journal_current = (
        journal_path.exists(),
        journal_path.read_bytes() if journal_path.exists() else b"",
    )
    original_registry_snapshot = _decoded_snapshot(registry["original"])
    released_registry_snapshot = _decoded_snapshot(registry["released"])
    original_journal_snapshot = _decoded_snapshot(journal["original"])
    prepared_journal_snapshot = _decoded_snapshot(journal["prepared"])
    released_journal_snapshot = _decoded_snapshot(journal["released"])
    if state == "prepared":
        registry_allowed = {
            original_registry_snapshot,
            released_registry_snapshot,
        }
        journal_allowed = {
            original_journal_snapshot,
            prepared_journal_snapshot,
        }
    else:
        registry_allowed = {released_registry_snapshot}
        journal_allowed = {
            prepared_journal_snapshot,
            released_journal_snapshot,
        }
    if registry_current not in registry_allowed:
        raise ValueError(
            "Pending reconciliation registry target does not match an allowed state."
        )
    if journal_current not in journal_allowed:
        raise ValueError(
            "Pending reconciliation journal target does not match an allowed state."
        )
    return {
        **pending,
        "registry_path": registry_path,
        "journal_path": journal_path,
    }


def _write_pending_reconciliation(
    common_directory: Path,
    pending: dict[str, Any],
) -> Path:
    path = _pending_reconciliation_path(common_directory)
    _validated_pending_reconciliation(common_directory, pending)
    content = (json.dumps(pending, indent=2, sort_keys=True) + "\n").encode("utf-8")
    _durable_atomic_replace(path, content)
    return path


def _restore_faults(target_name: str) -> dict[str, str]:
    prefix = f"AGENT_CLAIM_TEST_FAIL_RECONCILIATION_{target_name}_RESTORE"
    return {
        "write": f"{prefix}_WRITE",
        "short_write": f"{prefix}_SHORT_WRITE",
        "after_write": f"{prefix}_AFTER_WRITE",
        "fsync": f"{prefix}_FSYNC",
        "replace": f"{prefix}_REPLACE",
        "directory_fsync": f"{prefix}_DIRECTORY_FSYNC",
    }


def _restore_pending_snapshot(
    path: Path,
    snapshot: dict[str, Any],
    *,
    faults: dict[str, str] | None = None,
) -> None:
    exists, content = _decoded_snapshot(snapshot)
    if exists:
        _durable_atomic_replace(path, content, faults=faults)
    else:
        _durable_remove(path)


def _recover_pending_reconciliation(common_directory: Path) -> dict[str, Any] | None:
    marker_path = _pending_reconciliation_path(common_directory)
    if not os.path.lexists(marker_path):
        return None
    claim_id = "unknown"
    try:
        if stat.S_ISLNK(os.lstat(marker_path).st_mode):
            raise ValueError("Pending reconciliation marker cannot be a symbolic link.")
        decoded = marker_path.read_bytes().decode("utf-8")
        raw_pending = json.loads(decoded)
        if isinstance(raw_pending, dict) and isinstance(raw_pending.get("claim_id"), str):
            claim_id = raw_pending["claim_id"]
        pending = _validated_pending_reconciliation(common_directory, raw_pending)
        state = pending["state"]
        registry = pending["registry"]
        journal = pending["journal"]
        registry_path = pending["registry_path"]
        journal_path = pending["journal_path"]
        if state == "prepared":
            _restore_pending_snapshot(
                journal_path,
                journal["original"],
                faults=_restore_faults("JOURNAL"),
            )
            _restore_pending_snapshot(
                registry_path,
                registry["original"],
                faults=_restore_faults("REGISTRY"),
            )
        else:
            _restore_pending_snapshot(registry_path, registry["released"])
            _restore_pending_snapshot(journal_path, journal["released"])
        _durable_remove(
            marker_path,
            fault_environment=(
                "AGENT_CLAIM_TEST_FAIL_RECONCILIATION_MARKER_REMOVE"
            ),
        )
        return {
            "claim_id": claim_id,
            "event_id": pending.get("event_id"),
            "resolved_state": state,
        }
    except (
        AttributeError,
        binascii.Error,
        KeyError,
        OSError,
        TypeError,
        UnicodeDecodeError,
        ValueError,
        json.JSONDecodeError,
    ) as error:
        raise _PendingReconciliationError(
            f"Pending reconciliation recovery failed: {error}",
            claim_id,
            marker_path,
        ) from error


@contextmanager
def _locked_registry(
    repository: Path,
    *,
    recover_pending: bool = True,
) -> Iterator[tuple[Path, dict[str, Any]]]:
    registry_path, lock_path = _registry_paths(repository)
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+", encoding="utf-8") as lock_file:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
        try:
            marker_path = _pending_reconciliation_path(registry_path.parent)
            if recover_pending:
                _recover_pending_reconciliation(registry_path.parent)
            elif os.path.lexists(marker_path):
                raise _PendingReconciliationError(
                    "Pending reconciliation requires recovery through the same claim-helper interface before reporting.",
                    "unknown",
                    marker_path,
                )
            if registry_path.exists():
                data = json.loads(registry_path.read_text(encoding="utf-8"))
            else:
                data = {"claims": []}
            if not isinstance(data.get("claims"), list):
                raise ValueError(f"Invalid claim registry: {registry_path}")
            yield registry_path, data
        finally:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)


@contextmanager
def _maintenance_lock(common_directory: Path) -> Iterator[None]:
    root, _hot, _archive, _journal = _journal_paths(common_directory)
    root.mkdir(parents=True, exist_ok=True)
    with (root / "maintenance.lock").open("a+", encoding="utf-8") as lock_file:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)


def _write_registry(path: Path, data: dict[str, Any]) -> None:
    temporary_path = path.with_suffix(".tmp")
    temporary_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(temporary_path, path)


def _now() -> datetime:
    override = os.environ.get("AGENT_CLAIM_TEST_NOW")
    if override:
        parsed = datetime.fromisoformat(override.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    return datetime.now(timezone.utc)


def _format_timestamp(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


def _timestamp() -> str:
    return _format_timestamp(_now())


def _parse_timestamp(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _deadline_policy_seconds(
    policy: dict[str, Any],
    field: str,
    context: str,
    *,
    allow_zero: bool = False,
) -> int:
    value = policy.get(field)
    valid = isinstance(value, int) and not isinstance(value, bool)
    valid = valid and (value >= 0 if allow_zero else value > 0)
    if not valid:
        qualifier = "non-negative" if allow_zero else "positive"
        raise _DeadlineError(
            f"{context}.{field} must be a {qualifier} integer.",
            field,
            "invalid_project_deadline_policy",
        )
    return value


def _load_deadline_policy(repository: Path) -> dict[str, Any]:
    project_path = repository / "PROJECT.yaml"
    if not project_path.is_file():
        raise _DeadlineError(
            "PROJECT.yaml is required for named resource acquisition.",
            "PROJECT.yaml",
            "project_policy_missing",
        )
    try:
        project = yaml.safe_load(project_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as error:
        raise _DeadlineError(
            f"PROJECT.yaml resource deadline policy is unreadable or invalid: {error}.",
            "PROJECT.yaml",
            "project_policy_invalid",
        ) from error
    coordination = project.get("resource_coordination") if isinstance(project, dict) else None
    if not isinstance(coordination, dict) or coordination.get("selected") != "agent-claim":
        raise _DeadlineError(
            "PROJECT.yaml resource_coordination must select agent-claim for named resource acquisition.",
            "resource_coordination.selected",
            "resource_coordination_not_selected",
        )
    policy = coordination.get("deadline_policy")
    if not isinstance(policy, dict) or set(policy) != {"resource_classes", "resource_overrides"}:
        raise _DeadlineError(
            "resource_coordination.deadline_policy keys must be exactly: resource_classes, resource_overrides.",
            "resource_coordination.deadline_policy",
            "invalid_project_deadline_policy",
        )
    classes = policy.get("resource_classes")
    if not isinstance(classes, dict) or set(classes) != set(_RESOURCE_DEADLINE_CLASS_IDS):
        raise _DeadlineError(
            "resource_coordination.deadline_policy.resource_classes keys must be exactly: "
            + ", ".join(_RESOURCE_DEADLINE_CLASS_IDS)
            + ".",
            "resource_coordination.deadline_policy.resource_classes",
            "invalid_project_deadline_policy",
        )
    normalized_classes: dict[str, dict[str, int]] = {}
    for class_id in _RESOURCE_DEADLINE_CLASS_IDS:
        class_policy = classes[class_id]
        context = f"resource_coordination.deadline_policy.resource_classes.{class_id}"
        if not isinstance(class_policy, dict) or set(class_policy) != {
            "maximum_duration_seconds",
            "cleanup_grace_seconds",
        }:
            raise _DeadlineError(
                f"{context} keys must be exactly: maximum_duration_seconds, cleanup_grace_seconds.",
                context,
                "invalid_project_deadline_policy",
            )
        normalized_classes[class_id] = {
            "maximum_duration_seconds": _deadline_policy_seconds(
                class_policy,
                "maximum_duration_seconds",
                context,
            ),
            "cleanup_grace_seconds": _deadline_policy_seconds(
                class_policy,
                "cleanup_grace_seconds",
                context,
                allow_zero=True,
            ),
        }
    overrides = policy.get("resource_overrides")
    if not isinstance(overrides, dict):
        raise _DeadlineError(
            "resource_coordination.deadline_policy.resource_overrides must be a mapping.",
            "resource_coordination.deadline_policy.resource_overrides",
            "invalid_project_deadline_policy",
        )
    normalized_overrides: dict[str, dict[str, Any]] = {}
    for raw_resource_id, override in overrides.items():
        resource_id = raw_resource_id.strip() if isinstance(raw_resource_id, str) else ""
        context = f"resource_coordination.deadline_policy.resource_overrides.{resource_id}"
        if not resource_id or resource_id != raw_resource_id or len(resource_id) > MAX_IDENTIFIER_LENGTH:
            raise _DeadlineError(
                "resource override ids must be canonical non-empty strings of at most 200 characters.",
                "resource_id",
                "invalid_project_deadline_policy",
            )
        if not isinstance(override, dict) or set(override) != {
            "resource_class",
            "maximum_duration_seconds",
            "cleanup_grace_seconds",
        }:
            raise _DeadlineError(
                f"{context} keys must be exactly: resource_class, maximum_duration_seconds, cleanup_grace_seconds.",
                context,
                "invalid_project_deadline_policy",
            )
        resource_class = override.get("resource_class")
        if resource_class not in normalized_classes:
            raise _DeadlineError(
                f"{context}.resource_class must name a configured resource class.",
                "resource_class",
                "invalid_project_deadline_policy",
            )
        normalized_overrides[resource_id] = {
            "resource_class": resource_class,
            "maximum_duration_seconds": _deadline_policy_seconds(
                override,
                "maximum_duration_seconds",
                context,
            ),
            "cleanup_grace_seconds": _deadline_policy_seconds(
                override,
                "cleanup_grace_seconds",
                context,
                allow_zero=True,
            ),
        }
    return {"resource_classes": normalized_classes, "resource_overrides": normalized_overrides}


def _deadline_request_from_args(
    args: argparse.Namespace,
    resources: Sequence[str],
    repository: Path,
) -> dict[str, Any] | None:
    argument_names = (
        "resource_class",
        "resource_id",
        "expected_duration_seconds",
        "requested_hard_stop_duration_seconds",
    )
    values = {name: getattr(args, name, None) for name in argument_names}
    supplied = [name for name, value in values.items() if value is not None]
    if len(resources) > 1:
        raise _DeadlineError(
            "A claim may acquire exactly one named resource.",
            "resource",
            "multiple_resources_not_supported",
        )
    if not resources and not supplied:
        return None
    if not resources:
        raise _DeadlineError(
            "Resource timing arguments require exactly one named --resource.",
            "resource",
            "timing_without_resource",
        )
    if not supplied:
        raise _DeadlineError(
            "Named resource acquisition requires complete timing evidence.",
            "resource",
            "resource_timing_required",
        )
    if len(supplied) != len(argument_names):
        missing = sorted(set(argument_names) - set(supplied))
        raise _DeadlineError(
            f"Resource timing arguments must be supplied together; missing: {', '.join(missing)}.",
            ",".join(missing),
            "incomplete_deadline_arguments",
        )

    resource_class = values["resource_class"].strip() if isinstance(values["resource_class"], str) else None
    resource_id = values["resource_id"].strip() if isinstance(values["resource_id"], str) else None
    if not isinstance(resource_class, str) or not re.fullmatch(r"[a-z][a-z0-9-]*", resource_class):
        raise _DeadlineError(
            "resource class must be a stable lowercase identifier containing letters, digits, and hyphens.",
            "resource_class",
            "invalid_resource_class",
        )
    if not isinstance(resource_id, str) or resource_id != resources[0]:
        raise _DeadlineError(
            "resource id must exactly match one acquired --resource value.",
            "resource_id",
            "resource_id_not_acquired",
        )

    expected = values["expected_duration_seconds"]
    hard_stop = values["requested_hard_stop_duration_seconds"]
    for field, value in (
        ("expected_duration_seconds", expected),
        ("requested_hard_stop_duration_seconds", hard_stop),
    ):
        if not isinstance(value, int) or value <= 0:
            raise _DeadlineError(
                f"{field.replace('_', ' ')} must be a positive integer.",
                field,
                "invalid_duration",
            )
    if expected > hard_stop:
        raise _DeadlineError(
            "expected duration must not exceed requested hard stop.",
            "expected_duration_seconds",
            "expected_exceeds_hard_stop",
        )
    policy = _load_deadline_policy(repository)
    class_policy = policy["resource_classes"].get(resource_class)
    if class_policy is None:
        raise _DeadlineError(
            "resource class must name a configured PROJECT.yaml resource class.",
            "resource_class",
            "resource_class_not_configured",
        )
    override = policy["resource_overrides"].get(resource_id)
    if override is not None and override["resource_class"] != resource_class:
        raise _DeadlineError(
            f"resource id {resource_id} is configured for resource class {override['resource_class']}.",
            "resource_class",
            "resource_override_class_mismatch",
        )
    resolved = override or class_policy
    maximum = resolved["maximum_duration_seconds"]
    cleanup_grace = resolved["cleanup_grace_seconds"]
    if hard_stop > maximum:
        raise _DeadlineError(
            "requested hard stop must not exceed configured maximum.",
            "requested_hard_stop_duration_seconds",
            "hard_stop_exceeds_maximum",
        )

    return {
        "resource_class": resource_class,
        "resource_id": resource_id,
        "expected_duration_seconds": expected,
        "requested_hard_stop_duration_seconds": hard_stop,
        "configured_maximum_duration_seconds": maximum,
        "cleanup_grace_seconds": cleanup_grace,
    }


def _deadline_from_request(request: dict[str, Any], acquired_at: str) -> dict[str, Any]:
    acquired = _parse_timestamp(acquired_at)
    hard_stop = request["requested_hard_stop_duration_seconds"]
    cleanup_grace = request["cleanup_grace_seconds"]
    expected = request["expected_duration_seconds"]
    hard_stop_at = acquired + timedelta(seconds=hard_stop)
    return {
        **request,
        "acquired_at": acquired_at,
        "expected_release_at": _format_timestamp(acquired + timedelta(seconds=expected)),
        "hard_stop_at": _format_timestamp(hard_stop_at),
        "cleanup_grace_ends_at": _format_timestamp(
            hard_stop_at + timedelta(seconds=cleanup_grace)
        ),
        "extensions": [],
    }


def _deadline_status(deadline: dict[str, Any], evaluated_at: datetime) -> dict[str, Any]:
    hard_stop_at = _parse_timestamp(str(deadline["hard_stop_at"]))
    cleanup_grace_ends_at = _parse_timestamp(str(deadline["cleanup_grace_ends_at"]))
    overdue = evaluated_at >= hard_stop_at
    cleanup_elapsed = evaluated_at >= cleanup_grace_ends_at
    return {
        "evaluated_at": _format_timestamp(evaluated_at),
        "overdue": overdue,
        "cleanup_grace": {
            "seconds": deadline["cleanup_grace_seconds"],
            "ends_at": deadline["cleanup_grace_ends_at"],
            "active": overdue and not cleanup_elapsed,
            "elapsed": cleanup_elapsed,
        },
        "stopped_owner_actionability_inputs": {
            "owner_stopped": None,
            "immediately_actionable_when_stopped": True,
        },
    }


def _path_domain(path: str) -> str:
    return "backlog" if _path_is_within(path, BACKLOG_ROOT_DIRECTORY) else "project_files"


def _status_snapshot(worktree: Path) -> dict[str, dict[str, str]]:
    raw_entries = _git(
        worktree,
        "status",
        "--porcelain=v1",
        "-z",
        "--untracked-files=all",
    ).stdout.split("\0")
    snapshot: dict[str, dict[str, str]] = {"project_files": {}, "backlog": {}}
    index = 0
    while index < len(raw_entries):
        entry = raw_entries[index]
        index += 1
        if not entry:
            continue
        status = entry[:2]
        paths = [entry[3:]]
        if "R" in status or "C" in status:
            if index >= len(raw_entries) or not raw_entries[index]:
                raise ValueError("Incomplete NUL-terminated Git rename status record.")
            paths.append(raw_entries[index])
            index += 1
        for path in paths:
            snapshot[_path_domain(path)][path] = status
    return snapshot


def _status_entries(paths: dict[str, str]) -> list[dict[str, str]]:
    return [
        {"path": path, "status": status}
        for path, status in sorted(paths.items())
    ]


def _status_state(worktree: Path, snapshot: dict[str, dict[str, str]]) -> dict[str, dict[str, str]]:
    state: dict[str, dict[str, str]] = {}
    for paths in snapshot.values():
        for path, status in paths.items():
            candidate = worktree / path
            if candidate.is_symlink():
                worktree_digest = hashlib.sha256(os.readlink(candidate).encode("utf-8")).hexdigest()
            elif candidate.is_file():
                worktree_digest = hashlib.sha256(candidate.read_bytes()).hexdigest()
            else:
                worktree_digest = "missing"
            index_entry = _git(worktree, "ls-files", "--stage", "--", path).stdout.strip()
            state[path] = {
                "status": status,
                "worktree_sha256": worktree_digest,
                "index_entry": index_entry,
            }
    return state


def _state_outside_domain(
    state: dict[str, dict[str, str]],
    file_domain: str,
) -> dict[str, dict[str, str]]:
    return {
        path: details
        for path, details in state.items()
        if not _path_belongs_to_domain(path, file_domain)
    }


def _status_paths(entries: Sequence[dict[str, str]]) -> list[str]:
    return sorted({entry["path"] for entry in entries})


def _status_for_domain(
    snapshot: dict[str, dict[str, str]],
    file_domain: str,
    *,
    resource_only: bool = False,
) -> list[dict[str, str]]:
    if file_domain == "all_files" or (file_domain == "none" and not resource_only):
        return _status_entries({**snapshot["project_files"], **snapshot["backlog"]})
    if file_domain == "none":
        return []
    if file_domain in snapshot:
        return _status_entries(snapshot[file_domain])
    return []


def _status_outside_domain(
    snapshot: dict[str, dict[str, str]],
    file_domain: str,
) -> list[dict[str, str]]:
    if file_domain == "project_files":
        return _status_entries(snapshot["backlog"])
    if file_domain == "backlog":
        return _status_entries(snapshot["project_files"])
    return []


def _path_belongs_to_domain(path: str, file_domain: str) -> bool:
    return file_domain in {"all_files", "none"} or _path_domain(path) == file_domain


def _head(worktree: Path) -> str:
    return _git(worktree, "rev-parse", "HEAD").stdout.strip()


def _full_commit_sha(value: str) -> str:
    normalized = value.strip().lower()
    if not FULL_COMMIT_SHA_PATTERN.fullmatch(normalized):
        raise argparse.ArgumentTypeError("commit evidence must be one full 40-character hexadecimal SHA.")
    return normalized


def _commit_changed_paths(worktree: Path, commit: str) -> list[str]:
    completed = _git(
        worktree,
        "diff-tree",
        "--root",
        "--no-commit-id",
        "--name-only",
        "-r",
        "-m",
        "-z",
        commit,
    )
    return sorted({path for path in completed.stdout.split("\0") if path})


def _branch(worktree: Path) -> str:
    return _git(worktree, "branch", "--show-current").stdout.strip()


def _discard_incomplete_worktree(repository: Path, worktree: Path, branch: str) -> None:
    _git(repository, "worktree", "remove", "--force", str(worktree), check=False)
    _git(repository, "branch", "-D", branch, check=False)


def _create_isolated_worktree(repository: Path, worktree: Path, branch: str, base: str) -> str | None:
    created = _git(
        repository,
        "worktree",
        "add",
        "--no-checkout",
        "-b",
        branch,
        str(worktree),
        base,
        check=False,
    )
    if created.returncode != SUCCESS:
        return "git_worktree_create_failed"

    sparse_checkout = _git(
        worktree,
        "sparse-checkout",
        "set",
        "--no-cone",
        *ISOLATED_SPARSE_CHECKOUT_PATTERNS,
        check=False,
    )
    if sparse_checkout.returncode != SUCCESS:
        _discard_incomplete_worktree(repository, worktree, branch)
        return "sparse_checkout_configure_failed"

    populated = _git(worktree, "reset", "--hard", "HEAD", check=False)
    if populated.returncode != SUCCESS:
        _discard_incomplete_worktree(repository, worktree, branch)
        return "sparse_checkout_populate_failed"
    return None


def _bounded_identifier(value: str | None) -> str | None:
    if value is None:
        return None
    return value.strip()[:MAX_IDENTIFIER_LENGTH]


def _deduplicate(values: Sequence[str]) -> list[str]:
    return list(dict.fromkeys(values))


def _normalize_repository_path(repository: Path, value: str) -> str:
    stripped = value.strip()
    if not stripped:
        raise _ScopeError("Scope paths cannot be empty.", value, "provide a repository-relative path")
    if any(character in stripped for character in "*?["):
        raise _ScopeError(
            "Wildcard scopes are not supported.",
            stripped,
            "use --tree <path> or --all-files",
        )
    candidate = Path(stripped)
    if candidate.is_absolute():
        try:
            candidate = candidate.resolve().relative_to(repository)
        except ValueError as error:
            raise _ScopeError(
                "Scope paths must remain inside the repository.",
                stripped,
                "provide a repository-relative path",
            ) from error
    normalized = Path(os.path.normpath(str(candidate))).as_posix()
    if normalized == ".." or normalized.startswith("../"):
        raise _ScopeError(
            "Scope paths must remain inside the repository.",
            stripped,
            "provide a repository-relative path",
        )
    if _path_is_within(normalized, WORKTREE_ROOT_DIRECTORY):
        raise _ScopeError(
            "Ignored operational worktree state is outside file ownership domains.",
            normalized,
            "claim the project source path or an exclusive resource instead",
            "operational_path_not_claimable",
        )
    return normalized.rstrip("/") or "."


def _empty_scope() -> dict[str, Any]:
    return {
        "files": [],
        "trees": [],
        "project_files": False,
        "backlog": False,
        "all_files": False,
        "file_domain": "none",
        "resources": [],
        "scope_reason": None,
    }


def _scope_from_args(args: argparse.Namespace, repository: Path) -> tuple[dict[str, Any], list[dict[str, str]]]:
    scope = _empty_scope()
    warnings: list[dict[str, str]] = []
    compatibility = bool(getattr(args, "compat_file_directories", False))

    for raw_file in getattr(args, "file", []):
        normalized = _normalize_repository_path(repository, raw_file)
        if normalized == ".":
            raise _ScopeError(
                "Repository-wide ownership cannot be requested through --file.",
                raw_file,
                "use --all-files with --scope-reason",
            )
        if (repository / normalized).is_dir():
            if not compatibility:
                raise _ScopeError(
                    "Existing directories cannot be requested through --file.",
                    normalized,
                    "use --tree <path> with --scope-reason",
                )
            scope["trees"].append(normalized)
            warnings.append(
                {
                    "code": "legacy_file_directory_scope",
                    "message": f"Converted --file {normalized} to an explicit tree scope.",
                }
            )
        else:
            scope["files"].append(normalized)

    for raw_tree in getattr(args, "tree", []):
        normalized = _normalize_repository_path(repository, raw_tree)
        if normalized == ".":
            raise _ScopeError(
                "Repository root cannot be requested as a tree.",
                raw_tree,
                "use --all-files with --scope-reason",
            )
        if (repository / normalized).is_file():
            raise _ScopeError(
                "Existing files cannot be requested through --tree.",
                normalized,
                "use --file <path>",
            )
        scope["trees"].append(normalized)

    scope["files"] = _deduplicate(scope["files"])
    scope["trees"] = _deduplicate(scope["trees"])
    scope["resources"] = _deduplicate(
        value.strip() for value in getattr(args, "resource", []) if value.strip()
    )
    scope["project_files"] = bool(getattr(args, "project_files", False))
    scope["backlog"] = bool(getattr(args, "backlog", False))
    scope["all_files"] = bool(getattr(args, "all_files", False))

    selected_broad_domains = [
        domain
        for domain in ("project_files", "backlog", "all_files")
        if scope[domain]
    ]
    if len(selected_broad_domains) > 1:
        raise _ScopeError(
            "Broad file domains are mutually exclusive.",
            ", ".join(selected_broad_domains),
            "select exactly one of --project-files, --backlog, or --all-files",
            "multiple_broad_file_domains",
        )

    path_domains = {_path_domain(path) for _kind, path in _path_scopes(scope, include_broad=False)}
    if len(path_domains) > 1:
        raise _ScopeError(
            "One claim cannot mix project and backlog paths.",
            ", ".join(sorted(path_domains)),
            "use separate project and backlog claims",
            "mixed_file_domains",
        )
    broad_domain = selected_broad_domains[0] if selected_broad_domains else None
    path_domain = next(iter(path_domains), None)
    if broad_domain in {"project_files", "backlog"} and path_domain and broad_domain != path_domain:
        raise _ScopeError(
            "Explicit paths must belong to the selected broad file domain.",
            path_domain,
            f"use only {broad_domain.replace('_', '-')} paths or a separate claim",
            "mixed_file_domains",
        )
    scope["file_domain"] = broad_domain or path_domain or "none"
    if path_domain == "backlog" and not scope["backlog"]:
        warnings.append(
            {
                "code": "compat_backlog_path",
                "message": "Classified explicit backlog paths as backlog-domain ownership.",
            }
        )

    reason = getattr(args, "scope_reason", None)
    if reason is not None:
        reason = reason.strip()
        if not reason or "\n" in reason or "\r" in reason or len(reason) > MAX_SCOPE_REASON_LENGTH:
            raise _ScopeError(
                f"Scope reasons must contain 1 to {MAX_SCOPE_REASON_LENGTH} single-line characters.",
                reason,
                "provide a short coordination-only --scope-reason",
            )
    if (scope["trees"] or scope["project_files"] or scope["all_files"]) and not reason:
        raise _ScopeError(
            "Broad tree and repository-wide scopes require a reason.",
            ", ".join(scope["trees"]) or ".",
            "add --scope-reason with bounded coordination-only text",
        )
    scope["scope_reason"] = reason
    return scope, warnings


def _claim_scope(claim: dict[str, Any]) -> dict[str, Any]:
    return {
        "files": [str(value) for value in claim.get("files", [])],
        "trees": [str(value) for value in claim.get("trees", [])],
        "project_files": bool(claim.get("project_files", False)),
        "backlog": bool(claim.get("backlog", False)),
        "all_files": bool(claim.get("all_files", False)),
        "file_domain": str(claim.get("file_domain") or _legacy_file_domain(claim)),
        "resources": [str(value) for value in claim.get("resources", [])],
        "scope_reasons": dict(claim.get("scope_reasons", {})),
    }


def _legacy_file_domain(claim: dict[str, Any]) -> str:
    if claim.get("all_files"):
        return "all_files"
    domains = {
        _path_domain(str(path))
        for path in [*claim.get("files", []), *claim.get("trees", [])]
    }
    if len(domains) == 1:
        return next(iter(domains))
    if len(domains) > 1:
        return "legacy_mixed"
    return "none"


def _claim_for_output(
    claim: dict[str, Any],
    evaluated_at: datetime | None = None,
) -> dict[str, Any]:
    rendered = dict(claim)
    if "file_domain" not in claim:
        rendered["file_domain"] = _legacy_file_domain(claim)
        rendered["project_files"] = False
        rendered["backlog"] = False
        rendered["compatibility"] = {
            "legacy_registry_claim": True,
            "release_policy": "complete_worktree",
        }
    elif not isinstance(claim.get("baseline_out_of_domain_state"), dict):
        rendered["compatibility"] = {
            "missing_out_of_domain_baseline": True,
            "release_policy": "complete_worktree",
        }
    deadline = claim.get("deadline")
    if isinstance(deadline, dict) and evaluated_at is not None:
        rendered["deadline_status"] = _deadline_status(deadline, evaluated_at)
    return rendered


def _path_is_within(path: str, tree: str) -> bool:
    return path == tree or path.startswith(tree + "/")


def _path_scope_overlap(
    requested_kind: str,
    requested_path: str,
    claimed_kind: str,
    claimed_path: str,
) -> bool:
    if "all_files" in {requested_kind, claimed_kind}:
        return True
    if requested_kind == "project_files":
        return claimed_kind == "project_files" or _path_domain(claimed_path) == "project_files"
    if claimed_kind == "project_files":
        return requested_kind == "project_files" or _path_domain(requested_path) == "project_files"
    if requested_kind == "backlog":
        return claimed_kind == "backlog" or _path_domain(claimed_path) == "backlog"
    if claimed_kind == "backlog":
        return requested_kind == "backlog" or _path_domain(requested_path) == "backlog"
    if requested_kind == "file" and claimed_kind == "file":
        return requested_path == claimed_path
    if requested_kind == "tree" and claimed_kind == "tree":
        return _path_is_within(requested_path, claimed_path) or _path_is_within(claimed_path, requested_path)
    if requested_kind == "tree":
        return _path_is_within(claimed_path, requested_path)
    return _path_is_within(requested_path, claimed_path)


def _path_scopes(scope: dict[str, Any], include_broad: bool = True) -> list[tuple[str, str]]:
    values = [("file", value) for value in scope.get("files", [])]
    values.extend(("tree", value) for value in scope.get("trees", []))
    if include_broad:
        if scope.get("project_files"):
            values.append(("project_files", "."))
        if scope.get("backlog"):
            values.append(("backlog", BACKLOG_ROOT_DIRECTORY))
        if scope.get("all_files"):
            values.append(("all_files", "."))
    return values


def _scope_requires_primary_worktree(scope: dict[str, Any]) -> bool:
    return scope.get("file_domain") in {"backlog", "all_files"}


def _scope_file_domain(scope: dict[str, Any]) -> str:
    explicit = str(scope.get("file_domain") or "")
    if explicit:
        return explicit
    if scope.get("all_files"):
        return "all_files"
    if scope.get("project_files"):
        return "project_files"
    if scope.get("backlog"):
        return "backlog"
    domains = {
        _path_domain(str(path))
        for path in [*scope.get("files", []), *scope.get("trees", [])]
    }
    if len(domains) == 1:
        return next(iter(domains))
    return "legacy_mixed" if domains else "none"


def _scope_is_resource_only(scope: dict[str, Any]) -> bool:
    return _scope_file_domain(scope) == "none" and bool(scope.get("resources"))


def _overlap_details(requested: dict[str, Any], claimed: dict[str, Any]) -> list[dict[str, str]]:
    details: list[dict[str, str]] = []
    for requested_kind, requested_path in _path_scopes(requested):
        for claimed_kind, claimed_path in _path_scopes(claimed):
            if _path_scope_overlap(requested_kind, requested_path, claimed_kind, claimed_path):
                details.append(
                    {
                        "scope_kind": "path",
                        "requested_kind": requested_kind,
                        "requested": requested_path,
                        "claimed_kind": claimed_kind,
                        "claimed": claimed_path,
                    }
                )
    claimed_resources = set(claimed.get("resources", []))
    for resource in requested.get("resources", []):
        if resource in claimed_resources:
            details.append(
                {
                    "scope_kind": "resource",
                    "requested_kind": "resource",
                    "requested": resource,
                    "claimed_kind": "resource",
                    "claimed": resource,
                }
            )
    return details


def _conflicts(
    claims: list[dict[str, Any]],
    requested: dict[str, Any],
    excluded_claim_id: str | None = None,
) -> list[dict[str, Any]]:
    conflicts: list[dict[str, Any]] = []
    for claim in claims:
        if claim.get("claim_id") == excluded_claim_id:
            continue
        details = _overlap_details(requested, _claim_scope(claim))
        if details:
            conflicts.append({"claim_id": claim["claim_id"], "overlaps": details})
    return conflicts


def _scope_reasons(scope: dict[str, Any]) -> dict[str, str]:
    reason = scope.get("scope_reason")
    if not reason:
        return {}
    reasons = {f"tree:{path}": reason for path in scope.get("trees", [])}
    if scope.get("project_files"):
        reasons["project_files:."] = reason
    if scope.get("backlog"):
        reasons["backlog:backlog"] = reason
    if scope.get("all_files"):
        reasons["all_files:."] = reason
    return reasons


def _owned_and_added_scope(claim: dict[str, Any], requested: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    current = _claim_scope(claim)
    added = _empty_scope()
    owned = _empty_scope()

    current_domain = current["file_domain"]
    requested_domain = requested["file_domain"]
    if current_domain == "legacy_mixed" and requested_domain != "none":
        raise _ScopeError(
            "An active legacy claim with mixed paths cannot be extended with file scope.",
            "legacy_mixed",
            "finish or hand off the legacy claim before acquiring one explicit file domain",
            "legacy_mixed_file_domains",
        )
    if current_domain != "none" and requested_domain != "none" and current_domain != requested_domain:
        raise _ScopeError(
            "An active claim cannot cross file domains.",
            f"{current_domain}, {requested_domain}",
            "use a separate claim for the other file domain",
            "mixed_file_domains",
        )

    for file_path in requested["files"]:
        target = owned if (
            current["all_files"]
            or current["project_files"] and _path_domain(file_path) == "project_files"
            or current["backlog"] and _path_domain(file_path) == "backlog"
            or file_path in current["files"]
            or any(_path_is_within(file_path, tree) for tree in current["trees"])
        ) else added
        target["files"].append(file_path)
    for tree_path in requested["trees"]:
        target = owned if (
            current["all_files"]
            or current["project_files"] and _path_domain(tree_path) == "project_files"
            or current["backlog"] and _path_domain(tree_path) == "backlog"
            or any(_path_is_within(tree_path, tree) for tree in current["trees"])
        ) else added
        target["trees"].append(tree_path)
    if requested["project_files"]:
        (owned if current["project_files"] or current["all_files"] else added)["project_files"] = True
    if requested["backlog"]:
        (owned if current["backlog"] or current["all_files"] else added)["backlog"] = True
    if requested["all_files"]:
        (owned if current["all_files"] else added)["all_files"] = True
    current_resources = set(current["resources"])
    for resource in requested["resources"]:
        (owned if resource in current_resources else added)["resources"].append(resource)

    added["scope_reason"] = requested.get("scope_reason")
    owned["scope_reason"] = requested.get("scope_reason")
    added["file_domain"] = requested_domain if _scope_has_file_values(added) else "none"
    owned["file_domain"] = requested_domain if _scope_has_file_values(owned) else "none"
    return owned, added


def _scope_has_file_values(scope: dict[str, Any]) -> bool:
    return bool(
        scope["files"]
        or scope["trees"]
        or scope["project_files"]
        or scope["backlog"]
        or scope["all_files"]
    )


def _scope_has_values(scope: dict[str, Any]) -> bool:
    return bool(_scope_has_file_values(scope) or scope["resources"])


def _apply_scope(claim: dict[str, Any], added: dict[str, Any]) -> None:
    assign_file_domain = (
        added["file_domain"] != "none"
        and (
            claim.get("file_domain") == "none"
            or "file_domain" not in claim and _legacy_file_domain(claim) == "none"
        )
    )
    claim["files"] = _deduplicate([*claim.get("files", []), *added["files"]])
    claim["trees"] = _deduplicate([*claim.get("trees", []), *added["trees"]])
    claim["project_files"] = bool(claim.get("project_files", False) or added["project_files"])
    claim["backlog"] = bool(claim.get("backlog", False) or added["backlog"])
    claim["all_files"] = bool(claim.get("all_files", False) or added["all_files"])
    if assign_file_domain:
        claim["file_domain"] = added["file_domain"]
    claim["resources"] = _deduplicate([*claim.get("resources", []), *added["resources"]])
    reasons = dict(claim.get("scope_reasons", {}))
    reasons.update(_scope_reasons(added))
    claim["scope_reasons"] = reasons


def _worktree_identifier(claim: dict[str, Any]) -> str | None:
    topology = _checkout_topology(claim)
    if topology == "primary":
        return "primary"
    branch = claim.get("branch")
    if branch:
        return str(branch)
    return "linked" if topology == "linked" else None


def _event(
    action: str,
    outcome: str,
    args: argparse.Namespace,
    claim: dict[str, Any] | None = None,
    requested_scope: dict[str, Any] | None = None,
    conflicts: list[dict[str, Any]] | None = None,
    **extra: Any,
) -> dict[str, Any]:
    event = {
        "schema_version": EVENT_SCHEMA_VERSION,
        "event_id": str(uuid4()),
        "timestamp": _timestamp(),
        "action": action,
        "outcome": outcome,
        "claim_id": _bounded_identifier(getattr(args, "claim_id", None)),
        "incarnation_id": claim.get("incarnation_id") if claim else None,
        "root_task_id": _bounded_identifier(
            claim.get("root_task_id") if claim else getattr(args, "root_task_id", None)
        ),
        "parent_claim_id": _bounded_identifier(
            claim.get("parent_claim_id") if claim else getattr(args, "parent_claim_id", None)
        ),
        "agent": _bounded_identifier(claim.get("agent") if claim else getattr(args, "agent", None)),
        "mode": claim.get("mode") if claim else None,
        "scopes": _claim_scope(claim) if claim else None,
        "requested_scopes": requested_scope,
        "conflicting_claim_ids": [item["claim_id"] for item in conflicts or []],
        "overlaps": [
            {"claim_id": item["claim_id"], **overlap}
            for item in conflicts or []
            for overlap in item["overlaps"]
        ],
        "branch": claim.get("branch") if claim else None,
        "checkout_topology": _checkout_topology(claim) if claim else None,
        "worktree_id": _worktree_identifier(claim) if claim else None,
        "baseline_commit": claim.get("baseline_commit") if claim else None,
        "deadline": claim.get("deadline") if claim else None,
        "resulting_commit": extra.pop("resulting_commit", None),
        "command_warnings": extra.pop("command_warnings", []),
        "journal_warnings": [],
    }
    event.update(extra)
    return event


def _canonical_outcome(outcome: str, shared_checkout_claimed: bool = False) -> str:
    if outcome == "PRIMARY_REQUIRED" and shared_checkout_claimed:
        return "SHARED_CHECKOUT_RELEASE_REQUIRED"
    return LEGACY_OUTCOME_ALIASES.get(outcome, outcome)


def _normalized_event_outcomes(
    events: Sequence[dict[str, Any]],
) -> tuple[list[str], list[dict[str, str]]]:
    normalized: list[str] = []
    gaps: list[dict[str, str]] = []
    for event in sorted(events, key=_event_sort_key):
        event_id = str(event.get("event_id") or "")
        raw_outcome = str(event.get("outcome"))
        if raw_outcome == "PRIMARY_REQUIRED":
            shared_checkout_claimed = event.get("shared_checkout_claimed")
            if isinstance(shared_checkout_claimed, bool):
                outcome = _canonical_outcome(raw_outcome, shared_checkout_claimed)
            else:
                outcome = raw_outcome
                gaps.append(
                    {
                        "source": event_id,
                        "detail": (
                            "legacy PRIMARY_REQUIRED lacks deterministic "
                            "shared-checkout ownership evidence"
                        ),
                    }
                )
        else:
            outcome = _canonical_outcome(raw_outcome)
        normalized.append(outcome)
    return normalized, gaps


def _append_event(common_directory: Path, event: dict[str, Any]) -> Path:
    if os.environ.get("AGENT_CLAIM_TEST_FAIL_JOURNAL_WRITE") == "1":
        raise OSError("simulated journal write failure")
    _root, hot_directory, _archive, _journal = _journal_paths(common_directory)
    hot_directory.mkdir(parents=True, exist_ok=True)
    day = _parse_timestamp(event["timestamp"]).date().isoformat()
    path = hot_directory / f"{day}.jsonl"
    encoded = (json.dumps(event, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
    descriptor = os.open(path, os.O_APPEND | os.O_CREAT | os.O_WRONLY, 0o600)
    try:
        os.write(descriptor, encoded)
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    return path


def _reconciliation_journal_state(
    common_directory: Path,
    event: dict[str, Any],
) -> tuple[Path, bytes, bytes, bytes, bool]:
    _root, hot_directory, _archive, _journal = _journal_paths(common_directory)
    hot_directory.mkdir(parents=True, exist_ok=True)
    day = _parse_timestamp(event["timestamp"]).date().isoformat()
    path = hot_directory / f"{day}.jsonl"
    existed = path.exists()
    prior_bytes = path.read_bytes() if existed else b""
    event_bytes = (
        json.dumps(event, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("utf-8")
    pending_event = {
        **event,
        "outcome": "RELEASE_PENDING",
        "reconciliation_transaction_state": "prepared",
    }
    pending_event_bytes = (
        json.dumps(pending_event, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("utf-8")
    return (
        path,
        prior_bytes,
        prior_bytes + pending_event_bytes,
        prior_bytes + event_bytes,
        existed,
    )


def _append_reconciliation_event(path: Path, replacement_bytes: bytes) -> Path:
    faults = {
        "write": "AGENT_CLAIM_TEST_FAIL_JOURNAL_WRITE",
        "short_write": "AGENT_CLAIM_TEST_SHORT_RECONCILIATION_JOURNAL_WRITE",
        "after_write": "AGENT_CLAIM_TEST_FAIL_RECONCILIATION_JOURNAL_AFTER_WRITE",
        "fsync": "AGENT_CLAIM_TEST_FAIL_RECONCILIATION_JOURNAL_FSYNC",
        "replace": "AGENT_CLAIM_TEST_FAIL_RECONCILIATION_JOURNAL_REPLACE",
        "directory_fsync": (
            "AGENT_CLAIM_TEST_FAIL_RECONCILIATION_JOURNAL_DIRECTORY_FSYNC"
        ),
    }
    _durable_atomic_replace(path, replacement_bytes, faults=faults)
    return path


def _finalize_reconciliation_event(path: Path, released_bytes: bytes) -> Path:
    faults = {
        "write": "AGENT_CLAIM_TEST_FAIL_RECONCILIATION_FINAL_JOURNAL_WRITE",
        "short_write": (
            "AGENT_CLAIM_TEST_SHORT_RECONCILIATION_FINAL_JOURNAL_WRITE"
        ),
        "after_write": (
            "AGENT_CLAIM_TEST_FAIL_RECONCILIATION_FINAL_JOURNAL_AFTER_WRITE"
        ),
        "fsync": "AGENT_CLAIM_TEST_FAIL_RECONCILIATION_FINAL_JOURNAL_FSYNC",
        "replace": "AGENT_CLAIM_TEST_FAIL_RECONCILIATION_FINAL_JOURNAL_REPLACE",
        "directory_fsync": (
            "AGENT_CLAIM_TEST_FAIL_RECONCILIATION_FINAL_JOURNAL_DIRECTORY_FSYNC"
        ),
    }
    _durable_atomic_replace(path, released_bytes, faults=faults)
    return path


def _print_result(
    outcome: str,
    *,
    canonical_outcome: str | None = None,
    **details: Any,
) -> None:
    result_outcome = canonical_outcome or _canonical_outcome(outcome)
    result = {
        "schema_version": RESULT_SCHEMA_VERSION,
        "outcome": result_outcome,
        **details,
    }
    if result_outcome != outcome:
        result["legacy_outcome"] = outcome
    print(json.dumps(result, indent=2, sort_keys=True))


def _journaled_result(
    code: int,
    common_directory: Path,
    event: dict[str, Any],
    output_warnings: list[dict[str, str]] | None = None,
    canonical_outcome: str | None = None,
    **details: Any,
) -> int:
    warnings = list(output_warnings or [])
    try:
        path = _append_event(common_directory, event)
        journal = {"event_id": event["event_id"], "path": str(path)}
    except OSError as error:
        warning = {"code": "journal_write_failed", "message": str(error)}
        warnings.append(warning)
        journal = {"event_id": event["event_id"], "persisted": False}
    if warnings:
        details["warnings"] = warnings
    _print_result(
        event["outcome"],
        canonical_outcome=canonical_outcome,
        journal=journal,
        **details,
    )
    return code


def _invalid_scope_result(
    common_directory: Path,
    action: str,
    args: argparse.Namespace,
    error: _ScopeError,
) -> int:
    event = _event(
        action,
        "INVALID_SCOPE",
        args,
        rejection={
            "message": str(error),
            "offending_scope": error.offending_scope,
            "replacement": error.replacement,
            "reason": error.reason,
        },
    )
    return _journaled_result(
        ERROR,
        common_directory,
        event,
        message=str(error),
        offending_scope=error.offending_scope,
        replacement=error.replacement,
        rejection=event["rejection"],
    )


def _invalid_deadline_result(
    common_directory: Path,
    action: str,
    args: argparse.Namespace,
    error: _DeadlineError,
    claim: dict[str, Any] | None = None,
) -> int:
    outcome = "INVALID_DEADLINE_EXTENSION" if action == "extend-deadline" else "INVALID_DEADLINE_POLICY"
    event = _event(
        action,
        outcome,
        args,
        claim=claim,
        rejection={
            "message": str(error),
            "field": error.field,
            "reason": error.reason,
        },
    )
    return _journaled_result(
        ERROR,
        common_directory,
        event,
        message=str(error),
        field=error.field,
        rejection=event["rejection"],
    )


def _primary_required_result(
    common_directory: Path,
    action: str,
    args: argparse.Namespace,
    requested_scope: dict[str, Any],
    scope_warnings: list[dict[str, str]],
    claim: dict[str, Any] | None = None,
    **details: Any,
) -> int:
    reason = "backlog_requires_primary_worktree"
    message = "Backlog scope is available only from the primary worktree."
    event = _event(
        action,
        "PRIMARY_REQUIRED",
        args,
        claim=claim,
        requested_scope=requested_scope,
        reason=reason,
        shared_checkout_claimed=False,
        command_warnings=scope_warnings,
        **details,
    )
    return _journaled_result(
        COORDINATION_REQUIRED_EXIT_CODE,
        common_directory,
        event,
        scope_warnings,
        canonical_outcome=_canonical_outcome(
            event["outcome"],
            shared_checkout_claimed=False,
        ),
        reason=reason,
        message=message,
        requested_scopes=requested_scope,
        **details,
    )


def _invalid_identifier_result(common_directory: Path, args: argparse.Namespace) -> int:
    message = "claim_id must be one portable path component containing only letters, digits, dots, underscores, or hyphens."
    event = _event(
        "acquire",
        "INVALID_IDENTIFIER",
        args,
        field="claim_id",
        reason="claim_id_not_portable_path_component",
    )
    return _journaled_result(
        ERROR,
        common_directory,
        event,
        field="claim_id",
        message=message,
    )


def _invalid_worktree_path_result(
    common_directory: Path,
    args: argparse.Namespace,
    expected_worktree: Path,
    provided_worktree: Path,
) -> int:
    event = _event(
        "acquire",
        "INVALID_WORKTREE_PATH",
        args,
        reason="worktree_path_not_canonical",
    )
    return _journaled_result(
        ERROR,
        common_directory,
        event,
        expected_worktree=str(expected_worktree),
        provided_worktree=str(provided_worktree),
        message="The worktree path must match the canonical target under the primary worktree.",
    )


def _worktree_root_not_ignored_result(
    common_directory: Path,
    args: argparse.Namespace,
    worktree_root: Path,
) -> int:
    event = _event(
        "acquire",
        "WORKTREE_ROOT_NOT_IGNORED",
        args,
        reason="canonical_worktree_root_not_ignored",
    )
    return _journaled_result(
        ERROR,
        common_directory,
        event,
        worktree_root=str(worktree_root),
        required_ignore_pattern=WORKTREE_IGNORE_PATTERN,
        message="Ignore the canonical worktree root before creating an isolated worktree.",
    )


def _acquire(args: argparse.Namespace) -> int:
    repository = _repository_root(Path(args.repo).resolve())
    with _locked_registry(repository) as (registry_path, data):
        common_directory = registry_path.parent
        try:
            requested_scope, scope_warnings = _scope_from_args(args, repository)
        except _ScopeError as error:
            return _invalid_scope_result(common_directory, "acquire", args, error)
        try:
            deadline_request = _deadline_request_from_args(
                args,
                requested_scope["resources"],
                repository,
            )
        except _DeadlineError as error:
            return _invalid_deadline_result(common_directory, "acquire", args, error)
        if not _claim_id_is_safe_worktree_component(args.claim_id):
            return _invalid_identifier_result(common_directory, args)

        claims: list[dict[str, Any]] = data["claims"]
        if any(claim.get("claim_id") == args.claim_id for claim in claims):
            event = _event("acquire", "CLAIM_ID_EXISTS", args, requested_scope=requested_scope)
            return _journaled_result(ERROR, common_directory, event, claim_id=args.claim_id)

        conflicts = _conflicts(claims, requested_scope)
        if conflicts:
            event = _event(
                "acquire",
                "WAIT",
                args,
                requested_scope=requested_scope,
                conflicts=conflicts,
                command_warnings=scope_warnings,
            )
            return _journaled_result(
                COORDINATION_REQUIRED_EXIT_CODE,
                common_directory,
                event,
                scope_warnings,
                conflicting_claim_ids=[item["claim_id"] for item in conflicts],
                overlaps=event["overlaps"],
            )

        requires_primary = _scope_requires_primary_worktree(requested_scope)
        if requires_primary:
            primary_worktree = _primary_worktree(repository)
            caller_is_primary = repository == primary_worktree
            if not caller_is_primary:
                return _primary_required_result(
                    common_directory,
                    "acquire",
                    args,
                    requested_scope,
                    scope_warnings,
                    active_claim_count=len(claims),
                )

        if args.branch and not requires_primary:
            worktree_root = _canonical_worktree_root(repository)
            target_worktree = _canonical_worktree(repository, args.claim_id)
            if args.worktree_path:
                provided_worktree = Path(args.worktree_path).resolve()
                if provided_worktree != target_worktree:
                    return _invalid_worktree_path_result(
                        common_directory,
                        args,
                        target_worktree,
                        provided_worktree,
                    )
            if not _worktree_root_is_ignored(repository):
                return _worktree_root_not_ignored_result(common_directory, args, worktree_root)
            failure_reason = _create_isolated_worktree(
                repository,
                target_worktree,
                args.branch,
                args.base,
            )
            if failure_reason is not None:
                event = _event(
                    "acquire",
                    "WORKTREE_CREATE_FAILED",
                    args,
                    requested_scope=requested_scope,
                    reason=failure_reason,
                )
                return _journaled_result(ERROR, common_directory, event, message="Git worktree creation failed.")
            mode = "isolated"
            outcome = "ISOLATE"
        else:
            target_worktree = repository
            initial_snapshot = _status_snapshot(target_worktree)
            initial_status = _status_for_domain(
                initial_snapshot,
                requested_scope["file_domain"],
                resource_only=_scope_is_resource_only(requested_scope),
            )
            if initial_status and not args.allow_recovery:
                event = _event(
                    "acquire",
                    "RECOVERY_REQUIRED",
                    args,
                    requested_scope=requested_scope,
                    dirty_paths=_status_paths(initial_status),
                    command_warnings=scope_warnings,
                )
                return _journaled_result(
                    RECOVERY_AUTHORIZATION_EXIT_CODE,
                    common_directory,
                    event,
                    scope_warnings,
                    dirty_status=initial_status,
                )
            mode = "recovery" if initial_status else "primary"
            outcome = "RECOVER" if initial_status else "PRIMARY"

        baseline_snapshot = _status_snapshot(target_worktree)
        baseline_state = _status_state(target_worktree, baseline_snapshot)
        now = _timestamp()
        deadline = (
            _deadline_from_request(deadline_request, now)
            if deadline_request is not None
            else None
        )
        claim = {
            "agent": args.agent,
            "backlog": requested_scope["backlog"],
            "all_files": requested_scope["all_files"],
            "baseline_commit": _head(target_worktree),
            "baseline_status": _status_for_domain(
                baseline_snapshot,
                requested_scope["file_domain"],
                resource_only=_scope_is_resource_only(requested_scope),
            ),
            "baseline_out_of_domain_status": _status_outside_domain(
                baseline_snapshot,
                requested_scope["file_domain"],
            ),
            "baseline_out_of_domain_state": _state_outside_domain(
                baseline_state,
                requested_scope["file_domain"],
            ),
            "branch": _branch(target_worktree),
            "checkout_topology": (
                "primary"
                if target_worktree == _primary_worktree(repository)
                else "linked"
            ),
            "claim_id": args.claim_id,
            "claimed_at": now,
            "incarnation_id": str(uuid4()),
            "files": requested_scope["files"],
            "file_domain": requested_scope["file_domain"],
            "heartbeat": now,
            "mode": mode,
            "parent_claim_id": args.parent_claim_id,
            "project_files": requested_scope["project_files"],
            "resources": requested_scope["resources"],
            "root_task_id": args.root_task_id,
            "scope_reasons": _scope_reasons(requested_scope),
            "task": args.task,
            "trees": requested_scope["trees"],
            "worktree": str(target_worktree),
        }
        if deadline is not None:
            claim["deadline"] = deadline
        claims.append(claim)
        _write_registry(registry_path, data)
        event = _event(
            "acquire",
            outcome,
            args,
            claim=claim,
            requested_scope=requested_scope,
            command_warnings=scope_warnings,
        )
        return _journaled_result(
            SUCCESS,
            common_directory,
            event,
            scope_warnings,
            claim=claim,
            registry=str(registry_path),
            target={
                "mode": mode,
                "branch": claim["branch"],
                "checkout_topology": claim["checkout_topology"],
                "worktree": str(target_worktree),
            },
        )


def _extend(args: argparse.Namespace) -> int:
    repository = _repository_root(Path(args.repo).resolve())
    with _locked_registry(repository) as (registry_path, data):
        common_directory = registry_path.parent
        try:
            requested_scope, scope_warnings = _scope_from_args(args, repository)
        except _ScopeError as error:
            return _invalid_scope_result(common_directory, "extend", args, error)
        claims: list[dict[str, Any]] = data["claims"]
        claim = next((item for item in claims if item.get("claim_id") == args.claim_id), None)
        if claim is None:
            event = _event("extend", "CLAIM_NOT_FOUND", args, requested_scope=requested_scope)
            return _journaled_result(ERROR, common_directory, event, claim_id=args.claim_id)

        current_resources = [str(resource) for resource in claim.get("resources", [])]
        requested_resources = requested_scope["resources"]
        if requested_resources and current_resources and requested_resources != current_resources:
            error = _DeadlineError(
                "A claim that owns one named resource cannot add a second named resource.",
                "resource",
                "second_resource_not_supported",
            )
            return _invalid_deadline_result(common_directory, "extend", args, error, claim)
        try:
            deadline_request = _deadline_request_from_args(
                args,
                requested_resources,
                repository,
            )
        except _DeadlineError as error:
            return _invalid_deadline_result(common_directory, "extend", args, error, claim)
        if requested_resources and current_resources and not isinstance(claim.get("deadline"), dict):
            error = _DeadlineError(
                "The existing named resource has no complete timing evidence.",
                "deadline",
                "resource_timing_missing",
            )
            return _invalid_deadline_result(common_directory, "extend", args, error, claim)

        if claim.get("mode") == "isolated" and requested_scope.get("file_domain") in {
            "backlog",
            "all_files",
        }:
            return _primary_required_result(
                common_directory,
                "extend",
                args,
                requested_scope,
                scope_warnings,
                claim=claim,
            )

        try:
            already_owned, added = _owned_and_added_scope(claim, requested_scope)
        except _ScopeError as error:
            return _invalid_scope_result(common_directory, "extend", args, error)
        conflicts = _conflicts(claims, added, excluded_claim_id=args.claim_id) if _scope_has_values(added) else []
        if conflicts:
            event = _event(
                "extend",
                "WAIT",
                args,
                claim=claim,
                requested_scope=requested_scope,
                conflicts=conflicts,
                added_scope=added,
                already_owned_scope=already_owned,
                command_warnings=scope_warnings,
            )
            return _journaled_result(
                COORDINATION_REQUIRED_EXIT_CODE,
                common_directory,
                event,
                scope_warnings,
                conflicting_claim_ids=[item["claim_id"] for item in conflicts],
                overlaps=event["overlaps"],
                added_scope=added,
                already_owned_scope=already_owned,
            )

        if claim.get("mode") == "isolated" and _scope_requires_primary_worktree(added):
            return _primary_required_result(
                common_directory,
                "extend",
                args,
                requested_scope,
                scope_warnings,
                claim=claim,
                added_scope=added,
                already_owned_scope=already_owned,
            )

        if _scope_has_values(added):
            _apply_scope(claim, added)
            if added["resources"]:
                if deadline_request is None:
                    raise RuntimeError("Timed resource validation did not produce deadline evidence.")
                claim["deadline"] = _deadline_from_request(deadline_request, _timestamp())
            _write_registry(registry_path, data)
        event = _event(
            "extend",
            "EXTENDED",
            args,
            claim=claim,
            requested_scope=requested_scope,
            added_scope=added,
            already_owned_scope=already_owned,
            command_warnings=scope_warnings,
        )
        return _journaled_result(
            SUCCESS,
            common_directory,
            event,
            scope_warnings,
            claim=claim,
            added_scope=added,
            already_owned_scope=already_owned,
        )


def _heartbeat(args: argparse.Namespace) -> int:
    repository = _repository_root(Path(args.repo).resolve())
    with _locked_registry(repository) as (registry_path, data):
        common_directory = registry_path.parent
        for claim in data["claims"]:
            if claim.get("claim_id") == args.claim_id:
                claim["heartbeat"] = _timestamp()
                _write_registry(registry_path, data)
                event = _event("heartbeat", "HEARTBEAT", args, claim=claim)
                return _journaled_result(SUCCESS, common_directory, event, claim=claim)
        event = _event("heartbeat", "CLAIM_NOT_FOUND", args)
        return _journaled_result(ERROR, common_directory, event, claim_id=args.claim_id)


def _extend_deadline(args: argparse.Namespace) -> int:
    repository = _repository_root(Path(args.repo).resolve())
    with _locked_registry(repository) as (registry_path, data):
        common_directory = registry_path.parent
        claim = next(
            (item for item in data["claims"] if item.get("claim_id") == args.claim_id),
            None,
        )
        if claim is None:
            event = _event("extend-deadline", "CLAIM_NOT_FOUND", args)
            return _journaled_result(ERROR, common_directory, event, claim_id=args.claim_id)
        deadline = claim.get("deadline")
        if not isinstance(deadline, dict):
            error = _DeadlineError(
                "claim has no configured resource deadline to extend.",
                "claim_id",
                "deadline_not_configured",
            )
            return _invalid_deadline_result(
                common_directory,
                "extend-deadline",
                args,
                error,
                claim,
            )

        requested = args.requested_hard_stop_duration_seconds
        current = deadline["requested_hard_stop_duration_seconds"]
        maximum = deadline["configured_maximum_duration_seconds"]
        evidence = args.extension_evidence.strip()
        if requested <= current:
            error = _DeadlineError(
                "extended hard stop must be greater than the current requested hard stop.",
                "requested_hard_stop_duration_seconds",
                "hard_stop_not_extended",
            )
            return _invalid_deadline_result(common_directory, "extend-deadline", args, error, claim)
        if requested > maximum:
            error = _DeadlineError(
                "extended hard stop must not exceed configured maximum.",
                "requested_hard_stop_duration_seconds",
                "hard_stop_exceeds_maximum",
            )
            return _invalid_deadline_result(common_directory, "extend-deadline", args, error, claim)
        if not evidence or len(evidence) > MAX_EXTENSION_EVIDENCE_LENGTH:
            error = _DeadlineError(
                f"extension evidence must contain 1 to {MAX_EXTENSION_EVIDENCE_LENGTH} characters.",
                "extension_evidence",
                "invalid_extension_evidence",
            )
            return _invalid_deadline_result(common_directory, "extend-deadline", args, error, claim)

        extended_at = _timestamp()
        acquired_at = _parse_timestamp(str(deadline["acquired_at"]))
        hard_stop_at = acquired_at + timedelta(seconds=requested)
        extension = {
            "extended_at": extended_at,
            "previous_requested_hard_stop_duration_seconds": current,
            "requested_hard_stop_duration_seconds": requested,
            "evidence": evidence,
        }
        deadline["requested_hard_stop_duration_seconds"] = requested
        deadline["hard_stop_at"] = _format_timestamp(hard_stop_at)
        deadline["cleanup_grace_ends_at"] = _format_timestamp(
            hard_stop_at + timedelta(seconds=deadline["cleanup_grace_seconds"])
        )
        deadline.setdefault("extensions", []).append(extension)
        _write_registry(registry_path, data)
        event = _event(
            "extend-deadline",
            "DEADLINE_EXTENDED",
            args,
            claim=claim,
            deadline_extension=extension,
        )
        return _journaled_result(
            SUCCESS,
            common_directory,
            event,
            claim=claim,
            deadline_extension=extension,
        )


def _event_sequences(
    common_directory: Path,
) -> tuple[list[tuple[str, list[dict[str, Any]]]], list[dict[str, str]]]:
    """Load each physical journal in line order without trusting event clocks."""
    _root, hot_directory, archive_directory, _journal = _journal_paths(common_directory)
    coverage_gaps: list[dict[str, str]] = []
    sequences: list[tuple[str, list[dict[str, Any]]]] = []
    hot_paths = sorted(hot_directory.glob("*.jsonl")) if hot_directory.exists() else []
    archive_paths = (
        sorted(archive_directory.glob("**/*.jsonl.gz"))
        if archive_directory.exists()
        else []
    )
    daily_paths = sorted(
        [*archive_paths, *hot_paths],
        key=lambda path: (path.name.split(".jsonl", 1)[0], str(path)),
    )
    for path in daily_paths:
        source = str(path)
        try:
            raw = (
                gzip.decompress(path.read_bytes())
                if path.suffix == ".gz"
                else path.read_bytes()
            )
            sequences.append((source, _read_jsonl(raw, source, coverage_gaps)))
        except (OSError, EOFError) as error:
            coverage_gaps.append({"source": source, "detail": str(error)})
    return sequences, coverage_gaps


def _claim_facts_match(event: dict[str, Any], claim: dict[str, Any]) -> bool:
    expected = {
        "claim_id": claim.get("claim_id"),
        "root_task_id": _bounded_identifier(claim.get("root_task_id")),
        "parent_claim_id": _bounded_identifier(claim.get("parent_claim_id")),
        "agent": _bounded_identifier(claim.get("agent")),
        "mode": claim.get("mode"),
        "scopes": _claim_scope(claim),
        "branch": claim.get("branch"),
        "checkout_topology": _checkout_topology(claim),
        "worktree_id": _worktree_identifier(claim),
        "baseline_commit": claim.get("baseline_commit"),
    }
    return all(event.get(key) == value for key, value in expected.items())


def _legacy_claim_segments(
    sequences: Sequence[tuple[str, list[dict[str, Any]]]],
    claim_id: str,
) -> list[dict[str, Any]]:
    acquisition_outcomes = {
        "SHARED_CHECKOUT_ACQUIRED",
        "ISOLATED_CHECKOUT_ACQUIRED",
        "DIRTY_CHECKOUT_RECOVERY_ACQUIRED",
    }
    segments: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    for source, events in sequences:
        for event in events:
            if event.get("claim_id") != claim_id:
                continue
            is_acquisition = (
                event.get("action") == "acquire"
                and _canonical_outcome(str(event.get("outcome"))) in acquisition_outcomes
            )
            if is_acquisition:
                if current is not None:
                    segments.append(current)
                current = {
                    "source": source,
                    "acquisition": event,
                    "events": [event],
                    "released": False,
                }
                continue
            if current is None:
                continue
            current["events"].append(event)
            if event.get("action") == "release" and event.get("outcome") == "RELEASED":
                current["released"] = True
                segments.append(current)
                current = None
    if current is not None:
        segments.append(current)
    return segments


def _resolve_reconciliation_incarnation(
    common_directory: Path,
    claim: dict[str, Any],
    prior_reference: str,
) -> tuple[dict[str, Any], dict[str, str]]:
    sequences, coverage_gaps = _event_sequences(common_directory)
    claim_id = str(claim.get("claim_id") or "")
    incarnation_id = claim.get("incarnation_id")
    if incarnation_id is None:
        if coverage_gaps:
            raise _ReleaseReconciliationError(
                "Legacy claim incarnation resolution requires valid complete journal sequences.",
                "reconciliation_legacy_journal_invalid",
                journal_coverage_gaps=coverage_gaps,
            )
        relevant_event_ids: set[str] = set()
        duplicate_event_ids: set[str] = set()
        for _source, events in sequences:
            for event in events:
                if event.get("claim_id") != claim_id:
                    continue
                event_id = event.get("event_id")
                if not isinstance(event_id, str) or not event_id:
                    continue
                if event_id in relevant_event_ids:
                    duplicate_event_ids.add(event_id)
                relevant_event_ids.add(event_id)
        if duplicate_event_ids:
            raise _ReleaseReconciliationError(
                "Legacy claim history reuses an event identifier across lifecycle segments.",
                "reconciliation_legacy_duplicate_event_id",
                duplicate_event_ids=sorted(duplicate_event_ids),
            )
    prior_matches = [
        (source, index, event)
        for source, events in sequences
        for index, event in enumerate(events)
        if event.get("event_id") == prior_reference
    ]
    if len(prior_matches) > 1:
        raise _ReleaseReconciliationError(
            "The prior rejected release event reference is ambiguous.",
            "reconciliation_prior_rejection_ambiguous",
            prior_rejected_release_reference=prior_reference,
        )
    if not prior_matches:
        raise _ReleaseReconciliationError(
            "The prior rejected release event reference was not found.",
            "reconciliation_prior_rejection_not_found",
            prior_rejected_release_reference=prior_reference,
        )
    _prior_source, _prior_index, prior_event = prior_matches[0]

    if incarnation_id is not None:
        if not isinstance(incarnation_id, str) or not incarnation_id:
            raise _ReleaseReconciliationError(
                "The active claim has an invalid immutable incarnation identifier.",
                "reconciliation_claim_incarnation_invalid",
            )
        if prior_event.get("incarnation_id") != incarnation_id:
            raise _ReleaseReconciliationError(
                "The referenced rejection belongs to another claim incarnation.",
                "reconciliation_claim_incarnation_mismatch",
                prior_rejected_release_reference=prior_reference,
            )
        return prior_event, {"id": incarnation_id, "source": "registry"}

    segments = _legacy_claim_segments(sequences, claim_id)
    prior_segments = [
        segment
        for segment in segments
        if any(event is prior_event for event in segment["events"])
    ]
    if len(prior_segments) != 1:
        reason = (
            "reconciliation_legacy_incarnation_ambiguous"
            if len(prior_segments) > 1
            else "reconciliation_legacy_incarnation_unresolvable"
        )
        raise _ReleaseReconciliationError(
            "The referenced legacy rejection does not resolve to one acquisition event.",
            reason,
            prior_rejected_release_reference=prior_reference,
        )
    active_segments = []
    for segment in segments:
        if segment["released"]:
            continue
        fact_events = [
            event
            for event in reversed(segment["events"])
            if isinstance(event.get("scopes"), dict)
        ]
        if fact_events and _claim_facts_match(fact_events[0], claim):
            active_segments.append(segment)
    if len(active_segments) != 1:
        reason = (
            "reconciliation_legacy_incarnation_ambiguous"
            if len(active_segments) > 1
            else "reconciliation_legacy_incarnation_unresolvable"
        )
        raise _ReleaseReconciliationError(
            "The active legacy claim does not resolve to one acquisition event.",
            reason,
        )
    prior_acquisition_id = prior_segments[0]["acquisition"].get("event_id")
    active_acquisition_id = active_segments[0]["acquisition"].get("event_id")
    if (
        not isinstance(prior_acquisition_id, str)
        or not prior_acquisition_id
        or not isinstance(active_acquisition_id, str)
        or not active_acquisition_id
    ):
        raise _ReleaseReconciliationError(
            "Legacy claim acquisition identity is missing.",
            "reconciliation_legacy_incarnation_unresolvable",
        )
    if prior_acquisition_id != active_acquisition_id:
        raise _ReleaseReconciliationError(
            "The referenced legacy rejection belongs to another claim incarnation.",
            "reconciliation_legacy_incarnation_mismatch",
            active_acquisition_event_id=active_acquisition_id,
            prior_acquisition_event_id=prior_acquisition_id,
            prior_rejected_release_reference=prior_reference,
        )
    return prior_event, {
        "id": active_acquisition_id,
        "source": "legacy_acquisition_event",
    }


def _release_reconciliation_evidence(
    common_directory: Path,
    worktree: Path,
    claim: dict[str, Any],
    changed_paths: list[str],
    outside_status: list[dict[str, str]],
    args: argparse.Namespace,
) -> dict[str, Any]:
    file_domain = str(claim.get("file_domain") or _legacy_file_domain(claim))
    scope = _claim_scope(claim)
    if claim.get("mode") != "primary" or file_domain not in {"project_files", "backlog"}:
        raise _ReleaseReconciliationError(
            "Release reconciliation requires an active primary claim with one scoped file domain.",
            "reconciliation_requires_primary_scoped_claim",
        )
    if not isinstance(claim.get("baseline_out_of_domain_state"), dict):
        raise _ReleaseReconciliationError(
            "Release reconciliation requires a trustworthy out-of-domain acquisition baseline.",
            "reconciliation_baseline_missing",
        )
    if scope["resources"]:
        raise _ReleaseReconciliationError(
            "Release reconciliation cannot release a claim that still owns resources.",
            "reconciliation_resources_present",
            resources=scope["resources"],
        )
    if outside_status:
        raise _ReleaseReconciliationError(
            "Release reconciliation requires a clean current out-of-domain worktree and index.",
            "reconciliation_out_of_domain_not_clean",
            current_out_of_domain_status=outside_status,
        )
    if not changed_paths:
        raise _ReleaseReconciliationError(
            "Release reconciliation requires baseline-vs-current out-of-domain changes.",
            "reconciliation_paths_missing",
        )

    peer_commit = args.reconcile_out_of_domain_commit
    baseline_commit = str(claim.get("baseline_commit") or "")
    resulting_commit = _head(worktree)
    commit_exists = _git(
        worktree,
        "cat-file",
        "-e",
        f"{peer_commit}^{{commit}}",
        check=False,
    )
    if commit_exists.returncode != SUCCESS:
        raise _ReleaseReconciliationError(
            "The supplied peer commit does not resolve to a commit.",
            "reconciliation_commit_not_found",
            peer_commit=peer_commit,
        )
    baseline_before_peer = _git(
        worktree,
        "merge-base",
        "--is-ancestor",
        baseline_commit,
        peer_commit,
        check=False,
    )
    if peer_commit == baseline_commit or baseline_before_peer.returncode != SUCCESS:
        raise _ReleaseReconciliationError(
            "The supplied peer commit must be strictly after the claim baseline.",
            "reconciliation_commit_not_after_baseline",
            baseline_commit=baseline_commit,
            peer_commit=peer_commit,
        )
    peer_before_head = _git(
        worktree,
        "merge-base",
        "--is-ancestor",
        peer_commit,
        resulting_commit,
        check=False,
    )
    if peer_before_head.returncode != SUCCESS:
        raise _ReleaseReconciliationError(
            "The supplied peer commit must be an ancestor of the current HEAD.",
            "reconciliation_commit_not_ancestor_of_head",
            peer_commit=peer_commit,
            resulting_commit=resulting_commit,
        )

    peer_paths = _commit_changed_paths(worktree, peer_commit)
    claimed_peer_paths = [
        path for path in peer_paths if _path_belongs_to_domain(path, file_domain)
    ]
    if claimed_peer_paths:
        raise _ReleaseReconciliationError(
            "The supplied peer commit changes paths inside the claim's file domain.",
            "reconciliation_commit_changed_claimed_domain",
            claimed_domain_paths=claimed_peer_paths,
            peer_commit_paths=peer_paths,
        )
    if peer_paths != changed_paths:
        raise _ReleaseReconciliationError(
            "The supplied peer commit must change exactly the reconciled out-of-domain paths.",
            "reconciliation_commit_paths_mismatch",
            peer_commit_paths=peer_paths,
            reconciled_out_of_domain_paths=changed_paths,
        )
    current_tree_matches = _git(
        worktree,
        "diff",
        "--quiet",
        peer_commit,
        resulting_commit,
        "--",
        *changed_paths,
        check=False,
    )
    if current_tree_matches.returncode != SUCCESS:
        raise _ReleaseReconciliationError(
            "The current tree must match the supplied peer commit for every reconciled path.",
            "reconciliation_current_tree_mismatch",
            peer_commit=peer_commit,
            reconciled_out_of_domain_paths=changed_paths,
        )

    prior_reference = args.prior_rejected_release_reference
    if not prior_reference:
        raise _ReleaseReconciliationError(
            "Release reconciliation requires the prior rejected release event reference.",
            "reconciliation_prior_rejection_required",
        )
    prior_event, claim_incarnation = _resolve_reconciliation_incarnation(
        common_directory,
        claim,
        prior_reference,
    )
    expected_prior_evidence = {
        "action": "release",
        "outcome": "RELEASE_REJECTED",
        "claim_id": claim.get("claim_id"),
        "root_task_id": _bounded_identifier(claim.get("root_task_id")),
        "parent_claim_id": _bounded_identifier(claim.get("parent_claim_id")),
        "agent": _bounded_identifier(claim.get("agent")),
        "mode": claim.get("mode"),
        "scopes": _claim_scope(claim),
        "branch": claim.get("branch"),
        "checkout_topology": _checkout_topology(claim),
        "worktree_id": _worktree_identifier(claim),
        "reason": "out_of_domain_changes",
        "baseline_commit": baseline_commit,
        "out_of_domain_paths": changed_paths,
    }
    if any(prior_event.get(key) != value for key, value in expected_prior_evidence.items()):
        raise _ReleaseReconciliationError(
            "The referenced event does not prove the matching rejected release.",
            "reconciliation_prior_rejection_mismatch",
            prior_rejected_release_reference=prior_reference,
        )

    return {
        "baseline_commit": baseline_commit,
        "baseline_status": claim.get("baseline_status", []),
        "baseline_out_of_domain_status": claim.get("baseline_out_of_domain_status", []),
        "baseline_out_of_domain_state": claim["baseline_out_of_domain_state"],
        "peer_commit": peer_commit,
        "reconciled_out_of_domain_paths": changed_paths,
        "prior_rejected_release_reference": prior_reference,
        "claim_incarnation": claim_incarnation,
    }


def _release(args: argparse.Namespace) -> int:
    repository = _repository_root(Path(args.repo).resolve())
    with _locked_registry(repository) as (registry_path, data):
        common_directory = registry_path.parent
        claims: list[dict[str, Any]] = data["claims"]
        for index, claim in enumerate(claims):
            if claim.get("claim_id") != args.claim_id:
                continue
            worktree = Path(claim["worktree"])
            current_snapshot = _status_snapshot(worktree)
            file_domain = str(claim.get("file_domain") or _legacy_file_domain(claim))
            compatibility: dict[str, Any] | None = None
            complete_worktree_release = (
                "file_domain" not in claim
                or not isinstance(claim.get("baseline_out_of_domain_state"), dict)
            )
            if complete_worktree_release:
                compatibility = {
                    "release_policy": "complete_worktree",
                    "legacy_registry_claim": "file_domain" not in claim,
                    "missing_out_of_domain_baseline": not isinstance(
                        claim.get("baseline_out_of_domain_state"),
                        dict,
                    ),
                }
            owned_status = _status_for_domain(
                current_snapshot,
                "all_files" if complete_worktree_release else file_domain,
                resource_only=(
                    not complete_worktree_release
                    and _scope_is_resource_only(_claim_scope(claim))
                ),
            )
            if owned_status:
                event = _event(
                    "release",
                    "RELEASE_REJECTED",
                    args,
                    claim=claim,
                    reason="worktree_not_clean",
                    compatibility=compatibility,
                )
                return _journaled_result(
                    ERROR,
                    common_directory,
                    event,
                    reason="worktree_not_clean",
                    dirty_status=owned_status,
                    compatibility=compatibility,
                )
            if not complete_worktree_release and not _scope_is_resource_only(_claim_scope(claim)):
                outside_status = _status_outside_domain(current_snapshot, file_domain)
                baseline_outside_status = sorted(
                    claim.get("baseline_out_of_domain_status", []),
                    key=lambda entry: entry["path"] if isinstance(entry, dict) else str(entry),
                )
                current_outside_state = _state_outside_domain(
                    _status_state(worktree, current_snapshot),
                    file_domain,
                )
                baseline_outside_state = claim["baseline_out_of_domain_state"]
                changed_paths = sorted(
                    path
                    for path in set(current_outside_state) | set(baseline_outside_state)
                    if current_outside_state.get(path) != baseline_outside_state.get(path)
                )
            else:
                outside_status = []
                baseline_outside_status = []
                changed_paths = []
            reconciliation: dict[str, Any] | None = None
            if args.prior_rejected_release_reference and not args.reconcile_out_of_domain_commit:
                event = _event(
                    "release",
                    "RELEASE_REJECTED",
                    args,
                    claim=claim,
                    reason="prior_rejection_requires_reconciliation_commit",
                )
                return _journaled_result(
                    ERROR,
                    common_directory,
                    event,
                    reason="prior_rejection_requires_reconciliation_commit",
                )
            if args.reconcile_out_of_domain_commit:
                try:
                    reconciliation = _release_reconciliation_evidence(
                        common_directory,
                        worktree,
                        claim,
                        changed_paths,
                        outside_status,
                        args,
                    )
                except _ReleaseReconciliationError as error:
                    event = _event(
                        "release",
                        "RELEASE_REJECTED",
                        args,
                        claim=claim,
                        reason=error.reason,
                        **error.details,
                    )
                    return _journaled_result(
                        ERROR,
                        common_directory,
                        event,
                        reason=error.reason,
                        message=str(error),
                        **error.details,
                    )
            elif changed_paths:
                event = _event(
                    "release",
                    "RELEASE_REJECTED",
                    args,
                    claim=claim,
                    reason="out_of_domain_changes",
                    out_of_domain_paths=changed_paths,
                )
                return _journaled_result(
                    ERROR,
                    common_directory,
                    event,
                    reason="out_of_domain_changes",
                    out_of_domain_paths=changed_paths,
                    baseline_out_of_domain_status=baseline_outside_status,
                    current_out_of_domain_status=outside_status,
                )
            resulting_commit = _head(worktree)
            if resulting_commit == claim.get("baseline_commit") and not args.no_change:
                event = _event(
                    "release",
                    "RELEASE_REJECTED",
                    args,
                    claim=claim,
                    resulting_commit=resulting_commit,
                    reason="missing_commit_or_no_change",
                )
                return _journaled_result(ERROR, common_directory, event, reason="missing_commit_or_no_change")
            released = claims.pop(index)
            event = _event(
                "release",
                "RELEASED",
                args,
                claim=released,
                resulting_commit=resulting_commit,
                no_change=args.no_change,
                **(
                    {"incarnation_id": reconciliation["claim_incarnation"]["id"]}
                    if reconciliation
                    else {}
                ),
                **({"reconciliation": reconciliation} if reconciliation else {}),
            )
            if reconciliation is not None:
                registry_bytes_before_release = registry_path.read_bytes()
                released_registry_bytes = (
                    json.dumps(data, indent=2, sort_keys=True) + "\n"
                ).encode("utf-8")
                (
                    journal_path,
                    journal_bytes_before_release,
                    prepared_journal_bytes,
                    released_journal_bytes,
                    journal_existed,
                ) = _reconciliation_journal_state(common_directory, event)
                pending = {
                    "schema_version": 1,
                    "state": "prepared",
                    "claim_id": released.get("claim_id"),
                    "event_id": event["event_id"],
                    "incarnation_id": event["incarnation_id"],
                    "event_timestamp": event["timestamp"],
                    "prior_rejected_release_reference": reconciliation[
                        "prior_rejected_release_reference"
                    ],
                    "registry": {
                        "path": str(registry_path.relative_to(common_directory)),
                        "original": _encoded_snapshot(registry_bytes_before_release),
                        "released": _encoded_snapshot(released_registry_bytes),
                    },
                    "journal": {
                        "path": str(journal_path.relative_to(common_directory)),
                        "original": _encoded_snapshot(
                            journal_bytes_before_release,
                            exists=journal_existed,
                        ),
                        "prepared": _encoded_snapshot(prepared_journal_bytes),
                        "released": _encoded_snapshot(released_journal_bytes),
                    },
                }
                try:
                    marker_path = _write_pending_reconciliation(
                        common_directory,
                        pending,
                    )
                except OSError as error:
                    claims.insert(index, released)
                    rejected_event = _event(
                        "release",
                        "RELEASE_REJECTED",
                        args,
                        claim=released,
                        reason="reconciliation_marker_not_durable",
                        reconciliation=reconciliation,
                    )
                    _print_result(
                        rejected_event["outcome"],
                        journal={
                            "event_id": rejected_event["event_id"],
                            "persisted": False,
                        },
                        warnings=[
                            {
                                "code": "reconciliation_marker_write_failed",
                                "message": str(error),
                            }
                        ],
                        reason="reconciliation_marker_not_durable",
                        message=(
                            "The reconciliation did not start because its "
                            "recovery marker was not durable."
                        ),
                        reconciliation=reconciliation,
                    )
                    return ERROR
                transaction_committed = False
                try:
                    registry_faults = {
                        "write": (
                            "AGENT_CLAIM_TEST_FAIL_RECONCILIATION_REGISTRY_WRITE"
                        ),
                        "short_write": (
                            "AGENT_CLAIM_TEST_SHORT_RECONCILIATION_REGISTRY_WRITE"
                        ),
                        "after_write": (
                            "AGENT_CLAIM_TEST_FAIL_RECONCILIATION_REGISTRY_AFTER_WRITE"
                        ),
                        "fsync": (
                            "AGENT_CLAIM_TEST_FAIL_RECONCILIATION_REGISTRY_FSYNC"
                        ),
                        "replace": (
                            "AGENT_CLAIM_TEST_FAIL_RECONCILIATION_REGISTRY_REPLACE"
                        ),
                        "directory_fsync": (
                            "AGENT_CLAIM_TEST_FAIL_RECONCILIATION_REGISTRY_DIRECTORY_FSYNC"
                        ),
                    }
                    _append_reconciliation_event(
                        journal_path,
                        prepared_journal_bytes,
                    )
                    _durable_atomic_replace(
                        registry_path,
                        released_registry_bytes,
                        faults=registry_faults,
                    )
                    pending["state"] = "committed"
                    _write_pending_reconciliation(common_directory, pending)
                    transaction_committed = True
                    if (
                        os.environ.get(
                            "AGENT_CLAIM_TEST_STOP_AFTER_RECONCILIATION_COMMIT_MARKER"
                        )
                        == "1"
                    ):
                        _print_result(
                            "RECONCILIATION_RECOVERY_REQUIRED",
                            reason="committed_reconciliation_cleanup_pending",
                            message=(
                                "The reconciliation committed and marker cleanup "
                                "remains pending."
                            ),
                            ownership_authority="committed_marker",
                            pending_transaction={
                                "claim_id": released.get("claim_id"),
                                "marker": str(marker_path),
                                "state": "committed",
                            },
                        )
                        return ERROR
                    _finalize_reconciliation_event(
                        journal_path,
                        released_journal_bytes,
                    )
                    _durable_remove(
                        marker_path,
                        fault_environment=(
                            "AGENT_CLAIM_TEST_FAIL_RECONCILIATION_MARKER_REMOVE"
                        ),
                    )
                except OSError as error:
                    recovery_error: _PendingReconciliationError | None = None
                    try:
                        recovered = _recover_pending_reconciliation(common_directory)
                    except _PendingReconciliationError as pending_error:
                        recovered = None
                        recovery_error = pending_error
                    if recovery_error is not None and transaction_committed:
                        _print_result(
                            "RECONCILIATION_RECOVERY_REQUIRED",
                            warnings=[
                                {
                                    "code": "reconciliation_cleanup_failed",
                                    "message": str(recovery_error),
                                }
                            ],
                            reason="committed_reconciliation_cleanup_pending",
                            message=(
                                "The reconciliation committed and deterministic "
                                "cleanup remains pending."
                            ),
                            ownership_authority="committed_marker",
                            pending_transaction={
                                "claim_id": released.get("claim_id"),
                                "marker": str(marker_path),
                                "state": "committed",
                            },
                            reconciliation=reconciliation,
                        )
                        return ERROR
                    if transaction_committed or (
                        recovered is not None
                        and recovered.get("resolved_state") == "committed"
                    ):
                        _print_result(
                            event["outcome"],
                            journal={
                                "event_id": event["event_id"],
                                "path": str(journal_path),
                            },
                            warnings=[
                                {
                                    "code": "reconciliation_cleanup_recovered",
                                    "message": str(error),
                                }
                            ],
                            claim=released,
                            reconciliation=reconciliation,
                        )
                        return SUCCESS
                    rejected_event = _event(
                        "release",
                        "RELEASE_REJECTED",
                        args,
                        claim=released,
                        reason="reconciliation_journal_not_durable",
                        reconciliation=reconciliation,
                    )
                    if recovery_error is not None:
                        _print_result(
                            rejected_event["outcome"],
                            journal={
                                "event_id": rejected_event["event_id"],
                                "persisted": False,
                            },
                            warnings=[
                                {
                                    "code": "reconciliation_restore_failed",
                                    "message": str(recovery_error),
                                }
                            ],
                            reason="reconciliation_restore_pending",
                            message=(
                                "Reconciliation failed and exact ownership "
                                "restoration remains pending."
                            ),
                            ownership_authority="pending_marker",
                            pending_transaction={
                                "claim_id": released.get("claim_id"),
                                "marker": str(marker_path),
                                "state": "prepared",
                            },
                            reconciliation=reconciliation,
                        )
                        return ERROR
                    _print_result(
                        rejected_event["outcome"],
                        journal={
                            "event_id": rejected_event["event_id"],
                            "persisted": False,
                        },
                        warnings=[
                            {
                                "code": "journal_write_failed",
                                "message": str(error),
                            }
                        ],
                        reason="reconciliation_journal_not_durable",
                        message="The RELEASED reconciliation event was not durably journaled.",
                        reconciliation=reconciliation,
                    )
                    return ERROR
                _print_result(
                    event["outcome"],
                    journal={"event_id": event["event_id"], "path": str(journal_path)},
                    claim=released,
                    reconciliation=reconciliation,
                )
                return SUCCESS
            _write_registry(registry_path, data)
            return _journaled_result(
                SUCCESS,
                common_directory,
                event,
                claim=released,
                **({"reconciliation": reconciliation} if reconciliation else {}),
            )
        event = _event("release", "CLAIM_NOT_FOUND", args)
        return _journaled_result(ERROR, common_directory, event, claim_id=args.claim_id)


def _status_command(args: argparse.Namespace) -> int:
    repository = _repository_root(Path(args.repo).resolve())
    with _locked_registry(repository) as (registry_path, data):
        evaluated_at = _now()
        _print_result(
            "STATUS",
            registry=str(registry_path),
            claims=[_claim_for_output(claim, evaluated_at) for claim in data["claims"]],
        )
    return SUCCESS


def _event_sort_key(event: dict[str, Any]) -> tuple[str, str]:
    return str(event.get("timestamp", "")), str(event.get("event_id", ""))


def _read_jsonl(raw: bytes, source: str, coverage_gaps: list[dict[str, str]]) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    try:
        decoded = raw.decode("utf-8")
    except UnicodeDecodeError as error:
        coverage_gaps.append(
            {
                "source": source,
                "detail": f"invalid UTF-8 at byte {error.start}",
            }
        )
        return events
    for line_number, raw_line in enumerate(decoded.splitlines(), start=1):
        if not raw_line.strip():
            continue
        try:
            event = json.loads(raw_line)
        except json.JSONDecodeError as error:
            coverage_gaps.append({"source": source, "detail": f"line {line_number}: {error.msg}"})
            continue
        if not isinstance(event, dict) or not event.get("event_id") or not event.get("timestamp"):
            coverage_gaps.append({"source": source, "detail": f"line {line_number}: invalid event schema"})
            continue
        events.append(event)
    return events


def _load_events(common_directory: Path) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    _root, hot_directory, archive_directory, _journal = _journal_paths(common_directory)
    coverage_gaps: list[dict[str, str]] = []
    events: list[dict[str, Any]] = []
    for path in sorted(hot_directory.glob("*.jsonl")) if hot_directory.exists() else []:
        try:
            events.extend(_read_jsonl(path.read_bytes(), str(path), coverage_gaps))
        except OSError as error:
            coverage_gaps.append({"source": str(path), "detail": str(error)})
    for path in sorted(archive_directory.glob("**/*.jsonl.gz")) if archive_directory.exists() else []:
        try:
            events.extend(_read_jsonl(gzip.decompress(path.read_bytes()), str(path), coverage_gaps))
        except (OSError, EOFError) as error:
            coverage_gaps.append({"source": str(path), "detail": str(error)})

    unique_events: dict[str, dict[str, Any]] = {}
    for event in sorted(events, key=_event_sort_key):
        event_id = str(event["event_id"])
        if event_id in unique_events:
            coverage_gaps.append({"source": event_id, "detail": "duplicate event id"})
            continue
        unique_events[event_id] = event
    return list(unique_events.values()), coverage_gaps


def _percentile(values: list[float], percentile: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    rank = max(1, math.ceil(percentile * len(ordered)))
    return ordered[rank - 1]


def _top_counts(counter: Counter[str]) -> list[dict[str, Any]]:
    return [
        {"scope": scope, "count": count}
        for scope, count in sorted(counter.items(), key=lambda item: (-item[1], item[0]))[:10]
    ]


def _aggregate(
    events: list[dict[str, Any]],
    now: datetime,
    live_claims: list[dict[str, Any]],
) -> dict[str, Any]:
    ordered = sorted(events, key=_event_sort_key)
    normalized_outcomes, normalization_gaps = _normalized_event_outcomes(ordered)
    successful_outcomes = {
        "SHARED_CHECKOUT_ACQUIRED": "primary",
        "ISOLATED_CHECKOUT_ACQUIRED": "isolated",
        "DIRTY_CHECKOUT_RECOVERY_ACQUIRED": "recovery",
    }
    acquisitions = Counter()
    raw_outcome_counts = Counter(str(event.get("outcome")) for event in ordered)
    outcome_counts = Counter(normalized_outcomes)
    action_counts = Counter(str(event.get("action")) for event in ordered)
    acquisition_times: dict[str, datetime] = {}
    released_claims: set[str] = set()
    durations: list[float] = []
    active_waits: dict[tuple[str, str], dict[str, Any]] = {}
    wait_episodes: list[dict[str, Any]] = []
    exact_files: Counter[str] = Counter()
    trees: Counter[str] = Counter()
    resources: Counter[str] = Counter()
    broad_reasons: Counter[str] = Counter()
    broad_scope_count = 0
    broad_file_domains: Counter[str] = Counter()
    integration_resources: Counter[str] = Counter()
    journal_warning_count = 0

    for index, event in enumerate(ordered):
        outcome = normalized_outcomes[index]
        action = str(event.get("action"))
        claim_id = str(event.get("claim_id") or "")
        timestamp = _parse_timestamp(str(event["timestamp"]))
        if outcome in successful_outcomes:
            acquisitions[successful_outcomes[outcome]] += 1
            if claim_id:
                acquisition_times[claim_id] = timestamp
        if outcome == "RELEASED" and claim_id:
            released_claims.add(claim_id)
            acquired = acquisition_times.get(claim_id)
            if acquired is not None:
                durations.append(max(0.0, (timestamp - acquired).total_seconds()))

        wait_key = (claim_id, action)
        if outcome == "CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED" and claim_id:
            episode = active_waits.setdefault(
                wait_key,
                {
                    "claim_id": claim_id,
                    "action": action,
                    "started_at": event["timestamp"],
                    "attempt_count": 0,
                },
            )
            episode["attempt_count"] += 1
            episode["last_wait_at"] = event["timestamp"]
        elif wait_key in active_waits and outcome in {*successful_outcomes, "EXTENDED"}:
            episode = active_waits.pop(wait_key)
            episode["resolved_at"] = event["timestamp"]
            episode["duration_seconds"] = max(
                0.0,
                (timestamp - _parse_timestamp(str(episode["started_at"]))).total_seconds(),
            )
            wait_episodes.append(episode)

        if outcome == "CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED":
            for overlap in event.get("overlaps", []):
                if overlap.get("scope_kind") == "resource":
                    resources[str(overlap.get("requested"))] += 1
                elif "tree" in {overlap.get("requested_kind"), overlap.get("claimed_kind")} or "all_files" in {
                    overlap.get("requested_kind"), overlap.get("claimed_kind")
                }:
                    trees[str(overlap.get("requested"))] += 1
                else:
                    exact_files[str(overlap.get("requested"))] += 1

        requested = event.get("requested_scopes") or {}
        if outcome in {*successful_outcomes, "EXTENDED"}:
            if (
                requested.get("trees")
                or requested.get("project_files")
                or requested.get("backlog")
                or requested.get("all_files")
            ):
                broad_scope_count += 1
                if requested.get("scope_reason"):
                    broad_reasons[str(requested["scope_reason"])] += 1
                requested_domain = _scope_file_domain(requested)
                if requested_domain in {"project_files", "backlog", "all_files"}:
                    broad_file_domains[requested_domain] += 1
            for resource in requested.get("resources", []):
                if str(resource).startswith("merge:integration:"):
                    integration_resources[str(resource)] += 1
        journal_warning_count += len(event.get("journal_warnings", []))

    for episode in active_waits.values():
        episode["resolved_at"] = None
        episode["duration_seconds"] = None
        wait_episodes.append(episode)

    live_by_id = {str(claim.get("claim_id")): claim for claim in live_claims}
    stale_cutoff = now - timedelta(hours=STALE_HEARTBEAT_HOURS)
    stale_claims = sorted(
        claim_id
        for claim_id, claim in live_by_id.items()
        if claim.get("heartbeat") and _parse_timestamp(str(claim["heartbeat"])) < stale_cutoff
    )
    missing_releases = sorted(
        claim_id
        for claim_id in acquisition_times
        if claim_id not in released_claims and claim_id not in live_by_id
    )
    return {
        "action_counts": dict(sorted(action_counts.items())),
        "outcome_counts": dict(sorted(outcome_counts.items())),
        "raw_outcome_counts": dict(sorted(raw_outcome_counts.items())),
        "outcome_normalization_gaps": normalization_gaps,
        "successful_acquisitions": {
            mode: acquisitions.get(mode, 0) for mode in ("primary", "isolated", "recovery")
        },
        "wait_episodes": sorted(wait_episodes, key=lambda item: (item["started_at"], item["claim_id"])),
        "wait_attempt_count": outcome_counts.get("CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED", 0),
        "claim_duration_seconds": {
            "count": len(durations),
            "median": median(durations) if durations else None,
            "p95": _percentile(durations, 0.95),
            "maximum": max(durations) if durations else None,
        },
        "top_contention": {
            "exact_files": _top_counts(exact_files),
            "trees": _top_counts(trees),
            "resources": _top_counts(resources),
        },
        "broad_scopes": {
            "event_count": broad_scope_count,
            "file_domains": {
                domain: broad_file_domains.get(domain, 0)
                for domain in ("all_files", "backlog", "project_files")
            },
            "reasons": _top_counts(broad_reasons),
        },
        "open_claim_ids": sorted(live_by_id),
        "claims_with_missing_release": missing_releases,
        "stale_heartbeat_claim_ids": stale_claims,
        "integration_resources": _top_counts(integration_resources),
        "journal_warning_count": journal_warning_count,
    }


def _daily_summary(day: str, events: list[dict[str, Any]]) -> dict[str, Any]:
    metrics = _aggregate(events, _now(), [])
    event_ids = sorted(str(event["event_id"]) for event in events)
    return {
        "schema_version": SUMMARY_SCHEMA_VERSION,
        "date": day,
        "raw_event_count": len(events),
        "event_ids_sha256": hashlib.sha256("\n".join(event_ids).encode("utf-8")).hexdigest(),
        "action_counts": metrics["action_counts"],
        "outcome_counts": metrics["outcome_counts"],
        "raw_outcome_counts": metrics["raw_outcome_counts"],
        "claim_duration_seconds": metrics["claim_duration_seconds"],
        "wait_episodes": metrics["wait_episodes"],
        "top_contention": metrics["top_contention"],
        "recovery_event_count": metrics["outcome_counts"].get(
            "DIRTY_CHECKOUT_RECOVERY_ACQUIRED",
            0,
        ),
        "incomplete_lifecycle_claim_ids": metrics["claims_with_missing_release"],
    }


def _gzip_bytes(raw: bytes) -> bytes:
    from io import BytesIO

    destination = BytesIO()
    with gzip.GzipFile(fileobj=destination, mode="wb", mtime=0) as compressed:
        compressed.write(raw)
    return destination.getvalue()


def _atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    try:
        temporary.write_bytes(content)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def _write_validated_archive(path: Path, compressed: bytes, expected_raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    try:
        temporary.write_bytes(compressed)
        if os.environ.get("AGENT_CLAIM_TEST_FAIL_ARCHIVE_BEFORE_VALIDATE") == "1":
            raise OSError("simulated interruption before archive validation")
        if gzip.decompress(temporary.read_bytes()) != expected_raw:
            raise ValueError(f"Archive validation failed for {path}")
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def _maintain_journal(args: argparse.Namespace) -> int:
    repository = _repository_root(Path(args.repo).resolve())
    common_directory = _git_common_directory(repository)
    if args.hot_days < 1:
        _print_result("INVALID_HOT_DAYS", hot_days=args.hot_days)
        return ERROR
    _root, hot_directory, archive_directory, journal_directory = _journal_paths(common_directory)
    cutoff = _now().date() - timedelta(days=args.hot_days - 1)
    archived: list[dict[str, Any]] = []
    try:
        with _locked_registry(repository):
            with _maintenance_lock(common_directory):
                candidates = sorted(hot_directory.glob("*.jsonl")) if hot_directory.exists() else []
                for hot_path in candidates:
                    match = UTC_DAY_PATTERN.match(hot_path.name)
                    if not match:
                        continue
                    day_text = match.group(1)
                    day = date.fromisoformat(day_text)
                    if day >= cutoff:
                        continue
                    raw = hot_path.read_bytes()
                    coverage_gaps: list[dict[str, str]] = []
                    events = _read_jsonl(raw, str(hot_path), coverage_gaps)
                    if coverage_gaps:
                        raise ValueError(f"Cannot archive invalid journal {hot_path}: {coverage_gaps}")

                    year, month, _day = day_text.split("-")
                    archive_path = archive_directory / year / month / f"{day_text}.jsonl.gz"
                    summary_path = journal_directory / year / month / f"{day_text}.json"
                    compressed = _gzip_bytes(raw)

                    if archive_path.exists():
                        if gzip.decompress(archive_path.read_bytes()) != raw:
                            raise ValueError(f"Existing immutable archive does not match {hot_path}")
                    else:
                        _write_validated_archive(archive_path, compressed, raw)
                    if gzip.decompress(archive_path.read_bytes()) != raw:
                        raise ValueError(f"Archive validation failed for {archive_path}")

                    summary = _daily_summary(day_text, events)
                    rendered_summary = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
                    if summary_path.exists():
                        if summary_path.read_bytes() != rendered_summary:
                            raise ValueError(f"Existing immutable summary does not match {hot_path}")
                    else:
                        _atomic_write(summary_path, rendered_summary)
                    hot_path.unlink()
                    archived.append(
                        {
                            "date": day_text,
                            "event_count": len(events),
                            "archive": str(archive_path),
                            "summary": str(summary_path),
                        }
                    )
    except (OSError, ValueError) as error:
        _print_result("JOURNAL_MAINTENANCE_FAILED", message=str(error), archived=archived)
        return ERROR
    _print_result("JOURNAL_MAINTAINED", hot_days=args.hot_days, archived=archived)
    return SUCCESS


def _since_delta(value: str) -> timedelta:
    match = SINCE_PATTERN.match(value)
    if not match:
        raise ValueError("--since must use a positive duration such as 12h or 2d")
    amount = int(match.group(1))
    if amount < 1:
        raise ValueError("--since must be positive")
    return timedelta(hours=amount) if match.group(2) == "h" else timedelta(days=amount)


def _render_text_report(report: dict[str, Any]) -> str:
    metrics = report["metrics"]
    acquisitions = metrics["successful_acquisitions"]
    durations = metrics["claim_duration_seconds"]
    return "\n".join(
        (
            f"Claim report {report['window']['start']} to {report['window']['end']}",
            f"Events: {report['event_count']}",
            "Acquisitions: "
            f"primary={acquisitions['primary']} isolated={acquisitions['isolated']} recovery={acquisitions['recovery']}",
            f"Wait attempts: {metrics['wait_attempt_count']} in {len(metrics['wait_episodes'])} episodes",
            "Claim duration seconds: "
            f"median={durations['median']} p95={durations['p95']} maximum={durations['maximum']}",
            f"Open claims: {', '.join(metrics['open_claim_ids']) or 'none'}",
            f"Coverage gaps: {len(report['coverage_gaps'])}",
        )
    )


def _report(args: argparse.Namespace) -> int:
    repository = _repository_root(Path(args.repo).resolve())
    common_directory = _git_common_directory(repository)
    try:
        delta = _since_delta(args.since)
    except ValueError as error:
        _print_result("INVALID_SINCE", message=str(error))
        return ERROR
    end = _now()
    start = end - delta
    with _locked_registry(repository, recover_pending=False) as (
        _registry_path,
        data,
    ):
        events, coverage_gaps = _load_events(common_directory)
        filtered = [
            event
            for event in events
            if start <= _parse_timestamp(str(event["timestamp"])) <= end
        ]
        live_claims = [dict(claim) for claim in data["claims"]]
    acquired_claim_ids = {
        str(event.get("claim_id"))
        for event in events
        if _canonical_outcome(str(event.get("outcome")))
        in {
            "SHARED_CHECKOUT_ACQUIRED",
            "ISOLATED_CHECKOUT_ACQUIRED",
            "DIRTY_CHECKOUT_RECOVERY_ACQUIRED",
        }
    }
    for claim in live_claims:
        claim_id = str(claim.get("claim_id"))
        if claim_id not in acquired_claim_ids:
            coverage_gaps.append(
                {"source": claim_id, "detail": "live claim has no acquisition event"}
            )
    report = {
        "schema_version": REPORT_SCHEMA_VERSION,
        "window": {"since": args.since, "start": _format_timestamp(start), "end": _format_timestamp(end)},
        "event_count": len(filtered),
        "metrics": _aggregate(filtered, end, live_claims),
        "coverage_gaps": coverage_gaps,
    }
    if args.format == "text":
        print(_render_text_report(report))
    else:
        print(json.dumps(report, indent=2, sort_keys=True))
    return SUCCESS


def _add_scope_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--file", action="append", default=[], help="Exact intended file; future nonexistent files are allowed.")
    parser.add_argument("--tree", action="append", default=[], help="Intended directory subtree.")
    parser.add_argument(
        "--project-files",
        action="store_true",
        help="Claim every project file except the primary-only backlog and ignored operational state.",
    )


def _add_resource_timing_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--resource-class")
    parser.add_argument("--resource-id")
    parser.add_argument("--expected-duration-seconds", type=int)
    parser.add_argument("--requested-hard-stop-duration-seconds", type=int)
    parser.add_argument(
        "--backlog",
        action="store_true",
        help="Claim the complete primary-worktree-only backlog subtree.",
    )
    parser.add_argument(
        "--all-files",
        action="store_true",
        help="Claim the explicit union of project files and backlog.",
    )
    parser.add_argument("--resource", action="append", default=[], help="Exclusive repository-global runtime resource.")
    parser.add_argument(
        "--scope-reason",
        help="Bounded coordination-only reason required for tree, project-files, or all-files scope.",
    )
    parser.add_argument(
        "--compat-file-directories",
        action="store_true",
        help="Temporarily convert existing directories passed through --file into warned tree scopes.",
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Coordinate repository claims, worktrees, and claim diagnostics.")
    parser.add_argument("--repo", default=".", help="Path inside the repository.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    acquire = subparsers.add_parser("acquire", help="Atomically acquire primary, isolated, or recovery ownership.")
    acquire.add_argument("--claim-id", required=True)
    acquire.add_argument("--agent", required=True)
    acquire.add_argument("--task", required=True)
    acquire.add_argument("--root-task-id", required=True)
    acquire.add_argument("--parent-claim-id")
    _add_scope_arguments(acquire)
    acquire.add_argument("--branch")
    acquire.add_argument(
        "--worktree-path",
        help="Compatibility input that must equal the canonical primary-root .worktrees target.",
    )
    acquire.add_argument("--base", default="HEAD")
    acquire.add_argument("--allow-recovery", action="store_true")
    _add_resource_timing_arguments(acquire)
    acquire.set_defaults(handler=_acquire)

    extend = subparsers.add_parser("extend", help="Atomically add files, trees, or resources to an active claim.")
    extend.add_argument("--claim-id", required=True)
    _add_scope_arguments(extend)
    _add_resource_timing_arguments(extend)
    extend.set_defaults(handler=_extend)

    heartbeat = subparsers.add_parser("heartbeat", help="Refresh an active claim heartbeat.")
    heartbeat.add_argument("--claim-id", required=True)
    heartbeat.set_defaults(handler=_heartbeat)

    extend_deadline = subparsers.add_parser(
        "extend-deadline",
        help="Extend one configured resource hard stop with bounded evidence.",
    )
    extend_deadline.add_argument("--claim-id", required=True)
    extend_deadline.add_argument(
        "--requested-hard-stop-duration-seconds",
        required=True,
        type=int,
    )
    extend_deadline.add_argument("--extension-evidence", required=True)
    extend_deadline.set_defaults(handler=_extend_deadline)

    release = subparsers.add_parser("release", help="Release a committed clean claim or a declared no-change claim.")
    release.add_argument("--claim-id", required=True)
    release_mode = release.add_mutually_exclusive_group()
    release_mode.add_argument("--no-change", action="store_true")
    release_mode.add_argument(
        "--reconcile-out-of-domain-commit",
        type=_full_commit_sha,
        help="Release using exact peer-commit proof for a previously rejected out-of-domain change.",
    )
    release.add_argument(
        "--prior-rejected-release-reference",
        help="Event id for the matching prior RELEASE_REJECTED out-of-domain release.",
    )
    release.set_defaults(handler=_release)

    status = subparsers.add_parser("status", help="Show the repository-global live claim registry.")
    status.set_defaults(handler=_status_command)

    maintain = subparsers.add_parser("maintain-journal", help="Archive complete UTC journal days outside the hot window.")
    maintain.add_argument("--hot-days", type=int, default=DEFAULT_HOT_DAYS)
    maintain.set_defaults(handler=_maintain_journal)

    report = subparsers.add_parser("report", help="Report claim contention from the journal and live registry.")
    report.add_argument("--since", default="2d")
    report.add_argument("--format", choices=("json", "text"), default="json")
    report.set_defaults(handler=_report)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Dispatch one public claim command.

    Args:
        argv: Optional command arguments without the executable name. Process arguments
            are used when this value is absent.

    Returns:
        The stable command exit code. Commands may mutate the live registry, worktrees,
        or journal according to their documented boundary; report remains read-only.
    """
    args = _parser().parse_args(argv)
    try:
        return args.handler(args)
    except _PendingReconciliationError as error:
        _print_result(
            "RECONCILIATION_RECOVERY_REQUIRED",
            reason="pending_reconciliation_restore_failed",
            message=str(error),
            ownership_authority="pending_marker",
            pending_transaction={
                "claim_id": error.claim_id,
                "marker": str(error.marker_path),
            },
        )
        return ERROR


if __name__ == "__main__":
    raise SystemExit(main())
