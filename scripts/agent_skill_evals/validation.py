# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Validates evaluation catalogs, cases, evidence receipts, provenance, and digest freshness.

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence

import yaml

from .commands import command_spec
from .invocations import SUPPORTED_HARNESSES, agent_attribution_verified
from .judges import JUDGE_TYPES, validate_calibration_record
from .staging import selected_context_identity
from .workspace import (
    TRANSIENT_TREE_NAMES,
    dependency_inputs_digest,
    prepared_fixture_identity_key,
    snapshot_digest,
    snapshot_tree,
)


ROOT = Path(__file__).resolve().parents[2]
CASES_PATH = ROOT / "evals" / "cases.yaml"
_CATALOG_SPECS = {
    "skill-probes.yaml": (
        "probes",
        (
            "coverageStatus",
            "sourceDigestPolicy",
            "sourceCategoryPolicy",
            "evaluationCategoryVocabulary",
            "harnesses",
            "defaults",
            "probes",
        ),
    ),
    "agent-scenarios.yaml": (
        "agents",
        ("coverageStatus", "sourceDigestPolicy", "harnessPolicy", "fixtureProfiles", "agents"),
    ),
    "workflow-packs.yaml": ("packs", ("coverageStatus", "sourceDigestPolicy", "controls", "packs")),
    "judges.yaml": (
        "checks",
        (
            "coverageStatus",
            "sourceDigestPolicy",
            "judgeTypes",
            "executionOrder",
            "executionPolicy",
            "checks",
            "rubrics",
            "calibrationPolicy",
        ),
    ),
    "sandbox-profiles.yaml": (
        "profiles",
        (
            "coverageStatus",
            "sourceDigestPolicy",
            "snapshotPolicy",
            "containmentStatusVocabulary",
            "profiles",
        ),
    ),
}


@dataclass(frozen=True)
class EvidenceClassification:
    """Expose stable receipt state without requiring callers to parse validation messages."""

    executed: bool
    verified: bool
    stale_by_digest: bool
    errors: tuple[str, ...]
    stale_reasons: tuple[str, ...]

    def as_dict(self) -> dict[str, object]:
        """Return the reporting contract with stable camel-case field names."""

        return {
            "executed": self.executed,
            "verified": self.verified,
            "staleByDigest": self.stale_by_digest,
            "errors": list(self.errors),
            "staleReasons": list(self.stale_reasons),
        }


def content_digest(path: Path) -> str:
    """Return the SHA-256 digest of one source or evidence artifact."""

    return hashlib.sha256(path.read_bytes()).hexdigest()


def case_definition_digest(case: Mapping[str, object]) -> str:
    """Digest the complete selected case contract with a canonical JSON representation."""

    encoded = json.dumps(case, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def build_agent_evidence_identity(
    harness: str,
    agent_id: str,
    *,
    source_root: Path = ROOT,
) -> dict[str, object]:
    """Build current native adapter source and effective identities for an evidence producer."""

    if harness not in SUPPORTED_HARNESSES:
        raise ValueError(f"supported harness values are codex and junie, not {harness}")
    suffix = ".toml" if harness == "codex" else ".md"
    relative = Path("generated") / "adapters" / harness / "agents" / f"{agent_id}{suffix}"
    path = source_root.resolve() / relative
    source, effective, sanitizations = selected_context_identity(path, "agent-definition")
    return {
        "nativeAdapterSourceDigest": hashlib.sha256(source).hexdigest(),
        "nativeAdapterEffectiveDigest": hashlib.sha256(effective).hexdigest(),
        "nativeAdapterSanitizations": list(sanitizations),
    }


def build_skill_evidence_identity(
    case: Mapping[str, object],
    harness: str,
    skill_id: str,
    *,
    source_root: Path = ROOT,
) -> dict[str, object]:
    """Build the exact source/effective resource identity for one staged treatment skill."""

    if harness not in SUPPORTED_HARNESSES:
        raise ValueError(f"supported harness values are codex and junie, not {harness}")
    allowlists = case.get("skillResourceAllowlist", {})
    configured = allowlists.get(skill_id) if isinstance(allowlists, Mapping) else None
    selected = configured if isinstance(configured, list) else ["."]
    resource_paths = _selected_skill_resource_paths(source_root, skill_id, selected)
    resources: list[dict[str, object]] = []
    for relative in resource_paths:
        source, effective, sanitizations = selected_context_identity(
            source_root.resolve() / "skills" / skill_id / relative,
            "treatment-skill",
        )
        resources.append({
            "path": relative.as_posix(),
            "sourceDigest": hashlib.sha256(source).hexdigest(),
            "effectiveDigest": hashlib.sha256(effective).hexdigest(),
            "sanitizations": list(sanitizations),
        })
    by_path = {str(resource["path"]): resource for resource in resources}
    skill_file = by_path.get("SKILL.md")
    if skill_file is None:
        raise ValueError(f"skill resource selection must include SKILL.md: {skill_id}")
    return {
        "id": skill_id,
        "sourceDigest": skill_file["sourceDigest"],
        "effectiveDigest": skill_file["effectiveDigest"],
        "resourceManifestDigest": _resource_manifest_digest(resources),
        "resources": resources,
    }


def load_cases(path: Path = CASES_PATH) -> dict[str, dict[str, object]]:
    """Load the legacy-compatible executable case catalog and reject duplicate identifiers."""

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, Mapping) or not isinstance(data.get("cases"), list):
        raise ValueError(f"{path} must define a cases list.")
    cases: dict[str, dict[str, object]] = {}
    for item in data["cases"]:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str) or not item["id"].strip():
            raise ValueError("Every eval case must define a non-empty id.")
        if item["id"] in cases:
            raise ValueError(f"Duplicate eval case id: {item['id']}")
        cases[item["id"]] = item
    return cases


def validate_case_definition(case: Mapping[str, object]) -> list[str]:
    """Validate one executable case while accepting the original version-one field shape."""

    errors: list[str] = []
    _require_non_empty_string(case.get("id"), "case.id", errors)
    _require_non_empty_string(case.get("project"), "case.project", errors)
    _require_non_empty_string(case.get("task"), "case.task", errors)
    for field in ("requiredAgents", "requiredSkills", "requiredEvidence"):
        _validate_string_list(case.get(field), f"case.{field}", errors, required=True)
    _validate_string_list(case.get("requiredFindings", []), "case.requiredFindings", errors)
    _validate_string_list(case.get("forbiddenSkills", []), "case.forbiddenSkills", errors)
    harnesses = case.get("harnesses", sorted(SUPPORTED_HARNESSES))
    _validate_string_list(harnesses, "case.harnesses", errors, required=True)
    if isinstance(harnesses, list):
        unsupported = sorted(set(harnesses) - SUPPORTED_HARNESSES)
        if unsupported:
            errors.append(f"case harnesses contain unsupported values: {', '.join(unsupported)}")
    for field in ("install", "verify"):
        if field == "install" and (field not in case or case.get(field) is None):
            continue
        try:
            specification = command_spec(case.get(field))
        except ValueError as error:
            errors.append(f"case.{field}: {error}")
        else:
            if specification.inherit_environment:
                errors.append(f"case.{field} must not inherit the complete host environment")
    if "readOnly" in case and not isinstance(case.get("readOnly"), bool):
        errors.append("case.readOnly must be a boolean")
    for field in ("allowedWritePaths", "protectedPaths"):
        if field in case:
            _validate_string_list(case.get(field), f"case.{field}", errors)
    if isinstance(case.get("judgePlan"), Mapping) and not case.get("readOnly") and "allowedWritePaths" not in case:
        errors.append("case.allowedWritePaths is required for a mutation-capable version-two case")
    for field in ("sandboxProfiles", "minimumContainment"):
        value = case.get(field)
        if value is not None and not isinstance(value, Mapping):
            errors.append(f"case.{field} must map harnesses to values")
        elif isinstance(value, Mapping):
            unsupported = sorted(set(value) - SUPPORTED_HARNESSES)
            if unsupported:
                errors.append(f"case.{field} uses unsupported harnesses: {', '.join(unsupported)}")
    _validate_string_list(case.get("modelVisiblePaths", ["."]), "case.modelVisiblePaths", errors, required=True)
    resource_allowlist = case.get("skillResourceAllowlist", {})
    if not isinstance(resource_allowlist, Mapping):
        errors.append("case.skillResourceAllowlist must be a mapping")
    else:
        required_skills = set(_string_items(case.get("requiredSkills")))
        for skill, paths in resource_allowlist.items():
            if skill not in required_skills:
                errors.append(f"case.skillResourceAllowlist references a non-required skill: {skill}")
            _validate_string_list(paths, f"case.skillResourceAllowlist.{skill}", errors, required=True)
            if isinstance(paths, list) and "SKILL.md" not in paths:
                errors.append(f"case.skillResourceAllowlist.{skill} must include SKILL.md")
    overlap = set(_string_items(case.get("requiredSkills"))) & set(_string_items(case.get("forbiddenSkills")))
    if overlap:
        errors.append(f"case skills cannot be both required and forbidden: {', '.join(sorted(overlap))}")
    if isinstance(case.get("judgePlan"), Mapping) and isinstance(resource_allowlist, Mapping):
        for skill in _string_items(case.get("requiredSkills")):
            if skill not in resource_allowlist:
                errors.append(f"case.skillResourceAllowlist is missing required skill resources: {skill}")
    return errors


def validate_case(
    case: Mapping[str, object],
    project_root: Path,
    result_path: Path | None,
) -> list[str]:
    """Validate a case definition and its selected fixture and result artifacts."""

    errors = validate_case_definition(case)
    task_path = project_root / str(case.get("task", ""))
    if not task_path.is_file():
        errors.append(f"missing task: {task_path}")
    for skill in _string_items(case.get("requiredSkills")):
        skill_path = ROOT / "skills" / skill / "SKILL.md"
        if not skill_path.is_file():
            errors.append(f"missing skill: {skill}")
    for agent in _string_items(case.get("requiredAgents")):
        if _agent_source(agent) is None:
            errors.append(f"missing agent: {agent}")
    if result_path is not None:
        if not result_path.is_file():
            errors.append(f"missing result: {result_path}")
        else:
            result_text = result_path.read_text(encoding="utf-8")
            headings = case.get("resultHeadings", ["Skills Used", "Evidence Packet", "Review Synthesis"])
            for heading in _string_items(headings):
                if heading not in result_text:
                    errors.append(f"result missing section: {heading}")
    return errors


def load_framework_catalogs(evals_root: Path | None = None) -> dict[str, dict[str, object]]:
    """Load the operational probe, scenario, workflow, Judge, and sandbox catalogs that exist."""

    root = (evals_root or ROOT / "evals").resolve()
    catalogs: dict[str, dict[str, object]] = {}
    for filename in _CATALOG_SPECS:
        path = root / filename
        if not path.is_file():
            continue
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise ValueError(f"{filename} must contain a YAML mapping")
        catalogs[filename] = value
    return catalogs


def validate_framework_catalogs(
    evals_root: Path | None = None,
    cases: Mapping[str, Mapping[str, object]] | None = None,
) -> list[str]:
    """Validate framework catalog shape, harness restrictions, and executable-case links."""

    root = (evals_root or ROOT / "evals").resolve()
    selected_cases = cases or load_cases(root / "cases.yaml")
    errors: list[str] = []
    for case in selected_cases.values():
        errors.extend(f"cases.yaml:{case.get('id')}: {error}" for error in validate_case_definition(case))
    catalogs = load_framework_catalogs(root)
    for filename, data in catalogs.items():
        item_key, required = _CATALOG_SPECS[filename]
        if data.get("schema") is None or data.get("version") is None:
            errors.append(f"{filename} must define schema and version")
        for field in required:
            if field not in data:
                errors.append(f"{filename} missing {field}")
        items = data.get(item_key)
        if not isinstance(items, list):
            errors.append(f"{filename}.{item_key} must be a list")
            continue
        _validate_catalog_items(filename, item_key, items, selected_cases, errors)
        _validate_catalog_harnesses(filename, data, errors)
    judge_catalog = catalogs.get("judges.yaml")
    if judge_catalog is not None:
        judge_types_value = judge_catalog.get("judgeTypes")
        if isinstance(judge_types_value, Mapping):
            declared_judges = {
                str(item["name"])
                for item in judge_types_value.values()
                if isinstance(item, Mapping) and isinstance(item.get("name"), str)
            }
        else:
            declared_judges = _vocabulary_values(judge_types_value)
        if declared_judges != set(JUDGE_TYPES):
            errors.append("judges.yaml judgeTypes must be Deterministic Judge, Model Judge, and Human Judge")
        order = judge_catalog.get("executionOrder")
        if not isinstance(order, list) or not order or not str(order[0]).lower().startswith("deterministic"):
            errors.append("judges.yaml executionOrder must start with Deterministic Judge")
        calibration_policy = judge_catalog.get("calibrationPolicy")
        human_set = calibration_policy.get("humanScoredSet") if isinstance(calibration_policy, Mapping) else None
        if not isinstance(human_set, Mapping):
            errors.append("judges.yaml calibrationPolicy.humanScoredSet must be a mapping")
        else:
            minimums = {
                "minimumExamples": 25,
                "minimumExamplesPerClass": 5,
                "minimumCriticalDefects": 5,
            }
            for field, minimum in minimums.items():
                value = human_set.get(field)
                if not isinstance(value, int) or isinstance(value, bool) or value < minimum:
                    errors.append(
                        f"judges.yaml calibrationPolicy.humanScoredSet.{field} must be at least {minimum}"
                    )
        records = calibration_policy.get("records") if isinstance(calibration_policy, Mapping) else None
        if records is not None and not isinstance(records, list):
            errors.append("judges.yaml calibrationPolicy.records must be a list")
        elif isinstance(records, list):
            catalog_rubrics = _items_by_id(judge_catalog.get("rubrics"))
            for index, record in enumerate(records):
                if not isinstance(record, Mapping):
                    errors.append(f"judges.yaml calibrationPolicy.records[{index}] must be a mapping")
                    continue
                expected = {
                    field: record.get(field)
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
                rubric_id = record.get("rubricId")
                rubric = catalog_rubrics.get(str(rubric_id)) if isinstance(rubric_id, str) else None
                if rubric is None:
                    errors.append(
                        f"judges.yaml calibrationPolicy.records[{index}] must identify a current rubricId"
                    )
                else:
                    expected["rubricSha256"] = case_definition_digest(rubric)
                errors.extend(
                    f"judges.yaml calibrationPolicy.records[{index}]: {error}"
                    for error in validate_calibration_record(record, expected)
                )
    sandbox_catalog = catalogs.get("sandbox-profiles.yaml")
    if sandbox_catalog is not None:
        expected_levels = {"externally-contained", "workspace-isolated-only", "containment-unverified"}
        if _vocabulary_values(sandbox_catalog.get("containmentStatusVocabulary")) != expected_levels:
            errors.append("sandbox-profiles.yaml containmentStatusVocabulary does not match the receipt contract")
    if judge_catalog is not None:
        _validate_unique_ids("judges.yaml.rubrics", judge_catalog.get("rubrics"), errors)
    agent_catalog = catalogs.get("agent-scenarios.yaml")
    if agent_catalog is not None and isinstance(agent_catalog.get("agents"), list):
        scenarios = [
            scenario
            for agent in agent_catalog["agents"]
            if isinstance(agent, Mapping) and isinstance(agent.get("scenarios"), list)
            for scenario in agent["scenarios"]
        ]
        _validate_unique_ids("agent-scenarios.yaml.scenarios", scenarios, errors)
    _validate_catalog_cross_references(catalogs, selected_cases, root, errors)
    return errors


def classify_evidence(
    case: Mapping[str, object],
    evidence_path: Path | None,
) -> EvidenceClassification:
    """Classify execution, verification, and digest staleness for one evidence receipt."""

    if evidence_path is None:
        return EvidenceClassification(False, False, False, ("behavior evaluation requires --evidence",), ())
    if not evidence_path.is_file():
        return EvidenceClassification(False, False, False, (f"missing evidence receipt: {evidence_path}",), ())
    try:
        evidence = yaml.safe_load(evidence_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as error:
        return EvidenceClassification(False, False, False, (f"invalid evidence receipt: {error}",), ())
    if not isinstance(evidence, dict):
        return EvidenceClassification(False, False, False, (f"evidence receipt must be a YAML mapping: {evidence_path}",), ())
    executed = (
        evidence.get("schema") == "dev-methodology-eval-evidence"
        and evidence.get("version") in {1, 2}
        and evidence.get("case") == case.get("id")
    )
    errors: list[str] = []
    stale_reasons: list[str] = []
    if evidence.get("schema") != "dev-methodology-eval-evidence" or evidence.get("version") not in {1, 2}:
        errors.append("evidence receipt has unsupported schema or version")
    if evidence.get("case") != case.get("id"):
        errors.append("evidence receipt case does not match selected case")
    if evidence.get("verdict") != "verified":
        errors.append("evidence receipt verdict must be verified")
    _validate_capture_provenance(evidence, evidence_path, errors)
    if evidence.get("version") == 2:
        _validate_version_two(case, evidence, evidence_path, errors, stale_reasons)
    else:
        _validate_version_one(case, evidence, evidence_path, errors, stale_reasons)
    _validate_forbidden_skill_reads(case, evidence, evidence_path, errors)
    verified = executed and evidence.get("version") == 2 and not errors and not stale_reasons
    return EvidenceClassification(
        executed=executed,
        verified=verified,
        stale_by_digest=bool(stale_reasons),
        errors=tuple(errors),
        stale_reasons=tuple(stale_reasons),
    )


def validate_evidence(case: Mapping[str, object], evidence_path: Path | None) -> list[str]:
    """Return compatibility validation messages, including separately classified stale digests."""

    classification = classify_evidence(case, evidence_path)
    return [*classification.errors, *classification.stale_reasons]


def validate_reference(value: object, field: str, evidence_path: Path, errors: list[str]) -> None:
    """Validate a relative file-marker reference inside the evidence directory."""

    if not isinstance(value, str) or "#" not in value:
        errors.append(f"evidence {field} must be a relative file#marker reference")
        return
    file_name, marker = value.rsplit("#", 1)
    if not file_name or not marker:
        errors.append(f"evidence {field} must include a file and marker")
        return
    target = (evidence_path.parent / file_name).resolve()
    evidence_root = evidence_path.parent.resolve()
    if target != evidence_root and evidence_root not in target.parents:
        errors.append(f"evidence {field} reference escapes the receipt directory")
        return
    if not target.is_file():
        errors.append(f"evidence {field} reference target is missing: {file_name}")
        return
    try:
        referenced_text = target.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        errors.append(f"evidence {field} reference target is not UTF-8 text: {file_name}")
        return
    if marker not in referenced_text:
        errors.append(f"evidence {field} marker is missing from {file_name}: {marker}")


def _validate_reference_digest(
    reference: object,
    expected_digest: object,
    field: str,
    evidence_path: Path,
    errors: list[str],
) -> None:
    validate_reference(reference, field, evidence_path, errors)
    if not isinstance(reference, str) or "#" not in reference:
        return
    target = (evidence_path.parent / reference.rsplit("#", 1)[0]).resolve()
    if target.is_file() and expected_digest != content_digest(target):
        errors.append(f"evidence {field} content digest does not match the governed digest")


def validate_harness_event(
    value: object,
    field: str,
    evidence_path: Path,
    expected: Mapping[str, object],
    errors: list[str],
) -> None:
    """Validate that one reference resolves to exactly one matching JSON Lines event."""

    validate_reference(value, field, evidence_path, errors)
    events = _events_for_reference(value, evidence_path)
    if events is None:
        return
    if len(events) != 1:
        marker = str(value).rsplit("#", 1)[-1]
        errors.append(f"evidence {field} must identify exactly one JSON harness event: {marker}")
        return
    event = events[0]
    for key, expected_value in expected.items():
        if event.get(key) != expected_value:
            errors.append(f"evidence {field} harness event {key} does not match {expected_value}")


def require_non_empty_string(value: object, field: str, errors: list[str]) -> None:
    """Preserve the version-one helper API for callers that build custom receipt checks."""

    _require_non_empty_string(value, field, errors)


def _validate_version_one(
    case: Mapping[str, object],
    evidence: Mapping[str, object],
    evidence_path: Path,
    errors: list[str],
    stale_reasons: list[str],
) -> None:
    agent = evidence.get("agent")
    if not isinstance(agent, Mapping):
        errors.append("evidence agent must be a mapping")
    else:
        if agent.get("id") not in _string_items(case.get("requiredAgents")):
            errors.append("evidence agent id does not match a required agent")
        harness = agent.get("harness")
        if harness not in SUPPORTED_HARNESSES:
            errors.append("evidence agent.harness must be codex or junie")
        for field in ("harness", "model", "invocationEvidence"):
            _require_non_empty_string(agent.get(field), f"agent.{field}", errors)
        validate_harness_event(
            agent.get("invocationEvidence"),
            "agent.invocationEvidence",
            evidence_path,
            {"type": "invocation", "agent": agent.get("id"), "harness": harness, "model": agent.get("model")},
            errors,
        )
    _validate_legacy_skills(case, evidence, evidence_path, errors, stale_reasons)
    _validate_assertions_findings_commands(case, evidence, evidence_path, errors)
    judge = evidence.get("independentVerifier")
    if not isinstance(judge, Mapping):
        errors.append("evidence independentVerifier must be a mapping")
    else:
        _require_non_empty_string(judge.get("kind"), "independentVerifier.kind", errors)
        _require_non_empty_string(judge.get("reference"), "independentVerifier.reference", errors)
        validate_reference(judge.get("reference"), "independentVerifier.reference", evidence_path, errors)
    if case.get("readOnly"):
        before = evidence.get("projectHashBefore")
        after = evidence.get("projectHashAfter")
        _require_non_empty_string(before, "projectHashBefore", errors)
        _require_non_empty_string(after, "projectHashAfter", errors)
        if before != after:
            errors.append("read-only evaluation changed the project hash")


def _validate_version_two(
    case: Mapping[str, object],
    evidence: Mapping[str, object],
    evidence_path: Path,
    errors: list[str],
    stale_reasons: list[str],
) -> None:
    run = evidence.get("run")
    if not isinstance(run, Mapping):
        errors.append("evidence run must be a mapping")
        return
    for field in (
        "id",
        "harness",
        "harnessVersion",
        "harnessDigest",
        "harnessIdentityEvidence",
        "model",
        "modelDigest",
        "modelIdentityEvidence",
        "agentId",
        "conceptualAgentDigest",
        "nativeAdapterSourceDigest",
        "nativeAdapterEffectiveDigest",
        "invocationEvidence",
        "agentStartEvidence",
        "attributionStatus",
        "eventLedger",
        "contextPackDigest",
        "contextPackEvidence",
        "approvedInputManifestDigest",
        "caseDefinitionDigest",
    ):
        _require_non_empty_string(run.get(field), f"run.{field}", errors)
    for field in (
        "harnessDigest",
        "modelDigest",
        "conceptualAgentDigest",
        "nativeAdapterSourceDigest",
        "nativeAdapterEffectiveDigest",
        "contextPackDigest",
        "approvedInputManifestDigest",
        "caseDefinitionDigest",
    ):
        _require_digest(run.get(field), f"run.{field}", errors)
    for field in ("harnessIdentityEvidence", "modelIdentityEvidence", "contextPackEvidence"):
        validate_reference(run.get(field), f"run.{field}", evidence_path, errors)
    if not isinstance(run.get("installExecuted"), bool):
        errors.append("evidence run.installExecuted must be a boolean")
    if run.get("caseDefinitionDigest") != case_definition_digest(case):
        stale_reasons.append("evidence case definition digest mismatch")
    if isinstance(case.get("probeId"), str):
        if run.get("probeId") != case.get("probeId"):
            errors.append("evidence run.probeId does not match the selected probe")
        if run.get("probeVariant") != case.get("probeVariant"):
            errors.append("evidence run.probeVariant does not match the selected probe variant")
        if run.get("probeComparisonKey") != case.get("probeComparisonKey"):
            errors.append("evidence run.probeComparisonKey does not bind the frozen probe triplet")
        if run.get("probeVariant") not in {"treatment", "target-omitted", "wrong-skill"}:
            errors.append("evidence run.probeVariant is invalid")
    elif any(field in run for field in ("probeId", "probeVariant", "probeComparisonKey")):
        errors.append("evidence run cannot claim a probe variant for a base case")
    harness = run.get("harness")
    if harness not in SUPPORTED_HARNESSES:
        errors.append("evidence run.harness must be codex or junie")
    allowed_harnesses = case.get("harnesses", sorted(SUPPORTED_HARNESSES))
    if isinstance(allowed_harnesses, list) and harness not in allowed_harnesses:
        errors.append("evidence run.harness is not allowed by the case")
    if run.get("agentId") not in _string_items(case.get("requiredAgents")):
        errors.append("evidence run.agentId does not match a required agent")
    source = _agent_source(str(run.get("agentId", "")))
    if source is None:
        errors.append(f"evidence agent source is missing: {run.get('agentId')}")
    elif run.get("conceptualAgentDigest") != content_digest(source):
        stale_reasons.append(f"evidence conceptual agent digest mismatch: {run.get('agentId')}")
    if harness in SUPPORTED_HARNESSES and isinstance(run.get("agentId"), str):
        try:
            adapter_identity = build_agent_evidence_identity(harness, str(run["agentId"]))
        except ValueError as error:
            errors.append(f"evidence native adapter identity is unavailable: {error}")
        else:
            for field in ("nativeAdapterSourceDigest", "nativeAdapterEffectiveDigest"):
                if run.get(field) != adapter_identity[field]:
                    stale_reasons.append(f"evidence {field} mismatch: {run.get('agentId')}")
            if run.get("nativeAdapterSanitizations") != adapter_identity["nativeAdapterSanitizations"]:
                stale_reasons.append(f"evidence native adapter sanitizations mismatch: {run.get('agentId')}")
    validate_harness_event(
        run.get("invocationEvidence"),
        "run.invocationEvidence",
        evidence_path,
        {
            "type": "invocation",
            "agent": run.get("agentId"),
            "harness": harness,
            "model": run.get("model"),
        },
        errors,
    )
    validate_reference(run.get("eventLedger"), "run.eventLedger", evidence_path, errors)
    ledger_events = _all_events_for_reference(run.get("eventLedger"), evidence_path)
    if run.get("attributionStatus") not in {"verified", "unverified"}:
        errors.append("evidence run.attributionStatus must be verified or unverified")
    if run.get("attributionStatus") == "verified":
        validate_harness_event(
            run.get("agentStartEvidence"),
            "run.agentStartEvidence",
            evidence_path,
            {
                "type": "agent-start",
                "agent": run.get("agentId"),
                "contentDigest": run.get("nativeAdapterEffectiveDigest"),
            },
            errors,
        )
        if not agent_attribution_verified(
            ledger_events,
            str(run.get("agentId")),
            str(run.get("nativeAdapterEffectiveDigest")),
        ):
            errors.append(f"{harness} agent attribution lacks a matching digest-bound agent-start event")
    if run.get("attributionStatus") != "verified":
        errors.append("evidence agent attribution must be verified")

    _validate_skills(case, harness, evidence, evidence_path, errors, stale_reasons)
    _validate_budgets(evidence.get("budgets"), errors)
    _validate_prepared_fixture(case, evidence.get("preparedFixture"), evidence_path, errors, stale_reasons)
    _validate_isolation(case, harness, evidence.get("isolation"), evidence_path, errors)
    _validate_judges(case, evidence.get("judges"), evidence_path, errors, stale_reasons)
    _validate_assertions_findings_commands(case, evidence, evidence_path, errors)
    independent_judge = evidence.get("independentJudge")
    if not isinstance(independent_judge, Mapping):
        errors.append("evidence independentJudge must be a mapping")
    else:
        _validate_independent_judge(independent_judge, run, evidence_path, errors)


def _validate_skills(
    case: Mapping[str, object],
    harness: object,
    evidence: Mapping[str, object],
    evidence_path: Path,
    errors: list[str],
    stale_reasons: list[str],
) -> None:
    receipt_skills: dict[str, Mapping[str, object]] = {}
    skills = evidence.get("skills")
    if not isinstance(skills, list):
        errors.append("evidence skills must be a list")
        return
    for item in skills:
        if not isinstance(item, Mapping) or not isinstance(item.get("id"), str):
            errors.append("each evidence skill must be a mapping with id")
            continue
        receipt_skills[str(item["id"])] = item
    extra_skills = sorted(set(receipt_skills) - set(_string_items(case.get("requiredSkills"))))
    for skill in extra_skills:
        errors.append(f"evidence includes a skill outside case.requiredSkills: {skill}")
    for skill in _string_items(case.get("requiredSkills")):
        item = receipt_skills.get(skill)
        if item is None:
            errors.append(f"evidence missing required skill: {skill}")
            continue
        if harness not in SUPPORTED_HARNESSES:
            errors.append(f"evidence cannot resolve skill identity for unsupported harness: {harness}")
            continue
        try:
            expected = build_skill_evidence_identity(case, str(harness), skill)
        except ValueError as error:
            errors.append(f"evidence skill identity is unavailable for {skill}: {error}")
            continue
        for field in ("sourceDigest", "effectiveDigest", "resourceManifestDigest"):
            if item.get(field) != expected[field]:
                stale_reasons.append(f"evidence skill {field} mismatch: {skill}")
        if item.get("resources") != expected["resources"]:
            stale_reasons.append(f"evidence skill resource manifest mismatch: {skill}")
        read_evidence = item.get("readEvidence")
        if not isinstance(read_evidence, list) or not read_evidence:
            errors.append(f"evidence missing skill read tool evidence: {skill}")
            continue
        for index, value in enumerate(read_evidence):
            if not isinstance(value, Mapping) or value.get("type") != "tool-call" or not value.get("reference"):
                errors.append(f"skill read evidence must contain tool-call references: {skill}")
                continue
            validate_harness_event(
                value["reference"],
                f"skills.{skill}.readEvidence[{index}]",
                evidence_path,
                {"type": "tool-call", "skill": skill, "contentDigest": item.get("effectiveDigest")},
                errors,
            )


def _validate_legacy_skills(
    case: Mapping[str, object],
    evidence: Mapping[str, object],
    evidence_path: Path,
    errors: list[str],
    stale_reasons: list[str],
) -> None:
    receipt_skills = {
        str(item["id"]): item
        for item in evidence.get("skills", [])
        if isinstance(item, Mapping) and isinstance(item.get("id"), str)
    } if isinstance(evidence.get("skills"), list) else {}
    if not isinstance(evidence.get("skills"), list):
        errors.append("evidence skills must be a list")
        return
    for skill in _string_items(case.get("requiredSkills")):
        item = receipt_skills.get(skill)
        if item is None:
            errors.append(f"evidence missing required skill: {skill}")
            continue
        source = ROOT / "skills" / skill / "SKILL.md"
        if not source.is_file():
            errors.append(f"evidence skill source is missing: {skill}")
        elif item.get("contentDigest") != content_digest(source):
            stale_reasons.append(f"evidence skill digest mismatch: {skill}")
        read_evidence = item.get("readEvidence")
        if not isinstance(read_evidence, list) or not read_evidence:
            errors.append(f"evidence missing skill read tool evidence: {skill}")
            continue
        for index, value in enumerate(read_evidence):
            if not isinstance(value, Mapping) or value.get("type") != "tool-call" or not value.get("reference"):
                errors.append(f"skill read evidence must contain tool-call references: {skill}")
                continue
            validate_harness_event(
                value["reference"],
                f"skills.{skill}.readEvidence[{index}]",
                evidence_path,
                {"type": "tool-call", "skill": skill, "contentDigest": item.get("contentDigest")},
                errors,
            )


def _validate_assertions_findings_commands(
    case: Mapping[str, object],
    evidence: Mapping[str, object],
    evidence_path: Path,
    errors: list[str],
) -> None:
    assertions = evidence.get("behaviorAssertions")
    assertion_by_id = {
        str(item.get("id")): item
        for item in assertions
        if isinstance(item, Mapping)
    } if isinstance(assertions, list) else {}
    if not isinstance(assertions, list):
        errors.append("evidence behaviorAssertions must be a list")
    for assertion_id in _string_items(case.get("requiredEvidence")):
        item = assertion_by_id.get(assertion_id)
        if item is None:
            errors.append(f"evidence missing behavior assertion: {assertion_id}")
        elif item.get("verdict") != "passed" or not item.get("evidence"):
            errors.append(f"behavior assertion lacks passed evidence: {assertion_id}")
        else:
            validate_reference(item["evidence"], f"behaviorAssertions.{assertion_id}.evidence", evidence_path, errors)
    findings = evidence.get("findings", [])
    finding_by_id = {
        str(item.get("id")): item
        for item in findings
        if isinstance(item, Mapping) and item.get("evidence")
    } if isinstance(findings, list) else {}
    for finding_id in _string_items(case.get("requiredFindings")):
        item = finding_by_id.get(finding_id)
        if item is None:
            errors.append(f"evidence missing expected finding: {finding_id}")
        else:
            validate_reference(item["evidence"], f"findings.{finding_id}.evidence", evidence_path, errors)
    commands = evidence.get("commands")
    if not isinstance(commands, list) or not commands:
        errors.append("evidence commands must be a non-empty list")
        return
    normalized_commands: list[tuple[tuple[str, ...], Mapping[str, object]]] = []
    for item in commands:
        if not isinstance(item, Mapping):
            errors.append("each command evidence item must be a mapping")
            continue
        command_value = item.get("argv", item.get("command"))
        try:
            normalized = command_spec(command_value)
        except ValueError as error:
            errors.append(f"evidence command is invalid: {error}")
        else:
            normalized_commands.append((normalized.argv, item))
        if not isinstance(item.get("exitCode"), int) or isinstance(item.get("exitCode"), bool):
            errors.append("command exitCode must be an integer")
        _require_non_empty_string(item.get("expectation"), "commands.expectation", errors)
        _require_non_empty_string(item.get("evidence"), "commands.evidence", errors)
        validate_reference(item.get("evidence"), "commands.evidence", evidence_path, errors)
    try:
        verify_argv = command_spec(case.get("verify")).argv
    except ValueError:
        verify_argv = ()
    _validate_required_command_match(
        normalized_commands,
        verify_argv,
        "case.verify",
        expect_failure=bool(case.get("expectVerifyFailure")),
        errors=errors,
    )
    run = evidence.get("run")
    if isinstance(run, Mapping) and run.get("installExecuted") is True and case.get("install") is not None:
        try:
            install_argv = command_spec(case.get("install")).argv
        except ValueError:
            install_argv = ()
        _validate_required_command_match(
            normalized_commands,
            install_argv,
            "case.install",
            expect_failure=False,
            errors=errors,
        )


def _validate_required_command_match(
    commands: Sequence[tuple[tuple[str, ...], Mapping[str, object]]],
    expected_argv: tuple[str, ...],
    label: str,
    *,
    expect_failure: bool,
    errors: list[str],
) -> None:
    matches = [item for argv, item in commands if argv == expected_argv]
    if len(matches) != 1:
        errors.append(f"evidence commands must contain exactly one normalized {label} command")
        return
    item = matches[0]
    exit_code = item.get("exitCode")
    expected_label = "expected-failure" if expect_failure else "success"
    if item.get("expectation") != expected_label:
        errors.append(f"evidence {label} expectation must be {expected_label}")
    if expect_failure and isinstance(exit_code, int) and not isinstance(exit_code, bool) and exit_code == 0:
        errors.append(f"evidence {label} must record a non-zero expected-failure exit code")
    if not expect_failure and exit_code != 0:
        errors.append(f"evidence {label} must record exit code zero")


def _validate_budgets(value: object, errors: list[str]) -> None:
    if not isinstance(value, Mapping):
        errors.append("evidence budgets must be a mapping")
        return
    limits = value.get("limits")
    usage = value.get("usage")
    if not isinstance(limits, Mapping) or not isinstance(usage, Mapping):
        errors.append("evidence budgets limits and usage must be mappings")
        return
    for field in ("turns", "tokens", "seconds", "toolCalls"):
        limit = limits.get(field)
        consumed = usage.get(field)
        if not isinstance(limit, (int, float)) or isinstance(limit, bool) or limit < 0:
            errors.append(f"evidence budgets.limits.{field} must be a non-negative number")
        if not isinstance(consumed, (int, float)) or isinstance(consumed, bool) or consumed < 0:
            errors.append(f"evidence budgets.usage.{field} must be a non-negative number")
        if isinstance(limit, (int, float)) and isinstance(consumed, (int, float)) and consumed > limit:
            errors.append(f"evidence budget exceeded: {field}")


def _validate_prepared_fixture(
    case: Mapping[str, object],
    value: object,
    evidence_path: Path,
    errors: list[str],
    stale_reasons: list[str],
) -> None:
    if not isinstance(value, Mapping):
        errors.append("evidence preparedFixture must be a mapping")
        return
    for field in (
        "key",
        "sourceDigest",
        "dependencyDigest",
        "toolchainDigest",
        "preparationEnvironmentDigest",
    ):
        _require_digest(value.get(field), f"preparedFixture.{field}", errors)
    platform_value = value.get("platform")
    if not isinstance(platform_value, Mapping):
        errors.append("evidence preparedFixture.platform must be a mapping")
    else:
        for field in ("system", "release", "machine"):
            _require_non_empty_string(platform_value.get(field), f"preparedFixture.platform.{field}", errors)
    validate_reference(value.get("toolchainEvidence"), "preparedFixture.toolchainEvidence", evidence_path, errors)
    validate_reference(
        value.get("preparationEnvironmentEvidence"),
        "preparedFixture.preparationEnvironmentEvidence",
        evidence_path,
        errors,
    )
    project = ROOT / str(case.get("project", ""))
    if not project.is_dir():
        errors.append(f"evidence fixture source is missing: {project}")
        return
    current_source = snapshot_digest(snapshot_tree(project, exclude_transient=True))
    current_dependencies = dependency_inputs_digest(project)
    if value.get("sourceDigest") != current_source:
        stale_reasons.append("evidence prepared fixture sourceDigest mismatch")
    if value.get("dependencyDigest") != current_dependencies:
        stale_reasons.append("evidence prepared fixture dependencyDigest mismatch")
    if all(isinstance(value.get(field), str) for field in ("sourceDigest", "dependencyDigest", "toolchainDigest")):
        expected_key = prepared_fixture_identity_key(
            str(value["sourceDigest"]),
            str(value["dependencyDigest"]),
            str(value["toolchainDigest"]),
            case.get("install"),
            str(value.get("preparationEnvironmentDigest", "")),
        )
        if value.get("key") != expected_key:
            stale_reasons.append("evidence prepared fixture key does not match its governed inputs")


def _validate_isolation(
    case: Mapping[str, object],
    harness: object,
    value: object,
    evidence_path: Path,
    errors: list[str],
) -> None:
    if not isinstance(value, Mapping):
        errors.append("evidence isolation must be a mapping")
        return
    if value.get("workspacePreparation") not in {"copy-on-write", "full-copy"}:
        errors.append("evidence isolation.workspacePreparation must be copy-on-write or full-copy")
    functional = value.get("functional")
    if not isinstance(functional, Mapping):
        errors.append("evidence isolation.functional must be a mapping")
    else:
        if functional.get("status") != "verified":
            errors.append("evidence functional isolation status must be verified")
        before = functional.get("projectHashBefore")
        after = functional.get("projectHashAfter")
        _require_non_empty_string(before, "isolation.functional.projectHashBefore", errors)
        _require_non_empty_string(after, "isolation.functional.projectHashAfter", errors)
        _validate_string_list(functional.get("allowedWritePaths", []), "isolation.functional.allowedWritePaths", errors)
        _validate_string_list(functional.get("changedPaths"), "isolation.functional.changedPaths", errors)
        receipt_allowed = set(_string_items(functional.get("allowedWritePaths")))
        configured_allowed = set(_string_items(case.get("allowedWritePaths"))) if isinstance(
            case.get("judgePlan"), Mapping,
        ) else set(receipt_allowed)
        if not receipt_allowed.issubset(configured_allowed):
            errors.append("evidence functional allowedWritePaths exceeds the case contract")
        changed_paths = set(_string_items(functional.get("changedPaths")))
        protected = set(_string_items(case.get("protectedPaths")))
        for path in sorted(changed_paths):
            if not case.get("readOnly") and not _relative_path_is_allowed(path, receipt_allowed):
                errors.append(f"evidence functional changed path is outside allowedWritePaths: {path}")
            if _relative_path_is_allowed(path, protected):
                errors.append(f"evidence functional changed a protected path: {path}")
        validate_reference(functional.get("evidence"), "isolation.functional.evidence", evidence_path, errors)
        if case.get("readOnly") and before != after:
            errors.append("read-only evaluation changed the project hash")
        if case.get("readOnly") and changed_paths:
            errors.append("read-only evaluation reports changed product paths")
    containment = value.get("containment")
    if not isinstance(containment, Mapping):
        errors.append("evidence isolation.containment must be a mapping")
    else:
        level = containment.get("level")
        if level not in _containment_levels():
            errors.append("evidence containment level is not declared by the sandbox vocabulary")
        if containment.get("status") not in {"verified", "unverified", "failed"}:
            errors.append("evidence containment status must be verified, unverified, or failed")
        _require_non_empty_string(containment.get("enforcedBy"), "isolation.containment.enforcedBy", errors)
        if level == "containment-unverified" and containment.get("status") != "unverified":
            errors.append("containment-unverified level must have unverified evidence status")
        if level == "externally-contained" and containment.get("status") != "verified":
            errors.append("externally-contained level must have verified evidence status")
        if containment.get("status") == "verified":
            validate_reference(containment.get("evidence"), "isolation.containment.evidence", evidence_path, errors)
        minimums = case.get("minimumContainment")
        minimum = minimums.get(harness) if isinstance(minimums, Mapping) else None
        ranks = {"containment-unverified": 0, "workspace-isolated-only": 1, "externally-contained": 2}
        if minimum in ranks and level in ranks and ranks[str(level)] < ranks[str(minimum)]:
            errors.append(f"evidence containment level does not meet the case minimum for {harness}: {minimum}")
    sandbox_profiles = case.get("sandboxProfiles")
    if isinstance(sandbox_profiles, Mapping) and harness in sandbox_profiles:
        profile_id = sandbox_profiles[harness]
        if value.get("sandboxProfile") != profile_id:
            errors.append(f"evidence isolation.sandboxProfile must be {profile_id}")
        profiles = _items_by_id(load_framework_catalogs().get("sandbox-profiles.yaml", {}).get("profiles"))
        profile = profiles.get(str(profile_id))
        if profile is None:
            errors.append(f"evidence sandbox profile source is missing: {profile_id}")
        elif value.get("sandboxProfileDigest") != case_definition_digest(profile):
            errors.append(f"evidence sandbox profile digest mismatch: {profile_id}")
        validate_reference(
            value.get("sandboxProfileEvidence"),
            "isolation.sandboxProfileEvidence",
            evidence_path,
            errors,
        )
    if harness == "codex":
        native = value.get("codexNativeSandbox")
        if not isinstance(native, Mapping):
            errors.append("evidence isolation.codexNativeSandbox must be a mapping")
        else:
            expected_mode = "read-only" if case.get("readOnly") else "workspace-write"
            if native.get("mode") != expected_mode:
                errors.append(f"evidence Codex native sandbox mode must be {expected_mode}")
            validate_reference(native.get("evidence"), "isolation.codexNativeSandbox.evidence", evidence_path, errors)
    if harness == "junie":
        external = value.get("junieExternalContainment")
        if not isinstance(external, Mapping):
            errors.append("evidence isolation.junieExternalContainment must be a mapping")
        else:
            if external.get("capability") not in {"self-attested", "unavailable"}:
                errors.append("Junie external containment capability must be self-attested or unavailable")
            if external.get("status") not in {"verified", "unverified", "failed"}:
                errors.append("Junie external containment status must be verified, unverified, or failed")
            if external.get("capability") == "unavailable" and external.get("status") != "unverified":
                errors.append("unavailable Junie external containment must be unverified")
            if external.get("capability") == "self-attested":
                _require_digest(external.get("runnerDigest"), "isolation.junieExternalContainment.runnerDigest", errors)
                _require_digest(
                    external.get("attestationDigest"),
                    "isolation.junieExternalContainment.attestationDigest",
                    errors,
                )
                if external.get("status") != "unverified":
                    errors.append("self-attested Junie containment must remain unverified without a trust anchor")
            if isinstance(containment, Mapping) and (
                containment.get("level") == "externally-contained"
                or containment.get("status") == "verified"
            ):
                errors.append("Junie self-attestation cannot establish externally-contained verified evidence")
                validate_reference(
                    external.get("evidence"),
                    "isolation.junieExternalContainment.evidence",
                    evidence_path,
                    errors,
                )
            if isinstance(containment, Mapping) and external.get("status") != containment.get("status"):
                errors.append("Junie external containment status must match the containment status")


def _validate_judges(
    case: Mapping[str, object],
    value: object,
    evidence_path: Path,
    errors: list[str],
    stale_reasons: list[str],
) -> None:
    if not isinstance(value, Mapping):
        errors.append("evidence judges must be a mapping")
        return
    deterministic = value.get("deterministic")
    critical_deterministic_failed = False
    plan = case.get("judgePlan")
    required_check_ids = set(_string_items(plan.get("deterministicChecks"))) if isinstance(plan, Mapping) else set()
    judge_catalog = load_framework_catalogs().get("judges.yaml", {})
    check_definitions = _items_by_id(judge_catalog.get("checks"))
    rubric_definitions = _items_by_id(judge_catalog.get("rubrics"))
    if not isinstance(deterministic, Mapping):
        errors.append("evidence judges.deterministic must be a mapping")
    else:
        if deterministic.get("verdict") not in {"passed", "failed"}:
            errors.append("Deterministic Judge verdict must be passed or failed")
        records = deterministic.get("records")
        if not isinstance(records, list) or not records:
            errors.append("Deterministic Judge records must be a non-empty list")
        else:
            observed_ids: list[str] = []
            observed_verdicts: list[str] = []
            for index, record in enumerate(records):
                if not isinstance(record, Mapping):
                    errors.append("each Deterministic Judge record must be a mapping")
                else:
                    check_id = record.get("checkId", record.get("id"))
                    if not isinstance(check_id, str) or not check_id:
                        errors.append("each Deterministic Judge record must identify a checkId")
                        continue
                    if record.get("id") is not None and record.get("checkId") is not None and record.get("id") != check_id:
                        errors.append(f"Deterministic Judge record id and checkId disagree: {check_id}")
                    observed_ids.append(check_id)
                    definition = check_definitions.get(check_id)
                    if required_check_ids and definition is None:
                        errors.append(f"Deterministic Judge record uses unknown check: {check_id}")
                    expected_critical = definition.get("critical") if definition is not None else None
                    if not isinstance(record.get("critical"), bool):
                        errors.append("each Deterministic Judge record must declare critical as a boolean")
                    elif expected_critical is not None and record.get("critical") != expected_critical:
                        errors.append(f"Deterministic Judge critical flag does not match catalog: {check_id}")
                    verdict = record.get("verdict")
                    if verdict not in {"passed", "failed"}:
                        errors.append(f"Deterministic Judge record verdict is invalid: {check_id}")
                    else:
                        observed_verdicts.append(str(verdict))
                    if record.get("critical") is True and record.get("verdict") != "passed":
                        critical_deterministic_failed = True
                    validate_reference(
                        record.get("evidence"),
                        f"judges.deterministic.records[{index}].evidence",
                        evidence_path,
                        errors,
                    )
            duplicates = sorted({check_id for check_id in observed_ids if observed_ids.count(check_id) > 1})
            for check_id in duplicates:
                errors.append(f"Deterministic Judge record is duplicated: {check_id}")
            if required_check_ids:
                observed = set(observed_ids)
                for check_id in sorted(required_check_ids - observed):
                    errors.append(f"Deterministic Judge record is missing required check: {check_id}")
                for check_id in sorted(observed - required_check_ids):
                    errors.append(f"Deterministic Judge record is not configured for the case: {check_id}")
            expected_verdict = "passed" if observed_verdicts and all(
                verdict == "passed" for verdict in observed_verdicts
            ) else "failed"
            if deterministic.get("verdict") != expected_verdict:
                errors.append("Deterministic Judge aggregate verdict does not match its records")
    model = value.get("model")
    if not isinstance(model, Mapping):
        errors.append("evidence judges.model must be a mapping")
        return
    status = model.get("status")
    if status not in {"passed", "failed", "skipped-deterministic-failure", "not-required"}:
        errors.append("Model Judge status is invalid")
        return
    if critical_deterministic_failed and status != "skipped-deterministic-failure":
        errors.append("Model Judge must be skipped after a critical Deterministic Judge failure")
    if critical_deterministic_failed:
        errors.append("critical Deterministic Judge verdict must be passed")
    model_rubric = plan.get("modelRubric") if isinstance(plan, Mapping) else None
    if model_rubric is not None and model_rubric not in rubric_definitions:
        errors.append(f"case references an unknown Model Judge rubric: {model_rubric}")
    rubric_definition = rubric_definitions.get(str(model_rubric)) if model_rubric is not None else None
    if rubric_definition is not None and status in {"passed", "failed"}:
        dimensions_pass = _validate_model_dimension_scores(model, rubric_definition, evidence_path, errors)
        derived_status = "passed" if dimensions_pass else "failed"
        if status != derived_status:
            errors.append(f"Model Judge status must be {derived_status} under the current rubric pass rules")
    if not critical_deterministic_failed and model_rubric is not None and status != "passed":
        errors.append("case requires a passed Model Judge")
    if status == "passed":
        if model_rubric is not None and model.get("rubricId") != model_rubric:
            errors.append(f"Model Judge rubricId must be {model_rubric}")
        current_rubric_digest = case_definition_digest(rubric_definition) if rubric_definition is not None else None
        if current_rubric_digest is not None and model.get("rubricSha256") != current_rubric_digest:
            stale_reasons.append(f"Model Judge rubric digest mismatch: {model_rubric}")
        _validate_reference_digest(
            model.get("judgePromptEvidence"),
            model.get("judgePromptSha256"),
            "judges.model.judgePromptEvidence",
            evidence_path,
            errors,
        )
        validate_reference(
            model.get("judgeModelIdentityEvidence"),
            "judges.model.judgeModelIdentityEvidence",
            evidence_path,
            errors,
        )
        validate_reference(
            model.get("reasoningProfileEvidence"),
            "judges.model.reasoningProfileEvidence",
            evidence_path,
            errors,
        )
        expected = {
            "rubricId": model_rubric,
            "judgePromptSha256": model.get("judgePromptSha256"),
            "judgeOutputSchemaSha256": model.get("judgeOutputSchemaSha256"),
            "instructionEnvelopeSha256": model.get("instructionEnvelopeSha256"),
            "harness": model.get("harness"),
            "judgeModelIdentity": model.get("judgeModelIdentity"),
            "reasoningProfile": model.get("reasoningProfile"),
            "rubricSha256": current_rubric_digest or model.get("rubricSha256"),
            "calibrationSetSha256": model.get("calibrationSetSha256"),
        }
        calibration = model.get("calibration")
        if not isinstance(calibration, Mapping):
            errors.append("passed Model Judge requires a calibration record")
        else:
            calibration_errors = validate_calibration_record(calibration, expected)  # type: ignore[arg-type]
            for error in calibration_errors:
                if "stale" in error or "recordDigest" in error:
                    stale_reasons.append(error)
                else:
                    errors.append(error)
        validate_reference(model.get("evidence"), "judges.model.evidence", evidence_path, errors)


def _validate_capture_provenance(
    evidence: Mapping[str, object],
    evidence_path: Path,
    errors: list[str],
) -> None:
    provenance = evidence.get("captureProvenance")
    if not isinstance(provenance, Mapping):
        errors.append("evidence captureProvenance must be a mapping")
        return
    if provenance.get("kind") not in {"trusted-ci", "human-attested-harness-export"}:
        errors.append("evidence captureProvenance.kind must identify a trusted capture source")
    validate_reference(provenance.get("reference"), "captureProvenance.reference", evidence_path, errors)


def _validate_independent_judge(
    judge: Mapping[str, object],
    run: Mapping[str, object],
    evidence_path: Path,
    errors: list[str],
) -> None:
    if judge.get("kind") not in {"Deterministic Judge", "Model Judge", "Human Judge"}:
        errors.append("evidence independentJudge.kind must use a supported Judge type")
    for field in (
        "invocationId",
        "contextIdentity",
        "modelIdentity",
        "reasoningProfile",
        "evaluatedRunId",
    ):
        _require_non_empty_string(judge.get(field), f"independentJudge.{field}", errors)
    for field in ("judgePromptSha256", "inputManifestDigest"):
        _require_digest(judge.get(field), f"independentJudge.{field}", errors)
    for field in ("reference", "invocationEvidence", "contextEvidence", "inputManifestEvidence"):
        validate_reference(judge.get(field), f"independentJudge.{field}", evidence_path, errors)
    _validate_reference_digest(
        judge.get("judgePromptEvidence"),
        judge.get("judgePromptSha256"),
        "independentJudge.judgePromptEvidence",
        evidence_path,
        errors,
    )
    if judge.get("evaluatedRunId") != run.get("id"):
        errors.append("independent Judge must link to the evaluated run id")
    if judge.get("invocationId") == run.get("id"):
        errors.append("independent Judge invocation must differ from the evaluated run")
    if judge.get("contextIdentity") in {run.get("contextPackDigest"), run.get("approvedInputManifestDigest")}:
        errors.append("independent Judge context must differ from the evaluated run context")
    blindness = set(_string_items(judge.get("blindTo")))
    required_blindness = {"treatment", "expected-winner", "evaluated-model-identity"}
    if not required_blindness.issubset(blindness):
        errors.append("independent Judge blindness must cover treatment, expected winner, and evaluated model identity")
    if judge.get("kind") == "Human Judge":
        _require_non_empty_string(judge.get("adjudicatorId"), "independentJudge.adjudicatorId", errors)
        validate_reference(
            judge.get("adjudicationEvidence"),
            "independentJudge.adjudicationEvidence",
            evidence_path,
            errors,
        )


def _validate_model_dimension_scores(
    model: Mapping[str, object],
    rubric: Mapping[str, object],
    evidence_path: Path,
    errors: list[str],
) -> bool:
    dimensions = rubric.get("dimensions")
    expected_ids = [
        str(item.get("id")) if isinstance(item, Mapping) else str(item)
        for item in dimensions
    ] if isinstance(dimensions, list) else []
    values = model.get("dimensionScores")
    if not isinstance(values, list):
        errors.append("Model Judge dimensionScores must be a list")
        return False
    by_id: dict[str, Mapping[str, object]] = {}
    observed_order: list[str] = []
    duplicate_ids: set[str] = set()
    for index, item in enumerate(values):
        if not isinstance(item, Mapping) or not isinstance(item.get("id"), str):
            errors.append(f"Model Judge dimensionScores[{index}] must identify a dimension")
            continue
        dimension_id = str(item["id"])
        observed_order.append(dimension_id)
        if dimension_id in by_id:
            duplicate_ids.add(dimension_id)
        by_id[dimension_id] = item
    for dimension_id in sorted(duplicate_ids):
        errors.append(f"Model Judge dimension score is duplicated: {dimension_id}")
    if observed_order != expected_ids:
        errors.append("Model Judge dimension score order must exactly match the current rubric")
    missing = sorted(set(expected_ids) - set(by_id))
    extra = sorted(set(by_id) - set(expected_ids))
    for dimension_id in missing:
        errors.append(f"Model Judge dimension score is missing: {dimension_id}")
    for dimension_id in extra:
        errors.append(f"Model Judge dimension score is not in the rubric: {dimension_id}")
    valid_scores: dict[str, int] = {}
    for dimension_id in expected_ids:
        item = by_id.get(dimension_id)
        if item is None:
            continue
        score = item.get("score")
        if not isinstance(score, int) or isinstance(score, bool) or not 0 <= score <= 4:
            errors.append(f"Model Judge dimension score must be an integer from 0 through 4: {dimension_id}")
        else:
            valid_scores[dimension_id] = score
        if not isinstance(item.get("critical"), bool):
            errors.append(f"Model Judge dimension critical flag must be a boolean: {dimension_id}")
        rationale = item.get("rationale")
        if not isinstance(rationale, str) or not rationale.strip():
            errors.append(f"Model Judge dimension rationale is required: {dimension_id}")
        references = item.get("evidenceReferences")
        if not isinstance(references, list) or not references:
            errors.append(f"Model Judge dimension evidenceReferences must be non-empty: {dimension_id}")
        else:
            observed_references: set[tuple[str, str]] = set()
            for reference in references:
                if not isinstance(reference, Mapping):
                    errors.append(f"Model Judge evidence reference must be a mapping: {dimension_id}")
                    continue
                document_id = reference.get("documentId")
                locator = reference.get("locator")
                if not isinstance(document_id, str) or not document_id or not isinstance(locator, str) or not locator:
                    errors.append(f"Model Judge evidence reference must identify documentId and locator: {dimension_id}")
                    continue
                identity = (document_id, locator)
                if identity in observed_references:
                    errors.append(f"Model Judge evidence reference is duplicated: {dimension_id}")
                observed_references.add(identity)
    rules = rubric.get("passRules")
    if not isinstance(rules, Mapping) or set(valid_scores) != set(expected_ids):
        return False
    minimum = rules.get("minimumDimensionScore", 0)
    if not isinstance(minimum, int) or isinstance(minimum, bool) or not 0 <= minimum <= 4:
        errors.append("Model Judge rubric minimumDimensionScore must be an integer from 0 through 4")
        return False
    overrides = rules.get("minimumDimensionScores", {})
    if not isinstance(overrides, Mapping) or any(
        dimension_id not in expected_ids
        or not isinstance(score, int)
        or isinstance(score, bool)
        or not 0 <= score <= 4
        for dimension_id, score in overrides.items()
    ):
        errors.append("Model Judge rubric minimumDimensionScores must map known dimensions to zero-through-four integers")
        return False
    passed = all(
        score >= int(overrides.get(dimension_id, minimum))
        for dimension_id, score in valid_scores.items()
    )
    critical_dimensions = rules.get("criticalDimensions", [])
    if not isinstance(critical_dimensions, list) or any(
        dimension_id not in expected_ids for dimension_id in critical_dimensions
    ):
        errors.append("Model Judge rubric criticalDimensions must list known dimension ids")
        return False
    for dimension_id in expected_ids:
        item = by_id.get(dimension_id)
        if item is not None and item.get("critical") is not (dimension_id in critical_dimensions):
            errors.append(f"Model Judge critical flag does not match the current rubric: {dimension_id}")
    passed = passed and all(
        valid_scores[dimension_id] >= int(overrides.get(dimension_id, minimum))
        for dimension_id in critical_dimensions
    )
    contradiction_maximum = rules.get("contradictionMaximum")
    if contradiction_maximum is not None:
        contradiction_score = valid_scores.get("contradiction")
        if not isinstance(contradiction_maximum, int) or contradiction_score is None:
            errors.append("Model Judge rubric contradictionMaximum requires a contradiction dimension")
            passed = False
        else:
            passed = passed and contradiction_score <= contradiction_maximum
    overall = model.get("overall")
    recomputed_verdict = "pass" if passed else "fail"
    recomputed_critical = any(
        valid_scores.get(dimension_id, -1) < int(overrides.get(dimension_id, minimum))
        for dimension_id in critical_dimensions
    )
    if not isinstance(overall, Mapping):
        errors.append("Model Judge overall must be a mapping")
    else:
        if overall.get("verdict") != recomputed_verdict:
            errors.append(f"Model Judge overall verdict must be {recomputed_verdict}")
        if overall.get("criticalFailure") is not recomputed_critical:
            errors.append("Model Judge overall criticalFailure does not match current rubric rules")
    return passed


def _validate_forbidden_skill_reads(
    case: Mapping[str, object],
    evidence: Mapping[str, object],
    evidence_path: Path,
    errors: list[str],
) -> None:
    forbidden = set(_string_items(case.get("forbiddenSkills")))
    if not forbidden:
        return
    observed: set[str] = set()
    for path in _event_ledger_paths(evidence, evidence_path):
        observed.update(
            str(event.get("skill"))
            for event in _read_json_lines(path)
            if event.get("type") in {"tool-call", "skill-read"} and isinstance(event.get("skill"), str)
        )
    for skill in sorted(forbidden & observed):
        errors.append(f"evidence observed forbidden skill read: {skill}")


def _events_for_reference(value: object, evidence_path: Path) -> list[dict[str, object]] | None:
    if not isinstance(value, str) or "#" not in value:
        return None
    file_name, marker = value.rsplit("#", 1)
    target = (evidence_path.parent / file_name).resolve()
    if not target.is_file():
        return None
    return [event for event in _read_json_lines(target) if str(event.get("id")) == marker]


def _all_events_for_reference(value: object, evidence_path: Path) -> list[dict[str, object]]:
    if not isinstance(value, str) or "#" not in value:
        return []
    target = (evidence_path.parent / value.rsplit("#", 1)[0]).resolve()
    return _read_json_lines(target)


def _read_json_lines(path: Path) -> list[dict[str, object]]:
    if not path.is_file():
        return []
    events: list[dict[str, object]] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        return []
    for line in lines:
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            events.append(value)
    return events


def _event_ledger_paths(evidence: Mapping[str, object], evidence_path: Path) -> set[Path]:
    references: list[object] = []
    agent = evidence.get("agent")
    if isinstance(agent, Mapping):
        references.append(agent.get("invocationEvidence"))
    run = evidence.get("run")
    if isinstance(run, Mapping):
        references.extend([run.get("invocationEvidence"), run.get("eventLedger")])
    skills = evidence.get("skills")
    if isinstance(skills, list):
        for skill in skills:
            if not isinstance(skill, Mapping) or not isinstance(skill.get("readEvidence"), list):
                continue
            for item in skill["readEvidence"]:
                if isinstance(item, Mapping):
                    references.append(item.get("reference"))
    paths: set[Path] = set()
    evidence_root = evidence_path.parent.resolve()
    for reference in references:
        if not isinstance(reference, str) or "#" not in reference:
            continue
        path = (evidence_path.parent / reference.rsplit("#", 1)[0]).resolve()
        if path == evidence_root or evidence_root in path.parents:
            paths.add(path)
    return paths


def _agent_source(agent_id: str) -> Path | None:
    direct = list((ROOT / "agents" / "roles").glob(f"**/{agent_id}.yaml"))
    if len(direct) == 1:
        return direct[0]
    for path in (ROOT / "agents" / "roles").glob("**/*.yaml"):
        try:
            value = yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError:
            continue
        if isinstance(value, Mapping) and value.get("name") == agent_id:
            return path
    return None


def _validate_catalog_items(
    filename: str,
    item_key: str,
    items: list[object],
    cases: Mapping[str, Mapping[str, object]],
    errors: list[str],
) -> None:
    seen: set[str] = set()
    for index, item in enumerate(items):
        if not isinstance(item, Mapping):
            errors.append(f"{filename}.{item_key}[{index}] must be a mapping")
            continue
        item_id = item.get("id")
        if not isinstance(item_id, str) or not item_id:
            errors.append(f"{filename}.{item_key}[{index}] must define id")
            continue
        if item_id in seen:
            errors.append(f"{filename} duplicate id: {item_id}")
        seen.add(item_id)
        for case_id in _collect_executable_cases(item):
            if case_id not in cases:
                errors.append(f"{filename}:{item_id} references missing executable case: {case_id}")
        if filename == "skill-probes.yaml":
            for field in (
                "skill",
                "source",
                "evaluationCategory",
                "evaluationKind",
                "activationCondition",
                "negativeCondition",
                "expectedBehavior",
                "judgePlan",
                "scenarioAssociations",
                "workflowAssociations",
                "executableCases",
                "coverageStatus",
                "ablation",
            ):
                if field not in item:
                    errors.append(f"{filename}:{item_id} missing {field}")
        if filename == "agent-scenarios.yaml":
            for field in (
                "source",
                "scenarioFamily",
                "repositoryMutation",
                "harnesses",
                "outputContractFields",
                "judgePlan",
                "workflowAssociations",
                "scenarios",
            ):
                if field not in item:
                    errors.append(f"{filename}:{item_id} missing {field}")
            harnesses = item.get("harnesses")
            if isinstance(harnesses, list):
                unsupported = sorted(set(_string_items(harnesses)) - SUPPORTED_HARNESSES)
                if unsupported:
                    errors.append(f"{filename}:{item_id} has unsupported harnesses: {', '.join(unsupported)}")


def _validate_catalog_harnesses(filename: str, data: Mapping[str, object], errors: list[str]) -> None:
    for field in ("harnesses", "harnessPolicy"):
        value = data.get(field)
        if isinstance(value, list):
            unsupported = sorted(set(_string_items(value)) - SUPPORTED_HARNESSES)
            if unsupported:
                errors.append(f"{filename}.{field} has unsupported harnesses: {', '.join(unsupported)}")
        elif isinstance(value, Mapping):
            declared = value.get("supported", value.get("allowed", []))
            if isinstance(declared, list):
                unsupported = sorted(set(_string_items(declared)) - SUPPORTED_HARNESSES)
                if unsupported:
                    errors.append(f"{filename}.{field} has unsupported harnesses: {', '.join(unsupported)}")


def _validate_catalog_cross_references(
    catalogs: Mapping[str, Mapping[str, object]],
    cases: Mapping[str, Mapping[str, object]],
    evals_root: Path,
    errors: list[str],
) -> None:
    probes = _items_by_id(catalogs.get("skill-probes.yaml", {}).get("probes"))
    agents = _items_by_id(catalogs.get("agent-scenarios.yaml", {}).get("agents"))
    packs = _items_by_id(catalogs.get("workflow-packs.yaml", {}).get("packs"))
    checks = _items_by_id(catalogs.get("judges.yaml", {}).get("checks"))
    rubrics = _items_by_id(catalogs.get("judges.yaml", {}).get("rubrics"))
    profiles = _items_by_id(catalogs.get("sandbox-profiles.yaml", {}).get("profiles"))
    scenario_ids = {
        str(scenario["id"])
        for agent in agents.values()
        for scenario in agent.get("scenarios", [])
        if isinstance(scenario, Mapping) and isinstance(scenario.get("id"), str)
    }

    for probe_id, probe in probes.items():
        skill = probe.get("skill")
        source = probe.get("source")
        expected = f"skills/{skill}/SKILL.md" if isinstance(skill, str) else None
        if source != expected:
            errors.append(f"skill-probes.yaml:{probe_id} source must be {expected}")
        elif not (ROOT / str(source)).is_file():
            errors.append(f"skill-probes.yaml:{probe_id} source is missing: {source}")
        _validate_coverage_link(probe_id, probe, "skill-probes.yaml", errors)
        wrong_skill = probe.get("wrongSkillControl")
        if wrong_skill is None and isinstance(probe.get("ablation"), Mapping):
            wrong_skill = probe["ablation"].get("wrongSkillControl")
        if not isinstance(wrong_skill, str):
            errors.append(f"skill-probes.yaml:{probe_id} missing wrongSkillControl")
        elif wrong_skill == skill:
            errors.append(f"skill-probes.yaml:{probe_id} wrongSkillControl must differ from the target skill")
        elif not (ROOT / "skills" / wrong_skill / "SKILL.md").is_file():
            errors.append(f"skill-probes.yaml:{probe_id} wrongSkillControl is not a bundled skill: {wrong_skill}")
        vocabulary = catalogs.get("skill-probes.yaml", {}).get("evaluationCategoryVocabulary")
        declared_categories = _vocabulary_values(vocabulary)
        if declared_categories and probe.get("evaluationCategory") not in declared_categories:
            errors.append(f"skill-probes.yaml:{probe_id} uses an undeclared evaluationCategory")
        _validate_judge_plan_references(probe_id, probe.get("judgePlan"), checks, rubrics, errors)
        for pack_id in _string_items(probe.get("workflowAssociations")):
            if pack_id not in packs:
                errors.append(f"skill-probes.yaml:{probe_id} references missing workflow pack: {pack_id}")
        for scenario_id in _string_items(probe.get("scenarioAssociations")):
            if scenario_id not in scenario_ids and scenario_id not in agents:
                errors.append(f"skill-probes.yaml:{probe_id} references missing agent scenario: {scenario_id}")

    for agent_id, agent in agents.items():
        source = agent.get("source")
        source_path = ROOT / str(source) if isinstance(source, str) else None
        if source_path is None or not source_path.is_file():
            errors.append(f"agent-scenarios.yaml:{agent_id} source is missing: {source}")
        else:
            try:
                source_value = yaml.safe_load(source_path.read_text(encoding="utf-8"))
            except yaml.YAMLError:
                source_value = None
            if not isinstance(source_value, Mapping) or source_value.get("name") != agent_id:
                errors.append(f"agent-scenarios.yaml:{agent_id} source name does not match id")
        _validate_judge_plan_references(agent_id, agent.get("judgePlan"), checks, rubrics, errors)
        for pack_id in _string_items(agent.get("workflowAssociations")):
            if pack_id not in packs:
                errors.append(f"agent-scenarios.yaml:{agent_id} references missing workflow pack: {pack_id}")
        scenarios = agent.get("scenarios")
        if isinstance(scenarios, list):
            for scenario in scenarios:
                if not isinstance(scenario, Mapping):
                    continue
                scenario_id = str(scenario.get("id", "unknown"))
                _validate_coverage_link(scenario_id, scenario, "agent-scenarios.yaml", errors)
                _validate_judge_plan_references(
                    scenario_id, scenario.get("judgePlan"), checks, rubrics, errors,
                )

    for pack_id, pack in packs.items():
        _validate_coverage_link(pack_id, pack, "workflow-packs.yaml", errors)
        for agent_id in _reference_values(pack, {"agent", "agents", "agentId", "agentIds", "requiredAgents"}):
            if agent_id not in agents:
                errors.append(f"workflow-packs.yaml:{pack_id} references missing agent: {agent_id}")
        for probe_id in _reference_values(pack, {"probe", "probes", "skillProbe", "skillProbes"}):
            if probe_id not in probes:
                errors.append(f"workflow-packs.yaml:{pack_id} references missing skill probe: {probe_id}")
        _validate_judge_plan_references(pack_id, pack.get("judgePlan"), checks, rubrics, errors)

    for case_id, case in cases.items():
        for field, known in (
            ("skillProbes", probes),
            ("agentScenarios", {scenario_id: {} for scenario_id in scenario_ids}),
        ):
            for reference in _string_items(case.get(field)):
                if reference not in known:
                    errors.append(f"cases.yaml:{case_id} {field} references missing id: {reference}")
        workflow_pack = case.get("workflowPack")
        if workflow_pack is not None and workflow_pack not in packs:
            errors.append(f"cases.yaml:{case_id} workflowPack references missing id: {workflow_pack}")
        sandbox_profiles = case.get("sandboxProfiles")
        if sandbox_profiles is not None and not isinstance(sandbox_profiles, Mapping):
            errors.append(f"cases.yaml:{case_id} sandboxProfiles must map harnesses to profile ids")
        elif isinstance(sandbox_profiles, Mapping):
            for harness, profile_id in sandbox_profiles.items():
                profile = profiles.get(str(profile_id))
                if harness not in SUPPORTED_HARNESSES:
                    errors.append(f"cases.yaml:{case_id} sandboxProfiles uses unsupported harness: {harness}")
                elif profile is None:
                    errors.append(f"cases.yaml:{case_id} references missing sandbox profile: {profile_id}")
                elif profile.get("harness") != harness:
                    errors.append(
                        f"cases.yaml:{case_id} sandbox profile {profile_id} does not belong to harness {harness}"
                    )
        fixture_claims = set(_string_items(case.get("fixtureBackedProbeClaims")))
        declared_probes = set(_string_items(case.get("skillProbes")))
        for probe_id in sorted(fixture_claims - declared_probes):
            errors.append(f"cases.yaml:{case_id} fixtureBackedProbeClaims is not listed in skillProbes: {probe_id}")
        for probe_id in sorted(fixture_claims & set(probes)):
            if case_id not in _collect_executable_cases(probes[probe_id]):
                errors.append(
                    f"cases.yaml:{case_id} fixture-backed probe claim lacks reciprocal executable case: {probe_id}"
                )
            ablation = probes[probe_id].get("ablation")
            wrong_skill = ablation.get("wrongSkillControl") if isinstance(ablation, Mapping) else None
            if wrong_skill in set(_string_items(case.get("requiredSkills"))):
                errors.append(
                    f"cases.yaml:{case_id} includes wrongSkillControl in the positive treatment: {wrong_skill}"
                )
        _validate_judge_plan_references(case_id, case.get("judgePlan"), checks, rubrics, errors)
        required_skills = set(_string_items(case.get("requiredSkills")))
        for agent_id in _string_items(case.get("requiredAgents")):
            agent = agents.get(agent_id)
            if agent is None:
                errors.append(f"cases.yaml:{case_id} references missing required agent: {agent_id}")
                continue
            for skill in sorted(_unconditional_agent_skills(agent)):
                if skill not in required_skills:
                    errors.append(
                        f"cases.yaml:{case_id} omits unconditional agent skill {skill} for {agent_id}"
                    )

    for profile_id, profile in profiles.items():
        harness = profile.get("harness")
        if harness not in SUPPORTED_HARNESSES:
            errors.append(f"sandbox-profiles.yaml:{profile_id} has unsupported harness: {harness}")


def _validate_judge_plan_references(
    owner_id: str,
    plan: object,
    checks: Mapping[str, Mapping[str, object]],
    rubrics: Mapping[str, Mapping[str, object]],
    errors: list[str],
) -> None:
    for check_id in _reference_values(plan, {"check", "checks", "checkId", "checkIds", "deterministicChecks"}):
        if check_id not in checks:
            errors.append(f"judge plan {owner_id} references missing Judge check: {check_id}")
    for rubric_id in _reference_values(
        plan,
        {"rubric", "rubrics", "rubricId", "rubricIds", "modelRubric", "modelRubrics"},
    ):
        if rubric_id not in rubrics:
            errors.append(f"judge plan {owner_id} references missing Judge rubric: {rubric_id}")


def _validate_coverage_link(owner_id: str, item: Mapping[str, object], filename: str, errors: list[str]) -> None:
    if item.get("coverageStatus") == "fixture-backed" and not _collect_executable_cases(item):
        errors.append(f"{filename}:{owner_id} is fixture-backed without an executable case")


def _items_by_id(value: object) -> dict[str, Mapping[str, object]]:
    if not isinstance(value, list):
        return {}
    return {
        str(item["id"]): item
        for item in value
        if isinstance(item, Mapping) and isinstance(item.get("id"), str)
    }


def _validate_unique_ids(label: str, value: object, errors: list[str]) -> None:
    if not isinstance(value, list):
        return
    identifiers = [
        str(item["id"])
        for item in value
        if isinstance(item, Mapping) and isinstance(item.get("id"), str)
    ]
    duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
    for identifier in duplicates:
        errors.append(f"{label} duplicate id: {identifier}")


def _vocabulary_values(value: object) -> set[str]:
    if isinstance(value, list):
        values = set(_string_items(value))
        values.update(
            str(item["id"])
            for item in value
            if isinstance(item, Mapping) and isinstance(item.get("id"), str)
        )
        return values
    if isinstance(value, Mapping):
        return {str(key) for key in value if isinstance(key, str)}
    return set()


def _reference_values(value: object, keys: set[str]) -> set[str]:
    found: set[str] = set()
    if isinstance(value, Mapping):
        for key, item in value.items():
            if key in keys:
                if isinstance(item, str):
                    found.add(item)
                else:
                    found.update(_string_items(item))
            else:
                found.update(_reference_values(item, keys))
    elif isinstance(value, list):
        for item in value:
            found.update(_reference_values(item, keys))
    return found


def _collect_executable_cases(value: object) -> set[str]:
    found: set[str] = set()
    if isinstance(value, Mapping):
        for key, item in value.items():
            if key == "executableCases" and isinstance(item, list):
                found.update(_string_items(item))
            else:
                found.update(_collect_executable_cases(item))
    elif isinstance(value, list):
        for item in value:
            found.update(_collect_executable_cases(item))
    return found


def _selected_skill_resource_paths(
    source_root: Path,
    skill_id: str,
    selected: Sequence[object],
) -> tuple[Path, ...]:
    skill_root = source_root.resolve() / "skills" / skill_id
    found: set[Path] = set()
    for value in selected:
        if not isinstance(value, str) or not value:
            raise ValueError(f"skill resource paths must be non-empty strings: {skill_id}")
        relative = Path(value)
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError(f"skill resource path escapes its package: {skill_id}/{value}")
        entry = (skill_root / relative).resolve()
        if entry != skill_root and skill_root not in entry.parents:
            raise ValueError(f"skill resource path escapes its package: {skill_id}/{value}")
        if entry.is_file():
            found.add(entry.relative_to(skill_root))
        elif entry.is_dir():
            for directory, directory_names, file_names in os.walk(entry, topdown=True, followlinks=False):
                directory_names[:] = [
                    name for name in sorted(directory_names)
                    if name not in TRANSIENT_TREE_NAMES
                ]
                current = Path(directory)
                for name in sorted(file_names):
                    path = current / name
                    if path.is_file() and not path.is_symlink():
                        found.add(path.relative_to(skill_root))
        else:
            raise ValueError(f"skill resource path is missing: {skill_id}/{value}")
    return tuple(sorted(found, key=lambda path: path.as_posix()))


def _resource_manifest_digest(resources: Sequence[Mapping[str, object]]) -> str:
    encoded = json.dumps(
        sorted(resources, key=lambda item: str(item.get("path"))),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _relative_path_is_allowed(path: str, roots: set[str]) -> bool:
    candidate = Path(path)
    return any(candidate == Path(root) or Path(root) in candidate.parents for root in roots)


def _unconditional_agent_skills(agent_catalog_entry: Mapping[str, object]) -> set[str]:
    source = agent_catalog_entry.get("source")
    if not isinstance(source, str):
        return set()
    path = ROOT / source
    if not path.is_file():
        return set()
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, yaml.YAMLError):
        return set()
    skills = value.get("skills") if isinstance(value, Mapping) else None
    result: set[str] = set()
    if not isinstance(skills, list):
        return result
    for item in skills:
        if not isinstance(item, Mapping) or len(item) != 1:
            continue
        skill_id, configuration = next(iter(item.items()))
        if isinstance(skill_id, str) and (
            not isinstance(configuration, Mapping) or not configuration.get("condition")
        ):
            result.add(skill_id)
    return result


def _containment_levels() -> set[str]:
    defaults = {"externally-contained", "workspace-isolated-only", "containment-unverified"}
    path = ROOT / "evals" / "sandbox-profiles.yaml"
    if not path.is_file():
        return defaults
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError:
        return defaults
    if not isinstance(data, Mapping):
        return defaults
    vocabulary = data.get("containmentStatusVocabulary")
    if isinstance(vocabulary, list):
        declared = set(_string_items(vocabulary))
        return declared or defaults
    if isinstance(vocabulary, Mapping):
        declared = {key for key in vocabulary if isinstance(key, str) and key in defaults}
        if not declared:
            declared = {
                value for value in vocabulary.values()
                if isinstance(value, str) and value in defaults
            }
        return declared or defaults
    return defaults


def _require_non_empty_string(value: object, field: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"evidence missing non-empty {field}")


def _require_digest(value: object, field: str, errors: list[str]) -> None:
    if not isinstance(value, str) or len(value) != 64 or any(character not in "0123456789abcdef" for character in value):
        errors.append(f"evidence {field} must be a lowercase SHA-256 digest")


def _validate_string_list(value: object, field: str, errors: list[str], *, required: bool = False) -> None:
    if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
        errors.append(f"{field} must be a list of non-empty strings")
    elif required and not value:
        errors.append(f"{field} must not be empty")
    elif len(value) != len(set(value)):
        errors.append(f"{field} must not contain duplicates")


def _string_items(value: object) -> list[str]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        return []
    return [item for item in value if isinstance(item, str)]
