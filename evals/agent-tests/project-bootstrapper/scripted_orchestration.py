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
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any


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
_REVIEWERS = {
    "PROJECT.yaml": "dev-artifact-reviewer",
    "AGENTS.md": "dev-artifact-reviewer",
    "docs/coverage-manifest.yaml": "dev-artifact-reviewer",
    "docs/module-catalog.md": "dev-artifact-reviewer",
    "docs/module-orders.md": "dev-artifact-reviewer",
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
        "1165715b1e95e5552a4c86766fccef669701c176d45ae23cabfbe1aa79806ed2"
    ),
    "generated/adapters/codex/agents/project-bootstrapper.toml": (
        "5ea090968a1c08d293701eded10446fdd268c9355421a899cb682d02e15030af"
    ),
}


class _ScriptedDependency:
    def __init__(self, plan: Mapping[str, Sequence[str]], trace: list[dict[str, Any]]) -> None:
        self._plan = {key: list(values) for key, values in plan.items()}
        self._trace = trace

    def call(self, agent: str, phase: str, artifact: str = "") -> str:
        key = f"{phase}:{artifact}" if artifact else phase
        outcomes = self._plan.get(key, self._plan.get(agent, ["PASS"]))
        outcome = outcomes.pop(0) if outcomes else "PASS"
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


def _copy_inputs(workspace: Path) -> list[str]:
    copied: list[str] = []
    sources = (
        _SUITE_ROOT / "agents",
        _SUITE_ROOT / "skills" / "project-bootstrapper-suite-contract",
        _SUITE_ROOT / "fixtures" / _FIXTURE_NAME,
        _SUITE_ROOT / "scenarios.yaml",
        _SUITE_ROOT / "suite.yaml",
        _REPOSITORY_ROOT / "agents" / "roles" / "project-setup" / "project-bootstrapper.role.yaml",
        _REPOSITORY_ROOT / "generated" / "adapters" / "codex" / "agents" / "project-bootstrapper.toml",
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


def _write_artifact(candidate: Path, artifact: str) -> None:
    target = candidate / artifact
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.suffix == ".yaml":
        target.write_text("schema: scripted-bootstrap-evidence\n", encoding="utf-8")
    else:
        target.write_text(f"# Scripted {target.stem.replace('-', ' ').title()}\n", encoding="utf-8")


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


def _run_worker(plan: Mapping[str, Sequence[str]], workspace: Path) -> dict[str, Any]:
    trace: list[dict[str, Any]] = []
    dependencies = _ScriptedDependency(plan, trace)
    copied = _copy_inputs(workspace)
    _validate_snapshot_contract(workspace)
    candidate = workspace / "candidate"

    def invoke(agent: str, phase: str, artifact: str = "") -> str:
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
            return dependencies.call(agent, phase, artifact)
        finally:
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

    configuration = invoke("project-configurator", "configure", "PROJECT.yaml")
    if configuration != "PASS":
        return _terminal(configuration, trace, copiedInputs=copied, targetContractBound=True)
    for artifact in _SETUP_OUTPUTS:
        _write_artifact(candidate, artifact)

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
            _write_artifact(candidate, artifact)
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
        elif finding in _PRODUCERS:
            correction_owner = _PRODUCERS[finding]
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
    return _terminal(
        "PASS",
        trace,
        copiedInputs=copied,
        accepted=accepted,
        integrationChoice="dev-merge-coordinator",
        finalReview=True,
        finalVerification=True,
        targetContractBound=True,
    )


def run_isolated(
    plan: Mapping[str, Sequence[str]] | None = None,
    *,
    timeout_seconds: float = 180.0,
) -> dict[str, Any]:
    """Run one scripted Bootstrapper case in a disposable subprocess.

    The caller supplies ordered outcomes keyed by phase, phase and artifact, or agent name.
    The timeout is a positive wall-clock duration in seconds; the command-line boundary exposes
    it in minutes. The returned result contains the complete call trace and cleanup evidence.
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
    arguments = parser.parse_args(argv)
    plan = json.loads(arguments.plan.read_text(encoding="utf-8")) if arguments.plan else {}
    if arguments.worker:
        if arguments.result is None or arguments.workspace is None:
            parser.error("worker mode requires result and workspace")
        try:
            result = _run_worker(plan, arguments.workspace)
        except Exception as error:
            result = _terminal("INFRASTRUCTURE_FAILED", [], reason=str(error))
        arguments.result.write_text(json.dumps(result, sort_keys=True), encoding="utf-8")
        return 0
    result = run_isolated(plan, timeout_seconds=arguments.timeout_minutes * 60)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
