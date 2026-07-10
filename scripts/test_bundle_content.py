# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Modified with AI assistance.
# Summary: Verifies the distributable methodology bundle, generated artifacts, roles, and documentation contracts.

from __future__ import annotations

import importlib.util
import sys
import tempfile
import tomllib
import unittest
from dataclasses import replace
from pathlib import Path
from types import ModuleType

import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
README_PATH = REPOSITORY_ROOT / "README.md"
AGENTS_PATH = REPOSITORY_ROOT / "AGENTS.md"
SKILLS_ROOT = REPOSITORY_ROOT / "skills"
SKILL_CATEGORIES_PATH = REPOSITORY_ROOT / "design" / "skill-categories.yaml"
SKILL_DEFINITIONS_PATH = REPOSITORY_ROOT / "design" / "generated" / "skill-definitions.js"
ROLE_SCHEMA_PATH = REPOSITORY_ROOT / "agents" / "role-schema.yaml"
MODEL_PROFILES_PATH = REPOSITORY_ROOT / "agents" / "model-profiles.yaml"
ADAPTER_MODEL_PROFILE_PATHS = {
    "codex": REPOSITORY_ROOT / "adapters" / "codex" / "model-profiles.yaml",
    "claude": REPOSITORY_ROOT / "adapters" / "claude" / "model-profiles.yaml",
}
ROLE_DEFINITIONS_PATH = REPOSITORY_ROOT / "design" / "generated" / "role-definitions.js"
SUPPORT_CHECKLIST_PATH = REPOSITORY_ROOT / "design" / "agent-skill-test-coverage-checklist.md"
AGENT_BROWSER_PATH = REPOSITORY_ROOT / "design" / "agent-browser.js"
GENERATED_ADAPTERS_ROOT = REPOSITORY_ROOT / "generated" / "adapters"
BUILD_SKILL_DOCS_PATH = REPOSITORY_ROOT / "scripts" / "build-skill-docs.py"
BUILD_SKILL_DOCS_MODULE_NAME = "build_skill_docs"
REMOVED_ROOT_FILES = (
    "documentation-methodology.md",
    "procedure-reverse-engineer-project-documentation.md",
)
REMOVED_DEVELOPMENT_REFERENCES = (
    "documentation-methodology.md",
    "procedure-reverse-engineer-project-documentation.md",
)
NEW_WORKFLOW_SKILLS = (
    "documentation-bootstrap",
    "documentation-reverse-engineering",
    "code-project-wiki",
    "documentation-page-verifier",
    "create-agents-plan",
    "maintain-methodology-documentation",
)
NEW_DEVELOPMENT_SKILLS = (
    "detect-technology-skills",
    "code-discovery",
    "test-strategy",
    "end-to-end-verification",
    "application-security",
    "user-experience-review",
    "prompt-contracts",
    "code-comments",
    "code-review-evidence",
    "test-driven-development",
    "code-execution-tracing",
    "root-cause-analysis",
    "runtime-evidence-collection",
    "create-unit-test-plan",
    "review-unit-test-plan",
    "typescript-coding",
    "python-coding",
    "fastapi",
    "java-coding",
    "spring-boot",
    "sql-coding",
)
AGENTS_PLAN_SKILL = "create-agents-plan"
AGENTS_PLAN_TEMPLATE = "agents-plan-template.yaml"
AGENTS_PLAN_ARTIFACT = "AGENTS-PLAN.yaml"
ARTIFACT_CREATION_SKILLS = (
    (
        "create-project-wiki",
        "project-wiki-template.md",
        "review-project-wiki",
    ),
    (
        "create-functional-spec",
        "functional-spec-template.md",
        "review-functional-spec",
    ),
    (
        "create-architecture",
        "architecture-template.md",
        "review-architecture",
    ),
    (
        "create-high-level-design",
        "high-level-design-template.md",
        "review-high-level-design",
    ),
    (
        "create-module-design",
        "module-design-template.md",
        "review-module-design",
    ),
    (
        "create-unit-test-plan",
        "unit-test-plan-template.md",
        "review-unit-test-plan",
    ),
)
WIKI_ROLE_SKILLS = {
    "project-wiki",
    "project-wiki-query",
    "project-wiki-research",
    "project-wiki-topic-writer",
    "project-wiki-topic-verifier",
    "code-project-wiki",
    "create-project-wiki",
    "review-project-wiki",
}
WIKI_ACTIVITY_ROLES = {
    "public-source-collector",
    "wiki-artifact-reviewer",
    "wiki-ingest-agent",
    "wiki-query-agent",
    "wiki-research-agent",
    "wiki-setup-agent",
    "wiki-topic-verifier",
    "wiki-writer-agent",
}
ARTIFACT_REVIEW_SKILLS = (
    ("review-project-wiki", "project-wiki"),
    ("review-functional-spec", "functional-spec"),
    ("review-architecture", "architecture"),
    ("review-high-level-design", "high-level-design"),
    ("review-module-design", "module-design"),
    ("review-unit-test-plan", "unit-test-plan"),
)
ALL_REVIEW_SKILLS = ARTIFACT_REVIEW_SKILLS + (
    ("review-structured", "structured"),
)
EXAMPLE_PROJECT_SKILL_PACKS = (
    "api-routes",
    "clerk-auth",
    "electron-main",
    "electron-preload",
    "harness-implementation",
    "java-coding",
    "jest",
    "langgraph",
    "local-model-integration",
    "nextjs-app-router",
    "node-cli",
    "plan-engine-implementation",
    "playwright",
    "postgres-drizzle",
    "react-server-components",
    "react-vite-renderer",
    "tailwind-design-system",
    "tool-runtime-implementation",
    "spring-boot",
    "sql-coding",
    "typescript-coding",
    "typescript-esm",
    "typescript-strict",
    "vitest",
)
README_REQUIRED_PHRASES = (
    "Use the installed skills as the operating surface.",
    "documentation-bootstrap",
    "documentation-reverse-engineering",
    "code-project-wiki",
    "documentation-page-verifier",
    "create-agents-plan",
    "AGENTS-PLAN.yaml",
    "detection.yaml",
    "python3 scripts/build-technology-detection.py",
    "detect-technology-skills",
    "Agent role, task wording, prompt keywords, read confirmation, and optional local commands are not detection inputs",
    "create-project-wiki",
    "create-functional-spec",
    "create-architecture",
    "create-high-level-design",
    "create-module-design",
    "review-project-wiki",
    "review-functional-spec",
    "review-architecture",
    "review-high-level-design",
    "review-module-design",
    "Junie CLI",
    "--adapter junie",
    "skills/development-methodology/assets/templates",
    "python3 scripts/validate-agent-skills.py skills",
    "python3 scripts/refresh-shared-skills.py",
    "ownership manifest",
    "prune mode removes obsolete skills",
    "Keep Codex openai.yaml metadata beside each source SKILL.md",
    "Before renaming or deleting a source skill",
    "role definitions",
    "dispatch profiles",
    "Review Skill Checklist Convention",
    "review-checklist-[review-target].md",
    "artifact-name.review-checklist-[review-target].md",
    "python3 scripts/build-skill-docs.py",
    "python3 scripts/build-support-checklist.py",
    "design/generated/skill-definitions.js",
    "design/generated/role-definitions.js",
    "design/skill-categories.yaml",
    "agents/role-schema.yaml",
    "generated/adapters",
    "--install-agents",
    "--replace-customized",
    "maintain-methodology-documentation",
    "three-way discrepancy analysis",
    "A skill entry with a condition is request-specific",
    "repoRoot query parameter",
    "Code Comments is a fixed skill for Coding Agent and Code Review Agent.",
)
DEVELOPMENT_METHODOLOGY_REQUIRED_PHRASES = (
    "When a skill or role was renamed or deleted",
    "Do not remove unowned local skills or agents manually.",
    "generated agent installs",
    "sweep the source repository for the old skill id",
    "Codex metadata",
    "aggregate workflow examples",
    "Load only the skills needed for the current job.",
    "Artifact Creation Routes",
    "create-agents-plan",
    "agents-plan-template.yaml",
    "AGENTS-PLAN.yaml",
    "When the user, target file type, runtime schema, existing document, or surrounding documentation indicates a specific structure or format, preserve that structure.",
    "Use the shared page contract only when the selected artifact type requires it.",
)
STRATEGY_REQUIRED_PHRASES = (
    "Before a rename or deletion",
    "update role definitions, Codex metadata, skills, dispatch profiles",
)
AGENT_ROLE_MAP_REQUIRED_PHRASES = (
    "Role Agent Categories",
    "Methodology Maintenance Agents",
    "Project Setup And Update Agents",
    "Development Use Agents",
    "DEV_METHODOLOGY_ROLE_DEFINITIONS",
    "loadout-details",
    "generated/skill-definitions.js",
    "generated/role-definitions.js",
    "agent-browser.js",
    "skill-browser.js",
    "agent-card__heading",
    'definitionButton.textContent = "View"',
    "agent-grid",
    "grid-template-columns: repeat(3, minmax(0, 1fr));",
    "Skills",
    "Outputs",
    ".tag.output",
    ".tag.conditional-skill",
    ".tag.technology-skill",
    "technology-skill-detection-registry.js",
    "Interactive Agent And Skill Map",
    "select a skill to see every canonical agent that uses it.",
    "intentionally omitted from this map.",
    'class="hierarchy-embed"',
    "Open the interactive SVG diagram",
    'id="agent-skill-hierarchy"',
    "dev-methodology:view-definition",
    "event.source !== hierarchyMap.contentWindow",
    "openDefinitionFromHierarchy",
)
AGENT_DEFINITION_FORMATS_REQUIRED_PHRASES = (
    "Agent Definition Runtime Formats",
    "OpenAI Codex Subagents",
    "Claude Code Subagents",
    "Gemini CLI Subagents",
    "Junie CLI Custom Subagents",
    "GitHub Copilot Agent Mode",
    "GitHub Copilot Custom Agents",
    "GitHub Copilot Agent Skills",
    "Properties We Use",
    "Properties We Ignore",
    "Behavior We Default",
    "Skills, Tools, And MCP",
    "Runtime Controls",
    "[mcp_servers.name]",
    "[[skills.config]]",
    "~/.codex/config.toml",
    ".codex/config.toml",
    "prefix_rule",
    "Common Source Mapping",
    "Use A Common Role Source",
    "Generate Runtime Adapters",
    "Validate Against Skills",
    "Keep HTML Pure",
    "Fixed Roles And Setup-Time Technology Detection",
    "skills[].condition",
    "request-specific skill conditions",
    "design/generated/role-definitions.js",
)
DEVELOPMENT_USE_LOADOUTS = (
    "Development Orchestrator",
    "Coding Agent",
    "Code Review Agent",
    "QA And Verification Agent",
    "Documentation Writer",
    "Artifact Review Agent",
    "E2E Browser Agent",
    "UX Designer Or Reviewer",
    "Security Reviewer",
    "Runtime Diagnostician",
    "Prompt Contract Reviewer",
)
AGENT_ROLE_MAP_FORBIDDEN_PHRASES = (
    "const ROLE_LOADOUTS",
    "Default Skill Loadouts",
    "loadout-title",
    "Primary skills",
    "Optional skills",
    "expand-button",
    ".tag.optional",
    "Optional Specialist Roles",
    "specialists-title",
    "<span class=\"tag role\">",
    "card specialist",
    "tag specialist",
    "Full Model, Agent, And Skill Hierarchy",
    '<img src="agent-skill-hierarchy.svg"',
)
README_FORBIDDEN_PHRASES = (
    "Copy documentation-methodology.md",
    "Copy the templates folder",
    "procedure-reverse-engineer-project-documentation.md before treating the wiki as complete",
    "okf-skill-validate skills/*",
)
REVERSE_ENGINEERING_DISCOVERY_PHRASES = (
    "## Code Discovery Tools",
    "Use a routed structure-aware search tool when discovery depends on syntax, nesting, imports, exports, callers, route declarations, component shapes, async flow, error handling, or test structure.",
    "Confirm an optional search tool is available before using it.",
    "If it is unavailable, continue with text search, repository file walking, and direct source reading.",
    "Do not treat structural matches as documentation evidence until the matched code has been read.",
)
DOCUMENTATION_PAGE_VERIFIER_REVIEW_PHRASES = (
    "completed review checklist",
    "quoted evidence",
    "assessment",
    "Do not complete verification from memory",
    "## Format Selection",
    "When a specific structure or format is indicated, that structure is authoritative.",
    "Do not require shared page sections unless the selected artifact is a docs/wiki page",
)
AGENTS_REQUIRED_PHRASES = (
    "repo-local operating contract",
    "Do not create separate skill files for repo-local maintenance procedures.",
    "Update README.md when the public skill inventory",
    "Update the design HTML files that describe skills, agents",
    "Keep Codex openai.yaml metadata beside each source SKILL.md",
    "Run scripts/openai_metadata.py skills after skill name or description changes so derived Codex interface fields stay aligned while policy and dependencies remain hand-authored.",
    "python3 scripts/validate-agent-skills.py skills",
    "python3 scripts/refresh-shared-skills.py",
)


def review_checklist_name(review_target: str) -> str:
    return f"review-checklist-{review_target}.md"


def completed_review_checklist_suffix(review_target: str) -> str:
    return f".review-checklist-{review_target}.md"


def openai_metadata_path(skill_name: str) -> Path:
    return SKILLS_ROOT / skill_name / "agents" / "openai.yaml"


def load_build_skill_docs_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        BUILD_SKILL_DOCS_MODULE_NAME,
        BUILD_SKILL_DOCS_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load build-skill-docs.py.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[BUILD_SKILL_DOCS_MODULE_NAME] = module
    spec.loader.exec_module(module)
    return module


def load_yaml_object(path: Path) -> dict[str, object]:
    parsed = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(parsed, dict):
        raise AssertionError(f"Expected YAML object in {path}")
    return parsed


def load_yaml_object_from_frontmatter(path: Path) -> dict[str, object]:
    parts = path.read_text(encoding="utf-8").split("---", maxsplit=2)
    if len(parts) != 3:
        raise AssertionError(f"Expected YAML frontmatter in {path}")
    parsed = yaml.safe_load(parts[1])
    if not isinstance(parsed, dict):
        raise AssertionError(f"Expected YAML frontmatter object in {path}")
    return parsed


def css_hex_property(styles: str, selector: str, property_name: str) -> str:
    rule_marker = f"{selector} {{"
    if rule_marker not in styles:
        raise AssertionError(f"Missing CSS selector {selector}")
    rule_body = styles.split(rule_marker, maxsplit=1)[1].split("}", maxsplit=1)[0]
    property_marker = f"{property_name}:"
    for declaration in rule_body.split(";"):
        if declaration.strip().startswith(property_marker):
            return declaration.split(":", maxsplit=1)[1].strip()
    raise AssertionError(f"Missing CSS property {property_name} in {selector}")


def wcag_contrast_ratio(first_hex: str, second_hex: str) -> float:
    def relative_luminance(hex_color: str) -> float:
        channels = [
            int(hex_color[index:index + 2], 16) / 255
            for index in (1, 3, 5)
        ]
        linear_channels = [
            channel / 12.92
            if channel <= 0.04045
            else ((channel + 0.055) / 1.055) ** 2.4
            for channel in channels
        ]
        return (
            0.2126 * linear_channels[0]
            + 0.7152 * linear_channels[1]
            + 0.0722 * linear_channels[2]
        )

    first_luminance = relative_luminance(first_hex)
    second_luminance = relative_luminance(second_hex)
    lighter = max(first_luminance, second_luminance)
    darker = min(first_luminance, second_luminance)
    return (lighter + 0.05) / (darker + 0.05)


class BundleContentTests(unittest.TestCase):
    def test_redundant_root_manuals_are_removed(self) -> None:
        for file_name in REMOVED_ROOT_FILES:
            with self.subTest(file_name=file_name):
                self.assertFalse((REPOSITORY_ROOT / file_name).exists())

    def test_root_templates_are_not_a_second_distribution_surface(self) -> None:
        self.assertFalse((REPOSITORY_ROOT / "templates").exists())

    def test_development_methodology_does_not_copy_monolithic_references(self) -> None:
        references_root = SKILLS_ROOT / "development-methodology" / "references"

        for file_name in REMOVED_DEVELOPMENT_REFERENCES:
            with self.subTest(file_name=file_name):
                self.assertFalse((references_root / file_name).exists())

    def test_workflow_skills_and_codex_metadata_are_packaged(self) -> None:
        for skill_name in NEW_WORKFLOW_SKILLS:
            with self.subTest(skill_name=skill_name):
                self.assertTrue((SKILLS_ROOT / skill_name / "SKILL.md").is_file())
                self.assertTrue(openai_metadata_path(skill_name).is_file())

    def test_new_development_skills_and_codex_metadata_are_packaged(self) -> None:
        for skill_name in NEW_DEVELOPMENT_SKILLS:
            with self.subTest(skill_name=skill_name):
                self.assertTrue((SKILLS_ROOT / skill_name / "SKILL.md").is_file())
                self.assertTrue(openai_metadata_path(skill_name).is_file())

    def test_code_comments_is_a_core_coding_and_review_contract(self) -> None:
        skill_root = SKILLS_ROOT / "code-comments"
        skill_text = (skill_root / "SKILL.md").read_text(encoding="utf-8")
        checklist_text = (
            skill_root / "references" / "review-checklist-code-comments.md"
        ).read_text(encoding="utf-8")

        for phrase in (
            "Mandatory Code Artifact Header",
            "Do not require code headers in configuration",
            "load structured-explanation",
            "copyright statement defined by the applicable root, nearest, or global AGENTS.md",
            "accurate AI attribution",
            "AI attribution: Generated with AI assistance.",
            "public or exported construct",
            "valid values",
            "Observable side effects",
            "verify the implementation against it",
        ):
            with self.subTest(skill_phrase=phrase):
                self.assertIn(phrase, skill_text)

        for phrase in (
            "applicable AGENTS.md exactly",
            "generated with AI assistance",
            "public or exported construct",
            "respect the intent claimed by its comments",
        ):
            with self.subTest(checklist_phrase=phrase):
                self.assertIn(phrase, checklist_text)

        for role_name in ("coding-agent", "code-review-agent"):
            role_path = (
                REPOSITORY_ROOT
                / "agents"
                / "roles"
                / "development-use"
                / f"{role_name}.role.yaml"
            )
            role_source = load_yaml_object(role_path)
            code_comments_entries = [
                entry["code-comments"]
                for entry in role_source["skills"]
                if "code-comments" in entry
            ]
            with self.subTest(role_name=role_name):
                self.assertEqual(1, len(code_comments_entries))
                self.assertEqual({"justification"}, set(code_comments_entries[0]))

    def test_artifact_creation_skills_route_to_templates_and_reviews(self) -> None:
        development_methodology_text = (
            SKILLS_ROOT / "development-methodology" / "SKILL.md"
        ).read_text(encoding="utf-8")

        for skill_name, template_name, review_skill_name in ARTIFACT_CREATION_SKILLS:
            with self.subTest(skill_name=skill_name):
                skill_path = SKILLS_ROOT / skill_name / "SKILL.md"
                template_path = (
                    SKILLS_ROOT
                    / "development-methodology"
                    / "assets"
                    / "templates"
                    / template_name
                )
                metadata_path = openai_metadata_path(skill_name)

                self.assertTrue(skill_path.is_file())
                self.assertTrue(template_path.is_file())
                self.assertTrue(metadata_path.is_file())

                skill_text = skill_path.read_text(encoding="utf-8")

                self.assertIn(template_name, skill_text)
                self.assertIn(review_skill_name, skill_text)
                self.assertIn("Replace every TODO instruction", skill_text)
                self.assertIn("documentation-page-verifier", skill_text)
                self.assertIn(skill_name, development_methodology_text)
                self.assertIn(template_name, development_methodology_text)
                self.assertIn(review_skill_name, development_methodology_text)

    def test_agents_plan_skill_routes_to_template_and_verifier(self) -> None:
        development_methodology_text = (
            SKILLS_ROOT / "development-methodology" / "SKILL.md"
        ).read_text(encoding="utf-8")
        skill_path = SKILLS_ROOT / AGENTS_PLAN_SKILL / "SKILL.md"
        template_path = (
            SKILLS_ROOT
            / "development-methodology"
            / "assets"
            / "templates"
            / AGENTS_PLAN_TEMPLATE
        )
        metadata_path = openai_metadata_path(AGENTS_PLAN_SKILL)

        self.assertTrue(skill_path.is_file())
        self.assertTrue(template_path.is_file())
        self.assertTrue(metadata_path.is_file())

        skill_text = skill_path.read_text(encoding="utf-8")
        template_text = template_path.read_text(encoding="utf-8")

        self.assertIn(AGENTS_PLAN_TEMPLATE, skill_text)
        self.assertIn(AGENTS_PLAN_ARTIFACT, skill_text)
        self.assertIn("Replace every TODO instruction", skill_text)
        self.assertIn("documentation-page-verifier", skill_text)
        self.assertIn("customer-safe examples", skill_text)
        self.assertIn("schema: agents-plan", template_text)
        self.assertIn("proprietary_validation_notes:", template_text)
        self.assertIn("nested_agents_plan_files:", template_text)
        self.assertIn("claude_bridge_files:", template_text)
        self.assertIn("thin CLAUDE.md", skill_text)
        self.assertIn(AGENTS_PLAN_SKILL, development_methodology_text)
        self.assertIn(AGENTS_PLAN_TEMPLATE, development_methodology_text)
        self.assertIn("documentation-page-verifier", development_methodology_text)

    def test_artifact_review_skills_have_checklists_and_metadata(self) -> None:
        development_methodology_text = (
            SKILLS_ROOT / "development-methodology" / "SKILL.md"
        ).read_text(encoding="utf-8")

        for skill_name, review_target in ARTIFACT_REVIEW_SKILLS:
            with self.subTest(skill_name=skill_name):
                checklist_name = review_checklist_name(review_target)
                skill_path = SKILLS_ROOT / skill_name / "SKILL.md"
                checklist_path = SKILLS_ROOT / skill_name / "references" / checklist_name
                metadata_path = openai_metadata_path(skill_name)

                self.assertTrue(skill_path.is_file())
                self.assertTrue(checklist_path.is_file())
                self.assertTrue(metadata_path.is_file())

                skill_text = skill_path.read_text(encoding="utf-8")
                checklist_text = checklist_path.read_text(encoding="utf-8")

                self.assertIn(checklist_name, skill_text)
                self.assertIn("documentation-page-verifier", skill_text)
                self.assertIn("Review Checklist", checklist_text)
                self.assertIn("Findings", checklist_text)
                self.assertIn(skill_name, development_methodology_text)

    def test_review_skills_follow_checklist_evidence_contract(self) -> None:
        for skill_name, review_target in ALL_REVIEW_SKILLS:
            with self.subTest(skill_name=skill_name):
                checklist_name = review_checklist_name(review_target)
                completed_suffix = completed_review_checklist_suffix(review_target)
                skill_path = SKILLS_ROOT / skill_name / "SKILL.md"
                checklist_path = SKILLS_ROOT / skill_name / "references" / checklist_name

                self.assertTrue(skill_path.is_file())
                self.assertTrue(checklist_path.is_file())

                skill_text = skill_path.read_text(encoding="utf-8")
                checklist_text = checklist_path.read_text(encoding="utf-8")

                self.assertIn(checklist_name, skill_text)
                self.assertIn(completed_suffix, skill_text)
                self.assertIn("completed review checklist", skill_text)
                self.assertIn("Question:", checklist_text)
                self.assertIn("Status:", checklist_text)
                self.assertIn("Quoted evidence:", checklist_text)
                self.assertIn("Assessment:", checklist_text)
                self.assertIn("?", checklist_text)

    def test_documentation_page_verifier_uses_completed_checklist_evidence(self) -> None:
        skill_text = (
            SKILLS_ROOT / "documentation-page-verifier" / "SKILL.md"
        ).read_text(encoding="utf-8")

        for phrase in DOCUMENTATION_PAGE_VERIFIER_REVIEW_PHRASES:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, skill_text)

    def test_example_project_skill_packs_are_packaged(self) -> None:
        for skill_name in EXAMPLE_PROJECT_SKILL_PACKS:
            with self.subTest(skill_name=skill_name):
                skill_path = SKILLS_ROOT / skill_name / "SKILL.md"
                self.assertTrue(skill_path.is_file())
                self.assertTrue(openai_metadata_path(skill_name).is_file())

    def test_skill_frontmatter_uses_agent_skill_schema(self) -> None:
        for skill_path in sorted(SKILLS_ROOT.glob("*/SKILL.md")):
            with self.subTest(skill_path=skill_path):
                skill_text = skill_path.read_text(encoding="utf-8")
                frontmatter_text = skill_text.split("---", maxsplit=2)[1]
                frontmatter = yaml.safe_load(frontmatter_text)

                self.assertIsInstance(frontmatter, dict)
                self.assertIn("name", frontmatter)
                self.assertIn("description", frontmatter)
                self.assertNotIn("type", frontmatter)

    def test_skill_categories_are_declared_in_skill_metadata(self) -> None:
        category_data = load_yaml_object(SKILL_CATEGORIES_PATH)
        categories = category_data.get("categories")
        self.assertIsInstance(categories, list)
        category_ids = {
            category["id"]
            for category in categories
            if isinstance(category, dict) and isinstance(category.get("id"), str)
        }

        for skill_path in sorted(SKILLS_ROOT.glob("*/SKILL.md")):
            with self.subTest(skill_path=skill_path):
                skill_text = skill_path.read_text(encoding="utf-8")
                frontmatter = yaml.safe_load(skill_text.split("---", maxsplit=2)[1])
                self.assertIsInstance(frontmatter, dict)
                metadata = frontmatter.get("metadata")
                self.assertIsInstance(metadata, dict)
                category = metadata.get("category")
                self.assertIn(category, category_ids)

    def test_generated_skill_definition_data_is_current(self) -> None:
        build_skill_docs = load_build_skill_docs_module()
        rendered = build_skill_docs.render_javascript(build_skill_docs.build_payload())
        self.assertEqual(
            rendered,
            SKILL_DEFINITIONS_PATH.read_text(encoding="utf-8"),
        )

    def test_canonical_roles_generate_current_documentation_and_adapters(self) -> None:
        build_skill_docs = load_build_skill_docs_module()
        skill_payload = build_skill_docs.build_payload()
        roles = build_skill_docs.load_role_definitions(set(skill_payload["skills"]))
        expected_outputs = build_skill_docs.expected_role_outputs(roles)

        self.assertTrue(ROLE_SCHEMA_PATH.is_file())
        role_schema = load_yaml_object(ROLE_SCHEMA_PATH)
        self.assertEqual(2, role_schema["version"])
        self.assertEqual(
            "conditional-skill-entry-list",
            role_schema["properties"]["skills"],
        )
        self.assertEqual(
            expected_outputs[ROLE_DEFINITIONS_PATH],
            ROLE_DEFINITIONS_PATH.read_text(encoding="utf-8"),
        )
        for output_path, expected_content in expected_outputs.items():
            with self.subTest(output_path=output_path):
                self.assertTrue(output_path.is_file())
                self.assertEqual(expected_content, output_path.read_text(encoding="utf-8"))

        skill_names = set(skill_payload["skills"])
        role_payload = build_skill_docs.build_role_payload(roles)
        for role in roles:
            with self.subTest(role=role.name):
                self.assertTrue(set(role.skills).issubset(skill_names))
                role_source = yaml.safe_load(role.yaml)
                self.assertNotIn("skillComments", role_source)
                self.assertNotIn("outputComments", role_source)
                self.assertEqual(
                    list(role.skills),
                    [next(iter(entry)) for entry in role_source["skills"]],
                )
                self.assertEqual(
                    list(role.output_contract),
                    [next(iter(entry)) for entry in role_source["outputContract"]],
                )
                self.assertTrue(all(
                    set(next(iter(entry.values())))
                    in ({"justification"}, {"justification", "condition"})
                    for entry in role_source["skills"]
                ))
                self.assertTrue(
                    all(
                        set(next(iter(entry.values()))) == {"purpose"}
                        for entry in role_source["outputContract"]
                    )
                )
                self.assertEqual(
                    (REPOSITORY_ROOT / role.source_path).read_text(encoding="utf-8"),
                    role.yaml,
                )
                self.assertEqual(role.yaml, role_payload["roles"][role.name]["yaml"])
                self.assertIsInstance(role_payload["roles"][role.name]["examples"], list)
                self.assertEqual(
                    set(role.skills),
                    set(role_payload["roles"][role.name]["skillJustifications"]),
                )
                expected_conditions = {
                    skill: metadata["condition"].rstrip(".")
                    for entry in role_source["skills"]
                    for skill, metadata in entry.items()
                    if "condition" in metadata
                }
                self.assertEqual(expected_conditions, role.skill_conditions)
                self.assertEqual(
                    expected_conditions,
                    role_payload["roles"][role.name]["skillConditions"],
                )
                self.assertEqual(
                    set(role.output_contract),
                    set(role_payload["roles"][role.name]["outputPurposes"]),
                )
                for example in role_payload["roles"][role.name]["examples"]:
                    self.assertEqual(
                        set(example),
                        {"purpose", "runtimeInvocations", "plausibleResponse"},
                    )
                    self.assertEqual(
                        set(example["runtimeInvocations"]),
                        {"codex", "claude-code"},
                    )
                    for invocation in example["runtimeInvocations"].values():
                        self.assertIsInstance(invocation, str)
                        self.assertTrue(invocation.strip())
                if role.name == "documentation-writer":
                    self.assertEqual(
                        "when describing user-visible functionality, actor workflows, acceptance criteria, permissions, states, or error behavior",
                        role.skill_conditions["create-functional-spec"],
                    )
                    for example in role_payload["roles"][role.name]["examples"]:
                        self.assertTrue(
                            example["runtimeInvocations"]["codex"].startswith("$documentation-writer ")
                        )
                codex_agent_path = (
                    GENERATED_ADAPTERS_ROOT / "codex" / "agents" / f"{role.filename}.toml"
                )
                self.assertTrue(codex_agent_path.is_file())
                codex_agent_text = codex_agent_path.read_text(encoding="utf-8")
                self.assertIn('developer_instructions = """\n', codex_agent_text)
                self.assertIn("# Skill justifications:", codex_agent_text)
                if role.skill_conditions:
                    self.assertIn("# Request-specific skill conditions:", codex_agent_text)
                    self.assertIn("Use judgment when the request is ambiguous", codex_agent_text)
                    for skill, condition in role.skill_conditions.items():
                        self.assertIn(f"Use the {skill} skill {condition}.", codex_agent_text)
                self.assertIn("# Output purposes:", codex_agent_text)
                self.assertEqual(
                    build_skill_docs.role_instruction_text(role),
                    tomllib.loads(codex_agent_text)["developer_instructions"],
                )
                self.assertIn(
                    "Before acting, load these fixed-role skills completely; they govern the work:",
                    codex_agent_text,
                )
                if "skillAvailability" not in role.optional_fields:
                    self.assertNotIn("[[skills.config]]", codex_agent_text)
                self.assertTrue(
                    (GENERATED_ADAPTERS_ROOT / "claude" / "agents" / f"{role.filename}.md").is_file()
                )
                claude_agent_text = (
                    GENERATED_ADAPTERS_ROOT / "claude" / "agents" / f"{role.filename}.md"
                ).read_text(encoding="utf-8")
                self.assertIn("Skill justifications:", claude_agent_text)
                self.assertIn("Output purposes:", claude_agent_text)
                claude_frontmatter = yaml.safe_load(claude_agent_text.split("---", 2)[1])
                self.assertEqual(
                    list(build_skill_docs.fixed_role_skills(role)),
                    claude_frontmatter["skills"],
                )
                self.assertIn("These fixed-role skills are preloaded and govern the work", claude_agent_text)
                for skill, condition in role.skill_conditions.items():
                    self.assertNotIn(skill, claude_frontmatter["skills"])
                    self.assertIn(f"Use the {skill} skill {condition}.", claude_agent_text)

        non_setup_roles = [
            role for role in roles
            if role.name != "project-agent-setup-agent"
        ]
        self.assertTrue(all("detect-technology-skills" not in role.skills for role in non_setup_roles))
        setup_role = next(role for role in roles if role.name == "project-agent-setup-agent")
        self.assertIn("detect-technology-skills", setup_role.skills)

    def test_wiki_skills_are_owned_by_wiki_activity_roles(self) -> None:
        build_skill_docs = load_build_skill_docs_module()
        skill_payload = build_skill_docs.build_payload()
        roles = build_skill_docs.load_role_definitions(set(skill_payload["skills"]))
        wiki_roles = {role.name for role in roles if role.group == "wiki-activities"}

        self.assertEqual(WIKI_ACTIVITY_ROLES, wiki_roles)
        for role in roles:
            wiki_skills = set(role.skills) & WIKI_ROLE_SKILLS
            with self.subTest(role=role.name):
                if role.group == "wiki-activities":
                    self.assertTrue(wiki_skills)
                else:
                    self.assertFalse(wiki_skills)

    def test_dynamic_folder_skills_require_claude_skill_tool_in_restrictive_allowlist(self) -> None:
        build_skill_docs = load_build_skill_docs_module()
        skill_payload = build_skill_docs.build_payload()
        required, allowed, groups = build_skill_docs.load_role_schema()
        model_profiles = set(build_skill_docs.load_model_profiles())
        source_role = load_yaml_object(
            REPOSITORY_ROOT / "agents" / "roles" / "development-use" / "coding-agent.role.yaml"
        )
        source_role["tools"] = ["Read", "Grep"]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "development-use" / "coding-agent.role.yaml"
            path.parent.mkdir()
            path.write_text(yaml.safe_dump(source_role, sort_keys=False), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "must include Skill"):
                build_skill_docs.load_role_definition(
                    path,
                    required,
                    allowed,
                    groups,
                    set(skill_payload["skills"]),
                    model_profiles,
                )

    def test_nested_role_annotations_reject_invalid_shapes(self) -> None:
        build_skill_docs = load_build_skill_docs_module()
        skill_payload = build_skill_docs.build_payload()
        required, allowed, groups = build_skill_docs.load_role_schema()
        model_profiles = set(build_skill_docs.load_model_profiles())
        source_path = (
            REPOSITORY_ROOT
            / "agents"
            / "roles"
            / "development-use"
            / "documentation-writer.role.yaml"
        )

        wrong_annotation = load_yaml_object(source_path)
        first_skill = next(iter(wrong_annotation["skills"][0]))
        wrong_annotation["skills"][0][first_skill] = {"comment": "Describes the skill."}

        invalid_condition = load_yaml_object(source_path)
        conditional_metadata = next(
            metadata
            for entry in invalid_condition["skills"]
            for metadata in entry.values()
            if "condition" in metadata
        )
        conditional_metadata["condition"] = "on a matching request"

        parallel_legacy_map = load_yaml_object(source_path)
        parallel_legacy_map["skillComments"] = {
            next(iter(entry)): "Legacy comment."
            for entry in parallel_legacy_map["skills"]
        }

        for role_source, expected_error in (
            (wrong_annotation, "must contain justification and optional condition only"),
            (invalid_condition, "condition must be a non-empty fragment beginning with when"),
            (parallel_legacy_map, "unknown fields"),
        ):
            with self.subTest(expected_error=expected_error), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "development-use" / "documentation-writer.role.yaml"
                path.parent.mkdir()
                path.write_text(yaml.safe_dump(role_source, sort_keys=False), encoding="utf-8")
                with self.assertRaisesRegex(ValueError, expected_error):
                    build_skill_docs.load_role_definition(
                        path,
                        required,
                        allowed,
                        groups,
                        set(skill_payload["skills"]),
                        model_profiles,
                    )

    def test_codex_skill_availability_supports_name_and_path_overrides(self) -> None:
        build_skill_docs = load_build_skill_docs_module()
        skill_payload = build_skill_docs.build_payload()
        model_profiles = set(build_skill_docs.load_model_profiles())
        role = next(
            role for role in build_skill_docs.load_role_definitions(set(skill_payload["skills"]))
            if role.name == "coding-agent"
        )
        availability = [
            {"name": "python-coding", "enabled": False},
            {"path": "/opt/skills/fastapi", "enabled": True},
        ]
        role = replace(role, optional_fields={**role.optional_fields, "skillAvailability": availability})
        profiles = build_skill_docs.load_adapter_model_profiles("codex", model_profiles)
        rendered = build_skill_docs.render_codex_agent(role, profiles)
        parsed = tomllib.loads(rendered)
        self.assertEqual(
            [
                {"name": "python-coding", "enabled": False},
                {"path": "/opt/skills/fastapi", "enabled": True},
            ],
            parsed["skills"]["config"],
        )

    def test_model_profiles_are_semantic_and_adapter_complete(self) -> None:
        canonical = load_yaml_object(MODEL_PROFILES_PATH)["profiles"]
        self.assertEqual(
            {"simple", "default", "advanced", "advanced-long"},
            set(canonical),
        )

        adapter_profiles = {
            adapter: load_yaml_object(path)["profiles"]
            for adapter, path in ADAPTER_MODEL_PROFILE_PATHS.items()
        }
        for adapter, profiles in adapter_profiles.items():
            with self.subTest(adapter=adapter):
                self.assertEqual(set(canonical), set(profiles))
                for profile in profiles.values():
                    self.assertIsInstance(profile.get("model"), str)
                    self.assertTrue(profile["model"].strip())

        for profile in adapter_profiles["codex"].values():
            self.assertTrue(profile["model"].startswith("gpt-5.6-"))

        for role_path in sorted((REPOSITORY_ROOT / "agents" / "roles").glob("*/*.role.yaml")):
            with self.subTest(role_path=role_path):
                role = load_yaml_object(role_path)
                self.assertIn(role["modelProfile"], canonical)
                self.assertNotIn("model", role)
                self.assertNotIn("effort", role)
                for profile in role.get("modelStages", {}).values():
                    self.assertIn(profile, canonical)

    def test_agent_skill_evals_cover_implementation_and_independent_review(self) -> None:
        evals = load_yaml_object(REPOSITORY_ROOT / "evals" / "cases.yaml")["cases"]
        by_id = {case["id"]: case for case in evals}

        self.assertIn("typescript-order-pricing", by_id)
        self.assertIn("spring-boot-order-cancellation", by_id)
        for case in by_id.values():
            with self.subTest(code_comments_case=case["id"]):
                self.assertIn("code-comments", case["requiredSkills"])
        review_case = by_id["typescript-code-review"]
        self.assertTrue(review_case["expectVerifyFailure"])
        self.assertIn("code-review-evidence", review_case["requiredSkills"])
        self.assertEqual(3, len(review_case["requiredFindings"]))

    def test_support_checklist_covers_every_agent_and_skill(self) -> None:
        checklist = SUPPORT_CHECKLIST_PATH.read_text(encoding="utf-8")

        for role_path in sorted((REPOSITORY_ROOT / "agents" / "roles").glob("*/*.role.yaml")):
            role = load_yaml_object(role_path)
            with self.subTest(agent=role["name"]):
                self.assertIn(f"| {role['name']} |", checklist)

        for skill_path in sorted(SKILLS_ROOT.glob("*/SKILL.md")):
            skill_name = load_yaml_object_from_frontmatter(skill_path)["name"]
            with self.subTest(skill=skill_name):
                self.assertIn(f"- [x] {skill_name} — structural;", checklist)


    def test_readme_points_to_skill_based_setup(self) -> None:
        readme_text = README_PATH.read_text(encoding="utf-8")

        for phrase in README_REQUIRED_PHRASES:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, readme_text)

        for phrase in README_FORBIDDEN_PHRASES:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, readme_text)

    def test_agents_guidance_keeps_repo_maintenance_local(self) -> None:
        agents_text = AGENTS_PATH.read_text(encoding="utf-8")
        readme_text = README_PATH.read_text(encoding="utf-8")

        self.assertIn(
            "AGENTS.md contains repo-local maintenance directives",
            readme_text,
        )
        for phrase in AGENTS_REQUIRED_PHRASES:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, agents_text)

    def test_development_methodology_guides_skill_rename_cleanup(self) -> None:
        skill_text = (
            SKILLS_ROOT / "development-methodology" / "SKILL.md"
        ).read_text(encoding="utf-8")

        for phrase in DEVELOPMENT_METHODOLOGY_REQUIRED_PHRASES:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, skill_text)

    def test_strategy_guides_reference_sweep_for_skill_renames(self) -> None:
        strategy_text = (
            REPOSITORY_ROOT / "design" / "agent-skill-specialization-strategy.html"
        ).read_text(encoding="utf-8")

        for phrase in STRATEGY_REQUIRED_PHRASES:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, strategy_text)

    def test_agent_role_map_separates_lifecycle_categories(self) -> None:
        role_map_text = (
            REPOSITORY_ROOT / "design" / "agent-role-skill-map.html"
        ).read_text(encoding="utf-8")

        for phrase in AGENT_ROLE_MAP_REQUIRED_PHRASES:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, role_map_text)

        role_definitions_text = ROLE_DEFINITIONS_PATH.read_text(encoding="utf-8")
        for role_name in DEVELOPMENT_USE_LOADOUTS:
            with self.subTest(role_name=role_name):
                self.assertIn(
                    f'\"displayName\": \"{role_name}\"',
                    role_definitions_text,
                )

        for phrase in AGENT_ROLE_MAP_FORBIDDEN_PHRASES:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, role_map_text)

        agent_browser_text = AGENT_BROWSER_PATH.read_text(encoding="utf-8")
        for phrase in (
            "DEV_METHODOLOGY_ROLE_DEFINITIONS",
            "data-agent-definition",
            "agent-modal",
            "role.yaml",
            "repoRoot",
            "Escape",
            "Example scenarios",
            "View canonical role YAML",
            "Plausible response",
            "enhance-skill-definitions",
            ".skill-modal:not([hidden])",
            "skillJustifications",
            "skillConditions",
            "outputPurposes",
            "agent-modal__pill-comment",
            "agent-modal__pill--conditional",
            "runtimeInvocations",
            "agent-modal__runtime-select",
        ):
            with self.subTest(agent_browser_phrase=phrase):
                self.assertIn(phrase, agent_browser_text)
        self.assertIn(".agent-modal__yaml code {\n", agent_browser_text)
        self.assertIn(
            ".agent-modal__invocation-text code {\n",
            agent_browser_text,
        )
        self.assertIn('document.createElement("pre")', agent_browser_text)
        invocation_foreground = css_hex_property(
            agent_browser_text,
            ".agent-modal__invocation-text",
            "color",
        )
        invocation_background = css_hex_property(
            agent_browser_text,
            ".agent-modal__invocation-text",
            "background",
        )
        self.assertGreaterEqual(
            wcag_contrast_ratio(invocation_foreground, invocation_background),
            4.5,
        )
        self.assertNotIn("Condition:", agent_browser_text)

        skill_browser_text = (REPOSITORY_ROOT / "design" / "skill-browser.js").read_text(encoding="utf-8")
        self.assertIn("enhance-skill-definitions", skill_browser_text)
        self.assertIn("[data-skill-definition]", skill_browser_text)

    def test_user_experience_review_requires_measured_color_contrast(self) -> None:
        skill_root = SKILLS_ROOT / "user-experience-review"
        skill_text = (skill_root / "SKILL.md").read_text(encoding="utf-8")
        checklist_text = (
            skill_root / "references" / "review-checklist-user-experience-review.md"
        ).read_text(encoding="utf-8")

        self.assertIn("Measure text and essential non-text color contrast", skill_text)
        for phrase in (
            "code and syntax color",
            "at least 4.5:1 contrast",
            "at least 3:1 contrast",
            "default, hover, focus, selected, disabled, error",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, checklist_text)

    def test_agent_definition_formats_document_runtime_adapters(self) -> None:
        index_text = (REPOSITORY_ROOT / "index.html").read_text(encoding="utf-8")
        format_text = (
            REPOSITORY_ROOT / "design" / "agent-definition-runtime-formats.html"
        ).read_text(encoding="utf-8")

        self.assertIn("design/agent-definition-runtime-formats.html", index_text)

        for phrase in AGENT_DEFINITION_FORMATS_REQUIRED_PHRASES:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, format_text)

    def test_reverse_engineering_uses_structural_code_discovery(self) -> None:
        skill_text = (
            SKILLS_ROOT / "documentation-reverse-engineering" / "SKILL.md"
        ).read_text(encoding="utf-8")

        for phrase in REVERSE_ENGINEERING_DISCOVERY_PHRASES:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, skill_text)


if __name__ == "__main__":
    unittest.main()
