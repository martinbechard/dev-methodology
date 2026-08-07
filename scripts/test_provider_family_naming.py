# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Responsibility: Validate provider-family labels, interface stereotypes, and provider stems in maintained design diagrams.
# Governing design: design/object-oriented-agent-and-skill-model.md

"""Focused provider-family naming checks for maintained object-oriented designs."""

from __future__ import annotations

import re
import tempfile
import unittest
from dataclasses import dataclass
from pathlib import Path


_REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
_DESIGN_PATHS = (
    Path("design/object-oriented-agent-and-skill-model.md"),
    Path("design/object-oriented-skill-group-models.md"),
    Path("design/agents/baseline-development.md"),
    Path("design/agents/project-setup.md"),
    Path("design/agents/documentation-methodology.md"),
    Path("design/agents/backlog-management.md"),
    Path("design/agents/work-item-dispatching-and-delivery.md"),
    Path("design/agents/main-branch-delivery.md"),
    Path("design/agents/review-and-verification.md"),
)
_CLASS_PATTERN = re.compile(
    r'class\s+(?P<identity>[A-Za-z0-9_-]+)'
    r'(?:\["(?P<label>[^"]+)"\])?\s*\{(?P<body>.*?)\}',
    re.DOTALL,
)
_MERMAID_BLOCK_PATTERN = re.compile(r"```mermaid\s*(?P<body>.*?)```", re.DOTALL)
_REALIZATION_PATTERN = re.compile(
    r"^\s*(?P<provider>[A-Za-z0-9_-]+)\s+\.\.\|>\s+"
    r"(?P<interface>[A-Za-z0-9_-]+)\s*$",
    re.MULTILINE,
)
_WILDCARD_TOKEN_PATTERN = re.compile(
    r"(?<![A-Za-z0-9-])(?P<token>[a-z0-9]+(?:-[a-z0-9*]+)+)(?![A-Za-z0-9-])"
)
_FAMILY_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*-\*$")
_SKILL_IDENTITY_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


@dataclass(frozen=True)
class _DiagramClass:
    """Represent the naming data needed from one Mermaid class declaration."""

    identity: str
    label: str
    stereotypes: frozenset[str]


def _diagram_classes(text: str) -> tuple[dict[str, _DiagramClass], list[str]]:
    """Return one Mermaid block's classes and repeated-identity defects."""

    classes: dict[str, _DiagramClass] = {}
    errors: list[str] = []
    for match in _CLASS_PATTERN.finditer(text):
        body = match.group("body")
        stereotypes = frozenset(re.findall(r"<<([^>]+)>>", body))
        identity = match.group("identity")
        if identity in classes:
            errors.append(f"repeated Mermaid class identity {identity!r}")
            continue
        classes[identity] = _DiagramClass(
            identity=identity,
            label=match.group("label") or identity,
            stereotypes=stereotypes,
        )
    return classes, errors


def _interface_package_exists(repository_root: Path, interface_identity: str) -> bool:
    """Return whether a package path and frontmatter publish the exact identity."""

    skill_path = repository_root / "skills" / interface_identity / "SKILL.md"
    if not skill_path.is_file():
        return False
    frontmatter_name = re.search(
        r"^name:\s*(?P<name>[^\s]+)\s*$",
        skill_path.read_text(encoding="utf-8"),
        re.MULTILINE,
    )
    return bool(
        frontmatter_name and frontmatter_name.group("name") == interface_identity
    )


def _validate_diagram(
    repository_root: Path,
    path: Path,
    text: str,
    block_number: int,
) -> list[str]:
    """Return provider-family naming defects from one Mermaid block."""

    classes, class_errors = _diagram_classes(text)
    errors = [f"{path}: Mermaid block {block_number}: {error}" for error in class_errors]
    interface_classes: dict[str, tuple[_DiagramClass, str]] = {}
    for diagram_class in classes.values():
        interface_stereotypes = diagram_class.stereotypes.intersection(
            {"Skill interface", "Interface Skill"}
        )
        if not interface_stereotypes:
            continue
        if "Interface Skill" in interface_stereotypes:
            interface_identity = diagram_class.label
            if "*" in interface_identity:
                errors.append(
                    f"{path}: concrete Interface Skill {interface_identity!r} must "
                    "use its exact identity without a wildcard"
                )
                continue
        elif "*" in diagram_class.label:
            if not _FAMILY_PATTERN.fullmatch(diagram_class.label):
                errors.append(
                    f"{path}: interface {diagram_class.label!r} must display its exact "
                    "identity followed by '-*'"
                )
                continue
            interface_identity = diagram_class.label.removesuffix("-*")
        else:
            continue
        if not _SKILL_IDENTITY_PATTERN.fullmatch(interface_identity):
            errors.append(
                f"{path}: interface identity {interface_identity!r} is not kebab-case"
            )
            continue

        if "Interface Skill" in interface_stereotypes and not _interface_package_exists(
            repository_root, interface_identity
        ):
            errors.append(
                f"{path}: {diagram_class.label!r} uses Interface Skill without "
                f"skills/{interface_identity}/SKILL.md"
            )
        interface_classes[diagram_class.identity] = (
            diagram_class,
            interface_identity,
        )

    for match in _REALIZATION_PATTERN.finditer(text):
        interface_entry = interface_classes.get(match.group("interface"))
        if interface_entry is None:
            continue
        interface_class, interface_identity = interface_entry
        provider = classes.get(match.group("provider"))
        if provider is None or "Provider Skill" not in provider.stereotypes:
            errors.append(
                f"{path}: realization of {interface_class.label!r} must start at a "
                "Provider Skill class"
            )
            continue
        expected_prefix = f"{interface_identity}-"
        if not _SKILL_IDENTITY_PATTERN.fullmatch(provider.label):
            errors.append(
                f"{path}: provider {provider.label!r} is not an exact kebab-case skill "
                "identity"
            )
        elif not provider.label.startswith(expected_prefix):
            errors.append(
                f"{path}: provider {provider.label!r} must begin with the complete "
                f"interface stem {expected_prefix!r}"
            )

    return errors


def _validate_document(
    repository_root: Path,
    path: Path,
    text: str,
) -> list[str]:
    """Return deterministic provider-family naming defects for one design document."""

    errors: list[str] = []
    for match in _WILDCARD_TOKEN_PATTERN.finditer(text):
        token = match.group("token")
        if "*" in token and not _FAMILY_PATTERN.fullmatch(token):
            errors.append(
                f"{path}: provider-family label {token!r} must contain one terminal '-*'"
            )

    for block_number, match in enumerate(
        _MERMAID_BLOCK_PATTERN.finditer(text), start=1
    ):
        errors.extend(
            _validate_diagram(
                repository_root,
                path,
                match.group("body"),
                block_number,
            )
        )
    return errors


class ProviderFamilyNamingTest(unittest.TestCase):
    """Verify the terminal-wildcard and complete-stem provider naming contract."""

    def test_maintained_designs_follow_provider_family_naming(self) -> None:
        """Validate every maintained object-oriented method and skill-group document."""

        errors: list[str] = []
        for path in _DESIGN_PATHS:
            errors.extend(
                _validate_document(
                    _REPOSITORY_ROOT,
                    path,
                    (_REPOSITORY_ROOT / path).read_text(encoding="utf-8"),
                )
            )
        self.assertEqual([], errors, "\n".join(errors))

    def test_nonterminal_wildcard_is_rejected(self) -> None:
        """Reject historical family labels that place the wildcard in the middle."""

        text = """```mermaid
class CreateWorkItem[\"create-*-work-item\"] {
    <<Skill interface>>
}
```"""
        errors = _validate_document(Path("/nonexistent"), Path("example.md"), text)
        self.assertTrue(any("terminal '-*'" in error for error in errors), errors)

    def test_provider_without_complete_interface_stem_is_rejected(self) -> None:
        """Reject a provider whose identity does not extend the complete interface stem."""

        text = """```mermaid
class CreateWorkItem[\"create-work-item-*\"] {
    <<Skill interface>>
}
class create-file-work-item {
    <<Provider Skill>>
}
create-file-work-item ..|> CreateWorkItem
```"""
        errors = _validate_document(Path("/nonexistent"), Path("example.md"), text)
        self.assertTrue(any("complete interface stem" in error for error in errors), errors)

    def test_concrete_interface_requires_loadable_exact_identity(self) -> None:
        """Reject the concrete stereotype when the exact interface package is absent."""

        text = """```mermaid
class CreateWorkItem[\"create-work-item\"] {
    <<Interface Skill>>
}
```"""
        with tempfile.TemporaryDirectory() as directory:
            errors = _validate_document(
                Path(directory), Path("example.md"), text
            )
        self.assertTrue(
            any(
                "without skills/create-work-item/SKILL.md" in error
                for error in errors
            ),
            errors,
        )

    def test_concrete_interface_provider_stem_is_validated(self) -> None:
        """Validate realizing providers for an exact loadable Interface Skill."""

        text = """```mermaid
class CreateWorkItem[\"create-work-item\"] {
    <<Interface Skill>>
}
class create-file-work-item {
    <<Provider Skill>>
}
create-file-work-item ..|> CreateWorkItem
```"""
        with tempfile.TemporaryDirectory() as directory:
            repository_root = Path(directory)
            skill_directory = repository_root / "skills" / "create-work-item"
            skill_directory.mkdir(parents=True)
            (skill_directory / "SKILL.md").write_text(
                "---\nname: create-work-item\n---\n",
                encoding="utf-8",
            )
            errors = _validate_document(
                repository_root, Path("example.md"), text
            )
        self.assertTrue(
            any("complete interface stem" in error for error in errors), errors
        )

    def test_repeated_identity_in_later_block_cannot_hide_invalid_provider(self) -> None:
        """Keep each Mermaid block's declarations local to its realization edges."""

        text = """```mermaid
class CreateWorkItem[\"create-work-item-*\"] {
    <<Skill interface>>
}
class create-file-work-item {
    <<Provider Skill>>
}
create-file-work-item ..|> CreateWorkItem
```

```mermaid
class CreateWorkItem[\"create-work-item-*\"] {
    <<Skill interface>>
}
class create-work-item-file {
    <<Provider Skill>>
}
create-work-item-file ..|> CreateWorkItem
```"""
        errors = _validate_document(Path("/nonexistent"), Path("example.md"), text)
        self.assertTrue(
            any("complete interface stem" in error for error in errors), errors
        )


if __name__ == "__main__":
    unittest.main()
