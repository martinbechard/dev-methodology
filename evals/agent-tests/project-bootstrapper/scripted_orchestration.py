#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Runs the multi-contribution Bootstrapper contract with deterministic scripted agents in a disposable workspace.
# Governing test plan: evals/agent-tests/project-bootstrapper/test_scripted_orchestration.py

from __future__ import annotations

import argparse
import hashlib
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
_FIXTURE_NAME = "missing-configuration-multi-contribution"
_TERMINAL_OUTCOMES = frozenset({"PASS", "FAIL", "BLOCKED", "NEEDS_CORRECTION"})
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
    "agents/roles/project-setup/project-bootstrapper.role.yaml": (
        "a9c0dacbdb619dd0b4fed24e104fa0258c80c070ccb8f497ba8d8c3e951e73c5"
    ),
    "generated/adapters/codex/agents/project-bootstrapper.toml": (
        "55fbdedbfcfb9af332d748e9101040c73858a07b994f851b244f85e43df8228b"
    ),
    "agents/roles/wiki-activities/wiki-ingester.role.yaml": (
        "8f6f1947076a7f8c66cff52e8eb555ce18c845ff82582ce13060a5a44fbd66b4"
    ),
    "generated/adapters/codex/agents/wiki-ingester.toml": (
        "1fe6317f67e3595174c296cc263844de4ae3e75c4fbf8a70f6100b8d2a17ea0b"
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
        _REPOSITORY_ROOT / "agents" / "roles" / "project-setup" / "project-bootstrapper.role.yaml",
        _REPOSITORY_ROOT / "agents" / "roles" / "wiki-activities" / "wiki-ingester.role.yaml",
        _REPOSITORY_ROOT / "generated" / "adapters" / "codex" / "agents" / "project-bootstrapper.toml",
        _REPOSITORY_ROOT / "generated" / "adapters" / "codex" / "agents" / "wiki-ingester.toml",
        *(
            _REPOSITORY_ROOT / "skills" / skill
            for skill in (
                "agent-claim",
                "documentation-bootstrap",
                "development-methodology",
                "organise-project-files",
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
        **evidence,
    }


def _run_worker(
    plan: Mapping[str, Sequence[str]],
    workspace: Path,
    *,
    reverse_engineering: bool = False,
) -> dict[str, Any]:
    trace: list[dict[str, Any]] = []
    dependencies = _ScriptedDependency(plan, trace)
    copied = _copy_inputs(workspace)
    _validate_snapshot_contract(workspace)
    candidate = workspace / "candidate"
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
        if claim:
            trace.append(
                {
                    "index": len(trace),
                    "agent": "scripted-claim-double",
                    "phase": "claim-acquire",
                    "artifact": artifact or phase,
                    "outcome": "PASS",
                }
            )
        try:
            return dependencies.call(
                agent,
                phase,
                artifact,
                default_outcome=default_outcome,
            )
        finally:
            if claim:
                trace.append(
                    {
                        "index": len(trace),
                        "agent": "scripted-claim-double",
                        "phase": "claim-release",
                        "artifact": artifact or phase,
                        "outcome": "PASS",
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

    for procedure, artifact in (
        ("Configure Project Agents And Skills", "PROJECT.yaml"),
        ("Render Project Guidance", "AGENTS.md"),
        ("Verify Project Configuration", "PROJECT.yaml and AGENTS.md"),
    ):
        configuration = invoke("project-configurator", procedure, artifact)
        if configuration != "PASS":
            return _terminal(
                configuration,
                trace,
                copiedInputs=copied,
                targetContractBound=True,
            )
    for artifact in _SETUP_OUTPUTS:
        _write_artifact(candidate, artifact, contribution_phase=reverse_engineering)

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
    )


def run_isolated(
    plan: Mapping[str, Sequence[str]] | None = None,
    *,
    timeout_seconds: float = 180.0,
    reverse_engineering: bool = False,
) -> dict[str, Any]:
    """Run one scripted Bootstrapper case in a disposable subprocess.

    The caller supplies ordered outcomes keyed by phase, phase and artifact, or agent name.
    Reverse-engineering mode adds the Wiki Ingester final evidence audit, owner-routed
    corrections, and a clear re-audit; ordinary setup skips that branch. The timeout is a
    positive wall-clock duration in seconds, and the command-line boundary exposes it in
    minutes. The returned result contains the complete call trace and cleanup evidence.
    Infrastructure failures and timeouts are terminal and never retry a dependency.
    """

    if timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be positive")
    with tempfile.TemporaryDirectory(prefix="project-bootstrapper-scripted-") as directory:
        root = Path(directory)
        plan_path = root / "plan.json"
        result_path = root / "result.json"
        plan_path.write_text(json.dumps(plan or {}), encoding="utf-8")
        command = [
            sys.executable,
            str(Path(__file__).resolve()),
            "--worker",
            "--plan",
            str(plan_path),
            "--result",
            str(result_path),
            "--workspace",
            str(root / "workspace"),
        ]
        if reverse_engineering:
            command.append("--reverse-engineering")
        process = subprocess.Popen(command, start_new_session=True)
        try:
            process.wait(timeout=timeout_seconds)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait()
            return {
                "schema": "project-bootstrapper-scripted-result",
                "version": 1,
                "status": "INFRASTRUCTURE_FAILED",
                "reason": "wall-clock timeout",
                "timeoutSeconds": timeout_seconds,
                "ownedProcessCleanup": "complete",
                "workspaceRemoved": True,
                "workerPid": process.pid,
            }
        if process.returncode != 0 or not result_path.is_file():
            return {
                "schema": "project-bootstrapper-scripted-result",
                "version": 1,
                "status": "INFRASTRUCTURE_FAILED",
                "reason": f"scripted worker exited {process.returncode}",
                "ownedProcessCleanup": "complete",
                "workspaceRemoved": True,
            }
        result = json.loads(result_path.read_text(encoding="utf-8"))
    result["ownedProcessCleanup"] = "complete"
    result["workspaceRemoved"] = not root.exists()
    return result


def main(argv: Sequence[str] | None = None) -> int:
    """Run the deterministic suite case or its private isolated worker.

    Normal callers may provide a JSON plan and a wall-clock limit in minutes. The private worker
    form is used only by run_isolated to contain hangs and guarantee process-group cleanup.
    The command prints one JSON result and returns zero only for the expected PASS outcome.
    """

    parser = argparse.ArgumentParser(description="Run scripted Project Bootstrapper orchestration.")
    parser.add_argument("--plan", type=Path)
    parser.add_argument("--timeout-minutes", type=float, default=3.0)
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--result", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--workspace", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--reverse-engineering", action="store_true")
    arguments = parser.parse_args(argv)
    plan = json.loads(arguments.plan.read_text(encoding="utf-8")) if arguments.plan else {}
    if arguments.worker:
        if arguments.result is None or arguments.workspace is None:
            parser.error("worker mode requires result and workspace")
        try:
            result = _run_worker(
                plan,
                arguments.workspace,
                reverse_engineering=arguments.reverse_engineering,
            )
        except Exception as error:
            result = _terminal("INFRASTRUCTURE_FAILED", [], reason=str(error))
        arguments.result.write_text(json.dumps(result, sort_keys=True), encoding="utf-8")
        return 0
    result = run_isolated(
        plan,
        timeout_seconds=arguments.timeout_minutes * 60,
        reverse_engineering=arguments.reverse_engineering,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
