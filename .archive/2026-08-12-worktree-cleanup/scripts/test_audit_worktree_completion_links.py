# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies worktree inventory parsing and archived work-item correlation through ripgrep.

from __future__ import annotations

import importlib.util
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).with_name("audit-worktree-completion-links.py")
SPEC = importlib.util.spec_from_file_location("audit_worktree_completion_links", SCRIPT_PATH)
assert SPEC and SPEC.loader
AUDIT = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = AUDIT
SPEC.loader.exec_module(AUDIT)


class WorktreeCompletionLinkAuditTests(unittest.TestCase):
    """Exercise the read-only worktree-to-archive correlation contract."""

    def test_parse_worktrees_preserves_branch_detached_and_prunable_records(self) -> None:
        payload = "\n".join(
            (
                "worktree /repo",
                "HEAD aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "branch refs/heads/main",
                "",
                "worktree /repo/.worktrees/feature",
                "HEAD bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
                "branch refs/heads/codex/feature-work",
                "",
                "worktree /tmp/old",
                "HEAD cccccccccccccccccccccccccccccccccccccccc",
                "detached",
                "prunable gitdir file points to non-existent location",
                "",
            )
        )

        worktrees = AUDIT.parse_worktree_porcelain(payload)

        self.assertEqual(3, len(worktrees))
        self.assertEqual("codex/feature-work", worktrees[1].branch)
        self.assertTrue(worktrees[2].detached)
        self.assertIn("non-existent", worktrees[2].prunable)

    @unittest.skipUnless(shutil.which("rg"), "ripgrep is required")
    def test_search_archives_uses_worktree_signals_to_find_completed_item(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            archive = repo / "backlog" / "completed-backlog"
            item = archive / "features" / "feature-work.md"
            item.parent.mkdir(parents=True)
            item.write_text(
                "# Feature Work\n\nStatus: Completed\n\n"
                "Work Item ID: feature-work\n\n"
                "Branch: codex/feature-work\n",
                encoding="utf-8",
            )
            worktree = AUDIT.Worktree(
                path=repo / ".worktrees" / "feature-work",
                head="b" * 40,
                branch="codex/feature-work",
            )

            hits = AUDIT.search_archives(repo, (archive,), (worktree,), "rg")

        self.assertEqual(2, len(hits))
        self.assertEqual(
            {Path("backlog/completed-backlog/features/feature-work.md")},
            {hit.path for hit in hits},
        )
        self.assertIn("branch", {kind for hit in hits for kind in hit.signal_kinds})

    def test_correlate_prefers_exact_branch_over_normalized_slug(self) -> None:
        worktree = AUDIT.Worktree(
            path=Path("/repo/.worktrees/feature-work-correction-1"),
            head="d" * 40,
            branch="codex/feature-work-correction-1",
        )
        hits = (
            AUDIT.SearchHit(
                path=Path("backlog/completed-backlog/features/feature-work.md"),
                line_number=10,
                line="Summary for feature work.",
                signal_kinds=("normalized-slug",),
            ),
            AUDIT.SearchHit(
                path=Path("backlog/completed-backlog/features/exact.md"),
                line_number=20,
                line="Branch: codex/feature-work-correction-1",
                signal_kinds=("branch",),
            ),
        )

        result = AUDIT.correlate_worktree(worktree, hits)

        self.assertEqual("strong", result.confidence)
        self.assertEqual(Path("backlog/completed-backlog/features/exact.md"), result.matches[0].path)

    def test_codex_managed_worktree_omits_generic_repository_basename_signal(self) -> None:
        worktree = AUDIT.Worktree(
            path=Path("/Users/example/.codex/worktrees/69b1/dev-methodology"),
            head="f" * 40,
            detached=True,
        )

        signals = AUDIT.signals_for(worktree)

        self.assertNotIn("basename", {signal.kind for signal in signals})
        self.assertNotIn("normalized-slug", {signal.kind for signal in signals})
        self.assertNotIn("dev-methodology", {signal.value for signal in signals})

    def test_normalized_slug_removes_short_task_token_and_execution_suffix(self) -> None:
        worktree = AUDIT.Worktree(
            path=Path("/repo/.worktrees/019f77f4-backlog-resumption-correction-1"),
            head="1" * 40,
            branch="codex/019f77f4-backlog-resumption-correction-1",
        )

        self.assertEqual("backlog-resumption", AUDIT.normalized_slug(worktree))

    def test_render_text_keeps_unmatched_worktree_visible(self) -> None:
        worktree = AUDIT.Worktree(
            path=Path("/repo/.worktrees/no-link"),
            head="e" * 40,
            branch="codex/no-link",
        )
        result = AUDIT.Correlation(worktree=worktree, confidence="none", matches=())

        rendered = AUDIT.render_text(Path("/repo"), (result,))

        self.assertIn("total=1", rendered)
        self.assertIn("none=1", rendered)
        self.assertIn("codex/no-link", rendered)
        self.assertIn("no archived work-item match", rendered)

if __name__ == "__main__":
    unittest.main()
