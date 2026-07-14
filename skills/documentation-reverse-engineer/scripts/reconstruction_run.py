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
from typing import Mapping, Sequence
from urllib.parse import unquote, urlsplit


__all__ = (
    "ReconstructionRunError",
    "compare_archive_attestation",
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
    re.compile(r"(?<![A-Za-z0-9._-])/Users/[A-Za-z0-9._-]+(?:/|\Z)"),
    re.compile(
        r"(?<![A-Za-z0-9._-])/home/[A-Za-z0-9._-]+/"
        r"(?:dev|src|repos?|projects?|work|workspaces?|worktrees?|checkouts?|"
        r"\.cache|\.local|tmp)(?:/|\Z)",
        re.IGNORECASE,
    ),
    re.compile(
        r"(?<![A-Za-z0-9._-])[A-Za-z]:[\\/]+Users[\\/]+[A-Za-z0-9._-]+",
        re.IGNORECASE,
    ),
)
_ARCHIVE_MANIFEST_NAME = "archive-manifest.json"
_ARCHIVE_ATTESTATION_SUFFIX = ".attestation.json"
_ARCHIVE_SCHEMA_VERSION = 2
_ARCHIVE_SEMANTIC_CONTRACT = "reconstruction-archive-v2"
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
_REQUIRED_V2_ARCHIVE_FILES = (
    "reset/git-reconciliation.json",
    "parity/evaluator-manifest.json",
    "execution/provenance.json",
)
_REQUIRED_V2_DOCUMENTATION_DIRECTORIES = (
    "documentation/docs/architecture",
    "documentation/docs/functional",
    "documentation/docs/high-level",
    "documentation/docs/modules",
    "documentation/docs/wiki",
)
_REQUIRED_ISOLATION_CHANNELS = frozenset(
    {
        "alternate-path",
        "cache",
        "canonical-path",
        "environment-variable",
        "hardlink",
        "parent-traversal",
        "symlink",
        "temporary-file",
    }
)
_RUN_TERMINAL_STATUSES = frozenset({"BLOCKED", "FAILED", "READY"})
_HEX_SHA256_PATTERN = re.compile(r"[0-9a-f]{64}\Z")


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


def _load_json_object(path: Path, label: str) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or not payload:
        raise ReconstructionRunError(f"{label} must contain a non-empty JSON object")
    return payload


def _require_nonempty_string(
    payload: Mapping[str, object],
    key: str,
    label: str,
) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ReconstructionRunError(f"{label} {key} must be a non-empty string")
    return value


def _require_sha256(
    payload: Mapping[str, object],
    key: str,
    label: str,
) -> str:
    value = _require_nonempty_string(payload, key, label)
    if not _HEX_SHA256_PATTERN.fullmatch(value):
        raise ReconstructionRunError(f"{label} {key} must be a lowercase SHA-256 digest")
    return value


def _require_nonempty_sequence(
    payload: Mapping[str, object],
    key: str,
    label: str,
) -> list[object]:
    value = payload.get(key)
    if not isinstance(value, list) or not value:
        raise ReconstructionRunError(f"{label} {key} must be a non-empty list")
    return value


def _require_sequence(
    payload: Mapping[str, object],
    key: str,
    label: str,
) -> list[object]:
    value = payload.get(key)
    if not isinstance(value, list):
        raise ReconstructionRunError(f"{label} {key} must be a list")
    return value


def _binding_digest(*values: str) -> str:
    digest = hashlib.sha256()
    for value in values:
        digest.update(value.encode("utf-8"))
        digest.update(b"\0")
    return digest.hexdigest()


def _validate_evidence_reference(
    archive: Path,
    payload: Mapping[str, object],
    path_key: str,
    digest_key: str,
    label: str,
) -> Path:
    relative_value = _require_nonempty_string(payload, path_key, label)
    relative_path = _assert_project_relative(relative_value)
    if relative_path.name == _ARCHIVE_MANIFEST_NAME:
        raise ReconstructionRunError(f"{label} cannot use the archive manifest as evidence")
    evidence_path = archive / relative_path
    _assert_regular_independent_file(evidence_path, archive)
    expected_digest = _require_sha256(payload, digest_key, label)
    if _sha256(evidence_path) != expected_digest:
        raise ReconstructionRunError(f"{label} evidence hash mismatch: {relative_value}")
    return evidence_path


def _validate_run_record(
    archive: Path,
    run_id: str,
) -> tuple[dict[str, object], datetime, datetime]:
    run_data = _load_json_object(archive / "RUN.json", "RUN.json")
    if run_data.get("schemaVersion") != _ARCHIVE_SCHEMA_VERSION:
        raise ReconstructionRunError("Schema-v2 archive RUN.json must use schemaVersion 2")
    if run_data.get("runId") != run_id:
        raise ReconstructionRunError("RUN.json runId does not match the archive folder")
    status = _require_nonempty_string(run_data, "status", "RUN.json")
    if status not in _RUN_TERMINAL_STATUSES:
        raise ReconstructionRunError(
            f"RUN.json status must be one of {sorted(_RUN_TERMINAL_STATUSES)}"
        )
    _require_nonempty_string(run_data, "sourceBaseline", "RUN.json")
    nonce = _require_nonempty_string(run_data, "executionNonce", "RUN.json")
    if len(nonce) < 16:
        raise ReconstructionRunError("RUN.json executionNonce must contain at least 16 characters")
    started_at = _parse_timestamp(
        _require_nonempty_string(run_data, "startedAt", "RUN.json")
    )
    finished_at = _parse_timestamp(
        _require_nonempty_string(run_data, "finishedAt", "RUN.json")
    )
    if finished_at < started_at:
        raise ReconstructionRunError("RUN.json finishedAt precedes startedAt")
    return run_data, started_at, finished_at


def _validate_documentation_and_guidance(
    archive: Path,
    run_id: str,
) -> dict[str, object]:
    seed_manifest = _load_json_object(
        archive / "seed" / "seed-manifest.json",
        "seed/seed-manifest.json",
    )
    if seed_manifest.get("runId") != run_id:
        raise ReconstructionRunError("Seed manifest runId does not match the archive")
    if seed_manifest.get("status") == "NOT_RUN":
        _validate_not_run_record(archive, seed_manifest, "Seed manifest")
        for relative_directory in _REQUIRED_V2_DOCUMENTATION_DIRECTORIES:
            status_path = archive / relative_directory / "NOT_RUN.json"
            status_record = _load_json_object(
                status_path,
                f"{relative_directory}/NOT_RUN.json",
            )
            if status_record.get("runId") != run_id or status_record.get("status") != "NOT_RUN":
                raise ReconstructionRunError(
                    f"{relative_directory}/NOT_RUN.json is not bound to this run"
                )
            _validate_not_run_record(
                archive,
                status_record,
                f"{relative_directory}/NOT_RUN.json",
            )
        for relative_path in ("configuration/PROJECT.yaml", "configuration/AGENTS.md"):
            text = (archive / relative_path).read_text(encoding="utf-8")
            if "NOT_RUN" not in text or run_id not in text:
                raise ReconstructionRunError(
                    f"{relative_path} must record the project-guidance NOT_RUN state"
                )
        return seed_manifest
    seed_entries = _require_nonempty_sequence(
        seed_manifest,
        "files",
        "seed/seed-manifest.json",
    )
    entries_by_path: dict[str, Mapping[str, object]] = {}
    for raw_entry in seed_entries:
        if not isinstance(raw_entry, dict):
            raise ReconstructionRunError("Seed manifest file entry must be an object")
        relative_value = _require_nonempty_string(raw_entry, "path", "Seed file entry")
        normalized_path = _assert_project_relative(relative_value).as_posix()
        if normalized_path in entries_by_path:
            raise ReconstructionRunError(
                f"Seed manifest contains a duplicate path: {normalized_path}"
            )
        _require_sha256(raw_entry, "sha256", f"Seed file entry {normalized_path}")
        entries_by_path[normalized_path] = raw_entry

    for relative_directory in _REQUIRED_V2_DOCUMENTATION_DIRECTORIES:
        directory = archive / relative_directory
        if not directory.is_dir() or not any(path.is_file() for path in directory.rglob("*")):
            raise ReconstructionRunError(
                f"Schema-v2 archive documentation hierarchy is missing: {relative_directory}"
            )

    expected_documentation = {
        f"documentation/{path}": entry
        for path, entry in entries_by_path.items()
        if path == "docs" or path.startswith("docs/")
    }
    actual_documentation = {
        _relative_path(path, archive): path
        for path in _iter_tree_files(archive / "documentation" / "docs", archive)
    }
    if set(actual_documentation) != set(expected_documentation):
        raise ReconstructionRunError(
            "Archived documentation does not exactly mirror the validated seed; "
            f"missing={sorted(set(expected_documentation) - set(actual_documentation))}, "
            f"unexpected={sorted(set(actual_documentation) - set(expected_documentation))}"
        )
    for relative_path, seed_entry in expected_documentation.items():
        if _sha256(actual_documentation[relative_path]) != seed_entry["sha256"]:
            raise ReconstructionRunError(
                f"Archived documentation differs from the validated seed: {relative_path}"
            )

    expected_configuration = {
        f"configuration/{path}": entry
        for path, entry in entries_by_path.items()
        if Path(path).name in _CONFIGURATION_NAMES
    }
    for required_root in ("configuration/PROJECT.yaml", "configuration/AGENTS.md"):
        if required_root not in expected_configuration:
            raise ReconstructionRunError(
                f"Validated seed does not contain required root guidance: {required_root}"
            )
    actual_configuration = {
        _relative_path(path, archive): path
        for path in _iter_tree_files(archive / "configuration", archive)
    }
    if set(actual_configuration) != set(expected_configuration):
        raise ReconstructionRunError(
            "Archived project guidance does not exactly mirror root and nested seed guidance; "
            f"missing={sorted(set(expected_configuration) - set(actual_configuration))}, "
            f"unexpected={sorted(set(actual_configuration) - set(expected_configuration))}"
        )
    for relative_path, seed_entry in expected_configuration.items():
        if _sha256(actual_configuration[relative_path]) != seed_entry["sha256"]:
            raise ReconstructionRunError(
                f"Archived project guidance differs from the validated seed: {relative_path}"
            )
    return seed_manifest


def _validate_git_snapshot(snapshot: object, label: str) -> None:
    if not isinstance(snapshot, dict) or not snapshot:
        raise ReconstructionRunError(f"{label} must be a non-empty object")
    for key in ("head", "tree"):
        value = _require_nonempty_string(snapshot, key, label)
        if value != "UNBORN" and not re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", value):
            raise ReconstructionRunError(f"{label} {key} is not a Git object ID")
    _require_sha256(snapshot, "statusSha256", label)
    _require_sha256(snapshot, "gitMetadataSha256", label)


def _validate_git_reconciliation(archive: Path, run_id: str) -> None:
    path = archive / "reset" / "git-reconciliation.json"
    payload = _load_json_object(path, "reset/git-reconciliation.json")
    if payload.get("schemaVersion") != 2 or payload.get("runId") != run_id:
        raise ReconstructionRunError("Git reconciliation schema or runId is invalid")
    if payload.get("status") != "PASS":
        raise ReconstructionRunError("Git reconciliation status must be PASS")
    stages = _require_nonempty_sequence(payload, "stages", "Git reconciliation")
    seen_stage_ids: set[str] = set()
    for raw_stage in stages:
        if not isinstance(raw_stage, dict):
            raise ReconstructionRunError("Git reconciliation stage must be an object")
        stage_id = _require_nonempty_string(raw_stage, "id", "Git reconciliation stage")
        if stage_id in seen_stage_ids:
            raise ReconstructionRunError(f"Duplicate Git reconciliation stage: {stage_id}")
        seen_stage_ids.add(stage_id)
        _require_nonempty_string(raw_stage, "commandId", f"Git stage {stage_id}")
        _validate_git_snapshot(raw_stage.get("before"), f"Git stage {stage_id} before")
        _validate_git_snapshot(raw_stage.get("after"), f"Git stage {stage_id} after")
        if not isinstance(raw_stage.get("changes"), list):
            raise ReconstructionRunError(f"Git stage {stage_id} changes must be a list")
        if raw_stage.get("unexpectedChanges") != []:
            raise ReconstructionRunError(
                f"Git stage {stage_id} has missing or unresolved unexpected changes"
            )

    transient_changes = _require_nonempty_sequence(
        payload,
        "transientChanges",
        "Git reconciliation",
    )
    claim_registry_reconciled = False
    for change in transient_changes:
        if not isinstance(change, dict):
            raise ReconstructionRunError("Git transient change must be an object")
        change_path = _require_nonempty_string(change, "path", "Git transient change")
        resolution = _require_nonempty_string(change, "resolution", "Git transient change")
        if change_path.endswith("agent-claims.json") and resolution in {"RELEASED", "RESTORED"}:
            claim_registry_reconciled = True
    if not claim_registry_reconciled:
        raise ReconstructionRunError(
            "Git reconciliation must include the transient agent-claims registry resolution"
        )

    claim_lifecycle = payload.get("claimLifecycle")
    if not isinstance(claim_lifecycle, dict) or not claim_lifecycle:
        raise ReconstructionRunError("Git reconciliation claimLifecycle must be an object")
    if claim_lifecycle.get("acquired") is not True or claim_lifecycle.get("released") is not True:
        raise ReconstructionRunError("Git reconciliation must prove claim acquire and release")
    if claim_lifecycle.get("status") != "PASS":
        raise ReconstructionRunError("Git reconciliation claimLifecycle status must be PASS")
    _require_sha256(claim_lifecycle, "registryBeforeSha256", "Claim lifecycle")
    _require_sha256(claim_lifecycle, "registryAfterSha256", "Claim lifecycle")


def _validate_isolation_ledger(
    archive: Path,
    run_id: str,
    run_status: str,
) -> None:
    payload = _load_json_object(
        archive / "contamination" / "ledger.json",
        "contamination/ledger.json",
    )
    if payload.get("schemaVersion") != 2 or payload.get("runId") != run_id:
        raise ReconstructionRunError("Contamination ledger schema or runId is invalid")
    if payload.get("status") != "PASS":
        raise ReconstructionRunError("Contamination ledger evidence status must be PASS")
    environments = _require_nonempty_sequence(payload, "environments", "Contamination ledger")
    environments_by_role: dict[str, Mapping[str, object]] = {}
    sandbox_identities: set[str] = set()
    for raw_environment in environments:
        if not isinstance(raw_environment, dict):
            raise ReconstructionRunError("Isolation environment must be an object")
        role = _require_nonempty_string(raw_environment, "role", "Isolation environment")
        if role in environments_by_role:
            raise ReconstructionRunError(f"Duplicate isolation environment role: {role}")
        environments_by_role[role] = raw_environment
        status = _require_nonempty_string(raw_environment, "status", f"{role} isolation")
        if status == "NOT_RUN":
            _require_nonempty_string(raw_environment, "unmetGate", f"{role} isolation")
            _validate_evidence_reference(
                archive,
                raw_environment,
                "failureEvidence",
                "failureEvidenceSha256",
                f"{role} isolation NOT_RUN",
            )
            continue
        if status not in {"FAIL", "PASS"}:
            raise ReconstructionRunError(f"{role} isolation status is invalid: {status}")
        if raw_environment.get("originalSourceMounted") is not False:
            raise ReconstructionRunError(f"{role} isolation mounted or did not account for source")
        sandbox_identity = _require_nonempty_string(
            raw_environment,
            "sandboxIdentity",
            f"{role} isolation",
        )
        if sandbox_identity in sandbox_identities:
            raise ReconstructionRunError("Builder and verifier must use distinct sandboxes")
        sandbox_identities.add(sandbox_identity)
        _require_sha256(raw_environment, "environmentSha256", f"{role} isolation")
        _require_nonempty_sequence(raw_environment, "mountInventory", f"{role} isolation")
        probes = _require_nonempty_sequence(raw_environment, "deniedAccessProbes", f"{role} isolation")
        probes_by_channel: dict[str, Mapping[str, object]] = {}
        for raw_probe in probes:
            if not isinstance(raw_probe, dict):
                raise ReconstructionRunError(f"{role} isolation probe must be an object")
            channel = _require_nonempty_string(raw_probe, "channel", f"{role} isolation probe")
            if channel in probes_by_channel:
                raise ReconstructionRunError(f"Duplicate {role} isolation channel: {channel}")
            probes_by_channel[channel] = raw_probe
            if raw_probe.get("status") != "DENIED":
                raise ReconstructionRunError(f"{role} isolation channel was not denied: {channel}")
            readers = _require_nonempty_sequence(raw_probe, "readers", f"{role} {channel} probe")
            reader_names: set[str] = set()
            for raw_reader in readers:
                if not isinstance(raw_reader, dict):
                    raise ReconstructionRunError(f"{role} {channel} reader must be an object")
                reader_name = _require_nonempty_string(raw_reader, "name", f"{role} {channel} reader")
                reader_names.add(reader_name)
                if raw_reader.get("attemptedByteRead") is not True or raw_reader.get("status") != "DENIED":
                    raise ReconstructionRunError(
                        f"{role} {channel} reader did not prove a denied byte read"
                    )
                _validate_evidence_reference(
                    archive,
                    raw_reader,
                    "evidence",
                    "evidenceSha256",
                    f"{role} {channel} reader",
                )
            if len(reader_names) < 2:
                raise ReconstructionRunError(
                    f"{role} {channel} isolation requires two independent readers"
                )
        if set(probes_by_channel) != _REQUIRED_ISOLATION_CHANNELS:
            raise ReconstructionRunError(
                f"{role} isolation channel inventory mismatch; "
                f"missing={sorted(_REQUIRED_ISOLATION_CHANNELS - set(probes_by_channel))}, "
                f"unexpected={sorted(set(probes_by_channel) - _REQUIRED_ISOLATION_CHANNELS)}"
            )

    if set(environments_by_role) != {"builder", "verifier"}:
        raise ReconstructionRunError("Contamination ledger must contain builder and verifier environments")
    if run_status == "READY" and any(
        environment.get("status") != "PASS" for environment in environments_by_role.values()
    ):
        raise ReconstructionRunError("A READY run requires passing builder and verifier isolation")
    findings = payload.get("findings")
    unresolved = payload.get("unresolvedContaminationFindings")
    if not isinstance(findings, list) or not isinstance(unresolved, int) or unresolved < 0:
        raise ReconstructionRunError("Contamination ledger findings are invalid")
    if run_status == "READY" and unresolved != 0:
        raise ReconstructionRunError("A READY run has unresolved contamination findings")


def _validate_case_catalog(
    archive: Path,
    run_id: str,
) -> tuple[dict[str, Mapping[str, object]], set[str], set[str]]:
    payload = _load_json_object(archive / "parity" / "cases.json", "parity/cases.json")
    if payload.get("schemaVersion") != 2 or payload.get("runId") != run_id:
        raise ReconstructionRunError("Parity case catalog schema or runId is invalid")
    if payload.get("status") == "NOT_RUN":
        if payload.get("cases") != [] or payload.get("requiredCaseCount") != 0:
            raise ReconstructionRunError("NOT_RUN parity catalog must contain zero cases")
        _validate_not_run_record(archive, payload, "Parity case catalog NOT_RUN")
        return {}, set(), set()
    cases = _require_nonempty_sequence(payload, "cases", "Parity case catalog")
    cases_by_id: dict[str, Mapping[str, object]] = {}
    required_native_proofs: set[str] = set()
    required_report_kinds: set[str] = set()
    for raw_case in cases:
        if not isinstance(raw_case, dict):
            raise ReconstructionRunError("Parity case must be an object")
        case_id = _require_nonempty_string(raw_case, "id", "Parity case")
        if case_id in cases_by_id:
            raise ReconstructionRunError(f"Duplicate parity case ID: {case_id}")
        cases_by_id[case_id] = raw_case
        for key in (
            "owner",
            "originalCommand",
            "reconstructionCommand",
            "comparisonPolicy",
            "requiredProbeKind",
            "mandatoryExecutionStrength",
        ):
            _require_nonempty_string(raw_case, key, f"Parity case {case_id}")
        for key in ("preconditions", "inputs", "requiredEvidence"):
            _require_nonempty_sequence(raw_case, key, f"Parity case {case_id}")
        native_proof_id = raw_case.get("requiredNativeProofId")
        if native_proof_id is not None:
            if not isinstance(native_proof_id, str) or not native_proof_id.strip():
                raise ReconstructionRunError(f"Parity case {case_id} native proof ID is invalid")
            required_native_proofs.add(native_proof_id)
        report_kind = raw_case.get("requiredReportKind")
        probe_kind = str(raw_case["requiredProbeKind"]).lower()
        if any(marker in probe_kind for marker in ("browser", "cypress", "report")):
            if not isinstance(report_kind, str) or not report_kind.strip():
                raise ReconstructionRunError(
                    f"Parity case {case_id} requires explicit report provenance"
                )
        if report_kind is not None:
            if not isinstance(report_kind, str) or not report_kind.strip():
                raise ReconstructionRunError(f"Parity case {case_id} report kind is invalid")
            required_report_kinds.add(report_kind)
    if payload.get("requiredCaseCount") != len(cases_by_id):
        raise ReconstructionRunError("Parity case catalog requiredCaseCount is stale")
    return cases_by_id, required_native_proofs, required_report_kinds


def _validate_evaluator_manifest(
    archive: Path,
    run_id: str,
    execution_nonce: str,
    case_count: int,
    required_native_proofs: set[str],
    required_report_kinds: set[str],
) -> str:
    payload = _load_json_object(
        archive / "parity" / "evaluator-manifest.json",
        "parity/evaluator-manifest.json",
    )
    if payload.get("schemaVersion") != 2 or payload.get("runId") != run_id:
        raise ReconstructionRunError("Evaluator manifest schema or runId is invalid")
    if payload.get("executionNonce") != execution_nonce:
        raise ReconstructionRunError("Evaluator manifest is not bound to this execution")
    if payload.get("status") == "NOT_RUN":
        if (
            case_count != 0
            or payload.get("caseCount") != 0
            or payload.get("requiredNativeProofIds") != []
            or payload.get("requiredReportKinds") != []
        ):
            raise ReconstructionRunError("NOT_RUN evaluator manifest has stale requirements")
        _validate_not_run_record(archive, payload, "Evaluator manifest NOT_RUN")
        expected_digest = _binding_digest(run_id, execution_nonce, "evaluator-not-run")
        if payload.get("sealedDigest") != expected_digest:
            raise ReconstructionRunError("NOT_RUN evaluator digest is invalid")
        return expected_digest
    if payload.get("status") != "SEALED":
        raise ReconstructionRunError("Evaluator manifest is not sealed for this execution")
    if payload.get("caseCount") != case_count:
        raise ReconstructionRunError("Evaluator manifest caseCount is stale")
    manifest_native_ids = payload.get("requiredNativeProofIds")
    manifest_report_kinds = payload.get("requiredReportKinds")
    if not isinstance(manifest_native_ids, list) or set(manifest_native_ids) != required_native_proofs:
        raise ReconstructionRunError("Evaluator native proof inventory does not match parity cases")
    if not isinstance(manifest_report_kinds, list) or set(manifest_report_kinds) != required_report_kinds:
        raise ReconstructionRunError("Evaluator report inventory does not match parity cases")

    bindings = payload.get("bindings")
    if not isinstance(bindings, dict) or set(bindings) != {
        "caseCatalog",
        "contract",
        "evaluator",
        "oracle",
        "probeInventory",
    }:
        raise ReconstructionRunError("Evaluator manifest binding inventory is incomplete")
    binding_digests: dict[str, str] = {}
    for binding_name, raw_binding in bindings.items():
        if not isinstance(raw_binding, dict):
            raise ReconstructionRunError(f"Evaluator binding {binding_name} must be an object")
        _validate_evidence_reference(
            archive,
            raw_binding,
            "path",
            "sha256",
            f"Evaluator binding {binding_name}",
        )
        binding_digests[binding_name] = str(raw_binding["sha256"])
    if bindings["caseCatalog"].get("path") != "parity/cases.json":
        raise ReconstructionRunError("Evaluator caseCatalog binding must target parity/cases.json")
    if bindings["oracle"].get("path") != "oracle/original-baseline.json":
        raise ReconstructionRunError("Evaluator oracle binding must target original-baseline.json")
    sealed_digest = _binding_digest(
        *(f"{name}:{binding_digests[name]}" for name in sorted(binding_digests))
    )
    if payload.get("sealedDigest") != sealed_digest:
        raise ReconstructionRunError("Evaluator sealedDigest does not bind its component inventory")
    return sealed_digest


def _validate_record_time_window(
    payload: Mapping[str, object],
    label: str,
    run_started_at: datetime,
    run_finished_at: datetime,
) -> None:
    started_at = _parse_timestamp(_require_nonempty_string(payload, "startedAt", label))
    finished_at = _parse_timestamp(_require_nonempty_string(payload, "finishedAt", label))
    if started_at < run_started_at or finished_at > run_finished_at or finished_at < started_at:
        raise ReconstructionRunError(f"{label} timestamps fall outside the current run")


def _validate_not_run_record(
    archive: Path,
    payload: Mapping[str, object],
    label: str,
) -> None:
    _require_nonempty_string(payload, "unmetGate", label)
    _validate_evidence_reference(
        archive,
        payload,
        "failureEvidence",
        "failureEvidenceSha256",
        label,
    )


def _validate_execution_provenance(
    archive: Path,
    run_id: str,
    execution_nonce: str,
    run_status: str,
    run_started_at: datetime,
    run_finished_at: datetime,
    required_native_proofs: set[str],
    required_report_kinds: set[str],
    command_digests: Mapping[str, str],
) -> None:
    payload = _load_json_object(
        archive / "execution" / "provenance.json",
        "execution/provenance.json",
    )
    if payload.get("schemaVersion") != 2 or payload.get("runId") != run_id:
        raise ReconstructionRunError("Execution provenance schema or runId is invalid")
    if payload.get("executionNonce") != execution_nonce:
        raise ReconstructionRunError("Execution provenance nonce does not match RUN.json")
    if payload.get("status") == "NOT_RUN":
        if required_native_proofs or required_report_kinds:
            raise ReconstructionRunError("NOT_RUN provenance has sealed proof requirements")
        if payload.get("nativeProofs") != [] or payload.get("reportProofs") != []:
            raise ReconstructionRunError("NOT_RUN provenance must contain zero proof records")
        _validate_not_run_record(archive, payload, "Execution provenance NOT_RUN")
        return
    native_proofs = _require_sequence(payload, "nativeProofs", "Execution provenance")
    native_by_id: dict[str, Mapping[str, object]] = {}
    for raw_proof in native_proofs:
        if not isinstance(raw_proof, dict):
            raise ReconstructionRunError("Native proof must be an object")
        proof_id = _require_nonempty_string(raw_proof, "id", "Native proof")
        if proof_id in native_by_id:
            raise ReconstructionRunError(f"Duplicate native proof ID: {proof_id}")
        native_by_id[proof_id] = raw_proof
        if raw_proof.get("runId") != run_id or raw_proof.get("executionNonce") != execution_nonce:
            raise ReconstructionRunError(f"Native proof {proof_id} was not produced by this run")
        status = _require_nonempty_string(raw_proof, "status", f"Native proof {proof_id}")
        if status == "NOT_RUN":
            _validate_not_run_record(archive, raw_proof, f"Native proof {proof_id}")
            continue
        if status not in {"FAIL", "PASS"}:
            raise ReconstructionRunError(f"Native proof {proof_id} status is invalid")
        _validate_record_time_window(
            raw_proof,
            f"Native proof {proof_id}",
            run_started_at,
            run_finished_at,
        )
        for key in ("commandId", "targetIdentity", "processIdentity"):
            _require_nonempty_string(raw_proof, key, f"Native proof {proof_id}")
        for key in ("commandSha256", "targetDigest", "artifactDigest"):
            _require_sha256(raw_proof, key, f"Native proof {proof_id}")
        evidence_path = _validate_evidence_reference(
            archive,
            raw_proof,
            "evidence",
            "evidenceSha256",
            f"Native proof {proof_id}",
        )
        evidence_envelope = _load_json_object(
            evidence_path,
            f"Native proof {proof_id} evidence envelope",
        )
        if (
            evidence_envelope.get("runId") != run_id
            or evidence_envelope.get("executionNonce") != execution_nonce
            or evidence_envelope.get("commandSha256") != raw_proof.get("commandSha256")
            or evidence_envelope.get("targetDigest") != raw_proof.get("targetDigest")
            or evidence_envelope.get("artifactDigest") != raw_proof.get("artifactDigest")
            or evidence_envelope.get("processIdentity") != raw_proof.get("processIdentity")
        ):
            raise ReconstructionRunError(
                f"Native proof {proof_id} evidence envelope belongs to another run"
            )
        if command_digests.get(str(raw_proof["commandId"])) != raw_proof.get("commandSha256"):
            raise ReconstructionRunError(
                f"Native proof {proof_id} command is absent or differs from commands.jsonl"
            )
        expected_binding = _binding_digest(
            run_id,
            execution_nonce,
            "native",
            proof_id,
            str(raw_proof["evidenceSha256"]),
        )
        if raw_proof.get("proofBindingSha256") != expected_binding:
            raise ReconstructionRunError(f"Native proof {proof_id} binding is invalid")
    if set(native_by_id) != required_native_proofs:
        raise ReconstructionRunError(
            "Native proof set does not match the sealed evaluator; "
            f"missing={sorted(required_native_proofs - set(native_by_id))}, "
            f"unexpected={sorted(set(native_by_id) - required_native_proofs)}"
        )

    report_proofs = _require_sequence(payload, "reportProofs", "Execution provenance")
    report_by_kind: dict[str, Mapping[str, object]] = {}
    for raw_report in report_proofs:
        if not isinstance(raw_report, dict):
            raise ReconstructionRunError("Report proof must be an object")
        report_kind = _require_nonempty_string(raw_report, "kind", "Report proof")
        if report_kind in report_by_kind:
            raise ReconstructionRunError(f"Duplicate report proof kind: {report_kind}")
        report_by_kind[report_kind] = raw_report
        if raw_report.get("runId") != run_id or raw_report.get("executionNonce") != execution_nonce:
            raise ReconstructionRunError(f"Report proof {report_kind} was not produced by this run")
        status = _require_nonempty_string(raw_report, "status", f"Report proof {report_kind}")
        if status == "NOT_RUN":
            _validate_not_run_record(archive, raw_report, f"Report proof {report_kind}")
            continue
        if status not in {"FAIL", "PASS"}:
            raise ReconstructionRunError(f"Report proof {report_kind} status is invalid")
        _validate_record_time_window(
            raw_report,
            f"Report proof {report_kind}",
            run_started_at,
            run_finished_at,
        )
        for key in ("commandId", "targetIdentity", "processIdentity"):
            _require_nonempty_string(raw_report, key, f"Report proof {report_kind}")
        for key in ("commandSha256", "targetDigest", "artifactDigest"):
            _require_sha256(raw_report, key, f"Report proof {report_kind}")
        reporter = raw_report.get("reporter")
        if not isinstance(reporter, dict) or not reporter:
            raise ReconstructionRunError(f"Report proof {report_kind} reporter is missing")
        _require_nonempty_string(reporter, "name", f"Report proof {report_kind} reporter")
        _require_nonempty_string(reporter, "version", f"Report proof {report_kind} reporter")
        raw_report_path = _validate_evidence_reference(
            archive,
            raw_report,
            "rawReport",
            "rawReportSha256",
            f"Report proof {report_kind} raw report",
        )
        observation_path = _validate_evidence_reference(
            archive,
            raw_report,
            "observation",
            "observationSha256",
            f"Report proof {report_kind} observation",
        )
        observation_envelope = _load_json_object(
            observation_path,
            f"Report proof {report_kind} observation envelope",
        )
        if (
            observation_envelope.get("runId") != run_id
            or observation_envelope.get("executionNonce") != execution_nonce
            or observation_envelope.get("rawReportSha256") != _sha256(raw_report_path)
            or observation_envelope.get("commandSha256") != raw_report.get("commandSha256")
            or observation_envelope.get("targetDigest") != raw_report.get("targetDigest")
            or observation_envelope.get("artifactDigest") != raw_report.get("artifactDigest")
            or observation_envelope.get("processIdentity") != raw_report.get("processIdentity")
        ):
            raise ReconstructionRunError(
                f"Report proof {report_kind} observation is not bound to this raw report and run"
            )
        if command_digests.get(str(raw_report["commandId"])) != raw_report.get("commandSha256"):
            raise ReconstructionRunError(
                f"Report proof {report_kind} command is absent or differs from commands.jsonl"
            )
        expected_binding = _binding_digest(
            run_id,
            execution_nonce,
            "report",
            report_kind,
            str(raw_report["rawReportSha256"]),
            str(raw_report["observationSha256"]),
        )
        if raw_report.get("proofBindingSha256") != expected_binding:
            raise ReconstructionRunError(f"Report proof {report_kind} binding is invalid")
    if set(report_by_kind) != required_report_kinds:
        raise ReconstructionRunError(
            "Report proof set does not match the sealed evaluator; "
            f"missing={sorted(required_report_kinds - set(report_by_kind))}, "
            f"unexpected={sorted(set(report_by_kind) - required_report_kinds)}"
        )
    if run_status == "READY":
        if any(proof.get("status") != "PASS" for proof in native_by_id.values()):
            raise ReconstructionRunError("A READY run has an unpassed native proof")
        if any(proof.get("status") != "PASS" for proof in report_by_kind.values()):
            raise ReconstructionRunError("A READY run has an unpassed report proof")


def _validate_parity_reconciliation(
    archive: Path,
    run_id: str,
    run_status: str,
    evaluator_digest: str,
    cases_by_id: Mapping[str, Mapping[str, object]],
) -> None:
    payload = _load_json_object(
        archive / "parity" / "reconciliation.json",
        "parity/reconciliation.json",
    )
    if payload.get("schemaVersion") != 2 or payload.get("runId") != run_id:
        raise ReconstructionRunError("Parity reconciliation schema or runId is invalid")
    if payload.get("evaluatorDigest") != evaluator_digest:
        raise ReconstructionRunError("Parity reconciliation is bound to another evaluator")
    if payload.get("status") == "NOT_RUN":
        zero_counts = {"attempted": 0, "failed": 0, "notRun": 0, "passed": 0, "required": 0}
        if cases_by_id or payload.get("results") != [] or payload.get("counts") != zero_counts:
            raise ReconstructionRunError("NOT_RUN parity reconciliation has stale results")
        _validate_not_run_record(archive, payload, "Parity reconciliation NOT_RUN")
        return
    results = _require_nonempty_sequence(payload, "results", "Parity reconciliation")
    results_by_id: dict[str, Mapping[str, object]] = {}
    counts = {"attempted": 0, "failed": 0, "notRun": 0, "passed": 0, "required": len(cases_by_id)}
    for raw_result in results:
        if not isinstance(raw_result, dict):
            raise ReconstructionRunError("Parity result must be an object")
        case_id = _require_nonempty_string(raw_result, "caseId", "Parity result")
        if case_id in results_by_id:
            raise ReconstructionRunError(f"Duplicate parity result: {case_id}")
        results_by_id[case_id] = raw_result
        if case_id not in cases_by_id:
            raise ReconstructionRunError(f"Unknown parity result: {case_id}")
        status = _require_nonempty_string(raw_result, "status", f"Parity result {case_id}")
        if raw_result.get("probeKind") != cases_by_id[case_id].get("requiredProbeKind"):
            raise ReconstructionRunError(f"Parity result {case_id} used the wrong probe kind")
        if status == "NOT_RUN":
            counts["notRun"] += 1
            _validate_not_run_record(archive, raw_result, f"Parity result {case_id}")
        elif status in {"FAIL", "PASS"}:
            counts["attempted"] += 1
            counts["failed" if status == "FAIL" else "passed"] += 1
            _validate_evidence_reference(
                archive,
                raw_result,
                "evidence",
                "evidenceSha256",
                f"Parity result {case_id}",
            )
        else:
            raise ReconstructionRunError(f"Parity result {case_id} status is invalid")
    if set(results_by_id) != set(cases_by_id):
        raise ReconstructionRunError(
            "Parity result set is incomplete; "
            f"missing={sorted(set(cases_by_id) - set(results_by_id))}, "
            f"unexpected={sorted(set(results_by_id) - set(cases_by_id))}"
        )
    if payload.get("counts") != counts:
        raise ReconstructionRunError("Parity reconciliation counts are caller-supplied or stale")
    expected_status = "PASS" if counts["passed"] == counts["required"] else "FAIL"
    if payload.get("status") != expected_status:
        raise ReconstructionRunError("Parity reconciliation status does not match recomputed results")
    if run_status == "READY" and expected_status != "PASS":
        raise ReconstructionRunError("A READY run does not pass every required parity case")


def _validate_v2_machine_records(
    archive: Path,
    run_id: str,
    execution_nonce: str,
) -> dict[str, str]:
    json_paths = (
        "reset/source-baseline.json",
        "oracle/original-baseline.json",
        "generators/delta-ledger.json",
        "execution/results.json",
        "metrics/usage.json",
    )
    for relative_path in json_paths:
        payload = _load_json_object(archive / relative_path, relative_path)
        if payload.get("runId") != run_id:
            raise ReconstructionRunError(f"{relative_path} runId does not match the archive")
        status = _require_nonempty_string(payload, "status", relative_path)
        if status == "NOT_RUN":
            _validate_not_run_record(archive, payload, f"{relative_path} NOT_RUN")
    results = _load_json_object(archive / "execution" / "results.json", "execution/results.json")
    _require_nonempty_sequence(results, "activities", "execution/results.json")
    metrics = _load_json_object(archive / "metrics" / "usage.json", "metrics/usage.json")
    activities = _require_nonempty_sequence(metrics, "activities", "metrics/usage.json")
    for activity in activities:
        if not isinstance(activity, dict):
            raise ReconstructionRunError("metrics/usage.json activity must be an object")
        _require_nonempty_string(activity, "id", "Usage activity")
        if "elapsedSeconds" not in activity:
            raise ReconstructionRunError("Usage activity must record elapsedSeconds")
        if not any(key in activity for key in ("tokenCount", "tokenStatus")):
            raise ReconstructionRunError("Usage activity must record tokens or unavailability")
        if not any(key in activity for key in ("cost", "costStatus")):
            raise ReconstructionRunError("Usage activity must record cost or unavailability")

    command_path = archive / "execution" / "commands.jsonl"
    command_lines = [line for line in command_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not command_lines:
        raise ReconstructionRunError("execution/commands.jsonl must contain command records")
    seen_command_ids: set[str] = set()
    command_digests: dict[str, str] = {}
    for line_number, line in enumerate(command_lines, start=1):
        record = json.loads(line)
        if not isinstance(record, dict) or not record:
            raise ReconstructionRunError(
                f"execution/commands.jsonl line {line_number} must be a non-empty object"
            )
        if record.get("runId") != run_id or record.get("executionNonce") != execution_nonce:
            raise ReconstructionRunError(
                f"execution/commands.jsonl line {line_number} is not bound to this run"
            )
        command_id = _require_nonempty_string(record, "id", f"Command line {line_number}")
        command = _require_nonempty_string(record, "command", f"Command line {line_number}")
        if command_id in seen_command_ids:
            raise ReconstructionRunError(f"Duplicate command ID: {command_id}")
        seen_command_ids.add(command_id)
        command_digest = hashlib.sha256(command.encode("utf-8")).hexdigest()
        if record.get("commandSha256") != command_digest:
            raise ReconstructionRunError(
                f"Command {command_id} digest does not match its recorded command"
            )
        command_digests[command_id] = command_digest
    return command_digests


def _validate_v2_archive_semantics(archive: Path, run_id: str) -> None:
    run_data, run_started_at, run_finished_at = _validate_run_record(archive, run_id)
    execution_nonce = str(run_data["executionNonce"])
    run_status = str(run_data["status"])
    _validate_documentation_and_guidance(archive, run_id)
    _validate_git_reconciliation(archive, run_id)
    _validate_isolation_ledger(archive, run_id, run_status)
    cases_by_id, required_native_proofs, required_report_kinds = _validate_case_catalog(
        archive,
        run_id,
    )
    evaluator_digest = _validate_evaluator_manifest(
        archive,
        run_id,
        execution_nonce,
        len(cases_by_id),
        required_native_proofs,
        required_report_kinds,
    )
    command_digests = _validate_v2_machine_records(archive, run_id, execution_nonce)
    _validate_execution_provenance(
        archive,
        run_id,
        execution_nonce,
        run_status,
        run_started_at,
        run_finished_at,
        required_native_proofs,
        required_report_kinds,
        command_digests,
    )
    _validate_parity_reconciliation(
        archive,
        run_id,
        run_status,
        evaluator_digest,
        cases_by_id,
    )


def _assert_archive_candidate(archive: Path) -> tuple[str, int]:
    if not archive.is_dir():
        raise ReconstructionRunError(f"Archive candidate is not a directory: {archive}")
    run_data = _load_json_object(archive / "RUN.json", "RUN.json")
    schema_version = run_data.get("schemaVersion")
    if schema_version is None:
        schema_version = 1
    if schema_version not in {1, _ARCHIVE_SCHEMA_VERSION}:
        raise ReconstructionRunError(
            f"RUN.json schemaVersion must be 1 or {_ARCHIVE_SCHEMA_VERSION}"
        )
    required_files = list(_REQUIRED_ARCHIVE_FILES)
    required_directories = list(_REQUIRED_ARCHIVE_DIRECTORIES)
    if schema_version == _ARCHIVE_SCHEMA_VERSION:
        required_files.extend(_REQUIRED_V2_ARCHIVE_FILES)
        required_directories.extend(_REQUIRED_V2_DOCUMENTATION_DIRECTORIES)
    for relative_path in required_files:
        required_path = archive / relative_path
        if not required_path.is_file() or required_path.stat().st_size == 0:
            raise ReconstructionRunError(
                f"Missing or empty required archive entry: {relative_path}"
            )
    for relative_path in required_directories:
        required_directory = archive / relative_path
        if not required_directory.is_dir() or not any(
            path.is_file() for path in required_directory.rglob("*")
        ):
            raise ReconstructionRunError(
                f"Missing or empty required archive entry: {relative_path}"
            )

    run_id = run_data.get("runId")
    if run_id != archive.name:
        raise ReconstructionRunError(
            f"RUN.json runId must equal archive folder name: {archive.name}"
        )

    for path in _iter_tree_files(archive, archive):
        _assert_regular_independent_file(path, archive)
    if schema_version == _ARCHIVE_SCHEMA_VERSION:
        _validate_v2_archive_semantics(archive, str(run_id))
    return str(run_id), int(schema_version)


def _archive_attestation_path(archive: Path) -> Path:
    return archive.parent / f"{archive.name}{_ARCHIVE_ATTESTATION_SUFFIX}"


def _semantic_contract_digest() -> str:
    return _binding_digest(
        _ARCHIVE_SEMANTIC_CONTRACT,
        *_REQUIRED_ARCHIVE_FILES,
        *_REQUIRED_V2_ARCHIVE_FILES,
        *_REQUIRED_V2_DOCUMENTATION_DIRECTORIES,
        *sorted(_REQUIRED_ISOLATION_CHANNELS),
    )


def _validate_detached_attestation(
    archive: Path,
    manifest: Mapping[str, object],
    attestation_path: Path,
) -> dict[str, object]:
    if not attestation_path.is_file():
        raise ReconstructionRunError(
            f"Schema-v2 archive has no detached attestation: {attestation_path.name}"
        )
    attestation = _load_json_object(attestation_path, "Detached archive attestation")
    if attestation.get("schemaVersion") != _ARCHIVE_SCHEMA_VERSION:
        raise ReconstructionRunError("Detached archive attestation schema is invalid")
    if attestation.get("status") != "ATTESTED":
        raise ReconstructionRunError("Detached archive attestation status is invalid")
    if attestation.get("runId") != archive.name or attestation.get("archiveName") != archive.name:
        raise ReconstructionRunError("Detached archive attestation identifies another run")
    if attestation.get("manifestSha256") != _sha256(archive / _ARCHIVE_MANIFEST_NAME):
        raise ReconstructionRunError("Detached archive attestation does not match the manifest")
    if attestation.get("contentAggregateSha256") != manifest.get("contentAggregateSha256"):
        raise ReconstructionRunError("Detached archive attestation does not bind archive content")
    if attestation.get("semanticContractSha256") != _semantic_contract_digest():
        raise ReconstructionRunError("Detached archive attestation uses another semantic contract")
    _parse_timestamp(
        _require_nonempty_string(attestation, "attestedAt", "Detached archive attestation")
    )
    return attestation


def validate_archive(archive: Path) -> dict[str, object]:
    """Validate one sealed archive against its structural and semantic contract.

    archive identifies one sealed run folder. Historical schema-v1 runs must reproduce their
    exact manifest inventory and hashes. Schema-v2 runs must additionally pass documentation,
    guidance, Git, isolation, evaluator, provenance, parity, metrics, and detached-attestation
    validation. The function returns the validated manifest without modifying the archive.
    Missing, duplicate, hollow, stale, mutated, mismatched, or unreadable evidence raises
    ReconstructionRunError or preserves the owning JSON or filesystem error.
    """
    archive = archive.resolve(strict=True)
    manifest_path = archive / _ARCHIVE_MANIFEST_NAME
    if not manifest_path.is_file():
        raise ReconstructionRunError(
            f"Archive has no {_ARCHIVE_MANIFEST_NAME}: {archive.name}"
        )
    manifest = _load_json_object(manifest_path, _ARCHIVE_MANIFEST_NAME)
    schema_version = manifest.get("schemaVersion")
    if schema_version not in {1, _ARCHIVE_SCHEMA_VERSION}:
        raise ReconstructionRunError(f"Archive manifest schema is unsupported: {schema_version}")
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
    _, candidate_schema_version = _assert_archive_candidate(archive)
    if candidate_schema_version != schema_version:
        raise ReconstructionRunError("RUN.json and archive manifest schema versions differ")

    actual_files = {
        _relative_path(path, archive): path
        for path in _iter_tree_files(archive, archive)
        if path.name != _ARCHIVE_MANIFEST_NAME
    }
    manifest_entries = manifest.get("files")
    if not isinstance(manifest_entries, list):
        raise ReconstructionRunError(f"Archive file inventory is invalid: {archive.name}")
    expected_entries: dict[str, Mapping[str, object]] = {}
    recorded_paths: list[str] = []
    for raw_entry in manifest_entries:
        if not isinstance(raw_entry, dict):
            raise ReconstructionRunError(
                f"Archive file inventory entry is invalid: {archive.name}"
            )
        relative_value = _require_nonempty_string(raw_entry, "path", "Archive manifest entry")
        normalized_path = _assert_project_relative(relative_value).as_posix()
        if normalized_path != relative_value:
            raise ReconstructionRunError(
                f"Archive manifest path is not normalized: {relative_value}"
            )
        if normalized_path in expected_entries:
            raise ReconstructionRunError(
                f"Archive manifest contains a duplicate path: {normalized_path}"
            )
        if not isinstance(raw_entry.get("size"), int) or int(raw_entry["size"]) < 0:
            raise ReconstructionRunError(
                f"Archive manifest size is invalid: {normalized_path}"
            )
        _require_sha256(raw_entry, "sha256", f"Archive manifest entry {normalized_path}")
        expected_entries[normalized_path] = raw_entry
        recorded_paths.append(normalized_path)
    if recorded_paths != sorted(recorded_paths):
        raise ReconstructionRunError("Archive manifest entries must be sorted by path")
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
    if schema_version == _ARCHIVE_SCHEMA_VERSION:
        if manifest.get("semanticContract") != _ARCHIVE_SEMANTIC_CONTRACT:
            raise ReconstructionRunError("Archive manifest semantic contract is invalid")
        if manifest.get("semanticContractSha256") != _semantic_contract_digest():
            raise ReconstructionRunError("Archive manifest semantic contract digest is invalid")
        content_aggregate = _aggregate_digest(list(expected_entries.values()))
        if manifest.get("contentAggregateSha256") != content_aggregate:
            raise ReconstructionRunError("Archive manifest content aggregate is stale")
        expected_attestation_name = f"{archive.name}{_ARCHIVE_ATTESTATION_SUFFIX}"
        if manifest.get("detachedAttestation") != expected_attestation_name:
            raise ReconstructionRunError("Archive manifest detached attestation name is invalid")
        _validate_detached_attestation(
            archive,
            manifest,
            _archive_attestation_path(archive),
        )
    return manifest


def compare_archive_attestation(
    archive: Path,
    expected_attestation: Path,
) -> dict[str, object]:
    """Compare a sealed archive with an independently stored detached attestation.

    archive identifies the schema-v2 run folder to validate. expected_attestation identifies a
    detached copy obtained through a separate storage or transfer path. The function first
    performs full archive validation, then verifies the supplied attestation against the final
    manifest and requires it to match the archive-root sidecar byte for byte. It returns a MATCH
    result without modifying either input. Missing, stale, malformed, or mismatched evidence
    raises ReconstructionRunError or preserves the owning filesystem or JSON error.
    """
    archive = archive.expanduser().resolve(strict=True)
    expected_attestation = expected_attestation.expanduser().resolve(strict=True)
    manifest = validate_archive(archive)
    if manifest.get("schemaVersion") != _ARCHIVE_SCHEMA_VERSION:
        raise ReconstructionRunError("Detached attestation comparison requires schema version 2")
    _validate_detached_attestation(archive, manifest, expected_attestation)
    local_attestation = _archive_attestation_path(archive)
    if _sha256(expected_attestation) != _sha256(local_attestation):
        raise ReconstructionRunError("Detached attestation copies do not match")
    return {
        "attestation": expected_attestation.name,
        "runId": archive.name,
        "status": "MATCH",
    }


def _execution_evidence_digests(archive: Path) -> set[str]:
    provenance_path = archive / "execution" / "provenance.json"
    if not provenance_path.is_file():
        return set()
    payload = _load_json_object(provenance_path, "execution/provenance.json")
    digests: set[str] = set()
    for proof in payload.get("nativeProofs", []):
        if isinstance(proof, dict) and proof.get("status") in {"FAIL", "PASS"}:
            digest = proof.get("evidenceSha256")
            if isinstance(digest, str):
                digests.add(digest)
    for proof in payload.get("reportProofs", []):
        if isinstance(proof, dict) and proof.get("status") in {"FAIL", "PASS"}:
            digest = proof.get("observationSha256")
            if isinstance(digest, str):
                digests.add(digest)
    return digests


def _assert_unique_execution_evidence(archives: Sequence[Path]) -> None:
    owners_by_digest: dict[str, str] = {}
    for archive in archives:
        for digest in _execution_evidence_digests(archive):
            prior_owner = owners_by_digest.get(digest)
            if prior_owner is not None and prior_owner != archive.name:
                raise ReconstructionRunError(
                    "Schema-v2 archives reuse native or report evidence across runs: "
                    f"{prior_owner}, {archive.name}, {digest}"
                )
            owners_by_digest[digest] = archive.name


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
    independently validates an exact content manifest plus detached sidecar attestation, validates
    every sibling archive, rejects reused native or report proof bytes across schema-v2 runs, and
    only then deletes older validated runs. It returns the seal and retention result. Any invalid
    or unsealed run raises ReconstructionRunError before pruning and removes the new manifest and
    sidecar so the incomplete seal cannot be mistaken for accepted evidence.
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
    attestation_path = _archive_attestation_path(new_archive)
    if manifest_path.exists():
        raise ReconstructionRunError(f"Archive is already sealed: {new_archive.name}")
    if attestation_path.exists():
        raise ReconstructionRunError(
            f"Archive already has a detached attestation: {attestation_path.name}"
        )

    run_id, schema_version = _assert_archive_candidate(new_archive)
    if schema_version != _ARCHIVE_SCHEMA_VERSION:
        raise ReconstructionRunError(
            "New archives must use schemaVersion 2; schemaVersion 1 is validation-only"
        )
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
    content_aggregate = _aggregate_digest(file_entries)
    manifest = {
        "completedAt": completed_at,
        "contentAggregateSha256": content_aggregate,
        "detachedAttestation": attestation_path.name,
        "files": file_entries,
        "requiredDirectories": sorted(
            set(_REQUIRED_ARCHIVE_DIRECTORIES) | set(_REQUIRED_V2_DOCUMENTATION_DIRECTORIES)
        ),
        "requiredFiles": list(_REQUIRED_ARCHIVE_FILES) + list(_REQUIRED_V2_ARCHIVE_FILES),
        "runId": run_id,
        "schemaVersion": _ARCHIVE_SCHEMA_VERSION,
        "semanticContract": _ARCHIVE_SEMANTIC_CONTRACT,
        "semanticContractSha256": _semantic_contract_digest(),
        "status": "VALID",
    }
    _write_json(manifest_path, manifest)
    attestation = {
        "archiveName": new_archive.name,
        "attestedAt": _utc_now(),
        "contentAggregateSha256": content_aggregate,
        "manifestSha256": _sha256(manifest_path),
        "runId": run_id,
        "schemaVersion": _ARCHIVE_SCHEMA_VERSION,
        "semanticContractSha256": _semantic_contract_digest(),
        "status": "ATTESTED",
    }
    _write_json(attestation_path, attestation)

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
        _assert_unique_execution_evidence(
            [archive for _, _, archive in validated_archives]
        )
    except Exception:
        if manifest_path.exists():
            manifest_path.unlink()
        if attestation_path.exists():
            attestation_path.unlink()
        raise

    validated_archives.sort(key=lambda item: (item[0], item[1]))
    prune_candidates = validated_archives[:-retain]
    pruned_archives: list[str] = []
    for _, _, archive in prune_candidates:
        shutil.rmtree(archive)
        pruned_attestation = _archive_attestation_path(archive)
        if pruned_attestation.exists():
            pruned_attestation.unlink()
        pruned_archives.append(archive.name)

    return {
        "archiveManifest": _ARCHIVE_MANIFEST_NAME,
        "detachedAttestation": attestation_path.name,
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
    validate_archive_parser = subparsers.add_parser(
        "validate-archive",
        help="Validate archive structure, semantics, hashes, and detached attestation.",
    )
    validate_archive_parser.add_argument("--archive", required=True, type=Path)
    compare_archive_parser = subparsers.add_parser(
        "compare-archive",
        help="Compare a schema-v2 archive with an independently stored attestation.",
    )
    compare_archive_parser.add_argument("--archive", required=True, type=Path)
    compare_archive_parser.add_argument(
        "--expected-attestation",
        required=True,
        type=Path,
    )
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
    command emits the validated seed summary, validate-seed emits its read-only assessment,
    seal-archive emits the exact archive and retention result, validate-archive checks a sealed
    run, and compare-archive checks an independently stored attestation. Contract failures are
    written to standard error and return a nonzero status without pruning an unvalidated run;
    success writes JSON to standard output and returns zero.
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
        elif arguments.command == "validate-seed":
            result = validate_seed(
                build_root=arguments.build_root,
                exact=arguments.exact,
            )
        elif arguments.command == "validate-archive":
            result = validate_archive(arguments.archive)
        else:
            result = compare_archive_attestation(
                arguments.archive,
                arguments.expected_attestation,
            )
    except (OSError, ReconstructionRunError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
