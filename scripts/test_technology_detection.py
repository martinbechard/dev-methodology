# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Modified with AI assistance.
# Summary: Verifies setup-time technology detection, folder ownership, generated mirrors, and AGENTS.md rendering.

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
BUILD_SCRIPT = ROOT / "scripts" / "build-technology-detection.py"
DETECT_SCRIPT = ROOT / "scripts" / "detect-technology-skills.py"
INSTALLED_DETECT_SCRIPT = ROOT / "skills" / "detect-technology-skills" / "scripts" / "detect.py"
RENDER_SCRIPT = ROOT / "scripts" / "render-agents-technology-skills.py"
REGISTRY = ROOT / "skills" / "detect-technology-skills" / "references" / "technology-skill-detection-registry.yaml"


def run_detection(
    project: Path,
    *scopes: str,
    expected_code: int = 0,
    detector: Path = DETECT_SCRIPT,
    extra: list[str] | None = None,
) -> dict[str, object]:
    arguments = ["python3", str(detector), "--project-root", str(project)]
    for scope in scopes:
        arguments.extend(["--scope", scope])
    arguments.extend(extra or [])
    completed = subprocess.run(arguments, cwd=ROOT, check=False, capture_output=True, text=True)
    if completed.returncode != expected_code:
        raise AssertionError(f"expected {expected_code}, got {completed.returncode}: {completed.stderr}\n{completed.stdout}")
    return json.loads(completed.stdout)


class TechnologyDetectionTests(unittest.TestCase):
    def test_generated_registry_and_installed_detector_are_current(self) -> None:
        completed = subprocess.run(
            ["python3", str(BUILD_SCRIPT), "--check"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)
        self.assertEqual(DETECT_SCRIPT.read_text(encoding="utf-8"), INSTALLED_DETECT_SCRIPT.read_text(encoding="utf-8"))

    def test_typescript_scope_has_exact_loadout(self) -> None:
        for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
            with self.subTest(detector=detector):
                result = run_detection(ROOT / "evals" / "projects" / "typescript-order-pricing", "src", detector=detector)
                self.assertEqual(["typescript-coding", "typescript-esm", "typescript-strict"], result["loadouts"][0]["skills"])

    def test_spring_boot_scope_has_exact_loadout(self) -> None:
        for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
            with self.subTest(detector=detector):
                result = run_detection(ROOT / "evals" / "projects" / "spring-boot-order-cancellation", "src/main", detector=detector)
                self.assertEqual(["java-coding", "spring-boot", "sql-coding"], result["loadouts"][0]["skills"])

    def test_python_scope_has_exact_loadout(self) -> None:
        for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
            with self.subTest(detector=detector):
                result = run_detection(ROOT / "evals" / "projects" / "python-inventory", "src", detector=detector)
                self.assertEqual(["python-coding"], result["loadouts"][0]["skills"])

    def test_python_cli_filename_does_not_activate_node_cli(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "src").mkdir()
            (root / "src" / "cli.py").write_text("def main():\n    return 0\n", encoding="utf-8")
            (root / "pyproject.toml").write_text(
                '[project]\nname="python-cli"\nversion="1"\n',
                encoding="utf-8",
            )
            for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                with self.subTest(detector=detector):
                    result = run_detection(root, "src", detector=detector)
                    self.assertEqual(["python-coding"], result["loadouts"][0]["skills"])

    def test_node_cli_requires_a_javascript_or_typescript_cli_path(self) -> None:
        cases = (
            ("tool-cli.js", ["node-cli"]),
            ("tool-cli.ts", ["node-cli", "typescript-coding"]),
            ("client.ts", ["typescript-coding"]),
        )
        for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
            for file_name, expected in cases:
                with self.subTest(detector=detector, file_name=file_name):
                    with tempfile.TemporaryDirectory() as directory:
                        root = Path(directory)
                        (root / "src").mkdir()
                        (root / "src" / file_name).write_text("export const run = () => 0;\n", encoding="utf-8")
                        (root / "package.json").write_text(
                            '{"name":"node-cli","version":"1","bin":{"tool":"src/tool-cli.js"}}\n',
                            encoding="utf-8",
                        )
                        result = run_detection(root, "src", detector=detector)
                        self.assertEqual(expected, result["loadouts"][0]["skills"])

    def test_fastapi_scope_composes_with_python(self) -> None:
        for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
            with self.subTest(detector=detector):
                result = run_detection(ROOT / "evals" / "projects" / "fastapi-orders", "app", detector=detector)
                self.assertEqual(["fastapi", "python-coding"], result["loadouts"][0]["skills"])
                evidence = {row["skill"]: row["evidence"] for row in result["loadouts"][0]["sourceEvidence"]}
                self.assertTrue(any("fastapi" in value.lower() for value in evidence["fastapi"]))

    def test_mixed_repository_produces_separate_scope_loadouts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "web" / "src").mkdir(parents=True)
            (root / "api" / "app").mkdir(parents=True)
            (root / "web" / "src" / "main.ts").write_text("export const value = 1;\n", encoding="utf-8")
            (root / "web" / "package.json").write_text('{"devDependencies":{"typescript":"1"}}\n', encoding="utf-8")
            (root / "api" / "app" / "main.py").write_text("from fastapi import FastAPI\n", encoding="utf-8")
            (root / "api" / "requirements.txt").write_text("fastapi==1.0\n", encoding="utf-8")
            for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                with self.subTest(detector=detector):
                    result = run_detection(root, "web/src", "api/app", detector=detector)
                    self.assertEqual(["typescript-coding"], result["loadouts"][0]["skills"])
                    self.assertEqual(["fastapi", "python-coding"], result["loadouts"][1]["skills"])

    def test_root_workspace_dependencies_do_not_contaminate_owned_child(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "packages" / "core" / "src").mkdir(parents=True)
            (root / "packages" / "core" / "src" / "entry.ts").write_text("export const value = 1;\n", encoding="utf-8")
            (root / "package.json").write_text('{"dependencies":{"next":"1","@clerk/nextjs":"1"}}\n', encoding="utf-8")
            (root / "packages" / "core" / "package.json").write_text('{"dependencies":{}}\n', encoding="utf-8")
            result = run_detection(root, "packages/core/src")
            self.assertEqual(["typescript-coding"], result["loadouts"][0]["skills"])

    def test_sibling_spring_module_does_not_contaminate_python_scope(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "python" / "src").mkdir(parents=True)
            (root / "java" / "src").mkdir(parents=True)
            (root / "python" / "src" / "main.py").write_text("value = 1\n", encoding="utf-8")
            (root / "python" / "pyproject.toml").write_text('[project]\nname="python"\nversion="1"\n', encoding="utf-8")
            (root / "java" / "src" / "Main.java").write_text("class Main {}\n", encoding="utf-8")
            (root / "java" / "pom.xml").write_text("<artifactId>spring-boot</artifactId>\n", encoding="utf-8")
            result = run_detection(root, "python/src")
            self.assertEqual(["python-coding"], result["loadouts"][0]["skills"])

    def test_missing_detected_required_skill_blocks_setup(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = root / "project"
            skills = root / "skills"
            project.mkdir()
            skills.mkdir()
            (project / "main.py").write_text("value = 1\n", encoding="utf-8")
            registry = root / "registry.yaml"
            registry.write_text(yaml.safe_dump({"skills": [{
                "skill": "missing-python",
                "kind": "technology",
                "capabilities": ["language-coding"],
                "activation": {"fileExtensions": [".py"]},
                "companions": [],
                "selection": "additive",
                "priority": 100,
                "requiredWhenDetected": True,
            }]}), encoding="utf-8")
            for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                with self.subTest(detector=detector):
                    result = run_detection(
                        project,
                        "main.py",
                        expected_code=2,
                        detector=detector,
                        extra=["--registry", str(registry), "--skills-root", str(skills)],
                    )
                    self.assertEqual("BLOCKED", result["loadouts"][0]["status"])
                    self.assertEqual("missing-python", result["loadouts"][0]["missingRequiredSkills"][0]["skill"])

    def test_equal_priority_exclusive_matches_block_setup(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = root / "project"
            skills = root / "skills"
            project.mkdir()
            (project / "example.mix").write_text("mixed\n", encoding="utf-8")
            entries = []
            for skill in ("variant-one", "variant-two"):
                skill_root = skills / skill
                skill_root.mkdir(parents=True)
                (skill_root / "SKILL.md").write_text(f"---\nname: {skill}\ndescription: Test variant.\n---\n", encoding="utf-8")
                entries.append({
                    "skill": skill,
                    "kind": "technology",
                    "capabilities": ["language-coding"],
                    "activation": {"fileExtensions": [".mix"]},
                    "companions": [],
                    "selection": "exclusive",
                    "exclusiveGroup": "mixed-language",
                    "priority": 10,
                    "requiredWhenDetected": True,
                })
            registry = root / "registry.yaml"
            registry.write_text(yaml.safe_dump({"skills": entries}), encoding="utf-8")
            for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                with self.subTest(detector=detector):
                    result = run_detection(
                        project,
                        "example.mix",
                        expected_code=2,
                        detector=detector,
                        extra=["--registry", str(registry), "--skills-root", str(skills)],
                    )
                    self.assertEqual(["variant-one", "variant-two"], result["loadouts"][0]["exclusiveConflicts"][0]["skills"])

    def test_no_variant_is_explicit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.txt").write_text("plain\n", encoding="utf-8")
            result = run_detection(root, "README.txt")
            self.assertEqual("NO_VARIANT", result["loadouts"][0]["status"])
            self.assertEqual([], result["loadouts"][0]["skills"])

    def test_missing_scope_blocks_instead_of_reporting_no_variant(self) -> None:
        project = ROOT / "evals" / "projects" / "fastapi-orders"
        for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
            with self.subTest(detector=detector):
                result = run_detection(project, "does-not-exist", expected_code=2, detector=detector)
                self.assertEqual("BLOCKED", result["status"])
                self.assertEqual(["scope does not exist"], result["loadouts"][0]["scopeErrors"])

    def test_broad_scope_spanning_multiple_owners_blocks_partitioning(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "packages" / "web" / "src").mkdir(parents=True)
            (root / "packages" / "api" / "src").mkdir(parents=True)
            (root / "packages" / "web" / "src" / "main.ts").write_text("export const value = 1;\n", encoding="utf-8")
            (root / "packages" / "web" / "package.json").write_text('{"dependencies":{"next":"1"}}\n', encoding="utf-8")
            (root / "packages" / "api" / "src" / "main.py").write_text("value = 1\n", encoding="utf-8")
            (root / "packages" / "api" / "pyproject.toml").write_text('[project]\nname="api"\nversion="1"\n', encoding="utf-8")
            for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                with self.subTest(detector=detector):
                    result = run_detection(root, "packages", expected_code=2, detector=detector)
                    self.assertEqual("BLOCKED", result["status"])
                    self.assertIn("analyze each owner separately", result["loadouts"][0]["scopeErrors"][0])

    def test_installed_detector_matches_canonical_behavior(self) -> None:
        project = ROOT / "evals" / "projects" / "fastapi-orders"
        canonical = run_detection(project, "app")
        installed = run_detection(project, "app", detector=INSTALLED_DETECT_SCRIPT)
        self.assertEqual(canonical, installed)

    def test_detector_has_no_task_time_options(self) -> None:
        completed = subprocess.run(
            ["python3", str(DETECT_SCRIPT), "--help"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        for obsolete in ("--role", "--confirm-read", "--require-confirmed", "--agents-plan"):
            self.assertNotIn(obsolete, completed.stdout)

    def test_agents_section_requires_unconditional_loading_without_redetection(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            plan = Path(directory) / "AGENTS-PLAN.yaml"
            plan.write_text(yaml.safe_dump({"technology_skill_loadouts": [{
                "pathPattern": "api/**",
                "skills": ["fastapi", "python-coding"],
                "sourceEvidence": [{"skill": "fastapi", "evidence": ["owning manifest dependency fastapi"]}],
            }]}), encoding="utf-8")
            completed = subprocess.run(
                ["python3", str(RENDER_SCRIPT), "--agents-plan", str(plan)],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertIn("api/**: load fastapi, python-coding before acting", completed.stdout)
            self.assertIn("Do not rerun detection during ordinary work", completed.stdout)

    def test_registry_contains_only_specialized_skills(self) -> None:
        registry = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
        self.assertTrue(registry["skills"])
        self.assertEqual({"technology", "domain"}, {entry["kind"] for entry in registry["skills"]})
        self.assertFalse({"careful-coding", "test-strategy", "detect-technology-skills"} & {entry["skill"] for entry in registry["skills"]})


if __name__ == "__main__":
    unittest.main()
