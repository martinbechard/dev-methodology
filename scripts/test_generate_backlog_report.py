# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies backlog report inventory, Future Ideas authority, reconciliation, ordering, and offline HTML output.
# Governing backlog items: backlog/feature-backlog/add-styled-backlog-report-with-user-input.md, backlog/feature-backlog/add-lightweight-future-ideas-capture.md, and backlog/feature-backlog/add-dedicated-watchdog-and-stalled-lifecycle.md

"""Focused tests for the styled backlog report generator."""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT_PATH = Path(__file__).with_name("generate-backlog-report.py")
EXAMPLE_PATH = SCRIPT_PATH.parent.parent / "backlog" / "examples" / "styled-backlog-report.html"
_COMPLETE_STALLED_EVIDENCE = {
    "Last Known Productive Evidence": "Candidate commit retained.",
    "Phase Estimate": "Not present",
    "Hard Stop": "Not present",
    "Anomaly or Progress Gap": "No evidence-bearing output after the focused test began.",
    "Canonical Conversation": "conversation-stalled-fixture",
    "Root Agent Task": "task-stalled-fixture",
    "Current Ownership and Coordination State": (
        "Dev Orchestrator retains the canonical worktree; no active file claim."
    ),
    "Diagnostic Owner": "Dev Backlog Coordinator",
    "Next Investigation Action": "Inspect the retained focused-test trace.",
}
SPEC = importlib.util.spec_from_file_location("generate_backlog_report", SCRIPT_PATH)
assert SPEC and SPEC.loader
REPORT = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = REPORT
SPEC.loader.exec_module(REPORT)


class BacklogReportTest(unittest.TestCase):
    """Exercise report behavior through temporary repository-shaped fixtures."""

    def setUp(self) -> None:
        """Create a disposable repository root for each observable behavior test."""
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.output = self.root / "out" / "report.html"

    def tearDown(self) -> None:
        """Remove all fixture and generated files after each test."""
        self.temporary.cleanup()

    def write_item(
        self,
        relative: str,
        *,
        title: str,
        status: str,
        item_type: str,
        dependencies: str = "None",
        context: str = "Fixture context.",
        completion: str = "direct-main",
        include_open_questions: bool = True,
        owner: str = "",
        diagnostic_owner: str = "",
        next_investigation_action: str = "",
        work_item_id: str | None = None,
        source_evidence: str = "",
        stalled_evidence: dict[str, str] | None = None,
        extra: str = "",
    ) -> None:
        """Write one complete backlog item with optional queue-specific sections."""
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        open_questions = (
            "## Open Questions\n\nNone\n\n" if include_open_questions else ""
        )
        lifecycle_fields = "".join(
            (
                f"\nOwner: {owner}\n" if owner else "",
                f"\nDiagnostic Owner: {diagnostic_owner}\n"
                if diagnostic_owner
                else "",
                f"\nNext Investigation Action: {next_investigation_action}\n"
                if next_investigation_action
                else "",
            )
        )
        source_evidence_section = (
            f"## Source Evidence\n\n{source_evidence}\n\n"
            if source_evidence
            else ""
        )
        stalled_evidence_section = ""
        if stalled_evidence is not None:
            stalled_evidence_section = "## Stalled Evidence\n\n"
            stalled_evidence_section += "\n".join(
                f"{name}: {value}" for name, value in stalled_evidence.items()
            )
            stalled_evidence_section += "\n\n"
        path.write_text(
            f"""# {title}

Status: {status}

Type: {item_type}

Provider: file

Work Item ID: {work_item_id or path.stem}

Completion: {completion}
{lifecycle_fields}

## Summary

Summary for {title}.

## Context

{context}

## Requirements

- Deliver it.

## Acceptance Criteria

- It works.

## Dependencies

{dependencies}

## Verification

- Verify it.

{source_evidence_section}
{stalled_evidence_section}
{open_questions}
{extra}""",
            encoding="utf-8",
        )

    def write_idea(
        self,
        relative: str,
        *,
        title: str,
        synopsis: str = "A potentially useful direction.",
        origin: str = "Observed during repository work.",
        notes: str = "",
        revisit_trigger: str = "",
        promoted_to: str = "",
    ) -> None:
        """Write one lightweight Future Idea without work-item lifecycle fields."""
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        promoted_field = f"\nPromoted To: {promoted_to}\n" if promoted_to else ""
        optional_sections = ""
        if notes:
            optional_sections += f"\n## Notes\n\n{notes}\n"
        if revisit_trigger:
            optional_sections += f"\n## Revisit Trigger\n\n{revisit_trigger}\n"
        path.write_text(
            f"""# {title}
{promoted_field}
## Synopsis

{synopsis}

## Origin or Rationale

{origin}
{optional_sections}""",
            encoding="utf-8",
        )

    def generate(
        self,
        timestamp: str = "2026-07-19T06:00:00+00:00",
        *,
        include_future_ideas: bool = False,
    ) -> str:
        """Generate and return one report at a controlled snapshot time."""
        REPORT.generate_report(
            self.root,
            self.output,
            timestamp,
            include_future_ideas=include_future_ideas,
        )
        return self.output.read_text(encoding="utf-8")

    def test_future_ideas_are_excluded_by_default_and_listed_only_by_opt_in(self) -> None:
        """Future Ideas stay outside ordinary inventory, runnable counts, and Holding."""
        self.write_item(
            "backlog/feature-backlog/ready.md",
            title="Ready Work",
            status="Ready",
            item_type="Feature",
        )
        self.write_item(
            "backlog/holding/deferred.md",
            title="Deferred Work",
            status="Holding",
            item_type="Feature",
        )
        self.write_idea(
            "backlog/future-ideas/context-map.md",
            title="Context Map",
            notes="Compare two possible visual forms.",
            revisit_trigger="Revisit when the navigation model changes.",
        )
        (self.root / "backlog/future-ideas/index.md").write_text(
            "# Ideas\n\n- [Context Map](context-map.md)\n", encoding="utf-8"
        )

        ordinary = self.generate()

        self.assertNotIn("Context Map", ordinary)
        self.assertNotIn("backlog/future-ideas", ordinary)
        self.assertIn("<span>Active typed items</span><strong>1</strong>", ordinary)
        self.assertIn("<span>Runnable now</span><strong>1</strong>", ordinary)
        self.assertIn("<span>Holding</span><strong>1</strong>", ordinary)

        explicit = self.generate(include_future_ideas=True)

        self.assertIn("<span>Future ideas</span><strong>1</strong>", explicit)
        self.assertIn("<h2>Future Ideas</h2>", explicit)
        self.assertIn("Context Map", explicit)
        self.assertIn("A potentially useful direction.", explicit)
        self.assertIn("Observed during repository work.", explicit)
        self.assertIn("Compare two possible visual forms.", explicit)
        self.assertIn("Revisit when the navigation model changes.", explicit)
        self.assertIn("Not promoted", explicit)
        self.assertIn("backlog/future-ideas/context-map.md", explicit)
        self.assertIn("backlog/future-ideas/index.md", explicit)
        self.assertIn("<span>Active typed items</span><strong>1</strong>", explicit)
        self.assertIn("<span>Runnable now</span><strong>1</strong>", explicit)
        self.assertIn("<span>Holding</span><strong>1</strong>", explicit)

    def test_default_report_does_not_enumerate_read_or_stat_future_ideas(self) -> None:
        """The excluded Future Ideas store remains completely untouched by default."""
        self.write_item(
            "backlog/feature-backlog/ready.md",
            title="Ready Work",
            status="Ready",
            item_type="Feature",
        )
        self.write_idea(
            "backlog/future-ideas/unscanned.md",
            title="Unscanned",
        )
        original_rglob = Path.rglob
        original_read_text = Path.read_text
        original_stat = Path.stat

        def is_idea_path(path: Path) -> bool:
            parts = path.parts
            return any(
                parts[index : index + 2] == ("backlog", "future-ideas")
                for index in range(len(parts) - 1)
            )

        def reject_idea_rglob(path: Path, pattern: str):
            if is_idea_path(path):
                raise AssertionError("default report enumerated Future Ideas")
            return original_rglob(path, pattern)

        def reject_idea_read(
            path: Path, *args: object, **kwargs: object
        ) -> str:
            if is_idea_path(path):
                raise AssertionError("default report read Future Ideas")
            return original_read_text(path, *args, **kwargs)

        def reject_idea_stat(
            path: Path, *args: object, **kwargs: object
        ) -> os.stat_result:
            if is_idea_path(path):
                raise AssertionError("default report stated Future Ideas")
            return original_stat(path, *args, **kwargs)

        with (
            mock.patch.object(Path, "rglob", reject_idea_rglob),
            mock.patch.object(Path, "read_text", reject_idea_read),
            mock.patch.object(Path, "stat", reject_idea_stat),
        ):
            rendered = self.generate()

        self.assertNotIn("Unscanned", rendered)

    def test_promoted_ideas_validate_active_holding_and_user_action_targets(self) -> None:
        """Promotion accepts complete targets in each deliberate destination."""
        destinations = (
            (
                "active",
                "backlog/feature-backlog/active.md",
                "Ready",
                "Feature",
                "direct-main",
                "",
            ),
            (
                "holding",
                "backlog/holding/holding.md",
                "Holding",
                "Holding",
                "feature-branch",
                "",
            ),
            (
                "user-action",
                "backlog/user-action-required/user-action.md",
                "User Action Required",
                "Feature",
                "UNSET",
                """## User Action Required

The user owns the remaining decision.

## Question for the User

Should this work proceed?

## Why User Input Is Required

Only the user can authorize it.

## Resolution

Pending.

## Unattended Work Boundary

Do not implement.
""",
            ),
        )
        for slug, target, status, item_type, completion, destination_sections in destinations:
            source = f"backlog/future-ideas/{slug}.md"
            self.write_idea(source, title=f"{slug.title()} Idea", promoted_to=target)
            self.write_item(
                target,
                title=f"{slug.title()} Work",
                status=status,
                item_type=item_type,
                completion=completion,
                extra=f"""## Source Evidence

- {source}

{destination_sections}""",
            )

        rendered = self.generate(include_future_ideas=True)

        self.assertIn("<span>Future ideas</span><strong>3</strong>", rendered)
        self.assertNotIn("Promotion target is not a complete work item", rendered)
        self.assertNotIn(
            "Promotion target Source Evidence does not reference", rendered
        )

    def test_promotion_requires_supported_completion_and_reciprocal_source_evidence(
        self,
    ) -> None:
        """Unsupported completion or a source path outside Source Evidence fails validation."""
        invalid_completion_source = "backlog/future-ideas/invalid-completion.md"
        invalid_completion_target = "backlog/holding/invalid-completion.md"
        self.write_idea(
            invalid_completion_source,
            title="Invalid Completion",
            promoted_to=invalid_completion_target,
        )
        self.write_item(
            invalid_completion_target,
            title="Invalid Completion Work",
            status="Holding",
            item_type="Feature",
            completion="someday",
            extra=f"## Source Evidence\n\n- {invalid_completion_source}\n",
        )
        misplaced_source = "backlog/future-ideas/misplaced-source.md"
        misplaced_target = "backlog/feature-backlog/misplaced-source.md"
        self.write_idea(
            misplaced_source,
            title="Misplaced Source",
            promoted_to=misplaced_target,
        )
        self.write_item(
            misplaced_target,
            title="Misplaced Source Work",
            status="Ready",
            item_type="Feature",
            extra=f"""## Source Evidence

- unrelated observation

## Notes

The source path appears here instead: {misplaced_source}
""",
        )

        rendered = self.generate(include_future_ideas=True)

        self.assertIn(
            f"Promotion target is not a complete work item: {invalid_completion_target}.",
            rendered,
        )
        self.assertIn(
            f"Promotion target Source Evidence does not reference {misplaced_source}: {misplaced_target}.",
            rendered,
        )

    def test_promotion_requires_open_questions_in_the_complete_target(self) -> None:
        """A promoted ordinary record without Open Questions remains incomplete."""
        source = "backlog/future-ideas/missing-open-questions.md"
        target = "backlog/feature-backlog/missing-open-questions.md"
        self.write_idea(
            source,
            title="Missing Open Questions",
            promoted_to=target,
        )
        self.write_item(
            target,
            title="Missing Open Questions Work",
            status="Ready",
            item_type="Feature",
            include_open_questions=False,
            extra=f"## Source Evidence\n\n- {source}\n",
        )

        rendered = self.generate(include_future_ideas=True)

        self.assertIn(
            f"Promotion target is not a complete work item: {target}.",
            rendered,
        )

    def test_promotion_resolves_the_provider_owned_work_item_id(self) -> None:
        """Future Ideas link to an opaque item ID rather than a current path."""
        source = "backlog/future-ideas/provider-owned-id.md"
        target = "backlog/feature-backlog/provider-owned-id.md"
        self.write_idea(
            source,
            title="Provider Owned ID",
            promoted_to="provider-owned-id",
        )
        self.write_item(
            target,
            title="Provider Owned ID Work",
            status="Ready",
            item_type="Feature",
            extra=f"## Source Evidence\n\n- {source}\n",
        )

        rendered = self.generate(include_future_ideas=True)

        self.assertNotIn("Invalid Promoted To Work Item ID", rendered)
        self.assertNotIn("Promotion target is not a complete work item", rendered)
        self.assertIn(
            "<strong>Promoted To:</strong> provider-owned-id",
            rendered,
        )

    def test_missing_minimal_future_idea_fields_are_reported(self) -> None:
        """Opt-in validation reports missing title, Synopsis, and rationale fields."""
        incomplete = self.root / "backlog/future-ideas/incomplete.md"
        incomplete.parent.mkdir(parents=True)
        incomplete.write_text("## Notes\n\nOnly a note.\n", encoding="utf-8")

        rendered = self.generate(include_future_ideas=True)

        self.assertIn(
            "Missing required idea fields: Title, Synopsis, Origin or Rationale.",
            rendered,
        )

    def test_outward_symlinked_idea_and_promotion_target_are_not_read(self) -> None:
        """Symlinked records outside their canonical roots are findings, never authority."""
        ideas_root = self.root / "backlog/future-ideas"
        ideas_root.mkdir(parents=True)
        external_idea = self.root / "external-idea.md"
        external_idea.write_text(
            "# External Idea Secret\n\n## Synopsis\n\nDo not read me.\n\n"
            "## Origin or Rationale\n\nExternal.\n",
            encoding="utf-8",
        )
        (ideas_root / "escaped.md").symlink_to(external_idea)

        source = "backlog/future-ideas/promoted.md"
        target = "backlog/feature-backlog/escaped-target.md"
        self.write_idea(source, title="Promoted", promoted_to=target)
        external_target = self.root / "external-target.md"
        self.write_item(
            "external-target.md",
            title="External Target Secret",
            status="Ready",
            item_type="Feature",
            extra=f"## Source Evidence\n\n- {source}\n",
        )
        target_path = self.root / target
        target_path.parent.mkdir(parents=True)
        target_path.symlink_to(external_target)

        rendered = self.generate(include_future_ideas=True)

        self.assertIn(
            "Future Idea resolves outside canonical Future Ideas authority", rendered
        )
        self.assertIn(
            "Promotion target resolves outside canonical backlog authority", rendered
        )
        self.assertNotIn("External Idea Secret", rendered)
        self.assertNotIn("External Target Secret", rendered)

    def test_inventory_user_input_dependencies_order_and_ignored_files(self) -> None:
        """The report inventories every queue while enforcing dispatch and guidance rules."""
        self.write_item(
            "backlog/completed-backlog/features/base.md",
            title="Base",
            status="Completed",
            item_type="Feature",
        )
        series = self.root / "backlog/feature-backlog/platform"
        series.mkdir(parents=True)
        (series / "index.md").write_text(
            "# Platform Series\n\n## Recommended Order\n\n1. [Second](second.md)\n2. [First](first.md)\n",
            encoding="utf-8",
        )
        self.write_item(
            "backlog/feature-backlog/platform/first.md",
            title="First",
            status="Ready",
            item_type="Feature",
            dependencies="- missing-base",
        )
        self.write_item(
            "backlog/feature-backlog/platform/second.md",
            title="Second",
            status="Ready",
            item_type="Defect",
            dependencies="- [Base](../../completed-backlog/features/base.md)",
        )
        user_extra = """## User Action Required

User decision.

## Question for the User

May we use the exact option & preserve wording?

## Why User Input Is Required

Only the user owns approval.

## Resolution

Pending — no answer inferred.

## Unattended Work Boundary

Do not implement.
"""
        self.write_item(
            "backlog/user-action-required/choose.md",
            title="Choose",
            status="User Action Required",
            item_type="Analysis",
            extra=user_extra,
        )
        readme = self.root / "backlog/user-action-required/README.md"
        readme.write_text("# Queue Guidance\n", encoding="utf-8")
        self.write_item("backlog/holding/later.md", title="Later", status="Holding", item_type="Feature")
        self.write_item("backlog/holding/drift.md", title="Holding Drift", status="Ready", item_type="Feature")
        self.write_item("backlog/failed-backlog/defects/broken.md", title="Broken", status="Failed", item_type="Defect")

        rendered = self.generate()

        self.assertIn("<span>Active typed items</span><strong>2</strong>", rendered)
        self.assertIn("<span>Runnable now</span><strong>1</strong>", rendered)
        self.assertIn("<span>Needs your input</span><strong>1</strong>", rendered)
        self.assertIn("<span>Holding</span><strong>2</strong>", rendered)
        self.assertIn("<span>Completed archive</span><strong>1</strong>", rendered)
        self.assertIn("<span>Failed archive</span><strong>1</strong>", rendered)
        self.assertLess(rendered.index("Second"), rendered.index("First"))
        self.assertIn("Recommended order: 1", rendered)
        self.assertIn("May we use the exact option &amp; preserve wording?", rendered)
        self.assertIn("Pending — no answer inferred.", rendered)
        self.assertIn("Status: User Action Required", rendered)
        self.assertNotIn("no dispatchable underlying Type: Analysis", rendered)
        self.assertIn("Folder and Type mismatch", rendered)
        self.assertIn("Holding item has a non-Holding declared status.", rendered)
        self.assertIn("Unresolved dependency: missing-base.", rendered)
        self.assertIn("backlog/feature-backlog/platform/index.md", rendered)
        self.assertIn("backlog/user-action-required/README.md", rendered)
        self.assertNotIn("Queue Guidance</h3>", rendered)
        needs_input = rendered[rendered.index("Needs Your Input"):rendered.index("Runnable Work")]
        runnable = rendered[rendered.index("Runnable Work"):rendered.index("Blocked Work")]
        self.assertIn("Choose", needs_input)
        self.assertNotIn("Choose", runnable)
        self.assertIn("backlog/user-action-required/choose.md", rendered)
        self.assertNotIn("<script", rendered.lower())
        self.assertNotIn("https://", rendered.lower())

    def test_stalled_inventory_is_separate_and_shows_diagnostic_action(self) -> None:
        """Stalled work must not be rendered as runnable or Blocked inventory."""

        self.write_item(
            "backlog/feature-backlog/suspected-stall.md",
            title="Suspected Stall",
            status="Stalled",
            item_type="Feature",
            owner="Dev Orchestrator task-17",
            source_evidence="Focused test output retained at artifacts/test-output.txt.",
            stalled_evidence={
                **_COMPLETE_STALLED_EVIDENCE,
                "Next Investigation Action": "Inspect the last retained test output.",
            },
        )
        self.write_item(
            "backlog/defect-backlog/known-blocker.md",
            title="Known Blocker",
            status="Blocked",
            item_type="Defect",
        )

        rendered = self.generate()

        self.assertIn("<span>Stalled</span><strong>1</strong>", rendered)
        stalled_start = rendered.index("Stalled Work")
        blocked_start = rendered.index("Blocked Work")
        stalled = rendered[stalled_start:blocked_start]
        blocked = rendered[blocked_start:rendered.index("Holding", blocked_start)]
        runnable = rendered[rendered.index("Runnable Work"):stalled_start]
        self.assertIn("Suspected Stall", stalled)
        self.assertIn("Diagnostic Owner", stalled)
        self.assertIn("Dev Backlog Coordinator", stalled)
        self.assertIn("Next Investigation Action", stalled)
        self.assertIn("Inspect the last retained test output.", stalled)
        field_offsets = [
            stalled.index(f"<dt>{field}</dt>")
            for field in _COMPLETE_STALLED_EVIDENCE
        ]
        self.assertEqual(sorted(field_offsets), field_offsets)
        self.assertIn("<dt>Phase Estimate</dt><dd>Not present</dd>", stalled)
        self.assertIn("<dt>Hard Stop</dt><dd>Not present</dd>", stalled)
        self.assertNotIn("Missing Stalled evidence", rendered)
        self.assertNotIn("Suspected Stall", runnable)
        self.assertNotIn("Suspected Stall", blocked)
        self.assertIn("Known Blocker", blocked)

    def test_stalled_canonical_conversation_satisfies_validation(self) -> None:
        """Canonical Conversation is the required Stalled execution identity."""

        self.write_item(
            "backlog/feature-backlog/canonical-conversation.md",
            title="Canonical Conversation",
            status="Stalled",
            item_type="Feature",
            stalled_evidence=_COMPLETE_STALLED_EVIDENCE,
        )

        rendered = self.generate()

        self.assertNotIn(
            "Missing Stalled evidence: Canonical Conversation.",
            rendered,
        )
        self.assertIn(
            "<dt>Canonical Conversation</dt>"
            "<dd>conversation-stalled-fixture</dd>",
            rendered,
        )

    def test_legacy_canonical_thread_does_not_satisfy_stalled_validation(self) -> None:
        """Canonical Thread alone is migration debt, not canonical Stalled evidence."""

        stalled_evidence = dict(_COMPLETE_STALLED_EVIDENCE)
        del stalled_evidence["Canonical Conversation"]
        stalled_evidence["Canonical Thread"] = "thread-stalled-fixture"
        self.write_item(
            "backlog/feature-backlog/legacy-canonical-thread.md",
            title="Legacy Canonical Thread",
            status="Stalled",
            item_type="Feature",
            stalled_evidence=stalled_evidence,
        )

        rendered = self.generate()

        self.assertIn(
            "Missing Stalled evidence: Canonical Conversation.",
            rendered,
        )
        self.assertIn(
            "<dt>Canonical Conversation</dt><dd>Missing</dd>",
            rendered,
        )
        self.assertNotIn("<dt>Canonical Thread</dt>", rendered)

    def test_semantic_status_badges_are_distinct_and_wcag_aa_conformant(self) -> None:
        """Critical lifecycle badges need distinct classes and accessible palettes."""

        self.write_item(
            "backlog/feature-backlog/stalled.md",
            title="Stalled Item",
            status="Stalled",
            item_type="Feature",
            source_evidence="Retained trace at artifacts/stalled-trace.txt.",
            stalled_evidence=_COMPLETE_STALLED_EVIDENCE,
        )
        self.write_item(
            "backlog/defect-backlog/blocked.md",
            title="Blocked Item",
            status="Blocked",
            item_type="Defect",
        )
        self.write_item(
            "backlog/user-action-required/decision.md",
            title="Decision Item",
            status="User Action Required",
            item_type="Analysis",
            extra="""## User Action Required

### Exact Question

Which option should be selected?

### Why Input Is Required

Only the user owns this choice.

### Unattended-Work Boundary

Do not continue without the answer.
""",
        )

        rendered = self.generate()

        expected_badges = {
            "Stalled": "badge-status-stalled",
            "Blocked": "badge-status-blocked",
            "User Action Required": "badge-status-user-action-required",
        }
        for label, semantic_class in expected_badges.items():
            with self.subTest(label=label):
                self.assertIn(
                    f'<span class="badge badge-status {semantic_class}">{label}</span>',
                    rendered,
                )
                self.assertIn(f".{semantic_class}", rendered)
        self.assertEqual(3, len(set(expected_badges.values())))

        palettes = {
            "stalled-light": ("#7a3a0c", "#fff0df"),
            "blocked-light": ("#8c1d2c", "#fdebed"),
            "user-action-light": ("#5c3cad", "#f0ebff"),
            "stalled-dark": ("#ffc39c", "#4e2b18"),
            "blocked-dark": ("#ffb3bd", "#541f29"),
            "user-action-dark": ("#d0c1ff", "#35265b"),
        }

        def relative_luminance(color: str) -> float:
            channels = [
                int(color[index : index + 2], 16) / 255
                for index in (1, 3, 5)
            ]
            linear = [
                channel / 12.92
                if channel <= 0.04045
                else ((channel + 0.055) / 1.055) ** 2.4
                for channel in channels
            ]
            return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]

        for name, (foreground, background) in palettes.items():
            with self.subTest(palette=name):
                lighter, darker = sorted(
                    (relative_luminance(foreground), relative_luminance(background)),
                    reverse=True,
                )
                self.assertGreaterEqual((lighter + 0.05) / (darker + 0.05), 4.5)
                self.assertIn(foreground, rendered)
                self.assertIn(background, rendered)

    def test_stalled_records_require_complete_diagnostic_evidence(self) -> None:
        """Validation must identify every absent canonical Stalled evidence field."""

        for index, missing_field in enumerate(_COMPLETE_STALLED_EVIDENCE):
            evidence = dict(_COMPLETE_STALLED_EVIDENCE)
            del evidence[missing_field]
            self.write_item(
                f"backlog/feature-backlog/missing-{index}.md",
                title=f"Missing {missing_field}",
                status="Stalled",
                item_type="Feature",
                diagnostic_owner="Legacy Diagnostic Owner",
                next_investigation_action="Legacy next action.",
                source_evidence="Arbitrary general provenance that is not Stalled evidence.",
                stalled_evidence=evidence,
            )

        rendered = self.generate()

        for missing_field in _COMPLETE_STALLED_EVIDENCE:
            with self.subTest(missing_field=missing_field):
                self.assertEqual(
                    1,
                    rendered.count(f"Missing Stalled evidence: {missing_field}."),
                )
        self.assertNotIn("Missing Stalled evidence: Source Evidence.", rendered)

    def test_legacy_stalled_labels_render_but_do_not_satisfy_validation(self) -> None:
        """Legacy display fields remain visible without replacing canonical evidence."""

        self.write_item(
            "backlog/feature-backlog/legacy-stalled.md",
            title="Legacy Stalled",
            status="Stalled",
            item_type="Feature",
            owner="Dev Orchestrator legacy-task",
            diagnostic_owner="Legacy Diagnostic Owner",
            next_investigation_action="Inspect the legacy retained trace.",
            source_evidence="A general source reference.",
        )

        rendered = self.generate()

        self.assertIn(
            "<dt>Diagnostic Owner</dt><dd>Legacy Diagnostic Owner</dd>",
            rendered,
        )
        self.assertIn(
            "<dt>Next Investigation Action</dt>"
            "<dd>Inspect the legacy retained trace.</dd>",
            rendered,
        )
        for missing_field in _COMPLETE_STALLED_EVIDENCE:
            with self.subTest(missing_field=missing_field):
                self.assertIn(
                    f"Missing Stalled evidence: {missing_field}.",
                    rendered,
                )

    def test_committed_example_remains_a_curated_semantic_reference(self) -> None:
        """The visual fixture must not become a live operational backlog snapshot."""

        example = EXAMPLE_PATH.read_text(encoding="utf-8")

        self.assertIn(
            "Deterministic curated visual fixture based on generator output. "
            "This is not current backlog status.",
            example,
        )
        self.assertIn("This example is not current backlog status.", example)
        self.assertIn(
            "synthetic-fixture/user-action-required/example-report-audience.md",
            example,
        )
        self.assertIn(
            "synthetic-fixture/stalled/retained-verification-gap.md",
            example,
        )
        self.assertIn("<dt>Diagnostic Owner</dt>", example)
        self.assertIn("<dt>Next Investigation Action</dt>", example)
        for field in _COMPLETE_STALLED_EVIDENCE:
            with self.subTest(field=field):
                fixture_field = (
                    "Canonical Thread"
                    if field == "Canonical Conversation"
                    else field
                )
                self.assertIn(f"<dt>{fixture_field}</dt>", example)

    def test_external_prerequisites_remain_complete_unmet_and_non_runnable(self) -> None:
        """Plain-language prerequisites retain their text and require manual satisfaction."""
        self.write_item(
            "backlog/feature-backlog/python-runtime.md",
            title="Python Runtime",
            status="Ready",
            item_type="Feature",
            dependencies="- Python 3.11 or newer installed",
        )
        self.write_item(
            "backlog/analysis-backlog/template-conformance.md",
            title="Template Conformance",
            status="Ready",
            item_type="Analysis",
            dependencies="- Enforce Documentation Template Conformance.",
        )

        rendered = self.generate()

        self.assertIn("<span>Runnable now</span><strong>0</strong>", rendered)
        self.assertIn(
            "External prerequisite requires manual satisfaction: Python 3.11 or newer installed",
            rendered,
        )
        self.assertIn(
            "External prerequisite requires manual satisfaction: Enforce Documentation Template Conformance.",
            rendered,
        )
        self.assertIn("Python 3.11 or newer installed (unmet)", rendered)
        self.assertIn("Enforce Documentation Template Conformance. (unmet)", rendered)
        self.assertNotIn("Invalid dependency identifier: Python.", rendered)
        self.assertNotIn("Invalid dependency identifier: Enforce.", rendered)
        runnable = rendered[rendered.index("Runnable Work"):rendered.index("Blocked Work")]
        blocked_start = rendered.index("Blocked Work")
        blocked = rendered[blocked_start:rendered.index("Holding", blocked_start)]
        self.assertNotIn("Python Runtime", runnable)
        self.assertNotIn("Template Conformance", runnable)
        self.assertIn("Python Runtime", blocked)
        self.assertIn("Template Conformance", blocked)

    def test_embedded_local_markdown_link_remains_a_manual_prerequisite(self) -> None:
        """A local link embedded in prose cannot borrow same-stem completion evidence."""
        self.write_item(
            "backlog/completed-backlog/features/base.md",
            title="Base",
            status="Completed",
            item_type="Feature",
        )
        dependency = (
            "Complete [Base](../completed-backlog/features/base.md) before release"
        )
        self.write_item(
            "backlog/feature-backlog/embedded-link.md",
            title="Embedded Link",
            status="Ready",
            item_type="Feature",
            dependencies=f"- {dependency}",
        )

        rendered = self.generate()

        self.assertIn("<span>Runnable now</span><strong>0</strong>", rendered)
        self.assertIn(f"{dependency} (unmet)", rendered)
        self.assertIn(
            f"External prerequisite requires manual satisfaction: {dependency}",
            rendered,
        )
        runnable = rendered[rendered.index("Runnable Work"):rendered.index("Blocked Work")]
        self.assertNotIn("Embedded Link", runnable)
        self.assertNotIn("base (satisfied)", runnable)

    def test_punctuation_wrapped_markdown_links_remain_verbatim_manual_prerequisites(
        self,
    ) -> None:
        """Link prose without whitespace cannot be mistaken for a local identifier."""
        self.write_item(
            "backlog/completed-backlog/features/base.md",
            title="Base",
            status="Completed",
            item_type="Feature",
        )
        dependencies = {
            "Wrapped Local Link": "([Base](../completed-backlog/features/base.md))",
            "Wrapped External Link": (
                "([Base](https://example.invalid/base.md?view=full#approval))"
            ),
        }
        for title, dependency in dependencies.items():
            self.write_item(
                f"backlog/feature-backlog/{title.lower().replace(' ', '-')}.md",
                title=title,
                status="Ready",
                item_type="Feature",
                dependencies=f"- {dependency}",
            )

        rendered = self.generate()

        self.assertIn("<span>Runnable now</span><strong>0</strong>", rendered)
        runnable = rendered[rendered.index("Runnable Work"):rendered.index("Blocked Work")]
        for title, dependency in dependencies.items():
            with self.subTest(dependency=dependency):
                self.assertIn(f"{dependency} (unmet)", rendered)
                self.assertIn(
                    f"External prerequisite requires manual satisfaction: {dependency}",
                    rendered,
                )
                self.assertNotIn(f"Invalid dependency identifier: {dependency}", rendered)
                self.assertNotIn(title, runnable)
        self.assertNotIn("base (satisfied)", rendered)

    def test_external_markdown_uri_with_query_and_fragment_remains_manual(self) -> None:
        """An external link remains verbatim and cannot borrow same-stem completion evidence."""
        self.write_item(
            "backlog/completed-backlog/features/base.md",
            title="Base",
            status="Completed",
            item_type="Feature",
        )
        dependency = "[Base](https://example.invalid/base.md?view=full#approval)"
        self.write_item(
            "backlog/feature-backlog/external-link.md",
            title="External Link",
            status="Ready",
            item_type="Feature",
            dependencies=f"- {dependency}",
        )

        rendered = self.generate()

        self.assertIn("<span>Runnable now</span><strong>0</strong>", rendered)
        self.assertIn(f"{dependency} (unmet)", rendered)
        self.assertIn(
            f"External prerequisite requires manual satisfaction: {dependency}",
            rendered,
        )
        runnable = rendered[rendered.index("Runnable Work"):rendered.index("Blocked Work")]
        self.assertNotIn("External Link", runnable)
        self.assertNotIn("base (satisfied)", runnable)

    def test_nonlocal_markdown_paths_cannot_match_completed_local_slugs(self) -> None:
        """Absolute and backlog-escaping links remain manual despite matching stems."""
        self.write_item(
            "backlog/completed-backlog/features/base.md",
            title="Base",
            status="Completed",
            item_type="Feature",
        )
        dependencies = {
            "Absolute Link": "[Base](/tmp/base.md)",
            "Escaping Link": "[Base](../../outside/base.md)",
            "Plain External URI": "https://example.invalid/base.md?view=full#approval",
        }
        for title, dependency in dependencies.items():
            self.write_item(
                f"backlog/feature-backlog/{title.lower().replace(' ', '-')}.md",
                title=title,
                status="Ready",
                item_type="Feature",
                dependencies=f"- {dependency}",
            )

        rendered = self.generate()

        self.assertIn("<span>Runnable now</span><strong>0</strong>", rendered)
        runnable = rendered[rendered.index("Runnable Work"):rendered.index("Blocked Work")]
        for title, dependency in dependencies.items():
            with self.subTest(dependency=dependency):
                self.assertIn(f"{dependency} (unmet)", rendered)
                self.assertIn(
                    f"External prerequisite requires manual satisfaction: {dependency}",
                    rendered,
                )
                self.assertNotIn(title, runnable)
        self.assertNotIn("base (satisfied)", rendered)

    def test_whole_local_markdown_link_normalizes_to_completed_slug(self) -> None:
        """A complete relative backlog link can use same-stem completion evidence."""
        self.write_item(
            "backlog/completed-backlog/features/base.md",
            title="Base",
            status="Completed",
            item_type="Feature",
        )
        dependency = "[Base](../completed-backlog/features/base.md)"
        self.write_item(
            "backlog/feature-backlog/local-link.md",
            title="Local Link",
            status="Ready",
            item_type="Feature",
            dependencies=f"- {dependency}",
        )

        rendered = self.generate()

        self.assertIn("<span>Runnable now</span><strong>1</strong>", rendered)
        self.assertIn("base (satisfied)", rendered)
        runnable = rendered[rendered.index("Runnable Work"):rendered.index("Blocked Work")]
        self.assertIn("Local Link", runnable)
        self.assertNotIn(dependency, rendered)

    def test_local_markdown_links_with_query_or_fragment_remain_manual(self) -> None:
        """Qualified local links remain complete manual prerequisites despite matching stems."""
        self.write_item(
            "backlog/completed-backlog/features/base.md",
            title="Base",
            status="Completed",
            item_type="Feature",
        )
        dependencies = {
            "Query Link": "[Base](../completed-backlog/features/base.md?view=full)",
            "Fragment Link": "[Base](../completed-backlog/features/base.md#approval)",
            "Empty Query Link": "[Base](../completed-backlog/features/base.md?)",
            "Empty Fragment Link": "[Base](../completed-backlog/features/base.md#)",
        }
        for title, dependency in dependencies.items():
            self.write_item(
                f"backlog/feature-backlog/{title.lower().replace(' ', '-')}.md",
                title=title,
                status="Ready",
                item_type="Feature",
                dependencies=f"- {dependency}",
            )

        rendered = self.generate()

        self.assertIn("<span>Runnable now</span><strong>0</strong>", rendered)
        runnable = rendered[rendered.index("Runnable Work"):rendered.index("Blocked Work")]
        for title, dependency in dependencies.items():
            with self.subTest(dependency=dependency):
                self.assertIn(f"{dependency} (unmet)", rendered)
                self.assertIn(
                    f"External prerequisite requires manual satisfaction: {dependency}",
                    rendered,
                )
                self.assertNotIn(title, runnable)
        self.assertNotIn("base (satisfied)", rendered)

    def test_legacy_file_item_uses_filename_stem_as_work_item_id(self) -> None:
        """Existing records remain discoverable without a migration-only field edit."""
        relative = "backlog/feature-backlog/legacy-item.md"
        self.write_item(
            relative,
            title="Legacy Item",
            status="Ready",
            item_type="Feature",
        )
        path = self.root / relative
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                "Work Item ID: legacy-item\n\n",
                "",
            ),
            encoding="utf-8",
        )

        rendered = self.generate()

        self.assertIn(
            "<strong>Work Item ID:</strong> <code>legacy-item</code>",
            rendered,
        )
        self.assertNotIn("Work Item ID does not match", rendered)

    def test_archive_move_preserves_work_item_id_and_reports_current_location(self) -> None:
        """The file identity is stable while its diagnostic path changes."""
        relative = "backlog/completed-backlog/features/stable-item.md"
        self.write_item(
            relative,
            title="Stable Item",
            status="Completed",
            item_type="Feature",
        )

        rendered = self.generate()

        self.assertIn(
            "<strong>Work Item ID:</strong> <code>stable-item</code>",
            rendered,
        )
        self.assertIn(
            "<strong>Source:</strong> <code>"
            "backlog/completed-backlog/features/stable-item.md</code>",
            rendered,
        )

    def test_duplicate_work_item_id_across_active_and_archive_is_reported(self) -> None:
        """File-provider identity is unique across active and terminal storage."""
        self.write_item(
            "backlog/feature-backlog/duplicate.md",
            title="Active Duplicate",
            status="Ready",
            item_type="Feature",
        )
        self.write_item(
            "backlog/completed-backlog/features/duplicate.md",
            title="Archived Duplicate",
            status="Completed",
            item_type="Feature",
        )

        rendered = self.generate()

        self.assertIn("Duplicate Work Item ID duplicate:", rendered)
        self.assertIn("backlog/feature-backlog/duplicate.md", rendered)
        self.assertIn("backlog/completed-backlog/features/duplicate.md", rendered)

    def test_lifecycle_and_metadata_anomalies_are_visible(self) -> None:
        """Invalid states and archive or dependency drift remain visible without source mutation."""
        self.write_item("backlog/completed-backlog/features/done.md", title="Done", status="Completed", item_type="Feature")
        self.write_item(
            "backlog/feature-backlog/proposal.md",
            title="Proposal",
            status="Proposed",
            item_type="Feature",
        )
        self.write_item(
            "backlog/feature-backlog/invalid-dependency.md",
            title="Invalid Dependency",
            status="Ready",
            item_type="Feature",
            dependencies="- bad_slug",
        )
        self.write_item(
            "backlog/feature-backlog/stale.md",
            title="Stale",
            status="Blocked",
            item_type="Feature",
            dependencies="- done",
        )
        self.write_item("backlog/feature-backlog/closed.md", title="Closed", status="Completed", item_type="Feature")
        self.write_item(
            "backlog/feature-backlog/depends-on-active-completed.md",
            title="Depends On Active Completed",
            status="Ready",
            item_type="Feature",
            dependencies="- closed",
        )
        self.write_item("backlog/completed-backlog/analyses/wrong.md", title="Wrong", status="Ready", item_type="Analysis")
        self.write_item("backlog/failed-backlog/features/wrong-failure.md", title="Wrong Failure", status="Ready", item_type="Feature")
        missing = self.root / "backlog/analysis-backlog/missing.md"
        missing.parent.mkdir(parents=True)
        missing.write_text("# Missing\n\nStatus: Ready\n\nType: Analysis\n", encoding="utf-8")
        unreadable = self.root / "backlog/defect-backlog/unreadable.md"
        unreadable.parent.mkdir(parents=True)
        unreadable.write_bytes(b"\xff\xfe")

        rendered = self.generate()

        self.assertIn("Migration anomaly: Status Proposed is not an operational state.", rendered)
        self.assertIn('<th scope="row">Proposed</th><td>1</td>', rendered)
        self.assertIn('<span class="badge badge-status">Proposed</span>', rendered)
        self.assertIn(
            "Status: Proposed is treated as migration debt and never as an operational bucket.",
            rendered,
        )
        self.assertNotIn("Status: Proposed appears only here", rendered)
        self.assertIn("Invalid dependency identifier: bad_slug.", rendered)
        self.assertNotIn(
            "Stale blocked status: all declared dependencies are satisfied.",
            rendered,
        )
        self.assertIn("Completed item remains in an active folder.", rendered)
        self.assertIn("Unmet dependency: closed is not in the completed archive.", rendered)
        self.assertIn("Completed archive contains an item not declared Completed.", rendered)
        self.assertIn("Failed archive contains an item without Failed or Abandoned status.", rendered)
        self.assertIn("Missing required fields: Summary, Context, Requirements, Acceptance Criteria, Dependencies, Verification.", rendered)
        self.assertIn("Unreadable item: UnicodeDecodeError", rendered)
        self.assertIn("<span>Runnable now</span><strong>0</strong>", rendered)

    def test_non_dependency_blocker_is_not_reported_as_stale(self) -> None:
        """Blocked may describe a cause independent of declared dependencies."""

        self.write_item(
            "backlog/defect-backlog/provider-outage.md",
            title="Provider Outage",
            status="Blocked",
            item_type="Defect",
            dependencies="None",
            extra="""## Blocker

Cause: Provider API is unavailable.
Owner: Provider operator.
Unblock Condition: Provider health check succeeds.
Coordinator Action: Recheck the provider health endpoint.
""",
        )

        rendered = self.generate()

        self.assertIn("Provider Outage", rendered)
        self.assertNotIn("Stale blocked status", rendered)

    def test_missing_context_is_anomalous_and_not_runnable(self) -> None:
        """An otherwise complete Ready item without Context cannot be dispatched."""
        self.write_item(
            "backlog/feature-backlog/no-context.md",
            title="No Context",
            status="Ready",
            item_type="Feature",
            context="",
        )

        rendered = self.generate()

        self.assertIn("Missing required fields: Context.", rendered)
        self.assertIn("<span>Runnable now</span><strong>0</strong>", rendered)
        runnable = rendered[rendered.index("Runnable Work"):rendered.index("Blocked Work")]
        self.assertNotIn("No Context", runnable)

    def test_active_ready_non_dispatchable_types_are_anomalies_not_runnable(self) -> None:
        """Holding and invalid Types remain visible but cannot become runnable work."""
        self.write_item(
            "backlog/feature-backlog/holding-ready.md",
            title="Holding Ready",
            status="Ready",
            item_type="Holding",
        )
        self.write_item(
            "backlog/feature-backlog/epic-ready.md",
            title="Epic Ready",
            status="Ready",
            item_type="Epic",
        )

        rendered = self.generate()

        self.assertIn("<span>Active typed items</span><strong>2</strong>", rendered)
        self.assertIn("<span>Runnable now</span><strong>0</strong>", rendered)
        self.assertIn(
            "Folder and Type mismatch: feature-backlog expects Feature, item declares Holding.",
            rendered,
        )
        self.assertIn("Invalid Type value: Epic.", rendered)
        runnable = rendered[rendered.index("Runnable Work"):rendered.index("Blocked Work")]
        blocked_start = rendered.index("Blocked Work")
        blocked = rendered[blocked_start:rendered.index("<h2>Holding</h2>", blocked_start)]
        active = rendered[rendered.index("Active Typed Work"):rendered.index("Completed Archive")]
        self.assertNotIn("Holding Ready", runnable)
        self.assertNotIn("Epic Ready", runnable)
        self.assertNotIn("Holding Ready", blocked)
        self.assertNotIn("Epic Ready", blocked)
        self.assertIn("Holding Ready", active)
        self.assertIn("Epic Ready", active)

    def test_user_action_required_rejects_non_dispatchable_underlying_type(self) -> None:
        """User-action work requires a Type that maps to a typed active destination."""
        user_sections = """## User Action Required

Decision required.

## Question for the User

Should this proceed?

## Why User Input Is Required

The user owns the decision.

## Resolution

Pending.

## Unattended Work Boundary

Do not proceed.
"""
        self.write_item(
            "backlog/user-action-required/invalid-destination.md",
            title="Invalid Destination",
            status="User Action Required",
            item_type="Holding",
            extra=user_sections,
        )

        rendered = self.generate()

        self.assertIn(
            "User Action Required item has no dispatchable underlying Type: Holding.",
            rendered,
        )
        self.assertIn("<span>Needs your input</span><strong>1</strong>", rendered)
        self.assertIn("backlog/user-action-required/invalid-destination.md", rendered)

    def test_user_action_required_section_is_mandatory(self) -> None:
        """User-action work reports a missing queue-owning section as an anomaly."""
        user_sections = """## Question for the User

Should this proceed?

## Why User Input Is Required

The user owns the decision.

## Resolution

Pending.

## Unattended Work Boundary

Do not proceed.
"""
        self.write_item(
            "backlog/user-action-required/missing-owner-section.md",
            title="Missing Owner Section",
            status="User Action Required",
            item_type="Analysis",
            extra=user_sections,
        )

        rendered = self.generate()

        self.assertIn("Missing user-action fields: User Action Required.", rendered)
        self.assertIn("<span>Needs your input</span><strong>1</strong>", rendered)

    def test_unreadable_series_index_is_ignored_and_reported(self) -> None:
        """An invalid UTF-8 series index cannot abort or become a counted work item."""
        series = self.root / "backlog/feature-backlog/invalid-series"
        series.mkdir(parents=True)
        (series / "index.md").write_bytes(b"\xff\xfe")
        self.write_item(
            "backlog/feature-backlog/invalid-series/child.md",
            title="Child",
            status="Ready",
            item_type="Feature",
        )

        rendered = self.generate()

        self.assertIn("<span>Active typed items</span><strong>1</strong>", rendered)
        self.assertIn("<span>Validation findings</span><strong>1</strong>", rendered)
        self.assertIn("Unreadable series index: UnicodeDecodeError", rendered)
        self.assertIn("backlog/feature-backlog/invalid-series/index.md", rendered)
        self.assertNotIn("invalid-series/index.md</code></p></article>", rendered)

    def test_invalid_values_and_untyped_archive_placement_are_findings(self) -> None:
        """Unknown metadata and malformed archive groups remain visible as invalid evidence."""
        self.write_item(
            "backlog/feature-backlog/unknown.md",
            title="Unknown",
            status="Queued",
            item_type="Epic",
        )
        self.write_item(
            "backlog/completed-backlog/root-item.md",
            title="Root Archive Item",
            status="Completed",
            item_type="Feature",
        )
        self.write_item(
            "backlog/completed-backlog/epics/unknown-group.md",
            title="Unknown Archive Group",
            status="Completed",
            item_type="Feature",
        )

        rendered = self.generate()

        self.assertIn("Invalid Type value: Epic.", rendered)
        self.assertIn("Invalid Status value: Queued.", rendered)
        self.assertEqual(
            2,
            rendered.count("Archive placement is not a recognized typed archive folder."),
        )

    def test_output_cannot_overwrite_scanned_source_or_guidance(self) -> None:
        """Output validation protects work items and ignored coordination files before writing."""
        item = self.root / "backlog/feature-backlog/protected.md"
        self.write_item(
            "backlog/feature-backlog/protected.md",
            title="Protected",
            status="Ready",
            item_type="Feature",
        )
        readme = self.root / "backlog/user-action-required/README.md"
        readme.parent.mkdir(parents=True)
        readme.write_text("# Protected guidance\n", encoding="utf-8")
        item_before = item.read_bytes()
        readme_before = readme.read_bytes()
        alias = self.root / "report-alias.html"
        alias.symlink_to(item)

        for protected in (item, readme, alias):
            with self.subTest(protected=protected):
                with self.assertRaisesRegex(
                    ValueError, "Output path would overwrite a backlog source"
                ):
                    REPORT.generate_report(self.root, protected)

        self.assertEqual(item_before, item.read_bytes())
        self.assertEqual(readme_before, readme.read_bytes())

    def test_default_output_cannot_resolve_inside_future_ideas(self) -> None:
        """Direct and directory-alias outputs cannot overwrite an unscanned Future Idea."""
        idea = self.root / "backlog/future-ideas/protected.md"
        idea.parent.mkdir(parents=True)
        idea.write_bytes(b"\xff\xfeoriginal future idea bytes")
        before = idea.read_bytes()
        alias_root = self.root / "future-ideas-alias"
        alias_root.symlink_to(idea.parent, target_is_directory=True)

        for protected in (idea, alias_root / idea.name):
            with self.subTest(protected=protected):
                with self.assertRaisesRegex(
                    ValueError,
                    "Output path cannot resolve inside backlog/future-ideas",
                ):
                    REPORT.generate_report(self.root, protected)

        self.assertEqual(before, idea.read_bytes())

    def test_lexical_output_inside_future_ideas_cannot_follow_symlink_outward(
        self,
    ) -> None:
        """A Future Ideas path pointing outward cannot overwrite external bytes."""
        ideas_root = self.root / "backlog/future-ideas"
        ideas_root.mkdir(parents=True)
        external = self.root / "external-report-target.html"
        external.write_bytes(b"external target bytes")
        outward = ideas_root / "outward.html"
        outward.symlink_to(external)
        before = external.read_bytes()

        with self.assertRaisesRegex(
            ValueError,
            "Output path cannot be located inside backlog/future-ideas",
        ):
            REPORT.generate_report(self.root, outward)

        self.assertEqual(before, external.read_bytes())

    def test_hard_link_output_alias_cannot_replace_a_future_idea(self) -> None:
        """A hard-link alias is rejected while preserving the source idea inode bytes."""
        idea = self.root / "backlog/future-ideas/hard-linked.md"
        idea.parent.mkdir(parents=True)
        idea.write_bytes(b"original future idea bytes")
        self.output.parent.mkdir(parents=True)
        self.output.hardlink_to(idea)
        before = idea.read_bytes()

        with self.assertRaisesRegex(
            ValueError, "Output path would overwrite a backlog source"
        ):
            REPORT.generate_report(self.root, self.output)

        self.assertEqual(before, idea.read_bytes())
        self.assertEqual(before, self.output.read_bytes())

    def test_atomic_output_write_failure_preserves_prior_report_and_cleans_temp(
        self,
    ) -> None:
        """A still-open descriptor write failure preserves source and prior report."""
        self.write_item(
            "backlog/feature-backlog/ready.md",
            title="Ready",
            status="Ready",
            item_type="Feature",
        )
        idea = self.root / "backlog/future-ideas/preserved-on-write.md"
        self.write_idea(
            "backlog/future-ideas/preserved-on-write.md",
            title="Preserved On Write",
        )
        idea_before = idea.read_bytes()
        self.output.parent.mkdir(parents=True)
        self.output.write_bytes(b"prior report bytes")

        class FailingWriter:
            """Own and close the mkstemp descriptor while injecting a write failure."""

            def __init__(self, descriptor: int) -> None:
                self.descriptor = descriptor

            def __enter__(self) -> "FailingWriter":
                return self

            def __exit__(
                self,
                exc_type: type[BaseException] | None,
                exc_value: BaseException | None,
                traceback: object,
            ) -> None:
                os.close(self.descriptor)

            def write(self, content: bytes) -> int:
                raise OSError("injected output write failure")

        def failing_fdopen(
            descriptor: int, mode: str, **kwargs: object
        ) -> FailingWriter:
            self.assertEqual("wb", mode)
            self.assertEqual({}, kwargs)
            return FailingWriter(descriptor)

        with mock.patch.object(REPORT.os, "fdopen", side_effect=failing_fdopen):
            with self.assertRaisesRegex(OSError, "injected output write failure"):
                REPORT.generate_report(self.root, self.output)

        self.assertEqual(idea_before, idea.read_bytes())
        self.assertEqual(b"prior report bytes", self.output.read_bytes())
        self.assertEqual([], list(self.output.parent.glob(".*.tmp")))

    def test_atomic_output_never_reopens_the_mkstemp_pathname(self) -> None:
        """Report bytes flow through mkstemp's descriptor without pathname reopening."""
        self.write_item(
            "backlog/feature-backlog/ready.md",
            title="Ready",
            status="Ready",
            item_type="Feature",
        )
        self.output.parent.mkdir(parents=True)
        self.output.write_bytes(b"prior report bytes")
        original_open = Path.open
        original_write_text = Path.write_text
        original_mkstemp = REPORT.tempfile.mkstemp
        created_temporaries: list[Path] = []

        def record_mkstemp(*args: object, **kwargs: object) -> tuple[int, str]:
            descriptor, temporary_name = original_mkstemp(*args, **kwargs)
            created_temporaries.append(Path(temporary_name))
            return descriptor, temporary_name

        def reject_temp_open(
            path: Path, *args: object, **kwargs: object
        ):
            if path in created_temporaries:
                raise AssertionError("temporary pathname was reopened")
            return original_open(path, *args, **kwargs)

        def reject_temp_write_text(
            path: Path, *args: object, **kwargs: object
        ) -> int:
            if path in created_temporaries:
                raise AssertionError("temporary pathname was reopened")
            return original_write_text(path, *args, **kwargs)

        with (
            mock.patch.object(
                REPORT.tempfile, "mkstemp", side_effect=record_mkstemp
            ),
            mock.patch.object(Path, "open", reject_temp_open),
            mock.patch.object(Path, "write_text", reject_temp_write_text),
        ):
            REPORT.generate_report(self.root, self.output)

        self.assertIn(b"<!doctype html>", self.output.read_bytes())
        self.assertEqual([], list(self.output.parent.glob(".*.tmp")))

    def test_atomic_output_replace_failure_preserves_prior_report_and_cleans_temp(
        self,
    ) -> None:
        """An atomic replace failure leaves prior output and source bytes untouched."""
        self.write_item(
            "backlog/feature-backlog/ready.md",
            title="Ready",
            status="Ready",
            item_type="Feature",
        )
        idea = self.root / "backlog/future-ideas/preserved.md"
        self.write_idea(
            "backlog/future-ideas/preserved.md",
            title="Preserved",
        )
        idea_before = idea.read_bytes()
        self.output.parent.mkdir(parents=True)
        self.output.write_bytes(b"prior report bytes")

        with mock.patch.object(
            REPORT.os,
            "replace",
            side_effect=OSError("injected output replace failure"),
        ):
            with self.assertRaisesRegex(OSError, "injected output replace failure"):
                REPORT.generate_report(self.root, self.output)

        self.assertEqual(idea_before, idea.read_bytes())
        self.assertEqual(b"prior report bytes", self.output.read_bytes())
        self.assertEqual([], list(self.output.parent.glob(".*.tmp")))

    def test_missing_optional_folders_and_repeat_generation_are_deterministic(self) -> None:
        """A minimal backlog generates equivalent ordered content at a controlled snapshot time."""
        self.write_item(
            "backlog/feature-backlog/only.md",
            title="Only",
            status="Ready",
            item_type="Feature",
            dependencies="- None.",
        )

        first = self.generate()
        second_path = self.root / "second.html"
        REPORT.generate_report(self.root, second_path, "2026-07-19T06:00:00+00:00")
        second = second_path.read_text(encoding="utf-8")

        self.assertEqual(first, second)
        self.assertIn("backlog/feature-backlog/only.md", first)
        self.assertIn("<span>Runnable now</span><strong>1</strong>", first)
        self.assertNotIn("Invalid dependency identifier: None", first)
        self.assertIn("@media(prefers-color-scheme:dark)", first)
        self.assertIn("@media(max-width:420px)", first)
        self.assertIn('name="viewport"', first)
        self.assertIn("Workspace Claim Snapshot", first)
        self.assertIn("source commit unavailable", first)

    def test_long_snapshot_metadata_has_narrow_viewport_wrap_contract(self) -> None:
        """Long source and claim metadata cannot widen a 320-pixel viewport."""
        self.write_item(
            "backlog/feature-backlog/ready.md",
            title="Ready",
            status="Ready",
            item_type="Feature",
        )
        long_commit = "a" * 80
        long_claim_value = "claim-" + "b" * 80
        claim = {
            "claim_id": long_claim_value,
            "agent": "Fixture Agent",
            "branch": long_claim_value,
            "worktree": f"/fixture/{long_claim_value}",
            "heartbeat": "2026-07-19T05:59:00Z",
        }

        with (
            mock.patch.object(REPORT, "_source_commit", return_value=long_commit),
            mock.patch.object(
                REPORT,
                "_claim_snapshot",
                return_value=("2026-07-19T06:00:00+00:00", (claim,), "available"),
            ),
        ):
            rendered = self.generate()

        self.assertIn(f"source commit {long_commit}", rendered)
        self.assertIn(long_claim_value, rendered)
        self.assertIn(
            ".meta,.detail,.findings li,.snapshot{overflow-wrap:anywhere}",
            rendered,
        )
        self.assertIn("@media(max-width:420px)", rendered)

    def test_long_dependency_and_finding_have_narrow_viewport_wrap_contract(
        self,
    ) -> None:
        """Long prerequisite text cannot force report grids wider than the viewport."""
        dependency = "https://example.invalid/" + "unbroken-dependency-segment-" * 12
        self.write_item(
            "backlog/feature-backlog/long-dependency.md",
            title="Long Dependency",
            status="Ready",
            item_type="Feature",
            dependencies=f"- {dependency}",
        )

        rendered = self.generate()

        self.assertGreaterEqual(rendered.count(dependency), 2)
        self.assertIn(".metric,.item,.panel{min-width:0", rendered)
        self.assertIn(
            ".meta,.detail,.findings li,.snapshot{overflow-wrap:anywhere}",
            rendered,
        )
        self.assertIn('<meta name="viewport" content="width=device-width, initial-scale=1">', rendered)

    def test_git_source_and_claim_snapshot_do_not_change_eligibility(self) -> None:
        """Git and claim metadata form a separate snapshot and never remove Ready work."""
        self.write_item("backlog/feature-backlog/ready.md", title="Ready", status="Ready", item_type="Feature")
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        subprocess.run(["git", "-C", str(self.root), "add", "backlog"], check=True)
        subprocess.run(
            [
                "git",
                "-C",
                str(self.root),
                "-c",
                "user.name=Report Test",
                "-c",
                "user.email=report-test@example.invalid",
                "commit",
                "-qm",
                "fixture",
            ],
            check=True,
        )
        commit = subprocess.run(
            ["git", "-C", str(self.root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        (self.root / ".git/agent-claims.json").write_text(
            '{"claims":[{"claim_id":"fixture-claim","agent":"Fixture Agent","branch":"codex/fixture","worktree":"/fixture/worktree","heartbeat":"2026-07-19T05:59:00Z"}]}',
            encoding="utf-8",
        )

        rendered = self.generate()

        self.assertIn(f"source commit {commit}", rendered)
        self.assertIn("fixture-claim", rendered)
        self.assertIn("Fixture Agent", rendered)
        self.assertIn("codex/fixture", rendered)
        self.assertIn("/fixture/worktree", rendered)
        self.assertIn("Claims and worktrees are workspace coordination evidence", rendered)
        self.assertIn("<span>Runnable now</span><strong>1</strong>", rendered)

    def test_claim_snapshot_distinguishes_empty_from_unavailable_registry(self) -> None:
        """Missing, unreadable, and invalid registries never masquerade as confirmed empty."""
        self.write_item(
            "backlog/feature-backlog/ready.md",
            title="Ready",
            status="Ready",
            item_type="Feature",
        )
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        registry = self.root / ".git/agent-claims.json"

        missing = self.generate()
        self.assertIn("claim registry is missing", missing)
        self.assertNotIn("No active claims were present", missing)

        registry.write_text("not json", encoding="utf-8")
        invalid = self.generate()
        self.assertIn("claim registry contains invalid JSON", invalid)
        self.assertNotIn("No active claims were present", invalid)

        registry.write_text('{"claims":{}}', encoding="utf-8")
        invalid_shape = self.generate()
        self.assertIn("claim registry has an invalid claims field", invalid_shape)
        self.assertNotIn("No active claims were present", invalid_shape)

        registry.write_bytes(b"\xff\xfe")
        unreadable = self.generate()
        self.assertIn("claim registry is unreadable (UnicodeDecodeError)", unreadable)
        self.assertNotIn("No active claims were present", unreadable)

        registry.write_text('{"claims":[]}', encoding="utf-8")
        empty = self.generate()
        self.assertIn("No active claims were present", empty)
        self.assertNotIn("claim registry is missing", empty)

    def test_cli_writes_explicit_output_and_missing_backlog_fails(self) -> None:
        """The CLI owns explicit output creation and reports an absent backlog as input failure."""
        self.write_item("backlog/defect-backlog/fix.md", title="Fix", status="Ready", item_type="Defect")
        result = REPORT.main(
            [
                "--repository-root",
                str(self.root),
                "--output",
                str(self.output),
                "--generated-at",
                "2026-07-19T06:00:00+00:00",
            ]
        )
        self.assertEqual(0, result)
        self.assertTrue(self.output.is_file())
        self.write_idea("backlog/future-ideas/cli-opt-in.md", title="CLI Opt In")
        idea_output = self.root / "out" / "ideas.html"
        idea_result = REPORT.main(
            [
                "--repository-root",
                str(self.root),
                "--output",
                str(idea_output),
                "--include-future-ideas",
            ]
        )
        self.assertEqual(0, idea_result)
        self.assertIn("CLI Opt In", idea_output.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as empty:
            with self.assertRaisesRegex(ValueError, "Backlog directory does not exist"):
                REPORT.generate_report(Path(empty), Path(empty) / "report.html")


if __name__ == "__main__":
    unittest.main()
