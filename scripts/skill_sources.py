# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Classifies maintained skill source artifacts while excluding disposable cache entries.

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path


_DISPOSABLE_DIRECTORY_NAMES = frozenset({"__pycache__"})
_DISPOSABLE_FILE_NAMES = frozenset({".DS_Store"})
_PYTHON_BYTECODE_SUFFIX = ".pyc"


def is_disposable_source_entry(path: Path) -> bool:
    """Return whether one path is disposable cache or operating-system metadata."""

    return (
        path.name in _DISPOSABLE_DIRECTORY_NAMES
        or path.name in _DISPOSABLE_FILE_NAMES
        or path.suffix == _PYTHON_BYTECODE_SUFFIX
    )


def directory_has_maintained_source(directory: Path) -> bool:
    """Return whether a directory contains any non-disposable source artifact."""

    if directory.is_symlink():
        return True
    if not directory.is_dir() or is_disposable_source_entry(directory):
        return False
    return any(
        not is_disposable_source_entry(entry)
        and (
            entry.is_symlink()
            or entry.is_file()
            or directory_has_maintained_source(entry)
        )
        for entry in directory.iterdir()
    )


def is_cache_only_source_directory(directory: Path) -> bool:
    """Return whether a directory contains cache artifacts and no intended source."""

    if directory.is_symlink() or not directory.is_dir():
        return False
    found_cache = False
    for entry in directory.iterdir():
        if is_disposable_source_entry(entry):
            found_cache = True
            continue
        if entry.is_symlink() or entry.is_file():
            return False
        if not is_cache_only_source_directory(entry):
            return False
        found_cache = True
    return found_cache


def iter_maintained_source_files(root: Path) -> Iterator[Path]:
    """Yield non-disposable files below a root without traversing cache directories."""

    if is_disposable_source_entry(root):
        return
    if root.is_symlink() or root.is_file():
        yield root
        return
    if not root.is_dir():
        return
    for entry in sorted(root.iterdir()):
        yield from iter_maintained_source_files(entry)
