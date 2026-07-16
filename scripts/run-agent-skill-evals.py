#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Modified with AI assistance.
# Summary: Provides the CLI and compatibility API for agent and skill evaluation execution.

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import tempfile
from contextlib import contextmanager, nullcontext
from pathlib import Path
from typing import Iterable, Iterator, Mapping

import yaml

try:
    from agent_skill_evals import *  # noqa: F403
except ModuleNotFoundError:
    from scripts.agent_skill_evals import *  # type: ignore[no-redef]  # noqa: F403

try:
    from agent_skill_judge_contract import canonical_judge_identity
except ModuleNotFoundError:
    from scripts.agent_skill_judge_contract import canonical_judge_identity


_MAX_CAPTURE_REDACTION_BYTES = 10 * 1024 * 1024


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
                for item in load_framework_catalogs()["judges.yaml"].get(
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
            if args.result is not None or args.evidence is not None:
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


def _approved_environment_redactions(names: Iterable[str]) -> dict[str, str]:
    """Return non-empty explicitly approved environment values for capture scrubbing."""

    return {
        name: os.environ[name]
        for name in dict.fromkeys(names)
        if os.environ.get(name)
    }


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


def _handle_harness_invocation(
    args: argparse.Namespace,
    case: Mapping[str, object],
    active_root: Path,
) -> str | None:
    task_path = active_root / str(case["task"])
    prompt = task_path.read_text(encoding="utf-8")
    agent_id = args.agent_id or next(iter(case.get("requiredAgents", [])), None)
    if not isinstance(agent_id, str):
        return "harness invocation requires an agent id"
    if not (active_root / ".eval-workspace.json").is_file():
        return "harness invocation requires a runner-owned disposable workspace"
    if (active_root / ".git").exists() and not is_evaluation_git_workspace(active_root):  # noqa: F405
        return "harness invocation requires a disposable evaluation-owned Git workspace"
    default_evidence_root = Path(tempfile.gettempdir()).resolve() / "dev-methodology-evals" / "evidence"
    if default_evidence_root.is_symlink() or default_evidence_root.parent.is_symlink():
        return "runner-owned evidence root must not be a symlink"
    default_evidence_root.mkdir(parents=True, exist_ok=True)
    evidence_root = default_evidence_root.resolve()
    repository_root = ROOT.resolve()
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
    cache_dir = (
        event_output.parent
        / f".{case['id']}-{args.harness}-{active_root.name}-cache"
    )
    try:
        output_schema = _trusted_output_schema(args.output_schema)
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
            active_root,
            skill_files=resource_allowlist,
        )
        allowed_paths = case.get("modelVisiblePaths", ["."])
        if not isinstance(allowed_paths, list) or any(not isinstance(path, str) for path in allowed_paths):
            return "case.modelVisiblePaths must be a list of relative paths"
        input_manifest = build_input_manifest(active_root, allowed_paths)  # noqa: F405
        initialize_git_workspace(active_root)  # noqa: F405
        harness_identity = capture_harness_identity(args.harness)  # noqa: F405
    except (RuntimeError, ValueError) as error:
        return f"model-visible context preflight failed: {error}"
    command = build_harness_command(  # noqa: F405
        args.harness,
        active_root,
        agent_id,
        prompt,
        args.model,
        read_only=bool(case.get("readOnly")),
        event_output=event_output,
        evidence_root=evidence_root,
        isolated_config_root=active_root,
        output_schema=output_schema,
        last_message_output=args.result if case.get("readOnly") else None,
        cache_dir=cache_dir,
        skill_locations=[context_pack.skill_location],
        agent_locations=[context_pack.agent_location],
        approved_environment_names=args.approved_env_name,
        harness_executable=harness_identity.executable,
    )
    event_output = event_output.resolve()
    execution_command = command
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
        if isinstance(case.get("probeId"), str):
            invocation_record["probeId"] = case["probeId"]
            invocation_record["probeVariant"] = case.get("probeVariant")
            invocation_record["probeComparisonKey"] = case.get("probeComparisonKey")
            invocation_record["executionSkills"] = list(case.get("executionSkills", []))
            invocation_record["probeEvidenceStatus"] = "unverified-until-comparable-three-variant-receipts"
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
    try:
        with _reserve_capture_paths(capture_paths):
            if scratch is not None:
                scratch.mkdir(parents=True, exist_ok=True)
            try:
                result = run_command(execution_command, active_root)  # noqa: F405
            finally:
                if scratch is not None and scratch.is_dir():
                    shutil.rmtree(scratch)
                if cache_dir.is_dir():
                    shutil.rmtree(cache_dir)
                if junie_home is not None and junie_home.is_dir():
                    shutil.rmtree(junie_home)
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
            if not result.passed:
                return f"{args.harness} invocation failed with exit code {result.exit_code}"
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
    except ValueError as error:
        return str(error)
    return None


if __name__ == "__main__":
    raise SystemExit(main())
