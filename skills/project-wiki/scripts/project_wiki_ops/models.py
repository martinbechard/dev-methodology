"""Data models for project wiki operations."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class LintResult:
    path: Path
    message: str


@dataclass(frozen=True)
class OpenQuestion:
    path: Path
    line: int
    question: str


@dataclass(frozen=True)
class LeafPage:
    path: Path
    title: str


@dataclass(frozen=True)
class LeafLinkChange:
    leaf_path: Path
    target_path: Path
    title: str
