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
            dependencies="- [Base](../../../completed-backlog/features/base.md)",
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
        self.assertIn("Invalid dependency identifier: bad_slug.", rendered)
        self.assertIn("Stale blocked status: all declared dependencies are satisfied.", rendered)
        self.assertIn("Completed item remains in an active folder.", rendered)
        self.assertIn("Completed archive contains an item not declared Completed.", rendered)
        self.assertIn("Failed archive contains an item without Failed or Abandoned status.", rendered)
        self.assertIn("Missing required fields: Summary, Requirements, Acceptance Criteria, Dependencies, Verification.", rendered)
        self.assertIn("Unreadable item: UnicodeDecodeError", rendered)
        self.assertIn("<span>Runnable now</span><strong>0</strong>", rendered)

    def test_missing_optional_folders_and_repeat_generation_are_deterministic(self) -> None:
        """A minimal backlog generates equivalent ordered content at a controlled snapshot time."""
        self.write_item("backlog/feature-backlog/only.md", title="Only", status="Ready", item_type="Feature")

        first = self.generate()
        second_path = self.root / "second.html"
        REPORT.generate_report(self.root, second_path, "2026-07-19T06:00:00+00:00")
        second = second_path.read_text(encoding="utf-8")

        self.assertEqual(first, second)
        self.assertIn("backlog/feature-backlog/only.md", first)
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
