#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Modified with AI assistance.
# Summary: Builds truthful agent and skill evaluation coverage reports from catalogs and receipt classifications.

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from collections.abc import Sequence
from pathlib import Path
from types import ModuleType

import yaml


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "design" / "agent-skill-test-coverage-checklist.md"
EXPLORER_PATH = ROOT / "design" / "generated" / "agent-skill-explorer-data.js"
REGISTRY_PATH = (
    ROOT
    / "skills"
    / "detect-technology-skills"
    / "references"
    / "technology-skill-detection-registry.yaml"
)
EVAL_RUNNER_PATH = ROOT / "scripts" / "run-agent-skill-evals.py"

_SUPPORTED_HARNESSES = ("codex", "junie")
_CATALOG_FILES = {
    "cases": "cases.yaml",
    "skillProbes": "skill-probes.yaml",
    "agentScenarios": "agent-scenarios.yaml",
    "workflowPacks": "workflow-packs.yaml",
    "judges": "judges.yaml",
    "sandboxProfiles": "sandbox-profiles.yaml",
}
_COVERAGE_STATUSES = {"declared", "fixture-backed", "verified"}
_CATALOG_COVERAGE_STATUSES = _COVERAGE_STATUSES | {"mixed"}


def load_yaml(path: Path) -> dict[str, object]:
    """Load one required YAML mapping or raise a path-specific error."""
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected a mapping in {path}")
    return value


def role_skill_entries(role: dict[str, object]) -> list[tuple[str, str | None]]:
    """Return fixed and conditional skill references from one conceptual role."""
    value = role.get("skills")
    if not isinstance(value, list):
        raise ValueError(
            f"Conceptual agent definition {role.get('name')} skills must be a list."
        )
    entries: list[tuple[str, str | None]] = []
    for item in value:
        if isinstance(item, str):
            entries.append((item, None))
        elif isinstance(item, dict) and len(item) == 1:
            name, metadata = next(iter(item.items()))
            condition = metadata.get("condition") if isinstance(metadata, dict) else None
            entries.append(
                (str(name), str(condition) if condition is not None else None)
            )
        else:
            raise ValueError(
                f"Conceptual agent definition {role.get('name')} has an invalid skill entry: {item}"
            )
    return entries


def role_skill_names(role: dict[str, object]) -> list[str]:
    """Return skill identifiers referenced by one conceptual role."""
    return [name for name, _condition in role_skill_entries(role)]


def load_eval_runner(root: Path = ROOT) -> ModuleType:
    """Load the receipt validator and classifier owned by the evaluation runner."""
    path = root / "scripts" / "run-agent-skill-evals.py"
    spec = importlib.util.spec_from_file_location("run_agent_skill_evals", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load the agent-skill evaluation validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_skills(root: Path = ROOT) -> dict[str, str]:
    """Load the live bundled skill inventory and category assignments."""
    skills: dict[str, str] = {}
    for path in sorted((root / "skills").glob("*/SKILL.md")):
        parts = path.read_text(encoding="utf-8").split("---", 2)
        if len(parts) != 3:
            raise ValueError(f"Missing frontmatter in {path}")
        frontmatter = yaml.safe_load(parts[1])
        if not isinstance(frontmatter, dict):
            raise ValueError(f"Invalid frontmatter in {path}")
        name = str(frontmatter["name"])
        metadata = frontmatter.get("metadata", {})
        category = (
            str(metadata.get("category", "uncategorized"))
            if isinstance(metadata, dict)
            else "uncategorized"
        )
        skills[name] = category
    return skills


def load_roles(root: Path = ROOT) -> dict[str, dict[str, object]]:
    """Load the live conceptual agent inventory."""
    roles: dict[str, dict[str, object]] = {}
    for path in sorted((root / "agents" / "roles").glob("*/*.role.yaml")):
        role = load_yaml(path)
        role["_sourcePath"] = str(path.relative_to(root))
        roles[str(role["name"])] = role
    return roles


def _require_mapping(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a mapping")
    return value


def _require_list(value: object, label: str) -> list[object]:
    if not isinstance(value, list):
        raise ValueError(f"{label} must be a list")
    return value


def _string_list(value: object, label: str) -> list[str]:
    items = _require_list(value, label)
    if any(not isinstance(item, str) or not item for item in items):
        raise ValueError(f"{label} must contain non-empty strings")
    return [str(item) for item in items]


def _item_id(item: dict[str, object], label: str) -> str:
    value = item.get("id")
    if not isinstance(value, str) or not value:
        raise ValueError(f"{label} requires a non-empty id")
    return value


def _unique_items(
    value: object, label: str
) -> tuple[list[dict[str, object]], dict[str, dict[str, object]]]:
    items: list[dict[str, object]] = []
    by_id: dict[str, dict[str, object]] = {}
    for index, raw_item in enumerate(_require_list(value, label)):
        item = _require_mapping(raw_item, f"{label}[{index}]")
        item_id = _item_id(item, f"{label}[{index}]")
        if item_id in by_id:
            raise ValueError(f"{label} contains duplicate id {item_id}")
        items.append(item)
        by_id[item_id] = item
    return items, by_id


def _validate_catalog_header(path: Path, catalog: dict[str, object]) -> None:
    schema = catalog.get("schema")
    if not isinstance(schema, str) or not schema:
        raise ValueError(f"{path} requires a non-empty schema")
    if catalog.get("version") != 2:
        raise ValueError(f"{path} requires version 2")
    status = catalog.get("coverageStatus")
    if status not in _CATALOG_COVERAGE_STATUSES:
        raise ValueError(
            f"{path} coverageStatus must be declared, fixture-backed, mixed, or verified"
        )
    digest_policy = catalog.get("sourceDigestPolicy")
    if digest_policy is not None and digest_policy != "sha256-at-run":
        raise ValueError(f"{path} sourceDigestPolicy must be sha256-at-run")


def _load_catalogs(root: Path) -> dict[str, dict[str, object]]:
    evals_root = root / "evals"
    missing = sorted(
        filename
        for filename in _CATALOG_FILES.values()
        if not (evals_root / filename).is_file()
    )
    if missing:
        raise ValueError(
            "Missing required evaluation catalogs: " + ", ".join(missing)
        )
    catalogs: dict[str, dict[str, object]] = {}
    for key, filename in _CATALOG_FILES.items():
        path = evals_root / filename
        catalog = load_yaml(path)
        _validate_catalog_header(path, catalog)
        catalogs[key] = catalog
    return catalogs


def _validate_harnesses(value: object, label: str) -> list[str]:
    harnesses = sorted(_string_list(value, f"{label} harnesses"))
    expected = sorted(_SUPPORTED_HARNESSES)
    if harnesses != expected:
        raise ValueError(
            f"{label} harnesses must be exactly {', '.join(expected)}; "
            f"found {', '.join(harnesses) if harnesses else 'none'}"
        )
    return list(_SUPPORTED_HARNESSES)


def _coverage_status(item: dict[str, object], label: str) -> str:
    value = item.get("coverageStatus")
    if value not in _COVERAGE_STATUSES:
        raise ValueError(
            f"{label} coverageStatus must be declared, fixture-backed, or verified"
        )
    return str(value)


def _command_is_declared(value: object) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray, str)):
        return bool(value) and all(isinstance(item, str) and item for item in value)
    if not isinstance(value, dict):
        return False
    argv = value.get("argv")
    if not isinstance(argv, list) or not argv or any(
        not isinstance(item, str) or not item for item in argv
    ):
        return False
    environment = value.get("env", {})
    if not isinstance(environment, dict) or any(
        not isinstance(name, str)
        or not name
        or not isinstance(item, str)
        or not item
        for name, item in environment.items()
    ):
        return False
    timeout = value.get("timeoutSeconds")
    return timeout is None or (
        isinstance(timeout, (int, float)) and not isinstance(timeout, bool) and timeout > 0
    )


def _case_is_executable(root: Path, case: dict[str, object]) -> bool:
    project = case.get("project")
    task = case.get("task")
    if case.get("executionStatus") != "runnable":
        return False
    if not isinstance(project, str) or not project:
        return False
    if not isinstance(task, str) or not task:
        return False
    if not _command_is_declared(case.get("verify")):
        return False
    project_path = root / project
    return project_path.is_dir() and (project_path / task).is_file()


def _validate_case_refs(
    value: object,
    label: str,
    cases: dict[str, dict[str, object]],
) -> list[str]:
    references = _string_list(value, label)
    unknown = sorted(set(references) - set(cases))
    if unknown:
        raise ValueError(f"{label} references unknown cases: {', '.join(unknown)}")
    return sorted(set(references))


def _validate_declared_inventory(
    expected: set[str],
    declared: set[str],
    *,
    missing_label: str,
    unknown_label: str,
) -> None:
    missing = sorted(expected - declared)
    unknown = sorted(declared - expected)
    if missing:
        raise ValueError(f"{missing_label}: {', '.join(missing)}")
    if unknown:
        raise ValueError(f"{unknown_label}: {', '.join(unknown)}")


def _validate_judge_plan(
    value: object,
    label: str,
    checks: set[str],
    rubrics: set[str],
) -> str | None:
    plan = _require_mapping(value, f"{label} judgePlan")
    deterministic = _string_list(
        plan.get("deterministicChecks"), f"{label} judgePlan.deterministicChecks"
    )
    unknown_checks = sorted(set(deterministic) - checks)
    if unknown_checks:
        raise ValueError(
            f"{label} judgePlan references unknown deterministic checks: "
            + ", ".join(unknown_checks)
        )
    model_rubric = plan.get("modelRubric")
    if model_rubric is not None and (
        not isinstance(model_rubric, str) or model_rubric not in rubrics
    ):
        raise ValueError(f"{label} judgePlan references unknown Model Judge rubric")
    return str(model_rubric) if model_rubric is not None else None


def _valid_calibration_record(
    record: dict[str, object],
    rubric_id: str,
    rubric: dict[str, object],
    required_digests: list[str],
    validator: object,
) -> bool:
    record_rubric = record.get("rubricId", record.get("rubric"))
    if record_rubric != rubric_id:
        return False
    expected = {
        name: record.get(name)
        for name in required_digests
    }
    canonical_identity = getattr(validator, "canonical_judge_identity", None)
    if not callable(canonical_identity):
        return False
    try:
        governed_identity = canonical_identity(rubric)
    except (TypeError, ValueError):
        return False
    if not isinstance(governed_identity, dict):
        return False
    expected.update(governed_identity)
    expected["rubricSha256"] = hashlib.sha256(
        json.dumps(
            rubric,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("utf-8")
    ).hexdigest()
    if record.get("harness") not in _SUPPORTED_HARNESSES:
        return False
    if any(
        not isinstance(expected.get(name), str) or not expected[name]
        for name in required_digests
    ):
        return False
    validate = getattr(validator, "validate_calibration_record", None)
    if not callable(validate):
        return False
    try:
        errors = validate(record, expected)
    except (TypeError, ValueError):
        return False
    return isinstance(errors, Sequence) and not isinstance(
        errors, (bytes, bytearray, str)
    ) and not errors


def _judge_catalog_status(
    catalog: dict[str, object],
    validator: object | None,
) -> tuple[set[str], set[str], dict[str, str], dict[str, object]]:
    checks, checks_by_id = _unique_items(catalog.get("checks"), "judges checks")
    rubrics, rubrics_by_id = _unique_items(catalog.get("rubrics"), "judges rubrics")
    for check in checks:
        if check.get("type") not in {"deterministic", "model", "human"}:
            raise ValueError(
                f"Judge check {_item_id(check, 'judge check')} has an unsupported type"
            )
    policy = _require_mapping(
        catalog.get("calibrationPolicy"), "judges calibrationPolicy"
    )
    status = policy.get("status")
    if status not in {"pending", "partial", "calibrated"}:
        raise ValueError(
            "judges calibrationPolicy status must be pending, partial, or calibrated"
        )
    promotion_status = policy.get("promotionStatus")
    if promotion_status != "disabled-pending-provenance":
        raise ValueError(
            "judges calibrationPolicy promotionStatus must remain "
            "disabled-pending-provenance until per-sample provenance is implemented"
        )
    recorded_digests = _require_mapping(
        policy.get("recordedDigests"), "judges calibrationPolicy.recordedDigests"
    )
    required_digests = _string_list(
        recorded_digests.get("required"),
        "judges calibrationPolicy.recordedDigests.required",
    )
    _require_mapping(policy.get("thresholds"), "judges calibrationPolicy.thresholds")
    records = [
        _require_mapping(item, "judges calibrationPolicy record")
        for item in _require_list(
            policy.get("records"), "judges calibrationPolicy.records"
        )
    ]
    rubric_status = {rubric_id: "pending" for rubric_id in rubrics_by_id}
    if records and validator is None:
        raise ValueError(
            "judges calibrationPolicy records require the canonical calibration validator"
        )
    for rubric_id in rubrics_by_id:
        for record in records:
            _valid_calibration_record(
                record,
                rubric_id,
                rubrics_by_id[rubric_id],
                required_digests,
                validator,
            )
    calibrated_count = sum(
        rubric_state == "calibrated" for rubric_state in rubric_status.values()
    )
    derived_status = (
        "pending"
        if calibrated_count == 0
        else "calibrated"
        if calibrated_count == len(rubric_status)
        else "partial"
    )
    if status != derived_status:
        raise ValueError(
            "judges calibrationPolicy status does not match canonical records: "
            f"declared {status}, derived {derived_status}"
        )
    if records:
        unknown_record_rubrics = sorted(
            {
                str(record.get("rubricId", record.get("rubric")))
                for record in records
                if record.get("rubricId", record.get("rubric"))
                not in rubrics_by_id
            }
        )
        if unknown_record_rubrics:
            raise ValueError(
                "judges calibrationPolicy records reference unknown rubrics: "
                + ", ".join(unknown_record_rubrics)
            )
    judge_status = {
        "calibrationStatus": str(status),
        "promotionStatus": str(promotion_status),
        "diagnosticRecordCount": len(records),
        "requiredBeforeJudgeCalibrationClaim": bool(
            policy.get("requiredBeforeJudgeCalibrationClaim")
        ),
        "calibratedRubrics": sorted(
            rubric
            for rubric, rubric_state in rubric_status.items()
            if rubric_state == "calibrated"
        ),
        "pendingRubrics": sorted(
            rubric
            for rubric, rubric_state in rubric_status.items()
            if rubric_state != "calibrated"
        ),
    }
    return set(checks_by_id), set(rubrics_by_id), rubric_status, judge_status


def _calibration_for_rubrics(
    rubric_ids: list[str | None], rubric_status: dict[str, str]
) -> str:
    model_rubrics = [rubric for rubric in rubric_ids if rubric is not None]
    if not model_rubrics:
        return "not-required"
    if all(rubric_status[rubric] == "calibrated" for rubric in model_rubrics):
        return "calibrated"
    return "pending"


def _load_sandbox_profiles(
    catalog: dict[str, object],
) -> tuple[list[dict[str, object]], dict[str, dict[str, object]]]:
    raw_vocabulary = catalog.get("containmentStatusVocabulary")
    if isinstance(raw_vocabulary, dict):
        vocabulary = set(str(key) for key in raw_vocabulary)
    else:
        vocabulary = set(
            _string_list(raw_vocabulary, "sandbox containmentStatusVocabulary")
        )
    profiles, profiles_by_id = _unique_items(
        catalog.get("profiles"), "sandbox profiles"
    )
    normalized: list[dict[str, object]] = []
    seen_harnesses: set[str] = set()
    for profile in profiles:
        profile_id = _item_id(profile, "sandbox profile")
        harness = profile.get("harness")
        if harness not in _SUPPORTED_HARNESSES:
            raise ValueError(
                f"Sandbox profile {profile_id} uses unsupported harness {harness}"
            )
        seen_harnesses.add(str(harness))
        containment = _require_mapping(
            profile.get("containment"), f"Sandbox profile {profile_id} containment"
        )
        reported_status = containment.get("reportedStatus")
        if reported_status not in vocabulary:
            raise ValueError(
                f"Sandbox profile {profile_id} has unknown containment status {reported_status}"
            )
        workspace_isolation = profile.get("workspaceIsolation")
        if isinstance(workspace_isolation, dict):
            if workspace_isolation.get("externalRunnerRequired") is True:
                workspace_status: object = "external-runner-required"
            elif workspace_isolation.get("externalRunnerRequired") is False:
                workspace_status = (
                    "disposable-workspace-plus-mutation-audit"
                    if harness == "junie"
                    else "native-policy-plus-copy-on-write-declared"
                )
            else:
                workspace_status = workspace_isolation.get(
                    "reportedStatus", workspace_isolation.get("status", "declared")
                )
        elif isinstance(workspace_isolation, (str, bool)):
            workspace_status = workspace_isolation
        else:
            raise ValueError(
                f"Sandbox profile {profile_id} workspaceIsolation must be a mapping, string, or boolean"
            )
        normalized.append(
            {
                "id": profile_id,
                "harness": str(harness),
                "repositoryMutation": profile.get("repositoryMutation"),
                "implementationStatus": profile.get("implementationStatus"),
                "liveExecutionStatus": profile.get("liveExecutionStatus"),
                "preparedSnapshot": profile.get("preparedSnapshot"),
                "copyOnWriteWorkspace": profile.get("copyOnWriteWorkspace"),
                "warmWorker": profile.get("warmWorker"),
                "workspaceIsolation": workspace_status,
                "containmentStatus": str(reported_status),
            }
        )
    if seen_harnesses != set(_SUPPORTED_HARNESSES):
        missing = sorted(set(_SUPPORTED_HARNESSES) - seen_harnesses)
        raise ValueError(
            "Sandbox profiles missing evaluation harnesses: " + ", ".join(missing)
        )
    return sorted(normalized, key=lambda item: str(item["id"])), profiles_by_id


def _sandbox_references(value: object, label: str) -> dict[str, list[str]]:
    mapping = _require_mapping(value, label)
    _validate_harnesses(list(mapping), label)
    references: dict[str, list[str]] = {}
    for harness in _SUPPORTED_HARNESSES:
        raw_references = mapping[harness]
        if isinstance(raw_references, str):
            references[harness] = [raw_references]
        else:
            references[harness] = _string_list(
                raw_references, f"{label}.{harness}"
            )
    return references


def _classification_value(
    classification: object, camel_name: str, snake_name: str, default: object
) -> object:
    if isinstance(classification, dict):
        return classification.get(
            camel_name, classification.get(snake_name, default)
        )
    return getattr(
        classification,
        camel_name,
        getattr(classification, snake_name, default),
    )


def _is_digest_error(error: str) -> bool:
    lowered = error.lower()
    return "digest" in lowered and any(
        word in lowered for word in ("stale", "mismatch", "does not match", "current")
    )


def _classify_receipt(
    runner: ModuleType | object,
    case: dict[str, object],
    path: Path,
    receipt: dict[str, object],
) -> dict[str, object]:
    classifier = getattr(runner, "classify_evidence", None)
    if callable(classifier):
        classification = classifier(case, path)
        as_dict = getattr(classification, "as_dict", None)
        if callable(as_dict):
            classification = as_dict()
        errors_value = _classification_value(classification, "errors", "errors", [])
        errors = (
            [str(error) for error in errors_value]
            if isinstance(errors_value, Sequence)
            and not isinstance(errors_value, (bytes, bytearray, str))
            else []
        )
        return {
            "executed": bool(
                _classification_value(
                    classification, "executed", "executed", False
                )
            ),
            "verified": bool(
                _classification_value(
                    classification, "verified", "verified", False
                )
            ),
            "judgePassed": bool(
                _classification_value(
                    classification,
                    "judgePassed",
                    "judge_passed",
                    _classification_value(
                        classification, "verified", "verified", False
                    ),
                )
            ),
            "securityContained": bool(
                _classification_value(
                    classification,
                    "securityContained",
                    "security_contained",
                    False,
                )
            ),
            "judgeCalibrationStatus": str(
                _classification_value(
                    classification,
                    "judgeCalibrationStatus",
                    "judge_calibration_status",
                    "not-evaluated",
                )
            ),
            "staleByDigest": bool(
                _classification_value(
                    classification, "staleByDigest", "stale_by_digest", False
                )
            ),
            "errors": errors,
        }
    validator = getattr(runner, "validate_evidence", None)
    if not callable(validator):
        raise RuntimeError("Evaluation runner has no receipt classifier or validator")
    errors = [str(error) for error in validator(case, path)]
    stale = any(_is_digest_error(error) for error in errors)
    return {
        "executed": True,
        "verified": receipt.get("verdict") == "verified" and not errors,
        "judgePassed": receipt.get("verdict") == "verified" and not errors,
        "securityContained": False,
        "judgeCalibrationStatus": "not-evaluated",
        "staleByDigest": stale,
        "errors": errors,
    }


def _receipt_identity(
    receipt: dict[str, object],
) -> tuple[str | None, str | None, list[str]]:
    if receipt.get("version") == 2:
        run = _require_mapping(receipt.get("run"), "version 2 evidence run")
        agent_id = run.get("agentId")
        harness = run.get("harness")
    else:
        agent = _require_mapping(receipt.get("agent"), "version 1 evidence agent")
        agent_id = agent.get("id")
        harness = agent.get("harness")
    skills: list[str] = []
    for raw_skill in _require_list(receipt.get("skills"), "evidence skills"):
        skill = _require_mapping(raw_skill, "evidence skill")
        skill_id = skill.get("id")
        if isinstance(skill_id, str):
            skills.append(skill_id)
    return (
        str(agent_id) if isinstance(agent_id, str) else None,
        str(harness) if isinstance(harness, str) else None,
        skills,
    )


def _append_case(state: dict[str, object], key: str, case_id: str) -> None:
    values = state[key]
    if isinstance(values, list) and case_id not in values:
        values.append(case_id)
        values.sort()


def _apply_evidence(
    root: Path,
    coverage: dict[str, object],
    cases_by_id: dict[str, dict[str, object]],
    runner: ModuleType | object | None,
) -> None:
    evidence_root = root / "evals" / "evidence"
    evidence_paths = sorted(evidence_root.glob("*.yaml")) if evidence_root.is_dir() else []
    probe_skill = {
        probe_id: skill_id
        for skill_id, state in coverage["skills"].items()
        for probe_id in state["probeIds"]
    }
    executed_runs = 0
    judge_passed_runs = 0
    security_contained_runs = 0
    verified_runs = 0
    stale_runs = 0
    calibration_status_counts: dict[str, int] = {}
    if evidence_paths:
        active_runner = runner if runner is not None else load_eval_runner(root)
        for path in evidence_paths:
            receipt = load_yaml(path)
            if receipt.get("schema") != "dev-methodology-eval-evidence":
                raise ValueError(f"Unsupported evaluation evidence schema: {path}")
            if receipt.get("version") not in {1, 2}:
                raise ValueError(f"Unsupported evaluation evidence version: {path}")
            case_id = receipt.get("case")
            if not isinstance(case_id, str) or case_id not in cases_by_id:
                raise ValueError(
                    f"Evaluation evidence references unknown case {case_id}: {path}"
                )
            agent_id, harness, skill_ids = _receipt_identity(receipt)
            if agent_id not in coverage["agents"]:
                raise ValueError(
                    f"Evaluation evidence references unknown agent {agent_id}: {path}"
                )
            if harness not in _SUPPORTED_HARNESSES:
                raise ValueError(
                    f"Evaluation evidence uses unsupported harness {harness}: {path}"
                )
            unknown_skills = sorted(set(skill_ids) - set(coverage["skills"]))
            if unknown_skills:
                raise ValueError(
                    f"Evaluation evidence references unknown skills {', '.join(unknown_skills)}: {path}"
                )
            case = cases_by_id[case_id]
            extra_skills = sorted(
                set(skill_ids)
                - set(
                    _string_list(
                        case.get("requiredSkills", []),
                        f"Evaluation case {case_id} requiredSkills",
                    )
                )
            )
            if extra_skills:
                raise ValueError(
                    f"Evaluation evidence references non-case skills {', '.join(extra_skills)}: {path}"
                )
            classification = _classify_receipt(
                active_runner, case, path, receipt
            )
            errors = [
                str(error)
                for error in classification.get("errors", [])
                if isinstance(error, str)
            ]
            stale = bool(classification["staleByDigest"])
            non_stale_errors = [
                error for error in errors if not _is_digest_error(error)
            ]
            if receipt.get("verdict") == "verified" and non_stale_errors:
                raise ValueError(
                    f"Invalid verified evaluation evidence {path}: "
                    + "; ".join(non_stale_errors)
                )
            if bool(classification["verified"]) and stale:
                raise ValueError(
                    f"Evidence classifier marked stale receipt as verified: {path}"
                )
            target_agent_state = coverage["agents"][agent_id]
            target_probe_ids = _string_list(
                case.get("fixtureBackedProbeClaims", []),
                f"Evaluation case {case_id} fixtureBackedProbeClaims",
            )
            target_skill_states = [
                coverage["skills"][probe_skill[probe_id]]
                for probe_id in target_probe_ids
            ]
            if bool(classification["executed"]):
                executed_runs += 1
                _append_case(target_agent_state, "executedCases", case_id)
                for state in target_skill_states:
                    _append_case(state, "positiveExecutedCases", case_id)
                    if state["fixtureBacked"]:
                        _append_case(state, "executedCases", case_id)
            if bool(classification["judgePassed"]):
                judge_passed_runs += 1
                _append_case(target_agent_state, "judgePassedCases", case_id)
                for state in target_skill_states:
                    _append_case(state, "positiveJudgePassedCases", case_id)
                    if state["fixtureBacked"]:
                        _append_case(state, "judgePassedCases", case_id)
            if bool(classification["securityContained"]):
                security_contained_runs += 1
                _append_case(target_agent_state, "securityContainedCases", case_id)
                for state in target_skill_states:
                    _append_case(state, "positiveSecurityContainedCases", case_id)
                    if state["fixtureBacked"]:
                        _append_case(state, "securityContainedCases", case_id)
            if bool(classification["verified"]):
                verified_runs += 1
                _append_case(target_agent_state, "verifiedCases", case_id)
                for state in target_skill_states:
                    _append_case(state, "positiveVerifiedCases", case_id)
                    if state["fixtureBacked"]:
                        _append_case(state, "verifiedCases", case_id)
            if stale:
                stale_runs += 1
                _append_case(target_agent_state, "staleByDigestCases", case_id)
                for state in target_skill_states:
                    _append_case(state, "positiveStaleByDigestCases", case_id)
                    if state["fixtureBacked"]:
                        _append_case(state, "staleByDigestCases", case_id)
            calibration_status = str(
                classification.get("judgeCalibrationStatus", "not-evaluated")
            )
            calibration_status_counts[calibration_status] = (
                calibration_status_counts.get(calibration_status, 0) + 1
            )
    evidence_status = coverage["evidenceStatus"]
    evidence_status.update(
        {
            "executedRunCount": executed_runs,
            "judgePassedRunCount": judge_passed_runs,
            "securityContainedRunCount": security_contained_runs,
            "verifiedRunCount": verified_runs,
            "staleByDigestRunCount": stale_runs,
            "judgeCalibrationStatusCounts": dict(
                sorted(calibration_status_counts.items())
            ),
            "executedAgentCount": sum(
                bool(state["executedCases"])
                for state in coverage["agents"].values()
            ),
            "executedSkillCount": sum(
                bool(state["executedCases"])
                for state in coverage["skills"].values()
            ),
            "judgePassedAgentCount": sum(
                bool(state["judgePassedCases"])
                for state in coverage["agents"].values()
            ),
            "judgePassedSkillCount": sum(
                bool(state["judgePassedCases"])
                for state in coverage["skills"].values()
            ),
            "securityContainedAgentCount": sum(
                bool(state["securityContainedCases"])
                for state in coverage["agents"].values()
            ),
            "securityContainedSkillCount": sum(
                bool(state["securityContainedCases"])
                for state in coverage["skills"].values()
            ),
            "verifiedAgentCount": sum(
                bool(state["verifiedCases"])
                for state in coverage["agents"].values()
            ),
            "verifiedSkillCount": sum(
                bool(state["verifiedCases"])
                for state in coverage["skills"].values()
            ),
            "staleByDigestAgentCount": sum(
                bool(state["staleByDigestCases"])
                for state in coverage["agents"].values()
            ),
            "staleByDigestSkillCount": sum(
                bool(state["staleByDigestCases"])
                for state in coverage["skills"].values()
            ),
            "positiveExecutedSkillCount": sum(
                bool(state["positiveExecutedCases"])
                for state in coverage["skills"].values()
            ),
            "positiveJudgePassedSkillCount": sum(
                bool(state["positiveJudgePassedCases"])
                for state in coverage["skills"].values()
            ),
            "positiveSecurityContainedSkillCount": sum(
                bool(state["positiveSecurityContainedCases"])
                for state in coverage["skills"].values()
            ),
            "positiveVerifiedSkillCount": sum(
                bool(state["positiveVerifiedCases"])
                for state in coverage["skills"].values()
            ),
            "positiveStaleByDigestSkillCount": sum(
                bool(state["positiveStaleByDigestCases"])
                for state in coverage["skills"].values()
            ),
        }
    )


def build_evaluation_coverage(
    root: Path,
    skills: dict[str, str],
    roles: dict[str, dict[str, object]],
    *,
    eval_runner: ModuleType | object | None = None,
) -> dict[str, object]:
    """Validate all evaluation catalogs and return conservative coverage states."""
    catalogs = _load_catalogs(root)
    cases, cases_by_id = _unique_items(
        catalogs["cases"].get("cases"), "evaluation cases"
    )
    _validate_harnesses(
        catalogs["cases"].get("supportedHarnesses"), "evals/cases.yaml"
    )
    executable_cases: set[str] = set()
    runnable_cases_by_harness: dict[str, set[str]] = {
        harness: set() for harness in _SUPPORTED_HARNESSES
    }
    ordinary_local_cases: set[str] = set()
    high_risk_external_cases: set[str] = set()
    harness_case_status_values = {
        "runnable",
        "external-runner-required",
        "unavailable",
    }
    for case in cases:
        case_id = _item_id(case, "evaluation case")
        _coverage_status(case, f"Evaluation case {case_id}")
        _validate_harnesses(case.get("harnesses"), f"Evaluation case {case_id}")
        structurally_executable = _case_is_executable(root, case)
        if structurally_executable:
            executable_cases.add(case_id)
        elif case.get("coverageStatus") == "fixture-backed":
            raise ValueError(
                f"Fixture-backed evaluation case {case_id} is not executable"
            )
        harness_status = _require_mapping(
            case.get("harnessExecutionStatus"),
            f"Evaluation case {case_id} harnessExecutionStatus",
        )
        if set(harness_status) != set(_SUPPORTED_HARNESSES):
            raise ValueError(
                f"Evaluation case {case_id} harnessExecutionStatus must define codex and junie"
            )
        for harness, status in harness_status.items():
            if status not in harness_case_status_values:
                raise ValueError(
                    f"Evaluation case {case_id} has unsupported {harness} execution status {status}"
                )
            if status == "runnable" and structurally_executable:
                runnable_cases_by_harness[str(harness)].add(case_id)
        risk = _require_mapping(case.get("risk"), f"Evaluation case {case_id} risk")
        level = risk.get("level")
        reasons = _string_list(
            risk.get("reasons"), f"Evaluation case {case_id} risk reasons"
        )
        if level == "ordinary":
            if reasons:
                raise ValueError(
                    f"Ordinary evaluation case {case_id} must not declare risk reasons"
                )
            if (
                case.get("executionTier") != "local"
                or case.get("securityContainmentRequired") is not False
                or set(harness_status.values()) != {"runnable"}
            ):
                raise ValueError(
                    f"Ordinary evaluation case {case_id} must run locally on Codex and Junie without a security-containment requirement"
                )
            ordinary_local_cases.add(case_id)
        elif level == "high":
            if not reasons:
                raise ValueError(
                    f"High-risk evaluation case {case_id} must declare at least one reason"
                )
            if (
                case.get("executionTier") != "externally-contained"
                or case.get("securityContainmentRequired") is not True
                or set(harness_status.values()) != {"external-runner-required"}
            ):
                raise ValueError(
                    f"High-risk evaluation case {case_id} must use the externally-contained tier for Codex and Junie"
                )
            high_risk_external_cases.add(case_id)
        else:
            raise ValueError(
                f"Evaluation case {case_id} risk level must be ordinary or high"
            )

    calibration_validator = eval_runner
    calibration_policy = _require_mapping(
        catalogs["judges"].get("calibrationPolicy"),
        "judges calibrationPolicy",
    )
    calibration_records = calibration_policy.get("records")
    if (
        isinstance(calibration_records, list)
        and calibration_records
        and calibration_validator is None
    ):
        calibration_validator = load_eval_runner(root)
    checks, rubrics, rubric_status, judge_status = _judge_catalog_status(
        catalogs["judges"], calibration_validator
    )
    sandbox_profiles, sandbox_profiles_by_id = _load_sandbox_profiles(
        catalogs["sandboxProfiles"]
    )
    _validate_harnesses(
        catalogs["skillProbes"].get("harnesses"), "evals/skill-probes.yaml"
    )
    raw_evaluation_categories = catalogs["skillProbes"].get(
        "evaluationCategoryVocabulary"
    )
    if isinstance(raw_evaluation_categories, dict):
        evaluation_categories = set(str(key) for key in raw_evaluation_categories)
    else:
        evaluation_categories = set(
            _string_list(
                raw_evaluation_categories,
                "evals/skill-probes.yaml evaluationCategoryVocabulary",
            )
        )
    harness_policy = _require_mapping(
        catalogs["agentScenarios"].get("harnessPolicy"),
        "evals/agent-scenarios.yaml harnessPolicy",
    )
    _validate_harnesses(
        harness_policy.get("supported"),
        "evals/agent-scenarios.yaml harnessPolicy",
    )

    probes, probes_by_id = _unique_items(
        catalogs["skillProbes"].get("probes"), "skill probes"
    )
    probes_by_skill: dict[str, dict[str, object]] = {}
    probe_state: dict[str, dict[str, object]] = {}
    for probe in probes:
        probe_id = _item_id(probe, "skill probe")
        skill_id = probe.get("skill")
        if not isinstance(skill_id, str) or not skill_id:
            raise ValueError(f"Skill probe {probe_id} requires a skill")
        expected_source = f"skills/{skill_id}/SKILL.md"
        if probe.get("source") != expected_source:
            raise ValueError(
                f"Skill probe {probe_id} source must be {expected_source}"
            )
        evaluation_category = probe.get("evaluationCategory")
        if evaluation_category not in evaluation_categories:
            raise ValueError(
                f"Skill probe {probe_id} has unknown evaluationCategory {evaluation_category}"
            )
        if skill_id in probes_by_skill:
            raise ValueError(f"Skill {skill_id} has multiple probe declarations")
        probes_by_skill[skill_id] = probe
        status = _coverage_status(probe, f"Skill probe {probe_id}")
        case_refs = _validate_case_refs(
            probe.get("executableCases"),
            f"Skill probe {probe_id} executableCases",
            cases_by_id,
        )
        catalog_fixture_backed = status == "fixture-backed"
        if catalog_fixture_backed != bool(case_refs):
            raise ValueError(
                f"Skill probe {probe_id} fixture-backed status must match executableCases"
            )
        ablation = _require_mapping(
            probe.get("ablation"), f"Skill probe {probe_id} ablation"
        )
        if ablation.get("omitTargetSkill") is not True:
            raise ValueError(
                f"Skill probe {probe_id} must declare omitTargetSkill true"
            )
        wrong_skill = ablation.get("wrongSkillControl")
        if (
            not isinstance(wrong_skill, str)
            or ((root / "skills").is_dir() and wrong_skill not in skills)
        ):
            raise ValueError(
                f"Skill probe {probe_id} wrongSkillControl must reference a bundled skill"
            )
        if wrong_skill == skill_id:
            raise ValueError(
                f"Skill probe {probe_id} wrongSkillControl must differ from its target skill"
            )
        rubric = _validate_judge_plan(
            probe.get("judgePlan"), f"Skill probe {probe_id}", checks, rubrics
        )
        probe_state[skill_id] = {
            "structural": True,
            "probeDeclared": True,
            "probeIds": [probe_id],
            "evaluationCategory": str(evaluation_category),
            "catalogFixtureBacked": catalog_fixture_backed,
            "positiveCaseBacked": False,
            "positiveCaseBackedCases": [],
            "negativeCaseBacked": False,
            "negativeCaseBackedCases": [],
            "pairedControlsExecutable": False,
            "fixtureBacked": False,
            "fixtureBackedCases": [],
            "executableFixture": False,
            "executableCases": case_refs,
            "judgeCalibration": _calibration_for_rubrics(
                [rubric], rubric_status
            ),
            "scenarioAssociations": sorted(
                set(
                    _string_list(
                        probe.get("scenarioAssociations"),
                        f"Skill probe {probe_id} scenarioAssociations",
                    )
                )
            ),
            "workflowAssociations": sorted(
                set(
                    _string_list(
                        probe.get("workflowAssociations"),
                        f"Skill probe {probe_id} workflowAssociations",
                    )
                )
            ),
            "executedCases": [],
            "judgePassedCases": [],
            "securityContainedCases": [],
            "verifiedCases": [],
            "staleByDigestCases": [],
            "positiveExecutedCases": [],
            "positiveJudgePassedCases": [],
            "positiveSecurityContainedCases": [],
            "positiveVerifiedCases": [],
            "positiveStaleByDigestCases": [],
        }
    _validate_declared_inventory(
        set(skills),
        set(probes_by_skill),
        missing_label="Skills missing probe declarations",
        unknown_label="Probe declarations reference unknown skills",
    )

    agent_entries, agents_by_id = _unique_items(
        catalogs["agentScenarios"].get("agents"), "agent scenario declarations"
    )
    scenario_by_id: dict[str, dict[str, object]] = {}
    scenario_owner: dict[str, str] = {}
    agent_state: dict[str, dict[str, object]] = {}
    for agent in agent_entries:
        agent_id = _item_id(agent, "agent scenario declaration")
        if agent_id in roles:
            expected_source = roles[agent_id].get(
                "_sourcePath", roles[agent_id].get("sourcePath")
            )
            if isinstance(expected_source, str) and agent.get("source") != expected_source:
                raise ValueError(
                    f"Agent scenario declaration {agent_id} source must be {expected_source}"
                )
        _validate_harnesses(
            agent.get("harnesses"), f"Agent scenario declaration {agent_id}"
        )
        agent_rubrics = [
            _validate_judge_plan(
                agent.get("judgePlan"),
                f"Agent scenario declaration {agent_id}",
                checks,
                rubrics,
            )
        ]
        scenarios, scenario_items = _unique_items(
            agent.get("scenarios"), f"Agent {agent_id} scenarios"
        )
        if not scenarios:
            raise ValueError(f"Agent {agent_id} requires at least one scenario")
        case_refs: set[str] = set()
        scenario_coverage: dict[str, dict[str, object]] = {}
        case_backed_scenarios: set[str] = set()
        for scenario in scenarios:
            scenario_id = _item_id(scenario, f"Agent {agent_id} scenario")
            if scenario_id in scenario_by_id:
                raise ValueError(f"Duplicate scenario id {scenario_id}")
            scenario_by_id[scenario_id] = scenario
            scenario_owner[scenario_id] = agent_id
            status = _coverage_status(
                scenario, f"Agent {agent_id} scenario {scenario_id}"
            )
            scenario_cases = _validate_case_refs(
                scenario.get("executableCases"),
                f"Agent scenario {scenario_id} executableCases",
                cases_by_id,
            )
            scenario_fixture_backed = status == "fixture-backed"
            if scenario_fixture_backed != bool(scenario_cases):
                raise ValueError(
                    f"Agent scenario {scenario_id} fixture-backed status must match executableCases"
                )
            if scenario_fixture_backed:
                case_backed_scenarios.add(scenario_id)
            case_refs.update(scenario_cases)
            scenario_coverage[scenario_id] = {
                "caseBacked": scenario_fixture_backed,
                "executableFixture": scenario_fixture_backed
                and all(case_id in executable_cases for case_id in scenario_cases),
                "executableCases": scenario_cases,
            }
            agent_rubrics.append(
                _validate_judge_plan(
                    scenario.get("judgePlan"),
                    f"Agent scenario {scenario_id}",
                    checks,
                    rubrics,
                )
            )
        all_scenarios_backed = len(case_backed_scenarios) == len(scenarios)
        some_scenarios_backed = bool(case_backed_scenarios)
        agent_state[agent_id] = {
            "structural": True,
            "scenarioDeclared": True,
            "scenarioIds": sorted(scenario_items),
            "caseBacked": some_scenarios_backed,
            "caseBackedScenarioIds": sorted(case_backed_scenarios),
            "caseBackedCases": sorted(case_refs),
            "partialScenarioCoverage": some_scenarios_backed
            and not all_scenarios_backed,
            "fixtureBacked": all_scenarios_backed,
            "fixtureBackedCases": sorted(case_refs) if all_scenarios_backed else [],
            "executableFixture": all_scenarios_backed
            and bool(case_refs)
            and all(case_id in executable_cases for case_id in case_refs),
            "executableCases": sorted(case_refs),
            "scenarioCoverage": scenario_coverage,
            "judgeCalibration": _calibration_for_rubrics(
                agent_rubrics, rubric_status
            ),
            "workflowAssociations": sorted(
                set(
                    _string_list(
                        agent.get("workflowAssociations"),
                        f"Agent {agent_id} workflowAssociations",
                    )
                )
            ),
            "executedCases": [],
            "judgePassedCases": [],
            "securityContainedCases": [],
            "verifiedCases": [],
            "staleByDigestCases": [],
        }
    _validate_declared_inventory(
        set(roles),
        set(agents_by_id),
        missing_label="Conceptual agents missing scenario declarations",
        unknown_label="Scenario declarations reference unknown conceptual agents",
    )

    packs, packs_by_id = _unique_items(
        catalogs["workflowPacks"].get("packs"), "workflow packs"
    )
    workflow_state: dict[str, dict[str, object]] = {}
    for pack in packs:
        pack_id = _item_id(pack, "workflow pack")
        pack_status = _coverage_status(pack, f"Workflow pack {pack_id}")
        pack_case_refs = _validate_case_refs(
            pack.get("executableCases", []),
            f"Workflow pack {pack_id} executableCases",
            cases_by_id,
        )
        case_coverage_status = pack.get("caseCoverageStatus", "none")
        if case_coverage_status not in {"none", "partial", "complete"}:
            raise ValueError(
                f"Workflow pack {pack_id} caseCoverageStatus must be none, partial, or complete"
            )
        if bool(pack_case_refs) != (case_coverage_status != "none"):
            raise ValueError(
                f"Workflow pack {pack_id} caseCoverageStatus must match its associated executableCases"
            )
        pack_fixture_backed = pack_status == "fixture-backed"
        if pack_fixture_backed != (case_coverage_status == "complete"):
            raise ValueError(
                f"Workflow pack {pack_id} fixture-backed status requires complete end-to-end case coverage"
            )
        pack_agents = _string_list(
            pack.get("agents"), f"Workflow pack {pack_id} agents"
        )
        unknown_agents = sorted(set(pack_agents) - set(roles))
        if unknown_agents:
            raise ValueError(
                f"Workflow pack {pack_id} references unknown agents: "
                + ", ".join(unknown_agents)
            )
        pack_probes = _string_list(
            pack.get("skillProbes"), f"Workflow pack {pack_id} skillProbes"
        )
        unknown_probes = sorted(set(pack_probes) - set(probes_by_id))
        if unknown_probes:
            raise ValueError(
                f"Workflow pack {pack_id} references unknown skill probes: "
                + ", ".join(unknown_probes)
            )
        phases, _phases_by_id = _unique_items(
            pack.get("phases"), f"Workflow pack {pack_id} phases"
        )
        for phase in phases:
            phase_id = _item_id(phase, f"Workflow pack {pack_id} phase")
            phase_agents = _string_list(
                phase.get("agents"),
                f"Workflow pack {pack_id} phase {phase_id} agents",
            )
            unknown_phase_agents = sorted(set(phase_agents) - set(roles))
            if unknown_phase_agents:
                raise ValueError(
                    f"Workflow pack {pack_id} phase {phase_id} references unknown agents: "
                    + ", ".join(unknown_phase_agents)
                )
            _string_list(
                phase.get("requiredEvidence"),
                f"Workflow pack {pack_id} phase {phase_id} requiredEvidence",
            )
        sandbox_refs = _sandbox_references(
            pack.get("sandboxProfiles"),
            f"Workflow pack {pack_id} sandboxProfiles",
        )
        unknown_sandboxes = sorted(
            profile_id
            for profile_ids in sandbox_refs.values()
            for profile_id in profile_ids
            if profile_id not in sandbox_profiles_by_id
        )
        if unknown_sandboxes:
            raise ValueError(
                f"Workflow pack {pack_id} references unknown sandbox profiles: "
                + ", ".join(unknown_sandboxes)
            )
        rubric = _validate_judge_plan(
            pack.get("judgePlan"), f"Workflow pack {pack_id}", checks, rubrics
        )
        workflow_state[pack_id] = {
            "agents": sorted(set(pack_agents)),
            "skillProbes": sorted(set(pack_probes)),
            "caseBacked": bool(pack_case_refs),
            "caseCoverageStatus": str(case_coverage_status),
            "caseBackedCases": pack_case_refs,
            "fixtureBacked": pack_fixture_backed,
            "fixtureBackedCases": pack_case_refs if pack_fixture_backed else [],
            "executableFixture": pack_fixture_backed
            and bool(pack_case_refs)
            and all(case_id in executable_cases for case_id in pack_case_refs),
            "executableCases": pack_case_refs,
            "judgeCalibration": _calibration_for_rubrics(
                [rubric], rubric_status
            ),
        }

    for skill_id, state in probe_state.items():
        unknown_scenarios = sorted(
            set(state["scenarioAssociations"]) - set(scenario_by_id)
        )
        if unknown_scenarios:
            raise ValueError(
                f"Skill probe for {skill_id} references unknown scenarios: "
                + ", ".join(unknown_scenarios)
            )
        unknown_workflows = sorted(
            set(state["workflowAssociations"]) - set(packs_by_id)
        )
        if unknown_workflows:
            raise ValueError(
                f"Skill probe for {skill_id} references unknown workflows: "
                + ", ".join(unknown_workflows)
            )
    for agent_id, state in agent_state.items():
        unknown_workflows = sorted(
            set(state["workflowAssociations"]) - set(packs_by_id)
        )
        if unknown_workflows:
            raise ValueError(
                f"Agent {agent_id} references unknown workflows: "
                + ", ".join(unknown_workflows)
            )

    for case in cases:
        case_id = _item_id(case, "evaluation case")
        required_case_skills = set(
            _string_list(
                case.get("requiredSkills", []),
                f"Evaluation case {case_id} requiredSkills",
            )
        )
        case_probe_ids = set(
            _string_list(
                case.get("skillProbes"),
                f"Evaluation case {case_id} skillProbes",
            )
        )
        unknown_case_probes = sorted(case_probe_ids - set(probes_by_id))
        if unknown_case_probes:
            raise ValueError(
                f"Evaluation case {case_id} references unknown skill probes: "
                + ", ".join(unknown_case_probes)
            )
        fixture_backed_probe_ids = set(
            _string_list(
                case.get("fixtureBackedProbeClaims", []),
                f"Evaluation case {case_id} fixtureBackedProbeClaims",
            )
        )
        unassociated_fixture_claims = sorted(
            fixture_backed_probe_ids - case_probe_ids
        )
        if unassociated_fixture_claims:
            raise ValueError(
                f"Evaluation case {case_id} has unassociated fixture-backed probe claims: "
                + ", ".join(unassociated_fixture_claims)
            )
        case_scenario_ids = set(
            _string_list(
                case.get("agentScenarios"),
                f"Evaluation case {case_id} agentScenarios",
            )
        )
        unknown_case_scenarios = sorted(case_scenario_ids - set(scenario_by_id))
        if unknown_case_scenarios:
            raise ValueError(
                f"Evaluation case {case_id} references unknown agent scenarios: "
                + ", ".join(unknown_case_scenarios)
            )
        workflow_id = case.get("workflowPack")
        if workflow_id is not None and workflow_id not in packs_by_id:
            raise ValueError(
                f"Evaluation case {case_id} references unknown workflow pack {workflow_id}"
            )
        if isinstance(workflow_id, str):
            workflow = workflow_state[workflow_id]
            if (
                case.get("coverageStatus") == "fixture-backed"
                and case_id not in workflow["executableCases"]
            ):
                raise ValueError(
                    f"Evaluation case {case_id} and workflow pack {workflow_id} disagree on fixture association"
                )
        sandbox_refs = _sandbox_references(
            case.get("sandboxProfiles"),
            f"Evaluation case {case_id} sandboxProfiles",
        )
        unknown_case_sandboxes = sorted(
            profile_id
            for profile_ids in sandbox_refs.values()
            for profile_id in profile_ids
            if profile_id not in sandbox_profiles_by_id
        )
        if unknown_case_sandboxes:
            raise ValueError(
                f"Evaluation case {case_id} references unknown sandbox profiles: "
                + ", ".join(unknown_case_sandboxes)
            )
        _validate_judge_plan(
            case.get("judgePlan"), f"Evaluation case {case_id}", checks, rubrics
        )
        for probe_id in fixture_backed_probe_ids:
            if case_id not in probes_by_id[probe_id].get("executableCases", []):
                raise ValueError(
                    f"Evaluation case {case_id} and skill probe {probe_id} disagree on fixture association"
                )
            probe = probes_by_id[probe_id]
            target_skill_id = str(probe["skill"])
            if not probe_state[target_skill_id][
                "catalogFixtureBacked"
            ]:
                raise ValueError(
                    f"Evaluation case {case_id} claims declared-only skill probe {probe_id} as fixture-backed"
                )
            wrong_skill = _require_mapping(
                probe.get("ablation"), f"Skill probe {probe_id} ablation"
            ).get("wrongSkillControl")
            if wrong_skill in required_case_skills:
                raise ValueError(
                    f"Skill probe {probe_id} wrongSkillControl {wrong_skill} is already required by evaluation case {case_id}"
                )
            _append_case(
                probe_state[target_skill_id],
                "positiveCaseBackedCases",
                case_id,
            )
        for probe_id, probe in probes_by_id.items():
            if case_id in probe.get("executableCases", []) and probe_id not in case_probe_ids:
                raise ValueError(
                    f"Skill probe {probe_id} and evaluation case {case_id} disagree on executable association"
                )
        for scenario_id in case_scenario_ids:
            if case_id not in scenario_by_id[scenario_id].get(
                "executableCases", []
            ):
                raise ValueError(
                    f"Evaluation case {case_id} and agent scenario {scenario_id} disagree on fixture association"
                )

    for skill_id, state in probe_state.items():
        if bool(state["catalogFixtureBacked"]) != bool(
            state["positiveCaseBackedCases"]
        ):
            raise ValueError(
                f"Skill probe for {skill_id} fixture-backed status must match fixtureBackedProbeClaims"
            )
        state["positiveCaseBacked"] = bool(state["positiveCaseBackedCases"])
        state["fixtureBacked"] = bool(
            state["positiveCaseBacked"]
            and state["negativeCaseBacked"]
            and state["pairedControlsExecutable"]
        )
        state["fixtureBackedCases"] = (
            sorted(
                set(state["positiveCaseBackedCases"])
                | set(state["negativeCaseBackedCases"])
            )
            if state["fixtureBacked"]
            else []
        )
        state["executableFixture"] = bool(state["fixtureBackedCases"]) and all(
            case_id in executable_cases for case_id in state["fixtureBackedCases"]
        )

    coverage: dict[str, object] = {
        "harnesses": list(_SUPPORTED_HARNESSES),
        "runnableCasesByHarness": {
            harness: sorted(case_ids)
            for harness, case_ids in runnable_cases_by_harness.items()
        },
        "cases": cases_by_id,
        "skills": probe_state,
        "agents": agent_state,
        "workflows": workflow_state,
        "judgeStatus": judge_status,
        "sandboxProfiles": sandbox_profiles,
        "evidenceStatus": {
            "structuralAgentCount": len(roles),
            "structuralSkillCount": len(skills),
            "probeDeclaredSkillCount": len(probe_state),
            "scenarioDeclaredAgentCount": len(agent_state),
            "declaredScenarioCount": sum(
                len(state["scenarioIds"]) for state in agent_state.values()
            ),
            "workflowPackCount": len(workflow_state),
            "caseBackedWorkflowPackCount": sum(
                bool(state["caseBacked"]) for state in workflow_state.values()
            ),
            "partialWorkflowPackCount": sum(
                state["caseCoverageStatus"] == "partial"
                for state in workflow_state.values()
            ),
            "endToEndFixtureBackedWorkflowPackCount": sum(
                bool(state["fixtureBacked"]) for state in workflow_state.values()
            ),
            "fixtureBackedCaseCount": sum(
                case.get("coverageStatus") == "fixture-backed" for case in cases
            ),
            "executableCaseCount": len(executable_cases),
            "codexRunnableCaseCount": len(runnable_cases_by_harness["codex"]),
            "junieRunnableCaseCount": len(runnable_cases_by_harness["junie"]),
            "ordinaryLocalCaseCount": len(ordinary_local_cases),
            "highRiskExternalCaseCount": len(high_risk_external_cases),
            "caseBackedAgentCount": sum(
                bool(state["caseBacked"]) for state in agent_state.values()
            ),
            "partialScenarioBackedAgentCount": sum(
                bool(state["partialScenarioCoverage"])
                for state in agent_state.values()
            ),
            "fixtureBackedAgentCount": sum(
                bool(state["fixtureBacked"]) for state in agent_state.values()
            ),
            "positiveCaseBackedSkillCount": sum(
                bool(state["positiveCaseBacked"])
                for state in probe_state.values()
            ),
            "negativeCaseBackedSkillCount": sum(
                bool(state["negativeCaseBacked"])
                for state in probe_state.values()
            ),
            "pairedControlsExecutableSkillCount": sum(
                bool(state["pairedControlsExecutable"])
                for state in probe_state.values()
            ),
            "fixtureBackedSkillCount": sum(
                bool(state["fixtureBacked"]) for state in probe_state.values()
            ),
            "executableFixtureAgentCount": sum(
                bool(state["executableFixture"]) for state in agent_state.values()
            ),
            "executableFixtureSkillCount": sum(
                bool(state["executableFixture"]) for state in probe_state.values()
            ),
            "modelJudgeCalibratedAgentCount": sum(
                state["judgeCalibration"] == "calibrated"
                for state in agent_state.values()
            ),
            "modelJudgeCalibratedSkillCount": sum(
                state["judgeCalibration"] == "calibrated"
                for state in probe_state.values()
            ),
            "modelJudgePendingAgentCount": sum(
                state["judgeCalibration"] == "pending"
                for state in agent_state.values()
            ),
            "modelJudgePendingSkillCount": sum(
                state["judgeCalibration"] == "pending"
                for state in probe_state.values()
            ),
            "modelJudgeNotRequiredAgentCount": sum(
                state["judgeCalibration"] == "not-required"
                for state in agent_state.values()
            ),
            "modelJudgeNotRequiredSkillCount": sum(
                state["judgeCalibration"] == "not-required"
                for state in probe_state.values()
            ),
        },
    }
    _apply_evidence(root, coverage, cases_by_id, eval_runner)
    return coverage


def checkbox(value: bool) -> str:
    """Render one checklist boolean without implying evidence beyond its input."""
    return "[x]" if value else "[ ]"


def _case_list(value: object) -> str:
    if isinstance(value, list) and value:
        return ", ".join(str(item) for item in value)
    return "none"


def _workspace_text(value: object) -> str:
    if isinstance(value, (dict, list)):
        return json.dumps(value, sort_keys=True)
    return str(value)


def render(
    root: Path = ROOT,
    *,
    skills: dict[str, str] | None = None,
    roles: dict[str, dict[str, object]] | None = None,
    coverage: dict[str, object] | None = None,
) -> str:
    """Render Markdown, optionally reusing a previously validated live snapshot."""
    active_skills = skills if skills is not None else load_skills(root)
    active_roles = roles if roles is not None else load_roles(root)
    active_coverage = (
        coverage
        if coverage is not None
        else build_evaluation_coverage(root, active_skills, active_roles)
    )
    registry = load_yaml(
        root
        / "skills"
        / "detect-technology-skills"
        / "references"
        / "technology-skill-detection-registry.yaml"
    )
    categories = load_yaml(root / "design" / "skill-categories.yaml")["categories"]
    category_labels = {
        str(item["id"]): str(item["label"])
        for item in _require_list(categories, "skill categories")
        if isinstance(item, dict)
    }
    evidence = active_coverage["evidenceStatus"]
    lines = [
        "# Agent, Skill, Technology, And Test Coverage Checklist",
        "",
        "This page is generated from the live conceptual agent and skill inventories, all six evaluation catalogs, executable fixture checks, sandbox declarations, Judge calibration records, and classified evidence receipts. Regenerate it with scripts/build-support-checklist.py.",
        "",
        "## Status Meaning",
        "",
        "- Structural means the current agent or skill source exists and passes repository catalog checks.",
        "- Probe-declared and scenario-declared mean the current source has an explicit evaluation declaration. Declaration is not execution.",
        "- For agents, case-backed scenarios report exactly which declared scenarios have cases. Full fixture-backed status requires every declared scenario to be backed.",
        "- For skills, a positive case alone does not prove activation precision or causal skill contribution. Full probe coverage additionally requires a negative-activation case and executable target-present, target-omitted, and wrong-skill controls over frozen input.",
        "- Executable fixture means every case required for the corresponding full coverage claim has a project, task, and verification command.",
        "- A workflow pack may have partial case coverage without having an end-to-end fixture for every declared phase, agent, and handoff.",
        "- Model Judge calibration promotion is disabled pending per-sample provenance. Diagnostic records cannot create calibrated status; Deterministic-Judge-only declarations show not-required.",
        "- Executed means a version-two receipt has a structurally complete harness capture. It does not imply a Judge pass or security containment.",
        "- Judge-passed means the required Deterministic Judge and Model Judge checks passed. Model Judge calibration is reported separately and may remain pending.",
        "- Security-contained means a governed external runner established filesystem, process, network, and resource containment. The local tier does not make this claim.",
        "- Stale-by-digest means a prior execution no longer matches current agent, skill, model, or Judge artifacts.",
        "- Legacy verified fields remain for data compatibility only; primary reporting uses Executed, Judge-passed, Security-contained, and Stale-by-digest.",
        "- Catalog coverageStatus values never create execution or evidence claims.",
        "",
        "## Summary",
        "",
        f"- [x] {evidence['structuralAgentCount']} conceptual agents and {evidence['structuralSkillCount']} bundled skills have structural coverage.",
        f"- [x] {evidence['scenarioDeclaredAgentCount']} agents are scenario-declared and {evidence['probeDeclaredSkillCount']} skills are probe-declared.",
        f"- [x] {evidence['declaredScenarioCount']} agent scenarios and {evidence['workflowPackCount']} workflow packs are declared.",
        f"- {evidence['caseBackedWorkflowPackCount']} workflow packs have associated cases; {evidence['partialWorkflowPackCount']} are partial and {evidence['endToEndFixtureBackedWorkflowPackCount']} have end-to-end fixture coverage.",
        f"- {evidence['fixtureBackedCaseCount']} cases are fixture-backed and {evidence['executableCaseCount']} fixtures are structurally executable before harness readiness is considered.",
        f"- {evidence['codexRunnableCaseCount']} cases can run locally through Codex and {evidence['junieRunnableCaseCount']} can run locally through Junie.",
        f"- {evidence['ordinaryLocalCaseCount']} cases use the ordinary local tier; {evidence['highRiskExternalCaseCount']} explicitly high-risk cases require the externally-contained tier.",
        f"- {evidence['caseBackedAgentCount']} agents have at least one case-backed scenario; {evidence['partialScenarioBackedAgentCount']} are partial and {evidence['fixtureBackedAgentCount']} have all declared scenarios backed.",
        f"- {evidence['positiveCaseBackedSkillCount']} skills have positive-case support, {evidence['negativeCaseBackedSkillCount']} have negative-activation cases, {evidence['pairedControlsExecutableSkillCount']} have executable paired controls, and {evidence['fixtureBackedSkillCount']} satisfy the full probe contract.",
        f"- {evidence['executableFixtureAgentCount']} agents and {evidence['executableFixtureSkillCount']} skills have executable full fixtures.",
        f"- {evidence['modelJudgeCalibratedAgentCount']} agents and {evidence['modelJudgeCalibratedSkillCount']} skills have calibrated Model Judge status.",
        f"- {evidence['modelJudgePendingAgentCount']} agents and {evidence['modelJudgePendingSkillCount']} skills have pending Model Judge status.",
        f"- {evidence['modelJudgeNotRequiredAgentCount']} agents and {evidence['modelJudgeNotRequiredSkillCount']} skills use Deterministic Judges only and do not require Model Judge calibration.",
        f"- {evidence['executedAgentCount']} agents and {evidence['executedSkillCount']} skills have classified executions.",
        f"- {evidence['judgePassedAgentCount']} agents and {evidence['judgePassedSkillCount']} skills have Judge-passed evidence.",
        f"- {evidence['securityContainedAgentCount']} agents and {evidence['securityContainedSkillCount']} skills have security-contained evidence.",
        f"- {evidence['staleByDigestAgentCount']} agents and {evidence['staleByDigestSkillCount']} skills have stale-by-digest evidence.",
        f"- Positive-case-only skill evidence: {evidence['positiveExecutedSkillCount']} executed, {evidence['positiveJudgePassedSkillCount']} Judge-passed, {evidence['positiveSecurityContainedSkillCount']} security-contained, and {evidence['positiveStaleByDigestSkillCount']} stale; these do not promote full-probe status.",
        "",
        "## Evaluation Harness And Sandbox Support",
        "",
        "Evaluation execution support is limited to Codex and Junie. Ordinary synthetic cases run locally in disposable workspaces with controlled harness state, timeouts, cleanup, isolated evidence, and mutation audits. External containment is reserved for explicitly high-risk cases. Workspace isolation and tool configuration do not create a security-containment claim.",
        "",
        "| Harness | Profile | Implementation | Workspace isolation | Containment status |",
        "| --- | --- | --- | --- | --- |",
    ]
    for profile in active_coverage["sandboxProfiles"]:
        lines.append(
            f"| {profile['harness']} | {profile['id']} | {profile['implementationStatus']} | "
            f"{_workspace_text(profile['workspaceIsolation'])} | {profile['containmentStatus']} |"
        )

    lines.extend(
        [
            "",
            "## Agent Checklist",
            "",
            "| Agent | Profile | Structural | Scenario-declared | Case-backed scenarios | All scenarios backed | Executable full fixture | Judge calibration | Executed | Judge-passed | Security-contained | Stale-by-digest |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for name, role in sorted(active_roles.items()):
        state = active_coverage["agents"][name]
        lines.append(
            f"| {name} | {role['modelProfile']} | {checkbox(state['structural'])} | "
            f"{checkbox(state['scenarioDeclared'])} {_case_list(state['scenarioIds'])} | "
            f"{checkbox(state['caseBacked'])} {_case_list(state['caseBackedScenarioIds'])} | "
            f"{checkbox(state['fixtureBacked'])} {_case_list(state['fixtureBackedCases'])} | {checkbox(state['executableFixture'])} "
            f"{_case_list(state['fixtureBackedCases'])} | {state['judgeCalibration']} | "
            f"{_case_list(state['executedCases'])} | {_case_list(state['judgePassedCases'])} | "
            f"{_case_list(state['securityContainedCases'])} | "
            f"{_case_list(state['staleByDigestCases'])} |"
        )

    lines.extend(["", "## Bundled Skill Checklist", ""])
    for category in _require_list(categories, "skill categories"):
        category_mapping = _require_mapping(category, "skill category")
        category_id = str(category_mapping["id"])
        lines.extend([f"### {category_labels[category_id]}", ""])
        lines.extend(
            [
                "| Skill | Structural | Probe-declared | Positive case | Negative case | Paired controls | Full probe | Executable full fixture | Judge calibration | Executed | Judge-passed | Security-contained | Stale-by-digest |",
                "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
            ]
        )
        for name in sorted(
            skill for skill, value in active_skills.items() if value == category_id
        ):
            state = active_coverage["skills"][name]
            lines.append(
                f"| {name} | {checkbox(state['structural'])} | "
                f"{checkbox(state['probeDeclared'])} {_case_list(state['probeIds'])} | "
                f"{checkbox(state['positiveCaseBacked'])} {_case_list(state['positiveCaseBackedCases'])} | "
                f"{checkbox(state['negativeCaseBacked'])} {_case_list(state['negativeCaseBackedCases'])} | "
                f"{checkbox(state['pairedControlsExecutable'])} | "
                f"{checkbox(state['fixtureBacked'])} {_case_list(state['fixtureBackedCases'])} | {checkbox(state['executableFixture'])} "
                f"{_case_list(state['fixtureBackedCases'])} | {state['judgeCalibration']} | "
                f"{_case_list(state['executedCases'])} | {_case_list(state['judgePassedCases'])} | "
                f"{_case_list(state['securityContainedCases'])} | "
                f"{_case_list(state['staleByDigestCases'])} |"
            )
        lines.append("")

    lines.extend(
        [
            "## Technology Detection Registry",
            "",
            "| Skill | Kind | Label | Probe-declared | Positive case | Full probe fixture | Executed | Judge-passed | Security-contained | Stale-by-digest |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for entry in _require_list(registry["skills"], "technology registry skills"):
        mapping = _require_mapping(entry, "technology registry skill")
        skill_id = str(mapping["skill"])
        state = active_coverage["skills"][skill_id]
        lines.append(
            f"| {skill_id} | {mapping['kind']} | {mapping['label']} | "
            f"{checkbox(state['probeDeclared'])} | {checkbox(state['positiveCaseBacked'])} | {checkbox(state['executableFixture'])} | "
            f"{_case_list(state['executedCases'])} | {_case_list(state['judgePassedCases'])} | "
            f"{_case_list(state['securityContainedCases'])} | "
            f"{_case_list(state['staleByDigestCases'])} |"
        )

    lines.extend(
        [
            "",
            "## Judge Calibration",
            "",
            f"- Calibration policy status: {active_coverage['judgeStatus']['calibrationStatus']}.",
            f"- Calibrated Model Judge rubrics: {_case_list(active_coverage['judgeStatus']['calibratedRubrics'])}.",
            f"- Pending Model Judge rubrics: {_case_list(active_coverage['judgeStatus']['pendingRubrics'])}.",
            "- Judge outcome and calibration are separate: a raw Model Judge pass does not become calibrated until the governed calibration policy is enabled and satisfied.",
            "",
            "## Repository Verification Layers",
            "",
            "- [x] Every live skill has exactly one probe declaration.",
            "- [x] Every live conceptual agent has exactly one scenario declaration with at least one scenario.",
            "- [x] Evaluation catalog references, fixture paths, Judge plans, harnesses, workflow links, and sandbox profiles are validated.",
            "- [x] Codex and Junie are the only supported evaluation harnesses.",
            "- [x] Executed, Judge-passed, security-contained, calibration, and stale claims are classified independently by the evaluation runner.",
            "- [x] Explorer data carries the same conservative coverage snapshot.",
            "",
        ]
    )
    return "\n".join(lines)


def build_explorer_payload(
    skills: dict[str, str],
    roles: dict[str, dict[str, object]],
    detection: dict[str, object],
    coverage: dict[str, object],
) -> dict[str, object]:
    """Build version-two explorer data without promoting catalog declarations."""
    role_items: list[dict[str, object]] = []
    edges: list[dict[str, object]] = []
    for role_id, role in sorted(roles.items()):
        skill_entries = role_skill_entries(role)
        fixed_skills = [name for name, condition in skill_entries if condition is None]
        conditional_skills = {
            name: condition
            for name, condition in skill_entries
            if condition is not None
        }
        state = coverage["agents"][role_id]
        role_items.append(
            {
                "id": role_id,
                "label": role.get("label", role_id),
                "description": role.get("description", ""),
                "modelProfile": role["modelProfile"],
                "fixedSkills": fixed_skills,
                "conditionalSkills": conditional_skills,
                "dynamicFolderSkills": bool(role.get("dynamicFolderSkills", False)),
                "declaredCases": state["executableCases"],
                "executedCases": state["executedCases"],
                "judgePassedCases": state["judgePassedCases"],
                "securityContainedCases": state["securityContainedCases"],
                "verifiedCases": state["verifiedCases"],
                "coverage": state,
            }
        )
        edges.extend(
            {"role": role_id, "skill": skill, "kind": "fixed"}
            for skill in fixed_skills
        )
        edges.extend(
            {
                "role": role_id,
                "skill": skill,
                "kind": "conditional",
                "condition": condition,
            }
            for skill, condition in conditional_skills.items()
        )
    skill_items: list[dict[str, object]] = []
    for skill_id, category in sorted(skills.items()):
        state = coverage["skills"][skill_id]
        skill_items.append(
            {
                "id": skill_id,
                "category": category,
                "detection": detection.get(skill_id),
                "declaredCases": state["executableCases"],
                "executedCases": state["executedCases"],
                "judgePassedCases": state["judgePassedCases"],
                "securityContainedCases": state["securityContainedCases"],
                "verifiedCases": state["verifiedCases"],
                "coverage": state,
            }
        )
    return {
        "schema": "dev-methodology-agent-skill-explorer-data",
        "version": 2,
        "evaluationHarnesses": coverage["harnesses"],
        "roles": role_items,
        "skills": skill_items,
        "edges": sorted(
            edges, key=lambda item: (item["role"], item["kind"], item["skill"])
        ),
        "workflowCoverage": coverage["workflows"],
        "judgeStatus": coverage["judgeStatus"],
        "sandboxProfiles": coverage["sandboxProfiles"],
        "evidenceStatus": coverage["evidenceStatus"],
    }


def render_explorer_data(
    root: Path = ROOT,
    *,
    skills: dict[str, str] | None = None,
    roles: dict[str, dict[str, object]] | None = None,
    coverage: dict[str, object] | None = None,
) -> str:
    """Render explorer JavaScript, optionally reusing one validated snapshot."""
    active_skills = skills if skills is not None else load_skills(root)
    active_roles = roles if roles is not None else load_roles(root)
    active_coverage = (
        coverage
        if coverage is not None
        else build_evaluation_coverage(root, active_skills, active_roles)
    )
    registry = load_yaml(
        root
        / "skills"
        / "detect-technology-skills"
        / "references"
        / "technology-skill-detection-registry.yaml"
    )
    detection = {
        str(entry["skill"]): entry
        for entry in _require_list(
            registry["skills"], "technology detection registry skills"
        )
        if isinstance(entry, dict)
    }
    payload = build_explorer_payload(
        active_skills, active_roles, detection, active_coverage
    )
    return (
        "// Copyright (c) 2026 Martin.Bechard@DevConsult.ca\n"
        "// AI attribution: Generated with AI assistance.\n"
        "// Summary: Provides deterministic agent and skill evaluation coverage data to static design pages.\n"
        "// Generated by scripts/build-support-checklist.py. Do not edit by hand.\n"
        "window.DEV_METHODOLOGY_AGENT_SKILL_EXPLORER_DATA = "
        + json.dumps(payload, indent=2, sort_keys=True)
        + ";\n"
    )


def main() -> int:
    """Generate or freshness-check the Markdown and explorer outputs."""
    parser = argparse.ArgumentParser(
        description="Build the agent, skill, technology, and test coverage checklist."
    )
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    skills = load_skills()
    roles = load_roles()
    coverage = build_evaluation_coverage(ROOT, skills, roles)
    outputs = {
        OUTPUT_PATH: render(skills=skills, roles=roles, coverage=coverage),
        EXPLORER_PATH: render_explorer_data(
            skills=skills, roles=roles, coverage=coverage
        ),
    }
    if args.check:
        stale = [
            path
            for path, content in outputs.items()
            if not path.is_file() or path.read_text(encoding="utf-8") != content
        ]
        if stale:
            for path in stale:
                print(f"stale {path}")
            return 1
        print("Agent and skill support checklist is current.")
        return 0
    for path, content in outputs.items():
        path.write_text(content, encoding="utf-8")
        print(f"generated {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
