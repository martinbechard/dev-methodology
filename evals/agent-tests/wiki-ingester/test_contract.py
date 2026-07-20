# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies Wiki Ingester continuation through the real verifier injection boundary.

from __future__ import annotations

import importlib.util
import inspect
import json
import os
import re
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path


SUITE_ROOT = Path(__file__).resolve().parent
REPOSITORY_ROOT = SUITE_ROOT.parents[2]


def _load_module(name: str, path: Path):
    """Load one suite helper from path under a stable isolated module name."""
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot load suite module: {path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


def _validate_control_result(
    test: unittest.TestCase, plan, result: dict[str, object]
) -> None:
    """Assert target-owned continuation and clean closeout for one live control."""
    process = result["process"]
    test.assertIsInstance(process, dict)
    test.assertEqual(0, process["exitCode"])
    terminal = str(result["targetTerminalResponse"])
    test.assertIn("READY", terminal)
    test.assertNotIn("BLOCKED", terminal)
    test.assertEqual("", result["gitStatus"])
    test.assertEqual([], result["liveRegistryClaims"])
    test.assertIs(result["retryRawSourcePresent"], False)
    test.assertIs(result["retryProcessedSourcePresent"], True)
    result_text = str(result["evaluationResultText"]).lower()
    test.assertIn("ready", result_text)
    test.assertIn("interrupt", result_text)
    test.assertIn("ingested conclusions", result_text)
    test.assertIn("open questions", result_text)
    test.assertNotIn("restor", result_text)
    expected = plan.outcomes()
    observed = [
        {
            "gate": outcome["gate"],
            "invocation": outcome["invocation"],
            "outcome": outcome["outcome"],
        }
        for outcome in result["verifierControlTrace"]
    ]
    expected_trace = [
        {
            "gate": outcome["gate"],
            "invocation": outcome["invocation"],
            "outcome": outcome["outcome"],
        }
        for outcome in expected
    ]
    test.assertEqual(expected_trace, observed)
    _validate_execution_ownership(test, result)
    test.assertEqual(len(expected), len(result["dependencySessionIds"]))
    expected_gates = [str(outcome["gate"]) for outcome in expected]
    test.assertEqual(len(expected_gates), len(result["dependencyAgentPaths"]))
    for index, (gate, agent_path, response, outcome) in enumerate(zip(
        expected_gates,
        result["dependencyAgentPaths"],
        result["dependencyResponses"],
        expected,
        strict=True,
    )):
        test.assertTrue(
            str(agent_path).endswith(
                f"/{gate.replace('-', '_')}_verifier_{outcome['invocation']}"
            )
        )
        receipt = json.loads(str(response))
        expected_keys = {
            "gate",
            "invocation",
            "outcome",
            "ownedTreeDigest",
            "changedPaths",
        }
        if outcome["outcome"] == "NEEDS_CORRECTION":
            expected_keys.add("finding")
        elif outcome["outcome"] == "VERIFIER_INTERRUPTED":
            expected_keys.update(
                {"unresolvedPoint", "missingEvidence", "provenance", "appropriatePage"}
            )
        test.assertEqual(expected_keys, set(receipt))
        test.assertEqual(gate, receipt["gate"])
        test.assertEqual(outcome["invocation"], receipt["invocation"])
        test.assertEqual(outcome["outcome"], receipt["outcome"])
        test.assertRegex(receipt["ownedTreeDigest"], r"^[0-9a-f]{64}$")
        test.assertIsInstance(receipt["changedPaths"], list)
        if receipt["outcome"] == "VERIFIER_INTERRUPTED":
            test.assertNotIn("GOOD", receipt.values())
            test.assertNotIn("NEEDS_CORRECTION", receipt.values())
            test.assertEqual(
                "docs/wiki/retry-policy/fixed-retry-backoff.md",
                receipt["appropriatePage"],
            )
            test.assertIn("deployment retry policy", receipt["missingEvidence"])
            test.assertEqual("raw/retry-policy.md#Backoff", receipt["provenance"])
        test.assertEqual(result["verifierControlTrace"][index], receipt)
    trace_digests = [outcome["ownedTreeDigest"] for outcome in result["verifierControlTrace"]]
    test.assertNotEqual(result["initialOwnedTreeDigest"], trace_digests[0])
    for previous, current in zip(trace_digests, trace_digests[1:]):
        test.assertNotEqual(previous, current)
    for outcome in result["verifierControlTrace"]:
        changed_paths = outcome["changedPaths"]
        for path in changed_paths:
            allowed = str(path).startswith("docs/wiki/")
            if outcome["gate"] == "post-move":
                allowed = allowed or str(path) in {
                    "raw/retry-policy.md",
                    "raw/processed/retry-policy.md",
                }
            test.assertTrue(allowed, path)
    test.assertNotEqual(result["initialOwnedTreeDigest"], result["finalOwnedTreeDigest"])
    test.assertNotEqual(trace_digests[-1], result["finalOwnedTreeDigest"])
    committed_paths = set(result["committedPaths"])
    test.assertIn("eval-result.md", committed_paths)
    test.assertIn("raw/retry-policy.md", committed_paths)
    test.assertIn("raw/processed/retry-policy.md", committed_paths)
    retry_pages = {
        path: content
        for path, content in result["wikiContent"].items()
        if path.startswith("docs/wiki/retry-policy/")
    }
    test.assertTrue(retry_pages)
    test.assertTrue(set(retry_pages).issubset(committed_paths))
    open_question_pages = [
        (path, content.lower())
        for path, content in retry_pages.items()
        if "deployment" in content.lower()
        and "jitter" in content.lower()
        and "missing" in content.lower()
        and "## open questions" in content.lower()
    ]
    test.assertEqual(1, len(open_question_pages))
    open_question_path, open_question_text = open_question_pages[0]
    test.assertEqual(
        "docs/wiki/retry-policy/fixed-retry-backoff.md",
        open_question_path,
    )
    test.assertIn("raw/processed/retry-policy.md", open_question_text)
    test.assertIn(str(result["head"]), terminal)
    test.assertIn("RELEASED", terminal.upper())
    test.assertIn("CLEAN", terminal.upper())
    _validate_claim_events(test, result, terminal)


def _validate_execution_ownership(
    test: unittest.TestCase, result: dict[str, object]
) -> None:
    """Prove launcher and injected verifiers cannot perform target lifecycle work."""
    test.assertIn(
        result["targetInstructionMarker"],
        result["targetInstructionMarkers"],
    )
    root_calls = result["rootToolCalls"]
    test.assertIsInstance(root_calls, list)
    test.assertEqual(1, sum(call["name"] == "spawn_agent" for call in root_calls))
    test.assertTrue(all(call["name"] in {"spawn_agent", "wait_agent"} for call in root_calls))
    spawn = next(call for call in root_calls if call["name"] == "spawn_agent")
    spawn_arguments = json.loads(spawn["arguments"])
    test.assertEqual("wiki_ingester", spawn_arguments["agent_type"])
    test.assertTrue(
        spawn_arguments.get("fork_context") is False
        or spawn_arguments.get("fork_turns") == "none"
    )
    dependency_calls = result["dependencyToolCalls"]
    test.assertEqual(len(result["dependencySessionIds"]), len(dependency_calls))
    dependency_requests = result["dependencyRequests"]
    test.assertEqual(len(dependency_calls), len(dependency_requests))
    target_spawns = []
    for call in result["targetToolCalls"]:
        if call["name"] != "spawn_agent":
            continue
        arguments = json.loads(call["arguments"])
        if arguments.get("agent_type") == "wiki_topic_verifier":
            target_spawns.append(arguments)
    test.assertEqual(len(dependency_calls), len(target_spawns))
    for index, calls in enumerate(dependency_calls):
        test.assertEqual(1, len(calls))
        test.assertEqual("exec", calls[0]["name"])
        arguments = calls[0]["arguments"]
        test.assertEqual(["exec_command"], re.findall(r"tools\.([a-z_]+)", arguments))
        command_literals = re.findall(
            r'cmd\s*:\s*("(?:\\.|[^"\\])*")', arguments
        )
        test.assertEqual(1, len(command_literals))
        test.assertEqual(result["verifierDriverCommand"], json.loads(command_literals[0]))
        request_messages = dependency_requests[index]
        test.assertIsInstance(request_messages, list)
        test.assertTrue(request_messages)
        request = "\n".join(request_messages)
        trace = result["verifierControlTrace"][index]
        test.assertIn(result["repositoryPath"], request)
        test.assertIn(str(trace["gate"]), request.lower())
        test.assertIn("lint", request.lower())
        expected_source = (
            "raw/retry-policy.md"
            if trace["gate"] == "pre-move"
            else "raw/processed/retry-policy.md"
        )
        test.assertIn(expected_source, request)
        for path in trace["changedPaths"]:
            if str(path).startswith("docs/wiki/"):
                test.assertIn(path, request)
        spawn_arguments = target_spawns[index]
        test.assertTrue(
            spawn_arguments.get("fork_context") is False
            or spawn_arguments.get("fork_turns") == "none"
        )


def _validate_claim_events(
    test: unittest.TestCase, result: dict[str, object], terminal: str
) -> None:
    """Bind one successful acquisition and release receipt to the target commit."""
    claim_events = result["claimEvents"]
    test.assertIsInstance(claim_events, list)
    acquisitions = [
        event
        for event in claim_events
        if event.get("action") == "acquire" and event.get("outcome") == "PRIMARY"
    ]
    releases = [
        event
        for event in claim_events
        if event.get("action") == "release" and event.get("outcome") == "RELEASED"
    ]
    test.assertEqual(1, len(acquisitions))
    test.assertEqual(1, len(releases))
    acquisition = acquisitions[0]
    release = releases[0]
    test.assertTrue(acquisition["agent"].replace("_", "-").endswith("wiki-ingester"))
    test.assertEqual(acquisition["agent"], release["agent"])
    test.assertEqual(acquisition["claim_id"], release["claim_id"])
    test.assertEqual(result["head"], release["resulting_commit"])
    test.assertIn(release["event_id"], terminal)
    release_events = result["releaseEvents"]
    test.assertIn(release["event_id"], release_events)
    test.assertEqual(release, release_events[release["event_id"]])


class WikiIngesterTargetBoundaryTests(unittest.TestCase):
    """Protect the actual adapter path and all six injected interruption positions."""

    @classmethod
    def setUpClass(cls) -> None:
        """Load the executable boundary once for deterministic contract checks."""
        cls.harness = _load_module(
            "wiki_ingester_executable_harness",
            SUITE_ROOT / "executable_harness.py",
        )
        cls.fixture = _load_module(
            "wiki_ingester_stage_fixture",
            SUITE_ROOT / "fixtures" / "stage_fixture.py",
        )

    def test_all_bounded_interruption_plans_are_sequential_and_terminal(self) -> None:
        """Every gate interrupts initially or after either allowed correction."""
        observed = []
        for gate in ("pre-move", "post-move"):
            for interruption in range(3):
                with self.subTest(gate=gate, interruption=interruption):
                    plan = self.harness.VerifierPlan(gate, interruption)
                    outcomes = plan.outcomes()
                    observed.append((gate, interruption))
                    self.assertEqual("VERIFIER_INTERRUPTED", outcomes[-1]["outcome"])
                    self.assertEqual(gate, outcomes[-1]["gate"])
                    self.assertEqual(interruption, outcomes[-1]["invocation"])
                    self.assertEqual(
                        "docs/wiki/retry-policy/fixed-retry-backoff.md",
                        outcomes[-1]["appropriatePage"],
                    )
                    self.assertIn("missingEvidence", outcomes[-1])
                    self.assertIn("provenance", outcomes[-1])
                    gate_outcomes = outcomes[1:] if gate == "post-move" else outcomes
                    self.assertEqual(interruption + 1, len(gate_outcomes))
                    self.assertTrue(
                        all(
                            outcome["outcome"] == "NEEDS_CORRECTION"
                            for outcome in gate_outcomes[:-1]
                        )
                    )
                    self.assertTrue(
                        all(
                            str(outcome["finding"]).startswith("docs/wiki/retry-policy/")
                            for outcome in gate_outcomes[:-1]
                        )
                    )
        self.assertEqual(6, len(observed))

    def test_runtime_binds_canonical_target_and_only_injects_dependency(self) -> None:
        """The canonical target instructions are bound while only its verifier is replaced."""
        plan = self.harness.VerifierPlan("pre-move", 1)
        with tempfile.TemporaryDirectory() as temporary:
            layout = self.harness.stage_runtime(Path(temporary), plan)
            target, dependency = layout.staged_agents
            self.assertEqual(self.harness.NATIVE_ADAPTER, target.source)
            self.assertEqual("wiki_ingester", target.invocation)
            self.assertEqual(
                self.harness.NATIVE_ADAPTER.read_text(encoding="utf-8"),
                layout.target_source.read_text(encoding="utf-8"),
            )
            self.assertEqual("wiki_topic_verifier", dependency.invocation)
            self.assertEqual(layout.control_root, dependency.source.parent)
            self.assertNotEqual(target.source, dependency.source)
            staged_target = layout.codex_home / "agents/wiki_ingester.toml"
            self.assertTrue(staged_target.is_file())
            canonical = tomllib.loads(
                self.harness.NATIVE_ADAPTER.read_text(encoding="utf-8")
            )
            canonical_instructions = canonical["developer_instructions"]
            for phrase in (
                "every substantiated claim and relationship",
                "Open Questions section of the most relevant page",
                "not a NEEDS_CORRECTION verdict",
                "Verifier interruption alone is not a BLOCKED condition",
                "distinguishes ingested conclusions from recorded open questions",
            ):
                with self.subTest(canonical_phrase=phrase):
                    self.assertIn(phrase, canonical_instructions)
            staged = tomllib.loads(staged_target.read_text(encoding="utf-8"))
            self.assertEqual(
                canonical_instructions,
                target.developer_instructions,
            )
            self.assertIn(canonical_instructions, staged["developer_instructions"])
            self.assertIn(target.instruction_marker, staged["developer_instructions"])

    def test_claim_validator_rejects_prose_without_journal_receipts(self) -> None:
        """An empty registry and claimed RELEASED prose cannot replace journal evidence."""
        result = {
            "claimEvents": [],
            "releaseEvents": {},
            "head": "a" * 40,
        }
        with self.assertRaises(AssertionError):
            _validate_claim_events(self, result, "RELEASED with a clean registry")

    def test_live_validator_accepts_continuation_trace_shape(self) -> None:
        """A correction followed by interruption retains target-owned ingest evidence."""
        plan = self.harness.VerifierPlan("pre-move", 1)
        trace = [
            {
                **outcome,
                "ownedTreeDigest": character * 64,
                "changedPaths": ["docs/wiki/retry-policy/example.md"],
            }
            for outcome, character in zip(plan.outcomes(), ("a", "b"), strict=True)
        ]
        head = "c" * 40
        release_id = "release-event"
        claim_id = "wiki-ingester-control"
        acquisition = {
            "action": "acquire",
            "outcome": "PRIMARY",
            "agent": "wiki_ingester",
            "claim_id": claim_id,
            "event_id": "acquire-event",
        }
        release = {
            "action": "release",
            "outcome": "RELEASED",
            "agent": "wiki_ingester",
            "claim_id": claim_id,
            "event_id": release_id,
            "resulting_commit": head,
        }
        result = {
            "process": {"exitCode": 0},
            "targetInstructionMarker": "target-marker",
            "targetInstructionMarkers": ["target-marker"],
            "rootToolCalls": [
                {
                    "name": "spawn_agent",
                    "arguments": '{"agent_type":"wiki_ingester","fork_context":false}',
                },
                {"name": "wait_agent", "arguments": "{}"},
            ],
            "verifierDriverPath": "/control/next_verdict.py",
            "verifierDriverCommand": "/python /control/next_verdict.py",
            "repositoryPath": "/fixture",
            "targetToolCalls": [
                {
                    "name": "spawn_agent",
                    "arguments": '{"agent_type":"wiki_topic_verifier","fork_turns":"none"}',
                },
                {
                    "name": "spawn_agent",
                    "arguments": '{"agent_type":"wiki_topic_verifier","fork_turns":"none"}',
                },
            ],
            "dependencyToolCalls": [
                [
                    {
                        "name": "exec",
                        "arguments": 'const r=await tools.exec_command({cmd:"/python /control/next_verdict.py"}); text(r.output);',
                    }
                ],
                [
                    {
                        "name": "exec",
                        "arguments": 'const r=await tools.exec_command({cmd:"/python /control/next_verdict.py"}); text(r.output);',
                    }
                ],
            ],
            "dependencyRequests": [
                [
                    "/fixture pre-move raw/retry-policy.md lint "
                    "docs/wiki/retry-policy/example.md"
                ],
                [
                    "/fixture pre-move raw/retry-policy.md lint "
                    "docs/wiki/retry-policy/example.md"
                ],
            ],
            "targetTerminalResponse": f"READY {head} {release_id} RELEASED CLEAN",
            "gitStatus": "",
            "liveRegistryClaims": [],
            "retryRawSourcePresent": False,
            "retryProcessedSourcePresent": True,
            "evaluationResultText": (
                "READY interruption; ingested conclusions; recorded open questions"
            ),
            "verifierControlTrace": trace,
            "dependencySessionIds": ["verifier-0", "verifier-1"],
            "dependencyAgentPaths": [
                "/root/wiki_ingester/pre_move_verifier_0",
                "/root/wiki_ingester/pre_move_verifier_1",
            ],
            "dependencyResponses": [json.dumps(receipt) for receipt in trace],
            "initialOwnedTreeDigest": "d" * 64,
            "finalOwnedTreeDigest": "e" * 64,
            "committedPaths": [
                "docs/wiki/retry-policy/fixed-retry-backoff.md",
                "eval-result.md",
                "raw/processed/retry-policy.md",
                "raw/retry-policy.md",
            ],
            "wikiContent": {
                "docs/wiki/retry-policy/fixed-retry-backoff.md": (
                    "## Open Questions\n\n"
                    "- Deployment jitter is unresolved; missing authoritative deployment "
                    "retry policy evidence. Provenance: raw/processed/retry-policy.md.\n"
                )
            },
            "head": head,
            "claimEvents": [acquisition, release],
            "releaseEvents": {release_id: release},
        }
        _validate_control_result(self, plan, result)
        result["rootToolCalls"].append(
            {"name": "exec", "arguments": "git commit -am repair"}
        )
        with self.assertRaises(AssertionError):
            _validate_execution_ownership(self, result)
        result["rootToolCalls"].pop()
        original_arguments = result["dependencyToolCalls"][0][0]["arguments"]
        result["dependencyToolCalls"][0][0]["arguments"] = original_arguments.replace(
            "/control/next_verdict.py",
            "/control/next_verdict.py; git add docs/wiki",
        )
        with self.assertRaises(AssertionError):
            _validate_execution_ownership(self, result)
        result["dependencyToolCalls"][0][0]["arguments"] = original_arguments
        result["verifierControlTrace"][1]["ownedTreeDigest"] = "a" * 64
        result["dependencyResponses"][1] = json.dumps(
            result["verifierControlTrace"][1]
        )
        with self.assertRaises(AssertionError):
            _validate_control_result(self, plan, result)

    def test_verifier_driver_inventories_untracked_and_tracked_changes(self) -> None:
        """Verifier-time paths include new leaves as well as tracked modifications."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            destination = root / "fixture"
            self.harness._initialize_repository(destination, "raw-ingest")
            layout = self.harness.stage_runtime(
                root / "runtime",
                self.harness.VerifierPlan("pre-move", 0),
            )
            new_page = destination / "docs/wiki/retry-policy/new-leaf.md"
            new_page.parent.mkdir(parents=True)
            new_page.write_text("# New leaf\n", encoding="utf-8")
            tracked = destination / "docs/wiki/topic-index.md"
            tracked.write_text(
                tracked.read_text(encoding="utf-8") + "\nchanged\n",
                encoding="utf-8",
            )
            completed = self.harness._run(
                [sys.executable, str(layout.control_root / "next_verdict.py")],
                destination,
            )
            receipt = json.loads(completed.stdout)
            self.assertIn(
                "docs/wiki/retry-policy/new-leaf.md", receipt["changedPaths"]
            )
            self.assertIn("docs/wiki/topic-index.md", receipt["changedPaths"])

    def test_boundary_observes_but_never_repairs_target_lifecycle(self) -> None:
        """Execution and observation contain no target mutation or closeout helper."""
        source = "\n".join(
            (
                inspect.getsource(self.harness.run_control),
                inspect.getsource(self.harness._observe_target_result),
            )
        )
        for prohibited in (
            "git\", \"add",
            "git\", \"commit",
            "release\", \"--claim-id",
            "def _claim(",
            "def _closeout(",
            "class GeneratedWikiIngesterTarget",
        ):
            with self.subTest(prohibited=prohibited):
                self.assertNotIn(prohibited, source)

    def test_raw_ingest_collision_and_verifier_fixtures_preserve_boundaries(self) -> None:
        """All focused Wiki Ingester scenarios stage their distinct queue boundary."""
        expectations = {
            "raw-ingest": (
                ("raw/retry-policy.md", True),
                ("raw/processed/retry-policy.md", False),
            ),
            "destination-collision": (
                ("raw/provider.md", True),
                ("raw/processed/provider.md", True),
            ),
            "verifier-failure": (
                ("raw/provider-routing.md", True),
                ("raw/processed/provider-routing.md", False),
            ),
        }
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for scenario, paths in expectations.items():
                with self.subTest(scenario=scenario):
                    destination = root / scenario
                    self.fixture.stage_fixture(scenario, destination)
                    for relative, expected in paths:
                        self.assertEqual(expected, (destination / relative).is_file())


@unittest.skipUnless(
    os.environ.get("WIKI_INGESTER_LIVE_CONTROL") == "1",
    "set WIKI_INGESTER_LIVE_CONTROL=1 for actual adapter controls",
)
class WikiIngesterLiveInterruptionTests(unittest.TestCase):
    """Run the canonical Wiki Ingester through every forced interruption point."""

    @classmethod
    def setUpClass(cls) -> None:
        """Load the real executable boundary once for opt-in live controls."""
        cls.harness = _load_module(
            "wiki_ingester_live_executable_harness",
            SUITE_ROOT / "executable_harness.py",
        )

    def test_target_continues_and_closes_every_interruption(self) -> None:
        """Each injected non-verdict preserves supported content and closes cleanly."""
        for gate in ("pre-move", "post-move"):
            for interruption in range(3):
                with self.subTest(gate=gate, interruption=interruption):
                    with tempfile.TemporaryDirectory() as temporary:
                        plan = self.harness.VerifierPlan(gate, interruption)
                        result = self.harness.run_control(
                            plan,
                            Path(temporary) / "fixture",
                        )
                        _validate_control_result(self, plan, result)


@unittest.skipUnless(
    os.environ.get("WIKI_INGESTER_LIVE_NEIGHBORS") == "1",
    "set WIKI_INGESTER_LIVE_NEIGHBORS=1 for raw-ingest and collision controls",
)
class WikiIngesterLiveNeighborTests(unittest.TestCase):
    """Run canonical raw-ingest and collision behavior beside interruption controls."""

    @classmethod
    def setUpClass(cls) -> None:
        """Load the executable target boundary once for both neighboring scenarios."""
        cls.harness = _load_module(
            "wiki_ingester_neighbor_executable_harness",
            SUITE_ROOT / "executable_harness.py",
        )

    def test_raw_ingest_reaches_both_good_gates_and_closes_cleanly(self) -> None:
        """Normal ingest moves the source only after both target-owned verifier gates."""
        with tempfile.TemporaryDirectory() as temporary:
            result = self.harness.run_neighbor_control(
                "raw-ingest", Path(temporary) / "fixture"
            )
            self.assertEqual(0, result["process"]["exitCode"])
            self.assertIn("READY", result["targetTerminalResponse"])
            self.assertNotIn("raw/retry-policy.md", result["queueFiles"])
            self.assertIn("raw/processed/retry-policy.md", result["queueFiles"])
            self.assertEqual("", result["gitStatus"])
            self.assertEqual([], result["liveRegistryClaims"])
            self.assertEqual(3, len(result["dependencySessionIds"]))
            _validate_execution_ownership(self, result)
            expected = (
                ("pre-move", 0, "NEEDS_CORRECTION"),
                ("pre-move", 1, "GOOD"),
                ("post-move", 0, "GOOD"),
            )
            for index, ((gate, invocation, outcome), agent_path, response) in enumerate(zip(
                expected,
                result["dependencyAgentPaths"],
                result["dependencyResponses"],
                strict=True,
            )):
                self.assertTrue(
                    agent_path.endswith(
                        f"/{gate.replace('-', '_')}_verifier_{invocation}"
                    )
                )
                receipt = json.loads(response)
                self.assertEqual(gate, receipt["gate"])
                self.assertEqual(invocation, receipt["invocation"])
                self.assertEqual(outcome, receipt["outcome"])
                self.assertEqual(result["verifierControlTrace"][index], receipt)
            trace_digests = [
                outcome["ownedTreeDigest"]
                for outcome in result["verifierControlTrace"]
            ]
            self.assertNotEqual(result["initialOwnedTreeDigest"], trace_digests[0])
            for previous, current in zip(trace_digests, trace_digests[1:]):
                self.assertNotEqual(previous, current)
            self.assertIn("raw/processed/retry-policy.md", result["committedPaths"])
            self.assertIn("eval-result.md", result["committedPaths"])
            retry_pages = [
                path
                for path in result["wikiFiles"]
                if "retry" in path
                and path not in {
                    "docs/wiki/digests/2026-07.md",
                    "docs/wiki/topic-index.md",
                }
            ]
            self.assertGreaterEqual(len(retry_pages), 2)
            self.assertIn("docs/wiki/digests/2026-07.md", result["wikiFiles"])
            self.assertIn("docs/wiki/topic-index.md", result["wikiFiles"])
            for path in (
                "docs/wiki/digests/2026-07.md",
                "docs/wiki/topic-index.md",
            ):
                content = result["wikiContent"][path].lower()
                self.assertIn("retry", content)
                self.assertIn(path, result["committedPaths"])
            for path in retry_pages:
                self.assertIn(path, result["committedPaths"])
            result_text = result["evaluationResultText"].lower()
            for evidence in (
                "ready",
                "pre-move",
                "post-move",
                "needs_correction",
                "lint",
                "okf",
                "processed",
            ):
                self.assertIn(evidence, result_text)
            self.assertIn(str(result["head"]), result["targetTerminalResponse"])
            _validate_claim_events(self, result, result["targetTerminalResponse"])

    def test_collision_preserves_both_sources_without_verifier_mutation(self) -> None:
        """A destination collision keeps both source bytes and closes as clean BLOCKED."""
        with tempfile.TemporaryDirectory() as temporary:
            result = self.harness.run_neighbor_control(
                "destination-collision", Path(temporary) / "fixture"
            )
            self.assertEqual(0, result["process"]["exitCode"])
            self.assertIn("BLOCKED", result["targetTerminalResponse"])
            self.assertIn("raw/provider.md", result["queueFiles"])
            self.assertIn("raw/processed/provider.md", result["queueFiles"])
            self.assertEqual(
                result["initialOwnedTreeDigest"], result["finalOwnedTreeDigest"]
            )
            self.assertEqual([], result["dependencySessionIds"])
            self.assertEqual("", result["gitStatus"])
            self.assertEqual([], result["liveRegistryClaims"])
            _validate_execution_ownership(self, result)
            self.assertEqual(["eval-result.md"], result["committedPaths"])
            result_text = result["evaluationResultText"].lower()
            for evidence in (
                "blocked",
                "collision",
                "naming",
                "disposition",
                "no-product-change",
                "unchanged",
            ):
                self.assertIn(evidence, result_text)
            self.assertIn(str(result["head"]), result["targetTerminalResponse"])
            _validate_claim_events(self, result, result["targetTerminalResponse"])


if __name__ == "__main__":
    unittest.main()
