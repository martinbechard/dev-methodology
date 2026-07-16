# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Modified with AI assistance.
# Summary: Verifies setup-time technology detection, folder ownership, generated mirrors, and AGENTS.md rendering.

from __future__ import annotations

import json
import subprocess
import sys
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
    """Run one detector implementation and return its parsed result at the expected exit boundary."""
    arguments = [sys.executable, str(detector), "--project-root", str(project)]
    for scope in scopes:
        arguments.extend(["--scope", scope])
    arguments.extend(extra or [])
    completed = subprocess.run(arguments, cwd=ROOT, check=False, capture_output=True, text=True)
    if completed.returncode != expected_code:
        raise AssertionError(f"expected {expected_code}, got {completed.returncode}: {completed.stderr}\n{completed.stdout}")
    return json.loads(completed.stdout)


class TechnologyDetectionTests(unittest.TestCase):
    """Verify detector clauses, ownership isolation, generated mirrors, and routing output."""
    def test_explicit_activation_clause_requires_every_condition(self) -> None:
        for dependencies, expected in (([], False), (["example-framework"], True)):
            with self.subTest(dependencies=dependencies):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    project = root / "project"
                    skills = root / "skills"
                    project.mkdir()
                    (project / "main.py").write_text("value = 1\n", encoding="utf-8")
                    dependency_line = f"dependencies = {json.dumps(dependencies)}\n" if dependencies else ""
                    (project / "pyproject.toml").write_text(
                        '[project]\nname = "example"\nversion = "1"\n' + dependency_line,
                        encoding="utf-8",
                    )
                    skill_root = skills / "example-framework"
                    skill_root.mkdir(parents=True)
                    (skill_root / "SKILL.md").write_text(
                        "---\nname: example-framework\ndescription: Test framework.\n---\n",
                        encoding="utf-8",
                    )
                    registry = root / "registry.yaml"
                    registry.write_text(yaml.safe_dump({"skills": [{
                        "skill": "example-framework",
                        "kind": "technology",
                        "capabilities": ["application-framework"],
                        "activation": {"anyOf": [{"allOf": [
                            {"fileExtension": ".py"},
                            {"owningDependency": "example-framework"},
                        ]}]},
                        "companions": [],
                        "selection": "additive",
                        "priority": 100,
                        "requiredWhenDetected": True,
                    }]}), encoding="utf-8")

                    result = run_detection(
                        project,
                        "main.py",
                        extra=["--registry", str(registry), "--skills-root", str(skills)],
                    )

                    self.assertEqual(expected, "example-framework" in result["loadouts"][0]["skills"])

    def test_source_import_is_code_evidence_not_comment_or_string_text(self) -> None:
        cases = (
            ("from fastapi import FastAPI\n", True),
            ("# from fastapi import FastAPI\n", False),
            ('EXAMPLE = "from fastapi import FastAPI"\n', False),
        )
        for source, expected in cases:
            with self.subTest(source=source):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    project = root / "project"
                    skills = root / "skills"
                    project.mkdir()
                    (project / "main.py").write_text(source, encoding="utf-8")
                    skill_root = skills / "example-framework"
                    skill_root.mkdir(parents=True)
                    (skill_root / "SKILL.md").write_text(
                        "---\nname: example-framework\ndescription: Test framework.\n---\n",
                        encoding="utf-8",
                    )
                    registry = root / "registry.yaml"
                    registry.write_text(yaml.safe_dump({"skills": [{
                        "skill": "example-framework",
                        "kind": "technology",
                        "capabilities": ["application-framework"],
                        "activation": {"anyOf": [{"sourceImport": {
                            "module": "fastapi",
                            "extensions": [".py"],
                        }}]},
                        "companions": [],
                        "selection": "additive",
                        "priority": 100,
                        "requiredWhenDetected": True,
                    }]}), encoding="utf-8")

                    result = run_detection(
                        project,
                        "main.py",
                        extra=["--registry", str(registry), "--skills-root", str(skills)],
                    )

                    self.assertEqual(expected, "example-framework" in result["loadouts"][0]["skills"])

    def test_root_level_globstar_path_matches(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = root / "project"
            skills = root / "skills"
            route = project / "app" / "api" / "users" / "route.ts"
            route.parent.mkdir(parents=True)
            route.write_text("export const GET = () => new Response();\n", encoding="utf-8")
            skill_root = skills / "example-routes"
            skill_root.mkdir(parents=True)
            (skill_root / "SKILL.md").write_text(
                "---\nname: example-routes\ndescription: Test routes.\n---\n",
                encoding="utf-8",
            )
            registry = root / "registry.yaml"
            registry.write_text(yaml.safe_dump({"skills": [{
                "skill": "example-routes",
                "kind": "technology",
                "capabilities": ["http-api"],
                "activation": {"anyOf": [{"fileGlob": "**/app/api/**/route.ts"}]},
                "companions": [],
                "selection": "additive",
                "priority": 100,
                "requiredWhenDetected": True,
            }]}), encoding="utf-8")

            result = run_detection(
                project,
                "app/api",
                extra=["--registry", str(registry), "--skills-root", str(skills)],
            )

            self.assertEqual(["example-routes"], result["loadouts"][0]["skills"])

    def test_generated_registry_and_installed_detector_are_current(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(BUILD_SCRIPT), "--check"],
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
                self.assertEqual(["typescript", "typescript-esm", "typescript-strict"], result["loadouts"][0]["skills"])

    def test_spring_boot_scope_has_exact_loadout(self) -> None:
        for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
            with self.subTest(detector=detector):
                result = run_detection(ROOT / "evals" / "projects" / "spring-boot-order-cancellation", "src/main", detector=detector)
                self.assertEqual(
                    ["java", "java-design", "spring-boot", "spring-boot-design", "sql"],
                    result["loadouts"][0]["skills"],
                )

    def test_spring_data_jpa_composes_with_spring_design_and_sql(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "src" / "main" / "java" / "example"
            source.mkdir(parents=True)
            (source / "Order.java").write_text("class Order {}\n", encoding="utf-8")
            (root / "pom.xml").write_text(
                "<artifactId>spring-boot</artifactId>\n"
                "<artifactId>spring-boot-starter-data-jpa</artifactId>\n",
                encoding="utf-8",
            )

            expected = [
                "java",
                "java-design",
                "spring-boot",
                "spring-boot-design",
                "spring-data-jpa",
                "sql",
            ]
            for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                with self.subTest(detector=detector):
                    result = run_detection(root, "src/main", detector=detector)
                    self.assertEqual(expected, result["loadouts"][0]["skills"])

    def test_spring_boot_testing_requires_test_source_and_test_starter(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tests = root / "src" / "test" / "java" / "example"
            tests.mkdir(parents=True)
            (tests / "OrderTest.java").write_text("class OrderTest {}\n", encoding="utf-8")
            (root / "pom.xml").write_text(
                "<artifactId>spring-boot</artifactId>\n"
                "<artifactId>spring-boot-starter-test</artifactId>\n",
                encoding="utf-8",
            )

            expected = [
                "java",
                "java-design",
                "junit",
                "mockito",
                "spring-boot",
                "spring-boot-design",
                "spring-boot-testing",
            ]
            for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                with self.subTest(detector=detector):
                    result = run_detection(root, "src/test", detector=detector)
                    self.assertEqual(expected, result["loadouts"][0]["skills"])

    def test_quarkus_persistence_composes_with_java_design_and_sql(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "src" / "main" / "java" / "example"
            source.mkdir(parents=True)
            (source / "Order.java").write_text("class Order {}\n", encoding="utf-8")
            (root / "pom.xml").write_text(
                "<artifactId>quarkus-maven-plugin</artifactId>\n"
                "<artifactId>quarkus-hibernate-orm-panache</artifactId>\n",
                encoding="utf-8",
            )

            expected = [
                "java",
                "java-design",
                "quarkus",
                "quarkus-design",
                "quarkus-persistence",
                "sql",
            ]
            for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                with self.subTest(detector=detector):
                    result = run_detection(root, "src/main", detector=detector)
                    self.assertEqual(expected, result["loadouts"][0]["skills"])

    def test_quarkus_testing_requires_test_source_and_test_dependency(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tests = root / "src" / "test" / "java" / "example"
            tests.mkdir(parents=True)
            (tests / "OrderTest.java").write_text("class OrderTest {}\n", encoding="utf-8")
            (root / "pom.xml").write_text(
                "<artifactId>quarkus-maven-plugin</artifactId>\n"
                "<artifactId>quarkus-junit</artifactId>\n",
                encoding="utf-8",
            )

            expected = [
                "java",
                "java-design",
                "junit",
                "quarkus",
                "quarkus-design",
                "quarkus-testing",
            ]
            for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                with self.subTest(detector=detector):
                    result = run_detection(root, "src/test", detector=detector)
                    self.assertEqual(expected, result["loadouts"][0]["skills"])

    def test_junit_and_mockito_compose_for_java_tests(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tests = root / "src" / "test" / "java" / "example"
            tests.mkdir(parents=True)
            (tests / "OrderTest.java").write_text(
                "import org.junit.jupiter.api.Test;\n"
                "import org.mockito.Mock;\n"
                "class OrderTest {}\n",
                encoding="utf-8",
            )
            (root / "pom.xml").write_text(
                "<artifactId>junit-jupiter</artifactId>\n"
                "<artifactId>mockito-core</artifactId>\n",
                encoding="utf-8",
            )

            expected = ["java", "java-design", "junit", "mockito"]
            for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                with self.subTest(detector=detector):
                    result = run_detection(root, "src/test", detector=detector)
                    self.assertEqual(expected, result["loadouts"][0]["skills"])

    def test_liquibase_scope_composes_with_sql_without_jhipster(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            changelog = root / "src" / "main" / "resources" / "db" / "changelog"
            changelog.mkdir(parents=True)
            (root / "pom.xml").write_text(
                "<dependency><artifactId>liquibase-core</artifactId></dependency>\n",
                encoding="utf-8",
            )
            (changelog / "db.changelog-master.xml").write_text(
                "<databaseChangeLog/>\n",
                encoding="utf-8",
            )

            for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                with self.subTest(detector=detector):
                    result = run_detection(root, changelog.relative_to(root).as_posix(), detector=detector)
                    self.assertEqual(["liquibase", "sql"], result["loadouts"][0]["skills"])

    def test_liquibase_documentation_folder_does_not_activate_skill(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            notes = root / "docs" / "liquibase"
            notes.mkdir(parents=True)
            (root / "pom.xml").write_text(
                "<dependency><artifactId>liquibase-core</artifactId></dependency>\n",
                encoding="utf-8",
            )
            (notes / "example.xml").write_text("<databaseChangeLog/>\n", encoding="utf-8")

            for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                with self.subTest(detector=detector):
                    result = run_detection(root, notes.relative_to(root).as_posix(), detector=detector)
                    self.assertNotIn("liquibase", result["loadouts"][0]["skills"])

    def test_jhipster_scope_composes_focused_skills_with_java_and_spring_boot(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".jhipster").mkdir()
            (root / "src" / "main" / "java" / "example" / "config").mkdir(parents=True)
            (root / "src" / "main" / "resources" / "config" / "liquibase").mkdir(parents=True)
            (root / "src" / "test" / "java" / "example").mkdir(parents=True)
            (root / ".yo-rc.json").write_text(
                '{"generator-jhipster":{"baseName":"sample","jhipsterVersion":"9.1.0"}}\n',
                encoding="utf-8",
            )
            (root / "pom.xml").write_text(
                "<artifactId>spring-boot</artifactId>\n<artifactId>archunit-junit5</artifactId>\n",
                encoding="utf-8",
            )
            (root / ".jhipster" / "Order.json").write_text("{}\n", encoding="utf-8")
            (root / "src" / "main" / "java" / "example" / "Application.java").write_text(
                "class Application {}\n",
                encoding="utf-8",
            )
            (root / "src" / "main" / "java" / "example" / "config" / "SecurityConfiguration.java").write_text(
                "class SecurityConfiguration {}\n",
                encoding="utf-8",
            )
            (root / "src" / "main" / "resources" / "config" / "liquibase" / "master.xml").write_text(
                "<databaseChangeLog/>\n",
                encoding="utf-8",
            )
            (root / "src" / "test" / "java" / "example" / "TechnicalStructureTest.java").write_text(
                "class TechnicalStructureTest {}\n",
                encoding="utf-8",
            )

            expected = [
                "java",
                "java-design",
                "jhipster-domain-modeling",
                "jhipster-persistence",
                "jhipster-project",
                "jhipster-security",
                "jhipster-testing",
                "liquibase",
                "spring-boot",
                "spring-boot-design",
                "sql",
            ]
            for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                with self.subTest(detector=detector):
                    result = run_detection(root, ".", detector=detector)
                    self.assertEqual(expected, result["loadouts"][0]["skills"])

    def test_jhipster_concern_paths_do_not_activate_without_an_owning_marker(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "src" / "main" / "java" / "example" / "config"
            tests = root / "src" / "test" / "java" / "example"
            liquibase = root / "src" / "main" / "resources" / "config" / "liquibase"
            source.mkdir(parents=True)
            tests.mkdir(parents=True)
            liquibase.mkdir(parents=True)
            (root / ".jhipster").mkdir()
            (root / "pom.xml").write_text("<artifactId>spring-boot</artifactId>\n", encoding="utf-8")
            (source / "Application.java").write_text("class Application {}\n", encoding="utf-8")
            (source / "SecurityConfiguration.java").write_text("class SecurityConfiguration {}\n", encoding="utf-8")
            (tests / "ApplicationTest.java").write_text("class ApplicationTest {}\n", encoding="utf-8")
            (liquibase / "master.xml").write_text("<databaseChangeLog/>\n", encoding="utf-8")
            (root / ".jhipster" / "Order.json").write_text("{}\n", encoding="utf-8")

            for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                with self.subTest(detector=detector):
                    result = run_detection(root, ".", detector=detector)
                    self.assertFalse(any(skill.startswith("jhipster-") for skill in result["loadouts"][0]["skills"]))

    def test_jhipster_generator_config_requires_a_version(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "src" / "main" / "java" / "example"
            source.mkdir(parents=True)
            (root / ".yo-rc.json").write_text(
                '{"generator-jhipster":{"baseName":"sample"}}\n',
                encoding="utf-8",
            )
            (root / "pom.xml").write_text("<artifactId>spring-boot</artifactId>\n", encoding="utf-8")
            (source / "Application.java").write_text("class Application {}\n", encoding="utf-8")

            for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                with self.subTest(detector=detector):
                    result = run_detection(root, ".", detector=detector)
                    self.assertNotIn("jhipster-project", result["loadouts"][0]["skills"])

    def test_nested_jhipster_example_does_not_supply_the_owning_marker(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "src" / "main" / "java" / "example"
            example = root / "docs" / "jhipster-example"
            source.mkdir(parents=True)
            example.mkdir(parents=True)
            (root / "pom.xml").write_text("<artifactId>spring-boot</artifactId>\n", encoding="utf-8")
            (source / "Application.java").write_text("class Application {}\n", encoding="utf-8")
            (example / ".yo-rc.json").write_text(
                '{"generator-jhipster":{"jhipsterVersion":"9.1.0"}}\n',
                encoding="utf-8",
            )

            for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                with self.subTest(detector=detector):
                    result = run_detection(root, ".", detector=detector)
                    self.assertNotIn("jhipster-project", result["loadouts"][0]["skills"])

    def test_jhipster_gradle_runtime_marker_works_without_generator_config(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "src" / "main" / "java" / "example"
            source.mkdir(parents=True)
            (root / "build.gradle.kts").write_text(
                'plugins { id("org.springframework.boot") }\n'
                'dependencies { implementation("tech.jhipster:jhipster-framework:9.1.0") }\n',
                encoding="utf-8",
            )
            (source / "GatewayApplication.java").write_text("class GatewayApplication {}\n", encoding="utf-8")

            for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                with self.subTest(detector=detector):
                    result = run_detection(root, ".", detector=detector)
                    self.assertIn("jhipster-project", result["loadouts"][0]["skills"])

    def test_non_java_jhipster_generator_scope_is_no_variant(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "package.json").write_text(
                '{"devDependencies":{"generator-jhipster":"9.1.0"}}\n',
                encoding="utf-8",
            )
            (root / ".yo-rc.json").write_text(
                '{"generator-jhipster":{"jhipsterVersion":"9.1.0"}}\n',
                encoding="utf-8",
            )

            for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                with self.subTest(detector=detector):
                    result = run_detection(root, ".yo-rc.json", detector=detector)
                    self.assertEqual("NO_VARIANT", result["loadouts"][0]["status"])
                    self.assertEqual([], result["loadouts"][0]["skills"])

    def test_python_scope_has_exact_loadout(self) -> None:
        for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
            with self.subTest(detector=detector):
                result = run_detection(ROOT / "evals" / "projects" / "python-inventory", "src", detector=detector)
                self.assertEqual(["python"], result["loadouts"][0]["skills"])

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
                    self.assertEqual(["python"], result["loadouts"][0]["skills"])

    def test_node_cli_requires_a_javascript_or_typescript_cli_path(self) -> None:
        cases = (
            ("tool-cli.js", ["node-cli"]),
            ("tool-cli.ts", ["node-cli", "typescript"]),
            ("client.ts", ["typescript"]),
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
                self.assertEqual(["fastapi", "python"], result["loadouts"][0]["skills"])
                evidence = {row["skill"]: row["evidence"] for row in result["loadouts"][0]["sourceEvidence"]}
                self.assertTrue(any("fastapi" in value.lower() for value in evidence["fastapi"]))

    def test_fastapi_import_text_in_detector_tests_does_not_activate_fastapi(self) -> None:
        result = run_detection(ROOT, "scripts")
        self.assertEqual(["python"], result["loadouts"][0]["skills"])

    def test_next_api_routes_require_code_and_the_owning_next_dependency(self) -> None:
        cases = (
            ("route.py", {"next": "1"}, ["python"]),
            ("route.ts", {}, ["typescript"]),
            ("route.ts", {"next": "1"}, ["api-routes", "nextjs-app-router", "typescript"]),
        )
        for file_name, dependencies, expected in cases:
            with self.subTest(file_name=file_name, dependencies=dependencies):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    route = root / "app" / "api" / "users" / file_name
                    route.parent.mkdir(parents=True)
                    route.write_text("value = 1\n", encoding="utf-8")
                    (root / "package.json").write_text(
                        json.dumps({"dependencies": dependencies}) + "\n",
                        encoding="utf-8",
                    )
                    result = run_detection(root, "app")
                    self.assertEqual(expected, result["loadouts"][0]["skills"])

    def test_domain_detector_names_in_non_code_files_do_not_activate_product_skills(self) -> None:
        cases = (
            ("docs/harness-design.md", "agent harness\n"),
            ("docs/tool-runtime.md", "tool runtime\n"),
            ("docs/plan-engine.md", "plan engine\n"),
            ("docs/local-model.md", "localModel\n"),
            ("plans/example.yaml", "steps: []\n"),
        )
        for file_name, content in cases:
            with self.subTest(file_name=file_name):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    path = root / file_name
                    path.parent.mkdir(parents=True)
                    path.write_text(content, encoding="utf-8")
                    result = run_detection(root, path.parent.relative_to(root).as_posix())
                    self.assertEqual([], result["loadouts"][0]["skills"])

    def test_domain_detectors_accept_matching_code_artifacts(self) -> None:
        cases = (
            ("agent-harness.ts", "export const value = 1;\n", ["agent-harness", "typescript"]),
            ("tool-runtime.py", "value = 1\n", ["python", "tool-runtime"]),
            ("plan-engine.go", "package plan\n", ["plan-engine"]),
            ("local-model.ts", "export const localModel = true;\n", ["local-model-integration", "typescript"]),
        )
        for file_name, content, expected in cases:
            with self.subTest(file_name=file_name):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    (root / "src").mkdir()
                    (root / "src" / file_name).write_text(content, encoding="utf-8")
                    result = run_detection(root, "src")
                    self.assertEqual(expected, result["loadouts"][0]["skills"])

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
                    self.assertEqual(["typescript"], result["loadouts"][0]["skills"])
                    self.assertEqual(["fastapi", "python"], result["loadouts"][1]["skills"])

    def test_root_workspace_dependencies_do_not_contaminate_owned_child(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "packages" / "core" / "src").mkdir(parents=True)
            (root / "packages" / "core" / "src" / "entry.ts").write_text("export const value = 1;\n", encoding="utf-8")
            (root / "package.json").write_text('{"dependencies":{"next":"1","@clerk/nextjs":"1"}}\n', encoding="utf-8")
            (root / "packages" / "core" / "package.json").write_text('{"dependencies":{}}\n', encoding="utf-8")
            result = run_detection(root, "packages/core/src")
            self.assertEqual(["typescript"], result["loadouts"][0]["skills"])

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
            self.assertEqual(["python"], result["loadouts"][0]["skills"])

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
                "activation": {"anyOf": [{"fileExtension": ".py"}]},
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

    def test_explicit_runtime_catalog_overrides_methodology_source_skills(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = root / "project"
            skills = root / "skills"
            project.mkdir()
            skill_root = skills / "example-python"
            skill_root.mkdir(parents=True)
            (skill_root / "SKILL.md").write_text(
                "---\nname: example-python\ndescription: Test runtime catalog.\n---\n",
                encoding="utf-8",
            )
            (project / "main.py").write_text("value = 1\n", encoding="utf-8")
            registry = root / "registry.yaml"
            registry.write_text(yaml.safe_dump({"skills": [{
                "skill": "example-python",
                "kind": "technology",
                "capabilities": ["language-coding"],
                "activation": {"anyOf": [{"fileExtension": ".py"}]},
                "companions": [],
                "selection": "additive",
                "priority": 100,
                "requiredWhenDetected": True,
            }]}), encoding="utf-8")

            blocked = run_detection(
                project,
                "main.py",
                expected_code=2,
                extra=[
                    "--registry", str(registry),
                    "--skills-root", str(skills),
                    "--available-skill", "another-skill",
                ],
            )
            self.assertEqual("BLOCKED", blocked["loadouts"][0]["status"])
            self.assertEqual(
                "UNAVAILABLE",
                blocked["loadouts"][0]["sourceEvidence"][0]["runtimeAvailability"],
            )
            self.assertEqual(
                ["another-skill"],
                blocked["runtimeSkillCatalog"]["availableSkills"],
            )

            ready = run_detection(
                project,
                "main.py",
                extra=[
                    "--registry", str(registry),
                    "--skills-root", str(skills),
                    "--available-skill", "example-python",
                ],
            )
            self.assertEqual("READY", ready["loadouts"][0]["status"])
            self.assertEqual(
                "AVAILABLE",
                ready["loadouts"][0]["sourceEvidence"][0]["runtimeAvailability"],
            )

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
                    "activation": {"anyOf": [{"fileExtension": ".mix"}]},
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

    def test_installed_detector_matches_source_behavior(self) -> None:
        project = ROOT / "evals" / "projects" / "fastapi-orders"
        source_result = run_detection(project, "app")
        installed = run_detection(project, "app", detector=INSTALLED_DETECT_SCRIPT)
        self.assertEqual(source_result, installed)

    def test_detector_has_no_task_time_options(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(DETECT_SCRIPT), "--help"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        for obsolete in ("--role", "--confirm-read", "--require-confirmed"):
            self.assertNotIn(obsolete, completed.stdout)

    def test_agents_section_requires_unconditional_loading_without_redetection(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            plan = Path(directory) / "PROJECT.yaml"
            plan.write_text(yaml.safe_dump({
                "technology_skill_loadouts": [{
                    "pathPattern": "api/**",
                    "skills": ["fastapi", "python"],
                    "sourceEvidence": [{"skill": "fastapi", "evidence": ["owning manifest dependency fastapi"]}],
                }],
            }), encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, str(RENDER_SCRIPT), "--project", str(plan)],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertIn("api/**: load fastapi, python before acting", completed.stdout)
            self.assertIn("Do not rerun detection during ordinary work", completed.stdout)
            self.assertIn("most-specific matching pattern wins", completed.stdout)
            self.assertNotIn("Agent Claims And Worktrees", completed.stdout)
            self.assertNotIn("agent-claim", completed.stdout)

    def test_agents_section_preserves_no_variant_general_training_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            plan = Path(directory) / "PROJECT.yaml"
            plan.write_text(yaml.safe_dump({
                "technology_skill_loadouts": [
                    {
                        "pathPattern": "src/main/**",
                        "skills": ["python"],
                        "status": "READY",
                    },
                    {
                        "pathPattern": "config/**",
                        "skills": [],
                        "status": "NO_VARIANT",
                        "fallback": "general model training",
                    },
                ],
            }), encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, str(RENDER_SCRIPT), "--project", str(plan)],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertIn("src/main/**: load python before acting", completed.stdout)
            self.assertIn(
                "config/**: no pertinent specialized technology skill is available; use general model training and continue full scope coverage",
                completed.stdout,
            )
            self.assertIn("most-specific matching pattern wins", completed.stdout)

    def test_registry_contains_only_specialized_skills(self) -> None:
        registry = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
        self.assertEqual(2, registry["version"])
        self.assertTrue(registry["skills"])
        self.assertEqual({"technology", "domain"}, {entry["kind"] for entry in registry["skills"]})
        self.assertTrue(all(entry.get("skill") for entry in registry["skills"]))
        self.assertTrue(all(set(entry["activation"]) == {"anyOf"} for entry in registry["skills"]))
        self.assertFalse({"careful-coding", "test-strategy", "detect-technology-skills"} & {entry["skill"] for entry in registry["skills"]})


if __name__ == "__main__":
    unittest.main()
