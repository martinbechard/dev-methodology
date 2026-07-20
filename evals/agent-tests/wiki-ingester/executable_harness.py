# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Invokes the canonical Wiki Ingester adapter across controlled verifier interruptions.

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal


SUITE_ROOT = Path(__file__).resolve().parent
REPOSITORY_ROOT = SUITE_ROOT.parents[2]
STAGE_FIXTURE = SUITE_ROOT / "fixtures" / "stage_fixture.py"
RUNNER_PATH = REPOSITORY_ROOT / "evals" / "agent-tests" / "runner.py"
NATIVE_ADAPTER = REPOSITORY_ROOT / "generated/adapters/codex/agents/wiki-ingester.toml"
Gate = Literal["pre-move", "post-move"]
OWNED_ROOTS = (Path("docs/wiki"), Path("raw"))


def _load_runner() -> Any:
    """Load the repository agent-suite runner under an isolated module name.

    The executable boundary reuses the runner's canonical Codex staging, process,
    and retained-session readers. Import failures are surfaced to the caller.
    """
    specification = importlib.util.spec_from_file_location(
        "wiki_ingester_boundary_runner", RUNNER_PATH
    )
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot load agent-suite runner: {RUNNER_PATH}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    runner_directory = str(RUNNER_PATH.parent)
    inserted = runner_directory not in sys.path
    if inserted:
        sys.path.insert(0, runner_directory)
    try:
        specification.loader.exec_module(module)
    finally:
        if inserted:
            sys.path.remove(runner_directory)
    return module


@dataclass(frozen=True)
class VerifierPlan:
    """Define one interruption point in the bounded two-gate verifier loop.

    Use gate to select pre-move or post-move verification. Interruption selects
    submission zero, one, or two. Earlier submissions return NEEDS_CORRECTION;
    a post-move plan first accepts the pre-move state. The final dependency
    context returns no verifier verdict plus one verifier-dependent uncertainty,
    forcing the target's continuation-and-open-questions path.
    """

    gate: Gate
    interruption: int

    def __post_init__(self) -> None:
        """Reject gates or submission indexes outside the governed loop."""
        if self.gate not in {"pre-move", "post-move"}:
            raise ValueError(f"unsupported verifier gate: {self.gate}")
        if self.interruption not in range(3):
            raise ValueError("interruption must be 0, 1, or 2")

    def outcomes(self) -> tuple[dict[str, Any], ...]:
        """Return the ordered outcomes consumed by fresh verifier contexts."""
        outcomes: list[dict[str, Any]] = []
        if self.gate == "post-move":
            outcomes.append({"gate": "pre-move", "invocation": 0, "outcome": "GOOD"})
        outcomes.extend(
            {
                "gate": self.gate,
                "invocation": invocation,
                "outcome": (
                    "VERIFIER_INTERRUPTED"
                    if invocation == self.interruption
                    else "NEEDS_CORRECTION"
                ),
                **(
                    {
                        "finding": (
                            "docs/wiki/retry-policy/request-retry-eligibility.md: "
                            "add the exact heading '## Ineligible mutation requests' "
                            "and state beneath it that order creation, cancellation, and "
                            "payment mutation requests are never retried."
                            if invocation == 0
                            else "docs/wiki/retry-policy/fixed-retry-backoff.md: add an "
                            "exact '## Retry delay sequence' heading and state beneath it "
                            "that the first retry waits 200 milliseconds and the second "
                            "retry waits 500 milliseconds."
                        )
                    }
                    if invocation != self.interruption
                    else {
                        "unresolvedPoint": (
                            "Whether deployment-specific retry jitter changes the fixed "
                            "delay sequence remains unresolved."
                        ),
                        "missingEvidence": (
                            "an authoritative deployment retry policy or implementation"
                        ),
                        "provenance": "raw/retry-policy.md#Backoff",
                        "appropriatePage": (
                            "docs/wiki/retry-policy/fixed-retry-backoff.md"
                        ),
                    }
                ),
            }
            for invocation in range(self.interruption + 1)
        )
        return tuple(outcomes)


@dataclass(frozen=True)
class VerifierOutcomes:
    """Supply a fixed verifier sequence for a non-interruption neighbor scenario."""

    values: tuple[dict[str, Any], ...]

    def outcomes(self) -> tuple[dict[str, Any], ...]:
        """Return the fixed outcomes consumed by fresh verifier contexts."""
        return self.values


@dataclass(frozen=True)
class RuntimeLayout:
    """Identify the disposable target and dependency runtime staged for one control.

    The target_source is the canonical generated adapter. The control root owns
    only verifier outcome state; it has no authority over the evaluated repository.
    """

    codex_home: Path
    home: Path
    temporary: Path
    control_root: Path
    target_source: Path
    target_marker: str
    dependency_marker: str
    staged_agents: tuple[Any, ...]


def _run(arguments: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    """Run one fixture command and return its captured successful result."""
    return subprocess.run(
        arguments,
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    )


def _owned_tree_digest(repository: Path) -> str:
    """Return a stable content digest for the target-owned wiki and raw trees."""
    digest = hashlib.sha256()
    for owned_root in OWNED_ROOTS:
        root = repository / owned_root
        if not root.exists():
            continue
        for path in sorted(candidate for candidate in root.rglob("*") if candidate.is_file()):
            relative = path.relative_to(repository).as_posix()
            digest.update(relative.encode("utf-8"))
            digest.update(b"\0")
            digest.update(path.read_bytes())
            digest.update(b"\0")
    return digest.hexdigest()


def _initialize_repository(destination: Path, scenario: str) -> None:
    """Stage and commit one frozen Wiki Ingester fixture before target execution."""
    _run(
        [
            sys.executable,
            str(STAGE_FIXTURE),
            "--scenario",
            scenario,
            "--destination",
            str(destination),
        ],
        SUITE_ROOT,
    )
    _run(["git", "init", "-q"], destination)
    _run(["git", "config", "user.name", "Wiki Ingester Evaluation"], destination)
    _run(
        ["git", "config", "user.email", "wiki-ingester@example.invalid"],
        destination,
    )
    _run(["git", "add", "."], destination)
    _run(["git", "commit", "-qm", "Freeze verifier interruption fixture"], destination)


def _write_verifier_driver(control_root: Path, plan: VerifierPlan) -> Path:
    """Create the external sequential outcome driver used only by verifier children."""
    control_root.mkdir(parents=True, exist_ok=True)
    (control_root / "plan.json").write_text(
        json.dumps(plan.outcomes(), indent=2) + "\n", encoding="utf-8"
    )
    (control_root / "state.json").write_text("[]\n", encoding="utf-8")
    driver_path = control_root / "next_verdict.py"
    driver_path.write_text(
        '''# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Returns the next verifier outcome from a disposable interruption plan.
import hashlib
import json
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parent
plan = json.loads((root / "plan.json").read_text(encoding="utf-8"))
state_path = root / "state.json"
state = json.loads(state_path.read_text(encoding="utf-8"))
if len(state) >= len(plan):
    raise SystemExit("verifier plan exhausted")
outcome = plan[len(state)]
repository = Path.cwd()
digest = hashlib.sha256()
for relative_root in (Path("docs/wiki"), Path("raw")):
    owned_root = repository / relative_root
    if not owned_root.exists():
        continue
    for path in sorted(candidate for candidate in owned_root.rglob("*") if candidate.is_file()):
        relative = path.relative_to(repository).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\\0")
        digest.update(path.read_bytes())
        digest.update(b"\\0")
outcome["ownedTreeDigest"] = digest.hexdigest()
completed = subprocess.run(
    ["git", "diff", "--name-only", "HEAD"],
    cwd=repository,
    check=True,
    capture_output=True,
    text=True,
)
untracked = subprocess.run(
    ["git", "ls-files", "--others", "--exclude-standard"],
    cwd=repository,
    check=True,
    capture_output=True,
    text=True,
)
outcome["changedPaths"] = sorted(
    set(completed.stdout.splitlines()) | set(untracked.stdout.splitlines())
)
state.append(outcome)
state_path.write_text(json.dumps(state, indent=2) + "\\n", encoding="utf-8")
print(json.dumps(outcome, sort_keys=True))
''',
        encoding="utf-8",
    )
    return driver_path


def _write_injected_verifier(path: Path, driver_path: Path) -> None:
    """Write a verifier adapter whose only authority is returning one planned outcome."""
    instructions = f"""
You are the injected Wiki Topic Verifier dependency for one interruption control.
Remain read-only in the evaluated repository. Run this exact command once:

{sys.executable} {driver_path}

Parse its one JSON object. Confirm the target request matches its gate and invocation.
Return the JSON object exactly, without prose or a code fence. For GOOD or
NEEDS_CORRECTION, treat outcome as that exact verdict. For VERIFIER_INTERRUPTED,
return no GOOD or NEEDS_CORRECTION verdict. Do not edit the repository, retry,
delegate, repair target state, or consume another outcome.
""".strip()
    path.write_text(
        "model = \"gpt-5.6-terra\"\n"
        "name = \"wiki_topic_verifier\"\n"
        "description = \"Injected sequential Wiki Topic Verifier control.\"\n"
        "model_reasoning_effort = \"low\"\n"
        f'developer_instructions = """\n{instructions}\n"""\n',
        encoding="utf-8",
    )


def stage_runtime(runtime_root: Path, plan: Any) -> RuntimeLayout:
    """Stage the canonical target and replace only its declared verifier dependency.

    runtime_root receives an isolated Codex home and verifier control files. plan
    defines the dependency results. The evaluated repository is not inspected or
    mutated by this function. Missing adapters or skill packages raise errors.
    """
    runner = _load_runner()
    codex_home = runtime_root / "codex-home"
    agent_root = codex_home / "agents"
    skill_root = codex_home / "skills"
    home = runtime_root / "home"
    temporary = runtime_root / "tmp"
    control_root = runtime_root / "verifier-control"
    for directory in (agent_root, skill_root, home, temporary):
        directory.mkdir(parents=True, exist_ok=True)

    driver_path = _write_verifier_driver(control_root, plan)
    dependency_source = control_root / "wiki_topic_verifier.toml"
    _write_injected_verifier(dependency_source, driver_path)
    target = runner._copy_agent(
        NATIVE_ADAPTER,
        "wiki_ingester",
        agent_root,
    )
    dependency = runner._copy_agent(
        dependency_source,
        "wiki_topic_verifier",
        agent_root,
    )
    for skill_name in (
        "agent-claim",
        "code-project-wiki",
        "organise-project-files",
        "project-wiki",
        "project-wiki-topic-write",
    ):
        runner._copy_skill_package(
            REPOSITORY_ROOT / "skills" / skill_name / "SKILL.md",
            skill_root,
        )
    return RuntimeLayout(
        codex_home=codex_home,
        home=home,
        temporary=temporary,
        control_root=control_root,
        target_source=NATIVE_ADAPTER,
        target_marker=target.instruction_marker,
        dependency_marker=dependency.instruction_marker,
        staged_agents=(target, dependency),
    )


def _copy_auth(codex_home: Path) -> None:
    """Copy the current Codex authentication record into the isolated runtime home."""
    source = Path(
        os.environ.get("CODEX_AUTH_FILE", str(Path.home() / ".codex" / "auth.json"))
    )
    if not source.is_file():
        raise RuntimeError(f"Codex authentication file is unavailable: {source}")
    destination = codex_home / "auth.json"
    shutil.copyfile(source, destination)
    destination.chmod(0o600)


def _target_prompt(plan: VerifierPlan) -> str:
    """Return a launcher prompt that leaves all repository lifecycle work to the target."""
    return f"""
Act only as a one-child launcher. Do not inspect or mutate the repository yourself.
Spawn exactly wiki_ingester with fork_context false. Tell it to execute TASK.md in the
current repository and use only fresh wiki_topic_verifier contexts. This control forces
a verifier interruption at gate {plan.gate}, submission {plan.interruption}; an injected
dependency response of VERIFIER_INTERRUPTED is an unavailable required verdict. Tell it
to follow its canonical interruption-continuation instructions: preserve every
substantiated conclusion, record the supplied verifier-dependent point in the appropriate
page's Open Questions section with the missing evidence and provenance, finish the
processed-source links and validation, and distinguish ingested conclusions from recorded
open questions in eval-result.md. This canonical interruption branch governs when the
ordinary TASK.md GOOD path cannot finish. Wait for the child and return its terminal
response exactly. Name each verifier task exactly
pre_move_verifier_N or post_move_verifier_N, where N is the zero-based invocation at that
gate. Do not invoke another target or repair results.
""".strip()


def _neighbor_prompt(scenario: str) -> str:
    """Return a launcher prompt for one normal neighboring Wiki Ingester scenario."""
    return f"""
Act only as a one-child launcher. Do not inspect or mutate the repository yourself.
Spawn exactly wiki_ingester with fork_context false. Tell it to execute TASK.md in the
current repository for the {scenario} scenario and use fresh wiki_topic_verifier
contexts only when TASK.md requires them. Tell it to follow its canonical instructions.
Wait for the child and return its terminal response exactly. Do not invoke another target
or repair its results. Name each verifier task exactly pre_move_verifier_N or
post_move_verifier_N, where N is the zero-based invocation at that gate.
""".strip()


def _terminal_text(session: Any) -> str:
    """Decode a retained terminal response without inventing missing evidence."""
    if session.terminal_response is None:
        return ""
    return session.terminal_response.decode("utf-8", errors="replace")


def _dependency_agent_path(session: Any, codex_home: Path) -> str:
    """Return the target-assigned gate and submission identity for one dependency."""
    rollout_path = session.rollout_path
    if rollout_path is None:
        raise RuntimeError(f"dependency session has no retained rollout: {session.session_id}")
    resolved_home = codex_home.resolve()
    resolved_rollout = rollout_path.resolve()
    if resolved_home not in resolved_rollout.parents:
        raise RuntimeError(f"dependency rollout escapes isolated Codex home: {rollout_path}")
    for line in rollout_path.read_text(encoding="utf-8").splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(event, dict) or event.get("type") != "session_meta":
            continue
        payload = event.get("payload")
        if isinstance(payload, dict) and isinstance(payload.get("agent_path"), str):
            return str(payload["agent_path"])
    raise RuntimeError(f"dependency session has no agent path: {session.session_id}")


def _session_tool_calls(session: Any) -> list[dict[str, str]]:
    """Return retained tool names and serialized arguments for one runtime session."""
    if session.rollout_path is None:
        raise RuntimeError(f"session has no retained rollout: {session.session_id}")
    calls: list[dict[str, str]] = []
    for line in session.rollout_path.read_text(encoding="utf-8").splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(event, dict) or event.get("type") != "response_item":
            continue
        payload = event.get("payload")
        if not isinstance(payload, dict) or payload.get("type") not in {
            "function_call",
            "custom_tool_call",
        }:
            continue
        arguments = payload.get("arguments", payload.get("input", ""))
        calls.append(
            {
                "name": str(payload.get("name", "")),
                "arguments": (
                    arguments
                    if isinstance(arguments, str)
                    else json.dumps(arguments, sort_keys=True)
                ),
            }
        )
    return calls


def _session_user_messages(session: Any) -> list[str]:
    """Return retained user messages supplied to one nested runtime session."""
    if session.rollout_path is None:
        raise RuntimeError(f"session has no retained rollout: {session.session_id}")
    messages: list[str] = []
    for line in session.rollout_path.read_text(encoding="utf-8").splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(event, dict) or event.get("type") != "response_item":
            continue
        payload = event.get("payload")
        if not isinstance(payload, dict) or payload.get("type") != "message":
            continue
        if payload.get("role") != "user":
            continue
        messages.append(
            "\n".join(
                str(item.get("text", ""))
                for item in payload.get("content", [])
                if isinstance(item, dict) and item.get("type") == "input_text"
            )
        )
    return messages


def _claim_event_trace(runner: Any, repository: Path) -> list[dict[str, Any]]:
    """Return acquisition and release journal events from the contained fixture."""
    common = runner._git_common_directory(repository, repository, "fixture")
    event_root = common / "agent-claim-events" / "hot"
    events: list[dict[str, Any]] = []
    for journal in sorted(event_root.glob("*.jsonl")):
        resolved_journal = journal.resolve()
        if common not in resolved_journal.parents:
            raise RuntimeError(f"claim journal escapes fixture containment: {journal}")
        for line in journal.read_text(encoding="utf-8").splitlines():
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(event, dict) and event.get("action") in {"acquire", "release"}:
                events.append(event)
    return sorted(events, key=lambda event: str(event.get("timestamp", "")))


def _observe_target_result(
    runner: Any,
    layout: RuntimeLayout,
    destination: Path,
    process: dict[str, Any],
    initial_owned_tree_digest: str,
    baseline_commit: str,
) -> dict[str, Any]:
    """Observe target artifacts, Git state, claims, and retained sessions read-only."""
    sessions = runner._load_sessions(layout.codex_home)
    targets = [
        session
        for session in sessions
        if session.invocation == "wiki_ingester"
    ]
    if len(targets) != 1:
        raise RuntimeError(
            f"expected one canonical Wiki Ingester session, observed {len(targets)}"
        )
    target = targets[0]
    if layout.target_marker not in target.instruction_markers:
        raise RuntimeError("Wiki Ingester session lacks canonical instruction binding")
    roots = [session for session in sessions if session.session_id == target.parent_thread_id]
    if len(roots) != 1:
        raise RuntimeError(f"expected one retained target launcher, observed {len(roots)}")
    root = roots[0]
    dependencies = sorted(
        (
            session
            for session in sessions
            if session.invocation == "wiki_topic_verifier"
            and session.parent_thread_id == target.session_id
            and layout.dependency_marker in session.instruction_markers
        ),
        key=lambda session: session.started_at,
    )
    result_path = destination / "eval-result.md"
    result_text = result_path.read_text(encoding="utf-8") if result_path.is_file() else ""
    claim_status = json.loads(
        _run(
            [
                sys.executable,
                str(REPOSITORY_ROOT / "skills/agent-claim/scripts/claim.py"),
                "--repo",
                ".",
                "status",
            ],
            destination,
        ).stdout
    )
    claim_events = _claim_event_trace(runner, destination)
    release_events = runner._release_events(destination, destination)
    return {
        "process": process,
        "rootSessionId": root.session_id,
        "rootToolCalls": _session_tool_calls(root),
        "targetSessionId": target.session_id,
        "targetInstructionMarker": layout.target_marker,
        "targetInstructionMarkers": sorted(target.instruction_markers),
        "targetToolCalls": _session_tool_calls(target),
        "targetTerminalResponse": _terminal_text(target),
        "dependencySessionIds": [session.session_id for session in dependencies],
        "dependencyAgentPaths": [
            _dependency_agent_path(session, layout.codex_home)
            for session in dependencies
        ],
        "dependencyResponses": [_terminal_text(session) for session in dependencies],
        "dependencyRequests": [
            _session_user_messages(session) for session in dependencies
        ],
        "dependencyToolCalls": [
            _session_tool_calls(session) for session in dependencies
        ],
        "verifierDriverPath": str(layout.control_root / "next_verdict.py"),
        "verifierDriverCommand": f"{sys.executable} {layout.control_root / 'next_verdict.py'}",
        "repositoryPath": str(destination.resolve()),
        "verifierControlTrace": json.loads(
            (layout.control_root / "state.json").read_text(encoding="utf-8")
        ),
        "evaluationResultText": result_text,
        "initialOwnedTreeDigest": initial_owned_tree_digest,
        "finalOwnedTreeDigest": _owned_tree_digest(destination),
        "gitStatus": _run(["git", "status", "--porcelain"], destination).stdout.strip(),
        "head": _run(["git", "rev-parse", "HEAD"], destination).stdout.strip(),
        "baselineCommit": baseline_commit,
        "committedPaths": _run(
            ["git", "diff", "--name-only", f"{baseline_commit}..HEAD"],
            destination,
        ).stdout.splitlines(),
        "liveRegistryClaims": claim_status["claims"],
        "claimEvents": claim_events,
        "releaseEvents": release_events,
        "rawSourcePresent": (destination / "raw/provider-routing.md").is_file(),
        "processedSourcePresent": (
            destination / "raw/processed/provider-routing.md"
        ).is_file(),
        "retryRawSourcePresent": (destination / "raw/retry-policy.md").is_file(),
        "retryProcessedSourcePresent": (
            destination / "raw/processed/retry-policy.md"
        ).is_file(),
        "queueFiles": sorted(
            path.relative_to(destination).as_posix()
            for path in (destination / "raw").rglob("*")
            if path.is_file()
        ),
        "wikiFiles": sorted(
            path.relative_to(destination).as_posix()
            for path in (destination / "docs/wiki").rglob("*")
            if path.is_file()
        ),
        "wikiContent": {
            path.relative_to(destination).as_posix(): path.read_text(encoding="utf-8")
            for path in sorted((destination / "docs/wiki").rglob("*.md"))
            if path.is_file()
        },
        "rawRetrySourceReferences": sorted(
            path.relative_to(destination).as_posix()
            for path in (destination / "docs/wiki").rglob("*.md")
            if "raw/retry-policy.md" in path.read_text(encoding="utf-8")
            and "raw/processed/retry-policy.md" not in path.read_text(encoding="utf-8")
        ),
        "processedRetrySourceReferences": sorted(
            path.relative_to(destination).as_posix()
            for path in (destination / "docs/wiki").rglob("*.md")
            if "raw/processed/retry-policy.md" in path.read_text(encoding="utf-8")
        ),
    }


def _execute_target(
    runner: Any,
    layout: RuntimeLayout,
    destination: Path,
    prompt: str,
    timeout_seconds: int,
) -> dict[str, Any]:
    """Launch the canonical target through Codex and return captured process evidence."""
    command = [
        str(runner._bundled_codex_executable()),
        "--model",
        "gpt-5.6-terra",
        "--enable",
        "multi_agent",
        "--disable",
        "multi_agent_v2",
        "-c",
        "agents.max_threads=3",
        "--sandbox",
        "workspace-write",
        "-c",
        "agents.max_depth=2",
        "--ask-for-approval",
        "never",
        "--add-dir",
        str(destination / ".git"),
        "--add-dir",
        str(layout.control_root),
        "--strict-config",
        *runner._agent_registration_arguments(layout.staged_agents, layout.codex_home),
        "exec",
        "--json",
        "--ignore-rules",
        "-C",
        str(destination),
        prompt,
    ]
    environment = runner._controlled_environment(
        layout.home,
        layout.codex_home,
        layout.temporary,
    )
    return runner._run_process(
        command,
        destination,
        environment,
        timeout_seconds,
        containment_root=destination.parent,
    )


def run_control(
    plan: VerifierPlan,
    destination: Path,
    timeout_seconds: int = 900,
) -> dict[str, Any]:
    """Execute one actual Wiki Ingester interruption control.

    plan selects the verifier responses. destination must not exist and receives a
    disposable Git fixture. timeout_seconds limits the root Codex process. The target
    owns all repository edits, uncertainty classification, result writing, commits, and
    claim closeout;
    this function returns read-only observations after the process ends.
    """
    if destination.exists():
        raise ValueError(f"destination already exists: {destination}")
    runtime_root = destination.parent / f"{destination.name}-runtime"
    if runtime_root.exists():
        raise ValueError(f"runtime root already exists: {runtime_root}")
    runtime_root.mkdir(parents=True)
    _initialize_repository(destination, "raw-ingest")
    initial_owned_tree_digest = _owned_tree_digest(destination)
    baseline_commit = _run(["git", "rev-parse", "HEAD"], destination).stdout.strip()
    layout = stage_runtime(runtime_root, plan)
    _copy_auth(layout.codex_home)
    runner = _load_runner()
    process = _execute_target(
        runner,
        layout,
        destination,
        _target_prompt(plan),
        timeout_seconds,
    )
    return _observe_target_result(
        runner,
        layout,
        destination,
        process,
        initial_owned_tree_digest,
        baseline_commit,
    )


def run_neighbor_control(
    scenario: Literal["raw-ingest", "destination-collision"],
    destination: Path,
    timeout_seconds: int = 900,
) -> dict[str, Any]:
    """Execute one normal neighboring Wiki Ingester behavior control.

    scenario selects raw ingest with two GOOD verifier gates or collision with no
    verifier. destination must not exist. timeout_seconds limits the Codex process.
    The returned evidence is observed after the canonical target finishes.
    """
    if scenario not in {"raw-ingest", "destination-collision"}:
        raise ValueError(f"unsupported neighbor scenario: {scenario}")
    if destination.exists():
        raise ValueError(f"destination already exists: {destination}")
    runtime_root = destination.parent / f"{destination.name}-runtime"
    if runtime_root.exists():
        raise ValueError(f"runtime root already exists: {runtime_root}")
    runtime_root.mkdir(parents=True)
    _initialize_repository(destination, scenario)
    initial_owned_tree_digest = _owned_tree_digest(destination)
    baseline_commit = _run(["git", "rev-parse", "HEAD"], destination).stdout.strip()
    outcomes = (
        (
            {
                "gate": "pre-move",
                "invocation": 0,
                "outcome": "NEEDS_CORRECTION",
                "finding": "federated ownership duplicated",
            },
            {"gate": "pre-move", "invocation": 1, "outcome": "GOOD"},
            {"gate": "post-move", "invocation": 0, "outcome": "GOOD"},
        )
        if scenario == "raw-ingest"
        else ()
    )
    layout = stage_runtime(runtime_root, VerifierOutcomes(outcomes))
    _copy_auth(layout.codex_home)
    runner = _load_runner()
    process = _execute_target(
        runner,
        layout,
        destination,
        _neighbor_prompt(scenario),
        timeout_seconds,
    )
    return _observe_target_result(
        runner,
        layout,
        destination,
        process,
        initial_owned_tree_digest,
        baseline_commit,
    )


def main(arguments: list[str] | None = None) -> int:
    """Run one selected live control and print its complete observed result as JSON."""
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gate", required=True, choices=("pre-move", "post-move"))
    parser.add_argument("--interruption", required=True, type=int, choices=(0, 1, 2))
    parser.add_argument("--destination", required=True, type=Path)
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parsed = parser.parse_args(arguments)
    result = run_control(
        VerifierPlan(parsed.gate, parsed.interruption),
        parsed.destination.resolve(),
        parsed.timeout_seconds,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["process"]["exitCode"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
