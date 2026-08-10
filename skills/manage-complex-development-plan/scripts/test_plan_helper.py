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

    def _complete_default_plan(self, *, plan_name: str | None = None) -> None:
        for target in ("Inspect callers", "Discovery", "Implementation"):
            result, _ = self._invoke(
                *self._base_arguments(plan_name=plan_name),
                "update",
                "--target",
                target,
                "--complete",
            )
            self.assertEqual("UPDATED", result["outcome"])

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

    def test_capability_validation_checks_every_supplied_call_shape(self) -> None:
        module = self._load_helper_module()

        def valid_create(
            source: object,
            *,
            title: str,
            output_filename: str,
            output_folder: Path,
            completed_items: tuple[str, ...],
        ) -> Path:
            return output_folder / Path(output_filename).with_suffix(".json")

        def valid_render(
            source: object,
            *,
            title: str,
            theme: str,
            themes_folder: str | None,
            numbering: bool,
            checkboxes: bool,
            completed_items: tuple[str, ...],
            output_filename: str | None = None,
            output_folder: Path | None = None,
        ) -> str:
            return "<html></html>"

        def valid_update(
            plan_path: Path,
            target: str,
            *,
            completed: bool | None = None,
            add_child: str | None = None,
            add_peer_after: str | None = None,
        ) -> Path:
            return plan_path

        valid = {
            "create_hierarchy_plan": valid_create,
            "render_hierarchy_html": valid_render,
            "update_hierarchy_plan": valid_update,
        }
        signatures = module._validate_api_contract(valid)
        self.assertEqual(set(valid), set(signatures))

        def create_without_title(
            source: object,
            *,
            output_filename: str,
            output_folder: Path,
            completed_items: tuple[str, ...],
        ) -> Path:
            return output_folder / Path(output_filename).with_suffix(".json")

        def render_without_themes_folder(
            source: object,
            *,
            title: str,
            theme: str,
            numbering: bool,
            checkboxes: bool,
            completed_items: tuple[str, ...],
            output_filename: str | None = None,
            output_folder: Path | None = None,
        ) -> str:
            return "<html></html>"

        def update_with_keyword_only_target(
            plan_path: Path,
            *,
            target: str,
            completed: bool | None = None,
            add_child: str | None = None,
            add_peer_after: str | None = None,
        ) -> Path:
            return plan_path

        for function_name, incompatible in (
            ("create_hierarchy_plan", create_without_title),
            ("render_hierarchy_html", render_without_themes_folder),
            ("update_hierarchy_plan", update_with_keyword_only_target),
        ):
            with self.subTest(function_name=function_name):
                functions = dict(valid)
                functions[function_name] = incompatible
                with self.assertRaises(module._PlanHelperError) as raised:
                    module._validate_api_contract(functions)
                self.assertEqual("CAPABILITY_UNAVAILABLE", raised.exception.outcome)

        def unreadable_signature(*args: object, **kwargs: object) -> Path:
            return Path("plan.json")

        unreadable_signature.__signature__ = "invalid"  # type: ignore[attr-defined]
        functions = dict(valid)
        functions["create_hierarchy_plan"] = unreadable_signature
        with self.assertRaises(module._PlanHelperError) as raised:
            module._validate_api_contract(functions)
        self.assertEqual("CAPABILITY_UNAVAILABLE", raised.exception.outcome)
        self.assertIn(
            "create_hierarchy_plan", raised.exception.details["incompatibilities"]
        )

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
        operations = sorted(entry for entry in history_root.iterdir() if entry.is_dir())
        self.assertEqual(4, len(operations))
        for operation in operations:
            self.assertTrue((operation / "operation.json").is_file())
            self.assertTrue((operation / "result.json").is_file())
            self.assertTrue(
                json.loads((operation / "result.json").read_text())["terminal"]
            )
        self.assertFalse((operations[0] / "before.json").exists())
        self.assertFalse((operations[0] / "before.html").exists())
        for operation in operations[1:]:
            self.assertTrue((operation / "before.json").is_file())
            self.assertTrue((operation / "before.html").is_file())

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

    def test_stale_dotted_target_requires_the_expected_current_title(self) -> None:
        definition = self._definition_path(
            tasks=[
                {
                    "title": title,
                    "dependsOn": [],
                    "evidence": [],
                    "complete": False,
                    "children": [],
                }
                for title in ("Alpha", "Beta", "Gamma")
            ]
        )
        self._create(definition=definition)
        self._invoke(
            *self._base_arguments(),
            "update",
            "--target",
            "Alpha",
            "--add-peer-after",
            "Inserted workstream",
        )
        plan_path, html_path = self._plan_paths()
        before = (plan_path.read_bytes(), html_path.read_bytes())

        missing_guard, _ = self._invoke(
            *self._base_arguments(),
            "update",
            "--target",
            "4",
            "--complete",
            expected_exit=2,
        )
        self.assertEqual("EXPECTED_TITLE_REQUIRED", missing_guard["outcome"])

        stale, _ = self._invoke(
            *self._base_arguments(),
            "update",
            "--target",
            "4",
            "--expected-title",
            "Gamma",
            "--complete",
            expected_exit=2,
        )
        self.assertEqual("STALE_TARGET", stale["outcome"])
        self.assertEqual("Beta", stale["observed_title"])
        self.assertEqual(before, (plan_path.read_bytes(), html_path.read_bytes()))

        current, _ = self._invoke(
            *self._base_arguments(),
            "update",
            "--target",
            "5",
            "--expected-title",
            "Gamma",
            "--complete",
        )
        self.assertEqual("UPDATED", current["outcome"])

    def test_metadata_prefixes_are_reserved_for_structural_references(self) -> None:
        for prefix in ("Dependency reference: ", "Evidence reference: "):
            with self.subTest(prefix=prefix):
                plan_name = (
                    "dependency-prefix"
                    if prefix.startswith("Dependency")
                    else "evidence-prefix"
                )
                definition = self._definition_path(
                    tasks=[
                        {
                            "title": f"{prefix}actionable",
                            "dependsOn": [],
                            "evidence": [],
                            "complete": False,
                            "children": [],
                        }
                    ],
                    filename=f"{plan_name}.json",
                )
                rejected, _ = self._invoke(
                    *self._base_arguments(plan_name=plan_name),
                    "create",
                    "--definition",
                    str(definition),
                    expected_exit=2,
                )
                self.assertEqual("RESERVED_ACTION_TEXT", rejected["outcome"])

        self._create()
        plan_path, html_path = self._plan_paths()
        before = (plan_path.read_bytes(), html_path.read_bytes())
        for operation, text in (
            ("--add-child", "Dependency reference: discovered action"),
            ("--add-peer-after", "Evidence reference: discovered action"),
        ):
            rejected, _ = self._invoke(
                *self._base_arguments(),
                "update",
                "--target",
                "Implementation",
                operation,
                text,
                expected_exit=2,
            )
            self.assertEqual("RESERVED_ACTION_TEXT", rejected["outcome"])
            self.assertEqual(before, (plan_path.read_bytes(), html_path.read_bytes()))

        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        metadata = plan["items"][1]["children"][0]
        self.assertTrue(metadata["text"].startswith("Evidence reference: "))
        metadata["complete"] = False
        plan_path.write_text(json.dumps(plan) + "\n", encoding="utf-8")
        invalid, _ = self._invoke(
            *self._base_arguments(),
            "finalize",
            "--retention",
            "keep",
            expected_exit=2,
        )
        self.assertEqual("INVALID_PLAN", invalid["outcome"])

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

        inspected, _ = self._invoke(*self._base_arguments(), "inspect", expected_exit=4)
        reconciled, _ = self._invoke(
            *self._base_arguments(),
            "reconcile",
            "--recovery-token",
            str(inspected["recovery_token"]),
        )
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

        inspected, _ = self._invoke(*self._base_arguments(), "inspect", expected_exit=4)
        reconciled, _ = self._invoke(
            *self._base_arguments(),
            "reconcile",
            "--recovery-token",
            str(inspected["recovery_token"]),
        )
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

    def test_interrupted_updates_remain_unresolved_before_and_after_artifact_changes(
        self,
    ) -> None:
        self._create()
        module = self._load_helper_module()
        actual_api = module._load_api()

        for stop_after_change in (False, True):
            with self.subTest(stop_after_change=stop_after_change):

                def stop_during_dispatch(*args: object, **kwargs: object) -> Path:
                    if stop_after_change:
                        actual_api.update_hierarchy_plan(*args, **kwargs)
                    raise SystemExit("simulated process stop")

                interrupted_api = replace(
                    actual_api, update_hierarchy_plan=stop_during_dispatch
                )
                with patch.object(module, "_load_api", return_value=interrupted_api):
                    with self.assertRaises(SystemExit):
                        module.execute(
                            [
                                *self._base_arguments(),
                                "update",
                                "--target",
                                "Implementation",
                                "--complete" if stop_after_change else "--incomplete",
                            ]
                        )

                if stop_after_change:
                    plan_path, _ = self._plan_paths()
                    history_root = plan_path.parent / ".history" / self.plan_name
                    latest_operation = sorted(history_root.iterdir())[-1]
                    (latest_operation / "result.json").unlink()

                inspected, _ = self._invoke(
                    *self._base_arguments(), "inspect", expected_exit=4
                )
                self.assertEqual("RECOVERY_REQUIRED", inspected["outcome"])
                self.assertEqual("SYNCED", inspected["artifact_state"])
                self.assertTrue(inspected["unresolved_operations"])
                latest_detail = inspected["unresolved_details"][-1]
                self.assertEqual(
                    "missing" if stop_after_change else "pending",
                    latest_detail["result_state"],
                )
                recovered, _ = self._invoke(
                    *self._base_arguments(),
                    "reconcile",
                    "--recovery-token",
                    str(inspected["recovery_token"]),
                )
                self.assertEqual("RECONCILED", recovered["outcome"])
                self.assertTrue(recovered["reconciles"])
                settled, _ = self._invoke(*self._base_arguments(), "inspect")
                self.assertEqual("SYNCED", settled["outcome"])
                self.assertFalse(settled["unresolved_operations"])

    def test_missing_malformed_and_pending_results_are_unresolved_until_reconciled(
        self,
    ) -> None:
        self._create()
        module = self._load_helper_module()
        arguments = module._parser().parse_args([*self._base_arguments(), "inspect"])
        context = module._context(arguments)

        for state, expected_state in (
            ("missing", "missing"),
            ("malformed-json", "malformed"),
            ("malformed-terminal", "malformed"),
            ("pending", "pending"),
        ):
            with self.subTest(state=state):
                operation_id, operation_path = module._start_operation(
                    context,
                    "update",
                    {"target": "Implementation", "mutation": "completed"},
                )
                result_path = operation_path / "result.json"
                if state == "missing":
                    result_path.unlink()
                elif state == "malformed-json":
                    result_path.write_text("{invalid\n", encoding="utf-8")
                elif state == "malformed-terminal":
                    result_path.write_text(
                        json.dumps({"operation_id": operation_id, "terminal": True})
                        + "\n",
                        encoding="utf-8",
                    )

                inspected, _ = self._invoke(
                    *self._base_arguments(), "inspect", expected_exit=4
                )
                self.assertIn(operation_id, inspected["unresolved_operations"])
                detail = next(
                    item
                    for item in inspected["unresolved_details"]
                    if item["operation_id"] == operation_id
                )
                self.assertEqual(expected_state, detail["result_state"])
                recovered, _ = self._invoke(
                    *self._base_arguments(),
                    "reconcile",
                    "--recovery-token",
                    str(inspected["recovery_token"]),
                )
                self.assertIn(operation_id, recovered["reconciles"])
                settled, _ = self._invoke(*self._base_arguments(), "inspect")
                self.assertEqual("SYNCED", settled["outcome"])
                self.assertFalse(settled["unresolved_operations"])

    def test_interrupted_create_recovers_html_only_json_only_and_synchronized_states(
        self,
    ) -> None:
        module = self._load_helper_module()
        actual_api = module._load_api()

        for state in ("html-only", "json-only", "synchronized"):
            with self.subTest(state=state):
                plan_name = state.replace("-", "")
                definition = self._definition_path(
                    filename=f"{plan_name}-definition.json"
                )

                def create_then_stop(*args: object, **kwargs: object) -> Path:
                    if state == "html-only":
                        html_path = Path(str(kwargs["output_folder"])) / str(
                            kwargs["output_filename"]
                        )
                        html_path.write_text("partial HTML\n", encoding="utf-8")
                        raise RuntimeError("stop after HTML")
                    plan_path = actual_api.create_hierarchy_plan(*args, **kwargs)
                    if state == "json-only":
                        plan_path.with_suffix(".html").unlink()
                    raise SystemExit(f"stop with {state}")

                interrupted_api = replace(
                    actual_api, create_hierarchy_plan=create_then_stop
                )
                with patch.object(module, "_load_api", return_value=interrupted_api):
                    arguments = [
                        *self._base_arguments(plan_name=plan_name),
                        "create",
                        "--definition",
                        str(definition),
                    ]
                    if state == "html-only":
                        exit_code, uncertain = module.execute(arguments)
                        self.assertEqual(4, exit_code)
                        self.assertEqual("UNCERTAIN_CREATE", uncertain["outcome"])
                        self.assertFalse(uncertain["terminal"])
                    else:
                        with self.assertRaises(SystemExit):
                            module.execute(arguments)

                inspected, _ = self._invoke(
                    *self._base_arguments(plan_name=plan_name),
                    "inspect",
                    expected_exit=4,
                )
                self.assertEqual("RECOVERY_REQUIRED", inspected["outcome"])
                if state == "html-only":
                    _, interrupted_html = self._plan_paths(plan_name=plan_name)
                    interrupted_html.write_text(
                        "different partial HTML\n", encoding="utf-8"
                    )
                    stale, _ = self._invoke(
                        *self._base_arguments(plan_name=plan_name),
                        "reconcile",
                        "--recovery-token",
                        str(inspected["recovery_token"]),
                        expected_exit=4,
                    )
                    self.assertEqual("STALE_RECOVERY_TOKEN", stale["outcome"])
                    inspected, _ = self._invoke(
                        *self._base_arguments(plan_name=plan_name),
                        "inspect",
                        expected_exit=4,
                    )
                recovered, _ = self._invoke(
                    *self._base_arguments(plan_name=plan_name),
                    "reconcile",
                    "--recovery-token",
                    str(inspected["recovery_token"]),
                )
                if state == "html-only":
                    self.assertEqual("RECOVERED_ABSENT", recovered["outcome"])
                    absent, _ = self._invoke(
                        *self._base_arguments(plan_name=plan_name), "inspect"
                    )
                    self.assertEqual("ABSENT", absent["outcome"])
                    retry, _ = self._invoke(
                        *self._base_arguments(plan_name=plan_name),
                        "create",
                        "--definition",
                        str(definition),
                    )
                    self.assertEqual("CREATED", retry["outcome"])
                else:
                    self.assertEqual("RECONCILED", recovered["outcome"])
                    retained, _ = self._invoke(
                        *self._base_arguments(plan_name=plan_name), "inspect"
                    )
                    self.assertEqual("SYNCED", retained["outcome"])

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

        self._complete_default_plan()

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

    def test_interrupted_cleanup_recovers_before_and_after_each_artifact_removal(
        self,
    ) -> None:
        module = self._load_helper_module()

        for stage in ("before", "after-html", "after-json"):
            with self.subTest(stage=stage):
                plan_name = stage.replace("-", "")
                self._create(
                    definition=self._definition_path(
                        filename=f"{plan_name}-definition.json"
                    ),
                    plan_name=plan_name,
                )
                self._complete_default_plan(plan_name=plan_name)

                def stop_cleanup(context: Any) -> list[str]:
                    if stage in {"after-html", "after-json"}:
                        context.html_path.unlink()
                    if stage == "after-json":
                        context.plan_path.unlink()
                    raise SystemExit(f"cleanup stop {stage}")

                cleanup_effect: object = (
                    RuntimeError("cleanup stopped before removal")
                    if stage == "before"
                    else stop_cleanup
                )
                with patch.object(
                    module, "_cleanup_artifacts", side_effect=cleanup_effect
                ):
                    arguments = [
                        *self._base_arguments(plan_name=plan_name),
                        "finalize",
                        "--retention",
                        "remove",
                    ]
                    if stage == "before":
                        exit_code, uncertain = module.execute(arguments)
                        self.assertEqual(4, exit_code)
                        self.assertEqual("UNCERTAIN_CLEANUP", uncertain["outcome"])
                        self.assertFalse(uncertain["terminal"])
                    else:
                        with self.assertRaises(SystemExit):
                            module.execute(arguments)

                inspected, _ = self._invoke(
                    *self._base_arguments(plan_name=plan_name),
                    "inspect",
                    expected_exit=4,
                )
                self.assertEqual("RECOVERY_REQUIRED", inspected["outcome"])
                recovered, _ = self._invoke(
                    *self._base_arguments(plan_name=plan_name),
                    "reconcile",
                    "--recovery-token",
                    str(inspected["recovery_token"]),
                )
                self.assertEqual("RECOVERED_ABSENT", recovered["outcome"])
                absent, _ = self._invoke(
                    *self._base_arguments(plan_name=plan_name), "inspect"
                )
                self.assertEqual("ABSENT", absent["outcome"])
                self.assertTrue(absent["retryable_create"])

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
