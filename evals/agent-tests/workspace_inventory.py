#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Captures complete workspace inventories and cleans only files created after a recorded baseline.
# Governing design: evals/agent-tests/implementation-plan.md
# Governing test plan: evals/agent-tests/test_workspace_inventory.py

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from pathlib import Path
from typing import Any, Sequence


_INVENTORY_SCHEMA = "dev-methodology-workspace-inventory"
_MUTATION_SCHEMA = "dev-methodology-workspace-mutation-evidence"


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _git_paths(root: Path, arguments: Sequence[str]) -> set[str]:
    completed = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z", *arguments],
        check=False,
        capture_output=True,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"Git workspace classification failed: {' '.join(arguments)}: "
            f"{completed.stderr.decode('utf-8', errors='replace').strip()}"
        )
    return {
        value.decode("utf-8", errors="surrogateescape")
        for value in completed.stdout.split(b"\0")
        if value
    }


def _git_states(root: Path) -> dict[str, str]:
    tracked = _git_paths(root, ("--cached",))
    ignored = _git_paths(root, ("--others", "--ignored", "--exclude-standard"))
    untracked = _git_paths(root, ("--others", "--exclude-standard"))
    return {
        **{path: "tracked" for path in tracked},
        **{path: "ignored" for path in ignored},
        **{path: "untracked" for path in untracked},
    }


def _git_metadata(root: Path) -> dict[str, str | None]:
    def output(arguments: Sequence[str]) -> bytes:
        completed = subprocess.run(
            ["git", "-C", str(root), *arguments],
            check=False,
            capture_output=True,
        )
        if completed.returncode != 0:
            raise RuntimeError(
                f"Git workspace metadata failed: {' '.join(arguments)}: "
                f"{completed.stderr.decode('utf-8', errors='replace').strip()}"
            )
        return completed.stdout

    symbolic_head = subprocess.run(
        ["git", "-C", str(root), "symbolic-ref", "-q", "HEAD"],
        check=False,
        capture_output=True,
        text=True,
    )
    if symbolic_head.returncode not in (0, 1):
        raise RuntimeError(f"Git HEAD classification failed: {symbolic_head.stderr.strip()}")
    return {
        "head": output(("rev-parse", "HEAD")).decode("ascii").strip(),
        "symbolicHead": symbolic_head.stdout.strip() or None,
        "indexSha256": _sha256_bytes(output(("ls-files", "-z", "--stage", "--debug"))),
        "refsSha256": _sha256_bytes(
            output(("for-each-ref", "--format=%(refname)%00%(objectname)%00"))
        ),
    }


def _entry(root: Path, path: Path, git_states: dict[str, str]) -> dict[str, str]:
    relative = path.relative_to(root).as_posix()
    mode = f"{path.lstat().st_mode & 0o7777:04o}"
    if path.is_symlink():
        return {
            "path": relative,
            "kind": "symlink",
            "mode": mode,
            "sha256": _sha256_bytes(os.readlink(path).encode("utf-8", errors="surrogateescape")),
            "gitState": git_states.get(relative, "untracked"),
        }
    if path.is_dir():
        return {"path": relative, "kind": "directory", "mode": mode}
    return {
        "path": relative,
        "kind": "file",
        "mode": mode,
        "sha256": _sha256_bytes(path.read_bytes()),
        "gitState": git_states.get(relative, "untracked"),
    }


def _inventory(root: Path) -> dict[str, Any]:
    resolved_root = root.resolve(strict=True)
    if not resolved_root.is_dir():
        raise ValueError(f"Workspace inventory root is not a directory: {root}")
    git_states = _git_states(resolved_root)
    paths: list[Path] = []
    for current, directory_names, file_names in os.walk(resolved_root, followlinks=False):
        directory_names[:] = sorted(name for name in directory_names if name != ".git")
        current_path = Path(current)
        for name in directory_names:
            paths.append(current_path / name)
        for name in sorted(file_names):
            paths.append(current_path / name)
    return {
        "schema": _INVENTORY_SCHEMA,
        "version": 1,
        "root": str(resolved_root),
        "git": _git_metadata(resolved_root),
        "entries": [_entry(resolved_root, path, git_states) for path in sorted(paths)],
    }


def _canonical_sha256(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return _sha256_bytes(encoded)


def _load_baseline(path: Path, root: Path) -> dict[str, Any]:
    loaded = json.loads(path.read_text(encoding="utf-8"))
    if (
        not isinstance(loaded, dict)
        or loaded.get("schema") != _INVENTORY_SCHEMA
        or loaded.get("version") != 1
        or loaded.get("root") != str(root.resolve(strict=True))
        or not isinstance(loaded.get("git"), dict)
        or not isinstance(loaded.get("entries"), list)
    ):
        raise ValueError("Baseline is not a matching workspace inventory")
    return loaded


def _changes(baseline: dict[str, Any], observed: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    before = {str(entry["path"]): entry for entry in baseline["entries"]}
    after = {str(entry["path"]): entry for entry in observed["entries"]}
    return {
        "created": [after[path] for path in sorted(after.keys() - before.keys())],
        "modified": [
            {"path": path, "before": before[path], "after": after[path]}
            for path in sorted(before.keys() & after.keys())
            if before[path] != after[path]
        ],
        "deleted": [before[path] for path in sorted(before.keys() - after.keys())],
        "gitMetadata": (
            []
            if baseline["git"] == observed["git"]
            else [{"before": baseline["git"], "after": observed["git"]}]
        ),
    }


def _cleanup_created(root: Path, created: Sequence[dict[str, Any]]) -> tuple[list[str], list[str]]:
    removed: list[str] = []
    preserved: list[str] = []
    files = [entry for entry in created if entry.get("kind") != "directory"]
    directories = sorted(
        (entry for entry in created if entry.get("kind") == "directory"),
        key=lambda entry: len(Path(str(entry["path"])).parts),
        reverse=True,
    )
    for entry in [*files, *directories]:
        relative = str(entry["path"])
        candidate = root / relative
        try:
            if candidate.is_symlink() or candidate.is_file():
                candidate.unlink()
            elif candidate.is_dir():
                candidate.rmdir()
            else:
                preserved.append(relative)
                continue
        except OSError:
            preserved.append(relative)
            continue
        removed.append(relative)
    return sorted(removed), sorted(preserved)


def _mutation_evidence(root: Path, baseline_path: Path, cleanup_created: bool) -> dict[str, Any]:
    baseline = _load_baseline(baseline_path, root)
    observed = _inventory(root)
    detected = _changes(baseline, observed)
    removed: list[str] = []
    preserved: list[str] = []
    if cleanup_created:
        removed, preserved = _cleanup_created(root.resolve(strict=True), detected["created"])
    final = _inventory(root)
    remaining = _changes(baseline, final)
    side_effects_detected = any(detected.values())
    return {
        "schema": _MUTATION_SCHEMA,
        "version": 1,
        "root": str(root.resolve(strict=True)),
        "baseline": baseline,
        "baselineSha256": _canonical_sha256(baseline),
        "observed": observed,
        "observedSha256": _canonical_sha256(observed),
        "detected": detected,
        "derivedMutationClaim": "side-effects-detected" if side_effects_detected else "no-changes-detected",
        "preExisting": {
            "ignored": sorted(
                str(entry["path"]) for entry in baseline["entries"] if entry.get("gitState") == "ignored"
            ),
            "untracked": sorted(
                str(entry["path"]) for entry in baseline["entries"] if entry.get("gitState") == "untracked"
            ),
        },
        "cleanup": {
            "requested": cleanup_created,
            "removed": removed,
            "preserved": preserved,
        },
        "final": final,
        "finalSha256": _canonical_sha256(final),
        "remaining": remaining,
        "finalMatchesBaseline": not any(remaining.values()),
    }


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _parse_arguments(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Capture and compare complete workspace inventories")
    subparsers = parser.add_subparsers(dest="command", required=True)
    snapshot = subparsers.add_parser("snapshot")
    snapshot.add_argument("--root", type=Path, required=True)
    snapshot.add_argument("--output", type=Path, required=True)
    reconcile = subparsers.add_parser("reconcile")
    reconcile.add_argument("--root", type=Path, required=True)
    reconcile.add_argument("--baseline", type=Path, required=True)
    reconcile.add_argument("--output", type=Path, required=True)
    reconcile.add_argument("--cleanup-created", action="store_true")
    return parser.parse_args(argv)


def _main(argv: Sequence[str] | None = None) -> int:
    arguments = _parse_arguments(argv)
    if arguments.command == "snapshot":
        _write_json(arguments.output, _inventory(arguments.root))
    else:
        _write_json(
            arguments.output,
            _mutation_evidence(arguments.root, arguments.baseline, arguments.cleanup_created),
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
