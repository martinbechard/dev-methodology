# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies Wiki Ingester continuation through the real verifier injection boundary.

from __future__ import annotations

import importlib.util
import inspect
import json
import os
import re
import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path


SUITE_ROOT = Path(__file__).resolve().parent
REPOSITORY_ROOT = SUITE_ROOT.parents[2]
RETAINED_REPLAY_PATH = SUITE_ROOT / "fixtures" / "retained-evaluator-replay.json"
CORRECTION_EXPECTATIONS = (
    (
        "docs/wiki/retry-policy/request-eligibility.md",
        "## Ineligible mutation requests",
        "Order creation, cancellation, and payment mutation requests are never retried.",
    ),
    (
        "docs/wiki/retry-policy/retry-execution.md",
        "## Retry delay sequence",
        "The first retry waits 200 milliseconds and the second retry waits 500 milliseconds.",
    ),
)
CONCLUSION_INVENTORY_LABEL = (
    r"(?:(?:ingested|substantiated|supported)\s+"
    r"|(?:preserved|retained)\s+(?:substantiated|supported)\s+)"
    r"(?:conclusions?|content|facts|knowledge)"
)
OPEN_QUESTION_INVENTORY_LABEL = (
    r"(?:(?:recorded|retained|preserved|page-local)\s+)*"
    r"(?:open\s+questions?|unresolved\s+(?:questions?|points?|uncertaint(?:y|ies)))"
)
MISSING_EVIDENCE_PATTERN = (
    r"missing evidence|no .{0,80}evidence|lacks?.{0,80}evidence"
    r"|neither .{0,80} nor .{0,80} evidence"
    r"|authoritative.{0,80}evidence.{0,40}"
    r"(?:missing|absent|unavailable|not (?:been )?(?:identified|found|available))"
)
LIVE_CASE_SELECTOR_ENV = "WIKI_INGESTER_LIVE_CASES"
FOCUSED_LIVE_CASES = frozenset({"pre0", "raw-ingest"})


def _load_module(name: str, path: Path):
    """Load one suite helper from path under a stable isolated module name."""
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot load suite module: {path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


def _extract_single_exec_command(arguments: str) -> str:
    """Return the one literal command from a verifier's sole exec_command call."""
    tool_calls = re.findall(r"tools\.([a-z_]+)", arguments)
    if tool_calls != ["exec_command"]:
        raise ValueError(f"expected one exec_command call, observed {tool_calls}")
    call_objects = re.findall(
        r"tools\.exec_command\(\s*\{(.*?)\}\s*\)",
        arguments,
        flags=re.DOTALL,
    )
    if len(call_objects) != 1:
        raise ValueError(
            f"expected one literal exec_command object, observed {len(call_objects)}"
        )
    command_literals = re.findall(
        r'(?:^|,)\s*(?:"cmd"|cmd)\s*:\s*("(?:\\.|[^"\\])*")',
        call_objects[0],
    )
    if len(command_literals) != 1:
        raise ValueError(
            f"expected one quoted cmd value, observed {len(command_literals)}"
        )
    command = json.loads(command_literals[0])
    if not isinstance(command, str):
        raise ValueError("cmd value must decode to a string")
    return command


def _labeled_inventory(result_text: str, label_pattern: str) -> str:
    """Return entries beneath one Markdown heading or labeled inventory line."""
    lines = result_text.splitlines()
    label = re.compile(
        rf"^(?:[-*]\s*)?(?:#{{1,6}}\s*)?{label_pattern}\s*:?\s*(.*)$",
        flags=re.IGNORECASE,
    )
    any_inventory = re.compile(
        rf"^(?:[-*]\s*)?(?:#{{1,6}}\s*)?(?:{CONCLUSION_INVENTORY_LABEL})"
        rf"|^(?:[-*]\s*)?(?:#{{1,6}}\s*)?(?:{OPEN_QUESTION_INVENTORY_LABEL})",
        flags=re.IGNORECASE,
    )
    entries: list[str] = []
    for index, line in enumerate(lines):
        matched = label.match(line.strip())
        if matched is None:
            continue
        if matched.group(1):
            entries.append(matched.group(1))
        for following in lines[index + 1:]:
            stripped = following.strip()
            if re.match(r"^#{1,6}\s+", stripped) or any_inventory.match(stripped):
                break
            if stripped:
                entries.append(stripped)
    return "\n".join(entries).lower()


def _assert_result_inventory(test: unittest.TestCase, result_text: str) -> None:
    """Require distinct conclusion and open-question entries with fixture facts."""
    conclusions = _labeled_inventory(
        result_text,
        CONCLUSION_INVENTORY_LABEL,
    )
    open_questions = _labeled_inventory(
        result_text,
        OPEN_QUESTION_INVENTORY_LABEL,
    )
    _assert_inventory_scope(test, conclusions)
    _assert_inventory_scope(test, open_questions)
    _assert_fact_bearing_conclusion_bullet(test, conclusions)
    with test.subTest(result_inventory="conclusion-entry-present"):
        test.assertTrue(conclusions)
    with test.subTest(result_inventory="conclusion-retry-delays"):
        test.assertIn("200", conclusions)
        test.assertIn("500", conclusions)
    with test.subTest(result_inventory="conclusion-retry-boundary"):
        test.assertRegex(
            conclusions,
            r"(?:idempotent|order.status|mutation requests?.{0,40}(?:never|not) retr)",
        )
    with test.subTest(result_inventory="open-question-entry-present"):
        test.assertTrue(open_questions)
    with test.subTest(result_inventory="open-question-jitter"):
        test.assertIn("jitter", open_questions)
    with test.subTest(result_inventory="open-question-missing-evidence"):
        test.assertRegex(
            open_questions,
            MISSING_EVIDENCE_PATTERN,
        )
    with test.subTest(result_inventory="open-question-provenance"):
        test.assertIn("raw/processed/retry-policy.md", open_questions)


def _assert_inventory_scope(test: unittest.TestCase, inventory: str) -> None:
    """Require page and source scope, with stricter wording for an explicit None."""
    normalized = " ".join(inventory.lower().split())
    test.assertTrue(normalized)
    if re.search(r"(?:^|\n)\s*[-*]?\s*none\s*[.:;]", inventory, re.IGNORECASE):
        test.assertRegex(normalized, r"assessed source.{0,80}raw/")
        test.assertRegex(normalized, r"assessed page scope.{0,80}docs/wiki")
        return
    test.assertIn("raw/", normalized)
    test.assertIn("docs/wiki/", normalized)


def _assert_fact_bearing_conclusion_bullet(
    test: unittest.TestCase, conclusions: str
) -> None:
    """Require one conclusion bullet that binds fact, page, and source evidence."""
    bullets = [
        line.lower()
        for line in conclusions.splitlines()
        if re.match(r"^[-*]\s+", line.strip())
    ]
    test.assertTrue(
        any("docs/wiki/" in bullet and "raw/" in bullet for bullet in bullets)
    )


def _inventory_entries(inventory: str) -> list[str]:
    """Split an inventory into bullets or separately invalid prose entries."""
    entries: list[str] = []
    current: list[str] = []
    for line in inventory.splitlines():
        stripped = line.strip()
        if not stripped:
            if current:
                entries.append("\n".join(current))
                current = []
            continue
        if re.match(r"^[-*]\s+", stripped):
            if current:
                entries.append("\n".join(current))
            current = [stripped]
        elif current:
            current.append(stripped)
        else:
            entries.append(stripped)
    if current:
        entries.append("\n".join(current))
    return entries


def _assert_fact_bearing_inventory_entries(
    test: unittest.TestCase, inventory: str
) -> None:
    """Require every non-None entry to be a fact-bearing page/source bullet."""
    entries = _inventory_entries(inventory)
    test.assertTrue(entries)
    for entry in entries:
        normalized = " ".join(entry.lower().split())
        test.assertRegex(entry, r"^[-*]\s+")
        test.assertIn("docs/wiki/", normalized)
        test.assertIn("raw/", normalized)
        test.assertRegex(normalized, r":\s*\S")


def _assert_terminal_result_readback(
    test: unittest.TestCase,
    result_text: str,
    substantiated_content_written: bool,
) -> None:
    """Require literal on-disk inventories with bullets or one scoped None entry."""
    sections = {}
    for heading in ("Substantiated Conclusions", "Open Questions"):
        matches = re.findall(
            rf"^## {re.escape(heading)}\s*$",
            result_text,
            flags=re.MULTILINE,
        )
        test.assertEqual(1, len(matches))
        section = _markdown_section(result_text, heading)
        test.assertTrue(section)
        sections[heading] = section

    conclusions = sections["Substantiated Conclusions"]
    conclusion_is_none = re.search(
        r"(?:^|\n)\s*[-*]\s+none\s*[.:;]",
        conclusions,
        flags=re.IGNORECASE,
    ) is not None
    if conclusion_is_none:
        test.assertIs(substantiated_content_written, False)
        _assert_single_scoped_none_entry(test, conclusions)
    else:
        _assert_fact_bearing_inventory_entries(test, conclusions)

    open_questions = sections["Open Questions"]
    open_questions_is_none = re.search(
        r"(?:^|\n)\s*[-*]\s+none\s*[.:;]",
        open_questions,
        flags=re.IGNORECASE,
    ) is not None
    if open_questions_is_none:
        _assert_single_scoped_none_entry(test, open_questions)
    else:
        _assert_fact_bearing_inventory_entries(test, open_questions)


def _assert_single_scoped_none_entry(
    test: unittest.TestCase, inventory: str
) -> None:
    """Require exactly one explicit None entry with assessed source and page scope."""
    entries = _inventory_entries(inventory)
    test.assertEqual(1, len(entries))
    entry_start = entries[0]
    test.assertRegex(entry_start, r"^[-*]\s+")
    test.assertIsNotNone(
        re.search(r"^[-*]\s+none\s*[.:;]", entry_start, re.IGNORECASE)
    )
    _assert_inventory_scope(test, inventory)


def _markdown_section(page_text: str, heading: str) -> str:
    """Return one level-two Markdown section body without adjacent sections."""
    matched = re.search(
        rf"(?im)^##\s+{re.escape(heading)}\s*$",
        page_text,
    )
    if matched is None:
        return ""
    remainder = page_text[matched.end():]
    next_heading = re.search(r"(?m)^##\s+", remainder)
    return remainder[: next_heading.start() if next_heading else None].strip()


def _canonical_runtime_path(path: str) -> str:
    """Canonicalize runtime paths while collapsing the macOS /private/var alias."""
    canonical = os.path.realpath(path)
    if canonical == "/private/var" or canonical.startswith("/private/var/"):
        return canonical.removeprefix("/private")
    return canonical


def _contains_missing_evidence(text: str) -> bool:
    """Return whether text semantically identifies absent authoritative evidence."""
    return re.search(
        MISSING_EVIDENCE_PATTERN,
        text,
        flags=re.IGNORECASE | re.DOTALL,
    ) is not None


def _contains_correction_attempt_count(text: str) -> bool:
    """Return whether text reports the two allowed correction attempts."""
    return re.search(
        r"(?:two|2)(?:\s+genuine)?\s+correction attempts",
        text,
        flags=re.IGNORECASE,
    ) is not None


def _parse_live_case_selector(value: str | None) -> frozenset[str] | None:
    """Parse the exact portable selector for the approved focused live rerun."""
    if value is None:
        return None
    if not value or value.strip() != value:
        raise ValueError(f"invalid {LIVE_CASE_SELECTOR_ENV}: {value!r}")
    cases = value.split(",")
    if any(not case or case.strip() != case for case in cases):
        raise ValueError(f"invalid {LIVE_CASE_SELECTOR_ENV}: {value!r}")
    if len(cases) != len(set(cases)):
        raise ValueError(f"duplicate {LIVE_CASE_SELECTOR_ENV}: {value!r}")
    selected = frozenset(cases)
    unknown = selected - FOCUSED_LIVE_CASES
    if unknown:
        raise ValueError(
            f"unsupported {LIVE_CASE_SELECTOR_ENV}: {', '.join(sorted(unknown))}"
        )
    return selected


def _selected_live_cases() -> frozenset[str] | None:
    """Return the optional focused live selection from the environment."""
    return _parse_live_case_selector(os.environ.get(LIVE_CASE_SELECTOR_ENV))


def _assert_collision_no_change(
    test: unittest.TestCase, result_text: str
) -> None:
    """Require a collision result to identify the unchanged product surfaces."""
    normalized = result_text.lower()
    test.assertRegex(
        normalized,
        r"no[- ]product(?:[- ]changes?| or (?:durable )?wiki "
        r"(?:content )?(?:changed|changes?(?: (?:were|was) made)?))",
    )
    test.assertRegex(normalized, r"queue.{0,40}unchanged|unchanged.{0,40}queue")
    for surface in ("topic page", "digest", "source link", "code", "test"):
        with test.subTest(collision_surface=surface):
            test.assertIn(surface, normalized)


def _assert_collision_result_inventory(
    test: unittest.TestCase, result_text: str
) -> None:
    """Require scoped empty conclusions and one fact-bearing collision question."""
    conclusions = _labeled_inventory(result_text, CONCLUSION_INVENTORY_LABEL)
    open_questions = _labeled_inventory(result_text, OPEN_QUESTION_INVENTORY_LABEL)
    _assert_single_scoped_none_entry(test, conclusions)
    _assert_inventory_scope(test, open_questions)
    test.assertNotRegex(open_questions, r"\bnone\b")
    test.assertIn("raw/provider.md", conclusions)
    test.assertIn("raw/provider.md", open_questions)
    test.assertRegex(open_questions, r"collision|naming|disposition|authority")


def _provider_routing_pages(
    wiki_content: dict[str, str], committed_paths: set[str]
) -> list[tuple[str, str]]:
    """Return committed provider pages containing every substantiated routing fact."""
    return [
        (path, content)
        for path, content in wiki_content.items()
        if "provider" in path.lower()
        and path in committed_paths
        and "primary provider" in content.lower()
        and "secondary provider" in content.lower()
        and "mutation requests do not fail over" in content.lower()
    ]


def _assert_provider_result_inventory(
    test: unittest.TestCase, result_text: str
) -> None:
    """Require provider conclusions and ownership uncertainty in distinct inventories."""
    conclusions = _labeled_inventory(
        result_text,
        CONCLUSION_INVENTORY_LABEL,
    )
    open_questions = _labeled_inventory(
        result_text,
        OPEN_QUESTION_INVENTORY_LABEL,
    )
    _assert_fact_bearing_conclusion_bullet(test, conclusions)
    for fact in ("primary provider", "secondary provider", "mutation requests"):
        with test.subTest(provider_inventory="conclusion", fact=fact):
            test.assertIn(fact, conclusions)
    for fact in ("federat", "authoritative", "raw/provider-routing.md"):
        with test.subTest(provider_inventory="open-question", fact=fact):
            test.assertIn(fact, open_questions)


def _assert_single_jitter_open_question_page(
    test: unittest.TestCase,
    wiki_content: dict[str, str],
) -> str:
    """Require one retry-policy Open Questions section to own unresolved jitter."""
    jitter_pages = []
    for path, content in wiki_content.items():
        if not path.startswith("docs/wiki/retry-policy/"):
            continue
        open_questions = _markdown_section(content, "Open Questions").lower()
        if "jitter" in open_questions:
            jitter_pages.append((path, open_questions))
    with test.subTest(page_contract="jitter-open-question-count"):
        test.assertEqual(1, len(jitter_pages))
    if not jitter_pages:
        return ""
    path, open_questions = jitter_pages[0]
    with test.subTest(page_contract="jitter-open-question-missing-evidence"):
        test.assertTrue(_contains_missing_evidence(open_questions))
    with test.subTest(page_contract="jitter-open-question-provenance"):
        test.assertIn("raw/processed/retry-policy.md", open_questions)
    return path


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
    with test.subTest(result_disposition="interruption"):
        test.assertIn("interrupt", result_text)
    _assert_result_inventory(test, result_text)
    _assert_terminal_result_readback(
        test,
        str(result["evaluationResultText"]),
        substantiated_content_written=True,
    )
    with test.subTest(result_disposition="no-rollback"):
        test.assertNotIn("restor", result_text)
    expected = plan.outcomes()
    observed = [
        {
            "gate": observation["receipt"]["gate"],
            "invocation": observation["receipt"]["invocation"],
            "outcome": observation["receipt"]["outcome"],
        }
        for observation in result["verifierControlTrace"]
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
    with test.subTest(runtime_contract="execution-ownership"):
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
        expected_keys = {"gate", "invocation", "outcome"}
        if outcome["outcome"] == "NEEDS_CORRECTION":
            expected_keys.add("finding")
        test.assertEqual(expected_keys, set(receipt))
        test.assertEqual(gate, receipt["gate"])
        test.assertEqual(outcome["invocation"], receipt["invocation"])
        test.assertEqual(outcome["outcome"], receipt["outcome"])
        if receipt["outcome"] == "VERIFIER_INTERRUPTED":
            test.assertNotIn("GOOD", receipt.values())
            test.assertNotIn("NEEDS_CORRECTION", receipt.values())
        test.assertEqual(result["verifierControlTrace"][index]["receipt"], receipt)
    trace_digests = [
        observation["ownedTreeDigest"]
        for observation in result["verifierControlTrace"]
    ]
    for digest in trace_digests:
        test.assertRegex(digest, r"^[0-9a-f]{64}$")
    test.assertNotEqual(result["initialOwnedTreeDigest"], trace_digests[0])
    for previous, current in zip(trace_digests, trace_digests[1:]):
        test.assertNotEqual(previous, current)
    for observation in result["verifierControlTrace"]:
        changed_paths = observation["changedPaths"]
        test.assertIsInstance(changed_paths, list)
        for path in changed_paths:
            allowed = str(path).startswith("docs/wiki/")
            if observation["receipt"]["gate"] == "post-move":
                allowed = allowed or str(path) in {
                    "raw/retry-policy.md",
                    "raw/processed/retry-policy.md",
                }
            test.assertTrue(allowed, path)
    test.assertNotEqual(result["initialOwnedTreeDigest"], result["finalOwnedTreeDigest"])
    committed_paths = set(result["committedPaths"])
    test.assertIn("eval-result.md", committed_paths)
    test.assertIn("raw/processed/retry-policy.md", committed_paths)
    retry_pages = {
        path: content
        for path, content in result["wikiContent"].items()
        if path.startswith("docs/wiki/retry-policy/")
    }
    test.assertTrue(retry_pages)
    test.assertTrue(set(retry_pages).issubset(committed_paths))
    for index, outcome in enumerate(expected):
        if outcome["outcome"] != "NEEDS_CORRECTION":
            continue
        page_path, heading, statement = CORRECTION_EXPECTATIONS[
            outcome["invocation"]
        ]
        resubmission_pages = result["verifierControlTrace"][index + 1]["pageContents"]
        test.assertIn(page_path, resubmission_pages)
        test.assertIn(heading, resubmission_pages[page_path])
        test.assertIn(statement, resubmission_pages[page_path])
        test.assertIn(page_path, committed_paths)
        test.assertIn(heading, result["wikiContent"][page_path])
        test.assertIn(statement, result["wikiContent"][page_path])
    _assert_single_jitter_open_question_page(test, retry_pages)
    _assert_terminal_head(test, result, terminal)
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
    target_session_id = str(result["targetSessionId"])
    test.assertTrue(target_session_id)
    test.assertEqual(len(result["dependencySessionIds"]), len(dependency_calls))
    test.assertEqual(
        len(result["dependencySessionIds"]),
        len(set(result["dependencySessionIds"])),
    )
    test.assertEqual(
        len(result["dependencyAgentPaths"]),
        len(set(result["dependencyAgentPaths"])),
    )
    test.assertNotIn(target_session_id, result["dependencySessionIds"])
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
        test.assertEqual(
            result["verifierDriverCommand"],
            _extract_single_exec_command(arguments),
        )
        trace = result["verifierControlTrace"][index]
        receipt = trace["receipt"]
        response_receipt = json.loads(str(result["dependencyResponses"][index]))
        test.assertEqual(receipt, response_receipt)
        request_messages = dependency_requests[index]
        test.assertIsInstance(request_messages, list)
        test.assertTrue(request_messages)
        captured_environment = "\n".join(request_messages)
        captured_cwds = re.findall(r"<cwd>([^<]+)</cwd>", captured_environment)
        test.assertTrue(captured_cwds)
        test.assertEqual(
            _canonical_runtime_path(str(result["repositoryPath"])),
            _canonical_runtime_path(captured_cwds[-1]),
        )
        spawn_arguments = target_spawns[index]
        test.assertEqual("wiki_topic_verifier", spawn_arguments.get("agent_type"))
        expected_task_name = (
            f"{str(receipt['gate']).replace('-', '_')}_verifier_"
            f"{receipt['invocation']}"
        )
        test.assertEqual(expected_task_name, spawn_arguments.get("task_name"))
        agent_path = str(result["dependencyAgentPaths"][index])
        test.assertEqual(expected_task_name, agent_path.rsplit("/", maxsplit=1)[-1])
        test.assertTrue(agent_path.startswith("/root/wiki_ingester/"))
        verifier_request = str(spawn_arguments.get("message", ""))
        test.assertTrue(verifier_request)
        if not _is_encrypted_spawn_message(verifier_request):
            test.assertIn(str(receipt["gate"]), verifier_request.lower())
            test.assertIn("lint", verifier_request.lower())
            source_name = (
                "provider-routing.md"
                if result.get("rawSourcePresent") or result.get("processedSourcePresent")
                else "retry-policy.md"
            )
            expected_source = (
                f"raw/{source_name}"
                if receipt["gate"] == "pre-move"
                else f"raw/processed/{source_name}"
            )
            test.assertIn(expected_source, verifier_request)
            for path in trace["changedPaths"]:
                if str(path).startswith("docs/wiki/"):
                    test.assertIn(path, verifier_request)
        test.assertTrue(
            spawn_arguments.get("fork_context") is False
            or spawn_arguments.get("fork_turns") == "none"
        )


def _is_encrypted_spawn_message(message: str) -> bool:
    """Recognize retained Fernet-shaped spawn ciphertext without decoding it."""
    return re.fullmatch(r"gAAAA[A-Za-z0-9_-]{32,}={0,2}", message) is not None


def _retained_ownership_result(ownership: dict[str, object]) -> dict[str, object]:
    """Build a portable result shape from sanitized retained ownership evidence."""
    receipts = ownership["receipts"]
    session_ids = ownership["dependencySessionIds"]
    agent_paths = ownership["dependencyAgentPaths"]
    command = "/portable/python /portable/control/next_verdict.py"
    encrypted_message = "gAAAA" + "SANITIZED_RETAINED_CIPHERTEXT_" * 3
    target_calls = []
    dependency_calls = []
    dependency_requests = []
    traces = []
    for receipt, agent_path in zip(receipts, agent_paths, strict=True):
        target_calls.append({
            "name": "spawn_agent",
            "arguments": json.dumps({
                "agent_type": "wiki_topic_verifier",
                "fork_turns": "none",
                "task_name": str(agent_path).rsplit("/", maxsplit=1)[-1],
                "message": encrypted_message,
            }),
        })
        dependency_calls.append([{
            "name": "exec",
            "arguments": (
                "const r=await tools.exec_command({cmd:"
                f"{json.dumps(command)}"
                "}); text(r.output);"
            ),
        }])
        dependency_requests.append([
            "<environment_context><cwd>/portable/wiki-fixture</cwd>"
            "</environment_context>"
        ])
        traces.append({"receipt": receipt, "changedPaths": []})
    return {
        "targetSessionId": ownership["targetSessionId"],
        "targetInstructionMarker": "retained-target-marker",
        "targetInstructionMarkers": ["retained-target-marker"],
        "rootToolCalls": [{
            "name": "spawn_agent",
            "arguments": json.dumps({
                "agent_type": "wiki_ingester",
                "fork_turns": "none",
            }),
        }],
        "targetToolCalls": target_calls,
        "dependencySessionIds": session_ids,
        "dependencyAgentPaths": agent_paths,
        "dependencyResponses": [json.dumps(receipt) for receipt in receipts],
        "dependencyRequests": dependency_requests,
        "dependencyToolCalls": dependency_calls,
        "verifierDriverCommand": command,
        "repositoryPath": "/portable/wiki-fixture",
        "verifierControlTrace": traces,
    }


def _assert_terminal_head(
    test: unittest.TestCase,
    result: dict[str, object],
    terminal: str,
) -> None:
    """Require the full HEAD or one Git-resolved, labeled commit abbreviation."""
    expected_head = str(result["head"])
    if expected_head in terminal:
        return
    abbreviations = set(re.findall(
        r"(?i)\bcommit(?:ted)?\s*(?:(?:is|as)\s*)?[:=#-]?\s*`?"
        r"([0-9a-f]{7,39})\b",
        terminal,
    ))
    test.assertEqual(1, len(abbreviations))
    abbreviation = next(iter(abbreviations))
    completed = subprocess.run(
        ["git", "rev-parse", "--verify", f"{abbreviation}^{{commit}}"],
        cwd=str(result["repositoryPath"]),
        capture_output=True,
        text=True,
        check=False,
    )
    test.assertEqual(0, completed.returncode)
    test.assertEqual(expected_head, completed.stdout.strip())


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
                        {"gate", "invocation", "outcome"},
                        set(outcomes[-1]),
                    )
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
                    for outcome in gate_outcomes[:-1]:
                        page_path, heading, statement = CORRECTION_EXPECTATIONS[
                            outcome["invocation"]
                        ]
                        self.assertIn(page_path, outcome["finding"])
                        self.assertIn(heading, outcome["finding"])
                        self.assertIn(statement, outcome["finding"])
        self.assertEqual(6, len(observed))

    def test_launcher_does_not_supply_the_expected_interruption_disposition(self) -> None:
        """The canonical target, not its launcher, must derive the resulting behavior."""
        prompt = self.harness._target_prompt(
            self.harness.VerifierPlan("pre-move", 1)
        )
        for injected_expectation in (
            "substantiated conclusion",
            "Open Questions",
            "missing evidence",
            "provenance",
            "processed-source",
            "ingested conclusions",
            "VERIFIER_INTERRUPTED",
        ):
            with self.subTest(injected_expectation=injected_expectation):
                self.assertNotIn(injected_expectation, prompt)

    def test_exec_command_parser_accepts_current_quoted_and_unquoted_key_shapes(self) -> None:
        """Both emitted JavaScript object-key forms must preserve the exact command."""
        expected = "/python /control/next_verdict.py"
        for arguments in (
            'const r=await tools.exec_command({cmd:"/python /control/next_verdict.py"});',
            'const r=await tools.exec_command({"cmd":"/python /control/next_verdict.py"});',
        ):
            with self.subTest(arguments=arguments):
                self.assertEqual(expected, _extract_single_exec_command(arguments))
        for invalid in (
            'tools.exec_command({command:"/python /control/next_verdict.py"})',
            'tools.exec_command({cmd:"one", "cmd":"two"})',
            'tools.exec_command({cmd:"one"}); tools.write_stdin({})',
            'const evil="git add docs/wiki"; await tools.exec_command({cmd:evil}); '
            'const decoy={cmd:"/python /control/next_verdict.py"};',
        ):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    _extract_single_exec_command(invalid)

    def test_result_inventory_requires_labeled_entries_instead_of_category_words(self) -> None:
        """Negative prose must not masquerade as populated result inventories."""
        negative = (
            "No ingested conclusions were recorded.\n"
            "No open questions were recorded.\n"
        )
        self.assertEqual(
            "",
            _labeled_inventory(
                negative,
                r"(?:(?:ingested|substantiated|supported)\s+)?conclusions?",
            ),
        )
        self.assertEqual(
            "",
            _labeled_inventory(negative, r"(?:recorded\s+)?open questions?"),
        )
        positive = (
            "## Ingested Conclusion\n\n"
            "- Fixed retry delays are 200 and 500 milliseconds.\n\n"
            "## Open Questions\n\n"
            "- Jitter lacks authoritative evidence in raw/processed/retry-policy.md.\n"
        )
        self.assertIn("200", _labeled_inventory(
            positive,
            r"(?:(?:ingested|substantiated|supported)\s+)?conclusions?",
        ))
        self.assertIn(
            "jitter",
            _labeled_inventory(positive, r"(?:recorded\s+)?open questions?"),
        )

    def test_result_inventory_accepts_fact_bearing_semantic_labels(self) -> None:
        """Structured inventory variants remain valid when they carry required facts."""
        result_text = (
            "## Preserved substantiated content\n\n"
            "- docs/wiki/retry-policy/backoff.md: idempotent reads use fixed retry "
            "delays of 200 and 500 milliseconds. Source: "
            "raw/processed/retry-policy.md.\n\n"
            "## Page-local unresolved point\n\n"
            "- Deployment jitter remains unresolved because there is no deployment-policy "
            "or implementation evidence. Page: docs/wiki/retry-policy/backoff.md; "
            "source: raw/processed/retry-policy.md.\n"
        )
        _assert_result_inventory(self, result_text)
        unbulleted_conclusion = result_text.replace(
            "- docs/wiki/retry-policy/backoff.md: idempotent reads",
            "docs/wiki/retry-policy/backoff.md: idempotent reads",
            1,
        )
        with self.assertRaises(AssertionError):
            _assert_result_inventory(self, unbulleted_conclusion)

    def test_retained_evaluator_artifacts_replay_offline(self) -> None:
        """Sanitized retained evaluator artifacts must replay without live execution."""
        replay = json.loads(RETAINED_REPLAY_PATH.read_text(encoding="utf-8"))
        self.assertEqual(
            "4e2f8ce5abac470a099b46dcb178c62c4292e1cdea19d3de3c0b7620631a259f",
            replay["matrixSha256"],
        )
        executions = replay["executions"]
        _assert_result_inventory(self, executions["02"]["resultText"])
        _assert_result_inventory(self, executions["06"]["resultText"])
        self.assertTrue(_contains_missing_evidence(executions["06"]["resultText"]))
        _assert_collision_no_change(self, executions["08"]["resultText"])
        _assert_provider_result_inventory(self, executions["09"]["resultText"])
        self.assertTrue(_contains_correction_attempt_count(executions["09"]["resultText"]))
        for execution in ("02", "06", "09"):
            with self.subTest(retained_execution=execution):
                _validate_execution_ownership(
                    self,
                    _retained_ownership_result(executions[execution]["ownership"]),
                )
        self.assertTrue(
            executions["06"]["expectedHead"].startswith(
                executions["06"]["terminalCommit"]
            )
        )
        self.assertEqual(
            "6e3cad8d49df63ca055634f3e8940aa93794ba3918ce17928ae088898ae3729c",
            replay["fiveCaseLogSha256"],
        )
        self.assertEqual(
            "6dc61d29-4cd1-4879-b06f-6d72e1773a5f",
            replay["fiveCaseResourceReleaseEventId"],
        )
        page_local_jitter = replay["pageLocalJitterReplay"]
        self.assertEqual(
            "6d718e1333087bf078bedf7bed4aed085975a76153ca87a9177037d7035e9143",
            page_local_jitter["retainedRootCauseArtifactSha256"],
        )
        _assert_result_inventory(self, page_local_jitter["resultText"])
        accepted_jitter_page = _assert_single_jitter_open_question_page(
            self,
            page_local_jitter["wikiContent"],
        )
        self.assertEqual(page_local_jitter["expectedPage"], accepted_jitter_page)
        post1 = executions["post1"]
        self.assertEqual(
            [
                ("pre-move", 0, "GOOD"),
                ("post-move", 0, "NEEDS_CORRECTION"),
                ("post-move", 1, "VERIFIER_INTERRUPTED"),
            ],
            [
                (receipt["gate"], receipt["invocation"], receipt["outcome"])
                for receipt in post1["receipts"]
            ],
        )
        corrected_page = post1["resubmissionPageContents"][
            "docs/wiki/retry-policy/request-eligibility.md"
        ]
        self.assertIn("## Ineligible mutation requests", corrected_page)
        self.assertIn(
            "Order creation, cancellation, and payment mutation requests are never retried.",
            corrected_page,
        )
        _assert_result_inventory(self, post1["resultText"])
        jitter = _markdown_section(
            post1["wikiContent"]["docs/wiki/retry-policy/retry-execution.md"],
            "Open Questions",
        ).lower()
        self.assertIn("jitter", jitter)
        self.assertIn("raw/processed/retry-policy.md", jitter)
        self.assertEqual(
            {
                "rawSourcePresent": False,
                "processedSourcePresent": True,
                "processedLinksResolve": True,
            },
            post1["sourceState"],
        )
        self.assertEqual("", post1["gitStatus"])
        self.assertEqual([], post1["liveRegistryClaims"])
        self.assertIs(post1["claimReleased"], True)
        self.assertIs(post1["terminalResultWrittenBeforeCommit"], True)
        for name, capture in replay["terminalResultCaptures"].items():
            with self.subTest(terminal_result_capture=name):
                if capture["expected"] == "accept":
                    _assert_terminal_result_readback(
                        self,
                        capture["resultText"],
                        capture["substantiatedContentWritten"],
                    )
                else:
                    with self.assertRaises(AssertionError):
                        _assert_terminal_result_readback(
                            self,
                            capture["resultText"],
                            capture["substantiatedContentWritten"],
                        )

    def test_jitter_page_contract_rejects_missing_or_duplicate_evidence(self) -> None:
        """One page-local jitter question must retain reason and provenance."""
        replay = json.loads(RETAINED_REPLAY_PATH.read_text(encoding="utf-8"))
        valid = replay["pageLocalJitterReplay"]["wikiContent"]
        page_path = replay["pageLocalJitterReplay"]["expectedPage"]
        page = valid[page_path]
        invalid_pages = (
            {page_path: page.replace("## Open Questions", "## Notes")},
            {page_path: page.replace("no authoritative", "unspecified")},
            {
                page_path: page.replace(
                    "no authoritative deployment-policy or implementation evidence is available",
                    "authoritative evidence is available",
                )
            },
            {page_path: page.replace("raw/processed/retry-policy.md", "the source")},
            {
                **valid,
                "docs/wiki/retry-policy/retry-timing.md": page,
            },
        )
        for invalid in invalid_pages:
            with self.subTest(invalid=invalid):
                with self.assertRaises(AssertionError):
                    _assert_single_jitter_open_question_page(
                        unittest.TestCase(),
                        invalid,
                    )

    def test_encrypted_spawn_fallback_rejects_false_identity_and_receipts(self) -> None:
        """Opaque prompts cannot bypass fresh-child, call, or receipt evidence."""
        replay = json.loads(RETAINED_REPLAY_PATH.read_text(encoding="utf-8"))
        baseline = _retained_ownership_result(
            replay["executions"]["02"]["ownership"]
        )
        _validate_execution_ownership(self, baseline)
        mutations = (
            lambda result: result["dependencySessionIds"].__setitem__(
                1, result["dependencySessionIds"][0]
            ),
            lambda result: result["dependencyAgentPaths"].__setitem__(
                0, "/root/unbound/pre_move_verifier_0"
            ),
            lambda result: result["dependencyResponses"].__setitem__(
                0, json.dumps({"gate": "pre-move", "invocation": 0, "outcome": "GOOD"})
            ),
            lambda result: result["dependencyToolCalls"][0].append({
                "name": "exec",
                "arguments": "tools.exec_command({cmd:\"git status\"})",
            }),
            lambda result: result["targetToolCalls"][0].__setitem__(
                "arguments",
                json.dumps({
                    "agent_type": "wiki_topic_verifier",
                    "fork_turns": "none",
                    "task_name": "wrong_verifier_identity",
                    "message": "gAAAA" + "SANITIZED_CIPHERTEXT_" * 3,
                }),
            ),
        )
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                adversarial = json.loads(json.dumps(baseline))
                mutate(adversarial)
                with self.assertRaises(AssertionError):
                    _validate_execution_ownership(self, adversarial)
        inspectable_bypass = json.loads(json.dumps(baseline))
        arguments = json.loads(inspectable_bypass["targetToolCalls"][0]["arguments"])
        arguments["message"] = "opaque but not encrypted"
        inspectable_bypass["targetToolCalls"][0]["arguments"] = json.dumps(arguments)
        with self.assertRaises(AssertionError):
            _validate_execution_ownership(self, inspectable_bypass)

    def test_terminal_commit_accepts_only_resolved_expected_head(self) -> None:
        """A labeled abbreviation must resolve uniquely to the observed HEAD."""
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=REPOSITORY_ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        result = {"head": head, "repositoryPath": str(REPOSITORY_ROOT)}
        _assert_terminal_head(self, result, f"READY. Commit: {head[:7]}.")
        for terminal in (
            "READY. Commit: abcdef0.",
            f"READY. Commit: {head[:6]}.",
            "READY without commit evidence.",
        ):
            with self.subTest(terminal=terminal):
                with self.assertRaises(AssertionError):
                    _assert_terminal_head(self, result, terminal)

    def test_live_case_selector_is_exact_and_rejects_adversarial_input(self) -> None:
        """Focused reruns select only named interruption and raw-ingest controls."""
        self.assertIsNone(_parse_live_case_selector(None))
        self.assertEqual(
            frozenset({"pre0", "raw-ingest"}),
            _parse_live_case_selector("pre0,raw-ingest"),
        )
        for invalid in (
            "",
            "pre1",
            "post1",
            "pre2",
            "post0",
            "pre0,pre0",
            "pre0, raw-ingest",
            "all",
        ):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    _parse_live_case_selector(invalid)

    def test_none_inventory_requires_assessed_source_and_page_scope(self) -> None:
        """None is valid only with explicit assessed raw source and wiki page scope."""
        valid = (
            "- None. Assessed source: raw/provider.md. "
            "Assessed page scope: docs/wiki; no pages changed."
        )
        _assert_inventory_scope(self, valid)
        for invalid in (
            "",
            "- None.",
            "- None. Assessed source: raw/provider.md.",
            "- None. Assessed page scope: docs/wiki.",
        ):
            with self.subTest(invalid=invalid):
                with self.assertRaises(AssertionError):
                    _assert_inventory_scope(self, invalid)

    def test_path_aliases_canonicalize_before_runtime_ownership_comparison(self) -> None:
        """macOS /var and /private/var names identify the same captured repository."""
        self.assertEqual(
            _canonical_runtime_path("/var/folders/example/fixture"),
            _canonical_runtime_path("/private/var/folders/example/fixture"),
        )

    def test_collision_result_accepts_durable_wiki_phrase_and_enumerated_surfaces(self) -> None:
        """A semantic no-change statement must still enumerate every protected surface."""
        result_text = (
            "Queue unchanged. No product or durable wiki content changed. "
            "No topic page, digest, source link, code, or test was changed.\n\n"
            "## Substantiated Conclusions\n\n"
            "- None. Assessed source: raw/provider.md. "
            "Assessed page scope: docs/wiki; no pages changed.\n\n"
            "## Open Questions\n\n"
            "- docs/wiki/ page scope for raw/provider.md: the destination collision "
            "requires naming or disposition authority."
        )
        _assert_collision_no_change(self, result_text)
        _assert_collision_result_inventory(self, result_text)
        bypass = result_text.replace(
            "- None. Assessed source: raw/provider.md. "
            "Assessed page scope: docs/wiki; no pages changed.",
            "- There are none. raw/provider.md docs/wiki/.",
        )
        with self.assertRaises(AssertionError):
            _assert_collision_result_inventory(self, bypass)
        second_entry = result_text.replace(
            "Assessed page scope: docs/wiki; no pages changed.",
            "Assessed page scope: docs/wiki; no pages changed.\n"
            "- A second conclusion from raw/provider.md for docs/wiki/.",
        )
        with self.assertRaises(AssertionError):
            _assert_collision_result_inventory(self, second_entry)

    def test_provider_page_contract_is_bound_to_one_committed_page(self) -> None:
        """Provider conclusions and their open question must share one committed page."""
        provider_page = (
            "Primary provider handles reads. Secondary provider handles failover. "
            "Mutation requests do not fail over.\n\n"
            "## Open Questions\n\n"
            "- Federation ownership lacks an authoritative decision; provenance: "
            "raw/provider-routing.md.\n"
        )
        pages = _provider_routing_pages(
            {
                "docs/wiki/provider-routing.md": provider_page,
                "docs/wiki/uncommitted-provider.md": provider_page,
                "docs/wiki/unrelated.md": "## Open Questions\n\n- raw/provider-routing.md",
            },
            {"docs/wiki/provider-routing.md", "docs/wiki/unrelated.md"},
        )
        self.assertEqual(
            [("docs/wiki/provider-routing.md", provider_page)],
            pages,
        )
        open_questions = _markdown_section(pages[0][1], "Open Questions").lower()
        for fact in ("federat", "authoritative", "raw/provider-routing.md"):
            with self.subTest(fact=fact):
                self.assertIn(fact, open_questions)

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
                "Open Questions section of exactly one most-relevant existing page",
                "not a NEEDS_CORRECTION verdict",
                "do not invoke wiki_topic_verifier again for that source",
                "Verifier interruption alone is not a BLOCKED condition",
                "labeled ingested or substantiated conclusions inventory",
                "labeled Open Questions inventory",
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
                "receipt": outcome,
                "ownedTreeDigest": character * 64,
                "changedPaths": ["docs/wiki/retry-policy/example.md"],
                "pageContents": (
                    {
                        CORRECTION_EXPECTATIONS[0][0]: (
                            f"{CORRECTION_EXPECTATIONS[0][1]}\n\n"
                            f"{CORRECTION_EXPECTATIONS[0][2]}\n"
                        )
                    }
                    if index == 1
                    else {}
                ),
            }
            for index, (outcome, character) in enumerate(
                zip(plan.outcomes(), ("a", "b"), strict=True)
            )
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
            "targetSessionId": "target-session",
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
            "repositoryPath": "/private/var/folders/example/fixture",
            "targetToolCalls": [
                {
                    "name": "spawn_agent",
                    "arguments": json.dumps({
                        "agent_type": "wiki_topic_verifier",
                        "fork_turns": "none",
                        "task_name": "pre_move_verifier_0",
                        "message": (
                            "/var/folders/example/fixture pre-move raw/retry-policy.md "
                            "lint docs/wiki/retry-policy/example.md"
                        ),
                    }),
                },
                {
                    "name": "spawn_agent",
                    "arguments": json.dumps({
                        "agent_type": "wiki_topic_verifier",
                        "fork_turns": "none",
                        "task_name": "pre_move_verifier_1",
                        "message": (
                            "/var/folders/example/fixture pre-move raw/retry-policy.md "
                            "lint docs/wiki/retry-policy/example.md"
                        ),
                    }),
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
                    "<environment_context><cwd>/var/folders/example/fixture</cwd>"
                    "</environment_context>"
                ],
                [
                    "<environment_context><cwd>/var/folders/example/fixture</cwd>"
                    "</environment_context>"
                ],
            ],
            "targetTerminalResponse": f"READY {head} {release_id} RELEASED CLEAN",
            "gitStatus": "",
            "liveRegistryClaims": [],
            "retryRawSourcePresent": False,
            "retryProcessedSourcePresent": True,
            "evaluationResultText": (
                "Interruption continuation completed.\n\n"
                "## Substantiated Conclusions\n\n"
                "- docs/wiki/retry-policy/retry-execution.md: idempotent reads "
                "use retry delays of 200 and 500 milliseconds. Source: "
                "raw/processed/retry-policy.md.\n\n"
                "## Open Questions\n\n"
                "- docs/wiki/retry-policy/retry-execution.md: jitter lacks "
                "authoritative evidence in raw/processed/retry-policy.md.\n"
            ),
            "verifierControlTrace": trace,
            "dependencySessionIds": ["verifier-0", "verifier-1"],
            "dependencyAgentPaths": [
                "/root/wiki_ingester/pre_move_verifier_0",
                "/root/wiki_ingester/pre_move_verifier_1",
            ],
            "dependencyResponses": [
                json.dumps(observation["receipt"])
                for observation in trace
            ],
            "initialOwnedTreeDigest": "d" * 64,
            "finalOwnedTreeDigest": "b" * 64,
            "committedPaths": [
                "docs/wiki/retry-policy/retry-execution.md",
                "docs/wiki/retry-policy/request-eligibility.md",
                "eval-result.md",
                "raw/processed/retry-policy.md",
            ],
            "wikiContent": {
                "docs/wiki/retry-policy/retry-execution.md": (
                    "## Open Questions\n\n"
                    "- Jitter remains unresolved because authoritative retry-policy "
                    "evidence is missing. Provenance: raw/processed/retry-policy.md.\n"
                ),
                CORRECTION_EXPECTATIONS[0][0]: (
                    f"{CORRECTION_EXPECTATIONS[0][1]}\n\n"
                    f"{CORRECTION_EXPECTATIONS[0][2]}\n"
                ),
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
            result["verifierControlTrace"][1]["receipt"]
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
            self.assertEqual(
                {"gate", "invocation", "outcome"},
                set(receipt),
            )
            observation = json.loads(
                (layout.control_root / "state.json").read_text(encoding="utf-8")
            )[0]
            self.assertIn(
                "docs/wiki/retry-policy/new-leaf.md", observation["changedPaths"]
            )
            self.assertIn("docs/wiki/topic-index.md", observation["changedPaths"])
            self.assertIn(
                "docs/wiki/retry-policy/new-leaf.md",
                observation["pageContents"],
            )

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
        observer = inspect.getsource(self.harness._observe_target_result)
        self.assertIn("session.parent_thread_id == target.session_id", observer)

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

    def test_retry_fixture_declares_jitter_as_unresolved_source_evidence(self) -> None:
        """The source itself, not evaluator injection, must establish the open question."""
        source_text = (
            SUITE_ROOT
            / "fixtures/scenario-files/raw-ingest/raw/retry-policy.md"
        ).read_text(encoding="utf-8")
        self.assertIn("deployment-specific jitter", source_text)
        self.assertIn("remains unresolved", source_text)
        self.assertIn(
            "authoritative deployment policy or implementation evidence",
            source_text,
        )
        self.assertNotIn(
            "deployment-specific jitter",
            self.harness._target_prompt(self.harness.VerifierPlan("pre-move", 0)),
        )
        interruption = self.harness.VerifierPlan("pre-move", 0).outcomes()[-1]
        self.assertEqual({"gate", "invocation", "outcome"}, set(interruption))

    def test_verifier_failure_neighbor_uses_three_real_correction_verdicts(self) -> None:
        """The executable neighbor must exhaust the real bounded verifier loop."""
        outcomes = self.harness._neighbor_outcomes("verifier-failure")
        self.assertEqual(3, len(outcomes))
        self.assertEqual([0, 1, 2], [outcome["invocation"] for outcome in outcomes])
        self.assertTrue(
            all(outcome["outcome"] == "NEEDS_CORRECTION" for outcome in outcomes)
        )
        self.assertTrue(
            all(outcome["finding"] == "federated ownership duplicated" for outcome in outcomes)
        )
        task_text = (
            SUITE_ROOT
            / "fixtures/scenario-files/verifier-failure/TASK.md"
        ).read_text(encoding="utf-8")
        self.assertIn("preserve every substantiated local-routing conclusion", task_text)
        self.assertIn("Open Questions section", task_text)
        self.assertIn("raw-source provenance", task_text)
        self.assertNotIn("restore every unaccepted wiki edit", task_text)


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
        selected = _selected_live_cases()
        for gate in ("pre-move", "post-move"):
            for interruption in range(3):
                case = f"{'pre' if gate == 'pre-move' else 'post'}{interruption}"
                if selected is not None and case not in selected:
                    continue
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
        selected = _selected_live_cases()
        if selected is not None and "raw-ingest" not in selected:
            self.skipTest("raw-ingest not selected by focused live case selector")
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
            with self.subTest(runtime_contract="execution-ownership"):
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
                self.assertEqual(
                    result["verifierControlTrace"][index]["receipt"],
                    receipt,
                )
            trace_digests = [
                observation["ownedTreeDigest"]
                for observation in result["verifierControlTrace"]
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
            _assert_single_jitter_open_question_page(
                self,
                {
                    path: result["wikiContent"][path]
                    for path in retry_pages
                },
            )
            result_text = result["evaluationResultText"].lower()
            for evidence, pattern in (
                ("pre-move gate", r"pre[- ]move"),
                ("post-move gate", r"post[- ]move"),
                ("correction verdict", r"needs[_ -]correction"),
                ("lint", r"lint"),
                ("okf", r"okf"),
                ("processed source", r"processed"),
            ):
                with self.subTest(result_evidence=evidence):
                    self.assertRegex(result_text, pattern)
            _assert_result_inventory(self, result_text)
            _assert_terminal_result_readback(
                self,
                result["evaluationResultText"],
                substantiated_content_written=True,
            )
            _assert_terminal_head(self, result, result["targetTerminalResponse"])
            _validate_claim_events(self, result, result["targetTerminalResponse"])

    def test_collision_preserves_both_sources_without_verifier_mutation(self) -> None:
        """A destination collision keeps both source bytes and closes as clean BLOCKED."""
        if _selected_live_cases() is not None:
            self.skipTest("collision excluded from the focused live correction rerun")
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
            with self.subTest(runtime_contract="execution-ownership"):
                _validate_execution_ownership(self, result)
            self.assertEqual(["eval-result.md"], result["committedPaths"])
            result_text = result["evaluationResultText"].lower()
            for evidence, pattern in (
                ("collision", r"collision"),
                ("naming", r"naming"),
                ("disposition", r"disposition"),
            ):
                with self.subTest(result_evidence=evidence):
                    self.assertRegex(result_text, pattern)
            _assert_collision_no_change(self, result_text)
            _assert_collision_result_inventory(self, result_text)
            _assert_terminal_result_readback(
                self,
                result["evaluationResultText"],
                substantiated_content_written=False,
            )
            _assert_terminal_head(self, result, result["targetTerminalResponse"])
            _validate_claim_events(self, result, result["targetTerminalResponse"])

    def test_verifier_failure_retains_substantiated_content_and_closes_blocked(self) -> None:
        """Three real correction verdicts retain supported content and release cleanly."""
        if _selected_live_cases() is not None:
            self.skipTest("verifier-failure excluded from focused live correction rerun")
        with tempfile.TemporaryDirectory() as temporary:
            result = self.harness.run_neighbor_control(
                "verifier-failure", Path(temporary) / "fixture"
            )
            self.assertEqual(0, result["process"]["exitCode"])
            terminal = result["targetTerminalResponse"]
            self.assertIn("BLOCKED", terminal)
            self.assertNotIn("READY", terminal)
            self.assertIs(result["rawSourcePresent"], True)
            self.assertIs(result["processedSourcePresent"], False)
            self.assertEqual("", result["gitStatus"])
            self.assertEqual([], result["liveRegistryClaims"])
            self.assertEqual(3, len(result["dependencySessionIds"]))
            with self.subTest(runtime_contract="execution-ownership"):
                _validate_execution_ownership(self, result)
            for invocation, (agent_path, response, observation) in enumerate(zip(
                result["dependencyAgentPaths"],
                result["dependencyResponses"],
                result["verifierControlTrace"],
                strict=True,
            )):
                self.assertTrue(
                    agent_path.endswith(f"/pre_move_verifier_{invocation}")
                )
                receipt = json.loads(response)
                self.assertEqual("pre-move", receipt["gate"])
                self.assertEqual(invocation, receipt["invocation"])
                self.assertEqual("NEEDS_CORRECTION", receipt["outcome"])
                self.assertEqual(observation["receipt"], receipt)
            self.assertNotEqual(
                result["initialOwnedTreeDigest"], result["finalOwnedTreeDigest"]
            )
            committed_paths = set(result["committedPaths"])
            self.assertIn("eval-result.md", committed_paths)
            self.assertNotIn("raw/provider-routing.md", committed_paths)
            self.assertNotIn("raw/processed/provider-routing.md", committed_paths)
            provider_pages = _provider_routing_pages(
                result["wikiContent"],
                committed_paths,
            )
            with self.subTest(page_contract="provider-routing-page-count"):
                self.assertEqual(1, len(provider_pages))
            if provider_pages:
                provider_path, provider_content = provider_pages[0]
                with self.subTest(page_contract="provider-routing-path"):
                    self.assertIn("provider", provider_path.lower())
                    self.assertIn(provider_path, committed_paths)
                open_questions = _markdown_section(
                    provider_content,
                    "Open Questions",
                ).lower()
                for fact in (
                    "federat",
                    "authoritative",
                    "raw/provider-routing.md",
                ):
                    with self.subTest(
                        page_contract="provider-routing-open-question",
                        fact=fact,
                    ):
                        self.assertIn(fact, open_questions)
            result_text = result["evaluationResultText"].lower()
            for evidence, pattern in (
                ("correction verdict", r"needs[_ -]correction"),
                (
                    "correction count",
                    r"(?:two|2)(?:\s+genuine)?\s+correction attempts",
                ),
            ):
                with self.subTest(result_evidence=evidence):
                    self.assertRegex(result_text, pattern)
            _assert_provider_result_inventory(self, result_text)
            _assert_terminal_result_readback(
                self,
                result["evaluationResultText"],
                substantiated_content_written=True,
            )
            _assert_terminal_head(self, result, terminal)
            _validate_claim_events(self, result, terminal)


if __name__ == "__main__":
    unittest.main()
