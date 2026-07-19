# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Verifies the disposable dependency-routing fixture and its omission diagnostics.
# Governing test plan: evals/agent-tests/dev-orchestrator/fixtures/dependency-routing/fixture-contract.yaml

from __future__ import annotations

import importlib.util
import json
import re
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

    @staticmethod
    def _complete_dependency_routing_report() -> tuple[object, dict[str, object]]:
        """Build a complete structured report for omission-matrix tests."""
        catalog = runner._load_catalog(_SUITE_ROOT.parent, {"dev-orchestrator"})
        suite = catalog["dev-orchestrator"]
        scenario = next(item for item in suite.scenarios if item["id"] == "dependency-routing")
        suite = runner._Suite(suite.suite_id, suite.priority, suite.path, suite.manifest, (scenario,))
        run = runner._RunSpec(suite, ("dependency-routing",))
        fields = scenario["requiredHandoffReceiptFields"]
        receipts = [
            {field: lane if field == "lane" else f"{field}-evidence" for field in fields}
            for lane in scenario["requiredHandoffReceiptLanes"]
        ]
        report = {
            "runs": [
                {
                    "suite": "dev-orchestrator",
                    "scenarioResults": [
                        {
                            "scenario": "dependency-routing",
                            "status": "PASS",
                            "targetInvoked": True,
                            "judgeInvoked": True,
                            "identityEvidence": ["thread-bound"],
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
