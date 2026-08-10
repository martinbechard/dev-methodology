# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Manages task-owned hierarchy plans through the installed mcp-agent-ops package APIs.

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
import sys
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path


RESULT_SCHEMA_VERSION = 1
DEFINITION_SCHEMA = "dev-methodology-complex-plan-input"
DEFINITION_VERSION = 1
PLAN_SCHEMA = "mcp-agent-ops-hierarchy-plan"
PLAN_VERSION = 1
PLAN_ROOT_PARTS = (".codex", "plans")
HISTORY_LIMIT = 20
REEXEC_MARKER = "MCP_AGENT_OPS_PLAN_REEXECUTED"
SAFE_TASK_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,199}")
SAFE_PLAN_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,99}")
DOTTED_PATH = re.compile(r"[1-9][0-9]*(?:\.[1-9][0-9]*)*")
HISTORY_DIRECTORY = re.compile(r"(?P<sequence>[0-9]{6})-(?:update|reconcile)")
METADATA_PREFIXES = ("Dependency reference: ", "Evidence reference: ")


class _PlanHelperError(Exception):
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
        raise _PlanHelperError("INVALID_REQUEST", message)


@dataclass(frozen=True)
class _PlanApi:
    create_hierarchy_plan: Callable[..., Path]
    render_hierarchy_html: Callable[..., str | Path]
    update_hierarchy_plan: Callable[..., Path]
    package_version: str


@dataclass(frozen=True)
class _PlanContext:
    workspace: Path
    task_root: Path
    plan_name: str
    plan_path: Path
    html_path: Path
    history_root: Path


@dataclass(frozen=True)
class _PlanItem:
    text: str
    complete: bool
    children: tuple[_PlanItem, ...]


@dataclass(frozen=True)
class _PlanDocument:
    title: str
    theme: str
    themes_folder: str | None
    html_filename: str
    root_label: str
    items: tuple[_PlanItem, ...]


def _result(outcome: str, **details: object) -> dict[str, object]:
    return {"schema_version": RESULT_SCHEMA_VERSION, "outcome": outcome, **details}


def _load_api() -> _PlanApi:
    try:
        from mcp_agent_ops.hierarchy import (
            create_hierarchy_plan,
            render_hierarchy_html,
            update_hierarchy_plan,
        )
    except (ImportError, ModuleNotFoundError) as error:
        raise _PlanHelperError(
            "CAPABILITY_UNAVAILABLE",
            "The installed Python runtime cannot import mcp_agent_ops.hierarchy.",
            exit_code=3,
            cause=str(error),
        ) from error

    functions = {
        "create_hierarchy_plan": create_hierarchy_plan,
        "render_hierarchy_html": render_hierarchy_html,
        "update_hierarchy_plan": update_hierarchy_plan,
    }
    required_parameters = {
        "create_hierarchy_plan": {"source", "output_filename", "output_folder"},
        "render_hierarchy_html": {
            "source",
            "title",
            "theme",
            "numbering",
            "checkboxes",
            "completed_items",
            "output_filename",
            "output_folder",
        },
        "update_hierarchy_plan": {
            "plan_path",
            "target",
            "completed",
            "add_child",
            "add_peer_after",
        },
    }
    missing: dict[str, list[str]] = {}
    for name, function in functions.items():
        if not callable(function):
            missing[name] = ["callable"]
            continue
        observed = set(inspect.signature(function).parameters)
        absent = sorted(required_parameters[name] - observed)
        if absent:
            missing[name] = absent
    if missing:
        raise _PlanHelperError(
            "CAPABILITY_UNAVAILABLE",
            "The installed mcp-agent-ops package does not expose the required hierarchy API signatures.",
            exit_code=3,
            missing=missing,
        )
    try:
        package_version = importlib.metadata.version("mcp-agent-ops")
    except importlib.metadata.PackageNotFoundError:
        package_version = "unknown"
    return _PlanApi(
        create_hierarchy_plan=create_hierarchy_plan,
        render_hierarchy_html=render_hierarchy_html,
        update_hierarchy_plan=update_hierarchy_plan,
        package_version=package_version,
    )


def _capability_result(api: _PlanApi) -> dict[str, object]:
    return _result(
        "CAPABILITIES_AVAILABLE",
        package="mcp-agent-ops",
        package_version=api.package_version,
        interpreter=str(Path(sys.executable).resolve()),
        capabilities=[
            "create_hierarchy_plan",
            "render_hierarchy_html",
            "update_hierarchy_plan",
        ],
        signatures={
            "create_hierarchy_plan": str(inspect.signature(api.create_hierarchy_plan)),
            "render_hierarchy_html": str(inspect.signature(api.render_hierarchy_html)),
            "update_hierarchy_plan": str(inspect.signature(api.update_hierarchy_plan)),
        },
    )


def _reexec_interpreter() -> tuple[Path, list[str]] | None:
    command = shutil.which("mcp-agent-ops")
    if command is None:
        return None
    command_path = Path(command)
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


def _maybe_reexec(argv: Sequence[str]) -> None:
    try:
        _load_api()
        return
    except _PlanHelperError as error:
        if (
            error.outcome != "CAPABILITY_UNAVAILABLE"
            or os.environ.get(REEXEC_MARKER) == "1"
        ):
            return
    resolved = _reexec_interpreter()
    if resolved is None:
        return
    interpreter, interpreter_arguments = resolved
    if interpreter == Path(sys.executable):
        return
    environment = dict(os.environ)
    environment[REEXEC_MARKER] = "1"
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
        raise _PlanHelperError(
            "CAPABILITY_UNAVAILABLE",
            "The mcp-agent-ops executable interpreter could not start the plan helper.",
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
        raise _PlanHelperError(
            "PATH_OUTSIDE_WORKSPACE",
            "The requested path is outside the absolute workspace.",
            path=str(target),
            workspace=str(workspace),
        ) from error
    if ".." in relative.parts:
        raise _PlanHelperError(
            "PATH_OUTSIDE_WORKSPACE",
            "The requested path contains workspace traversal.",
            path=str(target),
            workspace=str(workspace),
        )
    current = workspace
    if current.is_symlink():
        raise _PlanHelperError(
            "SYMLINK_PATH_REJECTED",
            "The workspace must not be a symbolic link.",
            path=str(current),
        )
    for part in relative.parts:
        current = current / part
        if _lexists(current) and current.is_symlink():
            raise _PlanHelperError(
                "SYMLINK_PATH_REJECTED",
                "Plan paths and their existing parents must not be symbolic links.",
                path=str(current),
            )
    if not _is_within(target, workspace):
        raise _PlanHelperError(
            "PATH_OUTSIDE_WORKSPACE",
            "The requested path resolves outside the absolute workspace.",
            path=str(target),
            workspace=str(workspace),
        )


def _safe_workspace(value: str) -> Path:
    candidate = Path(value)
    if not candidate.is_absolute():
        raise _PlanHelperError(
            "INVALID_WORKSPACE",
            "--workspace must be an absolute directory path.",
            workspace=value,
        )
    if not candidate.is_dir():
        raise _PlanHelperError(
            "INVALID_WORKSPACE",
            "--workspace must identify an existing directory.",
            workspace=value,
        )
    if candidate.is_symlink() or candidate.resolve() != candidate:
        raise _PlanHelperError(
            "INVALID_WORKSPACE",
            "--workspace must be a canonical absolute path without symbolic-link aliases.",
            workspace=value,
        )
    return candidate


def _safe_name(value: str, pattern: re.Pattern[str], field: str) -> str:
    if pattern.fullmatch(value) is None or value in {".", ".."}:
        raise _PlanHelperError(
            "INVALID_NAME",
            f"{field} contains an unsafe task or plan name.",
            field=field,
            value=value,
        )
    return value


def _context(arguments: argparse.Namespace) -> _PlanContext:
    if (
        arguments.workspace is None
        or arguments.root_task_id is None
        or arguments.plan_name is None
    ):
        raise _PlanHelperError(
            "INVALID_REQUEST",
            "Plan operations require --workspace, --root-task-id, and --plan-name.",
        )
    workspace = _safe_workspace(arguments.workspace)
    root_task_id = _safe_name(arguments.root_task_id, SAFE_TASK_NAME, "root-task-id")
    plan_name = _safe_name(arguments.plan_name, SAFE_PLAN_NAME, "plan-name")
    task_root = workspace.joinpath(*PLAN_ROOT_PARTS, root_task_id)
    _reject_symlink_components(workspace, task_root)
    plan_path = task_root / f"{plan_name}.json"
    html_path = task_root / f"{plan_name}.html"
    history_root = task_root / ".history" / plan_name
    return _PlanContext(
        workspace=workspace,
        task_root=task_root,
        plan_name=plan_name,
        plan_path=plan_path,
        html_path=html_path,
        history_root=history_root,
    )


def _make_safe_directory(workspace: Path, directory: Path) -> None:
    _reject_symlink_components(workspace, directory)
    current = workspace
    for part in directory.relative_to(workspace).parts:
        current = current / part
        if _lexists(current):
            if current.is_symlink():
                raise _PlanHelperError(
                    "SYMLINK_PATH_REJECTED",
                    "Plan directory parents must not be symbolic links.",
                    path=str(current),
                )
            if not current.is_dir():
                raise _PlanHelperError(
                    "INVALID_PATH",
                    "A plan directory parent is not a directory.",
                    path=str(current),
                )
        else:
            current.mkdir()


def _safe_file(path: Path, context: _PlanContext, *, required: bool) -> None:
    _reject_symlink_components(context.workspace, path)
    if required and not path.is_file():
        raise _PlanHelperError(
            "PLAN_NOT_FOUND",
            "The requested plan artifact does not exist.",
            path=str(path),
        )
    if _lexists(path) and (path.is_symlink() or not path.is_file()):
        raise _PlanHelperError(
            "SYMLINK_PATH_REJECTED" if path.is_symlink() else "INVALID_PATH",
            "Plan artifacts must be regular non-symbolic-link files.",
            path=str(path),
        )


def _read_json(path: Path, outcome: str, description: str) -> dict[str, object]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise _PlanHelperError(
            outcome, description, cause=str(error), path=str(path)
        ) from error
    if not isinstance(payload, dict):
        raise _PlanHelperError(outcome, description, path=str(path))
    return payload


def _single_line(value: object, field: str, *, maximum: int = 500) -> str:
    if not isinstance(value, str) or not value.strip() or value != value.strip():
        raise _PlanHelperError(
            "INVALID_DEFINITION",
            f"Definition field {field} must be a non-empty trimmed string.",
            field=field,
        )
    if len(value) > maximum or any(
        character in value for character in ("\r", "\n", "\x00")
    ):
        raise _PlanHelperError(
            "INVALID_DEFINITION",
            f"Definition field {field} must be one line of at most {maximum} characters.",
            field=field,
        )
    return value


def _string_list(value: object, field: str) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise _PlanHelperError(
            "INVALID_DEFINITION",
            f"Definition field {field} must be a JSON array.",
            field=field,
        )
    return tuple(_single_line(item, field) for item in value)


def _definition_item(
    value: object,
    field: str,
    *,
    depth: int,
    counter: list[int],
) -> dict[str, object]:
    if depth > 20:
        raise _PlanHelperError(
            "INVALID_DEFINITION", "Definition task nesting exceeds 20 levels."
        )
    if not isinstance(value, dict):
        raise _PlanHelperError(
            "INVALID_DEFINITION", f"Definition field {field} must be an object."
        )
    allowed = {"title", "dependsOn", "evidence", "complete", "children"}
    unknown = sorted(set(value) - allowed)
    if unknown:
        raise _PlanHelperError(
            "INVALID_DEFINITION",
            f"Definition field {field} contains unsupported properties.",
            unsupported=unknown,
        )
    required = allowed - set(value)
    if required:
        raise _PlanHelperError(
            "INVALID_DEFINITION",
            f"Definition field {field} is missing required properties.",
            missing=sorted(required),
        )
    complete = value["complete"]
    if not isinstance(complete, bool):
        raise _PlanHelperError(
            "INVALID_DEFINITION",
            f"Definition field {field}.complete must be true or false.",
        )
    raw_children = value["children"]
    if not isinstance(raw_children, list):
        raise _PlanHelperError(
            "INVALID_DEFINITION",
            f"Definition field {field}.children must be a JSON array.",
        )
    counter[0] += 1
    if counter[0] > 1000:
        raise _PlanHelperError(
            "INVALID_DEFINITION", "Definition contains more than 1000 tasks."
        )
    return {
        "title": _single_line(value["title"], f"{field}.title"),
        "dependsOn": _string_list(value["dependsOn"], f"{field}.dependsOn"),
        "evidence": _string_list(value["evidence"], f"{field}.evidence"),
        "complete": complete,
        "children": [
            _definition_item(
                child, f"{field}.children[{index}]", depth=depth + 1, counter=counter
            )
            for index, child in enumerate(raw_children)
        ],
    }


def _load_definition(path_value: str, context: _PlanContext) -> dict[str, object]:
    path = Path(path_value)
    if not path.is_absolute():
        raise _PlanHelperError(
            "INVALID_PATH",
            "--definition must be an absolute path inside the workspace.",
            path=path_value,
        )
    if not _is_within(path, context.workspace):
        raise _PlanHelperError(
            "PATH_OUTSIDE_WORKSPACE",
            "The plan definition must be inside the absolute workspace.",
            path=str(path),
            workspace=str(context.workspace),
        )
    _reject_symlink_components(context.workspace, path)
    if not path.is_file() or path.is_symlink():
        raise _PlanHelperError(
            "INVALID_PATH",
            "The plan definition must be a regular non-symbolic-link file.",
            path=str(path),
        )
    payload = _read_json(
        path, "INVALID_DEFINITION", "The plan definition is not valid JSON."
    )
    if (
        payload.get("schema") != DEFINITION_SCHEMA
        or payload.get("version") != DEFINITION_VERSION
    ):
        raise _PlanHelperError(
            "INVALID_DEFINITION",
            "The plan definition has an unsupported schema or version.",
            expected_schema=DEFINITION_SCHEMA,
            expected_version=DEFINITION_VERSION,
        )
    allowed = {"schema", "version", "title", "objective", "tasks"}
    unknown = sorted(set(payload) - allowed)
    if unknown:
        raise _PlanHelperError(
            "INVALID_DEFINITION",
            "The plan definition contains unsupported top-level properties.",
            unsupported=unknown,
        )
    raw_tasks = payload.get("tasks")
    if not isinstance(raw_tasks, list) or not raw_tasks:
        raise _PlanHelperError(
            "INVALID_DEFINITION", "The plan definition requires at least one task."
        )
    counter = [0]
    return {
        "path": path,
        "title": _single_line(payload.get("title"), "title", maximum=200),
        "objective": _single_line(payload.get("objective"), "objective", maximum=1000),
        "tasks": [
            _definition_item(item, f"tasks[{index}]", depth=1, counter=counter)
            for index, item in enumerate(raw_tasks)
        ],
    }


def _definition_hierarchy(
    definition: dict[str, object],
) -> tuple[dict[str, object], tuple[str, ...]]:
    completed_paths: list[str] = []

    def render_item(item: dict[str, object], path: tuple[int, ...]) -> object:
        if item["complete"]:
            completed_paths.append(".".join(str(part) for part in path))
        children: list[object] = []
        next_index = 1
        for prefix in METADATA_PREFIXES:
            source_name = "dependsOn" if prefix.startswith("Dependency") else "evidence"
            for reference in item[source_name]:
                children.append(f"{prefix}{reference}")
                completed_paths.append(
                    ".".join(str(part) for part in (*path, next_index))
                )
                next_index += 1
        for child in item["children"]:
            children.append(render_item(child, (*path, next_index)))
            next_index += 1
        if children:
            return {item["title"]: children}
        return item["title"]

    rendered_tasks = [
        render_item(item, (index,))
        for index, item in enumerate(definition["tasks"], start=2)
    ]
    hierarchy = {
        definition["title"]: [f"Objective: {definition['objective']}", *rendered_tasks]
    }
    return hierarchy, tuple(completed_paths)


def _plan_item(value: object, field: str, *, depth: int = 1) -> _PlanItem:
    if depth > 50 or not isinstance(value, dict):
        raise _PlanHelperError(
            "INVALID_PLAN", f"Plan field {field} is not a valid item object."
        )
    if set(value) != {"text", "complete", "children"}:
        raise _PlanHelperError(
            "INVALID_PLAN", f"Plan field {field} has an invalid item shape."
        )
    text = value["text"]
    complete = value["complete"]
    children = value["children"]
    if not isinstance(text, str) or not text.strip() or text != text.strip():
        raise _PlanHelperError("INVALID_PLAN", f"Plan field {field}.text is invalid.")
    if not isinstance(complete, bool) or not isinstance(children, list):
        raise _PlanHelperError(
            "INVALID_PLAN", f"Plan field {field} has invalid state or children."
        )
    return _PlanItem(
        text=text,
        complete=complete,
        children=tuple(
            _plan_item(child, f"{field}.children[{index}]", depth=depth + 1)
            for index, child in enumerate(children)
        ),
    )


def _load_plan(context: _PlanContext) -> _PlanDocument:
    _safe_file(context.plan_path, context, required=True)
    payload = _read_json(
        context.plan_path,
        "INVALID_PLAN",
        "The authoritative hierarchy plan is not valid JSON.",
    )
    if payload.get("schema") != PLAN_SCHEMA or payload.get("version") != PLAN_VERSION:
        raise _PlanHelperError(
            "INVALID_PLAN", "The hierarchy plan has an unsupported schema or version."
        )
    required = {
        "schema",
        "version",
        "title",
        "theme",
        "themesFolder",
        "htmlFilename",
        "rootLabel",
        "items",
    }
    if set(payload) != required:
        raise _PlanHelperError(
            "INVALID_PLAN", "The hierarchy plan has an invalid document shape."
        )
    for field in ("title", "theme", "htmlFilename", "rootLabel"):
        if not isinstance(payload[field], str) or not payload[field]:
            raise _PlanHelperError(
                "INVALID_PLAN", f"Plan field {field} must be a non-empty string."
            )
    if payload["themesFolder"] is not None:
        raise _PlanHelperError(
            "INVALID_PLAN",
            "Task-owned plans do not accept external theme folders.",
        )
    if payload["htmlFilename"] != context.html_path.name:
        raise _PlanHelperError(
            "INVALID_PLAN",
            "The plan HTML filename does not match the fixed task-owned plan path.",
            expected=context.html_path.name,
            observed=payload["htmlFilename"],
        )
    items = payload["items"]
    if not isinstance(items, list) or not items:
        raise _PlanHelperError(
            "INVALID_PLAN", "Plan field items must be a non-empty JSON array."
        )
    return _PlanDocument(
        title=payload["title"],
        theme=payload["theme"],
        themes_folder=payload["themesFolder"],
        html_filename=payload["htmlFilename"],
        root_label=payload["rootLabel"],
        items=tuple(
            _plan_item(item, f"items[{index}]") for index, item in enumerate(items)
        ),
    )


def _hierarchy_items(items: Sequence[_PlanItem]) -> list[object]:
    rendered: list[object] = []
    for item in items:
        if item.children:
            rendered.append({item.text: _hierarchy_items(item.children)})
        else:
            rendered.append(item.text)
    return rendered


def _completed_paths(
    items: Sequence[_PlanItem], prefix: tuple[int, ...] = ()
) -> list[str]:
    completed: list[str] = []
    for index, item in enumerate(items, start=1):
        path = (*prefix, index)
        if item.complete:
            completed.append(".".join(str(part) for part in path))
        completed.extend(_completed_paths(item.children, path))
    return completed


def _sha256(path: Path) -> str | None:
    if not path.is_file() or path.is_symlink():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _evidence(context: _PlanContext) -> dict[str, object]:
    return {
        "plan_path": str(context.plan_path.resolve(strict=False)),
        "html_path": str(context.html_path.resolve(strict=False)),
        "json_sha256": _sha256(context.plan_path),
        "html_sha256": _sha256(context.html_path),
    }


def _reconciliation_token(evidence: dict[str, object]) -> str | None:
    json_hash = evidence.get("json_sha256")
    html_hash = evidence.get("html_sha256")
    if not isinstance(json_hash, str) or not isinstance(html_hash, str):
        return None
    return hashlib.sha256(f"{json_hash}:{html_hash}".encode("ascii")).hexdigest()


def _inspect(context: _PlanContext, api: _PlanApi) -> dict[str, object]:
    document = _load_plan(context)
    _safe_file(context.html_path, context, required=False)
    expected = api.render_hierarchy_html(
        {document.root_label: _hierarchy_items(document.items)},
        title=document.title,
        theme=document.theme,
        themes_folder=document.themes_folder,
        numbering=True,
        checkboxes=True,
        completed_items=_completed_paths(document.items),
    )
    if not isinstance(expected, str):
        raise _PlanHelperError(
            "CAPABILITY_UNAVAILABLE",
            "render_hierarchy_html did not return HTML for a non-writing inspection.",
            exit_code=3,
        )
    observed = None
    if context.html_path.is_file():
        try:
            observed = context.html_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            raise _PlanHelperError(
                "INVALID_HTML",
                "The sibling HTML plan cannot be read as UTF-8.",
                cause=str(error),
            ) from error
    evidence = _evidence(context)
    synchronized = observed == expected
    unresolved = _unresolved_uncertain_operations(context)
    return _result(
        "SYNCED" if synchronized else "DRIFT",
        synchronized=synchronized,
        authoritative_source="json",
        expected_html_sha256=hashlib.sha256(expected.encode("utf-8")).hexdigest(),
        reconciliation_token=_reconciliation_token(evidence) if synchronized else None,
        unresolved_operations=unresolved,
        **evidence,
    )


def _walk_items(
    items: Sequence[_PlanItem], prefix: tuple[int, ...] = ()
) -> list[tuple[str, _PlanItem]]:
    walked: list[tuple[str, _PlanItem]] = []
    for index, item in enumerate(items, start=1):
        path = (*prefix, index)
        dotted = ".".join(str(part) for part in path)
        walked.append((dotted, item))
        walked.extend(_walk_items(item.children, path))
    return walked


def _validate_target(document: _PlanDocument, target: str) -> None:
    normalized = target.strip()
    if not normalized:
        raise _PlanHelperError("MISSING_TARGET", "The update target is empty.")
    walked = _walk_items(document.items)
    if DOTTED_PATH.fullmatch(normalized):
        if normalized not in {path for path, _ in walked}:
            raise _PlanHelperError(
                "MISSING_TARGET",
                "The dotted target does not identify a plan item.",
                target=target,
            )
        return
    matches = [path for path, item in walked if item.text == normalized]
    if not matches:
        raise _PlanHelperError(
            "MISSING_TARGET",
            "The exact title target does not identify a plan item.",
            target=target,
        )
    if len(matches) > 1:
        raise _PlanHelperError(
            "AMBIGUOUS_TARGET",
            "The exact title target matches more than one plan item; use a dotted path.",
            target=target,
            matches=matches,
        )


def _history_directories(context: _PlanContext) -> list[Path]:
    if not context.history_root.is_dir():
        return []
    _reject_symlink_components(context.workspace, context.history_root)
    directories: list[Path] = []
    for entry in context.history_root.iterdir():
        if (
            entry.is_symlink()
            or not entry.is_dir()
            or HISTORY_DIRECTORY.fullmatch(entry.name) is None
        ):
            raise _PlanHelperError(
                "INVALID_HISTORY",
                "The operational plan history contains an unexpected entry.",
                exit_code=4,
                path=str(entry),
            )
        directories.append(entry)
    return sorted(directories)


def _history_results(context: _PlanContext) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for directory in _history_directories(context):
        result_path = directory / "result.json"
        if not result_path.is_file() or result_path.is_symlink():
            continue
        payload = _read_json(
            result_path, "INVALID_HISTORY", "A plan history result is invalid."
        )
        results.append(payload)
    return results


def _unresolved_uncertain_operations(context: _PlanContext) -> list[str]:
    uncertain: set[str] = set()
    reconciled: set[str] = set()
    for result in _history_results(context):
        operation_id = result.get("operation_id")
        if result.get("outcome") in {
            "UNCERTAIN_UPDATE",
            "UNCERTAIN_RECONCILIATION",
        } and isinstance(operation_id, str):
            uncertain.add(operation_id)
        references = result.get("reconciles", [])
        if isinstance(references, list):
            reconciled.update(
                reference for reference in references if isinstance(reference, str)
            )
    return sorted(uncertain - reconciled)


def _remove_tree(directory: Path, root: Path) -> None:
    if not _is_within(directory, root) or directory == root or directory.is_symlink():
        raise _PlanHelperError(
            "CLEANUP_REJECTED",
            "Cleanup refused an unsafe directory boundary.",
            exit_code=4,
            path=str(directory),
        )
    if not directory.exists():
        return
    for entry in directory.iterdir():
        if entry.is_symlink():
            raise _PlanHelperError(
                "CLEANUP_REJECTED",
                "Cleanup refuses symbolic links in plan operational state.",
                exit_code=4,
                path=str(entry),
            )
        if entry.is_dir():
            _remove_tree(entry, root)
        elif entry.is_file():
            entry.unlink()
        else:
            raise _PlanHelperError(
                "CLEANUP_REJECTED",
                "Cleanup refuses non-file plan operational state.",
                exit_code=4,
                path=str(entry),
            )
    directory.rmdir()


def _validate_cleanup_tree(directory: Path, root: Path) -> None:
    if not _is_within(directory, root) or directory == root or directory.is_symlink():
        raise _PlanHelperError(
            "CLEANUP_REJECTED",
            "Cleanup refused an unsafe directory boundary.",
            exit_code=4,
            path=str(directory),
        )
    if not directory.exists():
        return
    for entry in directory.iterdir():
        if entry.is_symlink():
            raise _PlanHelperError(
                "CLEANUP_REJECTED",
                "Cleanup refuses symbolic links in plan operational state.",
                exit_code=4,
                path=str(entry),
            )
        if entry.is_dir():
            _validate_cleanup_tree(entry, root)
        elif not entry.is_file():
            raise _PlanHelperError(
                "CLEANUP_REJECTED",
                "Cleanup refuses non-file plan operational state.",
                exit_code=4,
                path=str(entry),
            )


def _prune_history(context: _PlanContext) -> None:
    directories = _history_directories(context)
    if len(directories) < HISTORY_LIMIT:
        return
    unresolved = set(_unresolved_uncertain_operations(context))
    for directory in list(directories):
        result_path = directory / "result.json"
        operation_id = None
        if result_path.is_file() and not result_path.is_symlink():
            payload = _read_json(
                result_path, "INVALID_HISTORY", "A plan history result is invalid."
            )
            operation_id = payload.get("operation_id")
        if operation_id not in unresolved:
            _remove_tree(directory, context.history_root)
            directories.remove(directory)
            if len(directories) < HISTORY_LIMIT:
                return
    raise _PlanHelperError(
        "HISTORY_LIMIT_REACHED",
        "Twenty unresolved operational snapshots are retained; reconcile them before another mutation.",
        exit_code=4,
        unresolved_operations=sorted(unresolved),
    )


def _start_history(context: _PlanContext, operation: str) -> tuple[str, Path]:
    _make_safe_directory(context.workspace, context.history_root)
    _prune_history(context)
    directories = _history_directories(context)
    sequence = 1
    if directories:
        match = HISTORY_DIRECTORY.fullmatch(directories[-1].name)
        if match is not None:
            sequence = int(match.group("sequence")) + 1
    operation_id = f"{sequence:06d}-{operation}"
    operation_path = context.history_root / operation_id
    operation_path.mkdir()
    (operation_path / "before.json").write_bytes(context.plan_path.read_bytes())
    before_html = context.html_path.read_bytes() if context.html_path.is_file() else b""
    (operation_path / "before.html").write_bytes(before_html)
    return operation_id, operation_path


def _write_history_result(operation_path: Path, result: dict[str, object]) -> None:
    target = operation_path / "result.json"
    target.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def _create(
    context: _PlanContext, arguments: argparse.Namespace, api: _PlanApi
) -> dict[str, object]:
    definition = _load_definition(arguments.definition, context)
    _reject_symlink_components(context.workspace, context.plan_path)
    if _lexists(context.plan_path) or _lexists(context.html_path):
        raise _PlanHelperError(
            "PLAN_ALREADY_EXISTS",
            "Create refuses to overwrite an existing canonical plan or sibling HTML file.",
            plan_path=str(context.plan_path),
            html_path=str(context.html_path),
        )
    _make_safe_directory(context.workspace, context.task_root)
    hierarchy, completed_paths = _definition_hierarchy(definition)
    mutation_started = False
    try:
        mutation_started = True
        observed_path = api.create_hierarchy_plan(
            hierarchy,
            title=definition["title"],
            output_filename=context.html_path.name,
            output_folder=context.task_root,
            completed_items=completed_paths,
        )
        if Path(observed_path).resolve() != context.plan_path.resolve():
            raise RuntimeError(
                "create_hierarchy_plan returned an unexpected canonical path"
            )
        inspected = _inspect(context, api)
        if not inspected["synchronized"]:
            raise RuntimeError(
                "created JSON and HTML plan artifacts are not synchronized"
            )
    except Exception as error:
        outcome = "UNCERTAIN_CREATE" if mutation_started else "CREATE_FAILED"
        raise _PlanHelperError(
            outcome,
            "Plan creation may have changed the task-owned artifacts; inspect before retrying.",
            exit_code=4,
            inspect_required=True,
            cause=str(error),
            current=_evidence(context),
        ) from error
    return _result(
        "CREATED",
        package_version=api.package_version,
        definition_path=str(definition["path"]),
        task_plan_root=str(context.task_root),
        history_policy={
            "kind": "operational",
            "maximum_settled_snapshots": HISTORY_LIMIT,
        },
        plan_path=str(context.plan_path.resolve()),
        html_path=str(context.html_path.resolve()),
        after=_evidence(context),
        synchronized=True,
    )


def _update(
    context: _PlanContext, arguments: argparse.Namespace, api: _PlanApi
) -> dict[str, object]:
    inspected = _inspect(context, api)
    if not inspected["synchronized"]:
        raise _PlanHelperError(
            "RECONCILIATION_REQUIRED",
            "The authoritative JSON and sibling HTML differ; run reconcile before update.",
            exit_code=4,
            unresolved_operations=inspected["unresolved_operations"],
            inspect_required=True,
            inspect=inspected,
        )
    unresolved = list(inspected["unresolved_operations"])
    reconciliation_token = arguments.reconciliation_token
    if unresolved:
        if reconciliation_token != inspected["reconciliation_token"]:
            raise _PlanHelperError(
                "RECONCILIATION_REQUIRED",
                "A prior uncertain mutation requires a current inspect token or successful reconcile before retry.",
                exit_code=4,
                unresolved_operations=unresolved,
                inspect_required=True,
            )
    elif reconciliation_token is not None:
        raise _PlanHelperError(
            "INVALID_REQUEST",
            "--reconciliation-token is valid only when inspect reports unresolved uncertain operations.",
        )
    document = _load_plan(context)
    _validate_target(document, arguments.target)
    mutation: dict[str, object]
    if arguments.complete:
        mutation = {"completed": True}
    elif arguments.incomplete:
        mutation = {"completed": False}
    elif arguments.add_child is not None:
        mutation = {"add_child": _single_line(arguments.add_child, "add-child")}
    elif arguments.add_peer_after is not None:
        mutation = {
            "add_peer_after": _single_line(arguments.add_peer_after, "add-peer-after")
        }
    else:
        raise _PlanHelperError(
            "INVALID_REQUEST", "Update requires exactly one supported mutation."
        )

    before = _evidence(context)
    operation_id, operation_path = _start_history(context, "update")
    try:
        api.update_hierarchy_plan(context.plan_path, arguments.target, **mutation)
        after_inspection = _inspect(context, api)
        if not after_inspection["synchronized"]:
            raise RuntimeError(
                "updated JSON and HTML plan artifacts are not synchronized"
            )
        after = _evidence(context)
        result = _result(
            "UPDATED",
            operation_id=operation_id,
            history_path=str(operation_path),
            mutation=next(iter(mutation)),
            target=arguments.target,
            before=before,
            after=after,
            synchronized=True,
            reconciles=unresolved,
        )
        _write_history_result(operation_path, result)
        return result
    except Exception as error:
        result = _result(
            "UNCERTAIN_UPDATE",
            operation_id=operation_id,
            history_path=str(operation_path),
            mutation=next(iter(mutation)),
            target=arguments.target,
            before=before,
            current=_evidence(context),
            error=str(error),
            inspect_required=True,
            retry_allowed=False,
            reconciles=[],
        )
        try:
            _write_history_result(operation_path, result)
        except OSError:
            pass
        return result


def _reconcile(context: _PlanContext, api: _PlanApi) -> dict[str, object]:
    inspected = _inspect(context, api)
    if inspected["synchronized"]:
        unresolved = list(inspected["unresolved_operations"])
        if not unresolved:
            return _result(
                "ALREADY_SYNCED",
                **{key: value for key, value in inspected.items() if key != "outcome"},
            )
        operation_id, operation_path = _start_history(context, "reconcile")
        result = _result(
            "RECONCILED",
            operation_id=operation_id,
            history_path=str(operation_path),
            synchronized=True,
            reconciles=unresolved,
            no_artifact_change=True,
            **_evidence(context),
        )
        _write_history_result(operation_path, result)
        return result
    document = _load_plan(context)
    before = _evidence(context)
    operation_id, operation_path = _start_history(context, "reconcile")
    unresolved = _unresolved_uncertain_operations(context)
    try:
        api.render_hierarchy_html(
            {document.root_label: _hierarchy_items(document.items)},
            title=document.title,
            theme=document.theme,
            themes_folder=document.themes_folder,
            numbering=True,
            checkboxes=True,
            completed_items=_completed_paths(document.items),
            output_filename=context.html_path.name,
            output_folder=context.task_root,
        )
        after_inspection = _inspect(context, api)
        if not after_inspection["synchronized"]:
            raise RuntimeError(
                "HTML reconciliation did not synchronize the plan artifacts"
            )
        result = _result(
            "RECONCILED",
            operation_id=operation_id,
            history_path=str(operation_path),
            authoritative_source="json",
            before=before,
            after=_evidence(context),
            synchronized=True,
            reconciles=unresolved,
        )
        _write_history_result(operation_path, result)
        return result
    except Exception as error:
        result = _result(
            "UNCERTAIN_RECONCILIATION",
            operation_id=operation_id,
            history_path=str(operation_path),
            before=before,
            current=_evidence(context),
            error=str(error),
            inspect_required=True,
            retry_allowed=False,
            reconciles=[],
        )
        try:
            _write_history_result(operation_path, result)
        except OSError:
            pass
        return result


def _incomplete_items(document: _PlanDocument) -> list[str]:
    incomplete: list[str] = []
    for path, item in _walk_items(document.items):
        if path == "1" and item.text.startswith("Objective: "):
            continue
        if item.text.startswith(METADATA_PREFIXES):
            continue
        if not item.complete:
            incomplete.append(item.text)
    return incomplete


def _validate_plan_cleanup(context: _PlanContext) -> None:
    for path in (context.plan_path, context.html_path):
        _safe_file(path, context, required=True)
    if context.history_root.exists():
        _validate_cleanup_tree(context.history_root, context.task_root)


def _remove_plan(context: _PlanContext) -> list[str]:
    removed: list[str] = []
    for path in (context.plan_path, context.html_path):
        path.unlink()
        removed.append(str(path))
    if context.history_root.exists():
        _remove_tree(context.history_root, context.task_root)
        removed.append(str(context.history_root))
    history_parent = context.task_root / ".history"
    if history_parent.is_dir() and not any(history_parent.iterdir()):
        history_parent.rmdir()
    if context.task_root.is_dir() and not any(context.task_root.iterdir()):
        context.task_root.rmdir()
    return removed


def _finalize(
    context: _PlanContext, arguments: argparse.Namespace, api: _PlanApi
) -> dict[str, object]:
    inspected = _inspect(context, api)
    if not inspected["synchronized"] or inspected["unresolved_operations"]:
        raise _PlanHelperError(
            "RECONCILIATION_REQUIRED",
            "Finalize requires synchronized artifacts and no unresolved uncertain operation.",
            exit_code=4,
            inspect=inspected,
        )
    document = _load_plan(context)
    incomplete = _incomplete_items(document)
    if incomplete:
        raise _PlanHelperError(
            "FINALIZATION_INCOMPLETE",
            "Finalize requires every actionable task and subtask to be complete.",
            exit_code=4,
            incomplete_items=incomplete,
        )
    evidence = _evidence(context)
    if arguments.retention == "keep":
        return _result(
            "FINALIZED",
            retention="keep",
            synchronized=True,
            authoritative_source="json",
            evidence=evidence,
            history_policy={
                "kind": "operational",
                "maximum_settled_snapshots": HISTORY_LIMIT,
            },
        )
    _validate_plan_cleanup(context)
    try:
        removed = _remove_plan(context)
    except (OSError, _PlanHelperError) as error:
        raise _PlanHelperError(
            "UNCERTAIN_CLEANUP",
            "Cleanup may have removed part of the selected task-owned plan; reconcile exact paths before retry.",
            exit_code=4,
            cause=str(error),
            current=_evidence(context),
            retry_allowed=False,
            reconciliation_required=True,
        ) from error
    return _result(
        "CLEANED",
        retention="remove",
        synchronized_before_cleanup=True,
        evidence_before_cleanup=evidence,
        removed=removed,
        provider_state_changed=False,
    )


def _parser() -> _JsonArgumentParser:
    parser = _JsonArgumentParser(
        description="Manage one task-owned complex-development hierarchy plan."
    )
    parser.add_argument("--workspace")
    parser.add_argument("--root-task-id")
    parser.add_argument("--plan-name")
    subparsers = parser.add_subparsers(
        dest="command", required=True, parser_class=_JsonArgumentParser
    )
    subparsers.add_parser("capabilities")

    create = subparsers.add_parser("create")
    create.add_argument("--definition", required=True)

    update = subparsers.add_parser("update")
    update.add_argument("--target", required=True)
    update.add_argument("--reconciliation-token")
    mutations = update.add_mutually_exclusive_group(required=True)
    mutations.add_argument("--complete", action="store_true")
    mutations.add_argument("--incomplete", action="store_true")
    mutations.add_argument("--add-child")
    mutations.add_argument("--add-peer-after")

    subparsers.add_parser("inspect")
    subparsers.add_parser("reconcile")

    finalize = subparsers.add_parser("finalize")
    finalize.add_argument("--retention", choices=("keep", "remove"), required=True)
    return parser


def execute(argv: Sequence[str] | None = None) -> tuple[int, dict[str, object]]:
    """Execute one helper command and return its process code plus structured result.

    Args:
        argv: Command arguments without the executable name. Process arguments are used
            when this value is omitted.

    Returns:
        A process exit code and one JSON-serializable result object. Code zero denotes a
        completed operation. Codes two, three, and four denote invalid input, unavailable
        package capability, and required reconciliation respectively.

    Side effects:
        Plan commands can create or update files only under the fixed task-owned plan root.
        The capabilities and inspect commands do not change plan artifacts.
    """
    try:
        arguments = _parser().parse_args(list(sys.argv[1:] if argv is None else argv))
        api = _load_api()
        if arguments.command == "capabilities":
            return 0, _capability_result(api)
        context = _context(arguments)
        if arguments.command == "create":
            return 0, _create(context, arguments, api)
        if arguments.command == "inspect":
            inspected = _inspect(context, api)
            return (0 if inspected["synchronized"] else 4), inspected
        if arguments.command == "update":
            result = _update(context, arguments, api)
            return (4 if result["outcome"] == "UNCERTAIN_UPDATE" else 0), result
        if arguments.command == "reconcile":
            result = _reconcile(context, api)
            return (4 if result["outcome"] == "UNCERTAIN_RECONCILIATION" else 0), result
        if arguments.command == "finalize":
            return 0, _finalize(context, arguments, api)
        raise _PlanHelperError("INVALID_REQUEST", "Unknown helper command.")
    except _PlanHelperError as error:
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
    """Run the portable command and print exactly one structured JSON result.

    Args:
        argv: Optional command arguments without the executable name.

    Returns:
        The process exit code paired with the printed result.

    Side effects:
        The command can re-exec under the installed mcp-agent-ops interpreter, print one
        JSON result, and perform only the task-owned file effects of the selected command.
    """
    arguments = list(sys.argv[1:] if argv is None else argv)
    try:
        _maybe_reexec(arguments)
        exit_code, result = execute(arguments)
    except _PlanHelperError as error:
        exit_code = error.exit_code
        result = _result(error.outcome, error=error.message, **error.details)
    print(json.dumps(result, sort_keys=True))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
