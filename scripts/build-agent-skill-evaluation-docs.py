#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Builds source-reconciled static HTML documentation for agent and skill evaluations.

from __future__ import annotations

import argparse
import hashlib
import html
import posixpath
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Sequence

import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = REPOSITORY_ROOT / "design" / "agent-and-skill-evaluations.html"
SKILLS_ROOT = REPOSITORY_ROOT / "skills"
ROLES_ROOT = REPOSITORY_ROOT / "agents" / "roles"
PROBES_PATH = REPOSITORY_ROOT / "evals" / "skill-probes.yaml"
CASES_PATH = REPOSITORY_ROOT / "evals" / "cases.yaml"
AGENT_SCENARIOS_PATH = REPOSITORY_ROOT / "evals" / "agent-scenarios.yaml"
WORKFLOW_PACKS_PATH = REPOSITORY_ROOT / "evals" / "workflow-packs.yaml"
SUITE_INDEX_PATH = REPOSITORY_ROOT / "evals" / "agent-tests" / "suite-index.yaml"
SUITE_PROTOCOL_PATH = REPOSITORY_ROOT / "evals" / "agent-tests" / "AGENTS.md"
SUITE_STRATEGY_PATH = REPOSITORY_ROOT / "evals" / "agent-tests" / "README.md"
EVAL_README_PATH = REPOSITORY_ROOT / "evals" / "README.md"
JUDGES_PATH = REPOSITORY_ROOT / "evals" / "judges.yaml"
CAMPAIGN_PATH = (
    REPOSITORY_ROOT
    / "evals"
    / "agent-tests"
    / "results"
    / "2026-07-17-complete-agent-suites.md"
)
MANUAL_OBSERVATION_PATH = (
    REPOSITORY_ROOT / "evals" / "results" / "2026-07-09-live-agent-evaluations.md"
)
CAMPAIGN_EVIDENCE_LEVEL = "Governed agent-suite campaign"
VERDICTS = ("PASS", "BLOCKED", "FAIL")
SUCCESS_EXIT_CODE = 0
ERROR_EXIT_CODE = 1
EVALUATION_PAGE_PROVENANCE = """<!--
Copyright (c) 2026 Martin.Bechard@DevConsult.ca
Artifact-ID: 5a1eb6bc-bd8c-4dc4-bb88-62d9064841ed
Created-UTC: 2026-07-22T18:57:11Z
Creating-Agent: historical-unknown
Runtime: historical-unknown
Dispatched-Model: historical-unknown
Reasoning-Effort: historical-unknown
Task-ID: historical-unknown
Artifact-ID-Evidence: migration-assigned
Created-UTC-Evidence: git-derived
Creating-Agent-Evidence: historical-unknown
Runtime-Evidence: historical-unknown
Dispatched-Model-Evidence: historical-unknown
Reasoning-Effort-Evidence: historical-unknown
Task-ID-Evidence: historical-unknown
-->"""


def load_yaml(path: Path) -> dict[str, object]:
    """Return one required YAML mapping from path or raise a source-contract error."""
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected a YAML mapping: {path}")
    return value


def load_skill(path: Path, root: Path) -> dict[str, object]:
    """Read one bundled skill frontmatter record for the evaluation inventory."""
    text = path.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    if len(parts) != 3:
        raise ValueError(f"Missing YAML frontmatter: {path}")
    frontmatter = yaml.safe_load(parts[1])
    if not isinstance(frontmatter, dict):
        raise ValueError(f"Invalid YAML frontmatter: {path}")
    name = frontmatter.get("name")
    if name != path.parent.name:
        raise ValueError(f"Skill directory and frontmatter name differ: {path}")
    return {
        "id": name,
        "description": str(frontmatter.get("description", "")),
        "category": str(frontmatter.get("metadata", {}).get("category", "uncategorized")),
        "sourcePath": path.relative_to(root).as_posix(),
    }


EXPLICIT_FOLLOWUP_AGENT_BY_SLUG = {
    "replace-bootstrapper-marathon-with-isolated-test-doubles.md": "project-bootstrapper",
    "restore-wiki-ingester-on-verifier-interruption.md": "wiki-ingester",
}


def unique_ids(records: list[dict[str, object]], label: str) -> set[str]:
    """Return non-empty unique ids from a catalog list or reject malformed records."""
    identifiers: set[str] = set()
    for record in records:
        identifier = str(record.get("id", ""))
        if not identifier or identifier in identifiers:
            raise ValueError(f"missing or duplicate {label} id: {identifier or '<empty>'}")
        identifiers.add(identifier)
    return identifiers


def unique_field_values(
    records: list[dict[str, object]], field: str, label: str
) -> set[object]:
    """Return non-empty unique field values or reject an ambiguous catalog."""
    values: set[object] = set()
    for record in records:
        value = record.get(field)
        if value is None or value == "" or value in values:
            raise ValueError(f"missing or duplicate {label}: {value or '<empty>'}")
        values.add(value)
    return values


def unique_integer_field_values(
    records: list[dict[str, object]], field: str, label: str
) -> set[int]:
    """Return unique integer-normalized field values or reject ambiguous input."""
    values: set[int] = set()
    for record in records:
        raw_value = record.get(field)
        if isinstance(raw_value, bool):
            raise ValueError(f"invalid {label}: {raw_value}")
        if isinstance(raw_value, int):
            value = raw_value
        elif isinstance(raw_value, str) and re.fullmatch(
            r"[+-]?\d+", raw_value.strip()
        ):
            value = int(raw_value)
        else:
            raise ValueError(f"invalid {label}: {raw_value or '<empty>'}")
        if value in values:
            raise ValueError(f"missing or duplicate {label}: {value}")
        values.add(value)
    return values


def repository_path_exists(root: Path, relative_path: str) -> bool:
    """Return whether a safe repository-relative path is tracked at HEAD."""
    normalized = posixpath.normpath(relative_path)
    if (
        posixpath.isabs(relative_path)
        or normalized in (".", "..")
        or normalized.startswith("../")
    ):
        raise ValueError(f"Repository source path escapes the repository: {relative_path}")
    result = subprocess.run(
        ["git", "-C", str(root), "cat-file", "-e", f"HEAD:{normalized}"],
        check=False,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def resolve_repository_link(root: Path, relative_path: str) -> str:
    """Resolve a report link, following one unambiguous tracked backlog archive move."""
    normalized = posixpath.normpath(relative_path)
    if repository_path_exists(root, normalized):
        return normalized
    if not normalized.startswith("backlog/"):
        raise ValueError(
            f"Campaign follow-up link is outside tracked backlog history: {normalized}"
        )
    history = subprocess.run(
        [
            "git",
            "-C",
            str(root),
            "log",
            "-1",
            "--format=%H",
            "HEAD",
            "--",
            f":(literal){normalized}",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if history.returncode != 0 or not history.stdout.strip():
        raise ValueError(f"Campaign follow-up link was never tracked: {normalized}")
    result = subprocess.run(
        ["git", "-C", str(root), "ls-tree", "-r", "--name-only", "HEAD", "backlog"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise ValueError(f"Cannot inspect tracked paths for report link: {relative_path}")
    basename = Path(normalized).name
    matches = [path for path in result.stdout.splitlines() if Path(path).name == basename]
    if len(matches) != 1:
        raise ValueError(
            f"Campaign follow-up link has {len(matches)} tracked matches: {normalized}"
        )
    return matches[0]


def parse_campaign(path: Path, root: Path = REPOSITORY_ROOT) -> dict[str, object]:
    """Parse the selected governed report without treating narrative evidence as structured facts."""
    text = path.read_text(encoding="utf-8")
    date_match = re.search(r"^Date:\s*(.+)$", text, re.MULTILINE)
    runtime_match = re.search(r"^Runtime:\s*(.+)$", text, re.MULTILINE)
    if not date_match or not runtime_match:
        raise ValueError(f"Campaign metadata is incomplete: {path}")

    totals: dict[str, int] = {}
    total_rows = re.findall(
        r"^\| (PASS|BLOCKED|FAIL|Total) \| (\d+) \|$", text, re.MULTILINE
    )
    for verdict, count in total_rows:
        if verdict in totals:
            raise ValueError(f"Duplicate campaign total row: {verdict}")
        totals[verdict] = int(count)
    if set(totals) != {*VERDICTS, "Total"}:
        raise ValueError("Campaign verdict table is incomplete")

    ledger_match = re.search(
        r"^## Scenario Ledger\s*$\n\n\| Suite \| Governed scenario results \|\n"
        r"\| --- \| --- \|\n(?P<rows>.*?)(?=\n\n## )",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if not ledger_match:
        raise ValueError(f"Campaign scenario ledger is missing: {path}")

    suites: dict[str, dict[str, str]] = {}
    ledger_row_pattern = re.compile(r"\| ([a-z0-9-]+) \| ([^|]+) \|")
    ledger_rows = ledger_match.group("rows").splitlines()
    if not ledger_rows:
        raise ValueError(f"Campaign scenario ledger has no rows: {path}")
    for ledger_row in ledger_rows:
        ledger_row_match = ledger_row_pattern.fullmatch(ledger_row)
        if not ledger_row_match:
            raise ValueError(f"Malformed campaign scenario ledger row: {ledger_row}")
        suite_id, results_text = ledger_row_match.groups()
        if suite_id in suites:
            raise ValueError(f"Duplicate campaign suite row: {suite_id}")
        scenario_results: dict[str, str] = {}
        for result in results_text.split("; "):
            result_match = re.fullmatch(
                rf"([a-z0-9-]+): ({'|'.join(VERDICTS)})", result
            )
            if not result_match:
                raise ValueError(f"Invalid scenario result in {path}: {result}")
            scenario_id, verdict = result_match.groups()
            if scenario_id in scenario_results:
                raise ValueError(
                    f"Duplicate campaign scenario row: {suite_id}/{scenario_id}"
                )
            scenario_results[scenario_id] = verdict
        suites[suite_id] = scenario_results

    ledger_counts = Counter(
        verdict for scenarios in suites.values() for verdict in scenarios.values()
    )
    reported_verdicts = {verdict: totals.get(verdict, 0) for verdict in VERDICTS}
    scenario_count = sum(ledger_counts.values())
    if dict(ledger_counts) != {key: value for key, value in reported_verdicts.items() if value}:
        raise ValueError("Campaign verdict table does not reconcile with its scenario ledger")
    if totals.get("Total") != scenario_count:
        raise ValueError("Campaign total does not reconcile with its scenario ledger")

    followup_match = re.search(
        r"^## Product And Skill Findings\s*$\n(?P<body>.*?)(?=\n## )",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if not followup_match:
        raise ValueError("Campaign follow-up section is missing")
    followups: list[dict[str, object]] = []
    followup_pattern = re.compile(r"(\d+)\. \[([^]]+)]\(([^)]+)\)\.")
    followup_titles: set[str] = set()
    followup_targets: set[str] = set()
    candidate_lines = [
        line
        for line in followup_match.group("body").splitlines()
        if re.match(r"^\s*(?:\d+|[-*+])\s*[.)]?\s+", line)
        or (line.lstrip().startswith("[") and re.search(r"\[[^]]+]\([^)]+\)", line))
    ]
    if not candidate_lines:
        raise ValueError("Campaign follow-up section has no numbered entries")
    for expected_number, line in enumerate(candidate_lines, start=1):
        entry_match = followup_pattern.fullmatch(line)
        if not entry_match:
            raise ValueError(f"Malformed campaign follow-up entry: {line}")
        number_text, title, target = entry_match.groups()
        if int(number_text) != expected_number:
            raise ValueError(
                f"Campaign follow-up entries are not sequential: {number_text}"
            )
        if title in followup_titles:
            raise ValueError(f"Duplicate campaign follow-up title: {title}")
        followup_titles.add(title)
        normalized = posixpath.normpath(
            posixpath.join(path.parent.relative_to(root).as_posix(), target)
        )
        normalized = resolve_repository_link(root, normalized)
        if normalized in followup_targets:
            raise ValueError(f"Duplicate campaign follow-up target: {normalized}")
        followup_targets.add(normalized)
        agent_id = EXPLICIT_FOLLOWUP_AGENT_BY_SLUG.get(Path(normalized).name)
        followups.append(
            {
                "title": title,
                "sourcePath": normalized,
                "agent": agent_id,
                "scope": "agent-mapped" if agent_id else "campaign-wide",
            }
        )

    source_path = path.relative_to(root).as_posix()
    return {
        "dateRange": date_match.group(1).strip(),
        "runtime": runtime_match.group(1).strip(),
        "harness": "Codex" if runtime_match.group(1).startswith("Codex") else "Not reported",
        "evidenceLevel": CAMPAIGN_EVIDENCE_LEVEL,
        "sourcePath": source_path,
        "suiteCount": len(suites),
        "scenarioCount": scenario_count,
        "verdicts": reported_verdicts,
        "suites": suites,
        "scenarioSnapshot": None,
        "scenarioSnapshotDigest": None,
        "followUps": followups,
    }


def classify_skill(
    probe: dict[str, object] | None,
    scenario_links: list[dict[str, object]],
    direct_governed_result: dict[str, object] | None,
) -> str:
    """Classify recorded skill coverage without promoting indirect suite use to direct evidence."""
    if direct_governed_result is not None:
        return "direct-governed"
    if probe is not None:
        return "direct-probe"
    if scenario_links:
        return "indirect-only"
    return "none"


def scenario_skill_associations(
    scenario: dict[str, object],
) -> list[dict[str, object]]:
    """Normalize one scenario's unconditional and conditional skill associations.

    The source-model builder uses this boundary to retain skills declared by a
    resource-coordination case without adding them to the scenario's
    unconditional targetSkills contract. The returned records preserve source
    order and identify whether each association is conditional. Malformed
    target-skill or coordination-case values raise ValueError.
    """
    associations: dict[str, bool] = {}
    target_skills = scenario.get("targetSkills", [])
    if not isinstance(target_skills, list):
        raise ValueError("Scenario targetSkills must be a list")
    for skill in target_skills:
        associations[str(skill)] = False
    coordination_cases = scenario.get("resourceCoordinationCases", {})
    if not isinstance(coordination_cases, dict):
        raise ValueError("Scenario resourceCoordinationCases must be a mapping")
    for case in coordination_cases.values():
        if not isinstance(case, dict):
            raise ValueError("Scenario resource coordination case must be a mapping")
        conditional_skills = case.get("targetSkills", [])
        if not isinstance(conditional_skills, list):
            raise ValueError("Scenario conditional targetSkills must be a list")
        for skill in conditional_skills:
            associations.setdefault(str(skill), True)
    return [
        {"skill": skill, "conditional": conditional}
        for skill, conditional in associations.items()
    ]


def reconcile_scenarios(
    current_scenarios: list[dict[str, object]],
    campaign_results: dict[str, str],
    retained_snapshot: dict[str, dict[str, object]] | None,
) -> list[dict[str, object]]:
    """Reconcile current scenarios with historical verdicts and an optional retained definition snapshot."""
    current_ids = unique_ids(current_scenarios, "current scenario")
    records: list[dict[str, object]] = []
    comparison_fields = ("purpose", "expectedTerminalStatus", "targetSkills")
    for scenario in current_scenarios:
        scenario_id = str(scenario["id"])
        verdict = campaign_results.get(scenario_id)
        drift_fields: list[str] = []
        if verdict is None:
            evidence_state = "missing"
        elif retained_snapshot is None or scenario_id not in retained_snapshot:
            evidence_state = "historical-id-only"
        else:
            historical = retained_snapshot[scenario_id]
            drift_fields = [
                field
                for field in comparison_fields
                if scenario.get(field) != historical.get(field)
            ]
            evidence_state = (
                "historical-drift" if drift_fields else "historical-snapshot-aligned"
            )
        records.append(
            {
                **scenario,
                "campaignVerdict": verdict,
                "evidenceState": evidence_state,
                "catalogState": "current",
                "driftFields": drift_fields,
            }
        )

    for scenario_id, verdict in campaign_results.items():
        if scenario_id in current_ids:
            continue
        historical = (retained_snapshot or {}).get(scenario_id, {})
        records.append(
            {
                "id": scenario_id,
                "purpose": historical.get(
                    "purpose", "Campaign-only row; historical definition was not retained."
                ),
                "expectedTerminalStatus": historical.get(
                    "expectedTerminalStatus", "Not retained"
                ),
                "targetSkills": historical.get("targetSkills", []),
                "campaignVerdict": verdict,
                "evidenceState": "historical-removed",
                "catalogState": "campaign-only",
                "driftFields": [],
            }
        )
    return records


def build_model(root: Path = REPOSITORY_ROOT) -> dict[str, object]:
    """Build the complete current-catalog and selected-campaign documentation model."""
    skills_root = root / "skills"
    roles_root = root / "agents" / "roles"
    probes_path = root / PROBES_PATH.relative_to(REPOSITORY_ROOT)
    cases_path = root / CASES_PATH.relative_to(REPOSITORY_ROOT)
    agent_scenarios_path = root / AGENT_SCENARIOS_PATH.relative_to(REPOSITORY_ROOT)
    workflow_packs_path = root / WORKFLOW_PACKS_PATH.relative_to(REPOSITORY_ROOT)
    suite_index_path = root / SUITE_INDEX_PATH.relative_to(REPOSITORY_ROOT)
    campaign_path = root / CAMPAIGN_PATH.relative_to(REPOSITORY_ROOT)

    skill_records = [
        load_skill(path, root) for path in sorted(skills_root.glob("*/SKILL.md"))
    ]
    probes_document = load_yaml(probes_path)
    probes = probes_document.get("probes")
    if not isinstance(probes, list):
        raise ValueError(f"Probe catalog has no probe list: {probes_path}")
    probe_ids = unique_ids(probes, "probe")
    probes_by_skill: dict[str, dict[str, object]] = {}
    for probe in probes:
        skill_id = str(probe.get("skill", ""))
        if not skill_id or skill_id in probes_by_skill:
            raise ValueError(f"Every probe must name one unique bundled skill: {skill_id}")
        probes_by_skill[skill_id] = probe

    cases_document = load_yaml(cases_path)
    case_records = cases_document.get("cases")
    agent_scenarios_document = load_yaml(agent_scenarios_path)
    agent_catalog_records = agent_scenarios_document.get("agents")
    workflow_packs_document = load_yaml(workflow_packs_path)
    workflow_pack_records = workflow_packs_document.get("packs")
    if not isinstance(case_records, list):
        raise ValueError(f"Case catalog has no cases: {cases_path}")
    if not isinstance(agent_catalog_records, list):
        raise ValueError(f"Agent scenario catalog has no agents: {agent_scenarios_path}")
    if not isinstance(workflow_pack_records, list):
        raise ValueError(f"Workflow catalog has no packs: {workflow_packs_path}")
    case_ids = unique_ids(case_records, "case")
    unique_ids(agent_catalog_records, "agent scenario catalog agent")
    agent_scenario_records = [
        scenario
        for agent in agent_catalog_records
        for scenario in agent.get("scenarios", [])
    ]
    agent_scenario_ids = unique_ids(agent_scenario_records, "agent scenario")
    workflow_pack_ids = unique_ids(workflow_pack_records, "workflow pack")
    association_specs = (
        ("executableCases", case_ids),
        ("scenarioAssociations", agent_scenario_ids),
        ("workflowAssociations", workflow_pack_ids),
    )
    for probe in probes:
        for field, valid_ids in association_specs:
            for identifier in probe.get(field, []):
                if identifier not in valid_ids:
                    raise ValueError(
                        f"Probe {probe['id']} has unknown {field} entry: {identifier}"
                    )

    roles: dict[str, dict[str, object]] = {}
    for path in sorted(roles_root.glob("**/*.role.yaml")):
        role = load_yaml(path)
        role_id = str(role.get("name", ""))
        if not role_id or role_id in roles:
            raise ValueError(f"Conceptual role id is missing or duplicated: {path}")
        roles[role_id] = {
            "id": role_id,
            "description": str(role.get("description", "")),
            "sourcePath": path.relative_to(root).as_posix(),
        }

    suite_index = load_yaml(suite_index_path)
    suite_entries = suite_index.get("suites")
    if not isinstance(suite_entries, list):
        raise ValueError(f"Suite index has no suites: {suite_index_path}")
    unique_ids(suite_entries, "suite index")
    unique_field_values(suite_entries, "path", "suite index path")
    unique_integer_field_values(suite_entries, "priority", "suite index priority")
    campaign = parse_campaign(campaign_path, root)
    campaign_suites = campaign["suites"]
    if not isinstance(campaign_suites, dict):
        raise ValueError("Campaign suites are not a mapping")

    agents: list[dict[str, object]] = []
    all_scenario_links: list[dict[str, object]] = []
    source_paths = {
        PROBES_PATH.relative_to(REPOSITORY_ROOT).as_posix(),
        CASES_PATH.relative_to(REPOSITORY_ROOT).as_posix(),
        AGENT_SCENARIOS_PATH.relative_to(REPOSITORY_ROOT).as_posix(),
        WORKFLOW_PACKS_PATH.relative_to(REPOSITORY_ROOT).as_posix(),
        SUITE_INDEX_PATH.relative_to(REPOSITORY_ROOT).as_posix(),
        CAMPAIGN_PATH.relative_to(REPOSITORY_ROOT).as_posix(),
        EVAL_README_PATH.relative_to(REPOSITORY_ROOT).as_posix(),
        SUITE_PROTOCOL_PATH.relative_to(REPOSITORY_ROOT).as_posix(),
        SUITE_STRATEGY_PATH.relative_to(REPOSITORY_ROOT).as_posix(),
        JUDGES_PATH.relative_to(REPOSITORY_ROOT).as_posix(),
        MANUAL_OBSERVATION_PATH.relative_to(REPOSITORY_ROOT).as_posix(),
    }
    for index_entry in sorted(suite_entries, key=lambda item: int(item["priority"])):
        suite_id = str(index_entry["id"])
        if suite_id not in roles:
            raise ValueError(f"Suite has no conceptual role: {suite_id}")
        suite_root = root / "evals" / "agent-tests" / str(index_entry["path"])
        suite_path = suite_root / "suite.yaml"
        scenarios_path = suite_root / "scenarios.yaml"
        suite = load_yaml(suite_path)
        scenarios_document = load_yaml(scenarios_path)
        if suite.get("id") != suite_id or scenarios_document.get("suite") != suite_id:
            raise ValueError(f"Suite source identities differ for {suite_id}")
        scenarios = scenarios_document.get("scenarios")
        if not isinstance(scenarios, list):
            raise ValueError(f"Suite has no scenario list: {scenarios_path}")
        unique_integer_field_values(
            scenarios, "priority", f"{suite_id} scenario priority"
        )
        source_paths.update(
            {
                roles[suite_id]["sourcePath"],
                suite_path.relative_to(root).as_posix(),
                scenarios_path.relative_to(root).as_posix(),
            }
        )

        report_results = campaign_suites.get(suite_id)
        report_results = report_results if isinstance(report_results, dict) else {}
        normalized_current_scenarios: list[dict[str, object]] = []
        for scenario in sorted(scenarios, key=lambda item: int(item["priority"])):
            normalized_current_scenarios.append(
                {
                    "id": str(scenario["id"]),
                    "purpose": str(scenario.get("purpose", "")),
                    "expectedTerminalStatus": str(
                        scenario.get("expectedTerminalStatus", "Not declared")
                    ),
                    "targetSkills": [
                        str(value) for value in scenario.get("targetSkills", [])
                    ],
                    "skillAssociations": scenario_skill_associations(scenario),
                }
            )
        retained_snapshot = campaign["scenarioSnapshot"]
        suite_snapshot = (
            retained_snapshot.get(suite_id)
            if isinstance(retained_snapshot, dict)
            else None
        )
        scenario_records = reconcile_scenarios(
            normalized_current_scenarios, report_results, suite_snapshot
        )
        states = {str(record["evidenceState"]) for record in scenario_records}
        if not report_results:
            freshness = "missing"
        elif "historical-drift" in states or "historical-removed" in states:
            freshness = "historical-drift"
        elif "historical-id-only" in states:
            freshness = "historical-unknown"
        elif "missing" in states:
            freshness = "historical-drift"
        else:
            freshness = "snapshot-aligned"

        for scenario_record in scenario_records:
            associations = scenario_record.get(
                "skillAssociations",
                [
                    {"skill": skill_id, "conditional": False}
                    for skill_id in scenario_record["targetSkills"]
                ],
            )
            for association in associations:
                all_scenario_links.append(
                    {
                        "skill": association["skill"],
                        "conditional": association["conditional"],
                        "suite": suite_id,
                        "scenario": scenario_record["id"],
                        "campaignVerdict": scenario_record["campaignVerdict"],
                        "evidenceState": scenario_record["evidenceState"],
                        "scenarioPath": scenarios_path.relative_to(root).as_posix(),
                    }
                )

        verdict_counts = Counter(
            str(item["campaignVerdict"])
            for item in scenario_records
            if item["campaignVerdict"] is not None
        )
        agents.append(
            {
                **roles[suite_id],
                "priority": int(index_entry["priority"]),
                "rationale": str(index_entry.get("rationale", "")),
                "suitePath": suite_path.relative_to(root).as_posix(),
                "scenariosPath": scenarios_path.relative_to(root).as_posix(),
                "freshness": freshness,
                "scenarios": scenario_records,
                "campaignVerdicts": {key: verdict_counts.get(key, 0) for key in VERDICTS},
                "missingScenarioCount": sum(
                    item["catalogState"] == "current"
                    and item["campaignVerdict"] is None
                    for item in scenario_records
                ),
                "removedScenarioCount": sum(
                    item["catalogState"] == "campaign-only" for item in scenario_records
                ),
                "followUps": [
                    item
                    for item in campaign["followUps"]
                    if item["agent"] == suite_id
                ],
            }
        )

    role_ids = set(roles)
    suite_ids = {str(entry["id"]) for entry in suite_entries}
    if role_ids != suite_ids:
        raise ValueError(
            "Conceptual role and suite inventories differ: "
            f"roles-only={sorted(role_ids - suite_ids)}, suites-only={sorted(suite_ids - role_ids)}"
        )

    skill_ids = {str(skill["id"]) for skill in skill_records}
    orphan_probe_skills = set(probes_by_skill) - skill_ids
    if orphan_probe_skills:
        raise ValueError(
            f"Probes reference non-bundled skills: {sorted(orphan_probe_skills)}"
        )
    unknown_scenario_skills = {
        str(link["skill"]) for link in all_scenario_links if link["skill"] not in skill_ids
    }
    if unknown_scenario_skills:
        raise ValueError(f"Scenarios reference unknown skills: {sorted(unknown_scenario_skills)}")

    skills: list[dict[str, object]] = []
    classifications = Counter()
    for skill in sorted(skill_records, key=lambda item: str(item["id"])):
        skill_id = str(skill["id"])
        probe = probes_by_skill.get(skill_id)
        links = [link for link in all_scenario_links if link["skill"] == skill_id]
        governed_links = [link for link in links if link["campaignVerdict"] is not None]
        direct_governed_result = None
        classification = classify_skill(probe, links, direct_governed_result)
        classifications[classification] += 1
        outcomes = sorted(
            {str(link["campaignVerdict"]) for link in governed_links},
            key=VERDICTS.index,
        )
        if outcomes:
            latest_outcome = (
                "Linked agent-scenario Evaluation result categories: "
                + ", ".join(outcomes)
            )
        else:
            latest_outcome = "No selected Campaign Evaluation result link"
        skills.append(
            {
                **skill,
                "probe": probe,
                "scenarioLinks": links,
                "governedScenarioLinks": governed_links,
                "classification": classification,
                "directGovernedResult": direct_governed_result,
                "latestGovernedOutcome": latest_outcome,
                "limitation": (
                    "A probe declaration or linked agent-scenario Evaluation result does not establish a "
                    "skill-level Evaluation result. The selected Test report publishes no skill-level "
                    "Evaluation result."
                ),
            }
        )
        source_paths.add(str(skill["sourcePath"]))

    displayed_scenarios = [scenario for agent in agents for scenario in agent["scenarios"]]
    current_scenarios = [
        scenario for scenario in displayed_scenarios if scenario["catalogState"] == "current"
    ]
    missing_results = sum(
        scenario["campaignVerdict"] is None for scenario in current_scenarios
    )
    evidence_counts = Counter(
        str(scenario["evidenceState"]) for scenario in displayed_scenarios
    )
    visible_campaign_counts = Counter(
        str(scenario["campaignVerdict"])
        for scenario in displayed_scenarios
        if scenario["campaignVerdict"] is not None
    )
    if visible_campaign_counts != Counter(campaign["verdicts"]):
        raise ValueError("Visible campaign scenario rows do not reconcile with campaign totals")

    digest = hashlib.sha256()
    for relative_path in sorted(source_paths):
        digest.update(relative_path.encode("utf-8"))
        digest.update(b"\0")
        digest.update((root / relative_path).read_bytes())
        digest.update(b"\0")

    return {
        "sourceDigest": digest.hexdigest(),
        "snapshotMetadata": {
            "mode": "Deterministic source snapshot",
            "wallClockBuildTimeRetained": False,
            "campaignDateRange": campaign["dateRange"],
        },
        "associationCatalogCounts": {
            "cases": len(case_ids),
            "agentScenarios": len(agent_scenario_ids),
            "workflowPacks": len(workflow_pack_ids),
        },
        "campaign": campaign,
        "summary": {
            "skillCount": len(skills),
            "probeCount": len(probes),
            "roleCount": len(roles),
            "suiteCount": len(agents),
            "currentScenarioCount": len(current_scenarios),
            "directGovernedSkillCount": classifications["direct-governed"],
            "directProbeSkillCount": classifications["direct-probe"],
            "indirectOnlySkillCount": classifications["indirect-only"],
            "noRecordedEvidenceSkillCount": classifications["none"],
            "skillsWithGovernedLinks": sum(
                bool(skill["governedScenarioLinks"]) for skill in skills
            ),
            "skillsWithoutGovernedLinks": sum(
                not skill["governedScenarioLinks"] for skill in skills
            ),
            "historicalIdOnlyResults": evidence_counts["historical-id-only"],
            "snapshotAlignedResults": evidence_counts["historical-snapshot-aligned"],
            "definitionDriftResults": evidence_counts["historical-drift"],
            "removedCampaignResults": evidence_counts["historical-removed"],
            "missingScenarioResults": missing_results,
            "historicalUnknownSuiteResults": sum(
                agent["freshness"] == "historical-unknown" for agent in agents
            ),
            "snapshotAlignedSuiteResults": sum(
                agent["freshness"] == "snapshot-aligned" for agent in agents
            ),
            "definitionDriftSuiteResults": sum(
                agent["freshness"] == "historical-drift" for agent in agents
            ),
            "missingSuiteResults": sum(agent["freshness"] == "missing" for agent in agents),
        },
        "skills": skills,
        "agents": agents,
    }


def escape(value: object) -> str:
    """Escape one source value for safe static HTML text or attributes."""
    return html.escape(str(value), quote=True)


def source_link(path: str, label: str | None = None) -> str:
    """Render one repository-local source link from the design directory."""
    return f'<a href="../{escape(path)}">{escape(label or path)}</a>'


def status_badge(label: str, status: str) -> str:
    """Render a text-bearing status badge whose meaning does not depend on color."""
    return f'<span class="status status--{escape(status.lower())}">{escape(label)}</span>'


def percent(numerator: int, denominator: int) -> str:
    """Format a source-derived percentage with one decimal place."""
    return "0.0%" if denominator == 0 else f"{numerator / denominator:.1%}"


def render_skill_card(skill: dict[str, object]) -> str:
    """Render one complete static skill entry with probe and campaign limitations."""
    probe = skill["probe"]
    if not isinstance(probe, dict):
        probe_html = (
            f'<p>{status_badge("No direct probe declaration", "missing")}</p>'
            "<p>No diagnostic probe is declared for this skill.</p>"
        )
        probe_id = "none"
    else:
        executable_cases = probe.get("executableCases", [])
        cases = ", ".join(
            source_link("evals/cases.yaml", str(case)) for case in executable_cases
        ) or "None declared"
        scenario_associations = ", ".join(
            source_link("evals/agent-scenarios.yaml", str(value))
            for value in probe.get("scenarioAssociations", [])
        ) or "None declared"
        workflow_associations = ", ".join(
            source_link("evals/workflow-packs.yaml", str(value))
            for value in probe.get("workflowAssociations", [])
        ) or "None declared"
        deterministic = probe.get("judgePlan", {}).get("deterministicChecks", [])
        model_rubric = probe.get("judgePlan", {}).get("modelRubric")
        probe_html = f"""
        <dl class="compact-list">
          <div><dt>Probe</dt><dd>{source_link('evals/skill-probes.yaml', str(probe['id']))}</dd></div>
          <div><dt>Coverage state</dt><dd>{escape(probe.get('coverageStatus', 'Not declared'))}: catalog declaration, not a verified run</dd></div>
          <div><dt>Kind</dt><dd>{escape(probe.get('evaluationKind', 'Not declared'))}</dd></div>
          <div><dt>Executable cases</dt><dd>{cases}</dd></div>
          <div><dt>Scenario associations</dt><dd>{scenario_associations}</dd></div>
          <div><dt>Workflow associations</dt><dd>{workflow_associations}</dd></div>
          <div><dt>Deterministic checks</dt><dd>{escape(', '.join(deterministic) or 'None declared')}</dd></div>
          <div><dt>Model rubric</dt><dd>{escape(model_rubric or 'None; deterministic plan only')}</dd></div>
        </dl>
        """
        probe_id = str(probe["id"])

    links = skill["governedScenarioLinks"]
    if links:
        link_items = "".join(
            "<li>"
            + source_link(
                str(item["scenarioPath"]),
                f"{item['suite']} / {item['scenario']}",
            )
            + " &mdash; "
            + status_badge(str(item["campaignVerdict"]), str(item["campaignVerdict"]))
            + " "
            + status_badge(
                {
                    "historical-id-only": "Historical ID alignment; definition freshness unknown",
                    "historical-snapshot-aligned": "Historical snapshot aligned",
                    "historical-drift": "Historical definition drift",
                    "historical-removed": "Campaign-only / removed",
                }.get(str(item["evidenceState"]), "Missing campaign evidence"),
                str(item["evidenceState"]),
            )
            + "</li>"
            for item in links
        )
        governed_html = f"<ul class=\"link-list\">{link_items}</ul>"
    else:
        governed_html = (
            f'<p>{status_badge("No selected Campaign scenario link", "missing")}</p>'
            "<p>No scenario in the selected Campaign currently names this skill as a target skill.</p>"
        )

    search_text = " ".join(
        [
            str(skill["id"]),
            str(skill["description"]),
            str(skill["category"]),
            probe_id,
            str(skill["latestGovernedOutcome"]),
        ]
    ).lower()
    coverage_labels = {
        "direct-governed": "Direct governed skill result",
        "direct-probe": "Direct diagnostic probe declaration",
        "indirect-only": "Indirect agent-scenario evidence only",
        "none": "No recorded evaluation evidence",
    }
    return f"""
    <article class="evaluation-card skill-card" id="skill-{escape(skill['id'])}"
      data-kind="skill" data-status="{escape(skill['classification'])}" data-search="{escape(search_text)}">
      <div class="card-heading">
        <div><span class="card-kicker">Skill</span><h3>{escape(skill['id'])}</h3></div>
        {status_badge(coverage_labels[str(skill['classification'])], str(skill['classification']))}
      </div>
      <p>{escape(skill['description'])}</p>
      <p class="source-row">{source_link(str(skill['sourcePath']), 'Skill source')}</p>
      <h4>Direct diagnostic probe declaration</h4>
      {probe_html}
      <h4>Selected Campaign scenario links</h4>
      {governed_html}
      <dl class="compact-list">
        <div><dt>Linked Campaign Evaluation results</dt><dd>{escape(skill['latestGovernedOutcome'])}</dd></div>
        <div><dt>Evidence level</dt><dd>Agent-scenario evidence only; no skill-level Evaluation result</dd></div>
        <div><dt>Limitation</dt><dd>{escape(skill['limitation'])}</dd></div>
      </dl>
    </article>
    """


def render_agent_card(agent: dict[str, object], campaign: dict[str, object]) -> str:
    """Render one current conceptual agent and every current scenario evidence state."""
    freshness_labels = {
        "historical-unknown": "Historical ID alignment; definition freshness unknown",
        "snapshot-aligned": "Historical snapshot aligned",
        "historical-drift": "Historical definition drift",
        "missing": "Missing campaign evidence",
    }
    scenario_evidence_labels = {
        "historical-id-only": "Historical ID alignment; definition freshness unknown",
        "historical-snapshot-aligned": "Historical snapshot aligned",
        "historical-drift": "Historical definition drift",
        "historical-removed": "Campaign-only / removed from current catalog",
        "missing": "Missing campaign evidence",
    }
    scenario_rows = []
    for scenario in agent["scenarios"]:
        verdict = scenario["campaignVerdict"]
        verdict_html = (
            status_badge(str(verdict), str(verdict))
            if verdict is not None
            else status_badge("Missing campaign evidence", "missing")
        )
        alignment_html = status_badge(
            scenario_evidence_labels[str(scenario["evidenceState"])],
            str(scenario["evidenceState"]),
        )
        drift_html = (
            escape(", ".join(scenario["driftFields"]))
            if scenario["driftFields"]
            else "None proved"
        )
        scenario_rows.append(
            f"""
            <tr data-campaign-verdict="{escape(verdict or '')}">
              <th scope="row">{escape(scenario['id'])}</th>
              <td>{escape(scenario['purpose'])}</td>
              <td>{escape(scenario['expectedTerminalStatus'])}</td>
              <td>{verdict_html}</td>
              <td>{alignment_html}</td>
              <td>{escape(scenario['catalogState'])}</td>
              <td>{drift_html}</td>
            </tr>
            """
        )
    verdict_text = ", ".join(
        f"{verdict} {agent['campaignVerdicts'][verdict]}" for verdict in VERDICTS
    )
    unresolved = []
    if agent["campaignVerdicts"]["FAIL"]:
        unresolved.append(
            f"{agent['campaignVerdicts']['FAIL']} FAIL Evaluation result(s)"
        )
    if agent["campaignVerdicts"]["BLOCKED"]:
        unresolved.append(
            f"{agent['campaignVerdicts']['BLOCKED']} BLOCKED Evaluation result(s)"
        )
    if agent["missingScenarioCount"]:
        unresolved.append(f"{agent['missingScenarioCount']} current scenario(s) without campaign evidence")
    if agent["freshness"] == "historical-unknown":
        unresolved.append("campaign did not retain scenario definitions or their digests")
    if agent["freshness"] == "historical-drift":
        unresolved.append("campaign and current scenario catalogs do not align")
    if agent["removedScenarioCount"]:
        unresolved.append(f"{agent['removedScenarioCount']} campaign-only row(s)")
    if not unresolved:
        unresolved.append("No unresolved result category recorded in the selected campaign")
    search_text = " ".join(
        [
            str(agent["id"]),
            str(agent["description"]),
            str(agent["freshness"]),
            *(str(scenario["id"]) for scenario in agent["scenarios"]),
            verdict_text,
        ]
    ).lower()
    followup_html = ""
    if agent["followUps"]:
        followup_html = "<h4>Recorded agent-mapped follow-ups</h4><ul class=\"link-list\">" + "".join(
            f"<li>{source_link(str(item['sourcePath']), str(item['title']))}</li>"
            for item in agent["followUps"]
        ) + "</ul>"
    return f"""
    <article class="evaluation-card agent-card" id="agent-{escape(agent['id'])}"
      data-kind="agent" data-status="{escape(agent['freshness'])}" data-search="{escape(search_text)}">
      <div class="card-heading">
        <div><span class="card-kicker">Conceptual agent</span><h3>{escape(agent['id'])}</h3></div>
        {status_badge(freshness_labels[str(agent['freshness'])], str(agent['freshness']))}
      </div>
      <p>{escape(agent['description'])}</p>
      <p class="source-row">
        {source_link(str(agent['sourcePath']), 'Role source')} &middot;
        {source_link(str(agent['suitePath']), 'Suite')} &middot;
        {source_link(str(agent['scenariosPath']), 'Scenarios')}
      </p>
      <dl class="compact-list">
        <div><dt>Campaign Evaluation result aggregate</dt><dd>{escape(verdict_text)}</dd></div>
        <div><dt>Evidence level</dt><dd>{escape(campaign['evidenceLevel'])}; scenario Evaluation results are not skill Evaluation results</dd></div>
        <div><dt>Execution context</dt><dd>{escape(campaign['harness'])}; disposable synthetic workspaces; per-scenario containment not reported</dd></div>
        <div><dt>Judge dimension</dt><dd>Governed Judge workflow or proved deterministic boundary; raw per-scenario Judge and calibration fields are not published in this report</dd></div>
        <div><dt>Unresolved</dt><dd>{escape('; '.join(unresolved))}</dd></div>
      </dl>
      {followup_html}
      <div class="table-scroll" tabindex="0" aria-label="Scenario results for {escape(agent['id'])}">
        <table>
          <thead><tr><th>Scenario</th><th>Purpose</th><th>Expected target status</th><th>Evaluation result</th><th>Evidence alignment</th><th>Catalog state</th><th>Proved drift fields</th></tr></thead>
          <tbody>{''.join(scenario_rows)}</tbody>
        </table>
      </div>
    </article>
    """


def render_page(model: dict[str, object]) -> str:
    """Render the maintained static-first evaluation documentation page."""
    summary = model["summary"]
    campaign = model["campaign"]
    skills_html = "".join(render_skill_card(skill) for skill in model["skills"])
    agents_html = "".join(render_agent_card(agent, campaign) for agent in model["agents"])
    verdict_cards = "".join(
        f"""
        <article class="metric"><strong>{escape(campaign['verdicts'][verdict])}</strong>
        <span>{verdict} ({percent(campaign['verdicts'][verdict], campaign['scenarioCount'])})</span></article>
        """
        for verdict in VERDICTS
    )
    followups_html = "".join(
        "<li>"
        + source_link(str(item["sourcePath"]), str(item["title"]))
        + " &mdash; "
        + (
            status_badge(f"Agent mapping: {item['agent']}", "declared")
            if item["agent"]
            else status_badge(
                "Campaign-wide; the report does not map this correction to one agent",
                "historical-id-only",
            )
        )
        + "</li>"
        for item in campaign["followUps"]
    )
    page = f"""<!doctype html>
{EVALUATION_PAGE_PROVENANCE}
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Agent and Skill Evaluations</title>
  <style>
    :root {{
      --ink: #172033; --muted: #536079; --page: #f2f5f8; --panel: #ffffff;
      --line: #cbd5e1; --navy: #17406d; --teal: #006b67; --amber: #8a4b00;
      --red: #9f2431; --green: #17633b; --violet: #5a3b8a; --soft-blue: #e5eef8;
      --soft-teal: #def2ef; --soft-amber: #fff0d2; --soft-red: #fbe4e7;
      --soft-violet: #eee8f7; --soft-gray: #edf1f5; --shadow: 0 14px 36px rgba(23,32,51,.08);
      --radius: .7rem; --content: 1240px;
    }}
    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{ margin: 0; color: var(--ink); background: linear-gradient(180deg,#e5eef8 0,transparent 25rem),var(--page); font-family: Inter,ui-sans-serif,system-ui,sans-serif; line-height: 1.55; }}
    a {{ color: var(--navy); }}
    a:focus-visible, button:focus-visible, input:focus-visible, select:focus-visible, [tabindex="0"]:focus-visible {{ outline: 3px solid #b35f00; outline-offset: 3px; }}
    h1,h2,h3,h4 {{ margin: 0; line-height: 1.15; }}
    h1 {{ max-width: 900px; font-size: clamp(2.5rem,6vw,5rem); }}
    h2 {{ font-size: clamp(1.8rem,4vw,3rem); }}
    h3 {{ overflow-wrap: anywhere; font-size: 1.25rem; }}
    h4 {{ margin-top: .4rem; font-size: .93rem; text-transform: uppercase; letter-spacing: .04em; }}
    p {{ margin: 0; color: var(--muted); }}
    p + p {{ margin-top: .65rem; }}
    .site-header, main, .site-footer {{ width: min(100% - 2rem,var(--content)); margin-inline: auto; }}
    .site-header {{ display: flex; align-items: center; gap: .75rem; padding-top: 1.2rem; }}
    .site-brand {{ display: inline-flex; min-width: 0; align-items: center; gap: .75rem; color: var(--ink); font-weight: 800; text-decoration: none; }}
    .site-logo {{ width: 2.35rem; height: 2.35rem; border-radius: .45rem; }}
    main {{ padding: 2rem 0 5rem; }}
    .document-nav, .document-sequence {{ display: flex; flex-wrap: wrap; gap: .65rem; }}
    .document-nav {{ justify-content: space-between; margin-bottom: 3rem; }}
    .document-nav a {{ padding: .5rem .8rem; border: 1px solid var(--line); border-radius: 999px; background: rgba(255,255,255,.8); color: var(--muted); font-size: .86rem; font-weight: 750; text-decoration: none; }}
    .hero {{ display: grid; gap: 1.4rem; padding: clamp(2rem,6vw,5rem) 0 2rem; }}
    .eyebrow, .card-kicker {{ color: var(--teal); font-size: .78rem; font-weight: 850; letter-spacing: .08em; text-transform: uppercase; }}
    .lede {{ max-width: 900px; font-size: 1.15rem; }}
    .scope-note {{ max-width: 980px; padding: 1rem 1.2rem; border-left: .35rem solid var(--amber); background: var(--panel); box-shadow: var(--shadow); }}
    .chapter-nav {{ position: sticky; top: 0; z-index: 5; display: flex; gap: .35rem; margin: 1rem 0 4rem; padding: .55rem; overflow-x: auto; border: 1px solid var(--line); border-radius: 999px; background: rgba(255,255,255,.94); box-shadow: var(--shadow); }}
    .chapter-nav a {{ flex: 0 0 auto; padding: .5rem .75rem; border-radius: 999px; color: var(--muted); font-size: .8rem; font-weight: 800; text-decoration: none; }}
    .chapter-nav a:hover {{ background: var(--soft-teal); color: var(--teal); }}
    .section {{ margin-top: clamp(4rem,9vw,7rem); scroll-margin-top: 6rem; }}
    .section-heading {{ display: grid; gap: .65rem; max-width: 850px; margin-bottom: 2rem; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit,minmax(min(100%,18rem),1fr)); gap: 1rem; }}
    .metric, .method-card, .evaluation-card, .filters {{ border: 1px solid var(--line); border-radius: var(--radius); background: var(--panel); box-shadow: var(--shadow); }}
    .metric {{ display: grid; gap: .2rem; padding: 1.2rem; }}
    .metric strong {{ font-size: 2rem; }}
    .metric span {{ color: var(--muted); font-weight: 700; }}
    .method-card {{ padding: 1.2rem; }}
    .method-card h3 {{ margin-bottom: .55rem; }}
    .method-card ul {{ margin-bottom: 0; padding-left: 1.2rem; color: var(--muted); }}
    .legend {{ display: flex; flex-wrap: wrap; gap: .55rem; margin-top: 1rem; }}
    .status {{ display: inline-flex; width: fit-content; max-width: 100%; box-sizing: border-box; align-items: center; padding: .25rem .55rem; border: 1px solid currentColor; border-radius: 999px; background: var(--soft-gray); color: var(--navy); font-size: .76rem; font-weight: 850; white-space: nowrap; }}
    .status--pass, .status--snapshot-aligned, .status--historical-snapshot-aligned {{ background: var(--soft-teal); color: var(--green); }}
    .status--fail {{ background: var(--soft-red); color: var(--red); }}
    .status--blocked, .status--historical-drift, .status--historical-removed {{ background: var(--soft-amber); color: var(--amber); }}
    .status--missing, .status--none {{ background: var(--soft-violet); color: var(--violet); }}
    .status--declared, .status--historical-id-only, .status--historical-unknown, .status--direct-probe, .status--direct-governed, .status--indirect-only {{ background: var(--soft-blue); color: var(--navy); }}
    .filters {{ display: grid; grid-template-columns: minmax(12rem,1fr) minmax(11rem,.35fr) auto; gap: 1rem; align-items: end; margin-bottom: 1.2rem; padding: 1rem; }}
    .field {{ display: grid; gap: .35rem; color: var(--ink); font-weight: 750; }}
    input, select, button {{ min-height: 2.65rem; padding: .5rem .65rem; border: 1px solid #8492a6; border-radius: .4rem; background: white; color: var(--ink); font: inherit; }}
    button {{ cursor: pointer; font-weight: 800; }}
    .result-count {{ min-height: 1.6rem; margin-bottom: 1rem; color: var(--muted); }}
    .catalog {{ display: grid; gap: 1rem; }}
    .evaluation-card {{ display: grid; min-width: 0; gap: 1rem; padding: clamp(1rem,2.5vw,1.5rem); scroll-margin-top: 6rem; }}
    .evaluation-card[hidden] {{ display: none; }}
    .card-heading {{ display: flex; min-width: 0; flex-wrap: wrap; justify-content: space-between; gap: 1rem; align-items: start; }}
    .card-heading > * {{ min-width: 0; }}
    .source-row {{ font-size: .88rem; }}
    .compact-list {{ display: grid; margin: 0; border-top: 1px solid var(--line); }}
    .compact-list div {{ display: grid; grid-template-columns: minmax(10rem,.3fr) minmax(0,1fr); gap: 1rem; padding: .65rem 0; border-bottom: 1px solid var(--line); }}
    .compact-list dt {{ font-weight: 800; }}
    .compact-list dd {{ margin: 0; color: var(--muted); overflow-wrap: anywhere; }}
    .link-list {{ margin: 0; padding-left: 1.2rem; color: var(--muted); }}
    .table-scroll {{ overflow-x: auto; }}
    table {{ width: 100%; min-width: 52rem; border-collapse: collapse; font-size: .88rem; }}
    th,td {{ padding: .7rem; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; }}
    th {{ color: var(--ink); }}
    td {{ color: var(--muted); }}
    .site-footer {{ padding: 1.5rem 0 3rem; border-top: 1px solid var(--line); }}
    @media (max-width: 720px) {{
      .chapter-nav {{ position: static; border-radius: var(--radius); }}
      .filters {{ grid-template-columns: 1fr; }}
      .compact-list div {{ grid-template-columns: 1fr; gap: .2rem; }}
      .status {{ overflow-wrap: anywhere; white-space: normal; }}
    }}
    @media print {{ .chapter-nav,.filters,.document-nav {{ display: none; }} body {{ background: white; }} .evaluation-card {{ break-inside: avoid; box-shadow: none; }} }}
  </style>
</head>
<body>
<header class="site-header">
  <a class="site-brand" href="../index.html"><img class="site-logo" src="../logo.png" alt="DevConsult Canada logo"><span>AI-Assisted Coding Toolkit Index</span></a>
</header>
<main>
  <nav class="document-nav" aria-label="Documentation navigation">
    <div class="document-sequence">
      <a href="agent-and-skill-definitions.html" rel="prev"><span aria-hidden="true">&larr;</span> Previous: Core Agent and Skills</a>
      <a href="agent-owned-evaluation-suites.html" rel="next">Next: Agent-Owned Evaluation Suites <span aria-hidden="true">&rarr;</span></a>
    </div>
  </nav>
  <section class="hero" aria-labelledby="page-title">
    <span class="eyebrow">Evaluation evidence</span>
    <h1 id="page-title">Agent and Skill Evaluations</h1>
    <p class="lede">Current catalogs and one selected historical Campaign Test report show how the bundle is evaluated. The page keeps catalog coverage, historical Evaluation results, definition freshness, and missing evidence separate.</p>
    <p class="scope-note"><strong>Evidence boundary.</strong> Probe declarations describe diagnostic plans. Linked agent-scenario Evaluation results do not establish skill-level Evaluation results. Historical alignment, result categories, manual observations, Judge results, calibration, functional isolation, and security containment remain separate evidence dimensions.</p>
  </section>
  <nav class="chapter-nav" aria-label="Page sections">
    <a href="#methodology">Purpose and method</a><a href="#coverage">Coverage and cases</a><a href="#campaign">Campaign Evaluation results</a><a href="#limitations">Limitations</a><a href="#history">Historical evidence</a><a href="#agents">Agents</a><a href="#skills">Skills</a><a href="#follow-ups">Follow-ups</a><a href="#sources">Sources</a>
  </nav>

  <section class="section" id="methodology" aria-labelledby="methodology-title">
    <div class="section-heading"><h2 id="methodology-title">Evaluation purpose and method</h2><p>The current methodology separates structural checks, agent behavior, targeted skill diagnostics, and multi-agent Workflow evidence. Deterministic Judges run before semantic judgment.</p></div>
    <div class="grid">
      <article class="method-card"><h3>Evaluation layers</h3><ul><li>Structural validation checks suite structure, catalogs, source references, harness policy, executable-case links, and current digests.</li><li>Agent suites check responsibility, output contracts, mutation policy, decisions, delegation, failure handling, and terminal outcomes.</li><li>Skill probes diagnose activation, negative activation, expected behavior, and ablation controls. They are not exhaustive skill verification.</li><li>Workflow evidence checks delegation, handoffs, claims, integration, verification, and terminal status across allowed dependencies.</li></ul></article>
      <article class="method-card"><h3>Harness, workspace, and privacy</h3><ul><li>The current evaluation system supports Codex and Junie.</li><li>Ordinary cases use disposable workspaces with controlled harness state and synthetic inputs.</li><li>Inputs must exclude personal, customer, company-confidential, credential, and secret material.</li><li>Functional isolation compares complete before-and-after workspace manifests with the allowed-write contract.</li><li>Security containment is a separate claim. Local reproducibility or a tool allowlist does not prove hostile-code containment.</li></ul></article>
      <article class="method-card"><h3>Current protocol and selected-report results</h3><ul><li><strong>Current PASS:</strong> Every critical deterministic gate passed, and the required semantic Judge accepted the run.</li><li><strong>Current FAIL:</strong> Governed evidence demonstrates a target-agent contract violation.</li><li><strong>Current BLOCKED:</strong> The run could not reach a verdict because a required dependency, harness feature, fixture capability, or approved authority was unavailable.</li><li><strong>Current STALE:</strong> A governed source, adapter, scenario, fixture, rubric, or evidence digest no longer matches the run.</li><li><strong>Selected 2026 Test report PASS:</strong> The Test suite accepted the target behavior. A target can correctly return BLOCKED inside a PASS when a scenario tests a governed boundary.</li><li><strong>Selected 2026 Test report FAIL:</strong> The report records a reproducible target, skill, or test-contract defect.</li><li><strong>Selected 2026 Test report BLOCKED:</strong> The report records a governed boundary or unavailable semantic acceptance. All 78 report scenarios were executed.</li><li>A critical Deterministic Judge failure skips semantic judgment. It does not mean that a Model Judge passed.</li><li>Human Judges create calibration labels and adjudicate ambiguity. Calibration promotion is disabled, so the current state is <strong>Uncalibrated Model Judge</strong>.</li></ul></article>
    </div>
  </section>

  <section class="section" id="coverage" aria-labelledby="coverage-title">
    <div class="section-heading"><h2 id="coverage-title">Coverage and case catalogs</h2><p>Current catalog inventory remains separate from the selected historical Campaign Evaluation results. Probe records retain executable-case, agent-scenario, and Workflow associations without turning declarations into verified runs.</p></div>
    <h3>Current catalog inventory</h3>
    <div class="grid" style="margin-top:1rem">
      <article class="metric"><strong>{summary['skillCount']}</strong><span>Bundled skills</span></article>
      <article class="metric"><strong>{summary['probeCount']}</strong><span>Diagnostic probe records</span></article>
      <article class="metric"><strong>{summary['roleCount']}</strong><span>Conceptual agents</span></article>
      <article class="metric"><strong>{summary['suiteCount']}</strong><span>Current Test suites</span></article>
      <article class="metric"><strong>{summary['currentScenarioCount']}</strong><span>Current Test suite scenarios</span></article>
    </div>
    <div style="margin-top:2rem"><h3>Case and workflow catalogs</h3></div>
    <div class="grid" style="margin-top:1rem">
      <article class="metric"><strong>{model['associationCatalogCounts']['cases']}</strong><span>Executable cases</span></article>
      <article class="metric"><strong>{model['associationCatalogCounts']['agentScenarios']}</strong><span>Agent scenarios</span></article>
      <article class="metric"><strong>{model['associationCatalogCounts']['workflowPacks']}</strong><span>Workflow packs</span></article>
    </div>
    <div class="grid" style="margin-top:1rem">
      <article class="method-card"><h3>Skill catalog states</h3><ul><li>{summary['directGovernedSkillCount']} skills have a direct governed Evaluation result.</li><li>{summary['directProbeSkillCount']} skills have a direct diagnostic probe declaration but no direct Evaluation result.</li><li>{summary['indirectOnlySkillCount']} skills have only indirect current Test suite coverage without a direct probe or Evaluation result.</li><li>{summary['noRecordedEvidenceSkillCount']} skills have no recorded evaluation evidence.</li><li>{summary['skillsWithGovernedLinks']} skills are named by at least one scenario in the selected Campaign; {summary['skillsWithoutGovernedLinks']} are not.</li></ul><p><strong>No skill-level Evaluation result:</strong> The selected Test report publishes no skill-level Evaluation results. Linked PASS results remain agent-scenario evidence.</p></article>
    </div>
  </section>

  <section class="section" id="campaign" aria-labelledby="campaign-title">
    <div class="section-heading"><h2 id="campaign-title">Selected Campaign Test report and Evaluation results</h2><p>The generator selects one governed Test report by path. It does not infer selection from filename order or merge multiple Campaigns. Current catalog coverage is calculated separately.</p></div>
    <h3>Test report metadata</h3>
    <dl class="compact-list">
      <div><dt>Test report</dt><dd>{source_link(str(campaign['sourcePath']), 'Complete Agent Suite Results')}</dd></div>
      <div><dt>Execution range</dt><dd>{escape(campaign['dateRange'])}</dd></div>
      <div><dt>Harness</dt><dd>{escape(campaign['harness'])}</dd></div>
      <div><dt>Runtime</dt><dd>{escape(campaign['runtime'])}</dd></div>
      <div><dt>Evidence level</dt><dd>{escape(campaign['evidenceLevel'])}</dd></div>
      <div><dt>Source snapshot mode</dt><dd>{escape(model['snapshotMetadata']['mode'])}</dd></div>
      <div><dt>Wall-clock build time</dt><dd>Not retained; deterministic output does not claim an unsupported generation timestamp</dd></div>
      <div><dt>Current source digest</dt><dd><code>{escape(model['sourceDigest'])}</code>; regenerated and compared by the focused check</dd></div>
    </dl>
    <div style="margin-top:2rem"><h3>Evaluation results</h3></div>
    <div class="grid" style="margin-top:1rem">
      <article class="metric"><strong>{campaign['suiteCount']} / {summary['suiteCount']}</strong><span>Selected-report Test suites / current Test suites ({percent(campaign['suiteCount'], summary['suiteCount'])})</span></article>
      <article class="metric"><strong>{campaign['scenarioCount']} / {summary['currentScenarioCount']}</strong><span>Selected-report Evaluation results / current scenarios ({percent(campaign['scenarioCount'], summary['currentScenarioCount'])})</span></article>
      {verdict_cards}
    </div>
  </section>

  <section class="section" id="limitations" aria-labelledby="limitations-title">
    <div class="section-heading"><h2 id="limitations-title">Evidence limitations</h2><p>Result categories, harness context, containment claims, and skill-level evidence remain separate so the page does not promote incomplete evidence to a verified pass.</p></div>
    <div class="grid">
      <article class="method-card"><h3>Harness and evidence breakdown</h3><ul><li>{campaign['scenarioCount']} selected-report scenario results use {escape(campaign['harness'])} at the {escape(campaign['evidenceLevel'])} evidence level.</li><li>{summary['missingScenarioResults']} current scenarios have no result in the selected Test report.</li><li>Per-scenario functional-isolation and security-containment fields are not published in the selected Test report. The report states clean suite-owned closeout globally.</li></ul></article>
      <article class="method-card"><h3>Evidence that does not prove a pass</h3><ul><li>The selected Test report contains {campaign['verdicts']['BLOCKED']} BLOCKED results. They are governed boundaries or unavailable semantic acceptance, not PASS or FAIL.</li><li>The selected Test report contains {campaign['verdicts']['FAIL']} FAIL results. They are reproducible defects, not verified passes.</li><li>Missing, historical-only, removed, or drifted current-catalog evidence does not inherit a current PASS.</li><li>Manual observations and uncalibrated semantic Judge results do not establish verified passes.</li></ul></article>
    </div>
    <div class="legend" aria-label="Status legend">
      {status_badge('PASS', 'pass')}{status_badge('FAIL', 'fail')}{status_badge('BLOCKED', 'blocked')}{status_badge('Missing campaign evidence', 'missing')}{status_badge('Historical ID alignment; definition freshness unknown', 'historical-id-only')}{status_badge('Campaign-only / removed', 'historical-removed')}{status_badge('Diagnostic declaration', 'declared')}
    </div>
  </section>

  <section class="section" id="history" aria-labelledby="history-title">
    <div class="section-heading"><h2 id="history-title">Historical evidence alignment</h2><p>Historical Campaign Evaluation results remain visible, while current definition freshness and current-scenario gaps are reported separately.</p></div>
    <div class="grid">
      <article class="method-card"><h3>Alignment and strength</h3><ul><li><strong>Historical ID alignment; definition freshness unknown</strong> means the current catalog and Campaign ledger share a scenario ID, but the Test report retained no scenario-definition snapshot or digest.</li><li>Historical snapshot aligned is available only when a retained definition proves that <code>purpose</code>, <code>expectedTerminalStatus</code>, and <code>targetSkills</code> match.</li><li>Historical definition drift lists proved differences in those fields. Campaign-only / removed rows remain visible.</li><li>Missing Campaign evidence means that the current scenario has no result in the selected Test report.</li><li>A Manual observation in an older report is historical context, not governed verification.</li></ul></article>
      <article class="method-card"><h3>Evidence alignment states</h3><ul><li>{summary['historicalIdOnlyResults']} Evaluation results have only historical id alignment; definition freshness is unknown.</li><li>{summary['snapshotAlignedResults']} Evaluation results are aligned to a retained definition snapshot.</li><li>{summary['definitionDriftResults']} Evaluation results have proved definition-field drift.</li><li>{summary['removedCampaignResults']} Campaign Evaluation results are Campaign-only / removed from the current catalog.</li><li>{summary['missingScenarioResults']} current scenarios have missing Campaign evidence.</li><li>{summary['historicalUnknownSuiteResults']} Test suites are historical-unknown, {summary['snapshotAlignedSuiteResults']} snapshot-aligned, {summary['definitionDriftSuiteResults']} drifted, and {summary['missingSuiteResults']} missing.</li></ul></article>
    </div>
  </section>

  <section class="section" id="agents" aria-labelledby="agents-title">
    <div class="section-heading"><h2 id="agents-title">Agent-by-agent evidence</h2><p>All current conceptual agents are present. Each card includes current scenarios, any Campaign-only row, the expected target status when retained, the selected-report Evaluation result, evidence alignment, sources, and unresolved findings.</p></div>
    <div class="filters" data-filter-scope="agent">
      <label class="field" for="agent-search">Search agents or scenarios<input id="agent-search" type="search" autocomplete="off" data-filter-search="agent"></label>
      <label class="field" for="agent-status">Evidence status<select id="agent-status" data-filter-status="agent"><option value="all">All statuses</option><option value="historical-unknown">Historical, definition unknown</option><option value="snapshot-aligned">Snapshot aligned</option><option value="historical-drift">Definition drift</option><option value="missing">Missing</option></select></label>
      <button type="button" data-filter-clear="agent">Clear agent filters</button>
    </div>
    <p class="result-count" id="agent-result-count" aria-live="polite">Showing all {summary['roleCount']} agents.</p>
    <noscript><p class="scope-note">JavaScript is disabled. All agent entries remain visible; text and status filtering are optional enhancements.</p></noscript>
    <div class="catalog" id="agent-catalog">{agents_html}</div>
  </section>

  <section class="section" id="skills" aria-labelledby="skills-title">
    <div class="section-heading"><h2 id="skills-title">Skill-by-skill evidence</h2><p>All bundled skills are present. Direct diagnostic probe declarations, linked selected-report scenarios, linked Evaluation result categories, evidence level, sources, and limitations remain distinct.</p></div>
    <div class="filters" data-filter-scope="skill">
      <label class="field" for="skill-search">Search skills or probes<input id="skill-search" type="search" autocomplete="off" data-filter-search="skill"></label>
      <label class="field" for="skill-status">Coverage status<select id="skill-status" data-filter-status="skill"><option value="all">All statuses</option><option value="direct-governed">Direct governed Evaluation result</option><option value="direct-probe">Direct diagnostic probe</option><option value="indirect-only">Indirect Test suite only</option><option value="none">No recorded evidence</option></select></label>
      <button type="button" data-filter-clear="skill">Clear skill filters</button>
    </div>
    <p class="result-count" id="skill-result-count" aria-live="polite">Showing all {summary['skillCount']} skills.</p>
    <noscript><p class="scope-note">JavaScript is disabled. All skill entries remain visible; text and status filtering are optional enhancements.</p></noscript>
    <div class="catalog" id="skill-catalog">{skills_html}</div>
  </section>

  <section class="section" id="follow-ups" aria-labelledby="follow-ups-title">
    <div class="section-heading"><h2 id="follow-ups-title">Recorded Campaign follow-ups</h2><p>The selected report records {len(campaign['followUps'])} linked correction items. Only explicit narrative mappings are attached to an Agent. All other items remain Campaign-wide.</p></div>
    <ol class="link-list">{followups_html}</ol>
  </section>

  <section class="section" id="sources" aria-labelledby="sources-title">
    <div class="section-heading"><h2 id="sources-title">Authoritative sources</h2><p>Tracked repository artifacts remain authoritative. Temporary retained-summary paths named in the historical Test report are context, not the only support for any statistic on this page.</p></div>
    <div class="grid">
      <article class="method-card"><h3>Method and catalogs</h3><ul><li>{source_link('evals/README.md', 'Evaluation methodology')}</li><li>{source_link('evals/agent-tests/AGENTS.md', 'Current Agent Test Suite Protocol')}</li><li>{source_link('evals/agent-tests/README.md', 'Agent-Owned Evaluation Suites strategy')}</li><li>{source_link('evals/skill-probes.yaml', 'Skill probe catalog')}</li><li>{source_link('evals/cases.yaml', f"Executable cases ({model['associationCatalogCounts']['cases']})")}</li><li>{source_link('evals/agent-scenarios.yaml', f"Agent scenarios ({model['associationCatalogCounts']['agentScenarios']})")}</li><li>{source_link('evals/workflow-packs.yaml', f"Workflow packs ({model['associationCatalogCounts']['workflowPacks']})")}</li><li>{source_link('evals/agent-tests/suite-index.yaml', 'Agent suite index')}</li><li>{source_link('evals/judges.yaml', 'Judge catalog and calibration policy')}</li></ul></article>
      <article class="method-card"><h3>Results</h3><ul><li>{source_link(str(campaign['sourcePath']), 'Selected Campaign Test report')}</li><li>{source_link('evals/results/2026-07-09-live-agent-evaluations.md', 'Older Manual observation report')}</li></ul><p>The older report is not merged into the selected Campaign totals.</p></article>
    </div>
  </section>
</main>
<footer class="site-footer"><p>Copyright (c) 2026 Martin.Bechard@DevConsult.ca - <a href="../LICENSE">MIT License</a></p></footer>
<script src="documentation-settings.js"></script>
<script src="agent-and-skill-evaluations.js"></script>
</body>
</html>
"""
    return "\n".join(line.rstrip() for line in page.splitlines()) + "\n"


def write_or_check(output_path: Path, content: str, check: bool) -> int:
    """Write generated HTML or report whether the tracked output is source-current."""
    if check:
        if not output_path.exists() or output_path.read_text(encoding="utf-8") != content:
            print(
                f"Evaluation documentation is stale: run {Path(__file__).name}",
                file=sys.stderr,
            )
            return ERROR_EXIT_CODE
        print(f"Evaluation documentation is up to date: {output_path.relative_to(REPOSITORY_ROOT)}")
        return SUCCESS_EXIT_CODE
    output_path.write_text(content, encoding="utf-8")
    print(f"Wrote {output_path.relative_to(REPOSITORY_ROOT)}")
    return SUCCESS_EXIT_CODE


def main(argv: Sequence[str] | None = None) -> int:
    """Generate the evaluation page or validate its deterministic freshness."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail when generated HTML differs")
    arguments = parser.parse_args(argv)
    model = build_model(REPOSITORY_ROOT)
    return write_or_check(OUTPUT_PATH, render_page(model), arguments.check)


if __name__ == "__main__":
    raise SystemExit(main())
