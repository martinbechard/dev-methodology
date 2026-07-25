# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies command claims, resource deadlines, journaling, isolation, recovery, and release invariants.

from __future__ import annotations

import base64
import gzip
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from collections.abc import Mapping
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLAIM_SCRIPT = ROOT / "skills" / "agent-claim-command" / "scripts" / "claim.py"


class AgentClaimTests(unittest.TestCase):
    """Exercises the public claim command against temporary linked Git worktrees."""

    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.repository = Path(self.temporary_directory.name) / "repository"
        self.repository.mkdir()
        (self.repository / "src").mkdir()
        (self.repository / "docs").mkdir()
        (self.repository / "backlog" / "feature-backlog").mkdir(parents=True)
        (self.repository / ".gitignore").write_text("/.worktrees/\n", encoding="utf-8")
        (self.repository / "README.md").write_text("baseline\n", encoding="utf-8")
        (self.repository / "src" / "one.py").write_text("one\n", encoding="utf-8")
        (self.repository / "docs" / "guide.md").write_text("guide\n", encoding="utf-8")
        (self.repository / "backlog" / "feature-backlog" / "queued.md").write_text(
            "queued\n",
            encoding="utf-8",
        )
        self.write_deadline_policy()
        self.git("init")
        self.git("config", "user.email", "test@example.invalid")
        self.git("config", "user.name", "Claim Test")
        self.git("add", ".")
        self.git("commit", "-m", "baseline")

    def git(self, *arguments: str, worktree: Path | None = None) -> subprocess.CompletedProcess[str]:
        """Run Git in the requested temporary worktree and require success."""
        return subprocess.run(
            ["git", "-C", str(worktree or self.repository), *arguments],
            check=True,
            text=True,
            capture_output=True,
        )

    def claim(
        self,
        *arguments: str,
        repo: Path | None = None,
        environment: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        """Run the bundled command with optional deterministic-clock and fault-injection variables."""
        command_environment = os.environ.copy()
        command_environment["PYTHONDONTWRITEBYTECODE"] = "1"
        command_environment.update(environment or {})
        return subprocess.run(
            [sys.executable, str(CLAIM_SCRIPT), "--repo", str(repo or self.repository), *arguments],
            check=False,
            text=True,
            capture_output=True,
            env=command_environment,
        )

    def claim_command(self, *arguments: str, repo: Path | None = None) -> list[str]:
        """Build a subprocess command for concurrency tests without executing it."""
        return [sys.executable, str(CLAIM_SCRIPT), "--repo", str(repo or self.repository), *arguments]

    def acquire_arguments(self, claim_id: str) -> list[str]:
        """Build the common acquisition arguments for one independent test task."""
        return [
            "acquire",
            "--claim-id",
            claim_id,
            "--agent",
            claim_id,
            "--task",
            f"task {claim_id}",
            "--root-task-id",
            claim_id,
        ]

    def isolated_arguments(self, claim_id: str, path_name: str | None = None) -> tuple[list[str], Path]:
        """Build a unique branch and the canonical worktree expected for a later writer."""
        isolated_path = (self.repository / ".worktrees" / (path_name or claim_id)).resolve()
        return ["--branch", f"codex/{claim_id}"], isolated_path

    def existing_linked_worktree(self, name: str = "private") -> Path:
        """Create an existing non-canonical linked checkout for caller-topology tests."""
        linked_path = (Path(self.temporary_directory.name) / f"{name}-checkout").resolve()
        self.git("worktree", "add", "-b", f"codex/{name}", str(linked_path), "HEAD")
        return linked_path

    def timed_resource_arguments(
        self,
        resource: str = "port:3000",
        resource_class: str = "database-port",
        resource_id: str | None = None,
        expected_duration_seconds: int = 300,
        requested_hard_stop_duration_seconds: int = 900,
    ) -> list[str]:
        """Build one complete deterministic deadline request for a named resource."""
        return [
            "--resource",
            resource,
            "--resource-class",
            resource_class,
            "--resource-id",
            resource if resource_id is None else resource_id,
            "--expected-duration-seconds",
            str(expected_duration_seconds),
            "--requested-hard-stop-duration-seconds",
            str(requested_hard_stop_duration_seconds),
        ]

    def deadline_policy(self) -> dict[str, object]:
        """Return the five configured class defaults used by command tests."""
        return {
            "resource_coordination": {
                "selected": "agent-claim",
                "deadline_policy": {
                    "resource_classes": {
                        "backlog-mutation": {
                            "maximum_duration_seconds": 600,
                            "cleanup_grace_seconds": 120,
                        },
                        "main-integration": {
                            "maximum_duration_seconds": 2700,
                            "cleanup_grace_seconds": 600,
                        },
                        "browser-server": {
                            "maximum_duration_seconds": 3600,
                            "cleanup_grace_seconds": 600,
                        },
                        "database-port": {
                            "maximum_duration_seconds": 1800,
                            "cleanup_grace_seconds": 300,
                        },
                        "live-model-evaluation": {
                            "maximum_duration_seconds": 14400,
                            "cleanup_grace_seconds": 1800,
                        },
                    },
                    "resource_overrides": {},
                },
            }
        }

    def write_deadline_policy(self, policy: dict[str, object] | None = None) -> None:
        """Write one YAML-compatible JSON project policy into the temporary repository."""
        (self.repository / "PROJECT.yaml").write_text(
            json.dumps(policy if policy is not None else self.deadline_policy(), indent=2) + "\n",
            encoding="utf-8",
        )

    def output(self, completed: subprocess.CompletedProcess[str]) -> dict[str, object]:
        """Decode one structured command result."""
        return json.loads(completed.stdout)

    def common_directory(self) -> Path:
        """Return the temporary repository's Git common directory."""
        raw = Path(self.git("rev-parse", "--git-common-dir").stdout.strip())
        return raw if raw.is_absolute() else self.repository / raw

    def registry_path(self) -> Path:
        """Return the repository-global live registry path."""
        return self.common_directory() / "agent-claims.json"

    def hot_directory(self) -> Path:
        """Return the repository-global hot journal directory."""
        return self.common_directory() / "agent-claim-events" / "hot"

    def journal_events(self) -> list[dict[str, object]]:
        """Read all hot events for lifecycle and concurrency assertions."""
        events: list[dict[str, object]] = []
        for path in sorted(self.hot_directory().glob("*.jsonl")):
            events.extend(json.loads(line) for line in path.read_text(encoding="utf-8").splitlines())
        return events

    def journal_bytes(self) -> dict[str, bytes]:
        """Return exact hot-journal bytes keyed by repository-relative journal path."""
        return {
            str(path.relative_to(self.common_directory())): path.read_bytes()
            for path in sorted(self.hot_directory().glob("*.jsonl"))
        }

    def downgrade_claim_incarnations_to_legacy_fixture(self) -> None:
        """Remove incarnation fields from temporary registry and journal fixtures."""
        registry = json.loads(self.registry_path().read_text(encoding="utf-8"))
        for claim in registry["claims"]:
            claim.pop("incarnation_id", None)
        self.registry_path().write_text(
            json.dumps(registry, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        for path in sorted(self.hot_directory().glob("*.jsonl")):
            events = [
                json.loads(line)
                for line in path.read_text(encoding="utf-8").splitlines()
            ]
            for event in events:
                event.pop("incarnation_id", None)
            path.write_text(
                "".join(
                    json.dumps(event, sort_keys=True, separators=(",", ":")) + "\n"
                    for event in events
                ),
                encoding="utf-8",
            )

    def write_daily_events(self, day: str, events: list[dict[str, object]]) -> Path:
        """Write a deterministic historical hot file for archive and report tests."""
        self.hot_directory().mkdir(parents=True, exist_ok=True)
        path = self.hot_directory() / f"{day}.jsonl"
        path.write_text("".join(json.dumps(event, sort_keys=True) + "\n" for event in events), encoding="utf-8")
        return path

    def synthetic_event(
        self,
        event_id: str,
        timestamp: str,
        action: str,
        outcome: str,
        claim_id: str,
        **values: object,
    ) -> dict[str, object]:
        """Build the minimum versioned event fixture accepted by reporting and archival."""
        event: dict[str, object] = {
            "schema_version": 1,
            "event_id": event_id,
            "timestamp": timestamp,
            "action": action,
            "outcome": outcome,
            "claim_id": claim_id,
            "journal_warnings": [],
        }
        event.update(values)
        return event

    def release_reconciliation_fixture(
        self,
        claim_id: str = "project",
    ) -> dict[str, str]:
        """Create one rejected release whose baseline dirtiness was preserved by a peer commit."""
        backlog_path = self.repository / "backlog" / "feature-backlog" / "queued.md"
        backlog_path.write_text("pre-existing peer work\n", encoding="utf-8")
        acquired = self.claim(
            *self.acquire_arguments(claim_id),
            "--project-files",
            "--scope-reason",
            "project work",
        )
        self.assertEqual(0, acquired.returncode, acquired.stderr)
        baseline_commit = self.output(acquired)["claim"]["baseline_commit"]

        self.git("add", "backlog/feature-backlog/queued.md")
        self.git("commit", "-m", "preserve peer backlog work")
        peer_commit = self.git("rev-parse", "HEAD").stdout.strip()

        (self.repository / "src" / "one.py").write_text("claimed work\n", encoding="utf-8")
        self.git("add", "src/one.py")
        self.git("commit", "-m", "complete claimed project work")
        head_commit = self.git("rev-parse", "HEAD").stdout.strip()

        rejected = self.claim("release", "--claim-id", claim_id)
        self.assertEqual(1, rejected.returncode, rejected.stderr)
        rejection = self.output(rejected)
        self.assertEqual("out_of_domain_changes", rejection["reason"])
        return {
            "baseline_commit": str(baseline_commit),
            "head_commit": head_commit,
            "peer_commit": peer_commit,
            "prior_rejected_release_reference": str(rejection["journal"]["event_id"]),
        }

    def test_first_writer_claims_clean_primary_worktree(self) -> None:
        completed = self.claim(*self.acquire_arguments("first"), "--file", "README.md")

        self.assertEqual(0, completed.returncode, completed.stderr)
        result = self.output(completed)
        self.assertEqual(2, result["schema_version"])
        self.assertEqual("SHARED_CHECKOUT_ACQUIRED", result["outcome"])
        self.assertEqual("PRIMARY", result["legacy_outcome"])
        self.assertEqual(str(self.repository.resolve()), result["claim"]["worktree"])
        self.assertEqual("primary", result["claim"]["checkout_topology"])
        self.assertEqual("primary", result["target"]["mode"])
        self.assertEqual("primary", result["target"]["checkout_topology"])
        event = self.journal_events()[-1]
        self.assertEqual("primary", event["checkout_topology"])
        self.assertEqual("primary", event["worktree_id"])
        self.assertNotIn(str(self.temporary_directory.name), json.dumps(event))

    def test_new_claim_events_share_one_immutable_incarnation_id(self) -> None:
        acquired = self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        heartbeat = self.claim("heartbeat", "--claim-id", "first")
        released = self.claim("release", "--claim-id", "first", "--no-change")

        self.assertEqual(0, acquired.returncode, acquired.stderr)
        self.assertEqual(0, heartbeat.returncode, heartbeat.stderr)
        self.assertEqual(0, released.returncode, released.stderr)
        incarnation_id = self.output(acquired)["claim"]["incarnation_id"]
        self.assertRegex(
            incarnation_id,
            r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$",
        )
        self.assertEqual(
            [incarnation_id, incarnation_id, incarnation_id],
            [event["incarnation_id"] for event in self.journal_events()],
        )

    def test_first_writer_in_existing_linked_checkout_reports_linked_topology(self) -> None:
        linked_path = self.existing_linked_worktree()
        primary_head = self.git("rev-parse", "HEAD").stdout
        primary_status = self.git("status", "--porcelain=v1").stdout

        completed = self.claim(
            *self.acquire_arguments("private"),
            "--file",
            "README.md",
            repo=linked_path,
        )

        self.assertEqual(0, completed.returncode, completed.stderr)
        result = self.output(completed)
        self.assertEqual("SHARED_CHECKOUT_ACQUIRED", result["outcome"])
        self.assertEqual("PRIMARY", result["legacy_outcome"])
        self.assertEqual("primary", result["claim"]["mode"])
        self.assertEqual("linked", result["claim"]["checkout_topology"])
        self.assertEqual(str(linked_path), result["claim"]["worktree"])
        self.assertEqual("primary", result["target"]["mode"])
        self.assertEqual("linked", result["target"]["checkout_topology"])
        self.assertFalse((self.repository / ".worktrees" / "private").exists())
        self.assertEqual(primary_head, self.git("rev-parse", "HEAD").stdout)
        self.assertEqual(primary_status, self.git("status", "--porcelain=v1").stdout)
        event = self.journal_events()[-1]
        self.assertEqual("linked", event["checkout_topology"])
        self.assertEqual("codex/private", event["worktree_id"])
        self.assertEqual("codex/private", event["branch"])
        self.assertNotIn(str(self.temporary_directory.name), json.dumps(event))

    def test_timed_resource_acquisition_records_complete_deadline_evidence(self) -> None:
        acquired = self.claim(
            *self.acquire_arguments("timed"),
            *self.timed_resource_arguments(),
            environment={"AGENT_CLAIM_TEST_NOW": "2026-07-22T10:00:00Z"},
        )

        self.assertEqual(0, acquired.returncode, acquired.stderr)
        result = self.output(acquired)
        deadline = result["claim"]["deadline"]
        self.assertEqual("database-port", deadline["resource_class"])
        self.assertEqual("port:3000", deadline["resource_id"])
        self.assertEqual(300, deadline["expected_duration_seconds"])
        self.assertEqual(900, deadline["requested_hard_stop_duration_seconds"])
        self.assertEqual(1800, deadline["configured_maximum_duration_seconds"])
        self.assertEqual(300, deadline["cleanup_grace_seconds"])
        self.assertEqual("2026-07-22T10:05:00.000000Z", deadline["expected_release_at"])
        self.assertEqual("2026-07-22T10:15:00.000000Z", deadline["hard_stop_at"])
        self.assertEqual("2026-07-22T10:20:00.000000Z", deadline["cleanup_grace_ends_at"])
        self.assertEqual([], deadline["extensions"])
        event = self.journal_events()[-1]
        self.assertEqual(deadline, event["deadline"])

    def test_timed_resource_acquisition_rejects_incomplete_or_invalid_ordering(self) -> None:
        cases = (
            (
                ["--resource", "port:3000"],
                "Named resource acquisition requires complete timing evidence",
            ),
            (
                ["--resource", "port:3000", "--expected-duration-seconds", "300"],
                "timing arguments must be supplied together",
            ),
            (
                [
                    *self.timed_resource_arguments(),
                    "--expected-duration-seconds",
                    "901",
                ],
                "expected duration must not exceed requested hard stop",
            ),
            (
                [
                    *self.timed_resource_arguments(),
                    "--requested-hard-stop-duration-seconds",
                    "1801",
                ],
                "requested hard stop must not exceed configured maximum",
            ),
        )

        for index, (arguments, message) in enumerate(cases):
            with self.subTest(message=message):
                rejected = self.claim(
                    *self.acquire_arguments(f"invalid-{index}"),
                    *arguments,
                )
                self.assertEqual(1, rejected.returncode, rejected.stderr)
                result = self.output(rejected)
                self.assertEqual("INVALID_DEADLINE_POLICY", result["outcome"])
                self.assertIn(message, result["message"])

        status = self.output(self.claim("status"))
        self.assertEqual([], status["claims"])

    def test_timed_resource_rejects_missing_invalid_or_unselected_project_policy(self) -> None:
        cases: tuple[tuple[dict[str, object] | None, str], ...] = (
            (None, "PROJECT.yaml is required for named resource acquisition"),
            ({}, "resource_coordination must select agent-claim"),
            (
                {"resource_coordination": {"selected": "none"}},
                "resource_coordination must select agent-claim",
            ),
            (
                {
                    "resource_coordination": {
                        "selected": "agent-claim",
                        "deadline_policy": {"resource_classes": {}, "resource_overrides": {}},
                    }
                },
                "resource_classes keys must be exactly",
            ),
        )

        for index, (policy, message) in enumerate(cases):
            with self.subTest(message=message):
                if policy is None:
                    (self.repository / "PROJECT.yaml").unlink()
                else:
                    self.write_deadline_policy(policy)
                rejected = self.claim(
                    *self.acquire_arguments(f"policy-{index}"),
                    *self.timed_resource_arguments(),
                )
                self.assertEqual(1, rejected.returncode, rejected.stderr)
                self.assertEqual("INVALID_DEADLINE_POLICY", self.output(rejected)["outcome"])
                self.assertIn(message, self.output(rejected)["message"])
                self.write_deadline_policy()

    def test_exact_resource_override_replaces_class_default(self) -> None:
        policy = self.deadline_policy()
        policy["resource_coordination"]["deadline_policy"]["resource_overrides"] = {
            "port:3000": {
                "resource_class": "database-port",
                "maximum_duration_seconds": 1200,
                "cleanup_grace_seconds": 120,
            }
        }
        self.write_deadline_policy(policy)
        self.git("add", "PROJECT.yaml")
        self.git("commit", "-m", "configure exact resource override")

        acquired = self.claim(
            *self.acquire_arguments("override"),
            *self.timed_resource_arguments(requested_hard_stop_duration_seconds=1200),
        )

        self.assertEqual(0, acquired.returncode, acquired.stderr)
        deadline = self.output(acquired)["claim"]["deadline"]
        self.assertEqual(1200, deadline["configured_maximum_duration_seconds"])
        self.assertEqual(120, deadline["cleanup_grace_seconds"])

    def test_resource_class_and_exact_override_binding_must_be_configured(self) -> None:
        unknown_class = self.claim(
            *self.acquire_arguments("unknown-class"),
            *self.timed_resource_arguments(resource_class="unknown-class"),
        )
        self.assertEqual(1, unknown_class.returncode, unknown_class.stderr)
        self.assertIn("must name a configured PROJECT.yaml resource class", self.output(unknown_class)["message"])

        policy = self.deadline_policy()
        policy["resource_coordination"]["deadline_policy"]["resource_overrides"] = {
            "port:3000": {
                "resource_class": "browser-server",
                "maximum_duration_seconds": 1200,
                "cleanup_grace_seconds": 120,
            }
        }
        self.write_deadline_policy(policy)
        mismatch = self.claim(
            *self.acquire_arguments("override-mismatch"),
            *self.timed_resource_arguments(resource_class="database-port"),
        )

        self.assertEqual(1, mismatch.returncode, mismatch.stderr)
        self.assertIn("is configured for resource class browser-server", self.output(mismatch)["message"])

    def test_resource_id_is_canonicalized_before_policy_resolution_and_storage(self) -> None:
        acquired = self.claim(
            *self.acquire_arguments("normalized"),
            *self.timed_resource_arguments(
                resource="  port:3000  ",
                resource_id=" port:3000 ",
            ),
        )

        self.assertEqual(0, acquired.returncode, acquired.stderr)
        claim = self.output(acquired)["claim"]
        self.assertEqual(["port:3000"], claim["resources"])
        self.assertEqual("port:3000", claim["deadline"]["resource_id"])

    def test_resource_claim_rejects_multiple_resources_and_caller_asserted_policy(self) -> None:
        multiple = self.claim(
            *self.acquire_arguments("multiple"),
            *self.timed_resource_arguments(),
            "--resource",
            "database:secondary",
        )
        caller_maximum = self.claim(
            *self.acquire_arguments("caller-maximum"),
            *self.timed_resource_arguments(),
            "--configured-maximum-duration-seconds",
            "999999",
        )

        self.assertEqual(1, multiple.returncode, multiple.stderr)
        self.assertEqual("INVALID_DEADLINE_POLICY", self.output(multiple)["outcome"])
        self.assertIn("exactly one named resource", self.output(multiple)["message"])
        self.assertEqual(2, caller_maximum.returncode)
        self.assertIn("unrecognized arguments", caller_maximum.stderr)

    def test_file_claim_can_add_one_timed_resource_but_cannot_add_a_second(self) -> None:
        acquired = self.claim(*self.acquire_arguments("extend-resource"), "--file", "README.md")
        extended = self.claim(
            "extend",
            "--claim-id",
            "extend-resource",
            *self.timed_resource_arguments(),
            environment={"AGENT_CLAIM_TEST_NOW": "2026-07-22T11:00:00Z"},
        )
        registry_before_second = self.registry_path().read_bytes()
        second = self.claim(
            "extend",
            "--claim-id",
            "extend-resource",
            *self.timed_resource_arguments(
                resource="database:secondary",
                resource_class="database-port",
            ),
        )

        self.assertEqual(0, acquired.returncode, acquired.stderr)
        self.assertEqual(0, extended.returncode, extended.stderr)
        deadline = self.output(extended)["claim"]["deadline"]
        self.assertEqual("2026-07-22T11:00:00.000000Z", deadline["acquired_at"])
        self.assertEqual(["port:3000"], self.output(extended)["claim"]["resources"])
        self.assertEqual(1, second.returncode, second.stderr)
        self.assertEqual("INVALID_DEADLINE_POLICY", self.output(second)["outcome"])
        self.assertIn("cannot add a second named resource", self.output(second)["message"])
        self.assertEqual(registry_before_second, self.registry_path().read_bytes())

    def test_file_claim_rejects_untimed_resource_extension(self) -> None:
        acquired = self.claim(*self.acquire_arguments("extend-untimed"), "--file", "README.md")
        extended = self.claim(
            "extend",
            "--claim-id",
            "extend-untimed",
            "--resource",
            "port:3000",
        )

        self.assertEqual(0, acquired.returncode, acquired.stderr)
        self.assertEqual(1, extended.returncode, extended.stderr)
        self.assertEqual("INVALID_DEADLINE_POLICY", self.output(extended)["outcome"])

    def test_heartbeat_preserves_hard_stop_and_evidence_backed_extension_is_bounded(self) -> None:
        acquired = self.claim(
            *self.acquire_arguments("timed"),
            *self.timed_resource_arguments(),
            environment={"AGENT_CLAIM_TEST_NOW": "2026-07-22T10:00:00Z"},
        )
        extended = self.claim(
            "extend-deadline",
            "--claim-id",
            "timed",
            "--requested-hard-stop-duration-seconds",
            "1200",
            "--extension-evidence",
            "browser fixture needs one final deterministic assertion",
            environment={"AGENT_CLAIM_TEST_NOW": "2026-07-22T10:10:00Z"},
        )
        heartbeat = self.claim(
            "heartbeat",
            "--claim-id",
            "timed",
            environment={"AGENT_CLAIM_TEST_NOW": "2026-07-22T10:19:00Z"},
        )

        self.assertEqual(0, acquired.returncode, acquired.stderr)
        self.assertEqual(0, extended.returncode, extended.stderr)
        self.assertEqual(0, heartbeat.returncode, heartbeat.stderr)
        deadline = self.output(heartbeat)["claim"]["deadline"]
        self.assertEqual("2026-07-22T10:20:00.000000Z", deadline["hard_stop_at"])
        self.assertEqual(1200, deadline["requested_hard_stop_duration_seconds"])
        self.assertEqual(1, len(deadline["extensions"]))
        self.assertEqual(
            "browser fixture needs one final deterministic assertion",
            deadline["extensions"][0]["evidence"],
        )
        self.assertEqual("2026-07-22T10:19:00.000000Z", self.output(heartbeat)["claim"]["heartbeat"])
        extension_event = next(
            event
            for event in self.journal_events()
            if event["action"] == "extend-deadline" and event["outcome"] == "DEADLINE_EXTENDED"
        )
        self.assertEqual(900, extension_event["deadline_extension"]["previous_requested_hard_stop_duration_seconds"])
        self.assertEqual(1200, extension_event["deadline_extension"]["requested_hard_stop_duration_seconds"])
        self.assertEqual(1800, extension_event["deadline"]["configured_maximum_duration_seconds"])

        registry_before_rejection = self.registry_path().read_bytes()
        rejected = self.claim(
            "extend-deadline",
            "--claim-id",
            "timed",
            "--requested-hard-stop-duration-seconds",
            "1801",
            "--extension-evidence",
            "unsupported extra time",
        )
        self.assertEqual(1, rejected.returncode, rejected.stderr)
        self.assertEqual("INVALID_DEADLINE_EXTENSION", self.output(rejected)["outcome"])
        self.assertEqual(registry_before_rejection, self.registry_path().read_bytes())

    def test_status_keeps_overdue_claim_visible_without_delivery_inference_or_auto_release(self) -> None:
        acquired = self.claim(
            *self.acquire_arguments("timed"),
            *self.timed_resource_arguments(),
            environment={"AGENT_CLAIM_TEST_NOW": "2026-07-22T10:00:00Z"},
        )
        registry_before_status = self.registry_path().read_bytes()
        status = self.claim(
            "status",
            environment={"AGENT_CLAIM_TEST_NOW": "2026-07-22T10:17:00Z"},
        )

        self.assertEqual(0, acquired.returncode, acquired.stderr)
        self.assertEqual(0, status.returncode, status.stderr)
        claims = self.output(status)["claims"]
        self.assertEqual(1, len(claims))
        health = claims[0]["deadline_status"]
        self.assertTrue(health["overdue"])
        self.assertEqual(
            {
                "seconds": 300,
                "ends_at": "2026-07-22T10:20:00.000000Z",
                "active": True,
                "elapsed": False,
            },
            health["cleanup_grace"],
        )
        self.assertEqual(
            {
                "owner_stopped": None,
                "immediately_actionable_when_stopped": True,
            },
            health["stopped_owner_actionability_inputs"],
        )
        self.assertNotIn("delivery_status", health)
        self.assertNotIn("completion_ready", health)
        self.assertEqual(registry_before_status, self.registry_path().read_bytes())

    def test_second_independent_writer_gets_isolated_worktree(self) -> None:
        first = self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        isolated, isolated_path = self.isolated_arguments("second")
        second = self.claim(
            *self.acquire_arguments("second"),
            "--file",
            "src/one.py",
            *isolated,
        )

        self.assertEqual(0, first.returncode, first.stderr)
        self.assertEqual(0, second.returncode, second.stderr)
        result = self.output(second)
        self.assertEqual("ISOLATED_CHECKOUT_ACQUIRED", result["outcome"])
        self.assertEqual("ISOLATE", result["legacy_outcome"])
        self.assertEqual(str(isolated_path), result["target"]["worktree"])
        self.assertEqual("linked", result["claim"]["checkout_topology"])
        self.assertEqual("linked", result["target"]["checkout_topology"])
        self.assertTrue((isolated_path / ".git").is_file())
        self.assertTrue((isolated_path / "src" / "one.py").is_file())
        self.assertFalse((isolated_path / "backlog").exists())
        self.assertTrue((self.repository / "backlog" / "feature-backlog" / "queued.md").is_file())
        self.assertEqual("", self.git("status", "--porcelain").stdout)
        event = self.journal_events()[-1]
        self.assertEqual("linked", event["checkout_topology"])
        self.assertEqual("codex/second", event["worktree_id"])
        self.assertNotIn(str(self.temporary_directory.name), json.dumps(event))

    def test_existing_linked_checkout_with_active_peer_uses_canonical_isolation(self) -> None:
        linked_path = self.existing_linked_worktree()
        first = self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        isolated, isolated_path = self.isolated_arguments("second")
        primary_head = self.git("rev-parse", "HEAD").stdout
        primary_status = self.git("status", "--porcelain=v1").stdout
        linked_head = self.git("rev-parse", "HEAD", worktree=linked_path).stdout
        linked_status = self.git("status", "--porcelain=v1", worktree=linked_path).stdout

        second = self.claim(
            *self.acquire_arguments("second"),
            "--file",
            "src/one.py",
            *isolated,
            repo=linked_path,
        )

        self.assertEqual(0, first.returncode, first.stderr)
        self.assertEqual(0, second.returncode, second.stderr)
        result = self.output(second)
        self.assertEqual("ISOLATED_CHECKOUT_ACQUIRED", result["outcome"])
        self.assertEqual("ISOLATE", result["legacy_outcome"])
        self.assertEqual("isolated", result["claim"]["mode"])
        self.assertEqual("linked", result["claim"]["checkout_topology"])
        self.assertEqual(str(isolated_path), result["target"]["worktree"])
        self.assertEqual("linked", result["target"]["checkout_topology"])
        self.assertNotEqual(linked_path, isolated_path)
        self.assertEqual(primary_head, self.git("rev-parse", "HEAD").stdout)
        self.assertEqual(primary_status, self.git("status", "--porcelain=v1").stdout)
        self.assertEqual(linked_head, self.git("rev-parse", "HEAD", worktree=linked_path).stdout)
        self.assertEqual(linked_status, self.git("status", "--porcelain=v1", worktree=linked_path).stdout)
        event = self.journal_events()[-1]
        self.assertEqual("linked", event["checkout_topology"])
        self.assertEqual("codex/second", event["worktree_id"])
        self.assertNotIn(str(self.temporary_directory.name), json.dumps(event))

    def test_nonoverlapping_primary_claims_coexist_without_isolation(self) -> None:
        self.claim(*self.acquire_arguments("first"), "--file", "README.md")

        completed = self.claim(*self.acquire_arguments("second"), "--file", "src/one.py")

        self.assertEqual(0, completed.returncode, completed.stderr)
        result = self.output(completed)
        self.assertEqual("SHARED_CHECKOUT_ACQUIRED", result["outcome"])
        self.assertEqual("primary", result["claim"]["checkout_topology"])
        self.assertEqual(
            ["first", "second"],
            [claim["claim_id"] for claim in self.output(self.claim("status"))["claims"]],
        )

    def test_explicit_worktree_path_must_match_the_canonical_target(self) -> None:
        self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        outside_path = Path(self.temporary_directory.name) / "outside"

        completed = self.claim(
            *self.acquire_arguments("second"),
            "--file",
            "src/one.py",
            "--branch",
            "codex/second",
            "--worktree-path",
            str(outside_path),
        )

        self.assertEqual(1, completed.returncode)
        result = self.output(completed)
        self.assertEqual(2, result["schema_version"])
        self.assertEqual("INVALID_WORKTREE_PATH", result["outcome"])
        self.assertNotIn("legacy_outcome", result)
        self.assertEqual(
            str((self.repository / ".worktrees" / "second").resolve()),
            result["expected_worktree"],
        )
        self.assertFalse(outside_path.exists())

    def test_compatible_caller_may_supply_the_exact_canonical_worktree_path(self) -> None:
        self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        canonical_path = (self.repository / ".worktrees" / "second").resolve()

        completed = self.claim(
            *self.acquire_arguments("second"),
            "--file",
            "src/one.py",
            "--branch",
            "codex/second",
            "--worktree-path",
            str(canonical_path),
        )

        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertEqual(str(canonical_path), self.output(completed)["target"]["worktree"])

    def test_isolation_requires_the_canonical_root_to_be_ignored(self) -> None:
        (self.repository / ".gitignore").write_text("", encoding="utf-8")
        self.git("add", ".gitignore")
        self.git("commit", "-m", "remove worktree ignore")
        self.claim(*self.acquire_arguments("first"), "--file", "README.md")

        completed = self.claim(
            *self.acquire_arguments("second"),
            "--file",
            "src/one.py",
            "--branch",
            "codex/second",
        )

        self.assertEqual(1, completed.returncode)
        result = self.output(completed)
        self.assertEqual("WORKTREE_ROOT_NOT_IGNORED", result["outcome"])
        self.assertEqual("/.worktrees/", result["required_ignore_pattern"])
        self.assertFalse((self.repository / ".worktrees").exists())

    def test_claim_id_cannot_create_a_recursive_worktree_path(self) -> None:
        self.claim(*self.acquire_arguments("first"), "--file", "README.md")

        completed = self.claim(
            *self.acquire_arguments("../recursive"),
            "--file",
            "src/one.py",
            "--branch",
            "codex/recursive",
        )

        self.assertEqual(1, completed.returncode)
        result = self.output(completed)
        self.assertEqual("INVALID_IDENTIFIER", result["outcome"])
        self.assertEqual("claim_id", result["field"])
        self.assertFalse((self.repository / "recursive").exists())

    def test_exact_backlog_scope_coexists_with_nonoverlapping_primary_project_claim(self) -> None:
        self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        isolated, isolated_path = self.isolated_arguments("backlog")

        completed = self.claim(
            *self.acquire_arguments("backlog"),
            "--file",
            "backlog/feature-backlog/queued.md",
            *isolated,
        )

        self.assertEqual(0, completed.returncode, completed.stderr)
        result = self.output(completed)
        self.assertEqual("SHARED_CHECKOUT_ACQUIRED", result["outcome"])
        self.assertEqual("primary", result["claim"]["checkout_topology"])
        self.assertFalse(isolated_path.exists())

    def test_backlog_scope_uses_available_primary_while_isolated_claim_remains(self) -> None:
        self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        isolated, _isolated_path = self.isolated_arguments("second")
        self.claim(
            *self.acquire_arguments("second"),
            "--file",
            "src/one.py",
            *isolated,
        )
        released = self.claim("release", "--claim-id", "first", "--no-change")

        completed = self.claim(
            *self.acquire_arguments("backlog"),
            "--file",
            "backlog/feature-backlog/queued.md",
            *self.timed_resource_arguments(
                resource="git-index:primary",
                resource_class="main-integration",
            ),
        )

        self.assertEqual(0, released.returncode, released.stderr)
        self.assertEqual(0, completed.returncode, completed.stderr)
        result = self.output(completed)
        self.assertEqual("SHARED_CHECKOUT_ACQUIRED", result["outcome"])
        self.assertEqual(str(self.repository.resolve()), result["target"]["worktree"])

    def test_primary_integration_scope_uses_available_primary_while_isolated_claim_remains(self) -> None:
        self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        isolated, _isolated_path = self.isolated_arguments("isolated")
        self.claim(
            *self.acquire_arguments("isolated"),
            "--file",
            "src/one.py",
            *isolated,
        )
        self.claim("release", "--claim-id", "first", "--no-change")

        completed = self.claim(
            *self.acquire_arguments("integration"),
            "--file",
            "skills/codex-workitem-coordination/SKILL.md",
            "--file",
            "design/generated/skill-definitions.js",
            *self.timed_resource_arguments(
                resource="merge:integration:main",
                resource_class="main-integration",
            ),
        )

        self.assertEqual(0, completed.returncode, completed.stderr)
        result = self.output(completed)
        self.assertEqual("SHARED_CHECKOUT_ACQUIRED", result["outcome"])
        self.assertEqual(str(self.repository.resolve()), result["target"]["worktree"])

    def test_resource_only_claim_does_not_force_unrelated_file_claim_into_isolation(self) -> None:
        resource = self.claim(
            *self.acquire_arguments("resource"),
            *self.timed_resource_arguments(),
        )

        completed = self.claim(
            *self.acquire_arguments("file"),
            "--file",
            "src/one.py",
        )

        self.assertEqual(0, resource.returncode, resource.stderr)
        self.assertEqual(0, completed.returncode, completed.stderr)
        result = self.output(completed)
        self.assertEqual("SHARED_CHECKOUT_ACQUIRED", result["outcome"])
        self.assertEqual(str(self.repository.resolve()), result["target"]["worktree"])

    def test_primary_resource_only_claim_can_extend_into_a_nonoverlapping_file_scope(self) -> None:
        self.claim(*self.acquire_arguments("file"), "--file", "README.md")
        resource = self.claim(
            *self.acquire_arguments("resource"),
            *self.timed_resource_arguments(),
        )

        extended = self.claim(
            "extend",
            "--claim-id",
            "resource",
            "--file",
            "src/one.py",
        )

        self.assertEqual(0, resource.returncode, resource.stderr)
        self.assertEqual(0, extended.returncode, extended.stderr)
        result = self.output(extended)
        self.assertEqual("EXTENDED", result["outcome"])
        status = self.output(self.claim("status"))["claims"]
        stored = next(claim for claim in status if claim["claim_id"] == "resource")
        self.assertEqual("project_files", stored["file_domain"])
        self.assertEqual(["src/one.py"], stored["files"])

    def test_resource_only_claim_does_not_block_unrelated_primary_integration(self) -> None:
        resource = self.claim(
            *self.acquire_arguments("resource"),
            *self.timed_resource_arguments(),
        )

        completed = self.claim(
            *self.acquire_arguments("integration"),
            "--file",
            "skills/codex-workitem-coordination/SKILL.md",
            "--file",
            "design/generated/skill-definitions.js",
            *self.timed_resource_arguments(
                resource="merge:integration:main",
                resource_class="main-integration",
            ),
        )

        self.assertEqual(0, resource.returncode, resource.stderr)
        self.assertEqual(0, completed.returncode, completed.stderr)
        result = self.output(completed)
        self.assertEqual("SHARED_CHECKOUT_ACQUIRED", result["outcome"])
        self.assertEqual(str(self.repository.resolve()), result["target"]["worktree"])

    def test_resource_only_claim_ignores_unrelated_dirty_files(self) -> None:
        source_path = self.repository / "src" / "one.py"
        source_path.write_text("private worktree edit\n", encoding="utf-8")

        acquired = self.claim(
            *self.acquire_arguments("resource"),
            *self.timed_resource_arguments(),
        )
        source_path.write_text("continued private worktree edit\n", encoding="utf-8")
        released = self.claim("release", "--claim-id", "resource", "--no-change")

        self.assertEqual(0, acquired.returncode, acquired.stderr)
        self.assertEqual(0, released.returncode, released.stderr)
        self.assertEqual("RELEASED", self.output(released)["outcome"])
        self.assertEqual(
            "continued private worktree edit\n",
            source_path.read_text(encoding="utf-8"),
        )

    def test_private_resource_only_claim_does_not_serialize_file_or_integration_claims(self) -> None:
        self.claim(*self.acquire_arguments("primary-file"), "--file", "README.md")
        isolated_arguments, isolated_path = self.isolated_arguments("isolated-file")
        isolated = self.claim(
            *self.acquire_arguments("isolated-file"),
            "--file",
            "src/one.py",
            *isolated_arguments,
        )
        self.assertEqual(0, isolated.returncode, isolated.stderr)
        self.claim("release", "--claim-id", "isolated-file", "--no-change")

        resource = self.claim(
            *self.acquire_arguments("private-resource"),
            *self.timed_resource_arguments(resource="test:e2e"),
            repo=isolated_path,
        )
        self.assertEqual(0, resource.returncode, resource.stderr)
        self.assertEqual(
            isolated_path.resolve(),
            Path(self.output(resource)["target"]["worktree"]).resolve(),
        )
        self.claim("release", "--claim-id", "primary-file", "--no-change")

        integration = self.claim(
            *self.acquire_arguments("five-file-integration"),
            "--file",
            "README.md",
            "--file",
            "src/one.py",
            "--file",
            "docs/guide.md",
            "--file",
            "docs/future.md",
            "--file",
            "src/future.py",
            *self.timed_resource_arguments(
                resource="merge:integration:main",
                resource_class="main-integration",
            ),
        )

        self.assertEqual(0, integration.returncode, integration.stderr)
        result = self.output(integration)
        self.assertEqual("SHARED_CHECKOUT_ACQUIRED", result["outcome"])
        self.assertEqual(str(self.repository.resolve()), result["target"]["worktree"])
        self.assertFalse((self.repository / ".worktrees" / "five-file-integration").exists())

    def test_primary_git_index_resource_uses_available_primary_while_isolated_claim_remains(self) -> None:
        self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        isolated, _isolated_path = self.isolated_arguments("isolated")
        self.claim(
            *self.acquire_arguments("isolated"),
            "--file",
            "src/one.py",
            *isolated,
        )
        self.claim("release", "--claim-id", "first", "--no-change")

        completed = self.claim(
            *self.acquire_arguments("git-index"),
            *self.timed_resource_arguments(
                resource="git-index:primary",
                resource_class="main-integration",
            ),
        )

        self.assertEqual(0, completed.returncode, completed.stderr)
        result = self.output(completed)
        self.assertEqual("SHARED_CHECKOUT_ACQUIRED", result["outcome"])
        self.assertEqual(str(self.repository.resolve()), result["target"]["worktree"])

    def test_primary_integration_scope_waits_for_overlapping_isolated_claim(self) -> None:
        self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        isolated, _isolated_path = self.isolated_arguments("isolated")
        self.claim(
            *self.acquire_arguments("isolated"),
            "--file",
            "skills/codex-workitem-coordination/SKILL.md",
            *isolated,
        )
        self.claim("release", "--claim-id", "first", "--no-change")

        completed = self.claim(
            *self.acquire_arguments("integration"),
            "--file",
            "skills/codex-workitem-coordination/SKILL.md",
            "--file",
            "design/generated/skill-definitions.js",
            *self.timed_resource_arguments(
                resource="merge:integration:main",
                resource_class="main-integration",
            ),
        )

        self.assertEqual(3, completed.returncode)
        result = self.output(completed)
        self.assertEqual("CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED", result["outcome"])
        self.assertEqual("WAIT", result["legacy_outcome"])
        self.assertEqual(["isolated"], result["conflicting_claim_ids"])

    def test_primary_integration_scope_coexists_with_nonoverlapping_primary_owner(self) -> None:
        self.claim(*self.acquire_arguments("first"), "--file", "README.md")

        completed = self.claim(
            *self.acquire_arguments("integration"),
            "--file",
            "design/generated/skill-definitions.js",
            *self.timed_resource_arguments(
                resource="merge:integration:main",
                resource_class="main-integration",
            ),
        )

        self.assertEqual(0, completed.returncode, completed.stderr)
        result = self.output(completed)
        self.assertEqual("SHARED_CHECKOUT_ACQUIRED", result["outcome"])
        self.assertEqual("primary", result["claim"]["checkout_topology"])

    def test_primary_integration_scope_preserves_dirty_primary_recovery(self) -> None:
        self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        isolated, _isolated_path = self.isolated_arguments("isolated")
        self.claim(
            *self.acquire_arguments("isolated"),
            "--file",
            "src/one.py",
            *isolated,
        )
        self.claim("release", "--claim-id", "first", "--no-change")
        (self.repository / "docs" / "guide.md").write_text("dirty\n", encoding="utf-8")

        completed = self.claim(
            *self.acquire_arguments("integration"),
            "--file",
            "design/generated/skill-definitions.js",
            *self.timed_resource_arguments(
                resource="merge:integration:main",
                resource_class="main-integration",
            ),
        )

        self.assertEqual(5, completed.returncode)
        result = self.output(completed)
        self.assertEqual("DIRTY_CHECKOUT_RECOVERY_AUTHORIZATION_REQUIRED", result["outcome"])
        self.assertEqual("RECOVERY_REQUIRED", result["legacy_outcome"])
        self.assertEqual(
            [{"path": "docs/guide.md", "status": " M"}],
            result["dirty_status"],
        )

    def test_simultaneous_nonoverlapping_claims_can_both_use_primary(self) -> None:
        commands = [self.claim_command(*self.acquire_arguments(claim_id)) for claim_id in ("first", "second")]
        processes = [
            subprocess.Popen(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            for command in commands
        ]
        completed = [process.communicate() + (process.returncode,) for process in processes]
        outcomes = {json.loads(stdout)["outcome"] for stdout, _stderr, _code in completed}
        return_codes = sorted(code for _stdout, _stderr, code in completed)

        self.assertEqual([0, 0], return_codes)
        self.assertEqual({"SHARED_CHECKOUT_ACQUIRED"}, outcomes)

    def test_exact_files_do_not_use_ancestry_overlap(self) -> None:
        first = self.claim(*self.acquire_arguments("first"), "--file", "future")
        isolated, _isolated_path = self.isolated_arguments("second")
        second = self.claim(
            *self.acquire_arguments("second"),
            "--file",
            "future/child.py",
            *isolated,
        )

        self.assertEqual(0, first.returncode, first.stderr)
        self.assertEqual(0, second.returncode, second.stderr)
        self.assertEqual("ISOLATED_CHECKOUT_ACQUIRED", self.output(second)["outcome"])

    def test_tree_and_all_files_scopes_overlap_descendants(self) -> None:
        tree = self.claim(
            *self.acquire_arguments("tree"),
            "--tree",
            "src",
            "--scope-reason",
            "bounded source generation",
        )
        isolated, blocked_path = self.isolated_arguments("blocked")
        nested = self.claim(
            *self.acquire_arguments("blocked"),
            "--file",
            "src/one.py",
            *isolated,
        )

        self.assertEqual(0, tree.returncode, tree.stderr)
        self.assertEqual(3, nested.returncode)
        nested_result = self.output(nested)
        self.assertEqual("CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED", nested_result["outcome"])
        self.assertEqual("tree", nested_result["overlaps"][0]["claimed_kind"])
        self.assertFalse(blocked_path.exists())

        self.claim("release", "--claim-id", "tree", "--no-change")
        all_files = self.claim(
            *self.acquire_arguments("all"),
            "--all-files",
            "--scope-reason",
            "repository migration",
        )
        resource = self.claim(
            *self.acquire_arguments("other"),
            *self.timed_resource_arguments(),
        )
        exact = self.claim(*self.acquire_arguments("exact"), "--file", "docs/guide.md")
        self.assertEqual(0, all_files.returncode, all_files.stderr)
        self.assertEqual(0, resource.returncode, resource.stderr)
        self.assertEqual("SHARED_CHECKOUT_ACQUIRED", self.output(resource)["outcome"])
        self.assertEqual(3, exact.returncode)

    def test_project_files_and_backlog_are_separate_broad_domains(self) -> None:
        project = self.claim(
            *self.acquire_arguments("project"),
            "--project-files",
            "--scope-reason",
            "project delivery",
        )
        isolated, isolated_path = self.isolated_arguments("other-project")
        other_project = self.claim(
            *self.acquire_arguments("other-project"),
            "--file",
            "src/one.py",
            *isolated,
        )
        backlog = self.claim(
            *self.acquire_arguments("backlog"),
            "--file",
            "backlog/feature-backlog/queued.md",
        )

        self.assertEqual(0, project.returncode, project.stderr)
        self.assertEqual("project_files", self.output(project)["claim"]["file_domain"])
        self.assertEqual(3, other_project.returncode)
        self.assertFalse(isolated_path.exists())
        self.assertEqual(0, backlog.returncode, backlog.stderr)
        self.assertEqual("SHARED_CHECKOUT_ACQUIRED", self.output(backlog)["outcome"])
        self.assertEqual(
            ["project", "backlog"],
            [item["claim_id"] for item in self.output(self.claim("status"))["claims"]],
        )

    def test_different_exact_backlog_items_coexist(self) -> None:
        first = self.claim(
            *self.acquire_arguments("first-backlog"),
            "--file",
            "backlog/feature-backlog/queued.md",
        )
        second = self.claim(
            *self.acquire_arguments("second-backlog"),
            "--file",
            "backlog/feature-backlog/second.md",
        )

        self.assertEqual(0, first.returncode, first.stderr)
        self.assertEqual(0, second.returncode, second.stderr)
        self.assertEqual("SHARED_CHECKOUT_ACQUIRED", self.output(second)["outcome"])
        self.assertEqual(
            ["first-backlog", "second-backlog"],
            [item["claim_id"] for item in self.output(self.claim("status"))["claims"]],
        )

    def test_backlog_broad_scope_does_not_overlap_project_paths(self) -> None:
        backlog = self.claim(*self.acquire_arguments("backlog"), "--backlog")
        self.assertEqual(0, backlog.returncode, backlog.stderr)
        self.assertEqual("backlog", self.output(backlog)["claim"]["file_domain"])
        self.claim("release", "--claim-id", "backlog", "--no-change")

        project = self.claim(*self.acquire_arguments("project"), "--file", "src/one.py")
        self.assertEqual(0, project.returncode, project.stderr)

    def test_mixed_project_and_backlog_paths_are_rejected_atomically(self) -> None:
        completed = self.claim(
            *self.acquire_arguments("mixed"),
            "--file",
            "src/one.py",
            "--file",
            "backlog/feature-backlog/queued.md",
        )

        self.assertEqual(1, completed.returncode)
        result = self.output(completed)
        self.assertEqual("INVALID_SCOPE", result["outcome"])
        self.assertEqual("mixed_file_domains", result["rejection"]["reason"])
        self.assertEqual([], self.output(self.claim("status"))["claims"])

    def test_broad_file_domains_are_mutually_exclusive(self) -> None:
        for index, arguments in enumerate(
            (
                ("--project-files", "--backlog"),
                ("--project-files", "--all-files"),
                ("--backlog", "--all-files"),
            )
        ):
            with self.subTest(arguments=arguments):
                completed = self.claim(
                    *self.acquire_arguments(f"mixed-{index}"),
                    *arguments,
                    "--scope-reason",
                    "invalid broad combination",
                )
                self.assertEqual(1, completed.returncode)
                self.assertEqual("INVALID_SCOPE", self.output(completed)["outcome"])

    def test_compatibility_backlog_file_uses_backlog_domain_and_primary_rules(self) -> None:
        self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        completed = self.claim(
            *self.acquire_arguments("backlog"),
            "--file",
            "backlog/feature-backlog/queued.md",
        )

        self.assertEqual(0, completed.returncode, completed.stderr)
        result = self.output(completed)
        self.assertEqual("SHARED_CHECKOUT_ACQUIRED", result["outcome"])
        self.assertEqual("backlog", result["claim"]["file_domain"])
        self.assertEqual("compat_backlog_path", result["warnings"][0]["code"])

    def test_project_claim_ignores_unchanged_preexisting_backlog_dirtiness(self) -> None:
        backlog_path = self.repository / "backlog" / "feature-backlog" / "queued.md"
        backlog_path.write_text("preexisting\n", encoding="utf-8")

        acquired = self.claim(*self.acquire_arguments("project"), "--project-files", "--scope-reason", "project work")
        released = self.claim("release", "--claim-id", "project", "--no-change")

        self.assertEqual(0, acquired.returncode, acquired.stderr)
        self.assertEqual("SHARED_CHECKOUT_ACQUIRED", self.output(acquired)["outcome"])
        self.assertEqual(0, released.returncode, released.stderr)

    def test_project_claim_detects_content_change_to_preexisting_dirty_backlog_path(self) -> None:
        backlog_path = self.repository / "backlog" / "feature-backlog" / "queued.md"
        backlog_path.write_text("preexisting\n", encoding="utf-8")
        acquired = self.claim(
            *self.acquire_arguments("project"),
            "--project-files",
            "--scope-reason",
            "project work",
        )
        backlog_path.write_text("changed again\n", encoding="utf-8")

        released = self.claim("release", "--claim-id", "project", "--no-change")

        self.assertEqual(0, acquired.returncode, acquired.stderr)
        self.assertEqual(1, released.returncode)
        self.assertEqual("out_of_domain_changes", self.output(released)["reason"])

    def test_nul_status_tracks_special_backlog_paths_and_reports_only_changed_entries(self) -> None:
        changed_path = self.repository / "backlog" / "feature-backlog" / 'quoted " café space.md'
        unchanged_path = self.repository / "backlog" / "feature-backlog" / "line\nbreak.md"
        arrow_path = self.repository / "backlog" / "feature-backlog" / "before -> after.md"
        changed_path.write_text("before\n", encoding="utf-8")
        unchanged_path.write_text("unchanged\n", encoding="utf-8")
        arrow_path.write_text("unchanged\n", encoding="utf-8")
        acquired = self.claim(
            *self.acquire_arguments("project"),
            "--project-files",
            "--scope-reason",
            "project work",
        )
        changed_path.write_text("after\n", encoding="utf-8")

        released = self.claim("release", "--claim-id", "project", "--no-change")

        self.assertEqual(0, acquired.returncode, acquired.stderr)
        self.assertEqual(1, released.returncode)
        self.assertEqual(
            ['backlog/feature-backlog/quoted " café space.md'],
            self.output(released)["out_of_domain_paths"],
        )

    def test_nul_status_preserves_unchanged_backlog_rename_records(self) -> None:
        renamed_path = "backlog/feature-backlog/renamed café item.md"
        self.git("mv", "backlog/feature-backlog/queued.md", renamed_path)
        acquired = self.claim(
            *self.acquire_arguments("project"),
            "--project-files",
            "--scope-reason",
            "project work",
        )

        released = self.claim("release", "--claim-id", "project", "--no-change")

        self.assertEqual(0, acquired.returncode, acquired.stderr)
        self.assertEqual(0, released.returncode, released.stderr)

    def test_project_claim_release_rejects_new_backlog_change(self) -> None:
        acquired = self.claim(*self.acquire_arguments("project"), "--project-files", "--scope-reason", "project work")
        self.assertEqual(0, acquired.returncode, acquired.stderr)
        backlog_path = self.repository / "backlog" / "feature-backlog" / "queued.md"
        backlog_path.write_text("changed\n", encoding="utf-8")

        released = self.claim("release", "--claim-id", "project", "--no-change")

        self.assertEqual(1, released.returncode)
        result = self.output(released)
        self.assertEqual("out_of_domain_changes", result["reason"])
        self.assertEqual(["backlog/feature-backlog/queued.md"], result["out_of_domain_paths"])

    def test_project_claim_release_does_not_audit_committed_backlog_history(self) -> None:
        acquired = self.claim(*self.acquire_arguments("project"), "--project-files", "--scope-reason", "project work")
        self.assertEqual(0, acquired.returncode, acquired.stderr)
        backlog_path = self.repository / "backlog" / "feature-backlog" / "queued.md"
        backlog_path.write_text("committed\n", encoding="utf-8")
        self.git("add", str(backlog_path))
        self.git("commit", "-m", "review-owned scope decision")

        released = self.claim("release", "--claim-id", "project")

        self.assertEqual(0, released.returncode, released.stderr)
        self.assertEqual("RELEASED", self.output(released)["outcome"])

    def test_release_reconciles_exact_peer_commit_after_dirty_out_of_domain_baseline(self) -> None:
        fixture = self.release_reconciliation_fixture()
        auxiliary = self.claim(
            *self.acquire_arguments("auxiliary"),
            *self.timed_resource_arguments(),
        )
        self.assertEqual(0, auxiliary.returncode, auxiliary.stderr)

        released = self.claim(
            "release",
            "--claim-id",
            "project",
            "--reconcile-out-of-domain-commit",
            fixture["peer_commit"],
            "--prior-rejected-release-reference",
            fixture["prior_rejected_release_reference"],
        )

        self.assertEqual(0, released.returncode, released.stderr)
        result = self.output(released)
        self.assertEqual("RELEASED", result["outcome"])
        self.assertEqual(
            ["auxiliary"],
            [
                claim["claim_id"]
                for claim in self.output(self.claim("status"))["claims"]
            ],
        )
        evidence = result["reconciliation"]
        self.assertEqual(fixture["baseline_commit"], evidence["baseline_commit"])
        self.assertEqual(fixture["peer_commit"], evidence["peer_commit"])
        self.assertEqual(
            ["backlog/feature-backlog/queued.md"],
            evidence["reconciled_out_of_domain_paths"],
        )
        self.assertEqual(
            fixture["prior_rejected_release_reference"],
            evidence["prior_rejected_release_reference"],
        )
        self.assertEqual(
            {
                "backlog/feature-backlog/queued.md": hashlib.sha256(
                    b"pre-existing peer work\n"
                ).hexdigest()
            },
            evidence["peer_commit_content_sha256"],
        )
        event = self.journal_events()[-1]
        self.assertEqual("RELEASED", event["outcome"])
        self.assertEqual(fixture["head_commit"], event["resulting_commit"])
        self.assertEqual(evidence, event["reconciliation"])
        self.assertEqual(
            [{"path": "backlog/feature-backlog/queued.md", "status": " M"}],
            evidence["baseline_out_of_domain_status"],
        )
        baseline_state = evidence["baseline_out_of_domain_state"]
        self.assertEqual(
            ["backlog/feature-backlog/queued.md"],
            sorted(baseline_state),
        )
        self.assertEqual(" M", baseline_state["backlog/feature-backlog/queued.md"]["status"])
        self.assertTrue(
            baseline_state["backlog/feature-backlog/queued.md"]["index_entry"].startswith("100644 ")
        )
        self.assertEqual(
            64,
            len(baseline_state["backlog/feature-backlog/queued.md"]["worktree_sha256"]),
        )

    def test_release_reconciliation_requires_full_sha_exclusive_mode_and_prior_evidence(self) -> None:
        fixture = self.release_reconciliation_fixture()
        registry_bytes = self.registry_path().read_bytes()

        abbreviated = self.claim(
            "release",
            "--claim-id",
            "project",
            "--reconcile-out-of-domain-commit",
            fixture["peer_commit"][:8],
            "--prior-rejected-release-reference",
            fixture["prior_rejected_release_reference"],
        )
        self.assertEqual(2, abbreviated.returncode)
        self.assertEqual(registry_bytes, self.registry_path().read_bytes())

        mutually_exclusive = self.claim(
            "release",
            "--claim-id",
            "project",
            "--no-change",
            "--reconcile-out-of-domain-commit",
            fixture["peer_commit"],
            "--prior-rejected-release-reference",
            fixture["prior_rejected_release_reference"],
        )
        self.assertEqual(2, mutually_exclusive.returncode)
        self.assertEqual(registry_bytes, self.registry_path().read_bytes())

        missing_prior_evidence = self.claim(
            "release",
            "--claim-id",
            "project",
            "--reconcile-out-of-domain-commit",
            fixture["peer_commit"],
        )
        self.assertEqual(1, missing_prior_evidence.returncode)
        self.assertEqual(
            "reconciliation_prior_rejection_required",
            self.output(missing_prior_evidence)["reason"],
        )
        self.assertEqual(registry_bytes, self.registry_path().read_bytes())

        wrong_prior_evidence = self.claim(
            "release",
            "--claim-id",
            "project",
            "--reconcile-out-of-domain-commit",
            fixture["peer_commit"],
            "--prior-rejected-release-reference",
            self.journal_events()[0]["event_id"],
        )
        self.assertEqual(1, wrong_prior_evidence.returncode)
        self.assertEqual(
            "reconciliation_prior_rejection_mismatch",
            self.output(wrong_prior_evidence)["reason"],
        )
        self.assertEqual(registry_bytes, self.registry_path().read_bytes())

        reference_without_commit = self.claim(
            "release",
            "--claim-id",
            "project",
            "--prior-rejected-release-reference",
            fixture["prior_rejected_release_reference"],
        )
        self.assertEqual(1, reference_without_commit.returncode)
        self.assertEqual(
            "prior_rejection_requires_reconciliation_commit",
            self.output(reference_without_commit)["reason"],
        )
        self.assertEqual(registry_bytes, self.registry_path().read_bytes())

        for mode in ((), ("--no-change",)):
            with self.subTest(mode=mode):
                rejected = self.claim("release", "--claim-id", "project", *mode)
                self.assertEqual(1, rejected.returncode)
                self.assertEqual("out_of_domain_changes", self.output(rejected)["reason"])
                self.assertEqual(registry_bytes, self.registry_path().read_bytes())

    def test_release_reconciliation_rejects_wrong_and_nonancestor_commits_without_registry_change(self) -> None:
        fixture = self.release_reconciliation_fixture()
        registry_bytes = self.registry_path().read_bytes()
        original_branch = self.git("branch", "--show-current").stdout.strip()

        wrong_commits = (
            (fixture["baseline_commit"], "reconciliation_commit_not_after_baseline"),
            ("f" * 40, "reconciliation_commit_not_found"),
        )
        for commit, reason in wrong_commits:
            with self.subTest(reason=reason):
                rejected = self.claim(
                    "release",
                    "--claim-id",
                    "project",
                    "--reconcile-out-of-domain-commit",
                    commit,
                    "--prior-rejected-release-reference",
                    fixture["prior_rejected_release_reference"],
                )
                self.assertEqual(1, rejected.returncode)
                self.assertEqual(reason, self.output(rejected)["reason"])
                self.assertEqual(registry_bytes, self.registry_path().read_bytes())

        self.git("checkout", "-b", "unrelated-peer", fixture["baseline_commit"])
        (self.repository / "backlog" / "feature-backlog" / "queued.md").write_text(
            "unrelated peer work\n",
            encoding="utf-8",
        )
        self.git("add", "backlog/feature-backlog/queued.md")
        self.git("commit", "-m", "unrelated peer commit")
        unrelated_commit = self.git("rev-parse", "HEAD").stdout.strip()
        self.git("checkout", original_branch)

        nonancestor = self.claim(
            "release",
            "--claim-id",
            "project",
            "--reconcile-out-of-domain-commit",
            unrelated_commit,
            "--prior-rejected-release-reference",
            fixture["prior_rejected_release_reference"],
        )
        self.assertEqual(1, nonancestor.returncode)
        self.assertEqual(
            "reconciliation_commit_not_ancestor_of_head",
            self.output(nonancestor)["reason"],
        )
        self.assertEqual(registry_bytes, self.registry_path().read_bytes())

    def test_release_reconciliation_rejects_nonprimary_claim(self) -> None:
        (self.repository / "README.md").write_text("recovery work\n", encoding="utf-8")
        acquired = self.claim(
            *self.acquire_arguments("recovery"),
            "--all-files",
            "--scope-reason",
            "preserve recovery state",
            "--allow-recovery",
        )
        self.assertEqual(0, acquired.returncode, acquired.stderr)
        baseline_commit = self.output(acquired)["claim"]["baseline_commit"]
        self.git("add", "README.md")
        self.git("commit", "-m", "recovery checkpoint")
        checkpoint = self.git("rev-parse", "HEAD").stdout.strip()
        self.assertNotEqual(baseline_commit, checkpoint)
        registry_bytes = self.registry_path().read_bytes()

        reconciled = self.claim(
            "release",
            "--claim-id",
            "recovery",
            "--reconcile-out-of-domain-commit",
            checkpoint,
            "--prior-rejected-release-reference",
            "00000000-0000-0000-0000-000000000000",
        )

        self.assertEqual(1, reconciled.returncode)
        self.assertEqual(
            "reconciliation_requires_primary_scoped_claim",
            self.output(reconciled)["reason"],
        )
        self.assertEqual(registry_bytes, self.registry_path().read_bytes())

    def test_release_reconciliation_rejects_peer_commit_with_claimed_domain_path(self) -> None:
        backlog_path = self.repository / "backlog" / "feature-backlog" / "queued.md"
        backlog_path.write_text("pre-existing peer work\n", encoding="utf-8")
        acquired = self.claim(
            *self.acquire_arguments("project"),
            "--project-files",
            "--scope-reason",
            "project work",
        )
        self.assertEqual(0, acquired.returncode, acquired.stderr)
        backlog_path.write_text("peer backlog work\n", encoding="utf-8")
        (self.repository / "src" / "one.py").write_text("mixed peer work\n", encoding="utf-8")
        self.git("add", "backlog/feature-backlog/queued.md", "src/one.py")
        self.git("commit", "-m", "mixed peer commit")
        peer_commit = self.git("rev-parse", "HEAD").stdout.strip()
        (self.repository / "docs" / "guide.md").write_text("claimed work\n", encoding="utf-8")
        self.git("add", "docs/guide.md")
        self.git("commit", "-m", "complete claimed work")
        rejected_release = self.claim("release", "--claim-id", "project")
        prior_reference = self.output(rejected_release)["journal"]["event_id"]
        registry_bytes = self.registry_path().read_bytes()

        reconciled = self.claim(
            "release",
            "--claim-id",
            "project",
            "--reconcile-out-of-domain-commit",
            peer_commit,
            "--prior-rejected-release-reference",
            prior_reference,
        )

        self.assertEqual(1, reconciled.returncode)
        result = self.output(reconciled)
        self.assertEqual("reconciliation_commit_changed_claimed_domain", result["reason"])
        self.assertEqual(["src/one.py"], result["claimed_domain_paths"])
        self.assertEqual(registry_bytes, self.registry_path().read_bytes())

    def test_release_reconciliation_rejects_dirty_claimed_and_out_of_domain_state(self) -> None:
        fixture = self.release_reconciliation_fixture()
        registry_bytes = self.registry_path().read_bytes()
        (self.repository / "src" / "one.py").write_text("dirty claimed work\n", encoding="utf-8")

        dirty_claimed = self.claim(
            "release",
            "--claim-id",
            "project",
            "--reconcile-out-of-domain-commit",
            fixture["peer_commit"],
            "--prior-rejected-release-reference",
            fixture["prior_rejected_release_reference"],
        )

        self.assertEqual(1, dirty_claimed.returncode)
        self.assertEqual("worktree_not_clean", self.output(dirty_claimed)["reason"])
        self.assertEqual(registry_bytes, self.registry_path().read_bytes())
        self.git("restore", "src/one.py")
        (self.repository / "backlog" / "feature-backlog" / "queued.md").write_text(
            "dirty current peer work\n",
            encoding="utf-8",
        )

        dirty_outside = self.claim(
            "release",
            "--claim-id",
            "project",
            "--reconcile-out-of-domain-commit",
            fixture["peer_commit"],
            "--prior-rejected-release-reference",
            fixture["prior_rejected_release_reference"],
        )

        self.assertEqual(1, dirty_outside.returncode)
        self.assertEqual(
            "reconciliation_out_of_domain_not_clean",
            self.output(dirty_outside)["reason"],
        )
        self.assertEqual(registry_bytes, self.registry_path().read_bytes())

    def test_release_reconciliation_rejects_claim_with_resource(self) -> None:
        backlog_path = self.repository / "backlog" / "feature-backlog" / "queued.md"
        backlog_path.write_text("pre-existing peer work\n", encoding="utf-8")
        acquired = self.claim(
            *self.acquire_arguments("project"),
            "--project-files",
            "--scope-reason",
            "project work",
            *self.timed_resource_arguments(),
        )
        self.assertEqual(0, acquired.returncode, acquired.stderr)
        self.git("add", "backlog/feature-backlog/queued.md")
        self.git("commit", "-m", "preserve peer backlog work")
        peer_commit = self.git("rev-parse", "HEAD").stdout.strip()
        (self.repository / "src" / "one.py").write_text("claimed work\n", encoding="utf-8")
        self.git("add", "src/one.py")
        self.git("commit", "-m", "complete claimed work")
        rejected_release = self.claim("release", "--claim-id", "project")
        prior_reference = self.output(rejected_release)["journal"]["event_id"]
        registry_bytes = self.registry_path().read_bytes()

        reconciled = self.claim(
            "release",
            "--claim-id",
            "project",
            "--reconcile-out-of-domain-commit",
            peer_commit,
            "--prior-rejected-release-reference",
            prior_reference,
        )

        self.assertEqual(1, reconciled.returncode)
        self.assertEqual("reconciliation_resources_present", self.output(reconciled)["reason"])
        self.assertEqual(registry_bytes, self.registry_path().read_bytes())

    def test_release_reconciliation_requires_exact_peer_paths(self) -> None:
        fixture = self.release_reconciliation_fixture()
        registry_bytes = self.registry_path().read_bytes()
        extra_path = self.repository / "backlog" / "feature-backlog" / "extra.md"
        extra_path.write_text("extra committed peer work\n", encoding="utf-8")
        self.git("add", "backlog/feature-backlog/extra.md")
        self.git("commit", "-m", "unrelated later peer path")
        wrong_paths_commit = self.git("rev-parse", "HEAD").stdout.strip()

        wrong_paths = self.claim(
            "release",
            "--claim-id",
            "project",
            "--reconcile-out-of-domain-commit",
            wrong_paths_commit,
            "--prior-rejected-release-reference",
            fixture["prior_rejected_release_reference"],
        )

        self.assertEqual(1, wrong_paths.returncode)
        self.assertEqual("reconciliation_commit_paths_mismatch", self.output(wrong_paths)["reason"])
        self.assertEqual(registry_bytes, self.registry_path().read_bytes())

    def test_release_reconciliation_allows_later_descendant_change_to_reconciled_path(
        self,
    ) -> None:
        fixture = self.release_reconciliation_fixture()
        queued_path = self.repository / "backlog" / "feature-backlog" / "queued.md"
        queued_path.write_text("later committed peer value\n", encoding="utf-8")
        self.git("add", "backlog/feature-backlog/queued.md")
        self.git("commit", "-m", "change reconciled path after peer")
        descendant_commit = self.git("rev-parse", "HEAD").stdout.strip()

        released = self.claim(
            "release",
            "--claim-id",
            "project",
            "--reconcile-out-of-domain-commit",
            fixture["peer_commit"],
            "--prior-rejected-release-reference",
            fixture["prior_rejected_release_reference"],
        )

        self.assertEqual(0, released.returncode, released.stderr)
        result = self.output(released)
        self.assertEqual("RELEASED", result["outcome"])
        self.assertEqual(descendant_commit, self.journal_events()[-1]["resulting_commit"])
        self.assertEqual(
            fixture["peer_commit"],
            result["reconciliation"]["peer_commit"],
        )
        self.assertEqual(
            ["backlog/feature-backlog/queued.md"],
            result["reconciliation"]["reconciled_out_of_domain_paths"],
        )
        self.assertEqual([], self.output(self.claim("status"))["claims"])

    def test_release_reconciliation_requires_peer_content_to_match_acquisition_snapshot(
        self,
    ) -> None:
        backlog_path = self.repository / "backlog" / "feature-backlog" / "queued.md"
        backlog_path.write_text("acquisition-time peer work\n", encoding="utf-8")
        acquired = self.claim(
            *self.acquire_arguments("project"),
            "--project-files",
            "--scope-reason",
            "project work",
        )
        self.assertEqual(0, acquired.returncode, acquired.stderr)
        backlog_path.write_text("different committed peer work\n", encoding="utf-8")
        self.git("add", "backlog/feature-backlog/queued.md")
        self.git("commit", "-m", "commit different peer content")
        peer_commit = self.git("rev-parse", "HEAD").stdout.strip()
        (self.repository / "src" / "one.py").write_text("claimed work\n", encoding="utf-8")
        self.git("add", "src/one.py")
        self.git("commit", "-m", "complete claimed project work")
        rejected_release = self.claim("release", "--claim-id", "project")
        prior_reference = self.output(rejected_release)["journal"]["event_id"]
        registry_bytes = self.registry_path().read_bytes()

        reconciled = self.claim(
            "release",
            "--claim-id",
            "project",
            "--reconcile-out-of-domain-commit",
            peer_commit,
            "--prior-rejected-release-reference",
            prior_reference,
        )

        self.assertEqual(1, reconciled.returncode)
        result = self.output(reconciled)
        self.assertEqual("reconciliation_commit_content_mismatch", result["reason"])
        self.assertEqual(
            ["backlog/feature-backlog/queued.md"],
            [mismatch["path"] for mismatch in result["content_mismatches"]],
        )
        self.assertEqual(registry_bytes, self.registry_path().read_bytes())

    def test_release_reconciliation_rejects_missing_acquisition_content_evidence(
        self,
    ) -> None:
        fixture = self.release_reconciliation_fixture()
        registry = json.loads(self.registry_path().read_text(encoding="utf-8"))
        del registry["claims"][0]["baseline_out_of_domain_state"][
            "backlog/feature-backlog/queued.md"
        ]["worktree_sha256"]
        self.registry_path().write_text(json.dumps(registry), encoding="utf-8")
        registry_bytes = self.registry_path().read_bytes()

        reconciled = self.claim(
            "release",
            "--claim-id",
            "project",
            "--reconcile-out-of-domain-commit",
            fixture["peer_commit"],
            "--prior-rejected-release-reference",
            fixture["prior_rejected_release_reference"],
        )

        self.assertEqual(1, reconciled.returncode)
        result = self.output(reconciled)
        self.assertEqual("reconciliation_baseline_content_invalid", result["reason"])
        self.assertEqual(
            ["backlog/feature-backlog/queued.md"],
            result["invalid_baseline_content_paths"],
        )
        self.assertEqual(registry_bytes, self.registry_path().read_bytes())

    def test_release_reconciliation_rejects_stale_prior_event_from_reused_claim_identity(self) -> None:
        backlog_path = self.repository / "backlog" / "feature-backlog" / "queued.md"
        backlog_path.write_text("pre-existing peer work\n", encoding="utf-8")
        acquired = self.claim(
            *self.acquire_arguments("project"),
            "--project-files",
            "--scope-reason",
            "project work",
            environment={"AGENT_CLAIM_TEST_NOW": "2026-07-25T12:00:00Z"},
        )
        self.assertEqual(0, acquired.returncode, acquired.stderr)
        baseline_commit = self.output(acquired)["claim"]["baseline_commit"]
        original_branch = self.git("branch", "--show-current").stdout.strip()

        self.git("add", "backlog/feature-backlog/queued.md")
        self.git("commit", "-m", "preserve peer backlog work")
        peer_commit = self.git("rev-parse", "HEAD").stdout.strip()
        (self.repository / "src" / "one.py").write_text("claimed work\n", encoding="utf-8")
        self.git("add", "src/one.py")
        self.git("commit", "-m", "complete claimed project work")
        claimed_head = self.git("rev-parse", "HEAD").stdout.strip()
        old_rejection = self.claim(
            "release",
            "--claim-id",
            "project",
            environment={"AGENT_CLAIM_TEST_NOW": "2026-07-25T12:01:00Z"},
        )
        old_reference = self.output(old_rejection)["journal"]["event_id"]
        old_release = self.claim(
            "release",
            "--claim-id",
            "project",
            "--reconcile-out-of-domain-commit",
            peer_commit,
            "--prior-rejected-release-reference",
            old_reference,
            environment={"AGENT_CLAIM_TEST_NOW": "2026-07-25T12:02:00Z"},
        )
        self.assertEqual(0, old_release.returncode, old_release.stderr)

        self.git("checkout", "--detach", baseline_commit)
        self.git("branch", "-f", original_branch, baseline_commit)
        self.git("checkout", original_branch)
        backlog_path.write_text("pre-existing peer work\n", encoding="utf-8")
        reacquired = self.claim(
            *self.acquire_arguments("project"),
            "--project-files",
            "--scope-reason",
            "project work",
            environment={"AGENT_CLAIM_TEST_NOW": "2026-07-25T11:00:00Z"},
        )
        self.assertEqual(0, reacquired.returncode, reacquired.stderr)
        self.assertEqual(baseline_commit, self.output(reacquired)["claim"]["baseline_commit"])
        self.git("restore", "backlog/feature-backlog/queued.md")
        self.git("merge", "--ff-only", peer_commit)
        self.git("merge", "--ff-only", claimed_head)
        self.downgrade_claim_incarnations_to_legacy_fixture()
        registry_bytes = self.registry_path().read_bytes()

        stale_reconciliation = self.claim(
            "release",
            "--claim-id",
            "project",
            "--reconcile-out-of-domain-commit",
            peer_commit,
            "--prior-rejected-release-reference",
            old_reference,
            environment={"AGENT_CLAIM_TEST_NOW": "2026-07-25T10:00:00Z"},
        )

        self.assertEqual(1, stale_reconciliation.returncode)
        self.assertEqual(
            "reconciliation_legacy_incarnation_mismatch",
            self.output(stale_reconciliation)["reason"],
        )
        self.assertEqual(registry_bytes, self.registry_path().read_bytes())
        self.assertEqual(
            ["project"],
            [claim["claim_id"] for claim in self.output(self.claim("status"))["claims"]],
        )

    def test_release_reconciliation_resolves_one_legacy_acquisition_event_identity(self) -> None:
        fixture = self.release_reconciliation_fixture()
        acquisition_event_id = self.journal_events()[0]["event_id"]
        self.downgrade_claim_incarnations_to_legacy_fixture()

        released = self.claim(
            "release",
            "--claim-id",
            "project",
            "--reconcile-out-of-domain-commit",
            fixture["peer_commit"],
            "--prior-rejected-release-reference",
            fixture["prior_rejected_release_reference"],
        )

        self.assertEqual(0, released.returncode, released.stderr)
        evidence = self.output(released)["reconciliation"]["claim_incarnation"]
        self.assertEqual(
            {
                "id": acquisition_event_id,
                "source": "legacy_acquisition_event",
            },
            evidence,
        )
        self.assertEqual(
            acquisition_event_id,
            self.journal_events()[-1]["incarnation_id"],
        )

    def test_release_reconciliation_carries_legacy_lifecycle_across_hot_utc_midnight(
        self,
    ) -> None:
        fixture = self.release_reconciliation_fixture()
        self.downgrade_claim_incarnations_to_legacy_fixture()
        events = self.journal_events()
        acquisition = dict(events[0], timestamp="2026-07-24T23:59:59.000000Z")
        later_events = [
            dict(event, timestamp="2026-07-25T00:00:00.000000Z")
            for event in events[1:]
        ]
        for path in self.hot_directory().glob("*.jsonl"):
            path.unlink()
        self.write_daily_events("2026-07-24", [acquisition])
        self.write_daily_events("2026-07-25", later_events)

        released = self.claim(
            "release",
            "--claim-id",
            "project",
            "--reconcile-out-of-domain-commit",
            fixture["peer_commit"],
            "--prior-rejected-release-reference",
            fixture["prior_rejected_release_reference"],
            environment={"AGENT_CLAIM_TEST_NOW": "2026-07-25T00:00:01Z"},
        )

        self.assertEqual(0, released.returncode, released.stderr)
        self.assertEqual(
            acquisition["event_id"],
            self.output(released)["reconciliation"]["claim_incarnation"]["id"],
        )

    def test_release_reconciliation_carries_legacy_lifecycle_from_archive_to_hot(
        self,
    ) -> None:
        fixture = self.release_reconciliation_fixture()
        self.downgrade_claim_incarnations_to_legacy_fixture()
        events = self.journal_events()
        acquisition = dict(events[0], timestamp="2026-07-24T23:59:59.000000Z")
        later_events = [
            dict(event, timestamp="2026-07-25T00:00:00.000000Z")
            for event in events[1:]
        ]
        for path in self.hot_directory().glob("*.jsonl"):
            path.unlink()
        self.write_daily_events("2026-07-25", later_events)
        archive_path = (
            self.common_directory()
            / "agent-claim-events"
            / "archive"
            / "2026"
            / "07"
            / "2026-07-24.jsonl.gz"
        )
        archive_path.parent.mkdir(parents=True)
        archive_path.write_bytes(
            gzip.compress(
                (
                    json.dumps(acquisition, sort_keys=True, separators=(",", ":"))
                    + "\n"
                ).encode("utf-8"),
                mtime=0,
            )
        )

        released = self.claim(
            "release",
            "--claim-id",
            "project",
            "--reconcile-out-of-domain-commit",
            fixture["peer_commit"],
            "--prior-rejected-release-reference",
            fixture["prior_rejected_release_reference"],
            environment={"AGENT_CLAIM_TEST_NOW": "2026-07-25T00:00:01Z"},
        )

        self.assertEqual(0, released.returncode, released.stderr)
        self.assertEqual(
            acquisition["event_id"],
            self.output(released)["reconciliation"]["claim_incarnation"]["id"],
        )

    def test_release_reconciliation_rejects_ambiguous_legacy_acquisition_sequence(self) -> None:
        fixture = self.release_reconciliation_fixture()
        self.downgrade_claim_incarnations_to_legacy_fixture()
        journal_path = next(self.hot_directory().glob("*.jsonl"))
        events = [
            json.loads(line)
            for line in journal_path.read_text(encoding="utf-8").splitlines()
        ]
        events.insert(1, dict(events[0]))
        journal_path.write_text(
            "".join(
                json.dumps(event, sort_keys=True, separators=(",", ":")) + "\n"
                for event in events
            ),
            encoding="utf-8",
        )
        registry_bytes = self.registry_path().read_bytes()

        released = self.claim(
            "release",
            "--claim-id",
            "project",
            "--reconcile-out-of-domain-commit",
            fixture["peer_commit"],
            "--prior-rejected-release-reference",
            fixture["prior_rejected_release_reference"],
        )

        self.assertEqual(1, released.returncode)
        self.assertEqual(
            "reconciliation_legacy_duplicate_event_id",
            self.output(released)["reason"],
        )
        self.assertEqual(registry_bytes, self.registry_path().read_bytes())

    def test_release_reconciliation_rejects_reused_legacy_event_id_across_lifecycles(
        self,
    ) -> None:
        fixture = self.release_reconciliation_fixture()
        self.downgrade_claim_incarnations_to_legacy_fixture()
        events = self.journal_events()
        acquisition = events[0]
        rejection = events[-1]
        released = self.synthetic_event(
            "old-release",
            "2026-07-25T12:01:00Z",
            "release",
            "RELEASED",
            "project",
        )
        for path in self.hot_directory().glob("*.jsonl"):
            path.unlink()
        self.write_daily_events(
            "2026-07-24",
            [
                dict(acquisition, timestamp="2026-07-25T12:00:00Z"),
                released,
            ],
        )
        self.write_daily_events(
            "2026-07-25",
            [
                dict(acquisition, timestamp="2026-07-25T12:00:00Z"),
                dict(rejection, timestamp="2026-07-25T10:00:00Z"),
            ],
        )
        registry_bytes = self.registry_path().read_bytes()

        completed = self.claim(
            "release",
            "--claim-id",
            "project",
            "--reconcile-out-of-domain-commit",
            fixture["peer_commit"],
            "--prior-rejected-release-reference",
            fixture["prior_rejected_release_reference"],
        )

        self.assertEqual(1, completed.returncode)
        self.assertEqual(
            "reconciliation_legacy_duplicate_event_id",
            self.output(completed)["reason"],
        )
        self.assertEqual(registry_bytes, self.registry_path().read_bytes())

    def test_release_reconciliation_rejects_invalid_utf8_legacy_journal_structurally(
        self,
    ) -> None:
        fixture = self.release_reconciliation_fixture()
        self.downgrade_claim_incarnations_to_legacy_fixture()
        journal_path = next(self.hot_directory().glob("*.jsonl"))
        journal_path.write_bytes(journal_path.read_bytes() + b"\xff\n")
        registry_bytes = self.registry_path().read_bytes()

        completed = self.claim(
            "release",
            "--claim-id",
            "project",
            "--reconcile-out-of-domain-commit",
            fixture["peer_commit"],
            "--prior-rejected-release-reference",
            fixture["prior_rejected_release_reference"],
        )

        self.assertEqual(1, completed.returncode)
        self.assertEqual("", completed.stderr)
        self.assertEqual(
            "reconciliation_legacy_journal_invalid",
            self.output(completed)["reason"],
        )
        self.assertEqual(registry_bytes, self.registry_path().read_bytes())

    def test_release_reconciliation_rejects_malformed_legacy_journal_structurally(
        self,
    ) -> None:
        fixture = self.release_reconciliation_fixture()
        self.downgrade_claim_incarnations_to_legacy_fixture()
        journal_path = next(self.hot_directory().glob("*.jsonl"))
        journal_path.write_bytes(journal_path.read_bytes() + b"{malformed}\n")
        registry_bytes = self.registry_path().read_bytes()

        completed = self.claim(
            "release",
            "--claim-id",
            "project",
            "--reconcile-out-of-domain-commit",
            fixture["peer_commit"],
            "--prior-rejected-release-reference",
            fixture["prior_rejected_release_reference"],
        )

        self.assertEqual(1, completed.returncode)
        self.assertEqual("", completed.stderr)
        self.assertEqual(
            "reconciliation_legacy_journal_invalid",
            self.output(completed)["reason"],
        )
        self.assertEqual(registry_bytes, self.registry_path().read_bytes())

    def test_release_reconciliation_rejects_unresolvable_legacy_acquisition_sequence(self) -> None:
        fixture = self.release_reconciliation_fixture()
        self.downgrade_claim_incarnations_to_legacy_fixture()
        journal_path = next(self.hot_directory().glob("*.jsonl"))
        events = [
            json.loads(line)
            for line in journal_path.read_text(encoding="utf-8").splitlines()
        ]
        journal_path.write_text(
            "".join(
                json.dumps(event, sort_keys=True, separators=(",", ":")) + "\n"
                for event in events
                if event["action"] != "acquire"
            ),
            encoding="utf-8",
        )
        registry_bytes = self.registry_path().read_bytes()

        released = self.claim(
            "release",
            "--claim-id",
            "project",
            "--reconcile-out-of-domain-commit",
            fixture["peer_commit"],
            "--prior-rejected-release-reference",
            fixture["prior_rejected_release_reference"],
        )

        self.assertEqual(1, released.returncode)
        self.assertEqual(
            "reconciliation_legacy_incarnation_unresolvable",
            self.output(released)["reason"],
        )
        self.assertEqual(registry_bytes, self.registry_path().read_bytes())

    def test_release_reconciliation_requires_durable_released_journal_event(self) -> None:
        fixture = self.release_reconciliation_fixture()
        registry_bytes = self.registry_path().read_bytes()
        journal_bytes = self.journal_bytes()
        failures: Mapping[str, str] = {
            "AGENT_CLAIM_TEST_FAIL_JOURNAL_WRITE": "before_write",
            "AGENT_CLAIM_TEST_FAIL_RECONCILIATION_JOURNAL_AFTER_WRITE": "after_write",
            "AGENT_CLAIM_TEST_SHORT_RECONCILIATION_JOURNAL_WRITE": "short_write",
            "AGENT_CLAIM_TEST_FAIL_RECONCILIATION_JOURNAL_FSYNC": "fsync",
            "AGENT_CLAIM_TEST_FAIL_RECONCILIATION_JOURNAL_REPLACE": "replace",
            "AGENT_CLAIM_TEST_FAIL_RECONCILIATION_JOURNAL_DIRECTORY_FSYNC": (
                "journal_directory_fsync"
            ),
            "AGENT_CLAIM_TEST_FAIL_RECONCILIATION_REGISTRY_WRITE": (
                "registry_write"
            ),
            "AGENT_CLAIM_TEST_SHORT_RECONCILIATION_REGISTRY_WRITE": (
                "registry_short_write"
            ),
            "AGENT_CLAIM_TEST_FAIL_RECONCILIATION_REGISTRY_AFTER_WRITE": (
                "registry_after_write"
            ),
            "AGENT_CLAIM_TEST_FAIL_RECONCILIATION_REGISTRY_FSYNC": (
                "registry_fsync"
            ),
            "AGENT_CLAIM_TEST_FAIL_RECONCILIATION_REGISTRY_REPLACE": (
                "registry_replace"
            ),
            "AGENT_CLAIM_TEST_FAIL_RECONCILIATION_REGISTRY_DIRECTORY_FSYNC": (
                "registry_directory_fsync"
            ),
        }

        for variable, boundary in failures.items():
            with self.subTest(boundary=boundary):
                released = self.claim(
                    "release",
                    "--claim-id",
                    "project",
                    "--reconcile-out-of-domain-commit",
                    fixture["peer_commit"],
                    "--prior-rejected-release-reference",
                    fixture["prior_rejected_release_reference"],
                    environment={variable: "1"},
                )

                self.assertEqual(1, released.returncode)
                result = self.output(released)
                self.assertEqual("RELEASE_REJECTED", result["outcome"])
                self.assertEqual("reconciliation_journal_not_durable", result["reason"])
                self.assertFalse(result["journal"]["persisted"])
                self.assertEqual(registry_bytes, self.registry_path().read_bytes())
                self.assertEqual(journal_bytes, self.journal_bytes())
                self.assertEqual(
                    ["project"],
                    [
                        claim["claim_id"]
                        for claim in self.output(self.claim("status"))["claims"]
                    ],
                )

    def test_release_reconciliation_restore_failures_leave_recoverable_ownership(
        self,
    ) -> None:
        fixture = self.release_reconciliation_fixture()
        registry_bytes = self.registry_path().read_bytes()
        journal_bytes = self.journal_bytes()
        pending_path = (
            self.common_directory() / "agent-claim-reconciliation-pending.json"
        )
        restore_failures: Mapping[str, str] = {
            "AGENT_CLAIM_TEST_FAIL_RECONCILIATION_REGISTRY_RESTORE_WRITE": (
                "restore_write"
            ),
            "AGENT_CLAIM_TEST_FAIL_RECONCILIATION_REGISTRY_RESTORE_REPLACE": (
                "restore_replace"
            ),
            "AGENT_CLAIM_TEST_FAIL_RECONCILIATION_REGISTRY_RESTORE_FSYNC": (
                "restore_fsync"
            ),
            "AGENT_CLAIM_TEST_FAIL_RECONCILIATION_REGISTRY_RESTORE_DIRECTORY_FSYNC": (
                "restore_directory_fsync"
            ),
        }

        for variable, boundary in restore_failures.items():
            with self.subTest(boundary=boundary):
                released = self.claim(
                    "release",
                    "--claim-id",
                    "project",
                    "--reconcile-out-of-domain-commit",
                    fixture["peer_commit"],
                    "--prior-rejected-release-reference",
                    fixture["prior_rejected_release_reference"],
                    environment={
                        "AGENT_CLAIM_TEST_FAIL_JOURNAL_WRITE": "1",
                        variable: "1",
                    },
                )

                self.assertEqual(1, released.returncode)
                result = self.output(released)
                self.assertEqual("RELEASE_REJECTED", result["outcome"])
                self.assertEqual("reconciliation_restore_pending", result["reason"])
                self.assertEqual("pending_marker", result["ownership_authority"])
                self.assertTrue(pending_path.exists())
                pending = json.loads(pending_path.read_text(encoding="utf-8"))
                original_registry = json.loads(
                    base64.b64decode(pending["registry"]["original"]["base64"])
                )
                self.assertEqual(
                    ["project"],
                    [claim["claim_id"] for claim in original_registry["claims"]],
                )
                self.assertEqual(journal_bytes, self.journal_bytes())

                blocked_acquisition = self.claim(
                    *self.acquire_arguments("intruder"),
                    "--file",
                    "README.md",
                    environment={variable: "1"},
                )

                self.assertEqual(1, blocked_acquisition.returncode)
                blocked_result = self.output(blocked_acquisition)
                self.assertEqual(
                    "RECONCILIATION_RECOVERY_REQUIRED",
                    blocked_result["outcome"],
                )
                self.assertEqual(
                    "pending_marker",
                    blocked_result["ownership_authority"],
                )
                self.assertTrue(pending_path.exists())

                recovered_status = self.claim("status")

                self.assertEqual(0, recovered_status.returncode, recovered_status.stderr)
                self.assertEqual(
                    ["project"],
                    [
                        claim["claim_id"]
                        for claim in self.output(recovered_status)["claims"]
                    ],
                )
                self.assertFalse(pending_path.exists())
                self.assertEqual(registry_bytes, self.registry_path().read_bytes())
                self.assertEqual(journal_bytes, self.journal_bytes())

    def test_release_reconciliation_recovers_committed_marker_without_duplicate_event(
        self,
    ) -> None:
        fixture = self.release_reconciliation_fixture()
        pending_path = (
            self.common_directory() / "agent-claim-reconciliation-pending.json"
        )

        interrupted = self.claim(
            "release",
            "--claim-id",
            "project",
            "--reconcile-out-of-domain-commit",
            fixture["peer_commit"],
            "--prior-rejected-release-reference",
            fixture["prior_rejected_release_reference"],
            environment={
                "AGENT_CLAIM_TEST_STOP_AFTER_RECONCILIATION_COMMIT_MARKER": "1"
            },
        )

        self.assertEqual(1, interrupted.returncode)
        result = self.output(interrupted)
        self.assertEqual("RECONCILIATION_RECOVERY_REQUIRED", result["outcome"])
        self.assertEqual("committed_marker", result["ownership_authority"])
        self.assertTrue(pending_path.exists())
        self.assertEqual(
            0,
            sum(
                event["outcome"] == "RELEASED"
                and event["claim_id"] == "project"
                for event in self.journal_events()
            ),
        )
        self.assertEqual(
            1,
            sum(
                event["outcome"] == "RELEASE_PENDING"
                and event["claim_id"] == "project"
                for event in self.journal_events()
            ),
        )

        recovered_status = self.claim("status")

        self.assertEqual(0, recovered_status.returncode, recovered_status.stderr)
        self.assertEqual([], self.output(recovered_status)["claims"])
        self.assertFalse(pending_path.exists())
        self.assertEqual(
            1,
            sum(
                event["outcome"] == "RELEASED"
                and event["claim_id"] == "project"
                for event in self.journal_events()
            ),
        )
        self.assertEqual(
            0,
            sum(
                event["outcome"] == "RELEASE_PENDING"
                and event["claim_id"] == "project"
                for event in self.journal_events()
            ),
        )

    def test_report_blocks_read_only_when_committed_marker_exists(self) -> None:
        fixture = self.release_reconciliation_fixture()
        interrupted = self.claim(
            "release",
            "--claim-id",
            "project",
            "--reconcile-out-of-domain-commit",
            fixture["peer_commit"],
            "--prior-rejected-release-reference",
            fixture["prior_rejected_release_reference"],
            environment={
                "AGENT_CLAIM_TEST_STOP_AFTER_RECONCILIATION_COMMIT_MARKER": "1"
            },
        )
        self.assertEqual(1, interrupted.returncode)
        marker_path = (
            self.common_directory() / "agent-claim-reconciliation-pending.json"
        )
        marker_bytes = marker_path.read_bytes()
        registry_bytes = self.registry_path().read_bytes()
        journal_bytes = self.journal_bytes()

        reported = self.claim("report", "--since", "2d")

        self.assertEqual(1, reported.returncode)
        self.assertEqual(
            "RECONCILIATION_RECOVERY_REQUIRED",
            self.output(reported)["outcome"],
        )
        self.assertEqual(marker_bytes, marker_path.read_bytes())
        self.assertEqual(registry_bytes, self.registry_path().read_bytes())
        self.assertEqual(journal_bytes, self.journal_bytes())

    def test_report_blocks_read_only_when_prepared_marker_exists(self) -> None:
        fixture = self.release_reconciliation_fixture()
        interrupted = self.claim(
            "release",
            "--claim-id",
            "project",
            "--reconcile-out-of-domain-commit",
            fixture["peer_commit"],
            "--prior-rejected-release-reference",
            fixture["prior_rejected_release_reference"],
            environment={
                "AGENT_CLAIM_TEST_FAIL_RECONCILIATION_JOURNAL_DIRECTORY_FSYNC": "1",
                "AGENT_CLAIM_TEST_FAIL_RECONCILIATION_JOURNAL_RESTORE_WRITE": "1",
            },
        )
        self.assertEqual(1, interrupted.returncode)
        marker_path = (
            self.common_directory() / "agent-claim-reconciliation-pending.json"
        )
        marker_bytes = marker_path.read_bytes()
        registry_bytes = self.registry_path().read_bytes()
        journal_bytes = self.journal_bytes()

        reported = self.claim("report", "--since", "2d")

        self.assertEqual(1, reported.returncode)
        self.assertEqual(
            "RECONCILIATION_RECOVERY_REQUIRED",
            self.output(reported)["outcome"],
        )
        self.assertEqual(marker_bytes, marker_path.read_bytes())
        self.assertEqual(registry_bytes, self.registry_path().read_bytes())
        self.assertEqual(journal_bytes, self.journal_bytes())

    def test_corrupt_marker_schema_is_retained_without_target_mutation(self) -> None:
        fixture = self.release_reconciliation_fixture()
        interrupted = self.claim(
            "release",
            "--claim-id",
            "project",
            "--reconcile-out-of-domain-commit",
            fixture["peer_commit"],
            "--prior-rejected-release-reference",
            fixture["prior_rejected_release_reference"],
            environment={
                "AGENT_CLAIM_TEST_STOP_AFTER_RECONCILIATION_COMMIT_MARKER": "1"
            },
        )
        self.assertEqual(1, interrupted.returncode)
        marker_path = (
            self.common_directory() / "agent-claim-reconciliation-pending.json"
        )
        marker = json.loads(marker_path.read_text(encoding="utf-8"))
        marker["schema_version"] = 999
        marker_path.write_text(
            json.dumps(marker, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        marker_bytes = marker_path.read_bytes()
        registry_bytes = self.registry_path().read_bytes()
        journal_bytes = self.journal_bytes()

        status = self.claim("status")

        self.assertEqual(1, status.returncode)
        self.assertEqual("", status.stderr)
        self.assertEqual(
            "RECONCILIATION_RECOVERY_REQUIRED",
            self.output(status)["outcome"],
        )
        self.assertEqual(marker_bytes, marker_path.read_bytes())
        self.assertEqual(registry_bytes, self.registry_path().read_bytes())
        self.assertEqual(journal_bytes, self.journal_bytes())

    def test_marker_cannot_redirect_registry_snapshot_to_sentinel(self) -> None:
        fixture = self.release_reconciliation_fixture()
        interrupted = self.claim(
            "release",
            "--claim-id",
            "project",
            "--reconcile-out-of-domain-commit",
            fixture["peer_commit"],
            "--prior-rejected-release-reference",
            fixture["prior_rejected_release_reference"],
            environment={
                "AGENT_CLAIM_TEST_STOP_AFTER_RECONCILIATION_COMMIT_MARKER": "1"
            },
        )
        self.assertEqual(1, interrupted.returncode)
        marker_path = (
            self.common_directory() / "agent-claim-reconciliation-pending.json"
        )
        marker = json.loads(marker_path.read_text(encoding="utf-8"))
        marker["registry"]["path"] = "sentinel.txt"
        marker_path.write_text(
            json.dumps(marker, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        sentinel = self.common_directory() / "sentinel.txt"
        sentinel.write_bytes(b"sentinel\n")
        registry_bytes = self.registry_path().read_bytes()
        journal_bytes = self.journal_bytes()

        status = self.claim("status")

        self.assertEqual(1, status.returncode)
        self.assertEqual(
            "RECONCILIATION_RECOVERY_REQUIRED",
            self.output(status)["outcome"],
        )
        self.assertEqual(b"sentinel\n", sentinel.read_bytes())
        self.assertTrue(marker_path.exists())
        self.assertEqual(registry_bytes, self.registry_path().read_bytes())
        self.assertEqual(journal_bytes, self.journal_bytes())

    def test_marker_rejects_swapped_and_duplicate_targets(self) -> None:
        fixture = self.release_reconciliation_fixture()
        interrupted = self.claim(
            "release",
            "--claim-id",
            "project",
            "--reconcile-out-of-domain-commit",
            fixture["peer_commit"],
            "--prior-rejected-release-reference",
            fixture["prior_rejected_release_reference"],
            environment={
                "AGENT_CLAIM_TEST_STOP_AFTER_RECONCILIATION_COMMIT_MARKER": "1"
            },
        )
        self.assertEqual(1, interrupted.returncode)
        marker_path = (
            self.common_directory() / "agent-claim-reconciliation-pending.json"
        )
        original_marker = json.loads(marker_path.read_text(encoding="utf-8"))
        registry_bytes = self.registry_path().read_bytes()
        journal_bytes = self.journal_bytes()
        registry_target = original_marker["registry"]["path"]
        journal_target = original_marker["journal"]["path"]
        target_cases = {
            "swapped": (journal_target, registry_target),
            "duplicate": (registry_target, registry_target),
        }

        for label, (registry_path, journal_path) in target_cases.items():
            with self.subTest(label=label):
                marker = json.loads(json.dumps(original_marker))
                marker["registry"]["path"] = registry_path
                marker["journal"]["path"] = journal_path
                marker_path.write_text(
                    json.dumps(marker, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8",
                )
                status = self.claim("status")
                self.assertEqual(1, status.returncode)
                self.assertEqual(
                    "RECONCILIATION_RECOVERY_REQUIRED",
                    self.output(status)["outcome"],
                )
                self.assertTrue(marker_path.exists())
                self.assertEqual(registry_bytes, self.registry_path().read_bytes())
                self.assertEqual(journal_bytes, self.journal_bytes())

    def test_forged_self_consistent_marker_snapshots_are_rejected(self) -> None:
        fixture = self.release_reconciliation_fixture()
        interrupted = self.claim(
            "release",
            "--claim-id",
            "project",
            "--reconcile-out-of-domain-commit",
            fixture["peer_commit"],
            "--prior-rejected-release-reference",
            fixture["prior_rejected_release_reference"],
            environment={
                "AGENT_CLAIM_TEST_STOP_AFTER_RECONCILIATION_COMMIT_MARKER": "1"
            },
        )
        self.assertEqual(1, interrupted.returncode)
        marker_path = (
            self.common_directory() / "agent-claim-reconciliation-pending.json"
        )
        marker = json.loads(marker_path.read_text(encoding="utf-8"))
        original = base64.b64decode(marker["registry"]["original"]["base64"])
        marker["registry"]["released"] = {
            "exists": True,
            "sha256": hashlib.sha256(original).hexdigest(),
            "base64": base64.b64encode(original).decode("ascii"),
        }
        marker_path.write_text(
            json.dumps(marker, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        marker_bytes = marker_path.read_bytes()
        registry_bytes = self.registry_path().read_bytes()
        journal_bytes = self.journal_bytes()

        status = self.claim("status")

        self.assertEqual(1, status.returncode)
        self.assertEqual(
            "RECONCILIATION_RECOVERY_REQUIRED",
            self.output(status)["outcome"],
        )
        self.assertEqual(marker_bytes, marker_path.read_bytes())
        self.assertEqual(registry_bytes, self.registry_path().read_bytes())
        self.assertEqual(journal_bytes, self.journal_bytes())

    def test_marker_target_symlink_is_rejected_without_following_it(self) -> None:
        fixture = self.release_reconciliation_fixture()
        interrupted = self.claim(
            "release",
            "--claim-id",
            "project",
            "--reconcile-out-of-domain-commit",
            fixture["peer_commit"],
            "--prior-rejected-release-reference",
            fixture["prior_rejected_release_reference"],
            environment={
                "AGENT_CLAIM_TEST_STOP_AFTER_RECONCILIATION_COMMIT_MARKER": "1"
            },
        )
        self.assertEqual(1, interrupted.returncode)
        marker_path = (
            self.common_directory() / "agent-claim-reconciliation-pending.json"
        )
        marker_bytes = marker_path.read_bytes()
        registry_bytes = self.registry_path().read_bytes()
        event_root = self.common_directory() / "agent-claim-events"
        hot = event_root / "hot"
        real_hot = event_root / "real-hot"
        hot.rename(real_hot)
        hot.symlink_to(real_hot, target_is_directory=True)
        real_bytes = {
            path.name: path.read_bytes()
            for path in real_hot.glob("*.jsonl")
        }

        status = self.claim("status")

        self.assertEqual(1, status.returncode)
        self.assertEqual(
            "RECONCILIATION_RECOVERY_REQUIRED",
            self.output(status)["outcome"],
        )
        self.assertEqual(marker_bytes, marker_path.read_bytes())
        self.assertEqual(registry_bytes, self.registry_path().read_bytes())
        self.assertEqual(
            real_bytes,
            {path.name: path.read_bytes() for path in real_hot.glob("*.jsonl")},
        )

    def test_invalid_utf8_marker_returns_structured_recovery_required(self) -> None:
        fixture = self.release_reconciliation_fixture()
        interrupted = self.claim(
            "release",
            "--claim-id",
            "project",
            "--reconcile-out-of-domain-commit",
            fixture["peer_commit"],
            "--prior-rejected-release-reference",
            fixture["prior_rejected_release_reference"],
            environment={
                "AGENT_CLAIM_TEST_STOP_AFTER_RECONCILIATION_COMMIT_MARKER": "1"
            },
        )
        self.assertEqual(1, interrupted.returncode)
        marker_path = (
            self.common_directory() / "agent-claim-reconciliation-pending.json"
        )
        marker_path.write_bytes(b"\xff\n")
        registry_bytes = self.registry_path().read_bytes()
        journal_bytes = self.journal_bytes()

        status = self.claim("status")

        self.assertEqual(1, status.returncode)
        self.assertEqual("", status.stderr)
        self.assertEqual(
            "RECONCILIATION_RECOVERY_REQUIRED",
            self.output(status)["outcome"],
        )
        self.assertEqual(b"\xff\n", marker_path.read_bytes())
        self.assertEqual(registry_bytes, self.registry_path().read_bytes())
        self.assertEqual(journal_bytes, self.journal_bytes())

    def test_reconciliation_preserves_registry_and_journal_file_modes(self) -> None:
        fixture = self.release_reconciliation_fixture()
        journal_path = next(self.hot_directory().glob("*.jsonl"))
        self.registry_path().chmod(0o640)
        journal_path.chmod(0o640)

        released = self.claim(
            "release",
            "--claim-id",
            "project",
            "--reconcile-out-of-domain-commit",
            fixture["peer_commit"],
            "--prior-rejected-release-reference",
            fixture["prior_rejected_release_reference"],
        )

        self.assertEqual(0, released.returncode, released.stderr)
        self.assertEqual(0o640, self.registry_path().stat().st_mode & 0o777)
        self.assertEqual(0o640, journal_path.stat().st_mode & 0o777)

    def test_committed_marker_delete_failure_is_recoverable_without_duplicate_release(
        self,
    ) -> None:
        fixture = self.release_reconciliation_fixture()
        marker_path = (
            self.common_directory() / "agent-claim-reconciliation-pending.json"
        )

        interrupted = self.claim(
            "release",
            "--claim-id",
            "project",
            "--reconcile-out-of-domain-commit",
            fixture["peer_commit"],
            "--prior-rejected-release-reference",
            fixture["prior_rejected_release_reference"],
            environment={
                "AGENT_CLAIM_TEST_FAIL_RECONCILIATION_MARKER_REMOVE": "1"
            },
        )

        self.assertEqual(1, interrupted.returncode)
        self.assertEqual(
            "committed_reconciliation_cleanup_pending",
            self.output(interrupted)["reason"],
        )
        self.assertTrue(marker_path.exists())
        recovered = self.claim("status")
        self.assertEqual(0, recovered.returncode, recovered.stderr)
        self.assertFalse(marker_path.exists())
        self.assertEqual([], self.output(recovered)["claims"])
        self.assertEqual(
            1,
            sum(
                event["outcome"] == "RELEASED"
                and event["claim_id"] == "project"
                for event in self.journal_events()
            ),
        )

    def test_release_reconciliation_restore_failure_never_exposes_false_released_event(
        self,
    ) -> None:
        fixture = self.release_reconciliation_fixture()
        registry_bytes = self.registry_path().read_bytes()
        journal_bytes = self.journal_bytes()
        pending_path = (
            self.common_directory() / "agent-claim-reconciliation-pending.json"
        )
        environment = {
            "AGENT_CLAIM_TEST_FAIL_RECONCILIATION_JOURNAL_DIRECTORY_FSYNC": "1",
            "AGENT_CLAIM_TEST_FAIL_RECONCILIATION_JOURNAL_RESTORE_WRITE": "1",
        }

        interrupted = self.claim(
            "release",
            "--claim-id",
            "project",
            "--reconcile-out-of-domain-commit",
            fixture["peer_commit"],
            "--prior-rejected-release-reference",
            fixture["prior_rejected_release_reference"],
            environment=environment,
        )

        self.assertEqual(1, interrupted.returncode)
        result = self.output(interrupted)
        self.assertEqual("reconciliation_restore_pending", result["reason"])
        self.assertEqual("pending_marker", result["ownership_authority"])
        self.assertTrue(pending_path.exists())
        self.assertEqual(
            0,
            sum(
                event["outcome"] == "RELEASED"
                and event["claim_id"] == "project"
                for event in self.journal_events()
            ),
        )
        self.assertEqual(
            1,
            sum(
                event["outcome"] == "RELEASE_PENDING"
                and event["claim_id"] == "project"
                for event in self.journal_events()
            ),
        )

        blocked_acquisition = self.claim(
            *self.acquire_arguments("intruder"),
            "--file",
            "README.md",
            environment={
                "AGENT_CLAIM_TEST_FAIL_RECONCILIATION_JOURNAL_RESTORE_WRITE": "1"
            },
        )

        self.assertEqual(1, blocked_acquisition.returncode)
        self.assertEqual(
            "RECONCILIATION_RECOVERY_REQUIRED",
            self.output(blocked_acquisition)["outcome"],
        )

        recovered_status = self.claim("status")

        self.assertEqual(0, recovered_status.returncode, recovered_status.stderr)
        self.assertEqual(
            ["project"],
            [claim["claim_id"] for claim in self.output(recovered_status)["claims"]],
        )
        self.assertFalse(pending_path.exists())
        self.assertEqual(registry_bytes, self.registry_path().read_bytes())
        self.assertEqual(journal_bytes, self.journal_bytes())

    def test_release_reconciliation_recovers_final_journal_directory_failure(
        self,
    ) -> None:
        fixture = self.release_reconciliation_fixture()
        pending_path = (
            self.common_directory() / "agent-claim-reconciliation-pending.json"
        )

        released = self.claim(
            "release",
            "--claim-id",
            "project",
            "--reconcile-out-of-domain-commit",
            fixture["peer_commit"],
            "--prior-rejected-release-reference",
            fixture["prior_rejected_release_reference"],
            environment={
                "AGENT_CLAIM_TEST_FAIL_RECONCILIATION_FINAL_JOURNAL_DIRECTORY_FSYNC": (
                    "1"
                )
            },
        )

        self.assertEqual(0, released.returncode, released.stderr)
        result = self.output(released)
        self.assertEqual("RELEASED", result["outcome"])
        self.assertEqual(
            "reconciliation_cleanup_recovered",
            result["warnings"][0]["code"],
        )
        self.assertFalse(pending_path.exists())
        self.assertEqual(
            1,
            sum(
                event["outcome"] == "RELEASED"
                and event["claim_id"] == "project"
                for event in self.journal_events()
            ),
        )
        self.assertEqual(
            0,
            sum(
                event["outcome"] == "RELEASE_PENDING"
                and event["claim_id"] == "project"
                for event in self.journal_events()
            ),
        )

    def test_project_claim_release_ignores_merge_parent_history(self) -> None:
        source_branch = "project-source"
        target_branch = self.git("branch", "--show-current").stdout.strip()
        self.git("branch", source_branch)
        backlog_path = self.repository / "backlog" / "feature-backlog" / "queued.md"
        backlog_path.write_text("completed before claim\n", encoding="utf-8")
        self.git("add", str(backlog_path))
        self.git("commit", "-m", "complete backlog work before claim")
        acquired = self.claim(*self.acquire_arguments("project"), "--project-files", "--scope-reason", "project work")
        self.assertEqual(0, acquired.returncode, acquired.stderr)

        self.git("checkout", source_branch)
        source_path = self.repository / "src" / "one.py"
        source_path.write_text("project change\n", encoding="utf-8")
        self.git("add", str(source_path))
        self.git("commit", "-m", "project source change")
        self.git("checkout", target_branch)
        self.git("merge", "--no-ff", source_branch, "-m", "integrate project source")

        released = self.claim("release", "--claim-id", "project")

        self.assertEqual(0, released.returncode, released.stderr)
        self.assertEqual("RELEASED", self.output(released)["outcome"])

    def test_status_and_extend_preserve_active_legacy_mixed_claim(self) -> None:
        legacy_claim = {
            "agent": "legacy",
            "all_files": False,
            "baseline_commit": self.git("rev-parse", "HEAD").stdout.strip(),
            "baseline_status": [],
            "branch": "main",
            "claim_id": "legacy-mixed",
            "claimed_at": "2026-07-12T10:00:00Z",
            "files": ["src/one.py", "backlog/feature-backlog/queued.md"],
            "heartbeat": "2026-07-12T10:00:00Z",
            "mode": "primary",
            "parent_claim_id": None,
            "resources": [],
            "root_task_id": "legacy-root",
            "scope_reasons": {},
            "task": "legacy mixed claim",
            "trees": [],
            "worktree": str(self.repository),
        }
        self.registry_path().write_text(json.dumps({"claims": [legacy_claim]}), encoding="utf-8")

        status = self.output(self.claim("status"))["claims"][0]
        extended = self.claim("extend", "--claim-id", "legacy-mixed", "--file", "docs/guide.md")
        stored = json.loads(self.registry_path().read_text(encoding="utf-8"))["claims"][0]

        self.assertEqual("legacy_mixed", status["file_domain"])
        self.assertEqual("complete_worktree", status["compatibility"]["release_policy"])
        self.assertEqual(1, extended.returncode)
        self.assertEqual("legacy_mixed_file_domains", self.output(extended)["rejection"]["reason"])
        self.assertNotIn("file_domain", stored)
        self.assertEqual(legacy_claim["files"], stored["files"])

    def test_legacy_claim_without_out_of_domain_baseline_keeps_complete_worktree_release(self) -> None:
        acquired = self.claim(*self.acquire_arguments("project"), "--file", "src/one.py")
        self.assertEqual(0, acquired.returncode, acquired.stderr)
        registry = json.loads(self.registry_path().read_text(encoding="utf-8"))
        claim = registry["claims"][0]
        claim.pop("baseline_out_of_domain_state")
        claim.pop("baseline_out_of_domain_status")
        self.registry_path().write_text(json.dumps(registry), encoding="utf-8")
        (self.repository / "backlog" / "feature-backlog" / "queued.md").write_text(
            "changed\n",
            encoding="utf-8",
        )

        released = self.claim("release", "--claim-id", "project", "--no-change")

        self.assertEqual(1, released.returncode)
        result = self.output(released)
        self.assertEqual("worktree_not_clean", result["reason"])
        self.assertEqual("complete_worktree", result["compatibility"]["release_policy"])

    def test_legacy_resource_only_claim_reports_none_and_accepts_project_domain(self) -> None:
        legacy_claim = {
            "agent": "legacy",
            "all_files": False,
            "baseline_commit": self.git("rev-parse", "HEAD").stdout.strip(),
            "baseline_status": [],
            "branch": "main",
            "claim_id": "legacy-resource",
            "claimed_at": "2026-07-12T10:00:00Z",
            "files": [],
            "heartbeat": "2026-07-12T10:00:00Z",
            "mode": "primary",
            "parent_claim_id": None,
            "resources": ["port:3000"],
            "root_task_id": "legacy-root",
            "scope_reasons": {},
            "task": "legacy resource claim",
            "trees": [],
            "worktree": str(self.repository),
        }
        self.registry_path().write_text(json.dumps({"claims": [legacy_claim]}), encoding="utf-8")

        status = self.output(self.claim("status"))["claims"][0]
        extended = self.claim(
            "extend",
            "--claim-id",
            "legacy-resource",
            "--file",
            "src/one.py",
        )

        self.assertEqual("none", status["file_domain"])
        self.assertEqual("complete_worktree", status["compatibility"]["release_policy"])
        self.assertEqual(0, extended.returncode, extended.stderr)
        claim = self.output(extended)["claim"]
        self.assertEqual("project_files", claim["file_domain"])
        self.assertEqual(["src/one.py"], claim["files"])
        self.assertEqual(["port:3000"], claim["resources"])

    def test_legacy_resource_only_claim_accepts_backlog_domain(self) -> None:
        legacy_claim = {
            "agent": "legacy",
            "all_files": False,
            "baseline_commit": self.git("rev-parse", "HEAD").stdout.strip(),
            "baseline_status": [],
            "branch": "main",
            "claim_id": "legacy-resource",
            "claimed_at": "2026-07-12T10:00:00Z",
            "files": [],
            "heartbeat": "2026-07-12T10:00:00Z",
            "mode": "primary",
            "parent_claim_id": None,
            "resources": ["database:seed"],
            "root_task_id": "legacy-root",
            "scope_reasons": {},
            "task": "legacy resource claim",
            "trees": [],
            "worktree": str(self.repository),
        }
        self.registry_path().write_text(json.dumps({"claims": [legacy_claim]}), encoding="utf-8")

        extended = self.claim("extend", "--claim-id", "legacy-resource", "--backlog")

        self.assertEqual(0, extended.returncode, extended.stderr)
        claim = self.output(extended)["claim"]
        self.assertEqual("backlog", claim["file_domain"])
        self.assertTrue(claim["backlog"])
        self.assertEqual(["database:seed"], claim["resources"])

    def test_legacy_complete_worktree_release_allows_opposite_domain_commit_after_extension(self) -> None:
        legacy_claim = {
            "agent": "legacy",
            "all_files": False,
            "baseline_commit": self.git("rev-parse", "HEAD").stdout.strip(),
            "baseline_status": [],
            "branch": "main",
            "claim_id": "legacy-resource",
            "claimed_at": "2026-07-12T10:00:00Z",
            "files": [],
            "heartbeat": "2026-07-12T10:00:00Z",
            "mode": "primary",
            "parent_claim_id": None,
            "resources": ["port:3000"],
            "root_task_id": "legacy-root",
            "scope_reasons": {},
            "task": "legacy resource claim",
            "trees": [],
            "worktree": str(self.repository),
        }
        self.registry_path().write_text(json.dumps({"claims": [legacy_claim]}), encoding="utf-8")
        extended = self.claim("extend", "--claim-id", "legacy-resource", "--file", "src/one.py")
        self.assertEqual(0, extended.returncode, extended.stderr)
        backlog_path = self.repository / "backlog" / "feature-backlog" / "queued.md"
        backlog_path.write_text("legacy committed\n", encoding="utf-8")
        self.git("add", str(backlog_path))
        self.git("commit", "-m", "legacy complete worktree commit")

        released = self.claim("release", "--claim-id", "legacy-resource")

        self.assertEqual(0, released.returncode, released.stderr)
        self.assertEqual("RELEASED", self.output(released)["outcome"])

    def test_backlog_claim_release_rejects_project_change(self) -> None:
        acquired = self.claim(*self.acquire_arguments("backlog"), "--backlog")
        self.assertEqual(0, acquired.returncode, acquired.stderr)
        (self.repository / "src" / "one.py").write_text("changed\n", encoding="utf-8")

        released = self.claim("release", "--claim-id", "backlog", "--no-change")

        self.assertEqual(1, released.returncode)
        result = self.output(released)
        self.assertEqual("out_of_domain_changes", result["reason"])
        self.assertEqual(["src/one.py"], result["out_of_domain_paths"])

    def test_backlog_claim_ignores_unchanged_preexisting_project_dirtiness(self) -> None:
        project_path = self.repository / "src" / "one.py"
        project_path.write_text("preexisting\n", encoding="utf-8")

        acquired = self.claim(*self.acquire_arguments("backlog"), "--backlog")
        released = self.claim("release", "--claim-id", "backlog", "--no-change")

        self.assertEqual(0, acquired.returncode, acquired.stderr)
        self.assertEqual("SHARED_CHECKOUT_ACQUIRED", self.output(acquired)["outcome"])
        self.assertEqual(0, released.returncode, released.stderr)

    def test_operational_worktree_paths_are_not_claimable_as_project_files(self) -> None:
        completed = self.claim(
            *self.acquire_arguments("operational"),
            "--file",
            ".worktrees/internal-state",
        )

        self.assertEqual(1, completed.returncode)
        result = self.output(completed)
        self.assertEqual("INVALID_SCOPE", result["outcome"])
        self.assertEqual("operational_path_not_claimable", result["rejection"]["reason"])

    def test_extend_cannot_cross_from_project_into_backlog_domain(self) -> None:
        acquired = self.claim(*self.acquire_arguments("project"), "--file", "src/one.py")
        extended = self.claim(
            "extend",
            "--claim-id",
            "project",
            "--file",
            "backlog/feature-backlog/queued.md",
        )

        self.assertEqual(0, acquired.returncode, acquired.stderr)
        self.assertEqual(1, extended.returncode)
        self.assertEqual("INVALID_SCOPE", self.output(extended)["outcome"])
        claim = self.output(self.claim("status"))["claims"][0]
        self.assertEqual("project_files", claim["file_domain"])
        self.assertEqual(["src/one.py"], claim["files"])

    def test_broad_scope_guardrails_and_future_file_behavior(self) -> None:
        invalid_commands = (
            (["--file", "."], "use --all-files"),
            (["--file", "**"], "use --tree"),
            (["--file", "src"], "use --tree"),
            (["--tree", "README.md", "--scope-reason", "wrong kind"], "use --file"),
            (["--tree", ".", "--scope-reason", "too broad"], "use --all-files"),
            (["--tree", "src"], "add --scope-reason"),
        )
        for index, (scope_arguments, replacement) in enumerate(invalid_commands):
            with self.subTest(scope_arguments=scope_arguments):
                completed = self.claim(*self.acquire_arguments(f"invalid-{index}"), *scope_arguments)
                self.assertEqual(1, completed.returncode)
                result = self.output(completed)
                self.assertEqual("INVALID_SCOPE", result["outcome"])
                self.assertIn(replacement, result["replacement"])

        future = self.claim(*self.acquire_arguments("future"), "--file", "not-created-yet.py")
        self.assertEqual(0, future.returncode, future.stderr)

    def test_compatibility_mode_converts_directory_file_scope_with_warning(self) -> None:
        completed = self.claim(
            *self.acquire_arguments("legacy"),
            "--file",
            "src",
            "--compat-file-directories",
            "--scope-reason",
            "temporary legacy caller",
        )

        self.assertEqual(0, completed.returncode, completed.stderr)
        result = self.output(completed)
        self.assertEqual(["src"], result["claim"]["trees"])
        self.assertEqual("legacy_file_directory_scope", result["warnings"][0]["code"])

    def test_extend_adds_multiple_scopes_and_is_idempotent(self) -> None:
        acquired = self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        extended = self.claim(
            "extend",
            "--claim-id",
            "first",
            "--file",
            "future.py",
            *self.timed_resource_arguments(
                resource="generated:codegen",
                resource_class="live-model-evaluation",
            ),
        )
        repeated = self.claim(
            "extend",
            "--claim-id",
            "first",
            "--file",
            "future.py",
            *self.timed_resource_arguments(
                resource="generated:codegen",
                resource_class="live-model-evaluation",
            ),
        )

        self.assertEqual(0, acquired.returncode, acquired.stderr)
        self.assertEqual(0, extended.returncode, extended.stderr)
        added = self.output(extended)["added_scope"]
        self.assertEqual(["future.py"], added["files"])
        self.assertEqual(["generated:codegen"], added["resources"])
        repeated_result = self.output(repeated)
        self.assertEqual("EXTENDED", repeated_result["outcome"])
        self.assertEqual([], repeated_result["added_scope"]["files"])
        self.assertEqual(["future.py"], repeated_result["already_owned_scope"]["files"])

    def test_conflicting_extension_leaves_registry_byte_for_byte_unchanged(self) -> None:
        self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        isolated, _isolated_path = self.isolated_arguments("second")
        self.claim(*self.acquire_arguments("second"), "--file", "src/one.py", *isolated)
        before = self.registry_path().read_bytes()

        blocked = self.claim("extend", "--claim-id", "second", "--file", "README.md")

        self.assertEqual(3, blocked.returncode)
        self.assertEqual("CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED", self.output(blocked)["outcome"])
        self.assertEqual(before, self.registry_path().read_bytes())

    def test_isolated_extension_reports_primary_resource_overlap_before_location(self) -> None:
        self.claim(
            *self.acquire_arguments("first"),
            *self.timed_resource_arguments(
                resource="merge:integration:main",
                resource_class="main-integration",
            ),
        )
        isolated, _isolated_path = self.isolated_arguments("second")
        self.claim(*self.acquire_arguments("second"), "--file", "src/one.py", *isolated)
        before = self.registry_path().read_bytes()

        blocked = self.claim(
            "extend",
            "--claim-id",
            "second",
            *self.timed_resource_arguments(
                resource="merge:integration:main",
                resource_class="main-integration",
            ),
        )

        self.assertEqual(3, blocked.returncode)
        result = self.output(blocked)
        self.assertEqual("CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED", result["outcome"])
        self.assertEqual(["first"], result["conflicting_claim_ids"])
        self.assertEqual(before, self.registry_path().read_bytes())

    def test_simultaneous_extensions_cannot_both_acquire_same_file(self) -> None:
        self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        isolated, _isolated_path = self.isolated_arguments("second")
        self.claim(*self.acquire_arguments("second"), "--file", "src/one.py", *isolated)
        commands = [
            self.claim_command("extend", "--claim-id", claim_id, "--file", "shared-new.py")
            for claim_id in ("first", "second")
        ]
        processes = [
            subprocess.Popen(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            for command in commands
        ]
        completed = [process.communicate() + (process.returncode,) for process in processes]

        self.assertEqual([0, 3], sorted(code for _stdout, _stderr, code in completed))
        self.assertEqual(
            {"CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED", "EXTENDED"},
            {json.loads(stdout)["outcome"] for stdout, _stderr, _code in completed},
        )

    def test_extending_isolated_claim_preserves_worktree_metadata(self) -> None:
        self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        isolated, _isolated_path = self.isolated_arguments("second")
        acquired = self.claim(*self.acquire_arguments("second"), "--file", "src/one.py", *isolated)
        before = self.output(acquired)["claim"]

        extended = self.claim("extend", "--claim-id", "second", "--file", "future.py")
        after = self.output(extended)["claim"]

        for field in (
            "worktree",
            "branch",
            "checkout_topology",
            "baseline_commit",
            "claimed_at",
            "mode",
        ):
            self.assertEqual(before[field], after[field])

    def test_isolated_claim_hands_backlog_extension_to_primary_despite_unrelated_claim(self) -> None:
        self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        isolated, isolated_path = self.isolated_arguments("second")
        self.claim(*self.acquire_arguments("second"), "--file", "src/one.py", *isolated)
        before = self.registry_path().read_bytes()

        completed = self.claim(
            "extend",
            "--claim-id",
            "second",
            "--file",
            "backlog/feature-backlog/queued.md",
            repo=isolated_path,
        )
        report = self.claim("report", "--since", "2d")

        self.assertEqual(3, completed.returncode)
        result = self.output(completed)
        self.assertEqual("SHARED_CHECKOUT_REQUIRED", result["outcome"])
        self.assertEqual("PRIMARY_REQUIRED", result["legacy_outcome"])
        self.assertEqual(before, self.registry_path().read_bytes())
        event = next(
            event
            for event in self.journal_events()
            if event["claim_id"] == "second" and event["outcome"] == "PRIMARY_REQUIRED"
        )
        self.assertIs(event["shared_checkout_claimed"], False)
        self.assertEqual(0, report.returncode, report.stderr)
        metrics = self.output(report)["metrics"]
        self.assertEqual(1, metrics["outcome_counts"]["SHARED_CHECKOUT_REQUIRED"])
        self.assertEqual(1, metrics["raw_outcome_counts"]["PRIMARY_REQUIRED"])
        self.assertEqual([], metrics["outcome_normalization_gaps"])

    def test_isolated_backlog_extension_reports_available_shared_checkout(self) -> None:
        self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        isolated, isolated_path = self.isolated_arguments("second")
        self.claim(*self.acquire_arguments("second"), "--file", "src/one.py", *isolated)
        self.claim("release", "--claim-id", "first", "--no-change")

        completed = self.claim(
            "extend",
            "--claim-id",
            "second",
            "--file",
            "backlog/feature-backlog/queued.md",
            repo=isolated_path,
        )

        self.assertEqual(3, completed.returncode)
        self.assertEqual("SHARED_CHECKOUT_REQUIRED", self.output(completed)["outcome"])
        event = next(
            event
            for event in self.journal_events()
            if event["claim_id"] == "second" and event["outcome"] == "PRIMARY_REQUIRED"
        )
        self.assertIs(event["shared_checkout_claimed"], False)

    def test_isolated_named_resource_extension_ignores_unrelated_primary_claim(self) -> None:
        self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        isolated, isolated_path = self.isolated_arguments("second")
        self.claim(*self.acquire_arguments("second"), "--file", "src/one.py", *isolated)

        completed = self.claim(
            "extend",
            "--claim-id",
            "second",
            *self.timed_resource_arguments(
                resource="git-index:primary",
                resource_class="main-integration",
            ),
            repo=isolated_path,
        )

        self.assertEqual(0, completed.returncode, completed.stderr)
        result = self.output(completed)
        self.assertEqual("EXTENDED", result["outcome"])
        event = next(
            event
            for event in reversed(self.journal_events())
            if event["claim_id"] == "second" and event["outcome"] == "EXTENDED"
        )
        self.assertEqual(["git-index:primary"], event["added_scope"]["resources"])

    def test_report_uses_explicit_context_when_shared_checkout_is_available(self) -> None:
        self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        isolated, isolated_path = self.isolated_arguments("isolated")
        self.claim(*self.acquire_arguments("isolated"), "--file", "src/one.py", *isolated)
        self.claim("release", "--claim-id", "first", "--no-change")

        required = self.claim(
            *self.acquire_arguments("backlog"),
            "--backlog",
            repo=isolated_path,
        )
        report = self.claim("report", "--since", "2d")

        self.assertEqual(3, required.returncode)
        event = next(event for event in self.journal_events() if event["claim_id"] == "backlog")
        self.assertIs(event["shared_checkout_claimed"], False)
        self.assertEqual(0, report.returncode, report.stderr)
        metrics = self.output(report)["metrics"]
        self.assertEqual(1, metrics["outcome_counts"]["SHARED_CHECKOUT_REQUIRED"])
        self.assertEqual(1, metrics["raw_outcome_counts"]["PRIMARY_REQUIRED"])
        self.assertEqual([], metrics["outcome_normalization_gaps"])

    def test_linked_worktrees_share_one_journal(self) -> None:
        self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        isolated, isolated_path = self.isolated_arguments("second")
        self.claim(*self.acquire_arguments("second"), "--file", "src/one.py", *isolated)
        third_arguments, third_path = self.isolated_arguments("third")
        third = self.claim(
            *self.acquire_arguments("third"),
            "--file",
            "docs/guide.md",
            *third_arguments,
            repo=isolated_path,
        )
        heartbeat = self.claim("heartbeat", "--claim-id", "second", repo=isolated_path)

        self.assertEqual(0, third.returncode, third.stderr)
        self.assertEqual(0, heartbeat.returncode, heartbeat.stderr)
        self.assertTrue(third_path.is_dir())
        self.assertFalse((isolated_path / ".worktrees" / "third").exists())
        events = self.journal_events()
        self.assertEqual(["first", "second", "third", "second"], [event["claim_id"] for event in events])
        self.assertEqual(1, len(list(self.hot_directory().glob("*.jsonl"))))
        linked_event = next(event for event in events if event["claim_id"] == "third")
        self.assertEqual("codex/third", linked_event["worktree_id"])
        self.assertNotIn(str(self.temporary_directory.name), json.dumps(linked_event))

    def test_legacy_linked_claim_without_topology_retains_accurate_journal_fallback(self) -> None:
        linked_path = self.existing_linked_worktree()
        acquired = self.claim(
            *self.acquire_arguments("private"),
            "--file",
            "README.md",
            repo=linked_path,
        )
        registry = json.loads(self.registry_path().read_text(encoding="utf-8"))
        registry["claims"][0].pop("checkout_topology")
        self.registry_path().write_text(
            json.dumps(registry, indent=2) + "\n",
            encoding="utf-8",
        )

        heartbeat = self.claim("heartbeat", "--claim-id", "private", repo=linked_path)

        self.assertEqual(0, acquired.returncode, acquired.stderr)
        self.assertEqual(0, heartbeat.returncode, heartbeat.stderr)
        event = self.journal_events()[-1]
        self.assertEqual("HEARTBEAT", event["outcome"])
        self.assertEqual("primary", event["mode"])
        self.assertEqual("linked", event["checkout_topology"])
        self.assertEqual("codex/private", event["worktree_id"])
        self.assertNotIn(str(self.temporary_directory.name), json.dumps(event))

    def test_concurrent_journal_events_are_complete_and_unique(self) -> None:
        self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        commands = [self.claim_command("heartbeat", "--claim-id", "first") for _index in range(12)]
        processes = [
            subprocess.Popen(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            for command in commands
        ]
        completed = [process.communicate() + (process.returncode,) for process in processes]

        self.assertTrue(all(code == 0 for _stdout, _stderr, code in completed))
        events = self.journal_events()
        self.assertEqual(13, len(events))
        self.assertEqual(13, len({event["event_id"] for event in events}))

    def test_journal_failure_warns_without_weakening_registry_safety(self) -> None:
        completed = self.claim(
            *self.acquire_arguments("first"),
            "--file",
            "README.md",
            environment={"AGENT_CLAIM_TEST_FAIL_JOURNAL_WRITE": "1"},
        )

        self.assertEqual(0, completed.returncode, completed.stderr)
        result = self.output(completed)
        self.assertEqual("journal_write_failed", result["warnings"][0]["code"])
        self.assertFalse(result["journal"]["persisted"])
        registry = json.loads(self.registry_path().read_text(encoding="utf-8"))
        self.assertEqual(["first"], [claim["claim_id"] for claim in registry["claims"]])
        report = self.claim("report", "--since", "2d")
        self.assertEqual(
            [{"detail": "live claim has no acquisition event", "source": "first"}],
            json.loads(report.stdout)["coverage_gaps"],
        )

    def test_released_claim_reconstructs_as_journal_lifecycle(self) -> None:
        self.claim(*self.acquire_arguments("first"), "--file", "README.md")
        self.claim("heartbeat", "--claim-id", "first")
        (self.repository / "README.md").write_text("committed\n", encoding="utf-8")
        self.git("add", "README.md")
        self.git("commit", "-m", "change")
        released = self.claim("release", "--claim-id", "first")

        self.assertEqual(0, released.returncode, released.stderr)
        events = self.journal_events()
        self.assertTrue(all(event["schema_version"] == 1 for event in events))
        self.assertEqual(["PRIMARY", "HEARTBEAT", "RELEASED"], [event["outcome"] for event in events])
        self.assertEqual(self.git("rev-parse", "HEAD").stdout.strip(), events[-1]["resulting_commit"])

    def test_release_requires_clean_commit_or_explicit_no_change(self) -> None:
        acquired = self.claim(*self.acquire_arguments("first"))
        rejected = self.claim("release", "--claim-id", "first")
        (self.repository / "README.md").write_text("committed\n", encoding="utf-8")
        self.git("add", "README.md")
        self.git("commit", "-m", "change")
        released = self.claim("release", "--claim-id", "first")

        self.assertEqual(0, acquired.returncode, acquired.stderr)
        self.assertEqual(1, rejected.returncode)
        self.assertEqual("RELEASE_REJECTED", self.output(rejected)["outcome"])
        self.assertEqual(0, released.returncode, released.stderr)
        self.assertEqual("RELEASED", self.output(released)["outcome"])

    def test_recovery_claim_preserves_dirty_baseline_until_checkpoint_commit(self) -> None:
        (self.repository / "README.md").write_text("recovery\n", encoding="utf-8")
        acquired = self.claim(*self.acquire_arguments("recovery"), "--allow-recovery")
        rejected = self.claim("release", "--claim-id", "recovery")
        self.git("add", "README.md")
        self.git("commit", "-m", "recovery checkpoint")
        released = self.claim("release", "--claim-id", "recovery")

        self.assertEqual(0, acquired.returncode, acquired.stderr)
        result = self.output(acquired)
        self.assertEqual("DIRTY_CHECKOUT_RECOVERY_ACQUIRED", result["outcome"])
        self.assertEqual("RECOVER", result["legacy_outcome"])
        self.assertEqual(1, rejected.returncode)
        self.assertEqual(0, released.returncode, released.stderr)

    def test_isolated_worktrees_commit_without_global_commit_resource(self) -> None:
        self.claim(*self.acquire_arguments("first"), "--file", "first.txt")
        isolated, isolated_path = self.isolated_arguments("second")
        self.claim(*self.acquire_arguments("second"), "--file", "second.txt", *isolated)
        (self.repository / "first.txt").write_text("first\n", encoding="utf-8")
        (isolated_path / "second.txt").write_text("second\n", encoding="utf-8")
        self.git("add", "first.txt")
        self.git("add", "second.txt", worktree=isolated_path)
        processes = [
            subprocess.Popen(
                ["git", "-C", str(worktree), "commit", "-m", message],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            for worktree, message in ((self.repository, "first"), (isolated_path, "second"))
        ]
        completed = [process.communicate() + (process.returncode,) for process in processes]

        self.assertTrue(all(code == 0 for _stdout, _stderr, code in completed), completed)

    def test_integration_resources_conflict_per_target_branch(self) -> None:
        main = self.claim(
            *self.acquire_arguments("main"),
            *self.timed_resource_arguments(
                resource="merge:integration:main",
                resource_class="main-integration",
            ),
        )
        same_target = self.claim(
            *self.acquire_arguments("same"),
            *self.timed_resource_arguments(
                resource="merge:integration:main",
                resource_class="main-integration",
            ),
        )
        isolated, _isolated_path = self.isolated_arguments("release")
        other_target = self.claim(
            *self.acquire_arguments("release"),
            *self.timed_resource_arguments(
                resource="merge:integration:release",
                resource_class="main-integration",
            ),
            *isolated,
        )

        self.assertEqual(0, main.returncode, main.stderr)
        self.assertEqual(3, same_target.returncode)
        self.assertEqual(0, other_target.returncode, other_target.stderr)

    def test_maintenance_keeps_two_hot_days_and_archives_older_days_losslessly(self) -> None:
        for day in ("2026-07-10", "2026-07-11", "2026-07-12", "2026-07-13"):
            event = self.synthetic_event(
                f"event-{day}",
                f"{day}T12:00:00Z",
                "acquire",
                "PRIMARY",
                f"claim-{day}",
            )
            self.write_daily_events(day, [event])
        environment = {"AGENT_CLAIM_TEST_NOW": "2026-07-13T15:00:00Z"}

        maintained = self.claim("maintain-journal", "--hot-days", "2", environment=environment)
        rerun = self.claim("maintain-journal", "--hot-days", "2", environment=environment)

        self.assertEqual(0, maintained.returncode, maintained.stderr)
        self.assertEqual(0, rerun.returncode, rerun.stderr)
        self.assertEqual(
            ["2026-07-12.jsonl", "2026-07-13.jsonl"],
            sorted(path.name for path in self.hot_directory().glob("*.jsonl")),
        )
        archive_root = self.common_directory() / "agent-claim-events" / "archive" / "2026" / "07"
        summary_root = self.common_directory() / "agent-claim-events" / "journal" / "2026" / "07"
        for day in ("2026-07-10", "2026-07-11"):
            archive = archive_root / f"{day}.jsonl.gz"
            summary = summary_root / f"{day}.json"
            events = [json.loads(line) for line in gzip.decompress(archive.read_bytes()).decode().splitlines()]
            self.assertEqual([f"event-{day}"], [event["event_id"] for event in events])
            self.assertEqual(1, json.loads(summary.read_text(encoding="utf-8"))["raw_event_count"])
        self.assertEqual([], self.output(rerun)["archived"])

    def test_maintenance_recovers_prepared_marker_before_hot_day_rollover(self) -> None:
        fixture = self.release_reconciliation_fixture()
        registry_bytes = self.registry_path().read_bytes()
        original_journal = self.journal_bytes()
        interrupted = self.claim(
            "release",
            "--claim-id",
            "project",
            "--reconcile-out-of-domain-commit",
            fixture["peer_commit"],
            "--prior-rejected-release-reference",
            fixture["prior_rejected_release_reference"],
            environment={
                "AGENT_CLAIM_TEST_FAIL_RECONCILIATION_JOURNAL_DIRECTORY_FSYNC": "1",
                "AGENT_CLAIM_TEST_FAIL_RECONCILIATION_JOURNAL_RESTORE_WRITE": "1",
            },
        )
        self.assertEqual(1, interrupted.returncode)
        marker_path = (
            self.common_directory() / "agent-claim-reconciliation-pending.json"
        )
        self.assertEqual("prepared", json.loads(marker_path.read_text())["state"])

        maintained = self.claim(
            "maintain-journal",
            "--hot-days",
            "1",
            environment={"AGENT_CLAIM_TEST_NOW": "2026-07-26T00:01:00Z"},
        )

        self.assertEqual(0, maintained.returncode, maintained.stderr)
        self.assertFalse(marker_path.exists())
        self.assertEqual(registry_bytes, self.registry_path().read_bytes())
        archived_bytes: dict[str, bytes] = {}
        archive_root = self.common_directory() / "agent-claim-events" / "archive"
        for path in archive_root.glob("**/*.jsonl.gz"):
            archived_bytes[
                f"agent-claim-events/hot/{path.name.removesuffix('.gz')}"
            ] = gzip.decompress(path.read_bytes())
        self.assertEqual(original_journal, archived_bytes)
        self.assertFalse(
            any(
                event["outcome"] in {"RELEASE_PENDING", "RELEASED"}
                and event["claim_id"] == "project"
                for raw in archived_bytes.values()
                for event in (
                    json.loads(line)
                    for line in raw.decode("utf-8").splitlines()
                )
            )
        )

    def test_maintenance_finalizes_committed_marker_before_hot_day_rollover(self) -> None:
        fixture = self.release_reconciliation_fixture()
        interrupted = self.claim(
            "release",
            "--claim-id",
            "project",
            "--reconcile-out-of-domain-commit",
            fixture["peer_commit"],
            "--prior-rejected-release-reference",
            fixture["prior_rejected_release_reference"],
            environment={
                "AGENT_CLAIM_TEST_STOP_AFTER_RECONCILIATION_COMMIT_MARKER": "1"
            },
        )
        self.assertEqual(1, interrupted.returncode)
        marker_path = (
            self.common_directory() / "agent-claim-reconciliation-pending.json"
        )
        self.assertEqual("committed", json.loads(marker_path.read_text())["state"])

        maintained = self.claim(
            "maintain-journal",
            "--hot-days",
            "1",
            environment={"AGENT_CLAIM_TEST_NOW": "2026-07-26T00:01:00Z"},
        )

        self.assertEqual(0, maintained.returncode, maintained.stderr)
        self.assertFalse(marker_path.exists())
        self.assertEqual([], self.output(self.claim("status"))["claims"])
        archive_root = self.common_directory() / "agent-claim-events" / "archive"
        archived_events = [
            json.loads(line)
            for path in archive_root.glob("**/*.jsonl.gz")
            for line in gzip.decompress(path.read_bytes()).decode("utf-8").splitlines()
        ]
        self.assertEqual(
            1,
            sum(
                event["outcome"] == "RELEASED"
                and event["claim_id"] == "project"
                for event in archived_events
            ),
        )
        self.assertFalse(
            any(event["outcome"] == "RELEASE_PENDING" for event in archived_events)
        )

    def test_archive_interruption_leaves_hot_file_for_safe_rerun(self) -> None:
        event = self.synthetic_event("old", "2026-07-10T12:00:00Z", "acquire", "PRIMARY", "old")
        hot = self.write_daily_events("2026-07-10", [event])
        environment = {
            "AGENT_CLAIM_TEST_NOW": "2026-07-13T15:00:00Z",
            "AGENT_CLAIM_TEST_FAIL_ARCHIVE_BEFORE_VALIDATE": "1",
        }

        interrupted = self.claim("maintain-journal", environment=environment)

        self.assertEqual(1, interrupted.returncode)
        self.assertTrue(hot.exists())
        archive = self.common_directory() / "agent-claim-events" / "archive" / "2026" / "07" / "2026-07-10.jsonl.gz"
        self.assertFalse(archive.exists())
        completed = self.claim(
            "maintain-journal",
            environment={"AGENT_CLAIM_TEST_NOW": "2026-07-13T15:00:00Z"},
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertFalse(hot.exists())

    def test_archive_validation_failure_preserves_hot_source(self) -> None:
        event = self.synthetic_event("old", "2026-07-10T12:00:00Z", "acquire", "PRIMARY", "old")
        hot = self.write_daily_events("2026-07-10", [event])
        archive = self.common_directory() / "agent-claim-events" / "archive" / "2026" / "07" / "2026-07-10.jsonl.gz"
        archive.parent.mkdir(parents=True)
        archive.write_bytes(gzip.compress(b'{"different":"event"}\n'))

        completed = self.claim(
            "maintain-journal",
            environment={"AGENT_CLAIM_TEST_NOW": "2026-07-13T15:00:00Z"},
        )

        self.assertEqual(1, completed.returncode)
        self.assertEqual("JOURNAL_MAINTENANCE_FAILED", self.output(completed)["outcome"])
        self.assertTrue(hot.exists())

    def test_report_groups_waits_and_distinguishes_contention_kinds(self) -> None:
        events = [
            self.synthetic_event(
                "wait-1",
                "2026-07-12T10:00:00Z",
                "acquire",
                "WAIT",
                "blocked",
                overlaps=[
                    {
                        "scope_kind": "path",
                        "requested_kind": "file",
                        "requested": "src/one.py",
                        "claimed_kind": "file",
                        "claimed": "src/one.py",
                    },
                    {
                        "scope_kind": "resource",
                        "requested_kind": "resource",
                        "requested": "port:3000",
                        "claimed_kind": "resource",
                        "claimed": "port:3000",
                    },
                ],
                journal_warnings=[{"code": "prior_journal_warning"}],
            ),
            self.synthetic_event(
                "wait-2",
                "2026-07-12T10:02:00Z",
                "acquire",
                "WAIT",
                "blocked",
                overlaps=[
                    {
                        "scope_kind": "path",
                        "requested_kind": "file",
                        "requested": "src/one.py",
                        "claimed_kind": "tree",
                        "claimed": "src",
                    }
                ],
            ),
            self.synthetic_event(
                "acquire",
                "2026-07-12T10:05:00Z",
                "acquire",
                "PRIMARY",
                "blocked",
                requested_scopes={
                    "files": [],
                    "trees": ["src"],
                    "project_files": False,
                    "backlog": False,
                    "all_files": False,
                    "file_domain": "project_files",
                    "resources": ["merge:integration:main"],
                    "scope_reason": "source migration",
                },
            ),
            self.synthetic_event(
                "backlog-domain",
                "2026-07-12T10:05:10Z",
                "extend",
                "EXTENDED",
                "backlog-domain",
                requested_scopes={
                    "files": [],
                    "trees": [],
                    "project_files": False,
                    "backlog": True,
                    "all_files": False,
                    "file_domain": "backlog",
                    "resources": [],
                    "scope_reason": None,
                },
            ),
            self.synthetic_event(
                "all-domain",
                "2026-07-12T10:05:20Z",
                "extend",
                "EXTENDED",
                "all-domain",
                requested_scopes={
                    "files": [],
                    "trees": [],
                    "project_files": False,
                    "backlog": False,
                    "all_files": True,
                    "file_domain": "all_files",
                    "resources": [],
                    "scope_reason": "source migration",
                },
            ),
            self.synthetic_event("release", "2026-07-12T10:06:00Z", "release", "RELEASED", "blocked"),
            self.synthetic_event(
                "isolate",
                "2026-07-12T10:10:00Z",
                "acquire",
                "ISOLATE",
                "isolated",
                mode="isolated",
            ),
            self.synthetic_event(
                "shared-required",
                "2026-07-12T10:10:30Z",
                "acquire",
                "PRIMARY_REQUIRED",
                "shared-required",
                active_claim_count=1,
                shared_checkout_claimed=False,
            ),
            self.synthetic_event("isolate-release", "2026-07-12T10:11:00Z", "release", "RELEASED", "isolated"),
            self.synthetic_event("recover", "2026-07-12T10:20:00Z", "acquire", "RECOVER", "recovery"),
            self.synthetic_event("recover-release", "2026-07-12T10:21:00Z", "release", "RELEASED", "recovery"),
        ]
        self.write_daily_events("2026-07-12", events)
        environment = {"AGENT_CLAIM_TEST_NOW": "2026-07-13T10:00:00Z"}
        registry_before = self.registry_path().read_bytes() if self.registry_path().exists() else None
        journal_before = (self.hot_directory() / "2026-07-12.jsonl").read_bytes()

        completed = self.claim("report", "--since", "2d", environment=environment)

        self.assertEqual(0, completed.returncode, completed.stderr)
        report = json.loads(completed.stdout)
        self.assertEqual(2, report["schema_version"])
        metrics = report["metrics"]
        self.assertEqual(
            {"primary": 1, "isolated": 1, "recovery": 1},
            metrics["successful_acquisitions"],
        )
        self.assertEqual(2, metrics["wait_attempt_count"])
        self.assertEqual(2, metrics["outcome_counts"]["CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED"])
        self.assertEqual(2, metrics["raw_outcome_counts"]["WAIT"])
        self.assertEqual(1, metrics["outcome_counts"]["SHARED_CHECKOUT_REQUIRED"])
        self.assertEqual(1, metrics["raw_outcome_counts"]["PRIMARY_REQUIRED"])
        self.assertEqual(1, len(metrics["wait_episodes"]))
        self.assertEqual(300.0, metrics["wait_episodes"][0]["duration_seconds"])
        self.assertEqual("src/one.py", metrics["top_contention"]["exact_files"][0]["scope"])
        self.assertEqual("src/one.py", metrics["top_contention"]["trees"][0]["scope"])
        self.assertEqual("port:3000", metrics["top_contention"]["resources"][0]["scope"])
        self.assertEqual(60.0, metrics["claim_duration_seconds"]["median"])
        self.assertEqual("source migration", metrics["broad_scopes"]["reasons"][0]["scope"])
        self.assertEqual(
            {"all_files": 1, "backlog": 1, "project_files": 1},
            metrics["broad_scopes"]["file_domains"],
        )
        self.assertEqual("merge:integration:main", metrics["integration_resources"][0]["scope"])
        self.assertEqual(1, metrics["journal_warning_count"])
        self.assertEqual(registry_before, self.registry_path().read_bytes() if self.registry_path().exists() else None)
        self.assertEqual(journal_before, (self.hot_directory() / "2026-07-12.jsonl").read_bytes())

    def test_report_keeps_ambiguous_legacy_primary_required_outcome_raw(self) -> None:
        event = self.synthetic_event(
            "ambiguous-primary-required",
            "2026-07-12T10:00:00Z",
            "acquire",
            "PRIMARY_REQUIRED",
            "ambiguous",
            active_claim_count=1,
        )
        self.write_daily_events("2026-07-12", [event])

        completed = self.claim(
            "report",
            "--since",
            "2d",
            environment={"AGENT_CLAIM_TEST_NOW": "2026-07-13T10:00:00Z"},
        )

        self.assertEqual(0, completed.returncode, completed.stderr)
        report = self.output(completed)
        self.assertEqual(1, report["metrics"]["outcome_counts"]["PRIMARY_REQUIRED"])
        self.assertEqual(
            "legacy PRIMARY_REQUIRED lacks deterministic shared-checkout ownership evidence",
            report["metrics"]["outcome_normalization_gaps"][0]["detail"],
        )

    def test_daily_boundaries_use_utc_not_local_daylight_saving(self) -> None:
        event = self.synthetic_event("old", "2026-11-01T23:30:00Z", "acquire", "PRIMARY", "old")
        old = self.write_daily_events("2026-11-01", [event])
        current = self.write_daily_events(
            "2026-11-03",
            [self.synthetic_event("current", "2026-11-03T00:01:00Z", "heartbeat", "HEARTBEAT", "current")],
        )

        completed = self.claim(
            "maintain-journal",
            "--hot-days",
            "2",
            environment={"AGENT_CLAIM_TEST_NOW": "2026-11-03T00:05:00Z", "TZ": "America/Toronto"},
        )

        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertFalse(old.exists())
        self.assertTrue(current.exists())


if __name__ == "__main__":
    unittest.main()
