# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Modified with AI assistance.
# Summary: Verifies the distributable methodology bundle, generated artifacts, roles, and documentation contracts.

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sys
import tempfile
import tomllib
import unittest
from dataclasses import replace
from html.parser import HTMLParser
from pathlib import Path
from types import ModuleType

import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
README_PATH = REPOSITORY_ROOT / "README.md"
AGENTS_PATH = REPOSITORY_ROOT / "AGENTS.md"
SKILLS_ROOT = REPOSITORY_ROOT / "skills"
ROLES_ROOT = REPOSITORY_ROOT / "agents" / "roles"
SKILL_CATEGORIES_PATH = REPOSITORY_ROOT / "design" / "skill-categories.yaml"
SKILL_DEFINITIONS_PATH = REPOSITORY_ROOT / "design" / "generated" / "skill-definitions.js"
ROLE_SCHEMA_PATH = REPOSITORY_ROOT / "agents" / "role-schema.yaml"
MODEL_PROFILES_PATH = REPOSITORY_ROOT / "agents" / "model-profiles.yaml"
ADAPTER_MODEL_PROFILE_PATHS = {
    "codex": REPOSITORY_ROOT / "adapters" / "codex" / "model-profiles.yaml",
    "claude": REPOSITORY_ROOT / "adapters" / "claude" / "model-profiles.yaml",
    "gemini": REPOSITORY_ROOT / "adapters" / "gemini" / "model-profiles.yaml",
    "junie": REPOSITORY_ROOT / "adapters" / "junie" / "model-profiles.yaml",
}
ROLE_DEFINITIONS_PATH = REPOSITORY_ROOT / "design" / "generated" / "role-definitions.js"
SUPPORT_CHECKLIST_PATH = REPOSITORY_ROOT / "design" / "agent-skill-test-coverage-checklist.md"
AGENT_BROWSER_PATH = REPOSITORY_ROOT / "design" / "agent-browser.js"
GENERATED_ADAPTERS_ROOT = REPOSITORY_ROOT / "generated" / "adapters"
AGENT_GENERATION_MANIFEST_PATH = GENERATED_ADAPTERS_ROOT / "agent-generation-manifest.json"
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
    "documentation-reverse-engineer",
    "code-project-wiki",
    "documentation-page-verify",
    "create-project-configuration",
    "maintain-methodology-documentation",
    "skill-authoring",
    "name-methodology-artifacts",
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
    "organise-project-files",
    "create-unit-test-plan",
    "review-unit-test-plan",
    "typescript",
    "python",
    "fastapi",
    "java",
    "spring-boot",
    "sql",
)
PROJECT_CONFIGURATION_SKILL = "create-project-configuration"
PROJECT_TEMPLATE = "project-template.yaml"
PROJECT_ARTIFACT = "PROJECT.yaml"
ARTIFACT_CREATION_SKILLS = (
    (
        "project-wiki-create",
        "project-wiki-template.md",
        "project-wiki-review",
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
    "project-wiki-topic-write",
    "project-wiki-topic-verify",
    "code-project-wiki",
    "project-wiki-create",
    "project-wiki-review",
}
WIKI_ACTIVITY_ROLES = {
    "wiki-source-collector",
    "wiki-artifact-reviewer",
    "wiki-ingester",
    "wiki-query-responder",
    "wiki-researcher",
    "wiki-architect",
    "wiki-topic-verifier",
    "wiki-writer",
}
ARTIFACT_REVIEW_SKILLS = (
    ("project-wiki-review", "project-wiki"),
    ("review-functional-spec", "functional-spec"),
    ("review-architecture", "architecture"),
    ("review-high-level-design", "high-level-design"),
    ("review-module-design", "module-design"),
    ("review-unit-test-plan", "unit-test-plan"),
)
ALL_REVIEW_SKILLS = ARTIFACT_REVIEW_SKILLS + (
    ("review-structured-artifact", "structured"),
)
EXAMPLE_PROJECT_SKILL_PACKS = (
    "api-routes",
    "clerk-auth",
    "electron-main",
    "electron-preload",
    "agent-harness",
    "java",
    "jest",
    "langgraph",
    "local-model-integration",
    "nextjs-app-router",
    "node-cli",
    "plan-engine",
    "playwright",
    "postgres-drizzle",
    "react-server-components",
    "react-vite-renderer",
    "tailwind-design-system",
    "tool-runtime",
    "spring-boot",
    "sql",
    "typescript",
    "typescript-esm",
    "typescript-strict",
    "vitest",
)
README_REQUIRED_PHRASES = (
    "Use the repository skill sources and generated adapters as the operating surface.",
    "documentation-bootstrap",
    "documentation-reverse-engineer",
    "code-project-wiki",
    "documentation-page-verify",
    "create-project-configuration",
    "PROJECT.yaml",
    "detection.yaml",
    "python3 scripts/build-technology-detection.py",
    "detect-technology-skills",
    "The [specialization strategy](design/agent-skill-specialization-strategy.html) owns detector inputs",
    "project-wiki-create",
    "create-functional-spec",
    "create-architecture",
    "create-high-level-design",
    "create-module-design",
    "project-wiki-review",
    "review-functional-spec",
    "review-architecture",
    "review-high-level-design",
    "review-module-design",
    "Junie CLI",
    "--adapter junie",
    "Codex, Claude Code, Gemini CLI, and Junie CLI definitions",
    "Deploy the Gemini CLI bundle globally",
    "Deploy the Junie CLI bundle globally",
    "Use project-level skill and agent directories only when the project needs customized definitions",
    "skills/development-methodology/assets/templates",
    "python3 scripts/validate-agent-skills.py skills",
    "ownership manifest",
    "every destination must be supplied by the caller",
    "--remove-owned",
    "Unowned skills and agents are never removed.",
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
    "agent-generation-manifest.json",
    "--install-agents",
    "--replace-customized",
    "maintain-methodology-documentation",
    "skill-authoring",
    "three-way discrepancy analysis",
    "repoRoot query parameter",
    "Within the linked HTML design set, the documentation index assigns one owner to each substantive topic.",
    "The generated diagram and generated cards are the intentional duplicate views",
)
DEVELOPMENT_METHODOLOGY_REQUIRED_PHRASES = (
    "Do not copy this bundle's skills or generated agents into user-home runtime folders",
    "Run the installer only for an explicitly requested deployment with caller-supplied target directories.",
    "sweep the source repository for the old skill id",
    "Codex metadata",
    "aggregate workflow examples",
    "Load only the skills needed for the current job.",
    "Artifact Creation Routes",
    "create-project-configuration",
    "project-template.yaml",
    "PROJECT.yaml",
    "When the user, target file type, runtime schema, existing document, or surrounding documentation indicates a specific structure or format, preserve that structure.",
    "Use the shared page contract only when the selected artifact type requires it.",
)
STRATEGY_REQUIRED_PHRASES = (
    "Selection Model",
    "Deterministic Setup-Time Technology Detection",
    "When To Create A Specialized Agent",
    "Fixed role skill",
    "Request-specific skill",
    "Folder technology skill",
)
AGENT_ROLE_MAP_REQUIRED_PHRASES = (
    "Methodology Maintenance",
    "Project Setup",
    "Wiki Activities",
    "Dev Activities",
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
    "select a skill to see every agent that uses it.",
    "intentionally omitted from this map.",
    'class="hierarchy-embed"',
    "Open the interactive SVG diagram",
    'id="agent-skill-hierarchy"',
    "dev-methodology:view-definition",
    "event.source !== hierarchyMap.contentWindow",
    "openDefinitionFromHierarchy",
    "definitionReturnTarget",
)
GENERIC_AGENT_DEFINITIONS_REQUIRED_PHRASES = (
    "Agentic Configuration",
    "Choose The Context That Shapes The Code",
    "Configuration Has Three Layers",
    "Configuration File Locations",
    "&lt;project-root&gt;/.&lt;harness-name&gt;/agents/&lt;agent-name&gt;.md",
    "&lt;project-root&gt;/&lt;folder-path&gt;/AGENTS.md",
    "The Portability Problem",
    "Skills Have A Portable File Standard",
    "Agents Do Not Have One Portable Runtime File",
    "The source skill definition is also the runtime skill definition.",
    "From Logical Roles To Native Agents",
    "logical source definition, not a file that an agent harness loads directly",
    "Property conversion is not just a filename change",
    "Authoritative Runtime Sources",
    "OpenAI Codex Subagents",
    "Claude Code Subagents",
    "Gemini CLI Subagents",
    "Junie CLI Custom Subagents",
    "generated/adapters/gemini/agents/",
    "generated/adapters/junie/agents/",
    "GitHub Copilot Agent Mode",
    "GitHub Copilot Custom Agents",
    "agent-generation-manifest.json",
    "GitHub Copilot Agent Skills",
    "Logical Role Properties",
    "Properties We Ignore",
    "Behavior We Default",
    "Native Runtime Packaging",
    "[mcp_servers.name]",
    "[[skills.config]]",
    "prefix_rule",
    "Logical-To-Native Property Mapping",
    "skills[].condition",
    "skillAvailability",
    "fixedBehavior.userInvocable",
    "fixedBehavior.automaticDelegation",
    "design/generated/role-definitions.js",
)
DOCUMENT_INFORMATION_OWNERS = {
    "agentic-development-operating-model.html": (
        "Project Classification",
        "Project Guidance And Precedence",
    ),
    "orchestrated-development-lifecycle.html": (
        "Orchestrated Development Loop",
        "Execution Evidence",
    ),
    "agent-skill-specialization-strategy.html": STRATEGY_REQUIRED_PHRASES[:3],
    "agent-role-skill-map.html": (
        "Agent and Skill Definitions",
        "Interactive Agent And Skill Map",
        "Skill Catalog",
    ),
    "agent-skill-specialization-examples.html": (
        "Configuration Examples",
        "Northwind Tools: Root-Only Guidance",
        "Acme Ledger: Nested Tier Guidance",
        "Beacon Knowledge Base: Workflow Separation",
    ),
    "generic-agent-definitions-source.html": (
        "Choose The Context That Shapes The Code",
        "Configuration Has Three Layers",
        "Configuration File Locations",
        "The Portability Problem",
        "From Logical Roles To Native Agents",
        "Logical Role Properties",
        "Native Runtime Packaging",
        "Logical-To-Native Property Mapping",
    ),
}
DOCUMENT_FORBIDDEN_HEADINGS = {
    "agentic-development-operating-model.html": (
        "Role Agent Set",
        "Skill Load Model",
        "File Contracts",
    ),
    "agent-skill-specialization-strategy.html": (
        "Semantic Model Profiles",
        "Role Agent Dispatch Loop",
        "Root AGENTS.md Policy Pattern",
        "Nested AGENTS.md Shape",
        "Agent Set Normalization",
    ),
    "agent-role-skill-map.html": (
        "Reference Model",
        "Routing Rules",
        "Catalog Boundary",
    ),
    "agent-skill-specialization-examples.html": (
        "One-Command Project Bootstrap",
        "PROJECT.yaml Template Sections",
        "Project Setup Flow",
        "Example: Direct Customer Customization",
    ),
    "generic-agent-definitions-source.html": (
        "Current Understanding",
        "Related Code",
        "Related Tests",
        "Related Backlog Items",
        "Related Wiki Pages",
        "Decision",
        "Fixed Roles And Setup-Time Technology Detection",
        "Deployment And Update Policy",
        "Next Adapter Work",
        "Maintenance Notes",
    ),
}
DOCUMENT_REQUIRED_LINKS = {
    "agentic-development-operating-model.html": (
        "agent-role-skill-map.html",
        "agent-skill-specialization-strategy.html",
        "agent-skill-specialization-examples.html",
        "generic-agent-definitions-source.html",
        "orchestrated-development-lifecycle.html",
    ),
    "orchestrated-development-lifecycle.html": (
        "agentic-development-operating-model.html",
        "agent-role-skill-map.html",
    ),
    "agent-skill-specialization-strategy.html": (
        "agent-role-skill-map.html",
        "agentic-development-operating-model.html",
        "orchestrated-development-lifecycle.html",
        "generic-agent-definitions-source.html",
    ),
    "agent-role-skill-map.html": (
        "agent-skill-specialization-strategy.html",
        "orchestrated-development-lifecycle.html",
    ),
    "agent-skill-specialization-examples.html": (
        "agent-skill-specialization-strategy.html",
        "agentic-development-operating-model.html",
        "orchestrated-development-lifecycle.html",
        "../skills/development-methodology/assets/templates/project-template.yaml",
    ),
    "generic-agent-definitions-source.html": (
        "agent-role-skill-map.html",
        "agent-skill-specialization-strategy.html",
        "../README.md#explicit-target-deployment",
    ),
}
DEVELOPMENT_USE_LOADOUTS = (
    "Dev Orchestrator",
    "Dev Coder",
    "Dev Code Reviewer",
    "Dev Verifier",
    "Dev Documentation Writer",
    "Dev Artifact Reviewer",
    "Dev Browser Operator",
    "Dev UX Specialist",
    "Dev Security Reviewer",
    "Dev Runtime Diagnostician",
    "Dev Prompt Reviewer",
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
)


def review_checklist_name(review_target: str) -> str:
    return f"review-checklist-{review_target}.md"


def completed_review_checklist_suffix(review_target: str) -> str:
    return f".review-checklist-{review_target}.md"


def openai_metadata_path(skill_name: str) -> Path:
    return SKILLS_ROOT / skill_name / "agents" / "openai.yaml"


class VisibleProseParser(HTMLParser):
    """Collect visible prose blocks from hand-authored HTML."""

    def __init__(self) -> None:
        super().__init__()
        self._skip_depth = 0
        self._capture_tag: str | None = None
        self._buffer: list[str] = []
        self.blocks: list[str] = []

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        del attrs
        if tag in {"script", "style"}:
            self._skip_depth += 1
            return
        if (
            self._skip_depth == 0
            and self._capture_tag is None
            and tag in {"p", "li", "td"}
        ):
            self._capture_tag = tag
            self._buffer = []

    def handle_data(self, data: str) -> None:
        if self._skip_depth == 0 and self._capture_tag is not None:
            self._buffer.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style"} and self._skip_depth:
            self._skip_depth -= 1
            return
        if self._skip_depth == 0 and tag == self._capture_tag:
            block = re.sub(r"\s+", " ", "".join(self._buffer)).strip()
            if block:
                self.blocks.append(block)
            self._capture_tag = None
            self._buffer = []


def visible_prose_blocks(path: Path) -> list[str]:
    parser = VisibleProseParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser.blocks


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

    def test_user_home_shared_install_workflow_is_removed(self) -> None:
        for path in (
            REPOSITORY_ROOT / "scripts" / "refresh-shared-skills.py",
            REPOSITORY_ROOT / "scripts" / "test_refresh_shared_skills.py",
        ):
            with self.subTest(path=path):
                self.assertFalse(path.exists())
        for path in (
            README_PATH,
            AGENTS_PATH,
            SKILLS_ROOT / "development-methodology" / "SKILL.md",
            SKILLS_ROOT / "maintain-methodology-documentation" / "SKILL.md",
        ):
            with self.subTest(path=path):
                self.assertNotIn(
                    "scripts/refresh-shared-skills.py",
                    path.read_text(encoding="utf-8"),
                )

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

    def test_skill_authoring_contract_is_shared_by_maintainer_and_reviewer(self) -> None:
        skill_text = (SKILLS_ROOT / "skill-authoring" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        for phrase in (
            "Treat applicable root and nested project instructions supplied by the harness as already loaded.",
            "Do not tell ordinary task agents to locate, open, read, reread, or follow AGENTS.md",
            "Inspect an instruction file explicitly only when the task creates, updates, validates, renders, or reviews that file as an artifact",
            "Search the complete skill package for instruction-loading language before accepting it.",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, skill_text)

        for role_name in ("methodology-maintainer", "methodology-artifact-reviewer"):
            role_path = ROLES_ROOT / "methodology-maintenance" / f"{role_name}.role.yaml"
            role = load_yaml_object(role_path)
            role_skills = {
                next(iter(entry))
                for entry in role["skills"]
                if isinstance(entry, dict) and len(entry) == 1
            }
            with self.subTest(role=role_name):
                self.assertIn("skill-authoring", role_skills)

    def test_skills_and_roles_do_not_reissue_harness_instruction_loading(self) -> None:
        instruction_target = r"(?:AGENTS\.md|CLAUDE\.md|project instructions|repository coordination instructions)"
        manual_target = rf"(?:{instruction_target}|agent instructions)"
        manual_action = r"(?:read(?:s|ing)?|re[- ]?read(?:s|ing)?|open(?:s|ed|ing)?|locat(?:e|es|ed|ing)|follow(?:s|ed|ing)?|inspect(?:s|ed|ing)?|discover(?:s|ed|ing)?|scan(?:s|ned|ning)?)"
        load_action = r"load(?:s|ed|ing)?"
        manual_loading = re.compile(
            rf"(?:\b{manual_action}\b[^.;!?]{{0,100}}\b{manual_target}\b|\b{load_action}\b\s+(?:the\s+)?(?:(?:root|nearest|applicable|nested)\s+)?\b{instruction_target}\b|\b{instruction_target}\b[^.;!?]{{0,120}}\b(?:agents?|reviewers?|writers?|coders?|orchestrators?)\b[^.;!?]{{0,60}}\b(?:{manual_action}|{load_action})\b|\b{instruction_target}\b[^.;!?]{{0,50}}\b(?:is|are|was|were|gets?|got)\s*(?:{manual_action}|{load_action})\b)",
            re.IGNORECASE,
        )
        prohibition = re.compile(
            r"\b(?:do not|does not|must not|should not|never|prevent(?:s|ed|ing)?|reject(?:s|ed|ing)?|forbid(?:s|den|ding)?)\b",
            re.IGNORECASE,
        )
        def is_redundant_loading(text: str) -> bool:
            match = manual_loading.search(text)
            if match is None:
                return False

            prefix = text[max(0, match.start() - 120):match.start()]
            suffix = text[match.end():match.end() + 60]
            governed_prohibition = (
                prohibition.search(prefix) is not None
                and re.search(r"\b(?:but|however)\b", prefix, re.IGNORECASE) is None
            )
            explicit_artifact_inspection = (
                re.search(r"\binspect(?:s|ed|ing)?\b", match.group(), re.IGNORECASE)
                is not None
                and re.search(r"\bartifact(?:s)?\b", match.group() + suffix, re.IGNORECASE)
                is not None
            )
            automatic_subject = re.search(
                r"\b(?:harness|runtime)\b[^.;!?]{0,40}$",
                prefix,
                re.IGNORECASE,
            )
            automatic_passive = re.search(
                r"^\s*(?:automatically\s+)?by\s+(?:the\s+)?(?:harness|runtime)\b",
                suffix,
                re.IGNORECASE,
            )
            automatic_load = (
                re.search(r"\bload(?:s|ed|ing)?\b", match.group(), re.IGNORECASE)
                is not None
                and (automatic_subject is not None or automatic_passive is not None)
            )
            return not (governed_prohibition or explicit_artifact_inspection or automatic_load)

        prohibited_examples = (
            "Read the root AGENTS.md before acting.",
            "Before acting, read the nearest AGENTS.md.",
            "Ordinary agents must read AGENTS.md before changing files.",
            "The reviewer re-reads CLAUDE.md for every task.",
            "AGENTS.md is reread before acting.",
            "Inspect the applicable project instructions before coding.",
            "Discover and scan AGENTS.md during startup.",
            "Before acting, read the root and nearest\nAGENTS.md files.",
            "Before creating files, read AGENTS.md.",
            "The coder reads AGENTS.md before writing source files.",
            "The harness supplies tools, but the coder reads AGENTS.md before acting.",
        )
        allowed_examples = (
            "Do not tell ordinary agents to read AGENTS.md.",
            "Create or update AGENTS.md as the task artifact.",
            "Review the existing AGENTS.md artifact.",
            "Investigate whether the harness loads AGENTS.md.",
            "The harness supplies applicable AGENTS.md instructions automatically.",
        )
        for example in prohibited_examples:
            with self.subTest(prohibited_example=example):
                self.assertTrue(is_redundant_loading(example))
        for example in allowed_examples:
            with self.subTest(allowed_example=example):
                self.assertFalse(is_redundant_loading(example))

        text_suffixes = {".md", ".yaml", ".yml", ".toml"}
        paths = [README_PATH]
        paths.extend(
            path
            for path in sorted(SKILLS_ROOT.rglob("*"))
            if path.is_file() and path.suffix in text_suffixes
        )
        paths.extend(sorted(ROLES_ROOT.rglob("*.yaml")))
        paths.extend(sorted((REPOSITORY_ROOT / "design").glob("*.html")))
        paths.extend(sorted((REPOSITORY_ROOT / "design").glob("*.md")))
        paths.extend(
            path
            for path in sorted(GENERATED_ADAPTERS_ROOT.rglob("*"))
            if path.is_file() and path.suffix in {".md", ".toml"}
        )

        for path in paths:
            normalized_text = re.sub(
                r"\s+",
                " ",
                path.read_text(encoding="utf-8"),
            )
            snippets = re.split(
                r"(?<=[.!?])\s+|</(?:li|p|td|th|strong|span|div)>",
                normalized_text,
            )
            violations = [
                snippet.strip()
                for snippet in snippets
                if is_redundant_loading(snippet)
            ]
            with self.subTest(path=path.relative_to(REPOSITORY_ROOT)):
                self.assertEqual([], violations)

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
            "copyright statement supplied by the applicable project instructions",
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
            "applicable project instructions exactly",
            "generated with AI assistance",
            "public or exported construct",
            "respect the intent claimed by its comments",
        ):
            with self.subTest(checklist_phrase=phrase):
                self.assertIn(phrase, checklist_text)

        for role_name in ("dev-coder", "dev-code-reviewer"):
            role_path = (
                REPOSITORY_ROOT
                / "agents"
                / "roles"
                / "dev-activities"
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
                self.assertIn("documentation-page-verify", skill_text)
                self.assertIn(skill_name, development_methodology_text)
                self.assertIn(template_name, development_methodology_text)
                self.assertIn(review_skill_name, development_methodology_text)

    def test_project_configuration_routes_to_template_and_verifier(self) -> None:
        development_methodology_text = (
            SKILLS_ROOT / "development-methodology" / "SKILL.md"
        ).read_text(encoding="utf-8")
        skill_path = SKILLS_ROOT / PROJECT_CONFIGURATION_SKILL / "SKILL.md"
        template_path = (
            SKILLS_ROOT
            / "development-methodology"
            / "assets"
            / "templates"
            / PROJECT_TEMPLATE
        )
        metadata_path = openai_metadata_path(PROJECT_CONFIGURATION_SKILL)

        self.assertTrue(skill_path.is_file())
        self.assertTrue(template_path.is_file())
        self.assertTrue(metadata_path.is_file())

        skill_text = skill_path.read_text(encoding="utf-8")
        template_text = template_path.read_text(encoding="utf-8")
        operating_model_text = (
            REPOSITORY_ROOT / "design" / "agentic-development-operating-model.html"
        ).read_text(encoding="utf-8")
        examples_text = (
            REPOSITORY_ROOT / "design" / "agent-skill-specialization-examples.html"
        ).read_text(encoding="utf-8")

        self.assertIn(PROJECT_TEMPLATE, skill_text)
        self.assertIn(PROJECT_ARTIFACT, skill_text)
        self.assertIn("Replace every TODO instruction", skill_text)
        self.assertIn("documentation-page-verify", skill_text)
        self.assertIn("customer-safe examples", skill_text)
        self.assertIn("schema: project", template_text)
        self.assertIn("proprietary_validation_notes:", template_text)
        self.assertIn("nested_agents_files:", template_text)
        self.assertNotIn("nested_project_files:", template_text)
        self.assertIn("Create exactly one PROJECT.yaml", skill_text)
        self.assertIn("Do not create nested PROJECT.yaml files", skill_text)
        self.assertIn(
            "PROJECT.yaml is the project-root setup and validation record",
            operating_model_text,
        )
        self.assertIn("linked template", examples_text)
        self.assertNotIn("service/PROJECT.yaml", examples_text)
        self.assertNotIn("nested PROJECT.yaml recommendations", operating_model_text)
        self.assertNotIn("&lt;subtree&gt;/PROJECT.yaml", operating_model_text)
        self.assertIn("claude_bridge_files:", template_text)
        self.assertNotIn("agent_coordination:", template_text)
        self.assertNotIn("coordination_overrides:", template_text)
        self.assertIn(
            "Generic repository-mutation behavior belongs to role definitions",
            skill_text,
        )
        self.assertIn(
            "Do not reproduce that procedure in PROJECT.yaml or AGENTS.md",
            skill_text,
        )
        self.assertIn("Record a coordination_overrides mapping only when", skill_text)
        self.assertIn(
            "Treat a missing role definition, skill, or command as BLOCKED",
            skill_text,
        )
        self.assertIn("agent-claim", skill_text)
        self.assertIn("thin CLAUDE.md", skill_text)
        self.assertIn(PROJECT_CONFIGURATION_SKILL, development_methodology_text)
        self.assertIn(PROJECT_TEMPLATE, development_methodology_text)
        self.assertIn("documentation-page-verify", development_methodology_text)

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
                self.assertIn("documentation-page-verify", skill_text)
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
            SKILLS_ROOT / "documentation-page-verify" / "SKILL.md"
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

    def test_methodology_naming_skill_separates_category_from_pattern(self) -> None:
        skill_text = (
            SKILLS_ROOT / "name-methodology-artifacts" / "SKILL.md"
        ).read_text(encoding="utf-8")

        required_guidance = (
            "Determine category membership from the skill's subject area and responsibility.",
            "Each skill category mostly follows one naming pattern, but this is not an absolute rule.",
            "Use best judgment to choose the most appropriate category",
            "Treat the naming pattern as a word-order convention, not as the definition of category membership.",
            "For an object-centered naming pattern",
            "For an action-centered naming pattern",
        )
        for guidance in required_guidance:
            with self.subTest(guidance=guidance):
                self.assertIn(guidance, skill_text)

    def test_project_file_organisation_defines_taxonomy_contract(self) -> None:
        skill_text = (
            SKILLS_ROOT / "organise-project-files" / "SKILL.md"
        ).read_text(encoding="utf-8")

        required_guidance = (
            "The project taxonomy is docs/project-taxonomy.md relative to the repository root.",
            "Read the complete taxonomy fresh before every placement decision.",
            "Conventions: defines ID prefixes and formats, filename casing, and test-mirroring rules.",
            "Top-Level Folder Principles:",
            "Each entry defines Purpose, Signals, and Filename pattern.",
            "Source categories may add Tests location; test categories may add Mirrors; entries may add Example.",
            "Change log: records taxonomy extensions newest first",
            "report that no taxonomy exists",
            "do not invent it as a side effect of an ordinary placement decision.",
        )
        for guidance in required_guidance:
            with self.subTest(guidance=guidance):
                self.assertIn(guidance, skill_text)

    def test_skill_names_follow_category_naming_rules(self) -> None:
        build_skill_docs = load_build_skill_docs_module()
        payload = build_skill_docs.build_payload()

        for skill_name, skill in payload["skills"].items():
            with self.subTest(skill_name=skill_name):
                self.assertNotIn(
                    skill_name.split("-")[-1],
                    build_skill_docs.SKILL_ACTOR_SUFFIXES,
                )
                if skill["category"] == "artifact-creation":
                    self.assertTrue(skill_name.startswith("create-"))
                if skill["category"] == "artifact-review":
                    self.assertTrue(skill_name.startswith("review-"))
                if skill["category"] == "wiki-and-knowledge":
                    self.assertTrue(
                        skill_name.startswith("project-wiki")
                        or skill_name == "code-project-wiki"
                    )

    def test_generated_skill_definition_data_is_current(self) -> None:
        build_skill_docs = load_build_skill_docs_module()
        rendered = build_skill_docs.render_javascript(build_skill_docs.build_payload())
        self.assertEqual(
            rendered,
            SKILL_DEFINITIONS_PATH.read_text(encoding="utf-8"),
        )

    def test_source_roles_generate_current_documentation_and_adapters(self) -> None:
        build_skill_docs = load_build_skill_docs_module()
        skill_payload = build_skill_docs.build_payload()
        roles = build_skill_docs.load_role_definitions(set(skill_payload["skills"]))
        expected_outputs = build_skill_docs.expected_role_outputs(roles)

        maintenance_skill = (
            SKILLS_ROOT / "maintain-methodology-documentation" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "generated Codex, Claude Code, Gemini CLI, and Junie CLI agent definitions",
            maintenance_skill,
        )
        self.assertNotIn("generated Codex and Claude agent definitions", maintenance_skill)

        self.assertTrue(ROLE_SCHEMA_PATH.is_file())
        role_schema = load_yaml_object(ROLE_SCHEMA_PATH)
        self.assertEqual(4, role_schema["version"])
        self.assertEqual(
            "instruction-content",
            role_schema["properties"]["instructions"],
        )
        self.assertEqual(
            "conditional-skill-entry-list",
            role_schema["properties"]["skills"],
        )
        self.assertEqual(
            "mutation-policy",
            role_schema["properties"]["repositoryMutation"],
        )
        self.assertEqual(
            "string-list",
            role_schema["properties"]["agentDependencies"],
        )
        self.assertEqual(
            expected_outputs[ROLE_DEFINITIONS_PATH],
            ROLE_DEFINITIONS_PATH.read_text(encoding="utf-8"),
        )
        for output_path, expected_content in expected_outputs.items():
            with self.subTest(output_path=output_path):
                self.assertTrue(output_path.is_file())
                self.assertEqual(expected_content, output_path.read_text(encoding="utf-8"))

        source_role_names = {role.name for role in roles}
        self.assertIn("project-bootstrapper", source_role_names)
        self.assertNotIn("methodology-shared-install-verifier", source_role_names)
        generation_manifest = json.loads(
            AGENT_GENERATION_MANIFEST_PATH.read_text(encoding="utf-8")
        )
        self.assertEqual(len(roles), generation_manifest["canonicalRoleCount"])
        for adapter_name, extension in (
            ("codex", ".toml"),
            ("claude", ".md"),
            ("gemini", ".md"),
            ("junie", ".md"),
        ):
            with self.subTest(adapter=adapter_name):
                adapter_manifest = generation_manifest["adapters"][adapter_name]
                manifest_role_names = {
                    agent["name"] for agent in adapter_manifest["agents"]
                }
                generated_role_names = {
                    path.stem
                    for path in (
                        GENERATED_ADAPTERS_ROOT / adapter_name / "agents"
                    ).glob(f"*{extension}")
                }
                self.assertEqual(len(roles), adapter_manifest["agentCount"])
                self.assertEqual(source_role_names, manifest_role_names)
                self.assertEqual(source_role_names, generated_role_names)
                for agent in adapter_manifest["agents"]:
                    generated_agent_path = REPOSITORY_ROOT / agent["output"]
                    self.assertEqual(
                        agent["sha256"],
                        hashlib.sha256(generated_agent_path.read_bytes()).hexdigest(),
                    )

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
                    role_source.get("agentDependencies", []),
                    list(role.agent_dependencies),
                )
                self.assertEqual(
                    role_source.get("agentDependencies", []),
                    role_payload["roles"][role.name]["agentDependencies"],
                )
                self.assertEqual(
                    role.instruction_sections,
                    role_payload["roles"][role.name]["instructionSections"],
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
                if role.name == "dev-documentation-writer":
                    self.assertEqual(
                        "when describing user-visible functionality, actor workflows, acceptance criteria, permissions, states, or error behavior",
                        role.skill_conditions["create-functional-spec"],
                    )
                    self.assertEqual(
                        "when creating or updating a README or custom non-wiki entry document whose established format must be preserved",
                        role.skill_conditions["documentation-page-verify"],
                    )
                    for example in role_payload["roles"][role.name]["examples"]:
                        self.assertTrue(
                            example["runtimeInvocations"]["codex"].startswith("$dev-documentation-writer ")
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

                gemini_agent_path = (
                    GENERATED_ADAPTERS_ROOT / "gemini" / "agents" / f"{role.filename}.md"
                )
                self.assertTrue(gemini_agent_path.is_file())
                gemini_agent_text = gemini_agent_path.read_text(encoding="utf-8")
                self.assertTrue(gemini_agent_text.startswith("---\n"))
                gemini_frontmatter = yaml.safe_load(gemini_agent_text.split("---", 2)[1])
                self.assertEqual(role.name, gemini_frontmatter["name"])
                self.assertEqual(role.description, gemini_frontmatter["description"])
                self.assertEqual("local", gemini_frontmatter["kind"])
                self.assertNotIn("skills", gemini_frontmatter)
                self.assertIn("Before acting, load these fixed-role skills completely", gemini_agent_text)
                for skill, condition in role.skill_conditions.items():
                    self.assertIn(f"Use the {skill} skill {condition}.", gemini_agent_text)

                junie_agent_path = (
                    GENERATED_ADAPTERS_ROOT / "junie" / "agents" / f"{role.filename}.md"
                )
                self.assertTrue(junie_agent_path.is_file())
                junie_agent_text = junie_agent_path.read_text(encoding="utf-8")
                self.assertTrue(junie_agent_text.startswith("---\n"))
                junie_frontmatter = yaml.safe_load(junie_agent_text.split("---", 2)[1])
                self.assertEqual(role.name, junie_frontmatter["name"])
                self.assertEqual(role.description, junie_frontmatter["description"])
                self.assertEqual(
                    list(build_skill_docs.fixed_role_skills(role)),
                    junie_frontmatter["skills"],
                )
                self.assertIn("reasoningLevel", junie_frontmatter)
                self.assertIn("These fixed-role skills are preloaded and govern the work", junie_agent_text)
                for skill, condition in role.skill_conditions.items():
                    self.assertNotIn(skill, junie_frontmatter["skills"])
                    self.assertIn(f"Use the {skill} skill {condition}.", junie_agent_text)

        non_setup_roles = [
            role for role in roles
            if role.name != "project-configurator"
        ]
        self.assertTrue(all("detect-technology-skills" not in role.skills for role in non_setup_roles))
        setup_role = next(role for role in roles if role.name == "project-configurator")
        self.assertIn("detect-technology-skills", setup_role.skills)

    def test_role_instructions_support_concise_and_structured_forms(self) -> None:
        build_skill_docs = load_build_skill_docs_module()

        rendered, sections = build_skill_docs.validate_role_instructions(
            "Perform one bounded responsibility.",
            ROLE_SCHEMA_PATH,
        )
        self.assertEqual("Perform one bounded responsibility.", rendered)
        self.assertEqual({}, sections)

        rendered, sections = build_skill_docs.validate_role_instructions(
            {
                "objective": "Complete the bounded responsibility.",
                "workflow": ["Inspect evidence.", "Produce the result."],
                "failureHandling": ["Return BLOCKED when authority is missing."],
                "completion": ["Return READY with verification evidence."],
            },
            ROLE_SCHEMA_PATH,
        )
        self.assertIn("## Objective", rendered)
        self.assertIn("1. Inspect evidence.", rendered)
        self.assertIn("## Failure Handling", rendered)
        self.assertEqual(
            ["Inspect evidence.", "Produce the result."],
            sections["workflow"],
        )

        with self.assertRaisesRegex(ValueError, "missing sections"):
            build_skill_docs.validate_role_instructions(
                {"objective": "Incomplete role."},
                ROLE_SCHEMA_PATH,
            )

    def test_modifying_roles_use_claims_and_coordination_roles_require_clean_commits(self) -> None:
        build_skill_docs = load_build_skill_docs_module()
        skill_payload = build_skill_docs.build_payload()
        roles = build_skill_docs.load_role_definitions(set(skill_payload["skills"]))
        roles_by_name = {role.name: role for role in roles}
        for role in roles:
            with self.subTest(role=role.name, mutation_policy=role.repository_mutation):
                if role.repository_mutation == "required":
                    self.assertIn("agent-claim", build_skill_docs.fixed_role_skills(role))
                elif role.repository_mutation == "conditional":
                    self.assertIn("agent-claim", role.skill_conditions)
                else:
                    self.assertNotIn(
                        "agent-claim",
                        build_skill_docs.fixed_role_skills(role),
                    )
                    self.assertNotIn("agent-claim", role.skill_conditions)

        orchestrator = roles_by_name["dev-orchestrator"]
        merge_coordinator = roles_by_name["dev-merge-coordinator"]
        self.assertIn("committed handoffs", orchestrator.instructions)
        self.assertIn("verified, committed, clean, and released", orchestrator.instructions)
        self.assertIn("committed clean contributions", merge_coordinator.instructions)
        self.assertIn("release only from a clean worktree", merge_coordinator.instructions)
        self.assertTrue((SKILLS_ROOT / "agent-claim" / "scripts" / "claim.py").is_file())
        self.assertIn("Agent Claims And Worktrees", README_PATH.read_text(encoding="utf-8"))
        self.assertNotIn("Agent Claims And Worktrees", AGENTS_PATH.read_text(encoding="utf-8"))

    def test_direct_agent_dependencies_have_complete_routing_contracts(self) -> None:
        """Every maintained direct dependency should have an explicit orchestration contract."""
        build_skill_docs = load_build_skill_docs_module()
        skill_payload = build_skill_docs.build_payload()
        roles = build_skill_docs.load_role_definitions(set(skill_payload["skills"]))
        roles_by_name = {role.name: role for role in roles}
        expected_dependencies = {
            "dev-orchestrator": (
                "dev-coder",
                "dev-code-reviewer",
                "dev-verifier",
                "dev-merge-coordinator",
            ),
            "methodology-maintainer": (
                "methodology-artifact-reviewer",
                "dev-verifier",
            ),
            "project-bootstrapper": (
                "project-configurator",
                "dev-documentation-writer",
                "wiki-architect",
                "wiki-writer",
                "dev-artifact-reviewer",
                "wiki-artifact-reviewer",
                "wiki-topic-verifier",
                "dev-merge-coordinator",
                "dev-verifier",
            ),
            "wiki-ingester": ("wiki-topic-verifier",),
            "wiki-writer": ("wiki-topic-verifier",),
        }
        actual_dependencies = {
            role.name: role.agent_dependencies
            for role in roles
            if role.agent_dependencies
        }

        self.assertEqual(expected_dependencies, actual_dependencies)
        for role_name, dependencies in expected_dependencies.items():
            role = roles_by_name[role_name]
            with self.subTest(role=role_name):
                self.assertTrue(
                    {"delegation", "review", "failureHandling", "completion"}
                    .issubset(role.instruction_sections)
                )
                self.assertIn("status", role.output_contract)
                self.assertRegex(role.instructions, r"fresh(?:-| )context")
                routing_text = " ".join(
                    item
                    for section_name in ("delegation", "review")
                    for item in role.instruction_sections[section_name]
                )
                failure_text = " ".join(role.instruction_sections["failureHandling"])
                completion_text = " ".join(role.instruction_sections["completion"])
                example_responses = [
                    example["plausibleResponse"]
                    for example in role.examples
                ]
                for dependency in dependencies:
                    self.assertIn(dependency, routing_text)
                self.assertRegex(
                    failure_text,
                    r"(?i)(?:after|at most).*two.*correction attempts",
                )
                self.assertRegex(
                    failure_text,
                    r"(?i)(?:unavailable|cannot provide a required agent)",
                )
                self.assertRegex(
                    f"{routing_text} {failure_text}",
                    r"(?i)(?:route|return|this role owns|apply only)",
                )
                self.assertTrue(
                    any("STATUS: READY" in response for response in example_responses)
                )
                self.assertTrue(
                    any("STATUS: BLOCKED" in response for response in example_responses)
                )
                for closeout_term in ("commit", "clean", "release"):
                    self.assertIn(closeout_term, completion_text.lower())

        orchestrator = roles_by_name["dev-orchestrator"]
        self.assertNotIn("agent-work-merge", orchestrator.skills)
        self.assertNotIn("review-structured-artifact", orchestrator.skills)

        topic_write_skill = (
            SKILLS_ROOT / "project-wiki-topic-write" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("at most two corrected resubmissions", topic_write_skill)
        self.assertIn("governing cap is exhausted", topic_write_skill)
        self.assertNotIn("Repeat until the verifier returns GOOD", topic_write_skill)

        direct_lane_example = next(
            example
            for example in orchestrator.examples
            if "one reviewed and verified source lane" in example["purpose"]
        )
        self.assertIn("STATUS: READY", direct_lane_example["plausibleResponse"])
        self.assertIn(
            "dev-merge-coordinator was not invoked",
            direct_lane_example["plausibleResponse"],
        )
        self.assertIn(
            "any required multi-contribution integration",
            " ".join(orchestrator.instruction_sections["completion"]),
        )

        wiki_ingester = roles_by_name["wiki-ingester"]
        for example in wiki_ingester.examples[:2]:
            with self.subTest(wiki_ingester_example=example["purpose"]):
                response = example["plausibleResponse"]
                self.assertIn("GOOD pre-move verdict", response)
                self.assertIn("GOOD post-move verdict", response)
                self.assertIn("released the ingest claim", response)

    def test_project_bootstrapper_owns_complete_setup_and_review_loop(self) -> None:
        build_skill_docs = load_build_skill_docs_module()
        skill_payload = build_skill_docs.build_payload()
        roles = build_skill_docs.load_role_definitions(set(skill_payload["skills"]))
        role = next(role for role in roles if role.name == "project-bootstrapper")

        self.assertNotIn("documentation-reverse-engineer", build_skill_docs.fixed_role_skills(role))
        self.assertNotIn("documentation-reverse-engineer", role.skill_conditions)
        self.assertLess(
            role.instructions.index("project-configurator"),
            role.instructions.index("dev-documentation-writer"),
        )
        self.assertEqual(
            {
                "objective",
                "decisions",
                "workflow",
                "delegation",
                "review",
                "failureHandling",
                "completion",
            },
            set(role.instruction_sections),
        )
        self.assertIn("## Objective", role.instructions)
        self.assertIn("## Failure Handling", role.instructions)
        self.assertNotIn("## Boundaries", role.instructions)
        self.assertIn("If PROJECT.yaml does not exist", role.instructions)
        self.assertIn(
            "Do not run technology detection or project-configurator again",
            role.instructions,
        )
        self.assertIn(
            "If PROJECT.yaml fails validation and the user has asked for reconfiguration",
            role.instructions,
        )
        self.assertIn(
            "ask project-configurator to repair it and run validation again",
            role.instructions,
        )
        self.assertIn(
            "If PROJECT.yaml fails validation and the user has not asked for reconfiguration",
            role.instructions,
        )
        self.assertIn("Run the installer only when the user has asked", role.instructions)
        for delegated_role in (
            "project-configurator",
            "dev-documentation-writer",
            "dev-artifact-reviewer",
            "wiki-architect",
            "wiki-writer",
            "wiki-artifact-reviewer",
            "wiki-topic-verifier",
            "dev-merge-coordinator",
            "dev-verifier",
        ):
            with self.subTest(delegated_role=delegated_role):
                self.assertIn(delegated_role, role.instructions)
        self.assertEqual(
            (
                "project-configurator",
                "dev-documentation-writer",
                "wiki-architect",
                "wiki-writer",
                "dev-artifact-reviewer",
                "wiki-artifact-reviewer",
                "wiki-topic-verifier",
                "dev-merge-coordinator",
                "dev-verifier",
            ),
            role.agent_dependencies,
        )
        self.assertIn("After two failed correction attempts", role.instructions)
        self.assertIn("Report READY only after", role.instructions)
        self.assertIn("Report BLOCKED only after two failed correction attempts", role.instructions)
        self.assertIn("existing code or product problem", role.instructions)
        self.assertIn("PROJECT.yaml, AGENTS.md, or Claude bridge problems", role.instructions)
        self.assertIn("non-wiki document problems", role.instructions)
        self.assertIn("wiki setup problems", role.instructions)
        self.assertIn("ordinary wiki page problems", role.instructions)
        self.assertEqual(
            (
                "status",
                "project setup files",
                "documentation",
                "checks",
                "remaining questions",
            ),
            role.output_contract,
        )
        self.assertEqual(4, len(role.examples))
        self.assertTrue(role.examples[0]["plausibleResponse"].startswith("STATUS: READY"))
        self.assertTrue(role.examples[1]["plausibleResponse"].startswith("STATUS: READY"))
        self.assertIn("STATUS: BLOCKED", role.examples[2]["plausibleResponse"])
        self.assertTrue(role.examples[3]["plausibleResponse"].startswith("STATUS: READY"))
        self.assertIn("valid existing routing", role.examples[0]["purpose"])
        self.assertIn("no project routing", role.examples[1]["purpose"])
        self.assertIn("invalid", role.examples[2]["purpose"])
        self.assertIn("authorized", role.examples[3]["purpose"])
        for example in role.examples:
            self.assertTrue(example["runtimeInvocations"]["codex"].startswith("$project-bootstrapper "))
            self.assertTrue(
                example["runtimeInvocations"]["claude-code"].startswith(
                    "@agent-project-bootstrapper "
                )
            )

    def test_dev_artifact_reviewer_combines_generic_and_specific_review_skills(self) -> None:
        build_skill_docs = load_build_skill_docs_module()
        skill_payload = build_skill_docs.build_payload()
        roles = build_skill_docs.load_role_definitions(set(skill_payload["skills"]))
        role = next(role for role in roles if role.name == "dev-artifact-reviewer")

        self.assertIn(
            "review-structured-artifact",
            build_skill_docs.fixed_role_skills(role),
        )
        self.assertEqual(
            {
                "agent-claim",
                "organise-project-files",
                "review-architecture",
                "review-functional-spec",
                "review-high-level-design",
                "review-module-design",
                "review-unit-test-plan",
            },
            set(role.skill_conditions),
        )

    def test_role_categories_and_names_follow_prefix_actor_rules(self) -> None:
        build_skill_docs = load_build_skill_docs_module()
        skill_payload = build_skill_docs.build_payload()
        roles = build_skill_docs.load_role_definitions(set(skill_payload["skills"]))
        category_words = [
            label.split()[0].lower()
            for label in build_skill_docs.ROLE_GROUP_LABELS.values()
        ]

        self.assertEqual(len(category_words), len(set(category_words)))
        for role in roles:
            with self.subTest(role=role.name):
                segments = role.name.split("-")
                self.assertEqual(
                    build_skill_docs.ROLE_GROUP_PREFIXES[role.group],
                    segments[0],
                )
                self.assertNotIn("agent", segments)
                self.assertIn(segments[-1], build_skill_docs.ROLE_ACTOR_SUFFIXES)

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
            REPOSITORY_ROOT / "agents" / "roles" / "dev-activities" / "dev-coder.role.yaml"
        )
        source_role["tools"] = ["Read", "Grep"]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "dev-activities" / "dev-coder.role.yaml"
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
            / "dev-activities"
            / "dev-documentation-writer.role.yaml"
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
                path = Path(directory) / "dev-activities" / "dev-documentation-writer.role.yaml"
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
            if role.name == "dev-coder"
        )
        availability = [
            {"name": "python", "enabled": False},
            {"path": "/opt/skills/fastapi", "enabled": True},
        ]
        role = replace(role, optional_fields={**role.optional_fields, "skillAvailability": availability})
        profiles = build_skill_docs.load_adapter_model_profiles("codex", model_profiles)
        rendered = build_skill_docs.render_codex_agent(role, profiles)
        parsed = tomllib.loads(rendered)
        self.assertEqual(
            [
                {"name": "python", "enabled": False},
                {"path": "/opt/skills/fastapi", "enabled": True},
            ],
            parsed["skills"]["config"],
        )

    def test_gemini_and_junie_render_native_frontmatter_fields(self) -> None:
        build_skill_docs = load_build_skill_docs_module()
        skill_payload = build_skill_docs.build_payload()
        model_profiles = set(build_skill_docs.load_model_profiles())
        role = next(
            role for role in build_skill_docs.load_role_definitions(set(skill_payload["skills"]))
            if role.name == "dev-coder"
        )
        role = replace(
            role,
            optional_fields={
                **role.optional_fields,
                "tools": ["Read", "Grep"],
                "disallowedTools": ["WebSearch"],
                "mcpServers": ["github"],
                "maxTurns": 12,
                "timeout": 8,
            },
        )

        gemini_profiles = build_skill_docs.load_adapter_model_profiles("gemini", model_profiles)
        gemini_text = build_skill_docs.render_gemini_agent(role, gemini_profiles)
        gemini_frontmatter = yaml.safe_load(gemini_text.split("---", 2)[1])
        self.assertEqual(["Read", "Grep"], gemini_frontmatter["tools"])
        self.assertEqual(12, gemini_frontmatter["max_turns"])
        self.assertEqual(8, gemini_frontmatter["timeout_mins"])
        self.assertNotIn("skills", gemini_frontmatter)
        self.assertNotIn("disallowedTools", gemini_frontmatter)
        self.assertNotIn("mcpServers", gemini_frontmatter)

        junie_profiles = build_skill_docs.load_adapter_model_profiles("junie", model_profiles)
        junie_text = build_skill_docs.render_junie_agent(role, junie_profiles)
        junie_frontmatter = yaml.safe_load(junie_text.split("---", 2)[1])
        self.assertEqual(["Read", "Grep"], junie_frontmatter["tools"])
        self.assertEqual(["WebSearch"], junie_frontmatter["disallowedTools"])
        self.assertEqual(["github"], junie_frontmatter["mcpServers"])
        self.assertEqual(12, junie_frontmatter["maxTurns"])
        self.assertEqual(
            junie_profiles[role.model_profile].effort,
            junie_frontmatter["reasoningLevel"],
        )
        self.assertNotIn("timeout", junie_frontmatter)
        self.assertNotIn("timeout_mins", junie_frontmatter)

    def test_model_profiles_are_semantic_and_adapter_complete(self) -> None:
        source_profiles = load_yaml_object(MODEL_PROFILES_PATH)["profiles"]
        self.assertEqual(
            {"simple", "default", "advanced", "advanced-long"},
            set(source_profiles),
        )

        adapter_profiles = {
            adapter: load_yaml_object(path)["profiles"]
            for adapter, path in ADAPTER_MODEL_PROFILE_PATHS.items()
        }
        for adapter, profiles in adapter_profiles.items():
            with self.subTest(adapter=adapter):
                self.assertEqual(set(source_profiles), set(profiles))
                for profile in profiles.values():
                    self.assertIsInstance(profile.get("model"), str)
                    self.assertTrue(profile["model"].strip())

        for profile in adapter_profiles["codex"].values():
            self.assertTrue(profile["model"].startswith("gpt-5.6-"))

        for role_path in sorted((REPOSITORY_ROOT / "agents" / "roles").glob("*/*.role.yaml")):
            with self.subTest(role_path=role_path):
                role = load_yaml_object(role_path)
                self.assertIn(role["modelProfile"], source_profiles)
                self.assertNotIn("model", role)
                self.assertNotIn("effort", role)
                for profile in role.get("modelStages", {}).values():
                    self.assertIn(profile, source_profiles)

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

    def test_html_documentation_assigns_single_topic_owners(self) -> None:
        design_root = REPOSITORY_ROOT / "design"
        page_text = {
            filename: (design_root / filename).read_text(encoding="utf-8")
            for filename in DOCUMENT_INFORMATION_OWNERS
        }

        strategy_text = page_text["agent-skill-specialization-strategy.html"]
        for phrase in STRATEGY_REQUIRED_PHRASES:
            with self.subTest(strategy_phrase=phrase):
                self.assertIn(phrase, strategy_text)

        for owner, headings in DOCUMENT_INFORMATION_OWNERS.items():
            for heading in headings:
                with self.subTest(owner=owner, heading=heading):
                    heading_pattern = rf"<h[123][^>]*>{re.escape(heading)}</h[123]>"
                    matches = [
                        filename
                        for filename, text in page_text.items()
                        if re.search(heading_pattern, text)
                    ]
                    self.assertEqual([owner], matches)

        for former_owner, forbidden_headings in DOCUMENT_FORBIDDEN_HEADINGS.items():
            for heading in forbidden_headings:
                with self.subTest(
                    former_owner=former_owner,
                    forbidden_heading=heading,
                ):
                    heading_pattern = rf"<h[123][^>]*>{re.escape(heading)}</h[123]>"
                    matches = [
                        filename
                        for filename, text in page_text.items()
                        if re.search(heading_pattern, text)
                    ]
                    self.assertEqual(
                        [],
                        matches,
                        f"Retired heading {heading!r} must not move to another page",
                    )

        for filename, required_links in DOCUMENT_REQUIRED_LINKS.items():
            for link in required_links:
                with self.subTest(filename=filename, required_link=link):
                    self.assertIn(f'href="{link}', page_text[filename])

        for filename, text in page_text.items():
            if "skill-browser.js" not in text:
                continue
            with self.subTest(skill_browser_consumer=filename):
                self.assertIn(
                    "data-skill-definition",
                    text,
                    "Pages must not load the skill browser without a definition trigger",
                )

        index_text = (REPOSITORY_ROOT / "index.html").read_text(encoding="utf-8")
        for filename in DOCUMENT_INFORMATION_OWNERS:
            with self.subTest(index_link=filename):
                self.assertIn(f'href="design/{filename}"', index_text)
        for owner in (
            "operating",
            "execution",
            "selection",
            "catalog",
            "examples",
            "agent-definitions",
        ):
            with self.subTest(index_owner=owner):
                self.assertEqual(
                    1,
                    index_text.count(f'data-information-owner="{owner}"'),
                )

        self.assertIn(
            "deliberately present the same role-to-skill relationships in two generated views",
            page_text["agent-role-skill-map.html"],
        )

    def test_html_documentation_has_no_repeated_long_prose_blocks(self) -> None:
        occurrences: dict[str, set[str]] = {}
        html_paths = {
            "index.html": REPOSITORY_ROOT / "index.html",
            **{
                filename: REPOSITORY_ROOT / "design" / filename
                for filename in DOCUMENT_INFORMATION_OWNERS
            },
        }
        for filename, path in html_paths.items():
            for block in visible_prose_blocks(path):
                if len(block.split()) < 12:
                    continue
                normalized = block.casefold()
                occurrences.setdefault(normalized, set()).add(filename)

        duplicates = {
            block: sorted(filenames)
            for block, filenames in occurrences.items()
            if len(filenames) > 1
        }
        self.assertEqual({}, duplicates)

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
            "View source role YAML",
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
            "instructionSections",
            "renderRoleInstructions",
            "agent-modal__instruction-sections",
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
        self.assertIn(
            'elements.close.textContent = returnTarget ? "Back to map" : "Close"',
            agent_browser_text,
        )
        self.assertIn("lastFocusedElement.scrollIntoView", agent_browser_text)

        skill_browser_text = (REPOSITORY_ROOT / "design" / "skill-browser.js").read_text(encoding="utf-8")
        self.assertIn("enhance-skill-definitions", skill_browser_text)
        self.assertIn("[data-skill-definition]", skill_browser_text)
        self.assertIn(
            'elements.close.textContent = returnTarget ? "Back to map" : "Close"',
            skill_browser_text,
        )
        self.assertIn("lastFocusedElement.scrollIntoView", skill_browser_text)

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

    def test_generic_agent_definitions_document_source_and_adapters(self) -> None:
        index_text = (REPOSITORY_ROOT / "index.html").read_text(encoding="utf-8")
        definition_text = (
            REPOSITORY_ROOT / "design" / "generic-agent-definitions-source.html"
        ).read_text(encoding="utf-8")
        role_schema = yaml.safe_load(
            (REPOSITORY_ROOT / "agents" / "role-schema.yaml").read_text(
                encoding="utf-8"
            )
        )

        self.assertIn("design/generic-agent-definitions-source.html", index_text)

        for phrase in GENERIC_AGENT_DEFINITIONS_REQUIRED_PHRASES:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, definition_text)

        self.assertNotIn("PROJECT.md", definition_text)
        self.assertNotIn("agents/*.toml", definition_text)
        self.assertNotIn("agents/*.md", definition_text)

        property_section = definition_text.split(
            '<h2 id="information-model-title">', maxsplit=1
        )[1].split('<h2 id="ignored-properties-title">', maxsplit=1)[0]
        for property_name in role_schema["properties"]:
            with self.subTest(source_property=property_name):
                self.assertIn(f"<code>{property_name}</code>", property_section)

        for behavior_name in role_schema["fixedBehavior"]:
            with self.subTest(fixed_behavior=behavior_name):
                self.assertIn(
                    f"<code>fixedBehavior.{behavior_name}</code>",
                    definition_text,
                )

    def test_reverse_engineering_uses_structural_code_discovery(self) -> None:
        skill_text = (
            SKILLS_ROOT / "documentation-reverse-engineer" / "SKILL.md"
        ).read_text(encoding="utf-8")

        for phrase in REVERSE_ENGINEERING_DISCOVERY_PHRASES:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, skill_text)


if __name__ == "__main__":
    unittest.main()
