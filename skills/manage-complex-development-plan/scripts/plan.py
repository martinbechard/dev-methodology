# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Manages task-owned hierarchy plans through the installed mcp-agent-ops package APIs.

from __future__ import annotations

import argparse
import errno
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
import time
from collections.abc import Callable, Sequence
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO, Iterator


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
HISTORY_DIRECTORY = re.compile(
    r"(?P<sequence>[0-9]{6})-(?P<kind>create|update|reconcile|cleanup)"
)
METADATA_PREFIXES = ("Dependency reference: ", "Evidence reference: ")
OPERATION_SCHEMA = "dev-methodology-complex-plan-operation"
OPERATION_VERSION = 1
RECOVERY_DECISION_VERSION = 1
LOCK_TIMEOUT_SECONDS = 5.0
LOCK_POLL_SECONDS = 0.05
TERMINAL_OPERATION_OUTCOMES = {
    "create": frozenset({"CREATED", "RECOVERED_OPERATION"}),
    "update": frozenset({"UPDATED", "RECOVERED_OPERATION"}),
    "reconcile": frozenset(
        {
            "RECONCILED",
            "RECOVERED_ABSENT",
            "RECOVERED_OPERATION",
            "RECOVERY_REJECTED",
        }
    ),
    "cleanup": frozenset({"CLEANED", "RECOVERED_OPERATION"}),
}


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
    signatures: dict[str, str]


@dataclass(frozen=True)
class _PlanContext:
    workspace: Path
    task_root: Path
    plan_name: str
    plan_path: Path
    html_path: Path
    history_root: Path
    lock_path: Path


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


@dataclass(frozen=True)
class _OperationStatus:
    operation_id: str
    kind: str
    path: Path
    terminal: bool
    result_state: str
    result: dict[str, object] | None
    operation_state: str
    operation: dict[str, object] | None


def _result(outcome: str, **details: object) -> dict[str, object]:
    return {"schema_version": RESULT_SCHEMA_VERSION, "outcome": outcome, **details}


def _validate_api_contract(
    functions: dict[str, Callable[..., object]],
) -> dict[str, str]:
    call_shapes: dict[str, tuple[tuple[tuple[object, ...], dict[str, object]], ...]] = {
        "create_hierarchy_plan": (
            (
                (object(),),
                {
                    "title": "Plan",
                    "output_filename": "plan.html",
                    "output_folder": Path("."),
                    "completed_items": (),
                },
            ),
        ),
        "render_hierarchy_html": (
            (
                (object(),),
                {
                    "title": "Plan",
                    "theme": "default",
                    "themes_folder": None,
                    "numbering": True,
                    "checkboxes": True,
                    "completed_items": (),
                },
            ),
            (
                (object(),),
                {
                    "title": "Plan",
                    "theme": "default",
                    "themes_folder": None,
                    "numbering": True,
                    "checkboxes": True,
                    "completed_items": (),
                    "output_filename": "plan.html",
                    "output_folder": Path("."),
                },
            ),
        ),
        "update_hierarchy_plan": (
            ((Path("plan.json"), "Task"), {"completed": True}),
            ((Path("plan.json"), "Task"), {"add_child": "Child"}),
            ((Path("plan.json"), "Task"), {"add_peer_after": "Peer"}),
        ),
    }
    signatures: dict[str, str] = {}
    incompatibilities: dict[str, str] = {}
    for name, shapes in call_shapes.items():
        function = functions.get(name)
        if not callable(function):
            incompatibilities[name] = "not callable"
            continue
        try:
            signature = inspect.signature(function)
            for positional, keywords in shapes:
                signature.bind(*positional, **keywords)
        except (TypeError, ValueError) as error:
            incompatibilities[name] = str(error)
            continue
        signatures[name] = str(signature)
    if incompatibilities:
        raise _PlanHelperError(
            "CAPABILITY_UNAVAILABLE",
            "The installed mcp-agent-ops package cannot accept every hierarchy call shape used by this helper.",
            exit_code=3,
            incompatibilities=incompatibilities,
        )
    return signatures


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
    signatures = _validate_api_contract(functions)
    try:
        package_version = importlib.metadata.version("mcp-agent-ops")
    except importlib.metadata.PackageNotFoundError:
        package_version = "unknown"
    return _PlanApi(
        create_hierarchy_plan=create_hierarchy_plan,
        render_hierarchy_html=render_hierarchy_html,
        update_hierarchy_plan=update_hierarchy_plan,
        package_version=package_version,
        signatures=signatures,
    )


def _capability_result(api: _PlanApi) -> dict[str, object]:
    if os.name not in {"posix", "nt"}:
        raise _PlanHelperError(
            "CAPABILITY_UNAVAILABLE",
            "The helper has no safe single-writer lock backend for this platform.",
            exit_code=3,
            platform=os.name,
        )
    _lock_module(os.name)
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
        signatures=api.signatures,
        lock_backend="fcntl" if os.name == "posix" else "msvcrt",
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
    lock_path = task_root / ".locks" / f"{plan_name}.lock"
    return _PlanContext(
        workspace=workspace,
        task_root=task_root,
        plan_name=plan_name,
        plan_path=plan_path,
        html_path=html_path,
        history_root=history_root,
        lock_path=lock_path,
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


def _lock_module(platform_name: str) -> object:
    module_name = "fcntl" if platform_name == "posix" else "msvcrt"
    try:
        return __import__(module_name)
    except ImportError as error:
        raise _PlanHelperError(
            "CAPABILITY_UNAVAILABLE",
            "This Python runtime does not provide the standard-library plan-lock backend.",
            exit_code=3,
            platform=platform_name,
            required_module=module_name,
        ) from error


def _try_platform_lock(
    lock_file: BinaryIO,
    *,
    platform_name: str | None = None,
    platform_module: object | None = None,
) -> bool:
    selected_platform = os.name if platform_name is None else platform_name
    if selected_platform not in {"posix", "nt"}:
        raise _PlanHelperError(
            "CAPABILITY_UNAVAILABLE",
            "The helper has no safe single-writer lock backend for this platform.",
            exit_code=3,
            platform=selected_platform,
        )
    module = (
        _lock_module(selected_platform) if platform_module is None else platform_module
    )
    try:
        if selected_platform == "posix":
            flock = getattr(module, "flock")
            flock(
                lock_file.fileno(),
                getattr(module, "LOCK_EX") | getattr(module, "LOCK_NB"),
            )
        else:
            lock_file.seek(0, os.SEEK_END)
            if lock_file.tell() == 0:
                lock_file.write(b"\0")
                lock_file.flush()
            lock_file.seek(0)
            locking = getattr(module, "locking")
            locking(lock_file.fileno(), getattr(module, "LK_NBLCK"), 1)
    except (BlockingIOError, PermissionError):
        return False
    except OSError as error:
        if error.errno in {errno.EACCES, errno.EAGAIN, errno.EDEADLK}:
            return False
        raise _PlanHelperError(
            "LOCK_FAILED",
            "The per-plan single-writer lock could not be acquired safely.",
            exit_code=4,
            cause=str(error),
        ) from error
    return True


def _release_platform_lock(
    lock_file: BinaryIO,
    *,
    platform_name: str | None = None,
    platform_module: object | None = None,
) -> None:
    selected_platform = os.name if platform_name is None else platform_name
    if selected_platform not in {"posix", "nt"}:
        raise _PlanHelperError(
            "CAPABILITY_UNAVAILABLE",
            "The helper has no safe single-writer lock backend for this platform.",
            exit_code=3,
            platform=selected_platform,
        )
    module = (
        _lock_module(selected_platform) if platform_module is None else platform_module
    )
    try:
        if selected_platform == "posix":
            getattr(module, "flock")(lock_file.fileno(), getattr(module, "LOCK_UN"))
        else:
            lock_file.seek(0)
            getattr(module, "locking")(
                lock_file.fileno(), getattr(module, "LK_UNLCK"), 1
            )
    except OSError as error:
        raise _PlanHelperError(
            "LOCK_FAILED",
            "The per-plan single-writer lock could not be released safely.",
            exit_code=4,
            cause=str(error),
        ) from error


@contextmanager
def _plan_lock(
    context: _PlanContext, *, timeout_seconds: float = LOCK_TIMEOUT_SECONDS
) -> Iterator[None]:
    _make_safe_directory(context.workspace, context.lock_path.parent)
    _reject_symlink_components(context.workspace, context.lock_path)
    flags = os.O_CREAT | os.O_RDWR
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(context.lock_path, flags, 0o600)
    except OSError as error:
        raise _PlanHelperError(
            "LOCK_FAILED",
            "The per-plan lock file could not be opened safely.",
            exit_code=4,
            lock_path=str(context.lock_path),
            cause=str(error),
        ) from error
    lock_file = os.fdopen(descriptor, "r+b", buffering=0)
    acquired = False
    try:
        if not stat.S_ISREG(os.fstat(lock_file.fileno()).st_mode):
            raise _PlanHelperError(
                "LOCK_FAILED",
                "The per-plan lock path is not a regular file.",
                exit_code=4,
                lock_path=str(context.lock_path),
            )
        deadline = time.monotonic() + timeout_seconds
        while not _try_platform_lock(lock_file):
            if time.monotonic() >= deadline:
                raise _PlanHelperError(
                    "LOCK_TIMEOUT",
                    "Another process retained the selected plan's single-writer lock.",
                    exit_code=4,
                    lock_path=str(context.lock_path),
                    timeout_seconds=timeout_seconds,
                    retry_allowed=True,
                )
            time.sleep(LOCK_POLL_SECONDS)
        acquired = True
        yield
    finally:
        try:
            if acquired:
                _release_platform_lock(lock_file)
        finally:
            lock_file.close()


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


def _action_text(value: object, field: str) -> str:
    text = _single_line(value, field)
    if text.startswith(METADATA_PREFIXES):
        raise _PlanHelperError(
            "RESERVED_ACTION_TEXT",
            "Actionable plan text must not use a structural reference prefix.",
            field=field,
            reserved_prefixes=list(METADATA_PREFIXES),
        )
    return text


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
        "title": _action_text(value["title"], f"{field}.title"),
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
    if text.startswith(METADATA_PREFIXES) and (not complete or children):
        raise _PlanHelperError(
            "INVALID_PLAN",
            f"Plan field {field} uses a structural reference prefix without complete leaf metadata state.",
        )
    return _PlanItem(
        text=text,
        complete=complete,
        children=tuple(
            _plan_item(child, f"{field}.children[{index}]", depth=depth + 1)
            for index, child in enumerate(children)
        ),
    )


def _plan_document_from_payload(
    payload: dict[str, object], context: _PlanContext
) -> _PlanDocument:
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


def _load_plan(context: _PlanContext) -> _PlanDocument:
    _safe_file(context.plan_path, context, required=True)
    payload = _read_json(
        context.plan_path,
        "INVALID_PLAN",
        "The authoritative hierarchy plan is not valid JSON.",
    )
    return _plan_document_from_payload(payload, context)


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
        "json_exists": context.plan_path.is_file()
        and not context.plan_path.is_symlink(),
        "html_exists": context.html_path.is_file()
        and not context.html_path.is_symlink(),
        "json_sha256": _sha256(context.plan_path),
        "html_sha256": _sha256(context.html_path),
    }


def _render_document(
    context: _PlanContext,
    document: _PlanDocument,
    api: _PlanApi,
    *,
    write: bool,
) -> str | Path:
    keywords: dict[str, object] = {
        "title": document.title,
        "theme": document.theme,
        "themes_folder": document.themes_folder,
        "numbering": True,
        "checkboxes": True,
        "completed_items": _completed_paths(document.items),
    }
    if write:
        keywords.update(
            output_filename=context.html_path.name,
            output_folder=context.task_root,
        )
    return api.render_hierarchy_html(
        {document.root_label: _hierarchy_items(document.items)},
        **keywords,
    )


def _analyze_artifacts(context: _PlanContext, api: _PlanApi) -> dict[str, object]:
    _safe_file(context.plan_path, context, required=False)
    _safe_file(context.html_path, context, required=False)
    evidence = _evidence(context)
    plan_exists = bool(evidence["json_exists"])
    html_exists = bool(evidence["html_exists"])
    if not plan_exists and not html_exists:
        return {
            "artifact_state": "ABSENT",
            "synchronized": False,
            "document": None,
            "expected_html_sha256": None,
            **evidence,
        }
    if not plan_exists:
        return {
            "artifact_state": "HTML_ONLY",
            "synchronized": False,
            "document": None,
            "expected_html_sha256": None,
            **evidence,
        }
    try:
        document = _load_plan(context)
    except _PlanHelperError as error:
        if error.outcome != "INVALID_PLAN":
            raise
        return {
            "artifact_state": "INVALID_JSON",
            "synchronized": False,
            "document": None,
            "invalid_plan_error": error.message,
            "invalid_plan_details": error.details,
            "expected_html_sha256": None,
            **evidence,
        }
    expected = _render_document(context, document, api, write=False)
    if not isinstance(expected, str):
        raise _PlanHelperError(
            "CAPABILITY_UNAVAILABLE",
            "render_hierarchy_html did not return HTML for a non-writing inspection.",
            exit_code=3,
        )
    expected_hash = hashlib.sha256(expected.encode("utf-8")).hexdigest()
    if not html_exists:
        return {
            "artifact_state": "JSON_ONLY",
            "synchronized": False,
            "document": document,
            "expected_html_sha256": expected_hash,
            **evidence,
        }
    try:
        observed = context.html_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise _PlanHelperError(
            "INVALID_HTML",
            "The sibling HTML plan cannot be read as UTF-8.",
            cause=str(error),
        ) from error
    synchronized = observed == expected
    return {
        "artifact_state": "SYNCED" if synchronized else "DRIFT",
        "synchronized": synchronized,
        "document": document,
        "expected_html_sha256": expected_hash,
        **evidence,
    }


def _file_fingerprint(path: Path) -> dict[str, object]:
    if not _lexists(path):
        return {"present": False, "type": "missing", "sha256": None}
    try:
        mode = path.lstat().st_mode
    except OSError:
        return {"present": True, "type": "unreadable", "sha256": None}
    if stat.S_ISREG(mode):
        try:
            content_hash = hashlib.sha256(path.read_bytes()).hexdigest()
        except OSError:
            content_hash = None
        return {"present": True, "type": "file", "sha256": content_hash}
    if stat.S_ISLNK(mode):
        try:
            target = os.readlink(path)
            content_hash = hashlib.sha256(target.encode("utf-8")).hexdigest()
        except (OSError, UnicodeError):
            content_hash = None
        return {"present": True, "type": "symlink", "sha256": content_hash}
    if stat.S_ISDIR(mode):
        return {"present": True, "type": "directory", "sha256": None}
    return {"present": True, "type": "other", "sha256": None}


def _recovery_inputs(
    artifact: dict[str, object],
    statuses: Sequence[_OperationStatus],
    *,
    exclude_operations: frozenset[str],
) -> dict[str, object]:
    return {
        "artifact": {
            key: artifact.get(key)
            for key in (
                "artifact_state",
                "json_exists",
                "html_exists",
                "json_sha256",
                "html_sha256",
                "expected_html_sha256",
            )
        },
        "operations": [
            {
                "operation_id": status.operation_id,
                "kind": status.kind,
                "terminal": status.terminal,
                "result_state": status.result_state,
                "files": {
                    filename: _file_fingerprint(status.path / filename)
                    for filename in (
                        "operation.json",
                        "result.json",
                        "before.json",
                        "before.html",
                    )
                },
            }
            for status in statuses
            if status.operation_id not in exclude_operations
        ],
    }


def _recovery_token_for_inputs(inputs: dict[str, object]) -> str:
    serialized = json.dumps(inputs, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def _recovery_token(
    artifact: dict[str, object],
    statuses: Sequence[_OperationStatus],
    *,
    exclude_operations: frozenset[str],
) -> str:
    inputs = _recovery_inputs(
        artifact, statuses, exclude_operations=exclude_operations
    )
    return _recovery_token_for_inputs(inputs)


def _current_recovery_inputs(
    context: _PlanContext,
    api: _PlanApi,
    *,
    exclude_operations: frozenset[str] = frozenset(),
) -> dict[str, object]:
    statuses = _operation_statuses(context)
    artifact = _analyze_artifacts(context, api)
    return _recovery_inputs(
        artifact, statuses, exclude_operations=exclude_operations
    )


def _current_recovery_token(
    context: _PlanContext,
    api: _PlanApi,
    *,
    exclude_operations: frozenset[str] = frozenset(),
) -> str:
    return _recovery_token_for_inputs(
        _current_recovery_inputs(
            context, api, exclude_operations=exclude_operations
        )
    )


def _inspect(
    context: _PlanContext,
    api: _PlanApi,
    *,
    exclude_operations: frozenset[str] = frozenset(),
) -> dict[str, object]:
    statuses = _operation_statuses(context)
    unresolved = [
        status
        for status in statuses
        if not status.terminal and status.operation_id not in exclude_operations
    ]
    artifact = _analyze_artifacts(context, api)
    token = _recovery_token(artifact, statuses, exclude_operations=exclude_operations)
    artifact_state = str(artifact["artifact_state"])
    if unresolved:
        outcome = "RECOVERY_REQUIRED"
    elif artifact_state == "SYNCED":
        outcome = "SYNCED"
    elif artifact_state == "ABSENT":
        outcome = "ABSENT"
    elif artifact_state in {"DRIFT", "JSON_ONLY"}:
        outcome = "DRIFT"
    elif artifact_state == "HTML_ONLY":
        outcome = "ORPHANED_HTML"
    else:
        details = artifact.get("invalid_plan_details")
        raise _PlanHelperError(
            "INVALID_PLAN",
            str(
                artifact.get(
                    "invalid_plan_error", "The authoritative JSON plan is invalid."
                )
            ),
            **(details if isinstance(details, dict) else {}),
        )
    return _result(
        outcome,
        artifact_state=artifact_state,
        synchronized=bool(artifact["synchronized"]),
        authoritative_source="json",
        expected_html_sha256=artifact["expected_html_sha256"],
        recovery_token=token,
        reconciliation_token=token,
        unresolved_operations=[status.operation_id for status in unresolved],
        unresolved_details=[
            {
                "operation_id": status.operation_id,
                "kind": status.kind,
                "result_state": status.result_state,
            }
            for status in unresolved
        ],
        recovery_required=bool(unresolved),
        retryable_create=artifact_state == "ABSENT" and not unresolved,
        **{
            key: value
            for key, value in artifact.items()
            if key
            not in {
                "artifact_state",
                "synchronized",
                "expected_html_sha256",
                "document",
                "invalid_plan_error",
                "invalid_plan_details",
            }
        },
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


def _validate_target(
    document: _PlanDocument, target: str, expected_title: str | None
) -> _PlanItem:
    normalized = target.strip()
    if not normalized:
        raise _PlanHelperError("MISSING_TARGET", "The update target is empty.")
    walked = _walk_items(document.items)
    if DOTTED_PATH.fullmatch(normalized):
        matched = next((item for path, item in walked if path == normalized), None)
        if matched is None:
            raise _PlanHelperError(
                "MISSING_TARGET",
                "The dotted target does not identify a plan item.",
                target=target,
            )
        if expected_title is None:
            raise _PlanHelperError(
                "EXPECTED_TITLE_REQUIRED",
                "A dotted target requires --expected-title from the current authoritative JSON.",
                target=target,
            )
        expected = _single_line(expected_title, "expected-title")
        if matched.text != expected:
            raise _PlanHelperError(
                "STALE_TARGET",
                "The dotted target no longer identifies the expected current title.",
                target=target,
                expected_title=expected,
                observed_title=matched.text,
            )
        if matched.text.startswith(METADATA_PREFIXES):
            raise _PlanHelperError(
                "INVALID_TARGET",
                "Structural dependency and evidence references are not actionable update targets.",
                target=target,
            )
        return matched
    if expected_title is not None:
        raise _PlanHelperError(
            "INVALID_REQUEST",
            "--expected-title is used only with a dotted target.",
        )
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
    matched = next(item for path, item in walked if path == matches[0])
    if matched.text.startswith(METADATA_PREFIXES):
        raise _PlanHelperError(
            "INVALID_TARGET",
            "Structural dependency and evidence references are not actionable update targets.",
            target=target,
        )
    return matched


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


def _soft_json(path: Path) -> tuple[str, dict[str, object] | None]:
    if not _lexists(path):
        return "missing", None
    if path.is_symlink() or not path.is_file():
        return "malformed", None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return "malformed", None
    if not isinstance(payload, dict):
        return "malformed", None
    return "present", payload


def _valid_evidence(value: object) -> bool:
    if not isinstance(value, dict):
        return False
    required = {
        "plan_path",
        "html_path",
        "json_exists",
        "html_exists",
        "json_sha256",
        "html_sha256",
    }
    if set(value) != required:
        return False
    return (
        isinstance(value["plan_path"], str)
        and isinstance(value["html_path"], str)
        and isinstance(value["json_exists"], bool)
        and isinstance(value["html_exists"], bool)
        and (
            value["json_sha256"] is None
            or (
                isinstance(value["json_sha256"], str)
                and re.fullmatch(r"[0-9a-f]{64}", value["json_sha256"]) is not None
            )
        )
        and (
            value["html_sha256"] is None
            or (
                isinstance(value["html_sha256"], str)
                and re.fullmatch(r"[0-9a-f]{64}", value["html_sha256"]) is not None
            )
        )
    )


def _valid_sha256(value: object) -> bool:
    return (
        isinstance(value, str)
        and re.fullmatch(r"[0-9a-f]{64}", value) is not None
    )


def _valid_nonempty_string(value: object, *, maximum: int | None = None) -> bool:
    return (
        isinstance(value, str)
        and bool(value)
        and value == value.strip()
        and "\x00" not in value
        and "\r" not in value
        and "\n" not in value
        and (maximum is None or len(value) <= maximum)
    )


def _valid_operation_ids(value: object) -> bool:
    return (
        isinstance(value, list)
        and all(
            isinstance(item, str) and HISTORY_DIRECTORY.fullmatch(item) is not None
            for item in value
        )
        and len(value) == len(set(value))
    )


def _valid_file_fingerprint(value: object) -> bool:
    if not isinstance(value, dict) or set(value) != {"present", "type", "sha256"}:
        return False
    present = value["present"]
    file_type = value["type"]
    content_hash = value["sha256"]
    if not isinstance(present, bool) or file_type not in {
        "missing",
        "unreadable",
        "file",
        "symlink",
        "directory",
        "other",
    }:
        return False
    if file_type == "missing":
        return present is False and content_hash is None
    if present is not True:
        return False
    if file_type in {"file", "symlink"}:
        return content_hash is None or _valid_sha256(content_hash)
    return content_hash is None


def _valid_recovery_inputs(value: object) -> bool:
    if not isinstance(value, dict) or set(value) != {"artifact", "operations"}:
        return False
    artifact = value["artifact"]
    operations = value["operations"]
    artifact_keys = {
        "artifact_state",
        "json_exists",
        "html_exists",
        "json_sha256",
        "html_sha256",
        "expected_html_sha256",
    }
    if not isinstance(artifact, dict) or set(artifact) != artifact_keys:
        return False
    if (
        artifact["artifact_state"]
        not in {"ABSENT", "HTML_ONLY", "JSON_ONLY", "INVALID_JSON", "DRIFT", "SYNCED"}
        or not isinstance(artifact["json_exists"], bool)
        or not isinstance(artifact["html_exists"], bool)
        or not (
            artifact["json_sha256"] is None
            or _valid_sha256(artifact["json_sha256"])
        )
        or not (
            artifact["html_sha256"] is None
            or _valid_sha256(artifact["html_sha256"])
        )
        or not (
            artifact["expected_html_sha256"] is None
            or _valid_sha256(artifact["expected_html_sha256"])
        )
    ):
        return False
    if not isinstance(operations, list):
        return False
    operation_ids: list[str] = []
    for operation in operations:
        if not isinstance(operation, dict) or set(operation) != {
            "operation_id",
            "kind",
            "terminal",
            "result_state",
            "files",
        }:
            return False
        operation_id = operation["operation_id"]
        kind = operation["kind"]
        files = operation["files"]
        match = (
            HISTORY_DIRECTORY.fullmatch(operation_id)
            if isinstance(operation_id, str)
            else None
        )
        if (
            match is None
            or kind != match.group("kind")
            or not isinstance(operation["terminal"], bool)
            or operation["result_state"]
            not in {"missing", "malformed", "pending", "terminal"}
            or not isinstance(files, dict)
            or set(files)
            != {"operation.json", "result.json", "before.json", "before.html"}
            or not all(_valid_file_fingerprint(item) for item in files.values())
        ):
            return False
        operation_ids.append(operation_id)
    return len(operation_ids) == len(set(operation_ids))


def _valid_recovery_decision(value: object) -> bool:
    if not isinstance(value, dict):
        return False
    expected_keys = {
        "version",
        "action",
        "previous_operations",
        "source",
        "source_operation_id",
        "source_json_sha256",
        "expected_html_sha256",
        "retained_create",
        "input_recovery_token",
        "input_recovery_fingerprints",
    }
    if set(value) != expected_keys:
        return False
    previous = value["previous_operations"]
    common_valid = (
        value["version"] == RECOVERY_DECISION_VERSION
        and value["action"] in {"synchronize", "absent"}
        and isinstance(previous, list)
        and all(isinstance(item, str) for item in previous)
        and len(previous) == len(set(previous))
        and isinstance(value["retained_create"], bool)
        and _valid_sha256(value["input_recovery_token"])
        and _valid_recovery_inputs(value["input_recovery_fingerprints"])
        and _recovery_token_for_inputs(value["input_recovery_fingerprints"])
        == value["input_recovery_token"]
    )
    if not common_valid:
        return False
    if value["action"] == "absent":
        return (
            all(
                value[field] is None
                for field in (
                    "source_operation_id",
                    "source_json_sha256",
                    "expected_html_sha256",
                )
            )
            and value["source"] == "none"
        )
    return (
        value["source"] in {"current-json", "snapshot"}
        and isinstance(value["source_json_sha256"], str)
        and re.fullmatch(r"[0-9a-f]{64}", value["source_json_sha256"]) is not None
        and isinstance(value["expected_html_sha256"], str)
        and re.fullmatch(r"[0-9a-f]{64}", value["expected_html_sha256"]) is not None
        and (
            (value["source"] == "current-json" and value["source_operation_id"] is None)
            or (
                value["source"] == "snapshot"
                and isinstance(value["source_operation_id"], str)
            )
        )
    )


def _valid_update_target_fields(target: object, expected_title: object) -> bool:
    if not _valid_nonempty_string(target, maximum=500):
        return False
    if DOTTED_PATH.fullmatch(target) is not None:
        return _valid_nonempty_string(expected_title, maximum=500)
    return expected_title is None


def _valid_operation_metadata(value: object, *, kind: str) -> bool:
    if not isinstance(value, dict):
        return False
    if kind == "create":
        return (
            set(value) in ({"definition_path"}, {"definition_path", "definition_sha256"})
            and _valid_nonempty_string(value["definition_path"])
            and (
                "definition_sha256" not in value
                or _valid_sha256(value["definition_sha256"])
            )
        )
    if kind == "update":
        return (
            set(value)
            in (
                {"target", "mutation"},
                {"target", "expected_title", "mutation"},
            )
            and _valid_update_target_fields(
                value["target"], value.get("expected_title")
            )
            and value["mutation"] in {"completed", "add_child", "add_peer_after"}
        )
    if kind == "reconcile":
        recovery_token = value.get("recovery_token")
        return (
            set(value) == {"recovery_token", "previous_unresolved"}
            and (recovery_token is None or _valid_sha256(recovery_token))
            and _valid_operation_ids(value["previous_unresolved"])
        )
    if kind == "cleanup":
        return (
            set(value) == {"retention", "synchronized_before_cleanup"}
            and value["retention"] == "remove"
            and value["synchronized_before_cleanup"] is True
        )
    return False


def _valid_operation_record(operation: object, *, operation_id: str, kind: str) -> bool:
    if not isinstance(operation, dict):
        return False
    state = operation.get("state")
    expected_keys = {
        "schema",
        "version",
        "operation_id",
        "kind",
        "state",
        "before",
        "metadata",
    }
    if state == "prepared":
        expected_keys.add("decision")
    if set(operation) != expected_keys:
        return False
    if not (
        operation.get("schema") == OPERATION_SCHEMA
        and operation.get("version") == OPERATION_VERSION
        and operation.get("operation_id") == operation_id
        and operation.get("kind") == kind
        and _valid_operation_metadata(operation.get("metadata"), kind=kind)
        and _valid_evidence(operation.get("before"))
    ):
        return False
    if state == "pending":
        return True
    if not (
        kind == "reconcile"
        and state == "prepared"
        and _valid_recovery_decision(operation.get("decision"))
    ):
        return False
    metadata = operation["metadata"]
    decision = operation["decision"]
    recovery_token = metadata["recovery_token"]
    return (
        metadata["previous_unresolved"] == decision["previous_operations"]
        and (
            recovery_token is None
            or recovery_token == decision["input_recovery_token"]
        )
    )


def _valid_result_record(
    result: object,
    *,
    operation_id: str,
    kind: str,
    operation: dict[str, object],
) -> tuple[bool, bool]:
    if not isinstance(result, dict):
        return False, False
    outcome = result.get("outcome")
    terminal = result.get("terminal")
    if not (
        result.get("schema_version") == RESULT_SCHEMA_VERSION
        and isinstance(outcome, str)
        and outcome
        and result.get("operation_id") == operation_id
        and isinstance(terminal, bool)
    ):
        return False, False

    pending_outcome = f"PENDING_{kind.upper()}"
    uncertain_outcome = (
        "UNCERTAIN_RECONCILIATION"
        if kind == "reconcile"
        else f"UNCERTAIN_{kind.upper()}"
    )
    base_fields = {"schema_version", "outcome", "operation_id", "terminal"}
    operation_state = operation["state"]
    metadata = operation["metadata"]
    if not isinstance(metadata, dict):
        return False, False
    if outcome == pending_outcome:
        valid = (
            set(result) == base_fields | {"history_path", "before", "retry_allowed"}
            and terminal is False
            and _valid_nonempty_string(result.get("history_path"))
            and _valid_evidence(result.get("before"))
            and result.get("before") == operation["before"]
            and result.get("retry_allowed") is False
        )
        return valid, False
    if outcome == uncertain_outcome:
        uncertain_fields = {
            "create": {"definition_path"},
            "update": {"mutation", "target", "expected_title", "before"},
            "reconcile": {"reconciles"},
            "cleanup": {"retention", "evidence_before_cleanup"},
        }
        valid = (
            set(result)
            == (
                base_fields
                | {
                    "history_path",
                    "current",
                    "error",
                    "inspect_required",
                    "recovery_required",
                    "retry_allowed",
                }
                | uncertain_fields[kind]
            )
            and terminal is False
            and _valid_nonempty_string(result.get("history_path"))
            and _valid_evidence(result.get("current"))
            and isinstance(result.get("error"), str)
            and result.get("inspect_required") is True
            and result.get("recovery_required") is True
            and result.get("retry_allowed") is False
            and (
                kind != "update"
                or (
                    result.get("mutation") == metadata["mutation"]
                    and result.get("target") == metadata["target"]
                    and result.get("expected_title") == metadata.get("expected_title")
                    and _valid_evidence(result.get("before"))
                    and result.get("before") == operation["before"]
                )
            )
            and (
                kind != "reconcile"
                or (
                    result.get("reconciles") == metadata["previous_unresolved"]
                )
            )
            and (
                kind != "cleanup"
                or (
                    result.get("retention") == "remove"
                    and _valid_evidence(result.get("evidence_before_cleanup"))
                    and result.get("evidence_before_cleanup")
                    == operation["before"]
                )
            )
            and (
                kind != "create"
                or result.get("definition_path") == metadata["definition_path"]
            )
        )
        return valid, False
    if terminal is not True or outcome not in TERMINAL_OPERATION_OUTCOMES[kind]:
        return False, False
    if kind == "reconcile":
        if outcome in {"RECONCILED", "RECOVERED_ABSENT", "RECOVERY_REJECTED"}:
            if operation_state != "prepared":
                return False, False
    elif operation_state != "pending":
        return False, False

    terminal_fields = {
        "CREATED": {
            "history_path",
            "package_version",
            "definition_path",
            "task_plan_root",
            "history_policy",
            "plan_path",
            "html_path",
            "after",
            "synchronized",
        },
        "UPDATED": {
            "history_path",
            "mutation",
            "target",
            "expected_title",
            "before",
            "after",
            "synchronized",
        },
        "RECONCILED": {
            "history_path",
            "authoritative_source",
            "before",
            "after",
            "synchronized",
            "reconciles",
            "retained_create",
        },
        "RECOVERED_ABSENT": {
            "history_path",
            "before",
            "after",
            "removed",
            "reconciles",
            "retryable_create",
        },
        "CLEANED": {
            "history_path",
            "retention",
            "synchronized_before_cleanup",
            "evidence_before_cleanup",
            "evidence_after_cleanup",
            "removed",
            "provider_state_changed",
            "retryable_create",
        },
        "RECOVERED_OPERATION": {"recovered_by", "resolution", "after"},
        "RECOVERY_REJECTED": {
            "history_path",
            "reason",
            "expected_recovery_token",
            "observed_recovery_token",
        },
    }
    if set(result) != base_fields | terminal_fields[outcome]:
        return False, False

    valid_terminal = False
    if outcome == "CREATED":
        valid_terminal = (
            _valid_nonempty_string(result.get("history_path"))
            and _valid_nonempty_string(result.get("package_version"))
            and result.get("definition_path") == metadata["definition_path"]
            and _valid_nonempty_string(result.get("task_plan_root"))
            and result.get("history_policy")
            == {
                "kind": "operational",
                "maximum_settled_snapshots": HISTORY_LIMIT,
            }
            and _valid_nonempty_string(result.get("plan_path"))
            and _valid_nonempty_string(result.get("html_path"))
            and _valid_evidence(result.get("after"))
            and result.get("synchronized") is True
        )
    elif outcome == "UPDATED":
        valid_terminal = (
            _valid_nonempty_string(result.get("history_path"))
            and _valid_evidence(result.get("before"))
            and result.get("before") == operation["before"]
            and _valid_evidence(result.get("after"))
            and result.get("synchronized") is True
            and result.get("mutation") == metadata["mutation"]
            and result.get("target") == metadata["target"]
            and result.get("expected_title") == metadata.get("expected_title")
        )
    elif outcome == "RECONCILED":
        decision = operation.get("decision")
        valid_terminal = (
            isinstance(decision, dict)
            and _valid_nonempty_string(result.get("history_path"))
            and _valid_evidence(result.get("before"))
            and result.get("before") == operation["before"]
            and _valid_evidence(result.get("after"))
            and result.get("synchronized") is True
            and result.get("reconciles") == decision.get("previous_operations")
            and result.get("authoritative_source") == "json"
            and result.get("retained_create") == decision.get("retained_create")
            and decision.get("action") == "synchronize"
        )
    elif outcome == "RECOVERED_ABSENT":
        decision = operation.get("decision")
        valid_terminal = (
            isinstance(decision, dict)
            and _valid_nonempty_string(result.get("history_path"))
            and _valid_evidence(result.get("before"))
            and result.get("before") == operation["before"]
            and _valid_evidence(result.get("after"))
            and result.get("reconciles") == decision.get("previous_operations")
            and isinstance(result.get("removed"), list)
            and all(_valid_nonempty_string(item) for item in result["removed"])
            and len(result["removed"]) == len(set(result["removed"]))
            and result.get("retryable_create") is True
            and decision.get("action") == "absent"
        )
    elif outcome == "CLEANED":
        valid_terminal = (
            _valid_nonempty_string(result.get("history_path"))
            and _valid_evidence(result.get("evidence_before_cleanup"))
            and result.get("evidence_before_cleanup") == operation["before"]
            and _valid_evidence(result.get("evidence_after_cleanup"))
            and result.get("retention") == metadata["retention"]
            and result.get("synchronized_before_cleanup")
            is metadata["synchronized_before_cleanup"]
            and isinstance(result.get("removed"), list)
            and all(_valid_nonempty_string(item) for item in result["removed"])
            and len(result["removed"]) == len(set(result["removed"]))
            and result.get("provider_state_changed") is False
            and result.get("retryable_create") is True
        )
    elif outcome == "RECOVERED_OPERATION":
        recovered_by = result.get("recovered_by")
        recovered_match = (
            HISTORY_DIRECTORY.fullmatch(recovered_by)
            if isinstance(recovered_by, str)
            else None
        )
        valid_terminal = (
            recovered_match is not None
            and recovered_match.group("kind") == "reconcile"
            and result.get("resolution") in {"synchronized", "absent"}
            and _valid_evidence(result.get("after"))
        )
    elif outcome == "RECOVERY_REJECTED":
        decision = operation.get("decision")
        valid_terminal = (
            isinstance(decision, dict)
            and _valid_nonempty_string(result.get("history_path"))
            and result.get("reason") == "stale-recovery-token"
            and result.get("expected_recovery_token")
            == decision.get("input_recovery_token")
            and _valid_sha256(result.get("observed_recovery_token"))
        )
    return valid_terminal, valid_terminal


def _operation_status(directory: Path) -> _OperationStatus:
    match = HISTORY_DIRECTORY.fullmatch(directory.name)
    if match is None:
        raise _PlanHelperError(
            "INVALID_HISTORY",
            "The operational plan history contains an invalid operation directory.",
            exit_code=4,
            path=str(directory),
        )
    operation_id = directory.name
    kind = match.group("kind")
    operation_state, operation = _soft_json(directory / "operation.json")
    result_state, result = _soft_json(directory / "result.json")
    operation_valid = operation_state == "present" and _valid_operation_record(
        operation, operation_id=operation_id, kind=kind
    )
    if not operation_valid:
        result_state = "malformed" if operation_state == "present" else operation_state
        terminal = False
    elif result_state == "present":
        valid_result, terminal = _valid_result_record(
            result,
            operation_id=operation_id,
            kind=kind,
            operation=operation,
        )
        result_state = (
            "terminal" if terminal else "pending" if valid_result else "malformed"
        )
    else:
        terminal = False
    return _OperationStatus(
        operation_id=operation_id,
        kind=kind,
        path=directory,
        terminal=terminal,
        result_state=result_state,
        result=result,
        operation_state=operation_state,
        operation=operation,
    )


def _operation_statuses(context: _PlanContext) -> list[_OperationStatus]:
    return [_operation_status(directory) for directory in _history_directories(context)]


def _unresolved_operations(
    context: _PlanContext, *, exclude: frozenset[str] = frozenset()
) -> list[_OperationStatus]:
    return [
        status
        for status in _operation_statuses(context)
        if not status.terminal and status.operation_id not in exclude
    ]


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
    statuses = _operation_statuses(context)
    for status in statuses:
        if status.terminal:
            _remove_tree(status.path, context.history_root)
            if len(_history_directories(context)) < HISTORY_LIMIT:
                return
    unresolved = [status.operation_id for status in statuses if not status.terminal]
    raise _PlanHelperError(
        "HISTORY_LIMIT_REACHED",
        "Twenty unresolved operational snapshots are retained; reconcile them before another mutation.",
        exit_code=4,
        unresolved_operations=unresolved,
    )


def _write_json_atomic(target: Path, payload: dict[str, object]) -> None:
    temporary = target.with_name(
        f".{target.name}.{os.getpid()}.{time.monotonic_ns()}.tmp"
    )
    encoded = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")
    try:
        descriptor = os.open(temporary, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        with os.fdopen(descriptor, "wb") as output:
            output.write(encoded)
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary, target)
    finally:
        if _lexists(temporary) and temporary.is_file() and not temporary.is_symlink():
            temporary.unlink()


def _write_operation_result(
    operation_path: Path, result: dict[str, object], *, terminal: bool
) -> dict[str, object]:
    stored = {**result, "terminal": terminal}
    _write_json_atomic(operation_path / "result.json", stored)
    return stored


def _prepare_recovery_operation(
    operation_path: Path, decision: dict[str, object]
) -> dict[str, object]:
    operation_path_json = operation_path / "operation.json"
    operation = _read_json(
        operation_path_json,
        "INVALID_HISTORY",
        "The pending reconciliation operation record is invalid.",
    )
    operation["state"] = "prepared"
    operation["decision"] = decision
    _write_json_atomic(operation_path_json, operation)
    return operation


def _start_operation(
    context: _PlanContext, kind: str, metadata: dict[str, object]
) -> tuple[str, Path]:
    _make_safe_directory(context.workspace, context.history_root)
    existing = _history_directories(context)
    sequence = 1
    if existing:
        match = HISTORY_DIRECTORY.fullmatch(existing[-1].name)
        if match is not None:
            sequence = int(match.group("sequence")) + 1
    _prune_history(context)
    operation_id = f"{sequence:06d}-{kind}"
    operation_path = context.history_root / operation_id
    operation_path.mkdir()
    before = _evidence(context)
    operation_record = {
        "schema": OPERATION_SCHEMA,
        "version": OPERATION_VERSION,
        "operation_id": operation_id,
        "kind": kind,
        "state": "pending",
        "before": before,
        "metadata": metadata,
    }
    _write_json_atomic(operation_path / "operation.json", operation_record)
    if bool(before["json_exists"]):
        (operation_path / "before.json").write_bytes(context.plan_path.read_bytes())
    if bool(before["html_exists"]):
        (operation_path / "before.html").write_bytes(context.html_path.read_bytes())
    _write_operation_result(
        operation_path,
        _result(
            f"PENDING_{kind.upper()}",
            operation_id=operation_id,
            history_path=str(operation_path),
            before=before,
            retry_allowed=False,
        ),
        terminal=False,
    )
    return operation_id, operation_path


def _record_uncertain(
    operation_path: Path,
    outcome: str,
    operation_id: str,
    context: _PlanContext,
    error: Exception,
    **details: object,
) -> dict[str, object]:
    result = _result(
        outcome,
        operation_id=operation_id,
        history_path=str(operation_path),
        current=_evidence(context),
        error=str(error),
        inspect_required=True,
        recovery_required=True,
        retry_allowed=False,
        **details,
    )
    try:
        return _write_operation_result(operation_path, result, terminal=False)
    except OSError:
        return {**result, "terminal": False}


def _create(
    context: _PlanContext, arguments: argparse.Namespace, api: _PlanApi
) -> dict[str, object]:
    definition = _load_definition(arguments.definition, context)
    _reject_symlink_components(context.workspace, context.plan_path)
    unresolved = _unresolved_operations(context)
    if unresolved:
        inspected = _inspect(context, api)
        raise _PlanHelperError(
            "RECONCILIATION_REQUIRED",
            "Create cannot start while a prior operation is unresolved.",
            exit_code=4,
            inspect=inspected,
            unresolved_operations=[status.operation_id for status in unresolved],
        )
    if _lexists(context.plan_path) or _lexists(context.html_path):
        raise _PlanHelperError(
            "PLAN_ALREADY_EXISTS",
            "Create refuses to overwrite an existing canonical plan or sibling HTML file.",
            plan_path=str(context.plan_path),
            html_path=str(context.html_path),
        )
    _make_safe_directory(context.workspace, context.task_root)
    hierarchy, completed_paths = _definition_hierarchy(definition)
    operation_id, operation_path = _start_operation(
        context,
        "create",
        {
            "definition_path": str(definition["path"]),
            "definition_sha256": _sha256(definition["path"]),
        },
    )
    try:
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
        inspected = _inspect(context, api, exclude_operations=frozenset({operation_id}))
        if inspected["outcome"] != "SYNCED":
            raise RuntimeError(
                "created JSON and HTML plan artifacts are not synchronized"
            )
    except Exception as error:
        return _record_uncertain(
            operation_path,
            "UNCERTAIN_CREATE",
            operation_id,
            context,
            error,
            definition_path=str(definition["path"]),
        )
    result = _result(
        "CREATED",
        operation_id=operation_id,
        history_path=str(operation_path),
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
    try:
        return _write_operation_result(operation_path, result, terminal=True)
    except OSError as error:
        return _record_uncertain(
            operation_path,
            "UNCERTAIN_CREATE",
            operation_id,
            context,
            error,
            definition_path=str(definition["path"]),
        )


def _update(
    context: _PlanContext, arguments: argparse.Namespace, api: _PlanApi
) -> dict[str, object]:
    inspected = _inspect(context, api)
    if inspected["outcome"] != "SYNCED":
        raise _PlanHelperError(
            "RECONCILIATION_REQUIRED",
            "Update requires synchronized artifacts and no unresolved operation.",
            exit_code=4,
            unresolved_operations=inspected["unresolved_operations"],
            inspect=inspected,
        )
    document = _load_plan(context)
    _validate_target(document, arguments.target, arguments.expected_title)
    mutation: dict[str, object]
    if arguments.complete:
        mutation = {"completed": True}
    elif arguments.incomplete:
        mutation = {"completed": False}
    elif arguments.add_child is not None:
        mutation = {"add_child": _action_text(arguments.add_child, "add-child")}
    elif arguments.add_peer_after is not None:
        mutation = {
            "add_peer_after": _action_text(arguments.add_peer_after, "add-peer-after")
        }
    else:
        raise _PlanHelperError(
            "INVALID_REQUEST", "Update requires exactly one supported mutation."
        )

    before = _evidence(context)
    operation_id, operation_path = _start_operation(
        context,
        "update",
        {
            "target": arguments.target,
            "expected_title": arguments.expected_title,
            "mutation": next(iter(mutation)),
        },
    )
    try:
        api.update_hierarchy_plan(context.plan_path, arguments.target, **mutation)
        after_inspection = _inspect(
            context, api, exclude_operations=frozenset({operation_id})
        )
        if after_inspection["outcome"] != "SYNCED":
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
            expected_title=arguments.expected_title,
            before=before,
            after=after,
            synchronized=True,
        )
        return _write_operation_result(operation_path, result, terminal=True)
    except Exception as error:
        return _record_uncertain(
            operation_path,
            "UNCERTAIN_UPDATE",
            operation_id,
            context,
            error,
            mutation=next(iter(mutation)),
            target=arguments.target,
            expected_title=arguments.expected_title,
            before=before,
        )


def _settle_operations(
    statuses: Sequence[_OperationStatus],
    *,
    recovered_by: str,
    resolution: str,
    evidence: dict[str, object],
) -> None:
    for status in statuses:
        if status.terminal:
            continue
        if not _valid_operation_record(
            status.operation,
            operation_id=status.operation_id,
            kind=status.kind,
        ):
            raise _PlanHelperError(
                "RECOVERY_BLOCKED",
                "Recovery cannot settle an operation with invalid metadata.",
                exit_code=4,
                invalid_operation=status.operation_id,
            )
        _write_operation_result(
            status.path,
            _result(
                "RECOVERED_OPERATION",
                operation_id=status.operation_id,
                recovered_by=recovered_by,
                resolution=resolution,
                after=evidence,
            ),
            terminal=True,
        )


def _latest_before_snapshot(
    context: _PlanContext, statuses: Sequence[_OperationStatus]
) -> tuple[_OperationStatus, _PlanDocument, str]:
    for status in reversed(statuses):
        snapshot = status.path / "before.json"
        if snapshot.is_symlink() or not snapshot.is_file():
            continue
        try:
            payload = json.loads(snapshot.read_text(encoding="utf-8"))
            if not isinstance(payload, dict):
                continue
            document = _plan_document_from_payload(payload, context)
        except (OSError, UnicodeError, json.JSONDecodeError, _PlanHelperError):
            continue
        snapshot_hash = _sha256(snapshot)
        if snapshot_hash is not None:
            return status, document, snapshot_hash
    raise _PlanHelperError(
        "RECOVERY_BLOCKED",
        "No valid pre-operation JSON snapshot can restore plan authority.",
        exit_code=4,
        unresolved_operations=[status.operation_id for status in statuses],
    )


def _rendered_document_hash(
    context: _PlanContext, document: _PlanDocument, api: _PlanApi
) -> str:
    rendered = _render_document(context, document, api, write=False)
    if not isinstance(rendered, str):
        raise _PlanHelperError(
            "CAPABILITY_UNAVAILABLE",
            "render_hierarchy_html did not return HTML for recovery validation.",
            exit_code=3,
        )
    return hashlib.sha256(rendered.encode("utf-8")).hexdigest()


def _build_recovery_decision(
    context: _PlanContext,
    api: _PlanApi,
    previous: Sequence[_OperationStatus],
    *,
    input_recovery_token: str,
) -> dict[str, object]:
    invalid_operations = [
        status.operation_id
        for status in previous
        if not _valid_operation_record(
            status.operation,
            operation_id=status.operation_id,
            kind=status.kind,
        )
    ]
    if invalid_operations:
        raise _PlanHelperError(
            "RECOVERY_BLOCKED",
            "Recovery requires valid kind-specific operation metadata.",
            exit_code=4,
            invalid_operations=invalid_operations,
        )
    input_fingerprints = _current_recovery_inputs(context, api)
    observed_input_token = _recovery_token_for_inputs(input_fingerprints)
    if observed_input_token != input_recovery_token:
        raise _PlanHelperError(
            "STALE_RECOVERY_TOKEN",
            "Recovery inputs changed before the decision could be prepared.",
            exit_code=4,
            expected_recovery_token=input_recovery_token,
            observed_recovery_token=observed_input_token,
        )
    previous_ids = [status.operation_id for status in previous]
    has_pending_create = any(status.kind == "create" for status in previous)
    cleanup_operations = [
        status.operation_id for status in previous if status.kind == "cleanup"
    ]
    if cleanup_operations:
        raise _PlanHelperError(
            "RECOVERY_BLOCKED",
            "Cleanup is never resumed automatically; run finalize with retention remove again for the current exact plan paths.",
            exit_code=4,
            cleanup_operations=cleanup_operations,
        )

    artifact = _analyze_artifacts(context, api)
    document = artifact.get("document")
    if has_pending_create and not isinstance(document, _PlanDocument):
        return {
            "version": RECOVERY_DECISION_VERSION,
            "action": "absent",
            "previous_operations": previous_ids,
            "source": "none",
            "source_operation_id": None,
            "source_json_sha256": None,
            "expected_html_sha256": None,
            "retained_create": False,
            "input_recovery_token": input_recovery_token,
            "input_recovery_fingerprints": input_fingerprints,
        }

    source = "current-json"
    source_operation_id: str | None = None
    source_hash = artifact.get("json_sha256")
    expected_html_hash = artifact.get("expected_html_sha256")
    if not isinstance(document, _PlanDocument):
        source_status, document, source_hash = _latest_before_snapshot(
            context, previous
        )
        source = "snapshot"
        source_operation_id = source_status.operation_id
        expected_html_hash = _rendered_document_hash(context, document, api)
    if not isinstance(source_hash, str) or not isinstance(expected_html_hash, str):
        raise _PlanHelperError(
            "RECOVERY_BLOCKED",
            "Recovery could not bind a valid JSON source and rendered HTML expectation.",
            exit_code=4,
            unresolved_operations=previous_ids,
        )
    return {
        "version": RECOVERY_DECISION_VERSION,
        "action": "synchronize",
        "previous_operations": previous_ids,
        "source": source,
        "source_operation_id": source_operation_id,
        "source_json_sha256": source_hash,
        "expected_html_sha256": expected_html_hash,
        "retained_create": has_pending_create,
        "input_recovery_token": input_recovery_token,
        "input_recovery_fingerprints": input_fingerprints,
    }


def _cleanup_artifacts(context: _PlanContext) -> list[str]:
    removed: list[str] = []
    for path in (context.html_path, context.plan_path):
        _safe_file(path, context, required=False)
        if path.is_file():
            path.unlink()
            removed.append(str(path))
    return removed


def _purge_plan_history(context: _PlanContext) -> None:
    if context.history_root.exists():
        _validate_cleanup_tree(context.history_root, context.task_root)
        _remove_tree(context.history_root, context.task_root)
    history_parent = context.task_root / ".history"
    if history_parent.is_dir() and not any(history_parent.iterdir()):
        history_parent.rmdir()
    if context.task_root.is_dir() and not any(context.task_root.iterdir()):
        context.task_root.rmdir()


def _prepared_reconciliation(
    statuses: Sequence[_OperationStatus],
) -> _OperationStatus | None:
    prepared = [
        status
        for status in statuses
        if not status.terminal
        and status.kind == "reconcile"
        and isinstance(status.operation, dict)
        and status.operation.get("state") == "prepared"
        and _valid_operation_record(
            status.operation,
            operation_id=status.operation_id,
            kind=status.kind,
        )
    ]
    if len(prepared) > 1:
        raise _PlanHelperError(
            "RECOVERY_BLOCKED",
            "More than one prepared reconciliation decision is unresolved.",
            exit_code=4,
            prepared_operations=[status.operation_id for status in prepared],
        )
    return prepared[0] if prepared else None


def _decision_previous_statuses(
    context: _PlanContext, decision: dict[str, object]
) -> list[_OperationStatus]:
    statuses = {status.operation_id: status for status in _operation_statuses(context)}
    previous_ids = decision["previous_operations"]
    if not isinstance(previous_ids, list):
        raise _PlanHelperError(
            "RECOVERY_BLOCKED",
            "The prepared reconciliation decision has invalid prior operations.",
            exit_code=4,
        )
    missing = [
        operation_id for operation_id in previous_ids if operation_id not in statuses
    ]
    if missing:
        raise _PlanHelperError(
            "RECOVERY_BLOCKED",
            "A journal entry bound to the prepared recovery decision is missing.",
            exit_code=4,
            missing_operations=missing,
        )
    return [statuses[operation_id] for operation_id in previous_ids]


def _reject_prepared_recovery(
    operation: _OperationStatus,
    *,
    expected_token: str,
    observed_token: str,
) -> None:
    _write_operation_result(
        operation.path,
        _result(
            "RECOVERY_REJECTED",
            operation_id=operation.operation_id,
            history_path=str(operation.path),
            reason="stale-recovery-token",
            expected_recovery_token=expected_token,
            observed_recovery_token=observed_token,
        ),
        terminal=True,
    )


def _execute_recovery_decision(
    context: _PlanContext,
    api: _PlanApi,
    operation: _OperationStatus,
    decision: dict[str, object],
) -> dict[str, object]:
    previous = _decision_previous_statuses(context, decision)
    previous_ids = [status.operation_id for status in previous]
    before = (
        operation.operation.get("before")
        if isinstance(operation.operation, dict)
        else None
    )
    if not _valid_evidence(before):
        raise _PlanHelperError(
            "RECOVERY_BLOCKED",
            "The prepared reconciliation has no valid before evidence.",
            exit_code=4,
        )

    if decision["action"] == "absent":
        removed = _cleanup_artifacts(context)
        artifact = _analyze_artifacts(context, api)
        if artifact["artifact_state"] != "ABSENT":
            raise RuntimeError("recovery did not reach complete absence")
        after = _evidence(context)
        _settle_operations(
            previous,
            recovered_by=operation.operation_id,
            resolution="absent",
            evidence=after,
        )
        stored = _write_operation_result(
            operation.path,
            _result(
                "RECOVERED_ABSENT",
                operation_id=operation.operation_id,
                history_path=str(operation.path),
                before=before,
                after=after,
                removed=removed,
                reconciles=previous_ids,
                retryable_create=True,
            ),
            terminal=True,
        )
        _purge_plan_history(context)
        return stored

    source_hash = str(decision["source_json_sha256"])
    source_path = context.plan_path
    if decision["source"] == "snapshot":
        source_operation_id = str(decision["source_operation_id"])
        source_status = next(
            status for status in previous if status.operation_id == source_operation_id
        )
        source_path = source_status.path / "before.json"
    if _sha256(source_path) != source_hash:
        raise _PlanHelperError(
            "STALE_RECOVERY_TOKEN",
            "The JSON source bound to the prepared recovery decision changed.",
            exit_code=4,
            source_path=str(source_path),
        )
    payload = _read_json(
        source_path,
        "RECOVERY_BLOCKED",
        "The JSON source bound to the prepared recovery decision is invalid.",
    )
    document = _plan_document_from_payload(payload, context)
    rendered_hash = _rendered_document_hash(context, document, api)
    if rendered_hash != decision["expected_html_sha256"]:
        raise _PlanHelperError(
            "STALE_RECOVERY_TOKEN",
            "The rendered-output expectation bound to recovery changed.",
            exit_code=4,
            expected_html_sha256=decision["expected_html_sha256"],
            observed_html_sha256=rendered_hash,
        )

    artifact = _analyze_artifacts(context, api)
    already_synchronized = (
        artifact["artifact_state"] == "SYNCED"
        and artifact["json_sha256"] == source_hash
        and artifact["expected_html_sha256"] == decision["expected_html_sha256"]
    )
    if not already_synchronized:
        if source_path != context.plan_path:
            _safe_file(context.plan_path, context, required=False)
            context.plan_path.write_bytes(source_path.read_bytes())
        _render_document(context, document, api, write=True)
    after_artifact = _analyze_artifacts(context, api)
    if (
        after_artifact["artifact_state"] != "SYNCED"
        or after_artifact["json_sha256"] != source_hash
        or after_artifact["expected_html_sha256"] != decision["expected_html_sha256"]
    ):
        raise RuntimeError("reconciliation did not synchronize the plan artifacts")
    after = _evidence(context)
    _settle_operations(
        previous,
        recovered_by=operation.operation_id,
        resolution="synchronized",
        evidence=after,
    )
    return _write_operation_result(
        operation.path,
        _result(
            "RECONCILED",
            operation_id=operation.operation_id,
            history_path=str(operation.path),
            authoritative_source="json",
            before=before,
            after=after,
            synchronized=True,
            reconciles=previous_ids,
            retained_create=bool(decision["retained_create"]),
        ),
        terminal=True,
    )


def _reconcile(
    context: _PlanContext, arguments: argparse.Namespace, api: _PlanApi
) -> dict[str, object]:
    inspected = _inspect(context, api)
    unresolved_ids = list(inspected["unresolved_operations"])
    supplied_token = arguments.recovery_token
    observed_token = inspected["recovery_token"]
    if unresolved_ids and supplied_token != observed_token:
        raise _PlanHelperError(
            "STALE_RECOVERY_TOKEN",
            "Reconciliation requires the recovery token from the current inspect result.",
            exit_code=4,
            unresolved_operations=unresolved_ids,
            expected_recovery_token=observed_token,
        )
    if supplied_token is not None and supplied_token != observed_token:
        raise _PlanHelperError(
            "STALE_RECOVERY_TOKEN",
            "The supplied recovery token does not match the current artifacts and operations.",
            exit_code=4,
            expected_recovery_token=observed_token,
        )
    statuses = _operation_statuses(context)
    prepared = _prepared_reconciliation(statuses)
    if not unresolved_ids and inspected["outcome"] == "SYNCED":
        return _result(
            "ALREADY_SYNCED",
            **{key: value for key, value in inspected.items() if key != "outcome"},
        )
    if not unresolved_ids and inspected["outcome"] == "ABSENT":
        return _result(
            "ALREADY_ABSENT",
            **{key: value for key, value in inspected.items() if key != "outcome"},
        )
    if not unresolved_ids and inspected["outcome"] == "ORPHANED_HTML":
        raise _PlanHelperError(
            "RECOVERY_BLOCKED",
            "HTML without authoritative JSON can be removed only as recovery for a pending create or cleanup.",
            exit_code=4,
            inspect=inspected,
        )

    operation: _OperationStatus
    if prepared is None:
        previous = [status for status in statuses if not status.terminal]
        decision = _build_recovery_decision(
            context,
            api,
            previous,
            input_recovery_token=str(observed_token),
        )
        operation_id, operation_path = _start_operation(
            context,
            "reconcile",
            {
                "recovery_token": supplied_token,
                "previous_unresolved": unresolved_ids,
            },
        )
        _prepare_recovery_operation(operation_path, decision)
        operation = _operation_status(operation_path)
        after_prepare_token = _current_recovery_token(
            context, api, exclude_operations=frozenset({operation_id})
        )
        if after_prepare_token != observed_token:
            _reject_prepared_recovery(
                operation,
                expected_token=str(observed_token),
                observed_token=after_prepare_token,
            )
            raise _PlanHelperError(
                "STALE_RECOVERY_TOKEN",
                "Recovery inputs changed after the decision was prepared and before any canonical effect.",
                exit_code=4,
                expected_recovery_token=observed_token,
                observed_recovery_token=after_prepare_token,
            )
    else:
        operation = prepared
        decision_value = operation.operation.get("decision")
        if not isinstance(decision_value, dict):
            raise _PlanHelperError(
                "RECOVERY_BLOCKED",
                "The prepared reconciliation decision is invalid.",
                exit_code=4,
            )
        decision = decision_value
        resume_token = _current_recovery_token(context, api)
        if resume_token != observed_token:
            _reject_prepared_recovery(
                operation,
                expected_token=str(observed_token),
                observed_token=resume_token,
            )
            raise _PlanHelperError(
                "STALE_RECOVERY_TOKEN",
                "Recovery inputs changed before the prepared decision could resume.",
                exit_code=4,
                expected_recovery_token=observed_token,
                observed_recovery_token=resume_token,
            )

    try:
        return _execute_recovery_decision(context, api, operation, decision)
    except _PlanHelperError as error:
        if error.outcome == "STALE_RECOVERY_TOKEN":
            _reject_prepared_recovery(
                operation,
                expected_token=str(observed_token),
                observed_token=_current_recovery_token(context, api),
            )
        raise
    except Exception as error:
        return _record_uncertain(
            operation.path,
            "UNCERTAIN_RECONCILIATION",
            operation.operation_id,
            context,
            error,
            reconciles=decision["previous_operations"],
        )


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


def _finalize(
    context: _PlanContext, arguments: argparse.Namespace, api: _PlanApi
) -> dict[str, object]:
    if arguments.retention == "keep":
        inspected = _inspect(context, api)
        if inspected["outcome"] != "SYNCED":
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
        return _result(
            "FINALIZED",
            retention="keep",
            synchronized=True,
            authoritative_source="json",
            evidence=_evidence(context),
            history_policy={
                "kind": "operational",
                "maximum_settled_snapshots": HISTORY_LIMIT,
            },
        )

    # Removal is an explicit, immediate operation on the current task-owned paths.
    # It does not persist a cleanup decision, recovery token, or resumable operation.
    selected = [context.plan_path, context.html_path, context.history_root]
    removed: list[str] = []
    try:
        removed.extend(_cleanup_artifacts(context))
        if context.history_root.exists():
            removed.append(str(context.history_root))
        _purge_plan_history(context)
        remaining = [str(path) for path in selected if _lexists(path)]
        if remaining:
            raise OSError("selected plan paths remain after deletion")
        return _result(
            "CLEANED",
            retention="remove",
            removed=removed,
            provider_state_changed=False,
            retryable_create=True,
        )
    except Exception as error:
        return _result(
            "CLEANUP_FAILED",
            retention="remove",
            error=str(error),
            remaining=[str(path) for path in selected if _lexists(path)],
            retry_allowed=True,
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
    update.add_argument("--expected-title")
    mutations = update.add_mutually_exclusive_group(required=True)
    mutations.add_argument("--complete", action="store_true")
    mutations.add_argument("--incomplete", action="store_true")
    mutations.add_argument("--add-child")
    mutations.add_argument("--add-peer-after")

    subparsers.add_parser("inspect")
    reconcile = subparsers.add_parser("reconcile")
    reconcile.add_argument("--recovery-token")

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
        with _plan_lock(context):
            if arguments.command == "create":
                result = _create(context, arguments, api)
                return (4 if result["outcome"] == "UNCERTAIN_CREATE" else 0), result
            if arguments.command == "inspect":
                inspected = _inspect(context, api)
                return (
                    0 if inspected["outcome"] in {"SYNCED", "ABSENT"} else 4
                ), inspected
            if arguments.command == "update":
                result = _update(context, arguments, api)
                return (4 if result["outcome"] == "UNCERTAIN_UPDATE" else 0), result
            if arguments.command == "reconcile":
                result = _reconcile(context, arguments, api)
                return (
                    4 if result["outcome"] == "UNCERTAIN_RECONCILIATION" else 0
                ), result
            if arguments.command == "finalize":
                result = _finalize(context, arguments, api)
                return (4 if result["outcome"] == "CLEANUP_FAILED" else 0), result
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
