# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Modified with AI assistance.
# Summary: Verifies feature-branch completion states, provider terminology, and Git merge evidence.

from __future__ import annotations

import subprocess
import tempfile
import unittest
from dataclasses import dataclass
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SKILL_PATH = (
    REPOSITORY_ROOT / "skills" / "complete-work-item-feature-branch" / "SKILL.md"
)


def load_host_state_table() -> dict[str, str]:
    """Return the scenario-to-disposition contract from the skill's decision table."""
    text = SKILL_PATH.read_text(encoding="utf-8")
    section = text.split("## Host State Decision Table", 1)[1].split("\n## ", 1)[0]
    rows: dict[str, str] = {}
    for line in section.splitlines():
        if not line.startswith("|") or line.startswith("| ---"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if cells[0] == "Scenario":
            continue
        rows[cells[0]] = cells[2]
    return rows


def run_git(
    repository: Path,
    *arguments: str,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    """Run one deterministic Git command in a disposable repository."""
    return subprocess.run(
        ["git", *arguments],
        cwd=repository,
        check=check,
        capture_output=True,
        text=True,
    )


@dataclass(frozen=True)
class MockHostState:
    """Provider-accurate evidence supplied by one mocked code host."""

    code_host: str = "github"
    delivery_term: str = "pull request"
    publication_state: str = "ready"
    checks: str = "passed"
    approval: str = "approved"
    dependencies: str = "merged"
    merge_state: str = "open"
    authority: bool = True
    base_contains_published_commit: bool = False
    draft_authorized: bool = False
    correction_required: bool = False
    correction_published: bool = False


def evaluate_mock_host(state: MockHostState) -> str:
    """Apply the skill's completion gate to deterministic mocked host evidence."""
    expected_term = {
        "github": "pull request",
        "gitlab": "merge request",
    }.get(state.code_host)
    if expected_term != state.delivery_term or not state.authority:
        return "BLOCKED"
    if state.publication_state not in {"ready", "draft"}:
        return "BLOCKED"
    if state.publication_state == "draft" and not state.draft_authorized:
        return "BLOCKED"
    if state.correction_required and not state.correction_published:
        return "BLOCKED"
    if state.checks not in {"pending", "passed", "failed"}:
        return "BLOCKED"
    if state.checks == "failed" or state.merge_state in {"closed", "superseded"}:
        return "BLOCKED"
    if state.publication_state == "draft" or state.correction_required:
        return "AWAITING_REVIEW"
    if state.merge_state == "merged" and not state.base_contains_published_commit:
        return "BLOCKED"
    if (
        state.merge_state == "merged"
        and state.checks == "passed"
        and state.approval == "approved"
        and state.dependencies == "merged"
        and state.base_contains_published_commit
    ):
        return "READY"
    return "AWAITING_REVIEW"


class CompleteWorkItemFeatureBranchTests(unittest.TestCase):
    def test_mocked_host_states_cover_review_merge_and_failure_boundaries(self) -> None:
        scenarios = {
            "Ready publication": MockHostState(),
            "Explicit draft": MockHostState(
                publication_state="draft",
                draft_authorized=True,
                merge_state="merged",
                base_contains_published_commit=True,
            ),
            "Review correction": MockHostState(
                correction_required=True,
                correction_published=True,
                merge_state="merged",
                base_contains_published_commit=True,
            ),
            "Checks pending": MockHostState(
                checks="pending",
                merge_state="merged",
                base_contains_published_commit=True,
            ),
            "Check failure": MockHostState(checks="failed"),
            "Approval pending": MockHostState(
                approval="pending",
                merge_state="merged",
                base_contains_published_commit=True,
            ),
            "Dependency pending": MockHostState(
                dependencies="pending",
                merge_state="merged",
                base_contains_published_commit=True,
            ),
            "Merge pending": MockHostState(
                merge_state="open",
                base_contains_published_commit=True,
            ),
            "Merge complete": MockHostState(
                merge_state="merged",
                base_contains_published_commit=True,
            ),
            "Merge evidence mismatch": MockHostState(
                merge_state="merged",
                base_contains_published_commit=False,
            ),
            "Closed unmerged": MockHostState(merge_state="closed"),
            "Superseded": MockHostState(merge_state="superseded"),
            "Missing authority": MockHostState(authority=False),
            "Terminology mismatch": MockHostState(
                code_host="gitlab",
                delivery_term="pull request",
            ),
        }
        expected = load_host_state_table()

        self.assertEqual(set(expected), set(scenarios))
        for name, state in scenarios.items():
            with self.subTest(name=name):
                self.assertEqual(expected[name], evaluate_mock_host(state))

        invalid_evidence = {
            "unauthorized draft": MockHostState(publication_state="draft"),
            "missing correction publication": MockHostState(
                correction_required=True,
            ),
        }
        for name, state in invalid_evidence.items():
            with self.subTest(name=name):
                self.assertEqual("BLOCKED", evaluate_mock_host(state))

    def test_provider_terminology_rejects_cross_shaped_evidence(self) -> None:
        skill_text = SKILL_PATH.read_text(encoding="utf-8")

        self.assertIn(
            "GitHub evidence is shaped as a merge request or GitLab evidence is shaped as a pull request",
            skill_text,
        )
        self.assertEqual("BLOCKED", load_host_state_table()["Terminology mismatch"])

    def test_git_graph_rejects_publication_and_accepts_merged_commit(self) -> None:
        skill_text = SKILL_PATH.read_text(encoding="utf-8")
        self.assertIn(
            "git merge-base --is-ancestor PUBLISHED_HEAD CONFIGURED_BASE",
            skill_text,
        )
        self.assertIn(
            "git merge-base --is-ancestor FINAL_MERGED_COMMIT CONFIGURED_BASE",
            skill_text,
        )

        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory)
            run_git(repository, "init", "--initial-branch=main")
            run_git(repository, "config", "user.name", "Verifier")
            run_git(repository, "config", "user.email", "verifier@example.invalid")
            (repository / "delivery.txt").write_text("base\n", encoding="utf-8")
            run_git(repository, "add", "delivery.txt")
            run_git(repository, "commit", "-m", "base")
            run_git(repository, "switch", "-c", "feature")
            (repository / "delivery.txt").write_text("feature\n", encoding="utf-8")
            run_git(repository, "commit", "-am", "feature")
            feature_commit = run_git(repository, "rev-parse", "HEAD").stdout.strip()

            publication_only = run_git(
                repository,
                "merge-base",
                "--is-ancestor",
                feature_commit,
                "main",
                check=False,
            )
            self.assertEqual(1, publication_only.returncode)

            run_git(repository, "switch", "main")
            run_git(repository, "merge", "--no-ff", "feature", "-m", "merge feature")
            final_merged_commit = run_git(repository, "rev-parse", "HEAD").stdout.strip()
            published_commit_merged = run_git(
                repository,
                "merge-base",
                "--is-ancestor",
                feature_commit,
                "main",
                check=False,
            )
            final_merge_observed = run_git(
                repository,
                "merge-base",
                "--is-ancestor",
                final_merged_commit,
                "main",
                check=False,
            )
            self.assertEqual(0, published_commit_merged.returncode)
            self.assertEqual(0, final_merge_observed.returncode)


if __name__ == "__main__":
    unittest.main()
