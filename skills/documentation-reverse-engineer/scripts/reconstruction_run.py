#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Creates isolated reconstruction seeds and safely retains validated run archives.
# Governing design: skills/documentation-reverse-engineer/SKILL.md
# Governing test plan: scripts/test_reconstruction_run_helper.py

"""Prepare portable reconstruction inputs and safely retain evaluation archives."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence
from urllib.parse import unquote, urlsplit


__all__ = (
    "ReconstructionRunError",
    "initialize_run",
    "seal_archive_and_prune",
    "validate_seed",
    "validate_archive",
    "main",
)

_CONFIGURATION_NAMES = frozenset({"PROJECT.yaml", "AGENTS.md", "CLAUDE.md"})
_SKIPPED_CONFIGURATION_DIRECTORIES = frozenset(
    {
        ".git",
        ".gradle",
        ".idea",
        ".next",
        ".tox",
        ".venv",
        "build",
        "dist",
        "node_modules",
        "target",
        "vendor",
    }
)
_MARKDOWN_LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
_RUN_ID_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}\Z")
_WORKSTATION_HOME_PATH_PATTERNS = (
    re.compile(r"(?<![A-Za-z0-9._-])/(?:Users|home)/[^/\s'\"<>]+(?:/|\Z)"),
    re.compile(
        r"(?<![A-Za-z0-9._-])[A-Za-z]:[\\/]+Users[\\/]+[^\\/\s'\"<>]+",
        re.IGNORECASE,
    ),
)
_ARCHIVE_MANIFEST_NAME = "archive-manifest.json"
_SEED_METADATA_DIRECTORY = ".reconstruction"
_REQUIRED_ARCHIVE_FILES = (
    "RUN.json",
    "reset/source-baseline.json",
    "configuration/PROJECT.yaml",
    "configuration/AGENTS.md",
    "reviews/reconstruction-readiness.review-checklist-reconstruction-readiness.md",
    "seed/seed-manifest.json",
    "oracle/original-baseline.json",
    "parity/cases.json",
    "parity/reconciliation.json",
    "generators/delta-ledger.json",
    "contamination/ledger.json",
    "execution/commands.jsonl",
    "execution/results.json",
    "metrics/usage.json",
)
_REQUIRED_ARCHIVE_DIRECTORIES = (
    "documentation/docs/wiki",
    "reconstruction",
)


class ReconstructionRunError(RuntimeError):
    """Report a seed, isolation, archive-integrity, or retention contract failure."""


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _parse_timestamp(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise ReconstructionRunError(f"Invalid ISO-8601 timestamp: {value}") from error
    if parsed.tzinfo is None:
        raise ReconstructionRunError(f"Timestamp must include a timezone: {value}")
    return parsed.astimezone(timezone.utc)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _aggregate_digest(entries: Sequence[dict[str, object]]) -> str:
    digest = hashlib.sha256()
    for entry in entries:
        digest.update(str(entry["path"]).encode("utf-8"))
        digest.update(b"\0")
        digest.update(str(entry["sha256"]).encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_name(f".{path.name}.tmp")
    temporary_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary_path.replace(path)


def _relative_path(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _assert_project_relative(value: str) -> Path:
    relative_path = Path(value)
    if relative_path.is_absolute() or ".." in relative_path.parts:
        raise ReconstructionRunError(
            f"Explicit seed path must be project-relative without parent traversal: {value}"
        )
    return relative_path


def _assert_no_symlink_components(path: Path, root: Path) -> None:
    current = path
    while current != root:
        if current.is_symlink():
            raise ReconstructionRunError(
                f"Seed corpus contains a symbolic link: {_relative_path(current, root)}"
            )
        current = current.parent


def _assert_regular_independent_file(path: Path, root: Path) -> None:
    _assert_no_symlink_components(path, root)
    if not path.is_file():
        raise ReconstructionRunError(
            f"Seed corpus entry is not a regular file: {_relative_path(path, root)}"
        )
    if path.stat().st_nlink != 1:
        raise ReconstructionRunError(
            f"Seed corpus contains a hard link: {_relative_path(path, root)}"
        )


def _iter_tree_files(root: Path, project_root: Path) -> list[Path]:
    if root.is_symlink():
        raise ReconstructionRunError(
            f"Seed corpus contains a symbolic link: {_relative_path(root, project_root)}"
        )
    if root.is_file():
        return [root]
    if not root.is_dir():
        raise ReconstructionRunError(
            f"Seed corpus path does not exist: {_relative_path(root, project_root)}"
        )

    files: list[Path] = []
    for directory, directory_names, file_names in os.walk(root, followlinks=False):
        directory_path = Path(directory)
        for directory_name in directory_names:
            child = directory_path / directory_name
            if child.is_symlink():
                raise ReconstructionRunError(
                    "Seed corpus contains a symbolic link: "
                    f"{_relative_path(child, project_root)}"
                )
        for file_name in file_names:
            files.append(directory_path / file_name)
    return sorted(files)


def _discover_configuration_files(source_project: Path) -> set[Path]:
    configuration_files: set[Path] = set()
    for directory, directory_names, file_names in os.walk(
        source_project,
        followlinks=False,
    ):
        directory_names[:] = [
            name
            for name in directory_names
            if name not in _SKIPPED_CONFIGURATION_DIRECTORIES
            and not (Path(directory) / name).is_symlink()
        ]
        directory_path = Path(directory)
        for file_name in file_names:
            if file_name in _CONFIGURATION_NAMES:
                configuration_files.add(directory_path / file_name)
    return configuration_files


def _markdown_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        return target[1 : target.index(">")]
    return target.split(maxsplit=1)[0]


def _is_external_or_runtime_link(target: str) -> bool:
    if target.startswith("#"):
        return True
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc:
        return True
    return parsed.path.startswith("/")


def _resolve_inside_project(path: Path, source_project: Path) -> Path:
    lexical_path = Path(os.path.abspath(path))
    try:
        lexical_path.relative_to(source_project)
    except ValueError as error:
        raise ReconstructionRunError(
            f"Documentation link escapes the source project: {path}"
        ) from error
    _assert_no_symlink_components(lexical_path, source_project)
    try:
        resolved = lexical_path.resolve(strict=True)
    except FileNotFoundError as error:
        raise ReconstructionRunError(f"Unresolved local documentation link: {path}") from error
    try:
        resolved.relative_to(source_project)
    except ValueError as error:
        raise ReconstructionRunError(
            f"Documentation link escapes the source project: {path}"
        ) from error
    return resolved


def _is_document_or_configuration(path: Path, source_project: Path) -> bool:
    relative_path = path.relative_to(source_project)
    return (
        relative_path.parts[0] == "docs"
        or path.name in _CONFIGURATION_NAMES
        or path.name.lower() in {"readme.md", "readme.mdx", "readme.rst"}
    )


def _discover_linked_corpus(
    source_project: Path,
    documentation_files: set[Path],
    explicit_files: set[Path],
) -> tuple[set[Path], list[dict[str, str]]]:
    linked_files: set[Path] = set()
    queued_markdown = sorted(
        path
        for path in documentation_files | explicit_files
        if path.suffix.lower() in {".md", ".mdx"}
    )
    inspected: set[Path] = set()
    evidence_references: dict[tuple[str, str], dict[str, str]] = {}

    while queued_markdown:
        document = queued_markdown.pop(0)
        if document in inspected:
            continue
        inspected.add(document)
        try:
            text = document.read_text(encoding="utf-8")
        except UnicodeDecodeError as error:
            raise ReconstructionRunError(
                f"Markdown seed document is not UTF-8: {_relative_path(document, source_project)}"
            ) from error

        for raw_target in _MARKDOWN_LINK_PATTERN.findall(text):
            target = _markdown_target(raw_target)
            if not target or _is_external_or_runtime_link(target):
                continue
            parsed_target = urlsplit(target)
            local_path = unquote(parsed_target.path)
            if not local_path:
                continue
            candidate = document.parent / local_path
            resolved = _resolve_inside_project(candidate, source_project)
            linked_targets = _iter_tree_files(resolved, source_project)
            target_is_explicit = all(
                linked_target in explicit_files for linked_target in linked_targets
            )
            if (
                not _is_document_or_configuration(resolved, source_project)
                and not target_is_explicit
            ):
                document_path = _relative_path(document, source_project)
                target_path = _relative_path(resolved, source_project)
                evidence_references[(document_path, target_path)] = {
                    "document": document_path,
                    "kind": "source-evidence",
                    "target": target_path,
                }
                continue
            for linked_target in linked_targets:
                if (
                    linked_target not in documentation_files
                    and linked_target not in explicit_files
                ):
                    linked_files.add(linked_target)
                if linked_target.suffix.lower() in {".md", ".mdx"}:
                    queued_markdown.append(linked_target)

    return linked_files, [
        evidence_references[key] for key in sorted(evidence_references)
    ]


def _scan_for_absolute_source_path(
    path: Path,
    source_project: Path,
    source_spellings: Sequence[str],
) -> None:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return
    if any(
        source_text in text or f"file://{source_text}" in text
        for source_text in source_spellings
    ):
        raise ReconstructionRunError(
            "Seed corpus contains an absolute source path: "
            f"{_relative_path(path, source_project)}"
        )
    if any(pattern.search(text) for pattern in _WORKSTATION_HOME_PATH_PATTERNS):
        raise ReconstructionRunError(
            "Seed corpus contains a workstation-specific path: "
            f"{_relative_path(path, source_project)}"
        )


def _copy_files(files: Sequence[Path], source_project: Path, build_root: Path) -> None:
    for source_path in files:
        destination_path = build_root / source_path.relative_to(source_project)
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, destination_path)


def _entry_for_file(
    source_path: Path,
    source_project: Path,
    phase: str,
    origin: str,
) -> dict[str, object]:
    return {
        "origin": origin,
        "path": _relative_path(source_path, source_project),
        "phase": phase,
        "sha256": _sha256(source_path),
        "size": source_path.stat().st_size,
    }


def _validate_copied_seed(
    build_root: Path,
    source_project: Path,
    source_spellings: Sequence[str],
    expected_entries: Sequence[dict[str, object]],
) -> None:
    expected_paths = {str(entry["path"]) for entry in expected_entries}
    actual_paths = {
        _relative_path(path, build_root)
        for path in _iter_tree_files(build_root, build_root)
    }
    if actual_paths != expected_paths:
        missing = sorted(expected_paths - actual_paths)
        unexpected = sorted(actual_paths - expected_paths)
        raise ReconstructionRunError(
            f"Copied seed file set mismatch; missing={missing}, unexpected={unexpected}"
        )

    expected_by_path = {str(entry["path"]): entry for entry in expected_entries}
    for relative_path in sorted(expected_paths):
        copied_path = build_root / relative_path
        _assert_regular_independent_file(copied_path, build_root)
        if _sha256(copied_path) != expected_by_path[relative_path]["sha256"]:
            raise ReconstructionRunError(f"Copied seed hash mismatch: {relative_path}")
        _scan_for_absolute_source_path(
            copied_path,
            source_project,
            source_spellings,
        )


def initialize_run(
    source_project: Path,
    build_root: Path,
    run_id: str,
    source_baseline: str,
    extra_paths: Sequence[str] = (),
) -> dict[str, object]:
    """Create and validate a new reconstruction root from wiki-led documentation inputs.

    source_project identifies the existing repository. build_root is the separate destination
    and must not exist. run_id is a stable archive-safe identifier. source_baseline identifies
    the immutable original inventory. extra_paths names approved project-relative public-generator
    or parity inputs. The function copies the complete wiki first, then the complete documentation
    tree, linked root documents, and project guidance. It records source links as non-seed evidence
    references, hashes copied content, checks link closure and inode independence, and rejects
    absolute source-path contamination. It returns the validated run summary. On failure it raises
    ReconstructionRunError or the owning filesystem error and removes only the destination it
    created during this call.
    """
    supplied_source_project = source_project.expanduser().absolute()
    source_project = supplied_source_project.resolve(strict=True)
    source_spellings = tuple(
        sorted({str(supplied_source_project), str(source_project)})
    )
    build_root = build_root.expanduser().resolve(strict=False)
    if not source_project.is_dir():
        raise ReconstructionRunError(f"Source project is not a directory: {source_project}")
    if build_root.exists():
        raise ReconstructionRunError(
            f"Reconstruction initialization requires a brand-new build root: {build_root}"
        )
    if source_project == build_root or source_project in build_root.parents:
        raise ReconstructionRunError(
            "The reconstruction build root must be outside the source project"
        )
    if not _RUN_ID_PATTERN.fullmatch(run_id):
        raise ReconstructionRunError(f"Invalid run identifier: {run_id}")
    if not source_baseline.strip():
        raise ReconstructionRunError("Source baseline must not be blank")

    wiki_root = source_project / "docs" / "wiki"
    if not wiki_root.is_dir():
        raise ReconstructionRunError("The source project must contain docs/wiki")
    wiki_files = set(_iter_tree_files(wiki_root, source_project))
    if not wiki_files:
        raise ReconstructionRunError("The source wiki is empty")
    documentation_files = set(
        _iter_tree_files(source_project / "docs", source_project)
    )

    explicit_files: set[Path] = set()
    for value in extra_paths:
        explicit_path = source_project / _assert_project_relative(value)
        explicit_files.update(_iter_tree_files(explicit_path, source_project))
    configuration_files = _discover_configuration_files(source_project)
    linked_files, evidence_references = _discover_linked_corpus(
        source_project,
        documentation_files,
        explicit_files,
    )

    selected_files = (
        documentation_files | linked_files | configuration_files | explicit_files
    )
    for source_path in sorted(selected_files):
        _assert_regular_independent_file(source_path, source_project)
        _scan_for_absolute_source_path(
            source_path,
            source_project,
            source_spellings,
        )

    wiki_phase_files = sorted(wiki_files)
    second_phase_files = sorted(selected_files - wiki_files)
    entries: list[dict[str, object]] = []
    for source_path in wiki_phase_files:
        entries.append(
            _entry_for_file(source_path, source_project, "wiki-first", "wiki")
        )
    for source_path in second_phase_files:
        if source_path in explicit_files:
            origin = "explicit"
        elif source_path in configuration_files:
            origin = "configuration"
        else:
            origin = "linked-document"
        entries.append(
            _entry_for_file(
                source_path,
                source_project,
                "linked-docs-and-config",
                origin,
            )
        )

    build_root.parent.mkdir(parents=True, exist_ok=True)
    build_root.mkdir()
    try:
        _copy_files(wiki_phase_files, source_project, build_root)
        _copy_files(second_phase_files, source_project, build_root)
        _validate_copied_seed(
            build_root,
            source_project,
            source_spellings,
            entries,
        )

        created_at = _utc_now()
        phase_entries = {
            "wiki-first": [
                entry for entry in entries if entry["phase"] == "wiki-first"
            ],
            "linked-docs-and-config": [
                entry
                for entry in entries
                if entry["phase"] == "linked-docs-and-config"
            ],
        }
        seed_manifest = {
            "copyPhases": [
                {
                    "aggregateSha256": _aggregate_digest(phase_entries[phase_name]),
                    "fileCount": len(phase_entries[phase_name]),
                    "name": phase_name,
                }
                for phase_name in ("wiki-first", "linked-docs-and-config")
            ],
            "createdAt": created_at,
            "evidenceReferences": evidence_references,
            "files": entries,
            "runId": run_id,
            "schemaVersion": 1,
            "sourceBaseline": source_baseline,
            "validation": {
                "checks": [
                    "brand-new destination",
                    "wiki copied first",
                    "complete documentation tree copied",
                    "linked documentation and configuration closure",
                    "relative source evidence references recorded without copying source",
                    "configuration corpus included",
                    "source and destination hashes match",
                    "no symbolic links",
                    "no hard links",
                    "no absolute source paths",
                ],
                "status": "PASS",
            },
        }
        contamination_ledger = {
            "checks": [
                {
                    "findingCount": 0,
                    "name": "symbolic-links",
                    "status": "PASS",
                },
                {
                    "findingCount": 0,
                    "name": "hard-links",
                    "status": "PASS",
                },
                {
                    "findingCount": 0,
                    "name": "absolute-source-paths",
                    "status": "PASS",
                },
                {
                    "findingCount": 0,
                    "name": "workstation-home-paths",
                    "status": "PASS",
                },
            ],
            "runId": run_id,
            "schemaVersion": 1,
            "status": "PASS",
        }
        run_metadata = {
            "archiveRetention": 3,
            "contaminationLedger": (
                f"{_SEED_METADATA_DIRECTORY}/contamination-ledger.json"
            ),
            "copyOrder": ["wiki-first", "linked-docs-and-config"],
            "createdAt": created_at,
            "runId": run_id,
            "schemaVersion": 1,
            "seedManifest": f"{_SEED_METADATA_DIRECTORY}/seed-manifest.json",
            "sourceBaseline": source_baseline,
            "status": "SEED_VALIDATED",
        }
        metadata_root = build_root / _SEED_METADATA_DIRECTORY
        _write_json(metadata_root / "seed-manifest.json", seed_manifest)
        _write_json(metadata_root / "contamination-ledger.json", contamination_ledger)
        _write_json(metadata_root / "run-metadata.json", run_metadata)
    except Exception:
        shutil.rmtree(build_root)
        raise

    return {
        "buildRoot": build_root.name,
        "fileCount": len(entries),
        "runId": run_id,
        "seedManifest": f"{_SEED_METADATA_DIRECTORY}/seed-manifest.json",
        "validationStatus": "PASS",
    }


def validate_seed(build_root: Path, exact: bool = False) -> dict[str, object]:
    """Revalidate a copied seed from its portable manifest without source access.

    build_root identifies an initialized destination. exact additionally rejects files outside
    the copied seed and its three metadata records, so callers use exact mode before reconstruction
    code is written or against a preserved seed snapshot. The function verifies project-relative
    unique paths, phase membership and aggregate hashes, file sizes and SHA-256 digests, inode
    independence, and portable source-evidence references. It returns counts and PASS status
    without modifying the seed. Invalid manifests, files, phases, hashes, or references raise
    ReconstructionRunError; unreadable filesystem state preserves its owning error.
    """
    build_root = build_root.expanduser().resolve(strict=True)
    manifest_path = build_root / _SEED_METADATA_DIRECTORY / "seed-manifest.json"
    if not manifest_path.is_file():
        raise ReconstructionRunError("Seed manifest is missing")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise ReconstructionRunError("Seed manifest must contain a JSON object")
    if manifest.get("schemaVersion") != 1:
        raise ReconstructionRunError("Seed manifest schemaVersion must be 1")
    manifest_entries = manifest.get("files")
    if not isinstance(manifest_entries, list) or not manifest_entries:
        raise ReconstructionRunError("Seed manifest files must be a non-empty list")

    entries_by_path: dict[str, dict[str, object]] = {}
    entries_by_phase: dict[str, list[dict[str, object]]] = {
        "wiki-first": [],
        "linked-docs-and-config": [],
    }
    for raw_entry in manifest_entries:
        if not isinstance(raw_entry, dict):
            raise ReconstructionRunError("Seed manifest file entry must be an object")
        relative_value = raw_entry.get("path")
        phase = raw_entry.get("phase")
        if not isinstance(relative_value, str):
            raise ReconstructionRunError("Seed manifest file path must be a string")
        relative_path = _assert_project_relative(relative_value)
        normalized_path = relative_path.as_posix()
        if normalized_path in entries_by_path:
            raise ReconstructionRunError(
                f"Seed manifest contains a duplicate path: {normalized_path}"
            )
        if phase not in entries_by_phase:
            raise ReconstructionRunError(
                f"Seed manifest contains an unknown copy phase: {phase}"
            )
        entries_by_path[normalized_path] = raw_entry
        entries_by_phase[str(phase)].append(raw_entry)

        copied_path = build_root / relative_path
        _assert_regular_independent_file(copied_path, build_root)
        if copied_path.stat().st_size != raw_entry.get("size"):
            raise ReconstructionRunError(
                f"Copied seed size mismatch: {normalized_path}"
            )
        if _sha256(copied_path) != raw_entry.get("sha256"):
            raise ReconstructionRunError(
                f"Copied seed hash mismatch: {normalized_path}"
            )

    copy_phases = manifest.get("copyPhases")
    if not isinstance(copy_phases, list):
        raise ReconstructionRunError("Seed manifest copyPhases must be a list")
    expected_phase_order = ["wiki-first", "linked-docs-and-config"]
    recorded_phase_order = [
        phase.get("name") for phase in copy_phases if isinstance(phase, dict)
    ]
    if recorded_phase_order != expected_phase_order:
        raise ReconstructionRunError(
            "Seed manifest copy phases must record wiki-first before linked-docs-and-config"
        )
    for phase_record in copy_phases:
        if not isinstance(phase_record, dict):
            raise ReconstructionRunError("Seed manifest copy phase must be an object")
        phase_name = str(phase_record["name"])
        phase_entries = entries_by_phase[phase_name]
        if phase_record.get("fileCount") != len(phase_entries):
            raise ReconstructionRunError(
                f"Seed phase file count mismatch: {phase_name}"
            )
        if phase_record.get("aggregateSha256") != _aggregate_digest(phase_entries):
            raise ReconstructionRunError(
                f"Seed phase aggregate hash mismatch: {phase_name}"
            )

    evidence_references = manifest.get("evidenceReferences")
    if not isinstance(evidence_references, list):
        raise ReconstructionRunError("Seed manifest evidenceReferences must be a list")
    seen_references: set[tuple[str, str]] = set()
    for reference in evidence_references:
        if not isinstance(reference, dict) or reference.get("kind") != "source-evidence":
            raise ReconstructionRunError("Seed evidence reference is invalid")
        document = reference.get("document")
        target = reference.get("target")
        if not isinstance(document, str) or not isinstance(target, str):
            raise ReconstructionRunError("Seed evidence paths must be strings")
        document_path = _assert_project_relative(document).as_posix()
        target_path = _assert_project_relative(target).as_posix()
        if document_path not in entries_by_path:
            raise ReconstructionRunError(
                f"Seed evidence document is not copied: {document_path}"
            )
        reference_key = (document_path, target_path)
        if reference_key in seen_references:
            raise ReconstructionRunError(
                f"Seed manifest contains a duplicate evidence reference: {reference_key}"
            )
        seen_references.add(reference_key)

    if exact:
        metadata_paths = {
            f"{_SEED_METADATA_DIRECTORY}/contamination-ledger.json",
            f"{_SEED_METADATA_DIRECTORY}/run-metadata.json",
            f"{_SEED_METADATA_DIRECTORY}/seed-manifest.json",
        }
        actual_paths = {
            _relative_path(path, build_root)
            for path in _iter_tree_files(build_root, build_root)
        }
        expected_paths = set(entries_by_path) | metadata_paths
        if actual_paths != expected_paths:
            raise ReconstructionRunError(
                "Seed exact file inventory does not match; "
                f"missing={sorted(expected_paths - actual_paths)}, "
                f"unexpected={sorted(actual_paths - expected_paths)}"
            )

    return {
        "evidenceReferenceCount": len(evidence_references),
        "exact": exact,
        "fileCount": len(entries_by_path),
        "runId": manifest.get("runId"),
        "status": "PASS",
    }


def _assert_archive_candidate(archive: Path) -> str:
    if not archive.is_dir():
        raise ReconstructionRunError(f"Archive candidate is not a directory: {archive}")
    for relative_path in _REQUIRED_ARCHIVE_FILES:
        required_path = archive / relative_path
        if not required_path.is_file() or required_path.stat().st_size == 0:
            raise ReconstructionRunError(
                f"Missing or empty required archive entry: {relative_path}"
            )
    for relative_path in _REQUIRED_ARCHIVE_DIRECTORIES:
        required_directory = archive / relative_path
        if not required_directory.is_dir() or not any(
            path.is_file() for path in required_directory.rglob("*")
        ):
            raise ReconstructionRunError(
                f"Missing or empty required archive entry: {relative_path}"
            )

    run_data = json.loads((archive / "RUN.json").read_text(encoding="utf-8"))
    if not isinstance(run_data, dict):
        raise ReconstructionRunError("RUN.json must contain a JSON object")
    run_id = run_data.get("runId")
    if run_id != archive.name:
        raise ReconstructionRunError(
            f"RUN.json runId must equal archive folder name: {archive.name}"
        )

    for path in _iter_tree_files(archive, archive):
        _assert_regular_independent_file(path, archive)
    return str(run_id)


def validate_archive(archive: Path) -> dict[str, object]:
    """Validate one sealed archive against its exact file inventory and digests.

    archive identifies one sealed run folder. It must contain every mandatory evaluation
    artifact, a manifest whose run ID matches the folder, no symlink or hardlink, and exactly
    the files and hashes recorded in that manifest. The function returns the validated manifest
    without modifying the archive. Invalid or unreadable evidence raises ReconstructionRunError
    or preserves the owning JSON or filesystem error.
    """
    archive = archive.resolve(strict=True)
    manifest_path = archive / _ARCHIVE_MANIFEST_NAME
    if not manifest_path.is_file():
        raise ReconstructionRunError(
            f"Archive has no {_ARCHIVE_MANIFEST_NAME}: {archive.name}"
        )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("status") != "VALID":
        raise ReconstructionRunError(f"Archive status is not VALID: {archive.name}")
    if manifest.get("runId") != archive.name:
        raise ReconstructionRunError(
            f"Archive manifest runId does not match folder: {archive.name}"
        )
    completed_at = manifest.get("completedAt")
    if not isinstance(completed_at, str):
        raise ReconstructionRunError(f"Archive completedAt is missing: {archive.name}")
    _parse_timestamp(completed_at)
    _assert_archive_candidate(archive)

    actual_files = {
        _relative_path(path, archive): path
        for path in _iter_tree_files(archive, archive)
        if path.name != _ARCHIVE_MANIFEST_NAME
    }
    manifest_entries = manifest.get("files")
    if not isinstance(manifest_entries, list):
        raise ReconstructionRunError(f"Archive file inventory is invalid: {archive.name}")
    expected_entries = {
        str(entry.get("path")): entry
        for entry in manifest_entries
        if isinstance(entry, dict)
    }
    if set(actual_files) != set(expected_entries):
        raise ReconstructionRunError(
            f"Archive exact file inventory does not match: {archive.name}"
        )
    for relative_path, path in actual_files.items():
        expected_entry = expected_entries[relative_path]
        if path.stat().st_size != expected_entry.get("size"):
            raise ReconstructionRunError(
                f"Archive file size mismatch: {archive.name}/{relative_path}"
            )
        if _sha256(path) != expected_entry.get("sha256"):
            raise ReconstructionRunError(
                f"Archive file hash mismatch: {archive.name}/{relative_path}"
            )
    return manifest


def seal_archive_and_prune(
    new_archive: Path,
    archive_root: Path,
    retain: int = 3,
    completed_at: str | None = None,
) -> dict[str, object]:
    """Seal a complete run, verify it, then retain only the newest valid archives.

    new_archive identifies an unsealed run that is a direct child of archive_root. retain is the
    positive number of newest archives to keep. completed_at is an optional timezone-aware
    ISO-8601 completion time and defaults to the current UTC time. The function writes and
    independently validates an exact content manifest, validates every sibling archive, and only
    then deletes older validated runs. It returns the seal and retention result. Any invalid or
    unsealed run raises ReconstructionRunError before pruning and removes the new manifest so the
    incomplete seal cannot be mistaken for accepted evidence.
    """
    if retain < 1:
        raise ReconstructionRunError("Archive retention count must be at least one")
    archive_root = archive_root.expanduser().resolve(strict=True)
    new_archive = new_archive.expanduser().resolve(strict=True)
    if new_archive.parent != archive_root:
        raise ReconstructionRunError(
            "The new archive must be a direct child of the archive root"
        )
    manifest_path = new_archive / _ARCHIVE_MANIFEST_NAME
    if manifest_path.exists():
        raise ReconstructionRunError(f"Archive is already sealed: {new_archive.name}")

    run_id = _assert_archive_candidate(new_archive)
    completed_at = completed_at or _utc_now()
    _parse_timestamp(completed_at)
    archive_files = [
        path
        for path in _iter_tree_files(new_archive, new_archive)
        if path.name != _ARCHIVE_MANIFEST_NAME
    ]
    file_entries = [
        {
            "path": _relative_path(path, new_archive),
            "sha256": _sha256(path),
            "size": path.stat().st_size,
        }
        for path in archive_files
    ]
    manifest = {
        "completedAt": completed_at,
        "files": file_entries,
        "requiredDirectories": list(_REQUIRED_ARCHIVE_DIRECTORIES),
        "requiredFiles": list(_REQUIRED_ARCHIVE_FILES),
        "runId": run_id,
        "schemaVersion": 1,
        "status": "VALID",
    }
    _write_json(manifest_path, manifest)

    try:
        validate_archive(new_archive)
        validated_archives: list[tuple[datetime, str, Path]] = []
        for candidate in sorted(path for path in archive_root.iterdir() if path.is_dir()):
            candidate_manifest_path = candidate / _ARCHIVE_MANIFEST_NAME
            if not candidate_manifest_path.exists():
                raise ReconstructionRunError(
                    f"Archive root contains an unsealed run: {candidate.name}"
                )
            candidate_manifest = validate_archive(candidate)
            validated_archives.append(
                (
                    _parse_timestamp(str(candidate_manifest["completedAt"])),
                    str(candidate_manifest["runId"]),
                    candidate,
                )
            )
    except Exception:
        if manifest_path.exists():
            manifest_path.unlink()
        raise

    validated_archives.sort(key=lambda item: (item[0], item[1]))
    prune_candidates = validated_archives[:-retain]
    pruned_archives: list[str] = []
    for _, _, archive in prune_candidates:
        shutil.rmtree(archive)
        pruned_archives.append(archive.name)

    return {
        "archiveManifest": _ARCHIVE_MANIFEST_NAME,
        "prunedArchives": pruned_archives,
        "retainedArchives": [
            archive.name for _, _, archive in validated_archives[-retain:]
        ],
        "runId": run_id,
        "status": "VALID",
    }


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Prepare reconstruction seeds and safely seal evaluation archives."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    initialize_parser = subparsers.add_parser(
        "initialize",
        help="Create a validated wiki-first reconstruction seed in a new build root.",
    )
    initialize_parser.add_argument("--source-project", required=True, type=Path)
    initialize_parser.add_argument("--build-root", required=True, type=Path)
    initialize_parser.add_argument("--run-id", required=True)
    initialize_parser.add_argument("--source-baseline", required=True)
    initialize_parser.add_argument(
        "--include",
        action="append",
        default=[],
        help="Additional project-relative public-generator or parity input to copy.",
    )

    archive_parser = subparsers.add_parser(
        "seal-archive",
        help="Seal a complete archive and prune only after exact validation passes.",
    )
    archive_parser.add_argument("--new-archive", required=True, type=Path)
    archive_parser.add_argument("--archive-root", required=True, type=Path)
    archive_parser.add_argument("--retain", type=int, default=3)
    archive_parser.add_argument("--completed-at")
    validate_seed_parser = subparsers.add_parser(
        "validate-seed",
        help="Revalidate a copied seed from its manifest without source access.",
    )
    validate_seed_parser.add_argument("--build-root", required=True, type=Path)
    validate_seed_parser.add_argument(
        "--exact",
        action="store_true",
        help="Reject files outside the seed and its metadata records.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the portable command-line interface and return a process exit status.

    argv contains optional command arguments and defaults to the process arguments. The initialize
    command emits the validated seed summary, validate-seed emits its read-only assessment, and
    seal-archive emits the exact archive and retention result. Contract failures are written to
    standard error and return a nonzero status without pruning an unvalidated run; success writes
    JSON to standard output and returns zero.
    """
    arguments = _build_parser().parse_args(argv)
    try:
        if arguments.command == "initialize":
            result = initialize_run(
                source_project=arguments.source_project,
                build_root=arguments.build_root,
                run_id=arguments.run_id,
                source_baseline=arguments.source_baseline,
                extra_paths=arguments.include,
            )
        elif arguments.command == "seal-archive":
            result = seal_archive_and_prune(
                new_archive=arguments.new_archive,
                archive_root=arguments.archive_root,
                retain=arguments.retain,
                completed_at=arguments.completed_at,
            )
        else:
            result = validate_seed(
                build_root=arguments.build_root,
                exact=arguments.exact,
            )
    except (OSError, ReconstructionRunError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
