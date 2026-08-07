# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies evaluation documentation reconciliation, freshness, semantics, links, and static completeness.

from __future__ import annotations

import importlib.util
import io
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from collections import Counter
from contextlib import contextmanager
from contextlib import redirect_stderr
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GENERATOR_PATH = ROOT / "scripts" / "build-agent-skill-evaluation-docs.py"
PAGE_PATH = ROOT / "design" / "agent-and-skill-evaluations.html"
SCRIPT_PATH = ROOT / "design" / "agent-and-skill-evaluations.js"
BACKLOG_STEWARD_SCENARIOS_PATH = (
    ROOT / "evals" / "agent-tests" / "dev-backlog-steward" / "scenarios.yaml"
)
NODE_PATH = shutil.which("node")


def write_git_reference(root: Path) -> None:
    """Point a temporary source root at this checkout's exact Git directory."""
    result = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "--absolute-git-dir"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0 or not result.stdout.strip():
        raise RuntimeError(f"Cannot resolve checkout Git directory: {result.stderr}")
    (root / ".git").write_text(
        f"gitdir: {result.stdout.strip()}\n", encoding="utf-8"
    )


@contextmanager
def temporary_source_root():
    """Yield a lightweight editable evaluation-source root backed by repository symlinks."""
    with tempfile.TemporaryDirectory() as temporary_directory:
        root = Path(temporary_directory)
        write_git_reference(root)
        (root / "skills").symlink_to(ROOT / "skills", target_is_directory=True)
        (root / "agents").symlink_to(ROOT / "agents", target_is_directory=True)
        evals = root / "evals"
        evals.mkdir()
        for name in (
            "README.md",
            "judges.yaml",
            "cases.yaml",
            "agent-scenarios.yaml",
            "workflow-packs.yaml",
            "skill-probes.yaml",
        ):
            shutil.copy2(ROOT / "evals" / name, evals / name)
        agent_tests = evals / "agent-tests"
        agent_tests.mkdir()
        source_agent_tests = ROOT / "evals" / "agent-tests"
        shutil.copy2(source_agent_tests / "suite-index.yaml", agent_tests / "suite-index.yaml")
        for source in source_agent_tests.iterdir():
            if source.name == "suite-index.yaml":
                continue
            (agent_tests / source.name).symlink_to(source, target_is_directory=source.is_dir())
        (evals / "results").symlink_to(
            ROOT / "evals" / "results", target_is_directory=True
        )
        yield root


def load_generator():
    """Load the hyphenated generator module for direct source-model assertions."""
    spec = importlib.util.spec_from_file_location("evaluation_docs_generator", GENERATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load generator: {GENERATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class AgentSkillEvaluationDocumentationTests(unittest.TestCase):
    """Protect the source-derived evaluation documentation contract."""

    @classmethod
    def setUpClass(cls) -> None:
        """Build one current source model for the focused test class."""
        cls.generator = load_generator()
        cls.model = cls.generator.build_model(ROOT)
        cls.page = PAGE_PATH.read_text(encoding="utf-8")

    def test_inventories_and_selected_campaign_reconcile(self) -> None:
        """Current catalogs and the selected governed campaign must reconcile exactly."""
        summary = self.model["summary"]
        campaign = self.model["campaign"]

        self.assertEqual(131, summary["skillCount"])
        self.assertEqual(129, summary["probeCount"])
        self.assertEqual(30, summary["roleCount"])
        self.assertEqual(30, summary["suiteCount"])
        self.assertEqual(104, summary["currentScenarioCount"])
        self.assertEqual(26, campaign["suiteCount"])
        self.assertEqual(78, campaign["scenarioCount"])
        self.assertEqual({"PASS": 52, "BLOCKED": 17, "FAIL": 9}, campaign["verdicts"])
        self.assertEqual(78, sum(campaign["verdicts"].values()))

    def test_historical_alignment_and_missing_campaign_evidence_are_explicit(self) -> None:
        """ID matches without retained definitions must remain historical with unknown freshness."""
        summary = self.model["summary"]
        agents = {agent["id"]: agent for agent in self.model["agents"]}

        self.assertEqual(26, summary["missingScenarioResults"])
        self.assertEqual(78, summary["historicalIdOnlyResults"])
        self.assertEqual(0, summary["snapshotAlignedResults"])
        self.assertEqual(0, summary["definitionDriftResults"])
        self.assertEqual(0, summary["removedCampaignResults"])
        coordinator = agents["dev-backlog-coordinator"]
        self.assertEqual("missing", coordinator["freshness"])
        self.assertEqual(9, coordinator["missingScenarioCount"])
        self.assertTrue(all(item["campaignVerdict"] is None for item in coordinator["scenarios"]))
        self.assertTrue(all(item["evidenceState"] == "missing" for item in coordinator["scenarios"]))
        coder = agents["dev-coder"]
        self.assertEqual("historical-unknown", coder["freshness"])
        self.assertTrue(
            all(item["evidenceState"] == "historical-id-only" for item in coder["scenarios"])
        )

    def test_backlog_steward_rows_publish_neutral_resource_coordination_variants(self) -> None:
        """All Steward rows must declare variants without asserting either one executed."""
        disclosure = (
            "this row declares project-selected resource coordination variants "
            "and does not claim both variants were executed"
        )
        claim_only_language = re.compile(
            r"\b(?:(?:agent[-_ ]?)?claims?(?:[-_][a-z0-9]+)*|"
            r"acquir(?:e|ed|ing|es|isition|isitions)|"
            r"releas(?:e|ed|ing|es)|registr(?:y|ies)|journals?|conflicts?)\b",
            re.IGNORECASE,
        )

        def assert_neutral_top_level(source: dict[str, object]) -> None:
            purpose = str(source["purpose"])
            self.assertEqual(1, purpose.count(disclosure))
            named_contract_fields = {
                field: value
                for field, value in source.items()
                if field == "purpose"
                or any(
                    token in field.lower()
                    for token in ("behavior", "skill", "check")
                )
            }
            named_contract_fields["purpose"] = purpose.replace(disclosure, "", 1)
            for field, value in named_contract_fields.items():
                values = value if isinstance(value, list) else [value]
                for item in values:
                    self.assertIsNone(
                        claim_only_language.search(str(item)),
                        f"{field} retains claim-only top-level language: {item}",
                    )

        steward = next(
            agent for agent in self.model["agents"] if agent["id"] == "dev-backlog-steward"
        )
        source_scenarios = self.generator.load_yaml(BACKLOG_STEWARD_SCENARIOS_PATH)[
            "scenarios"
        ]
        source_by_id = {scenario["id"]: scenario for scenario in source_scenarios}
        historical_ids = {
            "creation-and-claim",
            "interrupted-work-recovery",
            "blocked-state-transition",
            "blocked-unowned-running-shortcut",
            "blocked-claimed-resumption",
            "blocked-failed-claim-resumption",
            "future-ideas-capture-and-promotion",
        }
        rendered_by_id = {scenario["id"]: scenario for scenario in steward["scenarios"]}

        self.assertEqual(historical_ids, set(source_by_id))
        self.assertEqual(historical_ids, set(rendered_by_id))
        for scenario_id, source in source_by_id.items():
            with self.subTest(scenario=scenario_id):
                coordination_cases = source["resourceCoordinationCases"]
                self.assertEqual({"resource-claim", "none"}, set(coordination_cases))
                resource_claim = coordination_cases["resource-claim"]
                none = coordination_cases["none"]
                self.assertEqual(["resource-claim"], resource_claim["targetSkills"])
                self.assertEqual(["claim-lifecycle"], resource_claim["deterministicChecks"])
                self.assertTrue(resource_claim["claimCalls"])
                self.assertTrue(resource_claim["registryMutations"])
                self.assertTrue(resource_claim["journalWrites"])
                self.assertTrue(resource_claim["claimLifecycle"])
                self.assertEqual("required", resource_claim["claimEvidence"])
                self.assertEqual([], none["targetSkills"])
                self.assertEqual([], none["deterministicChecks"])
                self.assertEqual([], none["claimCalls"])
                self.assertEqual([], none["registryMutations"])
                self.assertEqual([], none["journalWrites"])
                self.assertEqual([], none["claimReleases"])
                self.assertEqual("absent", none["claimEvidence"])
                self.assertEqual(
                    resource_claim["providerLifecycle"],
                    none["providerLifecycle"],
                )
                assert_neutral_top_level(source)
                purpose = rendered_by_id[scenario_id]["purpose"]
                self.assertIn(
                    "declares project-selected resource coordination variants",
                    purpose,
                )
                self.assertIn(
                    "does not claim both variants were executed",
                    purpose,
                )
                self.assertNotIn("executable variant", purpose)
                self.assertNotIn("runner-enforced", purpose)
                self.assertIn(
                    f"<td>{self.generator.escape(purpose)}</td>",
                    self.page,
                )

        representative = source_scenarios[0]
        bypass_mutations = {
            "appended-purpose-directive": {
                **representative,
                "purpose": (
                    representative["purpose"]
                    + " Acquire a claim and publish claim evidence."
                ),
            },
            "alternative-check-id": {
                **representative,
                "deterministicChecks": [
                    *representative["deterministicChecks"],
                    "claim-evidence-gate",
                ],
            },
            "alternative-skill-id": {
                **representative,
                "targetSkills": [
                    *representative["targetSkills"],
                    "exclusive-ownership-claim",
                ],
            },
        }
        for mutation, mutated in bypass_mutations.items():
            with self.subTest(mutation=mutation), self.assertRaises(AssertionError):
                assert_neutral_top_level(mutated)

        resource_claim = next(
            skill for skill in self.model["skills"] if skill["id"] == "resource-claim"
        )
        steward = next(
            agent for agent in self.model["agents"] if agent["id"] == "dev-backlog-steward"
        )
        governed_steward_links = [
            link
            for link in resource_claim["governedScenarioLinks"]
            if link["suite"] == "dev-backlog-steward"
        ]

        self.assertEqual(
            {
                "creation-and-claim",
                "interrupted-work-recovery",
                "blocked-state-transition",
            },
            {link["scenario"] for link in governed_steward_links},
        )
        self.assertTrue(all(link["conditional"] for link in governed_steward_links))
        self.assertTrue(
            all(
                "resource-claim" not in scenario["targetSkills"]
                for scenario in steward["scenarios"]
            )
        )
        source = self.generator.load_yaml(BACKLOG_STEWARD_SCENARIOS_PATH)[
            "scenarios"
        ][0]
        none_only = {
            **source,
            "resourceCoordinationCases": {
                "none": source["resourceCoordinationCases"]["none"]
            },
        }
        self.assertNotIn(
            "resource-claim",
            {
                association["skill"]
                for association in self.generator.scenario_skill_associations(
                    none_only
                )
            },
        )

    def test_scenario_reconciliation_detects_definition_drift_and_removed_rows(self) -> None:
        """Retained snapshots must expose same-ID field drift and campaign-only rows."""
        current = [
            {"id": "purpose", "purpose": "new", "expectedTerminalStatus": "PASS", "targetSkills": ["a"]},
            {"id": "status", "purpose": "same", "expectedTerminalStatus": "FAIL", "targetSkills": ["a"]},
            {"id": "skills", "purpose": "same", "expectedTerminalStatus": "PASS", "targetSkills": ["b"]},
        ]
        snapshot = {
            "purpose": {"purpose": "old", "expectedTerminalStatus": "PASS", "targetSkills": ["a"]},
            "status": {"purpose": "same", "expectedTerminalStatus": "PASS", "targetSkills": ["a"]},
            "skills": {"purpose": "same", "expectedTerminalStatus": "PASS", "targetSkills": ["a"]},
            "removed": {"purpose": "historical", "expectedTerminalStatus": "BLOCKED", "targetSkills": ["a"]},
        }
        records = self.generator.reconcile_scenarios(
            current,
            {"purpose": "PASS", "status": "FAIL", "skills": "BLOCKED", "removed": "PASS"},
            snapshot,
        )
        by_id = {record["id"]: record for record in records}
        self.assertEqual(["purpose"], by_id["purpose"]["driftFields"])
        self.assertEqual(["expectedTerminalStatus"], by_id["status"]["driftFields"])
        self.assertEqual(["targetSkills"], by_id["skills"]["driftFields"])
        self.assertEqual("historical-removed", by_id["removed"]["evidenceState"])
        self.assertEqual("campaign-only", by_id["removed"]["catalogState"])
        without_snapshot = self.generator.reconcile_scenarios(
            current[:1], {"purpose": "PASS"}, None
        )
        self.assertEqual("historical-id-only", without_snapshot[0]["evidenceState"])

    def test_coverage_classifier_supports_no_evidence_and_indirect_only_states(self) -> None:
        """Synthetic boundary records must retain explicit no-evidence and indirect-only states."""
        self.assertEqual("none", self.generator.classify_skill(None, [], None))
        self.assertEqual(
            "indirect-only",
            self.generator.classify_skill(None, [{"suite": "example"}], None),
        )
        self.assertEqual(
            "direct-probe",
            self.generator.classify_skill({"id": "probe-example"}, [], None),
        )
        self.assertEqual(
            "direct-governed",
            self.generator.classify_skill(None, [], {"verdict": "PASS"}),
        )

    def test_build_model_allows_missing_probes_but_rejects_orphans_and_duplicates(self) -> None:
        """Probe coverage may be partial, while every declared probe must remain unique and bundled."""
        linked_skill = next(skill["id"] for skill in self.model["skills"] if skill["scenarioLinks"])
        unlinked_skill = next(skill["id"] for skill in self.model["skills"] if not skill["scenarioLinks"])
        with temporary_source_root() as root:
            path = root / "evals" / "skill-probes.yaml"
            document = self.generator.load_yaml(path)
            document["probes"] = [
                probe
                for probe in document["probes"]
                if probe["skill"] not in {linked_skill, unlinked_skill}
            ]
            path.write_text(self.generator.yaml.safe_dump(document, sort_keys=False), encoding="utf-8")
            model = self.generator.build_model(root)
            by_skill = {skill["id"]: skill for skill in model["skills"]}
            self.assertEqual("indirect-only", by_skill[linked_skill]["classification"])
            self.assertEqual("none", by_skill[unlinked_skill]["classification"])
            self.assertEqual(127, model["summary"]["probeCount"])
            page = self.generator.render_page(model)
            self.assertRegex(
                page,
                rf'id="skill-{re.escape(linked_skill)}"\s+data-kind="skill" data-status="indirect-only"',
            )
            self.assertRegex(
                page,
                rf'id="skill-{re.escape(unlinked_skill)}"\s+data-kind="skill" data-status="none"',
            )
            self.assertIn("Indirect agent-suite coverage only", page)
            self.assertIn("No recorded evaluation evidence", page)

        for mutation in ("orphan", "duplicate"):
            with self.subTest(mutation=mutation), temporary_source_root() as root:
                path = root / "evals" / "skill-probes.yaml"
                document = self.generator.load_yaml(path)
                probe = dict(document["probes"][0])
                if mutation == "orphan":
                    probe["id"] = "probe-orphan"
                    probe["skill"] = "orphan-skill"
                document["probes"].append(probe)
                path.write_text(
                    self.generator.yaml.safe_dump(document, sort_keys=False), encoding="utf-8"
                )
                with self.assertRaises(ValueError):
                    self.generator.build_model(root)

    def test_skill_entries_separate_probe_declarations_from_governed_outcomes(self) -> None:
        """Every skill must retain probe, indirect coverage, and outcome limitations separately."""
        self.assertEqual(131, len(self.model["skills"]))
        self.assertEqual(2, sum(skill["probe"] is None for skill in self.model["skills"]))
        self.assertEqual(129, self.model["summary"]["directProbeSkillCount"])
        self.assertEqual(1, self.model["summary"]["indirectOnlySkillCount"])
        self.assertEqual(1, self.model["summary"]["noRecordedEvidenceSkillCount"])
        self.assertTrue(
            any(not skill["governedScenarioLinks"] for skill in self.model["skills"])
        )
        self.assertTrue(
            all(
                skill["latestGovernedOutcome"] != "PASS"
                for skill in self.model["skills"]
            )
        )

    def test_page_preserves_verdict_and_evidence_semantics(self) -> None:
        """The page must name distinct verdict, manual, calibration, and containment states."""
        for text in (
            "PASS",
            "FAIL",
            "BLOCKED",
            "Missing campaign evidence",
            "Historical ID alignment; definition freshness unknown",
            "Manual observation",
            "Uncalibrated Model Judge",
            "Deterministic critical skip",
            "Functional isolation",
            "Security containment",
            "No skill-level verdict",
            "A suite PASS means the suite accepted the target behavior",
            "A target can correctly return BLOCKED inside a suite PASS",
            "A Judge pass is a separate semantic dimension",
            "does not mean a Model Judge passed",
        ):
            with self.subTest(text=text):
                self.assertIn(text, self.page)

    def test_page_topics_separate_method_coverage_results_limits_and_history(self) -> None:
        """The page hierarchy must keep distinct evaluation evidence roles in reader order."""
        section_topics = (
            ("methodology", "Evaluation purpose and method"),
            ("coverage", "Coverage and case catalogs"),
            ("campaign", "Campaign receipt and results"),
            ("limitations", "Evidence limitations"),
            ("history", "Historical evidence alignment"),
            ("agents", "Agent-by-agent evidence"),
            ("skills", "Skill-by-skill evidence"),
            ("follow-ups", "Recorded campaign follow-ups"),
            ("sources", "Authoritative sources"),
        )
        positions = []
        for section_id, title in section_topics:
            with self.subTest(section=section_id):
                section_marker = f'<section class="section" id="{section_id}"'
                heading_marker = f">{title}</h2>"
                self.assertIn(section_marker, self.page)
                self.assertIn(heading_marker, self.page)
                positions.append(self.page.index(section_marker))
                self.assertIn(f'href="#{section_id}"', self.page)
        self.assertEqual(sorted(positions), positions)

        for topic in (
            "Evaluation layers",
            "Workspace and privacy",
            "Verdicts and Judges",
            "Current catalog inventory",
            "Case and workflow catalogs",
            "Skill catalog states",
            "Campaign verdict results",
            "Harness and evidence breakdown",
            "Not verified passes",
            "Alignment and strength",
            "Evidence alignment states",
        ):
            with self.subTest(topic=topic):
                self.assertEqual(1, self.page.count(f"<h3>{topic}</h3>"))

        association_counts = self.model["associationCatalogCounts"]
        for count, label in (
            (association_counts["cases"], "Executable cases"),
            (association_counts["agentScenarios"], "Agent scenarios"),
            (association_counts["workflowPacks"], "Workflow packs"),
        ):
            with self.subTest(catalog=label):
                self.assertIn(f"<strong>{count}</strong><span>{label}</span>", self.page)

    def test_static_page_contains_every_entry_without_javascript(self) -> None:
        """Generated details must remain complete when the optional filter script is absent."""
        self.assertEqual(131, self.page.count('class="evaluation-card skill-card"'))
        self.assertEqual(30, self.page.count('class="evaluation-card agent-card"'))
        for opening_tag in re.findall(r"<(?:article|section)\b[^>]*>", self.page):
            attributes_only = re.sub(r'=(?:"[^"]*"|\'[^\']*\')', '=""', opening_tag)
            self.assertNotRegex(attributes_only, r"\shidden(?:\s|=|>)")
        self.assertIn('<script src="documentation-settings.js"></script>', self.page)
        self.assertIn('<script src="agent-and-skill-evaluations.js"></script>', self.page)
        self.assertIn('<a class="site-brand" href="../index.html">', self.page)
        self.assertIn("<span>AI-Assisted Coding Toolkit Index</span>", self.page)
        self.assertNotIn("Back to Documentation Index", self.page)
        self.assertRegex(
            self.page,
            r"\.site-header \{[^}]*display: flex;[^}]*align-items: center;",
        )
        self.assertIn('<noscript>', self.page)

    def test_responsive_controls_and_statuses_have_accessible_text_contracts(self) -> None:
        """Responsive layout, focus visibility, labels, and live counts must be explicit."""
        self.assertIn("@media (max-width: 720px)", self.page)
        self.assertIn("width: fit-content; max-width: 100%; box-sizing: border-box", self.page)
        self.assertIn(".evaluation-card { display: grid; min-width: 0", self.page)
        self.assertIn("overflow-wrap: anywhere; white-space: normal", self.page)
        self.assertIn(":focus-visible", self.page)
        self.assertIn('aria-label="Page sections"', self.page)
        self.assertEqual(2, self.page.count('aria-live="polite"'))
        for control_id in ("agent-search", "agent-status", "skill-search", "skill-status"):
            with self.subTest(control_id=control_id):
                self.assertIn(f'for="{control_id}"', self.page)
                self.assertIn(f'id="{control_id}"', self.page)
        self.assertIn('<th>Campaign verdict</th>', self.page)
        self.assertIn('<th>Evidence alignment</th>', self.page)
        self.assertNotIn("https://", self.page)
        self.assertNotIn("http://", self.page)

    def test_local_source_links_resolve(self) -> None:
        """Every tracked source link must resolve from the generated design page."""
        links = re.findall(r'href="([^"]+)"', self.page)
        local_paths = {
            link.split("#", 1)[0]
            for link in links
            if link
            and not link.startswith("#")
            and not link.startswith(("http://", "https://", "mailto:"))
        }
        missing = [
            path
            for path in sorted(local_paths)
            if not (PAGE_PATH.parent / path).resolve().exists()
            and not self.generator.repository_path_exists(
                ROOT,
                (PAGE_PATH.parent / path).resolve().relative_to(ROOT).as_posix(),
            )
        ]
        self.assertEqual([], missing)

    def test_generator_check_reports_current_output(self) -> None:
        """The focused freshness command must accept only source-current HTML."""
        result = subprocess.run(
            [sys.executable, str(GENERATOR_PATH), "--check"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("up to date", result.stdout)

    def test_campaign_parser_rejects_duplicate_totals_suites_and_scenarios(self) -> None:
        """Duplicate report rows must fail instead of being silently overwritten."""
        original = (ROOT / "evals/agent-tests/results/2026-07-17-complete-agent-suites.md").read_text(
            encoding="utf-8"
        )
        mutations = {
            "total": original.replace("| Total | 78 |", "| PASS | 52 |\n| Total | 78 |"),
            "suite": original.replace(
                "| dev-coder | typescript-behavior-change: PASS; spring-boundary-change: PASS; insufficient-contract-authority: BLOCKED |",
                "| dev-coder | typescript-behavior-change: PASS; spring-boundary-change: PASS; insufficient-contract-authority: BLOCKED |\n| dev-coder | duplicate: PASS |",
            ),
            "scenario": original.replace(
                "typescript-behavior-change: PASS; spring-boundary-change",
                "typescript-behavior-change: PASS; typescript-behavior-change: PASS; spring-boundary-change",
            ),
        }
        for kind, content in mutations.items():
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "report.md"
                path.write_text(content, encoding="utf-8")
                with self.assertRaises(ValueError):
                    self.generator.parse_campaign(path, ROOT)

    def test_build_model_rejects_duplicate_suite_index_identity_path_and_priority(self) -> None:
        """Suite index identity, source path, and execution priority must each be unique."""
        for field, message in (
            ("id", "duplicate suite index id"),
            ("path", "duplicate suite index path"),
            ("priority", "duplicate suite index priority"),
        ):
            with self.subTest(field=field), temporary_source_root() as root:
                path = root / "evals" / "agent-tests" / "suite-index.yaml"
                document = self.generator.load_yaml(path)
                document["suites"][1][field] = document["suites"][0][field]
                path.write_text(
                    self.generator.yaml.safe_dump(document, sort_keys=False), encoding="utf-8"
                )
                with self.assertRaisesRegex(ValueError, message):
                    self.generator.build_model(root)

    def test_build_model_rejects_priority_duplicates_after_integer_normalization(self) -> None:
        """Mixed scalar spellings must not create equal normalized priorities."""
        with temporary_source_root() as root:
            path = root / "evals" / "agent-tests" / "suite-index.yaml"
            document = self.generator.load_yaml(path)
            document["suites"][1]["priority"] = str(
                document["suites"][0]["priority"]
            )
            path.write_text(
                self.generator.yaml.safe_dump(document, sort_keys=False), encoding="utf-8"
            )
            with self.assertRaisesRegex(ValueError, "duplicate suite index priority"):
                self.generator.build_model(root)

        with temporary_source_root() as root:
            suite_index = self.generator.load_yaml(
                root / "evals" / "agent-tests" / "suite-index.yaml"
            )
            suite_entry = suite_index["suites"][0]
            path = (
                root
                / "evals"
                / "agent-tests"
                / suite_entry["path"]
                / "scenarios.yaml"
            )
            source = self.generator.load_yaml(path)
            source["scenarios"][1]["priority"] = str(
                source["scenarios"][0]["priority"]
            )
            suite_root = path.parent
            suite_root.unlink()
            suite_root.mkdir()
            shutil.copy2(
                ROOT
                / "evals"
                / "agent-tests"
                / suite_entry["path"]
                / "suite.yaml",
                suite_root / "suite.yaml",
            )
            path.write_text(
                self.generator.yaml.safe_dump(source, sort_keys=False), encoding="utf-8"
            )
            with self.assertRaisesRegex(ValueError, "duplicate .* scenario priority"):
                self.generator.build_model(root)

    def test_build_model_rejects_duplicate_top_level_agent_catalog_id(self) -> None:
        """Top-level agent-scenario owners must not be overwritten or double-counted."""
        with temporary_source_root() as root:
            path = root / "evals" / "agent-scenarios.yaml"
            document = self.generator.load_yaml(path)
            document["agents"][1]["id"] = document["agents"][0]["id"]
            path.write_text(
                self.generator.yaml.safe_dump(document, sort_keys=False), encoding="utf-8"
            )
            with self.assertRaisesRegex(
                ValueError, "duplicate agent scenario catalog agent id"
            ):
                self.generator.build_model(root)

    def test_campaign_parser_consumes_every_ledger_and_followup_entry(self) -> None:
        """Malformed, extra, duplicated, or renumbered evidence lines must be rejected."""
        campaign_path = ROOT / "evals/agent-tests/results/2026-07-17-complete-agent-suites.md"
        original = campaign_path.read_text(encoding="utf-8")
        valid = self.generator.parse_campaign(campaign_path, ROOT)
        self.assertEqual(valid["scenarioCount"], sum(valid["verdicts"].values()))
        self.assertEqual(15, len(valid["followUps"]))

        mutations = {
            "bad-ledger-suite": original.replace(
                "| dev-coder | typescript-behavior-change",
                "| BAD SUITE | ignored: PASS |\n| dev-coder | typescript-behavior-change",
            ),
            "ledger-missing-leading-pipe": original.replace(
                "| dev-coder | typescript-behavior-change",
                "dev-coder | typescript-behavior-change",
                1,
            ),
            "ledger-extra-column": original.replace(
                "insufficient-contract-authority: BLOCKED |",
                "insufficient-contract-authority: BLOCKED | extra |",
                1,
            ),
            "duplicate-followup-number": original.replace(
                "2. [Enforce behavioral regression assertions]",
                "1. [Enforce behavioral regression assertions]",
                1,
            ),
            "renumbered-followup": original.replace(
                "2. [Enforce behavioral regression assertions]",
                "20. [Enforce behavioral regression assertions]",
                1,
            ),
            "malformed-followup-parenthesis": original.replace(
                "1. [Align Project Organiser filename selection]",
                "1) [Align Project Organiser filename selection]",
                1,
            ),
            "reformatted-followup-bullet": original.replace(
                "1. [Align Project Organiser filename selection]",
                "- [Align Project Organiser filename selection]",
                1,
            ),
            "duplicate-followup-target": original.replace(
                "prevent-unsupported-review-findings.md",
                "enforce-behavioral-regression-assertions.md",
                1,
            ),
        }
        for kind, content in mutations.items():
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                write_git_reference(root)
                report = root / "evals/agent-tests/results/report.md"
                report.parent.mkdir(parents=True)
                report.write_text(content, encoding="utf-8")
                with self.assertRaises(ValueError):
                    self.generator.parse_campaign(report, root)

    def test_campaign_parser_rejects_asterisk_and_plus_followup_omissions_and_duplicates(self) -> None:
        """Alternate list markers must be consumed and rejected instead of disappearing."""
        campaign_path = ROOT / "evals/agent-tests/results/2026-07-17-complete-agent-suites.md"
        original = campaign_path.read_text(encoding="utf-8")
        first_entry = (
            "1. [Align Project Organiser filename selection]"
            "(../../../backlog/feature-backlog/agent-skill-lifecycle/"
            "align-project-organiser-filename-selection.md)."
        )
        for marker in ("*", "+"):
            mutations = {
                "omission": original.replace(
                    first_entry, f"{marker} {first_entry[3:]}", 1
                ),
                "duplicate": original.replace(
                    first_entry, f"{first_entry}\n{marker} {first_entry[3:]}", 1
                ),
            }
            for mutation, content in mutations.items():
                with (
                    self.subTest(marker=marker, mutation=mutation),
                    tempfile.TemporaryDirectory() as directory,
                ):
                    root = Path(directory)
                    write_git_reference(root)
                    report = root / "evals/agent-tests/results/report.md"
                    report.parent.mkdir(parents=True)
                    report.write_text(content, encoding="utf-8")
                    with self.assertRaisesRegex(
                        ValueError, "Malformed campaign follow-up entry"
                    ):
                        self.generator.parse_campaign(report, root)

    def test_campaign_parser_rejects_external_escaping_and_untracked_followup_paths(self) -> None:
        """Follow-up evidence must resolve to a tracked path inside the repository."""
        campaign_path = ROOT / "evals/agent-tests/results/2026-07-17-complete-agent-suites.md"
        original = campaign_path.read_text(encoding="utf-8")
        tracked_target = (
            "../../../backlog/feature-backlog/agent-skill-lifecycle/"
            "align-project-organiser-filename-selection.md"
        )
        mutations = {
            "absolute": ("/etc/passwd", "escapes the repository"),
            "escaping": ("../../../../../../etc/passwd", "escapes the repository"),
            "untracked": (
                "../../../untracked-follow-up.md",
                "outside tracked backlog history",
            ),
            "basename-alias": (
                "../../../not-backlog/align-project-organiser-filename-selection.md",
                "outside tracked backlog history",
            ),
            "untracked-backlog-alias": (
                "../../../backlog/fabricated/align-project-organiser-filename-selection.md",
                "was never tracked",
            ),
            "pathspec-wildcard-alias": (
                "../../../backlog/**/align-project-organiser-filename-selection.md",
                "was never tracked",
            ),
        }
        for mutation, (target, message) in mutations.items():
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                write_git_reference(root)
                if mutation == "untracked":
                    (root / "untracked-follow-up.md").write_text(
                        "not tracked", encoding="utf-8"
                    )
                report = root / "evals/agent-tests/results/report.md"
                report.parent.mkdir(parents=True)
                report.write_text(
                    original.replace(tracked_target, target, 1), encoding="utf-8"
                )
                with self.assertRaisesRegex(ValueError, message):
                    self.generator.parse_campaign(report, root)

    def test_visible_historical_rows_sum_exactly_to_campaign_totals(self) -> None:
        """Agent detail must retain every selected-campaign verdict exactly once."""
        visible = [
            scenario["campaignVerdict"]
            for agent in self.model["agents"]
            for scenario in agent["scenarios"]
            if scenario["campaignVerdict"] is not None
        ]
        self.assertEqual(self.model["campaign"]["scenarioCount"], len(visible))
        self.assertEqual(self.model["campaign"]["verdicts"], dict(Counter(visible)))
        for verdict, count in self.model["campaign"]["verdicts"].items():
            with self.subTest(verdict=verdict):
                self.assertEqual(
                    count,
                    self.page.count(f'data-campaign-verdict="{verdict}"'),
                )

    def test_evaluation_associations_resolve_and_catalog_drift_changes_snapshot(self) -> None:
        """Displayed case, agent-scenario, and workflow associations must be source-bound."""
        self.assertEqual({"cases", "agentScenarios", "workflowPacks"}, set(self.model["associationCatalogCounts"]))
        with temporary_source_root() as root:
            baseline = self.generator.build_model(root)["sourceDigest"]
            cases_path = root / "evals" / "cases.yaml"
            cases = self.generator.load_yaml(cases_path)
            cases["cases"][0]["coverageStatus"] = "declared"
            cases_path.write_text(
                self.generator.yaml.safe_dump(cases, sort_keys=False), encoding="utf-8"
            )
            changed = self.generator.build_model(root)["sourceDigest"]
            self.assertNotEqual(baseline, changed)

        for field, invalid in (
            ("executableCases", "missing-case"),
            ("scenarioAssociations", "missing-agent-scenario"),
            ("workflowAssociations", "missing-workflow"),
        ):
            with self.subTest(field=field), temporary_source_root() as root:
                path = root / "evals" / "skill-probes.yaml"
                document = self.generator.load_yaml(path)
                document["probes"][0][field] = [invalid]
                path.write_text(
                    self.generator.yaml.safe_dump(document, sort_keys=False), encoding="utf-8"
                )
                with self.assertRaisesRegex(ValueError, invalid):
                    self.generator.build_model(root)

    def test_campaign_followups_are_traceable_and_agent_mapping_is_source_bounded(self) -> None:
        """Every recorded correction item must remain linked, with only explicit agent mappings."""
        followups = self.model["campaign"]["followUps"]
        self.assertEqual(15, len(followups))
        self.assertTrue(
            all(
                self.generator.repository_path_exists(ROOT, item["sourcePath"])
                for item in followups
            )
        )
        mapped = {agent["id"]: agent["followUps"] for agent in self.model["agents"] if agent["followUps"]}
        self.assertIn("project-bootstrapper", mapped)
        self.assertIn("wiki-ingester", mapped)
        self.assertIn("Campaign-wide; the report does not map this correction to one agent", self.page)

    def test_snapshot_metadata_is_truthful_and_not_a_fabricated_generation_time(self) -> None:
        """Deterministic output must describe its source snapshot without claiming wall time."""
        self.assertNotIn("generatedAt", self.model)
        self.assertFalse(self.model["snapshotMetadata"]["wallClockBuildTimeRetained"])
        self.assertIn("Wall-clock build time", self.page)
        self.assertIn("Not retained", self.page)
        generator_source = GENERATOR_PATH.read_text(encoding="utf-8")
        self.assertNotIn("historical 78-scenario", generator_source)
        self.assertNotIn("against 27 suites", generator_source)

    def test_freshness_check_rejects_drifted_output(self) -> None:
        """A changed generated artifact must fail the deterministic freshness boundary."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            drifted_page = Path(temporary_directory) / "agent-and-skill-evaluations.html"
            drifted_page.write_text("stale", encoding="utf-8")
            diagnostics = io.StringIO()
            with redirect_stderr(diagnostics):
                result = self.generator.write_or_check(drifted_page, "current", True)
        self.assertEqual(1, result)
        self.assertIn("stale", diagnostics.getvalue())

    @unittest.skipUnless(NODE_PATH, "Node is unavailable for pure JavaScript checks")
    def test_optional_filter_matches_text_and_status_without_removing_static_content(self) -> None:
        """The pure filter helper must combine normalized text and exact evidence status."""
        fixture = [
            {"dataset": {"search": "dev coder pass", "status": "historical-unknown"}},
            {"dataset": {"search": "backlog coordinator missing", "status": "missing"}},
            {"dataset": {"search": "wiki ingester historical", "status": "historical-drift"}},
        ]
        program = f"""
const filters = require({json.dumps(str(SCRIPT_PATH))});
const cards = {json.dumps(fixture)};
const search = {{value: 'wiki', focused: false, focus() {{ this.focused = true; }}}};
const status = {{value: 'historical-drift'}};
const count = {{textContent: ''}};
const visible = filters.applyFilterElements('agent', {{cards, search, status, count}});
const beforeClear = {{visible, hidden: cards.map(card => card.hidden), message: count.textContent}};
const afterClear = filters.clearFilterElements('agent', {{cards, search, status, count}});
process.stdout.write(JSON.stringify({{
  text: filters.filterCards(cards, 'COORDINATOR', 'all').length,
  status: filters.filterCards(cards, '', 'historical-drift').length,
  combined: filters.filterCards(cards, 'wiki', 'historical-drift').length,
  none: filters.filterCards(cards, 'coder', 'missing').length,
  beforeClear,
  afterClear,
  afterState: {{search: search.value, status: status.value, focused: search.focused, message: count.textContent, hidden: cards.map(card => card.hidden)}}
}}));
"""
        result = subprocess.run(
            [NODE_PATH, "-e", program],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        actual = json.loads(result.stdout)
        self.assertEqual(
            {"text": 1, "status": 1, "combined": 1, "none": 0},
            {key: actual[key] for key in ("text", "status", "combined", "none")},
        )
        self.assertEqual(
            {"visible": 1, "hidden": [True, True, False], "message": "Showing 1 of 3 agents."},
            actual["beforeClear"],
        )
        self.assertEqual(3, actual["afterClear"])
        self.assertEqual(
            {"search": "", "status": "all", "focused": True, "message": "Showing 3 of 3 agents.", "hidden": [False, False, False]},
            actual["afterState"],
        )
        script = SCRIPT_PATH.read_text(encoding="utf-8")
        for event_name in ('"input"', '"change"', '"click"', '"DOMContentLoaded"'):
            self.assertIn(event_name, script)

    def test_navigation_places_evaluation_between_core_and_configuration(self) -> None:
        """The generated page must be a standard sequence member after the core catalog."""
        definitions_page = (ROOT / "design" / "agent-and-skill-definitions.html").read_text(
            encoding="utf-8"
        )
        configuration_page = (ROOT / "design" / "agentic-configuration.html").read_text(
            encoding="utf-8"
        )
        self.assertIn(
            '<a href="agent-and-skill-evaluations.html" rel="next">'
            'Next: Evaluation Evidence <span aria-hidden="true">&rarr;</span></a>',
            definitions_page,
        )
        self.assertIn(
            '<a href="agent-and-skill-definitions.html" rel="prev">'
            '<span aria-hidden="true">&larr;</span> Previous: Core Agent and Skills</a>',
            self.page,
        )
        self.assertIn(
            '<a href="agentic-configuration.html" rel="next">'
            'Next: Agentic Configuration <span aria-hidden="true">&rarr;</span></a>',
            self.page,
        )
        self.assertIn(
            '<a href="agent-and-skill-evaluations.html" rel="prev">'
            '<span aria-hidden="true">&larr;</span> Previous: Evaluation Evidence</a>',
            configuration_page,
        )


if __name__ == "__main__":
    unittest.main()
