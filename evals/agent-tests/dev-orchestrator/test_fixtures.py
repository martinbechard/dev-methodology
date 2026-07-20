# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Verifies the disposable dependency-routing fixture and its omission diagnostics.
# Governing test plan: evals/agent-tests/dev-orchestrator/fixtures/dependency-routing/fixture-contract.yaml

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


_SUITE_ROOT = Path(__file__).resolve().parent
_RUNNER_PATH = _SUITE_ROOT.parent / "runner.py"
_SPEC = importlib.util.spec_from_file_location("dependency_routing_runner", _RUNNER_PATH)
assert _SPEC is not None and _SPEC.loader is not None
runner = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = runner
_SPEC.loader.exec_module(runner)


class DependencyRoutingFixtureTests(unittest.TestCase):
    """Protect the structured dependency-routing fixture without live model calls."""

    def test_committed_fixture_contract_is_complete(self) -> None:
        """The dependency-routing scenario exposes every required structured input."""
        catalog = runner._load_catalog(_SUITE_ROOT.parent, {"dev-orchestrator"})
        suite = catalog["dev-orchestrator"]
        scenario = next(item for item in suite.scenarios if item["id"] == "dependency-routing")

        runner._validate_fixture_contract(suite, scenario)

    def test_every_fixture_field_has_an_exact_omission_diagnostic(self) -> None:
        """Each required dotted path fails independently with its exact identity."""
        source = _SUITE_ROOT / "fixtures" / "dependency-routing" / "fixture-contract.yaml"
        complete = runner._load_yaml(source)
        scenario = {
            "id": "dependency-routing",
            "fixtureContract": "fixture-contract.yaml",
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            suite = runner._Suite(
                "dev-orchestrator",
                1,
                root,
                {"target": {"allowedAgentDependencies": ["dev-coder"]}},
                (scenario,),
            )
            contract = root / "fixture-contract.yaml"
            for dotted_path in runner._DEPENDENCY_ROUTING_FIXTURE_FIELDS:
                with self.subTest(field=dotted_path):
                    omitted = self._without_path(complete, dotted_path)
                    contract.write_text(runner.yaml.safe_dump(omitted, sort_keys=False), encoding="utf-8")
                    with self.assertRaisesRegex(
                        ValueError,
                        rf"dev-orchestrator:dependency-routing missing fixture field {re.escape(dotted_path)}",
                    ):
                        runner._validate_fixture_contract(suite, scenario)

    def test_every_handoff_field_has_an_exact_omission_diagnostic(self) -> None:
        """Every required receipt field fails independently with lane-specific evidence."""
        run, report = self._complete_dependency_routing_report()
        for field in run.suite.scenarios[0]["requiredHandoffReceiptFields"]:
            with self.subTest(field=field):
                omitted = json.loads(json.dumps(report))
                del omitted["runs"][0]["scenarioResults"][0]["handoffReceipts"][0][field]
                expected = (
                    "dev-orchestrator:dependency-routing missing handoff receipt lane source"
                    if field == "lane"
                    else f"dev-orchestrator:dependency-routing handoff receipt source missing field {field}"
                )
                with self.assertRaisesRegex(
                    RuntimeError,
                    expected,
                ):
                    runner._audit_report((run,), omitted)

    def test_every_handoff_lane_has_an_exact_omission_diagnostic(self) -> None:
        """Every required lane fails independently with its exact lane name."""
        run, report = self._complete_dependency_routing_report()
        lanes = run.suite.scenarios[0]["requiredHandoffReceiptLanes"]
        for lane in lanes:
            with self.subTest(lane=lane):
                omitted = json.loads(json.dumps(report))
                receipts = omitted["runs"][0]["scenarioResults"][0]["handoffReceipts"]
                receipts[:] = [receipt for receipt in receipts if receipt["lane"] != lane]
                with self.assertRaisesRegex(
                    RuntimeError,
                    rf"dev-orchestrator:dependency-routing missing handoff receipt lane {lane}",
                ):
                    runner._audit_report((run,), omitted)

    def test_scalar_receipt_evidence_matrix_is_rejected(self) -> None:
        """Non-empty prose strings cannot masquerade as repository or runtime evidence."""
        run, report = self._complete_dependency_routing_report()
        for field in ("commit", "review", "verification", "claimRelease"):
            with self.subTest(field=field):
                fabricated = json.loads(json.dumps(report))
                fabricated["runs"][0]["scenarioResults"][0]["handoffReceipts"][0][field] = "looks-valid"
                with self.assertRaisesRegex(
                    RuntimeError,
                    f"dev-orchestrator:dependency-routing handoff receipt source field {field} must be structured",
                ):
                    runner._audit_report((run,), fabricated)

    def test_fabricated_receipt_evidence_matrix_is_rejected(self) -> None:
        """Receipts must resolve to commits, retained sessions, and release journal events."""
        with tempfile.TemporaryDirectory() as directory:
            run, report, sessions, fixture_root = self._evidence_fixture(Path(directory))
            runner._audit_report((run,), report)
            runner._audit_handoff_evidence((run,), report, sessions, fixture_root)
            cases = {
                "commit": (
                    lambda receipt: receipt["commit"].update({"sha": "f" * 40}),
                    "commit lacks repository ancestry evidence",
                ),
                "review": (
                    lambda receipt: receipt["review"].update({"sessionIds": ["fabricated-review"]}),
                    "review sessions are not retained evidence",
                ),
                "verification": (
                    lambda receipt: receipt["verification"].update(
                        {"sessionIds": ["fabricated-verification"]}
                    ),
                    "verification sessions are not retained evidence",
                ),
                "claimRelease": (
                    lambda receipt: receipt["claimRelease"].update({"eventIds": ["fabricated-release"]}),
                    "claim release lacks fixture lifecycle evidence",
                ),
            }
            for field, (mutate, diagnostic) in cases.items():
                with self.subTest(field=field):
                    fabricated = json.loads(json.dumps(report))
                    mutate(fabricated["runs"][0]["scenarioResults"][0]["handoffReceipts"][0])
                    with self.assertRaisesRegex(RuntimeError, diagnostic):
                        runner._audit_handoff_evidence((run,), fabricated, sessions, fixture_root)

    def test_producer_session_evidence_matrix_is_rejected(self) -> None:
        """Producer identity requires a matching invocation and exact retained session ID."""
        with tempfile.TemporaryDirectory() as directory:
            run, report, sessions, fixture_root = self._evidence_fixture(Path(directory))
            receipt = report["runs"][0]["scenarioResults"][0]["handoffReceipts"][0]
            receipt["role"] = {"invocation": "dev-coder"}
            with self.assertRaisesRegex(
                RuntimeError,
                "handoff receipt source field role must be structured",
            ):
                runner._audit_report((run,), report)

        cases = {
            "fabricated": (
                {"invocation": "dev_coder", "sessionIds": ["fabricated-producer"]},
                "producer sessions are not retained evidence",
            ),
            "wrong-role": (
                {"invocation": "dev-verifier", "sessionIds": ["coder"]},
                "role invocation does not match lane producer",
            ),
        }
        for name, (role, diagnostic) in cases.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                run, report, sessions, fixture_root = self._evidence_fixture(Path(directory))
                report["runs"][0]["scenarioResults"][0]["handoffReceipts"][0]["role"] = role
                with self.assertRaisesRegex(RuntimeError, diagnostic):
                    runner._audit_handoff_evidence((run,), report, sessions, fixture_root)

    def test_receipts_may_retain_additional_same_role_review_and_verification_sessions(self) -> None:
        """Later retained gates may supplement, but cannot replace, each lane's required evidence."""
        with tempfile.TemporaryDirectory() as directory:
            run, report, sessions, fixture_root = self._evidence_fixture(Path(directory))
            source = report["runs"][0]["scenarioResults"][0]["handoffReceipts"][0]
            source["review"]["sessionIds"] = ["code-review-2", "code-review-1"]
            source["verification"]["sessionIds"] = ["verifier-2", "verifier-1"]

            runner._audit_handoff_evidence((run,), report, sessions, fixture_root)

    def test_receipt_session_superset_rejects_duplicates_replacements_and_foreign_roles(self) -> None:
        """Supplemental gate evidence remains unique, role-bound, and additive to required sessions."""
        cases = {
            "duplicate-review": ("review", ["code-review-1", "code-review-1"]),
            "replacement-review": ("review", ["code-review-2"]),
            "foreign-review": ("review", ["code-review-1", "artifact-review-1"]),
            "duplicate-verification": ("verification", ["verifier-1", "verifier-1"]),
            "replacement-verification": ("verification", ["verifier-2"]),
            "foreign-verification": ("verification", ["verifier-1", "code-review-1"]),
        }
        for name, (field, session_ids) in cases.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                run, report, sessions, fixture_root = self._evidence_fixture(Path(directory))
                source = report["runs"][0]["scenarioResults"][0]["handoffReceipts"][0]
                source[field]["sessionIds"] = session_ids

                with self.assertRaisesRegex(
                    RuntimeError,
                    rf"handoff receipt source {field} sessions are not retained evidence",
                ):
                    runner._audit_handoff_evidence((run,), report, sessions, fixture_root)

    def test_hyphenated_producer_alias_does_not_match_registered_invocation(self) -> None:
        """Receipt and release aliases cannot substitute for the literal retained runtime invocation."""
        with tempfile.TemporaryDirectory() as directory:
            run, report, sessions, fixture_root = self._evidence_fixture(Path(directory))
            receipt = report["runs"][0]["scenarioResults"][0]["handoffReceipts"][0]
            receipt["role"]["invocation"] = "dev-coder"

            with self.assertRaisesRegex(
                RuntimeError,
                "role invocation does not match lane producer",
            ):
                runner._audit_handoff_evidence((run,), report, sessions, fixture_root)

    def test_dirty_receipt_repository_matrix_is_rejected(self) -> None:
        """Tracked and untracked post-commit drift invalidate every receipt for that candidate."""
        for drift in ("tracked", "untracked"):
            with self.subTest(drift=drift), tempfile.TemporaryDirectory() as directory:
                run, report, sessions, fixture_root = self._evidence_fixture(Path(directory))
                candidate = fixture_root / "dev-orchestrator" / "candidate"
                if drift == "tracked":
                    (candidate / "evidence.txt").write_text("changed\n", encoding="utf-8")
                else:
                    (candidate / "untracked.txt").write_text("new\n", encoding="utf-8")
                with self.assertRaisesRegex(
                    RuntimeError,
                    "handoff receipt source repository has uncommitted drift",
                ):
                    runner._audit_handoff_evidence((run,), report, sessions, fixture_root)

    @staticmethod
    def _complete_dependency_routing_report() -> tuple[object, dict[str, object]]:
        """Build a complete structured report for omission-matrix tests."""
        catalog = runner._load_catalog(_SUITE_ROOT.parent, {"dev-orchestrator"})
        suite = catalog["dev-orchestrator"]
        scenario = next(item for item in suite.scenarios if item["id"] == "dependency-routing")
        suite = runner._Suite(suite.suite_id, suite.priority, suite.path, suite.manifest, (scenario,))
        run = runner._RunSpec(suite, ("dependency-routing",))
        receipts = [
            {
                "lane": lane,
                "role": {
                    "invocation": {
                        "source": "dev-coder",
                        "documentation": "dev-documentation-writer",
                        "integration": "dev-merge-coordinator",
                        "closeout": "dev-backlog-steward",
                    }[lane],
                    "sessionIds": ["producer-evidence"],
                },
                "commit": {"repository": "candidate", "sha": "a" * 40},
                "review": {"sessionIds": ["review-evidence"]},
                "verification": {"sessionIds": ["verification-evidence"]},
                "claimRelease": {"eventIds": ["release-evidence"]},
            }
            for lane in scenario["requiredHandoffReceiptLanes"]
        ]
        report = {
            "runs": [
                {
                    "suite": "dev-orchestrator",
                    "scenarioResults": [
                        {
                            "scenario": "dependency-routing",
                            "status": "BLOCKED",
                            "targetInvoked": True,
                            "judgeInvoked": True,
                            "identityEvidence": ["thread-bound"],
                            "deterministicEvidence": [],
                            "modelJudgeEvidence": ["judge-bound"],
                            "evidenceReceipts": [],
                            "cleanup": "clean",
                            "evidence": ["synthetic"],
                            "handoffReceipts": receipts,
                        }
                    ],
                    "maximumActiveChildrenObserved": 1,
                    "cleanup": "clean",
                }
            ],
            "batchCleanup": "clean",
            "residualRisk": "",
        }
        return run, report

    @classmethod
    def _evidence_fixture(
        cls,
        temporary_root: Path,
    ) -> tuple[object, dict[str, object], tuple[object, ...], Path]:
        """Create a disposable candidate repository and retained dependency evidence."""
        run, report = cls._complete_dependency_routing_report()
        fixture_root = temporary_root / "fixtures"
        candidate = fixture_root / "dev-orchestrator" / "candidate"
        candidate.mkdir(parents=True)
        subprocess.run(["git", "init", "--quiet"], cwd=candidate, check=True)
        subprocess.run(["git", "config", "user.name", "Fixture"], cwd=candidate, check=True)
        subprocess.run(["git", "config", "user.email", "fixture@example.invalid"], cwd=candidate, check=True)
        (candidate / "evidence.txt").write_text("synthetic\n", encoding="utf-8")
        subprocess.run(["git", "add", "evidence.txt"], cwd=candidate, check=True)
        subprocess.run(["git", "commit", "--quiet", "-m", "fixture evidence"], cwd=candidate, check=True)
        sha = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=candidate,
            check=True,
            text=True,
            capture_output=True,
        ).stdout.strip()
        roles = (
            ("coder", "dev_coder"),
            ("code-review-1", "dev_code_reviewer"),
            ("writer", "dev_documentation_writer"),
            ("artifact-review-1", "dev_artifact_reviewer"),
            ("verifier-1", "dev_verifier"),
            ("merge", "dev_merge_coordinator"),
            ("code-review-2", "dev_code_reviewer"),
            ("artifact-review-2", "dev_artifact_reviewer"),
            ("verifier-2", "dev_verifier"),
            ("backlog", "dev_backlog_steward"),
        )
        sessions = (
            runner._Session("supervisor", "root", "dev_orchestrator_suite_supervisor", 1, 0.0, 30.0, frozenset()),
            runner._Session("target", "supervisor", "dev_orchestrator", 2, 1.0, 29.0, frozenset()),
            *tuple(
                runner._Session(session_id, "target", role, 3, float(index * 2 + 2), float(index * 2 + 3), frozenset())
                for index, (session_id, role) in enumerate(roles)
            ),
        )
        receipt_by_lane = {
            receipt["lane"]: receipt
            for receipt in report["runs"][0]["scenarioResults"][0]["handoffReceipts"]
        }
        evidence = {
            "source": ("dev_coder", ["code-review-1"], ["verifier-1"]),
            "documentation": ("dev_documentation_writer", ["artifact-review-1"], ["verifier-1"]),
            "integration": (
                "dev_merge_coordinator",
                ["code-review-2", "artifact-review-2"],
                ["verifier-2"],
            ),
            "closeout": (
                "dev_backlog_steward",
                ["code-review-2", "artifact-review-2"],
                ["verifier-2"],
            ),
        }
        producer_session_ids = {role: session_id for session_id, role in roles}
        event_root = candidate / ".git" / "agent-claim-events" / "hot"
        event_root.mkdir(parents=True)
        events = []
        for lane, (role, review_ids, verification_ids) in evidence.items():
            event_id = f"release-{lane}"
            receipt_by_lane[lane].update(
                {
                    "role": {"invocation": role, "sessionIds": [producer_session_ids[role]]},
                    "commit": {"repository": "candidate", "sha": sha},
                    "review": {"sessionIds": review_ids},
                    "verification": {"sessionIds": verification_ids},
                    "claimRelease": {"eventIds": [event_id]},
                }
            )
            events.append(
                {
                    "action": "release",
                    "outcome": "RELEASED",
                    "event_id": event_id,
                    "agent": role,
                    "resulting_commit": sha,
                }
            )
        (event_root / "2026-07-19.jsonl").write_text(
            "".join(json.dumps(event) + "\n" for event in events),
            encoding="utf-8",
        )
        return run, report, sessions, fixture_root

    @staticmethod
    def _without_path(document: dict[str, object], dotted_path: str) -> dict[str, object]:
        """Return a recursive copy with one dotted mapping path omitted."""
        copied = runner.json.loads(runner.json.dumps(document))
        cursor = copied
        parts = dotted_path.split(".")
        for part in parts[:-1]:
            cursor = cursor[part]
        del cursor[parts[-1]]
        return copied


if __name__ == "__main__":
    unittest.main()
