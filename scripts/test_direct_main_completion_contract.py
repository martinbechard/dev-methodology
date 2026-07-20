# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Modified with AI assistance.
# Summary: Exercises direct-main completion evidence against disposable Git repositories.

from __future__ import annotations

import subprocess
import tempfile
import unittest
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CompletionEvidence:
    disposition: str
    observed_main_commit: str | None
    provider_lifecycle_update: dict[str, str] | None
    blocker: str | None


class DisposableRepository:
    def __init__(self) -> None:
        self._temporary_directory = tempfile.TemporaryDirectory()
        self.path = Path(self._temporary_directory.name)
        self.git("init", "--initial-branch=main")
        self.git("config", "user.name", "Direct Main Contract Test")
        self.git("config", "user.email", "direct-main-contract@example.invalid")

    def close(self) -> None:
        self._temporary_directory.cleanup()

    def git(
        self,
        *arguments: str,
        check: bool = True,
        input_text: str | None = None,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", *arguments],
            cwd=self.path,
            check=check,
            capture_output=True,
            text=True,
            input=input_text,
        )

    def commit_file(self, relative_path: str, content: str, message: str) -> str:
        path = self.path / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        self.git("add", relative_path)
        self.git("commit", "-m", message)
        return self.rev_parse("HEAD")

    def rev_parse(self, revision: str) -> str:
        return self.git("rev-parse", revision).stdout.strip()

    def patch_id(self, commit: str) -> str:
        patch = self.git(
            "show",
            "--pretty=format:",
            "--binary",
            commit,
        ).stdout
        result = self.git("patch-id", "--stable", input_text=patch)
        return result.stdout.split()[0]


def observe_direct_main_completion(
    repository: DisposableRepository,
    *,
    configured_main: str,
    source_commit: str,
    integration_commit: str,
    verification_passed: bool = True,
    publication_required: bool = False,
    publication_authorized: bool = True,
    claim_released: bool = True,
    allow_non_ancestral_mapping: bool = False,
) -> CompletionEvidence:
    current_branch = repository.git("branch", "--show-current").stdout.strip()
    if current_branch != configured_main:
        return CompletionEvidence("BLOCKED", None, None, "configured-main-not-checked-out")

    if repository.git("status", "--porcelain").stdout:
        return CompletionEvidence("BLOCKED", None, None, "main-worktree-not-clean")

    observed_main = repository.rev_parse(configured_main)
    integration_reachable = repository.git(
        "merge-base",
        "--is-ancestor",
        integration_commit,
        configured_main,
        check=False,
    ).returncode == 0
    if not integration_reachable:
        return CompletionEvidence("BLOCKED", observed_main, None, "integration-not-on-main")

    source_reachable = repository.git(
        "merge-base",
        "--is-ancestor",
        source_commit,
        configured_main,
        check=False,
    ).returncode == 0
    if not source_reachable:
        mapping_matches = (
            allow_non_ancestral_mapping
            and repository.patch_id(source_commit) == repository.patch_id(integration_commit)
        )
        if not mapping_matches:
            return CompletionEvidence(
                "BLOCKED",
                observed_main,
                None,
                "source-not-represented-on-main",
            )

    if not verification_passed:
        return CompletionEvidence("BLOCKED", observed_main, None, "verification-failed")
    if publication_required and not publication_authorized:
        return CompletionEvidence(
            "BLOCKED",
            observed_main,
            None,
            "publication-authority-missing",
        )
    if not claim_released:
        return CompletionEvidence("BLOCKED", observed_main, None, "integration-claim-live")

    provider_update = {
        "completion_disposition": "READY",
        "requested_lifecycle": "COMPLETED",
        "source_commit": source_commit,
        "integration_commit": integration_commit,
        "observed_main_commit": observed_main,
    }
    return CompletionEvidence("READY", observed_main, provider_update, None)


class DirectMainCompletionContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DisposableRepository()
        self.addCleanup(self.repository.close)
        self.base_commit = self.repository.commit_file("base.txt", "base\n", "Base")

    def test_direct_primary_commit_completes_after_main_observation(self) -> None:
        source_commit = self.repository.commit_file(
            "feature.txt",
            "delivered\n",
            "Direct main delivery",
        )

        result = observe_direct_main_completion(
            self.repository,
            configured_main="main",
            source_commit=source_commit,
            integration_commit=source_commit,
        )

        self.assertEqual("READY", result.disposition)
        self.assertEqual(source_commit, result.observed_main_commit)

    def test_unmerged_isolated_commit_cannot_complete_then_merge_can(self) -> None:
        self.repository.git("switch", "-c", "temporary-delivery")
        source_commit = self.repository.commit_file(
            "feature.txt",
            "isolated\n",
            "Isolated delivery",
        )
        self.repository.git("switch", "main")

        before_merge = observe_direct_main_completion(
            self.repository,
            configured_main="main",
            source_commit=source_commit,
            integration_commit=source_commit,
        )
        self.assertEqual("BLOCKED", before_merge.disposition)
        self.assertEqual("integration-not-on-main", before_merge.blocker)

        self.repository.git("merge", "--no-ff", "temporary-delivery", "-m", "Integrate")
        integration_commit = self.repository.rev_parse("HEAD")
        after_merge = observe_direct_main_completion(
            self.repository,
            configured_main="main",
            source_commit=source_commit,
            integration_commit=integration_commit,
        )
        self.assertEqual("READY", after_merge.disposition)

    def test_unrelated_main_advance_is_preserved_during_integration(self) -> None:
        self.repository.git("switch", "-c", "temporary-delivery")
        source_commit = self.repository.commit_file(
            "feature.txt",
            "candidate\n",
            "Candidate",
        )
        self.repository.git("switch", "main")
        unrelated_commit = self.repository.commit_file(
            "unrelated.txt",
            "preserve\n",
            "Unrelated main advance",
        )
        self.repository.git("merge", "--no-ff", "temporary-delivery", "-m", "Integrate")
        integration_commit = self.repository.rev_parse("HEAD")

        result = observe_direct_main_completion(
            self.repository,
            configured_main="main",
            source_commit=source_commit,
            integration_commit=integration_commit,
        )

        self.assertEqual("READY", result.disposition)
        self.assertEqual("preserve\n", (self.repository.path / "unrelated.txt").read_text())
        self.assertEqual(
            0,
            self.repository.git(
                "merge-base",
                "--is-ancestor",
                unrelated_commit,
                "main",
                check=False,
            ).returncode,
        )

    def test_conflict_requires_resolution_and_post_integration_verification(self) -> None:
        self.repository.commit_file("shared.txt", "base\n", "Shared base")
        self.repository.git("switch", "-c", "temporary-delivery")
        source_commit = self.repository.commit_file(
            "shared.txt",
            "candidate\n",
            "Candidate conflict",
        )
        self.repository.git("switch", "main")
        self.repository.commit_file("shared.txt", "main\n", "Main conflict")
        merge = self.repository.git(
            "merge",
            "--no-ff",
            "temporary-delivery",
            "-m",
            "Integrate",
            check=False,
        )
        self.assertNotEqual(0, merge.returncode)

        unresolved = observe_direct_main_completion(
            self.repository,
            configured_main="main",
            source_commit=source_commit,
            integration_commit=source_commit,
        )
        self.assertEqual("BLOCKED", unresolved.disposition)
        self.assertEqual("main-worktree-not-clean", unresolved.blocker)

        (self.repository.path / "shared.txt").write_text(
            "main\ncandidate\n",
            encoding="utf-8",
        )
        self.repository.git("add", "shared.txt")
        self.repository.git("commit", "-m", "Resolve from both sources")
        integration_commit = self.repository.rev_parse("HEAD")
        resolved = observe_direct_main_completion(
            self.repository,
            configured_main="main",
            source_commit=source_commit,
            integration_commit=integration_commit,
            verification_passed=True,
        )
        self.assertEqual("READY", resolved.disposition)

    def test_failed_verification_missing_publication_authority_and_live_claim_block(self) -> None:
        source_commit = self.repository.commit_file(
            "feature.txt",
            "candidate\n",
            "Candidate",
        )
        scenarios = (
            ({"verification_passed": False}, "verification-failed"),
            (
                {"publication_required": True, "publication_authorized": False},
                "publication-authority-missing",
            ),
            ({"claim_released": False}, "integration-claim-live"),
        )
        for overrides, expected_blocker in scenarios:
            with self.subTest(expected_blocker=expected_blocker):
                result = observe_direct_main_completion(
                    self.repository,
                    configured_main="main",
                    source_commit=source_commit,
                    integration_commit=source_commit,
                    **overrides,
                )
                self.assertEqual("BLOCKED", result.disposition)
                self.assertEqual(expected_blocker, result.blocker)
                self.assertIsNone(result.provider_lifecycle_update)

    def test_non_ancestral_replay_requires_content_equivalence(self) -> None:
        self.repository.git("switch", "-c", "temporary-delivery")
        source_commit = self.repository.commit_file(
            "feature.txt",
            "candidate\n",
            "Candidate",
        )
        self.repository.git("switch", "main")
        self.repository.commit_file(
            "unrelated.txt",
            "main advance\n",
            "Advance main before replay",
        )
        self.repository.git("cherry-pick", source_commit)
        integration_commit = self.repository.rev_parse("HEAD")
        self.assertNotEqual(source_commit, integration_commit)
        self.assertNotEqual(
            0,
            self.repository.git(
                "merge-base",
                "--is-ancestor",
                source_commit,
                "main",
                check=False,
            ).returncode,
        )

        without_mapping = observe_direct_main_completion(
            self.repository,
            configured_main="main",
            source_commit=source_commit,
            integration_commit=integration_commit,
        )
        with_mapping = observe_direct_main_completion(
            self.repository,
            configured_main="main",
            source_commit=source_commit,
            integration_commit=integration_commit,
            allow_non_ancestral_mapping=True,
        )

        self.assertEqual("BLOCKED", without_mapping.disposition)
        self.assertEqual("READY", with_mapping.disposition)

    def test_provider_handoff_receives_exact_observed_main_commit(self) -> None:
        source_commit = self.repository.commit_file(
            "feature.txt",
            "candidate\n",
            "Candidate",
        )

        result = observe_direct_main_completion(
            self.repository,
            configured_main="main",
            source_commit=source_commit,
            integration_commit=source_commit,
        )

        self.assertIsNotNone(result.provider_lifecycle_update)
        assert result.provider_lifecycle_update is not None
        self.assertEqual(
            self.repository.rev_parse("main"),
            result.provider_lifecycle_update["observed_main_commit"],
        )
        self.assertEqual(
            "COMPLETED",
            result.provider_lifecycle_update["requested_lifecycle"],
        )


if __name__ == "__main__":
    unittest.main()
