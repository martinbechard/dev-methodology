# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Modified with AI assistance.
# Summary: Verifies constraint taxonomy, Starting, watchdog, and two-phase Persistence behavior in coordination contracts.
# Governing design: design/orchestrated-development-lifecycle.html

import json
from pathlib import Path
import re
import unittest

import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
README_PATH = REPOSITORY_ROOT / "README.md"
SKILL_PATH = REPOSITORY_ROOT / "skills" / "codex-workitem-coordination" / "SKILL.md"
MANAGE_FILE_WORK_ITEMS_PATH = REPOSITORY_ROOT / "skills" / "manage-file-work-items" / "SKILL.md"
COORDINATOR_ROLE_PATH = (
    REPOSITORY_ROOT / "agents" / "roles" / "dev-activities" / "dev-backlog-coordinator.role.yaml"
)
ORCHESTRATOR_ROLE_PATH = (
    REPOSITORY_ROOT / "agents" / "roles" / "dev-activities" / "dev-orchestrator.role.yaml"
)
STEWARD_ROLE_PATH = (
    REPOSITORY_ROOT / "agents" / "roles" / "dev-activities" / "dev-backlog-steward.role.yaml"
)
WATCHDOG_ROLE_PATH = (
    REPOSITORY_ROOT / "agents" / "roles" / "dev-activities" / "dev-backlog-watchdog.role.yaml"
)
HISTORICAL_PARENT_TASK_ID = "019f8b00-e6d7-7841-854a-40a50ca4e7f2"
HISTORICAL_REPOSITORY_ROOT = "/Users/martinbechard/dev/dev-methodology"
HISTORICAL_STANDING_PROMPT = """Act as the dedicated read-only Dev Methodology backlog watchdog for parent task 019f8b00-e6d7-7841-854a-40a50ca4e7f2 in /Users/martinbechard/dev/dev-methodology.

Apply skills/codex-workitem-coordination/SKILL.md, especially Dedicated Read-Only Watchdog and Fifteen-Minute Parent Review. On each cycle, read current file-backed work items, Git state, configured claim registry state, and Codex task state. Evaluate Running capacity and vacancies, phases and age, estimates/hard stops/evidence progress, Blocked unblock conditions, accepted work stranded before integration, integrated work awaiting provider closeout, terminal cleanup anomalies, waits at or beyond 30 minutes, and unsafe/stale/broad shared ownership.

Remain strictly read-only. Do not mutate repository files, lifecycle state, claims, tasks, branches, worktrees, or shared resources; do not dispatch, integrate, clean up, or run expensive/live verification. Notify parent task 019f8b00-e6d7-7841-854a-40a50ca4e7f2 only when an actionable condition exists, with exact evidence and the smallest recommended parent action. When healthy, record only a concise no-action cycle result here."""
HISTORICAL_HEARTBEAT_PROMPT = """Run one complete read-only watchdog cycle now using the task's standing contract. Notify parent task 019f8b00-e6d7-7841-854a-40a50ca4e7f2 only if an actionable condition exists; otherwise record a concise no-action cycle note here."""
_GENERATED_COORDINATOR_ADAPTERS = tuple(
    REPOSITORY_ROOT / "generated" / "adapters" / adapter / "agents" / filename
    for adapter, filename in (
        ("claude", "dev-backlog-coordinator.md"),
        ("codex", "dev-backlog-coordinator.toml"),
        ("gemini", "dev-backlog-coordinator.md"),
        ("junie", "dev-backlog-coordinator.md"),
    )
)
_RETIRED_QUEUE_CLAUSES = (
    "Count work items whose file-backed Status is Running.",
    "Count Work items whose file-backed Status is Running.",
    "When an item leaves Running, fill the active-capacity vacancy",
    "recount Running capacity",
    "ten are Running",
)
_RETIRED_RECONCILIATION_CLAUSES = (
    "Retry creation only once after that settled read still shows no match, then reconcile once more.",
    "Retry Thread creation after an ambiguous response.",
    "Retry Task creation after ambiguous startup.",
    "Create another Thread after ambiguous startup.",
)
_RETIRED_PROVIDER_SHORTCUT_CLAUSES = (
    "Record the owner, enabled coordination reference, and Status: Running, then commit.",
    "Ready -> Running",
    "Blocked -> Running",
    "Blocked/Ready -> Running",
    "Blocked or Ready -> Running",
)
_WATCHDOG_AUTHORITY_PATTERNS = (
    (
        "delivery authority",
        re.compile(
            r"\b(?:infer(?:s|red|ring)?|decid(?:e|es|ed|ing)|"
            r"determin(?:e|es|ed|ing))\b[^.!?\n]{0,160}?\b"
            r"(?:integration readiness|accepted delivery|completion readiness)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "state mutation authority",
        re.compile(
            r"\b(?:mutat(?:e|es|ed|ing)|chang(?:e|es|ed|ing))\b"
            r"[^.!?\n]{0,160}?\b(?:backlog(?: lifecycle)?|claims?|"
            r"coordination entries?|task state|work-item (?:lifecycle state|status))\b",
            re.IGNORECASE,
        ),
    ),
)
_NEGATED_AUTHORITY = re.compile(
    r"\b(?:must not|does not|do not|never|cannot|can't)\b",
    re.IGNORECASE,
)
_AUTHORITY_CONTRAST = re.compile(r"\b(?:but|however|yet)\b", re.IGNORECASE)


def _markdown_section(text: str, heading: str) -> str:
    marker = f"## {heading}"
    if marker not in text:
        raise AssertionError(f"missing coordination section: {marker}")
    return text.split(marker, 1)[1].split("\n## ", 1)[0]


def _text_template(text: str, heading: str) -> str:
    """Return one fenced text template immediately below a named heading."""

    section = text.split(heading, 1)[1]
    return section.split("```text\n", 1)[1].split("\n```", 1)[0]


def _present_retired_clauses(text: str, clauses: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(clause for clause in clauses if clause in text)


def _missing_contract_clauses(text: str, clauses: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(clause for clause in clauses if clause not in text)


def _watchdog_authority_violations(text: str) -> tuple[tuple[str, str], ...]:
    violations: list[tuple[str, str]] = []
    for sentence in re.split(r"(?<=[.!?])\s+", text):
        for label, pattern in _WATCHDOG_AUTHORITY_PATTERNS:
            for match in pattern.finditer(sentence):
                prefix = sentence[: match.start()]
                contrasts = tuple(_AUTHORITY_CONTRAST.finditer(prefix))
                if contrasts:
                    prefix = prefix[contrasts[-1].end() :]
                if not _NEGATED_AUTHORITY.search(prefix):
                    violations.append((label, sentence))
    return tuple(violations)


class CoordinationConstraintTaxonomyTests(unittest.TestCase):
    """Keep hard prerequisites separate from event-scoped overlap constraints."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.coordination = SKILL_PATH.read_text(encoding="utf-8")
        cls.provider = MANAGE_FILE_WORK_ITEMS_PATH.read_text(encoding="utf-8")
        cls.queue_section = _markdown_section(
            cls.coordination,
            "Queue Target And Dispatch",
        )
        cls.coordination_reporting = _markdown_section(
            cls.coordination,
            "Reporting",
        )
        cls.provider_dispatch = _markdown_section(
            cls.provider,
            "Dispatch Workflow",
        )
        cls.provider_reporting = _markdown_section(
            cls.provider,
            "Reporting",
        )

    def test_hard_prerequisites_block_dispatch_but_overlap_notes_do_not(self) -> None:
        required = (
            "An unmet hard prerequisite makes the item dispatch-ineligible.",
            "A coordination-only overlap note does not block a safe private-worktree start.",
        )
        for section in (self.queue_section, self.provider_dispatch):
            with self.subTest(section=section[:40]):
                self.assertEqual((), _missing_contract_clauses(section, required))

    def test_blocked_or_unowned_reference_without_live_claim_remains_eligible(
        self,
    ) -> None:
        scenario = (
            "When a coordination-only note references a Blocked or Unowned item "
            "and no live claim protects the relevant exact conflict, the candidate "
            "remains dispatch-eligible"
        )
        for section in (self.queue_section, self.provider_dispatch):
            with self.subTest(section=section[:40]):
                self.assertEqual(
                    (),
                    _missing_contract_clauses(section, (scenario,)),
                )
                for old, replacement in (
                    ("Blocked or Unowned", "Blocked"),
                    ("Blocked or Unowned", "Unowned"),
                    ("no live claim", "a live claim"),
                    ("remains dispatch-eligible", "becomes dispatch-ineligible"),
                ):
                    mutated = section.replace(old, replacement, 1)
                    with self.subTest(mutation=f"{old} -> {replacement}"):
                        with self.assertRaises(AssertionError):
                            self.assertEqual(
                                (),
                                _missing_contract_clauses(mutated, (scenario,)),
                            )

    def test_duplicate_ownership_and_implementation_are_reconciled_before_dispatch(
        self,
    ) -> None:
        required = (
            "Before dispatch, reconcile duplicate ownership or implementation",
            "one canonical effort",
        )
        for section in (self.queue_section, self.provider_dispatch):
            with self.subTest(section=section[:40]):
                self.assertEqual((), _missing_contract_clauses(section, required))

    def test_overlap_coordination_defers_only_the_relevant_event(self) -> None:
        required = (
            "Coordinate an exact-path conflict at the relevant edit, shared-resource, or integration event",
            "Defer only that event",
            "A live exact conflict may defer only its relevant event",
        )
        for section in (self.queue_section, self.provider_dispatch):
            with self.subTest(section=section[:40]):
                self.assertEqual((), _missing_contract_clauses(section, required))

    def test_reporting_distinguishes_each_constraint_dimension(self) -> None:
        required = (
            "dispatch eligibility",
            "unmet hard blocker",
            "coordination-only overlap constraint",
            "deferred edit, shared-resource, or integration event",
        )
        for section in (self.coordination_reporting, self.provider_reporting):
            with self.subTest(section=section[:40]):
                self.assertEqual((), _missing_contract_clauses(section, required))

    def test_taxonomy_guards_are_mutation_sensitive(self) -> None:
        cases = (
            (
                self.queue_section,
                "An unmet hard prerequisite makes the item dispatch-ineligible.",
            ),
            (
                self.provider_dispatch,
                "A coordination-only overlap note does not block a safe private-worktree start.",
            ),
            (
                self.queue_section,
                "Before dispatch, reconcile duplicate ownership or implementation",
            ),
            (
                self.provider_dispatch,
                "Coordinate an exact-path conflict at the relevant edit, shared-resource, or integration event",
            ),
            (
                self.coordination_reporting,
                "coordination-only overlap constraint",
            ),
            (
                self.provider_reporting,
                "deferred edit, shared-resource, or integration event",
            ),
        )
        for section, clause in cases:
            with self.subTest(clause=clause):
                self.assertEqual((), _missing_contract_clauses(section, (clause,)))
                mutated = section.replace(clause, "", 1)
                with self.assertRaises(AssertionError):
                    self.assertEqual(
                        (),
                        _missing_contract_clauses(mutated, (clause,)),
                    )


class CodexWorkItemCoordinationWatchdogTests(unittest.TestCase):
    """Keep watchdog authority and notification boundaries explicit."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.skill_text = SKILL_PATH.read_text(encoding="utf-8")
        heading = "### Dedicated Read-Only Watchdog"
        if heading not in cls.skill_text:
            raise AssertionError(f"missing watchdog section: {heading}")
        watchdog_section = cls.skill_text.split(heading, 1)[1].split("\n## ", 1)[0]
        cls.watchdog_section = " ".join(watchdog_section.split())

    def test_watchdog_is_one_scheduled_read_only_observer(self) -> None:
        required = (
            "assign one dedicated watchdog Task to an Agent",
            "Dev Backlog Watchdog Role",
            "never performs scheduling or recovery",
            "observes and reports; it is not a Work-item owner, queue entry, active-capacity slot, durable record, or substitute Coordinator",
            "The Watchdog is read-only.",
            "must not change repository files, provider records, lifecycle state, claims, task state, branches, worktrees, or shared resources",
            "does not create a replacement ledger or duplicate Watchdog",
        )
        for clause in required:
            with self.subTest(clause=clause):
                self.assertIn(clause, self.watchdog_section)

        for retired_clause in (
            "one dedicated watchdog task",
            "watchdog Thread",
            "work-item owner, queue entry, Running slot",
        ):
            with self.subTest(retired_clause=retired_clause):
                self.assertNotIn(retired_clause, self.watchdog_section)

    def test_watchdog_checks_blocked_running_and_terminal_boundaries(self) -> None:
        required = (
            "published estimate, hard stop, and latest evidence-bearing progress",
            "Blocked item's exact blocker and unblock condition",
            "accepted work stranded before Commit delivery",
            "READY Commit delivery awaiting provider closeout",
            "terminal work awaiting cleanup",
            "stale, unsafe, or unnecessarily broad claims",
        )
        for clause in required:
            with self.subTest(clause=clause):
                self.assertIn(clause, self.watchdog_section)

        self.assertIn(
            "When a progress anomaly has a known preventing cause, recommend the Blocked path rather than Stalled.",
            self.watchdog_section,
        )

    def test_watchdog_alerts_only_for_actionable_attention(self) -> None:
        required = (
            "Notify the parent only when action is required.",
            "Identify the affected provider identity or task, observed evidence, reason attention is required, and smallest recommended Coordinator action.",
            "unused capacity with eligible Ready work",
            "without messaging or interrupting the parent",
            "this self-report is its only task-state exception",
            "The parent retains every scheduling, lifecycle, ownership, recovery, dispatch, Commit-application, Persistence-closure, integration, and cleanup decision",
        )
        for clause in required:
            with self.subTest(clause=clause):
                self.assertIn(clause, self.watchdog_section)

    def test_watchdog_never_infers_or_mutates_delivery_semantics(self) -> None:
        required = (
            "must not change repository files, provider records, lifecycle state, claims, task state, branches, worktrees, or shared resources",
            "The parent retains every scheduling, lifecycle, ownership, recovery, dispatch, Commit-application, Persistence-closure, integration, and cleanup decision",
        )
        for clause in required:
            with self.subTest(clause=clause):
                self.assertIn(clause, self.watchdog_section)

        self.assertEqual((), _watchdog_authority_violations(self.watchdog_section))

    def test_watchdog_authority_guard_is_mutation_sensitive(self) -> None:
        prohibited_sentences = (
            "The watchdog infers integration readiness from a quiet Thread.",
            "The watchdog decides accepted delivery after review.",
            "The watchdog determines completion readiness from task state.",
            "The watchdog mutates backlog lifecycle after observing a transition.",
            "The watchdog changes claims and coordination entries during cleanup.",
            "The watchdog mutates task state when a deadline expires.",
            "The watchdog changes work-item lifecycle state.",
            "The watchdog mutates work-item status.",
            "The watchdog must not infer integration readiness but decides accepted delivery.",
        )
        for sentence in prohibited_sentences:
            with self.subTest(prohibited_sentence=sentence):
                with self.assertRaises(AssertionError):
                    self.assertEqual((), _watchdog_authority_violations(sentence))

        valid_mechanical_sentences = (
            "The watchdog determines whether a configured deadline is overdue.",
            "The watchdog changes its own process status after a read-only cycle.",
            "The watchdog reports that an Agent process stopped.",
        )
        for sentence in valid_mechanical_sentences:
            with self.subTest(valid_mechanical_sentence=sentence):
                self.assertEqual((), _watchdog_authority_violations(sentence))

    def test_watchdog_omits_coordination_registry_work_under_none(self) -> None:
        """Branch registry reads, ownership evaluation, and alerts inside the watchdog body."""

        self.assertNotIn(
            "reads current work items, Git state, coordination-registry state, and task state",
            self.watchdog_section,
        )
        for clause in (
            "When agent-claim is loaded, it also reads the claim registry.",
            "stale, unsafe, or unnecessarily broad claims when agent-claim is loaded",
        ):
            with self.subTest(clause=clause):
                self.assertIn(clause, self.watchdog_section)

    def test_coordination_delegates_claim_rules_to_agent_claim(self) -> None:
        """Keep claim behavior in the owning skill."""

        self.assertIn(
            "When agent-claim is loaded, use its Claim Events table and supporting rules.",
            self.skill_text,
        )
        self.assertNotIn("claim-free", self.skill_text)
        self.assertNotIn("needs no claim", self.skill_text)
        self.assertNotIn("exact existing-path and move-destination rule", self.skill_text)
        for adapter_path in _GENERATED_COORDINATOR_ADAPTERS:
            adapter = adapter_path.read_text(encoding="utf-8")
            with self.subTest(adapter=adapter_path.parent.parent.name):
                self.assertIn("enabled resource coordination", adapter)
                self.assertIn("shared mutation authority when enabled", adapter)
                self.assertIn("Provider none", adapter)
                self.assertNotIn(
                    "reads current work items, Git state, coordination-registry state, and task state",
                    adapter,
                )

    def test_canonical_watchdog_templates_render_historical_prompts_byte_for_byte(self) -> None:
        """Only the approved parent-task and repository-root substitutions may vary."""

        standing = _text_template(
            self.skill_text,
            "#### Canonical Standing Prompt Template",
        )
        heartbeat = _text_template(
            self.skill_text,
            "#### Canonical Heartbeat Prompt Template",
        )

        self.assertEqual(
            {"{parent_task_id}", "{repository_root}"},
            set(re.findall(r"\{[^}]+\}", standing)),
        )
        self.assertEqual(
            {"{parent_task_id}"},
            set(re.findall(r"\{[^}]+\}", heartbeat)),
        )
        self.assertEqual(
            HISTORICAL_STANDING_PROMPT,
            standing.replace("{parent_task_id}", HISTORICAL_PARENT_TASK_ID).replace(
                "{repository_root}",
                HISTORICAL_REPOSITORY_ROOT,
            ),
        )
        self.assertEqual(
            HISTORICAL_HEARTBEAT_PROMPT,
            heartbeat.replace("{parent_task_id}", HISTORICAL_PARENT_TASK_ID),
        )

    def test_watchdog_role_is_read_only_simple_and_outside_work_item_capacity(self) -> None:
        """The dedicated role must observe through the coordination contract only."""

        role = yaml.safe_load(WATCHDOG_ROLE_PATH.read_text(encoding="utf-8"))
        role_text = json.dumps(role, sort_keys=True)
        self.assertEqual("dev-backlog-watchdog", role["name"])
        self.assertEqual("never", role["repositoryMutation"])
        self.assertEqual("read-only", role["isolation"])
        self.assertEqual("simple", role["modelProfile"])
        self.assertEqual(
            {"codex-workitem-coordination"},
            {next(iter(entry)) for entry in role["skills"]},
        )
        self.assertIn("outside provider queue and Starting-plus-Running capacity", role_text)
        self.assertIn("canonical standing and heartbeat prompt templates", role_text)
        self.assertEqual(
            {
                "cycle result",
                "blocked reconciliation results",
                "actionable parent alert",
            },
            {next(iter(entry)) for entry in role["outputContract"]},
        )

    def test_blocked_watchdog_reconciliation_retains_results_and_alerts_only_actionable(
        self,
    ) -> None:
        """Keep every Blocked reconciliation while preserving Coordinator authority."""

        role = " ".join(
            WATCHDOG_ROLE_PATH.read_text(encoding="utf-8").split()
        )
        skill = " ".join(self.skill_text.split())
        for clause in (
            "every Blocked item",
            "exact blocker",
            "unblock condition",
            "next-action owner",
            "dependencies",
            "candidate",
            "review and verification evidence",
            "canonical task state",
            "Git state",
            "applicable live claims",
            "concise per-item reconciliation result",
        ):
            with self.subTest(clause=clause):
                self.assertIn(clause, f"{role} {skill}")
        for alert_condition in (
            "satisfied dependency or unblock evidence",
            "agent-actionable recovery",
            "exhausted correction attempts without a current disposition",
            "stale or contradictory lifecycle evidence",
            "incorrect next-action owner",
        ):
            with self.subTest(alert_condition=alert_condition):
                self.assertIn(alert_condition, f"{role} {skill}")
        self.assertIn(
            "never chooses a lifecycle outcome",
            f"{role} {skill}",
        )

    def test_exhausted_corrections_have_four_exact_non_vague_outcomes(self) -> None:
        """Require one concrete Coordinator disposition and retained resume evidence."""

        coordinator = " ".join(
            COORDINATOR_ROLE_PATH.read_text(encoding="utf-8").split()
        )
        contract = f"{coordinator} {' '.join(self.skill_text.split())}"
        for clause in (
            "concrete recovery action, owner, evidence, and links to every unresolved finding",
            "one fresh bounded retry plan",
            "evidence linked to every specific unresolved finding",
            "explanation, genuine user-owned decision, exact User Action Required question",
            "concrete external or technical dependency and observable trigger",
            "Reject a vague or indefinite Blocked outcome",
            "canonical task identity, candidate, review and verification, Git state, claim, and attempt history",
            "immutable decision",
            "Dev Backlog Steward",
        ):
            with self.subTest(clause=clause):
                self.assertIn(clause, contract)

    def test_stalled_and_known_blocker_authority_stays_with_coordinator_and_steward(self) -> None:
        """Observation, disposition, and provider mutation remain separate authorities."""

        provider = MANAGE_FILE_WORK_ITEMS_PATH.read_text(encoding="utf-8")
        coordinator = COORDINATOR_ROLE_PATH.read_text(encoding="utf-8")
        orchestrator = ORCHESTRATOR_ROLE_PATH.read_text(encoding="utf-8")
        steward = STEWARD_ROLE_PATH.read_text(encoding="utf-8")
        contract = "\n".join(
            (self.skill_text, provider, coordinator, orchestrator, steward)
        )
        normalized_contract = " ".join(contract.split())
        for clause in (
            "STALLED: current evidence indicates that the item is not making progress while the causal blocker or unblock condition remains unknown.",
            "Stalled does not count toward Starting-plus-Running capacity",
            "same canonical owner demonstrably resumes safely",
            "ownership has ended and normal redispatch is required",
            "concrete cause and Coordinator-owned next action are known",
            "concrete user-owned action is required",
            "Dev Backlog Coordinator is the lifecycle decision owner for Blocked",
            "Dev Backlog Steward performs the atomic provider mutation",
        ):
            with self.subTest(clause=clause):
                self.assertIn(" ".join(clause.split()), normalized_contract)

    def test_file_provider_series_and_archive_rules_keep_stalled_nonterminal(self) -> None:
        """Series and archive rules must not collapse Stalled into terminal failure."""

        provider = " ".join(
            MANAGE_FILE_WORK_ITEMS_PATH.read_text(encoding="utf-8").split()
        )
        for clause in (
            "active while any required child remains Ready, Starting, Running, or Awaiting Review",
            "stalled when every required nonterminal child is Stalled",
            "report the exact child-state inventory",
            "Stalled is nonterminal and cannot be archived directly",
            "first record Failed or Abandoned with the applicable terminal evidence",
            "matching backlog/failed-backlog type folder",
        ):
            with self.subTest(clause=clause):
                self.assertIn(" ".join(clause.split()), provider)

    def test_file_provider_active_folders_include_stalled_inventory(self) -> None:
        """Folder guidance must not imply that Stalled leaves typed active work."""

        provider = " ".join(
            MANAGE_FILE_WORK_ITEMS_PATH.read_text(encoding="utf-8").split()
        )
        self.assertIn(
            "Active typed folders contain dispatchable work, non-dispatchable "
            "unknown-cause Stalled work, or work Blocked by an explicit "
            "non-user dependency.",
            provider,
        )

    def test_orchestrator_known_blocker_handoff_is_immediate_and_complete(self) -> None:
        """A known blocker must be reported rather than left for watchdog discovery."""

        orchestrator = " ".join(
            ORCHESTRATOR_ROLE_PATH.read_text(encoding="utf-8").split()
        )
        coordinator = " ".join(
            COORDINATOR_ROLE_PATH.read_text(encoding="utf-8").split()
        )
        normalized_orchestrator = " ".join(orchestrator.split())
        for field in (
            "provider identity or provider-none task",
            "canonical Thread",
            "root Agent Task",
            "current phase",
            "exact blocker",
            "blocker owner",
            "unblock condition",
            "requested Coordinator action",
            "preserved commits and evidence",
            "resource-ownership disposition",
            "safe to resume",
        ):
            with self.subTest(field=field):
                self.assertIn(field, normalized_orchestrator)
        self.assertIn(
            "immediately notify the parent Dev Backlog Coordinator",
            orchestrator,
        )
        self.assertIn("acknowledge the blocker notification", coordinator)


class UserActionRequiredExplanationContractTests(unittest.TestCase):
    """Protect clear user-owned questions without false technical gates."""

    def test_user_request_is_explained_after_provider_reconciliation(self) -> None:
        provider = MANAGE_FILE_WORK_ITEMS_PATH.read_text(encoding="utf-8")
        orchestrator = ORCHESTRATOR_ROLE_PATH.read_text(encoding="utf-8")
        contract = " ".join(f"{provider} {orchestrator}".split())

        required = (
            "the provider records that state before presenting the request to the user",
            "Ask one plain-language question.",
            "Explain why the user owns the answer.",
            "an illustrative example",
            "practical consequence",
            "State the unattended-work boundary.",
            "Name the work that must stop",
            "independent work that may safely continue",
        )
        for clause in required:
            with self.subTest(clause=clause):
                self.assertIn(clause, contract)

    def test_vague_fabricated_repeated_and_false_requests_are_rejected(self) -> None:
        provider = MANAGE_FILE_WORK_ITEMS_PATH.read_text(encoding="utf-8")
        orchestrator = ORCHESTRATOR_ROLE_PATH.read_text(encoding="utf-8")
        contract = " ".join(f"{provider} {orchestrator}".split())

        rejected = (
            "Do not hide it inside background information.",
            "Do not invent options, risks, or consequences",
            "do not ask it again",
            "Do not turn a technical dependency, missing tool, implementation failure, or agent-resolvable question into a user choice.",
            "turn an agent-resolvable technical problem into a user choice",
            "repeat a recorded answer",
        )
        for clause in rejected:
            with self.subTest(clause=clause):
                self.assertIn(clause, contract)


class StartingLifecycleContractTests(unittest.TestCase):
    """Protect the durable startup bridge and mechanical watchdog boundaries."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.coordination = SKILL_PATH.read_text(encoding="utf-8")
        cls.provider = MANAGE_FILE_WORK_ITEMS_PATH.read_text(encoding="utf-8")
        cls.roles = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (
                COORDINATOR_ROLE_PATH,
                ORCHESTRATOR_ROLE_PATH,
                STEWARD_ROLE_PATH,
            )
        )
        cls.contract = "\n".join((cls.coordination, cls.provider, cls.roles))
        cls.queue_section = _markdown_section(
            cls.coordination,
            "Queue Target And Dispatch",
        )
        cls.reconciliation_section = _markdown_section(
            cls.coordination,
            "Dispatch Reconciliation",
        )
        cls.ownership_section = _markdown_section(
            cls.coordination,
            "Starting And Work-Item Thread Ownership",
        )
        cls.provider_dispatch_section = _markdown_section(
            cls.provider,
            "Dispatch Workflow",
        )
        cls.blocked_handoff_section = _markdown_section(
            cls.provider,
            "Blocked Handoff And Resumption",
        )
        cls.stalled_investigation_section = _markdown_section(
            cls.coordination,
            "Stalled Investigation And Blocker Handoff",
        )
        cls.provider_recovery_section = _markdown_section(
            cls.provider,
            "Recovery Workflow",
        )
        coordinator_role = yaml.safe_load(
            COORDINATOR_ROLE_PATH.read_text(encoding="utf-8")
        )
        cls.coordinator_decisions = " ".join(
            " ".join(coordinator_role["instructions"]["decisions"]).split()
        )
        cls.coordinator_workflow = " ".join(
            " ".join(coordinator_role["instructions"]["workflow"]).split()
        )

    def test_starting_counts_against_capacity_and_prevents_duplicate_start(self) -> None:
        required = (
            "Ready -> Starting",
            "Starting counts against capacity",
            "canonical task id",
            "must not create a duplicate",
            "ambiguous startup",
        )
        for clause in required:
            with self.subTest(clause=clause):
                self.assertIn(clause, self.contract)

        self.assertIn(
            "Count work items whose provider lifecycle state is Starting or Running.",
            self.queue_section,
        )

        self.assertIn(
            "create at most one user-visible work-item Thread for the Starting work item",
            self.queue_section,
        )
        self.assertIn(
            "Never retry Thread creation after an ambiguous response.",
            self.reconciliation_section,
        )
        self.assertIn(
            "Ready -> Starting is the parent Dev Backlog Coordinator's dispatch and capacity-reservation decision.",
            self.provider_dispatch_section,
        )
        self.assertIn(
            "Starting counts against capacity exactly like Running",
            self.provider_dispatch_section,
        )

    def test_restarted_coordinator_resets_claims_before_dispatch(self) -> None:
        self.assertIn(
            "When restarting after all agents have stopped, run the configured "
            "claim helper's reset command before reading inventory or dispatching work.",
            self.coordinator_workflow,
        )

    def test_stalled_resume_reconciles_capacity_atomically(self) -> None:
        """A refilled vacancy cannot become an eleventh active work item."""

        required = (
            "Stalled -> Running",
            "same serialized provider transaction",
            "Starting-plus-Running count is below ten",
            "preserve Stalled",
        )
        stalled_sections = "\n".join((self.coordination, self.provider))
        for clause in required:
            with self.subTest(clause=clause):
                self.assertIn(clause, stalled_sections)

    def test_retained_stalled_owner_cannot_resume_before_recorded_decision(self) -> None:
        """Retained execution identity is recovery context, not mutation authority."""

        required = (
            "A retained Stalled owner must not resume repository or provider mutation",
            "Coordinator decides Stalled -> Running",
            "Dev Backlog Steward records that transition",
        )
        for source in (self.coordination, self.provider):
            for clause in required:
                with self.subTest(source=source[:20], clause=clause):
                    self.assertIn(clause, source)

    def test_task_anomalies_require_reconciliation_before_lifecycle_choice(self) -> None:
        """Task anomalies preserve lifecycle until separate evidence supports a change."""

        required_contract = (
            "A failed, stopped, or missing canonical task in Starting or Running "
            "is an execution-identity anomaly, not lifecycle evidence.",
            "Preserve the current Starting or Running state and its "
            "Starting-plus-Running capacity while reconciling the canonical task, "
            "provider reservation or record, and ownership.",
            "The anomaly alone authorizes neither Stalled, Blocked, User Action "
            "Required, nor capacity release.",
            "Blocked requires a separately validated known preventing cause and "
            "Coordinator-owned action.",
            "User Action Required requires one separately identified concrete "
            "user-owned action.",
        )
        canonical_sources = {
            "coordination Stalled branch": " ".join(
                self.stalled_investigation_section.split()
            ),
            "file-provider recovery": " ".join(
                self.provider_recovery_section.split()
            ),
            "Coordinator decisions": self.coordinator_decisions,
        }
        for source_name, source in canonical_sources.items():
            for clause in required_contract:
                with self.subTest(source=source_name, clause=clause):
                    self.assertIn(clause, source)

        steward = " ".join(
            STEWARD_ROLE_PATH.read_text(encoding="utf-8").split()
        )
        for clause in required_contract[1:]:
            with self.subTest(source="Steward failure handling", clause=clause):
                self.assertIn(clause.lower(), steward.lower())

        for stale_shortcut in (
            "preserve the evidence and record Blocked or User Action Required",
            "preserve it and record Blocked or User Action Required",
            "preserve ownership evidence and use Blocked or User Action Required",
            "otherwise preserve evidence and record Blocked or User Action Required",
        ):
            with self.subTest(stale_shortcut=stale_shortcut):
                self.assertNotIn(stale_shortcut, self.contract)

    def test_active_folder_model_names_stalled_and_blocked_items(self) -> None:
        """Active typed folders retain both causal states without misclassification."""

        normalized_provider = " ".join(self.provider.split())
        self.assertIn(
            "Active typed folders contain dispatchable work, non-dispatchable "
            "unknown-cause Stalled work, or work Blocked by an explicit non-user "
            "dependency.",
            normalized_provider,
        )

    def test_readme_states_the_exact_lifecycle_authority_split(self) -> None:
        """The public overview must not assign every disposition to one role."""

        readme = README_PATH.read_text(encoding="utf-8")
        for clause in (
            "Dev Backlog Coordinator owns queue decisions, Ready -> Starting reservations, and Stalled or Blocked dispositions",
            "root Dev Orchestrator owns Starting -> Running acceptance and terminal closure requests",
            "Dev Backlog Steward performs each authorized provider mutation",
        ):
            with self.subTest(clause=clause):
                self.assertIn(clause, readme)
        self.assertNotIn("owns every lifecycle disposition", readme)

    def test_start_acceptance_and_recovery_preserve_ownership_evidence(self) -> None:
        required = (
            "Starting -> Running",
            "restore Ready",
            "preserve the current Starting or Running state",
            "branch, worktree, and applicable claim evidence",
            "root Dev Orchestrator",
            "Dev Backlog Steward child",
        )
        for clause in required:
            with self.subTest(clause=clause):
                self.assertIn(clause, self.contract)

        self.assertIn(
            "After the work-item Thread's root Dev Orchestrator Agent accepts ownership, it uses its Dev Backlog Steward child for the atomic Starting -> Running transition.",
            self.ownership_section,
        )
        self.assertIn(
            "Starting -> Running is owned by the root Dev Orchestrator after it accepts the item.",
            self.provider_dispatch_section,
        )
        self.assertIn(
            "Only after the work-item Thread's root Dev Orchestrator Agent accepts ownership",
            self.blocked_handoff_section,
        )

    def test_runtime_terms_remain_distinct(self) -> None:
        for clause in (
            "A Thread is one execution context or conversation.",
            "An Agent is a runtime instance operating under a Role",
            "A Task is a bounded assignment to an Agent; it is never a synonym for Thread.",
        ):
            with self.subTest(clause=clause):
                self.assertIn(clause, self.ownership_section)

        for retired_contradiction in (
            "A Thread is a bounded assignment to an Agent.",
            "A Task is one execution context or conversation.",
            "A Role is a runtime instance",
            "An Agent is a reusable responsibility and authority contract",
        ):
            with self.subTest(retired_contradiction=retired_contradiction):
                self.assertNotIn(retired_contradiction, self.ownership_section)

    def test_retired_capacity_and_startup_shortcuts_stay_absent(self) -> None:
        self.assertEqual(
            (),
            _present_retired_clauses(self.queue_section, _RETIRED_QUEUE_CLAUSES),
        )

        lifecycle_sections = "\n".join(
            (
                self.queue_section,
                self.ownership_section,
                self.provider_dispatch_section,
                self.blocked_handoff_section,
            )
        )
        self.assertEqual(
            (),
            _present_retired_clauses(
                lifecycle_sections,
                _RETIRED_PROVIDER_SHORTCUT_CLAUSES,
            ),
        )
        self.assertEqual(
            (),
            _present_retired_clauses(
                self.reconciliation_section,
                _RETIRED_RECONCILIATION_CLAUSES,
            ),
        )

    def test_exact_retired_clause_guards_are_mutation_sensitive(self) -> None:
        section_cases = (
            ("queue", self.queue_section, _RETIRED_QUEUE_CLAUSES),
            (
                "reconciliation",
                self.reconciliation_section,
                _RETIRED_RECONCILIATION_CLAUSES,
            ),
            (
                "provider",
                "\n".join(
                    (self.provider_dispatch_section, self.blocked_handoff_section)
                ),
                _RETIRED_PROVIDER_SHORTCUT_CLAUSES,
            ),
        )
        for section_name, section, clauses in section_cases:
            for clause in clauses:
                with self.subTest(section=section_name, retired_clause=clause):
                    mutated = f"{section}\n{clause}"
                    with self.assertRaises(AssertionError):
                        self.assertEqual(
                            (),
                            _present_retired_clauses(mutated, clauses),
                        )

    def test_watchdog_reports_mechanical_task_and_coordination_mismatches(self) -> None:
        required = (
            "stopped, failed, or missing canonical task",
            "Starting or Running",
            "every stopped task with a live claim",
            "every terminal item with a live claim",
        )
        for clause in required:
            with self.subTest(clause=clause):
                self.assertIn(clause, self.coordination)

    def test_watchdog_keeps_quiet_active_tasks_healthy_and_never_decides_delivery(self) -> None:
        required = (
            "active quiet tasks",
            "explicit deadline or hard stop",
            "must not change repository files, provider records, lifecycle state, claims, task state, branches, worktrees, or shared resources",
            "The parent retains every scheduling, lifecycle, ownership, recovery, dispatch, Commit-application, Persistence-closure, integration, and cleanup decision",
        )
        normalized_coordination = " ".join(self.coordination.split())
        for clause in required:
            with self.subTest(clause=clause):
                self.assertIn(clause, normalized_coordination)


class AwaitingReviewPersistenceContractTests(unittest.TestCase):
    """Keep nonterminal and terminal Persistence updates distinct and idempotent."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.skill_text = SKILL_PATH.read_text(encoding="utf-8")
        cls.role_text = json.dumps(
            yaml.safe_load(ORCHESTRATOR_ROLE_PATH.read_text(encoding="utf-8")),
            sort_keys=True,
        )

    def test_coordination_records_awaiting_review_once_before_terminal_closure(self) -> None:
        required = (
            "ask Dev Backlog Steward exactly once to record the nonterminal lifecycle AWAITING_REVIEW",
            "reconcile the existing update instead of dispatching a duplicate",
            "Never request lifecycle COMPLETED from an AWAITING_REVIEW handoff",
            "ask Dev Backlog Steward exactly once for the distinct terminal lifecycle COMPLETED update",
        )
        for clause in required:
            with self.subTest(clause=clause):
                self.assertIn(clause, self.skill_text)

    def test_orchestrator_routes_the_same_two_phase_persistence_sequence(self) -> None:
        required = (
            "dispatch dev-backlog-steward exactly once to record the nonterminal AWAITING_REVIEW lifecycle update",
            "reconcile that recorded update instead of dispatching a duplicate",
            "Do not request lifecycle COMPLETED while Commit is AWAITING_REVIEW",
            "dispatch dev-backlog-steward exactly once for the distinct terminal COMPLETED update",
        )
        for clause in required:
            with self.subTest(clause=clause):
                self.assertIn(clause, self.role_text)


if __name__ == "__main__":
    unittest.main()
