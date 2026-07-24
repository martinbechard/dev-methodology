# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies Dev Backlog Steward blocked-work resumption and Future Ideas evaluation contracts.
# Governing design: evals/agent-tests/dev-backlog-steward/skills/dev-backlog-steward-suite-contract/SKILL.md
# Governing test plan: evals/agent-tests/dev-backlog-steward/scenarios.yaml

from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import yaml


SUITE_ROOT = Path(__file__).resolve().parent
_HARNESS_PATH = SUITE_ROOT / "contract_harness.py"
_SPEC = importlib.util.spec_from_file_location(
    "dev_backlog_steward_contract_harness", _HARNESS_PATH
)
assert _SPEC is not None and _SPEC.loader is not None
contract_harness = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = contract_harness
_SPEC.loader.exec_module(contract_harness)


def _restore_snapshot(path: Path, existed: bool, content: bytes) -> None:
    """Restore one path to its exact pre-attempt bytes or absence."""
    if existed:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    else:
        path.unlink(missing_ok=True)


def _execute_promotion_transaction(
    repository: Path,
    idea: Path,
    target: Path,
    idea_after: bytes,
    target_after: bytes,
    *,
    fail_commit: bool = False,
) -> dict[str, object]:
    """Exercise the promotion contract against a real temporary Git index.

    The transaction snapshots exact worktree and index bytes, stages only the
    reciprocal records, and commits only those paths. A failed operation
    restores and verifies the snapshots. An injected rollback failure retains
    its evidence and reports the recovery owner instead of claiming readiness.
    """
    idea_relative = idea.relative_to(repository).as_posix()
    target_relative = target.relative_to(repository).as_posix()
    if target.exists():
        return {
            "status": "BLOCKED",
            "rollbackVerified": True,
            "claimRetained": False,
            "reason": "target collision",
        }
    idea_existed = idea.exists()
    idea_before = idea.read_bytes() if idea_existed else b""
    target_existed = target.exists()
    target_before = target.read_bytes() if target_existed else b""
    index_location = subprocess.run(
        ["git", "-C", str(repository), "rev-parse", "--git-path", "index"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    index_path = Path(index_location)
    if not index_path.is_absolute():
        index_path = repository / index_path
    index_existed = index_path.exists()
    index_before = index_path.read_bytes() if index_existed else b""
    recovery = (
        repository
        / ".git"
        / "future-idea-promotion-recovery"
        / "contract-attempt"
    )
    recovery.mkdir(parents=True)
    (recovery / "idea.bin").write_bytes(idea_before)
    (recovery / "target.bin").write_bytes(target_before)
    (recovery / "target-state").write_bytes(
        b"present\n" if target_existed else b"absent\n"
    )
    (recovery / "index.bin").write_bytes(index_before)
    (recovery / "index-state").write_bytes(
        b"present\n" if index_existed else b"absent\n"
    )

    commit_created = False
    try:
        idea.write_bytes(idea_after)
        target.write_bytes(target_after)
        subprocess.run(
            [
                "git",
                "-C",
                str(repository),
                "add",
                "--",
                idea_relative,
                target_relative,
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        if target_relative.encode("utf-8") not in idea_after:
            raise ValueError("idea lacks reciprocal target provenance")
        if idea_relative.encode("utf-8") not in target_after:
            raise ValueError("target lacks reciprocal idea provenance")
        commit_arguments = [
            "git",
            "-C",
            str(repository),
            "commit",
            "--quiet",
            "--only",
        ]
        if fail_commit:
            commit_arguments.append("--cleanup=invalid")
        commit_arguments.extend(
            [
                "-m",
                "Promote Future Idea",
                "--",
                idea_relative,
                target_relative,
            ]
        )
        subprocess.run(
            commit_arguments,
            check=True,
            capture_output=True,
            text=True,
        )
        commit_created = True
        committed_paths = set(
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(repository),
                    "diff-tree",
                    "--no-commit-id",
                    "--name-only",
                    "-r",
                    "HEAD",
                ],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.splitlines()
        )
        if committed_paths != {idea_relative, target_relative}:
            raise RuntimeError("confirmed commit does not contain exactly the pair")
        for relative_path, expected_content in (
            (idea_relative, idea_after),
            (target_relative, target_after),
        ):
            committed_content = subprocess.run(
                [
                    "git",
                    "-C",
                    str(repository),
                    "show",
                    f"HEAD:{relative_path}",
                ],
                check=True,
                capture_output=True,
            ).stdout
            if committed_content != expected_content:
                raise RuntimeError(
                    "confirmed reciprocal record bytes do not match"
                )
    except (OSError, subprocess.CalledProcessError, ValueError, RuntimeError) as exc:
        if commit_created:
            return {
                "status": "BLOCKED",
                "rollbackVerified": False,
                "claimRetained": True,
                "recoveryOwner": "Dev Backlog Steward",
                "preservedEvidence": recovery,
                "failure": str(exc),
            }
        try:
            _restore_snapshot(idea, idea_existed, idea_before)
            _restore_snapshot(target, target_existed, target_before)
            _restore_snapshot(index_path, index_existed, index_before)
            if (
                idea.exists() != idea_existed
                or target.exists() != target_existed
                or index_path.exists() != index_existed
                or (idea_existed and idea.read_bytes() != idea_before)
                or (target_existed and target.read_bytes() != target_before)
                or (index_existed and index_path.read_bytes() != index_before)
            ):
                raise OSError("rollback verification failed")
        except OSError as rollback_error:
            return {
                "status": "BLOCKED",
                "rollbackVerified": False,
                "claimRetained": True,
                "recoveryOwner": "Dev Backlog Steward",
                "preservedEvidence": recovery,
                "failure": str(rollback_error),
            }
        shutil.rmtree(recovery)
        return {
            "status": "BLOCKED",
            "rollbackVerified": True,
            "claimRetained": False,
            "failure": str(exc),
        }
    shutil.rmtree(recovery)
    return {
        "status": "READY",
        "commitVerified": True,
        "claimRetained": False,
    }


class DevBacklogStewardContractTests(unittest.TestCase):
    """Protect explicit claim acquisition and evidence preservation during resumption."""

    def _git(self, repository: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
        """Run one checked Git command in a disposable contract repository."""
        return subprocess.run(
            ["git", "-C", str(repository), *arguments],
            check=True,
            capture_output=True,
            text=True,
        )

    def _promotion_repository(
        self,
    ) -> tuple[tempfile.TemporaryDirectory[str], Path, Path, Path, Path, Path]:
        """Create a Git repository with one idea and unrelated staged state."""
        temporary = tempfile.TemporaryDirectory()
        repository = Path(temporary.name)
        self._git(repository, "init", "--quiet")
        self._git(repository, "config", "user.name", "Contract Test")
        self._git(repository, "config", "user.email", "contract@example.invalid")
        idea = repository / "backlog/future-ideas/retry-dashboard.md"
        target = repository / "backlog/feature-backlog/retry-dashboard.md"
        unrelated = repository / "unrelated.txt"
        idea.parent.mkdir(parents=True)
        target.parent.mkdir(parents=True)
        idea.write_bytes(
            b"# Retry Dashboard\n\n## Synopsis\n\nObserve retries.\n"
            b"\n## Origin or Rationale\n\nOperator feedback.\n"
        )
        unrelated.write_bytes(b"base unrelated bytes\n")
        self._git(repository, "add", "--", idea.relative_to(repository).as_posix())
        self._git(
            repository,
            "add",
            "--",
            unrelated.relative_to(repository).as_posix(),
        )
        self._git(repository, "commit", "--quiet", "-m", "Initial state")
        unrelated.write_bytes(b"unrelated staged bytes\n")
        self._git(
            repository,
            "add",
            "--",
            unrelated.relative_to(repository).as_posix(),
        )
        index_location = self._git(
            repository, "rev-parse", "--git-path", "index"
        ).stdout.strip()
        index_path = Path(index_location)
        if not index_path.is_absolute():
            index_path = repository / index_path
        return temporary, repository, idea, target, unrelated, index_path

    def test_blocked_handoff_releases_prior_ownership_and_preserves_evidence(self) -> None:
        """A blocked handoff ends the prior claim without losing durable evidence."""
        fixture = yaml.safe_load(
            (SUITE_ROOT / "fixtures" / "cases.yaml").read_text(encoding="utf-8")
        )["cases"]["blocked-state-transition"]
        before = fixture["itemBefore"].encode("utf-8")

        after, transitions = contract_harness.block_for_handoff(before)

        self.assertEqual(("running", "blocked", "released"), transitions)
        expected = before.replace(b"Status: Running", b"Status: Blocked", 1)
        expected = expected.replace(b"Owner: dev-coder", b"Owner: Unowned", 1)
        expected = expected.replace(
            b"Claim: schema-migration-active", b"Claim: None", 1
        )
        self.assertEqual(expected, after)
        for preserved_line in (
            b"Blocker: External schema decision is unavailable.",
            b"Unblock Condition: Approved schema decision is recorded.",
            b"Evidence: Existing schema analysis and verification log.",
            (
                b"Acceptance Criteria: Schema decision remains traceable; "
                b"existing verification remains required."
            ),
        ):
            with self.subTest(preserved_line=preserved_line):
                self.assertIn(preserved_line, after)

    def test_future_ideas_case_and_output_contract_are_aligned(self) -> None:
        """Every suite surface exposes a meaningful Future Idea output contract."""
        fixture = yaml.safe_load(
            (SUITE_ROOT / "fixtures" / "cases.yaml").read_text(encoding="utf-8")
        )["cases"]["future-ideas-capture-and-promotion"]
        scenarios = yaml.safe_load(
            (SUITE_ROOT / "scenarios.yaml").read_text(encoding="utf-8")
        )["scenarios"]
        scenario = next(
            entry
            for entry in scenarios
            if entry["id"] == "future-ideas-capture-and-promotion"
        )
        suite = yaml.safe_load(
            (SUITE_ROOT / "suite.yaml").read_text(encoding="utf-8")
        )
        role = yaml.safe_load(
            (
                SUITE_ROOT.parent.parent.parent
                / "agents"
                / "roles"
                / "dev-activities"
                / "dev-backlog-steward.role.yaml"
            ).read_text(encoding="utf-8")
        )
        expected_output = "backlog item, Future Idea, or status update"

        self.assertEqual("file", fixture["provider"])
        self.assertEqual("github", fixture["nonFileProviderWithoutOverride"])
        self.assertIn("BLOCKED", fixture["nonFileProviderResult"])
        self.assertFalse(fixture["ordinaryScanIncludesIdea"])
        self.assertNotIn("Status:", fixture["ideaBefore"])
        self.assertIn("Completion: direct-main", fixture["promotedWorkItem"])
        self.assertIn("## Open Questions", fixture["promotedWorkItem"])
        self.assertEqual(expected_output, fixture["expectedOutput"])
        self.assertIn(expected_output, scenario["expectedOutputs"])
        self.assertIn(expected_output, suite["target"]["requiredOutputs"])
        self.assertIn(
            expected_output,
            [next(iter(entry)) for entry in role["outputContract"]],
        )
        self.assertIn(
            "Return the Future Idea output contract", scenario["requiredBehaviors"]
        )

    def test_future_idea_promotion_is_failure_atomic_at_every_boundary(self) -> None:
        """Collision and injected failures restore exact pre-attempt promotion state."""
        fixture = yaml.safe_load(
            (SUITE_ROOT / "fixtures" / "cases.yaml").read_text(encoding="utf-8")
        )["cases"]["future-ideas-capture-and-promotion"]
        scenario = next(
            entry
            for entry in yaml.safe_load(
                (SUITE_ROOT / "scenarios.yaml").read_text(encoding="utf-8")
            )["scenarios"]
            if entry["id"] == "future-ideas-capture-and-promotion"
        )
        contract_text = (
            SUITE_ROOT
            / "skills"
            / "dev-backlog-steward-suite-contract"
            / "SKILL.md"
        ).read_text(encoding="utf-8")
        role = yaml.safe_load(
            (
                SUITE_ROOT.parent.parent.parent
                / "agents"
                / "roles"
                / "dev-activities"
                / "dev-backlog-steward.role.yaml"
            ).read_text(encoding="utf-8")
        )
        transaction = fixture["promotionTransaction"]
        collision = transaction["collision"]
        git_index = transaction["gitIndex"]

        self.assertEqual("BLOCKED", collision["result"])
        self.assertFalse(collision["writesAttempted"])
        self.assertEqual(collision["ideaBefore"], collision["ideaAfter"])
        self.assertEqual(collision["targetBefore"], collision["targetAfter"])
        self.assertEqual(
            {"target-write", "idea-write", "validation", "commit"},
            {
                failure["boundary"]
                for failure in transaction["injectedFailures"]
            },
        )
        for failure in transaction["injectedFailures"]:
            with self.subTest(boundary=failure["boundary"]):
                self.assertEqual(failure["ideaBefore"], failure["ideaAfter"])
                if failure["targetExistedBefore"]:
                    self.assertEqual(failure["targetBefore"], failure["targetAfter"])
                else:
                    self.assertEqual("absent", failure["targetAfter"])
                self.assertEqual(
                    "remove only a target created by this attempt",
                    failure["cleanupScope"],
                )

        self.assertEqual(
            "exact full file bytes and existence",
            git_index["preAttemptSnapshot"],
        )
        self.assertEqual(
            [fixture["ideaPath"], fixture["promotedWorkItemPath"]],
            git_index["stagedPaths"],
        )
        self.assertEqual("path-limited", git_index["commitMode"])
        self.assertTrue(git_index["preserveUnrelatedStagedState"])
        self.assertEqual(
            [fixture["ideaPath"], fixture["promotedWorkItemPath"]],
            git_index["verifiedCommitPaths"],
        )
        self.assertEqual(
            "restore exact bytes and existence then verify",
            git_index["failureRestoration"],
        )
        self.assertEqual("BLOCKED", git_index["rollbackFailure"]["status"])
        self.assertTrue(git_index["rollbackFailure"]["claimRetained"])
        self.assertEqual(
            "Dev Backlog Steward",
            git_index["rollbackFailure"]["recoveryOwner"],
        )
        for behavior in (
            "Preflight target collisions before any promotion write",
            "Snapshot exact idea bytes target bytes and target existence",
            "Restore exact pre-attempt state after target-write idea-write validation or commit failure",
            "Snapshot exact full Git index file bytes and existence under the serialized primary-main backlog claim",
            "Stage and path-limit commit to exactly the idea and target while preserving unrelated staged state",
            "Verify the confirmed commit contains exactly the reciprocal idea and target pair",
            "Restore and verify exact pre-attempt index bytes and existence on failure",
            "Retain the claim and recovery evidence when rollback cannot be verified",
        ):
            with self.subTest(required_behavior=behavior):
                self.assertIn(behavior, scenario["requiredBehaviors"])
        self.assertIn("failure-atomic transaction", contract_text)
        self.assertIn("target-write, idea-write, validation, or commit", contract_text)
        self.assertIn("exact full Git index file", contract_text)
        self.assertIn("path-limited commit", contract_text)
        self.assertIn("retain the backlog claim", contract_text)
        self.assertTrue(
            any(
                "Restore the exact pre-attempt idea and target state"
                in step
                for step in role["instructions"]["failureHandling"]
            )
        )
        self.assertTrue(
            any(
                "A retained recovery claim is always BLOCKED" in step
                for step in role["instructions"]["completion"]
            )
        )

    def test_failed_promotion_commit_restores_worktree_and_exact_index(self) -> None:
        """A failed path-limited commit restores bytes and unrelated staged state."""
        temporary, repository, idea, target, _, index_path = (
            self._promotion_repository()
        )
        self.addCleanup(temporary.cleanup)
        idea_before = idea.read_bytes()
        index_before = index_path.read_bytes()

        result = _execute_promotion_transaction(
            repository,
            idea,
            target,
            b"# Retry Dashboard\n\nPromoted To: "
            b"backlog/feature-backlog/retry-dashboard.md\n",
            b"# Retry Dashboard\n\n## Source Evidence\n\n"
            b"- backlog/future-ideas/retry-dashboard.md\n",
            fail_commit=True,
        )

        self.assertEqual("BLOCKED", result["status"])
        self.assertTrue(result["rollbackVerified"])
        self.assertFalse(result["claimRetained"])
        self.assertEqual(idea_before, idea.read_bytes())
        self.assertFalse(target.exists())
        self.assertEqual(index_before, index_path.read_bytes())
        self.assertEqual(
            "unrelated.txt",
            self._git(
                repository, "diff", "--cached", "--name-only"
            ).stdout.strip(),
        )

    def test_successful_promotion_commits_only_pair_and_preserves_staged_state(
        self,
    ) -> None:
        """A successful path-limited commit contains only reciprocal records."""
        temporary, repository, idea, target, _, _ = self._promotion_repository()
        self.addCleanup(temporary.cleanup)
        unrelated_staged_before = self._git(
            repository, "diff", "--cached", "--", "unrelated.txt"
        ).stdout

        result = _execute_promotion_transaction(
            repository,
            idea,
            target,
            b"# Retry Dashboard\n\nPromoted To: "
            b"backlog/feature-backlog/retry-dashboard.md\n",
            b"# Retry Dashboard\n\n## Source Evidence\n\n"
            b"- backlog/future-ideas/retry-dashboard.md\n",
        )

        self.assertEqual("READY", result["status"])
        self.assertTrue(result["commitVerified"])
        self.assertEqual(
            {
                "backlog/future-ideas/retry-dashboard.md",
                "backlog/feature-backlog/retry-dashboard.md",
            },
            set(
                self._git(
                    repository,
                    "diff-tree",
                    "--no-commit-id",
                    "--name-only",
                    "-r",
                    "HEAD",
                ).stdout.splitlines()
            ),
        )
        self.assertEqual(
            "unrelated.txt",
            self._git(
                repository, "diff", "--cached", "--name-only"
            ).stdout.strip(),
        )
        self.assertEqual(
            unrelated_staged_before,
            self._git(
                repository, "diff", "--cached", "--", "unrelated.txt"
            ).stdout,
        )

    def test_promotion_rollback_failure_retains_claim_and_recovery_evidence(
        self,
    ) -> None:
        """Rollback failure returns truthful BLOCKED ownership and durable evidence."""
        temporary, repository, idea, target, _, index_path = (
            self._promotion_repository()
        )
        self.addCleanup(temporary.cleanup)
        idea_before = idea.read_bytes()
        index_before = index_path.read_bytes()

        with mock.patch.object(
            sys.modules[__name__],
            "_restore_snapshot",
            side_effect=OSError("injected rollback failure"),
        ):
            result = _execute_promotion_transaction(
                repository,
                idea,
                target,
                b"# Retry Dashboard\n\nPromoted To: "
                b"backlog/feature-backlog/retry-dashboard.md\n",
                b"# Retry Dashboard\n\n## Source Evidence\n\n"
                b"- backlog/future-ideas/retry-dashboard.md\n",
                fail_commit=True,
            )

        evidence = Path(str(result["preservedEvidence"]))
        self.assertEqual("BLOCKED", result["status"])
        self.assertFalse(result["rollbackVerified"])
        self.assertTrue(result["claimRetained"])
        self.assertEqual("Dev Backlog Steward", result["recoveryOwner"])
        self.assertEqual(idea_before, (evidence / "idea.bin").read_bytes())
        self.assertEqual(index_before, (evidence / "index.bin").read_bytes())
        self.assertEqual(b"absent\n", (evidence / "target-state").read_bytes())

    def test_blocked_resumption_has_negative_and_positive_scenarios(self) -> None:
        """The suite covers unowned, failed-claim, and successful claim outcomes."""
        scenarios = yaml.safe_load(
            (SUITE_ROOT / "scenarios.yaml").read_text(encoding="utf-8")
        )["scenarios"]
        by_id = {scenario["id"]: scenario for scenario in scenarios}

        shortcut = by_id["blocked-unowned-running-shortcut"]
        self.assertEqual("BLOCKED", shortcut["expectedTerminalStatus"])
        self.assertIn("Leave the backlog item unchanged", shortcut["requiredBehaviors"])
        self.assertIn(
            "Reject because no new claim and owner exist",
            shortcut["requiredBehaviors"],
        )

        resumption = by_id["blocked-claimed-resumption"]
        self.assertEqual("PASS", resumption["expectedTerminalStatus"])
        self.assertIn(
            "Record Ready then a successful new claim and owner before Running",
            resumption["requiredBehaviors"],
        )

        failed_claim = by_id["blocked-failed-claim-resumption"]
        self.assertEqual("BLOCKED", failed_claim["expectedTerminalStatus"])
        self.assertIn("CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED", failed_claim["initialState"])
        self.assertIn("project-hash-policy", failed_claim["deterministicChecks"])

    def test_failed_or_missing_claim_leaves_the_item_unchanged(self) -> None:
        """Missing and conflict-wait claim outcomes keep exact blocked bytes and evidence."""
        cases = yaml.safe_load(
            (SUITE_ROOT / "fixtures" / "cases.yaml").read_text(encoding="utf-8")
        )["cases"]

        expected_transitions = {
            "blocked-unowned-running-shortcut": ("blocked", "rejected-unowned"),
            "blocked-failed-claim-resumption": (
                "blocked",
                "ready",
                "claim-failed",
                "blocked",
            ),
        }
        for case_id, transitions_expected in expected_transitions.items():
            fixture = cases[case_id]
            before = fixture["itemBefore"].encode("utf-8")
            claim_outcomes = [fixture["claimOutcome"]]
            claim_outcomes.extend(fixture.get("otherFailedClaimOutcomes", []))
            for claim_outcome in claim_outcomes:
                after, transitions = contract_harness.attempt_resumption(
                    before,
                    unblock_condition_satisfied=fixture["unblockConditionSatisfied"],
                    claim_outcome=claim_outcome,
                )

                with self.subTest(case_id=case_id, claim_outcome=claim_outcome):
                    self.assertEqual(before, after)
                    self.assertEqual(transitions_expected, transitions)
                    self.assertIn(b"Status: Blocked", after)
                    self.assertIn(b"Owner: Unowned", after)
                    self.assertIn(b"Claim: None", after)
                    self.assertNotIn(b"Status: Running", after)

    def test_successful_claim_resumes_in_order_and_preserves_evidence(self) -> None:
        """A new claim and owner precede Running without rewriting prior evidence."""
        fixture = yaml.safe_load(
            (SUITE_ROOT / "fixtures" / "cases.yaml").read_text(encoding="utf-8")
        )["cases"]["blocked-claimed-resumption"]
        before = fixture["itemBefore"].encode("utf-8")

        after, transitions = contract_harness.attempt_resumption(
            before,
            unblock_condition_satisfied=fixture["unblockConditionSatisfied"],
            claim_outcome=fixture["claimOutcome"],
            new_owner=fixture["newOwner"],
            new_claim=fixture["newClaim"],
        )

        self.assertEqual(("blocked", "ready", "claimed", "running"), transitions)
        self.assertLess(transitions.index("ready"), transitions.index("claimed"))
        self.assertLess(transitions.index("claimed"), transitions.index("running"))
        expected = before.replace(b"Status: Blocked", b"Status: Running", 1)
        expected = expected.replace(b"Owner: Unowned", b"Owner: dev-coder", 1)
        expected = expected.replace(
            b"Claim: None", b"Claim: schema-migration-resumption", 1
        )
        self.assertEqual(expected, after)
        for preserved_line in (
            b"Blocker: External schema decision is unavailable.",
            b"Unblock Condition: Approved schema decision is recorded.",
            b"Evidence: Existing schema analysis and verification log.",
            (
                b"Acceptance Criteria: Schema decision remains traceable; "
                b"existing verification remains required."
            ),
        ):
            with self.subTest(preserved_line=preserved_line):
                self.assertIn(preserved_line, after)


if __name__ == "__main__":
    unittest.main()
