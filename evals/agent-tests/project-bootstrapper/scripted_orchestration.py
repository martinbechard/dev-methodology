#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Runs the Bootstrapper primary-configuration handoff and configured multi-contribution contract with scripted agents.
# Governing test plan: evals/agent-tests/project-bootstrapper/test_scripted_orchestration.py

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from collections.abc import Collection, Mapping, Sequence
from pathlib import Path
from typing import Any

import yaml


_SUITE_ROOT = Path(__file__).resolve().parent
_REPOSITORY_ROOT = _SUITE_ROOT.parents[2]
_PROJECT_VALIDATOR = Path("scripts/render-agents-technology-skills.py")
_FIXTURE_NAME = "missing-configuration-multi-contribution"
_EXCLUDED_GENERATED_PROJECTIONS = (
    "generated/adapters/codex/agents/project-bootstrapper.toml",
    "generated/adapters/codex/agents/wiki-ingester.toml",
)
_REQUIRED_FRESH_MAIN_COMMANDS = (
    "python3 scripts/build-skill-docs.py",
    "python3 scripts/build-skill-docs.py --check",
    "python3.11 evals/agent-tests/project-bootstrapper/scripted_orchestration.py",
)
_TERMINAL_OUTCOMES = frozenset({"PASS", "FAIL", "BLOCKED", "NEEDS_CORRECTION"})
_CLEANUP_TIMEOUT_SECONDS = 10.0
_DEFAULT_JOB_WRAPPER_TIMEOUT_SECONDS = 190.0
_WINDOWS_JOB_WRAPPER = "--windows-job-wrapper"
JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE = 0x00002000
_CONTRIBUTIONS = (
    ("dev-documentation-writer", "docs/coverage-manifest.yaml"),
    ("dev-documentation-writer", "docs/module-catalog.md"),
    ("dev-documentation-writer", "docs/module-orders.md"),
    ("wiki-architect", "docs/wiki/README.md"),
    ("wiki-writer", "docs/wiki/topic-index.md"),
)
_SETUP_OUTPUTS = ("PROJECT.yaml", "AGENTS.md")
_REVERSE_ENGINEERING_MISSING_DOCUMENT = "docs/module-catalog-design.md"
_STALE_MARKERS = ("absent", "excluded", "contribution-phase", "future work")
_REVIEWERS = {
    "PROJECT.yaml": "dev-artifact-reviewer",
    "AGENTS.md": "dev-artifact-reviewer",
    "docs/coverage-manifest.yaml": "dev-artifact-reviewer",
    "docs/module-catalog.md": "dev-artifact-reviewer",
    "docs/module-orders.md": "dev-artifact-reviewer",
    _REVERSE_ENGINEERING_MISSING_DOCUMENT: "dev-artifact-reviewer",
    "docs/wiki/README.md": "wiki-artifact-reviewer",
    "docs/wiki/topic-index.md": "wiki-topic-verifier",
}
_PRODUCERS = {
    "PROJECT.yaml": "project-configurator",
    "AGENTS.md": "project-configurator",
    **{artifact: producer for producer, artifact in _CONTRIBUTIONS},
}
_TARGET_DIGESTS = {
    "skills/set-solo-mode/SKILL.md": (
        "57d1301e1d7f9a3feb0b842601438908464bff96e55d9f30d7bacf3d386a4cce"
    ),
    "skills/set-multitask-mode/SKILL.md": (
        "58db246cf60121136d7d363de6ea7b38d87c4c8f5c1093b945f69f1b4aec477b"
    ),
    "skills/resource-claim/SKILL.md": (
        "aee32e758a5c6110134be95bb26432faf319662527f7bd9d7c8dbefcdb54fb00"
    ),
    "agents/roles/project-setup/project-bootstrapper.role.yaml": (
        "167db9c594c8a1656df6112a3070f677a3a434ac691cb6ff0107d80385817ca0"
    ),
    "agents/roles/wiki-activities/wiki-ingester.role.yaml": (
        "304995274047372efbabeb19a244290b9509628f863607aa4b06a7bcbeda7d34"
    ),
}


def _evaluate_project_configuration_output(
    output: Mapping[str, Any],
    confirmed_skills: Collection[str],
) -> str:
    """Accept only explicit folder rows with exact-name technology skills."""
    catalog = tuple(confirmed_skills)
    if (
        not catalog
        or any(
            not isinstance(skill, str) or not skill or skill != skill.strip()
            for skill in catalog
        )
        or len(set(catalog)) != len(catalog)
    ):
        return "FAIL"
    allowed_skills = set(catalog)
    if set(output) != {"folder_routing"}:
        return "FAIL"
    routes = output["folder_routing"]
    if not isinstance(routes, list) or not routes:
        return "FAIL"
    for route in routes:
        if not isinstance(route, Mapping):
            return "FAIL"
        if set(route) != {"pattern", "required_skills"}:
            return "FAIL"
        if not isinstance(route["pattern"], str) or not route["pattern"]:
            return "FAIL"
        skills = route["required_skills"]
        if (
            not isinstance(skills, list)
            or not skills
            or any(
                not isinstance(skill, str)
                or not skill
                or skill != skill.strip()
                or skill not in allowed_skills
                for skill in skills
            )
            or len(set(skills)) != len(skills)
        ):
            return "FAIL"
    return "PASS"


def _load_project_validator(repository_root: Path):
    """Load the repository renderer that owns PROJECT.yaml validation."""

    validator_path = repository_root / _PROJECT_VALIDATOR
    specification = importlib.util.spec_from_file_location(
        f"project_bootstrapper_configuration_validator_{id(repository_root)}",
        validator_path,
    )
    if specification is None or specification.loader is None:
        raise RuntimeError(f"Unable to load project validator: {validator_path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


def _configuration_case(case: str, repository_root: Path) -> dict[str, Any]:
    """Build one canonical or supported legacy case from the repository configuration."""

    project = yaml.safe_load((repository_root / "PROJECT.yaml").read_text(encoding="utf-8"))
    if not isinstance(project, dict):
        raise ValueError("repository PROJECT.yaml must contain a mapping")
    project = copy.deepcopy(project)
    if case == "legacy":
        project.pop("project_setup", None)
        selection_policy = project["workflow_selection"].get("selection_policy")
        project["workflow_selection"] = {
            "backlog": {
                "default": "file-based-backlog",
                "folder_overrides": [],
            },
            "workitem": {
                "default": "simple-workitem",
                "folder_overrides": [],
            },
            "selection_policy": selection_policy,
        }
        return project
    if case not in {"canonical-solo", "canonical-multitask"}:
        raise ValueError(f"unknown configuration case: {case}")
    concurrent_tasking = case == "canonical-multitask"
    candidates: list[dict[str, Any]] = []
    accepted_skills: list[str] = []
    for loadout in project["technology_skill_loadouts"]:
        evidence_by_skill = {
            item["skill"]: item["evidence"]
            for item in loadout.get("sourceEvidence", [])
        }
        for skill in loadout["skills"]:
            candidates.append(
                {
                    "scope": loadout["pathPattern"],
                    "skill": skill,
                    "evidence": evidence_by_skill[skill],
                    "conflicts": [],
                    "disposition": "accepted",
                }
            )
            accepted_skills.append(skill)
    project["technology_confirmation"] = {
        "candidates": candidates,
        "accepted_skills": accepted_skills,
        "rejections": [],
        "confirmation": {
            "status": "confirmed",
            "evidence": "scripted primary Project Configurator confirmation",
        },
    }
    project["project_setup"] = {
        "mode": "advanced",
        "concurrent_tasking": concurrent_tasking,
        **({"concurrent_capacity": 3} if concurrent_tasking else {}),
        "persistence": "file",
        "commit": "main-branch",
        "documentation": "wiki",
        "core_skill_delivery": {
            "mode": "by-reference",
            "source": "installed-agent-metadata",
        },
        "technology_skill_delivery": "by-reference",
        "technology_confirmation_required": True,
    }
    if not concurrent_tasking:
        project["resource_coordination"] = {"selected": "none"}
        project.pop("agent_claim_transport", None)
    return project


def _validated_project_configuration(
    project: Mapping[str, Any],
    repository_root: Path,
) -> tuple[str, dict[str, Any]]:
    """Validate one complete project mapping and derive its independent selectors."""

    validator = _load_project_validator(repository_root)
    project_copy = copy.deepcopy(dict(project))
    rendered = validator.render(project_copy)
    workflow, _ = validator._canonical_workflow_selection(project_copy["workflow_selection"])
    persistence, _ = validator._workflow_configuration(
        workflow,
        "persistence",
        validator.PROVIDER_VALUES,
    )
    commit, _ = validator._workflow_configuration(
        workflow,
        "commit",
        validator.COMPLETION_VALUES,
    )
    setup = project_copy.get("project_setup")
    legacy = setup is None
    concurrent_tasking = None if legacy else setup["concurrent_tasking"]
    coordination = project_copy["resource_coordination"]["selected"]
    claim_stack_enabled = coordination == "resource-claim"
    if legacy:
        dispatch_selector = "PRESERVE_VALID_LEGACY_CONFIGURATION"
        secondary_dispatch_enabled = None
    elif concurrent_tasking:
        dispatch_selector = "ENABLED_BY_PROJECT_CONFIGURATION"
        secondary_dispatch_enabled = True
    else:
        dispatch_selector = "DISABLED_BY_PROJECT_CONFIGURATION"
        secondary_dispatch_enabled = False
    provider_skills = list(validator.PROVIDER_SKILLS.get(persistence, ()))
    commit_provider_skill = validator.COMPLETION_SKILLS.get(commit)
    coordination_provider_skills: list[str] = []
    if claim_stack_enabled:
        selected_helper = project_copy["agent_claim_transport"]["selected"]
        coordination_provider_skills.append(validator.CLAIM_HELPER_PROVIDERS[selected_helper])
    return rendered, {
        "validation": "PASS",
        "concurrentTasking": concurrent_tasking,
        "dispatchSelector": dispatch_selector,
        "secondaryDispatchEnabled": secondary_dispatch_enabled,
        "resourceCoordination": coordination,
        "claimStackEnabled": claim_stack_enabled,
        "legacyConfiguration": legacy,
        "persistence": persistence,
        "commit": commit,
        "persistenceProviderSkills": provider_skills,
        "commitProviderSkill": commit_provider_skill,
        "resourceCoordinationProviderSkills": coordination_provider_skills,
    }


def validated_configuration_case(case: str) -> dict[str, Any]:
    """Return selectors from one named configuration accepted by the repository validator.

    case selects canonical-solo, canonical-multitask, or legacy. The result contains the
    validated dispatch, coordination, Persistence, and Commit mappings. Unknown or invalid
    cases raise ValueError. This helper reads repository source and does not write project state.
    """

    project = _configuration_case(case, _REPOSITORY_ROOT)
    _, selectors = _validated_project_configuration(project, _REPOSITORY_ROOT)
    return selectors


class _ScriptedDependency:
    def __init__(self, plan: Mapping[str, Sequence[str]], trace: list[dict[str, Any]]) -> None:
        self._plan = {key: list(values) for key, values in plan.items()}
        self._trace = trace

    def call(
        self,
        agent: str,
        phase: str,
        artifact: str = "",
        *,
        default_outcome: str = "PASS",
        dispatch_context: str = "secondary",
    ) -> str:
        key = f"{phase}:{artifact}" if artifact else phase
        outcomes = self._plan.get(key, self._plan.get(agent, [default_outcome]))
        outcome = outcomes.pop(0) if outcomes else default_outcome
        self._trace.append(
            {
                "index": len(self._trace),
                "agent": agent,
                "phase": phase,
                "artifact": artifact,
                "outcome": outcome,
                "dispatchContext": dispatch_context,
            }
        )
        if outcome == "TIMEOUT":
            time.sleep(3600)
        if outcome not in _TERMINAL_OUTCOMES:
            raise ValueError(f"malformed handoff from {agent}: {outcome}")
        return outcome


class _AuditEvidenceUnavailable(RuntimeError):
    pass


def _unique_json_object(pairs: Sequence[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise _AuditEvidenceUnavailable(f"duplicate ledger key: {key}")
        result[key] = value
    return result


def _copy_inputs(workspace: Path) -> list[str]:
    copied: list[str] = []
    sources = (
        _SUITE_ROOT / "agents",
        _SUITE_ROOT / "skills" / "project-bootstrapper-suite-contract",
        _SUITE_ROOT / "fixtures" / _FIXTURE_NAME,
        _SUITE_ROOT / "scenarios.yaml",
        _SUITE_ROOT / "suite.yaml",
        _REPOSITORY_ROOT / "PROJECT.yaml",
        _REPOSITORY_ROOT / _PROJECT_VALIDATOR,
        _REPOSITORY_ROOT / "agents" / "roles" / "project-setup" / "project-bootstrapper.role.yaml",
        _REPOSITORY_ROOT / "agents" / "roles" / "wiki-activities" / "wiki-ingester.role.yaml",
        *(
            _REPOSITORY_ROOT / "skills" / skill
            for skill in (
                "set-solo-mode",
                "set-multitask-mode",
                "resource-claim",
                "resource-claim-helper-command",
                "bootstrap-project-documentation",
                "route-documentation-work",
                "organise-project-files",
                "structured-explanation",
                "document-provenance",
            )
        ),
    )
    for source in sources:
        relative = source.relative_to(_REPOSITORY_ROOT)
        destination = workspace / "snapshot" / relative
        if source.is_dir():
            shutil.copytree(source, destination)
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
        copied.append(relative.as_posix())
    fixture_copy = workspace / "candidate"
    shutil.copytree(_SUITE_ROOT / "fixtures" / _FIXTURE_NAME, fixture_copy)
    return copied


def _write_artifact(candidate: Path, artifact: str, *, contribution_phase: bool = False) -> None:
    target = candidate / artifact
    target.parent.mkdir(parents=True, exist_ok=True)
    if contribution_phase:
        marker = _STALE_MARKERS[sum(artifact.encode("utf-8")) % len(_STALE_MARKERS)]
        if target.suffix == ".yaml":
            target.write_text(
                "schema: scripted-bootstrap-evidence\n"
                f"documentationState: {marker}\n"
                "documentationOwner: contribution-agent\n",
                encoding="utf-8",
            )
        else:
            target.write_text(
                f"# Scripted {target.stem.replace('-', ' ').title()}\n\n"
                f"This integrated artifact is still described as {marker}.\n\n"
                "Owner: contribution-agent\n",
                encoding="utf-8",
            )
        return
    if target.suffix == ".yaml":
        target.write_text("schema: scripted-bootstrap-evidence\n", encoding="utf-8")
    else:
        target.write_text(f"# Scripted {target.stem.replace('-', ' ').title()}\n", encoding="utf-8")


def _write_steady_state_artifact(candidate: Path, artifact: str) -> None:
    target = candidate / artifact
    target.parent.mkdir(parents=True, exist_ok=True)
    contents = {
        "PROJECT.yaml": (
            "schema: scripted-bootstrap-evidence\n"
            "documentationState: complete\n"
            "documentationOwner: project-configurator\n"
        ),
        "AGENTS.md": (
            "# Project Guidance\n\n"
            "The complete documentation hierarchy is available.\n\n"
            "Owner: project-configurator\n"
        ),
        "docs/coverage-manifest.yaml": (
            "schema: scripted-coverage\n"
            "documentationOwner: dev-documentation-writer\n"
            "modules:\n"
            "  - source: src/orders.py\n"
            "    design: docs/module-orders.md\n"
            "  - source: src/catalog.py\n"
            "    design: docs/module-catalog-design.md\n"
        ),
        "docs/module-catalog.md": (
            "# Module Catalog\n\n"
            "- [Orders](module-orders.md)\n"
            "- [Catalog](module-catalog-design.md)\n"
            "\nOwner: dev-documentation-writer\n"
        ),
        "docs/module-orders.md": (
            "# Orders Module\n\n"
            "Source: ../src/orders.py\n\n"
            "Owner: dev-documentation-writer\n"
        ),
        _REVERSE_ENGINEERING_MISSING_DOCUMENT: (
            "# Catalog Module\n\n"
            "Source: ../src/catalog.py\n\n"
            "Owner: dev-documentation-writer\n"
        ),
        "docs/wiki/README.md": (
            "# Project Wiki\n\n"
            "- [Topic index](topic-index.md)\n\n"
            "Owner: wiki-architect\n"
        ),
        "docs/wiki/topic-index.md": (
            "# Topic Index\n\n"
            "- [Module catalog](../module-catalog.md)\n"
            "- [Orders module](../module-orders.md)\n"
            "- [Catalog module](../module-catalog-design.md)\n"
            "\nOwner: wiki-writer\n"
        ),
    }
    target.write_text(contents[artifact], encoding="utf-8")


def _ownership_values(text: str) -> list[str]:
    return [
        value.strip()
        for value in re.findall(
            r"^(?:documentationOwner|Owner):\s*(.+?)\s*$",
            text,
            flags=re.IGNORECASE | re.MULTILINE,
        )
    ]


def _audit_findings(candidate: Path, artifacts: Sequence[str]) -> list[dict[str, str]]:
    ledger_path = candidate / "path-coverage-ledger.json"
    if not ledger_path.is_file():
        raise _AuditEvidenceUnavailable("path-coverage-ledger.json is unavailable")
    try:
        ledger = json.loads(
            ledger_path.read_text(encoding="utf-8"),
            object_pairs_hook=_unique_json_object,
        )
        baseline_paths = ledger["sourceBaseline"]["paths"]
        tracked_classifications = ledger["trackedPathClassifications"]
        artifact_ownership = ledger["artifactOwnership"]
    except (KeyError, TypeError, json.JSONDecodeError) as error:
        raise _AuditEvidenceUnavailable("path-coverage-ledger.json is invalid") from error
    if not isinstance(baseline_paths, list) or not baseline_paths:
        raise _AuditEvidenceUnavailable("source baseline paths are unavailable")
    if not isinstance(tracked_classifications, dict) or not all(
        isinstance(path, str)
        and path
        and isinstance(classification, str)
        and classification
        for path, classification in tracked_classifications.items()
    ):
        raise _AuditEvidenceUnavailable("tracked path classifications are invalid")
    requirements = json.loads(
        (candidate / "bootstrap-requirements.json").read_text(encoding="utf-8")
    )
    output_paths = {
        path
        for group in ("configuration", "nonWikiDocumentation", "wikiDocumentation")
        for path in requirements[group]
    }
    output_paths.add(_REVERSE_ENGINEERING_MISSING_DOCUMENT)
    baseline_files = {
        path.relative_to(candidate).as_posix()
        for path in candidate.rglob("*")
        if path.is_file()
        and path.suffix != ".pyc"
        and "__pycache__" not in path.parts
        and path.relative_to(candidate).as_posix() not in output_paths
    }
    classified_paths = set(tracked_classifications)
    if classified_paths != baseline_files:
        missing = sorted(baseline_files - classified_paths)
        extra = sorted(classified_paths - baseline_files)
        raise _AuditEvidenceUnavailable(
            f"tracked path classifications do not match baseline: missing={missing}, extra={extra}"
        )
    expected_artifacts = output_paths
    if not isinstance(artifact_ownership, dict) or set(artifact_ownership) != expected_artifacts:
        raise _AuditEvidenceUnavailable("artifact ownership statements are incomplete")
    if not all(
        isinstance(owner, str) and owner
        for owner in artifact_ownership.values()
    ):
        raise _AuditEvidenceUnavailable("artifact ownership statements are invalid")

    findings_by_artifact: dict[str, dict[str, str]] = {}

    def add_finding(
        artifact: str,
        owner: str,
        reason: str,
        authoritative_evidence: str,
        required_work: str,
    ) -> None:
        existing = findings_by_artifact.get(artifact)
        if existing is None:
            findings_by_artifact[artifact] = {
                "artifact": artifact,
                "owner": owner,
                "reason": reason,
                "authoritativeEvidence": authoritative_evidence,
                "requiredWork": required_work,
            }
            return
        existing["reason"] = f'{existing["reason"]}; {reason}'
        existing["authoritativeEvidence"] = (
            f'{existing["authoritativeEvidence"]}; {authoritative_evidence}'
        )
        existing["requiredWork"] = f'{existing["requiredWork"]}; {required_work}'

    coverage_manifest = candidate / "docs/coverage-manifest.yaml"
    if not coverage_manifest.is_file():
        raise _AuditEvidenceUnavailable("coverage manifest is unavailable")

    for artifact in artifacts:
        artifact_path = candidate / artifact
        if not artifact_path.is_file():
            add_finding(
                artifact,
                artifact_ownership[artifact],
                "artifact is missing from the final integrated tree",
                f"path-coverage-ledger.json requires {artifact}",
                "recreate the assigned artifact from the current authoritative evidence",
            )
            continue
        text = artifact_path.read_text(encoding="utf-8").lower()
        markers = [marker for marker in _STALE_MARKERS if marker in text]
        if markers:
            add_finding(
                artifact,
                artifact_ownership[artifact],
                f"stale integrated-state marker: {markers[0]}",
                f"the final tree contains {artifact}",
                "replace contribution-phase wording with the final integrated state",
            )
        expected_owner = artifact_ownership[artifact]
        declared_owners = _ownership_values(
            (candidate / artifact).read_text(encoding="utf-8")
        )
        if declared_owners != [expected_owner]:
            add_finding(
                artifact,
                expected_owner,
                f"ownership statement {declared_owners} contradicts {expected_owner}",
                f"path-coverage-ledger.json assigns {artifact} to {expected_owner}",
                "replace the contribution owner with the final artifact owner",
            )

    module_catalog = candidate / "docs/module-catalog.md"
    topic_index = candidate / "docs/wiki/topic-index.md"
    coverage_text = coverage_manifest.read_text(encoding="utf-8")
    catalog_text = module_catalog.read_text(encoding="utf-8") if module_catalog.is_file() else ""
    topic_text = topic_index.read_text(encoding="utf-8") if topic_index.is_file() else ""
    baseline_source_paths: list[str] = []
    for entry in baseline_paths:
        if not isinstance(entry, dict):
            raise _AuditEvidenceUnavailable("source baseline entry is invalid")
        source = entry.get("path")
        expected_digest = entry.get("sha256")
        classification = entry.get("classification")
        document = entry.get("documentationOwner")
        if not all(
            isinstance(value, str) and value
            for value in (source, expected_digest, classification, document)
        ):
            raise _AuditEvidenceUnavailable("source baseline entry is incomplete")
        if tracked_classifications.get(source) != classification:
            raise _AuditEvidenceUnavailable(
                f"source baseline classification contradicts tracked ledger: {source}"
            )
        baseline_source_paths.append(source)
        source_path = candidate / source
        if not source_path.is_file():
            raise _AuditEvidenceUnavailable(f"source baseline path is unavailable: {source}")
        actual_digest = hashlib.sha256(source_path.read_bytes()).hexdigest()
        if actual_digest != expected_digest:
            raise _AuditEvidenceUnavailable(f"source baseline drifted: {source}")
        if not (candidate / document).is_file():
            add_finding(
                document,
                artifact_ownership[document],
                f"{source} has no module design",
                f"path-coverage-ledger.json maps {source} to {document}",
                "create the assigned module design from the current source baseline",
            )
        document_name = Path(document).name
        if document_name not in catalog_text:
            add_finding(
                "docs/module-catalog.md",
                artifact_ownership["docs/module-catalog.md"],
                f"module catalog does not link {document}",
                f"path-coverage-ledger.json requires {document}",
                "add the required module design link",
            )
        if document_name not in topic_text:
            add_finding(
                "docs/wiki/topic-index.md",
                artifact_ownership["docs/wiki/topic-index.md"],
                f"topic index does not link {document}",
                f"path-coverage-ledger.json requires navigation for {document}",
                "add the required final-tree navigation link",
            )

    if len(baseline_source_paths) != len(set(baseline_source_paths)):
        raise _AuditEvidenceUnavailable("source baseline contains duplicate paths")
    must_document_paths = {
        path
        for path, classification in tracked_classifications.items()
        if classification == "MUST_DOCUMENT"
    }
    if set(baseline_source_paths) != must_document_paths:
        missing = sorted(must_document_paths - set(baseline_source_paths))
        extra = sorted(set(baseline_source_paths) - must_document_paths)
        raise _AuditEvidenceUnavailable(
            f"MUST_DOCUMENT paths do not match hashed source baseline: missing={missing}, extra={extra}"
        )

    try:
        manifest = yaml.safe_load(coverage_text)
        manifest_rows = manifest.get("modules") if isinstance(manifest, dict) else None
    except yaml.YAMLError:
        manifest_rows = None
    actual_mappings: list[tuple[str, str]] = []
    manifest_is_structural = isinstance(manifest_rows, list)
    if manifest_is_structural:
        for row in manifest_rows:
            if not isinstance(row, dict) or set(row) != {"source", "design"}:
                manifest_is_structural = False
                break
            source = row["source"]
            design = row["design"]
            if not isinstance(source, str) or not isinstance(design, str):
                manifest_is_structural = False
                break
            actual_mappings.append((source, design))
    expected_mappings = [
        (entry["path"], entry["documentationOwner"])
        for entry in baseline_paths
    ]
    if not manifest_is_structural or sorted(actual_mappings) != sorted(expected_mappings):
        add_finding(
            "docs/coverage-manifest.yaml",
            artifact_ownership["docs/coverage-manifest.yaml"],
            "coverage manifest source-to-design mappings contradict the path ledger",
            f"path-coverage-ledger.json requires {sorted(expected_mappings)}",
            "replace the manifest rows with the exact source-to-design mappings",
        )

    for artifact in (
        "docs/module-catalog.md",
        "docs/wiki/README.md",
        "docs/wiki/topic-index.md",
    ):
        page = candidate / artifact
        if not page.is_file():
            continue
        for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", page.read_text(encoding="utf-8")):
            if not (page.parent / target).resolve().is_file():
                add_finding(
                    artifact,
                    artifact_ownership[artifact],
                    f"link does not resolve: {target}",
                    f"the final tree has no target for {artifact} -> {target}",
                    "replace the stale link with a path that resolves in the final tree",
                )
    return list(findings_by_artifact.values())


def _validate_snapshot_contract(workspace: Path) -> None:
    snapshot = workspace / "snapshot"
    for relative, expected in _TARGET_DIGESTS.items():
        actual = hashlib.sha256((snapshot / relative).read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError(f"Bootstrapper target contract drifted: {relative}")


def _terminal(status: str, trace: list[dict[str, Any]], **evidence: Any) -> dict[str, Any]:
    return {
        "schema": "project-bootstrapper-scripted-result",
        "version": 1,
        "status": status,
        "trace": trace,
        "claimCloseout": all(
            event["phase"] != "claim-acquire"
            or any(
                later["phase"] == "claim-release" and later["artifact"] == event["artifact"]
                for later in trace[event["index"] + 1 :]
            )
            for event in trace
        ),
        "generatedProjectionIntegration": {
            "candidateSnapshot": "authoritative-source-only",
            "excludedGeneratedProjections": list(_EXCLUDED_GENERATED_PROJECTIONS),
            "requiredFreshMainCommands": list(_REQUIRED_FRESH_MAIN_COMMANDS),
        },
        **evidence,
    }


def _start_owned_process(
    command: Sequence[str],
    *,
    timeout_seconds: float = _DEFAULT_JOB_WRAPPER_TIMEOUT_SECONDS,
) -> subprocess.Popen[bytes]:
    """Start one worker in a platform-owned process group without a shell."""
    process_options: dict[str, object] = {}
    process_argv = list(command)
    if os.name == "nt":
        process_options["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
        process_argv = [
            sys.executable,
            str(Path(__file__).resolve()),
            _WINDOWS_JOB_WRAPPER,
            str(timeout_seconds + _CLEANUP_TIMEOUT_SECONDS),
            *process_argv,
        ]
    else:
        process_options["start_new_session"] = True
    return subprocess.Popen(process_argv, **process_options)


def _terminate_owned_process_tree(process: subprocess.Popen[bytes]) -> None:
    """Terminate one owned worker tree and wait until its root descriptor is reaped."""
    if os.name == "nt":
        if process.poll() is None:
            try:
                process.kill()
            except OSError as error:
                if process.poll() is None:
                    raise RuntimeError("Unable to terminate the Windows Job Object owner") from error
    else:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    try:
        process.wait(timeout=_CLEANUP_TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired as error:
        raise RuntimeError("Owned process-tree root did not terminate") from error


def _run_windows_job_owned_command(command: Sequence[str], timeout_seconds: float) -> int:
    """Run one command assigned before resume to a kill-on-close Windows Job Object."""

    if os.name != "nt":
        raise RuntimeError("Windows Job Object wrapper invoked on a non-Windows host")
    if not command:
        raise ValueError("Windows Job Object wrapper requires a command")

    import ctypes
    from ctypes import wintypes

    class _JobObjectBasicLimitInformation(ctypes.Structure):
        _fields_ = (
            ("PerProcessUserTimeLimit", ctypes.c_int64),
            ("PerJobUserTimeLimit", ctypes.c_int64),
            ("LimitFlags", wintypes.DWORD),
            ("MinimumWorkingSetSize", ctypes.c_size_t),
            ("MaximumWorkingSetSize", ctypes.c_size_t),
            ("ActiveProcessLimit", wintypes.DWORD),
            ("Affinity", ctypes.c_size_t),
            ("PriorityClass", wintypes.DWORD),
            ("SchedulingClass", wintypes.DWORD),
        )

    class _IoCounters(ctypes.Structure):
        _fields_ = tuple((name, ctypes.c_uint64) for name in (
            "ReadOperationCount",
            "WriteOperationCount",
            "OtherOperationCount",
            "ReadTransferCount",
            "WriteTransferCount",
            "OtherTransferCount",
        ))

    class _JobObjectExtendedLimitInformation(ctypes.Structure):
        _fields_ = (
            ("BasicLimitInformation", _JobObjectBasicLimitInformation),
            ("IoInfo", _IoCounters),
            ("ProcessMemoryLimit", ctypes.c_size_t),
            ("JobMemoryLimit", ctypes.c_size_t),
            ("PeakProcessMemoryUsed", ctypes.c_size_t),
            ("PeakJobMemoryUsed", ctypes.c_size_t),
        )

    class _JobObjectBasicAccountingInformation(ctypes.Structure):
        _fields_ = (
            ("TotalUserTime", ctypes.c_int64),
            ("TotalKernelTime", ctypes.c_int64),
            ("ThisPeriodTotalUserTime", ctypes.c_int64),
            ("ThisPeriodTotalKernelTime", ctypes.c_int64),
            ("TotalPageFaultCount", wintypes.DWORD),
            ("TotalProcesses", wintypes.DWORD),
            ("ActiveProcesses", wintypes.DWORD),
            ("TotalTerminatedProcesses", wintypes.DWORD),
        )

    class _StartupInfo(ctypes.Structure):
        _fields_ = (
            ("cb", wintypes.DWORD),
            ("lpReserved", wintypes.LPWSTR),
            ("lpDesktop", wintypes.LPWSTR),
            ("lpTitle", wintypes.LPWSTR),
            ("dwX", wintypes.DWORD),
            ("dwY", wintypes.DWORD),
            ("dwXSize", wintypes.DWORD),
            ("dwYSize", wintypes.DWORD),
            ("dwXCountChars", wintypes.DWORD),
            ("dwYCountChars", wintypes.DWORD),
            ("dwFillAttribute", wintypes.DWORD),
            ("dwFlags", wintypes.DWORD),
            ("wShowWindow", wintypes.WORD),
            ("cbReserved2", wintypes.WORD),
            ("lpReserved2", ctypes.POINTER(wintypes.BYTE)),
            ("hStdInput", wintypes.HANDLE),
            ("hStdOutput", wintypes.HANDLE),
            ("hStdError", wintypes.HANDLE),
        )

    class _ProcessInformation(ctypes.Structure):
        _fields_ = (
            ("hProcess", wintypes.HANDLE),
            ("hThread", wintypes.HANDLE),
            ("dwProcessId", wintypes.DWORD),
            ("dwThreadId", wintypes.DWORD),
        )

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.CreateJobObjectW.argtypes = (ctypes.c_void_p, wintypes.LPCWSTR)
    kernel32.CreateJobObjectW.restype = wintypes.HANDLE
    kernel32.SetInformationJobObject.argtypes = (
        wintypes.HANDLE,
        ctypes.c_int,
        ctypes.c_void_p,
        wintypes.DWORD,
    )
    kernel32.SetInformationJobObject.restype = wintypes.BOOL
    kernel32.QueryInformationJobObject.argtypes = (
        wintypes.HANDLE,
        ctypes.c_int,
        ctypes.c_void_p,
        wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD),
    )
    kernel32.QueryInformationJobObject.restype = wintypes.BOOL
    kernel32.GetStdHandle.argtypes = (wintypes.DWORD,)
    kernel32.GetStdHandle.restype = wintypes.HANDLE
    kernel32.CreateProcessW.argtypes = (
        wintypes.LPCWSTR,
        wintypes.LPWSTR,
        ctypes.c_void_p,
        ctypes.c_void_p,
        wintypes.BOOL,
        wintypes.DWORD,
        ctypes.c_void_p,
        wintypes.LPCWSTR,
        ctypes.POINTER(_StartupInfo),
        ctypes.POINTER(_ProcessInformation),
    )
    kernel32.CreateProcessW.restype = wintypes.BOOL
    kernel32.AssignProcessToJobObject.argtypes = (wintypes.HANDLE, wintypes.HANDLE)
    kernel32.AssignProcessToJobObject.restype = wintypes.BOOL
    kernel32.ResumeThread.argtypes = (wintypes.HANDLE,)
    kernel32.ResumeThread.restype = wintypes.DWORD
    kernel32.WaitForSingleObject.argtypes = (wintypes.HANDLE, wintypes.DWORD)
    kernel32.WaitForSingleObject.restype = wintypes.DWORD
    kernel32.GetExitCodeProcess.argtypes = (wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD))
    kernel32.GetExitCodeProcess.restype = wintypes.BOOL
    kernel32.TerminateProcess.argtypes = (wintypes.HANDLE, wintypes.UINT)
    kernel32.TerminateProcess.restype = wintypes.BOOL
    kernel32.TerminateJobObject.argtypes = (wintypes.HANDLE, wintypes.UINT)
    kernel32.TerminateJobObject.restype = wintypes.BOOL
    kernel32.CloseHandle.argtypes = (wintypes.HANDLE,)
    kernel32.CloseHandle.restype = wintypes.BOOL

    wait_object_0 = 0
    wait_timeout = 258
    create_suspended = 0x00000004
    create_new_process_group = 0x00000200
    STARTF_USESTDHANDLES = 0x00000100
    std_input_handle = 0xFFFFFFF6
    std_output_handle = 0xFFFFFFF5
    std_error_handle = 0xFFFFFFF4
    invalid_handle_value = ctypes.c_void_p(-1).value
    job_object_basic_accounting_information = 1
    job_object_extended_limit_information = 9
    cleanup_timeout_ms = int(_CLEANUP_TIMEOUT_SECONDS * 1000)
    command_timeout_ms = min(0xFFFFFFFE, max(1, int(timeout_seconds * 1000)))

    def wait_for_empty_job() -> None:
        deadline = time.monotonic() + _CLEANUP_TIMEOUT_SECONDS
        while True:
            accounting = _JobObjectBasicAccountingInformation()
            returned_length = wintypes.DWORD()
            if not kernel32.QueryInformationJobObject(
                job,
                job_object_basic_accounting_information,
                ctypes.byref(accounting),
                ctypes.sizeof(accounting),
                ctypes.byref(returned_length),
            ):
                raise ctypes.WinError(ctypes.get_last_error())
            if accounting.ActiveProcesses == 0:
                return
            if time.monotonic() >= deadline:
                raise RuntimeError("Windows command job did not become empty")
            time.sleep(0.01)

    job = kernel32.CreateJobObjectW(None, None)
    if not job:
        raise ctypes.WinError(ctypes.get_last_error())
    process_information = _ProcessInformation()
    try:
        limits = _JobObjectExtendedLimitInformation()
        limits.BasicLimitInformation.LimitFlags = JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        if not kernel32.SetInformationJobObject(
            job,
            job_object_extended_limit_information,
            ctypes.byref(limits),
            ctypes.sizeof(limits),
        ):
            raise ctypes.WinError(ctypes.get_last_error())

        startup = _StartupInfo()
        startup.cb = ctypes.sizeof(startup)
        startup.dwFlags = STARTF_USESTDHANDLES
        startup.hStdInput = kernel32.GetStdHandle(std_input_handle)
        startup.hStdOutput = kernel32.GetStdHandle(std_output_handle)
        startup.hStdError = kernel32.GetStdHandle(std_error_handle)
        if any(
            handle in (None, invalid_handle_value)
            for handle in (startup.hStdInput, startup.hStdOutput, startup.hStdError)
        ):
            raise ctypes.WinError(ctypes.get_last_error())
        command_line = ctypes.create_unicode_buffer(subprocess.list2cmdline(list(command)))
        if not kernel32.CreateProcessW(
            None,
            command_line,
            None,
            None,
            True,
            create_suspended | create_new_process_group,
            None,
            None,
            ctypes.byref(startup),
            ctypes.byref(process_information),
        ):
            raise ctypes.WinError(ctypes.get_last_error())
        try:
            if not kernel32.AssignProcessToJobObject(job, process_information.hProcess):
                error_code = ctypes.get_last_error()
                if not kernel32.TerminateProcess(process_information.hProcess, 126):
                    raise ctypes.WinError(ctypes.get_last_error())
                if kernel32.WaitForSingleObject(
                    process_information.hProcess,
                    cleanup_timeout_ms,
                ) != wait_object_0:
                    raise RuntimeError("Unassigned suspended Windows command did not terminate")
                raise ctypes.WinError(error_code)
            if kernel32.ResumeThread(process_information.hThread) == 0xFFFFFFFF:
                error_code = ctypes.get_last_error()
                if not kernel32.TerminateJobObject(job, 126):
                    raise ctypes.WinError(ctypes.get_last_error())
                wait_for_empty_job()
                raise ctypes.WinError(error_code)

            wait_result = kernel32.WaitForSingleObject(
                process_information.hProcess,
                command_timeout_ms,
            )
            if wait_result == wait_timeout:
                if not kernel32.TerminateJobObject(job, 124):
                    raise ctypes.WinError(ctypes.get_last_error())
                wait_for_empty_job()
                return 124
            if wait_result != wait_object_0:
                raise ctypes.WinError(ctypes.get_last_error())

            exit_code = wintypes.DWORD()
            if not kernel32.GetExitCodeProcess(
                process_information.hProcess,
                ctypes.byref(exit_code),
            ):
                raise ctypes.WinError(ctypes.get_last_error())
            if not kernel32.TerminateJobObject(job, 1):
                raise ctypes.WinError(ctypes.get_last_error())
            wait_for_empty_job()
            return int(exit_code.value)
        finally:
            close_error = 0
            if process_information.hThread:
                if not kernel32.CloseHandle(process_information.hThread):
                    close_error = ctypes.get_last_error()
            if process_information.hProcess:
                if not kernel32.CloseHandle(process_information.hProcess) and not close_error:
                    close_error = ctypes.get_last_error()
            if close_error:
                raise ctypes.WinError(close_error)
    finally:
        if not kernel32.CloseHandle(job):
            raise ctypes.WinError(ctypes.get_last_error())


def _windows_job_wrapper_main(arguments: Sequence[str]) -> int:
    """Validate private wrapper arguments and surface ownership failures to the parent."""

    if len(arguments) < 2:
        print("Windows Job Object wrapper requires a timeout and command", file=sys.stderr)
        return 126
    try:
        timeout_seconds = float(arguments[0])
        if timeout_seconds <= 0:
            raise ValueError("timeout must be positive")
        return _run_windows_job_owned_command(arguments[1:], timeout_seconds)
    except Exception as error:
        print(f"Windows Job Object ownership failed: {error}", file=sys.stderr)
        return 126


def _run_missing_configuration_worker(workspace: Path) -> dict[str, Any]:
    """Return the terminal first Bootstrapper execution for an absent root configuration."""

    copied = _copy_inputs(workspace)
    _validate_snapshot_contract(workspace)
    candidate = workspace / "candidate"
    if (candidate / "PROJECT.yaml").exists():
        raise ValueError("missing-configuration fixture unexpectedly contains PROJECT.yaml")
    trace = [
        {
            "index": 0,
            "agent": "project-bootstrapper",
            "phase": "require-primary-project-configurator",
            "artifact": "PROJECT.yaml",
            "outcome": "PRIMARY_PROJECT_CONFIGURATOR_HANDOFF_REQUIRED",
            "dispatchContext": "primary",
            "coordinationMode": "SOLO",
        }
    ]
    claim_state_untouched = not (candidate / ".codex" / "agent-claim").exists()
    return _terminal(
        "BLOCKED",
        trace,
        executionId="initial-project-bootstrapper",
        reason="PRIMARY_PROJECT_CONFIGURATOR_HANDOFF_REQUIRED",
        copiedInputs=copied,
        targetContractBound=True,
        preconfigurationClaimStateUntouched=claim_state_untouched,
        effectiveCoordinationMode="SOLO",
    )


def _run_configuration_worker(
    plan: Mapping[str, Sequence[str]],
    workspace: Path,
    configuration_case: str,
) -> dict[str, Any]:
    """Run the independent primary Configurator execution and repository validation gate."""

    trace: list[dict[str, Any]] = []
    dependencies = _ScriptedDependency(plan, trace)
    copied = _copy_inputs(workspace)
    _validate_snapshot_contract(workspace)
    for procedure, artifact in (
        ("Configure Project Agents And Skills", "PROJECT.yaml"),
        ("Render Project Guidance", "AGENTS.md"),
        ("Verify Project Configuration", "PROJECT.yaml and AGENTS.md"),
    ):
        outcome = dependencies.call(
            "project-configurator",
            procedure,
            artifact,
            dispatch_context="primary",
        )
        if outcome != "PASS":
            return _terminal(
                outcome,
                trace,
                executionId="primary-project-configurator",
                copiedInputs=copied,
                targetContractBound=True,
            )
    snapshot_root = workspace / "snapshot"
    project = _configuration_case(configuration_case, snapshot_root)
    rendered, selectors = _validated_project_configuration(project, snapshot_root)
    return _terminal(
        "PASS",
        trace,
        executionId="primary-project-configurator",
        copiedInputs=copied,
        targetContractBound=True,
        validationGate="repository-render-validator",
        projectConfiguration=project,
        renderedGuidance=rendered,
        selectors=selectors,
    )


def _run_worker(
    plan: Mapping[str, Sequence[str]],
    workspace: Path,
    project_configuration: Mapping[str, Any],
    *,
    reverse_engineering: bool = False,
    legacy_runtime_dispatch: bool | None = None,
) -> dict[str, Any]:
    trace: list[dict[str, Any]] = []
    dependencies = _ScriptedDependency(plan, trace)
    copied = _copy_inputs(workspace)
    _validate_snapshot_contract(workspace)
    candidate = workspace / "candidate"
    project_path = candidate / "PROJECT.yaml"
    project_path.write_text(
        yaml.safe_dump(dict(project_configuration), sort_keys=False),
        encoding="utf-8",
    )
    persisted_project = yaml.safe_load(project_path.read_text(encoding="utf-8"))
    if not isinstance(persisted_project, dict):
        raise ValueError("resumed repository-root PROJECT.yaml must contain a mapping")
    rendered_guidance, selectors = _validated_project_configuration(
        persisted_project,
        workspace / "snapshot",
    )
    (candidate / "AGENTS.md").write_text(rendered_guidance, encoding="utf-8")
    if reverse_engineering:
        for artifact in _SETUP_OUTPUTS:
            _write_artifact(candidate, artifact, contribution_phase=True)
    secondary_dispatch_enabled = selectors["secondaryDispatchEnabled"]
    if secondary_dispatch_enabled is None:
        if not isinstance(legacy_runtime_dispatch, bool):
            raise ValueError(
                "legacy configuration requires an explicit existing runtime dispatch setting"
            )
        effective_secondary_dispatch = legacy_runtime_dispatch
        legacy_runtime_dispatch_before = legacy_runtime_dispatch
        legacy_runtime_dispatch_after = legacy_runtime_dispatch
    else:
        if legacy_runtime_dispatch is not None:
            raise ValueError(
                "legacy runtime dispatch setting is allowed only for legacy configuration"
            )
        effective_secondary_dispatch = secondary_dispatch_enabled
        legacy_runtime_dispatch_before = None
        legacy_runtime_dispatch_after = None
    claim_stack_enabled = selectors["claimStackEnabled"]
    trace.append(
        {
            "index": len(trace),
            "agent": "project-bootstrapper",
            "phase": "resume-after-valid-configuration",
            "artifact": "PROJECT.yaml",
            "outcome": "PASS",
            "dispatchContext": "primary",
            "coordinationMode": "CONFIGURED",
            "dispatchSelector": selectors["dispatchSelector"],
            "resourceCoordination": selectors["resourceCoordination"],
        }
    )
    if reverse_engineering and "path-coverage-ledger.json" in plan.get(
        "omitAuditEvidence",
        (),
    ):
        (candidate / "path-coverage-ledger.json").unlink()
    if reverse_engineering and plan.get("emptyTrackedClassifications"):
        ledger_path = candidate / "path-coverage-ledger.json"
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        ledger["trackedPathClassifications"] = {}
        ledger_path.write_text(json.dumps(ledger, sort_keys=True), encoding="utf-8")
    if reverse_engineering and plan.get("addUnmappedSource"):
        source_path = candidate / "src/payments.py"
        source_path.write_text("def total() -> int:\n    return 0\n", encoding="utf-8")
        ledger_path = candidate / "path-coverage-ledger.json"
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        ledger["trackedPathClassifications"]["src/payments.py"] = "MUST_DOCUMENT"
        ledger_path.write_text(json.dumps(ledger, sort_keys=True), encoding="utf-8")
    if reverse_engineering and plan.get("baselineClassificationMismatch"):
        ledger_path = candidate / "path-coverage-ledger.json"
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        ledger["sourceBaseline"]["paths"][0]["classification"] = "related-test"
        ledger_path.write_text(json.dumps(ledger, sort_keys=True), encoding="utf-8")

    def invoke(
        agent: str,
        phase: str,
        artifact: str = "",
        *,
        default_outcome: str = "PASS",
        claim: bool = True,
    ) -> str:
        if claim and claim_stack_enabled:
            trace.append(
                {
                    "index": len(trace),
                    "agent": "scripted-claim-double",
                    "phase": "claim-acquire",
                    "artifact": artifact or phase,
                    "outcome": "PASS",
                    "dispatchContext": "claim-helper",
                }
            )
        try:
            return dependencies.call(
                agent,
                phase,
                artifact,
                default_outcome=default_outcome,
                dispatch_context="secondary" if effective_secondary_dispatch else "primary",
            )
        finally:
            if claim and claim_stack_enabled:
                trace.append(
                    {
                        "index": len(trace),
                        "agent": "scripted-claim-double",
                        "phase": "claim-release",
                        "artifact": artifact or phase,
                        "outcome": "PASS",
                        "dispatchContext": "claim-helper",
                    }
                )

    def blocked(reason: str, accepted: list[str]) -> dict[str, Any]:
        return _terminal(
            "BLOCKED",
            trace,
            copiedInputs=copied,
            accepted=accepted,
            reason=reason,
            targetContractBound=True,
        )

    def correct_until_pass(
        agent: str,
        phase: str,
        artifact: str,
        correction_agent: str,
        correction_phase: str,
        accepted: list[str],
    ) -> str | dict[str, Any]:
        attempts = 0
        while True:
            outcome = invoke(agent, phase, artifact)
            if outcome == "PASS":
                return outcome
            if outcome in {"FAIL", "BLOCKED"}:
                return _terminal(
                    outcome,
                    trace,
                    copiedInputs=copied,
                    accepted=accepted,
                    targetContractBound=True,
                )
            attempts += 1
            if attempts > 2:
                return blocked("correction cap reached", accepted)
            correction = invoke(correction_agent, correction_phase, artifact)
            if correction != "PASS":
                return _terminal(
                    correction,
                    trace,
                    copiedInputs=copied,
                    accepted=accepted,
                    targetContractBound=True,
                )

    accepted: list[str] = []
    for artifact, producer in _PRODUCERS.items():
        if artifact not in _SETUP_OUTPUTS:
            produced = invoke(producer, "contribute", artifact)
            if produced != "PASS":
                return _terminal(
                    produced,
                    trace,
                    copiedInputs=copied,
                    accepted=accepted,
                    targetContractBound=True,
                )
            _write_artifact(candidate, artifact, contribution_phase=reverse_engineering)
        reviewer = _REVIEWERS[artifact]
        verdict = correct_until_pass(reviewer, "review", artifact, producer, "correct", accepted)
        if isinstance(verdict, dict):
            return verdict
        accepted.append(artifact)

    integration = correct_until_pass(
        "dev-merge-coordinator",
        "integrate",
        "multiple-contributions",
        "dev-merge-coordinator",
        "correct-integration",
        accepted,
    )
    if isinstance(integration, dict):
        return integration
    def post_integration_review(artifact: str, phase: str) -> dict[str, Any] | None:
        attempts = 0
        while True:
            verdict = invoke(_REVIEWERS[artifact], phase, artifact)
            if verdict == "PASS":
                return None
            if verdict in {"FAIL", "BLOCKED"}:
                return _terminal(
                    verdict,
                    trace,
                    copiedInputs=copied,
                    accepted=accepted,
                    targetContractBound=True,
                )
            attempts += 1
            if attempts > 2:
                return blocked("correction cap reached", accepted)
            correction = invoke(_PRODUCERS[artifact], "correct", artifact)
            if correction != "PASS":
                return _terminal(
                    correction,
                    trace,
                    copiedInputs=copied,
                    accepted=accepted,
                    targetContractBound=True,
                )
            reintegration = correct_until_pass(
                "dev-merge-coordinator",
                "reintegrate",
                artifact,
                "dev-merge-coordinator",
                "correct-integration",
                accepted,
            )
            if isinstance(reintegration, dict):
                return reintegration

    for artifact in accepted:
        finding = post_integration_review(artifact, "post-integration-review")
        if finding is not None:
            return finding
    for artifact in plan.get("ownershipSubstringTrap", ()):
        with (candidate / artifact).open("a", encoding="utf-8") as artifact_file:
            artifact_file.write("\nExpected maintainer: wiki-writer\n")
    if reverse_engineering and plan.get("swapCoverageManifestMappings"):
        coverage_path = candidate / "docs/coverage-manifest.yaml"
        _write_steady_state_artifact(candidate, "docs/coverage-manifest.yaml")
        manifest = yaml.safe_load(coverage_path.read_text(encoding="utf-8"))
        designs = [row["design"] for row in manifest["modules"]]
        for row, design in zip(manifest["modules"], reversed(designs), strict=True):
            row["design"] = design
        coverage_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
    for artifact in plan.get("removeAuditArtifact", ()):
        artifact_path = candidate / artifact
        if artifact_path.is_file():
            artifact_path.unlink()

    audit_findings: list[dict[str, str]] = []
    audit_owner_cycles: dict[str, int] = {}

    def audit_finding_key(finding: Mapping[str, str]) -> str:
        return "|".join(
            (
                finding["artifact"],
                finding["reason"],
                finding["authoritativeEvidence"],
            )
        )

    def apply_audit_owner_correction(
        finding: Mapping[str, str],
        phase: str,
    ) -> dict[str, Any] | None:
        artifact = finding["artifact"]
        owner = finding["owner"]
        finding_key = audit_finding_key(finding)
        while audit_owner_cycles.get(finding_key, 0) < 2:
            audit_owner_cycles[finding_key] = audit_owner_cycles.get(finding_key, 0) + 1
            correction = invoke(owner, phase, artifact)
            if correction == "PASS":
                _write_steady_state_artifact(candidate, artifact)
                if artifact not in accepted:
                    accepted.append(artifact)
                return None
            if correction in {"FAIL", "BLOCKED"}:
                return _terminal(
                    correction,
                    trace,
                    copiedInputs=copied,
                    accepted=accepted,
                    targetContractBound=True,
                )
        return blocked(f"audit owner correction cap reached: {artifact}", accepted)

    def route_audit_findings(
        findings: Sequence[dict[str, str]],
        integration_artifact: str,
    ) -> dict[str, Any] | None:
        for finding in findings:
            artifact = finding["artifact"]
            phase = "create" if not (candidate / artifact).is_file() else "correct-steady-state"
            correction_result = apply_audit_owner_correction(finding, phase)
            if correction_result is not None:
                return correction_result
        reintegration = correct_until_pass(
            "dev-merge-coordinator",
            "reintegrate",
            integration_artifact,
            "dev-merge-coordinator",
            "correct-integration",
            accepted,
        )
        if isinstance(reintegration, dict):
            return reintegration
        for finding in findings:
            artifact = finding["artifact"]
            review_attempts = 0
            while True:
                review = invoke(
                    _REVIEWERS[artifact],
                    "post-audit-integration-review",
                    artifact,
                )
                if review == "PASS":
                    break
                if review in {"FAIL", "BLOCKED"}:
                    return _terminal(
                        review,
                        trace,
                        copiedInputs=copied,
                        accepted=accepted,
                        targetContractBound=True,
                    )
                review_attempts += 1
                if review_attempts > 2:
                    return blocked(
                        f"post-audit integration review cap reached: {artifact}",
                        accepted,
                    )
                correction_result = apply_audit_owner_correction(
                    finding,
                    "correct-steady-state",
                )
                if correction_result is not None:
                    return correction_result
                reintegration = correct_until_pass(
                    "dev-merge-coordinator",
                    "reintegrate",
                    artifact,
                    "dev-merge-coordinator",
                    "correct-integration",
                    accepted,
                )
                if isinstance(reintegration, dict):
                    return reintegration
        return None

    def audit_until_clear(
        integration_artifact: str,
        initial_findings: Sequence[dict[str, str]] | None = None,
    ) -> dict[str, Any] | None:
        findings = list(initial_findings) if initial_findings is not None else None
        while True:
            if findings is None:
                try:
                    findings = _audit_findings(candidate, accepted)
                except _AuditEvidenceUnavailable as error:
                    invoke(
                        "wiki-ingester",
                        "final-evidence-audit",
                        "integrated-tree",
                        default_outcome="BLOCKED",
                        claim=False,
                    )
                    return blocked(str(error), accepted)
            audit = invoke(
                "wiki-ingester",
                "final-evidence-audit",
                "integrated-tree",
                default_outcome="NEEDS_CORRECTION" if findings else "PASS",
                claim=False,
            )
            expected_audit = "NEEDS_CORRECTION" if findings else "PASS"
            if audit != expected_audit:
                return _terminal(
                    "INFRASTRUCTURE_FAILED",
                    trace,
                    copiedInputs=copied,
                    accepted=accepted,
                    reason=f"final evidence audit returned {audit}, expected {expected_audit}",
                    targetContractBound=True,
                )
            if not findings:
                return None
            routing_result = route_audit_findings(findings, integration_artifact)
            if routing_result is not None:
                return routing_result
            findings = None

    if reverse_engineering:
        try:
            audit_findings = _audit_findings(candidate, accepted)
        except _AuditEvidenceUnavailable as error:
            invoke(
                "wiki-ingester",
                "final-evidence-audit",
                "integrated-tree",
                default_outcome="BLOCKED",
                claim=False,
            )
            return blocked(str(error), accepted)
        audit_result = audit_until_clear("audit-corrections", audit_findings)
        if audit_result is not None:
            return audit_result

    verification_attempts = 0
    while True:
        verification = invoke("dev-verifier", "final-verification", "integration")
        if verification == "PASS":
            break
        if verification in {"FAIL", "BLOCKED"}:
            return _terminal(
                verification,
                trace,
                copiedInputs=copied,
                accepted=accepted,
                targetContractBound=True,
            )
        verification_attempts += 1
        if verification_attempts > 2:
            return blocked("correction cap reached", accepted)
        raw_findings = plan.get("verificationFinding", ("integration",))
        finding = raw_findings[0] if raw_findings else "integration"
        if finding == "integration":
            correction_owner = "dev-merge-coordinator"
            correction_phase = "correct-integration"
        elif finding in _REVIEWERS:
            try:
                ledger = json.loads(
                    (candidate / "path-coverage-ledger.json").read_text(encoding="utf-8"),
                    object_pairs_hook=_unique_json_object,
                )
                correction_owner = ledger["artifactOwnership"][finding]
            except (KeyError, TypeError, json.JSONDecodeError, _AuditEvidenceUnavailable) as error:
                return _terminal(
                    "INFRASTRUCTURE_FAILED",
                    trace,
                    copiedInputs=copied,
                    accepted=accepted,
                    reason=f"verification finding has no persistent artifact owner: {finding}: {error}",
                    targetContractBound=True,
                )
            if not isinstance(correction_owner, str) or not correction_owner:
                return _terminal(
                    "INFRASTRUCTURE_FAILED",
                    trace,
                    copiedInputs=copied,
                    accepted=accepted,
                    reason=f"verification finding has no persistent artifact owner: {finding}",
                    targetContractBound=True,
                )
            correction_phase = "correct"
        else:
            return _terminal(
                "INFRASTRUCTURE_FAILED",
                trace,
                copiedInputs=copied,
                accepted=accepted,
                reason=f"unknown verification finding target: {finding}",
                targetContractBound=True,
            )
        correction = invoke(correction_owner, correction_phase, finding)
        if correction != "PASS":
            return _terminal(
                correction,
                trace,
                copiedInputs=copied,
                accepted=accepted,
                targetContractBound=True,
            )
        if reverse_engineering and finding in plan.get("verificationMutationMarker", ()):
            with (candidate / finding).open("a", encoding="utf-8") as artifact_file:
                artifact_file.write("\nFuture work remains after verification correction.\n")
        reintegration = correct_until_pass(
            "dev-merge-coordinator",
            "reintegrate",
            "integration",
            "dev-merge-coordinator",
            "correct-integration",
            accepted,
        )
        if isinstance(reintegration, dict):
            return reintegration
        review_targets = accepted if finding == "integration" else [finding]
        for artifact in review_targets:
            finding = post_integration_review(artifact, "post-verification-correction-review")
            if finding is not None:
                return finding
        if reverse_engineering:
            audit_result = audit_until_clear("verification-audit-corrections")
            if audit_result is not None:
                return audit_result
    return _terminal(
        "PASS",
        trace,
        executionId="resumed-project-bootstrapper",
        copiedInputs=copied,
        accepted=accepted,
        auditFindings=audit_findings,
        finalAuditFindings=[] if reverse_engineering else None,
        finalArtifacts={
            artifact: (candidate / artifact).read_text(encoding="utf-8")
            for artifact in accepted
        },
        integrationChoice="dev-merge-coordinator",
        finalReview=True,
        finalVerification=True,
        targetContractBound=True,
        validationGate="repository-render-validator",
        configuredCoordination=selectors["resourceCoordination"],
        secondaryDispatchEnabled=secondary_dispatch_enabled,
        effectiveSecondaryDispatchEnabled=effective_secondary_dispatch,
        legacyRuntimeDispatchBefore=legacy_runtime_dispatch_before,
        legacyRuntimeDispatchAfter=legacy_runtime_dispatch_after,
        dispatchSelector=selectors["dispatchSelector"],
        persistence=selectors["persistence"],
        commit=selectors["commit"],
        commitProviderSkill=selectors["commitProviderSkill"],
    )


def run_isolated(
    plan: Mapping[str, Sequence[str]] | None = None,
    *,
    timeout_seconds: float = 180.0,
    reverse_engineering: bool = False,
    configuration_case: str = "canonical-multitask",
    legacy_runtime_dispatch: bool | None = None,
) -> dict[str, Any]:
    """Run terminal and resumed Bootstrapper executions around primary configuration.

    The caller supplies ordered outcomes keyed by phase, phase and artifact, or agent name.
    Reverse-engineering mode adds the Wiki Ingester final evidence audit, owner-routed
    corrections, and a clear re-audit; ordinary setup skips that branch. A first isolated
    Bootstrapper execution terminates BLOCKED on missing configuration. A distinct primary
    Configurator execution writes and validates the selected configuration before a separately
    isolated Bootstrapper execution resumes. The timeout is one positive wall-clock budget for
    all executions. configuration_case selects canonical-solo, canonical-multitask, or legacy.
    A legacy case also requires legacy_runtime_dispatch to describe the existing runtime setting;
    the resumed execution preserves that setting. The result contains each isolated execution,
    cleanup evidence, and the fresh-main generated-projection prerequisite. Invalid arguments
    raise ValueError. Infrastructure failures and timeouts are terminal and never retry.
    """

    if timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be positive")
    if configuration_case == "legacy" and not isinstance(legacy_runtime_dispatch, bool):
        raise ValueError(
            "legacy configuration requires an explicit existing runtime dispatch setting"
        )
    if configuration_case != "legacy" and legacy_runtime_dispatch is not None:
        raise ValueError(
            "legacy runtime dispatch setting is allowed only for legacy configuration"
        )
    with tempfile.TemporaryDirectory(prefix="project-bootstrapper-scripted-") as directory:
        root = Path(directory)
        plan_path = root / "plan.json"
        plan_path.write_text(json.dumps(plan or {}), encoding="utf-8")
        deadline = time.monotonic() + timeout_seconds

        def launch(execution: str, project_path: Path | None = None) -> dict[str, Any]:
            result_path = root / f"{execution}-result.json"
            command = [
                sys.executable,
                str(Path(__file__).resolve()),
                "--worker",
                "--execution",
                execution,
                "--plan",
                str(plan_path),
                "--result",
                str(result_path),
                "--workspace",
                str(root / f"{execution}-workspace"),
                "--configuration-case",
                configuration_case,
            ]
            if project_path is not None:
                command.extend(("--project-configuration", str(project_path)))
            if execution == "resumed" and legacy_runtime_dispatch is not None:
                command.extend(
                    (
                        "--legacy-runtime-dispatch",
                        "enabled" if legacy_runtime_dispatch else "disabled",
                    )
                )
            if reverse_engineering and execution == "resumed":
                command.append("--reverse-engineering")
            remaining = deadline - time.monotonic()
            process = _start_owned_process(
                command,
                timeout_seconds=max(remaining, 0.001),
            )
            try:
                process.wait(timeout=max(remaining, 0.001))
            except subprocess.TimeoutExpired:
                _terminate_owned_process_tree(process)
                return {
                    "schema": "project-bootstrapper-scripted-result",
                    "version": 1,
                    "status": "INFRASTRUCTURE_FAILED",
                    "reason": "wall-clock timeout",
                    "timeoutSeconds": timeout_seconds,
                    "workerPid": process.pid,
                }
            if process.returncode != 0 or not result_path.is_file():
                return {
                    "schema": "project-bootstrapper-scripted-result",
                    "version": 1,
                    "status": "INFRASTRUCTURE_FAILED",
                    "reason": f"scripted {execution} worker exited {process.returncode}",
                }
            return json.loads(result_path.read_text(encoding="utf-8"))

        initial = launch("initial")
        if initial.get("status") == "INFRASTRUCTURE_FAILED":
            result = initial
        elif (
            initial.get("status") != "BLOCKED"
            or initial.get("reason") != "PRIMARY_PROJECT_CONFIGURATOR_HANDOFF_REQUIRED"
        ):
            result = {
                "schema": "project-bootstrapper-scripted-result",
                "version": 1,
                "status": "INFRASTRUCTURE_FAILED",
                "reason": "initial Bootstrapper execution did not return the required terminal handoff",
                "initialExecution": initial,
            }
        else:
            configuration = launch("configuration")
            if configuration.get("status") != "PASS":
                result = dict(configuration)
                result["initialExecution"] = initial
                result["configurationExecution"] = configuration
            else:
                project_configuration = configuration.pop("projectConfiguration")
                configuration.pop("renderedGuidance")
                project_path = root / "validated-project.json"
                project_path.write_text(
                    json.dumps(project_configuration, sort_keys=True),
                    encoding="utf-8",
                )
                resumed = launch("resumed", project_path)
                result = dict(resumed)
                result["initialExecution"] = initial
                result["configurationExecution"] = configuration
                result["resumedExecution"] = dict(resumed)
    result["ownedProcessCleanup"] = "complete"
    result["workspaceRemoved"] = not root.exists()
    return result


def main(argv: Sequence[str] | None = None) -> int:
    """Run the deterministic suite case or its private isolated worker.

    Normal callers may provide a JSON plan and a wall-clock limit in minutes. The private worker
    form is used only by run_isolated to contain hangs and guarantee process-group cleanup.
    The command prints one JSON result and returns zero only for the expected PASS outcome.
    """

    arguments_list = list(argv) if argv is not None else sys.argv[1:]
    if arguments_list[:1] == [_WINDOWS_JOB_WRAPPER]:
        return _windows_job_wrapper_main(arguments_list[1:])

    parser = argparse.ArgumentParser(description="Run scripted Project Bootstrapper orchestration.")
    parser.add_argument("--plan", type=Path)
    parser.add_argument("--timeout-minutes", type=float, default=3.0)
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument(
        "--execution",
        choices=("initial", "configuration", "resumed"),
        default="resumed",
        help=argparse.SUPPRESS,
    )
    parser.add_argument("--result", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--workspace", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--project-configuration", type=Path, help=argparse.SUPPRESS)
    parser.add_argument(
        "--legacy-runtime-dispatch",
        choices=("enabled", "disabled"),
        help="Existing dispatch setting required with --configuration-case legacy.",
    )
    parser.add_argument(
        "--configuration-case",
        choices=("canonical-solo", "canonical-multitask", "legacy"),
        default="canonical-multitask",
    )
    parser.add_argument("--reverse-engineering", action="store_true")
    arguments = parser.parse_args(arguments_list)
    plan = json.loads(arguments.plan.read_text(encoding="utf-8")) if arguments.plan else {}
    legacy_runtime_dispatch = (
        None
        if arguments.legacy_runtime_dispatch is None
        else arguments.legacy_runtime_dispatch == "enabled"
    )
    if arguments.worker:
        if arguments.result is None or arguments.workspace is None:
            parser.error("worker mode requires result and workspace")
        try:
            if arguments.execution == "initial":
                result = _run_missing_configuration_worker(arguments.workspace)
            elif arguments.execution == "configuration":
                result = _run_configuration_worker(
                    plan,
                    arguments.workspace,
                    arguments.configuration_case,
                )
            else:
                if arguments.project_configuration is None:
                    parser.error("resumed worker requires --project-configuration")
                project_configuration = json.loads(
                    arguments.project_configuration.read_text(encoding="utf-8")
                )
                result = _run_worker(
                    plan,
                    arguments.workspace,
                    project_configuration,
                    reverse_engineering=arguments.reverse_engineering,
                    legacy_runtime_dispatch=legacy_runtime_dispatch,
                )
        except Exception as error:
            result = _terminal("INFRASTRUCTURE_FAILED", [], reason=str(error))
        arguments.result.write_text(json.dumps(result, sort_keys=True), encoding="utf-8")
        return 0
    if arguments.configuration_case == "legacy" and legacy_runtime_dispatch is None:
        parser.error(
            "--configuration-case legacy requires --legacy-runtime-dispatch enabled or disabled"
        )
    if arguments.configuration_case != "legacy" and legacy_runtime_dispatch is not None:
        parser.error(
            "--legacy-runtime-dispatch is allowed only with --configuration-case legacy"
        )
    result = run_isolated(
        plan,
        timeout_seconds=arguments.timeout_minutes * 60,
        reverse_engineering=arguments.reverse_engineering,
        configuration_case=arguments.configuration_case,
        legacy_runtime_dispatch=legacy_runtime_dispatch,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
