# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Validates module-template structure, readiness, source evidence, test claims, and fixture tests.

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shlex
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


_ROOT = Path(__file__).resolve().parent
_CONTRACT_PATH = _ROOT / "fixture-contract.json"
_FENCE_OPEN = re.compile(r"^ {0,3}(?P<marker>`{3,}|~{3,})(?P<info>.*)$")
_BLOCKQUOTE_PREFIX = re.compile(r"^ {0,3}>[ \t]?")
_PATH_REFERENCE = re.compile(
    r"(?<![A-Za-z0-9_./-])"
    r"(?P<path>/(?:[A-Za-z0-9_.-]+/)*(?:src|tests)/[A-Za-z0-9_./-]+\.py"
    r"|(?:\.\.?/|[A-Za-z0-9_.-]+/)*(?:src|tests)/[A-Za-z0-9_./-]+\.py)"
)
_INLINE_LINK = re.compile(
    r"(?P<image>!?)\[[^\]\n]*\]\(\s*(?:<(?P<angle>[^>\n]+)>|(?P<plain>[^\s)]+))"
    r"(?:\s+(?:\"[^\"\n]*\"|'[^'\n]*'))?\s*\)"
)
_REFERENCE_DEFINITION = re.compile(
    r"^ {0,3}\[(?P<label>[^\]\n]+)\]:\s*"
    r"(?:<(?P<angle>[^>\n]+)>|(?P<plain>\S+))"
    r"(?:\s+(?:\"[^\"\n]*\"|'[^'\n]*'|\([^()\n]*\)))?\s*$"
)
_REFERENCE_LINK = re.compile(
    r"(?P<image>!?)\[(?P<text>[^\]\n]+)\]\[(?P<label>[^\]\n]*)\]"
)
_SHORTCUT_REFERENCE_LINK = re.compile(r"(?<!!)\[(?P<label>[^\]\n]+)\](?![\[(])")
_URI = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:|^//")
_URI_TOKEN = re.compile(r"(?<![A-Za-z0-9+.-])(?:[A-Za-z][A-Za-z0-9+.-]*:|//)\S+")
_INLINE_CODE = re.compile(r"(?<!`)`([^`\n]+)`(?!`)")
_DIRECTIVE = re.compile(
    r"^(?:(?:[^,.;!?]{1,80},\s+)|after\s+editing(?::\s+|\s+))?"
    r"(?:(?:to verify|before handoff|please|then|next),?\s+)?"
    r"(?:run|execute|invoke|use|try|call)\s+(.+)$",
    re.IGNORECASE,
)
_ASSIGNMENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=.*$")
_RUNNERS = {
    "bash",
    "bun",
    "cargo",
    "go",
    "gradle",
    "git",
    "java",
    "make",
    "mvn",
    "node",
    "nox",
    "npm",
    "npx",
    "pip",
    "pip3",
    "pnpm",
    "poetry",
    "pytest",
    "python",
    "python3",
    "ruby",
    "ruff",
    "sh",
    "tox",
    "uv",
    "yarn",
    "zsh",
}
_SIMPLE_WRAPPERS = {"command", "exec", "nohup"}
_SHELL_OPERATORS = {"&&", "||", ";", "|"}
_POSITIVE_COVERAGE = re.compile(
    r"(?:automated|unit|regression)?[- ]?(?:tests?|checks?|suites?)\s+"
    r"(?:cover|covers|exercise|exercises|verify|verifies|assert|asserts|"
    r"validate|validates|check|checks|test|tests)"
    r"|(?:covered|tested|verified|validated|checked|exercised|asserted)\s+"
    r"(?:fully\s+|automatically\s+)?by\s+(?:an?\s+)?"
    r"(?:automated|unit|regression)?[- ]?(?:tests?|checks?|suites?)"
    r"|(?:is\s+|are\s+)?(?:fully\s+)?(?:covered|tested|verified|validated|checked|exercised)\s+"
    r"(?:automatically|by\s+(?:unit|automated|regression)\s+(?:tests?|checks?))"
    r"|(?:is|are)\s+(?:fully|completely)\s+"
    r"(?:covered|tested|verified|validated|checked|exercised)"
    r"|(?:has|have)\s+(?:complete|full|automated|unit[- ]?test|regression)\s+coverage"
    r"|(?:complete|full)\s+(?:automated|unit[- ]?test|regression)?\s*coverage"
    r"|(?:automated|unit|regression)?[- ]?coverage\s+"
    r"(?:covers|includes|exercises|verifies|validates|checks|tests)"
)
_NEGATIVE_COVERAGE = re.compile(
    r"(?:is\s+)?not\s+(?:covered|tested|verified|validated|checked|exercised|asserted)\s+"
    r"by\s+(?:an?\s+)?(?:automated|unit|regression)?[- ]?(?:tests?|checks?|suites?)"
    r"|no\s+(?:automated|unit|regression)?[- ]?tests?"
    r"|untested|lacks?\s+(?:automated\s+|unit[- ]?test\s+|test\s+)?coverage"
)
_SOURCE_ONLY_SUBJECT = re.compile(
    r"blank(?:[- ]value)?(?:\s+(?:branch|behavior|case|path|rejection))?"
    r"|empty(?:[- ]value)?|valueerror|rejection|invalid(?:[- ]value)?"
    r"|error\s+(?:branch|path)|both\s+branches"
)
_ANAPHORA = re.compile(
    r"\b(?:it|this)(?:\s+(?:branch|behavior|case|path|rejection))?\b"
    r"|\bthat\s+(?:branch|behavior|case|path|rejection)\b"
    r"|\bthe\s+same\s+(?:branch|behavior|case|path|rejection)\b"
)


@dataclass(frozen=True)
class _MarkdownDocument:
    """Represent top-level structure, visible prose, fences, and parse validity."""

    outside_lines: tuple[str, ...]
    visible_lines: tuple[str, ...]
    fences: tuple[tuple[str, tuple[str, ...], bool], ...]
    valid: bool


def _load_contract() -> dict[str, object]:
    """Load the synthetic fixture contract."""

    return json.loads(_CONTRACT_PATH.read_text(encoding="utf-8"))


def _strip_html_comments_from_line(line: str, active: bool) -> tuple[str, bool]:
    """Remove comments from one non-fenced line and return multiline state."""

    pieces: list[str] = []
    cursor = 0
    if active:
        closing = line.find("-->")
        if closing == -1:
            return "", True
        cursor = closing + 3
        active = False
    while cursor < len(line):
        opening = line.find("<!--", cursor)
        if opening == -1:
            pieces.append(line[cursor:])
            break
        pieces.append(line[cursor:opening])
        closing = line.find("-->", opening + 4)
        if closing == -1:
            active = True
            break
        cursor = closing + 3
    return "".join(pieces), active


def _visible_line(line: str) -> str:
    """Remove every nested blockquote marker from one visible prose line."""

    return _dequoted_line(line)[0]


def _dequoted_line(line: str) -> tuple[str, int]:
    """Return visible prose and the number of removed blockquote markers."""

    visible = line
    depth = 0
    while True:
        stripped = _BLOCKQUOTE_PREFIX.sub("", visible, count=1)
        if stripped == visible:
            return visible, depth
        visible = stripped
        depth += 1


def _markdown_document(text: str) -> _MarkdownDocument:
    """Parse the bounded Markdown structures required by this fixture."""

    outside: list[str] = []
    visible: list[str] = []
    fences: list[tuple[str, tuple[str, ...], bool]] = []
    active_character = ""
    active_length = 0
    active_info = ""
    active_lines: list[str] = []
    active_quoted = False
    active_quote_depth = 0
    active_comment = False
    active_comment_depth: int | None = None
    container_state_valid = True

    for raw_line in text.splitlines():
        dequoted, quote_depth = _dequoted_line(raw_line)
        quoted = quote_depth > 0
        if active_character:
            if quote_depth != active_quote_depth:
                container_state_valid = False
            closing = re.fullmatch(
                rf" {{0,3}}{re.escape(active_character)}{{{active_length},}}\s*",
                dequoted,
            )
            outside.append("")
            visible.append("")
            if closing and quote_depth == active_quote_depth:
                fences.append((active_info, tuple(active_lines), active_quoted))
                active_character = ""
                active_length = 0
                active_info = ""
                active_lines = []
                active_quoted = False
                active_quote_depth = 0
            else:
                active_lines.append(dequoted)
            continue

        if active_comment and quote_depth != active_comment_depth:
            active_comment = False
            active_comment_depth = None
            container_state_valid = False
        was_active_comment = active_comment
        line, active_comment = _strip_html_comments_from_line(dequoted, active_comment)
        if active_comment and not was_active_comment:
            active_comment_depth = quote_depth
        elif not active_comment:
            active_comment_depth = None
        opening = _FENCE_OPEN.fullmatch(line)
        if opening and not (
            opening.group("marker").startswith("`") and "`" in opening.group("info")
        ):
            marker = opening.group("marker")
            active_character = marker[0]
            active_length = len(marker)
            active_info = opening.group("info").strip().lower()
            active_lines = []
            active_quoted = quoted
            active_quote_depth = quote_depth
            outside.append("")
            visible.append("")
            continue

        outside.append("" if quoted else line)
        visible.append(line)

    fences_valid = not active_character
    if active_character:
        fences.append((active_info, tuple(active_lines), active_quoted))
    return _MarkdownDocument(
        outside_lines=tuple(outside),
        visible_lines=tuple(visible),
        fences=tuple(fences),
        valid=not active_comment and fences_valid and container_state_valid,
    )


def _ordered_headings(path: Path) -> list[str]:
    """Return ordered top-level level-two headings outside hidden contexts."""

    document = _markdown_document(path.read_text(encoding="utf-8"))
    return [line for line in document.outside_lines if line.startswith("## ")]


def _first_section_content(text: str, heading: str) -> str:
    """Return the first visible nonblank content under one top-level heading."""

    document = _markdown_document(text)
    inside = False
    for structural, visible in zip(document.outside_lines, document.visible_lines):
        if structural == heading:
            inside = True
            continue
        if inside and structural.startswith("## "):
            return ""
        if inside and visible.strip():
            return visible.strip()
    return ""


def _sha256(path: Path) -> str:
    """Return the SHA-256 digest of one authoritative fixture input."""

    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def _token_segments(candidate: str) -> list[list[str]]:
    """Split one shell-like command candidate into operator-delimited token segments."""

    try:
        lexer = shlex.shlex(candidate, posix=True, punctuation_chars=";&|")
        lexer.commenters = ""
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return []
    segments: list[list[str]] = [[]]
    for token in tokens:
        if token in _SHELL_OPERATORS:
            segments.append([])
        else:
            segments[-1].append(token)
    return [segment for segment in segments if segment]


def _unwrap_launcher(tokens: list[str]) -> str | None:
    """Return the executable launched by bounded environment and process wrappers."""

    remaining = list(tokens)
    if remaining and remaining[0] == "$":
        remaining.pop(0)
    while remaining and _ASSIGNMENT.fullmatch(remaining[0]):
        remaining.pop(0)
    while remaining:
        launcher = Path(remaining[0]).name
        if launcher in _SIMPLE_WRAPPERS:
            remaining.pop(0)
            if launcher == "command" and remaining and remaining[0] == "--":
                remaining.pop(0)
            continue
        if launcher == "env":
            remaining.pop(0)
            while remaining:
                option = remaining[0]
                if _ASSIGNMENT.fullmatch(option):
                    remaining.pop(0)
                    continue
                if not option.startswith("-"):
                    break
                remaining.pop(0)
                if (
                    option in {"-u", "--unset", "-C", "--chdir", "-S", "--split-string"}
                    and remaining
                ):
                    remaining.pop(0)
            continue
        if launcher == "sudo":
            remaining.pop(0)
            while remaining and remaining[0].startswith("-"):
                option = remaining.pop(0)
                if option in {"-u", "--user", "-g", "--group"} and remaining:
                    remaining.pop(0)
            continue
        if launcher == "timeout":
            remaining.pop(0)
            while remaining and remaining[0].startswith("-"):
                option = remaining.pop(0)
                if option in {"-s", "--signal", "-k", "--kill-after"} and remaining:
                    remaining.pop(0)
            if remaining:
                remaining.pop(0)
            continue
        break
    if not remaining:
        return None
    launcher = Path(remaining[0]).name
    if re.fullmatch(r"python3(?:\.\d+)?", launcher):
        return launcher
    return launcher if launcher in _RUNNERS else None


def _is_runnable_command(candidate: str) -> bool:
    """Recognize one command without treating arbitrary tool prose as executable."""

    return any(
        _unwrap_launcher(segment) is not None for segment in _token_segments(candidate)
    )


def _runnable_prose_commands(line: str) -> list[str]:
    """Return runnable commands exposed through inline code or command-shaped prose."""

    commands: list[str] = []
    for match in _INLINE_CODE.finditer(line):
        candidate = match.group(1).strip()
        if _is_runnable_command(candidate):
            commands.append(candidate)
    without_inline = _INLINE_CODE.sub("", line)
    candidate = re.sub(r"^\s*(?:[-*+]\s+|\d+[.)]\s+)?", "", without_inline).strip()
    directive = _DIRECTIVE.search(candidate)
    runnable = directive.group(1).strip() if directive else candidate
    emphasis = re.fullmatch(r"(?P<marker>\*\*|__)(?P<body>.+)(?P=marker)", runnable)
    if emphasis:
        runnable = emphasis.group("body").strip()
    if _is_runnable_command(runnable):
        commands.append(runnable)
    return list(dict.fromkeys(commands))


def _command_claims(text: str) -> tuple[list[str], bool]:
    """Inventory command lines and require exactly one command-only shell fence."""

    document = _markdown_document(text)
    commands: list[str] = []
    extraneous: list[str] = []
    shell_fence_count = 0
    for info, lines, quoted in document.fences:
        is_shell = not quoted and info in {"bash", "sh", "shell"}
        if is_shell:
            shell_fence_count += 1
        for line in lines:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if is_shell:
                commands.append(stripped)
            elif _is_runnable_command(stripped):
                extraneous.append(stripped)
    for line in document.visible_lines:
        extraneous.extend(_runnable_prose_commands(line))
    commands.extend(extraneous)
    return commands, document.valid and shell_fence_count == 1 and not extraneous


def _readiness_valid(text: str) -> bool:
    """Accept plain or canonically emphasized READY and BLOCKED readiness leads."""

    first = _first_section_content(text, "## Implementation Readiness")
    return (
        re.match(r"^(?:READY\.|BLOCKED\.|\*\*(?:READY\.|BLOCKED\.)\*\*)(?=\s|$)", first)
        is not None
    )


def _normalized_label(label: str) -> str:
    """Normalize a reference label according to Markdown's case and whitespace rules."""

    return " ".join(label.split()).casefold()


def _local_evidence_destination(destination: str) -> str | None:
    """Return one local source or test destination without query or fragment suffixes."""

    if _URI.match(destination):
        return None
    candidate = re.split(r"[?#]", destination, maxsplit=1)[0]
    match = _PATH_REFERENCE.fullmatch(candidate)
    return match.group("path") if match else None


def _reference_inventory(text: str) -> tuple[list[str], list[str]]:
    """Inventory local evidence paths from inline, reference-style, and bare Markdown."""

    document = _markdown_document(text)
    prose = "\n".join(document.visible_lines)
    definitions: dict[str, str] = {}
    external: set[str] = set()
    retained_lines: list[str] = []
    for line in prose.splitlines():
        definition = _REFERENCE_DEFINITION.fullmatch(line)
        if definition:
            destination = definition.group("angle") or definition.group("plain") or ""
            definitions.setdefault(
                _normalized_label(definition.group("label")), destination
            )
        else:
            retained_lines.append(line)
    prose = "\n".join(retained_lines)
    references: set[str] = set()

    def consume_inline(match: re.Match[str]) -> str:
        if match.group("image"):
            return ""
        destination = match.group("angle") or match.group("plain") or ""
        local = _local_evidence_destination(destination)
        if local:
            references.add(local)
        elif _URI.match(destination):
            external.add(destination)
        return ""

    prose = _INLINE_LINK.sub(consume_inline, prose)

    def consume_reference(match: re.Match[str]) -> str:
        if match.group("image"):
            return ""
        label = match.group("label") or match.group("text")
        destination = definitions.get(_normalized_label(label))
        if destination is not None:
            local = _local_evidence_destination(destination)
            if local:
                references.add(local)
            elif _URI.match(destination):
                external.add(destination)
        return ""

    prose = _REFERENCE_LINK.sub(consume_reference, prose)

    def consume_shortcut(match: re.Match[str]) -> str:
        destination = definitions.get(_normalized_label(match.group("label")))
        if destination is None:
            return match.group(0)
        local = _local_evidence_destination(destination)
        if local:
            references.add(local)
        elif _URI.match(destination):
            external.add(destination)
        return ""

    prose = _SHORTCUT_REFERENCE_LINK.sub(consume_shortcut, prose)
    prose = _URI_TOKEN.sub("", prose)
    references.update(match.group("path") for match in _PATH_REFERENCE.finditer(prose))
    return sorted(references), sorted(external)


def _references_valid(
    referenced_paths: list[str],
    required_paths: set[str],
    *,
    artifact: Path,
) -> bool:
    """Resolve evidence relative to the artifact and contain it to the fixture root."""

    root = _ROOT.resolve()
    resolved: set[Path] = set()
    for path in referenced_paths:
        if Path(path).is_absolute():
            return False
        candidate = (artifact.parent / path).resolve()
        if not candidate.is_relative_to(root) or not candidate.is_file():
            return False
        resolved.add(candidate)
    required = {(_ROOT / path).resolve() for path in required_paths}
    return required.issubset(resolved)


def _test_claims_valid(text: str, required_terms: list[str]) -> bool:
    """Reject visible positive coverage claims for the declared source-only branch."""

    document = _markdown_document(text)
    prose = "\n".join(document.visible_lines)
    lowered = prose.casefold()
    if not all(term.casefold() in lowered for term in required_terms):
        return False
    source_context = False
    statements = re.split(
        r"(?<=[.!?])\s+|\n+|\s+(?:but|however|nevertheless|yet)\s+", lowered
    )
    for statement in statements:
        normalized = re.sub(r"\s+", " ", statement).strip()
        if not normalized:
            continue
        explicit_source = _SOURCE_ONLY_SUBJECT.search(normalized) is not None
        anaphoric_source = source_context and _ANAPHORA.search(normalized) is not None
        without_negative = _NEGATIVE_COVERAGE.sub("", normalized)
        if (explicit_source or anaphoric_source) and _POSITIVE_COVERAGE.search(
            without_negative
        ):
            return False
        if explicit_source:
            source_context = True
        elif "success path" in normalized:
            source_context = False
    return True


def _run_source_tests() -> tuple[int, bool, str]:
    """Run the fixture's accepted source-test boundary without bytecode writes."""

    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests"],
        cwd=_ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=10,
        env=environment,
    )
    output = completed.stdout + completed.stderr
    count_match = re.search(r"Ran (\d+) tests?\b", output)
    count = int(count_match.group(1)) if count_match else 0
    return count, completed.returncode == 0, output


def _initial_evidence(contract: dict[str, object]) -> dict[str, object]:
    """Return source, test, artifact, and executable test evidence."""

    artifact = _ROOT / str(contract["artifactPath"])
    tests_run, tests_pass, test_output = _run_source_tests()
    return {
        "sourcePresent": (_ROOT / str(contract["sourcePath"])).is_file(),
        "testPresent": (_ROOT / str(contract["testPath"])).is_file(),
        "artifactPresent": artifact.is_file(),
        "testsRun": tests_run,
        "testsPass": tests_pass,
        "testOutput": test_output,
    }


def _final_evidence(
    contract: dict[str, object],
    *,
    artifact: Path,
    template: Path,
) -> dict[str, object]:
    """Return deterministic conformance and source-fidelity evidence."""

    root = _ROOT.resolve()
    expected_artifact = (_ROOT / str(contract["artifactPath"])).resolve()
    resolved_artifact = artifact.resolve()
    artifact_path_valid = (
        resolved_artifact == expected_artifact
        and resolved_artifact.is_relative_to(root)
    )
    text = (
        artifact.read_text(encoding="utf-8")
        if artifact_path_valid and artifact.is_file()
        else ""
    )
    document = _markdown_document(text)
    referenced_paths, external_references = _reference_inventory(text)
    required_paths = {str(contract["sourcePath"]), str(contract["testPath"])}
    source_only_terms = [str(term) for term in contract["sourceOnlyBranchTerms"]]
    command_claims, command_structure_valid = _command_claims(text)
    initial = _initial_evidence(contract)
    return {
        **initial,
        "artifactPresent": artifact.is_file(),
        "artifactPathValid": artifact_path_valid,
        "templateAuthorityValid": template.is_file()
        and _sha256(template) == str(contract["canonicalTemplateSha256"]),
        "headingsMatch": artifact_path_valid
        and artifact.is_file()
        and template.is_file()
        and _ordered_headings(artifact) == _ordered_headings(template),
        "readinessValid": _readiness_valid(text),
        "markdownStructureValid": document.valid,
        "todoFree": "TODO" not in text,
        "evidenceReferencesValid": _references_valid(
            referenced_paths,
            required_paths,
            artifact=artifact,
        ),
        "testCommandValid": command_structure_valid
        and command_claims == [str(contract["acceptedTestCommand"])],
        "testClaimsValid": _test_claims_valid(text, source_only_terms),
        "commandClaims": command_claims,
        "commandStructureValid": command_structure_valid,
        "referencedPaths": referenced_paths,
        "externalReferences": external_references,
    }


def main() -> int:
    """Validate the selected fixture phase and print machine-readable evidence."""

    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=("initial", "final"))
    parser.add_argument("--artifact", type=Path)
    parser.add_argument("--template", type=Path, required=True)
    arguments = parser.parse_args()
    contract = _load_contract()

    if arguments.phase == "initial":
        evidence = _initial_evidence(contract)
        expected_count = int(contract["expectedTestCount"])
        accepted = (
            evidence["sourcePresent"]
            and evidence["testPresent"]
            and not evidence["artifactPresent"]
            and evidence["testsPass"]
            and evidence["testsRun"] == expected_count
        )
        print(json.dumps(evidence, sort_keys=True))
        return 0 if accepted else 2

    artifact = arguments.artifact or _ROOT / str(contract["artifactPath"])
    evidence = _final_evidence(contract, artifact=artifact, template=arguments.template)
    accepted = all(
        evidence[key]
        for key in (
            "sourcePresent",
            "testPresent",
            "artifactPresent",
            "artifactPathValid",
            "testsPass",
            "templateAuthorityValid",
            "headingsMatch",
            "readinessValid",
            "markdownStructureValid",
            "todoFree",
            "evidenceReferencesValid",
            "testCommandValid",
            "testClaimsValid",
        )
    ) and evidence["testsRun"] == int(contract["expectedTestCount"])
    print(json.dumps(evidence, sort_keys=True))
    return 0 if accepted else 3


if __name__ == "__main__":
    raise SystemExit(main())
