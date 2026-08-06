# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies offline Dev Orchestrator fixtures, dependency routing, target preservation, and finding evidence.
# Governing test plan: evals/agent-tests/dev-orchestrator/fixtures/dependency-routing/fixture-contract.yaml

from __future__ import annotations

import hashlib
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

    def test_none_coordination_is_not_a_required_target_skill(self) -> None:
        """The provider-none fixture does not select claim behavior or evidence."""
        catalog = runner._load_catalog(_SUITE_ROOT.parent, {"dev-orchestrator"})
        suite = catalog["dev-orchestrator"]
        scenario = next(item for item in suite.scenarios if item["id"] == "dependency-routing")
        project = runner._load_yaml(
            _SUITE_ROOT / "fixtures" / "dependency-routing" / "PROJECT.yaml"
        )

        self.assertEqual("none", project["resource_coordination"]["selected"])
        self.assertNotIn("agent-claim", suite.manifest["target"]["requiredSkills"])
        self.assertIn("agent-claim", suite.manifest["target"]["conditionalSkills"])
        self.assertNotIn("agent-claim", scenario["targetSkills"])
        self.assertNotIn("claim-lifecycle", scenario["deterministicChecks"])
        self.assertNotIn("claimRelease", scenario["requiredHandoffReceiptFields"])

    def test_skill_under_test_finding_uses_separate_protected_and_provider_boundaries(self) -> None:
        """Prove an unchanged target digest and a durable file-provider finding receipt."""

        catalog = runner._load_catalog(_SUITE_ROOT.parent, {"dev-orchestrator"})
        suite = catalog["dev-orchestrator"]
        scenario = next(
            item for item in suite.scenarios if item["id"] == "skill-under-test-defect-routing"
        )
        fixture = _SUITE_ROOT / scenario["executableCase"]
        source_target = fixture / "target-skill" / "SKILL.md"
        expected = runner._load_yaml(fixture / "expected-finding.yaml")
        source_bytes = source_target.read_bytes()
        self.assertNotIn(expected["missingBehavior"], source_bytes.decode("utf-8"))
        self.assertEqual("deliberately-excluded", expected["currentDeliveryDisposition"])
        self.assertEqual("create-file-work-item", expected["creationProcedure"])

        protection = scenario["protectedTarget"]
        allowed_mutations = scenario["allowedMutationPaths"]
        self.assertEqual(protection["path"], source_target.relative_to(fixture).as_posix())
        self.assertEqual(protection["sha256"], hashlib.sha256(source_bytes).hexdigest())
        self.assertEqual(
            allowed_mutations,
            [f"{expected['providerPath']}/{expected['providerItem']}"],
        )

        with tempfile.TemporaryDirectory() as directory:
            scenario_root = Path(directory)
            protected_target = scenario_root / protection["path"]
            protected_target.parent.mkdir(parents=True)
            protected_target.write_bytes(source_bytes)
            before_digest = hashlib.sha256(protected_target.read_bytes()).hexdigest()

            finding = (
                scenario_root
                / expected["providerPath"]
                / expected["providerItem"]
            )
            finding.parent.mkdir(parents=True)
            finding.write_text(
                "\n".join(
                    (
                        "# Synthetic Target Skill Missing Finding Receipt",
                        "",
                        "Status: Ready",
                        "",
                        "Type: Defect",
                        "",
                        "Provider: file",
                        "",
                        f"Provider Reference: {expected['providerPath']}/{expected['providerItem']}",
                        "",
                        "Completion: direct-main",
                        "",
                        "Owner: Unowned",
                        "",
                        "## Summary",
                        "",
                        "Record the missing synthetic target behavior without changing the target under test.",
                        "",
                        "## Source Evidence",
                        "",
                        f"Missing Behavior: {expected['missingBehavior']}",
                        "",
                        "Current Delivery Disposition: Deliberately excluded",
                        "",
                        f"Creation Procedure: {expected['creationProcedure']}",
                        "",
                        "Target Disposition: Preserved without mutation",
                        "",
                        "## Requirements",
                        "",
                        "- Preserve the frozen target bytes and digest.",
                        "- Correct the target only through a separately authorized delivery task.",
                        "",
                        "## Acceptance Criteria",
                        "",
                        "- The target finding is reproducible from the governed evidence.",
                        "- No evaluation run mutates the target to obtain a pass.",
                        "",
                        "## Dependencies",
                        "",
                        "None.",
                        "",
                        "## Verification",
                        "",
                        "Compare the frozen target digest before and after the evaluation.",
                        "",
                        "## Open Questions",
                        "",
                        "None.",
                        "",
                    )
                ),
                encoding="utf-8",
            )

            after_digest = hashlib.sha256(protected_target.read_bytes()).hexdigest()
            finding_text = finding.read_text(encoding="utf-8")
            observed_mutations = [finding.relative_to(scenario_root).as_posix()]

        self.assertEqual(before_digest, after_digest)
        self.assertEqual(protection["sha256"], after_digest)
        self.assertEqual(allowed_mutations, observed_mutations)
        self.assertIn("Status: Ready", finding_text)
        self.assertIn("Provider: file", finding_text)
        self.assertIn(expected["missingBehavior"], finding_text)
        self.assertIn("Current Delivery Disposition: Deliberately excluded", finding_text)
        self.assertIn("Creation Procedure: create-file-work-item", finding_text)
        self.assertIn("Target Disposition: Preserved without mutation", finding_text)
        self.assertNotIn("requiresWorkspaceInventory", scenario)
        self.assertNotIn("requiresNoDetectedMutation", scenario)
        self.assertEqual(["dev-backlog-steward"], scenario["allowedAgentDependencies"])
        self.assertEqual(["finding"], scenario["requiredHandoffReceiptLanes"])
        self.assertIn("allowed-paths-only", scenario["deterministicChecks"])
        self.assertNotIn("no-forbidden-mutation", scenario["deterministicChecks"])
        self.assertIn("committed-handoffs", scenario["deterministicChecks"])

    def test_resource_coordination_contract_keeps_both_selections(self) -> None:
        """The fixture keeps private file lanes claim-free and Event Contract claims scoped."""
        contract = runner._load_yaml(
            _SUITE_ROOT / "fixtures" / "dependency-routing" / "fixture-contract.yaml"
        )
        coordination = contract["resourceCoordination"]

        self.assertEqual("none", coordination["selected"])
        self.assertEqual([], coordination["cases"]["none"]["claimCalls"])
        self.assertEqual("absent", coordination["cases"]["none"]["claimEvidence"])
        self.assertNotIn(
            "claimRelease",
            coordination["cases"]["none"]["requiredHandoffReceiptFields"],
        )
        agent_claim = coordination["cases"]["agent-claim"]
        self.assertEqual(["source", "documentation"], agent_claim["claimFreeFileLanes"])
        self.assertEqual(["integration", "closeout"], agent_claim["claimedLanes"])
        self.assertEqual("project-files", agent_claim["integrationScope"])
        self.assertNotIn("integrationResource", agent_claim)
        self.assertNotIn("claimRelease", agent_claim["requiredHandoffReceiptFields"])

    def test_none_coordination_report_omits_claim_release_evidence(self) -> None:
        """Provider-none receipts remain structured without claim release objects."""
        run, report = self._complete_dependency_routing_report()

        runner._audit_report((run,), report)

    def test_coordinator_prompt_exposes_none_coordination_boundary(self) -> None:
        """The live assignment explicitly forbids claim behavior for provider-none."""
        run, _ = self._complete_dependency_routing_report()

        prompt = runner._coordinator_prompt(
            (run,),
            Path("/checkpoints"),
            Path("/fixtures"),
            "test-run",
        )

        self.assertIn(
            '"resourceCoordinationByScenario": {"dependency-routing": "none"}',
            prompt,
        )
        self.assertIn("must not invoke agent-claim", prompt)

    def test_report_rejects_extra_lane_with_or_without_claims(self) -> None:
        """None and agent-claim report configurations reject extra receipt lanes."""
        for claim_release in (False, True):
            with (
                self.subTest(claim_release=claim_release),
                tempfile.TemporaryDirectory() as directory,
            ):
                run, report, _, _ = self._evidence_fixture(
                    Path(directory),
                    claim_release=claim_release,
                )
                source = report["runs"][0]["scenarioResults"][0][
                    "handoffReceipts"
                ][0]
                extra = json.loads(json.dumps(source))
                extra["lane"] = "extra"
                if claim_release:
                    extra["claimRelease"] = {
                        "eventIds": ["fabricated-release"],
                    }
                report["runs"][0]["scenarioResults"][0][
                    "handoffReceipts"
                ].append(extra)

                with self.assertRaisesRegex(
                    RuntimeError,
                    r"handoff receipt lanes mismatch: expected "
                    r"\['closeout', 'documentation', 'integration', 'source'\], "
                    r"observed "
                    r"\['closeout', 'documentation', 'extra', 'integration', 'source'\]",
                ):
                    runner._audit_report((run,), report)

    def test_evidence_audit_rejects_extra_lane_with_or_without_claims(self) -> None:
        """Repository evidence cannot legitimize an unconfigured receipt lane."""
        for claim_release in (False, True):
            with (
                self.subTest(claim_release=claim_release),
                tempfile.TemporaryDirectory() as directory,
            ):
                run, report, sessions, fixture_root = self._evidence_fixture(
                    Path(directory),
                    claim_release=claim_release,
                )
                source = report["runs"][0]["scenarioResults"][0][
                    "handoffReceipts"
                ][0]
                extra = json.loads(json.dumps(source))
                extra["lane"] = "extra"
                if claim_release:
                    extra["claimRelease"] = {
                        "eventIds": ["fabricated-release"],
                    }
                report["runs"][0]["scenarioResults"][0][
                    "handoffReceipts"
                ].append(extra)

                with self.assertRaisesRegex(
                    RuntimeError,
                    r"handoff receipt lanes mismatch: expected "
                    r"\['closeout', 'documentation', 'integration', 'source'\], "
                    r"observed "
                    r"\['closeout', 'documentation', 'extra', 'integration', 'source'\]",
                ):
                    runner._audit_handoff_evidence(
                        (run,),
                        report,
                        sessions,
                        fixture_root,
                    )

    def test_report_rejects_receipt_for_empty_lane_set(self) -> None:
        """None and agent-claim report configurations reject unconfigured receipts."""
        for claim_release in (False, True):
            with (
                self.subTest(claim_release=claim_release),
                tempfile.TemporaryDirectory() as directory,
            ):
                run, report, _, _ = self._evidence_fixture(
                    Path(directory),
                    claim_release=claim_release,
                )
                scenario = dict(run.suite.scenarios[0])
                scenario["requiredHandoffReceiptLanes"] = []
                scenario["requiredHandoffReceiptFields"] = []
                suite = runner.dataclasses.replace(
                    run.suite,
                    scenarios=(scenario,),
                )
                run = runner.dataclasses.replace(run, suite=suite)
                fabricated_receipt = {"lane": "fabricated"}
                if claim_release:
                    fabricated_receipt["claimRelease"] = {
                        "eventIds": ["fabricated-release"],
                    }
                report["runs"][0]["scenarioResults"][0][
                    "handoffReceipts"
                ] = [fabricated_receipt]

                with self.assertRaisesRegex(
                    RuntimeError,
                    r"handoff receipt lanes mismatch: expected \[\], "
                    r"observed \['fabricated'\]",
                ):
                    runner._audit_report((run,), report)

    def test_evidence_audit_preserves_missing_and_duplicate_lane_errors(self) -> None:
        """Exact-set enforcement retains distinct missing and duplicate diagnostics."""
        for case, diagnostic in (
            ("missing", "missing handoff receipt lane source"),
            ("duplicate", "duplicate handoff receipt lane source"),
        ):
            with (
                self.subTest(case=case),
                tempfile.TemporaryDirectory() as directory,
            ):
                run, report, sessions, fixture_root = self._evidence_fixture(
                    Path(directory),
                    claim_release=False,
                )
                receipts = report["runs"][0]["scenarioResults"][0][
                    "handoffReceipts"
                ]
                if case == "missing":
                    receipts[:] = [
                        receipt
                        for receipt in receipts
                        if receipt["lane"] != "source"
                    ]
                else:
                    source = next(
                        receipt
                        for receipt in receipts
                        if receipt["lane"] == "source"
                    )
                    receipts.append(json.loads(json.dumps(source)))

                with self.assertRaisesRegex(RuntimeError, diagnostic):
                    runner._audit_handoff_evidence(
                        (run,),
                        report,
                        sessions,
                        fixture_root,
                    )

    def test_evidence_audit_rejects_receipt_for_empty_lane_set(self) -> None:
        """None and claim-bound scenarios reject receipts when no lanes are configured."""
        for claim_release in (False, True):
            with (
                self.subTest(claim_release=claim_release),
                tempfile.TemporaryDirectory() as directory,
            ):
                run, report, sessions, fixture_root = self._evidence_fixture(
                    Path(directory),
                    claim_release=claim_release,
                )
                scenario = dict(run.suite.scenarios[0])
                scenario["requiredHandoffReceiptLanes"] = []
                scenario["requiredHandoffReceiptFields"] = []
                suite = runner.dataclasses.replace(
                    run.suite,
                    scenarios=(scenario,),
                )
                run = runner.dataclasses.replace(run, suite=suite)
                fabricated_receipt = {"lane": "fabricated"}
                if claim_release:
                    fabricated_receipt["claimRelease"] = {
                        "eventIds": ["fabricated-release"],
                    }
                report["runs"][0]["scenarioResults"][0][
                    "handoffReceipts"
                ] = [fabricated_receipt]

                with self.assertRaisesRegex(
                    RuntimeError,
                    r"handoff receipt lanes mismatch: expected \[\], "
                    r"observed \['fabricated'\]",
                ):
                    runner._audit_handoff_evidence(
                        (run,),
                        report,
                        sessions,
                        fixture_root,
                    )

    def test_none_coordination_evidence_needs_no_claim_journal(self) -> None:
        """Provider-none handoffs validate without claim events or a claim registry."""
        with tempfile.TemporaryDirectory() as directory:
            run, report, sessions, fixture_root = self._evidence_fixture(
                Path(directory),
                claim_release=False,
            )

            runner._audit_report((run,), report)
            runner._audit_handoff_evidence((run,), report, sessions, fixture_root)
            candidate = (
                fixture_root
                / "dev-orchestrator"
                / "dependency-routing"
                / "candidate"
            )
            self.assertFalse((candidate / ".git" / "agent-claim-events").exists())
            self.assertFalse((candidate / ".git" / "agent-claims.json").exists())

    def test_none_coordination_ignores_pre_existing_claim_files(self) -> None:
        """Repository-wide claim files do not prove that this scenario used claims."""
        with tempfile.TemporaryDirectory() as directory:
            run, report, sessions, fixture_root = self._evidence_fixture(
                Path(directory),
                claim_release=False,
            )
            candidate = (
                fixture_root
                / "dev-orchestrator"
                / "dependency-routing"
                / "candidate"
            )
            (candidate / ".git" / "agent-claims.json").write_text(
                json.dumps({"claims": []}) + "\n",
                encoding="utf-8",
            )
            journal = (
                candidate
                / ".git"
                / "agent-claim-events"
                / "hot"
                / "2026-07-19.jsonl"
            )
            journal.parent.mkdir(parents=True)
            journal.write_text(
                json.dumps(
                    {
                        "action": "release",
                        "outcome": "RELEASED",
                        "event_id": "pre-existing-release",
                    }
                )
                + "\n",
                encoding="utf-8",
            )

            runner._audit_handoff_evidence(
                (run,),
                report,
                sessions,
                fixture_root,
            )

    def test_none_coordination_rejects_claim_invocation(self) -> None:
        """An actual claim-helper call by the scenario remains invalid."""
        for session_id in ("target", "coder"):
            with (
                self.subTest(session_id=session_id),
                tempfile.TemporaryDirectory() as directory,
            ):
                run, report, sessions, fixture_root = self._evidence_fixture(
                    Path(directory),
                    claim_release=False,
                )
                rollout = Path(directory) / f"rollout-{session_id}.jsonl"
                rollout.write_text(
                    json.dumps(
                        {
                            "timestamp": "2026-07-19T00:00:00Z",
                            "type": "response_item",
                            "payload": {
                                "type": "custom_tool_call",
                                "name": "exec",
                                "input": (
                                    "python3 /bundle/agent-claim-command/scripts/claim.py "
                                    "--repo . status"
                                ),
                            },
                        }
                    )
                    + "\n",
                    encoding="utf-8",
                )
                sessions = tuple(
                    (
                        runner.dataclasses.replace(session, rollout_path=rollout)
                        if session.session_id == session_id
                        else session
                    )
                    for session in sessions
                )

                with self.assertRaisesRegex(
                    RuntimeError,
                    "unexpected agent-claim invocation",
                ):
                    runner._audit_handoff_evidence(
                        (run,),
                        report,
                        sessions,
                        fixture_root,
                    )

    def test_agent_claim_companion_executes_and_audits_complete_lifecycle(self) -> None:
        """The selected provider proves configured acquire, commit, release, and cleanup."""
        with tempfile.TemporaryDirectory() as directory:
            run, report, sessions, fixture_root = self._evidence_fixture(Path(directory))
            prompt = runner._coordinator_prompt(
                (run,),
                Path(directory) / "checkpoints",
                fixture_root,
                "test-run",
            )

            runner._validate_fixture_contract(run.suite, run.suite.scenarios[0])
            runner._audit_report((run,), report)
            runner._audit_handoff_evidence((run,), report, sessions, fixture_root)
            self.assertIn(
                '"resourceCoordinationByScenario": {"dependency-routing": "agent-claim"}',
                prompt,
            )

            candidate = (
                fixture_root
                / "dev-orchestrator"
                / "dependency-routing"
                / "candidate"
            )
            registry = json.loads(
                (candidate / ".git" / "agent-claims.json").read_text(encoding="utf-8")
            )
            self.assertEqual([], registry["claims"])

    def test_agent_claim_companion_allows_released_named_resource_event(self) -> None:
        """A resource-only Event Contract claim remains independent of private file lanes."""
        with tempfile.TemporaryDirectory() as directory:
            run, report, sessions, fixture_root = self._evidence_fixture(Path(directory))
            candidate = (
                fixture_root
                / "dev-orchestrator"
                / "dependency-routing"
                / "candidate"
            )
            journal = (
                candidate
                / ".git"
                / "agent-claim-events"
                / "hot"
                / "2026-07-19.jsonl"
            )
            events = [
                json.loads(line)
                for line in journal.read_text(encoding="utf-8").splitlines()
            ]
            resource_scopes = {
                "files": [],
                "trees": [],
                "project_files": False,
                "backlog": False,
                "all_files": False,
                "file_domain": "none",
                "resources": ["browser-test:fixture"],
            }
            events.extend(
                (
                    {
                        "schema_version": 1,
                        "action": "acquire",
                        "outcome": "PRIMARY",
                        "event_id": "acquire-browser",
                        "claim_id": "browser-claim",
                        "agent": "dev_coder",
                        "baseline_commit": None,
                        "resulting_commit": None,
                        "scopes": resource_scopes,
                    },
                    {
                        "schema_version": 1,
                        "action": "release",
                        "outcome": "RELEASED",
                        "event_id": "release-browser",
                        "claim_id": "browser-claim",
                        "agent": "dev_coder",
                        "baseline_commit": None,
                        "resulting_commit": None,
                        "scopes": resource_scopes,
                    },
                )
            )
            journal.write_text(
                "".join(json.dumps(event) + "\n" for event in events),
                encoding="utf-8",
            )

            runner._audit_handoff_evidence(
                (run,),
                report,
                sessions,
                fixture_root,
            )

    def test_agent_claim_companion_rejects_lifecycle_breaks(self) -> None:
        """The selected provider rejects missing, late, mis-scoped, or dirty claims."""
        cases = {
            "missing-acquire": "has no matching PRIMARY acquisition",
            "acquire-after-release": "acquisition does not precede release",
            "acquire-after-mutation": "acquisition does not precede mutation",
            "early-integration-claim": "acquisition does not precede mutation",
            "wrong-integration-scope": "scope disagrees with configured integration scope",
            "unexpected-integration-resource": "unexpected claim resource",
            "unsupported-schema": "Unsupported claim journal schema",
            "isolated-integration-acquire": "no matching PRIMARY acquisition",
            "duplicate-release-event-ids": "exactly one claim release event",
            "multiple-release-event-ids": "exactly one claim release event",
            "surplus-bound-successful-release": "exactly one successful release",
            "surplus-private-file-claim": "unbound file-scope acquisition",
            "second-repository-surplus-claim": "unbound file-scope acquisition",
            "duplicate-claim-id-across-repositories": "unbound file-scope acquisition",
            "unrecognized-named-resource": "outside the Event Contract",
            "unreleased-named-resource": "lacks one later release",
            "resource-file-domain": "noncanonical file domain",
            "malformed-journal-json": "Malformed claim journal JSON",
            "active-registry": "retains active claims",
        }
        for case, diagnostic in cases.items():
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                run, report, sessions, fixture_root = self._evidence_fixture(Path(directory))
                candidate = (
                    fixture_root
                    / "dev-orchestrator"
                    / "dependency-routing"
                    / "candidate"
                )
                journal = (
                    candidate
                    / ".git"
                    / "agent-claim-events"
                    / "hot"
                    / "2026-07-19.jsonl"
                )
                events = [
                    json.loads(line)
                    for line in journal.read_text(encoding="utf-8").splitlines()
                ]
                if case == "missing-acquire":
                    events[:] = [
                        event
                        for event in events
                        if not (
                            event["action"] == "acquire"
                            and event["claim_id"] == "integration-claim"
                        )
                    ]
                elif case == "acquire-after-release":
                    integration_acquire = next(
                        event
                        for event in events
                        if event["action"] == "acquire"
                        and event["claim_id"] == "integration-claim"
                    )
                    events.remove(integration_acquire)
                    release_index = next(
                        index
                        for index, event in enumerate(events)
                        if event["action"] == "release"
                        and event["claim_id"] == "integration-claim"
                    )
                    events.insert(release_index + 1, integration_acquire)
                elif case == "acquire-after-mutation":
                    integration_acquire = next(
                        event
                        for event in events
                        if event["action"] == "acquire"
                        and event["claim_id"] == "integration-claim"
                    )
                    integration_release = next(
                        event
                        for event in events
                        if event["action"] == "release"
                        and event["claim_id"] == "integration-claim"
                    )
                    integration_acquire["baseline_commit"] = integration_release["resulting_commit"]
                elif case == "early-integration-claim":
                    integration_acquire = next(
                        event
                        for event in events
                        if event["action"] == "acquire"
                        and event["claim_id"] == "integration-claim"
                    )
                    integration_acquire["baseline_commit"] = subprocess.run(
                        ["git", "rev-parse", f"{integration_acquire['baseline_commit']}^"],
                        cwd=candidate,
                        check=True,
                        text=True,
                        capture_output=True,
                    ).stdout.strip()
                elif case == "wrong-integration-scope":
                    integration_acquire = next(
                        event
                        for event in events
                        if event["action"] == "acquire"
                        and event["claim_id"] == "integration-claim"
                    )
                    integration_acquire["scopes"]["project_files"] = False
                    integration_acquire["scopes"]["files"] = ["integration.txt"]
                elif case == "unexpected-integration-resource":
                    integration_acquire = next(
                        event
                        for event in events
                        if event["action"] == "acquire"
                        and event["claim_id"] == "integration-claim"
                    )
                    integration_acquire["scopes"]["resources"] = [
                        "merge:integration:fixture-main"
                    ]
                elif case == "unsupported-schema":
                    integration_acquire = next(
                        event
                        for event in events
                        if event["action"] == "acquire"
                        and event["claim_id"] == "integration-claim"
                    )
                    integration_acquire["schema_version"] = 999
                elif case == "isolated-integration-acquire":
                    integration_acquire = next(
                        event
                        for event in events
                        if event["action"] == "acquire"
                        and event["claim_id"] == "integration-claim"
                    )
                    integration_acquire["outcome"] = "ISOLATE"
                elif case in {
                    "duplicate-release-event-ids",
                    "multiple-release-event-ids",
                }:
                    integration_receipt = next(
                        receipt
                        for receipt in report["runs"][0]["scenarioResults"][0][
                            "handoffReceipts"
                        ]
                        if receipt["lane"] == "integration"
                    )
                    release_event_id = integration_receipt["claimRelease"]["eventIds"][0]
                    if case == "duplicate-release-event-ids":
                        integration_receipt["claimRelease"]["eventIds"] = [
                            release_event_id,
                            release_event_id,
                        ]
                    else:
                        integration_acquire = next(
                            event
                            for event in events
                            if event["action"] == "acquire"
                            and event["claim_id"] == "integration-claim"
                        )
                        integration_release = next(
                            event
                            for event in events
                            if event["action"] == "release"
                            and event["claim_id"] == "integration-claim"
                        )
                        second_acquire = json.loads(json.dumps(integration_acquire))
                        second_acquire.update(
                            {
                                "event_id": "acquire-integration-second",
                                "claim_id": "integration-claim-second",
                            }
                        )
                        second_release = json.loads(json.dumps(integration_release))
                        second_release.update(
                            {
                                "event_id": "release-integration-second",
                                "claim_id": "integration-claim-second",
                            }
                        )
                        events.extend((second_acquire, second_release))
                        integration_receipt["claimRelease"]["eventIds"] = [
                            release_event_id,
                            "release-integration-second",
                        ]
                elif case == "surplus-bound-successful-release":
                    integration_release = next(
                        event
                        for event in events
                        if event["action"] == "release"
                        and event["claim_id"] == "integration-claim"
                    )
                    second_release = json.loads(json.dumps(integration_release))
                    second_release["event_id"] = "release-integration-surplus"
                    events.append(second_release)
                elif case == "surplus-private-file-claim":
                    events.append(
                        {
                            "schema_version": 1,
                            "action": "acquire",
                            "outcome": "PRIMARY",
                            "event_id": "acquire-private-source",
                            "claim_id": "private-source-claim",
                            "agent": "dev_code_reviewer",
                            "baseline_commit": None,
                            "resulting_commit": None,
                            "scopes": {
                                "files": ["src/dependency_status.py"],
                                "trees": [],
                                "project_files": False,
                                "backlog": False,
                                "all_files": False,
                                "file_domain": "project_files",
                                "resources": [],
                            },
                        }
                    )
                elif case in {
                    "second-repository-surplus-claim",
                    "duplicate-claim-id-across-repositories",
                }:
                    second_repository = candidate.parent / "second-candidate"
                    second_repository.mkdir()
                    subprocess.run(
                        ["git", "init", "--quiet"],
                        cwd=second_repository,
                        check=True,
                    )
                    second_common = second_repository / ".git"
                    second_event_root = (
                        second_common / "agent-claim-events" / "hot"
                    )
                    second_event_root.mkdir(parents=True)
                    second_claim_id = (
                        "integration-claim"
                        if case == "duplicate-claim-id-across-repositories"
                        else "second-repository-claim"
                    )
                    second_event = {
                        "schema_version": 1,
                        "action": "acquire",
                        "outcome": "PRIMARY",
                        "event_id": f"acquire-{case}",
                        "claim_id": second_claim_id,
                        "agent": "dev_code_reviewer",
                        "baseline_commit": None,
                        "resulting_commit": None,
                        "scopes": {
                            "files": ["unbound.txt"],
                            "trees": [],
                            "project_files": False,
                            "backlog": False,
                            "all_files": False,
                            "file_domain": "project_files",
                            "resources": [],
                        },
                    }
                    (second_event_root / "2026-07-19.jsonl").write_text(
                        json.dumps(second_event) + "\n",
                        encoding="utf-8",
                    )
                    (second_common / "agent-claims.json").write_text(
                        json.dumps({"claims": []}) + "\n",
                        encoding="utf-8",
                    )
                elif case in {
                    "unrecognized-named-resource",
                    "unreleased-named-resource",
                    "resource-file-domain",
                }:
                    resource = (
                        "merge:integration:fixture-main"
                        if case == "unrecognized-named-resource"
                        else "browser-test:fixture"
                    )
                    events.append(
                        {
                            "schema_version": 1,
                            "action": "acquire",
                            "outcome": "PRIMARY",
                            "event_id": f"acquire-{case}",
                            "claim_id": f"{case}-claim",
                            "agent": "dev_code_reviewer",
                            "baseline_commit": None,
                            "resulting_commit": None,
                            "scopes": {
                                "files": [],
                                "trees": [],
                                "project_files": False,
                                "backlog": False,
                                "all_files": False,
                                "file_domain": (
                                    "project_files"
                                    if case == "resource-file-domain"
                                    else "none"
                                ),
                                "resources": [resource],
                            },
                        }
                    )
                elif case == "malformed-journal-json":
                    pass
                else:
                    (candidate / ".git" / "agent-claims.json").write_text(
                        json.dumps({"claims": [{"claim_id": "retained"}]}) + "\n",
                        encoding="utf-8",
                    )
                if case != "active-registry":
                    serialized_events = "".join(
                        json.dumps(event) + "\n" for event in events
                    )
                    if case == "malformed-journal-json":
                        serialized_events += "{malformed\n"
                    journal.write_text(serialized_events, encoding="utf-8")

                with self.assertRaisesRegex(RuntimeError, diagnostic):
                    runner._audit_handoff_evidence(
                        (run,),
                        report,
                        sessions,
                        fixture_root,
                    )

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
        scenario = runner._load_yaml(_SUITE_ROOT / "scenarios.yaml")["scenarios"][0]
        scenario["fixtureContract"] = "fixture-contract.yaml"
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
            (root / "PROJECT.yaml").write_text(
                (
                    _SUITE_ROOT
                    / "fixtures"
                    / "dependency-routing"
                    / "PROJECT.yaml"
                ).read_text(encoding="utf-8"),
                encoding="utf-8",
            )
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
        for field in ("commit", "review", "verification"):
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
                    receipts = fabricated["runs"][0]["scenarioResults"][0]["handoffReceipts"]
                    lane = "integration" if field == "claimRelease" else "source"
                    mutate(next(receipt for receipt in receipts if receipt["lane"] == lane))
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
                candidate = (
                    fixture_root
                    / "dev-orchestrator"
                    / "dependency-routing"
                    / "candidate"
                )
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
                            "deliveryResult": {"status": "COMPLETED"},
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

    def test_delivery_result_controls_provider_closeout(self) -> None:
        """Only COMPLETED permits the retained closeout lane."""

        with tempfile.TemporaryDirectory() as directory:
            run, report, sessions, fixture_root = self._evidence_fixture(
                Path(directory),
                claim_release=False,
            )
            report["runs"][0]["scenarioResults"][0]["status"] = "PASS"
            runner._audit_handoff_evidence(
                (run,),
                report,
                sessions,
                fixture_root,
            )

            scenario_result = report["runs"][0]["scenarioResults"][0]
            invalid_cases = (
                (None, "missing the structured deliveryResult"),
                ({"status": "UNKNOWN"}, "unknown status"),
            )
            for delivery_result, diagnostic in invalid_cases:
                with self.subTest(delivery_result=delivery_result):
                    if delivery_result is None:
                        scenario_result.pop("deliveryResult", None)
                    else:
                        scenario_result["deliveryResult"] = delivery_result
                    with self.assertRaisesRegex(RuntimeError, diagnostic):
                        runner._audit_handoff_evidence(
                            (run,),
                            report,
                            sessions,
                            fixture_root,
                        )

            receipts = scenario_result["handoffReceipts"]
            closeout = next(
                receipt for receipt in receipts if receipt["lane"] == "closeout"
            )
            scenario_result["handoffReceipts"] = [
                receipt for receipt in receipts if receipt["lane"] != "closeout"
            ]
            for status in ("NEEDS_REVIEW", "BLOCKED"):
                with self.subTest(status=status):
                    scenario_result["status"] = "BLOCKED"
                    scenario_result["deliveryResult"] = {"status": status}
                    runner._audit_handoff_evidence(
                        (run,),
                        report,
                        sessions,
                        fixture_root,
                    )
                    scenario_result["handoffReceipts"].append(closeout)
                    with self.assertRaisesRegex(
                        RuntimeError,
                        "handoff receipt lanes mismatch",
                    ):
                        runner._audit_handoff_evidence(
                            (run,),
                            report,
                            sessions,
                            fixture_root,
                        )
                    scenario_result["handoffReceipts"].remove(closeout)

            scenario_result["deliveryResult"] = {"status": "COMPLETED"}
            scenario_result["status"] = "PASS"
            scenario_result["handoffReceipts"].append(closeout)

    @classmethod
    def _evidence_fixture(
        cls,
        temporary_root: Path,
        claim_release: bool = True,
    ) -> tuple[object, dict[str, object], tuple[object, ...], Path]:
        """Create a disposable candidate repository and retained dependency evidence."""
        run, report = cls._complete_dependency_routing_report()
        source_root = _SUITE_ROOT / "fixtures" / "dependency-routing"
        if claim_release:
            scenario = dict(run.suite.scenarios[0])
            scenario["targetSkills"] = [*scenario["targetSkills"], "agent-claim"]
            scenario["deterministicChecks"] = [
                *scenario["deterministicChecks"],
                "claim-lifecycle",
            ]
            contract = runner._load_yaml(source_root / "fixture-contract.yaml")
            contract["resourceCoordination"]["selected"] = "agent-claim"
            contract["handoffReceipt"]["requiredFields"] = contract[
                "resourceCoordination"
            ]["cases"]["agent-claim"]["requiredHandoffReceiptFields"]
            project = runner._load_yaml(source_root / "PROJECT.yaml")
            project["resource_coordination"]["selected"] = "agent-claim"
            suite_root = temporary_root / "suite-source"
            contract_root = suite_root / "fixtures" / "dependency-routing"
            contract_root.mkdir(parents=True)
            (contract_root / "fixture-contract.yaml").write_text(
                runner.yaml.safe_dump(contract, sort_keys=False),
                encoding="utf-8",
            )
            (contract_root / "PROJECT.yaml").write_text(
                runner.yaml.safe_dump(project, sort_keys=False),
                encoding="utf-8",
            )
            suite = runner._Suite(
                run.suite.suite_id,
                run.suite.priority,
                suite_root,
                run.suite.manifest,
                (scenario,),
            )
            run = runner._RunSpec(suite, run.scenario_ids)
        fixture_root = temporary_root / "fixtures"
        candidate = (
            fixture_root
            / "dev-orchestrator"
            / "dependency-routing"
            / "candidate"
        )
        candidate.mkdir(parents=True)
        subprocess.run(["git", "init", "--quiet"], cwd=candidate, check=True)
        subprocess.run(["git", "config", "user.name", "Fixture"], cwd=candidate, check=True)
        subprocess.run(["git", "config", "user.email", "fixture@example.invalid"], cwd=candidate, check=True)
        (candidate / "baseline.txt").write_text("baseline\n", encoding="utf-8")
        backlog_relative = "backlog/feature-backlog/update-dependency-health-summary.md"
        backlog_destination = candidate / backlog_relative
        backlog_destination.parent.mkdir(parents=True)
        backlog_destination.write_text(
            (source_root / backlog_relative).read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        subprocess.run(
            ["git", "add", "baseline.txt", backlog_relative],
            cwd=candidate,
            check=True,
        )
        subprocess.run(["git", "commit", "--quiet", "-m", "fixture baseline"], cwd=candidate, check=True)
        previous_sha = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=candidate,
            check=True,
            text=True,
            capture_output=True,
        ).stdout.strip()
        lane_mutations = {
            "source": {
                "src/dependency_status.py": "STATUS = 'healthy'\n",
                "tests/test_dependency_status.py": "def test_status():\n    assert True\n",
            },
            "documentation": {
                "docs/operator-runbook.md": "# Operator runbook\n",
            },
            "integration": {"integration.txt": "integrated\n"},
            "closeout": {backlog_relative: "Status: Complete\n"},
        }
        commit_evidence = {}
        for lane, mutations in lane_mutations.items():
            baseline_sha = previous_sha
            for relative, content in mutations.items():
                destination = candidate / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_text(content, encoding="utf-8")
            subprocess.run(
                ["git", "add", "--", *mutations],
                cwd=candidate,
                check=True,
            )
            subprocess.run(
                ["git", "commit", "--quiet", "-m", f"fixture {lane}"],
                cwd=candidate,
                check=True,
            )
            previous_sha = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=candidate,
                check=True,
                text=True,
                capture_output=True,
            ).stdout.strip()
            commit_evidence[lane] = (baseline_sha, previous_sha)
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
        events = []
        scopes = {
            "integration": {
                "files": [],
                "project_files": True,
                "file_domain": "project_files",
                "resources": [],
            },
            "closeout": {
                "files": [backlog_relative],
                "project_files": False,
                "file_domain": "backlog",
                "resources": [],
            },
        }
        claimed_lanes = {"integration", "closeout"}
        for lane, (role, review_ids, verification_ids) in evidence.items():
            baseline_sha, sha = commit_evidence[lane]
            event_id = f"release-{lane}"
            receipt = {
                "role": {"invocation": role, "sessionIds": [producer_session_ids[role]]},
                "commit": {"repository": "candidate", "sha": sha},
                "review": {"sessionIds": review_ids},
                "verification": {"sessionIds": verification_ids},
            }
            if claim_release and lane in claimed_lanes:
                receipt["claimRelease"] = {"eventIds": [event_id]}
                claim_id = f"{lane}-claim"
                event_scopes = {
                    "files": scopes[lane]["files"],
                    "trees": [],
                    "project_files": scopes[lane]["project_files"],
                    "backlog": False,
                    "all_files": False,
                    "file_domain": scopes[lane]["file_domain"],
                    "resources": scopes[lane]["resources"],
                }
                events.extend(
                    (
                        {
                            "schema_version": 1,
                            "action": "acquire",
                            "outcome": "PRIMARY",
                            "event_id": f"acquire-{lane}",
                            "claim_id": claim_id,
                            "agent": role,
                            "baseline_commit": baseline_sha,
                            "resulting_commit": None,
                            "scopes": event_scopes,
                        },
                        {
                            "schema_version": 1,
                            "action": "release",
                            "outcome": "RELEASED",
                            "event_id": event_id,
                            "claim_id": claim_id,
                            "agent": role,
                            "baseline_commit": baseline_sha,
                            "resulting_commit": sha,
                            "scopes": event_scopes,
                        },
                    )
                )
            receipt_by_lane[lane].update(receipt)
        if claim_release:
            event_root = candidate / ".git" / "agent-claim-events" / "hot"
            event_root.mkdir(parents=True)
            (event_root / "2026-07-19.jsonl").write_text(
                "".join(json.dumps(event) + "\n" for event in events),
                encoding="utf-8",
            )
            (candidate / ".git" / "agent-claims.json").write_text(
                json.dumps({"claims": []}) + "\n",
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
