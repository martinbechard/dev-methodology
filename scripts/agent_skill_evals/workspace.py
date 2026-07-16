# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Prepares content-addressed fixtures and disposable copy-on-write evaluation workspaces.

from __future__ import annotations

import hashlib
import json
import os
import platform
import shutil
import stat
import subprocess
import time
import uuid
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Callable, Iterator, Mapping, Sequence

from .commands import CommandResult, CommandSpec, command_spec, run_command


TRANSIENT_TREE_NAMES = frozenset({
    ".git",
    ".cache",
    ".eval-cache",
    ".eval-runs",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    "runs",
    "target",
})
DEPENDENCY_INPUT_NAMES = frozenset({
    "Cargo.lock",
    "Cargo.toml",
    "build.gradle",
    "build.gradle.kts",
    "composer.json",
    "composer.lock",
    "go.mod",
    "go.sum",
    "gradle.lockfile",
    "package-lock.json",
    "package.json",
    "pnpm-lock.yaml",
    "pom.xml",
    "poetry.lock",
    "pyproject.toml",
    "requirements.txt",
    "uv.lock",
    "yarn.lock",
})


@dataclass(frozen=True)
class PreparedFixture:
    """Describe one immutable-by-contract prepared fixture cache entry."""

    key: str
    path: Path
    source_digest: str
    dependency_digest: str
    toolchain_digest: str
    preparation_environment_digest: str
    platform_identity: Mapping[str, str]
    cache_hit: bool


@dataclass(frozen=True)
class RunWorkspace:
    """Describe a disposable workspace cloned from a prepared fixture."""

    path: Path
    prepared_key: str
    preparation: str


@dataclass(frozen=True)
class FunctionalIsolationAudit:
    """Report whether observed file mutations stayed inside the functional boundary."""

    status: str
    changed_paths: tuple[str, ...]
    before_digest: str
    after_digest: str


class PreparedWorkspaceManager:
    """Own prepared-fixture caching and deterministic cleanup of per-run workspaces.

    Preparation commands run only while populating a new content-addressed cache entry. Creating
    one or more run workspaces from that entry never reruns dependency installation.
    """

    def __init__(
        self,
        cache_root: Path,
        runs_root: Path,
        command_runner: Callable[[CommandSpec, Path], CommandResult] = run_command,
        lock_timeout_seconds: float = 3600.0,
        integrity_mode: str = "source",
    ) -> None:
        self.cache_root = cache_root.resolve()
        self.runs_root = runs_root.resolve()
        self._command_runner = command_runner
        self._lock_timeout_seconds = lock_timeout_seconds
        if integrity_mode not in {"source", "full"}:
            raise ValueError("prepared integrity mode must be source or full")
        self._integrity_mode = integrity_mode

    def prepare(
        self,
        fixture_root: Path,
        toolchain: Mapping[str, str],
        prepare_command: object | None = None,
    ) -> PreparedFixture:
        """Return a cached prepared fixture, populating it once on a cache miss.

        The prepare command may download or install dependencies into the prepared snapshot. It is
        intentionally absent from the workspace creation path.
        """

        fixture_root = fixture_root.resolve()
        if prepare_command is not None and not toolchain:
            raise ValueError("prepared installs require explicit toolchain versions")
        source_snapshot = snapshot_tree(fixture_root, exclude_transient=True)
        source_digest = snapshot_digest(source_snapshot)
        dependency_digest = dependency_inputs_digest(fixture_root)
        platform_values = current_platform_identity()
        toolchain_digest = mapping_digest(_effective_toolchain(toolchain, platform_values))
        normalized_prepare = command_spec(prepare_command) if prepare_command is not None else None
        preparation_environment_digest = command_environment_digest(normalized_prepare)
        key = _prepared_key(
            source_digest,
            dependency_digest,
            toolchain_digest,
            preparation_environment_digest,
            normalized_prepare,
        )
        destination = self.cache_root / key
        expected_marker = {
            "key": key,
            "sourceDigest": source_digest,
            "dependencyDigest": dependency_digest,
            "toolchainDigest": toolchain_digest,
            "preparationEnvironmentDigest": preparation_environment_digest,
            "platform": platform_values,
        }
        if _prepared_cache_matches(destination, expected_marker, full=self._integrity_mode == "full"):
            return PreparedFixture(
                key,
                destination,
                source_digest,
                dependency_digest,
                toolchain_digest,
                preparation_environment_digest,
                platform_values,
                True,
            )

        self.cache_root.mkdir(parents=True, exist_ok=True)
        with _cache_key_lock(self.cache_root, key, self._lock_timeout_seconds):
            if _prepared_cache_matches(destination, expected_marker, full=self._integrity_mode == "full"):
                return PreparedFixture(
                    key,
                    destination,
                    source_digest,
                    dependency_digest,
                    toolchain_digest,
                    preparation_environment_digest,
                    platform_values,
                    True,
                )
            if destination.exists():
                _set_tree_writable(destination)
                shutil.rmtree(destination)
            temporary = self.cache_root / f".{key}.{uuid.uuid4().hex}.tmp"
            try:
                copy_tree_copy_on_write(fixture_root, temporary, exclude_transient=True)
                if normalized_prepare is not None:
                    result = self._command_runner(normalized_prepare, temporary)
                    if not result.passed:
                        raise RuntimeError(
                            f"fixture preparation failed with exit code {result.exit_code}: {result.stderr.strip()}"
                        )
                temporary_marker = temporary / ".eval-prepared.json"
                marker_data = {
                    **expected_marker,
                    "preparedSnapshotDigest": _prepared_snapshot_digest(temporary),
                }
                temporary_marker.write_text(json.dumps(marker_data, sort_keys=True) + "\n", encoding="utf-8")
                os.replace(temporary, destination)
            finally:
                if temporary.exists():
                    shutil.rmtree(temporary)
        return PreparedFixture(
            key,
            destination,
            source_digest,
            dependency_digest,
            toolchain_digest,
            preparation_environment_digest,
            platform_values,
            False,
        )

    @contextmanager
    def workspace(self, prepared: PreparedFixture, *, initialize_git: bool = True) -> Iterator[RunWorkspace]:
        """Yield a disposable run workspace and remove it even when the run fails."""

        self.runs_root.mkdir(parents=True, exist_ok=True)
        path = self.runs_root / f"{prepared.key[:12]}-{uuid.uuid4().hex}"
        preparation = copy_tree_copy_on_write(prepared.path, path, exclude_transient=False)
        try:
            (path / ".eval-workspace.json").write_text(
                json.dumps({"preparedKey": prepared.key, "disposable": True}, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            if initialize_git:
                initialize_git_workspace(path)
            yield RunWorkspace(path=path, prepared_key=prepared.key, preparation=preparation)
        finally:
            if path.exists():
                shutil.rmtree(path)


def prepared_fixture_key(
    fixture_root: Path,
    toolchain: Mapping[str, str],
    prepare_command: object | None = None,
) -> str:
    """Return the content address for source, dependency inputs, toolchain, and preparation."""

    source_digest = snapshot_digest(snapshot_tree(fixture_root.resolve(), exclude_transient=True))
    dependency_digest = dependency_inputs_digest(fixture_root.resolve())
    platform_values = current_platform_identity()
    toolchain_digest = mapping_digest(_effective_toolchain(toolchain, platform_values))
    normalized_prepare = command_spec(prepare_command) if prepare_command is not None else None
    return _prepared_key(
        source_digest,
        dependency_digest,
        toolchain_digest,
        command_environment_digest(normalized_prepare),
        normalized_prepare,
    )


def prepared_fixture_identity_key(
    source_digest: str,
    dependency_digest: str,
    toolchain_digest: str,
    prepare_command: object | None,
    preparation_environment_digest: str | None = None,
) -> str:
    """Rebuild a prepared key from receipt component digests and the governed prepare command."""

    normalized_prepare = command_spec(prepare_command) if prepare_command is not None else None
    environment_digest = preparation_environment_digest or command_environment_digest(normalized_prepare)
    return _prepared_key(source_digest, dependency_digest, toolchain_digest, environment_digest, normalized_prepare)


def command_environment_digest(command: CommandSpec | None) -> str:
    """Digest effective command environment inputs without storing their values in evidence."""

    if command is None:
        return hashlib.sha256(_canonical_json({})).hexdigest()
    inherited = os.environ if command.inherit_environment else {
        name: os.environ.get(name, "<unset>") for name in command.host_environment_allowlist
    }
    effective = {**inherited, **command.environment}
    value_digests = {
        name: hashlib.sha256(value.encode("utf-8")).hexdigest()
        for name, value in sorted(effective.items())
    }
    return hashlib.sha256(_canonical_json(value_digests)).hexdigest()


def copy_tree_copy_on_write(source: Path, destination: Path, *, exclude_transient: bool) -> str:
    """Clone a tree with platform copy-on-write support and fall back to a safe full copy.

    Transient-tree exclusion takes precedence over cloning the complete source. A source that
    contains excluded trees uses the filtered full-copy path so dependencies and build outputs do
    not leak into source preparation. Prepared snapshots normally use the fast clone path.
    """

    source = source.resolve()
    destination = destination.resolve()
    if not source.is_dir():
        raise ValueError(f"copy source is not a directory: {source}")
    if destination == source or source in destination.parents:
        raise ValueError("copy destination must be outside the source tree")
    if destination.exists():
        raise ValueError(f"copy destination already exists: {destination}")

    has_excluded_tree = exclude_transient and _contains_transient_tree(source)
    clone_command: list[str] | None = None
    if not has_excluded_tree and platform.system() == "Darwin":
        clone_command = ["cp", "-cR", str(source), str(destination)]
    elif not has_excluded_tree and platform.system() == "Linux":
        clone_command = ["cp", "--reflink=always", "-a", str(source), str(destination)]
    if clone_command is not None:
        completed = subprocess.run(clone_command, capture_output=True, text=True, check=False)
        if completed.returncode == 0:
            return "copy-on-write"
        if destination.exists():
            shutil.rmtree(destination)

    ignore = _ignore_transient if exclude_transient else None
    shutil.copytree(source, destination, symlinks=True, ignore=ignore)
    return "full-copy"


def snapshot_tree(root: Path, *, exclude_transient: bool = False) -> dict[str, str]:
    """Hash paths, content, mode bits, empty directories, and symlink targets into a manifest."""

    root = root.resolve()
    if not root.is_dir():
        raise ValueError(f"snapshot root is not a directory: {root}")
    snapshot: dict[str, str] = {}
    for path in _iter_tree(root, exclude_transient=exclude_transient):
        relative = path.relative_to(root)
        key = relative.as_posix()
        mode = stat.S_IMODE(path.lstat().st_mode)
        if path.is_symlink():
            snapshot[key] = f"link:{mode:o}:" + os.readlink(path)
        elif path.is_dir():
            snapshot[key] = f"dir:{mode:o}"
        elif path.is_file():
            snapshot[key] = f"file:{mode:o}:" + hashlib.sha256(path.read_bytes()).hexdigest()
    return snapshot


def snapshot_digest(snapshot: Mapping[str, str]) -> str:
    """Return a deterministic digest for a tree snapshot."""

    return hashlib.sha256(_canonical_json(snapshot)).hexdigest()


def snapshot_product_tree(root: Path) -> dict[str, str]:
    """Snapshot product files while excluding dependencies and runner-owned context artifacts."""

    snapshot = snapshot_tree(root, exclude_transient=True)
    runner_roots = {".agents", ".codex", ".eval-context", ".junie"}
    runner_files = {".eval-prepared.json", ".eval-workspace.json"}
    return {
        path: identity
        for path, identity in snapshot.items()
        if path not in runner_files and path.split("/", 1)[0] not in runner_roots
    }


def dependency_inputs_digest(fixture_root: Path) -> str:
    """Digest dependency manifests and lockfiles independently from transient install output."""

    inputs = {
        path.relative_to(fixture_root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in _iter_tree(fixture_root, exclude_transient=True)
        if path.is_file()
        and path.name in DEPENDENCY_INPUT_NAMES
    }
    return snapshot_digest(inputs)


def mapping_digest(value: Mapping[str, str]) -> str:
    """Return a deterministic digest for a string mapping."""

    if any(not isinstance(key, str) or not isinstance(item, str) for key, item in value.items()):
        raise ValueError("digest mappings must contain only string keys and values")
    return hashlib.sha256(_canonical_json(value)).hexdigest()


def current_platform_identity() -> dict[str, str]:
    """Return the automatic operating-system and architecture inputs for prepared-fixture keys."""

    return {
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
    }


def initialize_git_workspace(root: Path) -> str:
    """Create a clean deterministic Git baseline and isolated claim registry for a run workspace."""

    root = root.resolve()
    git_directory = root / ".git"
    if git_directory.exists():
        identity = subprocess.run(
            ["git", "config", "--get", "user.email"],
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
        )
        if identity.stdout.strip() != "eval-harness@example.invalid":
            raise RuntimeError("refusing to replace a Git repository not owned by the evaluation harness")
        shutil.rmtree(git_directory)
    environment = os.environ.copy()
    environment.update({
        "GIT_AUTHOR_DATE": "2000-01-01T00:00:00Z",
        "GIT_COMMITTER_DATE": "2000-01-01T00:00:00Z",
    })
    commands = (
        ["git", "init", "--quiet"],
        ["git", "config", "user.name", "Eval Harness"],
        ["git", "config", "user.email", "eval-harness@example.invalid"],
    )
    for argv in commands:
        completed = subprocess.run(argv, cwd=root, env=environment, capture_output=True, text=True, check=False)
        if completed.returncode != 0:
            raise RuntimeError(f"Git workspace initialization failed: {completed.stderr.strip()}")
    info_exclude = git_directory / "info" / "exclude"
    info_exclude.write_text("\n".join(sorted(TRANSIENT_TREE_NAMES)) + "\n", encoding="utf-8")
    for argv in (["git", "add", "-A"], ["git", "commit", "--quiet", "-m", "Evaluation baseline"]):
        completed = subprocess.run(argv, cwd=root, env=environment, capture_output=True, text=True, check=False)
        if completed.returncode != 0:
            raise RuntimeError(f"Git workspace baseline failed: {completed.stderr.strip()}")
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(f"Git workspace baseline lookup failed: {completed.stderr.strip()}")
    return completed.stdout.strip()


def is_evaluation_git_workspace(root: Path) -> bool:
    """Return whether an existing Git worktree uses the synthetic evaluation identity."""

    if not (root / ".git").exists():
        return False
    identity = subprocess.run(
        ["git", "config", "--get", "user.email"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    return identity.returncode == 0 and identity.stdout.strip() == "eval-harness@example.invalid"


def audit_functional_isolation(
    before: Mapping[str, str],
    after: Mapping[str, str],
    *,
    read_only: bool,
    allowed_write_paths: Sequence[str] = (),
) -> FunctionalIsolationAudit:
    """Compare workspace snapshots and classify read-only or allowed-path mutation behavior."""

    changed_paths = tuple(sorted(
        path for path in set(before) | set(after)
        if before.get(path) != after.get(path)
    ))
    allowed_roots = tuple(PurePosixPath(path) for path in allowed_write_paths)
    violating = changed_paths if read_only else tuple(
        path for path in changed_paths
        if not _path_is_allowed(PurePosixPath(path), allowed_roots)
    )
    return FunctionalIsolationAudit(
        status="violated" if violating else "verified",
        changed_paths=changed_paths,
        before_digest=snapshot_digest(before),
        after_digest=snapshot_digest(after),
    )


def _prepared_key(
    source_digest: str,
    dependency_digest: str,
    toolchain_digest: str,
    preparation_environment_digest: str,
    prepare_command: CommandSpec | None,
) -> str:
    payload = {
        "sourceDigest": source_digest,
        "dependencyDigest": dependency_digest,
        "toolchainDigest": toolchain_digest,
        "preparationEnvironmentDigest": preparation_environment_digest,
        "prepareArgv": list(prepare_command.argv) if prepare_command else [],
        "prepareEnvironmentNames": sorted(prepare_command.environment) if prepare_command else [],
        "prepareHostEnvironmentAllowlist": list(prepare_command.host_environment_allowlist) if prepare_command else [],
    }
    return hashlib.sha256(_canonical_json(payload)).hexdigest()


def _canonical_json(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def _ignore_transient(_directory: str, names: list[str]) -> set[str]:
    return set(names) & TRANSIENT_TREE_NAMES


def _path_is_allowed(path: PurePosixPath, roots: tuple[PurePosixPath, ...]) -> bool:
    return any(path == root or root in path.parents for root in roots)


def _effective_toolchain(toolchain: Mapping[str, str], platform_values: Mapping[str, str]) -> dict[str, str]:
    reserved = {"platform.system", "platform.release", "platform.machine"}
    overlap = reserved & set(toolchain)
    if overlap:
        raise ValueError(f"toolchain cannot override reserved platform identities: {', '.join(sorted(overlap))}")
    return {
        "platform.system": platform_values["system"],
        "platform.release": platform_values["release"],
        "platform.machine": platform_values["machine"],
        **toolchain,
    }


def _prepared_cache_matches(destination: Path, expected: Mapping[str, object], *, full: bool) -> bool:
    marker = destination / ".eval-prepared.json"
    if not marker.is_file():
        return False
    try:
        value = json.loads(marker.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError, OSError):
        return False
    if not isinstance(value, Mapping) or any(value.get(key) != item for key, item in expected.items()):
        return False
    source_snapshot = snapshot_tree(destination, exclude_transient=True)
    source_snapshot.pop(".eval-prepared.json", None)
    if snapshot_digest(source_snapshot) != expected.get("sourceDigest"):
        return False
    recorded = value.get("preparedSnapshotDigest")
    return isinstance(recorded, str) and (
        not full or recorded == _prepared_snapshot_digest(destination)
    )


def _prepared_snapshot_digest(root: Path) -> str:
    snapshot = snapshot_tree(root, exclude_transient=False)
    snapshot.pop(".eval-prepared.json", None)
    return snapshot_digest(snapshot)


def _set_tree_read_only(root: Path) -> None:
    for path in sorted(root.rglob("*"), key=lambda item: len(item.parts), reverse=True):
        if path.is_symlink():
            continue
        mode = stat.S_IMODE(path.stat().st_mode)
        path.chmod(mode & ~0o222)
    mode = stat.S_IMODE(root.stat().st_mode)
    root.chmod(mode & ~0o222)


def _set_tree_writable(root: Path) -> None:
    if not root.exists():
        return
    root.chmod(stat.S_IMODE(root.stat().st_mode) | 0o700)
    for path in root.rglob("*"):
        if path.is_symlink():
            continue
        mode = stat.S_IMODE(path.stat().st_mode)
        path.chmod(mode | (0o700 if path.is_dir() else 0o600))


class CacheKeyLock:
    def __init__(self, path: Path, timeout_seconds: float = 3600.0, stale_seconds: float = 600.0) -> None:
        self.path = path
        self.timeout_seconds = timeout_seconds
        self.stale_seconds = stale_seconds
        self.token = uuid.uuid4().hex

    def __enter__(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        deadline = time.monotonic() + self.timeout_seconds
        while True:
            try:
                descriptor = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            except FileExistsError:
                try:
                    observed = self.path.stat()
                    age = time.time() - observed.st_mtime
                except FileNotFoundError:
                    continue
                if age > self.stale_seconds:
                    owner = _read_lock_owner(self.path)
                    owner_pid = owner.get("pid") if isinstance(owner, Mapping) else None
                    if not isinstance(owner_pid, int) or not _process_is_alive(owner_pid):
                        try:
                            current = self.path.stat()
                            if current.st_ino == observed.st_ino and current.st_mtime_ns == observed.st_mtime_ns:
                                self.path.unlink()
                        except FileNotFoundError:
                            pass
                        continue
                if time.monotonic() >= deadline:
                    raise TimeoutError(f"timed out waiting for prepared fixture lock: {self.path.name}")
                time.sleep(0.05)
                continue
            with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
                handle.write(json.dumps({
                    "pid": os.getpid(),
                    "created": time.time(),
                    "token": self.token,
                }) + "\n")
            return None

    def __exit__(self, _exception_type: object, _exception: object, _traceback: object) -> None:
        owner = _read_lock_owner(self.path)
        if isinstance(owner, Mapping) and owner.get("token") == self.token:
            try:
                self.path.unlink()
            except FileNotFoundError:
                pass


def _cache_key_lock(cache_root: Path, key: str, timeout_seconds: float = 3600.0) -> CacheKeyLock:
    return CacheKeyLock(cache_root / ".locks" / f"{key}.lock", timeout_seconds=timeout_seconds)


def _read_lock_owner(path: Path) -> Mapping[str, object] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, UnicodeDecodeError, json.JSONDecodeError, OSError):
        return None
    return value if isinstance(value, Mapping) else None


def _process_is_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def _contains_transient_tree(root: Path) -> bool:
    for _directory, directory_names, _file_names in os.walk(root, topdown=True, followlinks=False):
        if any(name in TRANSIENT_TREE_NAMES for name in directory_names):
            return True
        directory_names[:] = [
            name for name in sorted(directory_names)
            if name not in TRANSIENT_TREE_NAMES
        ]
    return False


def _iter_tree(root: Path, *, exclude_transient: bool) -> Iterator[Path]:
    for directory, directory_names, file_names in os.walk(root, topdown=True, followlinks=False):
        current = Path(directory)
        retained_directories: list[str] = []
        for name in sorted(directory_names):
            path = current / name
            if exclude_transient and name in TRANSIENT_TREE_NAMES:
                continue
            if path.is_symlink():
                yield path
            else:
                retained_directories.append(name)
                yield path
        directory_names[:] = retained_directories
        for name in sorted(file_names):
            yield current / name
