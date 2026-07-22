# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Modified with AI assistance.
# Summary: Verifies the distributable methodology bundle, generated artifacts, roles, and documentation contracts.

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import tomllib
import unittest
from dataclasses import replace
from html.parser import HTMLParser
from pathlib import Path
from types import ModuleType
from urllib.parse import urlsplit

import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
README_PATH = REPOSITORY_ROOT / "README.md"
AGENTS_PATH = REPOSITORY_ROOT / "AGENTS.md"
GITIGNORE_PATH = REPOSITORY_ROOT / ".gitignore"
SKILLS_ROOT = REPOSITORY_ROOT / "skills"
ROLES_ROOT = REPOSITORY_ROOT / "agents" / "roles"
SKILL_CATEGORIES_PATH = REPOSITORY_ROOT / "design" / "skill-categories.yaml"
SKILL_DEFINITIONS_PATH = REPOSITORY_ROOT / "design" / "generated" / "skill-definitions.js"
TEMPLATE_DEFINITIONS_PATH = REPOSITORY_ROOT / "design" / "generated" / "template-definitions.js"
ROLE_SCHEMA_PATH = REPOSITORY_ROOT / "agents" / "role-schema.yaml"
MODEL_PROFILES_PATH = REPOSITORY_ROOT / "agents" / "model-profiles.yaml"
ADAPTER_MODEL_PROFILE_PATHS = {
    "codex": REPOSITORY_ROOT / "adapters" / "codex" / "model-profiles.yaml",
    "claude": REPOSITORY_ROOT / "adapters" / "claude" / "model-profiles.yaml",
    "gemini": REPOSITORY_ROOT / "adapters" / "gemini" / "model-profiles.yaml",
    "junie": REPOSITORY_ROOT / "adapters" / "junie" / "model-profiles.yaml",
}
CODEX_HARNESS_SKILL_NAME = "codex-harness-directives"
CODEX_HARNESS_SKILL_ROOT = (
    REPOSITORY_ROOT / "adapters" / "codex" / "skills" / CODEX_HARNESS_SKILL_NAME
)
ROLE_DEFINITIONS_PATH = REPOSITORY_ROOT / "design" / "generated" / "role-definitions.js"
SUPPORT_CHECKLIST_PATH = REPOSITORY_ROOT / "design" / "agent-skill-test-coverage-checklist.md"
AGENT_TEST_SUITES_ROOT = REPOSITORY_ROOT / "evals" / "agent-tests"
AGENT_BROWSER_PATH = REPOSITORY_ROOT / "design" / "agent-browser.js"
TEMPLATE_BROWSER_PATH = REPOSITORY_ROOT / "design" / "template-browser.js"
DOCUMENTATION_SETTINGS_PATH = REPOSITORY_ROOT / "design" / "documentation-settings.js"
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
    "execute-workitem",
    "complete-work-item-direct-main",
    "create-file-work-item",
    "manage-file-work-items",
    "file-based-backlog",
    "create-github-work-item",
    "manage-github-work-items",
    "github-issues-backlog",
    "create-gitlab-work-item",
    "manage-gitlab-work-items",
    "create-azure-devops-work-item",
    "manage-azure-devops-work-items",
    "create-jira-work-item",
    "manage-jira-work-items",
    "complete-work-item-feature-branch",
    "create-pull-request",
    "create-unit-test-plan",
    "review-unit-test-plan",
    "typescript",
    "python",
    "fastapi",
    "java",
    "java-comment",
    "java-design",
    "object-creation-patterns",
    "singleton-pattern",
    "interface-patterns",
    "composition-patterns",
    "state-strategy-patterns",
    "request-patterns",
    "collaboration-patterns",
    "traversal-patterns",
    "interpreter-pattern",
    "java-design-pattern-examples",
    "typescript-design-pattern-examples",
    "python-design-pattern-examples",
    "junit",
    "mockito",
    "spring-boot",
    "spring-boot-design",
    "spring-data-jpa",
    "spring-boot-testing",
    "quarkus",
    "quarkus-design",
    "quarkus-persistence",
    "hibernate-orm-panache",
    "quarkus-testing",
    "liquibase",
    "jhipster-project",
    "jhipster-domain-modeling",
    "jhipster-persistence",
    "jhipster-testing",
    "jhipster-security",
    "sql",
)


def resolve_primary_repository_root() -> Path:
    common_dir_text = subprocess.run(
        ["git", "rev-parse", "--git-common-dir"],
        cwd=REPOSITORY_ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    common_dir = Path(common_dir_text)
    if not common_dir.is_absolute():
        common_dir = (REPOSITORY_ROOT / common_dir).resolve()
    primary_root = common_dir.parent
    backlog_root = primary_root / "backlog"
    if not backlog_root.is_dir():
        raise AssertionError(
            f"Canonical primary backlog is inaccessible: {backlog_root}"
        )
    return primary_root


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
DOCUMENTATION_TEMPLATE_FILENAMES = (PROJECT_TEMPLATE,) + tuple(
    template_name for _, template_name, _ in ARTIFACT_CREATION_SKILLS
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
    "java-design",
    "object-creation-patterns",
    "singleton-pattern",
    "interface-patterns",
    "composition-patterns",
    "state-strategy-patterns",
    "request-patterns",
    "collaboration-patterns",
    "traversal-patterns",
    "interpreter-pattern",
    "java-design-pattern-examples",
    "typescript-design-pattern-examples",
    "python-design-pattern-examples",
    "junit",
    "mockito",
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
    "spring-boot-design",
    "spring-data-jpa",
    "spring-boot-testing",
    "quarkus",
    "quarkus-design",
    "quarkus-persistence",
    "hibernate-orm-panache",
    "quarkus-testing",
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
    "module-coverage.md",
    "code-project-wiki",
    "documentation-page-verify",
    "create-project-configuration",
    "PROJECT.yaml",
    "intermediate, reviewable intent log",
    "Normal planned development proceeds top down",
    "Project-specific evaluation skills may freeze inputs and compare completed candidates",
    "detection.yaml",
    "python3 scripts/build-technology-detection.py",
    "detect-technology-skills",
    "- liquibase",
    "- java-design",
    "- object-creation-patterns",
    "- singleton-pattern",
    "- interface-patterns",
    "- composition-patterns",
    "- state-strategy-patterns",
    "- request-patterns",
    "- collaboration-patterns",
    "- traversal-patterns",
    "- interpreter-pattern",
    "- java-design-pattern-examples",
    "- typescript-design-pattern-examples",
    "- python-design-pattern-examples",
    "- junit",
    "- mockito",
    "- spring-boot-design",
    "- spring-data-jpa",
    "- spring-boot-testing",
    "- quarkus",
    "- quarkus-design",
    "- quarkus-persistence",
    "- hibernate-orm-panache",
    "- quarkus-testing",
    "jhipster-domain-modeling",
    "[Technology Skills](design/skills-modularization.html) explains always-used and rule-selected agent skills",
    "[Wiki Skills And Project Context page](design/wiki-skills-and-project-context.html)",
    "The generic Gang of Four pattern skills are request-specific assignments for design authoring and design review.",
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
    "python3 scripts/validate-agent-skills.py adapters/codex/skills",
    "ownership manifest",
    "--scope user",
    "--scope project",
    "--cleanup false",
    "--prune-owned remains accepted as a deprecated compatibility alias",
    "--remove-owned",
    "Unowned skills and agents are never removed.",
    "For a user-scope Codex deployment, the MCP skill root is the resolved absolute path to ~/.agents/skills.",
    "--dest ~/.codex/skills",
    "claim tools advertise result schema version 2",
    "Published release 0.4.0 does not contain that claim-result contract",
    "fifteen exact MCP operations",
    "one call-bearing MCP process stream",
    "An outcome-less completed call is not semantic evidence.",
    "Keep Codex openai.yaml metadata beside each source SKILL.md",
    "Before renaming or deleting a source skill",
    "conceptual agent definitions",
    "dispatch profiles",
    "Review Skill Checklist Convention",
    "review-checklist-[review-target].md",
    "artifact-name.review-checklist-[review-target].md",
    "python3 scripts/build-skill-docs.py",
    "python3 scripts/build-support-checklist.py",
    "design/generated/skill-definitions.js",
    "design/generated/template-definitions.js",
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
    "adapters/[runtime]/skills/[skill-name]/SKILL.md",
    "The matching adapter skill source is merged only when that adapter is selected.",
    "codex-harness-directives",
)
DEVELOPMENT_METHODOLOGY_REQUIRED_PHRASES = (
    "Do not copy this bundle's skills or generated native agent definitions into user-home runtime folders",
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
MODULARIZATION_REQUIRED_PHRASES = (
    "Core Agent Skills",
    "Why Technology-Specific Skills Are Loaded Separately",
    "Technology Extensions Setup Process",
    "may directly reference both required and optional core skills",
    "Both kinds of directly referenced skills must be technology-agnostic",
    "Required core skill",
    "Optional core skill",
    "Required versus optional is not the architectural split",
    "No finite agent definition can list every language, framework, library, runtime, database, and tool",
    "only technology and domain skills that actually exist in the available skill collection",
    "New technology skills can be added without editing every generic agent definition",
    "Cross-Harness Skill Lifecycle",
    "Native runtime mechanisms",
    "Bundle selection and delivery",
    "Skill Inlining Benefits",
    "Avoiding known-skill retrieval tokens",
    "Reducing tool-call interruptions",
    "Conditional MCP delivery path",
    "directs the agent to load the complete selected set in one bounded <code>skill_load</code> call",
    "avoids constructing shell commands or helper code for retrieval",
    "preserving native Claude Code and Codex invocation paths",
    "Development precursor — outside setup",
    "Actor: Project Configurator",
    "reviewable intent log",
    "edit PROJECT.yaml to force a correction",
    "Operational result — after setup",
    "Technology Extension Skills",
    "generic pattern family covers all 23 Gang of Four object-oriented patterns",
    "request-specific assignments for Dev Documentation Writer and Dev Artifact Reviewer",
    "pattern examples remain setup-detected technology skills",
    "Changeset identity, include-chain, validation, update, rollback, and recovery guidance together with SQL.",
    "jhipster-domain-modeling",
    "How Setup-Time Technology Detection Works",
    "runs the detector once for each representative folder scope",
    "nearest supported owning project boundary",
    "Every rule has a root anyOf list",
    "Requires one file to satisfy both the path pattern and the allowed extension",
    "Comments and string literals are ignored",
    "For an exclusive group, the lowest numeric priority wins",
    "NO_VARIANT",
    "BLOCKED",
)
TECHNOLOGY_EXTENSION_SKILLS = (
    "python",
    "fastapi",
    "java",
    "java-design",
    "java-design-pattern-examples",
    "typescript-design-pattern-examples",
    "python-design-pattern-examples",
    "junit",
    "mockito",
    "spring-boot",
    "spring-boot-design",
    "spring-data-jpa",
    "spring-boot-testing",
    "quarkus",
    "quarkus-design",
    "quarkus-persistence",
    "hibernate-orm-panache",
    "quarkus-testing",
    "liquibase",
    "jhipster-project",
    "jhipster-domain-modeling",
    "jhipster-persistence",
    "jhipster-testing",
    "jhipster-security",
    "nextjs-app-router",
    "postgres-drizzle",
    "jest",
    "vitest",
    "electron-main",
)
CORE_PATTERN_SKILLS = (
    "object-creation-patterns",
    "singleton-pattern",
    "interface-patterns",
    "composition-patterns",
    "state-strategy-patterns",
    "request-patterns",
    "collaboration-patterns",
    "traversal-patterns",
    "interpreter-pattern",
)
AGENT_ROLE_MAP_REQUIRED_PHRASES = (
    "Agents for Methodology Maintenance",
    "Agents for Project Setup",
    "Agents for Wiki Activities",
    "Agents for Dev Activities",
    "DEV_METHODOLOGY_ROLE_DEFINITIONS",
    "loadout-details",
    "generated/skill-definitions.js",
    "generated/role-definitions.js",
    "agent-browser.js",
    "skill-browser.js",
    "skill-catalog__stack",
    "const developmentPracticeCategory = categoriesById.get(",
    'categoriesById.get("design-patterns")',
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
    'class="hierarchy-embed"',
    "Open the interactive SVG diagram",
    "explore agents, detected skills, harness loading, and evidence in the wiring map",
    'id="agent-skill-hierarchy"',
    "dev-methodology:view-definition",
    "event.source !== hierarchyMap.contentWindow",
    "openDefinitionFromHierarchy",
    "definitionReturnTarget",
)
GENERIC_AGENT_DEFINITIONS_REQUIRED_PHRASES = (
    "Generic Agent Definitions Source",
    "The Portability Problem",
    "Skills Have A Portable File Standard",
    "Agents Do Not Have One Portable Runtime File",
    "The source skill definition is also the runtime skill definition.",
    "From Conceptual Agent Definitions To Native Agent Definitions",
    "conceptual agent definition source, not a file that an agent harness loads directly",
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
    "Conceptual Agent Definition Properties",
    "Properties We Ignore",
    "Behavior We Default",
    "Native Runtime Packaging",
    "[mcp_servers.name]",
    "[[skills.config]]",
    "prefix_rule",
    "Conceptual-To-Native Property Mapping",
    "skills[].condition",
    "skillAvailability",
    "fixedBehavior.userInvocable",
    "fixedBehavior.automaticDelegation",
    "design/generated/role-definitions.js",
    "Harness-specific skill source",
    "adapters/&lt;harness-name&gt;/skills/&lt;skill-name&gt;/SKILL.md",
    "Mutation-capable definitions inline <code>codex-harness-directives</code> by default",
)
AGENTIC_CONFIGURATION_REQUIRED_PHRASES = (
    "Agentic Configuration",
    "This page describes runtime use.",
    "Knowledge Structure",
    "Context Layers",
    "Shared Definitions",
    "Skill Definition Files",
    "Agent Definition Files",
    "Project-Specific Definitions",
    "Project Skill Definition Files",
    "Project Agent Definition Files",
    "Root Project Instruction Files",
    "Nested Project Instruction Files",
    "Runtime Configuration File Locations",
    "In order to generate usable code, we need to provide all of the relevant context that will steer the agent to generating it in a way that is acceptable to us.",
    "The main problem is choosing the relevant context from many possible units of information.",
    "The solution is to split up the information into many files and have the agentic coding tool load just the skills it needs.",
    "The Agent Skills format uses a text file named <code>SKILL.md</code> to describe how to perform actions.",
    "It is adopted by all vendors and is the most granular unit of description.",
    "Harness-specific agent definition files describe the purpose of a specific agent, the skills and other agents it should use, and its other directives.",
    "Each agent operates with its own context and history, which allows us to partition the amount of information being worked on at a given time by creating a hierarchy of agents.",
    "Definitions installed for a harness are available to all projects that use that harness.",
    "Definitions and instructions stored within a project apply only to that project and can tailor shared behavior to its content.",
    "Project skill definition files describe actions that are specific to the project or customize a shared skill for the project.",
    "Project agent definition files define project-specific agents or customize shared harness-specific agent definitions for the project.",
    "Project setup creates a portable <code>AGENTS.md</code> at the project root.",
    "This guidance should usually act as a router to load skills appropriate for the project content.",
    "Project setup can place another portable <code>AGENTS.md</code> in a folder that needs specialized guidance.",
    "Every harness uses the same portable Agent Skills package",
    "Skill locations and precedence vary; the <code>SKILL.md</code> format does not.",
    '<label for="harness-filter">Show harness</label>',
    '<option value="all">All harnesses</option>',
    "Shared Or User Location",
    "Harness Rule Or File Format",
    "Package reusable action guidance that loads on demand when a task matches the skill.",
    "Define a specialized worker's purpose, isolated context, tools, model, and delegation behavior.",
    "Provide project-wide context and routing instructions that the harness loads for every applicable task.",
    "Add or override instructions for a folder, path pattern, or narrower working scope.",
    "~/.agents/skills/&lt;skill-name&gt;/SKILL.md",
    "~/.claude/skills/&lt;skill-name&gt;/SKILL.md",
    "~/.gemini/skills/&lt;skill-name&gt;/SKILL.md",
    "~/.junie/skills/&lt;skill-name&gt;/SKILL.md",
    "~/.copilot/skills/&lt;skill-name&gt;/SKILL.md",
    "&lt;project-root&gt;/.codex/agents/&lt;agent-name&gt;.toml",
    "&lt;project-root&gt;/.claude/agents/&lt;agent-name&gt;.md",
    "&lt;project-root&gt;/.gemini/agents/&lt;agent-name&gt;.md",
    "&lt;project-root&gt;/.junie/agents/&lt;agent-name&gt;.md",
    "&lt;project-root&gt;/.github/agents/&lt;agent-name&gt;.agent.md",
    "&lt;project-root&gt;/.github/copilot-instructions.md",
    "&lt;project-root&gt;/.github/instructions/&lt;rule-name&gt;.instructions.md",
    "&lt;project-root&gt;/AGENTS.md</code> with colocated <code>&lt;project-root&gt;/CLAUDE.md",
    "Inherited through the applicable <code>CLAUDE.md</code> bridge",
    "&lt;folder-path&gt;/AGENTS.md</code> with a colocated <code>&lt;folder-path&gt;/CLAUDE.md",
    "same portable folder guidance as other harnesses",
    "Adapter-owned skill definitions use the same <code>SKILL.md</code> format",
    "Codex-generated agents that may mutate the repository inline its instructions by default",
    "Read-only Codex agents and non-Codex adapters do not receive it.",
    "The Codex MCP skill root must match the selected installer destination.",
    "same fifteen MCP operations",
    "one call-bearing MCP process stream",
    "An outcome-less completed call is not semantic evidence.",
)
DOCUMENT_INFORMATION_OWNERS = {
    "agent-and-skill-definitions.html": (
        "Core Agent and Skills",
        "Interactive Agent And Skill Map",
        "Skill Catalog",
    ),
    "agentic-configuration.html": (
        "Knowledge Structure",
        "Context Layers",
        "Runtime Configuration File Locations",
    ),
    "skills-modularization.html": ("Technology Skills",) + MODULARIZATION_REQUIRED_PHRASES[:3] + (
        "Technology Extension Skills",
        "How Setup-Time Technology Detection Works",
    ),
    "generic-agent-definitions-source.html": (
        "The Portability Problem",
        "From Conceptual Agent Definitions To Native Agent Definitions",
        "Conceptual Agent Definition Properties",
        "Native Runtime Packaging",
        "Conceptual-To-Native Property Mapping",
    ),
    "agent-skill-specialization-examples.html": (
        "Examples",
        "Configuration Examples",
        "Northwind Tools: Root-Only Guidance",
        "Acme Ledger: Nested Tier Guidance",
        "Beacon Knowledge Base: Workflow Separation",
    ),
    "orchestrated-development-lifecycle.html": (
        "Start With The Backlog",
        "The File-Backed Backlog",
        "Agents And Handoffs",
        "Private Branches And Worktrees",
        "Coordinating Shared Resources",
        "Review, Verification, And Delivery",
        "User Decisions Stop Only The Affected Item",
        "Evidence That Proves Delivery",
        "Design And Documentation Work Uses The Same Loop",
    ),
    "documentation-templates.html": (
        "Documentation Templates",
        "Template Catalog",
        "Template Selection",
        "Wiki Format",
        "Template Completion",
    ),
    "wiki-skills-and-project-context.html": (
        "Wiki Skills And Project Context",
        "Four Layers, Not Four Names For One Thing",
        "Compiled Context Flow",
        "Project Wiki Operating Model",
        "Separation Of Work",
        "Skill Collaboration Boundaries",
        "Code-Aware Hybrid",
        "Verification And Compounding Health",
    ),
}
DOCUMENT_FORBIDDEN_HEADINGS = {
    "skills-modularization.html": (
        "Role Agent Set",
        "Skill Load Model",
        "File Contracts",
        "Semantic Model Profiles",
        "Role Agent Dispatch Loop",
        "Root AGENTS.md Policy Pattern",
        "Nested AGENTS.md Shape",
        "Agent Set Normalization",
        "Project Classification",
        "Project Guidance And Precedence",
        "Selection Model",
        "Deterministic Setup-Time Technology Detection",
        "When To Create A Specialized Agent",
    ),
    "agent-and-skill-definitions.html": (
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
DOCUMENT_REQUIRED_CONTENT_LINKS = {
    "skills-modularization.html": (
        "agent-and-skill-definitions.html#skills-title",
        "wiki-skills-and-project-context.html",
    ),
    "agent-skill-specialization-examples.html": (
        "../skills/development-methodology/assets/templates/project-template.yaml",
    ),
    "generic-agent-definitions-source.html": (
        "../README.md#explicit-target-deployment",
    ),
    "orchestrated-development-lifecycle.html": (
        "../skills/create-file-work-item/SKILL.md",
        "../skills/manage-file-work-items/SKILL.md",
        "../skills/agent-claim/SKILL.md",
        "../skills/complete-work-item-direct-main/SKILL.md",
        "../skills/complete-work-item-feature-branch/SKILL.md",
        "../skills/create-pull-request/SKILL.md",
        "../scripts/test_agent_claim.py",
        "../README.md#agent-claims-and-worktrees",
        "agent-and-skill-definitions.html#dev-activities-title",
        "documentation-templates.html",
        "wiki-skills-and-project-context.html",
    ),
    "documentation-templates.html": (
        "../skills/development-methodology/assets/templates/project-template.yaml",
        "../skills/development-methodology/assets/templates/project-wiki-template.md",
        "../skills/development-methodology/assets/templates/functional-spec-template.md",
        "../skills/development-methodology/assets/templates/architecture-template.md",
        "../skills/development-methodology/assets/templates/high-level-design-template.md",
        "../skills/development-methodology/assets/templates/module-design-template.md",
        "../skills/development-methodology/assets/templates/unit-test-plan-template.md",
        "../skills/project-wiki/references/page-schema.md",
        "wiki-skills-and-project-context.html",
    ),
    "wiki-skills-and-project-context.html": (
        "https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f",
        "https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing",
        "https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md",
        "../skills/project-wiki/SKILL.md",
        "../skills/project-wiki-create/SKILL.md",
        "../skills/project-wiki-query/SKILL.md",
        "../skills/project-wiki-research/SKILL.md",
        "../skills/project-wiki-review/SKILL.md",
        "../skills/project-wiki-topic-write/SKILL.md",
        "../skills/project-wiki-topic-verify/SKILL.md",
        "../skills/code-project-wiki/SKILL.md",
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
    "Update the design HTML files that describe skills, conceptual agent definitions",
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

    def test_codex_coordination_controls_long_running_tasks(self) -> None:
        skill_text = (
            SKILLS_ROOT / "codex-workitem-coordination" / "SKILL.md"
        ).read_text(encoding="utf-8")

        for phrase in (
            "Treat a heartbeat as ownership evidence only.",
            "expected to take more than five minutes",
            "the exact currently active unit and any later units that have not started",
            "a hard stop condition and the retained evidence path",
            "not a new backlog transaction or parent approval gate",
            "The task may start without waiting for parent acknowledgement.",
            "This observation must not serialize healthy work.",
            "must not describe queued work as running.",
            "classify its failure signature before repeating anything",
            "add the smallest offline replay or deterministic regression",
            "Run one cheapest representative first.",
            "prove the applicable worktree clean before releasing its shared claim",
            "retain and heartbeat the claim or hand it off explicitly",
            "Do not let later serial cases start automatically after a shared-boundary failure.",
            "require immediate parent investigation and a revised plan",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, skill_text)

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

    def test_structured_design_distinguishes_response_and_artifact_modes(self) -> None:
        skill_path = SKILLS_ROOT / "structured-design" / "SKILL.md"
        skill_text = skill_path.read_text(encoding="utf-8")
        frontmatter = load_yaml_object_from_frontmatter(skill_path)
        description = " ".join(frontmatter["description"].split())

        self.assertIn(
            "Produces a structured Markdown design as response content, or authors or revises a design artifact",
            description,
        )
        for phrase in (
            "Use design-response mode by default",
            "Do not create a design file merely because design content was requested.",
            "Use artifact-authoring mode when the request explicitly asks to create,",
            "This includes updating an existing authoritative design document as part of",
            "Use the requested path, an existing authoritative artifact, or the",
            "report the placement blocker",
            "Design an authentication system.",
            "Create docs/design/authentication.md.",
            "Update the existing component design while implementing this",
            "Use the repository's file-placement mechanism rather than",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, skill_text)

        for blanket_rule in (
            "This skill returns markdown text only.",
            "- Do not write files.",
            "- Do not choose filenames.",
        ):
            with self.subTest(blanket_rule=blanket_rule):
                self.assertNotIn(blanket_rule, skill_text)

        for preserved_contract in (
            "## Root-Level Item Types",
            "## Assertion Lines",
            "## Required Discipline",
            "## Recommended Section Order",
            "Use markdown nested bullets with two spaces per level.",
            "`SYNOPSIS` states the item's role.",
            "`BECAUSE` must justify its immediate parent line only.",
            "`CHAIN-OF-THOUGHT` exists only to explain how the immediate parent leads to",
        ):
            with self.subTest(preserved_contract=preserved_contract):
                self.assertIn(preserved_contract, skill_text)

        probes = load_yaml_object(REPOSITORY_ROOT / "evals" / "skill-probes.yaml")
        probe = next(
            entry
            for entry in probes["probes"]
            if entry["id"] == "probe-structured-design"
        )
        self.assertIn("response-only design request", probe["negativeCondition"])
        self.assertIn("repository placement mechanism", probe["expectedBehavior"])

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

    def test_azure_devops_and_jira_placeholders_block_without_fallback(self) -> None:
        expected = {
            "create-azure-devops-work-item": ("azure-devops", "create"),
            "manage-azure-devops-work-items": ("azure-devops", "the requested"),
            "create-jira-work-item": ("jira", "create"),
            "manage-jira-work-items": ("jira", "the requested"),
        }

        for skill_name, (provider, operation) in expected.items():
            with self.subTest(skill_name=skill_name):
                skill_text = (SKILLS_ROOT / skill_name / "SKILL.md").read_text(
                    encoding="utf-8"
                )
                self.assertIn("Status: BLOCKED.", skill_text)
                self.assertIn(f"Provider: {provider}.", skill_text)
                self.assertIn(f"Requested operation: {operation}", skill_text)
                self.assertIn("Missing capability:", skill_text)
                self.assertIn("Work-item identifier: none.", skill_text)
                self.assertIn("Mutation evidence:", skill_text)
                self.assertIn("Next authority or implementation decision:", skill_text)
                self.assertIn("Do not replace", skill_text)
                self.assertIn("filesystem", skill_text)
                metadata_text = openai_metadata_path(skill_name).read_text(
                    encoding="utf-8"
                )
                self.assertNotIn("dependencies:\n  tools:", metadata_text)

        probes = load_yaml_object(REPOSITORY_ROOT / "evals" / "skill-probes.yaml")
        probe_ids = {entry["id"] for entry in probes["probes"]}
        for skill_name in expected:
            self.assertIn(f"probe-{skill_name}", probe_ids)

        placeholder_probes = {
            entry["id"]: entry for entry in probes["probes"] if entry["id"] in probe_ids
        }
        for skill_name in expected:
            probe = placeholder_probes[f"probe-{skill_name}"]
            self.assertEqual(["provider-placeholder-matrix"], probe["executableCases"])
            self.assertEqual("fixture-backed", probe["coverageStatus"])

        cases = load_yaml_object(REPOSITORY_ROOT / "evals" / "cases.yaml")
        placeholder_case = next(
            case
            for case in cases["cases"]
            if case["id"] == "provider-placeholder-matrix"
        )
        self.assertTrue(placeholder_case["readOnly"])
        self.assertEqual([], placeholder_case["allowedWritePaths"])
        deterministic_checks = placeholder_case["judgePlan"]["deterministicChecks"]
        self.assertIn("no-forbidden-mutation", deterministic_checks)
        self.assertIn("output-contract-presence", deterministic_checks)

    def test_gitlab_work_item_skills_define_provider_native_authority_and_lifecycle(self) -> None:
        create_text = (SKILLS_ROOT / "create-gitlab-work-item" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        manage_text = (SKILLS_ROOT / "manage-gitlab-work-items" / "SKILL.md").read_text(
            encoding="utf-8"
        )

        for text in (create_text, manage_text):
            for phrase in (
                "authenticated GitLab issue interface",
                "issue internal identifier",
                "repository backlog files",
                "GitHub issues",
                "Return BLOCKED",
                "Read the issue back",
                "namespace",
                "project",
                "labels",
                "assignees",
                "relationships",
                "updated content",
            ):
                with self.subTest(phrase=phrase):
                    self.assertIn(phrase, text)
            self.assertNotIn("pull request", text.lower())

        for phrase in (
            "Search open and recently closed issues",
            "do not create another issue",
            "several plausible matches exist",
            "partial-mutation evidence",
            "Never retry by creating a second issue",
        ):
            with self.subTest(create_phrase=phrase):
                self.assertIn(phrase, create_text)

        for phrase in (
            "Keep issue completion independent from delivery completion",
            "Merge-request publication",
            "completion disposition READY",
            "successful pipeline",
            "main-observation",
            "claim-release",
            "Only after the terminal update is observed",
            "return terminal evidence and lifecycle COMPLETED",
            "preserve the READY disposition",
            "Reopen only when authorized recovery",
            "Do not repeat an ambiguous mutation",
        ):
            with self.subTest(manage_phrase=phrase):
                self.assertIn(phrase, manage_text)

    def test_create_pull_request_skill_and_template_define_modular_scope_and_review_order(
        self,
    ) -> None:
        skill_path = SKILLS_ROOT / "create-pull-request" / "SKILL.md"
        template_path = (
            SKILLS_ROOT
            / "create-pull-request"
            / "assets"
            / "pull-request-template.md"
        )
        skill_text = skill_path.read_text(encoding="utf-8")
        template_text = template_path.read_text(encoding="utf-8")

        for phrase in (
            "create the base dependency first",
            "recreate the pull requests in dependency order before handoff",
            "no substantive human review, comments, external references, or check history would be lost",
            "Do not leave a completed pull request in draft merely because it belongs to a stack.",
            "Create and verify replacements before closing obsolete pull requests.",
            "Prefer multiple focused pull requests over one avoidably broad pull request",
            "one common protocol and tooling pull request followed by one pull request per agent suite",
            "Keep work together when splitting would break an atomic behavior",
            "Do not use file count alone to decide the split.",
        ):
            with self.subTest(skill_phrase=phrase):
                self.assertIn(phrase, skill_text)

        for heading in (
            "## Summary",
            "## Changes",
            "## Scope And Modularity",
            "## Verification",
            "## Review State",
            "## Review Order",
            "## Risks And Follow-Up",
        ):
            with self.subTest(template_heading=heading):
                self.assertIn(heading, template_text)

        role = load_yaml_object(
            ROLES_ROOT / "dev-activities" / "dev-coder.role.yaml"
        )
        pull_request_skill = next(
            entry["create-pull-request"]
            for entry in role["skills"]
            if "create-pull-request" in entry
        )
        self.assertIn("feature-branch-workitem", pull_request_skill["condition"])

        probes = load_yaml_object(REPOSITORY_ROOT / "evals" / "skill-probes.yaml")
        probe = next(
            entry
            for entry in probes["probes"]
            if entry["id"] == "probe-create-pull-request"
        )
        self.assertIn("base dependencies before dependents", probe["expectedBehavior"])
        self.assertIn(
            "smallest coherent independently reviewable pull requests",
            probe["expectedBehavior"],
        )

        workflow_packs = load_yaml_object(
            REPOSITORY_ROOT / "evals" / "workflow-packs.yaml"
        )
        code_delivery = next(
            entry for entry in workflow_packs["packs"] if entry["id"] == "code-delivery"
        )
        self.assertIn("probe-create-pull-request", code_delivery["skillProbes"])
        self.assertIn(
            "- create-pull-request",
            README_PATH.read_text(encoding="utf-8"),
        )
        self.assertIn(
            "Focused pull requests separate shared foundations from independently reviewable changes",
            (REPOSITORY_ROOT / "design" / "agent-and-skill-definitions.html").read_text(
                encoding="utf-8"
            ),
        )

    def test_complete_work_item_feature_branch_requires_observed_provider_accurate_merge(
        self,
    ) -> None:
        skill_path = (
            SKILLS_ROOT / "complete-work-item-feature-branch" / "SKILL.md"
        )
        skill_text = skill_path.read_text(encoding="utf-8")

        for phrase in (
            "Create the intended feature branch from the assigned base before changing source files.",
            "use create-pull-request and GitHub evidence. Call it a pull request.",
            "use the configured merge-request capability and GitLab evidence. Call it a merge request.",
            "Successful publication returns AWAITING_REVIEW",
            "A ready publication is not READY delivery evidence.",
            "apply accepted corrections on the same branch",
            "The pull request or merge request reports a merged state",
            "reachable from the configured base branch in Git",
            "A closed-unmerged, abandoned, replaced, or superseded publication cannot return READY.",
            "canonical work-item identifier and provider reference",
            "the provider lifecycle update this evidence authorizes",
        ):
            with self.subTest(skill_phrase=phrase):
                self.assertIn(phrase, skill_text)

        self.assertIn(
            "- complete-work-item-feature-branch",
            README_PATH.read_text(encoding="utf-8"),
        )
        self.assertIn(
            "Publication is therefore a resumable handoff rather than completion.",
            (
                REPOSITORY_ROOT / "design" / "agent-and-skill-definitions.html"
            ).read_text(encoding="utf-8"),
        )

        probes = load_yaml_object(REPOSITORY_ROOT / "evals" / "skill-probes.yaml")
        probe = next(
            entry
            for entry in probes["probes"]
            if entry["id"] == "probe-complete-work-item-feature-branch"
        )
        self.assertEqual("complete-work-item-feature-branch", probe["skill"])
        self.assertIn("configured base-branch reachability", probe["expectedBehavior"])
        self.assertIn(
            "return AWAITING_REVIEW while review checks dependencies or merge remain pending",
            probe["expectedBehavior"],
        )
        self.assertIn(
            "return READY only after required approvals checks dependency order host merge and configured base-branch reachability",
            probe["expectedBehavior"],
        )
        self.assertEqual(
            "Explicitly selected direct-main completion, or a request only to draft publication content without feature-branch delivery, does not activate this skill.",
            probe["negativeCondition"],
        )
        self.assertIn(
            "only that manager or the provider-none task result records lifecycle COMPLETED",
            probe["expectedBehavior"],
        )
        self.assertNotIn("phase-order", probe["judgePlan"]["deterministicChecks"])
        self.assertIn(
            "readiness-consistency",
            probe["judgePlan"]["deterministicChecks"],
        )
        self.assertEqual(["code-delivery"], probe["workflowAssociations"])

        workflow_packs = load_yaml_object(
            REPOSITORY_ROOT / "evals" / "workflow-packs.yaml"
        )
        code_delivery = next(
            entry for entry in workflow_packs["packs"] if entry["id"] == "code-delivery"
        )
        self.assertIn(
            "probe-complete-work-item-feature-branch",
            code_delivery["skillProbes"],
        )

    def test_workitem_provider_and_completion_processes_are_selector_driven(self) -> None:
        execute_text = (
            SKILLS_ROOT / "execute-workitem" / "SKILL.md"
        ).read_text(encoding="utf-8")
        simple_text = (
            SKILLS_ROOT
            / "execute-workitem"
            / "references"
            / "simple-workitem.md"
        ).read_text(encoding="utf-8")
        feature_text = (
            SKILLS_ROOT
            / "execute-workitem"
            / "references"
            / "feature-branch-workitem.md"
        ).read_text(encoding="utf-8")
        create_file_text = (
            SKILLS_ROOT / "create-file-work-item" / "SKILL.md"
        ).read_text(encoding="utf-8")
        manage_file_text = (
            SKILLS_ROOT / "manage-file-work-items" / "SKILL.md"
        ).read_text(encoding="utf-8")
        legacy_file_text = (
            SKILLS_ROOT / "file-based-backlog" / "SKILL.md"
        ).read_text(encoding="utf-8")
        github_backlog_text = (
            SKILLS_ROOT / "github-issues-backlog" / "SKILL.md"
        ).read_text(encoding="utf-8")
        create_github_text = (
            SKILLS_ROOT / "create-github-work-item" / "SKILL.md"
        ).read_text(encoding="utf-8")
        manage_github_text = (
            SKILLS_ROOT / "manage-github-work-items" / "SKILL.md"
        ).read_text(encoding="utf-8")

        self.assertIn("simple-workitem or feature-branch-workitem", execute_text)
        self.assertIn("Read only the selected process", execute_text)
        self.assertIn("Do not push a branch or create a pull request", simple_text)
        self.assertIn("Set the pull request ready for review", feature_text)
        self.assertIn("report AWAITING_REVIEW", feature_text)
        self.assertIn("effective provider is file", create_file_text)
        self.assertIn("effective provider is file", manage_file_text)
        self.assertIn("create-file-work-item and manage-file-work-items", legacy_file_text)
        self.assertNotIn("## Operations", legacy_file_text)
        self.assertIn("transition route for current generated and configured callers", github_backlog_text)
        self.assertIn("create-github-work-item", github_backlog_text)
        self.assertIn("manage-github-work-items", github_backlog_text)
        self.assertIn("Search open and recently closed issues", create_github_text)
        self.assertIn("do not create another", create_github_text)
        self.assertIn("possibly completed mutation", create_github_text)
        self.assertIn("never retry creation blindly", create_github_text)
        self.assertIn("Do not create repository backlog files", create_github_text)
        self.assertIn("permission denial", create_github_text)
        self.assertIn("Re-read provider state before a transition", manage_github_text)
        self.assertIn("Record BLOCKED", manage_github_text)
        self.assertIn("Reopen only when explicit workflow authority permits it", manage_github_text)
        self.assertIn("publication or AWAITING_REVIEW alone", manage_github_text)
        self.assertIn("possibly applied", manage_github_text)
        self.assertIn("Do not create repository backlog files", manage_github_text)

        coder = load_yaml_object(
            ROLES_ROOT / "dev-activities" / "dev-coder.role.yaml"
        )
        coder_skills = {
            skill_name: metadata
            for entry in coder["skills"]
            for skill_name, metadata in entry.items()
        }
        self.assertIn("execute-workitem", coder_skills)
        self.assertNotIn("condition", coder_skills["execute-workitem"])
        self.assertIn("feature-branch-workitem", coder_skills["create-pull-request"]["condition"])
        self.assertIn("work-item delivery status", {
            next(iter(entry)) for entry in coder["outputContract"]
        })

        orchestrator = load_yaml_object(
            ROLES_ROOT / "dev-activities" / "dev-orchestrator.role.yaml"
        )
        orchestrator_skills = {
            next(iter(entry)) for entry in orchestrator["skills"]
        }
        self.assertNotIn("create-pull-request", orchestrator_skills)
        self.assertNotIn("manage-backlog", orchestrator_skills)
        self.assertIn("dev-backlog-steward", orchestrator["agentDependencies"])

        backlog_steward = load_yaml_object(
            ROLES_ROOT / "dev-activities" / "dev-backlog-steward.role.yaml"
        )
        backlog_skills = {
            skill_name: metadata
            for entry in backlog_steward["skills"]
            for skill_name, metadata in entry.items()
        }
        self.assertIn("file-based-backlog", backlog_skills)
        self.assertIn("github-issues-backlog", backlog_skills)
        self.assertIn("condition", backlog_skills["file-based-backlog"])
        self.assertIn("condition", backlog_skills["github-issues-backlog"])

        project_template = (
            SKILLS_ROOT
            / "development-methodology"
            / "assets"
            / "templates"
            / PROJECT_TEMPLATE
        ).read_text(encoding="utf-8")
        self.assertIn("workflow_selection:", project_template)
        self.assertIn("provider:", project_template)
        self.assertIn("file, github, gitlab, azure-devops, jira, none, or UNSET", project_template)
        self.assertIn(
            'provider: "TODO: file, github, gitlab, azure-devops, jira, none, or UNSET."',
            project_template,
        )
        self.assertIn("completion:", project_template)
        self.assertIn("direct-main, feature-branch, or UNSET", project_template)
        self.assertIn(
            'completion: "TODO: direct-main, feature-branch, or UNSET."',
            project_template,
        )
        self.assertNotIn("  workitem:", project_template)
        self.assertNotIn("  backlog:", project_template)

        project_configuration = load_yaml_object(REPOSITORY_ROOT / "PROJECT.yaml")
        self.assertEqual(
            "file",
            project_configuration["workflow_selection"]["provider"]["default"],
        )
        self.assertEqual(
            "direct-main",
            project_configuration["workflow_selection"]["completion"]["default"],
        )
        agents_text = (REPOSITORY_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("## Work-Item Workflow Skill References", agents_text)
        self.assertIn("create-file-work-item", agents_text)
        self.assertIn("manage-file-work-items", agents_text)
        self.assertIn("complete-work-item-direct-main", agents_text)
        self.assertIn("Technology skill inlining is a separate mechanism", agents_text)

        probes = load_yaml_object(REPOSITORY_ROOT / "evals" / "skill-probes.yaml")
        probe_ids = {entry["id"] for entry in probes["probes"]}
        for probe_id in (
            "probe-execute-workitem",
            "probe-file-based-backlog",
            "probe-create-github-work-item",
            "probe-manage-github-work-items",
            "probe-create-file-work-item",
            "probe-github-issues-backlog",
            "probe-manage-file-work-items",
        ):
            self.assertIn(probe_id, probe_ids)

        readme_text = README_PATH.read_text(encoding="utf-8")
        for skill_name in (
            "execute-workitem",
            "file-based-backlog",
            "create-github-work-item",
            "manage-github-work-items",
            "create-file-work-item",
            "github-issues-backlog",
            "manage-file-work-items",
        ):
            self.assertIn(f"- {skill_name}", readme_text)

    def test_direct_main_completion_requires_integrated_main_evidence(self) -> None:
        skill_name = "complete-work-item-direct-main"
        skill_path = SKILLS_ROOT / skill_name / "SKILL.md"
        skill_text = skill_path.read_text(encoding="utf-8")

        required_phrases = (
            "This skill owns Git delivery and main observation.",
            "Do not include provider lifecycle surfaces in this integration claim.",
            "Preserve unrelated main advances.",
            "do not manufacture a topology-only merge",
            "The integration commit is an ancestor of the observed main tip.",
            "content-equivalence evidence",
            "Do not report a provider-backed item as completed before that succeeds.",
            "An unmerged temporary branch can never return READY or cause lifecycle COMPLETED.",
        )
        for phrase in required_phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, skill_text)

        self.assertTrue(openai_metadata_path(skill_name).is_file())
        self.assertIn(
            f"- {skill_name}",
            README_PATH.read_text(encoding="utf-8"),
        )

        generated_text = SKILL_DEFINITIONS_PATH.read_text(encoding="utf-8")
        self.assertIn(f'"name": "{skill_name}"', generated_text)

        probes = load_yaml_object(REPOSITORY_ROOT / "evals" / "skill-probes.yaml")
        probe = next(
            entry
            for entry in probes["probes"]
            if entry["id"] == "probe-complete-work-item-direct-main"
        )
        self.assertEqual(skill_name, probe["skill"])
        self.assertIn("unmerged temporary branch", probe["negativeCondition"])

        workflow_packs = load_yaml_object(
            REPOSITORY_ROOT / "evals" / "workflow-packs.yaml"
        )
        code_delivery = next(
            entry for entry in workflow_packs["packs"] if entry["id"] == "code-delivery"
        )
        self.assertIn(
            "probe-complete-work-item-direct-main",
            code_delivery["skillProbes"],
        )
        self.assertTrue(
            (REPOSITORY_ROOT / "scripts" / "test_direct_main_completion_contract.py").is_file()
        )

    def test_jhipster_guidance_is_split_into_focused_skill_packages(self) -> None:
        expected_phrases = {
            "jhipster-project": "generated-code boundaries",
            "jhipster-domain-modeling": "relationship direction",
            "jhipster-persistence": "development fake data",
            "jhipster-testing": "Testcontainers profile",
            "jhipster-security": "AuthoritiesConstants",
        }

        for skill_name, phrase in expected_phrases.items():
            with self.subTest(skill_name=skill_name):
                skill_root = SKILLS_ROOT / skill_name
                skill_text = (skill_root / "SKILL.md").read_text(encoding="utf-8")
                self.assertLessEqual(len(skill_text.splitlines()), 40)
                self.assertIn(phrase, skill_text)
                self.assertIn("Java and Spring Boot", skill_text)
                self.assertTrue((skill_root / "detection.yaml").is_file())

        testing_text = (SKILLS_ROOT / "jhipster-testing" / "SKILL.md").read_text(encoding="utf-8")
        security_text = (SKILLS_ROOT / "jhipster-security" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Test Strategy", testing_text)
        self.assertNotIn("Run the narrow affected tests", testing_text)
        self.assertIn("Application Security", security_text)
        self.assertNotIn("Keep signing keys", security_text)

    def test_java_and_spring_design_are_separate_from_coding_guidance(self) -> None:
        expected = {
            "java": (
                "Coding Boundary",
                "references/coding-guidelines-java.md",
            ),
            "java-design": (
                "Design Boundary",
                "references/design-principles-java.md",
            ),
            "spring-boot": (
                "Framework Baseline",
                "references/coding-guidelines-spring-boot.md",
            ),
            "spring-boot-design": (
                "Design Boundary",
                "references/design-principles-spring-boot.md",
            ),
            "spring-data-jpa": (
                "Persistence Coding",
                "references/persistence-guidelines-spring-data-jpa.md",
            ),
            "spring-boot-testing": (
                "Test Selection",
                "references/testing-guidelines-spring-boot.md",
            ),
        }

        for skill_name, (boundary_phrase, reference_path) in expected.items():
            with self.subTest(skill_name=skill_name):
                skill_root = SKILLS_ROOT / skill_name
                skill_text = (skill_root / "SKILL.md").read_text(encoding="utf-8")
                self.assertIn(boundary_phrase, skill_text)
                self.assertTrue((skill_root / reference_path).is_file())
                self.assertTrue((skill_root / "detection.yaml").is_file())

        java_design = (SKILLS_ROOT / "java-design" / "SKILL.md").read_text(encoding="utf-8")
        spring_design = (SKILLS_ROOT / "spring-boot-design" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Do not own formatting", java_design)
        self.assertIn("not annotation syntax or routine framework coding", spring_design)

    def test_junit_and_mockito_are_separate_detection_backed_skills(self) -> None:
        expected = {
            "junit": (
                "JUnit Boundary",
                "references/testing-guidelines-junit.md",
            ),
            "mockito": (
                "Mockito Boundary",
                "references/mocking-guidelines-mockito.md",
            ),
        }

        for skill_name, (boundary_phrase, reference_path) in expected.items():
            with self.subTest(skill_name=skill_name):
                skill_root = SKILLS_ROOT / skill_name
                skill_text = (skill_root / "SKILL.md").read_text(encoding="utf-8")
                self.assertIn(boundary_phrase, skill_text)
                self.assertTrue((skill_root / reference_path).is_file())
                self.assertTrue((skill_root / "detection.yaml").is_file())

    def test_gof_pattern_families_are_generic_complete_and_role_assignable(self) -> None:
        expected = {
            "object-creation-patterns": (
                "Factory Method",
                "references/design-guidelines-object-creation-patterns.md",
            ),
            "singleton-pattern": (
                "exactly one instance",
                "references/design-guidelines-singleton-pattern.md",
            ),
            "interface-patterns": (
                "Use Adapter",
                "references/design-guidelines-interface-patterns.md",
            ),
            "composition-patterns": (
                "Use Composite",
                "references/design-guidelines-composition-patterns.md",
            ),
            "state-strategy-patterns": (
                "Use Strategy",
                "references/design-guidelines-state-strategy-patterns.md",
            ),
            "request-patterns": (
                "Use Command",
                "references/design-guidelines-request-patterns.md",
            ),
            "collaboration-patterns": (
                "Use Observer",
                "references/design-guidelines-collaboration-patterns.md",
            ),
            "traversal-patterns": (
                "Use Iterator",
                "references/design-guidelines-traversal-patterns.md",
            ),
            "interpreter-pattern": (
                "Use Interpreter",
                "references/design-guidelines-interpreter-pattern.md",
            ),
        }
        covered_patterns = {
            "object-creation-patterns": (
                "Factory Method",
                "Abstract Factory",
                "Builder",
                "Prototype",
            ),
            "singleton-pattern": ("Singleton",),
            "interface-patterns": ("Adapter", "Bridge", "Facade"),
            "composition-patterns": ("Composite", "Decorator", "Proxy", "Flyweight"),
            "state-strategy-patterns": ("Strategy", "State", "Template Method"),
            "request-patterns": ("Command", "Chain of Responsibility", "Memento"),
            "collaboration-patterns": ("Observer", "Mediator"),
            "traversal-patterns": ("Iterator", "Visitor"),
            "interpreter-pattern": ("Interpreter",),
        }

        flattened_patterns = {
            pattern
            for patterns in covered_patterns.values()
            for pattern in patterns
        }
        self.assertEqual(23, len(flattened_patterns))

        for skill_name, (boundary_phrase, reference_path) in expected.items():
            with self.subTest(skill_name=skill_name):
                skill_root = SKILLS_ROOT / skill_name
                skill_text = (skill_root / "SKILL.md").read_text(encoding="utf-8")
                reference_text = (skill_root / reference_path).read_text(encoding="utf-8")
                self.assertLessEqual(len(skill_text.splitlines()), 40)
                self.assertIn(boundary_phrase, skill_text)
                self.assertTrue((skill_root / reference_path).is_file())
                self.assertFalse((skill_root / "detection.yaml").exists())
                for pattern in covered_patterns[skill_name]:
                    self.assertIn(pattern, skill_text + reference_text)

        for language in ("java", "typescript", "python"):
            skill_root = SKILLS_ROOT / f"{language}-design-pattern-examples"
            example_text = "\n".join(
                path.read_text(encoding="utf-8")
                for path in sorted((skill_root / "references").glob("*-examples-*.md"))
            )
            self.assertTrue((skill_root / "detection.yaml").is_file())
            for pattern in flattened_patterns:
                self.assertIn(pattern, example_text)

    def test_generic_patterns_are_assigned_to_design_agents_and_examples_remain_detected(self) -> None:
        pattern_skills = {
            "object-creation-patterns",
            "singleton-pattern",
            "interface-patterns",
            "composition-patterns",
            "state-strategy-patterns",
            "request-patterns",
            "collaboration-patterns",
            "traversal-patterns",
            "interpreter-pattern",
        }
        example_skills = {
            "java-design-pattern-examples",
            "typescript-design-pattern-examples",
            "python-design-pattern-examples",
        }
        build_skill_docs = load_build_skill_docs_module()
        skill_payload = build_skill_docs.build_payload()
        roles = build_skill_docs.load_role_definitions(set(skill_payload["skills"]))
        roles_by_name = {role.name: role for role in roles}

        for role_name in ("dev-documentation-writer", "dev-artifact-reviewer"):
            role = roles_by_name[role_name]
            self.assertTrue(pattern_skills.issubset(role.skill_conditions))
            self.assertTrue(example_skills.isdisjoint(role.skills))

        for role in roles:
            self.assertTrue(example_skills.isdisjoint(role.skills))
            if role.name not in {"dev-documentation-writer", "dev-artifact-reviewer"}:
                self.assertTrue(pattern_skills.isdisjoint(role.skills))

    def test_quarkus_persistence_concerns_are_split_and_detection_backed(self) -> None:
        expected = {
            "quarkus": (
                "Framework Baseline",
                "references/coding-guidelines-quarkus.md",
            ),
            "quarkus-design": (
                "Design Boundary",
                "references/design-principles-quarkus.md",
            ),
            "quarkus-persistence": (
                "Shared Persistence Boundary",
                "references/persistence-guidelines-quarkus.md",
            ),
            "hibernate-orm-panache": (
                "Blocking Persistence Boundary",
                None,
            ),
            "quarkus-testing": (
                "Test Selection",
                "references/testing-guidelines-quarkus.md",
            ),
        }

        for skill_name, (boundary_phrase, reference_path) in expected.items():
            with self.subTest(skill_name=skill_name):
                skill_root = SKILLS_ROOT / skill_name
                skill_text = (skill_root / "SKILL.md").read_text(encoding="utf-8")
                self.assertIn(boundary_phrase, skill_text)
                if reference_path is not None:
                    self.assertTrue((skill_root / reference_path).is_file())
                self.assertTrue((skill_root / "detection.yaml").is_file())

        quarkus_text = (SKILLS_ROOT / "quarkus-persistence" / "SKILL.md").read_text(encoding="utf-8")
        panache_text = (SKILLS_ROOT / "hibernate-orm-panache" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Route stack-specific entity, repository, query, and transaction work", quarkus_text)
        self.assertIn("Do not use this skill for Hibernate Reactive with Panache", panache_text)

    def test_liquibase_guidance_is_portable_and_detection_backed(self) -> None:
        skill_root = SKILLS_ROOT / "liquibase"
        skill_text = (skill_root / "SKILL.md").read_text(encoding="utf-8")

        for phrase in (
            "DATABASECHANGELOG state",
            "Treat id, author, and file path as changeset identity",
            "Run Liquibase validation",
            "forward-recovery procedure",
        ):
            self.assertIn(phrase, skill_text)
        self.assertTrue((skill_root / "detection.yaml").is_file())

    def test_mysql_quartz_and_mapstruct_guidance_is_detection_backed(self) -> None:
        expected_phrases = {
            "mysql": (
                "clustered key's effect",
                "metadata-lock acquisition",
                "against the production engine",
            ),
            "quartz": (
                "explicit misfire instruction",
                "sources of duplicate or partial execution",
                "JDBCJobStore",
                "cluster membership",
            ),
            "mapstruct": (
                "explicit unmapped-target policy",
                "@MappingTarget",
                "cycle tracking",
                "clean command-line compile",
                "Inspect the generated mapper implementation",
            ),
        }

        for skill_name, phrases in expected_phrases.items():
            with self.subTest(skill=skill_name):
                skill_root = SKILLS_ROOT / skill_name
                skill_text = (skill_root / "SKILL.md").read_text(encoding="utf-8")
                self.assertTrue((skill_root / "agents" / "openai.yaml").is_file())
                self.assertTrue((skill_root / "detection.yaml").is_file())
                for phrase in phrases:
                    self.assertIn(phrase, skill_text)

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

    def test_java_comment_refines_generic_header_placement_without_losing_fields(self) -> None:
        generic_root = SKILLS_ROOT / "code-comments"
        java_root = SKILLS_ROOT / "java-comment"
        generic_text = (generic_root / "SKILL.md").read_text(encoding="utf-8")
        generic_checklist = (
            generic_root / "references" / "review-checklist-code-comments.md"
        ).read_text(encoding="utf-8")
        java_text = (java_root / "SKILL.md").read_text(encoding="utf-8")
        java_checklist = (
            java_root / "references" / "review-checklist-java-comment.md"
        ).read_text(encoding="utf-8")

        for phrase in (
            "default placement for most languages",
            "language-specific comment skill may override only the placement",
            "preserve every required information field",
        ):
            with self.subTest(generic_phrase=phrase):
                self.assertIn(phrase, generic_text)
        self.assertIn("language-specific placement override", generic_checklist)

        java_examples = re.findall(r"```java\n(.*?)```", java_text, re.DOTALL)
        self.assertEqual(4, len(java_examples))
        package_info, packaged_type, no_package_type, duplicate = java_examples
        required_fields = (
            "[exact project copyright statement]",
            "AI attribution:",
            "Responsibility:",
            "Design:",
            "Test plan:",
        )
        for example_name, example in (
            ("package_info", package_info),
            ("packaged_type", packaged_type),
            ("no_package_type", no_package_type),
        ):
            for field in required_fields:
                with self.subTest(example=example_name, field=field):
                    self.assertEqual(1, example.count(field))

        self.assertTrue(package_info.startswith("/**"))
        self.assertLess(package_info.index("*/"), package_info.index("package "))
        self.assertTrue(packaged_type.startswith("package "))
        self.assertLess(packaged_type.index("package "), packaged_type.index("/**"))
        self.assertLess(packaged_type.index("/**"), packaged_type.index("public final class"))
        self.assertTrue(no_package_type.startswith("/**"))
        self.assertNotIn("package ", no_package_type)
        self.assertLess(no_package_type.index("/**"), no_package_type.index("public final class"))
        self.assertTrue(duplicate.startswith("/* "))
        self.assertIn("\n/**", duplicate)
        for field in ("copyright", "AI attribution", "responsibility", "design", "test-plan"):
            with self.subTest(duplicate_field=field):
                self.assertEqual(2, duplicate.lower().count(field.lower()))
        for phrase in (
            "valid Javadoc",
            "package documentation or first top-level type",
            "duplicate standalone header",
            "required generic information",
        ):
            with self.subTest(java_checklist_phrase=phrase):
                self.assertIn(phrase, java_checklist)

        detection = load_yaml_object(java_root / "detection.yaml")
        self.assertEqual("java-comment", detection["skill"])
        self.assertEqual(
            {"anyOf": [{"fileExtension": ".java"}]},
            detection["activation"],
        )
        self.assertEqual([], detection["companions"])
        self.assertEqual("additive", detection["selection"])

        probes = load_yaml_object(REPOSITORY_ROOT / "evals" / "skill-probes.yaml")
        probe = next(
            entry for entry in probes["probes"] if entry["id"] == "probe-java-comment"
        )
        self.assertIn("package-info.java", probe["activationCondition"])
        self.assertIn("duplicate standalone header", probe["negativeCondition"])
        self.assertIn("required generic fields", probe["expectedBehavior"])
        self.assertEqual(["java-comment-placement"], probe["executableCases"])

        cases = load_yaml_object(REPOSITORY_ROOT / "evals" / "cases.yaml")["cases"]
        java_case = next(case for case in cases if case["id"] == "java-comment-placement")
        self.assertEqual("evals/projects/java-comment-placement", java_case["project"])
        self.assertEqual("python3 verify.py", java_case["verify"])
        self.assertEqual(["src", "eval-result.md"], java_case["allowedWritePaths"])
        self.assertIn("negative-fixtures", java_case["protectedPaths"])
        self.assertIn("negative-fixtures", java_case["contextPack"]["include"])
        self.assertIn("java-comment", java_case["requiredSkills"])
        self.assertIn("probe-java-comment", java_case["skillProbes"])
        self.assertIn("probe-java-comment", java_case["fixtureBackedProbeClaims"])
        self.assertIn("java-comment", java_case["contextPack"]["stagedSkillPackages"])
        self.assertEqual(
            ["SKILL.md", "references/review-checklist-java-comment.md"],
            java_case["skillResourceAllowlist"]["java-comment"],
        )

        fixture_root = REPOSITORY_ROOT / java_case["project"]
        verify_path = fixture_root / "verify.py"
        spec = importlib.util.spec_from_file_location("java_comment_fixture_verify", verify_path)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        verifier = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(verifier)

        golden_root = fixture_root / "negative-fixtures" / "golden"
        goldens = {
            "package-info.java": golden_root / "package-info.java",
            "OrderService.java": golden_root / "OrderService.java",
            "OrderImport.java": golden_root / "OrderImport.java",
        }
        for filename, golden in goldens.items():
            with self.subTest(golden=filename):
                self.assertEqual([], verifier.validate_java(golden, golden))

        service_golden = goldens["OrderService.java"]
        service_text = service_golden.read_text(encoding="utf-8")
        mutations = {
            "blank_value": (
                service_text.replace(
                    "Responsibility: Coordinates validated order submission for application callers.",
                    "Responsibility:",
                ),
                "Responsibility value is blank",
            ),
            "changed_value": (
                service_text.replace("Design: TASK.md", "Design: changed-design.md"),
                "Design value differs from protected golden",
            ),
            "removed_public_prose": (
                service_text.replace(" * Accepts valid orders from application callers.\n", ""),
                "public documentation differs from protected golden",
            ),
        }
        with tempfile.TemporaryDirectory() as directory:
            mutation_root = Path(directory)
            for name, (content, expected_error) in mutations.items():
                candidate = mutation_root / f"{name}.java"
                candidate.write_text(content, encoding="utf-8")
                with self.subTest(invalid=name):
                    errors = verifier.validate_java(candidate, service_golden)
                    self.assertTrue(any(expected_error in error for error in errors), errors)

            attached_javadoc = verifier.attached_javadoc(service_text, service_golden)
            metadata_only = attached_javadoc.replace(
                " * Accepts valid orders from application callers.\n",
                "",
            )
            public_only = "/**\n * Accepts valid orders from application callers.\n */"
            detached = service_text.replace(
                attached_javadoc,
                metadata_only + "\n" + public_only,
            )
            detached_path = mutation_root / "DetachedJavadocs.java"
            detached_path.write_text(detached, encoding="utf-8")
            detached_errors = verifier.validate_java(detached_path, service_golden)
            self.assertTrue(
                any("metadata-bearing Javadoc is not attached" in error for error in detached_errors),
                detached_errors,
            )

        duplicate_errors = verifier.validate_java(
            fixture_root / "negative-fixtures" / "duplicate" / "DuplicateHeader.java",
            service_golden,
        )
        missing_errors = verifier.validate_java(
            fixture_root / "negative-fixtures" / "missing" / "MissingInformation.java",
            goldens["OrderImport.java"],
        )
        self.assertTrue(any("standalone metadata" in error for error in duplicate_errors))
        self.assertTrue(any("duplicate required metadata" in error for error in duplicate_errors))
        self.assertTrue(any("Test plan is missing" in error for error in missing_errors))

        task_text = (fixture_root / "TASK.md").read_text(encoding="utf-8")
        self.assertIn(
            "Affected path: <non-empty repository-relative path>",
            task_text,
        )
        self.assertIn("Verification result: <non-empty result>", task_text)
        self.assertIn("exactly one of each field", task_text)
        self.assertIn("HTML is allowed in verification-result content", task_text)
        self.assertIn("does not interpret HTML", task_text)

        complete_evidence = "\n\n".join(
            (
                f"## {heading}\n"
                f"Affected path: evidence/{heading.lower()}.md\n"
                "Verification result: PASS - verified by the focused fixture."
            )
            for heading in verifier.REQUIRED_EVIDENCE_HEADINGS
        )
        self.assertEqual([], verifier.validate_evidence(complete_evidence))
        html_evidence = complete_evidence.replace(
            "Verification result: PASS - verified by the focused fixture.",
            "Verification result: <details><summary>PASS</summary><p>Verified.</p></details>",
            1,
        )
        self.assertEqual([], verifier.validate_evidence(html_evidence))
        html_wrapped_evidence = "<section>\n" + complete_evidence + "\n</section>"
        self.assertEqual([], verifier.validate_evidence(html_wrapped_evidence))
        evidence_with_fenced_example = (
            "```markdown\n"
            "## JAVA-COMMENT-PACKAGE\n"
            "Affected path: ignored/example.java\n"
            "Verification result: ignored example\n"
            "```\n\n"
            + complete_evidence
        )
        self.assertEqual([], verifier.validate_evidence(evidence_with_fenced_example))

        evidence_contract_cases = {
            "bare_labels": (
                "\n".join(verifier.REQUIRED_EVIDENCE_HEADINGS),
                "missing required Markdown heading: JAVA-COMMENT-PACKAGE",
            ),
            "headings_only": (
                "\n\n".join(f"## {heading}" for heading in verifier.REQUIRED_EVIDENCE_HEADINGS),
                "JAVA-COMMENT-PACKAGE: missing Affected path field",
            ),
            "blank_affected_path": (
                complete_evidence.replace(
                    "Affected path: evidence/java-comment-package.md",
                    "Affected path:",
                    1,
                ),
                "JAVA-COMMENT-PACKAGE: Affected path value is blank",
            ),
            "blank_verification_result": (
                complete_evidence.replace(
                    "Verification result: PASS - verified by the focused fixture.",
                    "Verification result:",
                    1,
                ),
                "JAVA-COMMENT-PACKAGE: Verification result value is blank",
            ),
            "malformed_affected_path_label": (
                complete_evidence.replace(
                    "Affected path: evidence/java-comment-package.md",
                    "Affected paths: evidence/java-comment-package.md",
                    1,
                ),
                "JAVA-COMMENT-PACKAGE: missing Affected path field",
            ),
            "malformed_verification_result_separator": (
                complete_evidence.replace(
                    "Verification result: PASS - verified by the focused fixture.",
                    "Verification result PASS - verified by the focused fixture.",
                    1,
                ),
                "JAVA-COMMENT-PACKAGE: missing Verification result field",
            ),
            "duplicate_affected_path": (
                complete_evidence.replace(
                    "Affected path: evidence/java-comment-package.md",
                    "Affected path: evidence/java-comment-package.md\n"
                    "Affected path: evidence/duplicate.md",
                    1,
                ),
                "JAVA-COMMENT-PACKAGE: duplicate Affected path field",
            ),
            "duplicate_verification_result": (
                complete_evidence.replace(
                    "Verification result: PASS - verified by the focused fixture.",
                    "Verification result: PASS - verified by the focused fixture.\n"
                    "Verification result: duplicate",
                    1,
                ),
                "JAVA-COMMENT-PACKAGE: duplicate Verification result field",
            ),
            "duplicate_heading": (
                complete_evidence
                + "\n\n## REVIEW-SYNTHESIS\n"
                + "Affected path: duplicate.md\nVerification result: PASS",
                "duplicate required Markdown heading: REVIEW-SYNTHESIS",
            ),
            "malformed_heading": (
                complete_evidence.replace(
                    "## JAVA-COMMENT-PACKAGE",
                    "## JAVA-COMMENT-PACKAGE#",
                    1,
                ),
                "missing required Markdown heading: JAVA-COMMENT-PACKAGE",
            ),
            "fenced_pseudo_headings": (
                "```markdown\n" + complete_evidence + "\n```",
                "missing required Markdown heading: JAVA-COMMENT-PACKAGE",
            ),
            "windows_absolute_path": (
                complete_evidence.replace(
                    "evidence/java-comment-package.md",
                    r"C:\outside\result.md",
                    1,
                ),
                "JAVA-COMMENT-PACKAGE: Affected path must be repository-relative",
            ),
            "uri_path": (
                complete_evidence.replace(
                    "evidence/java-comment-package.md",
                    "https://example.test/result.md",
                    1,
                ),
                "JAVA-COMMENT-PACKAGE: Affected path must be repository-relative",
            ),
            "html_affected_path": (
                complete_evidence.replace(
                    "evidence/java-comment-package.md",
                    "<span>evidence/java-comment-package.md</span>",
                    1,
                ),
                "JAVA-COMMENT-PACKAGE: Affected path must be repository-relative",
            ),
            "nul_affected_path": (
                complete_evidence.replace(
                    "evidence/java-comment-package.md",
                    "evidence/\x00result.md",
                    1,
                ),
                "JAVA-COMMENT-PACKAGE: Affected path must be repository-relative",
            ),
        }
        for name, (content, expected_error) in evidence_contract_cases.items():
            with self.subTest(invalid_evidence=name):
                self.assertIn(expected_error, verifier.validate_evidence(content))

        initial_verify = subprocess.run(
            [sys.executable, str(verify_path)],
            cwd=fixture_root,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(0, initial_verify.returncode)
        self.assertIn("source verification failed", initial_verify.stdout + initial_verify.stderr)

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

    def test_planned_hld_and_module_creation_contracts(self) -> None:
        cases = {
            "create-high-level-design": {
                "template": "high-level-design-template.md",
                "sections": (
                    "## Requirements Coverage",
                    "## Critical Trust And Identity Boundaries",
                    "## Cross-Module Contract Reconciliation",
                    "## Implementation Readiness",
                ),
                "phrases": (
                    "producer-consumer boundary",
                    "actor and authentication source",
                    "authorization, ownership, tenancy, and data filtering",
                    "selector and mismatch behavior",
                    "payload and response disclosure",
                    "validation owner",
                    "state owner and transition",
                    "transaction or asynchronous boundary",
                    "error timing",
                    "installed documentation path",
                    "transient assembly or control files",
                    "source-category inventory",
                    "operation-and-obligation inventory",
                    "boundary-edge inventory",
                    "configuration, default, lifetime",
                    "accepted exact validation commands",
                    "exact method, route, command, event, or job identity",
                    "abstract operation group",
                    "exact route variant or supporting UI action",
                    "anonymous, authenticated, administrator, service, or background actor",
                ),
            },
            "create-module-design": {
                "template": "module-design-template.md",
                "sections": (
                    "## Requirements Coverage",
                    "## Trust And Identity Boundaries",
                    "## External And Asynchronous Effect Phases",
                    "## Implementation Readiness",
                ),
                "phrases": (
                    "route, event, command, job, UI guard",
                    "identity selector and mismatch behavior",
                    "validation owner",
                    "response and disclosure shape",
                    "state owner and transition",
                    "transaction or asynchronous boundary",
                    "failure timing",
                    "sensitive-data handling",
                    "operation-contract ledger",
                    "scope-bearing qualifier",
                    "exact level of specificity",
                    "Preserve partial specificity",
                    "exact operation identity",
                    "field-level input constraints",
                    "sensitive inputs",
                    "submission owner",
                    "operation uses it",
                    "compatible accepted inputs",
                    "list or query operations",
                    "phase ledger",
                    "invent a provider-delivery phase",
                    "unsupported transaction or construction mechanism",
                    "security outcome separate from its implementation mechanism",
                    "public projection",
                    "do not prove anonymous access",
                    "returned or emitted value",
                    "fallback emission",
                    "cache replacement or retention",
                    "level-two heading",
                    "Preserve the heading text and order exactly",
                    "executor acceptance or rejection before any work",
                    "Do not merge executor rejection",
                    "first nonblank content under Implementation Readiness",
                    "installed documentation path",
                    "transient assembly or control files",
                    "source-category inventory",
                    "owning-HLD open question",
                ),
            },
        }

        for skill_name, case in cases.items():
            with self.subTest(skill_name=skill_name):
                skill_text = (SKILLS_ROOT / skill_name / "SKILL.md").read_text(
                    encoding="utf-8"
                )
                template_text = (
                    SKILLS_ROOT
                    / "development-methodology"
                    / "assets"
                    / "templates"
                    / case["template"]
                ).read_text(encoding="utf-8")

                for phrase in (
                    "PLANNED_DEVELOPMENT",
                    "EXISTING_IMPLEMENTATION",
                    "MIXED_CHANGE",
                    "authoritative input set",
                    "source-precedence rule",
                    "Requirements Coverage",
                    "DEFINED, OPEN, or OUT_OF_SCOPE",
                    "blocking open question",
                    "CURRENT_BEHAVIOR",
                    "CURRENT_LIMITATION",
                    "PROPOSED_CHANGE",
                    "specific operation",
                ) + case["phrases"]:
                    self.assertIn(phrase, skill_text)

                for evaluation_phrase in (
                    "target reference artifact",
                    "hidden comparison material",
                    "evaluator rubric",
                ):
                    self.assertNotIn(evaluation_phrase, skill_text)

                for section in case["sections"]:
                    self.assertEqual(1, template_text.count(section))

                for phrase in (
                    "Out-of-scope authority, rationale, and owning artifact",
                    "required for OUT_OF_SCOPE",
                    "every applicable requirement",
                    "affected downstream work",
                    "Do not collapse the baseline and target",
                    "operation-specific",
                ) + (
                    (
                        "body identity",
                        "safer intended target separately",
                        "entity-shaped response",
                        "exact method and route",
                        "write-only contract",
                        "suggestive type name",
                        "submission rejection",
                        "different facets of the same exact operation",
                        "deterministic ordering",
                        "State already committed",
                        "Completion evidence",
                        "Do not invent a provider-delivery phase",
                        "authenticated-only or role-required outcome",
                        "similar label as anonymous-access evidence",
                        "shared cache is created, replaced, retained, or invalidated",
                        "failed cached source remains retained or is replaced",
                        "place executor acceptance or rejection before every executor-owned action",
                        "Begin this section with **READY.** or **BLOCKED.**",
                    )
                    if skill_name == "create-module-design"
                    else ()
                ):
                    self.assertIn(phrase, template_text)

        module_template = (
            SKILLS_ROOT
            / "development-methodology"
            / "assets"
            / "templates"
            / "module-design-template.md"
        ).read_text(encoding="utf-8")
        for phrase in (
            "path, body, token, session, message, or persistence identifiers",
            "synchronous and asynchronous failure behavior",
            "which side effects have already committed",
            "Sensitive data and logging",
        ):
            self.assertIn(phrase, module_template)

    def test_forward_document_design_prevents_downstream_coordination_chaos(self) -> None:
        """Planned document levels must close resolvable gaps for their consumers."""
        cases = {
            "functional-spec": {
                "create": "create-functional-spec",
                "review": "review-functional-spec",
                "checklist": "review-checklist-functional-spec.md",
                "create_phrases": (
                    "avoid chaos in architecture and design",
                    "justified functional proposition",
                    "basis, why it is necessary",
                    "stable operation identity",
                    "Unicode ellipsis",
                ),
                "review_phrases": (
                    "prevents chaos in architecture and design",
                    "justified functional propositions",
                    "Avoidable open questions",
                ),
                "checklist_phrases": (
                    "one coherent actor-visible contract",
                    "role that owns or may revise it",
                    "catch-all wording",
                ),
            },
            "architecture": {
                "create": "create-architecture",
                "review": "review-architecture",
                "checklist": "review-checklist-architecture.md",
                "create_phrases": (
                    "avoid chaos in high-level designs",
                    "justified architecture proposition",
                    "system-frame ledger",
                    "complete repository-relative paths",
                    "Unicode ellipsis",
                ),
                "review_phrases": (
                    "prevents chaos in high-level designs",
                    "justified propositions",
                    "incomplete paths",
                ),
                "checklist_phrases": (
                    "one coherent system frame",
                    "system-frame ledger",
                    "complete repository-relative",
                ),
            },
            "high-level-design": {
                "create": "create-high-level-design",
                "review": "review-high-level-design",
                "checklist": "review-checklist-high-level-design.md",
                "create_phrases": (
                    "avoid chaos at the next level of detail",
                    "Precise artifact placement",
                    "artifact-placement ledger",
                    "complete package or module name",
                    "Unicode ellipsis",
                ),
                "review_phrases": (
                    "prevents chaos at the next level of detail",
                    "justified HLD proposition",
                    "precise artifact placement",
                ),
                "checklist_phrases": (
                    "one consistent coordination frame",
                    "artifact-placement ledger",
                    "without interpretation",
                ),
            },
            "module-design": {
                "create": "create-module-design",
                "review": "review-module-design",
                "checklist": "review-checklist-module-design.md",
                "create_phrases": (
                    "avoid chaos in implementation",
                    "justified module proposition",
                    "implementation-placement and symbol ledger",
                    "complete package or module names",
                    "Unicode ellipsis",
                ),
                "review_phrases": (
                    "prevents chaos in implementation",
                    "justified module propositions",
                    "incomplete signatures",
                ),
                "checklist_phrases": (
                    "one directly usable frame",
                    "implementation-placement and symbol ledger",
                    "method signatures",
                ),
            },
        }

        for level, case in cases.items():
            with self.subTest(level=level):
                create_text = (SKILLS_ROOT / case["create"] / "SKILL.md").read_text(
                    encoding="utf-8"
                )
                review_text = (SKILLS_ROOT / case["review"] / "SKILL.md").read_text(
                    encoding="utf-8"
                )
                checklist_text = (
                    SKILLS_ROOT
                    / case["review"]
                    / "references"
                    / case["checklist"]
                ).read_text(encoding="utf-8")

                for phrase in case["create_phrases"]:
                    self.assertIn(phrase, create_text)
                for phrase in case["review_phrases"]:
                    self.assertIn(phrase, review_text)
                for phrase in case["checklist_phrases"]:
                    self.assertIn(phrase, checklist_text)

        module_create = (SKILLS_ROOT / "create-module-design" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("Do not invent paths.", module_create)

    def test_hld_ordered_action_sequences_require_diagrams(self) -> None:
        """Keep lifecycle and delivery sequences out of dense prose-only blocks."""
        create_text = (SKILLS_ROOT / "create-high-level-design" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        template_text = (
            SKILLS_ROOT
            / "development-methodology"
            / "assets"
            / "templates"
            / "high-level-design-template.md"
        ).read_text(encoding="utf-8")
        review_text = (SKILLS_ROOT / "review-high-level-design" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        checklist_text = (
            SKILLS_ROOT
            / "review-high-level-design"
            / "references"
            / "review-checklist-high-level-design.md"
        ).read_text(encoding="utf-8")

        for phrase in (
            "Use a Mermaid diagram whenever a section describes an ordered sequence",
            "must not carry the complete sequence alone",
            "no lifecycle or implementation sequence remains a dense text blob",
        ):
            self.assertIn(phrase, create_text)

        for phrase in (
            "Add a Mermaid Lifecycle Diagram whenever this section describes an ordered sequence",
            "Do not leave the complete sequence only in prose or a table",
            "Add a Mermaid Implementation Sequence Diagram whenever this section describes ordered or dependent implementation actions",
            "Do not leave the complete sequence only in a numbered list, prose, or a table",
        ):
            self.assertIn(phrase, template_text)

        for phrase in (
            "Require an appropriate Mermaid diagram whenever the HLD describes an ordered sequence",
            "a complete sequence carried only by prose, a numbered list, or a table",
        ):
            self.assertIn(phrase, review_text)

        for phrase in (
            "does it include an appropriate Mermaid sequence, state, or flow diagram",
            "an ordered action sequence left only in prose, a numbered list, or a table",
        ):
            self.assertIn(phrase, checklist_text)

    def test_objective_diagram_and_repository_path_tree_contracts(self) -> None:
        """Keep objective diagram and path-tree rules aligned across the bundle."""

        def skill_text(skill_name: str) -> str:
            return (SKILLS_ROOT / skill_name / "SKILL.md").read_text(encoding="utf-8")

        def template_text(template_name: str) -> str:
            return (
                SKILLS_ROOT
                / "development-methodology"
                / "assets"
                / "templates"
                / template_name
            ).read_text(encoding="utf-8")

        def checklist_text(skill_name: str, checklist_name: str) -> str:
            return (
                SKILLS_ROOT / skill_name / "references" / checklist_name
            ).read_text(encoding="utf-8")

        development_text = skill_text("development-methodology")
        architecture_create = skill_text("create-architecture")
        functional_create = skill_text("create-functional-spec")
        hld_create = skill_text("create-high-level-design")
        module_create = skill_text("create-module-design")
        architecture_review = skill_text("review-architecture")
        functional_review = skill_text("review-functional-spec")
        hld_review = skill_text("review-high-level-design")
        module_review = skill_text("review-module-design")

        templates = {
            name: template_text(name)
            for name in (
                "architecture-template.md",
                "functional-spec-template.md",
                "high-level-design-template.md",
                "module-design-template.md",
                "project-template.yaml",
                "project-wiki-template.md",
                "unit-test-plan-template.md",
            )
        }
        checklists = {
            "architecture": checklist_text(
                "review-architecture", "review-checklist-architecture.md"
            ),
            "functional-spec": checklist_text(
                "review-functional-spec", "review-checklist-functional-spec.md"
            ),
            "high-level-design": checklist_text(
                "review-high-level-design", "review-checklist-high-level-design.md"
            ),
            "module-design": checklist_text(
                "review-module-design", "review-checklist-module-design.md"
            ),
            "project-wiki": checklist_text(
                "project-wiki-review", "review-checklist-project-wiki.md"
            ),
            "unit-test-plan": checklist_text(
                "review-unit-test-plan", "review-checklist-unit-test-plan.md"
            ),
        }

        ordered_trigger_surfaces = (
            development_text,
            architecture_create,
            functional_create,
            module_create,
            templates["architecture-template.md"],
            templates["functional-spec-template.md"],
            templates["module-design-template.md"],
            templates["project-wiki-template.md"],
            checklists["architecture"],
            checklists["functional-spec"],
            checklists["module-design"],
            checklists["project-wiki"],
        )
        for text in ordered_trigger_surfaces:
            self.assertIn("two or more ordered", text)
            self.assertRegex(text, r"two or more ordered[^.]+, or any")

        for trigger in ("handoff", "branch", "retry", "recovery path", "state transition"):
            with self.subTest(independent_diagram_trigger=trigger):
                self.assertIn(trigger, development_text)
                self.assertIn(trigger, templates["project-wiki-template.md"])
                self.assertIn(trigger, checklists["project-wiki"])

        structural_surfaces = (
            development_text,
            architecture_create,
            hld_create,
            templates["architecture-template.md"],
            templates["high-level-design-template.md"],
            templates["module-design-template.md"],
            templates["project-wiki-template.md"],
            checklists["architecture"],
            checklists["high-level-design"],
            checklists["module-design"],
            checklists["project-wiki"],
        )
        for text in structural_surfaces:
            self.assertIn("connects to two or more", text)
            self.assertIn("spans three or more nodes", text)
            self.assertIn("cycle exists", text)
            self.assertIn("containment spans two or more levels", text)

        module_diagram_surfaces = (
            module_create,
            module_review,
            templates["module-design-template.md"],
            checklists["module-design"],
        )
        for text in module_diagram_surfaces:
            self.assertIn("one-row synchronous effect", text)
            self.assertIn("external handoff", text)
            self.assertRegex(text, r"only when[^.]+no branch, retry, error path")

        for text in templates.values():
            self.assertIn("Path tree example", text)
            self.assertIn("tree", text)
        for phrase in (
            "three or more repository paths",
            "fenced text tree",
            "complete repository-relative root segments",
            "split it into named subsections by component or ownership area",
            "metadata immediately after the tree",
            "Markdown table cells",
            "common prefix",
            "one table row per full path",
            "Machine-readable configuration schemas keep their required path arrays",
        ):
            self.assertIn(phrase, development_text)
        self.assertIn(
            "Keep the schema-required path arrays below machine-readable",
            templates["project-template.yaml"],
        )

        for name, text in checklists.items():
            with self.subTest(path_tree_checklist=name):
                for phrase in (
                    "three or more repository paths that share a prefix",
                    "fenced text trees",
                    "complete repository-relative",
                    "named component or ownership subsections",
                    "adjacent metadata",
                    "multiline table cells",
                    "simulated HTML breaks",
                    "repeated common-prefix lists",
                    "one row per full path",
                    "a missing or malformed required path tree",
                    "duplicated full paths or common prefixes",
                ):
                    self.assertIn(phrase, text)

        for text in (
            architecture_create,
            functional_create,
            hld_create,
            module_create,
        ):
            self.assertIn("intentionally created later", text)
            self.assertIn("current reverse-engineering pass", text)

        self.assertIn("dependent implementation steps", hld_create)
        self.assertIn(
            "ordered or dependent implementation actions or verification gates",
            templates["high-level-design-template.md"],
        )
        self.assertIn("ordered sequence", hld_review)
        self.assertIn("dependent implementation steps", checklists["high-level-design"])
        self.assertIn("missing required structural diagram", checklists["high-level-design"])
        self.assertIn("missing required context or structural diagram", checklists["module-design"])
        self.assertIn("missing required structural diagram", checklists["project-wiki"])
        self.assertIn("qualifying workflow", functional_review)
        self.assertIn("qualifying ordered or structural relationship", architecture_review)

        def line_containing(text: str, marker: str) -> str:
            for line in text.splitlines():
                if marker.lower() in line.lower():
                    return line
            self.fail(f"Expected a contract line containing {marker!r}")

        architecture_diagram_surfaces = {
            "create skill": architecture_create,
            "review skill": architecture_review,
            "template": templates["architecture-template.md"],
            "checklist": checklists["architecture"],
        }
        architecture_ordered_triggers = (
            "two or more ordered actions or phases",
            "handoff",
            "data movement",
            "lifecycle transition",
            "branch",
            "retry",
            "recovery path",
            "startup or shutdown dependency",
            "dependent implementation phase",
        )
        for name, text in architecture_diagram_surfaces.items():
            with self.subTest(architecture_ordered_surface=name):
                ordered_rule = line_containing(
                    text, "two or more ordered actions or phases"
                )
                for trigger in architecture_ordered_triggers:
                    self.assertIn(trigger, ordered_rule)
                self.assertIn("diagram", ordered_rule)
                for supporting_form in ("prose", "numbered list", "table"):
                    self.assertIn(supporting_form, ordered_rule.lower())
                self.assertTrue(
                    "must not carry" in ordered_rule.lower()
                    or "instead of leaving" in ordered_rule.lower()
                )

                additive_rule = line_containing(text, "additive minimum")
                self.assertIn("shared development-methodology rule", additive_rule)
                self.assertRegex(
                    additive_rule,
                    r"does not waive another shared trigger|"
                    r"without using one satisfied section trigger to waive another shared trigger",
                )

        functional_diagram_surfaces = {
            "create skill": (functional_create, "Mermaid workflow diagram whenever"),
            "review skill": (functional_review, "Mermaid diagram whenever"),
            "template": (
                templates["functional-spec-template.md"],
                "Mermaid diagram whenever",
            ),
            "checklist": (
                checklists["functional-spec"],
                "appropriate Mermaid sequence, state, or flow diagram",
            ),
        }
        functional_ordered_triggers = (
            "two or more ordered actor actions",
            "branch",
            "permission gate",
            "alternate path",
            "recovery path",
            "state transition",
            "external handoff",
        )
        for name, (text, marker) in functional_diagram_surfaces.items():
            with self.subTest(functional_ordered_surface=name):
                ordered_rule = line_containing(text, marker)
                for trigger in functional_ordered_triggers:
                    self.assertIn(trigger, ordered_rule)
                self.assertIn("Mermaid", ordered_rule)
                for supporting_form in ("prose", "numbered list", "table"):
                    self.assertIn(supporting_form, ordered_rule.lower())
                verification_exception = line_containing(
                    text, "Verification-step lists"
                )
                self.assertIn("test procedures", verification_exception)
                self.assertIn("trigger", verification_exception)

        module_diagram_surfaces = {
            "create skill": module_create,
            "review skill": module_review,
            "template": templates["module-design-template.md"],
            "checklist": checklists["module-design"],
        }
        module_exception_disqualifiers = (
            "branch",
            "retry",
            "error path",
            "state transition",
            "external handoff",
            "asynchronous phase transition",
        )
        for name, text in module_diagram_surfaces.items():
            with self.subTest(module_exception_surface=name):
                exception_rule = line_containing(text, "one-row synchronous effect")
                self.assertRegex(exception_rule, r"exception|exempting|may omit|omission")
                self.assertRegex(exception_rule, r"only when.*\bno\b")
                for trigger in module_exception_disqualifiers:
                    self.assertIn(trigger, exception_rule)

        path_tree_template_contracts = {
            "architecture-template.md": {
                "trigger": "repository placement of source code, tests, design documents",
                "complete": "complete repository-relative paths",
                "split": "named subsections by runtime unit or ownership area",
                "metadata": "metadata immediately after the tree",
                "deduplicate": (
                    "Do not repeat shared prefixes",
                    "do not repeat every full path",
                ),
            },
            "functional-spec-template.md": {
                "trigger": "three or more related paths share a prefix, or span two or more folders",
                "complete": "complete project paths",
                "split": "named subsections by surface",
                "metadata": "metadata immediately after the tree",
                "deduplicate": (
                    "share a prefix",
                    "instead of repeating full paths",
                ),
            },
            "high-level-design-template.md": {
                "trigger": "three or more paths share a prefix or span two or more folders",
                "complete": "complete planned or existing layout",
                "split": "named subsections by component or ownership area",
                "metadata": "metadata immediately after the tree",
                "deduplicate": (
                    "do not repeat the same prefixes",
                    "do not restate full paths in every row",
                ),
            },
            "module-design-template.md": {
                "trigger": "three or more paths share a prefix or span two or more folders",
                "complete": "complete repository-relative folders and package segments",
                "split": "named subsections by ownership area",
                "metadata": "metadata immediately after the tree",
                "deduplicate": (
                    "do not abbreviate or repeat them in a long list",
                    "do not repeat the full path in each row",
                ),
            },
            "project-wiki-template.md": {
                "trigger": "three or more paths share a prefix or span two or more folders",
                "complete": "complete wiki layout",
                "split": "named subsections by topic family",
                "metadata": "metadata immediately after the tree",
                "deduplicate": (
                    "Do not repeat the docs/wiki prefix",
                    "instead of repeating full paths",
                ),
            },
            "unit-test-plan-template.md": {
                "trigger": "three or more implementation, test, fixture, snapshot, or configuration paths share a prefix or span two or more folders",
                "complete": "complete project paths",
                "split": "named subsections by test group",
                "metadata": "metadata immediately after the tree",
                "deduplicate": (
                    "rather than repeating full paths",
                    "do not repeat the full common prefix for every test",
                ),
            },
            "project-template.yaml": {
                "trigger": "present repeated prefixes once as a tree",
                "complete": "project-root/",
                "split": "named subsections by ownership area",
                "metadata": "nearby metadata",
                "deduplicate": (
                    "present repeated prefixes once",
                    "rather than creating one row per full path",
                ),
            },
        }
        for name, contract in path_tree_template_contracts.items():
            text = templates[name]
            normalized_text = " ".join(text.split())
            contract_text = normalized_text
            if name == "project-template.yaml":
                contract_text = " ".join(
                    line.removeprefix("#").strip()
                    for line in text.splitlines()
                    if line.startswith("#")
                )
            with self.subTest(path_tree_template=name):
                self.assertIn(contract["trigger"], contract_text)
                self.assertIn(contract["complete"], contract_text)
                self.assertIn("Path tree example", contract_text)
                self.assertIn(contract["split"], contract_text)
                self.assertIn(contract["metadata"], contract_text)
                self.assertIn("fenced text tree", contract_text)
                self.assertIn("Markdown table cells", contract_text)
                for deduplication_rule in contract["deduplicate"]:
                    self.assertIn(deduplication_rule, contract_text)
                self.assertNotRegex(text, r"<br\s*/?>")
                if name != "project-template.yaml":
                    self.assertIn("```text", text)
                    self.assertIn("HTML breaks", text)

        project_template = templates["project-template.yaml"]
        self.assertIn("schema-required path arrays below machine-readable", project_template)
        self.assertIn("generated prose", project_template)
        project_config = yaml.safe_load(project_template)
        configured_paths = project_config["project_taxonomy"]["application_tiers"][0][
            "paths"
        ]
        self.assertIsInstance(configured_paths, list)
        self.assertTrue(configured_paths)
        self.assertTrue(
            all(isinstance(path, str) and path for path in configured_paths)
        )

        for name, text in checklists.items():
            questions, findings = text.split("## Findings", maxsplit=1)
            with self.subTest(path_tree_checklist_enforcement=name):
                for phrase in (
                    "three or more repository paths that share a prefix",
                    "paths spanning two or more folders",
                    "fenced text trees",
                    "complete repository-relative",
                    "named component or ownership subsections",
                    "adjacent metadata",
                    "multiline table cells",
                    "simulated HTML breaks",
                    "repeated common-prefix lists",
                    "one row per full path",
                ):
                    self.assertIn(phrase, questions)
                for finding in (
                    "a missing or malformed required path tree",
                    "missing complete repository-relative tree segments",
                    "unsplit large trees",
                    "tree metadata separated from its owning tree",
                    "table-cell or HTML-simulated trees",
                    "duplicated full paths or common prefixes",
                ):
                    self.assertIn(finding, findings)

        hld_ordered_create_rule = line_containing(hld_create, "ordered sequence")
        self.assertIn("dependent implementation steps", hld_ordered_create_rule)
        self.assertIn("complete sequence alone", hld_ordered_create_rule)
        hld_ordered_review_rule = line_containing(hld_review, "ordered sequence")
        self.assertIn("dependent implementation steps", hld_ordered_review_rule)
        self.assertIn("response-adequacy finding", hld_ordered_review_rule)

        hld_template = templates["high-level-design-template.md"]
        implementation_rule = line_containing(
            hld_template, "ordered or dependent implementation actions"
        )
        self.assertIn("verification gates", implementation_rule)
        self.assertIn("complete sequence only", implementation_rule)
        verification_rule = line_containing(
            hld_template, "dependency order and required verification gates"
        )
        self.assertIn("Implementation Sequence Diagram", verification_rule)

        hld_questions, hld_findings = checklists["high-level-design"].split(
            "## Findings", maxsplit=1
        )
        hld_checklist_rule = line_containing(hld_questions, "ordered sequence")
        self.assertIn("dependent implementation steps", hld_checklist_rule)
        self.assertIn("Mermaid sequence, state, or flow diagram", hld_checklist_rule)
        self.assertIn("Does Implementation Order give a credible sequence", hld_questions)
        self.assertIn(
            "an ordered action sequence left only in prose, a numbered list, or a table",
            hld_findings,
        )

    def test_hld_data_anchors_are_actionable_for_downstream_design(self) -> None:
        """Keep HLD anchors concrete, owned, and reusable by later designs."""
        template_text = (
            SKILLS_ROOT
            / "development-methodology"
            / "assets"
            / "templates"
            / "high-level-design-template.md"
        ).read_text(encoding="utf-8")
        checklist_text = (
            SKILLS_ROOT
            / "review-high-level-design"
            / "references"
            / "review-checklist-high-level-design.md"
        ).read_text(encoding="utf-8")

        for phrase in (
            "the next design layer must elaborate without redefining",
            "| Anchor | Anchor type | Authority | Owner and representation | Constraint for the next design layer |",
            "cite the exact accepted artifact plus requirement ID or section",
            "name or link the exact fields or state boundary",
            "identify the downstream consumers that must reuse it",
            "they are not authorities",
            "Split anchors that have different owners or downstream constraints",
            "replace, append, clear, or recompute rules",
            "lifetime, reset, failure-preservation, and persistence restrictions",
        ):
            self.assertIn(phrase, template_text)

        for phrase in (
            "a concrete anchor, its anchor type, its authority, its owner and representation",
            "an exact accepted artifact plus requirement ID or section",
            "a justified HLD proposition with its basis and decision owner",
            "the exact configuration contract and decision authority",
            "the fields or state boundary that must remain consistent",
            "replace, append, clear, reset, recompute, lifetime, or persistence rules",
        ):
            self.assertIn(phrase, checklist_text)

    def test_forward_design_closes_supporting_operation_inventories(self) -> None:
        """Keep supporting APIs from disappearing between functional and design levels."""
        functional_create = (SKILLS_ROOT / "create-functional-spec" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        functional_template = (
            SKILLS_ROOT
            / "development-methodology"
            / "assets"
            / "templates"
            / "functional-spec-template.md"
        ).read_text(encoding="utf-8")
        functional_review = (
            SKILLS_ROOT
            / "review-functional-spec"
            / "references"
            / "review-checklist-functional-spec.md"
        ).read_text(encoding="utf-8")

        for text in (functional_create, functional_template, functional_review):
            for phrase in (
                "primary and supporting operation inventory",
                "supporting reference-data lookup",
                "actor and authentication source",
                "authorization, ownership, tenancy, and data filtering",
                "selector, request, paging, and sort",
                "response projection, disclosure, status, and error",
            ):
                self.assertIn(phrase, text)

        for skill_name, checklist_name in (
            ("review-high-level-design", "review-checklist-high-level-design.md"),
            ("review-module-design", "review-checklist-module-design.md"),
        ):
            skill_text = (SKILLS_ROOT / skill_name / "SKILL.md").read_text(
                encoding="utf-8"
            )
            checklist_text = (
                SKILLS_ROOT / skill_name / "references" / checklist_name
            ).read_text(encoding="utf-8")
            self.assertIn("operation inventory reconciliation", skill_text)
            self.assertIn("operation inventory reconciliation", checklist_text)
            self.assertIn("supporting operation", checklist_text)

        hld_template = (
            SKILLS_ROOT
            / "development-methodology"
            / "assets"
            / "templates"
            / "high-level-design-template.md"
        ).read_text(encoding="utf-8")
        self.assertIn("exact route variant or supporting UI action", hld_template)
        self.assertIn(
            "anonymous, authenticated, administrator, service, or background actor",
            hld_template,
        )

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
        modularization_text = (
            REPOSITORY_ROOT / "design" / "skills-modularization.html"
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
        self.assertIn("agent_claim_transport:", template_text)
        self.assertIn("selected: \"TODO: mcp or command", template_text)
        self.assertIn("Select exactly one agent_claim_transport value", skill_text)
        self.assertIn("inline exactly the selected claim transport adapter", skill_text)
        self.assertIn("workflow_selection:", template_text)
        self.assertIn("project_skill_extensions: []", template_text)
        self.assertIn("file, github, gitlab, azure-devops, jira, none, or UNSET", template_text)
        self.assertIn("direct-main, feature-branch, or UNSET", template_text)
        self.assertIn("simple-workitem to direct-main", skill_text)
        self.assertIn("file-based-backlog to file", skill_text)
        self.assertIn("selected create, manage, and completion skills as references only", skill_text)
        for phrase in (
            "Record project_skill_extensions as one ordered list",
            "registration must be registered",
            "availability must be AVAILABLE",
            "normalized identifier for duplicate",
            "Reject an extension that duplicates any fixed or conditional skill",
            "at the end of root AGENTS.md",
            "Do not copy the section to nested AGENTS.md files",
        ):
            with self.subTest(project_skill_extension_phrase=phrase):
                self.assertIn(phrase, skill_text)
        self.assertIn("record explicit UNSET rather than omitting a deferred decision", skill_text)
        self.assertIn("one exact folder pattern may appear only once", skill_text)
        self.assertIn("one exact folder pattern may appear only once", template_text)
        self.assertNotIn("nested_project_files:", template_text)
        self.assertIn("Create exactly one PROJECT.yaml", skill_text)
        self.assertIn("Do not create nested PROJECT.yaml files", skill_text)
        self.assertIn("intermediate, reviewable intent log", skill_text)
        self.assertIn("treat them as requested configuration intent", skill_text)
        self.assertIn("Project Configurator owns the setup process", modularization_text)
        self.assertIn("Project-level extension selection", modularization_text)
        self.assertIn("project_skill_extensions", modularization_text)
        self.assertIn("Nested guidance does not inherit or repeat the section", modularization_text)
        self.assertIn("edit PROJECT.yaml to force a correction", modularization_text)
        self.assertIn("linked template", examples_text)
        self.assertNotIn("service/PROJECT.yaml", examples_text)
        self.assertNotIn("nested PROJECT.yaml recommendations", modularization_text)
        self.assertNotIn("&lt;subtree&gt;/PROJECT.yaml", modularization_text)
        self.assertIn("claude_bridge_files:", template_text)
        self.assertNotIn("agent_coordination:", template_text)
        self.assertNotIn("coordination_overrides:", template_text)
        self.assertIn(
            "Generic repository-mutation behavior belongs to conceptual agent definitions",
            skill_text,
        )
        self.assertIn(
            "Do not reproduce that procedure in PROJECT.yaml or AGENTS.md",
            skill_text,
        )
        self.assertIn("Record a coordination_overrides mapping only when", skill_text)
        self.assertIn("Keep workflow configuration selector-only", skill_text)
        self.assertIn("Do not infer either selector", skill_text)
        development_methodology_text = (
            SKILLS_ROOT / "development-methodology" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("ordered project-level skill extensions", development_methodology_text)
        readme_text = (REPOSITORY_ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("ordered project_skill_extensions list", readme_text)
        self.assertIn("final root-only section", readme_text)
        self.assertIn(
            "Treat a missing conceptual agent definition, skill, or command as BLOCKED",
            skill_text,
        )
        self.assertIn("agent-claim", skill_text)
        self.assertIn("exact anchored /.worktrees/ entry", skill_text)
        self.assertIn("must never derive it from another linked checkout", skill_text)
        self.assertIn("Do not record a machine-specific absolute worktree path", skill_text)
        self.assertIn(
            "The .worktrees directory is ignored operational state immediately beneath the primary worktree",
            template_text,
        )
        self.assertIn("Contains the anchored /.worktrees/ entry", template_text)
        self.assertIn("worktree ignore behavior", modularization_text)
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

    def test_hld_and_module_reviews_enforce_adequacy_and_security_contracts(self) -> None:
        cases = {
            "review-high-level-design": (
                "review-checklist-high-level-design.md",
                (
                    "## Cross-Module Reconciliation Questions",
                    "producer-consumer boundary",
                    "actor and authentication source",
                    "authorization, role, ownership, tenancy, and data filtering",
                    "selector mismatch behavior",
                    "state owner and transition",
                    "transaction, asynchronous, and error timing",
                ),
            ),
            "review-module-design": (
                "review-checklist-module-design.md",
                (
                    "route, event, command, job, UI guard",
                    "precedence and mismatch behavior",
                    "committed side effects",
                    "sensitive logging behavior",
                ),
            ),
        }

        for skill_name, (checklist_name, specific_phrases) in cases.items():
            with self.subTest(skill_name=skill_name):
                skill_text = (SKILLS_ROOT / skill_name / "SKILL.md").read_text(
                    encoding="utf-8"
                )
                checklist_text = (
                    SKILLS_ROOT / skill_name / "references" / checklist_name
                ).read_text(encoding="utf-8")

                for phrase in (
                    "requirements coverage",
                    "implementation readiness",
                    "response adequacy",
                    "identity and security",
                ):
                    self.assertIn(phrase, skill_text.lower())

                if skill_name == "review-high-level-design":
                    self.assertIn("never qualify a status", skill_text)

                for phrase in (
                    "## Response Adequacy Questions",
                    "## Identity And Security Questions",
                    "every applicable",
                    "DEFINED, OPEN, or OUT_OF_SCOPE",
                    "high-impact blocking question",
                    "authority, rationale, and owning artifact",
                    "affected downstream work",
                    "CURRENT_LIMITATION",
                    "baseline and target stated separately",
                    "operation-specific",
                ) + specific_phrases + (
                    (
                        "exact level of specificity",
                        "operation-contract ledger",
                        "partial specificity",
                        "close synonym",
                        "field-level constraint",
                        "exact method and route",
                        "sensitive inputs",
                        "suggestive name",
                        "submission owner",
                        "durable receipt",
                        "ordered level-two headings",
                        "executor acceptance or rejection occur before every executor-owned action",
                        "sender or provider rejection",
                        "first nonblank content under Implementation Readiness",
                        "scope-bearing qualifier",
                    )
                    if skill_name == "review-module-design"
                    else ()
                ):
                    self.assertIn(phrase, checklist_text)

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

    def test_dev_backlog_steward_requires_claimed_blocked_work_resumption(self) -> None:
        """The suite makes claim-backed resumption and lossless failure observable."""
        suite_root = AGENT_TEST_SUITES_ROOT / "dev-backlog-steward"
        manage_file_text = (
            SKILLS_ROOT / "manage-file-work-items" / "SKILL.md"
        ).read_text(encoding="utf-8")
        legacy_bridge_text = (
            SKILLS_ROOT / "manage-backlog" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertNotIn(
            "## Blocked Handoff And Resumption",
            legacy_bridge_text,
        )
        for required_phrase in (
            "## Blocked Handoff And Resumption",
            "replace the prior owner with Owner: Unowned",
            "replace the prior claim with Claim: None",
            "Set the item to Ready",
            "Only after a successful claim",
            "Restore the byte-for-byte pre-attempt Blocked item",
        ):
            with self.subTest(manage_file_contract=required_phrase):
                self.assertIn(required_phrase, manage_file_text)

        scenarios = load_yaml_object(suite_root / "scenarios.yaml")["scenarios"]
        by_id = {scenario["id"]: scenario for scenario in scenarios}
        for scenario_id in (
            "blocked-state-transition",
            "blocked-unowned-running-shortcut",
            "blocked-claimed-resumption",
            "blocked-failed-claim-resumption",
        ):
            with self.subTest(retargeted_scenario=scenario_id):
                target_skills = by_id[scenario_id]["targetSkills"]
                self.assertIn("manage-file-work-items", target_skills)
                self.assertNotIn("manage-backlog", target_skills)

        known_checks = {
            check["id"]
            for check in load_yaml_object(REPOSITORY_ROOT / "evals" / "judges.yaml")[
                "checks"
            ]
        }
        for scenario in scenarios:
            with self.subTest(scenario_checks=scenario["id"]):
                self.assertLessEqual(set(scenario["deterministicChecks"]), known_checks)

        blocked_handoff_checks = by_id["blocked-state-transition"][
            "deterministicChecks"
        ]
        self.assertIn("queue-state-transition", blocked_handoff_checks)
        self.assertNotIn("test-state-transition", blocked_handoff_checks)

        self.assertEqual(
            "BLOCKED",
            by_id["blocked-unowned-running-shortcut"]["expectedTerminalStatus"],
        )
        self.assertEqual(
            "PASS", by_id["blocked-claimed-resumption"]["expectedTerminalStatus"]
        )
        self.assertEqual(
            "BLOCKED",
            by_id["blocked-failed-claim-resumption"]["expectedTerminalStatus"],
        )
        self.assertTrue((suite_root / "contract_harness.py").is_file())
        judge_text = (suite_root / "agents" / "judge.toml").read_text(
            encoding="utf-8"
        )
        self.assertIn("reject direct unowned Blocked to Running", judge_text)
        self.assertIn("byte-for-byte pre-attempt Blocked item", judge_text)

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

    def test_design_pattern_skills_have_dedicated_category(self) -> None:
        category_data = load_yaml_object(SKILL_CATEGORIES_PATH)
        categories = category_data.get("categories")
        self.assertIsInstance(categories, list)
        category_labels = {
            category["id"]: category["label"]
            for category in categories
            if isinstance(category, dict)
            and isinstance(category.get("id"), str)
            and isinstance(category.get("label"), str)
        }
        self.assertEqual(
            "Design pattern skills",
            category_labels.get("design-patterns"),
        )

        grouped_skills = set()
        for skill_path in sorted(SKILLS_ROOT.glob("*/SKILL.md")):
            skill_text = skill_path.read_text(encoding="utf-8")
            frontmatter = yaml.safe_load(skill_text.split("---", maxsplit=2)[1])
            if frontmatter.get("metadata", {}).get("category") == "design-patterns":
                grouped_skills.add(skill_path.parent.name)

        self.assertEqual(set(CORE_PATTERN_SKILLS), grouped_skills)

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

    def test_project_organiser_retains_filename_selection_authority(self) -> None:
        """Project Organiser adapters retain authority without response-only conflicts."""
        role = load_yaml_object(
            ROLES_ROOT / "project-setup" / "project-organiser.role.yaml"
        )
        role_skill_names = [next(iter(entry)) for entry in role["skills"]]
        role_output_names = [next(iter(entry)) for entry in role["outputContract"]]

        role_outputs = {
            next(iter(entry)): next(iter(entry.values()))
            for entry in role["outputContract"]
        }

        self.assertIn("organise-project-files", role_skill_names)
        decision_output_name = "approved path or placement blocker"
        self.assertIn(decision_output_name, role_output_names)
        self.assertNotIn("approved path", role_output_names)
        self.assertNotIn("placement blocker", role_output_names)
        self.assertIn("placement rationale", role_output_names)
        self.assertIn("file-placement audit", role_output_names)

        approved_path_instruction = (
            "When a path can be approved, return the selected path, rationale, and "
            "placement audit."
        )
        blocked_path_instruction = (
            "When no path can be approved, omit the approved path and return the "
            "explicit six-facet classification, exact blocker, rationale, and "
            "placement audit."
        )
        self.assertIn(approved_path_instruction, role["instructions"])
        self.assertIn(blocked_path_instruction, role["instructions"])
        self.assertIn(
            "Successful decisions return an approved path",
            role_outputs[decision_output_name]["purpose"],
        )
        self.assertIn(
            "blocked decisions omit it and return the exact blocker",
            role_outputs[decision_output_name]["purpose"],
        )

        classification_labels = (
            "Purpose:",
            "Owner:",
            "Lifecycle:",
            "Consumers:",
            "Mutability:",
            "Artifact kind:",
        )
        for example in role["examples"]:
            with self.subTest(example=example["purpose"]):
                for label in classification_labels:
                    self.assertIn(label, example["plausibleResponse"])

        example_responses = [
            example["plausibleResponse"] for example in role["examples"]
        ]
        successful_example_indexes = {
            index
            for index, response in enumerate(example_responses)
            if "Approved path:" in response
        }
        blocked_example_indexes = {
            index
            for index, response in enumerate(example_responses)
            if "Status: BLOCKED" in response
        }
        self.assertEqual(2, len(example_responses))
        self.assertEqual({0}, successful_example_indexes)
        self.assertEqual({1}, blocked_example_indexes)
        self.assertTrue(
            successful_example_indexes.isdisjoint(blocked_example_indexes)
        )
        self.assertEqual(
            set(range(len(example_responses))),
            successful_example_indexes | blocked_example_indexes,
        )

        successful_response = example_responses[0]
        successful_required_markers = (
            "Approved path:",
            "Rationale:",
            "Placement audit:",
        )
        structured_field_prefix = (
            r"(?:\A|[\r\n]+\s*|(?<=[.!?;])\s+)(?:[-*+]\s+)?"
        )
        standalone_marker_suffix = r"(?=\s*(?:[.!;](?:\s|$)|$))"
        chosen_path_label_pattern = (
            r"(?:(?:approved|selected|chosen)[\s-]+"
            r"(?:path|destination)|destination)"
        )
        recognized_structured_field_pattern = (
            rf"(?:purpose|owner|lifecycle|consumers|mutability|"
            rf"artifact[\s-]+kind|{chosen_path_label_pattern}|blocker|"
            rf"exact[\s-]+decision(?:[\s-]+(?:needed|required))?|"
            rf"rationale|placement[\s-]+audit|status)"
        )
        omission_value_pattern = (
            r"(?:omitted|absent|unavailable|none|n/a|not[\s-]+"
            r"(?:applicable|approved|selected|provided))"
        )
        complete_field_boundary_pattern = (
            r"(?=(?:[ \t]*(?:[.;])?[ \t]*(?:[\r\n]|$)|"
            r"(?:[ \t]*[.;][ \t]*|[ \t]+)(?:[-*+][ \t]+)?"
            rf"{recognized_structured_field_pattern}[ \t]*:))"
        )
        complete_omission_pattern = (
            rf"{omission_value_pattern}{complete_field_boundary_pattern}"
        )
        successful_forbidden_marker_patterns = (
            (
                "blocked",
                re.compile(
                    rf"(?:{structured_field_prefix}status\s*:\s*blocked\b|"
                    rf"{structured_field_prefix}blocked"
                    rf"{standalone_marker_suffix})",
                    re.IGNORECASE,
                ),
            ),
            (
                "blocker",
                re.compile(
                    rf"{structured_field_prefix}blocker(?:\s*:|"
                    rf"{standalone_marker_suffix})",
                    re.IGNORECASE,
                ),
            ),
            (
                "exact decision",
                re.compile(
                    rf"{structured_field_prefix}exact[\s-]+decision[\s-]+"
                    rf"(?:needed|required)(?:\s*:|{standalone_marker_suffix})",
                    re.IGNORECASE,
                ),
            ),
            (
                "path omission",
                re.compile(
                    rf"{structured_field_prefix}{chosen_path_label_pattern}"
                    rf"\s*(?::|-)?\s*(?:is\s+)?"
                    rf"{complete_omission_pattern}",
                    re.IGNORECASE,
                ),
            ),
        )

        def forbidden_success_marker_families(response: str) -> tuple[str, ...]:
            return tuple(
                marker_family
                for marker_family, pattern in successful_forbidden_marker_patterns
                if pattern.search(response)
            )

        for marker in successful_required_markers:
            self.assertIn(marker, successful_response)
        self.assertEqual((), forbidden_success_marker_families(successful_response))

        blocked_response = example_responses[1]
        blocked_required_markers = (
            *classification_labels,
            "Blocker:",
            "Exact decision needed:",
            "Rationale:",
            "Placement audit:",
            "Approved path omitted.",
            "Status: BLOCKED",
        )
        selected_path_pattern = re.compile(
            rf"\b{chosen_path_label_pattern}\s*:\s*"
            rf"(?!{complete_omission_pattern})\S",
            re.IGNORECASE,
        )

        for marker in blocked_required_markers:
            self.assertIn(marker, blocked_response)
        self.assertIsNone(selected_path_pattern.search(blocked_response))

        successful_response_mutations = (
            ("bare blocked", "\nBLOCKED"),
            ("exact decision required", "\nExact decision required"),
            (
                "combined blocker markers",
                "\nBLOCKED\nExact decision required",
            ),
            ("case-insensitive blocker", "\nblocker"),
            ("exact decision needed", "\nEXACT DECISION NEEDED"),
            ("approved path omission", "\napproved path: omitted"),
            ("selected-path omission", "\nSelected-path omitted"),
        )
        for mutation, addition in successful_response_mutations:
            with self.subTest(success_mutation=mutation):
                self.assertNotEqual(
                    (),
                    forbidden_success_marker_families(
                        successful_response + addition
                    ),
                )

        structured_success_marker_mutations = (
            ("start bare blocked", f"BLOCKED. {successful_response}"),
            (
                "folded blocker field",
                f"{successful_response} Blocker: unresolved ownership.",
            ),
            (
                "folded blocked status field",
                f"{successful_response} Status: BLOCKED.",
            ),
            (
                "markdown exact-decision field",
                f"{successful_response}\n- Exact decision required",
            ),
            (
                "folded path-omission field",
                f"{successful_response} Selected path omitted.",
            ),
        )
        for mutation, mutated_response in structured_success_marker_mutations:
            with self.subTest(structured_success_mutation=mutation):
                self.assertNotEqual(
                    (),
                    forbidden_success_marker_families(mutated_response),
                )

        benign_success_rationale_additions = (
            ("resolved blocker", " The prior blocker was resolved."),
            (
                "completed exact decision",
                " The exact decision required by the taxonomy has been made.",
            ),
        )
        for rationale, addition in benign_success_rationale_additions:
            with self.subTest(benign_success_rationale=rationale):
                self.assertEqual(
                    (),
                    forbidden_success_marker_families(
                        successful_response + addition
                    ),
                )

        blocked_response_mutations = (
            (
                "approved path",
                "\nApproved path: fixtures/client/compatibility.json",
            ),
            (
                "selected path",
                "\nSelected path: fixtures/client/compatibility.json",
            ),
            (
                "destination",
                "\nDestination: fixtures/client/compatibility.json",
            ),
            (
                "approved destination",
                "\nApproved destination: fixtures/client/compatibility.json",
            ),
            (
                "selected destination",
                "\nSelected destination: fixtures/client/compatibility.json",
            ),
        )
        for mutation, addition in blocked_response_mutations:
            with self.subTest(blocker_mutation=mutation):
                self.assertIsNotNone(
                    selected_path_pattern.search(blocked_response + addition)
                )

        chosen_path_aliases = (
            "Approved path",
            "Selected path",
            "Chosen path",
            "Destination",
            "Approved destination",
            "Selected destination",
            "Chosen destination",
        )
        path_presentations = (
            ("line", "\n"),
            ("folded", " "),
            ("markdown", "\n- "),
        )
        successful_path_field = (
            "Approved path: docs/operations/deployment-rollback.md."
        )
        successful_path_replacement_formats = {
            "line": "\n{label}: {value}.\n",
            "folded": "{label}: {value}.",
            "markdown": "\n- {label}: {value}\n",
        }
        self.assertEqual(1, successful_response.count(successful_path_field))

        def replace_successful_path_field(
            response: str,
            presentation: str,
            label: str,
            value: str,
        ) -> str:
            replacement = successful_path_replacement_formats[
                presentation
            ].format(label=label, value=value)
            return response.replace(successful_path_field, replacement, 1)

        for presentation, prefix in path_presentations:
            for chosen_path_alias in chosen_path_aliases:
                with self.subTest(
                    chosen_path_presentation=presentation,
                    chosen_path_alias=chosen_path_alias,
                ):
                    self.assertIsNotNone(
                        selected_path_pattern.search(
                            f"{blocked_response}{prefix}{chosen_path_alias}: "
                            "fixtures/client/compatibility.json"
                        )
                    )

        sentinel_prefixed_paths = (
            "none.md",
            "unavailable/report.md",
            "not-provided.json",
            "omitted.md",
            "absent/report.md",
            "not-selected/result.md",
            "na",
            "n/a.md",
        )
        punctuation_continued_paths = (
            "none. report.md",
            "none. /report.md",
            "unavailable; report.md",
            "not provided; reports/output.md",
            "not-provided. json",
        )
        recognized_name_continued_paths = (
            "none. status-report.md",
            "none. owner-report.md",
            "none. rationale-report.md",
            "none. placement-audit-report.md",
            "none. purpose-report.md",
            "none. artifact-kind-report.md",
        )
        real_path_values = (
            sentinel_prefixed_paths
            + punctuation_continued_paths
            + recognized_name_continued_paths
        )
        for presentation, prefix in path_presentations:
            for chosen_path_alias in chosen_path_aliases:
                for real_path_value in real_path_values:
                    with self.subTest(
                        real_path_presentation=presentation,
                        chosen_path_alias=chosen_path_alias,
                        real_path_value=real_path_value,
                    ):
                        self.assertIsNotNone(
                            selected_path_pattern.search(
                                f"{blocked_response}{prefix}{chosen_path_alias}: "
                                f"{real_path_value}"
                            )
                        )
                        self.assertEqual(
                            (),
                            forbidden_success_marker_families(
                                f"{successful_response}{prefix}"
                                f"{chosen_path_alias}: {real_path_value}"
                            ),
                        )

        omission_values = (
            "omitted",
            "absent",
            "unavailable",
            "none",
            "n/a",
            "not applicable",
            "not approved",
            "not selected",
            "not provided",
            "not-provided",
        )
        actual_success_real_paths = (
            "na",
            "n/a.md",
            "omitted.md",
            "none. report.md",
            "none. status-report.md",
        )
        for presentation, _prefix in path_presentations:
            for chosen_path_alias in chosen_path_aliases:
                for actual_success_real_path in actual_success_real_paths:
                    with self.subTest(
                        actual_success_presentation=presentation,
                        chosen_path_alias=chosen_path_alias,
                        actual_success_real_path=actual_success_real_path,
                    ):
                        mutated_success = replace_successful_path_field(
                            successful_response,
                            presentation,
                            chosen_path_alias,
                            actual_success_real_path,
                        )
                        self.assertIsNotNone(
                            selected_path_pattern.search(mutated_success)
                        )
                        self.assertEqual(
                            (),
                            forbidden_success_marker_families(mutated_success),
                        )

                for actual_success_omission in omission_values:
                    with self.subTest(
                        actual_success_presentation=presentation,
                        chosen_path_alias=chosen_path_alias,
                        actual_success_omission=actual_success_omission,
                    ):
                        mutated_success = replace_successful_path_field(
                            successful_response,
                            presentation,
                            chosen_path_alias,
                            actual_success_omission,
                        )
                        self.assertIsNone(
                            selected_path_pattern.search(mutated_success)
                        )
                        self.assertIn(
                            "path omission",
                            forbidden_success_marker_families(mutated_success),
                        )

        for presentation, prefix in path_presentations:
            for chosen_path_alias in chosen_path_aliases:
                for omission_value in omission_values:
                    for terminal_punctuation in ("", ".", ";"):
                        with self.subTest(
                            omission_presentation=presentation,
                            chosen_path_alias=chosen_path_alias,
                            omission_value=omission_value,
                            terminal_punctuation=terminal_punctuation,
                        ):
                            omission_field = (
                                f"{prefix}{chosen_path_alias}: {omission_value}"
                                f"{terminal_punctuation}"
                            )
                            self.assertIsNone(
                                selected_path_pattern.search(
                                    blocked_response + omission_field
                                )
                            )
                            self.assertIn(
                                "path omission",
                                forbidden_success_marker_families(
                                    successful_response + omission_field
                                ),
                            )

        recognized_folded_fields = (
            "Purpose: test fixture",
            "Owner: repository maintainers",
            "Lifecycle: maintained",
            "Consumers: bundle tests",
            "Mutability: source-controlled",
            "Artifact kind: test fixture",
            "Approved path: omitted",
            "Selected path: not applicable",
            "Chosen path: not approved",
            "Destination: unavailable",
            "Approved destination: none",
            "Selected destination: not selected",
            "Chosen destination: not provided",
            "Blocker: unresolved ownership",
            "Exact decision needed: select one owner",
            "Rationale: taxonomy is ambiguous",
            "Placement audit: no file created",
            "Status: BLOCKED",
        )
        for omission_value in omission_values:
            for folded_field in recognized_folded_fields:
                for folded_separator in (" ", ". ", "; "):
                    for markdown_marker in ("", "- "):
                        with self.subTest(
                            folded_omission_value=omission_value,
                            recognized_folded_field=folded_field,
                            folded_separator=folded_separator,
                            markdown_marker=markdown_marker,
                        ):
                            folded_omission = (
                                f" Selected path: {omission_value}"
                                f"{folded_separator}{markdown_marker}"
                                f"{folded_field}"
                            )
                            self.assertIsNone(
                                selected_path_pattern.search(
                                    blocked_response + folded_omission
                                )
                            )
                            self.assertIn(
                                "path omission",
                                forbidden_success_marker_families(
                                    successful_response + folded_omission
                                ),
                            )

        unknown_folded_field_continuations = (
            "none. Notes: report.md",
            "none. Status report: report.md",
        )
        for presentation, prefix in path_presentations:
            for chosen_path_alias in chosen_path_aliases:
                for unknown_continuation in unknown_folded_field_continuations:
                    with self.subTest(
                        unknown_field_presentation=presentation,
                        chosen_path_alias=chosen_path_alias,
                        unknown_continuation=unknown_continuation,
                    ):
                        self.assertIsNotNone(
                            selected_path_pattern.search(
                                f"{blocked_response}{prefix}"
                                f"{chosen_path_alias}: {unknown_continuation}"
                            )
                        )
                        self.assertEqual(
                            (),
                            forbidden_success_marker_families(
                                f"{successful_response}{prefix}"
                                f"{chosen_path_alias}: {unknown_continuation}"
                            ),
                        )

        classification_instruction = (
            "Explicitly state the artifact purpose, owner, lifecycle, consumers, "
            "mutability, and artifact kind in every placement rationale or blocker."
        )
        self.assertIn(classification_instruction, role["instructions"])

        filename_instruction = "Choose the filename from local conventions."
        response_only_instruction = (
            "Do not invent a filename or path for response-only design content."
        )
        forbidden_blanket_rules = (
            "- Do not choose filenames.",
            "- Do not write files.",
        )
        skill_texts = {
            "organise-project-files": (
                SKILLS_ROOT / "organise-project-files" / "SKILL.md"
            ).read_text(encoding="utf-8"),
            "structured-design": (
                SKILLS_ROOT / "structured-design" / "SKILL.md"
            ).read_text(encoding="utf-8"),
        }
        self.assertIn(filename_instruction, skill_texts["organise-project-files"])
        self.assertIn(response_only_instruction, skill_texts["structured-design"])
        self.assertIn(
            "Do not create a design file merely because design content was requested.",
            skill_texts["structured-design"],
        )

        adapter_paths = {
            "codex": GENERATED_ADAPTERS_ROOT
            / "codex"
            / "agents"
            / "project-organiser.toml",
            "claude": GENERATED_ADAPTERS_ROOT
            / "claude"
            / "agents"
            / "project-organiser.md",
            "gemini": GENERATED_ADAPTERS_ROOT
            / "gemini"
            / "agents"
            / "project-organiser.md",
            "junie": GENERATED_ADAPTERS_ROOT
            / "junie"
            / "agents"
            / "project-organiser.md",
        }
        markdown_return = (
            "Return:\n\n- approved path or placement blocker\n"
            "- placement rationale\n- file-placement audit"
        )
        expected_adapter_returns = {
            "codex": (
                "Return: approved path or placement blocker; placement rationale; "
                "file-placement audit."
            ),
            "claude": markdown_return,
            "gemini": markdown_return,
            "junie": markdown_return,
        }
        standalone_adapter_return_patterns = {
            "codex": (
                r"(?m)^Return: (?:[^;\n]+; )*approved path(?:; [^;\n]+)*\.$",
                r"(?m)^Return: (?:[^;\n]+; )*placement blocker(?:; [^;\n]+)*\.$",
            ),
            "claude": (
                r"(?m)^- approved path$",
                r"(?m)^- placement blocker$",
            ),
            "gemini": (
                r"(?m)^- approved path$",
                r"(?m)^- placement blocker$",
            ),
            "junie": (
                r"(?m)^- approved path$",
                r"(?m)^- placement blocker$",
            ),
        }
        for adapter, adapter_path in adapter_paths.items():
            adapter_text = adapter_path.read_text(encoding="utf-8")
            with self.subTest(adapter=adapter):
                self.assertIn(
                    "BEGIN INLINED CORE SKILL: organise-project-files",
                    adapter_text,
                )
                self.assertIn(filename_instruction, adapter_text)
                self.assertIn(
                    "BEGIN INLINED CORE SKILL: structured-design",
                    adapter_text,
                )
                self.assertIn(response_only_instruction, adapter_text)
                self.assertIn(classification_instruction, adapter_text)
                self.assertIn(approved_path_instruction, adapter_text)
                self.assertIn(blocked_path_instruction, adapter_text)
                self.assertIn(expected_adapter_returns[adapter], adapter_text)
                for pattern in standalone_adapter_return_patterns[adapter]:
                    self.assertNotRegex(adapter_text, pattern)
                for forbidden_rule in forbidden_blanket_rules:
                    self.assertNotIn(forbidden_rule, adapter_text)

    def test_backlog_skills_separate_user_action_required_from_dispatchable_work(self) -> None:
        primary_root = resolve_primary_repository_root()
        create_text = (SKILLS_ROOT / "create-file-work-item" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        manage_text = (SKILLS_ROOT / "manage-file-work-items" / "SKILL.md").read_text(
            encoding="utf-8"
        )

        for skill_name, skill_text in (
            ("create-file-work-item", create_text),
            ("manage-file-work-items", manage_text),
        ):
            with self.subTest(skill=skill_name):
                self.assertIn("backlog/user-action-required", skill_text)
                self.assertNotIn("docs/user-action-required", skill_text)
                self.assertIn("user action required", skill_text.lower())

        for required_guidance in (
            "User Action Required",
            "Question for the User",
            "Why User Input Is Required",
            "Do not place an item in backlog/user-action-required merely because",
            "synthetic evaluation boundary",
        ):
            with self.subTest(create_guidance=required_guidance):
                self.assertIn(required_guidance, create_text)

        for required_guidance in (
            "Do not claim, dispatch, implement, or resolve user-action-required work",
            "Ask the user the exact question recorded in the item",
            "Move an approved or answered item into its typed active backlog folder",
            "set Status: Ready before any separately requested claim or running transition",
            "backlog/holding is for intentionally deferred work",
        ):
            with self.subTest(manage_guidance=required_guidance):
                self.assertIn(required_guidance, manage_text)
        self.assertNotIn("set its active status according to project convention", manage_text)

    def test_file_work_item_skills_own_behavior_and_legacy_ids_are_migration_only(self) -> None:
        primary_root = resolve_primary_repository_root()
        canonical_contracts = {
            "create-file-work-item": (
                "The only authoritative file-provider storage root is backlog in the primary worktree while that worktree is on main.",
                "Do not write a shadow queue elsewhere.",
                "Before writing, search every active typed folder",
                "Source Evidence",
                "released backlog claim reference",
            ),
            "manage-file-work-items": (
                "The only authoritative file-provider storage root is backlog in the primary worktree while that worktree is on main.",
                "must not create, transition, or archive the canonical record",
                "SHARED_CHECKOUT_RELEASE_REQUIRED is a coordination outcome rather than a failed mutation",
                "AWAITING_REVIEW",
                "main observation",
                "failed archive path",
            ),
        }

        for skill_name, required_contracts in canonical_contracts.items():
            skill_path = SKILLS_ROOT / skill_name / "SKILL.md"
            skill_text = skill_path.read_text(encoding="utf-8")
            frontmatter = load_yaml_object_from_frontmatter(skill_path)
            with self.subTest(skill=skill_name):
                self.assertEqual(skill_name, frontmatter["name"])
                self.assertIn("effective provider is file", frontmatter["description"])
                for required_contract in required_contracts:
                    self.assertIn(required_contract, skill_text)

        legacy_replacements = {
            "create-backlog": ("create-file-work-item",),
            "manage-backlog": ("manage-file-work-items",),
            "file-based-backlog": (
                "create-file-work-item",
                "manage-file-work-items",
            ),
        }
        for legacy_name, replacements in legacy_replacements.items():
            legacy_text = (SKILLS_ROOT / legacy_name / "SKILL.md").read_text(
                encoding="utf-8"
            )
            with self.subTest(legacy=legacy_name):
                self.assertIn("migration-only", legacy_text.lower())
                self.assertIn("supplies no", legacy_text)
                self.assertNotIn("## Operations", legacy_text)
                self.assertNotIn("## Folder Model", legacy_text)
                self.assertNotIn("## Completion Workflow", legacy_text)
                for replacement in replacements:
                    self.assertIn(replacement, legacy_text)

        user_action_required_root = primary_root / "backlog" / "user-action-required"
        queue_readme = user_action_required_root / "README.md"
        classification_item = (
            primary_root
            / "backlog"
            / "completed-backlog"
            / "analyses"
            / "classify-agent-suite-blocking-resources.md"
        )
        self.assertTrue(queue_readme.is_file())
        self.assertTrue(classification_item.is_file())
        queue_text = queue_readme.read_text(encoding="utf-8")
        for required_queue_contract in (
            "# User Action Required Queue",
            "Status: User Action Required",
            "README.md is queue guidance and is not a backlog item.",
        ):
            with self.subTest(queue_contract=required_queue_contract):
                self.assertIn(required_queue_contract, queue_text)
        classification_text = classification_item.read_text(encoding="utf-8")
        for required_item_contract in (
            "Status: Completed",
            "Type: Analysis",
            "## User Action Required",
            "### Question for the User",
            "### Why User Input Is Required",
            "### Resolution",
            "Resolved 2026-07-19.",
            "Which blocked categories should become real follow-up backlog work: test infrastructure limitations only, selected authority or evidence gaps, all categories, or none?",
        ):
            with self.subTest(item_contract=required_item_contract):
                self.assertIn(required_item_contract, classification_text)

    def test_user_action_required_migration_has_no_stale_canonical_references(self) -> None:
        primary_root = resolve_primary_repository_root()
        tracked = subprocess.run(
            ["git", "ls-files", "-z"],
            cwd=primary_root,
            check=True,
            capture_output=True,
        ).stdout.decode("utf-8").split("\0")
        historical_name = "rename-user-review-state-for-clarity.md"
        stale_path = "backlog/" + "user-review"
        stale_status = "Status: User" + " Review"
        stale_references: list[str] = []

        for relative_path in filter(None, tracked):
            path = primary_root / relative_path
            if not path.is_file():
                continue
            if relative_path.startswith("legacy_procedures/") or path.name == historical_name:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if stale_path in text or stale_status in text:
                stale_references.append(relative_path)

        self.assertEqual([], stale_references)

    def test_active_typed_backlog_has_no_proposed_status(self) -> None:
        primary_root = resolve_primary_repository_root()
        active_roots = (
            primary_root / "backlog" / "defect-backlog",
            primary_root / "backlog" / "feature-backlog",
            primary_root / "backlog" / "analysis-backlog",
            primary_root / "backlog" / "investigation-backlog",
        )
        existing_roots = tuple(root for root in active_roots if root.is_dir())
        self.assertTrue(existing_roots, "No canonical active typed backlog is accessible")
        stale_status = "Status: " + "Proposed"
        proposed_items = [
            str(path.relative_to(primary_root))
            for root in existing_roots
            for path in root.rglob("*.md")
            if path.name != "index.md"
            and stale_status in path.read_text(encoding="utf-8")
        ]

        self.assertEqual([], proposed_items)

    def test_backlog_regressions_resolve_the_canonical_primary_worktree(self) -> None:
        primary_root = resolve_primary_repository_root()
        tracked_backlog = subprocess.run(
            ["git", "ls-files", "backlog"],
            cwd=primary_root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()

        self.assertTrue(tracked_backlog, "Canonical primary backlog has no tracked inputs")
        self.assertTrue(all((primary_root / path).is_file() for path in tracked_backlog))

    def test_answered_user_action_enters_ready_before_claiming(self) -> None:
        manage_text = (SKILLS_ROOT / "manage-file-work-items" / "SKILL.md").read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "set Status: Ready before any separately requested claim or running transition",
            manage_text,
        )
        self.assertNotIn(
            "set its active status according to project convention",
            manage_text,
        )

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

    def test_generated_template_definition_data_is_current(self) -> None:
        build_skill_docs = load_build_skill_docs_module()
        payload = build_skill_docs.build_template_payload()
        rendered = build_skill_docs.render_template_javascript(payload)

        self.assertEqual(
            set(DOCUMENTATION_TEMPLATE_FILENAMES),
            set(payload["templates"]),
        )
        self.assertEqual(
            rendered,
            TEMPLATE_DEFINITIONS_PATH.read_text(encoding="utf-8"),
        )
        for template_name, template in payload["templates"].items():
            with self.subTest(template=template_name):
                self.assertNotIn("Witty remark:", template["content"])
                self.assertTrue((REPOSITORY_ROOT / template["sourcePath"]).is_file())

    def test_generated_skill_definition_links_resolve_from_design_pages(self) -> None:
        build_skill_docs = load_build_skill_docs_module()
        payload = build_skill_docs.build_payload()

        for skill_name, skill in payload["skills"].items():
            for href in re.findall(r'href="([^"]+)"', skill["html"]):
                parsed = urlsplit(href)
                if parsed.scheme or parsed.netloc or not parsed.path or parsed.path.startswith("/"):
                    continue
                target = (REPOSITORY_ROOT / "design" / parsed.path).resolve()
                with self.subTest(skill_name=skill_name, href=href):
                    self.assertTrue(target.is_file(), f"Generated skill link does not exist: {target}")

    def test_skill_link_rebasing_preserves_nonlocal_targets_and_fragments(self) -> None:
        build_skill_docs = load_build_skill_docs_module()
        skill_directory = SKILLS_ROOT / "spring-boot-design"

        expected_links = {
            "https://example.com/guidance": "https://example.com/guidance",
            "#design-boundary": "#design-boundary",
            "/shared/guidance.md": "/shared/guidance.md",
            "references/design-principles-spring-boot.md#modules": (
                "../skills/spring-boot-design/references/"
                "design-principles-spring-boot.md#modules"
            ),
        }
        for source, expected in expected_links.items():
            with self.subTest(source=source):
                self.assertEqual(
                    expected,
                    build_skill_docs._design_href_for_skill_link(source, skill_directory),
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
            "generated Codex, Claude Code, Gemini CLI, and Junie CLI native agent definitions",
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
        self.assertEqual(3, generation_manifest["version"])
        self.assertEqual(
            {"inlineCoreSkills": True},
            generation_manifest["generationOptions"],
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
                harness_skills = adapter_manifest["harnessSkills"]
                if adapter_name == "codex":
                    self.assertEqual([CODEX_HARNESS_SKILL_NAME], [item["name"] for item in harness_skills])
                    self.assertEqual(
                        "adapters/codex/skills/codex-harness-directives",
                        harness_skills[0]["source"],
                    )
                    self.assertRegex(harness_skills[0]["sha256"], r"^[0-9a-f]{64}$")
                else:
                    self.assertEqual([], harness_skills)
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
                            example["runtimeInvocations"]["codex"].startswith("$dev_documentation_writer ")
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
                    build_skill_docs.codex_role_instruction_text(
                        role,
                        known_role_names=tuple(sorted(source_role_names)),
                    ),
                    tomllib.loads(codex_agent_text)["developer_instructions"],
                )
                self.assertNotIn(
                    "Before acting, load these definition-owned skills completely; they govern the work:",
                    codex_agent_text,
                )
                for skill in build_skill_docs.fixed_role_skills(role):
                    self.assertIn(f"BEGIN INLINED CORE SKILL: {skill}", codex_agent_text)
                codex_payload = tomllib.loads(codex_agent_text)
                configured_skills = codex_payload.get("skills", {}).get("config", [])
                if role.repository_mutation == "never":
                    self.assertNotIn(CODEX_HARNESS_SKILL_NAME, codex_agent_text)
                    self.assertNotIn(
                        CODEX_HARNESS_SKILL_NAME,
                        [item.get("name") for item in configured_skills],
                    )
                else:
                    self.assertIn(
                        f"BEGIN INLINED CORE SKILL: {CODEX_HARNESS_SKILL_NAME}",
                        codex_agent_text,
                    )
                    self.assertNotIn(
                        CODEX_HARNESS_SKILL_NAME,
                        [item.get("name") for item in configured_skills],
                    )
                if "skillAvailability" not in role.optional_fields:
                    self.assertNotIn("[[skills.config]]", codex_agent_text)
                self.assertTrue(
                    (GENERATED_ADAPTERS_ROOT / "claude" / "agents" / f"{role.filename}.md").is_file()
                )
                claude_agent_text = (
                    GENERATED_ADAPTERS_ROOT / "claude" / "agents" / f"{role.filename}.md"
                ).read_text(encoding="utf-8")
                self.assertNotIn(CODEX_HARNESS_SKILL_NAME, claude_agent_text)
                self.assertIn("Skill justifications:", claude_agent_text)
                self.assertIn("Output purposes:", claude_agent_text)
                claude_frontmatter = yaml.safe_load(claude_agent_text.split("---", 2)[1])
                self.assertNotIn("skills", claude_frontmatter)
                self.assertNotIn("These definition-owned skills are preloaded and govern the work", claude_agent_text)
                for skill in build_skill_docs.fixed_role_skills(role):
                    self.assertIn(f"BEGIN INLINED CORE SKILL: {skill}", claude_agent_text)
                for skill, condition in role.skill_conditions.items():
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
                self.assertNotIn("Before acting, load these definition-owned skills completely", gemini_agent_text)
                for skill in build_skill_docs.fixed_role_skills(role):
                    self.assertIn(f"BEGIN INLINED CORE SKILL: {skill}", gemini_agent_text)
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
                self.assertNotIn("skills", junie_frontmatter)
                self.assertIn("reasoningLevel", junie_frontmatter)
                self.assertNotIn("These definition-owned skills are preloaded and govern the work", junie_agent_text)
                for skill in build_skill_docs.fixed_role_skills(role):
                    self.assertIn(f"BEGIN INLINED CORE SKILL: {skill}", junie_agent_text)
                for skill, condition in role.skill_conditions.items():
                    self.assertIn(f"Use the {skill} skill {condition}.", junie_agent_text)

        non_setup_roles = [
            role for role in roles
            if role.name != "project-configurator"
        ]
        self.assertTrue(all("detect-technology-skills" not in role.skills for role in non_setup_roles))
        setup_role = next(role for role in roles if role.name == "project-configurator")
        self.assertIn("detect-technology-skills", setup_role.skills)

    def test_core_skills_inline_by_default_and_can_use_native_loading(self) -> None:
        build_skill_docs = load_build_skill_docs_module()
        skill_payload = build_skill_docs.build_payload()
        role = next(
            role
            for role in build_skill_docs.load_role_definitions(set(skill_payload["skills"]))
            if role.name == "dev-coder"
        )
        profile_ids = set(build_skill_docs.load_model_profiles())

        claude_profiles = build_skill_docs.load_adapter_model_profiles("claude", profile_ids)
        inlined = build_skill_docs.render_claude_agent(role, claude_profiles)
        inlined_frontmatter = yaml.safe_load(inlined.split("---", 2)[1])
        self.assertNotIn("skills", inlined_frontmatter)
        self.assertNotIn(
            "Before acting, load these definition-owned skills completely",
            inlined,
        )
        for skill in build_skill_docs.fixed_role_skills(role):
            self.assertIn(f"BEGIN INLINED CORE SKILL: {skill}", inlined)
        for skill, condition in role.skill_conditions.items():
            self.assertIn(f"Use the {skill} skill {condition}.", inlined)
            self.assertNotIn(f"BEGIN INLINED CORE SKILL: {skill}", inlined)

        dynamically_loaded = build_skill_docs.render_claude_agent(
            role,
            claude_profiles,
            inline_core_skills=False,
        )
        dynamically_loaded_frontmatter = yaml.safe_load(
            dynamically_loaded.split("---", 2)[1]
        )
        self.assertEqual(
            list(build_skill_docs.fixed_role_skills(role)),
            dynamically_loaded_frontmatter["skills"],
        )
        self.assertNotIn("BEGIN INLINED CORE SKILL", dynamically_loaded)
        self.assertIn(
            "These definition-owned skills are preloaded and govern the work",
            dynamically_loaded,
        )

        codex_profiles = build_skill_docs.load_adapter_model_profiles("codex", profile_ids)
        codex_inlined = tomllib.loads(
            build_skill_docs.render_codex_agent(role, codex_profiles)
        )
        self.assertNotIn(
            CODEX_HARNESS_SKILL_NAME,
            [
                item.get("name")
                for item in codex_inlined.get("skills", {}).get("config", [])
            ],
        )
        self.assertIn(
            f"BEGIN INLINED CORE SKILL: {CODEX_HARNESS_SKILL_NAME}",
            codex_inlined["developer_instructions"],
        )

        codex_dynamic = tomllib.loads(
            build_skill_docs.render_codex_agent(
                role,
                codex_profiles,
                inline_core_skills=False,
            )
        )
        self.assertIn(
            {"name": CODEX_HARNESS_SKILL_NAME, "enabled": True},
            codex_dynamic["skills"]["config"],
        )
        self.assertNotIn("BEGIN INLINED CORE SKILL", codex_dynamic["developer_instructions"])

        gemini_profiles = build_skill_docs.load_adapter_model_profiles("gemini", profile_ids)
        gemini_dynamic = build_skill_docs.render_gemini_agent(
            role,
            gemini_profiles,
            inline_core_skills=False,
        )
        self.assertIn(
            "Before acting, load these definition-owned skills completely",
            gemini_dynamic,
        )
        self.assertNotIn("BEGIN INLINED CORE SKILL", gemini_dynamic)

        junie_profiles = build_skill_docs.load_adapter_model_profiles("junie", profile_ids)
        junie_inlined = build_skill_docs.render_junie_agent(role, junie_profiles)
        self.assertNotIn("skills", yaml.safe_load(junie_inlined.split("---", 2)[1]))
        junie_dynamic = build_skill_docs.render_junie_agent(
            role,
            junie_profiles,
            inline_core_skills=False,
        )
        self.assertEqual(
            list(build_skill_docs.fixed_role_skills(role)),
            yaml.safe_load(junie_dynamic.split("---", 2)[1])["skills"],
        )
        self.assertNotIn("BEGIN INLINED CORE SKILL", junie_dynamic)

    def test_adapter_generator_cli_defaults_to_inlined_core_skills(self) -> None:
        current = subprocess.run(
            [sys.executable, str(BUILD_SKILL_DOCS_PATH), "--check"],
            cwd=REPOSITORY_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, current.returncode, current.stdout + current.stderr)

        dynamic = subprocess.run(
            [
                sys.executable,
                str(BUILD_SKILL_DOCS_PATH),
                "--check",
                "--inline-core-skills",
                "false",
            ],
            cwd=REPOSITORY_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(1, dynamic.returncode)
        self.assertIn("stale", dynamic.stdout)

        invalid = subprocess.run(
            [
                sys.executable,
                str(BUILD_SKILL_DOCS_PATH),
                "--inline-core-skills",
                "yes",
            ],
            cwd=REPOSITORY_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(2, invalid.returncode)
        self.assertIn("expected true or false", invalid.stderr)

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
                {"objective": "Incomplete conceptual agent definition."},
                ROLE_SCHEMA_PATH,
            )

    def test_claim_guidance_separates_project_backlog_and_union_domains(self) -> None:
        claim_text = (SKILLS_ROOT / "agent-claim" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        readme_text = README_PATH.read_text(encoding="utf-8")

        for required_contract in (
            "project-files names every project file except backlog and ignored operational worktree state",
            "backlog names the complete repository-root backlog subtree",
            "all-files names the explicit union of project-files and backlog",
            "A request that mixes project and backlog paths is rejected atomically",
            "compat_backlog_path warning",
            "Project-files claims remain eligible for canonical isolated worktrees",
        ):
            with self.subTest(claim_contract=required_contract):
                self.assertIn(required_contract, claim_text)

        for required_contract in (
            "Project-files owns the repository file tree except backlog and ignored operational state",
            "Backlog owns only the complete primary-worktree backlog subtree",
            "All-files is their deliberate union for recovery and true repository-wide work",
            "Keep backlog lifecycle commits separate from long-running implementation claims",
        ):
            with self.subTest(readme_contract=required_contract):
                self.assertIn(required_contract, readme_text)

    def test_backlog_claim_guidance_uses_short_primary_batons(self) -> None:
        create_text = (SKILLS_ROOT / "create-file-work-item" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        manage_text = (SKILLS_ROOT / "manage-file-work-items" / "SKILL.md").read_text(
            encoding="utf-8"
        )

        for required_contract in (
            "short backlog-domain claim",
            "release that claim immediately",
            "Do not combine backlog creation with a project-files implementation claim",
            "acquire a separate exact, tree, or project-files implementation claim",
            "A later backlog claim records terminal evidence and archive movement",
        ):
            with self.subTest(create_contract=required_contract):
                self.assertIn(required_contract, create_text)

        for required_contract in (
            "record Status: Running and ownership evidence",
            "release immediately",
            "Delivery then uses a separate exact, tree, or project-files claim without backlog ownership",
            "acquire a later backlog claim to record result evidence and archive the item",
            "SHARED_CHECKOUT_RELEASE_REQUIRED is a coordination outcome rather than a failed mutation",
            "suspend without polling",
            "Resume only after that notification",
        ):
            with self.subTest(manage_contract=required_contract):
                self.assertIn(required_contract, manage_text)

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
        claim_skill = (SKILLS_ROOT / "agent-claim" / "SKILL.md").read_text(encoding="utf-8")
        mcp_skill = (SKILLS_ROOT / "agent-claim-mcp" / "SKILL.md").read_text(encoding="utf-8")
        command_skill = (SKILLS_ROOT / "agent-claim-command" / "SKILL.md").read_text(encoding="utf-8")
        merge_skill = (SKILLS_ROOT / "agent-work-merge" / "SKILL.md").read_text(encoding="utf-8")
        claim_script = SKILLS_ROOT / "agent-claim-command" / "scripts" / "claim.py"
        self.assertTrue(claim_script.is_file())
        self.assertFalse((SKILLS_ROOT / "agent-claim" / "scripts" / "claim.py").exists())
        self.assertNotIn("## Operation Selection", claim_skill)
        self.assertNotIn("CLAIM_SCRIPT", claim_skill)
        self.assertIn("## Coordination Outcomes", claim_skill)
        for tool_name in (
            "claim_status",
            "claim_acquire",
            "claim_extend",
            "claim_heartbeat",
            "claim_release",
            "claim_maintain_journal",
            "claim_report",
        ):
            self.assertIn(tool_name, mcp_skill)
            self.assertNotIn(tool_name, claim_skill)
        for required_outcome in (
            "SHARED_CHECKOUT_REQUIRED",
            "SHARED_CHECKOUT_RELEASE_REQUIRED",
        ):
            self.assertIn(required_outcome, claim_skill)
        self.assertIn("canonical .worktrees directory", claim_skill)
        self.assertIn("CLAIM_TRANSPORT_UNAVAILABLE", mcp_skill)
        self.assertIn("CLAIM_TRANSPORT_UNAVAILABLE", command_skill)
        self.assertIn("do not switch transports", mcp_skill)
        self.assertIn("do not switch transports", command_skill)
        self.assertIn(
            'CLAIM_SCRIPT="${HOME}/.agents/skills/agent-claim-command/scripts/claim.py"',
            command_skill,
        )
        self.assertIn("skills/agent-claim-command/scripts/claim.py", command_skill)
        self.assertNotIn("agent-claim-command", mcp_skill)
        self.assertNotIn("agent-claim-mcp", command_skill)
        self.assertIn("Stable process exit codes", command_skill)
        self.assertIn("4 for ISOLATED_CHECKOUT_SETUP_REQUIRED", command_skill)
        self.assertIn("3 for CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED", command_skill)
        self.assertIn("5 for DIRTY_CHECKOUT_RECOVERY_AUTHORIZATION_REQUIRED", command_skill)
        self.assertIn("### Shared Checkout Acquisition", claim_skill)
        self.assertIn("### Isolated Checkout Acquisition", claim_skill)
        self.assertIn("primary worktree's .worktrees directory", claim_skill)
        self.assertIn("INVALID_WORKTREE_PATH", claim_skill)
        self.assertIn("WORKTREE_ROOT_NOT_IGNORED", claim_skill)
        self.assertNotIn("--worktree-path ../project-task-123", command_skill)
        self.assertIn("repository-root backlog directory", claim_skill)
        self.assertIn("worktree-specific sparse checkout", claim_skill)
        self.assertIn("### Claim Scope Conflict Wait", claim_skill)
        self.assertIn("### Recovery Acquisition", claim_skill)
        self.assertIn("--base main", command_skill)
        self.assertIn("--allow-recovery", command_skill)
        self.assertIn("## Heartbeat", claim_skill)
        self.assertIn("### No-Change Release", claim_skill)
        self.assertIn("--no-change", command_skill)
        self.assertIn("## Atomic Scope Extension", claim_skill)
        self.assertIn("tree", claim_skill)
        self.assertIn("all-files", claim_skill)
        self.assertIn("## Event Journal Safety", claim_skill)
        self.assertIn("maintain-journal --hot-days 2", command_skill)
        self.assertIn("report --since 2d", command_skill)
        self.assertNotIn("git:commit", claim_skill)
        self.assertIn("merge:integration:main", claim_skill)
        self.assertIn("merge:integration:main", merge_skill)
        readme_text = README_PATH.read_text(encoding="utf-8")
        self.assertIn("Agent Claims And Worktrees", readme_text)
        self.assertIn("repository-global event journal", readme_text)
        self.assertIn("target-specific integration resource", readme_text)
        self.assertIn("primary worktree's .worktrees directory", readme_text)
        self.assertIn("Double-force Git clean is prohibited", readme_text)
        self.assertNotIn("Agent Claims And Worktrees", AGENTS_PATH.read_text(encoding="utf-8"))
        self.assertIn("## Agent Claim Transport", AGENTS_PATH.read_text(encoding="utf-8"))
        self.assertIn(
            ".worktrees contains ignored linked agent checkouts rooted at the primary worktree",
            AGENTS_PATH.read_text(encoding="utf-8"),
        )
        self.assertIn("/.worktrees/", GITIGNORE_PATH.read_text(encoding="utf-8").splitlines())

    def test_coordination_registry_reset_and_current_main_reconciliation_contracts(self) -> None:
        """Protect inactive-entry reset and ancestry-bounded integration guidance."""
        claim_text = (SKILLS_ROOT / "agent-claim" / "SKILL.md").read_text(encoding="utf-8")
        merge_text = (SKILLS_ROOT / "agent-work-merge" / "SKILL.md").read_text(encoding="utf-8")
        coordination_text = (
            SKILLS_ROOT / "codex-workitem-coordination" / "SKILL.md"
        ).read_text(encoding="utf-8")
        design_text = (
            REPOSITORY_ROOT / "design" / "orchestrated-development-lifecycle.html"
        ).read_text(encoding="utf-8")

        for required_contract in (
            "temporary conflict protection for shared mutation",
            "does not decide whether reviewed, verified, committed product delivery exists",
            "Release validates operational coordination state, not committed content",
            "does not traverse commit history, audit committed paths, enforce contribution scope, or interpret merge ancestry",
            "Independent review and integration own committed-content, changed-path, and provenance decisions",
            "## Administrative Reset Of Inactive Entries",
            "dirty unpreserved claimed worktree",
            "another active owner's protection",
            "a resource still in use",
            "no other active protection can be affected",
            "retain a readable registry snapshot or exact journal references",
            "host-supported targeted atomic reset operation",
            "revalidates the safeguards at mutation time",
            "bundled portable command does not expose an administrative reset subcommand",
            "Never edit the live registry file manually",
            "must not rewrite Git, edit project files, discard a worktree, manufacture a release event",
            "release-validation failures as coordination diagnostics",
            "inactive registry entry remains after work and resources are preserved",
        ):
            with self.subTest(claim_contract=required_contract):
                self.assertIn(required_contract, claim_text)

        for required_contract in (
            "fresh reconciliation branch from current main",
            "exact accepted paths",
            "Do not merge cumulative feature-branch history merely to preserve provenance",
            "Record every source commit identifier",
            "Use a full-history merge only when the complete imported history is intentional",
            "reconcile their semantic union on the fresh branch",
            "Content equivalence and durable source mapping are valid provenance evidence",
            "Use a full-history merge only when that complete ancestry is intentional",
            "The default ancestry-bounded path is a fresh branch from current main",
        ):
            with self.subTest(merge_contract=required_contract):
                self.assertIn(required_contract, merge_text)

        for required_contract in (
            "temporary shared-mutation protection",
            "Designate this fresh branch as the task integration and cleanup branch",
            "Do not import cumulative branch ancestry merely to preserve provenance",
            "Keep administrative coordination-registry cleanup, Git integration, and terminal backlog completion as three distinct operations",
            "A live owner, dirty unpreserved worktree, resource in use, or unclear evidence blocks reset",
            "The bundled portable claim command has no reset operation",
            "If a supported atomic operation is unavailable, stop and route the reset",
            "Claim release does not audit commit history or interpret merge ancestry",
            "fresh task integration branch is fully merged",
            "prior candidate branch used only as a non-ancestral content source is not the task cleanup branch",
        ):
            with self.subTest(coordination_contract=required_contract):
                self.assertIn(required_contract, coordination_text)

        for required_contract in (
            "fresh reconciliation branch from that exact commit",
            "do not import unrelated ancestry merely for provenance",
            "It does not audit commit history or decide whether committed paths belong to the contribution",
            "Independent review and integration own committed-content, changed-path, and provenance decisions",
            "Reset only an inactive coordination entry whose work is preserved",
            "A reset changes temporary registry state only",
            "Neither bundled coordination transport exposes reset",
            "manual registry editing is forbidden",
            "route the operation to an administrator",
            "Registry cleanup, Git integration, and backlog closeout are distinct operations",
            "this becomes the task integration and cleanup branch",
            "older candidate branch retained only as a non-ancestral content source is handled separately",
        ):
            with self.subTest(design_contract=required_contract):
                self.assertIn(required_contract, design_text)

    def test_codex_read_only_sandbox_is_reserved_for_never_mutating_roles(self) -> None:
        """Keep evidence-writing reviewers writable while preserving true read-only agents."""
        build_skill_docs = load_build_skill_docs_module()
        skill_payload = build_skill_docs.build_payload()
        roles = build_skill_docs.load_role_definitions(set(skill_payload["skills"]))
        codex_profiles = build_skill_docs.load_adapter_model_profiles(
            "codex", set(build_skill_docs.load_model_profiles())
        )
        read_only_roles = {
            role.name
            for role in roles
            if role.optional_fields.get("isolation") == "read-only"
        }

        self.assertEqual(
            {"wiki-query-responder", "wiki-topic-verifier"},
            read_only_roles,
        )
        for role in roles:
            with self.subTest(role=role.name, mutation_policy=role.repository_mutation):
                rendered = tomllib.loads(
                    build_skill_docs.render_codex_agent(role, codex_profiles)
                )
                if role.repository_mutation == "never":
                    self.assertEqual("read-only", rendered.get("sandbox_mode"))
                else:
                    self.assertNotIn("sandbox_mode", rendered)

        design_text = (
            REPOSITORY_ROOT / "design" / "generic-agent-definitions-source.html"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "Read-only isolation is valid only when repository mutation is never allowed",
            design_text,
        )

    def test_mcp_agent_ops_is_preferred_without_becoming_a_hard_runtime_dependency(self) -> None:
        skill_texts = {
            skill: (SKILLS_ROOT / skill / "SKILL.md").read_text(encoding="utf-8")
            for skill in (
                "agent-claim-mcp",
                "detect-technology-skills",
                "create-project-configuration",
                "skill-authoring",
                "maintain-methodology-documentation",
                "documentation-page-verify",
                "development-methodology",
            )
        }
        for skill, text in skill_texts.items():
            with self.subTest(skill=skill):
                self.assertIn("mcp-agent-ops", text)
                self.assertIn("rejection", text)

        shared_claim_text = (SKILLS_ROOT / "agent-claim" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("mcp-agent-ops", shared_claim_text)
        self.assertIn("one skill_load call", skill_texts["development-methodology"])
        self.assertIn("skill_resource_load", skill_texts["development-methodology"])
        self.assertIn("Do not reread a skill through MCP", skill_texts["development-methodology"])
        self.assertIn("detect_technology_skills", skill_texts["detect-technology-skills"])
        self.assertIn("skill_list plus detect_technology_skills", skill_texts["create-project-configuration"])
        self.assertIn("skill_validate", skill_texts["skill-authoring"])
        self.assertIn("verify_markdown_links", skill_texts["documentation-page-verify"])
        self.assertIn("skill_refresh", skill_texts["maintain-methodology-documentation"])

        readme_text = README_PATH.read_text(encoding="utf-8")
        for phrase in (
            "Preferred MCP Operations Layer",
            "[mcp_servers.mcp-agent-ops]",
            '"mcpServers"',
            "MCP_AGENT_OPS_SKILL_ROOTS",
            "MCP_AGENT_OPS_DETECTION_REGISTRY",
            "MCP_AGENT_OPS_WORKSPACE_ROOTS",
            "Scoped Codex and Junie deployments configure mcp-agent-ops by default.",
            "config.mcp-agent-ops.toml",
            "mcp-agent-ops.json",
            "--configure-mcp false",
        ):
            self.assertIn(phrase, readme_text)

        for role_path in ROLES_ROOT.rglob("*.role.yaml"):
            self.assertNotIn("mcp-agent-ops", role_path.read_text(encoding="utf-8"))

    def test_codex_harness_directives_are_adapter_owned_and_mutation_scoped(self) -> None:
        """Keep Codex-only routing policy out of portable roles and other harness outputs."""

        build_skill_docs = load_build_skill_docs_module()
        skill_text = (CODEX_HARNESS_SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Sol-, Terra-, or Luna-backed Codex agent", skill_text)
        self.assertIn("additional automated-safeguard check", skill_text)
        self.assertEqual(
            (CODEX_HARNESS_SKILL_NAME,),
            build_skill_docs.adapter_skill_names("codex"),
        )
        self.assertNotIn(CODEX_HARNESS_SKILL_NAME, build_skill_docs.build_payload()["skills"])

        roles = build_skill_docs.load_role_definitions(
            set(build_skill_docs.build_payload()["skills"])
        )
        codex_profiles = build_skill_docs.load_adapter_model_profiles(
            "codex", set(build_skill_docs.load_model_profiles())
        )
        for role in roles:
            with self.subTest(role=role.name, mutation=role.repository_mutation):
                rendered = build_skill_docs.render_codex_agent(role, codex_profiles)
                instructions = tomllib.loads(rendered)["developer_instructions"]
                if role.repository_mutation == "never":
                    self.assertNotIn(CODEX_HARNESS_SKILL_NAME, instructions)
                else:
                    self.assertEqual(
                        1,
                        instructions.count(
                            f"BEGIN INLINED CORE SKILL: {CODEX_HARNESS_SKILL_NAME}"
                        ),
                    )

        for adapter_name, extension in (("claude", ".md"), ("gemini", ".md"), ("junie", ".md")):
            for path in (GENERATED_ADAPTERS_ROOT / adapter_name / "agents").glob(f"*{extension}"):
                with self.subTest(adapter=adapter_name, agent=path.stem):
                    self.assertNotIn(CODEX_HARNESS_SKILL_NAME, path.read_text(encoding="utf-8"))

    def test_direct_agent_dependencies_have_complete_routing_contracts(self) -> None:
        """Every maintained direct dependency should have an explicit orchestration contract."""
        build_skill_docs = load_build_skill_docs_module()
        skill_payload = build_skill_docs.build_payload()
        roles = build_skill_docs.load_role_definitions(set(skill_payload["skills"]))
        roles_by_name = {role.name: role for role in roles}
        expected_dependencies = {
            "dev-backlog-coordinator": (
                "dev-orchestrator",
                "dev-backlog-steward",
            ),
            "dev-orchestrator": (
                "dev-coder",
                "dev-code-reviewer",
                "dev-verifier",
                "dev-merge-coordinator",
                "dev-backlog-steward",
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
                "wiki-ingester",
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
                    r"(?i)(?:route|return|this agent owns|apply only)",
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

    def test_wiki_ingester_continues_substantiated_ingest_after_verifier_interruption(
        self,
    ) -> None:
        """Verifier interruption should expose uncertainty without erasing supported work."""
        build_skill_docs = load_build_skill_docs_module()
        skill_payload = build_skill_docs.build_payload()
        roles = build_skill_docs.load_role_definitions(set(skill_payload["skills"]))
        role = next(role for role in roles if role.name == "wiki-ingester")

        workflow_text = " ".join(role.instruction_sections["workflow"])
        review_text = " ".join(role.instruction_sections["review"])
        failure_text = " ".join(role.instruction_sections["failureHandling"])
        completion_text = " ".join(role.instruction_sections["completion"])
        interruption_example = next(
            example
            for example in role.examples
            if "interruption" in example["purpose"].lower()
        )
        interruption_response = interruption_example["plausibleResponse"]

        for phrase in (
            "substantiated claim and relationship",
            "Open Questions section of exactly one most-relevant existing page",
            "missing evidence or decision",
            "provenance",
        ):
            with self.subTest(workflow_phrase=phrase):
                self.assertIn(phrase, workflow_text)
        self.assertIn("interrupted", review_text)
        self.assertIn("not a NEEDS_CORRECTION verdict", review_text)
        self.assertIn("before and after the source move", review_text)
        self.assertIn("do not report BLOCKED on the first finding", workflow_text)
        self.assertIn("Do not roll back substantiated", failure_text)
        self.assertIn("do not restore substantiated content", failure_text)
        self.assertNotIn("restore the source and its page links", failure_text)
        self.assertIn("verifier interruption", completion_text)
        self.assertIn("labeled ingested or substantiated", completion_text)
        self.assertIn("labeled Open Questions inventory", completion_text)
        self.assertIn("conclusions inventory must contain", completion_text)
        self.assertIn("Open Questions inventory must be nonempty", completion_text)
        self.assertIn("Use None only when that category truly has no entries", completion_text)
        self.assertIn("before creating the commit", workflow_text.lower())
        self.assertIn("re-open eval-result.md from disk", workflow_text.lower())
        self.assertIn("Do not commit until", workflow_text)
        self.assertIn("literal level-two", workflow_text)
        self.assertIn("Substantiated Conclusions", workflow_text)
        self.assertIn("Open Questions", workflow_text)
        self.assertIn("every non-None entry", workflow_text)
        self.assertIn("field order of page, source", workflow_text)
        self.assertIn("colon immediately before the fact", workflow_text)
        self.assertIn("valid scoped None", workflow_text)
        self.assertIn("substantiated content was written", workflow_text)
        self.assertIn("at least one fact-bearing bullet", completion_text)
        self.assertIn("exactly one most-relevant existing page", workflow_text)
        self.assertIn("only when no appropriate existing page fits", workflow_text)
        self.assertIn("STATUS: READY", interruption_response)
        self.assertIn("OPEN QUESTIONS:", interruption_response)
        self.assertIn(
            "docs/wiki/retry-policy/request-eligibility.md",
            interruption_response,
        )
        self.assertIn(
            "docs/wiki/retry-policy/retry-execution.md",
            interruption_response,
        )
        self.assertNotIn("docs/wiki/retry-policy/backoff.md", interruption_response)
        self.assertRegex(
            interruption_response,
            r"(?:missing evidence|evidence is\s+missing)",
        )
        self.assertNotIn("STATUS: BLOCKED", interruption_response)
        self.assertNotIn("restore", interruption_response.lower())
        audit_examples = [
            example
            for example in role.examples
            if "audit the final integrated tree" in example["purpose"].lower()
        ]
        self.assertEqual(1, len(audit_examples))
        self.assertIn("STATUS: NEEDS_CORRECTION", audit_examples[0]["plausibleResponse"])
        self.assertIn("explicit no-change result", audit_examples[0]["plausibleResponse"])
        for example in role.examples:
            if example in audit_examples:
                continue
            response = example["plausibleResponse"]
            with self.subTest(wiki_ingester_inventory=example["purpose"]):
                self.assertRegex(
                    response,
                    r"(?:INGESTED|SUBSTANTIATED) CONCLUSIONS:",
                )
                self.assertIn("OPEN QUESTIONS:", response)
                self.assertIn("docs/wiki/", response)
                self.assertIn("raw/", response)

        role_payload = load_yaml_object(
            ROLES_ROOT / "wiki-activities" / "wiki-ingester.role.yaml"
        )
        output_text = " ".join(
            item["purpose"]
            for output in role_payload["outputContract"]
            for item in output.values()
        )
        self.assertIn("ingested or substantiated conclusions", output_text)
        self.assertIn("Open Questions", output_text)

    def test_dev_orchestrator_routes_artifact_aware_independent_review(self) -> None:
        """Orchestration should review every changed surface through its owning review lane."""
        build_skill_docs = load_build_skill_docs_module()
        skill_payload = build_skill_docs.build_payload()
        roles = build_skill_docs.load_role_definitions(set(skill_payload["skills"]))
        role = next(role for role in roles if role.name == "dev-orchestrator")

        self.assertEqual(
            (
                "dev-coder",
                "dev-code-reviewer",
                "dev-verifier",
                "dev-merge-coordinator",
                "dev-backlog-steward",
            ),
            role.agent_dependencies,
        )

        workflow_steps = list(role.instruction_sections["workflow"])
        contribution_review_indexes = [
            index
            for index, step in enumerate(workflow_steps)
            if "source" in step.lower()
            and "dev-code-reviewer" in step
            and "every changed" not in step.lower()
            and "fresh" in step.lower()
            and "context" in step.lower()
        ]
        self.assertTrue(contribution_review_indexes)

        non_source_review_indexes = [
            index
            for index, step in enumerate(workflow_steps)
            if "non-source" in step.lower()
            and "every changed" not in step.lower()
            and "task-selected" in step.lower()
            and "independent" in step.lower()
            and "reviewer" in step.lower()
            and "fresh" in step.lower()
            and "context" in step.lower()
        ]
        self.assertTrue(non_source_review_indexes)

        contribution_verification_indexes = [
            index
            for index, step in enumerate(workflow_steps)
            if "dev-verifier" in step
            and "accepted" in step.lower()
            and "integrat" not in step.lower()
        ]
        self.assertTrue(contribution_verification_indexes)
        first_contribution_verification = min(contribution_verification_indexes)
        self.assertLess(max(contribution_review_indexes), first_contribution_verification)
        self.assertLess(max(non_source_review_indexes), first_contribution_verification)

        correction_text = " ".join(
            role.instruction_sections["workflow"]
            + role.instruction_sections["review"]
            + role.instruction_sections["failureHandling"]
        )
        self.assertRegex(
            correction_text,
            r"(?i)(?:route|return|send).{0,120}(?:finding|correction).{0,160}"
            r"original (?:producer|producing agent|executor)",
        )

        integration_indexes = [
            index
            for index, step in enumerate(workflow_steps)
            if "multiple accepted committed contributions" in step.lower()
            and "dev-merge-coordinator" in step
        ]
        self.assertEqual(1, len(integration_indexes))
        integration_index = integration_indexes[0]

        post_integration_review_indexes = [
            index
            for index, step in enumerate(workflow_steps)
            if index > integration_index
            and "every changed" in step.lower()
            and "source" in step.lower()
            and "non-source" in step.lower()
            and "dev-code-reviewer" in step
            and "task-selected" in step.lower()
            and "reviewer" in step.lower()
            and "fresh" in step.lower()
            and "context" in step.lower()
        ]
        self.assertEqual(1, len(post_integration_review_indexes))
        post_integration_review_index = post_integration_review_indexes[0]

        integrated_verification_indexes = [
            index
            for index, step in enumerate(workflow_steps)
            if index >= post_integration_review_index
            and "dev-verifier" in step
            and "complete integrated" in step.lower()
        ]
        self.assertEqual(1, len(integrated_verification_indexes))
        integrated_verification_index = integrated_verification_indexes[0]
        self.assertLessEqual(
            post_integration_review_index,
            integrated_verification_index,
        )
        verification_step = workflow_steps[integrated_verification_index]
        self.assertRegex(
            verification_step,
            r"(?i)all.{0,120}review gates.{0,120}pass.{0,120}before.{0,80}"
            r"dev-verifier",
        )

        missing_reviewer_blockers = [
            step
            for step in role.instruction_sections["failureHandling"]
            if "task-selected" in step.lower()
            and "reviewer" in step.lower()
            and "unavailable" in step.lower()
            and "BLOCKED" in step
        ]
        self.assertTrue(missing_reviewer_blockers)

        correction_steps = [
            step
            for step in role.instruction_sections["failureHandling"]
            if "replacement committed clean handoff" in step.lower()
            and "dev-merge-coordinator" in step
            and "review" in step.lower()
            and "dev-verifier" in step
            and "complete integrated" in step.lower()
        ]
        self.assertEqual(1, len(correction_steps))
        correction_step = correction_steps[0].lower()
        for phrase in (
            "replacement committed clean handoff",
            "fresh appropriate review",
            "every affected changed surface",
            "complete integrated outcome",
            "same bounded correction loop",
        ):
            with self.subTest(correction_phrase=phrase):
                self.assertIn(phrase, correction_step)
        replacement_index = correction_step.index("replacement committed clean handoff")
        merge_index = correction_step.index("dev-merge-coordinator", replacement_index)
        review_index = correction_step.index("review", merge_index)
        verifier_index = correction_step.index("dev-verifier", review_index)
        self.assertLess(replacement_index, merge_index)
        self.assertLess(merge_index, review_index)
        self.assertLess(review_index, verifier_index)

        failure_text = " ".join(role.instruction_sections["failureHandling"])
        self.assertRegex(
            failure_text,
            r"(?i)after two failed correction attempts",
        )

        artifact_aware_examples = [
            example
            for example in role.examples
            if re.search(
                r"(?i)(?:non-source|mixed|documentation|runbook|wiki)",
                f"{example['purpose']} {example['plausibleResponse']}",
            )
            and "reviewer" in example["plausibleResponse"].lower()
            and "fresh" in example["plausibleResponse"].lower()
            and "context" in example["plausibleResponse"].lower()
        ]
        self.assertTrue(artifact_aware_examples)
        example_response = artifact_aware_examples[0]["plausibleResponse"]
        self.assertIn("dev-code-reviewer", example_response)
        self.assertRegex(
            example_response,
            r"(?i)(?:task-selected|artifact|domain).{0,100}reviewer",
        )
        self.assertIn("dev-verifier", example_response)

    def test_project_wiki_companions_bound_topic_verifier_corrections(self) -> None:
        """Mandatory ingest companions should share one finite verifier retry contract."""
        companion_paths = (
            SKILLS_ROOT / "project-wiki" / "SKILL.md",
            SKILLS_ROOT / "project-wiki" / "references" / "operations.md",
        )

        for path in companion_paths:
            normalized_text = re.sub(
                r"\s+",
                " ",
                path.read_text(encoding="utf-8"),
            )
            with self.subTest(path=path.relative_to(REPOSITORY_ROOT)):
                self.assertRegex(
                    normalized_text,
                    r"(?i)explicit caller or owning-agent correction-attempt cap",
                )
                self.assertRegex(
                    normalized_text,
                    r"(?i)at most two corrected resubmissions after the initial "
                    r"verifier verdict",
                )
                self.assertRegex(
                    normalized_text,
                    r"(?i)(?:exhausted.{0,180}report BLOCKED|"
                    r"report BLOCKED.{0,180}exhausted)",
                )
                self.assertRegex(
                    normalized_text,
                    r"(?i)correction-attempt cap (?:governs each verification "
                    r"gate|to the pre-move verification gate)",
                )
                self.assertRegex(
                    normalized_text,
                    r"(?i)(?:correction-attempt|governing) cap.{0,120}"
                    r"post-move verification gate",
                )
                self.assertRegex(
                    normalized_text,
                    r"(?i)(?:bounded default.{0,120}post-move verification gate|"
                    r"post-move verification gate.{0,320}at most two corrected "
                    r"resubmissions after the initial post-move verdict)",
                )
                self.assertRegex(
                    normalized_text,
                    r"(?i)(?:BLOCKED stop rule.{0,120}post-move verification gate|"
                    r"post-move verification gate.{0,760}exhausted.{0,180}"
                    r"report BLOCKED)",
                )
                self.assertNotRegex(
                    normalized_text,
                    r"(?i)repeat(?: lint plus verification)? until "
                    r"(?:the verifier|it) returns GOOD",
                )

    def test_lifecycle_documents_simplified_coordination_and_delivery_sequences(self) -> None:
        """The lifecycle should teach concepts progressively without runtime-specific clutter."""
        lifecycle_path = (
            REPOSITORY_ROOT / "design" / "orchestrated-development-lifecycle.html"
        )
        lifecycle_text = lifecycle_path.read_text(encoding="utf-8")

        ordered_headings = (
            "Start With The Backlog",
            "The File-Backed Backlog",
            "Agents And Handoffs",
            "Private Branches And Worktrees",
            "Coordinating Shared Resources",
            "Review, Verification, And Delivery",
            "User Decisions Stop Only The Affected Item",
            "Evidence That Proves Delivery",
            "Design And Documentation Work Uses The Same Loop",
        )
        heading_positions = tuple(
            lifecycle_text.index(f">{heading}<") for heading in ordered_headings
        )
        self.assertEqual(tuple(sorted(heading_positions)), heading_positions)

        self.assertEqual(1, lifecycle_text.count('class="lifecycle-rail"'))
        self.assertEqual(1, lifecycle_text.count('class="status-figure"'))
        self.assertEqual(2, lifecycle_text.count('class="sequence-figure"'))
        self.assertEqual(1, lifecycle_text.count('class="branch-figure"'))
        self.assertEqual(1, lifecycle_text.count('class="resource-figure"'))
        self.assertEqual(1, lifecycle_text.count('class="evidence-table"'))
        self.assertEqual(1, lifecycle_text.count("<table"))
        self.assertGreater(lifecycle_text.count('aria-label="sends to"'), 0)

        paragraphs = re.findall(r"<p(?:\s[^>]*)?>(.*?)</p>", lifecycle_text, re.DOTALL)
        paragraph_word_counts = [
            len(re.sub(r"<[^>]+>", " ", paragraph).split())
            for paragraph in paragraphs
        ]
        self.assertTrue(paragraph_word_counts)
        self.assertLessEqual(max(paragraph_word_counts), 60)

        for phrase in (
            "Feature",
            "Defect",
            "Analysis",
            "Investigation",
            "User Action Required",
            "Holding",
            "Blocked",
            "Completed",
            "Awaiting Review",
            "Archive placement is not another lifecycle status",
            "The work item is the only durable task record",
            "Backlog Coordinator",
            "Backlog Steward",
            "Work Orchestrator",
            "Independent Reviewer",
            "Verifier",
            "Merge Coordinator",
            "its own branch in its own worktree",
            "Direct-main delivery",
            "Pull-request delivery",
            "temporary conflict-avoidance scratchpad",
            "not proof of review, verification, delivery, or work-item completion",
            "one cheapest representative first",
            "A user answer resolves the decision gate",
            "An agent runtime session is not another evidence record",
        ):
            with self.subTest(lifecycle_phrase=phrase):
                self.assertIn(phrase, lifecycle_text)

        for obsolete_phrase in (
            "Codex task",
            "One user-visible Dev Orchestrator task",
            "ten are Running",
            "SHARED_CHECKOUT_RELEASE_REQUIRED",
            "ISOLATED_CHECKOUT_SETUP_REQUIRED",
            "DIRTY_CHECKOUT_RECOVERY_AUTHORIZATION_REQUIRED",
            "parent ledger",
            "ARTIFACT GO",
            "ARTIFACT WAIT",
            "ARTIFACT RESUME",
            "LIFECYCLE START",
            ".agents/runs/",
            "claim engine",
            '>Archived</div>',
        ):
            with self.subTest(obsolete_phrase=obsolete_phrase):
                self.assertNotIn(obsolete_phrase, lifecycle_text)

        self.assertIn("@media (prefers-reduced-motion: reduce)", lifecycle_text)
        self.assertIn("@media (prefers-color-scheme: dark)", lifecycle_text)
        self.assertIn("overflow-x: auto", lifecycle_text)

    def test_lifecycle_routes_direct_main_and_pull_request_completion_paths(self) -> None:
        """The lifecycle should distinguish direct-main and pull-request delivery."""
        lifecycle_path = (
            REPOSITORY_ROOT / "design" / "orchestrated-development-lifecycle.html"
        )
        lifecycle_text = lifecycle_path.read_text(encoding="utf-8")

        for phrase in (
            "Direct-main delivery",
            "fresh reconciliation branch from that exact commit",
            "Apply only the accepted paths",
            "exact shared integration paths",
            "Pull-request delivery",
            "authorized reviewer or merge owner",
            "does not acquire a duplicate main-integration claim",
            "Conditional integration role",
            "nested Merge Coordinator",
            "inside the same work item",
            "Re-review reconciled content when integration changes meaning",
            "separate short claim",
            "record Completed",
            "delete the merged branch",
            "refill queue capacity",
        ):
            with self.subTest(delivery_phrase=phrase):
                self.assertIn(phrase, lifecycle_text)

        direct_main = lifecycle_text[
            lifecycle_text.index(">Direct-main delivery<") :
            lifecycle_text.index(">Pull-request delivery<")
        ]
        direct_main_steps = (
            "Review and verify the private candidate",
            "Acquire exact shared integration paths",
            "Under that ownership, refresh current main",
            "Apply only the accepted paths",
        )
        direct_main_positions = tuple(
            direct_main.index(step) for step in direct_main_steps
        )
        self.assertEqual(tuple(sorted(direct_main_positions)), direct_main_positions)

        self.assertIn('table class="evidence-table" aria-labelledby=', lifecycle_text)
        self.assertIn("<caption id=", lifecycle_text)
        self.assertEqual(3, lifecycle_text.count('<th scope="col">'))
        self.assertGreater(lifecycle_text.count('role="img" aria-label="sends to"'), 0)
        self.assertIn("position: static; flex-wrap: wrap", lifecycle_text)

        private_index = lifecycle_text.index(">Private Branches And Worktrees<")
        coordination_index = lifecycle_text.index(">Coordinating Shared Resources<")
        delivery_index = lifecycle_text.index(">Review, Verification, And Delivery<")
        self.assertLess(private_index, coordination_index)
        self.assertLess(coordination_index, delivery_index)

    def test_lifecycle_documents_planned_design_progression(self) -> None:
        lifecycle_text = (
            REPOSITORY_ROOT / "design" / "orchestrated-development-lifecycle.html"
        ).read_text(encoding="utf-8")

        self.assertEqual(
            1,
            lifecycle_text.count(">Design And Documentation Work Uses The Same Loop<"),
        )
        ordered_stages = (
            "Functional intent",
            "Architecture",
            "High-level design",
            "Module design",
            "Implementation",
        )
        planned_text = lifecycle_text[
            lifecycle_text.index(">Design And Documentation Work Uses The Same Loop<") :
        ]
        stage_positions = tuple(
            planned_text.index(f">{stage}<") for stage in ordered_stages
        )
        self.assertEqual(tuple(sorted(stage_positions)), stage_positions)

        for phrase in (
            "Accepted functional specifications and architecture are upstream authority",
            "Create and review high-level and module designs",
            "unresolved high-impact",
            "blocks downstream work",
            "Documentation acceptance and implementation readiness are separate decisions",
            "hybrid-specifications-and-wiki",
            "top-down semantic reconciliation",
            "Documentation Templates",
            "Wiki Skills And Project Context",
            "Agent And Skill Catalog",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, lifecycle_text)

    def test_project_bootstrapper_routes_direct_and_integrated_handoffs(self) -> None:
        """Project bootstrap should preserve distinct single- and multi-contribution gates."""
        build_skill_docs = load_build_skill_docs_module()
        skill_payload = build_skill_docs.build_payload()
        roles = build_skill_docs.load_role_definitions(set(skill_payload["skills"]))
        role = next(role for role in roles if role.name == "project-bootstrapper")
        workflow_steps = list(role.instruction_sections["workflow"])

        single_steps = [
            step
            for step in workflow_steps
            if re.search(
                r"(?i)exactly one accepted committed contribution",
                step,
            )
        ]
        self.assertEqual(1, len(single_steps))
        self.assertIn("final direct commit", single_steps[0].lower())
        self.assertRegex(
            single_steps[0],
            r"(?i)(?:do not invoke|without invoking) dev-merge-coordinator",
        )

        multi_step_indexes = [
            index
            for index, step in enumerate(workflow_steps)
            if "multiple accepted committed contributions" in step.lower()
        ]
        self.assertEqual(1, len(multi_step_indexes))
        multi_step_index = multi_step_indexes[0]
        self.assertIn(
            "dev-merge-coordinator",
            workflow_steps[multi_step_index],
        )

        post_integration_review_indexes = [
            index
            for index, step in enumerate(workflow_steps)
            if index > multi_step_index
            and "multi-contribution integration" in step.lower()
            and "independent" in step.lower()
            and "artifact reviewer" in step.lower()
            and re.search(r"(?i)fresh(?:-| )contexts?", step)
        ]
        self.assertEqual(1, len(post_integration_review_indexes))
        post_integration_review_index = post_integration_review_indexes[0]

        integrated_verification_indexes = [
            index
            for index, step in enumerate(workflow_steps)
            if index >= post_integration_review_index
            and "dev-verifier" in step
            and "complete integrated result" in step.lower()
        ]
        self.assertEqual(1, len(integrated_verification_indexes))
        integrated_verification_index = integrated_verification_indexes[0]
        self.assertLessEqual(
            post_integration_review_index,
            integrated_verification_index,
        )
        if post_integration_review_index == integrated_verification_index:
            combined_gate = workflow_steps[post_integration_review_index].lower()
            self.assertLess(
                combined_gate.index("review"),
                combined_gate.index("dev-verifier"),
            )

        review_text = " ".join(role.instruction_sections["review"])
        for reviewer in (
            "dev-artifact-reviewer",
            "wiki-artifact-reviewer",
            "wiki-topic-verifier",
        ):
            with self.subTest(integrated_reviewer=reviewer):
                self.assertIn(reviewer, review_text)

        completion_text = " ".join(role.instruction_sections["completion"]).lower()
        for completion_term in (
            "final direct commit",
            "final integration commit",
            "clean",
            "release",
        ):
            with self.subTest(completion_term=completion_term):
                self.assertIn(completion_term, completion_text)

        direct_examples = [
            example
            for example in role.examples
            if "final direct commit" in example["plausibleResponse"].lower()
        ]
        self.assertTrue(direct_examples)
        direct_response = direct_examples[0]["plausibleResponse"]
        self.assertRegex(
            direct_response,
            r"(?i)exactly one accepted committed contribution",
        )
        self.assertRegex(
            direct_response,
            r"(?i)dev-merge-coordinator was not invoked",
        )
        self.assertIn("clean status", direct_response.lower())
        self.assertIn("released claims", direct_response.lower())

        integrated_examples = [
            example
            for example in role.examples
            if "final integration commit" in example["plausibleResponse"].lower()
        ]
        self.assertTrue(integrated_examples)
        integrated_response = integrated_examples[0]["plausibleResponse"]
        self.assertIn(
            "multiple accepted committed contributions",
            integrated_response.lower(),
        )
        self.assertIn("dev-merge-coordinator", integrated_response)
        integration_tail = integrated_response.split(
            "dev-merge-coordinator",
            maxsplit=1,
        )[1]
        for reviewer in (
            "dev-artifact-reviewer",
            "wiki-artifact-reviewer",
            "wiki-topic-verifier",
        ):
            with self.subTest(integrated_example_reviewer=reviewer):
                self.assertIn(reviewer, integration_tail)
        self.assertRegex(integration_tail, r"(?i)fresh(?:-| )contexts?")
        self.assertIn("dev-verifier", integration_tail)
        self.assertLess(
            integration_tail.lower().index("review"),
            integration_tail.index("dev-verifier"),
        )
        self.assertIn("complete integrated result", integration_tail.lower())
        self.assertIn("clean status", integrated_response.lower())
        self.assertIn("released claims", integrated_response.lower())

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
        self.assertIn("For reverse engineering, require the project configuration pass", role.instructions)
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
            "wiki-ingester",
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
                "wiki-ingester",
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
        self.assertEqual(5, len(role.examples))
        self.assertTrue(role.examples[0]["plausibleResponse"].startswith("STATUS: READY"))
        self.assertTrue(role.examples[1]["plausibleResponse"].startswith("STATUS: READY"))
        self.assertIn("STATUS: BLOCKED", role.examples[2]["plausibleResponse"])
        self.assertTrue(role.examples[3]["plausibleResponse"].startswith("STATUS: READY"))
        self.assertIn("valid existing routing", role.examples[0]["purpose"])
        self.assertIn("no project routing", role.examples[1]["purpose"])
        self.assertIn("invalid", role.examples[2]["purpose"])
        self.assertIn("authorized", role.examples[3]["purpose"])
        for example in role.examples:
            self.assertTrue(example["runtimeInvocations"]["codex"].startswith("$project_bootstrapper "))
            self.assertTrue(
                example["runtimeInvocations"]["claude-code"].startswith(
                    "@agent-project-bootstrapper "
                )
            )

    def test_dev_verifier_loads_prompt_contracts_conditionally(self) -> None:
        build_skill_docs = load_build_skill_docs_module()
        skill_payload = build_skill_docs.build_payload()
        roles = build_skill_docs.load_role_definitions(set(skill_payload["skills"]))
        role = next(role for role in roles if role.name == "dev-verifier")

        self.assertNotIn(
            "documentation-reverse-engineer",
            build_skill_docs.fixed_role_skills(role),
        )
        self.assertNotIn(
            "prompt-contracts",
            build_skill_docs.fixed_role_skills(role),
        )
        self.assertNotIn("documentation-reverse-engineer", role.skill_conditions)
        self.assertIn("prompt-contracts", role.skill_conditions)
        self.assertIn("model-facing evaluator", role.skill_conditions["prompt-contracts"])
        self.assertIn("model-facing evaluator", role.instructions)
        self.assertEqual(2, len(role.examples))

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
            } | set(CORE_PATTERN_SKILLS),
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
            {"simple", "default", "documentation", "advanced", "advanced-long"},
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

        self.assertEqual(
            {
                "simple": "gpt-5.6-luna",
                "default": "gpt-5.6-terra",
                "documentation": "gpt-5.6-sol",
                "advanced": "gpt-5.6-sol",
                "advanced-long": "gpt-5.6-sol",
            },
            {
                profile_name: profile["model"]
                for profile_name, profile in adapter_profiles["codex"].items()
            },
        )

        for role_path in sorted((REPOSITORY_ROOT / "agents" / "roles").glob("*/*.role.yaml")):
            with self.subTest(role_path=role_path):
                role = load_yaml_object(role_path)
                self.assertIn(role["modelProfile"], source_profiles)
                self.assertNotIn("model", role)
                self.assertNotIn("effort", role)
                for profile in role.get("modelStages", {}).values():
                    self.assertIn(profile, source_profiles)

    def test_dev_documentation_writer_uses_dedicated_model_profile(self) -> None:
        build_skill_docs = load_build_skill_docs_module()
        skill_names = set(build_skill_docs.build_payload()["skills"])
        roles = build_skill_docs.load_role_definitions(skill_names)
        writer = next(role for role in roles if role.name == "dev-documentation-writer")
        unrelated_roles = [role for role in roles if role.name != writer.name]
        source_profile_ids = set(build_skill_docs.load_model_profiles())

        self.assertEqual("documentation", writer.model_profile)
        self.assertTrue(all(role.model_profile != "documentation" for role in unrelated_roles))

        expected_profiles = {
            "codex": {
                "simple": ("gpt-5.6-luna", "medium"),
                "default": ("gpt-5.6-terra", "medium"),
                "documentation": ("gpt-5.6-sol", "high"),
                "advanced": ("gpt-5.6-sol", "high"),
                "advanced-long": ("gpt-5.6-sol", "high"),
            },
            "claude": {
                "simple": ("fable-5", None),
                "default": ("sonnet-5", None),
                "documentation": ("fable-5", None),
                "advanced": ("opus-4.8", None),
                "advanced-long": ("opus-4.8", None),
            },
            "gemini": {
                "simple": ("flash", None),
                "default": ("auto", None),
                "documentation": ("auto", None),
                "advanced": ("pro", None),
                "advanced-long": ("pro", None),
            },
            "junie": {
                "simple": ("gemini-flash", "low"),
                "default": ("sonnet", "medium"),
                "documentation": ("gpt-5.6-sol", "high"),
                "advanced": ("opus", "high"),
                "advanced-long": ("opus", "high"),
            },
        }

        profiles_by_adapter = {
            adapter: build_skill_docs.load_adapter_model_profiles(adapter, source_profile_ids)
            for adapter in expected_profiles
        }
        for adapter, expected in expected_profiles.items():
            with self.subTest(adapter=adapter):
                self.assertEqual(
                    expected,
                    {
                        profile_id: (profile.model, profile.effort)
                        for profile_id, profile in profiles_by_adapter[adapter].items()
                    },
                )

        codex_text = build_skill_docs.render_codex_agent(
            writer,
            profiles_by_adapter["codex"],
            known_role_names=tuple(role.name for role in roles),
        )
        self.assertIn('model = "gpt-5.6-sol"', codex_text)
        self.assertIn('model_reasoning_effort = "high"', codex_text)

        claude_frontmatter = yaml.safe_load(
            build_skill_docs.render_claude_agent(
                writer, profiles_by_adapter["claude"]
            ).split("---", 2)[1]
        )
        self.assertEqual("fable-5", claude_frontmatter["model"])

        gemini_frontmatter = yaml.safe_load(
            build_skill_docs.render_gemini_agent(
                writer, profiles_by_adapter["gemini"]
            ).split("---", 2)[1]
        )
        self.assertEqual("auto", gemini_frontmatter["model"])

        junie_frontmatter = yaml.safe_load(
            build_skill_docs.render_junie_agent(
                writer, profiles_by_adapter["junie"]
            ).split("---", 2)[1]
        )
        self.assertEqual("gpt-5.6-sol", junie_frontmatter["model"])
        self.assertEqual("high", junie_frontmatter["reasoningLevel"])

    def test_agent_skill_evals_cover_implementation_and_independent_review(self) -> None:
        """Code-delivery fixtures keep coding contracts without imposing them on other workflows."""
        evals = load_yaml_object(REPOSITORY_ROOT / "evals" / "cases.yaml")["cases"]
        by_id = {case["id"]: case for case in evals}

        self.assertIn("typescript-order-pricing", by_id)
        self.assertIn("spring-boot-order-cancellation", by_id)
        code_delivery_cases = [
            case
            for case in by_id.values()
            if case.get("workflowPack") in {None, "code-delivery"}
        ]
        for case in code_delivery_cases:
            with self.subTest(code_comments_case=case["id"]):
                self.assertIn("code-comments", case["requiredSkills"])
        review_case = by_id["typescript-code-review"]
        self.assertTrue(review_case["expectVerifyFailure"])
        self.assertIn("code-review-evidence", review_case["requiredSkills"])
        self.assertEqual(3, len(review_case["requiredFindings"]))

        file_boundary_case = by_id["file-work-item-no-mutation"]
        self.assertEqual(
            ["dev-backlog-steward-provider-boundary"],
            file_boundary_case["agentScenarios"],
        )
        self.assertEqual([], file_boundary_case["fixtureBackedProbeClaims"])
        self.assertEqual(["eval-result.md"], file_boundary_case["allowedWritePaths"])
        self.assertEqual(
            {"create-file-work-item", "manage-file-work-items"},
            set(file_boundary_case["requiredSkills"]) - {"structured-explanation"},
        )

        probes = load_yaml_object(REPOSITORY_ROOT / "evals" / "skill-probes.yaml")
        probes_by_id = {probe["id"]: probe for probe in probes["probes"]}
        self.assertEqual(
            "declared",
            probes_by_id["probe-create-file-work-item"]["coverageStatus"],
        )
        self.assertEqual(
            ["backlog-lifecycle"],
            probes_by_id["probe-manage-file-work-items"]["executableCases"],
        )

    def test_agent_owned_eval_suites_hardcode_steady_state_orchestration(self) -> None:
        """Agent-first suites must keep target, supervisor, Judge, skill, and concurrency contracts explicit."""
        index = load_yaml_object(AGENT_TEST_SUITES_ROOT / "suite-index.yaml")
        execution = index["execution"]
        self.assertEqual(4, execution["maximumConcurrentSupervisors"])
        self.assertEqual(1, execution["maximumActiveChildrenPerSupervisor"])
        self.assertEqual(9, execution["normalMaximumActiveAgents"])
        self.assertEqual(10, execution["temporaryMaximumActiveAgents"])

        expected_suites = [
            "dev-coder",
            "dev-code-reviewer",
            "dev-runtime-diagnostician",
            "project-bootstrapper",
            "dev-verifier",
            "dev-orchestrator",
            "project-configurator",
            "dev-security-reviewer",
            "dev-backlog-steward",
            "dev-merge-coordinator",
            "dev-documentation-writer",
            "wiki-ingester",
            "wiki-writer",
            "wiki-query-responder",
            "dev-artifact-reviewer",
            "dev-prompt-reviewer",
            "dev-ux-specialist",
            "dev-browser-operator",
            "project-organiser",
            "wiki-architect",
            "wiki-topic-verifier",
            "wiki-artifact-reviewer",
            "wiki-researcher",
            "wiki-source-collector",
            "methodology-maintainer",
            "methodology-artifact-reviewer",
            "dev-backlog-coordinator",
        ]
        suite_entries = index["suites"]
        self.assertEqual(expected_suites, [entry["id"] for entry in suite_entries])
        self.assertEqual(list(range(1, 28)), [entry["priority"] for entry in suite_entries])
        suite_directories = {
            path.name
            for path in AGENT_TEST_SUITES_ROOT.iterdir()
            if path.is_dir() and path.name not in {"results", "skills"} and not path.name.startswith("__")
        }
        self.assertEqual(set(expected_suites), suite_directories)

        protocol = (AGENT_TEST_SUITES_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        for phrase in (
            "at most four suite supervisors concurrently",
            "exactly one active child agent at a time",
            "normal ceiling is nine active agents",
            "temporary tenth agent",
            "The Judge is read-only and independent",
            "isolated CODEX_HOME agents directory",
            "matching task name alone does not satisfy the identity gate",
            "missing applicable skill is a critical preflight BLOCKED result",
            "Exactly one authoritative scenario catalog named scenarios.yaml",
            "Route a finding about the canonical agent definition",
            "correct only that infrastructure",
        ):
            with self.subTest(protocol_phrase=phrase):
                self.assertIn(phrase, protocol)

        shared_skill_paths = [AGENT_TEST_SUITES_ROOT / path for path in index["sharedSkills"]]
        for skill_path in shared_skill_paths:
            with self.subTest(shared_skill=skill_path):
                frontmatter = load_yaml_object_from_frontmatter(skill_path)
                self.assertEqual(skill_path.parent.name, frontmatter["name"])

        evidence_judging = (
            AGENT_TEST_SUITES_ROOT
            / "skills"
            / "agent-evidence-judging"
            / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("The runner owns ordered runtime traces", evidence_judging)
        self.assertIn("corrected harness-only retry", evidence_judging)
        wiki_research_contract = (
            AGENT_TEST_SUITES_ROOT
            / "wiki-researcher"
            / "skills"
            / "wiki-researcher-suite-contract"
            / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Do not require an unavailable target-internal tool trace", wiki_research_contract)

        readme_text = (AGENT_TEST_SUITES_ROOT / "README.md").read_text(encoding="utf-8")
        self.assertNotRegex(readme_text, r"(?i)\bwave\b")
        self.assertIn("one authoritative scenarios.yaml catalog", readme_text)
        self.assertTrue(
            (AGENT_TEST_SUITES_ROOT / "results" / "2026-07-17-codex-agent-suites.md").is_file()
        )
        completion_report = (
            AGENT_TEST_SUITES_ROOT
            / "results"
            / "2026-07-17-complete-agent-suites.md"
        )
        self.assertTrue(completion_report.is_file())
        implementation_plan = (
            AGENT_TEST_SUITES_ROOT / "implementation-plan.md"
        ).read_text(encoding="utf-8")
        self.assertIn("26 of 26 suites complete", implementation_plan)
        self.assertIn("78 of 78 scenarios executed", implementation_plan)
        scenario_design = (
            AGENT_TEST_SUITES_ROOT
            / "skills"
            / "agent-scenario-design"
            / "SKILL.md"
        ).read_text(encoding="utf-8")
        supervision = (
            AGENT_TEST_SUITES_ROOT
            / "skills"
            / "agent-suite-supervision"
            / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("conditionally pending the runner post-audit", supervision)
        self.assertIn("exactly one authoritative scenario catalog named scenarios.yaml", scenario_design)
        self.assertIn("authoritative scenarios.yaml catalog", supervision)
        self.assertIn("Send agent-definition", supervision)
        self.assertIn("Correct only test infrastructure", supervision)
        self.assertIn("checkpointRoot at suite-id/scenario-id.json", supervision)
        self.assertIn("exactly 64 lowercase hexadecimal characters", supervision)
        self.assertIn("repository-global status as the sole mutation gate", supervision)
        self.assertIn("ordered target tool-call trace", supervision)
        self.assertTrue((AGENT_TEST_SUITES_ROOT / "runner.py").is_file())
        self.assertTrue((AGENT_TEST_SUITES_ROOT / "test_runner.py").is_file())
        legacy_case_ids = {
            str(case["id"])
            for case in load_yaml_object(REPOSITORY_ROOT / "evals" / "cases.yaml")["cases"]
        }

        for entry in suite_entries:
            suite_root = AGENT_TEST_SUITES_ROOT / entry["path"]
            suite = load_yaml_object(suite_root / "suite.yaml")
            scenarios = load_yaml_object(suite_root / "scenarios.yaml")
            target = suite["target"]
            role = load_yaml_object(REPOSITORY_ROOT / target["conceptualRole"])

            with self.subTest(suite=entry["id"]):
                self.assertEqual(entry["id"], suite["id"])
                self.assertEqual(entry["id"], role["filename"])
                self.assertTrue((REPOSITORY_ROOT / target["nativeAgent"]).is_file())
                self.assertEqual(1, suite["execution"]["maximumActiveChildren"])
                self.assertTrue(suite["execution"]["requireCodexIdentityEvidence"])
                self.assertEqual(
                    role.get("agentDependencies", []),
                    target["allowedAgentDependencies"],
                )
                self.assertEqual(entry["id"], scenarios["suite"])
                if entry["id"] == "dev-code-reviewer":
                    self.assertEqual(4, len(scenarios["scenarios"]))
                    self.assertEqual(
                        {
                            "seeded-typescript-defects",
                            "justified-clean-review",
                            "incomplete-review-evidence",
                            "header-policy-authority-boundary",
                        },
                        {
                            scenario["id"]
                            for scenario in scenarios["scenarios"]
                        },
                    )
                elif entry["id"] == "dev-backlog-steward":
                    self.assertEqual(6, len(scenarios["scenarios"]))
                elif entry["id"] == "project-bootstrapper":
                    self.assertEqual(4, len(scenarios["scenarios"]))
                    self.assertEqual(
                        {
                            "valid-configuration-direct-path",
                            "missing-configuration-multi-contribution",
                            "whole-project-reverse-engineering-steady-state",
                            "invalid-configuration-no-authority",
                        },
                        {
                            scenario["id"]
                            for scenario in scenarios["scenarios"]
                        },
                    )
                elif entry["id"] == "wiki-ingester":
                    self.assertEqual(4, len(scenarios["scenarios"]))
                    self.assertEqual(
                        {
                            "raw-ingest",
                            "destination-collision",
                            "verifier-failure",
                            "final-evidence-audit-read-only",
                        },
                        {
                            scenario["id"]
                            for scenario in scenarios["scenarios"]
                        },
                    )
                else:
                    self.assertEqual(3, len(scenarios["scenarios"]))

            for scenario in scenarios["scenarios"]:
                executable_case = scenario.get("executableCase")
                with self.subTest(
                    suite=entry["id"],
                    executable_scenario=scenario["id"],
                ):
                    self.assertIn(scenario["status"], {"executable", "fixture-backed"})
                    self.assertIsInstance(executable_case, str)
                    self.assertTrue(
                        (suite_root / executable_case).exists() or executable_case in legacy_case_ids
                    )

            for agent_kind, relative_path in suite["projectAgents"].items():
                agent_path = suite_root / relative_path
                with self.subTest(suite=entry["id"], agent=agent_kind):
                    agent = tomllib.loads(agent_path.read_text(encoding="utf-8"))
                    self.assertEqual(
                        f"{entry['id']}-suite-{agent_kind}".replace("-", "_"),
                        agent["name"],
                    )
                    self.assertRegex(agent["name"], r"^[a-z0-9_]+$")
                    self.assertIn("developer_instructions", agent)
                    if agent_kind == "judge":
                        self.assertEqual("read-only", agent["sandbox_mode"])

            execution = suite["execution"]
            self.assertEqual(
                f"{entry['id']}-suite-supervisor".replace("-", "_"),
                execution["supervisorInvocation"],
            )
            self.assertEqual(
                entry["id"].replace("-", "_"),
                execution["targetInvocation"],
            )
            self.assertEqual(
                f"{entry['id']}-suite-judge".replace("-", "_"),
                execution["judgeInvocation"],
            )

            if entry["id"] == "dev-coder":
                first_scenario = scenarios["scenarios"][0]
                self.assertIn("organise-project-files", first_scenario["targetSkills"])

            configured_skills = [
                *suite["projectSkills"]["shared"],
                *suite["projectSkills"]["suite"],
            ]
            for relative_path in configured_skills:
                skill_path = suite_root / relative_path
                with self.subTest(suite=entry["id"], project_skill=relative_path):
                    frontmatter = load_yaml_object_from_frontmatter(skill_path)
                    self.assertEqual(skill_path.parent.name, frontmatter["name"])

    def test_support_checklist_covers_every_agent_and_skill(self) -> None:
        """The generated report must expose every live declaration without inflating evidence."""
        checklist = SUPPORT_CHECKLIST_PATH.read_text(encoding="utf-8")
        agent_section = checklist.split("## Agent Checklist", 1)[1].split(
            "## Bundled Skill Checklist", 1
        )[0]
        skill_section = checklist.split("## Bundled Skill Checklist", 1)[1].split(
            "## Technology Detection Registry", 1
        )[0]
        role_paths = sorted(
            (REPOSITORY_ROOT / "agents" / "roles").glob("*/*.role.yaml")
        )
        skill_paths = sorted(SKILLS_ROOT.glob("*/SKILL.md"))

        self.assertIn(
            f"- [x] {len(role_paths)} conceptual agents and {len(skill_paths)} bundled skills have structural coverage.",
            checklist,
        )
        for phrase in (
            "Probe-declared",
            "Scenario-declared",
            "Positive case",
            "Negative case",
            "Paired controls",
            "Full probe",
            "All scenarios backed",
            "Executable full fixture",
            "Judge calibration",
            "Executed",
            "Judge-passed",
            "Security-contained",
            "Stale-by-digest",
        ):
            with self.subTest(status=phrase):
                self.assertIn(phrase, checklist)
        self.assertIn("Evaluation execution support is limited to Codex and Junie.", checklist)
        cases = load_yaml_object(REPOSITORY_ROOT / "evals" / "cases.yaml")["cases"]
        runnable_by_harness = {
            harness: sum(
                case.get("harnessExecutionStatus", {}).get(harness) == "runnable"
                for case in cases
            )
            for harness in ("codex", "junie")
        }
        self.assertIn(
            f"{runnable_by_harness['codex']} cases can run locally through Codex and "
            f"{runnable_by_harness['junie']} can run locally through Junie.",
            checklist,
        )
        self.assertNotIn("Every post-run verification command still requires trusted external containment.", checklist)
        self.assertNotIn("| Claude Code |", checklist)
        self.assertNotIn("| Gemini CLI |", checklist)

        for role_path in role_paths:
            role = load_yaml_object(role_path)
            with self.subTest(agent=role["name"]):
                self.assertIn(f"| {role['name']} |", agent_section)

        for skill_path in skill_paths:
            skill_name = load_yaml_object_from_frontmatter(skill_path)["name"]
            with self.subTest(skill=skill_name):
                self.assertIn(f"| {skill_name} | [x] | [x] ", skill_section)


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

        modularization_text = page_text["skills-modularization.html"]
        for phrase in MODULARIZATION_REQUIRED_PHRASES:
            with self.subTest(modularization_phrase=phrase):
                self.assertIn(phrase, modularization_text)

        modularization_section_order = (
            "Core Agent Skills",
            "Technology Extension Skills",
            "Why Technology-Specific Skills Are Loaded Separately",
            "Skill Inlining Benefits",
            "Technology Extensions Setup Process",
            "How Setup-Time Technology Detection Works",
        )
        modularization_section_positions = tuple(
            modularization_text.index(f">{heading}</h2>")
            for heading in modularization_section_order
        )
        self.assertEqual(
            tuple(sorted(modularization_section_positions)),
            modularization_section_positions,
        )
        technology_section = modularization_text.split(
            '<section class="section" aria-labelledby="technology-examples-title">',
            maxsplit=1,
        )[1].split("</section>", maxsplit=1)[0]
        for skill_name in TECHNOLOGY_EXTENSION_SKILLS:
            with self.subTest(technology_extension_skill=skill_name):
                self.assertEqual(
                    1,
                    technology_section.count(
                        f'data-skill-definition="{skill_name}"'
                    ),
                )
        core_section = modularization_text.split(
            '<section class="section" aria-labelledby="agent-skills-title">',
            maxsplit=1,
        )[1].split("</section>", maxsplit=1)[0]
        for skill_name in CORE_PATTERN_SKILLS:
            with self.subTest(core_pattern_skill=skill_name):
                self.assertEqual(
                    1,
                    core_section.count(f'data-skill-definition="{skill_name}"'),
                )
        self.assertIn(
            '<script src="generated/skill-definitions.js"></script>',
            modularization_text,
        )
        self.assertIn(
            '<script src="skill-browser.js"></script>',
            modularization_text,
        )

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

        for filename, required_links in DOCUMENT_REQUIRED_CONTENT_LINKS.items():
            for link in required_links:
                with self.subTest(filename=filename, required_link=link):
                    self.assertIn(f'href="{link}', page_text[filename])

        wiki_context_path = design_root / "wiki-skills-and-project-context.html"
        wiki_context_hrefs = set(
            re.findall(
                r'href="([^"]+)"',
                page_text["wiki-skills-and-project-context.html"],
            )
        )
        for link in DOCUMENT_REQUIRED_CONTENT_LINKS[
            "wiki-skills-and-project-context.html"
        ]:
            with self.subTest(wiki_context_exact_link=link):
                self.assertIn(link, wiki_context_hrefs)
            if not link.startswith("../"):
                continue
            with self.subTest(wiki_context_local_link=link):
                actual_link = next(href for href in wiki_context_hrefs if href == link)
                local_target = (wiki_context_path.parent / actual_link).resolve()
                self.assertTrue(
                    local_target.is_file(),
                    f"Wiki context link does not resolve: {link}",
                )

        template_page_text = page_text["documentation-templates.html"]
        for template_name in DOCUMENTATION_TEMPLATE_FILENAMES:
            with self.subTest(template_modal_trigger=template_name):
                self.assertEqual(
                    1,
                    template_page_text.count(
                        f'data-template-definition="{template_name}"'
                    ),
                )
        self.assertIn(
            '<script src="generated/template-definitions.js"></script>',
            template_page_text,
        )
        self.assertIn(
            '<script src="template-browser.js"></script>',
            template_page_text,
        )

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
        expected_index_owners = (
            "catalog",
            "configuration",
            "modularization",
            "agent-definitions",
            "examples",
            "execution",
            "templates",
            "wiki-context",
        )
        index_owners = tuple(
            re.findall(
                r'<a class="doc-card [^"]+" data-information-owner="([^"]+)"',
                index_text,
            )
        )
        self.assertEqual(expected_index_owners, index_owners)
        index_pages = tuple(
            re.findall(
                r'<a class="doc-card [^"]+" data-information-owner="[^"]+" '
                r'href="design/([^"]+)">',
                index_text,
            )
        )
        self.assertEqual(tuple(DOCUMENT_INFORMATION_OWNERS), index_pages)

        for position, filename in enumerate(index_pages):
            text = page_text[filename]
            with self.subTest(document_navigation=filename):
                self.assertEqual(
                    1,
                    text.count(
                        '<nav class="document-nav" '
                        'aria-label="Documentation navigation">'
                    ),
                )
                self.assertIn(
                    '<a href="../index.html">Back to Documentation Index</a>',
                    text,
                )
                self.assertEqual(
                    1,
                    text.count('<div class="document-sequence">'),
                )
                nav = text.split(
                    '<nav class="document-nav" '
                    'aria-label="Documentation navigation">',
                    maxsplit=1,
                )[1].split("</nav>", maxsplit=1)[0]
                sequence = nav.split(
                    '<div class="document-sequence">', maxsplit=1
                )[1].split("</div>", maxsplit=1)[0]
                self.assertLess(
                    nav.index("Back to Documentation Index"),
                    nav.index('<div class="document-sequence">'),
                )

                if position == 0:
                    self.assertNotIn('rel="prev"', sequence)
                else:
                    self.assertIn(
                        f'<a href="{index_pages[position - 1]}" rel="prev">',
                        sequence,
                    )

                if position == len(index_pages) - 1:
                    self.assertNotIn('rel="next"', sequence)
                else:
                    self.assertIn(
                        f'<a href="{index_pages[position + 1]}" rel="next">',
                        sequence,
                    )

                hero = text.split('<section class="hero"', maxsplit=1)[1].split(
                    "</section>", maxsplit=1
                )[0]
                self.assertNotIn("<a ", hero)
                for badge_marker in (
                    'class="legend"',
                    'class="pill-row"',
                    'class="pill"',
                ):
                    self.assertNotIn(badge_marker, hero)
        for owner in expected_index_owners:
            with self.subTest(index_owner=owner):
                self.assertEqual(
                    1,
                    index_text.count(f'data-information-owner="{owner}"'),
                )

        self.assertIn("<title>AI-Assisted Coding Toolkit</title>", index_text)
        self.assertIn(
            '<h1 id="page-title">AI-Assisted Coding Toolkit</h1>',
            index_text,
        )
        self.assertIn("<h3>Core Agent and Skills</h3>", index_text)
        self.assertIn("<h3>Technology Skills</h3>", index_text)

        expected_gradient = (
            "linear-gradient(180deg, rgba(232, 240, 255, 0.9), "
            "rgba(246, 248, 251, 0) 340px)"
        )
        html_pages = {"index.html": index_text, **page_text}
        for filename, text in html_pages.items():
            with self.subTest(site_chrome=filename):
                self.assertEqual(1, text.count('<header class="site-header">'))
                self.assertEqual(1, text.count('<footer class="site-footer">'))
                self.assertIn("AI-Assisted Coding Toolkit", text)
                self.assertEqual(1, text.count(expected_gradient))
                if filename == "index.html":
                    self.assertIn('src="logo.png"', text)
                    self.assertIn('href="LICENSE">MIT License</a>', text)
                else:
                    self.assertIn('src="../logo.png"', text)
                    self.assertIn('href="../LICENSE">MIT License</a>', text)

        license_text = (REPOSITORY_ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("MIT License", license_text)
        self.assertIn(
            "Copyright (c) 2026 Martin.Bechard@DevConsult.ca",
            license_text,
        )
        self.assertNotIn('class="summary"', index_text)
        self.assertNotIn('class="pill"', index_text)
        self.assertIn('aria-hidden="true">07</span>', index_text)
        for retired_page in (
            "agent-role-skill-map.html",
            "agentic-development-operating-model.html",
            "agent-skill-specialization-strategy.html",
        ):
            with self.subTest(retired_page=retired_page):
                self.assertFalse((design_root / retired_page).exists())

        self.assertIn(
            "deliberately present the same definition-to-skill relationships in two generated views",
            page_text["agent-and-skill-definitions.html"],
        )

    def test_html_documentation_loads_accessible_persistent_settings(self) -> None:
        settings_text = DOCUMENTATION_SETTINGS_PATH.read_text(encoding="utf-8")
        design_pages = tuple((REPOSITORY_ROOT / "design").glob("*.html"))

        self.assertIn(
            '<script src="design/documentation-settings.js"></script>',
            (REPOSITORY_ROOT / "index.html").read_text(encoding="utf-8"),
        )
        for page_path in design_pages:
            with self.subTest(settings_consumer=page_path.name):
                self.assertIn(
                    '<script src="documentation-settings.js"></script>',
                    page_path.read_text(encoding="utf-8"),
                )

        for phrase in (
            "Copyright (c) 2026 Martin.Bechard@DevConsult.ca",
            "DEV_METHODOLOGY_DOCUMENTATION_SETTINGS",
            "dev-methodology.documentation.default-harness",
            "dev-methodology.documentation.editor",
            'trigger.setAttribute("aria-label", "Settings")',
            'trigger.setAttribute("aria-expanded", "false")',
            'dialog.setAttribute("role", "dialog")',
            'dialog.setAttribute("aria-modal", "true")',
            'harnessLabel.textContent = "Default harness"',
            'editorLabel.textContent = "Editor"',
            'const KEY_ESCAPE = "Escape"',
            'const KEY_TAB = "Tab"',
            "storage.getItem",
            "storage.setItem",
            'return `idea://open?file=${encodeURIComponent(filePath)}`;',
        ):
            with self.subTest(documentation_settings_phrase=phrase):
                self.assertIn(phrase, settings_text)

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
            REPOSITORY_ROOT / "design" / "agent-and-skill-definitions.html"
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
            "View conceptual agent definition YAML",
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

        template_browser_text = TEMPLATE_BROWSER_PATH.read_text(encoding="utf-8")
        for phrase in (
            "Copyright (c) 2026 Martin.Bechard@DevConsult.ca",
            "AI attribution: Generated with AI assistance.",
            "Design: design/documentation-templates.html",
            "DEV_METHODOLOGY_TEMPLATE_DEFINITIONS",
            "[data-template-definition]",
            'aria-modal="true"',
            "aria-haspopup",
            "Open source",
            "Escape",
            "Tab",
            "lastFocusedElement.focus",
            "template-modal-open",
            ".template-modal__content code {",
        ):
            with self.subTest(template_browser_phrase=phrase):
                self.assertIn(phrase, template_browser_text)
        template_code_foreground = css_hex_property(
            template_browser_text,
            ".template-modal__content",
            "color",
        )
        template_code_background = css_hex_property(
            template_browser_text,
            ".template-modal__content",
            "background",
        )
        self.assertGreaterEqual(
            wcag_contrast_ratio(
                template_code_foreground,
                template_code_background,
            ),
            4.5,
        )

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

        for runtime_heading in (
            "Knowledge Structure",
            "Skills And Agent Definitions",
            "Runtime Configuration File Locations",
        ):
            with self.subTest(runtime_heading=runtime_heading):
                self.assertNotIn(runtime_heading, definition_text)

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

    def test_agentic_configuration_document_describes_runtime_files(self) -> None:
        index_text = (REPOSITORY_ROOT / "index.html").read_text(encoding="utf-8")
        configuration_text = (
            REPOSITORY_ROOT / "design" / "agentic-configuration.html"
        ).read_text(encoding="utf-8")

        self.assertIn("design/agentic-configuration.html", index_text)
        self.assertIn(
            "skills, agent definitions, and project instructions",
            index_text,
        )
        for phrase in AGENTIC_CONFIGURATION_REQUIRED_PHRASES:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, configuration_text)

        self.assertNotIn("PROJECT.md", configuration_text)
        self.assertNotIn("agents/*.toml", configuration_text)
        self.assertNotIn("agents/*.md", configuration_text)
        self.assertNotIn("Generated Code", configuration_text)

        layer_section = configuration_text.split(
            '<ol class="context-layers">', maxsplit=1
        )[1].split("</section>", maxsplit=1)[0]
        layer_headings = (
            ("h3", "Shared Definitions"),
            ("h4", "Skill Definition Files"),
            ("h4", "Agent Definition Files"),
            ("h3", "Project-Specific Definitions"),
            ("h4", "Project Skill Definition Files"),
            ("h4", "Project Agent Definition Files"),
            ("h4", "Root Project Instruction Files"),
            ("h4", "Nested Project Instruction Files"),
        )
        layer_positions = [
            layer_section.index(f"<{tag}>{heading}</{tag}>")
            for tag, heading in layer_headings
        ]
        self.assertEqual(sorted(layer_positions), layer_positions)
        self.assertEqual(2, layer_section.count('<ol class="nested-layers">'))
        for redundant_heading in (
            "Skills Describe How To Perform Actions",
            "Agent Configuration",
            "Shared And Project Definitions",
        ):
            with self.subTest(redundant_heading=redundant_heading):
                self.assertNotIn(redundant_heading, configuration_text)
        for source_heading in (
            "The Portability Problem",
            "From Conceptual Agent Definitions To Native Agent Definitions",
            "Conceptual-To-Native Property Mapping",
        ):
            with self.subTest(source_heading=source_heading):
                self.assertNotIn(source_heading, configuration_text)

        locations_section = configuration_text.split(
            '<section class="section" aria-labelledby="locations-title">', maxsplit=1
        )[1].split("</section>", maxsplit=1)[0]
        purpose_headings = (
            "Skill Definition Files",
            "Agent Definition Files",
            "Root Project Instruction Files",
            "Nested Project Instruction Files",
        )
        purpose_positions = [
            locations_section.index(f'<th colspan="4" scope="rowgroup">{heading}')
            for heading in purpose_headings
        ]
        self.assertEqual(sorted(purpose_positions), purpose_positions)

        harnesses = ("codex", "claude", "gemini", "junie", "copilot")
        harness_rows = re.findall(
            r'<tr data-harness-row data-harness="([^"]+)">',
            locations_section,
        )
        self.assertEqual(20, len(harness_rows))
        for harness in harnesses:
            with self.subTest(harness=harness):
                self.assertEqual(4, harness_rows.count(harness))
                self.assertIn(f'<option value="{harness}">', locations_section)

        self.assertIn(
            'row.hidden = selectedHarness !== "all" && row.dataset.harness !== selectedHarness;',
            configuration_text,
        )
        self.assertIn(
            'harnessFilter.addEventListener("change", () => {',
            configuration_text,
        )
        self.assertIn(
            'settings.set("harness", filterHarnessToSettings[harnessFilter.value]);',
            configuration_text,
        )
        self.assertNotIn("Markdown agent definition", locations_section)
        self.assertNotIn("TOML agent definition", locations_section)
        self.assertIsNone(re.search(r"\bnative\b", configuration_text, re.IGNORECASE))
        self.assertNotIn(".claude/rules", configuration_text)
        self.assertNotIn("&lt;project-root&gt;/.claude/CLAUDE.md", configuration_text)

    def test_reverse_engineering_uses_structural_code_discovery(self) -> None:
        skill_text = (
            SKILLS_ROOT / "documentation-reverse-engineer" / "SKILL.md"
        ).read_text(encoding="utf-8")

        for phrase in REVERSE_ENGINEERING_DISCOVERY_PHRASES:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, skill_text)

    def test_reverse_engineering_requires_full_gated_coverage(self) -> None:
        reverse_skill_text = (
            SKILLS_ROOT / "documentation-reverse-engineer" / "SKILL.md"
        ).read_text(encoding="utf-8")
        bootstrap_skill_text = (
            SKILLS_ROOT / "documentation-bootstrap" / "SKILL.md"
        ).read_text(encoding="utf-8")

        required_reverse_phrases = (
            "Whole-repository reverse engineering is exhaustive",
            "Inventory every tracked path",
            "path ledger and coverage manifest must reconcile mechanically in both directions",
            "Higher-level synthesis never substitutes for missing lower-level coverage",
            "Pass -1: Project Configuration",
            "Pass 0: Repository Orientation",
            "Pass 1: Module Designs",
            "Pass 2: High-Level Designs",
            "Pass 3: Architecture",
            "Pass 4: Functional Specifications",
            "Pass 5: README And Wiki Integration",
            "Every accepted module appears in an accepted HLD",
            "Pass 5 plus a passing final reconciliation completes whole-repository reverse engineering",
            "separate project-owned evaluation",
        )
        for phrase in required_reverse_phrases:
            with self.subTest(reverse_skill_phrase=phrase):
                self.assertIn(phrase, reverse_skill_text)

        for phrase in (
            "treat the entire codebase as in scope",
            "Do not ask the user to select a documentation breadth",
            "require the project configuration gate, documentation coverage manifest, and every pass completion gate",
            "general-model-training fallback",
        ):
            with self.subTest(bootstrap_skill_phrase=phrase):
                self.assertIn(phrase, bootstrap_skill_text)

        build_skill_docs = load_build_skill_docs_module()
        skill_payload = build_skill_docs.build_payload()
        roles = build_skill_docs.load_role_definitions(set(skill_payload["skills"]))
        bootstrapper = next(role for role in roles if role.name == "project-bootstrapper")
        writer = next(role for role in roles if role.name == "dev-documentation-writer")

        for phrase in (
            "full-codebase documentation request",
            "coverage manifest",
            "machine-checkable path coverage ledger",
            "Stop between documentation levels",
            "Do not accept higher-level summaries as substitutes",
            "available-skill catalog",
        ):
            with self.subTest(bootstrapper_phrase=phrase):
                self.assertIn(phrase, bootstrapper.instructions)

        for phrase in (
            "do not ask for a documentation breadth",
            "document and review every meaningful module before any high-level design",
            "group every module into reviewed high-level designs before architecture",
            "never describe that result as complete project reverse engineering",
        ):
            with self.subTest(writer_phrase=phrase):
                self.assertIn(phrase, writer.instructions)

        development_methodology_text = (
            SKILLS_ROOT / "development-methodology" / "SKILL.md"
        ).read_text(encoding="utf-8")
        readme_text = README_PATH.read_text(encoding="utf-8")
        lifecycle_text = (
            REPOSITORY_ROOT / "design" / "orchestrated-development-lifecycle.html"
        ).read_text(encoding="utf-8")
        source_texts = (
            reverse_skill_text,
            development_methodology_text,
            bootstrapper.instructions,
            writer.instructions,
            readme_text,
            lifecycle_text,
        )
        for phrase in (
            "review-reconstruction-readiness",
            "Pass 6",
            "MUST_DOCUMENT",
            "PUBLIC_GENERATOR",
            "PARITY_TEST_ONLY",
            "reconstruction_run.py",
            "evals/reconstruction-review",
            "reconstruction-readiness",
        ):
            for source_text in source_texts:
                with self.subTest(removed_shared_phrase=phrase):
                    self.assertNotIn(phrase, source_text)

        self.assertFalse((SKILLS_ROOT / "review-reconstruction-readiness").exists())
        self.assertFalse(
            (
                SKILLS_ROOT
                / "documentation-reverse-engineer"
                / "scripts"
                / "reconstruction_run.py"
            ).exists()
        )
        self.assertFalse((REPOSITORY_ROOT / "evals" / "reconstruction-review").exists())

    def test_reverse_engineering_final_audit_preserves_artifact_ownership(self) -> None:
        """Whole-project reverse engineering should audit final evidence without widening authorship."""
        build_skill_docs = load_build_skill_docs_module()
        skill_payload = build_skill_docs.build_payload()
        roles = build_skill_docs.load_role_definitions(set(skill_payload["skills"]))
        roles_by_name = {role.name: role for role in roles}
        bootstrapper = roles_by_name["project-bootstrapper"]
        ingester = roles_by_name["wiki-ingester"]

        bootstrap_workflow = " ".join(bootstrapper.instruction_sections["workflow"])
        bootstrap_delegation = " ".join(bootstrapper.instruction_sections["delegation"])
        bootstrap_completion = " ".join(bootstrapper.instruction_sections["completion"])
        bootstrap_failure = " ".join(bootstrapper.instruction_sections["failureHandling"])
        self.assertIn("Only for whole-project reverse engineering", bootstrapper.instructions)
        self.assertIn("Do not invoke this audit for ordinary project setup", bootstrapper.instructions)
        self.assertIn(
            "whole-project reverse-engineering no-change path still requires the final audit",
            bootstrapper.instructions,
        )
        self.assertIn("wiki-ingester", bootstrap_workflow)
        self.assertIn("complete tree", bootstrap_workflow)
        self.assertIn("missing module design", bootstrap_workflow)
        self.assertIn("dev-documentation-writer", bootstrap_workflow)
        self.assertIn("fresh independent review", bootstrap_workflow)
        self.assertIn("wiki-ingester", bootstrap_delegation)
        self.assertIn("does not become the non-wiki document author", bootstrap_delegation)
        self.assertIn("final wiki-ingester audit reports no stale", bootstrap_completion)
        self.assertIn(
            "after any verification-driven correction",
            bootstrap_failure,
        )
        self.assertIn("before retrying dev-verifier", bootstrap_failure)

        ingester_boundaries = " ".join(ingester.instruction_sections["boundaries"])
        ingester_workflow = " ".join(ingester.instruction_sections["workflow"])
        ingester_completion = " ".join(ingester.instruction_sections["completion"])
        self.assertIn("inspect and report only", ingester_boundaries)
        self.assertIn("Do not create, update, move, or correct", ingester_boundaries)
        for artifact in (
            "PROJECT.yaml",
            "AGENTS.md",
            "wiki navigation",
            "module catalogs",
            "coverage manifests",
            "module pages",
            "links",
            "ownership statements",
        ):
            with self.subTest(audited_artifact=artifact):
                self.assertIn(artifact, ingester_workflow)
        for stale_marker in ("absent", "excluded", "contribution-phase", "future work"):
            with self.subTest(stale_marker=stale_marker):
                self.assertIn(stale_marker, ingester_workflow)
        self.assertIn("NEEDS_CORRECTION", ingester_completion)
        self.assertIn("explicit no-change result", ingester_completion)
        self.assertNotIn(
            "final evidence audit",
            roles_by_name["dev-documentation-writer"].instructions,
        )
    def test_reverse_engineering_separates_pass_acceptance_and_readiness(self) -> None:
        """Keep bottom-up acceptance, persisted mode, wiki routing, and reconciliation aligned."""
        reverse_text = (
            SKILLS_ROOT / "documentation-reverse-engineer" / "SKILL.md"
        ).read_text(encoding="utf-8")
        bootstrap_text = (
            SKILLS_ROOT / "documentation-bootstrap" / "SKILL.md"
        ).read_text(encoding="utf-8")
        configuration_text = (
            SKILLS_ROOT / "create-project-configuration" / "SKILL.md"
        ).read_text(encoding="utf-8")
        project_template_text = (
            SKILLS_ROOT
            / "development-methodology"
            / "assets"
            / "templates"
            / "project-template.yaml"
        ).read_text(encoding="utf-8")

        ordered_passes = (
            "Pass -1: Project Configuration",
            "Pass 0: Repository Orientation",
            "Pass 1: Module Designs",
            "Pass 2: High-Level Designs",
            "Pass 3: Architecture",
            "Pass 4: Functional Specifications",
            "Pass 5: README And Wiki Integration",
            "Final Top-Down Semantic Reconciliation",
        )
        pass_positions = [reverse_text.index(heading) for heading in ordered_passes]
        self.assertEqual(sorted(pass_positions), pass_positions)

        for phrase in (
            "source evidence, accepted prerequisite layers, and current-pass requirements",
            "intentionally created by a later reverse-engineering pass",
            "Documentation acceptance and downstream implementation readiness are separate decisions",
            "supplements rather than replaces the bottom-up creation sequence",
            "wiki and functional specifications",
            "architecture, then high-level designs, then module designs, and finally source",
            "Correction ownership follows source authority",
        ):
            with self.subTest(reverse_phrase=phrase):
                self.assertIn(phrase, reverse_text)

        for phrase in (
            "hybrid-specifications-and-wiki",
            "legacy PROJECT.yaml",
            "unsupported documentation mode",
            "conversational context",
        ):
            with self.subTest(configuration_phrase=phrase):
                self.assertIn(phrase, configuration_text)
                self.assertIn(phrase, bootstrap_text)

        for phrase in (
            "documentation_mode:",
            "selected: \"hybrid-specifications-and-wiki\"",
            "legacy_missing_field_policy:",
            "unsupported_value_policy:",
        ):
            with self.subTest(project_template_phrase=phrase):
                self.assertIn(phrase, project_template_text)

        wiki_handoffs = (
            "project-wiki",
            "project-wiki-create",
            "project-wiki-topic-write",
            "project-wiki-review",
            "project-wiki-topic-verify",
        )
        for handoff in wiki_handoffs:
            with self.subTest(wiki_handoff=handoff):
                self.assertIn(handoff, reverse_text)
        for phrase in ("Required inputs", "Owned outputs", "Completion evidence"):
            self.assertIn(phrase, reverse_text)
        for phrase in (
            "Invoke project-wiki to initialize docs/wiki",
            "Required inputs are the repository root, accepted PROJECT.yaml, accepted wiki setup recommendation",
            "Owned outputs are the initialized docs/wiki root",
            "Completion evidence is the exact created or changed wiki page list",
            "project-wiki-topic-write for main pages",
            "Required inputs are the repository root, bounded page scope",
            "project-wiki-topic-verify in a fresh read-only context",
            "Required inputs are the repository root, exact page list",
        ):
            with self.subTest(wiki_contract_phrase=phrase):
                self.assertIn(phrase, reverse_text)

        artifact_contracts = (
            ("create-module-design", "review-module-design", "module-design-template.md", "review-checklist-module-design.md"),
            ("create-high-level-design", "review-high-level-design", "high-level-design-template.md", "review-checklist-high-level-design.md"),
            ("create-architecture", "review-architecture", "architecture-template.md", "review-checklist-architecture.md"),
            ("create-functional-spec", "review-functional-spec", "functional-spec-template.md", "review-checklist-functional-spec.md"),
        )
        for create_name, review_name, template_name, checklist_name in artifact_contracts:
            create_text = (SKILLS_ROOT / create_name / "SKILL.md").read_text(
                encoding="utf-8"
            )
            review_text = (SKILLS_ROOT / review_name / "SKILL.md").read_text(
                encoding="utf-8"
            )
            template_text = (
                SKILLS_ROOT
                / "development-methodology"
                / "assets"
                / "templates"
                / template_name
            ).read_text(encoding="utf-8")
            checklist_text = (
                SKILLS_ROOT / review_name / "references" / checklist_name
            ).read_text(encoding="utf-8")
            for text in (create_text, review_text, checklist_text):
                with self.subTest(contract=create_name, phrase="documentation acceptance"):
                    self.assertIn("documentation acceptance", text.lower())
                with self.subTest(contract=create_name, phrase="implementation readiness"):
                    self.assertIn("implementation readiness", text.lower())
                with self.subTest(contract=create_name, phrase="current pass"):
                    self.assertIn("current reverse-engineering pass", text.lower())
            self.assertEqual(1, template_text.count("## Documentation Acceptance"))
            self.assertEqual(1, template_text.count("## Implementation Readiness"))
            self.assertIn(
                "Begin this section with **ACCEPTED.** or **BLOCKED.**",
                template_text,
            )
            self.assertIn(
                "Begin this section with **READY.** or **BLOCKED.**",
                template_text,
            )
            self.assertIn(
                "first nonblank content under Documentation Acceptance",
                checklist_text,
            )
            self.assertIn(
                "first nonblank content under Implementation Readiness",
                checklist_text,
            )

        readme_text = README_PATH.read_text(encoding="utf-8")
        applying_bundle_text = readme_text.split(
            "## Applying This Bundle To A Project", maxsplit=1
        )[1].split("## Neutral Target Project Layout", maxsplit=1)[0]
        self.assertIn("README and wiki integration", applying_bundle_text)
        self.assertIn("final supplemental top-down semantic reconciliation", applying_bundle_text)
        lifecycle_text = (
            REPOSITORY_ROOT / "design" / "orchestrated-development-lifecycle.html"
        ).read_text(encoding="utf-8")
        for text in (readme_text, lifecycle_text):
            self.assertIn("hybrid-specifications-and-wiki", text)
            self.assertIn("top-down semantic reconciliation", text)
            self.assertIn("documentation acceptance", text.lower())
            self.assertIn("implementation readiness", text.lower())
    def test_project_configuration_distinguishes_no_variant_from_missing_required_skill(self) -> None:
        detector_text = (SKILLS_ROOT / "detect-technology-skills" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        configuration_text = (
            SKILLS_ROOT / "create-project-configuration" / "SKILL.md"
        ).read_text(encoding="utf-8")
        template_text = (
            SKILLS_ROOT / "development-methodology" / "assets" / "templates" / "project-template.yaml"
        ).read_text(encoding="utf-8")

        for phrase in (
            "technology skills actually exposed by the target runtime",
            "--available-skill",
            "route that scope to general model training",
            "detected required-but-unavailable skill",
            "candidate evidence, not automatic proof",
            "It must be pertinent to the folder's source-backed responsibility",
        ):
            with self.subTest(detector_phrase=phrase):
                self.assertIn(phrase, detector_text)

        for phrase in (
            "inspect the technology skills actually exposed by the target runtime",
            "Pass the complete catalog to the fallback detector",
            "general-model-training fallback",
            "required-but-unavailable skill `BLOCKED`",
            "Reject owning-manifest overreach",
            "complete fixed and conditional skill metadata",
            "Use only real repository-relative paths or valid globs",
            "most-specific-pattern-wins rule",
            "Never embed an absolute checkout, user-home, worktree, cache, or temporary-directory path",
            "Search for POSIX and Windows user-home paths",
        ):
            with self.subTest(configuration_phrase=phrase):
                self.assertIn(phrase, configuration_text)

        self.assertIn("required_but_unavailable_policy", template_text)
        self.assertIn("runtime_catalog_source:", template_text)
        self.assertIn("runtimeAvailability:", template_text)
        self.assertIn("fallback:", template_text)
        self.assertIn("rejectedCandidates:", template_text)
        self.assertIn("conditional_skills:", template_text)
        self.assertIn("folder_route_precedence:", template_text)
        self.assertIn("NO_VARIANT scopes use general model training", template_text)


if __name__ == "__main__":
    unittest.main()
