#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Modified with AI assistance.
# Summary: Provides the CLI and compatibility API for agent and skill evaluation execution.

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
from contextlib import contextmanager, nullcontext
from pathlib import Path, PurePosixPath
from typing import Iterable, Iterator, Mapping, NamedTuple

import yaml

try:
    from agent_skill_evals import *  # noqa: F403
    from agent_skill_evals.staging import (
        ModelVisibleProjection,
        ProjectionEvidenceDirectory,
        create_projection_evidence_directory,
        seal_model_visible_projection,
        stage_mcp_reference_context,
        stage_model_visible_projection,
        synchronize_model_visible_projection,
        write_model_visible_projection_manifest,
    )
except ModuleNotFoundError:
    from scripts.agent_skill_evals import *  # type: ignore[no-redef]  # noqa: F403
    from scripts.agent_skill_evals.staging import (
        ModelVisibleProjection,
        ProjectionEvidenceDirectory,
        create_projection_evidence_directory,
        seal_model_visible_projection,
        stage_mcp_reference_context,
        stage_model_visible_projection,
        synchronize_model_visible_projection,
        write_model_visible_projection_manifest,
    )

try:
    from agent_skill_judge_contract import canonical_judge_identity
except ModuleNotFoundError:
    from scripts.agent_skill_judge_contract import canonical_judge_identity


_MAX_CAPTURE_REDACTION_BYTES = 10 * 1024 * 1024
_MAX_PRESERVED_OUTPUT_FILES = 512
_MAX_PRESERVED_OUTPUT_BYTES = 20 * 1024 * 1024


class TrustedProjectionVerifier(NamedTuple):
    """Bind one normalized evaluator-owned verifier to exact executable and source bytes."""

    specification: object
    governed_argv: tuple[str, ...]
    interpreter_name: str
    interpreter_digest: str
    source_kind: str
    source_path: str
    source_digest: str
    source_size: int
    source_evidence: str
    script_path: Path
    execution_script_digest: str
    contract_digest: str
    semantic_result_field: str
    semantic_red_exit_code: int | None


def run(command: object, cwd: Path) -> bool:
    """Run a fixture command through the shell-free compatibility boundary."""

    spec = command_spec(command)  # noqa: F405
    print(f"[{cwd.name}] {json.dumps(list(spec.argv))}")
    result = run_command(spec, cwd)  # noqa: F405
    if result.stdout:
        print(result.stdout, end="" if result.stdout.endswith("\n") else "\n")
    if result.stderr:
        print(result.stderr, file=sys.stderr, end="" if result.stderr.endswith("\n") else "\n")
    return result.passed


def main(argv: list[str] | None = None) -> int:
    """Validate catalogs, prepare fixtures, print harness commands, or execute selected cases."""

    parser = _argument_parser()
    args = parser.parse_args(argv)
    cases = load_cases()  # noqa: F405

    if args.validate_calibration is not None:
        value = yaml.safe_load(args.validate_calibration.read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            print("FAIL calibration record must be a YAML mapping", file=sys.stderr)
            return 1
        expected = {
            field: value.get(field)
            for field in (
                "rubricId",
                "judgePromptSha256",
                "judgeOutputSchemaSha256",
                "instructionEnvelopeSha256",
                "harness",
                "judgeModelIdentity",
                "reasoningProfile",
                "rubricSha256",
                "calibrationSetSha256",
            )
        }
        rubric_id = value.get("rubricId")
        rubric = next(
            (
                item
                for item in load_framework_catalogs()["judges.yaml"].get(  # noqa: F405
                    "rubrics", []
                )
                if isinstance(item, dict) and item.get("id") == rubric_id
            ),
            None,
        )
        if rubric is None:
            print(
                "FAIL calibration record must identify a current Model Judge rubric",
                file=sys.stderr,
            )
            return 1
        try:
            expected.update(canonical_judge_identity(rubric))
        except ValueError as error:
            print(f"FAIL canonical Judge contract: {error}", file=sys.stderr)
            return 1
        calibration_errors = validate_calibration_record(value, expected)  # noqa: F405
        if calibration_errors:
            for error in calibration_errors:
                print(f"FAIL {error}", file=sys.stderr)
            return 1
        print(json.dumps({
            "calibration": "diagnostic-valid",
            "promotionEligible": False,
            "metrics": compute_calibration_metrics(value["samples"]),  # noqa: F405
            "recordDigest": value["recordDigest"],
        }, sort_keys=True))
        return 0

    if args.validate_catalogs:
        catalog_errors = validate_framework_catalogs(cases=cases)  # noqa: F405
        if catalog_errors:
            for error in catalog_errors:
                print(f"FAIL {error}", file=sys.stderr)
            return 1
        print("CATALOGS VALID")
        if not any((args.case, args.skill_probe, args.agent_scenario, args.workflow_pack, args.prepare, args.print_invocation, args.invoke_harness)):
            return 0

    try:
        selected = _select_cases(cases, args.case, args.skill_probe, args.agent_scenario, args.workflow_pack)
    except ValueError as error:
        parser.error(str(error))
    if args.prepare and not args.case:
        parser.error("--prepare requires --case")
    if args.prepare and args.project_root is not None:
        parser.error("--prepare is limited to the catalog-owned synthetic fixture")
    if args.install and not args.prepare:
        parser.error("--install is allowed only with an explicit --prepare step")
    if args.probe_variant and not args.skill_probe:
        parser.error("--probe-variant requires --skill-probe")
    if args.skill_probe and (args.print_invocation or args.invoke_harness):
        if args.probe_variant is None:
            parser.error("harness-backed skill probes require --probe-variant")
        try:
            selected = [
                _apply_probe_variant(case, args.skill_probe, args.probe_variant)
                for case in selected
            ]
        except ValueError as error:
            parser.error(str(error))
    if args.invoke_harness and any(case.get("readOnly") for case in selected) and args.result is None:
        parser.error("read-only harness execution requires --result outside the product workspace")
    if (args.print_invocation or args.invoke_harness) and (len(selected) != 1 or not args.harness):
        parser.error("harness invocation requires one selected case and --harness")
    if args.mcp_agent_ops_executable is not None and (
        len(selected) != 1 or not _case_uses_mcp_agent_ops(selected[0])
    ):
        parser.error("--mcp-agent-ops-executable is valid only for an MCP-enabled case")
    if (
        (args.print_invocation or args.invoke_harness)
        and len(selected) == 1
        and _case_uses_mcp_agent_ops(selected[0])
        and args.mcp_agent_ops_executable is None
    ):
        parser.error("MCP-enabled harness invocation requires --mcp-agent-ops-executable")
    if args.codex_auth_file is not None and (
        not args.invoke_harness or args.harness != "codex"
    ):
        parser.error("--codex-auth-file is valid only for a live Codex invocation")
    if args.invoke_harness and args.project_root is None and args.prepared_cache is None:
        args.prepared_cache = Path(tempfile.gettempdir()) / "dev-methodology-evals" / "prepared"
    if args.invoke_harness and any(_requires_external_containment(case) for case in selected):
        parser.error(
            "high-risk evaluation cases require the externally-contained tier, "
            "which is not implemented"
        )
    definition_failures = [
        f"{case.get('id', 'unknown')}: {error}"
        for case in selected
        for error in validate_case_definition(case)  # noqa: F405
    ]
    if definition_failures:
        for failure in definition_failures:
            print(f"FAIL {failure}", file=sys.stderr)
        return 1

    toolchain = _parse_toolchain(args.toolchain)
    manager = _workspace_manager(args)
    failures: list[str] = []
    for case in selected:
        default_root = ROOT / str(case["project"])  # noqa: F405
        project_root = args.project_root.resolve() if args.project_root else default_root
        if args.prepare:
            assert manager is not None
            prepared = manager.prepare(
                project_root,
                toolchain,
                case.get("install") if args.install else None,
            )
            print(json.dumps({
                "case": case["id"],
                "preparedFixture": {
                    "key": prepared.key,
                    "sourceDigest": prepared.source_digest,
                    "preparedSnapshotDigest": prepared.prepared_snapshot_digest,
                    "dependencyDigest": prepared.dependency_digest,
                    "toolchainDigest": prepared.toolchain_digest,
                    "preparationEnvironmentDigest": prepared.preparation_environment_digest,
                    "platform": dict(prepared.platform_identity),
                    "cacheHit": prepared.cache_hit,
                },
            }, sort_keys=True))
            continue

        prepared = None
        workspace_context = nullcontext(None)
        if manager is not None:
            prepare_command = case.get("install") if args.invoke_harness else None
            prepared = manager.prepare(
                project_root,
                toolchain,
                prepare_command,
                allow_create=not (
                    args.invoke_harness and prepare_command is not None
                ),
            )
            workspace_context = manager.workspace(
                prepared,
                initialize_git=not (args.print_invocation or args.invoke_harness),
            )
        with workspace_context as run_workspace:
            active_root = run_workspace.path if run_workspace is not None else project_root
            result_for_preflight = None if args.invoke_harness else args.result
            case_errors = validate_case(case, active_root, result_for_preflight)  # noqa: F405
            if args.evidence is not None or (
                args.result is not None and not args.invoke_harness
            ):
                classification = classify_evidence(case, args.evidence)  # noqa: F405
                case_errors.extend(classification.errors)
                case_errors.extend(classification.stale_reasons)
                print(json.dumps({"case": case["id"], "evidence": classification.as_dict()}, sort_keys=True))
            before_product = snapshot_product_tree(active_root) if args.invoke_harness else None  # noqa: F405
            invocation_attempted = False
            if args.print_invocation or args.invoke_harness:
                if not case_errors:
                    invocation_attempted = True
                    invocation_error = _handle_harness_invocation(args, case, active_root)
                    if invocation_error is not None:
                        case_errors.append(invocation_error)
            if args.invoke_harness and invocation_attempted and before_product is not None:
                allowed_write_paths = case.get("allowedWritePaths", [])
                ephemeral_write_paths = case.get("ephemeralWritePaths", [])
                if not isinstance(allowed_write_paths, list) or any(
                    not isinstance(path, str) for path in allowed_write_paths
                ):
                    case_errors.append("case.allowedWritePaths must be a list of relative paths")
                elif not isinstance(ephemeral_write_paths, list) or any(
                    not isinstance(path, str) for path in ephemeral_write_paths
                ):
                    case_errors.append("case.ephemeralWritePaths must be a list of relative paths")
                else:
                    isolation_audit = audit_functional_isolation(  # noqa: F405
                        before_product,
                        snapshot_product_tree(active_root),  # noqa: F405
                        read_only=bool(case.get("readOnly")),
                        allowed_write_paths=allowed_write_paths,
                        ephemeral_write_paths=ephemeral_write_paths,
                    )
                    print(json.dumps({
                        "case": case["id"],
                        "functionalIsolation": {
                            "status": isolation_audit.status,
                            "beforeDigest": isolation_audit.before_digest,
                            "afterDigest": isolation_audit.after_digest,
                            "workspaceBeforeDigest": isolation_audit.workspace_before_digest,
                            "workspaceAfterDigest": isolation_audit.workspace_after_digest,
                            "changedPaths": list(isolation_audit.changed_paths),
                            "ephemeralChangedPaths": list(isolation_audit.ephemeral_changed_paths),
                            "allowedWritePaths": allowed_write_paths,
                            "ephemeralWritePaths": ephemeral_write_paths,
                        },
                    }, sort_keys=True))
                    if isolation_audit.status != "verified":
                        case_errors.append("functional isolation audit detected out-of-contract mutation")
            if args.invoke_harness and args.result is not None:
                case_errors.extend(validate_case(case, active_root, args.result))  # noqa: F405
            if args.print_invocation and not args.invoke_harness:
                if case_errors:
                    failures.extend(f"{case['id']}: {error}" for error in case_errors)
                else:
                    print(f"PREFLIGHT PASS {case['id']}")
                continue
            if args.invoke_harness:
                if case_errors:
                    failures.extend(f"{case['id']}: {error}" for error in case_errors)
                else:
                    print(
                        f"HARNESS CAPTURE PASS {case['id']} "
                        "(local execution; security containment not claimed)"
                    )
                continue
            if args.result is not None or args.evidence is not None:
                if case_errors:
                    failures.extend(f"{case['id']}: {error}" for error in case_errors)
                else:
                    print(f"EVIDENCE VALID {case['id']}")
                continue
            if args.project_root is not None:
                failures.append(
                    f"{case['id']}: direct verification is limited to catalog-owned synthetic fixtures"
                )
                continue
            if case_errors:
                failures.extend(f"{case['id']}: {error}" for error in case_errors)
                continue
            verification_passed = run(case["verify"], active_root)
            expect_verify_failure = bool(case.get("expectVerifyFailure", False))
            if verification_passed == expect_verify_failure:
                expectation = "failure" if expect_verify_failure else "success"
                case_errors.append(f"verification command did not produce expected {expectation}")
            if case_errors:
                failures.extend(f"{case['id']}: {error}" for error in case_errors)
            else:
                print(f"FIXTURE PASS {case['id']}")

    if failures:
        for failure in failures:
            print(f"FAIL {failure}", file=sys.stderr)
        return 1
    return 0


def _argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Codex and Junie agent and skill evaluations.")
    parser.add_argument("--case")
    parser.add_argument("--skill-probe")
    parser.add_argument("--probe-variant", choices=("treatment", "target-omitted", "wrong-skill"))
    parser.add_argument("--agent-scenario")
    parser.add_argument("--workflow-pack")
    parser.add_argument("--validate-catalogs", action="store_true")
    parser.add_argument("--validate-calibration", type=Path)
    parser.add_argument("--install", action="store_true")
    parser.add_argument("--prepare", action="store_true")
    parser.add_argument("--prepared-cache", type=Path)
    parser.add_argument("--workspace-root", type=Path)
    parser.add_argument("--toolchain", action="append", default=[], metavar="NAME=VERSION")
    parser.add_argument("--project-root", type=Path)
    parser.add_argument("--result", type=Path)
    parser.add_argument("--evidence", type=Path)
    parser.add_argument("--harness", choices=sorted(SUPPORTED_HARNESSES))  # noqa: F405
    parser.add_argument("--agent-id")
    parser.add_argument("--model", default="configured-model")
    parser.add_argument("--event-output", type=Path)
    parser.add_argument("--receipt-artifact-directory", type=Path)
    parser.add_argument("--mcp-agent-ops-executable", type=Path)
    parser.add_argument("--codex-auth-file", type=Path)
    parser.add_argument("--output-schema", type=Path)
    parser.add_argument("--print-invocation", action="store_true")
    parser.add_argument("--invoke-harness", action="store_true")
    parser.add_argument("--approved-env-name", action="append", default=[])
    return parser


def _requires_external_containment(case: Mapping[str, object]) -> bool:
    """Return whether a case explicitly opts into the high-risk execution tier."""

    risk = case.get("risk")
    return (
        isinstance(risk, Mapping)
        and risk.get("level") == "high"
        and case.get("executionTier") == "externally-contained"
        and case.get("securityContainmentRequired") is True
    )


def _case_uses_mcp_agent_ops(case: Mapping[str, object]) -> bool:
    """Return whether the selected base case or probe treatment enables MCP operations."""
    contract = case.get("mcpAgentOps")
    if not isinstance(contract, Mapping):
        return False
    enablement = contract.get("enablement")
    if enablement == "base-case-only":
        return "probeVariant" not in case
    return (
        enablement == "probe-treatment-only"
        and case.get("probeVariant") == "treatment"
    )


@contextmanager
def _reserve_capture_paths(paths: Iterable[Path]) -> Iterator[None]:
    """Reserve unused evidence destinations so concurrent runs cannot share them."""

    outputs = [path.resolve() for path in paths]
    if len(outputs) != len(set(outputs)):
        raise ValueError("capture output paths must be distinct")
    locks: list[Path] = []
    try:
        for output in outputs:
            output.parent.mkdir(parents=True, exist_ok=True)
            if output.is_symlink() or output.exists():
                raise ValueError(f"capture output path already exists: {output}")
            lock = output.with_name(f".{output.name}.eval-lock")
            try:
                descriptor = os.open(
                    lock,
                    os.O_CREAT | os.O_EXCL | os.O_WRONLY,
                    0o600,
                )
            except FileExistsError as error:
                raise ValueError(
                    f"capture output path is already reserved: {output}"
                ) from error
            os.close(descriptor)
            locks.append(lock)
            if output.is_symlink() or output.exists():
                raise ValueError(f"capture output path already exists: {output}")
        yield
    finally:
        for lock in reversed(locks):
            lock.unlink(missing_ok=True)


def _preserve_allowed_outputs(
    workspace: Path,
    allowed_paths: object,
    evidence_directory: Path,
) -> tuple[Path, str]:
    """Copy a bounded non-symlink output set into evaluator-owned evidence."""
    if not isinstance(allowed_paths, list) or any(
        not isinstance(value, str) for value in allowed_paths
    ):
        raise ValueError("case.allowedWritePaths must be a list of relative paths")
    workspace = workspace.resolve()
    evidence_directory = evidence_directory.resolve()
    output_root = evidence_directory / "outputs"
    if output_root.exists() or output_root.is_symlink():
        raise ValueError("MCP output evidence destination must be unused")
    output_root.mkdir(mode=0o700)
    selected: dict[str, Path] = {}
    for value in allowed_paths:
        relative = PurePosixPath(value)
        if (
            not value
            or relative.is_absolute()
            or ".." in relative.parts
            or relative.as_posix() != value
        ):
            raise ValueError(f"allowed output path must be normalized and relative: {value}")
        source = workspace.joinpath(*relative.parts)
        if source.is_symlink():
            raise ValueError(f"allowed output path must not be a symlink: {value}")
        if not source.exists():
            continue
        pending = [source]
        while pending:
            candidate = pending.pop()
            if candidate.is_symlink():
                raise ValueError(
                    "allowed output evidence contains a symlink: "
                    + candidate.relative_to(workspace).as_posix()
                )
            if candidate.is_dir():
                pending.extend(sorted(candidate.iterdir(), reverse=True))
                continue
            if not candidate.is_file():
                raise ValueError(
                    "allowed output evidence contains a non-regular file: "
                    + candidate.relative_to(workspace).as_posix()
                )
            resolved = candidate.resolve()
            if workspace not in resolved.parents:
                raise ValueError("allowed output evidence escapes the disposable workspace")
            selected[candidate.relative_to(workspace).as_posix()] = candidate
    if len(selected) > _MAX_PRESERVED_OUTPUT_FILES:
        raise ValueError("allowed output evidence exceeds the file-count limit")
    total_size = sum(path.stat().st_size for path in selected.values())
    if total_size > _MAX_PRESERVED_OUTPUT_BYTES:
        raise ValueError("allowed output evidence exceeds the byte limit")
    records: list[dict[str, object]] = []
    for relative, source in sorted(selected.items()):
        content = source.read_bytes()
        destination = output_root.joinpath(*PurePosixPath(relative).parts)
        destination.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        destination.write_bytes(content)
        os.chmod(destination, 0o600)
        records.append({
            "path": relative,
            "size": len(content),
            "sha256": hashlib.sha256(content).hexdigest(),
        })
    manifest = {
        "schema": "dev-methodology-eval-output-manifest",
        "version": 1,
        "allowedWritePaths": allowed_paths,
        "files": records,
    }
    encoded = (
        json.dumps(manifest, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("utf-8")
    manifest_path = evidence_directory / "outputs-manifest.json"
    manifest_path.write_bytes(encoded)
    os.chmod(manifest_path, 0o600)
    return manifest_path, hashlib.sha256(encoded).hexdigest()


def _preserve_junie_agent_attribution(
    junie_home: Path,
    agent_id: str,
    evidence_directory: Path,
) -> tuple[str, Path, str]:
    """Retain bounded name-level Junie custom-agent lifecycle evidence."""
    session_root = junie_home / "sessions"
    relevant: dict[str, dict[str, object]] = {}
    if session_root.is_dir() and not session_root.is_symlink():
        for event_path in sorted(session_root.rglob("events.jsonl")):
            if event_path.is_symlink() or not event_path.is_file():
                continue
            if event_path.stat().st_size > _MAX_CAPTURE_REDACTION_BYTES:
                raise ValueError("Junie session event ledger exceeds the capture limit")
            current = event_path.parent
            while current != session_root:
                if current.is_symlink():
                    raise ValueError("Junie session event ledger uses a symlink")
                current = current.parent
            for line in event_path.read_text(encoding="utf-8").splitlines():
                try:
                    value = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if not isinstance(value, Mapping):
                    continue
                event = value.get("event")
                agent_event = event.get("agentEvent") if isinstance(event, Mapping) else None
                agent = agent_event.get("agent") if isinstance(agent_event, Mapping) else None
                if (
                    not isinstance(agent_event, Mapping)
                    or agent_event.get("kind") != "CustomAgentBlockUpdatedEvent"
                    or not isinstance(agent, Mapping)
                    or agent.get("kind") != "CustomAgent"
                    or agent.get("name") != agent_id
                    or agent_event.get("name") != agent_id
                    or agent_event.get("status") not in {"STARTED", "FINISHED"}
                    or not isinstance(agent_event.get("stepId"), str)
                    or not re.fullmatch(
                        r"[A-Za-z0-9][A-Za-z0-9._:-]{7,127}",
                        str(agent_event.get("stepId")),
                    )
                ):
                    continue
                step_id = str(agent_event["stepId"])
                record = relevant.setdefault(step_id, {
                    "stepId": step_id,
                    "statuses": [],
                    "eventDigests": [],
                })
                statuses = record["statuses"]
                event_digests = record["eventDigests"]
                assert isinstance(statuses, list)
                assert isinstance(event_digests, list)
                status = str(agent_event["status"])
                if status not in statuses:
                    statuses.append(status)
                line_digest = hashlib.sha256(line.encode("utf-8")).hexdigest()
                if line_digest not in event_digests:
                    event_digests.append(line_digest)
    complete = [
        record
        for record in relevant.values()
        if set(record["statuses"]) == {"STARTED", "FINISHED"}
    ]
    if len(complete) > 1:
        raise ValueError("Junie session ledger contains multiple matching custom-agent lifecycles")
    status = "name-verified" if len(complete) == 1 else "unverified"
    payload = {
        "schema": "dev-methodology-eval-junie-agent-attribution",
        "version": 1,
        "agentId": agent_id,
        "status": status,
        "definitionDigestBound": False,
        "lifecycle": complete[0] if complete else None,
    }
    encoded = (
        json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("utf-8")
    path = evidence_directory / "junie-agent-attribution.json"
    path.write_bytes(encoded)
    os.chmod(path, 0o600)
    return status, path, hashlib.sha256(encoded).hexdigest()


def _approved_environment_redactions(names: Iterable[str]) -> dict[str, str]:
    """Return non-empty explicitly approved environment values for capture scrubbing."""

    return {
        name: os.environ[name]
        for name in dict.fromkeys(names)
        if os.environ.get(name)
    }


def _load_codex_auth_file(
    path: Path,
    workspace: Path,
    evidence_root: Path,
) -> bytes:
    """Load one tightly permissioned Codex authentication file without retaining it."""
    if path.is_symlink():
        raise ValueError("Codex authentication source must be a regular non-symlink file")
    resolved = path.expanduser().resolve()
    if not resolved.is_file() or resolved.stat().st_size > 1024 * 1024:
        raise ValueError("Codex authentication source must be a bounded regular file")
    if (
        resolved == workspace
        or workspace in resolved.parents
        or resolved == evidence_root
        or evidence_root in resolved.parents
    ):
        raise ValueError("Codex authentication source must stay outside workspace and evidence roots")
    if resolved.stat().st_mode & 0o077:
        raise ValueError("Codex authentication source must not grant group or other permissions")
    content = resolved.read_bytes()
    try:
        value = json.loads(content)
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ValueError("Codex authentication source must contain valid JSON") from error
    if not isinstance(value, Mapping):
        raise ValueError("Codex authentication source must contain a JSON mapping")
    return content


def _redact_approved_environment(
    text: str,
    redactions: Mapping[str, str],
) -> str:
    """Remove approved environment values from one captured text artifact."""

    result = text
    values = sorted(redactions.items(), key=lambda item: (-len(item[1]), item[0]))
    for name, value in values:
        placeholder = f"[REDACTED_APPROVED_ENV:{name}]"
        result = result.replace(value, placeholder)
        escaped = json.dumps(value)[1:-1]
        if escaped != value:
            result = result.replace(escaped, placeholder)
    return result


def _redact_capture_file(path: Path, redactions: Mapping[str, str]) -> None:
    """Scrub a bounded regular capture file before it is parsed, printed, or retained."""

    if not (path.exists() or path.is_symlink()):
        return
    if path.is_symlink() or not path.is_file():
        path.unlink(missing_ok=True)
        raise ValueError(f"capture output must be a regular non-symlink file: {path}")
    if path.stat().st_size > _MAX_CAPTURE_REDACTION_BYTES:
        path.unlink()
        raise ValueError(f"capture output exceeded the redaction size limit and was removed: {path}")
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        path.unlink(missing_ok=True)
        raise ValueError(f"capture output could not be safely redacted and was removed: {path}") from error
    if not redactions:
        return
    redacted = _redact_approved_environment(text, redactions)
    if redacted == text:
        return
    temporary = path.with_name(f".{path.name}.redacted-{os.getpid()}")
    try:
        descriptor = os.open(
            temporary,
            os.O_CREAT | os.O_EXCL | os.O_WRONLY,
            0o600,
        )
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(redacted)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def _select_cases(
    cases: Mapping[str, dict[str, object]],
    case_id: str | None,
    skill_probe: str | None,
    agent_scenario: str | None,
    workflow_pack: str | None,
) -> list[dict[str, object]]:
    selectors = [value for value in (case_id, skill_probe, agent_scenario, workflow_pack) if value]
    if len(selectors) > 1:
        raise ValueError("select only one of --case, --skill-probe, or --agent-scenario")
    if case_id:
        if case_id not in cases:
            raise ValueError(f"unknown case: {case_id}")
        return [cases[case_id]]
    if skill_probe:
        linked = _linked_cases("skill-probes.yaml", skill_probe)
        return _cases_for_ids(cases, linked, f"skill probe {skill_probe}")
    if agent_scenario:
        linked = _linked_cases("agent-scenarios.yaml", agent_scenario)
        return _cases_for_ids(cases, linked, f"agent scenario {agent_scenario}")
    if workflow_pack:
        linked = _linked_cases("workflow-packs.yaml", workflow_pack)
        return _cases_for_ids(cases, linked, f"workflow pack {workflow_pack}")
    return list(cases.values())


def _linked_cases(filename: str, selector: str) -> set[str]:
    catalogs = load_framework_catalogs()  # noqa: F405
    catalog = catalogs.get(filename)
    if catalog is None:
        raise ValueError(f"catalog is missing: {filename}")
    matches = _find_catalog_entries(catalog, selector)
    if not matches:
        raise ValueError(f"unknown catalog selector in {filename}: {selector}")
    linked: set[str] = set()
    for match in matches:
        linked.update(_collect_linked_cases(match))
    if not linked:
        raise ValueError(f"catalog selector has no executable cases: {selector}")
    return linked


def _apply_probe_variant(
    case: Mapping[str, object],
    probe_id: str,
    variant: str,
) -> dict[str, object]:
    catalogs = load_framework_catalogs()  # noqa: F405
    matches = _find_catalog_entries(catalogs.get("skill-probes.yaml", {}), probe_id)
    if len(matches) != 1:
        raise ValueError(f"skill probe must resolve exactly once: {probe_id}")
    probe = matches[0]
    target = probe.get("skill")
    ablation = probe.get("ablation")
    wrong = ablation.get("wrongSkillControl") if isinstance(ablation, Mapping) else probe.get("wrongSkillControl")
    if not isinstance(target, str) or not isinstance(wrong, str):
        raise ValueError(f"skill probe lacks target or wrong-skill control: {probe_id}")
    treatment = list(case.get("requiredSkills", []))
    if target not in treatment:
        raise ValueError(f"skill probe target is not in case.requiredSkills: {probe_id}/{case.get('id')}")
    if variant == "treatment":
        execution_skills = treatment
    elif variant == "target-omitted":
        execution_skills = [skill for skill in treatment if skill != target]
    else:
        execution_skills = [skill for skill in treatment if skill != target]
        if wrong not in execution_skills:
            execution_skills.append(wrong)
    derived = dict(case)
    derived["probeId"] = probe_id
    derived["probeVariant"] = variant
    derived["executionSkills"] = execution_skills
    derived["probeComparisonKey"] = mapping_digest({  # noqa: F405
        "case": str(case.get("id")),
        "caseDefinitionDigest": case_definition_digest(case),  # noqa: F405
        "probe": probe_id,
    })
    mcp_contract = derived.get("mcpAgentOps")
    treatment_only_mcp = (
        isinstance(mcp_contract, Mapping)
        and mcp_contract.get("enablement") == "probe-treatment-only"
    )
    if variant != "treatment" or not treatment_only_mcp:
        derived.pop("mcpAgentOps", None)
    if variant in {"target-omitted", "wrong-skill"}:
        forbidden_skills = list(derived.get("forbiddenSkills", []))
        if target not in forbidden_skills:
            forbidden_skills.append(target)
        derived["forbiddenSkills"] = forbidden_skills
    return derived


def _find_catalog_entries(value: object, selector: str) -> list[Mapping[str, object]]:
    matches: list[Mapping[str, object]] = []
    if isinstance(value, Mapping):
        if value.get("id") == selector:
            matches.append(value)
        for item in value.values():
            matches.extend(_find_catalog_entries(item, selector))
    elif isinstance(value, list):
        for item in value:
            matches.extend(_find_catalog_entries(item, selector))
    return matches


def _collect_linked_cases(value: object) -> set[str]:
    linked: set[str] = set()
    if isinstance(value, Mapping):
        for key, item in value.items():
            if key == "executableCases" and isinstance(item, list):
                linked.update(candidate for candidate in item if isinstance(candidate, str))
            else:
                linked.update(_collect_linked_cases(item))
    elif isinstance(value, list):
        for item in value:
            linked.update(_collect_linked_cases(item))
    return linked


def _cases_for_ids(
    cases: Mapping[str, dict[str, object]],
    linked: Iterable[str],
    label: str,
) -> list[dict[str, object]]:
    missing = sorted(set(linked) - set(cases))
    if missing:
        raise ValueError(f"{label} references missing cases: {', '.join(missing)}")
    return [cases[case_id] for case_id in sorted(set(linked))]


def _parse_toolchain(values: list[str]) -> dict[str, str]:
    toolchain: dict[str, str] = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"toolchain value must use NAME=VERSION: {value}")
        name, version = value.split("=", 1)
        if not name or not version:
            raise ValueError(f"toolchain value must use NAME=VERSION: {value}")
        toolchain[name] = version
    return toolchain


def _workspace_manager(args: argparse.Namespace) -> object | None:
    if (args.prepare or args.print_invocation or args.invoke_harness) and args.prepared_cache is None:
        args.prepared_cache = Path(tempfile.gettempdir()) / "dev-methodology-evals" / "prepared"
    if args.prepared_cache is None:
        return None
    runs_root = args.workspace_root or args.prepared_cache.parent / "runs"
    return PreparedWorkspaceManager(  # noqa: F405
        args.prepared_cache,
        runs_root,
        integrity_mode="full" if args.invoke_harness else "source",
    )


def _trusted_output_schema(path: Path | None) -> Path | None:
    """Resolve the digest-bound evaluator-owned Codex JSON Schema."""

    if path is None:
        return None
    return validate_codex_output_schema(path)  # noqa: F405


def _prepare_projection_verifier_command(
    case: Mapping[str, object],
    projection: ModelVisibleProjection,
    package: ProjectionEvidenceDirectory,
) -> TrustedProjectionVerifier:
    """Normalize one exact catalog verifier into a digest-bound evaluator-owned script."""

    case_id = case.get("id")
    catalog_case = load_cases().get(str(case_id))  # noqa: F405
    if (
        case_id not in {
            "terminology-standard-effect",
            "terminology-standard-negative-activation",
        }
        or not isinstance(catalog_case, Mapping)
        or case.get("verify") != catalog_case.get("verify")
    ):
        raise ValueError(
            "trusted projection verifier is not an exact governed catalog command"
        )
    governed = command_spec(case.get("verify"))  # noqa: F405
    if governed.inherit_environment or governed.environment:
        raise ValueError("trusted projection verifier cannot inherit or add environment values")
    governed_argv = tuple(governed.argv)
    if governed_argv[0] != "python3":
        raise ValueError("trusted projection verifier must use the governed Python interpreter")

    source_kind: str
    source_path: str
    semantic_result_field: str
    semantic_red_exit_code: int | None
    if (
        case_id == "terminology-standard-effect"
        and len(governed_argv) == 3
        and governed_argv[1] == "-c"
    ):
        source_kind = "case-inline-normalized"
        source_path = "case.verify.argv[2]"
        source_content = governed_argv[2].encode("utf-8")
        execution_content = source_content
        semantic_result_field = "passed"
        semantic_red_exit_code = 3
    elif (
        case_id == "terminology-standard-negative-activation"
        and governed_argv == ("python3", "verify.py", "preserved-evidence.md")
        and any(
            _relative_path_contains_for_projection("verify.py", selected)
            for selected in projection.evaluator_only_paths
        )
    ):
        source_kind = "evaluator-only-source"
        source_path = "verify.py"
        source = projection.source_root / source_path
        if source.is_symlink() or not source.is_file():
            raise ValueError("trusted projection verifier source is missing or unsafe")
        source_content = source.read_bytes()
        expected = next(
            (entry for entry in projection.source_files if entry.path == source_path),
            None,
        )
        if (
            expected is None
            or expected.type != "file"
            or expected.digest != hashlib.sha256(source_content).hexdigest()
            or expected.size != len(source_content)
        ):
            raise ValueError("trusted projection verifier source differs from the prepared snapshot")
        original_file = source_path
        execution_content = (
            "import sys\n"
            f"sys.argv = {json.dumps([source_path, *governed_argv[2:]])}\n"
            f"__file__ = {json.dumps(original_file)}\n"
        ).encode("utf-8") + source_content
        semantic_result_field = "exactBytesPreserved"
        semantic_red_exit_code = None
    else:
        raise ValueError(
            "trusted projection verifier command is not one of the two governed forms"
        )

    interpreter_value = shutil.which("python3")
    if interpreter_value is None:
        raise ValueError("trusted projection verifier Python interpreter is unavailable")
    interpreter = Path(interpreter_value).resolve(strict=True)
    if not interpreter.is_file():
        raise ValueError("trusted projection verifier Python interpreter is not a file")
    interpreter_digest = hashlib.sha256(interpreter.read_bytes()).hexdigest()
    source_digest = hashlib.sha256(source_content).hexdigest()
    execution_script_digest = hashlib.sha256(execution_content).hexdigest()
    script_path = package.path("trusted-verifier.py")
    _write_owner_only_bytes(script_path, execution_content)
    source_evidence_path = package.path("trusted-verifier-source.json")
    source_marker = "dev-methodology-eval-projection-verifier-source"
    _write_owner_only_json(
        source_evidence_path,
        {
            "schema": source_marker,
            "version": 1,
            "kind": source_kind,
            "path": source_path,
            "digest": source_digest,
            "size": len(source_content),
            "contentBase64": base64.b64encode(source_content).decode("ascii"),
        },
    )
    source_evidence = package.reference(source_evidence_path, source_marker)
    contract_payload = {
        "schema": "dev-methodology-eval-projection-verifier-command",
        "version": 1,
        "case": case_id,
        "governedArgv": list(governed_argv),
        "interpreterName": "python3",
        "interpreterDigest": interpreter_digest,
        "sourceKind": source_kind,
        "sourcePath": source_path,
        "sourceDigest": source_digest,
        "sourceSize": len(source_content),
        "sourceEvidence": source_evidence,
        "executionScriptDigest": execution_script_digest,
        "semanticResultField": semantic_result_field,
        "semanticRedExitCode": semantic_red_exit_code,
    }
    contract_digest = hashlib.sha256(
        json.dumps(contract_payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    trusted = TrustedProjectionVerifier(
        specification=command_spec([str(interpreter), str(script_path)]),  # noqa: F405
        governed_argv=governed_argv,
        interpreter_name="python3",
        interpreter_digest=interpreter_digest,
        source_kind=source_kind,
        source_path=source_path,
        source_digest=source_digest,
        source_size=len(source_content),
        source_evidence=source_evidence,
        script_path=script_path,
        execution_script_digest=execution_script_digest,
        contract_digest=contract_digest,
        semantic_result_field=semantic_result_field,
        semantic_red_exit_code=semantic_red_exit_code,
    )
    _validate_projection_verifier_command(trusted.specification, projection, trusted)
    return trusted


def _validate_projection_verifier_command(
    specification: object,
    projection: ModelVisibleProjection,
    trusted: TrustedProjectionVerifier,
) -> None:
    """Require the exact normalized interpreter and evaluator-owned script command."""

    expected_argv = tuple(trusted.specification.argv)
    argv = tuple(specification.argv)
    valid = (
        argv == expected_argv
        and len(argv) == 2
        and Path(argv[0]).resolve() == Path(expected_argv[0]).resolve()
        and Path(argv[1]).resolve() == trusted.script_path.resolve()
        and not specification.inherit_environment
        and not specification.environment
    )
    if not valid:
        raise ValueError(
            "trusted projection verifier must match the exact evaluator-owned command contract"
        )
    if any(argument in {"-c", "-e", "-m"} or argument.startswith("-") for argument in argv):
        raise ValueError(
            "trusted projection verifier must match the exact evaluator-owned command contract"
        )
    if any(_projection_argument_is_model_write_path(argument, projection) for argument in argv):
        raise ValueError(
            "trusted projection verifier must match the exact evaluator-owned command contract"
        )
    interpreter = Path(argv[0])
    if (
        interpreter.is_symlink()
        or not interpreter.is_file()
        or hashlib.sha256(interpreter.read_bytes()).hexdigest()
        != trusted.interpreter_digest
    ):
        raise ValueError("trusted projection verifier interpreter identity changed before execution")
    if (
        trusted.script_path.is_symlink()
        or not trusted.script_path.is_file()
        or hashlib.sha256(trusted.script_path.read_bytes()).hexdigest()
        != trusted.execution_script_digest
    ):
        raise ValueError("trusted projection verifier script identity changed before execution")


def _projection_argument_is_model_write_path(
    argument: str,
    projection: ModelVisibleProjection,
) -> bool:
    candidate = Path(argument)
    if candidate.is_absolute():
        for root in (projection.source_root, projection.root):
            try:
                relative = candidate.resolve().relative_to(root)
            except ValueError:
                continue
            candidate = relative
            break
        else:
            return False
    relative = PurePosixPath(candidate.as_posix())
    if any(part in {"", ".", ".."} for part in relative.parts):
        return False
    return any(
        relative == selected or selected in relative.parents
        for selected in map(PurePosixPath, projection.sync_paths)
    )


def _relative_path_contains_for_projection(path: str, selected: str) -> bool:
    selected_path = PurePosixPath(selected)
    value = PurePosixPath(path)
    return selected_path.as_posix() == "." or value == selected_path or selected_path in value.parents


def _run_projection_verifier(
    case: Mapping[str, object],
    active_root: Path,
    specification: object,
    evidence_path: Path,
    redactions: Mapping[str, str],
    *,
    expected_fixture_digest: str,
    trusted: TrustedProjectionVerifier | None = None,
) -> tuple[dict[str, object], bool]:
    """Run and retain one evaluator-owned verifier against the full disposable fixture."""

    before = snapshot_product_tree(active_root)  # noqa: F405
    before_digest = snapshot_digest(before)  # noqa: F405
    if before_digest != expected_fixture_digest:
        raise ValueError(
            "trusted projection verifier pre-state differs from the post-sync fixture identity"
        )
    result = run_command(specification, active_root)  # noqa: F405
    after = snapshot_product_tree(active_root)  # noqa: F405
    stdout = _redact_approved_environment(result.stdout, redactions)
    stderr = _redact_approved_environment(result.stderr, redactions)
    control_observation = case.get("probeVariant") in {
        "target-omitted",
        "wrong-skill",
    }
    semantic_field = (
        trusted.semantic_result_field
        if trusted is not None
        else "passed"
    )
    semantic_result: Mapping[str, object] | None = None
    try:
        parsed = json.loads(stdout)
        if isinstance(parsed, Mapping) and isinstance(parsed.get(semantic_field), bool):
            semantic_result = parsed
    except json.JSONDecodeError:
        pass
    semantic_value = (
        semantic_result.get(semantic_field)
        if semantic_result is not None
        else None
    )
    red_exit_code = (
        trusted.semantic_red_exit_code
        if trusted is not None
        else 3
    )
    infrastructure_failure: str | None = None
    if result.exit_code == 124 and "timed out" in stderr:
        outcome = "infrastructure-failure"
        infrastructure_failure = "timeout"
    elif result.exit_code == 125 and "output exceeded" in stderr:
        outcome = "infrastructure-failure"
        infrastructure_failure = "output-cap"
    elif result.exit_code < 0:
        outcome = "infrastructure-failure"
        infrastructure_failure = "signal"
    elif result.exit_code not in {0, red_exit_code}:
        outcome = "infrastructure-failure"
        infrastructure_failure = "crash"
    elif semantic_result is None:
        outcome = "infrastructure-failure"
        infrastructure_failure = "malformed-result"
    elif result.exit_code == 0 and semantic_value is True:
        outcome = "semantic-green"
    elif (
        control_observation
        and red_exit_code is not None
        and result.exit_code == red_exit_code
        and semantic_value is False
    ):
        outcome = "semantic-red"
    else:
        outcome = "infrastructure-failure"
        infrastructure_failure = "malformed-result"
    command_contract = (
        _projection_verifier_contract_record(case, trusted)
        if trusted is not None
        else None
    )
    payload = {
        "schema": "dev-methodology-eval-projection-verification",
        "version": 2,
        "case": case["id"],
        "argv": list(trusted.governed_argv if trusted is not None else specification.argv),
        "commandContract": command_contract,
        "commandContractDigest": trusted.contract_digest if trusted is not None else None,
        "exitCode": result.exit_code,
        "passed": outcome == "semantic-green",
        "outcome": outcome,
        "infrastructureFailure": infrastructure_failure,
        "semanticResultDigest": (
            hashlib.sha256(
                json.dumps(
                    semantic_result,
                    sort_keys=True,
                    separators=(",", ":"),
                ).encode("utf-8")
            ).hexdigest()
            if semantic_result is not None
            else None
        ),
        "expectation": (
            "control-observation" if control_observation else "success-required"
        ),
        "expectedFixtureDigest": expected_fixture_digest,
        "fixtureDigestBefore": before_digest,
        "fixtureDigestAfter": snapshot_digest(after),  # noqa: F405
        "fixtureUnchanged": before == after,
        "stdout": stdout,
        "stderr": stderr,
    }
    _write_owner_only_json(evidence_path, payload)
    acceptable_outcome = (
        outcome == "semantic-red"
        if control_observation
        else outcome == "semantic-green"
    )
    return payload, acceptable_outcome and before == after


def _projection_verifier_contract_record(
    case: Mapping[str, object],
    trusted: TrustedProjectionVerifier,
) -> dict[str, object]:
    return {
        "schema": "dev-methodology-eval-projection-verifier-command",
        "version": 1,
        "case": case.get("id"),
        "governedArgv": list(trusted.governed_argv),
        "interpreterName": trusted.interpreter_name,
        "interpreterDigest": trusted.interpreter_digest,
        "sourceKind": trusted.source_kind,
        "sourcePath": trusted.source_path,
        "sourceDigest": trusted.source_digest,
        "sourceSize": trusted.source_size,
        "sourceEvidence": trusted.source_evidence,
        "executionScriptDigest": trusted.execution_script_digest,
        "semanticResultField": trusted.semantic_result_field,
        "semanticRedExitCode": trusted.semantic_red_exit_code,
    }


def _write_owner_only_bytes(path: Path, content: bytes) -> None:
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags, 0o600)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            descriptor = -1
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
    except Exception:
        if descriptor >= 0:
            os.close(descriptor)
        path.unlink(missing_ok=True)
        raise
    os.chmod(path, 0o600)


def _write_owner_only_json(path: Path, value: Mapping[str, object]) -> None:
    _write_owner_only_bytes(
        path,
        (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8"),
    )


def _handle_harness_invocation(
    args: argparse.Namespace,
    case: Mapping[str, object],
    active_root: Path,
) -> str | None:
    projection_contract = case.get("modelVisibleProjection")
    if projection_contract is None:
        return _handle_harness_invocation_in_workspace(
            args,
            case,
            active_root,
            active_root,
            None,
        )
    if (
        not isinstance(projection_contract, Mapping)
        or set(projection_contract)
        != {"schemaVersion", "mode", "evaluatorOnlyPaths"}
        or projection_contract.get("schemaVersion") != 1
        or projection_contract.get("mode") != "isolated-harness-workspace"
        or not isinstance(projection_contract.get("evaluatorOnlyPaths"), list)
        or any(
            not isinstance(path, str)
            for path in projection_contract.get("evaluatorOnlyPaths", [])
        )
    ):
        return "case.modelVisibleProjection is not the supported exact opt-in contract"
    model_visible_paths = case.get("modelVisiblePaths")
    allowed_write_paths = case.get("allowedWritePaths", [])
    ephemeral_write_paths = case.get("ephemeralWritePaths", [])
    if (
        not isinstance(model_visible_paths, list)
        or any(not isinstance(path, str) for path in model_visible_paths)
        or not isinstance(allowed_write_paths, list)
        or any(not isinstance(path, str) for path in allowed_write_paths)
        or not isinstance(ephemeral_write_paths, list)
        or any(not isinstance(path, str) for path in ephemeral_write_paths)
    ):
        return "model-visible projection requires validated path lists"
    try:
        marker = active_root / ".eval-workspace.json"
        if not marker.is_file() or marker.is_symlink():
            return "harness invocation requires a runner-owned disposable workspace"
        marker_value = json.loads(marker.read_text(encoding="utf-8"))
        prepared_snapshot_digest = (
            marker_value.get("preparedSnapshotDigest")
            if isinstance(marker_value, Mapping)
            else None
        )
        if (
            not isinstance(prepared_snapshot_digest, str)
            or not re.fullmatch(r"[0-9a-f]{64}", prepared_snapshot_digest)
        ):
            return "harness invocation workspace lacks a prepared snapshot identity"
        with tempfile.TemporaryDirectory(
            prefix=f".{case['id']}-{args.harness}-model-visible-",
            dir=active_root.parent,
        ) as container:
            projection = stage_model_visible_projection(
                active_root,
                Path(container) / "workspace",
                model_visible_paths,
                evaluator_only_paths=projection_contract["evaluatorOnlyPaths"],
                sync_paths=[*allowed_write_paths, *ephemeral_write_paths],
                prepared_snapshot_digest=prepared_snapshot_digest,
            )
            shutil.copy2(marker, projection.root / marker.name)
            return _handle_harness_invocation_in_workspace(
                args,
                case,
                active_root,
                projection.root,
                projection,
            )
    except (OSError, RuntimeError, ValueError) as error:
        return f"model-visible projection preflight failed: {error}"


def _handle_harness_invocation_in_workspace(
    args: argparse.Namespace,
    case: Mapping[str, object],
    active_root: Path,
    harness_root: Path,
    projection: ModelVisibleProjection | None,
) -> str | None:
    task_path = harness_root / str(case["task"])
    prompt = task_path.read_text(encoding="utf-8")
    agent_id = args.agent_id or next(iter(case.get("requiredAgents", [])), None)
    if not isinstance(agent_id, str):
        return "harness invocation requires an agent id"
    if not (harness_root / ".eval-workspace.json").is_file():
        return "harness invocation requires a runner-owned disposable workspace"
    if (harness_root / ".git").exists() and not is_evaluation_git_workspace(harness_root):  # noqa: F405
        return "harness invocation requires a disposable evaluation-owned Git workspace"
    default_evidence_root = Path(tempfile.gettempdir()).resolve() / "dev-methodology-evals" / "evidence"
    if default_evidence_root.is_symlink() or default_evidence_root.parent.is_symlink():
        return "runner-owned evidence root must not be a symlink"
    default_evidence_root.mkdir(parents=True, exist_ok=True)
    evidence_root = default_evidence_root.resolve()
    repository_root = ROOT.resolve()  # noqa: F405
    if evidence_root == repository_root or repository_root in evidence_root.parents:
        return "runner-owned evidence root must stay outside the evaluator repository"
    if args.prepared_cache is not None:
        prepared_cache = args.prepared_cache.resolve()
        if (
            evidence_root == prepared_cache
            or prepared_cache in evidence_root.parents
            or evidence_root in prepared_cache.parents
        ):
            return "runner-owned evidence root must be disjoint from the prepared cache"
    event_output = (
        args.event_output
        or evidence_root / f"{case['id']}-{args.harness}-{active_root.name}-events.jsonl"
    )
    event_output = event_output.resolve()
    projection_evidence_directory = None
    if projection is not None:
        package_path = (
            args.receipt_artifact_directory
            or event_output.with_name(f"{event_output.stem}-receipt-artifacts")
        )
        try:
            projection_evidence_directory = create_projection_evidence_directory(
                package_path,
                active_root,
                harness_root,
            )
        except ValueError as error:
            return f"projection receipt artifact packaging failed: {error}"
    mcp_audit_output = event_output.with_name(
        f"{event_output.stem}-mcp-audit.jsonl"
    )
    mcp_identity_output = event_output.with_name(
        f"{event_output.stem}-mcp-identity.json"
    )
    projection_sync_output = (
        projection_evidence_directory.path("projection-sync.json")
        if projection is not None
        else None
    )
    projection_manifest_output = (
        projection_evidence_directory.path("projection-manifest.json")
        if projection is not None
        else None
    )
    projection_verifier_output = (
        projection_evidence_directory.path("projection-verifier.json")
        if projection is not None
        else None
    )
    cache_dir = (
        event_output.parent
        / f".{case['id']}-{args.harness}-{active_root.name}-cache"
    )
    codex_auth_content: bytes | None = None
    codex_home: Path | None = None
    if args.codex_auth_file is not None:
        try:
            codex_auth_content = _load_codex_auth_file(
                args.codex_auth_file,
                active_root,
                evidence_root,
            )
        except ValueError as error:
            return f"Codex authentication preflight failed: {error}"
        codex_home = event_output.parent / f".codex-home-{active_root.name}"
    projection_verifier = None
    projection_verifier_specification = None
    try:
        output_schema = _trusted_output_schema(args.output_schema)
        if projection is not None:
            assert projection_evidence_directory is not None
            projection_verifier = _prepare_projection_verifier_command(
                case,
                projection,
                projection_evidence_directory,
            )
            projection_verifier_specification = projection_verifier.specification
        resource_allowlist = case.get("skillResourceAllowlist", {})
        if not isinstance(resource_allowlist, dict) or any(
            not isinstance(skill, str)
            or not isinstance(paths, list)
            or any(not isinstance(path, str) for path in paths)
            for skill, paths in resource_allowlist.items()
        ):
            return "case.skillResourceAllowlist must map skill ids to relative file lists"
        context_pack = ContextPackBuilder(ROOT).stage(  # noqa: F405
            args.harness,
            agent_id,
            list(case.get("executionSkills", case.get("requiredSkills", []))),
            harness_root,
            skill_files=resource_allowlist,
        )
        mcp_context = None
        required_tool_sequences: list[list[str]] = []
        required_tool_outcomes: dict[str, list[str]] = {}
        required_tool_argument_digests: dict[str, str] = {}
        permission_profile_host_home_digest: str | None = None
        if _case_uses_mcp_agent_ops(case):
            mcp_contract = case["mcpAgentOps"]
            assert isinstance(mcp_contract, Mapping)
            required_tool_sequences = [
                list(sequence)
                for sequence in mcp_contract["requiredToolSequences"]
            ]
            required_tool_outcomes = {
                str(tool): list(outcomes)
                for tool, outcomes in mcp_contract["requiredToolOutcomes"].items()
            }
            mcp_identity = capture_mcp_agent_ops_identity(  # noqa: F405
                args.mcp_agent_ops_executable,
                required_version=str(mcp_contract["requiredVersion"]),
                required_runtime_digest=str(mcp_contract["requiredRuntimeDigest"]),
            )
            if mcp_contract.get("schemaVersion") == 5:
                required_tool_argument_digests = resolve_mcp_tool_argument_digests(  # noqa: F405
                    mcp_contract["requiredToolArguments"],
                    harness_root,
                )
                mcp_context = stage_mcp_reference_context(  # noqa: F405
                    args.harness,
                    harness_root,
                    mcp_identity,
                    mcp_audit_output,
                    evidence_root,
                    reference_names=mcp_contract["referenceNames"],
                    enabled_tools=mcp_contract["enabledTools"],
                )
            else:
                available_skills = read_mcp_skill_catalog(  # noqa: F405
                    harness_root,
                    str(mcp_contract["skillCatalogSource"]),
                    ROOT,  # noqa: F405
                )
                staged_mcp_skill_root = (
                    harness_root / ".eval-context" / "mcp-agent-ops" / "skills"
                )
                required_tool_argument_digests = resolve_mcp_tool_argument_digests(  # noqa: F405
                    mcp_contract["requiredToolArguments"],
                    harness_root,
                    skill_root=staged_mcp_skill_root,
                )
                mcp_context = stage_mcp_agent_ops_context(  # noqa: F405
                    args.harness,
                    harness_root,
                    mcp_identity,
                    ROOT,  # noqa: F405
                    context_pack.skill_location,
                    available_skills,
                    list(case.get("executionSkills", case.get("requiredSkills", []))),
                    mcp_audit_output,
                    evidence_root,
                    catalog_resource_allowlist=mcp_contract[
                        "catalogResourceAllowlist"
                    ],
                    mcp_only_skill_ids=mcp_contract["mcpOnlySkills"],
                )
            if args.harness == "codex" and mcp_context.codex_permission_profile:
                permission_profile_host_home_digest = mcp_value_digest(  # noqa: F405
                    str(mcp_context.host_home)
                )
            mcp_identity_output = mcp_context.evidence_directory / "identity.json"
        allowed_paths = case.get("modelVisiblePaths", ["."])
        if not isinstance(allowed_paths, list) or any(not isinstance(path, str) for path in allowed_paths):
            return "case.modelVisiblePaths must be a list of relative paths"
        input_manifest = build_input_manifest(harness_root, allowed_paths)  # noqa: F405
        initialize_git_workspace(harness_root)  # noqa: F405
        harness_identity = capture_harness_identity(args.harness)  # noqa: F405
    except (RuntimeError, ValueError) as error:
        return f"model-visible context preflight failed: {error}"
    command = build_harness_command(  # noqa: F405
        args.harness,
        harness_root,
        agent_id,
        prompt,
        args.model,
        read_only=bool(case.get("readOnly")),
        event_output=event_output,
        evidence_root=evidence_root,
        isolated_config_root=harness_root,
        output_schema=output_schema,
        last_message_output=args.result,
        cache_dir=cache_dir,
        skill_locations=[context_pack.skill_location],
        agent_locations=[context_pack.agent_location],
        approved_environment_names=args.approved_env_name,
        harness_executable=harness_identity.executable,
        mcp_agent_ops=mcp_context,
        codex_home=codex_home,
    )
    if projection is not None:
        projection = seal_model_visible_projection(projection)
    execution_command = command
    projection_manifest_evidence = None
    if projection is not None and projection_manifest_output is not None:
        try:
            projection_manifest_evidence = write_model_visible_projection_manifest(
                projection,
                projection_manifest_output,
            )
        except (OSError, ValueError) as error:
            return f"model-visible projection evidence preflight failed: {error}"
    if args.print_invocation:
        invocation_record = {
            "harness": args.harness,
            "harnessVersion": harness_identity.version,
            "harnessDigest": harness_identity.content_digest,
            "modelDigest": mapping_digest({"harness": args.harness, "model": args.model}),  # noqa: F405
            "argv": list(execution_command.argv),
            "contextManifestDigest": context_pack.manifest_digest,
            "approvedInputManifestDigest": input_manifest.manifest_digest,
            "functionalIsolation": "pending-runtime-audit" if args.invoke_harness else "preflight-only",
            "executionTier": case.get("executionTier"),
            "riskLevel": (
                case.get("risk", {}).get("level")
                if isinstance(case.get("risk"), Mapping)
                else None
            ),
            "securityContainmentRequired": case.get("securityContainmentRequired"),
            "securityContained": False,
            "containmentLevel": "containment-unverified",
            "approvedEnvironmentNames": list(execution_command.host_environment_allowlist),
        }
        if projection is not None:
            assert projection_evidence_directory is not None
            invocation_record["modelVisibleProjection"] = {
                "mode": "isolated-harness-workspace",
                "preparedSnapshotDigest": projection.prepared_snapshot_digest,
                "sourceIdentityDigest": projection.source_identity_digest,
                "projectionManifestDigest": projection_manifest_evidence.manifest_digest,
                "projectionEvidence": projection_evidence_directory.reference(
                    projection_manifest_evidence.evidence_path,
                    "dev-methodology-eval-model-visible-projection",
                ),
                "projectionEvidenceDigest": (
                    projection_manifest_evidence.content_digest
                ),
                "projectedInputs": list(projection_manifest_evidence.projected_inputs),
                "evaluatorOnlyPaths": list(projection.evaluator_only_paths),
                "syncPaths": list(projection.sync_paths),
                "syncEvidenceStatus": (
                    "pending-runtime" if args.invoke_harness else "preflight-only"
                ),
            }
            invocation_record["receiptArtifactDirectory"] = str(
                projection_evidence_directory.root
            )
        if isinstance(case.get("probeId"), str):
            invocation_record["probeId"] = case["probeId"]
            invocation_record["probeVariant"] = case.get("probeVariant")
            invocation_record["probeComparisonKey"] = case.get("probeComparisonKey")
            invocation_record["executionSkills"] = list(case.get("executionSkills", []))
            invocation_record["probeEvidenceStatus"] = "unverified-until-comparable-three-variant-receipts"
        if mcp_context is not None:
            invocation_record["mcpAgentOps"] = {
                "serverName": mcp_context.server_name,
                "version": mcp_context.identity.version,
                "launcherDigest": mcp_context.identity.launcher_digest,
                "runtimeDigest": mcp_context.identity.runtime_digest,
                "identityDigest": mcp_context.identity.identity_digest,
                "configurationDigest": mcp_context.configuration_digest,
                "catalogManifestDigest": mcp_context.catalog_manifest_digest,
                "auditSessionId": mcp_context.audit_session_id,
                "requiredToolSequences": required_tool_sequences,
                "requiredToolOutcomes": required_tool_outcomes,
                "requiredToolArgumentDigests": required_tool_argument_digests,
                "permissionProfileHostHomeDigest": (
                    permission_profile_host_home_digest
                ),
                "toolEvidenceStatus": "pending-runtime",
            }
            if mcp_context.skill_root is not None:
                invocation_record["mcpAgentOps"]["skillRoot"] = (
                    mcp_context.skill_root.relative_to(harness_root).as_posix()
                )
        sandbox_profiles = case.get("sandboxProfiles")
        if isinstance(sandbox_profiles, Mapping) and args.harness in sandbox_profiles:
            profile_id = sandbox_profiles[args.harness]
            profiles_catalog = load_framework_catalogs().get("sandbox-profiles.yaml", {})  # noqa: F405
            profile = next(
                (
                    item
                    for item in profiles_catalog.get("profiles", [])
                    if isinstance(item, Mapping) and item.get("id") == profile_id
                ),
                None,
            )
            invocation_record["sandboxProfile"] = profile_id
            invocation_record["sandboxProfileDigest"] = (
                case_definition_digest(profile) if isinstance(profile, Mapping) else None  # noqa: F405
            )
        print(json.dumps(invocation_record, sort_keys=True))
    if not args.invoke_harness:
        return None
    event_output.parent.mkdir(parents=True, exist_ok=True)
    result_output = args.result.resolve() if args.result is not None else None
    if result_output is not None:
        result_output.parent.mkdir(parents=True, exist_ok=True)
    scratch_value = execution_command.environment.get("TMPDIR")
    scratch = Path(scratch_value) if isinstance(scratch_value, str) and scratch_value else None
    junie_home_value = execution_command.environment.get("JUNIE_HOME")
    junie_home = (
        Path(junie_home_value)
        if isinstance(junie_home_value, str) and junie_home_value
        else None
    )
    redactions = _approved_environment_redactions(args.approved_env_name)
    capture_paths = [event_output]
    if result_output is not None:
        capture_paths.append(result_output)
    if mcp_context is not None:
        capture_paths.extend((mcp_context.audit_log, mcp_identity_output))
    if projection_sync_output is not None:
        capture_paths.append(projection_sync_output)
    if projection_verifier_output is not None:
        capture_paths.append(projection_verifier_output)
    junie_attribution_status: str | None = None
    junie_attribution_path: Path | None = None
    junie_attribution_digest: str | None = None
    try:
        with _reserve_capture_paths(capture_paths):
            if mcp_context is not None:
                mcp_identity_output.write_text(
                    json.dumps(
                        {
                            "schema": "dev-methodology-eval-mcp-identity",
                            "version": 3,
                            "serverName": mcp_context.server_name,
                            "packageVersion": mcp_context.identity.version,
                            "launcherDigest": mcp_context.identity.launcher_digest,
                            "runtimeDigest": mcp_context.identity.runtime_digest,
                            "identityDigest": mcp_context.identity.identity_digest,
                            "configurationDigest": mcp_context.configuration_digest,
                            "catalogManifestDigest": mcp_context.catalog_manifest_digest,
                            "auditSessionId": mcp_context.audit_session_id,
                            "configurationEvidenceDigest": hashlib.sha256(
                                mcp_context.configuration_evidence.read_bytes()
                            ).hexdigest(),
                            "catalogEvidenceDigest": hashlib.sha256(
                                mcp_context.catalog_evidence.read_bytes()
                            ).hexdigest(),
                            "authorizationDigest": mcp_context.authorization_digest,
                            "requiredToolArgumentDigests": (
                                required_tool_argument_digests
                            ),
                            "permissionProfileHostHomeDigest": (
                                permission_profile_host_home_digest
                            ),
                        },
                        sort_keys=True,
                    )
                    + "\n",
                    encoding="utf-8",
                )
                os.chmod(mcp_identity_output, 0o600)
            if scratch is not None:
                scratch.mkdir(parents=True, exist_ok=True)
            if junie_home is not None:
                if junie_home.exists() or junie_home.is_symlink():
                    raise ValueError("isolated Junie home must be an unused non-symlink path")
                junie_home.mkdir(mode=0o700)
                if mcp_context is not None:
                    if mcp_context.authorization_evidence is None:
                        raise ValueError("Junie MCP execution requires an authorization policy")
                    allowlist = junie_home / "allowlist.json"
                    allowlist.write_bytes(
                        mcp_context.authorization_evidence.read_bytes()
                    )
                    os.chmod(allowlist, 0o600)
            if codex_home is not None and codex_auth_content is not None:
                codex_home.mkdir(mode=0o700)
                auth_destination = codex_home / "auth.json"
                auth_destination.write_bytes(codex_auth_content)
                os.chmod(auth_destination, 0o600)
            try:
                result = run_command(execution_command, harness_root)  # noqa: F405
                if junie_home is not None and mcp_context is not None:
                    (
                        junie_attribution_status,
                        junie_attribution_path,
                        junie_attribution_digest,
                    ) = _preserve_junie_agent_attribution(
                        junie_home,
                        agent_id,
                        mcp_context.evidence_directory,
                    )
            finally:
                if scratch is not None and scratch.is_dir():
                    shutil.rmtree(scratch)
                if cache_dir.is_dir():
                    shutil.rmtree(cache_dir)
                if junie_home is not None and junie_home.is_dir():
                    shutil.rmtree(junie_home)
                if codex_home is not None and codex_home.is_dir():
                    shutil.rmtree(codex_home)
            if args.harness == "codex":
                event_output.write_text(
                    _redact_approved_environment(result.stdout, redactions),
                    encoding="utf-8",
                )
            else:
                _redact_capture_file(event_output, redactions)
            if result_output is not None:
                _redact_capture_file(result_output, redactions)
            stderr = _redact_approved_environment(result.stderr, redactions)
            if stderr:
                print(
                    stderr,
                    file=sys.stderr,
                    end="" if stderr.endswith("\n") else "\n",
                )
            if projection is not None and projection_sync_output is not None:
                projection_sync = synchronize_model_visible_projection(
                    projection,
                    projection_sync_output,
                    projection_manifest=projection_manifest_evidence,
                )
            if not result.passed:
                return f"{args.harness} invocation failed with exit code {result.exit_code}"
            if (
                projection is not None
                and projection_verifier_output is not None
                and projection_verifier_specification is not None
            ):
                verifier_record, verifier_acceptable = _run_projection_verifier(
                    case,
                    active_root,
                    projection_verifier_specification,
                    projection_verifier_output,
                    redactions,
                    expected_fixture_digest=(
                        projection_sync.post_sync_source_identity_digest
                    ),
                    trusted=projection_verifier,
                )
                assert projection_sync is not None
                assert projection_evidence_directory is not None
                projection_record = {
                    "mode": "isolated-harness-workspace",
                    "preparedSnapshotDigest": projection.prepared_snapshot_digest,
                    "sourceIdentityDigest": projection.source_identity_digest,
                    "postSyncSourceIdentityDigest": (
                        projection_sync.post_sync_source_identity_digest
                    ),
                    "projectionManifestDigest": projection_manifest_evidence.manifest_digest,
                    "projectionEvidence": projection_evidence_directory.reference(
                        projection_manifest_evidence.evidence_path,
                        "dev-methodology-eval-model-visible-projection",
                    ),
                    "projectionEvidenceDigest": (
                        projection_manifest_evidence.content_digest
                    ),
                    "projectedInputs": list(projection_manifest_evidence.projected_inputs),
                    "evaluatorOnlyPaths": list(projection.evaluator_only_paths),
                    "syncPaths": list(projection.sync_paths),
                    "syncEvidence": projection_evidence_directory.reference(
                        projection_sync.evidence_path,
                        "dev-methodology-eval-model-visible-projection-sync",
                    ),
                    "syncEvidenceDigest": hashlib.sha256(
                        projection_sync.evidence_path.read_bytes()
                    ).hexdigest(),
                    "syncManifestDigest": projection_sync.manifest_digest,
                    "createdDirectories": list(
                        projection_sync.created_directories
                    ),
                    "mutations": list(projection_sync.mutation_records),
                    "evaluatorVerificationEvidence": projection_evidence_directory.reference(
                        projection_verifier_output,
                        "dev-methodology-eval-projection-verification",
                    ),
                    "evaluatorVerificationEvidenceDigest": hashlib.sha256(
                        projection_verifier_output.read_bytes()
                    ).hexdigest(),
                    "evaluatorVerificationStatus": verifier_record["outcome"],
                    "evaluatorVerificationExitCode": verifier_record["exitCode"],
                    "evaluatorVerificationExpectation": verifier_record[
                        "expectation"
                    ],
                    "evaluatorVerificationCommandDigest": (
                        projection_verifier.contract_digest
                    ),
                    "syncEvidenceStatus": "applied-and-recorded",
                }
                print(json.dumps({
                    "case": case["id"],
                    "receiptArtifactDirectory": str(
                        projection_evidence_directory.root
                    ),
                    "modelVisibleProjection": projection_record,
                }, sort_keys=True))
                if not verifier_acceptable:
                    if verifier_record["fixtureUnchanged"] is not True:
                        return "trusted full-fixture verifier changed the fixture"
                    return (
                        "trusted full-fixture verifier did not produce an acceptable "
                        f"semantic outcome: {verifier_record['outcome']}"
                    )
            if (
                args.harness == "codex"
                and result_output is not None
                and (
                    not result_output.is_file()
                    or result_output.stat().st_size == 0
                )
            ):
                return "captured Codex final response is missing or empty"
            events = read_harness_event_stream(args.harness, event_output)  # noqa: F405
            if args.harness == "junie":
                final_response = extract_harness_final_response("junie", events)  # noqa: F405
                if result_output is not None:
                    result_output.write_text(final_response, encoding="utf-8")
            if mcp_context is not None:
                output_manifest, output_manifest_digest = _preserve_allowed_outputs(
                    harness_root,
                    case.get("allowedWritePaths", []),
                    mcp_context.evidence_directory,
                )
                audit_records = read_mcp_agent_ops_audit(mcp_context.audit_log)  # noqa: F405
                session_ids = {
                    str(record.get("sessionId")) for record in audit_records
                }
                if session_ids != {mcp_context.audit_session_id}:
                    return "captured MCP tool audit session does not match the staged run"
                selected_stream, completed_tools, tool_outcomes = select_mcp_tool_stream(  # noqa: F405
                    audit_records,
                    required_tool_sequences,
                    required_tool_outcomes,
                    required_tool_argument_digests,
                )
                identity_digest = hashlib.sha256(
                    mcp_identity_output.read_bytes()
                ).hexdigest()
                print(json.dumps({
                    "case": case["id"],
                    "mcpAgentOps": {
                        "serverName": mcp_context.server_name,
                        "version": mcp_context.identity.version,
                        "launcherDigest": mcp_context.identity.launcher_digest,
                        "runtimeDigest": mcp_context.identity.runtime_digest,
                        "identityDigest": mcp_context.identity.identity_digest,
                        "configurationDigest": mcp_context.configuration_digest,
                        "catalogManifestDigest": mcp_context.catalog_manifest_digest,
                        "auditSessionId": mcp_context.audit_session_id,
                        "auditStreamId": selected_stream,
                        "auditDigest": hashlib.sha256(
                            mcp_context.audit_log.read_bytes()
                        ).hexdigest(),
                        "auditEvidence": str(mcp_context.audit_log),
                        "identityEvidence": str(mcp_identity_output),
                        "identityEvidenceDigest": identity_digest,
                        "configurationEvidence": str(
                            mcp_context.configuration_evidence
                        ),
                        "catalogEvidence": str(mcp_context.catalog_evidence),
                        "catalogEvidenceDigest": hashlib.sha256(
                            mcp_context.catalog_evidence.read_bytes()
                        ).hexdigest(),
                        "authorizationEvidence": (
                            str(mcp_context.authorization_evidence)
                            if mcp_context.authorization_evidence is not None
                            else None
                        ),
                        "authorizationDigest": mcp_context.authorization_digest,
                        "outputManifestEvidence": str(output_manifest),
                        "outputManifestDigest": output_manifest_digest,
                        "resultEvidence": (
                            str(result_output) if result_output is not None else None
                        ),
                        "junieAgentAttributionStatus": junie_attribution_status,
                        "junieAgentAttributionEvidence": (
                            str(junie_attribution_path)
                            if junie_attribution_path is not None
                            else None
                        ),
                        "junieAgentAttributionDigest": junie_attribution_digest,
                        "completedTools": completed_tools,
                        "toolOutcomes": tool_outcomes,
                        "requiredToolSequences": required_tool_sequences,
                        "requiredToolOutcomes": required_tool_outcomes,
                        "requiredToolArgumentDigests": (
                            required_tool_argument_digests
                        ),
                        "permissionProfileHostHomeDigest": (
                            permission_profile_host_home_digest
                        ),
                        "toolEvidenceStatus": "verified",
                    },
                }, sort_keys=True))
    except ValueError as error:
        return str(error)
    return None


if __name__ == "__main__":
    raise SystemExit(main())
