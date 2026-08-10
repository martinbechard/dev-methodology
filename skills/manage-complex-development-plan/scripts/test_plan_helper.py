# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies the deterministic complex-development plan helper against the installed hierarchy package.

from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path
from types import ModuleType
from typing import Any
from unittest.mock import patch


HELPER_PATH = Path(__file__).with_name("plan.py")


class PlanHelperTests(unittest.TestCase):
    """Exercise the helper CLI, safe-path boundary, recovery contract, and real package APIs."""

    def setUp(self) -> None:
        """Create one isolated absolute workspace for each helper scenario."""
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.workspace = Path(self.temporary_directory.name).resolve()
        self.task_id = "task-123"
        self.plan_name = "delivery"

    def _definition_path(
        self,
        *,
        tasks: list[dict[str, object]] | None = None,
        filename: str = "definition.json",
    ) -> Path:
        path = self.workspace / filename
        path.write_text(
            json.dumps(
                {
                    "schema": "dev-methodology-complex-plan-input",
                    "version": 1,
                    "title": "Delivery plan",
                    "objective": "Deliver the accepted change",
                    "tasks": tasks
                    or [
                        {
                            "title": "Discovery",
                            "dependsOn": [],
                            "evidence": ["work-item:task-123"],
                            "complete": False,
                            "children": [
                                {
                                    "title": "Inspect callers",
                                    "dependsOn": [],
                                    "evidence": [],
                                    "complete": False,
                                    "children": [],
                                }
                            ],
                        },
                        {
                            "title": "Implementation",
                            "dependsOn": ["Discovery"],
                            "evidence": [],
                            "complete": False,
                            "children": [],
                        },
                    ],
                }
            )
            + "\n",
            encoding="utf-8",
        )
        return path

    def _base_arguments(self, *, plan_name: str | None = None) -> list[str]:
        return [
            "--workspace",
            str(self.workspace),
            "--root-task-id",
            self.task_id,
            "--plan-name",
            plan_name or self.plan_name,
        ]

    def _invoke(
        self,
        *arguments: str,
        expected_exit: int | None = 0,
        interpreter: str | None = None,
    ) -> tuple[dict[str, object], subprocess.CompletedProcess[str]]:
        completed = subprocess.run(
            [interpreter or sys.executable, str(HELPER_PATH), *arguments],
            check=False,
            capture_output=True,
            text=True,
        )
        if expected_exit is not None:
            self.assertEqual(expected_exit, completed.returncode, completed.stderr)
        try:
            result = json.loads(completed.stdout)
        except json.JSONDecodeError as error:
            self.fail(
                f"Helper did not return JSON: {completed.stdout!r}; {completed.stderr!r}; {error}"
            )
        self.assertIsInstance(result, dict)
        return result, completed

    def _create(
        self, *, definition: Path | None = None, plan_name: str | None = None
    ) -> dict[str, object]:
        result, _ = self._invoke(
            *self._base_arguments(plan_name=plan_name),
            "create",
            "--definition",
            str(definition or self._definition_path()),
        )
        self.assertEqual("CREATED", result["outcome"])
        return result

    def _plan_paths(self, *, plan_name: str | None = None) -> tuple[Path, Path]:
        root = self.workspace / ".codex" / "plans" / self.task_id
        name = plan_name or self.plan_name
        return root / f"{name}.json", root / f"{name}.html"

    def test_capability_check_imports_all_public_apis_and_system_python_can_reexec(
        self,
    ) -> None:
        system_python = shutil.which("python3")
        self.assertIsNotNone(system_python)
        result, completed = self._invoke(
            "capabilities",
            interpreter=system_python,
        )

        self.assertEqual("CAPABILITIES_AVAILABLE", result["outcome"])
        self.assertEqual(
            ["create_hierarchy_plan", "render_hierarchy_html", "update_hierarchy_plan"],
            result["capabilities"],
        )
        self.assertRegex(str(result["package_version"]), r"^\d+\.\d+\.\d+")
        self.assertEqual("", completed.stderr)

    def test_create_and_single_updates_keep_json_and_html_synchronized(self) -> None:
        created = self._create()
        plan_path, html_path = self._plan_paths()

        self.assertEqual(str(plan_path.resolve()), created["plan_path"])
        self.assertEqual(str(html_path.resolve()), created["html_path"])
        self.assertTrue(plan_path.is_file())
        self.assertTrue(html_path.is_file())
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        self.assertEqual(
            "Objective: Deliver the accepted change", plan["items"][0]["text"]
        )
        self.assertEqual("Discovery", plan["items"][1]["text"])
        discovery_children = plan["items"][1]["children"]
        self.assertEqual(
            "Evidence reference: work-item:task-123", discovery_children[0]["text"]
        )
        self.assertTrue(discovery_children[0]["complete"])

        for target, operation, text in (
            ("Discovery", "--add-child", "Confirm runtime capability"),
            ("Implementation", "--add-peer-after", "Documentation"),
        ):
            before_json = hashlib.sha256(plan_path.read_bytes()).hexdigest()
            before_html = hashlib.sha256(html_path.read_bytes()).hexdigest()
            result, _ = self._invoke(
                *self._base_arguments(),
                "update",
                "--target",
                target,
                operation,
                text,
            )
            self.assertEqual("UPDATED", result["outcome"])
            self.assertEqual(before_json, result["before"]["json_sha256"])
            self.assertEqual(before_html, result["before"]["html_sha256"])
            self.assertNotEqual(result["before"], result["after"])

        completed, _ = self._invoke(
            *self._base_arguments(),
            "update",
            "--target",
            "Discovery",
            "--complete",
        )
        self.assertEqual("UPDATED", completed["outcome"])
        inspected, _ = self._invoke(*self._base_arguments(), "inspect")
        self.assertEqual("SYNCED", inspected["outcome"])
        self.assertTrue(inspected["synchronized"])
        self.assertRegex(str(inspected["reconciliation_token"]), r"^[0-9a-f]{64}$")
        html = html_path.read_text(encoding="utf-8")
        for text in ("Confirm runtime capability", "Documentation"):
            self.assertIn(text, html)

        history_root = plan_path.parent / ".history" / self.plan_name
        operations = [entry for entry in history_root.iterdir() if entry.is_dir()]
        self.assertEqual(3, len(operations))
        for operation in operations:
            self.assertTrue((operation / "before.json").is_file())
            self.assertTrue((operation / "before.html").is_file())
            self.assertTrue((operation / "result.json").is_file())

    def test_invalid_paths_targets_and_multi_action_requests_do_not_change_artifacts(
        self,
    ) -> None:
        invalid_definition = self.workspace / "invalid-definition.json"
        invalid_definition.write_text("{}\n", encoding="utf-8")
        invalid_schema, _ = self._invoke(
            *self._base_arguments(plan_name="invalid-definition"),
            "create",
            "--definition",
            str(invalid_definition),
            expected_exit=2,
        )
        self.assertEqual("INVALID_DEFINITION", invalid_schema["outcome"])
        invalid_plan, invalid_html = self._plan_paths(plan_name="invalid-definition")
        self.assertFalse(invalid_plan.exists())
        self.assertFalse(invalid_html.exists())

        unsafe_name, _ = self._invoke(
            "--workspace",
            str(self.workspace),
            "--root-task-id",
            self.task_id,
            "--plan-name",
            "../escape",
            "inspect",
            expected_exit=2,
        )
        self.assertEqual("INVALID_NAME", unsafe_name["outcome"])

        duplicate_definition = self._definition_path(
            tasks=[
                {
                    "title": "Duplicate",
                    "dependsOn": [],
                    "evidence": [],
                    "complete": False,
                    "children": [],
                },
                {
                    "title": "Duplicate",
                    "dependsOn": [],
                    "evidence": [],
                    "complete": False,
                    "children": [],
                },
            ]
        )
        self._create(definition=duplicate_definition)
        plan_path, html_path = self._plan_paths()
        before = (plan_path.read_bytes(), html_path.read_bytes())

        for target in ("Duplicate", "9.9"):
            result, _ = self._invoke(
                *self._base_arguments(),
                "update",
                "--target",
                target,
                "--complete",
                expected_exit=2,
            )
            self.assertIn(result["outcome"], {"AMBIGUOUS_TARGET", "MISSING_TARGET"})
            self.assertEqual(before, (plan_path.read_bytes(), html_path.read_bytes()))

        result, _ = self._invoke(
            *self._base_arguments(),
            "update",
            "--target",
            "1",
            "--complete",
            "--add-child",
            "Not allowed",
            expected_exit=2,
        )
        self.assertEqual("INVALID_REQUEST", result["outcome"])
        self.assertEqual(before, (plan_path.read_bytes(), html_path.read_bytes()))

        relative, _ = self._invoke(
            "--workspace",
            ".",
            "--root-task-id",
            self.task_id,
            "--plan-name",
            self.plan_name,
            "inspect",
            expected_exit=2,
        )
        self.assertEqual("INVALID_WORKSPACE", relative["outcome"])

        outside_definition = (
            Path(tempfile.gettempdir()) / "outside-plan-definition.json"
        )
        outside_definition.write_text("{}\n", encoding="utf-8")
        self.addCleanup(outside_definition.unlink, missing_ok=True)
        escaped, _ = self._invoke(
            *self._base_arguments(plan_name="escaped"),
            "create",
            "--definition",
            str(outside_definition),
            expected_exit=2,
        )
        self.assertEqual("PATH_OUTSIDE_WORKSPACE", escaped["outcome"])

        traversal_definition = (
            self.workspace / ".." / f"{self.workspace.name}-outside.json"
        )
        traversal_definition.write_text("{}\n", encoding="utf-8")
        self.addCleanup(traversal_definition.unlink, missing_ok=True)
        traversed, _ = self._invoke(
            *self._base_arguments(plan_name="traversed"),
            "create",
            "--definition",
            str(traversal_definition),
            expected_exit=2,
        )
        self.assertEqual("PATH_OUTSIDE_WORKSPACE", traversed["outcome"])

        symlink_workspace = self.workspace / "symlink-workspace"
        symlink_workspace.mkdir()
        (symlink_workspace / ".codex").symlink_to(
            self.workspace / ".codex", target_is_directory=True
        )
        symlink_result, _ = self._invoke(
            "--workspace",
            str(symlink_workspace),
            "--root-task-id",
            self.task_id,
            "--plan-name",
            "symlinked",
            "create",
            "--definition",
            str(symlink_workspace / "definition.json"),
            expected_exit=2,
        )
        self.assertEqual("SYMLINK_PATH_REJECTED", symlink_result["outcome"])

    def test_invalid_plan_and_html_drift_require_deterministic_reconciliation(
        self,
    ) -> None:
        self._create()
        plan_path, html_path = self._plan_paths()
        html_path.write_text("drift\n", encoding="utf-8")

        inspected, _ = self._invoke(*self._base_arguments(), "inspect", expected_exit=4)
        self.assertEqual("DRIFT", inspected["outcome"])
        blocked, _ = self._invoke(
            *self._base_arguments(),
            "update",
            "--target",
            "Discovery",
            "--complete",
            expected_exit=4,
        )
        self.assertEqual("RECONCILIATION_REQUIRED", blocked["outcome"])

        reconciled, _ = self._invoke(*self._base_arguments(), "reconcile")
        self.assertEqual("RECONCILED", reconciled["outcome"])
        self.assertTrue(reconciled["synchronized"])
        inspected, _ = self._invoke(*self._base_arguments(), "inspect")
        self.assertEqual("SYNCED", inspected["outcome"])

        original_html = html_path.read_bytes()
        plan_path.write_text("{invalid\n", encoding="utf-8")
        invalid, _ = self._invoke(*self._base_arguments(), "inspect", expected_exit=2)
        self.assertEqual("INVALID_PLAN", invalid["outcome"])
        self.assertEqual(original_html, html_path.read_bytes())

    def test_post_dispatch_exception_is_uncertain_and_blocks_retry_until_reconciliation(
        self,
    ) -> None:
        self._create()
        module = self._load_helper_module()
        actual_api = module._load_api()

        def fail_after_html_change(*_args: object, **_kwargs: object) -> Path:
            _, html_path = self._plan_paths()
            html_path.write_text("partially changed\n", encoding="utf-8")
            raise RuntimeError("simulated failure after mutation began")

        failing_api = replace(actual_api, update_hierarchy_plan=fail_after_html_change)
        with patch.object(module, "_load_api", return_value=failing_api):
            exit_code, uncertain = module.execute(
                [
                    *self._base_arguments(),
                    "update",
                    "--target",
                    "Discovery",
                    "--complete",
                ]
            )

        self.assertEqual(4, exit_code)
        self.assertEqual("UNCERTAIN_UPDATE", uncertain["outcome"])
        self.assertTrue(uncertain["inspect_required"])
        self.assertIn("simulated failure", uncertain["error"])
        history_result = Path(str(uncertain["history_path"])) / "result.json"
        self.assertEqual(
            "UNCERTAIN_UPDATE", json.loads(history_result.read_text())["outcome"]
        )

        retry, _ = self._invoke(
            *self._base_arguments(),
            "update",
            "--target",
            "Discovery",
            "--complete",
            expected_exit=4,
        )
        self.assertEqual("RECONCILIATION_REQUIRED", retry["outcome"])
        self.assertIn(uncertain["operation_id"], retry["unresolved_operations"])

        reconciled, _ = self._invoke(*self._base_arguments(), "reconcile")
        self.assertEqual("RECONCILED", reconciled["outcome"])
        self.assertIn(uncertain["operation_id"], reconciled["reconciles"])
        completed, _ = self._invoke(
            *self._base_arguments(),
            "update",
            "--target",
            "Discovery",
            "--complete",
        )
        self.assertEqual("UPDATED", completed["outcome"])

    def test_finalize_requires_explicit_retention_and_removes_only_the_selected_plan(
        self,
    ) -> None:
        self._create()
        self._create(
            definition=self._definition_path(filename="other-definition.json"),
            plan_name="other",
        )

        missing_choice, _ = self._invoke(
            *self._base_arguments(),
            "finalize",
            expected_exit=2,
        )
        self.assertEqual("INVALID_REQUEST", missing_choice["outcome"])

        incomplete, _ = self._invoke(
            *self._base_arguments(),
            "finalize",
            "--retention",
            "keep",
            expected_exit=4,
        )
        self.assertEqual("FINALIZATION_INCOMPLETE", incomplete["outcome"])
        self.assertIn("Discovery", incomplete["incomplete_items"])

        for target in ("Inspect callers", "Discovery", "Implementation"):
            result, _ = self._invoke(
                *self._base_arguments(),
                "update",
                "--target",
                target,
                "--complete",
            )
            self.assertEqual("UPDATED", result["outcome"])

        kept, _ = self._invoke(
            *self._base_arguments(),
            "finalize",
            "--retention",
            "keep",
        )
        self.assertEqual("FINALIZED", kept["outcome"])
        plan_path, html_path = self._plan_paths()
        self.assertTrue(plan_path.exists())
        self.assertTrue(html_path.exists())

        removed, _ = self._invoke(
            *self._base_arguments(),
            "finalize",
            "--retention",
            "remove",
        )
        self.assertEqual("CLEANED", removed["outcome"])
        self.assertFalse(plan_path.exists())
        self.assertFalse(html_path.exists())
        other_plan, other_html = self._plan_paths(plan_name="other")
        self.assertTrue(other_plan.exists())
        self.assertTrue(other_html.exists())

    def test_partial_cleanup_failure_is_uncertain_and_requires_reconciliation(
        self,
    ) -> None:
        self._create()
        for target in ("Inspect callers", "Discovery", "Implementation"):
            self._invoke(
                *self._base_arguments(),
                "update",
                "--target",
                target,
                "--complete",
            )
        module = self._load_helper_module()

        def fail_after_first_removal(context: Any) -> list[str]:
            context.plan_path.unlink()
            raise OSError("simulated cleanup interruption")

        with patch.object(module, "_remove_plan", side_effect=fail_after_first_removal):
            exit_code, uncertain = module.execute(
                [*self._base_arguments(), "finalize", "--retention", "remove"]
            )

        self.assertEqual(4, exit_code)
        self.assertEqual("UNCERTAIN_CLEANUP", uncertain["outcome"])
        self.assertFalse(uncertain["retry_allowed"])
        self.assertTrue(uncertain["reconciliation_required"])
        self.assertIn("simulated cleanup interruption", uncertain["cause"])
        self.assertFalse(self._plan_paths()[0].exists())
        self.assertTrue(self._plan_paths()[1].exists())

    def _load_helper_module(self) -> ModuleType:
        specification = importlib.util.spec_from_file_location(
            "complex_plan_helper", HELPER_PATH
        )
        if specification is None or specification.loader is None:
            raise RuntimeError(f"Unable to load helper: {HELPER_PATH}")
        module = importlib.util.module_from_spec(specification)
        sys.modules[specification.name] = module
        self.addCleanup(sys.modules.pop, specification.name, None)
        specification.loader.exec_module(module)
        return module


if __name__ == "__main__":
    unittest.main()
