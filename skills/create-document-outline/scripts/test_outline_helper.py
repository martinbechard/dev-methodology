# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies source-traceable document outline validation and synchronized hierarchy rendering.

from __future__ import annotations

import copy
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path
from types import ModuleType


_HELPER_PATH = Path(__file__).with_name("outline.py")
_EXAMPLE_PATH = Path(__file__).parents[1] / "examples" / "large-multi-source-outline.json"


class OutlineHelperTests(unittest.TestCase):
    """Exercise the outline schema, safe paths, rendering, review state, and drift checks."""

    def setUp(self) -> None:
        """Create an isolated canonical workspace and copy the large example into it."""
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.workspace = Path(self.temporary_directory.name).resolve()
        self.output_folder = Path(".codex/outlines/task-123")
        self.outline_name = "service-reliability"
        output_root = self.workspace / self.output_folder
        output_root.mkdir(parents=True)
        self.definition = output_root / f"{self.outline_name}.json"
        shutil.copyfile(_EXAMPLE_PATH, self.definition)

    def _arguments(self) -> list[str]:
        return [
            "--workspace",
            str(self.workspace),
            "--output-folder",
            self.output_folder.as_posix(),
            "--name",
            self.outline_name,
        ]

    def _invoke(
        self, *arguments: str, expected_exit: int | None = 0
    ) -> tuple[dict[str, object], subprocess.CompletedProcess[str]]:
        completed = subprocess.run(
            [sys.executable, str(_HELPER_PATH), *arguments],
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
                f"Helper did not return JSON: {completed.stdout!r}; "
                f"{completed.stderr!r}; {error}"
            )
        self.assertIsInstance(result, dict)
        return result, completed

    def _payload(self) -> dict[str, object]:
        payload = json.loads(self.definition.read_text(encoding="utf-8"))
        self.assertIsInstance(payload, dict)
        return payload

    def _write_payload(self, payload: dict[str, object]) -> None:
        self.definition.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    def _build(self, *, expected_exit: int = 0) -> dict[str, object]:
        result, _ = self._invoke(
            *self._arguments(),
            "build",
            "--definition",
            str(self.definition),
            expected_exit=expected_exit,
        )
        return result

    def _artifact_paths(self) -> tuple[Path, Path]:
        root = self.workspace / self.output_folder
        return root / f"{self.outline_name}.json", root / f"{self.outline_name}.html"

    def _load_helper_module(self) -> ModuleType:
        """Load the helper without running its command-line entry point."""
        module_name = f"outline_helper_under_test_{id(self)}"
        spec = importlib.util.spec_from_file_location(module_name, _HELPER_PATH)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader if spec is not None else None)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        self.addCleanup(sys.modules.pop, module_name, None)
        assert spec.loader is not None
        spec.loader.exec_module(module)
        return module

    def test_capability_check_finds_the_installed_renderer_from_system_python(self) -> None:
        """The portable helper can re-exec through the installed mcp-agent-ops interpreter."""
        result, completed = self._invoke("capabilities")

        self.assertEqual("CAPABILITIES_AVAILABLE", result["outcome"])
        self.assertEqual(["render_hierarchy_html"], result["capabilities"])
        self.assertRegex(str(result["package_version"]), r"^\d+\.\d+\.\d+")
        self.assertEqual("", completed.stderr)

    def test_large_multi_source_example_builds_synchronized_review_html(self) -> None:
        """A source-rich outline produces authoritative JSON and accessible standalone HTML."""
        definition_before = self.definition.read_bytes()
        built = self._build()
        json_path, html_path = self._artifact_paths()

        self.assertEqual("BUILT", built["outcome"])
        self.assertTrue(built["synchronized"])
        self.assertEqual(4, built["source_count"])
        self.assertGreaterEqual(int(built["section_count"]), 10)
        self.assertEqual(2, built["unresolved_question_count"])
        self.assertEqual(definition_before, self.definition.read_bytes())
        self.assertEqual(
            [html_path.name, json_path.name],
            sorted(path.name for path in json_path.parent.iterdir()),
        )
        canonical = json.loads(json_path.read_text(encoding="utf-8"))
        self.assertEqual("dev-methodology-document-outline", canonical["schema"])
        self.assertEqual(
            ["requirements", "research", "implementation", "review"],
            [source["id"] for source in canonical["sources"]],
        )
        html = html_path.read_text(encoding="utf-8")
        for required in (
            "Service Reliability Guide",
            "Purpose and audience",
            "Failure-state conflict",
            "Q-1",
            "Copy content",
            "Expand all levels",
            'class="tree-levels"',
            'data-level="all"',
        ):
            with self.subTest(required=required):
                self.assertIn(required, html)
        self.assertIn("Human review &lt;draft&gt;", html)
        self.assertNotIn("Human review <draft>", html)
        self.assertNotIn('class="tree-checkbox"', html)

    def test_missing_source_coverage_and_sensitive_input_review_fail_closed(self) -> None:
        """Material facts require sources and renderer input requires a completed safety review."""
        original = self._payload()
        cases: list[tuple[str, dict[str, object]]] = []

        missing_source = copy.deepcopy(original)
        missing_source["root"]["children"][0]["sourceRefs"] = []
        cases.append(("source coverage", missing_source))

        unsafe_input = copy.deepcopy(original)
        unsafe_input["inputReview"]["sensitiveDataExcluded"] = False
        cases.append(("sensitive data review", unsafe_input))

        for label, payload in cases:
            with self.subTest(label=label):
                self._write_payload(payload)
                definition_before = self.definition.read_bytes()
                rejected = self._build(expected_exit=2)
                self.assertEqual("INVALID_OUTLINE", rejected["outcome"])
                json_path, html_path = self._artifact_paths()
                self.assertEqual(self.definition, json_path)
                self.assertEqual(definition_before, json_path.read_bytes())
                self.assertFalse(html_path.exists())

    def test_build_requires_the_canonical_json_path(self) -> None:
        """Build rejects a staging definition so the outline has exactly two artifacts."""
        staging = self.workspace / "staging-outline.json"
        shutil.copyfile(self.definition, staging)

        rejected, _ = self._invoke(
            *self._arguments(),
            "build",
            "--definition",
            str(staging),
            expected_exit=2,
        )

        self.assertEqual("INVALID_DEFINITION_PATH", rejected["outcome"])
        json_path, html_path = self._artifact_paths()
        self.assertFalse(html_path.exists())
        self.assertEqual([json_path.name], [path.name for path in json_path.parent.iterdir()])

    def test_duplicate_skipped_branch_text_and_empty_leaf_are_rejected(self) -> None:
        """The outline keeps one unambiguous heading tree with text only on nonempty leaves."""
        original = self._payload()
        cases: list[tuple[str, dict[str, object]]] = []

        duplicate = copy.deepcopy(original)
        duplicate["root"]["children"][1]["title"] = duplicate["root"]["children"][0]["title"]
        cases.append(("duplicate sibling", duplicate))

        skipped = copy.deepcopy(original)
        skipped["root"]["children"][1]["children"][0]["level"] = 4
        cases.append(("skipped level", skipped))

        branch_text = copy.deepcopy(original)
        branch_text["root"]["children"][1]["reviewText"] = "Branch text is ambiguous."
        cases.append(("branch text", branch_text))

        empty_leaf = copy.deepcopy(original)
        empty_leaf["root"]["children"][0]["reviewText"] = "   "
        cases.append(("empty leaf", empty_leaf))

        for label, payload in cases:
            with self.subTest(label=label):
                self._write_payload(payload)
                rejected = self._build(expected_exit=2)
                self.assertEqual("INVALID_OUTLINE", rejected["outcome"])
                self.assertIn(label.split()[0], str(rejected["error"]).lower())

    def test_schema_version_requires_an_integer_not_bool_or_float(self) -> None:
        """JSON values equal to one do not satisfy the integer version contract."""
        original = self._payload()

        for version in (True, 1.0):
            with self.subTest(version=version):
                payload = copy.deepcopy(original)
                payload["version"] = version
                self._write_payload(payload)
                rejected = self._build(expected_exit=2)
                self.assertEqual("INVALID_OUTLINE", rejected["outcome"])
                self.assertIn("version", str(rejected["error"]).lower())

        self._write_payload(original)
        self.assertEqual("BUILT", self._build()["outcome"])

    def test_output_paths_cannot_escape_or_traverse_the_workspace(self) -> None:
        """Unsafe output folders and names fail before any outline artifact is written."""
        for arguments in (
            [
                "--workspace",
                str(self.workspace),
                "--output-folder",
                "../escape",
                "--name",
                self.outline_name,
                "inspect",
            ],
            [
                "--workspace",
                str(self.workspace),
                "--output-folder",
                self.output_folder.as_posix(),
                "--name",
                "../escape",
                "inspect",
            ],
        ):
            with self.subTest(arguments=arguments):
                rejected, _ = self._invoke(*arguments, expected_exit=2)
                self.assertIn(
                    rejected["outcome"],
                    {"PATH_OUTSIDE_WORKSPACE", "INVALID_NAME"},
                )
        self.assertFalse((self.workspace.parent / "escape").exists())

    def test_html_output_rejects_hard_link_aliases_and_directories(self) -> None:
        """Existing HTML targets must be unaliased regular files before publication."""
        _json_path, html_path = self._artifact_paths()
        outside = self.workspace / "outside.html"
        outside.write_text("retained outside bytes\n", encoding="utf-8")
        try:
            os.link(outside, html_path)
        except OSError as error:
            self.skipTest(f"Hard links are unavailable: {error}")

        rejected, _ = self._invoke(*self._arguments(), "inspect", expected_exit=2)
        self.assertEqual("HARD_LINK_PATH_REJECTED", rejected["outcome"])
        self.assertEqual("retained outside bytes\n", outside.read_text(encoding="utf-8"))

        html_path.unlink()
        html_path.mkdir()
        rejected, _ = self._invoke(*self._arguments(), "inspect", expected_exit=2)
        self.assertEqual("INVALID_OUTPUT_TARGET", rejected["outcome"])

    def test_failed_renderer_write_keeps_the_previous_html_complete(self) -> None:
        """A renderer failure in temporary storage does not alter the published HTML."""
        self._build()
        json_path, html_path = self._artifact_paths()
        json_before = json_path.read_bytes()
        html_before = html_path.read_bytes()
        helper = self._load_helper_module()

        def failing_renderer(_source: object, **options: object) -> str | Path:
            output_folder = options.get("output_folder")
            if output_folder is None:
                return "<!doctype html><title>candidate</title>"
            output_path = Path(str(output_folder)) / str(options["output_filename"])
            output_path.write_text("partial renderer bytes", encoding="utf-8")
            raise RuntimeError("renderer stopped before completion")

        context = helper._context(
            Namespace(
                workspace=str(self.workspace),
                output_folder=self.output_folder.as_posix(),
                name=self.outline_name,
            )
        )
        api = helper._OutlineApi(failing_renderer, "test", "test signature")

        with self.assertRaisesRegex(RuntimeError, "stopped before completion"):
            helper._build(context, Namespace(definition=str(json_path)), api)

        self.assertEqual(json_before, json_path.read_bytes())
        self.assertEqual(html_before, html_path.read_bytes())
        self.assertEqual(
            [html_path.name, json_path.name],
            sorted(path.name for path in json_path.parent.iterdir()),
        )

    def test_native_windows_console_launcher_resolves_its_package_interpreter(self) -> None:
        """A Windows console launcher uses the sibling package Python interpreter."""
        helper = self._load_helper_module()
        scripts = self.workspace / "Scripts"
        scripts.mkdir()
        launcher = scripts / "mcp-agent-ops.exe"
        interpreter = scripts / "python.exe"
        launcher.write_bytes(b"launcher")
        interpreter.write_bytes(b"python")

        self.assertEqual((interpreter, []), helper._windows_interpreter(launcher))
        interpreter.unlink()
        self.assertIsNone(helper._windows_interpreter(launcher))

    def test_inspect_detects_stale_html_and_rebuild_restores_sync(self) -> None:
        """A changed or missing projection is stale until regenerated from authoritative JSON."""
        self._build()
        json_path, html_path = self._artifact_paths()
        source_before = json_path.read_bytes()
        html_path.write_text("stale projection\n", encoding="utf-8")

        stale, _ = self._invoke(*self._arguments(), "inspect", expected_exit=4)
        self.assertEqual("STALE_HTML", stale["outcome"])
        self.assertFalse(stale["synchronized"])
        self.assertEqual(source_before, json_path.read_bytes())

        rebuilt, _ = self._invoke(
            *self._arguments(),
            "build",
            "--definition",
            str(json_path),
        )
        self.assertEqual("BUILT", rebuilt["outcome"])
        synced, _ = self._invoke(*self._arguments(), "inspect")
        self.assertEqual("SYNCED", synced["outcome"])
        self.assertTrue(synced["synchronized"])

    def test_review_cannot_drop_unresolved_questions_and_acceptance_records_order(self) -> None:
        """Review keeps every open question and records the accepted top-level section order."""
        payload = self._payload()
        payload["review"]["remainingQuestionIds"] = ["Q-1"]
        self._write_payload(payload)
        rejected = self._build(expected_exit=2)
        self.assertEqual("INVALID_OUTLINE", rejected["outcome"])
        self.assertIn("remainingquestionids", str(rejected["error"]).lower())

        shutil.copyfile(_EXAMPLE_PATH, self.definition)
        draft = self._build()
        draft_json_hash = draft["json_sha256"]
        draft_html_hash = draft["html_sha256"]
        payload = self._payload()
        payload["review"] = {
            "status": "accepted",
            "acceptedSectionOrder": [
                section["title"] for section in payload["root"]["children"]
            ],
            "requiredCorrections": [],
            "remainingQuestionIds": [
                question["id"] for question in payload["unresolvedQuestions"]
            ],
        }
        self._write_payload(payload)
        built = self._build()
        self.assertEqual("accepted", built["review_status"])
        self.assertNotEqual(draft_json_hash, built["json_sha256"])
        self.assertNotEqual(draft_html_hash, built["html_sha256"])
        json_path, html_path = self._artifact_paths()
        canonical = json.loads(json_path.read_text(encoding="utf-8"))
        self.assertEqual(["Q-1", "Q-2"], canonical["review"]["remainingQuestionIds"])
        html = html_path.read_text(encoding="utf-8")
        self.assertIn("Accepted section order", html)
        self.assertIn("Q-2", html)


if __name__ == "__main__":
    unittest.main()
