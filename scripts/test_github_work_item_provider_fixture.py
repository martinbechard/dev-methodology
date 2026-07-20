# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
"""Focused mocked-provider coverage for the split GitHub work-item skills."""

import argparse
import importlib.util
import json
import unittest
from pathlib import Path
from typing import Any, Dict


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = REPOSITORY_ROOT / "evals" / "projects" / "github-work-item-provider"


def load_provider_module() -> Any:
    spec = importlib.util.spec_from_file_location(
        "mock_github_provider", FIXTURE_ROOT / "mock_github.py"
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load mock GitHub provider fixture")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PROVIDER = load_provider_module()


def fresh_state() -> Dict[str, Any]:
    return json.loads((FIXTURE_ROOT / "provider-state.json").read_text(encoding="utf-8"))


def arguments(command: str, repository: str, **values: Any) -> argparse.Namespace:
    defaults = {
        "command": command,
        "repository": repository,
        "query": None,
        "number": None,
        "title": None,
        "body": None,
        "label": [],
        "assignee": [],
        "add_label": [],
        "comment": None,
        "issue_state": None,
    }
    defaults.update(values)
    return argparse.Namespace(**defaults)


class GitHubWorkItemProviderFixtureTests(unittest.TestCase):
    def test_create_search_duplicate_and_no_shadow_file(self) -> None:
        state = fresh_state()
        search = PROVIDER.perform(
            arguments("search", "acme/widgets", query="Retry webhook delivery"), state
        )
        self.assertEqual([7], [issue["number"] for issue in search["issues"]])
        self.assertEqual(1, len(state["repositories"]["acme/widgets"]["issues"]))

        created = PROVIDER.perform(
            arguments(
                "create",
                "acme/widgets",
                title="Add idempotency key validation",
                body="Type: Feature\nRequirements: Validate keys.\nAcceptance Criteria: Reject duplicates.",
                label=["feature", "ready"],
                assignee=["worker"],
            ),
            state,
        )["issue"]
        self.assertEqual(8, created["number"])
        self.assertEqual(["worker"], created["assignees"])
        self.assertEqual(["feature", "ready"], created["labels"])
        self.assertFalse((FIXTURE_ROOT / "backlog").exists())

    def test_manage_update_dependency_block_reopen_and_close(self) -> None:
        state = fresh_state()
        created = PROVIDER.perform(
            arguments(
                "create",
                "acme/widgets",
                title="Add idempotency key validation",
                body="Lifecycle: READY",
                label=["feature", "ready"],
                assignee=["worker"],
            ),
            state,
        )["issue"]
        number = created["number"]
        for label, comment, issue_state in (
            ("running", "Task synthetic-task-42 phase Implementing", None),
            ("blocked", "Blocked by acme/widgets issue 7", None),
            ("running", "Dependency cleared; lifecycle RUNNING", None),
            ("terminal", "Commit abc123 reviewed, checks passed, observed on main", "closed"),
            ("correction", "Reopened with correction authority", "open"),
            ("terminal", "Corrected commit observed on main; claim released", "closed"),
        ):
            observed = PROVIDER.perform(
                arguments(
                    "update",
                    "acme/widgets",
                    number=number,
                    add_label=[label],
                    comment=comment,
                    issue_state=issue_state,
                ),
                state,
            )["issue"]
            self.assertIn(label, observed["labels"])
            self.assertEqual(issue_state or observed["state"], observed["state"])
        self.assertEqual("closed", observed["state"])
        self.assertIn("acme/widgets issue 7", "\n".join(observed["comments"]))

    def test_authentication_permission_and_partial_mutation_boundaries(self) -> None:
        state = fresh_state()
        with self.assertRaisesRegex(PROVIDER.ProviderError, "authentication unavailable"):
            PROVIDER.perform(arguments("search", "auth/widgets", query="anything"), state)
        with self.assertRaisesRegex(PROVIDER.ProviderError, "mutation permission unavailable"):
            PROVIDER.perform(
                arguments(
                    "create",
                    "readonly/widgets",
                    title="Forbidden",
                    body="Must not be created",
                ),
                state,
            )
        self.assertEqual([], state["repositories"]["readonly/widgets"]["issues"])

        with self.assertRaisesRegex(PROVIDER.ProviderError, "ambiguous partial update"):
            PROVIDER.perform(
                arguments(
                    "update",
                    "acme/partial",
                    number=3,
                    body="Delivery reference: pull request 55",
                    add_label=["awaiting-review"],
                ),
                state,
            )
        partial = state["repositories"]["acme/partial"]["issues"][0]
        self.assertIn("pull request 55", partial["body"])
        self.assertNotIn("awaiting-review", partial["labels"])
        reconciled = PROVIDER.perform(
            arguments(
                "update",
                "acme/partial",
                number=3,
                add_label=["awaiting-review"],
            ),
            state,
        )["issue"]
        self.assertIn("awaiting-review", reconciled["labels"])
        self.assertEqual("open", reconciled["state"])
        self.assertFalse((FIXTURE_ROOT / "backlog").exists())


if __name__ == "__main__":
    unittest.main()
