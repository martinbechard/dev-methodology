#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Atomically coordinates repository claims, optimistic primary-worktree use, isolation, recovery, and release.

from __future__ import annotations

import argparse
import fcntl
import json
import os
import subprocess
import sys
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator, Sequence


SUCCESS = 0
ERROR = 1
WAIT = 3
ISOLATE_REQUIRED = 4
RECOVERY_REQUIRED = 5
REGISTRY_FILE_NAME = "agent-claims.json"
LOCK_FILE_NAME = "agent-claims.lock"


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


def _registry_paths(repository: Path) -> tuple[Path, Path]:
    common_directory = _git_common_directory(repository)
    return common_directory / REGISTRY_FILE_NAME, common_directory / LOCK_FILE_NAME


@contextmanager
def _locked_registry(repository: Path) -> Iterator[tuple[Path, dict[str, Any]]]:
    registry_path, lock_path = _registry_paths(repository)
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+", encoding="utf-8") as lock_file:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
        try:
            if registry_path.exists():
                data = json.loads(registry_path.read_text(encoding="utf-8"))
            else:
                data = {"claims": []}
            if not isinstance(data.get("claims"), list):
                raise ValueError(f"Invalid claim registry: {registry_path}")
            yield registry_path, data
        finally:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)


def _write_registry(path: Path, data: dict[str, Any]) -> None:
    temporary_path = path.with_suffix(".tmp")
    temporary_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(temporary_path, path)


def _timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _status(worktree: Path) -> str:
    return _git(worktree, "status", "--porcelain").stdout


def _head(worktree: Path) -> str:
    return _git(worktree, "rev-parse", "HEAD").stdout.strip()


def _normalized_path(value: str) -> str:
    return value.strip().rstrip("/") or "."


def _paths_overlap(left: str, right: str) -> bool:
    left_path = _normalized_path(left)
    right_path = _normalized_path(right)
    if "**" in {left_path, right_path}:
        return True
    return (
        left_path == right_path
        or left_path.startswith(right_path + "/")
        or right_path.startswith(left_path + "/")
    )


def _overlapping_claims(
    claims: list[dict[str, Any]], files: list[str], resources: list[str]
) -> list[dict[str, Any]]:
    overlaps: list[dict[str, Any]] = []
    for claim in claims:
        claimed_files = [str(value) for value in claim.get("files", [])]
        claimed_resources = {str(value) for value in claim.get("resources", [])}
        file_overlap = any(
            _paths_overlap(requested, claimed)
            for requested in files
            for claimed in claimed_files
        )
        resource_overlap = bool(set(resources) & claimed_resources)
        if file_overlap or resource_overlap:
            overlaps.append(claim)
    return overlaps


def _print_result(outcome: str, **details: Any) -> None:
    print(json.dumps({"outcome": outcome, **details}, indent=2, sort_keys=True))


def _acquire(args: argparse.Namespace) -> int:
    repository = _repository_root(Path(args.repo).resolve())
    files = [_normalized_path(value) for value in args.file]
    resources = [value.strip() for value in args.resource]

    with _locked_registry(repository) as (registry_path, data):
        claims: list[dict[str, Any]] = data["claims"]
        overlaps = _overlapping_claims(claims, files, resources)
        if overlaps:
            _print_result(
                "WAIT",
                conflicting_claim_ids=[claim["claim_id"] for claim in overlaps],
            )
            return WAIT

        if claims:
            if not args.branch or not args.worktree_path:
                _print_result("ISOLATE_REQUIRED", active_claim_count=len(claims))
                return ISOLATE_REQUIRED
            target_worktree = Path(args.worktree_path).resolve()
            completed = _git(
                repository,
                "worktree",
                "add",
                "-b",
                args.branch,
                str(target_worktree),
                args.base,
                check=False,
            )
            if completed.returncode != SUCCESS:
                print(completed.stderr, file=sys.stderr, end="")
                return ERROR
            mode = "isolated"
            outcome = "ISOLATE"
        else:
            target_worktree = repository
            initial_status = _status(target_worktree)
            if initial_status and not args.allow_recovery:
                _print_result("RECOVERY_REQUIRED", dirty_status=initial_status.splitlines())
                return RECOVERY_REQUIRED
            mode = "recovery" if initial_status else "primary"
            outcome = "RECOVER" if initial_status else "PRIMARY"

        now = _timestamp()
        claim = {
            "agent": args.agent,
            "baseline_commit": _head(target_worktree),
            "baseline_status": _status(target_worktree).splitlines(),
            "claim_id": args.claim_id,
            "claimed_at": now,
            "files": files,
            "heartbeat": now,
            "mode": mode,
            "parent_claim_id": args.parent_claim_id,
            "resources": resources,
            "root_task_id": args.root_task_id,
            "task": args.task,
            "worktree": str(target_worktree),
        }
        claims.append(claim)
        _write_registry(registry_path, data)

    _print_result(outcome, claim=claim, registry=str(registry_path))
    return SUCCESS


def _heartbeat(args: argparse.Namespace) -> int:
    repository = _repository_root(Path(args.repo).resolve())
    with _locked_registry(repository) as (registry_path, data):
        for claim in data["claims"]:
            if claim.get("claim_id") == args.claim_id:
                claim["heartbeat"] = _timestamp()
                _write_registry(registry_path, data)
                _print_result("HEARTBEAT", claim=claim)
                return SUCCESS
    print(f"Claim not found: {args.claim_id}", file=sys.stderr)
    return ERROR


def _release(args: argparse.Namespace) -> int:
    repository = _repository_root(Path(args.repo).resolve())
    with _locked_registry(repository) as (registry_path, data):
        claims: list[dict[str, Any]] = data["claims"]
        for index, claim in enumerate(claims):
            if claim.get("claim_id") != args.claim_id:
                continue
            worktree = Path(claim["worktree"])
            if _status(worktree):
                _print_result("RELEASE_REJECTED", reason="worktree_not_clean")
                return ERROR
            if _head(worktree) == claim.get("baseline_commit") and not args.no_change:
                _print_result("RELEASE_REJECTED", reason="missing_commit_or_no_change")
                return ERROR
            released = claims.pop(index)
            _write_registry(registry_path, data)
            _print_result("RELEASED", claim=released)
            return SUCCESS
    print(f"Claim not found: {args.claim_id}", file=sys.stderr)
    return ERROR


def _status_command(args: argparse.Namespace) -> int:
    repository = _repository_root(Path(args.repo).resolve())
    with _locked_registry(repository) as (registry_path, data):
        _print_result("STATUS", registry=str(registry_path), claims=data["claims"])
    return SUCCESS


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Coordinate repository claims and worktrees.")
    parser.add_argument("--repo", default=".", help="Path inside the repository.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    acquire = subparsers.add_parser("acquire", help="Atomically acquire primary, isolated, or recovery ownership.")
    acquire.add_argument("--claim-id", required=True)
    acquire.add_argument("--agent", required=True)
    acquire.add_argument("--task", required=True)
    acquire.add_argument("--root-task-id", required=True)
    acquire.add_argument("--parent-claim-id")
    acquire.add_argument("--file", action="append", default=[])
    acquire.add_argument("--resource", action="append", default=[])
    acquire.add_argument("--branch")
    acquire.add_argument("--worktree-path")
    acquire.add_argument("--base", default="HEAD")
    acquire.add_argument("--allow-recovery", action="store_true")
    acquire.set_defaults(handler=_acquire)

    heartbeat = subparsers.add_parser("heartbeat", help="Refresh an active claim heartbeat.")
    heartbeat.add_argument("--claim-id", required=True)
    heartbeat.set_defaults(handler=_heartbeat)

    release = subparsers.add_parser("release", help="Release a committed clean claim or a declared no-change claim.")
    release.add_argument("--claim-id", required=True)
    release.add_argument("--no-change", action="store_true")
    release.set_defaults(handler=_release)

    status = subparsers.add_parser("status", help="Show the repository-global claim registry.")
    status.set_defaults(handler=_status_command)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the claim command selected by argv and return its stable process exit code."""
    args = _parser().parse_args(argv)
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
