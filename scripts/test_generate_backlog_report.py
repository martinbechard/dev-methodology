# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies backlog report inventory, reconciliation, ordering, and offline HTML output.
# Governing backlog item: backlog/feature-backlog/add-styled-backlog-report-with-user-input.md

"""Focused tests for the styled backlog report generator."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).with_name("generate-backlog-report.py")
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
        extra: str = "",
    ) -> None:
        """Write one complete backlog item with optional queue-specific sections."""
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            f"""# {title}

Status: {status}

Type: {item_type}

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

{extra}""",
            encoding="utf-8",
        )

    def generate(self, timestamp: str = "2026-07-19T06:00:00+00:00") -> str:
        """Generate and return one report at a controlled snapshot time."""
        REPORT.generate_report(self.root, self.output, timestamp)
        return self.output.read_text(encoding="utf-8")

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
        dependency = (
            "[Base](../completed-backlog/features/base.md?view=full#approval)"
        )
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
        self.assertIn("Stale blocked status: all declared dependencies are satisfied.", rendered)
        self.assertIn("Completed item remains in an active folder.", rendered)
        self.assertIn("Unmet dependency: closed is not in the completed archive.", rendered)
        self.assertIn("Completed archive contains an item not declared Completed.", rendered)
        self.assertIn("Failed archive contains an item without Failed or Abandoned status.", rendered)
        self.assertIn("Missing required fields: Summary, Context, Requirements, Acceptance Criteria, Dependencies, Verification.", rendered)
        self.assertIn("Unreadable item: UnicodeDecodeError", rendered)
        self.assertIn("<span>Runnable now</span><strong>0</strong>", rendered)

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
        with tempfile.TemporaryDirectory() as empty:
            with self.assertRaisesRegex(ValueError, "Backlog directory does not exist"):
                REPORT.generate_report(Path(empty), Path(empty) / "report.html")


if __name__ == "__main__":
    unittest.main()
