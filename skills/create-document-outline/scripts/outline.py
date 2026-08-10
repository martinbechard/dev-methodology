# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Validates source-traceable document outlines and renders synchronized HTML through mcp-agent-ops.

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import inspect
import json
import os
import re
import shlex
import shutil
import stat
import sys
import tempfile
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path


_RESULT_SCHEMA_VERSION = 1
_OUTLINE_SCHEMA = "dev-methodology-document-outline"
_OUTLINE_VERSION = 1
_REEXEC_MARKER = "MCP_AGENT_OPS_OUTLINE_REEXECUTED"
_SAFE_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,99}")
_SAFE_IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,99}")
_SECTION_KINDS = frozenset(
    {
        "source_fact",
        "proposed_organization",
        "unknown",
        "conflict",
        "final_document_decision",
    }
)
_KINDS_REQUIRING_SOURCES = frozenset(
    {"source_fact", "conflict", "final_document_decision"}
)


class _OutlineHelperError(Exception):
    def __init__(
        self, outcome: str, message: str, *, exit_code: int = 2, **details: object
    ) -> None:
        super().__init__(message)
        self.outcome = outcome
        self.message = message
        self.exit_code = exit_code
        self.details = details


class _JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise _OutlineHelperError("INVALID_REQUEST", message)


@dataclass(frozen=True)
class _OutlineApi:
    render_hierarchy_html: Callable[..., str | Path]
    package_version: str
    signature: str


@dataclass(frozen=True)
class _OutlineContext:
    workspace: Path
    output_root: Path
    outline_name: str
    json_path: Path
    html_path: Path


@dataclass(frozen=True)
class _ValidatedOutline:
    payload: dict[str, object]
    render_source: dict[str, object]
    title: str
    source_count: int
    section_count: int
    unresolved_question_count: int
    review_status: str


def _result(outcome: str, **details: object) -> dict[str, object]:
    return {"schema_version": _RESULT_SCHEMA_VERSION, "outcome": outcome, **details}


def _load_api() -> _OutlineApi:
    try:
        from mcp_agent_ops.hierarchy import render_hierarchy_html
    except (ImportError, ModuleNotFoundError) as error:
        raise _OutlineHelperError(
            "CAPABILITY_UNAVAILABLE",
            "The installed Python runtime cannot import mcp_agent_ops.hierarchy.",
            exit_code=3,
            cause=str(error),
        ) from error

    try:
        signature = inspect.signature(render_hierarchy_html)
        signature.bind(
            object(),
            title="Document outline",
            theme="outline",
            numbering=True,
            checkboxes=False,
            completed_items=(),
        )
        signature.bind(
            object(),
            title="Document outline",
            theme="outline",
            numbering=True,
            checkboxes=False,
            completed_items=(),
            output_filename="outline.html",
            output_folder=Path("."),
        )
    except (TypeError, ValueError) as error:
        raise _OutlineHelperError(
            "CAPABILITY_UNAVAILABLE",
            "The installed mcp-agent-ops renderer does not accept the helper call shapes.",
            exit_code=3,
            incompatibility=str(error),
        ) from error
    try:
        package_version = importlib.metadata.version("mcp-agent-ops")
    except importlib.metadata.PackageNotFoundError:
        package_version = "unknown"
    return _OutlineApi(
        render_hierarchy_html=render_hierarchy_html,
        package_version=package_version,
        signature=str(signature),
    )


def _reexec_interpreter() -> tuple[Path, list[str]] | None:
    command = shutil.which("mcp-agent-ops")
    if command is None:
        return None
    command_path = Path(command)
    if os.name == "nt":
        return _windows_interpreter(command_path)
    try:
        with command_path.open("r", encoding="utf-8") as executable:
            first_line = executable.readline().rstrip("\r\n")
    except (OSError, UnicodeError):
        return None
    if not first_line.startswith("#!"):
        return None
    words = shlex.split(first_line[2:].strip())
    if not words:
        return None
    interpreter = Path(words[0])
    interpreter_arguments = words[1:]
    if interpreter.name == "env":
        if not interpreter_arguments or interpreter_arguments[0].startswith("-"):
            return None
        resolved = shutil.which(interpreter_arguments[0])
        if resolved is None:
            return None
        interpreter = Path(resolved)
        interpreter_arguments = interpreter_arguments[1:]
    if not interpreter.is_absolute() or not interpreter.is_file():
        return None
    if "python" not in interpreter.name.lower():
        return None
    return interpreter, interpreter_arguments


def _windows_interpreter(command_path: Path) -> tuple[Path, list[str]] | None:
    interpreter = command_path.with_name("python.exe")
    if not interpreter.is_absolute() or not interpreter.is_file():
        return None
    return interpreter, []


def _maybe_reexec(argv: Sequence[str]) -> None:
    try:
        _load_api()
        return
    except _OutlineHelperError as error:
        if (
            error.outcome != "CAPABILITY_UNAVAILABLE"
            or os.environ.get(_REEXEC_MARKER) == "1"
        ):
            return
    resolved = _reexec_interpreter()
    if resolved is None:
        return
    interpreter, interpreter_arguments = resolved
    if interpreter == Path(sys.executable):
        return
    environment = dict(os.environ)
    environment[_REEXEC_MARKER] = "1"
    try:
        os.execve(
            interpreter,
            [
                str(interpreter),
                *interpreter_arguments,
                str(Path(__file__).resolve()),
                *argv,
            ],
            environment,
        )
    except OSError as error:
        raise _OutlineHelperError(
            "CAPABILITY_UNAVAILABLE",
            "The mcp-agent-ops executable interpreter could not start the outline helper.",
            exit_code=3,
            cause=str(error),
        ) from error


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve(strict=False).relative_to(root.resolve(strict=False))
        return True
    except ValueError:
        return False


def _lexists(path: Path) -> bool:
    return os.path.lexists(path)


def _reject_symlink_components(workspace: Path, target: Path) -> None:
    try:
        relative = target.relative_to(workspace)
    except ValueError as error:
        raise _OutlineHelperError(
            "PATH_OUTSIDE_WORKSPACE",
            "The requested path is outside the absolute workspace.",
            path=str(target),
            workspace=str(workspace),
        ) from error
    if ".." in relative.parts:
        raise _OutlineHelperError(
            "PATH_OUTSIDE_WORKSPACE",
            "The requested path contains workspace traversal.",
            path=str(target),
            workspace=str(workspace),
        )
    current = workspace
    if current.is_symlink():
        raise _OutlineHelperError(
            "SYMLINK_PATH_REJECTED",
            "The workspace must not be a symbolic link.",
            path=str(current),
        )
    for part in relative.parts:
        current = current / part
        if _lexists(current) and current.is_symlink():
            raise _OutlineHelperError(
                "SYMLINK_PATH_REJECTED",
                "Outline paths and their existing parents must not be symbolic links.",
                path=str(current),
            )
    if not _is_within(target, workspace):
        raise _OutlineHelperError(
            "PATH_OUTSIDE_WORKSPACE",
            "The requested path resolves outside the absolute workspace.",
            path=str(target),
            workspace=str(workspace),
        )


def _safe_workspace(value: str) -> Path:
    candidate = Path(value)
    if not candidate.is_absolute():
        raise _OutlineHelperError(
            "INVALID_WORKSPACE",
            "--workspace must be an absolute directory path.",
            workspace=value,
        )
    if not candidate.is_dir():
        raise _OutlineHelperError(
            "INVALID_WORKSPACE",
            "--workspace must identify an existing directory.",
            workspace=value,
        )
    if candidate.is_symlink() or candidate.resolve() != candidate:
        raise _OutlineHelperError(
            "INVALID_WORKSPACE",
            "--workspace must be a canonical absolute path without symbolic-link aliases.",
            workspace=value,
        )
    return candidate


def _context(arguments: argparse.Namespace) -> _OutlineContext:
    if (
        arguments.workspace is None
        or arguments.output_folder is None
        or arguments.name is None
    ):
        raise _OutlineHelperError(
            "INVALID_REQUEST",
            "Outline operations require --workspace, --output-folder, and --name.",
        )
    workspace = _safe_workspace(arguments.workspace)
    relative_folder = Path(arguments.output_folder)
    if relative_folder.is_absolute() or ".." in relative_folder.parts:
        raise _OutlineHelperError(
            "PATH_OUTSIDE_WORKSPACE",
            "--output-folder must be a project-relative path without traversal.",
            output_folder=arguments.output_folder,
            workspace=str(workspace),
        )
    if _SAFE_NAME.fullmatch(arguments.name) is None:
        raise _OutlineHelperError(
            "INVALID_NAME",
            "--name must be a safe base name without a suffix or directory.",
            name=arguments.name,
        )
    output_root = workspace / relative_folder
    _reject_symlink_components(workspace, output_root)
    json_path = output_root / f"{arguments.name}.json"
    html_path = output_root / f"{arguments.name}.html"
    _reject_symlink_components(workspace, json_path)
    _reject_symlink_components(workspace, html_path)
    context = _OutlineContext(
        workspace=workspace,
        output_root=output_root,
        outline_name=arguments.name,
        json_path=json_path,
        html_path=html_path,
    )
    _validate_html_target(context)
    return context


def _validate_html_target(context: _OutlineContext) -> None:
    try:
        target = os.lstat(context.html_path)
    except FileNotFoundError:
        return
    except OSError as error:
        raise _OutlineHelperError(
            "INVALID_OUTPUT_TARGET",
            "The HTML output target could not be inspected safely.",
            path=str(context.html_path),
            cause=str(error),
        ) from error
    if stat.S_ISLNK(target.st_mode):
        raise _OutlineHelperError(
            "SYMLINK_PATH_REJECTED",
            "The HTML output target must not be a symbolic link.",
            path=str(context.html_path),
        )
    if not stat.S_ISREG(target.st_mode):
        raise _OutlineHelperError(
            "INVALID_OUTPUT_TARGET",
            "The HTML output target must be a regular file when it exists.",
            path=str(context.html_path),
        )
    if target.st_nlink != 1:
        raise _OutlineHelperError(
            "HARD_LINK_PATH_REJECTED",
            "The HTML output target must not have hard-link aliases.",
            path=str(context.html_path),
            link_count=target.st_nlink,
        )


def _make_safe_directory(context: _OutlineContext) -> None:
    current = context.workspace
    for part in context.output_root.relative_to(context.workspace).parts:
        current = current / part
        if _lexists(current):
            if current.is_symlink():
                raise _OutlineHelperError(
                    "SYMLINK_PATH_REJECTED",
                    "Outline output folders must not contain symbolic links.",
                    path=str(current),
                )
            if not current.is_dir():
                raise _OutlineHelperError(
                    "INVALID_OUTPUT_PATH",
                    "An outline output-folder component is not a directory.",
                    path=str(current),
                )
            continue
        current.mkdir()
    _reject_symlink_components(context.workspace, context.output_root)


def _exact_keys(
    value: Mapping[str, object],
    required: set[str],
    path: str,
    optional: set[str] | None = None,
) -> None:
    allowed = required | (optional or set())
    missing = sorted(required - set(value))
    extra = sorted(set(value) - allowed)
    if missing or extra:
        details = []
        if missing:
            details.append(f"missing {', '.join(missing)}")
        if extra:
            details.append(f"unsupported {', '.join(extra)}")
        raise ValueError(f"{path} has {'; '.join(details)}.")


def _mapping(value: object, path: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ValueError(f"{path} must be a JSON object.")
    if any(not isinstance(key, str) for key in value):
        raise ValueError(f"{path} must use string field names.")
    return value


def _list(value: object, path: str) -> list[object]:
    if not isinstance(value, list):
        raise ValueError(f"{path} must be a JSON array.")
    return value


def _string(value: object, path: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{path} must be a nonempty string.")
    return value


def _string_list(value: object, path: str) -> list[str]:
    raw_items = _list(value, path)
    items = [_string(item, f"{path}[{index}]") for index, item in enumerate(raw_items)]
    if len(items) != len(set(items)):
        raise ValueError(f"{path} contains a duplicate value.")
    return items


def _source_references(
    value: object, path: str, source_ids: set[str]
) -> list[str]:
    references = _string_list(value, path)
    unknown = [reference for reference in references if reference not in source_ids]
    if unknown:
        raise ValueError(f"{path} contains unknown source reference {unknown[0]!r}.")
    return references


def _validate_section(
    raw_section: object,
    *,
    expected_level: int,
    source_ids: set[str],
    path: str,
) -> tuple[dict[str, object], int]:
    section = _mapping(raw_section, path)
    required = {"title", "level", "kind", "scope", "sourceRefs", "children"}
    _exact_keys(section, required, path, optional={"reviewText"})
    _string(section["title"], f"{path}.title")
    level = section["level"]
    if not isinstance(level, int) or isinstance(level, bool) or level != expected_level:
        raise ValueError(
            f"{path} has a skipped or incorrect level; expected {expected_level}."
        )
    kind = _string(section["kind"], f"{path}.kind")
    if kind not in _SECTION_KINDS:
        raise ValueError(f"{path}.kind is not a supported outline classification.")
    _string(section["scope"], f"{path}.scope")
    references = _source_references(
        section["sourceRefs"], f"{path}.sourceRefs", source_ids
    )
    if kind in _KINDS_REQUIRING_SOURCES and not references:
        raise ValueError(
            f"{path} is missing source coverage for material {kind.replace('_', ' ')} content."
        )
    children = _list(section["children"], f"{path}.children")
    if children:
        if "reviewText" in section:
            raise ValueError(f"{path} is a branch and must not contain reviewText.")
    else:
        if "reviewText" not in section:
            raise ValueError(f"{path} is an empty leaf without reviewText.")
        try:
            _string(section["reviewText"], f"{path}.reviewText")
        except ValueError as error:
            raise ValueError(f"{path} is an empty leaf without review text.") from error
    child_titles: set[str] = set()
    section_count = 1
    for index, raw_child in enumerate(children):
        child, child_count = _validate_section(
            raw_child,
            expected_level=expected_level + 1,
            source_ids=source_ids,
            path=f"{path}.children[{index}]",
        )
        child_title = _string(child["title"], f"{path}.children[{index}].title")
        if child_title in child_titles:
            raise ValueError(f"{path} contains duplicate sibling title {child_title!r}.")
        child_titles.add(child_title)
        section_count += child_count
    return section, section_count


def _render_section(section: Mapping[str, object]) -> dict[str, object]:
    rendered: dict[str, object] = {
        "Classification": str(section["kind"]).replace("_", " "),
        "Scope statement": section["scope"],
        "Source references": section["sourceRefs"],
    }
    children = section["children"]
    if not isinstance(children, list):
        raise ValueError("Validated section children changed type before rendering.")
    if children:
        rendered["Subsections"] = {
            str(child["title"]): _render_section(child)
            for child in children
            if isinstance(child, dict)
        }
    else:
        rendered["Review text"] = section["reviewText"]
    return rendered


def _load_json(path: Path) -> dict[str, object]:
    def reject_duplicate_fields(pairs: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"JSON contains duplicate field {key!r}.")
            result[key] = value
        return result

    try:
        parsed = json.loads(
            path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicate_fields
        )
    except json.JSONDecodeError as error:
        raise ValueError(f"Outline definition is not valid JSON: {error.msg}.") from error
    return _mapping(parsed, "outline")


def _validate_outline(payload: dict[str, object]) -> _ValidatedOutline:
    _exact_keys(
        payload,
        {
            "schema",
            "version",
            "title",
            "documentType",
            "inputReview",
            "sources",
            "root",
            "unresolvedQuestions",
            "review",
        },
        "outline",
    )
    if (
        payload["schema"] != _OUTLINE_SCHEMA
        or type(payload["version"]) is not int
        or payload["version"] != _OUTLINE_VERSION
    ):
        raise ValueError("outline has an unsupported schema or version.")
    title = _string(payload["title"], "outline.title")
    document_type = _string(payload["documentType"], "outline.documentType")

    input_review = _mapping(payload["inputReview"], "outline.inputReview")
    _exact_keys(
        input_review,
        {"authorized", "sensitiveDataExcluded"},
        "outline.inputReview",
    )
    if input_review["authorized"] is not True:
        raise ValueError("outline.inputReview.authorized must be true.")
    if input_review["sensitiveDataExcluded"] is not True:
        raise ValueError(
            "outline.inputReview.sensitiveDataExcluded must be true before rendering."
        )

    raw_sources = _list(payload["sources"], "outline.sources")
    if not raw_sources:
        raise ValueError("outline.sources must inventory at least one authorized source.")
    sources: list[dict[str, object]] = []
    source_ids: set[str] = set()
    for index, raw_source in enumerate(raw_sources):
        path = f"outline.sources[{index}]"
        source = _mapping(raw_source, path)
        _exact_keys(source, {"id", "label", "locator"}, path)
        source_id = _string(source["id"], f"{path}.id")
        if _SAFE_IDENTIFIER.fullmatch(source_id) is None:
            raise ValueError(f"{path}.id is not a safe source identifier.")
        if source_id in source_ids:
            raise ValueError(f"outline.sources contains duplicate source id {source_id!r}.")
        source_ids.add(source_id)
        _string(source["label"], f"{path}.label")
        _string(source["locator"], f"{path}.locator")
        sources.append(source)

    root, section_count = _validate_section(
        payload["root"], expected_level=1, source_ids=source_ids, path="outline.root"
    )
    if not root["children"]:
        raise ValueError("outline.root must contain at least one document section.")

    raw_questions = _list(
        payload["unresolvedQuestions"], "outline.unresolvedQuestions"
    )
    questions: list[dict[str, object]] = []
    question_ids: list[str] = []
    for index, raw_question in enumerate(raw_questions):
        path = f"outline.unresolvedQuestions[{index}]"
        question = _mapping(raw_question, path)
        _exact_keys(question, {"id", "question", "sourceRefs"}, path)
        question_id = _string(question["id"], f"{path}.id")
        if _SAFE_IDENTIFIER.fullmatch(question_id) is None:
            raise ValueError(f"{path}.id is not a safe question identifier.")
        if question_id in question_ids:
            raise ValueError(
                f"outline.unresolvedQuestions contains duplicate question id {question_id!r}."
            )
        _string(question["question"], f"{path}.question")
        references = _source_references(
            question["sourceRefs"], f"{path}.sourceRefs", source_ids
        )
        if not references:
            raise ValueError(f"{path} must retain at least one source reference.")
        question_ids.append(question_id)
        questions.append(question)

    review = _mapping(payload["review"], "outline.review")
    _exact_keys(
        review,
        {
            "status",
            "acceptedSectionOrder",
            "requiredCorrections",
            "remainingQuestionIds",
        },
        "outline.review",
    )
    review_status = _string(review["status"], "outline.review.status")
    if review_status not in {"draft", "accepted"}:
        raise ValueError("outline.review.status must be draft or accepted.")
    accepted_order = _string_list(
        review["acceptedSectionOrder"], "outline.review.acceptedSectionOrder"
    )
    corrections = _string_list(
        review["requiredCorrections"], "outline.review.requiredCorrections"
    )
    remaining_questions = _string_list(
        review["remainingQuestionIds"], "outline.review.remainingQuestionIds"
    )
    if remaining_questions != question_ids:
        raise ValueError(
            "outline.review.remainingQuestionIds must retain every unresolved question in source order."
        )
    section_order = [str(section["title"]) for section in root["children"]]
    if review_status == "accepted":
        if accepted_order != section_order:
            raise ValueError(
                "outline.review.acceptedSectionOrder must match the current top-level section order."
            )
        if corrections:
            raise ValueError(
                "outline.review.requiredCorrections must be empty when the outline is accepted."
            )
    elif accepted_order:
        raise ValueError(
            "outline.review.acceptedSectionOrder must be empty while the outline is draft."
        )

    render_sources = {
        str(source["id"]): {
            "Label": source["label"],
            "Locator": source["locator"],
        }
        for source in sources
    }
    render_questions = {
        str(question["id"]): {
            "Question": question["question"],
            "Source references": question["sourceRefs"],
        }
        for question in questions
    }
    render_source = {
        title: {
            "Document type": document_type,
            "Source inventory": render_sources,
            "Section outline": {str(root["title"]): _render_section(root)},
            "Unresolved questions": render_questions,
            "Review record": {
                "Status": review_status,
                "Accepted section order": accepted_order,
                "Required corrections": corrections,
                "Remaining question IDs": remaining_questions,
            },
        }
    }
    return _ValidatedOutline(
        payload=payload,
        render_source=render_source,
        title=title,
        source_count=len(sources),
        section_count=section_count,
        unresolved_question_count=len(questions),
        review_status=review_status,
    )


def _definition_path(value: str, context: _OutlineContext) -> Path:
    path = Path(value)
    if not path.is_absolute():
        raise _OutlineHelperError(
            "INVALID_DEFINITION_PATH",
            "--definition must be an absolute JSON path inside the workspace.",
            definition=value,
        )
    if not _is_within(path, context.workspace):
        raise _OutlineHelperError(
            "PATH_OUTSIDE_WORKSPACE",
            "The outline definition must be inside the absolute workspace.",
            definition=value,
            workspace=str(context.workspace),
        )
    _reject_symlink_components(context.workspace, path)
    if not path.is_file():
        raise _OutlineHelperError(
            "INVALID_DEFINITION_PATH",
            "--definition must identify an existing regular JSON file.",
            definition=value,
        )
    if path.suffix.lower() != ".json":
        raise _OutlineHelperError(
            "INVALID_DEFINITION_PATH",
            "--definition must use a .json extension.",
            definition=value,
        )
    if path.resolve() != context.json_path.resolve():
        raise _OutlineHelperError(
            "INVALID_DEFINITION_PATH",
            "--definition must identify the canonical JSON outline path.",
            definition=value,
            expected=str(context.json_path),
        )
    return path


def _render_html(outline: _ValidatedOutline, api: _OutlineApi) -> str:
    rendered = api.render_hierarchy_html(
        outline.render_source,
        title=f"{outline.title} outline",
        theme="outline",
        numbering=True,
        checkboxes=False,
        completed_items=(),
    )
    if not isinstance(rendered, str):
        raise _OutlineHelperError(
            "CAPABILITY_UNAVAILABLE",
            "The renderer did not return HTML text for an in-memory outline.",
            exit_code=3,
        )
    return rendered


def _render_validated_html(
    context: _OutlineContext,
    outline: _ValidatedOutline,
    api: _OutlineApi,
    expected_html: str,
) -> str:
    with tempfile.TemporaryDirectory(
        prefix=f".{context.outline_name}-render-", dir=context.output_root
    ) as temporary_directory:
        temporary_root = Path(temporary_directory)
        expected_path = temporary_root / context.html_path.name
        rendered_path = api.render_hierarchy_html(
            outline.render_source,
            title=f"{outline.title} outline",
            theme="outline",
            numbering=True,
            checkboxes=False,
            completed_items=(),
            output_filename=expected_path.name,
            output_folder=temporary_root,
        )
        try:
            observed_path = Path(rendered_path)
        except TypeError as error:
            raise _OutlineHelperError(
                "CAPABILITY_UNAVAILABLE",
                "The renderer did not return an HTML output path.",
                exit_code=3,
            ) from error
        if observed_path.resolve() != expected_path.resolve():
            raise _OutlineHelperError(
                "CAPABILITY_UNAVAILABLE",
                "The renderer returned an unexpected HTML output path.",
                exit_code=3,
                expected=str(expected_path),
                observed=str(rendered_path),
            )
        try:
            rendered_target = os.lstat(expected_path)
        except OSError as error:
            raise _OutlineHelperError(
                "CAPABILITY_UNAVAILABLE",
                "The renderer did not create a readable temporary HTML file.",
                exit_code=3,
                cause=str(error),
            ) from error
        if not stat.S_ISREG(rendered_target.st_mode) or rendered_target.st_nlink != 1:
            raise _OutlineHelperError(
                "CAPABILITY_UNAVAILABLE",
                "The renderer did not create one unaliased regular temporary HTML file.",
                exit_code=3,
            )
        actual_html = expected_path.read_text(encoding="utf-8")
        if actual_html != expected_html:
            raise _OutlineHelperError(
                "STALE_HTML",
                "The renderer output differs from the expected in-memory projection.",
                exit_code=4,
                json_path=str(context.json_path),
                html_path=str(context.html_path),
            )
        _validate_html_target(context)
        os.replace(expected_path, context.html_path)
        return actual_html


def _sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _summary(outline: _ValidatedOutline) -> dict[str, object]:
    return {
        "source_count": outline.source_count,
        "section_count": outline.section_count,
        "unresolved_question_count": outline.unresolved_question_count,
        "review_status": outline.review_status,
    }


def _build(
    context: _OutlineContext, arguments: argparse.Namespace, api: _OutlineApi
) -> dict[str, object]:
    definition_path = _definition_path(arguments.definition, context)
    try:
        outline = _validate_outline(_load_json(definition_path))
    except (OSError, UnicodeError, ValueError) as error:
        raise _OutlineHelperError("INVALID_OUTLINE", str(error)) from error
    expected_html = _render_html(outline, api)
    _make_safe_directory(context)
    actual_html = _render_validated_html(context, outline, api, expected_html)
    canonical_bytes = definition_path.read_bytes()
    return _result(
        "BUILT",
        json_path=str(context.json_path),
        html_path=str(context.html_path),
        json_sha256=_sha256(canonical_bytes),
        html_sha256=_sha256(actual_html.encode("utf-8")),
        synchronized=True,
        **_summary(outline),
    )


def _inspect(context: _OutlineContext, api: _OutlineApi) -> dict[str, object]:
    json_exists = context.json_path.is_file() and not context.json_path.is_symlink()
    html_exists = context.html_path.is_file() and not context.html_path.is_symlink()
    if not json_exists and not html_exists:
        return _result(
            "ABSENT",
            json_path=str(context.json_path),
            html_path=str(context.html_path),
            synchronized=False,
        )
    if not json_exists:
        return _result(
            "ORPHANED_HTML",
            json_path=str(context.json_path),
            html_path=str(context.html_path),
            synchronized=False,
        )
    try:
        outline = _validate_outline(_load_json(context.json_path))
    except (OSError, UnicodeError, ValueError) as error:
        raise _OutlineHelperError("INVALID_OUTLINE", str(error)) from error
    expected_html = _render_html(outline, api)
    canonical_bytes = context.json_path.read_bytes()
    actual_html = context.html_path.read_text(encoding="utf-8") if html_exists else None
    synchronized = actual_html == expected_html
    return _result(
        "SYNCED" if synchronized else "STALE_HTML",
        json_path=str(context.json_path),
        html_path=str(context.html_path),
        json_sha256=_sha256(canonical_bytes),
        html_sha256=(
            _sha256(actual_html.encode("utf-8")) if actual_html is not None else None
        ),
        expected_html_sha256=_sha256(expected_html.encode("utf-8")),
        synchronized=synchronized,
        **_summary(outline),
    )


def _parser() -> _JsonArgumentParser:
    parser = _JsonArgumentParser(
        description="Build and inspect one source-traceable document outline."
    )
    parser.add_argument("--workspace")
    parser.add_argument("--output-folder")
    parser.add_argument("--name")
    subparsers = parser.add_subparsers(
        dest="command", required=True, parser_class=_JsonArgumentParser
    )
    subparsers.add_parser("capabilities")
    build = subparsers.add_parser("build")
    build.add_argument("--definition", required=True)
    subparsers.add_parser("inspect")
    return parser


def execute(argv: Sequence[str] | None = None) -> tuple[int, dict[str, object]]:
    """Execute one outline command and return its process code and structured result.

    Args:
        argv: Command arguments without the executable name. Process arguments are used
            when this value is omitted.

    Returns:
        A process exit code and one JSON-serializable result. Codes zero, two, three,
        and four denote completion, invalid input, unavailable capability, and stale
        projection state respectively.

    Side effects:
        Build validates one canonical JSON file and atomically replaces its sibling HTML
        projection inside the selected workspace. Capabilities and inspect do not modify
        outline artifacts.
    """
    try:
        arguments = _parser().parse_args(list(sys.argv[1:] if argv is None else argv))
        api = _load_api()
        if arguments.command == "capabilities":
            return 0, _result(
                "CAPABILITIES_AVAILABLE",
                package="mcp-agent-ops",
                package_version=api.package_version,
                interpreter=str(Path(sys.executable).resolve()),
                capabilities=["render_hierarchy_html"],
                signatures={"render_hierarchy_html": api.signature},
            )
        context = _context(arguments)
        if arguments.command == "build":
            return 0, _build(context, arguments, api)
        if arguments.command == "inspect":
            inspected = _inspect(context, api)
            return (
                0 if inspected["outcome"] in {"SYNCED", "ABSENT"} else 4,
                inspected,
            )
        raise _OutlineHelperError("INVALID_REQUEST", "Unknown outline command.")
    except _OutlineHelperError as error:
        return error.exit_code, _result(
            error.outcome, error=error.message, **error.details
        )
    except Exception as error:
        return 4, _result(
            "INTERNAL_ERROR",
            error="The helper stopped at an unclassified boundary.",
            cause=str(error),
        )


def main(argv: Sequence[str] | None = None) -> int:
    """Run the portable outline helper and print exactly one structured JSON result.

    Args:
        argv: Optional command arguments without the executable name.

    Returns:
        The process exit code paired with the printed result.

    Side effects:
        The command can re-exec under the installed mcp-agent-ops interpreter, print one
        JSON result, and perform only the selected workspace-contained file effects.
    """
    arguments = list(sys.argv[1:] if argv is None else argv)
    try:
        _maybe_reexec(arguments)
        exit_code, result = execute(arguments)
    except _OutlineHelperError as error:
        exit_code = error.exit_code
        result = _result(error.outcome, error=error.message, **error.details)
    print(json.dumps(result, sort_keys=True))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
