from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
BUILD_SCRIPT = ROOT / "scripts" / "build-skill-routing.py"
RESOLVE_SCRIPT = ROOT / "skills" / "route-technology-skills" / "scripts" / "resolve.py"
RENDER_SCRIPT = ROOT / "skills" / "route-technology-skills" / "scripts" / "render_agents_routing.py"
REGISTRY = ROOT / "skills" / "route-technology-skills" / "references" / "technology-skill-registry.yaml"
EXPLORER_DATA = ROOT / "design" / "generated" / "agent-skill-explorer-data.js"


def run_json(arguments: list[str], expected_code: int = 0) -> dict[str, object]:
    completed = subprocess.run(
        ["python3", str(RESOLVE_SCRIPT), *arguments],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != expected_code:
        raise AssertionError(f"expected {expected_code}, got {completed.returncode}: {completed.stderr}\n{completed.stdout}")
    return json.loads(completed.stdout)


class SkillRoutingTests(unittest.TestCase):
    def test_registry_is_current_and_role_loadouts_are_generic(self) -> None:
        completed = subprocess.run(
            ["python3", str(BUILD_SCRIPT), "--check"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)

    def test_typescript_scope_resolves_only_applicable_variants(self) -> None:
        project = ROOT / "evals" / "projects" / "typescript-order-pricing"
        receipt = run_json([
            "--project-root", str(project),
            "--role", "coding-agent",
            "--scope", "src",
        ])
        skills = {item["skill"] for item in receipt["resolved"]}
        self.assertEqual({"typescript-coding", "typescript-esm", "typescript-strict"}, skills)
        self.assertEqual("READY", receipt["status"])

    def test_java_scope_resolves_java_framework_and_query_guidance(self) -> None:
        project = ROOT / "evals" / "projects" / "spring-boot-order-cancellation"
        receipt = run_json([
            "--project-root", str(project),
            "--role", "coding-agent",
            "--scope", "src/main",
        ])
        skills = {item["skill"] for item in receipt["resolved"]}
        self.assertEqual({"java-coding", "spring-boot", "sql-coding"}, skills)
        self.assertNotIn("typescript-coding", skills)

    def test_mixed_scope_resolves_both_languages_without_cross_binding(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "src").mkdir()
            (root / "src" / "entry.ts").write_text("export const value = 1;\n", encoding="utf-8")
            (root / "src" / "Entry.java").write_text("final class Entry {}\n", encoding="utf-8")
            receipt = run_json([
                "--project-root", str(root),
                "--role", "code-review-agent",
                "--scope", "src/entry.ts",
                "--scope", "src/Entry.java",
            ])
            skills = {item["skill"] for item in receipt["resolved"]}
            self.assertEqual({"java-coding", "typescript-coding"}, skills)

    def test_missing_project_bound_skill_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "src").mkdir()
            (root / "src" / "example.unknown").write_text("value\n", encoding="utf-8")
            plan = root / "AGENTS-PLAN.yaml"
            plan.write_text(yaml.safe_dump({
                "skill_loadouts": [{
                    "scope": "Unknown source",
                    "paths": ["src/**"],
                    "skills": ["unbundled-language-coding"],
                    "activation_evidence": ["src/example.unknown exists"],
                }]
            }), encoding="utf-8")
            receipt = run_json([
                "--project-root", str(root),
                "--role", "coding-agent",
                "--scope", "src/example.unknown",
                "--agents-plan", str(plan),
            ], expected_code=2)
            self.assertEqual("BLOCKED", receipt["status"])
            self.assertEqual("unbundled-language-coding", receipt["missing"][0]["skill"])

    def test_unbundled_language_uses_explicit_generic_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "src").mkdir()
            (root / "src" / "example.py").write_text("value = 1\n", encoding="utf-8")
            receipt = run_json([
                "--project-root", str(root),
                "--role", "coding-agent",
                "--scope", "src/example.py",
            ])
            self.assertEqual("READY_WITH_GAPS", receipt["status"])
            self.assertEqual(["language-coding"], receipt["unbundledCapabilities"])
            self.assertIn("generic role guidance", receipt["fallbackPolicy"])

    def test_missing_test_framework_is_not_silently_marked_loaded(self) -> None:
        project = ROOT / "evals" / "projects" / "typescript-order-pricing"
        receipt = run_json([
            "--project-root", str(project),
            "--role", "qa-and-verification-agent",
            "--scope", "test",
        ])
        self.assertEqual("READY_WITH_GAPS", receipt["status"])
        self.assertEqual(["test-framework"], receipt["unbundledCapabilities"])

    def test_sibling_spring_module_does_not_contaminate_typescript_scope(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "frontend" / "src").mkdir(parents=True)
            (root / "backend" / "src").mkdir(parents=True)
            (root / "frontend" / "src" / "entry.ts").write_text("export const value = 1;\n", encoding="utf-8")
            (root / "frontend" / "package.json").write_text('{"devDependencies":{"typescript":"1"}}\n', encoding="utf-8")
            (root / "backend" / "src" / "Entry.java").write_text("final class Entry {}\n", encoding="utf-8")
            (root / "backend" / "pom.xml").write_text("<artifactId>spring-boot</artifactId>\n", encoding="utf-8")
            receipt = run_json([
                "--project-root", str(root),
                "--role", "coding-agent",
                "--scope", "frontend/src/entry.ts",
            ])
            skills = {item["skill"] for item in receipt["resolved"]}
            self.assertEqual({"typescript-coding"}, skills)
            self.assertNotIn("spring-boot", skills)
            self.assertNotIn("java-coding", skills)

    def test_root_workspace_dependencies_do_not_contaminate_owned_child_package(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "packages" / "core" / "src").mkdir(parents=True)
            (root / "packages" / "core" / "src" / "entry.ts").write_text("export const value = 1;\n", encoding="utf-8")
            (root / "package.json").write_text(
                '{"dependencies":{"@clerk/nextjs":"1","drizzle-orm":"1","@langchain/langgraph":"1"}}\n',
                encoding="utf-8",
            )
            (root / "packages" / "core" / "package.json").write_text('{"dependencies":{}}\n', encoding="utf-8")
            receipt = run_json([
                "--project-root", str(root),
                "--role", "coding-agent",
                "--scope", "packages/core/src/entry.ts",
            ])
            skills = {item["skill"] for item in receipt["resolved"]}
            self.assertEqual({"typescript-coding"}, skills)
            self.assertFalse({"clerk-auth", "postgres-drizzle", "langgraph"} & skills)

    def test_root_agents_plan_is_loaded_and_stale_binding_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "src").mkdir()
            (root / "src" / "entry.ts").write_text("export const value = 1;\n", encoding="utf-8")
            plan = root / "AGENTS-PLAN.yaml"
            plan.write_text(yaml.safe_dump({
                "skill_loadouts": [{
                    "scope": "Stale backend binding",
                    "paths": ["src/**"],
                    "skills": ["java-coding"],
                    "activation_evidence": ["obsolete Java source inventory"],
                }]
            }), encoding="utf-8")
            receipt = run_json([
                "--project-root", str(root),
                "--role", "coding-agent",
                "--scope", "src/entry.ts",
            ], expected_code=2)
            self.assertEqual(str(plan.resolve()), receipt["agentsPlan"])
            self.assertEqual("BLOCKED", receipt["status"])
            self.assertEqual("project-binding", receipt["conflicts"][0]["group"])

    def test_manifest_dependency_or_config_file_can_activate_test_framework(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "test").mkdir()
            (root / "test" / "example.ts").write_text("export {};\n", encoding="utf-8")
            (root / "package.json").write_text('{"devDependencies":{"jest":"1"}}\n', encoding="utf-8")
            receipt = run_json([
                "--project-root", str(root),
                "--role", "qa-and-verification-agent",
                "--scope", "test/example.ts",
            ])
            skills = {item["skill"] for item in receipt["resolved"]}
            self.assertIn("jest", skills)
            self.assertNotIn("vitest", skills)

    def test_read_confirmation_requires_matching_content_digest(self) -> None:
        project = ROOT / "evals" / "projects" / "typescript-order-pricing"
        arguments = [
            "--project-root", str(project),
            "--role", "coding-agent",
            "--scope", "src/order-pricing.ts",
        ]
        first = run_json(arguments)
        confirmations = [f"{item['skill']}={item['contentDigest']}" for item in first["resolved"]]
        second_arguments = list(arguments)
        for confirmation in confirmations:
            second_arguments.extend(["--confirm-read", confirmation])
        second_arguments.append("--require-confirmed")
        confirmed = run_json(second_arguments)
        self.assertTrue(all(item["readConfirmed"] for item in confirmed["resolved"]))
        blocked = run_json([*arguments, "--confirm-read", "typescript-coding=wrong", "--require-confirmed"], expected_code=2)
        self.assertEqual("BLOCKED", blocked["status"])

    def test_equal_priority_exclusive_matches_block_as_ambiguous(self) -> None:
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
                    "applicableRoles": ["coding-agent"],
                    "activation": {"fileExtensions": [".mix"]},
                    "companions": [],
                    "selection": "exclusive",
                    "exclusiveGroup": "mixed-language",
                    "priority": 10,
                    "requiredWhenMatched": True,
                })
            registry = root / "registry.yaml"
            registry.write_text(yaml.safe_dump({
                "skills": entries,
                "roleCapabilityExpectations": {"coding-agent": ["language-coding"]},
            }), encoding="utf-8")
            receipt = run_json([
                "--project-root", str(project),
                "--role", "coding-agent",
                "--scope", "example.mix",
                "--registry", str(registry),
                "--skills-root", str(skills),
            ], expected_code=2)
            self.assertEqual("BLOCKED", receipt["status"])
            self.assertEqual("mixed-language", receipt["conflicts"][0]["group"])
            self.assertEqual(["variant-one", "variant-two"], receipt["conflicts"][0]["skills"])

    def test_agents_routing_section_renders_project_bindings(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            plan = Path(directory) / "AGENTS-PLAN.yaml"
            plan.write_text(yaml.safe_dump({
                "skill_loadouts": [{
                    "scope": "Service source",
                    "paths": ["src/**"],
                    "skills": ["java-coding"],
                }],
                "folder_routing": [{
                    "pattern": "migrations/**",
                    "required_skills": ["sql-coding"],
                }],
            }), encoding="utf-8")
            completed = subprocess.run(
                ["python3", str(RENDER_SCRIPT), "--agents-plan", str(plan)],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertIn("Service source: paths src/**; required skills java-coding", completed.stdout)
            self.assertIn("Folder route migrations/**: required skills sql-coding", completed.stdout)
            self.assertIn("Harness tool-call evidence", completed.stdout)

    def test_registry_has_every_stack_skill_and_a_truthful_policy(self) -> None:
        registry = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
        routed = {item["skill"] for item in registry["skills"]}
        stack = set()
        for path in (ROOT / "skills").glob("*/SKILL.md"):
            frontmatter = yaml.safe_load(path.read_text(encoding="utf-8").split("---", 2)[1])
            if frontmatter.get("metadata", {}).get("category") == "stack-and-domain":
                stack.add(path.parent.name)
        self.assertTrue(stack <= routed)
        self.assertEqual("advisory-only-not-selection", registry["selectionPolicy"]["promptKeywords"])
        self.assertEqual("blocked", registry["selectionPolicy"]["missingRequiredSkill"])

    def test_explorer_data_joins_roles_routes_and_evidence(self) -> None:
        text = EXPLORER_DATA.read_text(encoding="utf-8")
        self.assertIn("DEV_METHODOLOGY_AGENT_SKILL_EXPLORER_DATA", text)
        self.assertIn('"kind": "fixed"', text)
        self.assertIn('"kind": "routed"', text)
        self.assertIn('"evidenceStatus"', text)


if __name__ == "__main__":
    unittest.main()
