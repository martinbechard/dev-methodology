# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Exercises Wiki Writer evidence handling across deterministic verifier interruption.

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Literal


_INTERRUPTION = "wiki-topic-verifier became unavailable before returning a verdict"
_CHILD_FLAG = "--verifier-child"
_VerifierMode = Literal[
    "interrupted",
    "direct-write",
    "direct-write-restore",
    "dir-fd-write-restore",
    "replace-restore",
    "subprocess-write",
]


class VerifierMutationError(RuntimeError):
    """Signal that the verifier changed files inside the writer-owned wiki scope."""


def stage_writer_state(repository: Path) -> tuple[str, ...]:
    """Create representative writer edits over a committed fixture baseline.

    The repository parameter identifies the disposable fixture root. The function
    initializes Git, commits two baseline docs/wiki pages, applies writer edits, and
    returns their repository-relative inventory. Git and filesystem errors propagate.
    """
    baseline_contents = {
        "docs/wiki/deployment/deployment-policy.md": (
            "# Deployment Policy\n\n"
            "Rollback requirements are pending.\n"
        ),
        "docs/wiki/deployment/index.md": "# Deployment\n",
    }
    writer_contents = {
        "docs/wiki/deployment/deployment-policy.md": (
            "# Deployment Policy\n\n"
            "Rollback requires an operator-confirmed checkpoint.\n"
        ),
        "docs/wiki/deployment/index.md": (
            "# Deployment\n\n"
            "- [Deployment policy](deployment-policy.md)\n"
        ),
    }
    _write_pages(repository, baseline_contents)
    _run_git(repository, "init", "-q")
    _run_git(repository, "config", "user.name", "Wiki Writer Evaluation")
    _run_git(
        repository,
        "config",
        "user.email",
        "wiki-writer@example.invalid",
    )
    _run_git(repository, "add", ".")
    _run_git(repository, "commit", "-qm", "Freeze writer baseline")
    _write_pages(repository, writer_contents)
    return tuple(writer_contents)


def run_interruption_control(
    repository: Path,
    page_inventory: tuple[str, ...],
    verifier_mode: _VerifierMode,
    *,
    validation_results: dict[str, str],
    completed_attempts: int,
    attempt_cap: int,
) -> dict[str, object]:
    """Invoke one verifier seam and return role-owned BLOCKED evidence.

    The repository and page inventory identify the preserved writer state.
    The verifier mode runs in a separate Python process with a deterministic offline
    audit model for the exercised attempted-write cases; it is not a production
    sandbox. Validation results and correction counts are copied into the returned
    packet. A verifier write attempt or mutation raises VerifierMutationError.
    Invalid counts, an incomplete page inventory, or a non-interruption receipt
    raises ValueError.
    """
    invalid_attempt_count = (
        completed_attempts < 0
        or attempt_cap < 0
        or completed_attempts > attempt_cap
    )
    if invalid_attempt_count:
        raise ValueError("completed attempts must be between zero and the attempt cap")

    before = _writer_scope_fingerprint(repository)
    preserved_before = _preserved_writer_state(repository, page_inventory)
    receipt, write_attempts = _invoke_verifier_process(
        repository,
        page_inventory,
        verifier_mode,
    )
    after = _writer_scope_fingerprint(repository)
    preserved_after = _preserved_writer_state(repository, page_inventory)
    if write_attempts:
        raise VerifierMutationError(
            "wiki-topic-verifier triggered offline audit attempts: "
            + ", ".join(write_attempts)
        )
    if before != after or preserved_before != preserved_after:
        raise VerifierMutationError(
            "wiki-topic-verifier changed the writer-owned docs/wiki scope"
        )
    if (
        receipt.get("agent") != "wiki-topic-verifier"
        or receipt.get("outcome") != "INTERRUPTED"
        or not isinstance(receipt.get("interruption"), str)
    ):
        raise ValueError("verifier receipt must record an exact interruption")

    return {
        "status": "BLOCKED",
        "owner": "wiki-writer",
        "pageInventory": list(page_inventory),
        "validationResults": dict(validation_results),
        "invocationReceipt": dict(receipt),
        "correctionAttempts": {
            "completed": completed_attempts,
            "cap": attempt_cap,
        },
        "exactInterruption": receipt["interruption"],
        "writerState": {
            "before": before,
            "after": after,
        },
        "verifierFindings": {
            "status": "NOT_RETURNED",
            "reason": "verifier interrupted before returning a verdict",
        },
        "preservedWriterState": preserved_after,
        "verifierMutatedWriterScope": False,
    }


def _write_pages(repository: Path, page_contents: dict[str, str]) -> None:
    """Write one deterministic set of fixture pages beneath the repository."""
    for relative_path, content in page_contents.items():
        destination = repository / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")


def _run_git(repository: Path, *arguments: str) -> subprocess.CompletedProcess[bytes]:
    """Run one successful Git fixture command and return its captured bytes."""
    return subprocess.run(
        ["git", *arguments],
        cwd=repository,
        check=True,
        capture_output=True,
    )


def _preserved_writer_state(
    repository: Path,
    page_inventory: tuple[str, ...],
) -> dict[str, object]:
    """Return canonical Git-derived evidence for the complete dirty wiki scope."""
    status_bytes = _run_git(
        repository,
        "status",
        "--porcelain=v1",
        "--untracked-files=all",
        "--",
        "docs/wiki",
    ).stdout
    status_records = _run_git(
        repository,
        "status",
        "--porcelain=v1",
        "-z",
        "--untracked-files=all",
        "--",
        "docs/wiki",
    ).stdout
    entries = _parse_porcelain_records(status_records)
    dirty_paths = sorted(
        {
            path
            for _status, paths in entries
            for path in paths
        }
    )
    supplied_paths = list(page_inventory)
    if len(set(supplied_paths)) != len(supplied_paths):
        raise ValueError("page inventory contains duplicate paths")
    expected_paths = set(supplied_paths)
    actual_paths = set(dirty_paths)
    if expected_paths != actual_paths:
        omitted = sorted(actual_paths - expected_paths)
        non_dirty = sorted(expected_paths - actual_paths)
        raise ValueError(
            "page inventory does not equal dirty docs/wiki scope: "
            f"omitted={omitted}; nonDirty={non_dirty}"
        )

    digest = hashlib.sha256()
    _digest_field(digest, "format", b"wiki-writer-preserved-state-v2")
    for entry_status, paths in sorted(entries, key=lambda entry: entry[1]):
        _digest_field(digest, "status", entry_status.encode("ascii"))
        for path in paths:
            _digest_field(digest, "status-path", path.encode("utf-8"))
    for path in dirty_paths:
        _digest_field(digest, "path", path.encode("utf-8"))
        baseline_tree_entry = _run_git(
            repository,
            "ls-tree",
            "-z",
            "HEAD",
            "--",
            path,
        ).stdout
        baseline_mode = (
            baseline_tree_entry.split(b" ", maxsplit=1)[0]
            if baseline_tree_entry
            else b"missing"
        )
        _digest_field(digest, "baseline-git-tree-mode", baseline_mode)
        baseline_result = subprocess.run(
            ["git", "show", f"HEAD:{path}"],
            cwd=repository,
            check=False,
            capture_output=True,
        )
        if baseline_result.returncode == 0:
            _digest_field(digest, "baseline-kind", b"file")
            _digest_field(digest, "baseline-bytes", baseline_result.stdout)
        else:
            _digest_field(digest, "baseline-kind", b"missing")
        index_entry = _run_git(
            repository,
            "ls-files",
            "--stage",
            "-z",
            "--",
            path,
        ).stdout
        index_mode = (
            index_entry.split(b" ", maxsplit=1)[0]
            if index_entry
            else b"missing"
        )
        _digest_field(digest, "index-git-mode", index_mode)
        index_result = subprocess.run(
            ["git", "show", f":{path}"],
            cwd=repository,
            check=False,
            capture_output=True,
        )
        if index_result.returncode == 0:
            _digest_field(digest, "index-kind", b"file")
            _digest_field(digest, "index-bytes", index_result.stdout)
        else:
            _digest_field(digest, "index-kind", b"missing")
        worktree_path = repository / path
        try:
            worktree_mode = worktree_path.lstat().st_mode
        except FileNotFoundError:
            _digest_field(digest, "worktree-lstat-mode-type", b"missing")
        else:
            _digest_field(
                digest,
                "worktree-lstat-mode-type",
                worktree_mode.to_bytes(8, byteorder="big"),
            )
        if worktree_path.is_symlink():
            _digest_field(digest, "worktree-kind", b"symlink")
            _digest_field(
                digest,
                "worktree-bytes",
                os.fsencode(os.readlink(worktree_path)),
            )
        elif worktree_path.is_file():
            _digest_field(digest, "worktree-kind", b"file")
            _digest_field(digest, "worktree-bytes", worktree_path.read_bytes())
        elif worktree_path.is_dir():
            _digest_field(digest, "worktree-kind", b"directory")
        else:
            _digest_field(digest, "worktree-kind", b"missing")

    return {
        "worktreeStatus": status_bytes.decode("utf-8").rstrip("\n"),
        "diffDigest": digest.hexdigest(),
        "paths": dirty_paths,
    }


def _parse_porcelain_records(
    status_records: bytes,
) -> tuple[tuple[str, tuple[str, ...]], ...]:
    """Parse Git porcelain v1 NUL records, retaining both rename endpoints."""
    fields = status_records.split(b"\0")
    entries: list[tuple[str, tuple[str, ...]]] = []
    field_index = 0
    while field_index < len(fields) and fields[field_index]:
        record = fields[field_index]
        field_index += 1
        if len(record) < 4 or record[2:3] != b" ":
            raise ValueError("Git returned an invalid porcelain status record")
        status = record[:2].decode("ascii")
        current_path = os.fsdecode(record[3:])
        if "R" in status or "C" in status:
            if field_index >= len(fields) or not fields[field_index]:
                raise ValueError("Git returned an incomplete rename status record")
            original_path = os.fsdecode(fields[field_index])
            field_index += 1
            paths = (original_path, current_path)
        else:
            paths = (current_path,)
        entries.append((status, paths))
    return tuple(entries)


def _digest_field(
    digest: object,
    label: str,
    value: bytes,
) -> None:
    """Add one length-delimited field to the canonical preserved-state digest."""
    digest.update(label.encode("ascii"))
    digest.update(b"\0")
    digest.update(len(value).to_bytes(8, byteorder="big"))
    digest.update(value)


def _invoke_verifier_process(
    repository: Path,
    page_inventory: tuple[str, ...],
    verifier_mode: _VerifierMode,
) -> tuple[dict[str, object], tuple[str, ...]]:
    """Run one verifier mode behind the separate-process offline audit model."""
    supported_modes = {
        "interrupted",
        "direct-write",
        "direct-write-restore",
        "dir-fd-write-restore",
        "replace-restore",
        "subprocess-write",
    }
    if verifier_mode not in supported_modes:
        raise ValueError(f"unsupported verifier mode: {verifier_mode}")
    completed = subprocess.run(
        [
            sys.executable,
            str(Path(__file__).resolve()),
            _CHILD_FLAG,
            verifier_mode,
            str(repository),
            json.dumps(page_inventory),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    parsed = json.loads(completed.stdout)
    if not isinstance(parsed, dict):
        raise ValueError("verifier process must return a JSON object")
    receipt = parsed.get("receipt")
    write_attempts = parsed.get("writeAttempts")
    if not isinstance(receipt, dict) or not isinstance(write_attempts, list):
        raise ValueError("verifier process returned invalid observation evidence")
    return receipt, tuple(str(path) for path in write_attempts)


def _run_verifier_child(
    verifier_mode: str,
    repository: Path,
    page_inventory: tuple[str, ...],
) -> dict[str, object]:
    """Exercise one deterministic attempted-write case in the offline audit model."""
    wiki_root = (repository / "docs" / "wiki").resolve()
    target = repository / page_inventory[0]
    write_attempts: list[str] = []
    directory_descriptor: int | None = None
    relative_open_directory: Path | None = None
    if verifier_mode == "dir-fd-write-restore":
        directory_descriptor = os.open(target.parent, os.O_RDONLY)
        relative_open_directory = target.parent.resolve()
    write_flags = (
        os.O_WRONLY
        | os.O_RDWR
        | os.O_CREAT
        | os.O_TRUNC
        | os.O_APPEND
    )

    def normalized_writer_path(path_argument: object) -> str | None:
        """Return a normalized writer path when an audit argument enters scope."""
        if not isinstance(path_argument, (str, bytes, os.PathLike)):
            return None
        attempted_path = Path(os.fsdecode(path_argument))
        if not attempted_path.is_absolute() and relative_open_directory is not None:
            attempted_path = relative_open_directory / attempted_path
        attempted_path = attempted_path.absolute()
        try:
            attempted_path.relative_to(wiki_root)
        except ValueError:
            pass
        else:
            return attempted_path.as_posix()
        try:
            attempted_path.resolve().relative_to(wiki_root)
        except ValueError:
            return None
        return attempted_path.as_posix()

    def reject_paths(arguments: tuple[object, ...], positions: tuple[int, ...]) -> None:
        """Reject and record any selected audit path inside the writer scope."""
        rejected = [
            normalized
            for position in positions
            if position < len(arguments)
            if (normalized := normalized_writer_path(arguments[position])) is not None
        ]
        if not rejected:
            return
        write_attempts.extend(rejected)
        raise PermissionError(
            "offline verifier mutation rejected: " + ", ".join(rejected)
        )

    def audit_write_attempt(event: str, arguments: tuple[object, ...]) -> None:
        """Reject the mutation events exercised by this deterministic callback."""
        if event == "open" and len(arguments) >= 3:
            _path_argument, mode_argument, flags_argument = arguments[:3]
            mode_writes = isinstance(mode_argument, str) and any(
                character in mode_argument for character in "wax+"
            )
            flags_write = isinstance(flags_argument, int) and bool(
                flags_argument & write_flags
            )
            if mode_writes or flags_write:
                reject_paths(arguments, (0,))
            return
        if event in {
            "os.remove",
            "os.rmdir",
            "os.mkdir",
            "os.chmod",
            "os.chown",
            "os.truncate",
            "os.utime",
        }:
            reject_paths(arguments, (0,))
            return
        if event in {"os.rename", "os.link", "os.symlink"}:
            reject_paths(arguments, (0, 1))
            return
        if event in {
            "subprocess.Popen",
            "os.system",
            "os.posix_spawn",
            "os.exec",
            "os.spawn",
            "os.fork",
            "os.forkpty",
            "pty.spawn",
        }:
            attempt = f"process:{event}"
            write_attempts.append(attempt)
            raise PermissionError(f"offline verifier process escape rejected: {event}")

    sys.addaudithook(audit_write_attempt)
    if verifier_mode == "direct-write":
        try:
            target.write_text("verifier mutation\n", encoding="utf-8")
        except PermissionError:
            pass
    elif verifier_mode == "direct-write-restore":
        original = target.read_text(encoding="utf-8")
        for content in ("verifier mutation\n", original):
            try:
                target.write_text(content, encoding="utf-8")
            except PermissionError:
                pass
    elif verifier_mode == "dir-fd-write-restore":
        if directory_descriptor is None:
            raise RuntimeError("dir-fd mode requires its fixture descriptor")
        try:
            relative_target = target.name
            for content in (b"verifier mutation\n", target.read_bytes()):
                try:
                    opened = os.open(
                        relative_target,
                        os.O_WRONLY | os.O_TRUNC,
                        dir_fd=directory_descriptor,
                    )
                except PermissionError:
                    pass
                else:
                    try:
                        os.write(opened, content)
                    finally:
                        os.close(opened)
        finally:
            os.close(directory_descriptor)
    elif verifier_mode == "replace-restore":
        with tempfile.TemporaryDirectory() as temporary:
            replacement = Path(temporary) / "replacement.md"
            replacement.write_bytes(b"verifier replacement\n")
            for source, destination in (
                (replacement, target),
                (target, replacement),
            ):
                try:
                    os.replace(source, destination)
                except PermissionError:
                    pass
    elif verifier_mode == "subprocess-write":
        try:
            subprocess.run(
                [
                    sys.executable,
                    "-c",
                    (
                        "from pathlib import Path; import sys; "
                        "Path(sys.argv[1]).write_bytes(b'verifier mutation\\n')"
                    ),
                    str(target),
                ],
                check=True,
            )
        except PermissionError:
            pass
    elif verifier_mode != "interrupted":
        raise ValueError(f"unsupported verifier child mode: {verifier_mode}")

    return {
        "receipt": {
            "agent": "wiki-topic-verifier",
            "invocation": 2,
            "outcome": "INTERRUPTED",
            "boundary": "OFFLINE_PYTHON_AUDIT_MODEL",
            "interruption": _INTERRUPTION,
        },
        "writeAttempts": write_attempts,
    }


def _writer_scope_fingerprint(repository: Path) -> str:
    """Return a stable path-and-content digest for the writer-owned docs/wiki tree."""
    digest = hashlib.sha256()
    wiki_root = repository / "docs" / "wiki"
    if not wiki_root.is_dir():
        return digest.hexdigest()
    files = (
        candidate
        for candidate in wiki_root.rglob("*")
        if candidate.is_file()
    )
    for path in sorted(files):
        relative_path = path.relative_to(repository).as_posix()
        digest.update(relative_path.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def _main() -> int:
    """Run the isolated verifier child entry point when requested."""
    if len(sys.argv) != 5 or sys.argv[1] != _CHILD_FLAG:
        raise SystemExit("offline harness is invoked through run_interruption_control")
    observation = _run_verifier_child(
        sys.argv[2],
        Path(sys.argv[3]),
        tuple(json.loads(sys.argv[4])),
    )
    print(json.dumps(observation, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
