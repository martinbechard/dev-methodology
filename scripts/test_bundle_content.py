# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Modified with AI assistance.
# Summary: Verifies the distributable methodology bundle, generated artifacts, roles, and documentation contracts.
# Design: design/generic-agent-definitions-source.html and design/work-item-provider-and-completion-contracts.md

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
from unittest.mock import patch
from urllib.parse import urlsplit

import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
README_PATH = REPOSITORY_ROOT / "README.md"
AGENTS_PATH = REPOSITORY_ROOT / "AGENTS.md"
GITIGNORE_PATH = REPOSITORY_ROOT / ".gitignore"
REPOSITORY_MAINTENANCE_SKILL_PATH = (
    REPOSITORY_ROOT
    / ".agents"
    / "skills"
    / "dev-methodology-repository-maintenance"
    / "SKILL.md"
)
ANALYZE_DOCUMENT_TOPICS_SKILL_PATH = (
    REPOSITORY_ROOT
    / "skills"
    / "analyze-document-topics"
    / "SKILL.md"
)
REVISE_DOCUMENT_TOPICS_SKILL_PATH = (
    REPOSITORY_ROOT
    / "skills"
    / "revise-document-topics"
    / "SKILL.md"
)
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
    "bootstrap-project-documentation",
    "reverse-engineer-project-documentation",
    "code-project-wiki",
    "verify-documentation-page",
    "terminology-standard",
    "terminology-standard-review",
    "terminology-standard-update",
    "create-project-configuration",
    "maintain-methodology-documentation",
    "skill-authoring",
    "name-methodology-artifacts",
)
NEW_DEVELOPMENT_SKILLS = (
    "detect-technology-skills",
    "code-discovery",
    "test-strategy",
    "verify-end-to-end-workflow",
    "application-security",
    "user-experience-review",
    "review-prompt-contracts",
    "code-comments",
    "review-code-with-evidence",
    "test-driven-development",
    "trace-code-execution",
    "analyze-root-cause",
    "collect-runtime-evidence",
    "organise-project-files",
    "deliver-work-item",
    "deliver-work-item-main-branch",
    "create-work-item",
    "create-work-item-file",
    "commit-file-provider-transaction",
    "create-work-item-github",
    "create-work-item-gitlab",
    "create-work-item-azure-devops",
    "create-work-item-jira",
    "manage-work-items",
    "manage-work-items-file",
    "manage-future-ideas",
    "manage-work-items-github",
    "manage-work-items-gitlab",
    "manage-work-items-azure-devops",
    "manage-work-items-jira",
    "deliver-work-item-feature-branch",
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
DOCUMENTATION_TEMPLATE_FILENAMES = (
    PROJECT_TEMPLATE,
    "file-work-item-template.md",
) + tuple(template_name for _, template_name, _ in ARTIFACT_CREATION_SKILLS)
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
    "bootstrap-project-documentation",
    "reverse-engineer-project-documentation",
    "module-coverage.md",
    "code-project-wiki",
    "verify-documentation-page",
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
    "[Agent Skill Architecture](design/skills-modularization.html) explains always-used and rule-selected agent skills",
    "[Wiki Skills And Project Context page](design/wiki-skills-and-project-context.html)",
    "[Terminology Standard design](design/agents/terminology-standard.md)",
    "- terminology-standard",
    "- terminology-standard-review",
    "- terminology-standard-update",
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
    "skills/route-documentation-work/assets/templates",
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
    "This repository uses the command-line provider because the current MCP provider omits claim deadline extension and registry reset operations.",
    "Published release 0.4.0 does not support the required claim results",
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
DOCUMENTATION_LIST_WRITER_SKILLS = (
    "route-documentation-work",
    "maintain-methodology-documentation",
    "project-wiki-topic-write",
)
DOCUMENTATION_LIST_VERIFIER_SKILLS = (
    "verify-documentation-page",
    "project-wiki-topic-verify",
)
MODULARIZATION_REQUIRED_PHRASES = (
    "Core Skill Categories and Ownership",
    "Skill Selection Ownership and Technology Boundaries",
    "Technology Extension Configuration Process",
    "may directly reference both required and optional core skills",
    "Both kinds of directly referenced skills must be technology-agnostic",
    "Required core skill",
    "Optional core skill",
    "Required versus optional is not the architectural split",
    "No finite agent definition can list every language, framework, library, runtime, database, and tool",
    "only technology and domain skills that actually exist in the available skill collection",
    "New technology skills can be added without editing every generic agent definition",
    "Skill Lifecycle and Runtime Delivery",
    "Native Runtime Mechanisms",
    "Bundle Selection and Instruction Delivery",
    "Skill Instruction Delivery and Inlining",
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
    "Technology Extension Skill Catalog",
    "generic pattern family covers all 23 Gang of Four object-oriented patterns",
    "request-specific assignments for Dev Documentation Writer and Dev Artifact Reviewer",
    "pattern examples remain setup-detected technology skills",
    "Changeset identity, include-chain, validation, update, rollback, and recovery guidance together with SQL.",
    "jhipster-domain-modeling",
    "Setup-Time Technology Detection",
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
    'heading.textContent = `Agents for ${group.label}`',
    "roleData.catalogGroups.forEach((group) => {",
    'definitionButton.textContent = "View"',
    "agent-grid",
    "grid-template-columns: repeat(3, minmax(0, 1fr));",
    "Skills",
    "Outputs",
    "Model profile",
    "Repository mutation",
    "[role.modelProfile]",
    "[role.repositoryMutation]",
    'document.createElement("h4")',
    ".tag.output",
    ".tag.conditional-skill",
    ".tag.technology-skill",
    ".tag.model-profile",
    ".tag.mutation-policy",
    "technology-skill-detection-registry.js",
    "Conceptual Agent Definitions",
    "Skill Definitions",
    "Agent-Skill Relationships",
    "Interactive Agent And Skill Map",
    'class="hierarchy-embed"',
    "Open the interactive SVG diagram",
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
    "Mutation-capable definitions enable <code>codex-harness-directives</code> through <code>[[skills.config]]</code>",
)
AGENTIC_CONFIGURATION_REQUIRED_PHRASES = (
    "Coding-Agent Runtime Configuration And Its Cross-Harness Evaluation",
    "This page describes how coding agent runtimes use generated files and how cross-harness evaluations configure and audit those runtimes.",
    "Glossary",
    "Coding agent runtime",
    "a tool that runs an AI coding agent, such as Codex, Claude Code, Gemini CLI, Junie CLI, or GitHub Copilot.",
    "the part of a coding agent runtime that loads files and applies runtime rules.",
    "this repository's internal layer for generating and installing files for one coding agent runtime.",
    "The term appears in implementation identifiers such as <code>adapters/&lt;runtime&gt;/...</code>",
    "the <code>scripts/install-skills.py</code> command. It copies selected shared skills",
    "adapters/&lt;runtime&gt;/skills/&lt;skill-name&gt;/SKILL.md",
    "Adapter-owned skill",
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
    "Cross-Harness Evaluation Environment, Permission Profiles, And Audit Evidence",
    "Evaluation Environment And Retained Evidence",
    "Permission Profiles And Containment Limits",
    "Audit Validity And Protection Limits",
    "<code>PROJECT.yaml</code> records selected conceptual agents, installed core-skill delivery, user-confirmed folder technologies, Persistence, Commit, and technology delivery.",
    "It maps those selections to root and nested <code>AGENTS.md</code> guidance.",
    "Usable generated code needs relevant context that steers the agent toward the project's standards.",
    "The main problem is choosing the relevant context from many possible information units.",
    "The solution is to split the information into focused files, select only the skills relevant to the work, and deliver their instructions through the applicable harness lifecycle.",
    "Dynamic load-by-name guidance appears only when technology inlining is explicitly disabled.",
    "The Agent Skills format uses a text file named <code>SKILL.md</code> to describe how to perform actions.",
    "It is adopted by all vendors and is the most granular unit of description.",
    "Harness-specific agent definition files describe an agent's purpose, skills, other agent dependencies, and other directives.",
    "Each agent operates with its own context and history.",
    "That isolation partitions the active information through an agent hierarchy.",
    "Definitions installed for a harness are available to all projects that use that harness.",
    "Definitions and instructions stored within a project apply only to that project and can tailor shared behavior to its content.",
    "Project skill definition files describe actions that are specific to the project or customize a shared skill for the project.",
    "Project agent definition files define project-specific agents or customize shared harness-specific agent definitions for the project.",
    "Project setup creates a portable <code>AGENTS.md</code> at the project root.",
    "The root guidance names user-confirmed folder technology skills by reference by default",
    "Project setup can place another portable <code>AGENTS.md</code> in a folder that needs specialized guidance.",
    "Every harness uses the same portable Agent Skills package",
    "Skill locations and precedence vary; the <code>SKILL.md</code> format does not.",
    '<label for="harness-filter">Show harness</label>',
    '<option value="all">All harnesses</option>',
    "Shared Or User Location",
    "Harness Rule Or File Format",
    "Package reusable action guidance whose selection and instruction delivery follow the applicable harness lifecycle.",
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
    "Mutation-capable Codex agents reference it by default",
    "Read-only Codex agents and non-Codex runtimes do not receive it.",
    "cleanup rules for terminal tasks and execution contexts",
    "The build and maintenance workflow does not install skills or agents automatically.",
    "<code>--project-root</code> requires <code>--scope project</code>",
    "<code>--dest</code> overrides the skill destination",
    "<code>--agents-dest</code> overrides the generated agent-definition destination",
    "Use <code>--dry-run</code> to inspect a deployment",
    "Each destination keeps an ownership manifest named <code>.dev-methodology-install.json</code>",
    "A non-dry-run refresh stages complete destination trees",
    "Deploy a user-level bundle by selecting the target coding agent runtime with <code>--adapter</code>",
    "<code>--adapter claude</code>",
    "<code>--adapter gemini</code>",
    "<code>--adapter junie</code>",
    "Deploy the Codex bundle to the current project",
    "<code>--remove-owned</code>",
    "<code>--adapter-skills-source</code>",
    "The Codex MCP skill root must match the selected installer destination.",
    "<code>--mcp-workspace-root</code>",
    "<code>--mcp-agent-ops-executable</code>",
    "<code>--mcp-config</code>",
    "<code>--configure-mcp false</code>",
    "The bundle installer configures an existing mcp-agent-ops server; it does not install the executable.",
    "same fifteen MCP operations",
    "one call-bearing MCP process stream",
    "An outcome-less completed call is not semantic evidence.",
)
DOCUMENT_INFORMATION_OWNERS = {
    "agent-and-skill-definitions.html": (
        "Conceptual Agent and Skill Definitions",
        "Conceptual Definition Scope",
        "Conceptual Agent Definitions",
        "Skill Definitions",
        "Agent-Skill Relationships",
        "Interactive Agent And Skill Map",
        "Project-Selected Delivery and Technology Bindings",
        "Provider-Independent Dev Coder Inputs",
        "Work-Item Delivery Responsibilities",
    ),
    "agentic-configuration.html": (
        "Knowledge Structure",
        "Context Layers",
        "Runtime Configuration File Locations",
        "Bundle Deployment And Runtime Setup",
        "Cross-Harness Evaluation Environment, Permission Profiles, And Audit Evidence",
    ),
    "skills-modularization.html": ("Agent Skill Architecture",) + MODULARIZATION_REQUIRED_PHRASES[:3] + (
        "Technology Extension Skill Catalog",
        "Setup-Time Technology Detection",
    ),
    "generic-agent-definitions-source.html": (
        "The Portability Problem",
        "From Conceptual Agent Definitions To Native Agent Definitions",
        "Conceptual Agent Definition Properties",
        "Native Runtime Packaging",
        "Conceptual-To-Native Property Mapping",
    ),
    "agent-skill-specialization-examples.html": (
        "Agent And Skill Specialization Examples",
        "Configuration Examples By Project Structure",
        "Northwind Tools: Root-Only Guidance",
        "Acme Ledger: Nested Tier Guidance",
        "Beacon Knowledge Base: Workflow Separation",
    ),
    "orchestrated-development-lifecycle.html": (
        "Work-Item Backlog",
        "File-Backed Work Items",
        "Agent Roles",
        "Runtime Coordination",
        "Runtime Coordination Surfaces",
        "Private Workspaces",
        "Shared-Resource Coordination",
        "Delivery Stages",
        "Blocker Recovery",
        "User Decision Gates",
        "Delivery Evidence",
        "Design And Documentation Workflows",
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
        "Wiki Role Ownership",
        "Federation Responsibilities",
        "Skill Collaboration Boundaries",
        "Code-Aware Hybrid",
        "Verification Gates",
        "Compounding Context",
        "Primary And Local Sources",
    ),
}
DOCUMENT_NAVIGATION_ORDER = (
    "agent-and-skill-definitions.html",
    "agent-and-skill-evaluations.html",
    "agentic-configuration.html",
    "skills-modularization.html",
    "generic-agent-definitions-source.html",
    "agent-skill-specialization-examples.html",
    "orchestrated-development-lifecycle.html",
    "documentation-templates.html",
    "wiki-skills-and-project-context.html",
)
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
        "../skills/route-documentation-work/assets/templates/project-template.yaml",
    ),
    "generic-agent-definitions-source.html": (
        "../README.md#explicit-target-deployment",
    ),
    "orchestrated-development-lifecycle.html": (
        "../skills/create-work-item-file/SKILL.md",
        "../skills/manage-work-items-file/SKILL.md",
        "../skills/resource-claim/SKILL.md",
        "../skills/resource-claim-helper/SKILL.md",
        "../skills/deliver-work-item-main-branch/SKILL.md",
        "../skills/deliver-work-item-feature-branch/SKILL.md",
        "../skills/create-pull-request/SKILL.md",
        "../skills/resource-claim-helper-command/SKILL.md",
        "../skills/resource-claim-helper-mcp/SKILL.md",
        "agent-and-skill-definitions.html#dev-activities-title",
        "documentation-templates.html",
        "wiki-skills-and-project-context.html",
    ),
    "documentation-templates.html": (
        "../skills/route-documentation-work/assets/templates/project-template.yaml",
        "../skills/route-documentation-work/assets/templates/project-wiki-template.md",
        "../skills/route-documentation-work/assets/templates/functional-spec-template.md",
        "../skills/route-documentation-work/assets/templates/architecture-template.md",
        "../skills/route-documentation-work/assets/templates/high-level-design-template.md",
        "../skills/route-documentation-work/assets/templates/module-design-template.md",
        "../skills/route-documentation-work/assets/templates/unit-test-plan-template.md",
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
        "../agents/roles/wiki-activities/wiki-architect.role.yaml",
        "../agents/roles/wiki-activities/wiki-source-collector.role.yaml",
        "../agents/roles/wiki-activities/wiki-researcher.role.yaml",
        "../agents/roles/wiki-activities/wiki-ingester.role.yaml",
        "../agents/roles/wiki-activities/wiki-writer.role.yaml",
        "../agents/roles/wiki-activities/wiki-topic-verifier.role.yaml",
        "../agents/roles/wiki-activities/wiki-query-responder.role.yaml",
        "../agents/roles/wiki-activities/wiki-artifact-reviewer.role.yaml",
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
REPOSITORY_MAINTENANCE_REQUIRED_PHRASES = (
    "Keep repository-only maintenance rules in this project skill.",
    "Do not put repository-specific procedures in distributed skills.",
    "Update README.md when the public inventory, setup, verification, or bundle purpose changes.",
    "Update affected design HTML.",
    "Keep agents/openai.yaml beside the skill when Codex metadata, invocation policy, or tool dependencies are required.",
    "Run scripts/openai_metadata.py skills after changing a skill name or description.",
    "Choose tests from changed behavior and actual dependency paths.",
    "A tier identifies the affected surface; it does not trigger a full repository regression.",
    ".worktrees contains ignored operational checkouts under the primary worktree. Resolve this directory from the primary worktree, never from another linked checkout.",
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


class DocumentationNavigationParser(HTMLParser):
    """Inventory section targets, element IDs, and documentation navigation links."""

    _VOID_ELEMENTS = {
        "area",
        "base",
        "br",
        "col",
        "embed",
        "hr",
        "img",
        "input",
        "link",
        "meta",
        "param",
        "source",
        "track",
        "wbr",
    }
    _SECTION_NAVIGATION_LABELS = {"Page sections", "Lifecycle chapters"}

    def __init__(self) -> None:
        super().__init__()
        self._elements: list[str] = []
        self._section_navigation_depth: int | None = None
        self._document_navigation_depth: int | None = None
        self.element_id_counts: dict[str, int] = {}
        self.duplicate_element_ids: set[str] = set()
        self.major_section_targets: list[str | None] = []
        self.section_navigation_count = 0
        self.section_navigation_hrefs: list[str] = []
        self.section_navigation_targets: list[str] = []
        self.document_navigation_count = 0
        self.document_sequence_links: list[tuple[str, str]] = []

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        attributes = dict(attrs)
        parent = self._elements[-1] if self._elements else None
        classes = set((attributes.get("class") or "").split())
        element_id = attributes.get("id")

        if element_id:
            element_id_count = self.element_id_counts.get(element_id, 0) + 1
            self.element_id_counts[element_id] = element_id_count
            if element_id_count > 1:
                self.duplicate_element_ids.add(element_id)

        if tag == "section" and parent == "main" and "section" in classes:
            target = attributes.get("id") or attributes.get("aria-labelledby")
            target_tokens = target.split() if target else []
            self.major_section_targets.append(
                target_tokens[0] if len(target_tokens) == 1 else None
            )

        if tag == "nav":
            label = attributes.get("aria-label")
            if label in self._SECTION_NAVIGATION_LABELS:
                self.section_navigation_count += 1
                self._section_navigation_depth = len(self._elements) + 1
            elif label == "Documentation navigation":
                self.document_navigation_count += 1
                self._document_navigation_depth = len(self._elements) + 1

        if tag == "a":
            href = attributes.get("href") or ""
            if self._section_navigation_depth is not None:
                self.section_navigation_hrefs.append(href)
                if href.startswith("#"):
                    self.section_navigation_targets.append(href[1:])
            if self._document_navigation_depth is not None:
                relation = attributes.get("rel")
                if relation in {"prev", "next"}:
                    self.document_sequence_links.append((relation, href))

        if tag not in self._VOID_ELEMENTS:
            self._elements.append(tag)

    def handle_endtag(self, tag: str) -> None:
        if tag not in self._elements:
            return
        depth = len(self._elements)
        if tag == "nav" and depth == self._section_navigation_depth:
            self._section_navigation_depth = None
        if tag == "nav" and depth == self._document_navigation_depth:
            self._document_navigation_depth = None
        while self._elements:
            open_tag = self._elements.pop()
            if open_tag == tag:
                break


def visible_prose_blocks(path: Path) -> list[str]:
    return visible_prose_from_html(path.read_text(encoding="utf-8"))


def visible_prose_from_html(html: str) -> list[str]:
    parser = VisibleProseParser()
    parser.feed(html)
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


def load_python_module(path: Path, module_name: str) -> ModuleType:
    """Load a repository Python module for executable contract assertions."""
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {path}.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
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


def _scan_stale_identities(
    source_text_by_path: dict[Path, str],
    retired_identities: tuple[str, ...],
    literal_allowances: dict[tuple[Path, str], int],
) -> tuple[list[str], dict[tuple[Path, str], int]]:
    """Return violations and unconsumed exact-line fixture allowances."""

    remaining_literal_allowances = literal_allowances.copy()
    stale_identity_violations: list[str] = []
    for relative_path, text in sorted(source_text_by_path.items()):
        for line_number, line in enumerate(text.splitlines(), start=1):
            for retired_identity in retired_identities:
                if retired_identity not in line:
                    continue
                allowance_key = (relative_path, line.strip())
                if remaining_literal_allowances.get(allowance_key, 0) > 0:
                    remaining_literal_allowances[allowance_key] -= 1
                    continue
                stale_identity_violations.append(
                    f"{relative_path}:{line_number}: {retired_identity}"
                )

    return stale_identity_violations, {
        allowance: remaining
        for allowance, remaining in remaining_literal_allowances.items()
        if remaining
    }


class BundleContentTests(unittest.TestCase):
    def test_document_provenance_package_templates_and_probe_are_aligned(self) -> None:
        """Keep provenance sources, templates, routing, and declared evaluation aligned."""

        skill_root = SKILLS_ROOT / "document-provenance"
        skill_path = skill_root / "SKILL.md"
        metadata_path = skill_root / "agents" / "openai.yaml"
        format_contract_path = skill_root / "references" / "format-contract.md"
        migration_path = skill_root / "references" / "historical-migration.md"
        validator_path = skill_root / "scripts" / "validate_document_provenance.py"
        validator_test_path = (
            skill_root / "scripts" / "test_validate_document_provenance.py"
        )
        envelope_path = skill_root / "fixtures" / "runtime-envelope.json"
        schema_path = skill_root / "assets" / "provenance-envelope.schema.json"

        for path in (
            skill_path,
            metadata_path,
            format_contract_path,
            migration_path,
            validator_path,
            validator_test_path,
            envelope_path,
            schema_path,
        ):
            with self.subTest(path=path.relative_to(REPOSITORY_ROOT)):
                self.assertTrue(path.is_file())

        frontmatter = load_yaml_object_from_frontmatter(skill_path)
        metadata = load_yaml_object(metadata_path)
        skill_text = skill_path.read_text(encoding="utf-8")
        self.assertEqual("document-provenance", frontmatter["name"])
        self.assertEqual("documentation-methodology", frontmatter["metadata"]["category"])
        self.assertEqual("Document Provenance", metadata["interface"]["display_name"])
        self.assertIn("$document-provenance", metadata["interface"]["default_prompt"])
        for heading in (
            "## Authority Boundary",
            "## Runtime Provenance Envelope",
            "## Placement Rules",
            "## Historical Documents",
            "## Deterministic Validation",
        ):
            self.assertIn(heading, skill_text)
        json.loads(schema_path.read_text(encoding="utf-8"))

        expected_creation_records = [
            {
                "Artifact-ID": "f633e99c-ffc4-4bc9-9c11-75e8dc070914",
                "Created-UTC": "2026-08-08T18:22:49Z",
                "Creating-Agent": "Dev Coder",
                "Runtime": "Codex",
                "Dispatched-Model": "gpt-5.6-sol",
                "Reasoning-Effort": "high",
                "Task-ID": "019fe291-1ba8-7a43-8d21-391a04dfa9a9",
            },
            {
                "Artifact-ID": "0b7a6eef-de34-488e-957d-11788f18314d",
                "Created-UTC": "2026-08-08T18:22:49Z",
                "Creating-Agent": "Dev Coder",
                "Runtime": "Codex",
                "Dispatched-Model": "gpt-5.6-sol",
                "Reasoning-Effort": "high",
                "Task-ID": "019fe291-1ba8-7a43-8d21-391a04dfa9a9",
            },
            {
                "Artifact-ID": "52badfc3-ee93-4a3c-8aa8-b4195cacb745",
                "Created-UTC": "2026-08-08T18:22:49Z",
                "Creating-Agent": "Dev Coder",
                "Runtime": "Codex",
                "Dispatched-Model": "gpt-5.6-sol",
                "Reasoning-Effort": "high",
                "Task-ID": "019fe291-1ba8-7a43-8d21-391a04dfa9a9",
            },
        ]
        envelope = json.loads(envelope_path.read_text(encoding="utf-8"))
        self.assertEqual(expected_creation_records, envelope["records"][:3])
        for path, record in zip(
            (skill_path, format_contract_path, migration_path),
            expected_creation_records,
            strict=True,
        ):
            text = path.read_text(encoding="utf-8")
            for field, expected in record.items():
                self.assertIn(f"{field}: {expected}", text)
                self.assertIn(f"{field}-Evidence: runtime-supplied", text)

        template_root = (
            SKILLS_ROOT / "route-documentation-work" / "assets" / "templates"
        )
        governed_templates = (
            "architecture-template.md",
            "functional-spec-template.md",
            "high-level-design-template.md",
            "module-design-template.md",
            "project-wiki-template.md",
            "unit-test-plan-template.md",
        )
        placeholder_fields = (
            "COPYRIGHT",
            "ARTIFACT_ID",
            "CREATED_UTC",
            "CREATING_AGENT",
            "RUNTIME",
            "DISPATCHED_MODEL",
            "REASONING_EFFORT",
            "TASK_ID",
        )
        evidence_labels = (
            "Artifact-ID",
            "Created-UTC",
            "Creating-Agent",
            "Runtime",
            "Dispatched-Model",
            "Reasoning-Effort",
            "Task-ID",
        )
        for template_name in governed_templates:
            template_text = (template_root / template_name).read_text(encoding="utf-8")
            with self.subTest(template=template_name):
                for field in placeholder_fields:
                    self.assertIn(f"{{{{{field}}}}}", template_text)
                for label in evidence_labels:
                    self.assertIn(f"{label}-Evidence: runtime-supplied", template_text)
                self.assertNotIn("Copyright (c) 2025", template_text)
                self.assertNotIn("MIT License", template_text)
                self.assertNotIn("File path:", template_text)
                self.assertNotIn("1-line summary:", template_text)
        file_work_item = (template_root / "file-work-item-template.md").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("{{ARTIFACT_ID}}", file_work_item)
        project_template = load_yaml_object(template_root / "project-template.yaml")
        self.assertEqual({"enabled": False}, project_template["document_provenance"])
        self.assertNotIn(
            "document-provenance",
            [entry["skill"] for entry in project_template["shared_agent_skills"]],
        )

        probes = load_yaml_object(REPOSITORY_ROOT / "evals" / "skill-probes.yaml")
        probe = next(
            entry
            for entry in probes["probes"]
            if entry["id"] == "probe-document-provenance"
        )
        self.assertEqual("document-provenance", probe["skill"])
        self.assertEqual("declared", probe["coverageStatus"])
        self.assertEqual([], probe["executableCases"])
        self.assertIn("do not activate", probe["negativeCondition"])
        self.assertIn("runtime", probe["expectedBehavior"])

        project = load_yaml_object(REPOSITORY_ROOT / "PROJECT.yaml")
        shared_skills = [entry["skill"] for entry in project["shared_agent_skills"]]
        self.assertIn("document-provenance", shared_skills)
        self.assertEqual(True, project["document_provenance"]["enabled"])
        self.assertEqual(
            "Copyright (c) 2026 Martin.Bechard@DevConsult.ca",
            project["document_provenance"]["copyright"],
        )
        agents_text = AGENTS_PATH.read_text(encoding="utf-8")
        self.assertEqual(1, agents_text.count("## Document Provenance"))
        self.assertIn("document-provenance", README_PATH.read_text(encoding="utf-8"))

    def test_baseline_development_skills_expose_approved_operations_and_rename(
        self,
    ) -> None:
        """Keep Baseline Development procedures, probes, and direct role references aligned."""

        expected_operations = {
            "careful-coding": (
                "## Confirm Work Before Coding",
                "## Validate Authorized Contract",
                "## Execute Goal-Driven Loop",
            ),
            "code-comments": (
                "## Write Structured Comments",
                "## Add Code Artifact Header",
                "## Document Public Constructs",
                "## Review Code Comments",
            ),
            "code-discovery": (
                "## Discover Code Context",
                "## Determine Change Scope",
            ),
            "test-driven-development": ("## Run Red-Green-Refactor Loop",),
            "structured-design": (
                "## Create Structured Design",
                "## Self-Review Structured Design",
            ),
            "structured-explanation": ("## Create Structured Explanation",),
            "organise-project-files": ("## Choose Project File Placement",),
            "review-structured-artifact": ("## Review Structured Artifact",),
            "explain-code-fix": ("## Explain Code Fix",),
        }
        for skill_id, headings in expected_operations.items():
            skill_text = (SKILLS_ROOT / skill_id / "SKILL.md").read_text(
                encoding="utf-8"
            )
            for heading in headings:
                with self.subTest(skill=skill_id, heading=heading):
                    self.assertIn(heading, skill_text)

        self.assertFalse((SKILLS_ROOT / "fix-explanation").exists())

        expected_probe_phrases = {
            "probe-careful-coding": "Confirm Work Before Coding, Validate Authorized Contract, and Execute Goal-Driven Loop",
            "probe-code-comments": "Write Structured Comments, Add Code Artifact Header, Document Public Constructs, and Review Code Comments",
            "probe-code-discovery": "Discover Code Context before Determine Change Scope",
            "probe-test-driven-development": "Run Red-Green-Refactor Loop",
            "probe-structured-design": "Create Structured Design and Self-Review Structured Design",
            "probe-organise-project-files": "Choose Project File Placement",
            "probe-review-structured-artifact": "Review Structured Artifact",
            "probe-explain-code-fix": "Explain Code Fix",
        }
        probes = load_yaml_object(REPOSITORY_ROOT / "evals" / "skill-probes.yaml")
        probes_by_id = {probe["id"]: probe for probe in probes["probes"]}
        for probe_id, phrase in expected_probe_phrases.items():
            with self.subTest(probe=probe_id):
                self.assertIn(phrase, probes_by_id[probe_id]["expectedBehavior"])

        self.assertEqual(
            "Create Structured Explanation by starting with a top-level QUERY; "
            "use SUB-QUERY items only when they help; classify direct evidence, "
            "plausible unproven explanations, and unresolved gaps as FACT, "
            "HYPOTHESIS, and UNKNOWN; close each query with an ANSWER supported "
            "by the items directly under that query; end with an ANSWER to the "
            "main QUERY; and use structured-design items only when concrete "
            "system structure is needed, keeping them subordinate to the "
            "explanation flow.",
            probes_by_id["probe-structured-explanation"]["expectedBehavior"],
        )

        for role_name in ("dev-coder", "dev-merge-coordinator"):
            role = load_yaml_object(
                ROLES_ROOT / "dev-activities" / f"{role_name}.role.yaml"
            )
            role_skills = {next(iter(entry)) for entry in role["skills"]}
            with self.subTest(role=role_name):
                self.assertIn("explain-code-fix", role_skills)
                self.assertNotIn("fix-explanation", role_skills)

    def _assert_documentation_navigation(
        self,
        html: str,
        expected_sequence_links: list[tuple[str, str]],
    ) -> None:
        parser = DocumentationNavigationParser()
        parser.feed(html)

        self.assertFalse(
            parser.duplicate_element_ids,
            f"Duplicate element IDs: {sorted(parser.duplicate_element_ids)}",
        )
        self.assertEqual(1, parser.section_navigation_count)
        unusable_section_indexes = [
            index
            for index, target in enumerate(parser.major_section_targets, start=1)
            if target is None
        ]
        self.assertFalse(
            unusable_section_indexes,
            "Every top-level section must expose exactly one usable target",
        )
        for href in parser.section_navigation_hrefs:
            parsed_href = urlsplit(href)
            self.assertTrue(
                parsed_href.fragment
                and not parsed_href.scheme
                and not parsed_href.netloc
                and not parsed_href.path
                and not parsed_href.query,
                "Section navigation href must be a non-empty same-page fragment",
            )
        usable_major_section_targets = [
            target for target in parser.major_section_targets if target is not None
        ]
        self.assertEqual(
            usable_major_section_targets,
            parser.section_navigation_targets,
        )
        self.assertEqual(
            len(parser.section_navigation_targets),
            len(set(parser.section_navigation_targets)),
        )
        for target in parser.section_navigation_targets:
            self.assertEqual(
                1,
                parser.element_id_counts.get(target, 0),
                f"Section target #{target} must resolve exactly once",
            )
        self.assertEqual(1, parser.document_navigation_count)
        self.assertEqual(
            expected_sequence_links,
            parser.document_sequence_links,
            "Documentation links must match the adjacent index detail pages",
        )

    def test_index_detail_pages_expose_complete_section_navigation(self) -> None:
        """Every index detail page has one complete menu and keeps sequence links."""
        index_text = (REPOSITORY_ROOT / "index.html").read_text(encoding="utf-8")
        detail_pages = re.findall(
            r'<a class="doc-card\b[^"]*"[^>]*href="(design/[^"#]+\.html)"',
            index_text,
        )

        self.assertEqual(9, len(detail_pages))
        for page_index, relative_path in enumerate(detail_pages):
            with self.subTest(detail_page=relative_path):
                expected_sequence_links: list[tuple[str, str]] = []
                if page_index > 0:
                    expected_sequence_links.append(
                        ("prev", Path(detail_pages[page_index - 1]).name)
                    )
                if page_index < len(detail_pages) - 1:
                    expected_sequence_links.append(
                        ("next", Path(detail_pages[page_index + 1]).name)
                    )
                self._assert_documentation_navigation(
                    (REPOSITORY_ROOT / relative_path).read_text(encoding="utf-8"),
                    expected_sequence_links,
                )

    def test_documentation_navigation_rejects_invalid_ids_and_sequence_links(
        self,
    ) -> None:
        """Adversarial pages fail for broken IDs and document sequence links."""
        valid_html = """
            <main>
              <nav aria-label="Documentation navigation">
                <a href="previous.html" rel="prev">Previous</a>
                <a href="next.html" rel="next">Next</a>
              </nav>
              <nav aria-label="Page sections">
                <a href="#overview">Overview</a>
                <a href="#details">Details</a>
              </nav>
              <section class="section" aria-labelledby="overview">
                <h2 id="overview">Overview</h2>
              </section>
              <section class="section" id="details" aria-labelledby="details-heading">
                <h2 id="details-heading">Details</h2>
              </section>
            </main>
        """
        expected_sequence_links = [
            ("prev", "previous.html"),
            ("next", "next.html"),
        ]
        invalid_cases = {
            "missing_target_id": (
                valid_html.replace('id="overview"', 'id="missing-overview"'),
                r"Section target #overview must resolve exactly once",
            ),
            "duplicate_id": (
                valid_html.replace(
                    "<h2 id=\"overview\">Overview</h2>",
                    '<h2 id="overview">Overview</h2><span id="overview"></span>',
                ),
                r"Duplicate element IDs",
            ),
            "missing_interior_relation": (
                valid_html.replace(
                    '<a href="next.html" rel="next">Next</a>',
                    "",
                ),
                r"Documentation links must match",
            ),
            "wrong_adjacent_destination": (
                valid_html.replace("next.html", "missing.html"),
                r"Documentation links must match",
            ),
            "untargeted_top_level_section": (
                valid_html.replace(
                    "              </section>\n            </main>",
                    """              </section>
              <section class="section">
                <h2 id="untargeted">Untargeted</h2>
              </section>
            </main>""",
                ),
                r"Every top-level section must expose exactly one usable target",
            ),
            "empty_section_link": (
                valid_html.replace(
                    '<a href="#details">Details</a>',
                    '<a href="">Details</a>',
                ),
                r"Section navigation href must be a non-empty same-page fragment",
            ),
            "cross_page_section_link": (
                valid_html.replace(
                    '<a href="#details">Details</a>',
                    '<a href="other.html#details">Details</a>',
                ),
                r"Section navigation href must be a non-empty same-page fragment",
            ),
        }

        for case_name, (html, expected_error) in invalid_cases.items():
            with self.subTest(case=case_name):
                with self.assertRaisesRegex(AssertionError, expected_error):
                    self._assert_documentation_navigation(
                        html,
                        expected_sequence_links,
                    )

    def test_fix_explanation_separates_concept_roles_from_item_types(self) -> None:
        structured_text = (
            SKILLS_ROOT / "structured-explanation" / "SKILL.md"
        ).read_text(encoding="utf-8")
        core_model = structured_text.split(
            "The format has six item types:", 1
        )[1].split("Use them in this order of thought:", 1)[0]
        allowed_item_types = {
            "QUERY",
            "SUB-QUERY",
            "FACT",
            "HYPOTHESIS",
            "UNKNOWN",
            "ANSWER",
        }

        self.assertEqual(
            allowed_item_types,
            set(re.findall(r"^- `([A-Z-]+)`$", core_model, re.MULTILINE)),
        )

        fix_text = (SKILLS_ROOT / "explain-code-fix" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        relationship_rules = fix_text.split("## Relationship Rules", 1)[1].split(
            "## Persistence Rule", 1
        )[0]
        self.assertIn(
            "PROBLEM, FIX, TEST, and BENEFIT are CONCEPT-ROLE values, not item types.",
            relationship_rules,
        )

        example = relationship_rules.split(
            "Representative relationship example:", 1
        )[1]
        example_items = re.findall(
            r"^( *)- \*\*([A-Z-]+): ([A-Z][A-Z0-9-]*)\*\*$",
            example,
            re.MULTILINE,
        )
        self.assertEqual(
            [
                ("", "QUERY", "Q-FIX-1"),
                ("  ", "FACT", "F-PROBLEM-1"),
                ("  ", "FACT", "F-PROBLEM-2"),
                ("  ", "FACT", "F-FIX-1"),
                ("    ", "FACT", "F-TEST-1"),
                ("    ", "FACT", "F-BENEFIT-1"),
                ("  ", "ANSWER", "A-FIX-1"),
            ],
            example_items,
        )
        example_ids = [item_id for _, _, item_id in example_items]
        self.assertEqual(len(example_ids), len(set(example_ids)))
        self.assertTrue(
            all(
                item_type in allowed_item_types
                for _, item_type, _ in example_items
            )
        )
        expected_roles = {
            "F-PROBLEM-1": ("  ", "FACT", "PROBLEM"),
            "F-PROBLEM-2": ("  ", "FACT", "PROBLEM"),
            "F-FIX-1": ("  ", "FACT", "FIX"),
            "F-TEST-1": ("    ", "FACT", "TEST"),
            "F-BENEFIT-1": ("    ", "FACT", "BENEFIT"),
        }
        self.assertEqual(
            ["PROBLEM", "PROBLEM", "FIX", "TEST", "BENEFIT"],
            re.findall(
                r"^ *- \*\*CONCEPT-ROLE:\*\* ([A-Z]+)$",
                example,
                re.MULTILINE,
            ),
        )
        for item_id, (indent, item_type, concept_role) in expected_roles.items():
            with self.subTest(item_id=item_id):
                self.assertRegex(
                    example,
                    (
                        rf"(?m)^{indent}- \*\*{item_type}: {item_id}\*\*\n"
                        rf"^{indent}  - \*\*SYNOPSIS:\*\* [^\n]+\n"
                        rf"^{indent}  - \*\*CONCEPT-ROLE:\*\* {concept_role}$"
                    ),
                )

        item_line = re.compile(
            r"^(?P<indent> *)- \*\*[A-Z-]+: (?P<item_id>[A-Z][A-Z0-9-]*)\*\*$"
        )
        relationship_line = re.compile(
            (
                r"^(?P<indent> *)- \*\*"
                r"(?P<relationship>ADDRESSES|VERIFIES|FOLLOWS-FROM|SUPPORTED-BY)"
                r":\*\* (?P<targets>[A-Z0-9, -]+)$"
            )
        )

        def relationship_owners(markdown: str) -> list[tuple[str, str, str]]:
            item_stack: list[tuple[int, str]] = []
            owners: list[tuple[str, str, str]] = []
            for line in markdown.splitlines():
                item_match = item_line.match(line)
                if item_match:
                    indent = len(item_match.group("indent"))
                    while item_stack and item_stack[-1][0] >= indent:
                        item_stack.pop()
                    item_stack.append((indent, item_match.group("item_id")))
                    continue
                relationship_match = relationship_line.match(line)
                if relationship_match is None:
                    continue
                indent = len(relationship_match.group("indent"))
                while item_stack and item_stack[-1][0] >= indent:
                    item_stack.pop()
                self.assertTrue(item_stack)
                owner_indent, owner_id = item_stack[-1]
                self.assertEqual(owner_indent + 2, indent)
                owners.append(
                    (
                        owner_id,
                        relationship_match.group("relationship"),
                        relationship_match.group("targets"),
                    )
                )
            return owners

        expected_relationships = [
            ("F-FIX-1", "ADDRESSES", "F-PROBLEM-1, F-PROBLEM-2"),
            ("F-TEST-1", "VERIFIES", "F-FIX-1"),
            ("F-BENEFIT-1", "FOLLOWS-FROM", "F-FIX-1"),
            (
                "A-FIX-1",
                "SUPPORTED-BY",
                "F-PROBLEM-1, F-PROBLEM-2, F-FIX-1, F-TEST-1, F-BENEFIT-1",
            ),
        ]
        relationships = relationship_owners(example)
        self.assertEqual(expected_relationships, relationships)
        misplaced_verifies = example.replace(
            "      - **VERIFIES:** F-FIX-1",
            "    - **VERIFIES:** F-FIX-1",
            1,
        )
        with self.assertRaises(AssertionError):
            self.assertEqual(
                expected_relationships,
                relationship_owners(misplaced_verifies),
            )
        for _, _, target_list in relationships:
            for target in target_list.split(", "):
                with self.subTest(target=target):
                    self.assertIn(target, example_ids)

        build_skill_docs = load_build_skill_docs_module()
        rendered_html = build_skill_docs.build_payload()["skills"][
            "explain-code-fix"
        ]["html"]
        policy_clauses = (
            "The six item types from structured-explanation remain authoritative: QUERY, SUB-QUERY, FACT, HYPOTHESIS, UNKNOWN, and ANSWER.",
            "PROBLEM, FIX, TEST, and BENEFIT are CONCEPT-ROLE values, not item types.",
            "The item type is the structural reasoning axis. CONCEPT-ROLE is a separate domain and reference axis.",
            "Give each domain linchpin an allowed item type, a stable ID, and a CONCEPT-ROLE. Use relationship fields to reference those IDs.",
        )
        for clause in policy_clauses:
            with self.subTest(clause=clause):
                self.assertIn(f"<li>{clause}</li>", rendered_html)

    def test_tool_runtime_excludes_sensitive_content_from_retained_traces(
        self,
    ) -> None:
        skill_text = (SKILLS_ROOT / "tool-runtime" / "SKILL.md").read_text(
            encoding="utf-8"
        )

        for phrase in (
            "Exclude sensitive values and protected payload or file contents from retained logs and traces, or redact them before retention.",
            "Apply this rule to successful, denied, malformed, partial, and retried tool calls.",
            "Preserve enough non-sensitive execution trace for users and reviewers to understand what happened without retaining protected content.",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, skill_text)

    def test_backlog_blockage_and_dispatch_modes_are_separate(self) -> None:
        blockage_text = (
            SKILLS_ROOT / "resolve-backlog-blockage" / "SKILL.md"
        ).read_text(encoding="utf-8")
        solo_text = (SKILLS_ROOT / "set-solo-mode" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        multitask_text = (
            SKILLS_ROOT / "set-multitask-mode" / "SKILL.md"
        ).read_text(encoding="utf-8")
        coordinator = yaml.safe_load(
            (
                ROLES_ROOT
                / "dev-activities"
                / "dev-backlog-coordinator.role.yaml"
            ).read_text(encoding="utf-8")
        )
        watchdog = yaml.safe_load(
            (
                ROLES_ROOT
                / "dev-activities"
                / "dev-backlog-watchdog.role.yaml"
            ).read_text(encoding="utf-8")
        )

        self.assertFalse((SKILLS_ROOT / "backlog-crisis-mode" / "SKILL.md").exists())
        self.assertFalse(
            (SKILLS_ROOT / "backlog-crisis-mode" / "agents" / "openai.yaml").exists()
        )
        for phrase in (
            "Stop claim operations.",
            "Process one blockage item at a time.",
            "Commit the current item before starting another item.",
            "Moving an item to Ready does not resolve it.",
            "When the same blockage state and recovery result are observed again, return the existing result without repeating lifecycle mutation.",
        ):
            self.assertIn(phrase, blockage_text)

        for skill_text, action, unchanged_result, sibling in (
            (
                solo_text,
                "Disable dispatch to secondary threads.",
                "ALREADY_SOLO",
                "set-multitask-mode",
            ),
            (
                multitask_text,
                "Enable dispatch to secondary threads.",
                "ALREADY_MULTITASK",
                "set-solo-mode",
            ),
        ):
            self.assertIn(action, skill_text)
            self.assertIn(unchanged_result, skill_text)
            self.assertIn(
                "When no secondary-thread dispatch mechanism is configured, return NOT_APPLICABLE without mutation.",
                skill_text,
            )
            for forbidden in (
                "Blocked",
                "lifecycle mutation",
                "resolve-backlog-blockage",
                sibling,
            ):
                self.assertNotIn(forbidden, skill_text)

        coordinator_skills = {
            name: contract
            for entry in coordinator["skills"]
            for name, contract in entry.items()
        }
        watchdog_skills = {
            name: contract
            for entry in watchdog["skills"]
            for name, contract in entry.items()
        }
        self.assertTrue(
            {"resolve-backlog-blockage", "set-solo-mode", "set-multitask-mode"}
            <= coordinator_skills.keys()
        )
        for skill in (
            "resolve-backlog-blockage",
            "set-solo-mode",
            "set-multitask-mode",
        ):
            self.assertIn("condition", coordinator_skills[skill])
        self.assertIn("resolve-backlog-blockage", watchdog_skills)
        self.assertIn("condition", watchdog_skills["resolve-backlog-blockage"])
        self.assertNotIn("set-solo-mode", watchdog_skills)
        self.assertNotIn("set-multitask-mode", watchdog_skills)

        coordinator_contract = json.dumps(coordinator, sort_keys=True)
        self.assertIn(
            "when a secondary-thread dispatch mechanism is configured",
            coordinator_contract,
        )
        self.assertIn(
            "without requiring a dispatch-mode skill",
            coordinator_contract,
        )

        probes = load_yaml_object(REPOSITORY_ROOT / "evals" / "skill-probes.yaml")
        probes_by_skill = {probe["skill"]: probe for probe in probes["probes"]}
        for skill in (
            "resolve-backlog-blockage",
            "set-solo-mode",
            "set-multitask-mode",
        ):
            with self.subTest(probe=skill):
                self.assertEqual("activation-and-behavior", probes_by_skill[skill]["evaluationKind"])
                self.assertEqual("declared", probes_by_skill[skill]["coverageStatus"])

        coordinator_scenarios = load_yaml_object(
            REPOSITORY_ROOT
            / "evals"
            / "agent-tests"
            / "dev-backlog-coordinator"
            / "scenarios.yaml"
        )
        watchdog_scenarios = load_yaml_object(
            REPOSITORY_ROOT
            / "evals"
            / "agent-tests"
            / "dev-backlog-watchdog"
            / "scenarios.yaml"
        )
        self.assertTrue(
            {
                "blockage-entry-disables-secondary-dispatch",
                "blockage-recovery-resumes-secondary-dispatch",
            }
            <= {scenario["id"] for scenario in coordinator_scenarios["scenarios"]}
        )
        self.assertTrue(
            {
                "active-blockage-continues-without-repeat",
                "blockage-exit-condition-recovery-alert",
            }
            <= {scenario["id"] for scenario in watchdog_scenarios["scenarios"]}
        )

    def test_new_file_item_notifies_coordinator_without_dispatch(self) -> None:
        create_skill = (
            SKILLS_ROOT / "create-work-item-file" / "SKILL.md"
        ).read_text(encoding="utf-8")
        coordination_skill = (
            SKILLS_ROOT / "coordinate-work-items" / "SKILL.md"
        ).read_text(encoding="utf-8")

        self.assertIn(
            "After a new work-item file is committed successfully",
            create_skill,
        )
        self.assertIn(
            "send its Work Item ID to the existing Dev Backlog Coordinator task",
            create_skill,
        )
        self.assertIn(
            "Send no message when creation fails or when duplicate reconciliation creates no item.",
            create_skill,
        )
        self.assertIn(
            "reread current provider inventory before deciding whether to reserve or dispatch anything",
            coordination_skill,
        )
        self.assertIn(
            "The message is not lifecycle authority",
            coordination_skill,
        )

    def test_coordination_roles_select_portable_and_codex_peer_skills(self) -> None:
        """Portable policy and Codex task mechanics remain separate peer contracts."""

        coordination_text = (
            SKILLS_ROOT / "coordinate-work-items" / "SKILL.md"
        ).read_text(encoding="utf-8")
        codex_text = (
            SKILLS_ROOT / "coordinate-codex-tasks" / "SKILL.md"
        ).read_text(encoding="utf-8")
        provider_text = (
            SKILLS_ROOT / "manage-work-items-file" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("single normative authority", coordination_text)
        self.assertIn("## Active Execution And Capacity", coordination_text)
        self.assertNotIn("Conversation Title Contract", coordination_text)
        self.assertIn("## Conversation Title Contract", codex_text)
        self.assertIn("Apply coordinate-work-items together with this skill", codex_text)
        self.assertNotIn("Active Execution Evidence", provider_text)
        self.assertNotIn("conversation-title synchronization", provider_text)

        role_names = (
            "dev-backlog-coordinator",
            "dev-backlog-steward",
            "dev-orchestrator",
            "dev-backlog-watchdog",
        )
        central_section = "Active Execution And Capacity"
        duplicated_markers = (
            "60-second",
            "Reservation Started At",
            "Settlement Deadline",
            "Runtime Launch Result",
            "Owner Acceptance:",
            "Reconciliation Result:",
            "Condition Type:",
            "Deadline or Expires At:",
            "Next Reconciliation At:",
            "Active Execution Evidence",
            "Starting-plus-Running count",
            "Implementing —",
        )
        for role_name in role_names:
            role = load_yaml_object(
                ROLES_ROOT / "dev-activities" / f"{role_name}.role.yaml"
            )
            selected_skills = {next(iter(entry)) for entry in role["skills"]}
            role_text = json.dumps(role, sort_keys=True)
            with self.subTest(role=role_name):
                self.assertIn("coordinate-work-items", selected_skills)
                self.assertIn("coordinate-codex-tasks", selected_skills)
                self.assertIn(central_section, role_text)
                for marker in duplicated_markers:
                    self.assertNotIn(marker, role_text)

        for generated_path in (
            SKILL_DEFINITIONS_PATH,
            ROLE_DEFINITIONS_PATH,
            *(
                GENERATED_ADAPTERS_ROOT / adapter / "agents" / f"{role_name}{extension}"
                for adapter, extension in (
                    ("codex", ".toml"),
                    ("claude", ".md"),
                    ("gemini", ".md"),
                    ("junie", ".md"),
                )
                for role_name in role_names
            ),
        ):
            with self.subTest(generated=generated_path):
                generated_text = generated_path.read_text(encoding="utf-8")
                self.assertIn("coordinate-work-items", generated_text)
                self.assertIn("coordinate-codex-tasks", generated_text)

    def test_watchdog_requires_complete_terminal_task_reconciliation(self) -> None:
        """The bundle keeps terminal reconciliation complete, scoped, and read-only."""

        coordination_text = (
            SKILLS_ROOT / "coordinate-work-items" / "SKILL.md"
        ).read_text(encoding="utf-8")
        codex_text = (
            SKILLS_ROOT / "coordinate-codex-tasks" / "SKILL.md"
        ).read_text(encoding="utf-8")
        watchdog = load_yaml_object(
            ROLES_ROOT / "dev-activities" / "dev-backlog-watchdog.role.yaml"
        )
        watchdog_text = json.dumps(watchdog, sort_keys=True)
        scenarios = load_yaml_object(
            AGENT_TEST_SUITES_ROOT / "dev-backlog-watchdog" / "scenarios.yaml"
        )
        scenario_ids = {scenario["id"] for scenario in scenarios["scenarios"]}
        lifecycle_text = (
            REPOSITORY_ROOT / "design" / "orchestrated-development-lifecycle.html"
        ).read_text(encoding="utf-8")

        for clause in (
            "Reconcile each terminal task independently, even after one actionable anomaly is found.",
            "A preserved source branch never suppresses an independently authorized alert to remove its clean terminal worktree.",
            "NO_ACTION is valid only after every terminal task has complete acknowledged provider, claim, worktree, branch, notification, preservation, and archival reconciliation.",
        ):
            with self.subTest(portable_clause=clause):
                self.assertIn(clause, coordination_text)
        for clause in (
            "Completed requires merged delivery before default archival.",
            "Failed and Abandoned require valid terminal evidence and do not require or imply merged delivery.",
            "Do not infer, inherit, carry forward, or persist a campaign-wide pause from earlier conversation.",
            "A valid pause suppresses archival only for its named tasks.",
        ):
            with self.subTest(codex_clause=clause):
                self.assertIn(clause, codex_text)
        self.assertNotIn("Respect any user pause on archival.", codex_text)
        self.assertIn("Send exactly one aggregate parent alert", watchdog_text)
        self.assertIn("Never infer or inherit a campaign-wide pause", watchdog_text)
        self.assertIn(
            "Completed requires merged delivery before default archival.",
            SKILL_DEFINITIONS_PATH.read_text(encoding="utf-8"),
        )
        self.assertIn(
            "Failed and Abandoned require valid terminal evidence and do not require or imply merged delivery.",
            SKILL_DEFINITIONS_PATH.read_text(encoding="utf-8"),
        )
        for generated_path in (
            ROLE_DEFINITIONS_PATH,
            GENERATED_ADAPTERS_ROOT
            / "claude"
            / "agents"
            / "dev-backlog-watchdog.md",
            GENERATED_ADAPTERS_ROOT
            / "codex"
            / "agents"
            / "dev-backlog-watchdog.toml",
            GENERATED_ADAPTERS_ROOT
            / "gemini"
            / "agents"
            / "dev-backlog-watchdog.md",
            GENERATED_ADAPTERS_ROOT
            / "junie"
            / "agents"
            / "dev-backlog-watchdog.md",
        ):
            with self.subTest(generated_path=generated_path):
                generated_text = generated_path.read_text(encoding="utf-8")
                self.assertIn(
                    "Reconcile every terminal task associated with the observed Coordinator campaign",
                    generated_text,
                )
                self.assertIn(
                    "For Completed, require merged delivery before default archival.",
                    generated_text,
                )
                self.assertIn(
                    "For Failed and Abandoned, require valid terminal evidence without inferring merged delivery.",
                    generated_text,
                )
                self.assertIn("Send exactly one aggregate parent alert", generated_text)
        self.assertTrue(
            {
                "terminal-archive-pause-does-not-pause-cleanup",
                "terminal-default-archival-notification",
                "terminal-preserved-branch-removable-worktree",
                "terminal-aggregate-all-anomalies",
                "terminal-complete-no-action",
                "terminal-preservation-alert-deduplication",
                "terminal-failed-abandoned-status-aware",
                "terminal-claim-applicability-evidence",
            }
            <= scenario_ids
        )
        self.assertIn(
            "A valid named-task archival pause suppresses no other terminal action.",
            lifecycle_text,
        )
        self.assertIn(
            "Failed and Abandoned require valid terminal evidence without a fabricated merge gate.",
            lifecycle_text,
        )

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
            SKILLS_ROOT / "route-documentation-work" / "SKILL.md",
            SKILLS_ROOT / "maintain-methodology-documentation" / "SKILL.md",
        ):
            with self.subTest(path=path):
                self.assertNotIn(
                    "scripts/refresh-shared-skills.py",
                    path.read_text(encoding="utf-8"),
                )

    def test_development_methodology_does_not_copy_monolithic_references(self) -> None:
        references_root = SKILLS_ROOT / "route-documentation-work" / "references"

        for file_name in REMOVED_DEVELOPMENT_REFERENCES:
            with self.subTest(file_name=file_name):
                self.assertFalse((references_root / file_name).exists())

    def test_workflow_skills_and_codex_metadata_are_packaged(self) -> None:
        for skill_name in NEW_WORKFLOW_SKILLS:
            with self.subTest(skill_name=skill_name):
                self.assertTrue((SKILLS_ROOT / skill_name / "SKILL.md").is_file())
                self.assertTrue(openai_metadata_path(skill_name).is_file())

    def test_portable_coordination_controls_long_running_execution(self) -> None:
        skill_text = (
            SKILLS_ROOT / "coordinate-work-items" / "SKILL.md"
        ).read_text(encoding="utf-8")

        for phrase in (
            "expected to take more than five minutes",
            "the exact active unit and later units not started",
            "a hard stop condition and retained evidence path",
            "not a provider transaction or approval gate",
            "Distinguish active serial work from selected or queued work.",
            "classify the failure before repeating anything",
            "add the smallest offline replay or deterministic regression",
            "follow resource-claim for any triggered claim",
            "Two unproductive attempts require parent investigation and a revised plan.",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, skill_text)

    def test_combined_regression_runs_once_after_independent_merges(self) -> None:
        """Protect focused per-item delivery and one later combined regression."""

        skill_text = (
            SKILLS_ROOT / "coordinate-work-items" / "SKILL.md"
        ).read_text(encoding="utf-8")
        role_text = (
            ROLES_ROOT / "dev-activities" / "dev-backlog-coordinator.role.yaml"
        ).read_text(encoding="utf-8")
        readme_text = README_PATH.read_text(encoding="utf-8")
        lifecycle_text = (
            REPOSITORY_ROOT / "design" / "orchestrated-development-lifecycle.html"
        ).read_text(encoding="utf-8")

        for phrase in (
            "Merge each accepted item independently.",
            "After every selected item is present on main",
            "run the system-wide regression once",
            "Record that commit with the result.",
            "Do not automatically invalidate focused evidence for unrelated work items.",
        ):
            with self.subTest(skill_contract=phrase):
                self.assertIn(phrase, skill_text)

        for phrase in (
            "Do not delay individual merges for this later run.",
            "Record the commit and selected items.",
            "without automatically invalidating unrelated focused evidence",
        ):
            with self.subTest(role_contract=phrase):
                self.assertIn(phrase, role_text)

        self.assertIn("one combined regression", readme_text)
        self.assertIn("One Combined Regression After Independent Merges", lifecycle_text)

    def test_user_action_resumption_splits_lifecycle_from_codex_identity(self) -> None:
        """Portable lifecycle and Codex task identity preserve one resumption path."""

        coordination_text = (
            SKILLS_ROOT / "coordinate-work-items" / "SKILL.md"
        ).read_text(encoding="utf-8")
        codex_text = (
            SKILLS_ROOT / "coordinate-codex-tasks" / "SKILL.md"
        ).read_text(encoding="utf-8")
        manage_text = (
            SKILLS_ROOT / "manage-work-items-file" / "SKILL.md"
        ).read_text(encoding="utf-8")
        readme_text = README_PATH.read_text(encoding="utf-8")
        lifecycle_text = (
            REPOSITORY_ROOT / "design" / "orchestrated-development-lifecycle.html"
        ).read_text(encoding="utf-8")
        normalized_coordination = " ".join(coordination_text.split())
        normalized_codex = " ".join(codex_text.split())
        normalized_manage = " ".join(manage_text.split())
        normalized_readme = " ".join(readme_text.split())

        for phrase in (
            "A user answer resolves a decision gate once",
            "The user does not repeat the answer elsewhere.",
            "the Coordinator records User Action Required -> Ready",
            "Ready -> Starting for that same execution",
            "Preserve out-of-sequence work as evidence.",
            "Resume only after Running is durable",
        ):
            with self.subTest(coordination_contract=phrase):
                self.assertIn(phrase, normalized_coordination)

        for phrase in (
            "When an existing canonical task was preserved through User Action Required",
            "resume that task",
            "Do not create a replacement merely because the task is idle.",
        ):
            with self.subTest(codex_contract=phrase):
                self.assertIn(phrase, normalized_codex)

        for phrase in (
            "Accept the answer in the canonical work-item conversation that asked the question",
            "Do not require the user to switch conversations or repeat the answer.",
            "parent Coordinator authorizes resumption, record Ready -> Starting for the existing canonical conversation",
            "Work performed before User Action Required -> Ready -> Starting -> Running reconciliation is not automatically accepted or discarded.",
            "Do not continue delivery until the parent and the same root Orchestrator reconcile",
        ):
            with self.subTest(manage_contract=phrase):
                self.assertIn(phrase, normalized_manage)

        self.assertIn(
            "When coordinate-codex-tasks is active, the user may answer and continue in the canonical work-item conversation",
            normalized_readme,
        )
        self.assertIn(
            "The Coordinator directly records Ready and Starting through the selected manager",
            normalized_readme,
        )
        self.assertIn(
            "the same root Orchestrator directly records Running through that manager",
            normalized_readme,
        )
        self.assertIn("Same-Thread Resume", lifecycle_text)
        self.assertIn(
            "does not need to repeat the answer in the parent Thread",
            lifecycle_text,
        )

        role_paths = (
            ROLES_ROOT / "dev-activities" / "dev-backlog-coordinator.role.yaml",
            ROLES_ROOT / "dev-activities" / "dev-orchestrator.role.yaml",
        )
        for role_path in role_paths:
            with self.subTest(role=role_path.name):
                role_text = role_path.read_text(encoding="utf-8")
                self.assertRegex(role_text, r"canonical(?: work-item)? execution")
                self.assertIn("User Action Required", role_text)
                self.assertRegex(
                    role_text,
                    r"(?s)(?:Never reject|Do not discard|Never reject, delete).*solely",
                )

    def test_codex_coordination_routes_provider_and_delivery_state_through_selected_skills(
        self,
    ) -> None:
        """Coordination must stay neutral across Persistence and Commit selections."""
        skill_text = (
            SKILLS_ROOT / "coordinate-work-items" / "SKILL.md"
        ).read_text(encoding="utf-8")

        for phrase in (
            "Obtain queue inventory, lifecycle counts, provider identities, and dispatchable state only by applying the effective Persistence-selected management skill.",
            "Provider file uses ordinary repository backlog identities through its selected file-provider manager.",
            "Do not scan or count Future Ideas unless the parent explicitly requests ideation or promotion.",
            "Provider github uses GitHub issue identities and provider lifecycle evidence.",
            "Provider gitlab uses GitLab issue identities and provider lifecycle evidence.",
            "Provider azure-devops or jira applies the selected placeholder management skill, preserves its BLOCKED zero-mutation result, and does not fall back.",
            "Provider none has no durable inventory, count, creation, transition, or closure.",
            "Apply or resume the effective Commit-selected skill only after candidate review and source verification accept the direct or combined commit.",
            "Only after the effective Commit-selected skill returns READY",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, skill_text)

        self.assertNotIn("Derive active capacity from the backlog files", skill_text)
        self.assertNotIn("Direct Delivery Without A Pull Request", skill_text)
        self.assertNotIn("Pull-Request Delivery", skill_text)
        self.assertLess(
            skill_text.index(
                "Apply or resume the effective Commit-selected skill only after candidate review"
            ),
            skill_text.index("Only after the effective Commit-selected skill returns READY"),
        )

    def test_end_to_end_verification_routes_evidence_through_commit_authority(
        self,
    ) -> None:
        """Verification evidence must not grant the verifier delivery authority."""
        skill_text = (
            SKILLS_ROOT / "verify-end-to-end-workflow" / "SKILL.md"
        ).read_text(encoding="utf-8")

        for phrase in (
            "Only the delivery owner applies the effective Commit-selected skill.",
            "For main-branch, the delivery owner applies deliver-work-item-main-branch.",
            "For feature-branch, the delivery owner applies deliver-work-item-feature-branch.",
            "Evidence-only or no mutation authority is terminal: return the evidence handoff without applying a Commit skill or creating a commit.",
            "When repository delivery is required and Commit is UNSET, ask for the Commit selection and stop before delivery.",
            "Do not create a commit outside the effective Commit-selected skill.",
        ):
            with self.subTest(commit_authority_contract=phrase):
                self.assertIn(phrase, skill_text)

        section = skill_text.split(
            "## Evidence Delivery Decision Table", 1
        )[1].split("\n## ", 1)[0]
        rows = {}
        for line in section.splitlines():
            if not line.startswith("|") or line.startswith("| ---"):
                continue
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if cells[0] == "Request authority":
                continue
            rows[(cells[0], cells[1])] = cells[2]

        self.assertEqual(
            "Return the terminal evidence handoff; apply no Commit workflow and create no commit.",
            rows[("Evidence-only or no mutation authority", "UNSET")],
        )
        self.assertEqual(
            "Ask for Commit selection and stop before delivery; create no commit.",
            rows[("Repository delivery required", "UNSET")],
        )

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
        for artifact in ("DECISION", "EVIDENCE", "UNCERTAINTY", "BECAUSE"):
            with self.subTest(frontmatter_artifact=artifact):
                self.assertIn(artifact, description)

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
            "`DECISION` states the selected conclusion, option, or course of action.",
            "`EVIDENCE` records observable support for its immediate parent.",
            "`UNCERTAINTY` records a material unresolved gap, assumption, or limit.",
            "Do not request or expose hidden reasoning or private deliberation.",
            "**DECISION:** Release the read-only report before write operations.",
            "**EVIDENCE:** The accepted requirements authorize reporting but do not authorize mutations.",
            "**UNCERTAINTY:** Expected report volume is unknown; excessive response size or latency could make the report unusable. Measure both with a representative load test.",
        ):
            with self.subTest(preserved_contract=preserved_contract):
                self.assertIn(preserved_contract, skill_text)

        review_skill_text = (
            SKILLS_ROOT / "review-structured-artifact" / "SKILL.md"
        ).read_text(encoding="utf-8")
        for phrase in (
            "Review observable decisions, evidence, and uncertainty",
            "the stated decision is clear and authorized by the inputs",
            "the recorded evidence is observable, traceable, and supports its immediate parent",
            "material uncertainty is explicit about its impact and how it can be resolved",
            "BECAUSE remains a concise justification rather than a request for private reasoning",
        ):
            with self.subTest(review_contract=phrase):
                self.assertIn(phrase, review_skill_text)

        generated_skill_text = SKILL_DEFINITIONS_PATH.read_text(encoding="utf-8")
        evaluation_page_text = (
            REPOSITORY_ROOT / "design" / "agent-and-skill-evaluations.html"
        ).read_text(encoding="utf-8")
        for text in (
            description,
            skill_text,
            review_skill_text,
            generated_skill_text,
            evaluation_page_text,
        ):
            with self.subTest(forbidden_contract="CHAIN-OF-THOUGHT"):
                self.assertNotIn("CHAIN-OF-THOUGHT", text)

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
        manual_action = r"(?:read(?:s|ing)?|re[- ]?read(?:s|ing)?|open(?:s|ed|ing)?(?!-)|locat(?:e|es|ed|ing)|follow(?:s|ed|ing)?|inspect(?:s|ed|ing)?|discover(?:s|ed|ing)?|scan(?:s|ned|ning)?)"
        load_action = r"load(?:s|ed|ing)?"
        all_actions = rf"(?:{manual_action}|{load_action})"
        agent_subject = r"(?:agents?|reviewers?|writers?|workers?|coders?|orchestrators?)"
        target_prefix = r"(?:the\s+)?(?:all\s+)?(?:(?:root|nearest|applicable|nested)(?:\s+and\s+(?:root|nearest|applicable|nested))?\s+)?"
        direct_loading = rf"(?:\b(?:first|carefully|manually)\s+)?\b{all_actions}\b(?:\s+and\s+\b{all_actions}\b)?\s+{target_prefix}\b{manual_target}\b"
        manual_loading = re.compile(
            rf"(?:^(?:<[^>]+>\s*|[-*#]+\s*)*(?:(?:before|after)\b[^,.;!?]{{0,80}},\s*)?{direct_loading}|\b{agent_subject}\b(?:(?:\s+(?:must|should|shall|will|can|needs?\s+to|has\s+to|is\s+required\s+to|first|manually)){{0,2}}\s+){direct_loading}|\b{instruction_target}\b(?:\s+(?:file|files|instructions?))?\s+(?:is|are|was|were|gets?|got)\s*\b{all_actions}\b|\b{instruction_target}\b[^.;!?]{{0,80}}\b{agent_subject}\b[^.;!?]{{0,40}}\b{all_actions}\b\s+(?:it|them|that\s+(?:file|artifact)|the\s+(?:file|instructions?))\b)",
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
            "Load the applicable project instructions before coding.",
            "The orchestrator loads the project instructions before delivery.",
            "After AGENTS.md is available, the reviewer reads it before review.",
            "First read AGENTS.md before coding.",
            "Before acting, carefully read the applicable AGENTS.md.",
            "The reviewer is required to read AGENTS.md before review.",
            "Workers must read the nearest AGENTS.md before changing files.",
        )
        allowed_examples = (
            "Do not tell ordinary agents to read AGENTS.md.",
            "Create or update AGENTS.md as the task artifact.",
            "Review the existing AGENTS.md artifact.",
            "Investigate whether the harness loads AGENTS.md.",
            "The harness supplies applicable AGENTS.md instructions automatically.",
            "Each runtime has its own files and rules for discovering skills, agent definitions, project instructions, and optional MCP configuration.",
            "The open-diamond arrow shows that AGENTS.md names the skill selected for the project.",
            "After AGENTS.md selects manage-work-items-gitlab, the agent reads that SKILL.md.",
            "A reader can follow the request through AGENTS.md injection to the selected procedure.",
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

    def test_work_item_creation_interface_and_provider_names_are_canonical(self) -> None:
        """Creation uses one interface stem and provider implementations preserve it."""
        interface_name = "create-work-item"
        provider_names = (
            "create-work-item-file",
            "create-work-item-github",
            "create-work-item-gitlab",
            "create-work-item-azure-devops",
            "create-work-item-jira",
        )
        retired_names = (
            "create-file-work-item",
            "create-github-work-item",
            "create-gitlab-work-item",
            "create-azure-devops-work-item",
            "create-jira-work-item",
        )

        interface_path = SKILLS_ROOT / interface_name / "SKILL.md"
        interface_text = interface_path.read_text(encoding="utf-8")
        interface_frontmatter = load_yaml_object_from_frontmatter(interface_path)
        self.assertEqual(interface_name, interface_frontmatter["name"])
        for heading in ("Work Item Identity", "Inputs", "Create Work Item", "Result"):
            self.assertIn(f"## {heading}", interface_text)
        for contract_statement in (
            "Treat Work Item ID as one opaque provider-owned identifier.",
            "Resolve the effective Persistence selection",
            "Apply the exact selected create-work-item provider implementation. Do not call a different provider as a fallback.",
            "Let the provider own duplicate detection, creation authority, mutation, partial-mutation recovery, and read-after-write verification.",
            "Return CREATED, EXISTING, or BLOCKED",
            "CREATED and EXISTING require provider-observed identity and state.",
            "BLOCKED names the failed authority, capability, ambiguity, or verification boundary",
        ):
            with self.subTest(contract_statement=contract_statement):
                self.assertIn(contract_statement, interface_text)

        probes = load_yaml_object(REPOSITORY_ROOT / "evals" / "skill-probes.yaml")
        interface_probe = next(
            probe for probe in probes["probes"] if probe["id"] == "probe-create-work-item"
        )
        self.assertEqual(interface_name, interface_probe["skill"])
        self.assertEqual("declared", interface_probe["coverageStatus"])

        for provider_name in provider_names:
            with self.subTest(provider=provider_name):
                provider_path = SKILLS_ROOT / provider_name / "SKILL.md"
                self.assertTrue(provider_path.is_file())
                self.assertTrue(openai_metadata_path(provider_name).is_file())
                self.assertEqual(
                    provider_name,
                    load_yaml_object_from_frontmatter(provider_path)["name"],
                )

        for retired_name in retired_names:
            with self.subTest(retired=retired_name):
                self.assertFalse((SKILLS_ROOT / retired_name).exists())

        maintained_surface_roots = (
            REPOSITORY_ROOT / ".agents",
            REPOSITORY_ROOT / ".codex",
            REPOSITORY_ROOT / "adapters",
            REPOSITORY_ROOT / "agents",
            REPOSITORY_ROOT / "design",
            REPOSITORY_ROOT / "evals",
            REPOSITORY_ROOT / "generated",
            REPOSITORY_ROOT / "legacy_procedures",
            REPOSITORY_ROOT / "scripts",
            REPOSITORY_ROOT / "skills",
            AGENTS_PATH,
            REPOSITORY_ROOT / "PROJECT.yaml",
            README_PATH,
            REPOSITORY_ROOT / "index.html",
        )
        maintained_text_suffixes = {
            ".html",
            ".js",
            ".json",
            ".md",
            ".py",
            ".sh",
            ".svg",
            ".toml",
            ".txt",
            ".yaml",
            ".yml",
        }
        maintained_paths: set[Path] = set()
        for root in maintained_surface_roots:
            if root.is_file():
                maintained_paths.add(root)
                continue
            maintained_paths.update(
                path
                for path in root.rglob("*")
                if path.is_file() and path.suffix in maintained_text_suffixes
            )

        immutable_history_root = Path("evals/results")
        retired_identities = (*retired_names, "create-" + "*-work-item")
        provider_naming_fixture = Path("scripts/test_provider_family_naming.py")
        fixture_provider_identity = retired_names[0]
        intentional_literal_allowances = {
            (
                Path("scripts/test_bundle_content.py"),
                f'"{retired_name}",',
            ): 1
            for retired_name in retired_names
        }
        intentional_literal_allowances.update(
            {
                (
                    provider_naming_fixture,
                    f'class CreateWorkItem[\\"{retired_identities[-1]}\\"] {{',
                ): 1,
                (
                    provider_naming_fixture,
                    f"class {fixture_provider_identity} {{",
                ): 3,
                (
                    provider_naming_fixture,
                    f"{fixture_provider_identity} ..|> CreateWorkItem",
                ): 3,
            }
        )
        maintained_source_text: dict[Path, str] = {}
        for path in sorted(maintained_paths):
            relative_path = path.relative_to(REPOSITORY_ROOT)
            if relative_path.is_relative_to(immutable_history_root):
                continue
            maintained_source_text[relative_path] = path.read_text(encoding="utf-8")

        stale_identity_violations, unused_literal_allowances = (
            _scan_stale_identities(
                maintained_source_text,
                retired_identities,
                intentional_literal_allowances,
            )
        )

        self.assertEqual([], stale_identity_violations)
        self.assertEqual({}, unused_literal_allowances)

        file_provider_text = (
            SKILLS_ROOT / "create-work-item-file" / "SKILL.md"
        ).read_text(encoding="utf-8")
        user_action_condition = (
            "The item can state one concrete question whose answer changes what happens next."
        )
        self.assertEqual(1, file_provider_text.count(user_action_condition))

    def test_stale_identity_fixture_allowances_are_counted_exactly(self) -> None:
        """Report removed and duplicated fixture lines through allowance accounting."""

        retired_identity = "create-" + "file-work-item"
        fixture_path = Path("scripts/example_fixture.py")
        fixture_line = f'"{retired_identity}",'
        allowances = {(fixture_path, fixture_line): 1}

        with self.subTest(change="removed"):
            violations, unused_allowances = _scan_stale_identities(
                {fixture_path: ""},
                (retired_identity,),
                allowances,
            )
            self.assertEqual([], violations)
            self.assertEqual(allowances, unused_allowances)

        with self.subTest(change="duplicated"):
            violations, unused_allowances = _scan_stale_identities(
                {fixture_path: f"{fixture_line}\n{fixture_line}\n"},
                (retired_identity,),
                allowances,
            )
            self.assertEqual(
                [f"{fixture_path}:2: {retired_identity}"],
                violations,
            )
            self.assertEqual({}, unused_allowances)

    def test_provider_naming_fixture_does_not_hide_unexpected_stale_identity(
        self,
    ) -> None:
        """Scan unexpected stale identities even within the allowed fixture module."""

        retired_identity = "create-" + "file-work-item"
        fixture_path = Path("scripts/test_provider_family_naming.py")
        allowed_line = f"class {retired_identity} {{"
        unexpected_line = f'legacy_provider = "{retired_identity}"'
        violations, unused_allowances = _scan_stale_identities(
            {fixture_path: f"{allowed_line}\n{unexpected_line}\n"},
            (retired_identity,),
            {(fixture_path, allowed_line): 1},
        )

        self.assertEqual(
            [f"{fixture_path}:2: {retired_identity}"],
            violations,
        )
        self.assertEqual({}, unused_allowances)

    def test_azure_devops_and_jira_placeholders_block_without_fallback(self) -> None:
        expected = {
            "create-work-item-azure-devops": ("azure-devops", "create"),
            "create-work-item-jira": ("jira", "create"),
            "manage-work-items-azure-devops": ("azure-devops", "the requested"),
            "manage-work-items-jira": ("jira", "the requested"),
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
                self.assertIn("Work Item ID: none.", skill_text)
                self.assertIn("Mutation evidence:", skill_text)
                self.assertIn("Next authority or implementation decision:", skill_text)
                self.assertIn("Do not replace", skill_text)
                self.assertIn("filesystem", skill_text)
                metadata_text = openai_metadata_path(skill_name).read_text(
                    encoding="utf-8"
                )
                self.assertNotIn("dependencies:\n  tools:", metadata_text)

    def test_work_item_creation_providers_expose_shared_public_procedure(self) -> None:
        expected_boundaries = {
            "create-work-item-file": "commit-file-provider-transaction",
            "create-work-item-github": "ambiguous create response",
            "create-work-item-gitlab": "Never retry by creating a second issue",
            "create-work-item-azure-devops": "Status: BLOCKED.",
            "create-work-item-jira": "Status: BLOCKED.",
        }

        for skill_name, provider_boundary in expected_boundaries.items():
            with self.subTest(skill_name=skill_name):
                skill_text = (SKILLS_ROOT / skill_name / "SKILL.md").read_text(
                    encoding="utf-8"
                )
                self.assertEqual(1, skill_text.count("## Create Work Item"))
                self.assertIn(provider_boundary, skill_text)

        placeholder_skill_names = {
            "create-work-item-azure-devops",
            "create-work-item-jira",
            "manage-work-items-azure-devops",
            "manage-work-items-jira",
        }

        canonical_examples = {
            "manage-work-items-azure-devops": (
                "Requested operation: reconcile-work-item-completion",
                "Requested operation: close,",
            ),
            "manage-work-items-jira": (
                "Requested operation: transition-work-item",
                "Requested operation: transition,",
            ),
        }
        for skill_name, (canonical, legacy) in canonical_examples.items():
            skill_text = (SKILLS_ROOT / skill_name / "SKILL.md").read_text(
                encoding="utf-8"
            )
            example = skill_text.split("## Example", 1)[1].split(
                "## Implementation Boundary", 1
            )[0]
            with self.subTest(example_operation=skill_name):
                self.assertIn(canonical, example)
                self.assertNotIn(legacy, example)

        probes = load_yaml_object(REPOSITORY_ROOT / "evals" / "skill-probes.yaml")
        probe_ids = {entry["id"] for entry in probes["probes"]}
        for skill_name in placeholder_skill_names:
            self.assertIn(f"probe-{skill_name}", probe_ids)

        placeholder_probes = {
            entry["id"]: entry for entry in probes["probes"] if entry["id"] in probe_ids
        }
        for skill_name in placeholder_skill_names:
            probe = placeholder_probes[f"probe-{skill_name}"]
            self.assertIn("provider-placeholder-matrix", probe["executableCases"])
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

    def test_configured_providers_own_work_item_id_resolution(self) -> None:
        """Generic callers pass IDs unchanged while each provider owns their meaning."""
        expected = {
            "create-work-item-github": (
                "observed GitHub repository identity plus issue number",
                "issue URL as diagnostic location evidence",
            ),
            "manage-work-items-github": (
                "Accept the GitHub Work Item ID as one opaque input",
                "Generic callers must not parse",
            ),
            "create-work-item-gitlab": (
                "observed GitLab instance, namespace, project, and issue IID",
                "issue URL as diagnostic location evidence",
            ),
            "manage-work-items-gitlab": (
                "Accept the GitLab Work Item ID as one opaque input",
                "Generic callers must not parse",
            ),
            "create-work-item-azure-devops": (
                "Work Item ID Boundary",
                "must not fabricate an ID",
            ),
            "manage-work-items-azure-devops": (
                "Work Item ID Boundary",
                "must not parse or fabricate one",
            ),
            "create-work-item-jira": (
                "Work Item ID Boundary",
                "must not fabricate an ID",
            ),
            "manage-work-items-jira": (
                "Work Item ID Boundary",
                "must not parse or fabricate one",
            ),
        }

        for skill_name, phrases in expected.items():
            with self.subTest(skill_name=skill_name):
                skill_text = (SKILLS_ROOT / skill_name / "SKILL.md").read_text(
                    encoding="utf-8"
                )
                for phrase in phrases:
                    self.assertIn(phrase, skill_text)

    def test_work_item_management_providers_share_operations_without_losing_native_behavior(
        self,
    ) -> None:
        """The interface and providers keep shared and provider-specific contracts."""

        headings = (
            "Inventory Work Items",
            "Transition Work Item",
            "Reconcile Work Item Completion",
            "Recover Work Item",
            "Report Work Items",
        )
        interface_text = (SKILLS_ROOT / "manage-work-items" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("## Work Item Identity", interface_text)
        self.assertIn("## Lifecycle Definitions", interface_text)
        self.assertIn("## Result Vocabulary", interface_text)
        self.assertEqual(
            list(headings),
            [heading for heading in headings if f"## {heading}\n" in interface_text],
        )

        expected_behavior = {
            "manage-work-items-file": (
                "Scan active folders",
                "current state permits the requested",
                "configured completion process returned disposition READY",
                "Read visible active items first",
                "lifecycle counts",
            ),
            "manage-work-items-github": (
                "Report ambiguous matches rather than guessing",
                "After every mutation, re-read the issue",
                "completion disposition READY",
                "ambiguous mutation response as possibly applied",
                "issue number and diagnostic URL",
            ),
            "manage-work-items-gitlab": (
                "provider-native filters",
                "update only configured labels",
                "completion disposition READY",
                "Do not repeat an ambiguous mutation",
                "issue internal identifier",
            ),
            "manage-work-items-azure-devops": (
                "Requested operation: inventory-work-items",
                "Requested operation: transition-work-item",
                "Requested operation: reconcile-work-item-completion",
                "Requested operation: recover-work-item",
                "Requested operation: report-work-items",
            ),
            "manage-work-items-jira": (
                "Requested operation: inventory-work-items",
                "Requested operation: transition-work-item",
                "Requested operation: reconcile-work-item-completion",
                "Requested operation: recover-work-item",
                "Requested operation: report-work-items",
            ),
        }

        for skill_name, phrases in expected_behavior.items():
            text = (SKILLS_ROOT / skill_name / "SKILL.md").read_text(encoding="utf-8")
            with self.subTest(skill_name=skill_name):
                self.assertEqual(
                    list(headings),
                    [heading for heading in headings if f"## {heading}\n" in text],
                )
                for phrase in phrases:
                    self.assertIn(phrase, text)

        probes = load_yaml_object(REPOSITORY_ROOT / "evals" / "skill-probes.yaml")
        probes_by_id = {probe["id"]: probe for probe in probes["probes"]}
        case_id = "work-item-management-provider-operations"
        self.assertEqual(
            "manage-work-items",
            probes_by_id["probe-manage-work-items"]["skill"],
        )
        self.assertIn(
            case_id,
            probes_by_id["probe-manage-work-items"]["executableCases"],
        )
        for skill_name in expected_behavior:
            with self.subTest(eval_probe=skill_name):
                self.assertIn(
                    case_id,
                    probes_by_id[f"probe-{skill_name}"]["executableCases"],
                )

        build_skill_docs = load_build_skill_docs_module()
        skill_payload = build_skill_docs.build_payload()
        roles = {
            role.name: role
            for role in build_skill_docs.load_role_definitions(
                set(skill_payload["skills"])
            )
        }
        for role_name in (
            "dev-backlog-coordinator",
            "dev-backlog-steward",
            "dev-backlog-watchdog",
            "dev-orchestrator",
        ):
            with self.subTest(interface_consumer=role_name):
                self.assertIn(
                    "manage-work-items",
                    build_skill_docs.fixed_role_skills(roles[role_name]),
                )

        cases = load_yaml_object(REPOSITORY_ROOT / "evals" / "cases.yaml")
        operation_case = next(case for case in cases["cases"] if case["id"] == case_id)
        self.assertEqual(
            {
                f"{provider.upper()}-{operation.upper()}"
                for provider in (
                    "file",
                    "github",
                    "gitlab",
                    "azure-devops",
                    "jira",
                )
                for operation in (
                    "inventory",
                    "transition",
                    "reconcile",
                    "recover",
                    "report",
                )
            },
            set(operation_case["requiredEvidence"]),
        )

    def test_renderer_has_no_standalone_definition_approval_contract(self) -> None:
        """Keep obsolete approval records and checker options out of the bundle."""

        self.assertEqual([], sorted(REPOSITORY_ROOT.glob("approval-record-*.yaml")))
        self.assertFalse((REPOSITORY_ROOT / ".codex" / "approval-records").exists())

        renderer = (
            REPOSITORY_ROOT / "scripts" / "render-agents-technology-skills.py"
        ).read_text(encoding="utf-8")
        project = (REPOSITORY_ROOT / "PROJECT.yaml").read_text(encoding="utf-8")
        agents = AGENTS_PATH.read_text(encoding="utf-8")
        readme = README_PATH.read_text(encoding="utf-8")
        rendered = subprocess.run(
            [
                sys.executable,
                str(REPOSITORY_ROOT / "scripts" / "render-agents-technology-skills.py"),
                "--project",
                str(REPOSITORY_ROOT / "PROJECT.yaml"),
            ],
            cwd=REPOSITORY_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, rendered.returncode, rendered.stderr)
        self.assertEqual(agents, rendered.stdout)
        for retired_text in (
            "definition_change_authority",
            "--check-definition-change",
            "--approval-record",
            "--regenerated-from",
            "--update-authority-directive",
            "Agent And Skill Definition Approval",
        ):
            with self.subTest(retired_text=retired_text):
                self.assertNotIn(retired_text, renderer)
                self.assertNotIn(retired_text, project)
                self.assertNotIn(retired_text, agents)
                self.assertNotIn(retired_text, readme)

    def test_agent_test_protocol_scopes_target_protection(self) -> None:
        """Keep target no-repair and finding routing local to agent evaluation work."""

        protocol = (AGENT_TEST_SUITES_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        for required_text in (
            "must not change a skill under test",
            "an agent definition or behavior under test",
            "generated target behavior under test",
            "or a product target merely to make the scenario pass",
            "Preserve the target bytes, digests, transcript, and failing evidence",
            "The authorized finding owner logs a target finding directly through the configured backlog path",
            "Use Dev Backlog Steward only for provider-wide inventory, normalization, archival audit, or recovery",
        ):
            with self.subTest(required_text=required_text):
                self.assertIn(required_text, protocol)

        self.assertNotIn("## Agent And Skill Definition Approval", AGENTS_PATH.read_text(encoding="utf-8"))



    def test_gitlab_work_item_skills_define_provider_native_authority_and_lifecycle(self) -> None:
        create_text = (SKILLS_ROOT / "create-work-item-gitlab" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        manage_text = (SKILLS_ROOT / "manage-work-items-gitlab" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        provider_contract_text = (
            REPOSITORY_ROOT
            / "design"
            / "work-item-provider-and-completion-contracts.md"
        ).read_text(encoding="utf-8")

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
            "enabled resource-coordination release evidence",
            "Only after the terminal update is observed",
            "return terminal evidence and lifecycle COMPLETED",
            "preserve the READY disposition",
            "Reopen only when authorized recovery",
            "Do not repeat an ambiguous mutation",
        ):
            with self.subTest(manage_phrase=phrase):
                self.assertIn(phrase, manage_text)

        for phrase in (
            "For feature-branch delivery, preserve lifecycle AWAITING_REVIEW for the same delivery identity.",
            "For main-branch delivery, preserve lifecycle RUNNING.",
            "Record lifecycle BLOCKED when safe reconciliation cannot continue.",
            "Never unconditionally reset lifecycle to RUNNING.",
        ):
            with self.subTest(reconciliation_phrase=phrase):
                self.assertIn(phrase, manage_text)
                self.assertIn(phrase, provider_contract_text)

        for stale_phrase in (
            "leave the lifecycle RUNNING or set it to BLOCKED",
            "keep lifecycle RUNNING or set it to BLOCKED",
            "remains lifecycle RUNNING or becomes BLOCKED",
            "remains RUNNING or BLOCKED",
        ):
            with self.subTest(stale_reconciliation_phrase=stale_phrase):
                self.assertNotIn(stale_phrase, manage_text)
                self.assertNotIn(stale_phrase, provider_contract_text)

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

        self.assertIn("## Create Or Update Pull Request", skill_text)
        self.assertNotIn("## Workflow", skill_text)

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

        role = load_yaml_object(ROLES_ROOT / "dev-activities" / "dev-coder.role.yaml")
        self.assertNotIn(
            "create-pull-request",
            {next(iter(entry)) for entry in role["skills"]},
        )
        feature_completion_text = (
            SKILLS_ROOT / "deliver-work-item-feature-branch" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "Apply [create-pull-request]",
            feature_completion_text,
        )

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

    def test_deliver_work_item_interface_routes_consumer_and_providers(self) -> None:
        """Delivery consumers must use one interface while Commit selects providers."""
        interface_name = "deliver-work-item"
        interface_path = SKILLS_ROOT / interface_name / "SKILL.md"
        interface_text = interface_path.read_text(encoding="utf-8")

        self.assertIn("name: deliver-work-item", interface_text)
        self.assertIn("# Deliver Work Item", interface_text)
        for heading in (
            "## Accepted Commit Input",
            "## Deliver Work Item",
            "## Delivery Results",
            "## Delivery Evidence",
            "## Provider Contract",
        ):
            with self.subTest(interface_heading=heading):
                self.assertIn(heading, interface_text)
        for phrase in (
            "Opaque Work Item ID and provider selector.",
            "Receive the already-resolved Commit provider",
            "If Commit is UNSET, return BLOCKED without selecting a default.",
            "must not modify the accepted commit",
            "preserve one delivery identity",
            "READY, AWAITING_REVIEW, or BLOCKED",
            "prepared Persistence handoff",
            "must not select a provider",
            "must not mutate Persistence or dispatch a provider manager",
        ):
            with self.subTest(interface_contract=phrase):
                self.assertIn(phrase, interface_text)
        self.assertNotIn(
            "Resolve the effective Commit-selected provider",
            interface_text,
        )

        self.assertTrue(openai_metadata_path(interface_name).is_file())

        orchestrator = load_yaml_object(
            ROLES_ROOT / "dev-activities" / "dev-orchestrator.role.yaml"
        )
        orchestrator_skills = {next(iter(entry)) for entry in orchestrator["skills"]}
        self.assertIn(interface_name, orchestrator_skills)
        self.assertTrue(
            orchestrator_skills.isdisjoint(
                {
                    "deliver-work-item-main-branch",
                    "deliver-work-item-feature-branch",
                }
            )
        )

        provider_results = {
            "deliver-work-item-main-branch": ("READY", "BLOCKED"),
            "deliver-work-item-feature-branch": (
                "READY",
                "AWAITING_REVIEW",
                "BLOCKED",
            ),
        }
        for provider_name, results in provider_results.items():
            provider_text = (
                SKILLS_ROOT / provider_name / "SKILL.md"
            ).read_text(encoding="utf-8")
            with self.subTest(provider=provider_name):
                self.assertIn("## Interface Conformance", provider_text)
                self.assertIn("deliver-work-item interface", provider_text)
                self.assertIn("does not select the Commit provider", provider_text)
                self.assertIn("does not mutate Persistence", provider_text)
                for result in results:
                    self.assertIn(result, provider_text)

        project = load_yaml_object(REPOSITORY_ROOT / "PROJECT.yaml")
        self.assertEqual(
            "main-branch",
            project["workflow_selection"]["commit"]["default"],
        )
        agents_text = AGENTS_PATH.read_text(encoding="utf-8")
        self.assertIn("Default commit main-branch: use deliver-work-item-main-branch", agents_text)
        self.assertNotIn("Default commit main-branch: use deliver-work-item.", agents_text)

        probes = load_yaml_object(REPOSITORY_ROOT / "evals" / "skill-probes.yaml")
        probe = next(
            entry
            for entry in probes["probes"]
            if entry["id"] == "probe-deliver-work-item"
        )
        self.assertEqual(interface_name, probe["skill"])
        self.assertEqual(
            ["dev-orchestrator-happy", "dev-orchestrator-boundary"],
            probe["scenarioAssociations"],
        )

        scenarios = load_yaml_object(
            AGENT_TEST_SUITES_ROOT / "dev-orchestrator" / "scenarios.yaml"
        )["scenarios"]
        dependency_routing = next(
            scenario
            for scenario in scenarios
            if scenario["id"] == "dependency-routing"
        )
        required_behaviors = dependency_routing["requiredBehaviors"]
        forbidden_behaviors = dependency_routing["forbiddenBehaviors"]
        self.assertIn(
            "Return one structured Commit result with READY, AWAITING_REVIEW, or BLOCKED",
            required_behaviors,
        )
        self.assertIn(
            "Record Persistence COMPLETED only after Commit READY",
            required_behaviors,
        )
        self.assertIn(
            "Leave Persistence nonterminal after Commit AWAITING_REVIEW or BLOCKED",
            required_behaviors,
        )
        self.assertIn(
            "Treat Commit AWAITING_REVIEW or BLOCKED as Persistence COMPLETED",
            forbidden_behaviors,
        )
        scenario_text = json.dumps(dependency_routing, sort_keys=True)
        self.assertNotIn("NEEDS_REVIEW", scenario_text)
        self.assertNotIn("delivery COMPLETED", scenario_text)

    def test_deliver_work_item_feature_branch_requires_observed_provider_accurate_merge(
        self,
    ) -> None:
        skill_path = (
            SKILLS_ROOT / "deliver-work-item-feature-branch" / "SKILL.md"
        )
        skill_text = skill_path.read_text(encoding="utf-8")

        self.assertIn("# Deliver Work Item Feature Branch", skill_text)
        self.assertIn("## Deliver Work Item", skill_text)

        for phrase in (
            "Consume an already accepted, independently reviewed and verified candidate commit.",
            "use create-pull-request and GitHub evidence. Call it a pull request.",
            "use the configured merge-request capability and GitLab evidence. Call it a merge request.",
            "Successful publication returns AWAITING_REVIEW",
            "A ready publication is not READY delivery evidence.",
            "Return every source correction request to the caller for Dev Orchestrator to route to the original Dev Coder.",
            "Resume the same branch, publication, and delivery identity only after the replacement candidate passes fresh independent review and verification.",
            "The pull request or merge request reports a merged state",
            "reachable from the configured base branch in Git",
            "A closed-unmerged, abandoned, replaced, or superseded publication cannot return READY.",
            "Work Item ID and provider selector",
            "the provider lifecycle update this evidence authorizes",
        ):
            with self.subTest(skill_phrase=phrase):
                self.assertIn(phrase, skill_text)

        self.assertIn(
            "- deliver-work-item-feature-branch",
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
            if entry["id"] == "probe-deliver-work-item-feature-branch"
        )
        self.assertEqual("deliver-work-item-feature-branch", probe["skill"])
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
            "Explicitly selected main-branch completion, or a request only to draft publication content without feature-branch delivery, does not activate this skill.",
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
            "probe-deliver-work-item-feature-branch",
            code_delivery["skillProbes"],
        )

    def test_workitem_provider_and_completion_processes_are_selector_driven(self) -> None:
        create_file_text = (
            SKILLS_ROOT / "create-work-item-file" / "SKILL.md"
        ).read_text(encoding="utf-8")
        manage_file_text = (
            SKILLS_ROOT / "manage-work-items-file" / "SKILL.md"
        ).read_text(encoding="utf-8")
        create_github_text = (
            SKILLS_ROOT / "create-work-item-github" / "SKILL.md"
        ).read_text(encoding="utf-8")
        manage_github_text = (
            SKILLS_ROOT / "manage-work-items-github" / "SKILL.md"
        ).read_text(encoding="utf-8")

        self.assertIn("effective provider is file", create_file_text)
        self.assertIn("effective provider is file", manage_file_text)
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
        self.assertNotIn("execute-workitem", coder_skills)
        self.assertNotIn("create-pull-request", coder_skills)
        self.assertIn("candidate handoff status", {
            next(iter(entry)) for entry in coder["outputContract"]
        })

        orchestrator = load_yaml_object(
            ROLES_ROOT / "dev-activities" / "dev-orchestrator.role.yaml"
        )
        orchestrator_skills = {
            next(iter(entry)) for entry in orchestrator["skills"]
        }
        self.assertNotIn("create-pull-request", orchestrator_skills)
        self.assertTrue(
            orchestrator_skills.isdisjoint(
                {
                    "create-work-item-file",
                    "create-work-item-github",
                    "manage-work-items-file",
                    "manage-work-items-github",
                    "deliver-work-item-main-branch",
                    "deliver-work-item-feature-branch",
                }
            )
        )
        self.assertNotIn("dev-backlog-steward", orchestrator["agentDependencies"])

        backlog_steward = load_yaml_object(
            ROLES_ROOT / "dev-activities" / "dev-backlog-steward.role.yaml"
        )
        backlog_text = json.dumps(backlog_steward, sort_keys=True)
        self.assertIn("provider-wide", backlog_text)
        self.assertIn("Do not perform Ready -> Starting", backlog_text)
        self.assertIn("ordinary lifecycle operations remain with the authorized Coordinator or Orchestrator", backlog_text)
        backlog_skills = {
            skill_name: metadata
            for entry in backlog_steward["skills"]
            for skill_name, metadata in entry.items()
        }
        self.assertTrue(
            backlog_skills.keys().isdisjoint(
                {
                    "create-work-item-file",
                    "create-work-item-github",
                    "manage-work-items-file",
                    "manage-work-items-github",
                }
            )
        )

        project_template = (
            SKILLS_ROOT
            / "route-documentation-work"
            / "assets"
            / "templates"
            / PROJECT_TEMPLATE
        ).read_text(encoding="utf-8")
        self.assertIn("workflow_selection:", project_template)
        self.assertIn("persistence:", project_template)
        self.assertIn("file, github, gitlab, azure-devops, jira, none, or UNSET", project_template)
        self.assertIn(
            'persistence: "TODO: file, github, gitlab, azure-devops, jira, none, or UNSET."',
            project_template,
        )
        self.assertIn("commit:", project_template)
        self.assertIn("main-branch, feature-branch, or UNSET", project_template)
        self.assertIn(
            'commit: "TODO: main-branch, feature-branch, or UNSET."',
            project_template,
        )
        self.assertNotIn("  provider:", project_template)
        self.assertNotIn("  completion:", project_template)
        self.assertNotIn("  workitem:", project_template)
        self.assertNotIn("  backlog:", project_template)

        project_configuration = load_yaml_object(REPOSITORY_ROOT / "PROJECT.yaml")
        self.assertEqual(
            "file",
            project_configuration["workflow_selection"]["persistence"]["default"],
        )
        self.assertEqual(
            "main-branch",
            project_configuration["workflow_selection"]["commit"]["default"],
        )
        agents_text = (REPOSITORY_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("## Work-Item Workflow Skill References", agents_text)
        self.assertIn("create-work-item-file", agents_text)
        self.assertIn("manage-work-items-file", agents_text)
        self.assertIn("deliver-work-item-main-branch", agents_text)
        self.assertIn("technology skill routing remains separate", agents_text)

        probes = load_yaml_object(REPOSITORY_ROOT / "evals" / "skill-probes.yaml")
        probe_ids = {entry["id"] for entry in probes["probes"]}
        for probe_id in (
            "probe-create-work-item-github",
            "probe-create-work-item-file",
            "probe-manage-work-items-github",
            "probe-manage-work-items-file",
            "probe-deliver-work-item",
            "probe-deliver-work-item-main-branch",
            "probe-deliver-work-item-feature-branch",
        ):
            self.assertIn(probe_id, probe_ids)
        for retired_probe_id in (
            "probe-execute-workitem",
            "probe-file-based-backlog",
            "probe-github-issues-backlog",
            "probe-create-backlog",
            "probe-manage-backlog",
        ):
            self.assertNotIn(retired_probe_id, probe_ids)

        readme_text = README_PATH.read_text(encoding="utf-8")
        for skill_name in (
            "create-work-item-github",
            "create-work-item-file",
            "manage-work-items-github",
            "manage-work-items-file",
            "deliver-work-item",
            "deliver-work-item-main-branch",
            "deliver-work-item-feature-branch",
        ):
            self.assertIn(f"- {skill_name}", readme_text)
        for retired_skill in (
            "create-backlog",
            "manage-backlog",
            "file-based-backlog",
            "github-issues-backlog",
            "execute-workitem",
        ):
            self.assertFalse((SKILLS_ROOT / retired_skill).exists())

    def test_dev_coder_and_orchestrator_preserve_candidate_review_commit_order(self) -> None:
        """Terminal Commit delivery must begin only after independent candidate acceptance."""
        coder = load_yaml_object(
            ROLES_ROOT / "dev-activities" / "dev-coder.role.yaml"
        )
        orchestrator = load_yaml_object(
            ROLES_ROOT / "dev-activities" / "dev-orchestrator.role.yaml"
        )
        coder_text = json.dumps(coder, sort_keys=True)
        orchestrator_text = json.dumps(orchestrator, sort_keys=True)

        self.assertIn(
            "Return a clean verified candidate commit to Dev Orchestrator for independent review.",
            coder_text,
        )
        self.assertIn("Do not apply the effective Commit-selected skill", coder_text)
        self.assertNotIn("applied the effective Commit-selected skill", coder_text)
        self.assertNotIn("main observation", coder_text)

        for phrase in (
            "Apply or resume the effective Commit-selected skill to the accepted direct or combined commit only after independent review and source verification pass.",
            "The effective Commit-selected skill returns the prepared terminal delivery handoff",
            "directly record the nonterminal AWAITING_REVIEW lifecycle update through the effective Persistence-selected management skill",
            "reconcile that recorded update instead of dispatching a duplicate",
            "Do not request lifecycle COMPLETED while Commit is AWAITING_REVIEW",
            "Resume the same effective Commit-selected skill through review corrections, checks, dependency order, merge, and main observation until it returns READY or BLOCKED.",
            "directly apply the effective Persistence-selected management skill for the distinct terminal COMPLETED update",
            "verify the selected manager's recorded closure and the applicable runtime cleanup before reporting READY",
            "When coordinate-codex-tasks is active, verify its terminal title handoff",
            "For other runtimes, do not require Codex title behavior",
            "For provider none, do not mutate Persistence",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, orchestrator_text)
        self.assertNotIn(
            "terminal central-contract conversation-title handoff",
            orchestrator_text,
        )

        workflow_text = "\n".join(orchestrator["instructions"]["workflow"])
        candidate_index = workflow_text.index("candidate commit")
        review_index = workflow_text.index("fresh read-only")
        commit_index = workflow_text.index(
            "Apply or resume the effective Commit-selected skill to the accepted direct or combined commit"
        )
        persistence_index = workflow_text.index(
            "directly record the nonterminal AWAITING_REVIEW lifecycle update through the effective Persistence-selected management skill"
        )
        self.assertLess(candidate_index, review_index)
        self.assertLess(review_index, commit_index)
        self.assertLess(commit_index, persistence_index)

        status_output = next(
            entry["status"]["purpose"]
            for entry in orchestrator["outputContract"]
            if "status" in entry
        )
        for status in ("READY", "AWAITING_REVIEW", "BLOCKED"):
            self.assertIn(status, status_output)

        ready_examples = [
            example["plausibleResponse"]
            for example in orchestrator["examples"]
            if "STATUS: READY" in example["plausibleResponse"]
        ]
        self.assertTrue(ready_examples)
        self.assertTrue(any("provider none" in response for response in ready_examples))
        for response in ready_examples:
            with self.subTest(ready_example=response[:80]):
                self.assertIn("Commit returned READY", response)
                commit_ready_index = response.index("Commit returned READY")
                if "provider none" in response:
                    finalization_index = response.index("task-local COMPLETED finalization")
                else:
                    terminal_dispatch = "Persistence manager directly"
                    self.assertIn(terminal_dispatch, response)
                    self.assertIn("recorded closure", response)
                    finalization_index = response.rindex(terminal_dispatch)
                    closure_index = response.index("recorded closure")
                    self.assertLess(finalization_index, closure_index)
                self.assertLess(commit_ready_index, finalization_index)

        provider_contract = (
            REPOSITORY_ROOT / "design" / "work-item-provider-and-completion-contracts.md"
        ).read_text(encoding="utf-8")
        for phrase in (
            "workflow_selection.persistence",
            "workflow_selection.commit",
            "Commit AWAITING_REVIEW",
            "Commit READY",
            "Persistence closure",
            "GitHub pull request",
            "GitLab merge request",
        ):
            with self.subTest(provider_contract=phrase):
                self.assertIn(phrase, provider_contract)
        self.assertNotIn("workflow_selection.provider", provider_contract)
        self.assertNotIn("workflow_selection.completion", provider_contract)

        lifecycle_text = (
            REPOSITORY_ROOT / "design" / "orchestrated-development-lifecycle.html"
        ).read_text(encoding="utf-8")
        for phrase in (
            "Commit AWAITING_REVIEW",
            "Commit READY",
            "Persistence closure",
            "pull request or GitLab merge request",
            "exactly once",
        ):
            with self.subTest(lifecycle_contract=phrase):
                self.assertIn(phrase, lifecycle_text)

        cases = load_yaml_object(REPOSITORY_ROOT / "evals" / "cases.yaml")["cases"]
        for case in cases:
            if "dev-coder" not in case.get("requiredAgents", []):
                continue
            with self.subTest(dev_coder_case=case["id"]):
                self.assertNotIn(
                    "deliver-work-item-main-branch",
                    case.get("requiredSkills", []),
                )
                self.assertNotIn(
                    "deliver-work-item-main-branch",
                    case.get("contextPack", {}).get("stagedSkillPackages", []),
                )

        for skill_name in ("create-work-item-file", "manage-work-items-file"):
            migration = (
                SKILLS_ROOT / skill_name / "SKILL.md"
            ).read_text(encoding="utf-8").split("## Migration", 1)[1]
            with self.subTest(skill_name=skill_name):
                self.assertIn("Callers migrated", migration)
                self.assertIn("legacy shells were removed", migration)
                self.assertIn("Historical mapping:", migration)
                self.assertNotIn("until their separately governed callers move", migration)

    def test_main_branch_completion_requires_integrated_main_evidence(self) -> None:
        skill_name = "deliver-work-item-main-branch"
        skill_path = SKILLS_ROOT / skill_name / "SKILL.md"
        skill_text = skill_path.read_text(encoding="utf-8")

        self.assertIn("# Deliver Work Item Main Branch", skill_text)
        self.assertIn("## Deliver Work Item", skill_text)

        required_phrases = (
            "This skill owns Git delivery and main observation.",
            "Provider closure remains a separate Persistence transaction.",
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
            if entry["id"] == "probe-deliver-work-item-main-branch"
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
            "probe-deliver-work-item-main-branch",
            code_delivery["skillProbes"],
        )
        self.assertTrue(
            (REPOSITORY_ROOT / "scripts" / "test_main_branch_completion_contract.py").is_file()
        )

    def test_review_and_verification_skills_use_operation_shaped_interfaces(self) -> None:
        expected_titles = {
            "review-code-with-evidence": "# Review Code With Evidence",
            "verify-end-to-end-workflow": "# Verify End To End Workflow",
            "analyze-root-cause": "# Analyze Root Cause",
            "collect-runtime-evidence": "# Collect Runtime Evidence",
            "trace-code-execution": "# Trace Code Execution",
            "review-prompt-contracts": "# Review Prompt Contracts",
        }
        retired_names = (
            "code-review-evidence",
            "end-to-end-verification",
            "root-cause-analysis",
            "runtime-evidence-collection",
            "code-execution-tracing",
            "prompt-contracts",
        )

        for skill_name, title in expected_titles.items():
            with self.subTest(skill_name=skill_name):
                skill_path = SKILLS_ROOT / skill_name / "SKILL.md"
                self.assertTrue(skill_path.is_file())
                skill_text = skill_path.read_text(encoding="utf-8")
                self.assertIn(f"name: {skill_name}", skill_text)
                self.assertIn(title, skill_text)

        for retired_name in retired_names:
            with self.subTest(retired_name=retired_name):
                self.assertFalse((SKILLS_ROOT / retired_name).exists())

        test_strategy = (SKILLS_ROOT / "test-strategy" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("## Select And Run Tests", test_strategy)
        self.assertNotIn("## Workflow", test_strategy)

        probes = load_yaml_object(REPOSITORY_ROOT / "evals" / "skill-probes.yaml")
        probe_ids = {entry["id"] for entry in probes["probes"]}
        for skill_name in expected_titles:
            self.assertIn(f"probe-{skill_name}", probe_ids)

    def test_documentation_methodology_skills_use_operation_shaped_interfaces(self) -> None:
        expected_titles = {
            "route-documentation-work": "# Route Documentation Work",
            "bootstrap-project-documentation": "# Bootstrap Project Documentation",
            "reverse-engineer-project-documentation": "# Reverse Engineer Project Documentation",
            "verify-documentation-page": "# Verify Documentation Page",
        }
        retired_names = (
            "development-methodology",
            "documentation-bootstrap",
            "documentation-reverse-engineer",
            "documentation-page-verify",
        )

        for skill_name, title in expected_titles.items():
            with self.subTest(skill_name=skill_name):
                skill_path = SKILLS_ROOT / skill_name / "SKILL.md"
                self.assertTrue(skill_path.is_file())
                skill_text = skill_path.read_text(encoding="utf-8")
                self.assertIn(f"name: {skill_name}", skill_text)
                self.assertIn(title, skill_text)

        for retired_name in retired_names:
            with self.subTest(retired_name=retired_name):
                self.assertFalse((SKILLS_ROOT / retired_name).exists())

        probes = load_yaml_object(REPOSITORY_ROOT / "evals" / "skill-probes.yaml")
        probe_ids = {entry["id"] for entry in probes["probes"]}
        for skill_name in expected_titles:
            self.assertIn(f"probe-{skill_name}", probe_ids)

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
            "Add Code Artifact Header",
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
            SKILLS_ROOT / "route-documentation-work" / "SKILL.md"
        ).read_text(encoding="utf-8")

        for skill_name, template_name, review_skill_name in ARTIFACT_CREATION_SKILLS:
            with self.subTest(skill_name=skill_name):
                skill_path = SKILLS_ROOT / skill_name / "SKILL.md"
                template_path = (
                    SKILLS_ROOT
                    / "route-documentation-work"
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
                self.assertIn("verify-documentation-page", skill_text)
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
                    "skip any leading retained explanatory note or notes",
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
                    / "route-documentation-work"
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
                        "After any leading retained explanatory note or notes, begin the first authored decision with **READY.** or **BLOCKED.**",
                    )
                    if skill_name == "create-module-design"
                    else ()
                ):
                    self.assertIn(phrase, template_text)

        module_template = (
            SKILLS_ROOT
            / "route-documentation-work"
            / "assets"
            / "templates"
            / "module-design-template.md"
        ).read_text(encoding="utf-8")
        module_create = (SKILLS_ROOT / "create-module-design" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        module_review = (SKILLS_ROOT / "review-module-design" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "Treat every level-two heading in the template as mandatory.",
            module_create,
        )
        self.assertIn(
            "Every template heading is mandatory and must retain its exact text and order",
            module_review,
        )
        for phrase in (
            "path, body, token, session, message, or persistence identifiers",
            "synchronous and asynchronous failure behavior",
            "which side effects have already committed",
            "Sensitive data and logging",
        ):
            self.assertIn(phrase, module_template)

        mandatory_section_instructions = (
            (
                "## Configuration",
                "TODO: Retain this section. If the module has no configuration, "
                "state why configuration is not applicable.",
                "TODO: Remove this section if the module has no configuration.",
                "Not applicable because this module has no configuration.",
            ),
            (
                "## External Interfaces",
                "TODO: Retain this section. If the module has no external interface, "
                "state why external interfaces are not applicable.",
                "TODO: Remove this section if the module has no external interface.",
                "Not applicable because this module has no external interface.",
            ),
            (
                "## UI And Notification Behavior",
                "TODO: Retain this section. If the module has no UI or notification "
                "behavior, state why UI and notification behavior are not applicable.",
                "TODO: Remove this section if the module has no UI or notification "
                "behavior.",
                "Not applicable because this module has no UI or notification behavior.",
            ),
        )
        representative_module = module_template
        for _, instruction, _, explanation in mandatory_section_instructions:
            representative_module = representative_module.replace(
                instruction,
                explanation,
            )

        template_headings = re.findall(r"^## .+$", module_template, flags=re.MULTILINE)
        representative_headings = re.findall(
            r"^## .+$",
            representative_module,
            flags=re.MULTILINE,
        )
        self.assertEqual(template_headings, representative_headings)

        for heading, instruction, removal_instruction, explanation in (
            mandatory_section_instructions
        ):
            with self.subTest(mandatory_module_section=heading):
                self.assertEqual(1, module_template.count(heading))
                self.assertIn(instruction, module_template)
                self.assertNotIn(removal_instruction, module_template)
                self.assertRegex(
                    representative_module,
                    rf"(?ms)^{re.escape(heading)}$.*?^{re.escape(explanation)}$"
                    r".*?(?=^## |\Z)",
                )

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
            / "route-documentation-work"
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
                / "route-documentation-work"
                / "assets"
                / "templates"
                / template_name
            ).read_text(encoding="utf-8")

        def checklist_text(skill_name: str, checklist_name: str) -> str:
            return (
                SKILLS_ROOT / skill_name / "references" / checklist_name
            ).read_text(encoding="utf-8")

        development_text = skill_text("route-documentation-work")
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

        def assert_terms(text: str, terms: tuple[str, ...]) -> None:
            for term in terms:
                self.assertIn(term, text)

        architecture_surfaces = {
            "create": architecture_create,
            "review": architecture_review,
            "template": templates["architecture-template.md"],
            "checklist": checklists["architecture"],
        }
        architecture_triggers = (
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
        for name, text in architecture_surfaces.items():
            with self.subTest(architecture_ordered_surface=name):
                rule = line_containing(text, architecture_triggers[0])
                assert_terms(rule, architecture_triggers)
                assert_terms(rule.lower(), ("diagram", "prose", "numbered list", "table"))
                self.assertRegex(rule.lower(), r"must not carry|instead of leaving")
                additive_rule = line_containing(text, "additive minimum")
                self.assertIn("shared route-documentation-work rule", additive_rule)
                self.assertRegex(
                    additive_rule,
                    r"does not waive another shared trigger|"
                    r"without using one satisfied section trigger to waive another shared trigger",
                )

        functional_surfaces = {
            "create": (functional_create, "Mermaid workflow diagram whenever"),
            "review": (functional_review, "Mermaid diagram whenever"),
            "template": (
                templates["functional-spec-template.md"],
                "Mermaid diagram whenever",
            ),
            "checklist": (
                checklists["functional-spec"],
                "appropriate Mermaid sequence, state, or flow diagram",
            ),
        }
        functional_triggers = (
            "two or more ordered actor actions",
            "branch",
            "permission gate",
            "alternate path",
            "recovery path",
            "state transition",
            "external handoff",
        )
        for name, (text, marker) in functional_surfaces.items():
            with self.subTest(functional_ordered_surface=name):
                rule = line_containing(text, marker)
                assert_terms(rule, functional_triggers)
                assert_terms(rule.lower(), ("mermaid", "prose", "numbered list", "table"))
                verification_exception = line_containing(text, "verification-step lists")
                assert_terms(verification_exception, ("test procedures", "trigger"))

        module_surfaces = {
            "create": module_create,
            "review": module_review,
            "template": templates["module-design-template.md"],
            "checklist": checklists["module-design"],
        }
        module_disqualifiers = (
            "branch",
            "retry",
            "error path",
            "state transition",
            "external handoff",
            "asynchronous phase transition",
        )
        for name, text in module_surfaces.items():
            with self.subTest(module_synchronous_exception_surface=name):
                rule = line_containing(text, "one-row synchronous effect")
                self.assertRegex(rule, r"exception|exempting|may omit|omission")
                self.assertRegex(rule, r"only when.*\bno\b")
                assert_terms(rule, module_disqualifiers)

        path_tree_contracts = {
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
        for name, contract in path_tree_contracts.items():
            text = templates[name]
            contract_text = " ".join(text.split())
            if name == "project-template.yaml":
                contract_text = " ".join(
                    line.removeprefix("#").strip()
                    for line in text.splitlines()
                    if line.startswith("#")
                )
            with self.subTest(path_tree_template=name):
                assert_terms(
                    contract_text,
                    (
                        contract["trigger"],
                        contract["complete"],
                        "Path tree example",
                        "fenced text tree",
                        contract["split"],
                        contract["metadata"],
                        "Markdown table cells",
                    ),
                )
                assert_terms(contract_text, contract["deduplicate"])
                self.assertNotRegex(text, r"<br\s*/?>")
                if name != "project-template.yaml":
                    assert_terms(text, ("```text", "HTML breaks"))

        project_template = templates["project-template.yaml"]
        assert_terms(
            project_template,
            ("schema-required path arrays below machine-readable", "generated prose"),
        )
        configured_paths = yaml.safe_load(project_template)["project_taxonomy"][
            "application_tiers"
        ][0]["paths"]
        self.assertTrue(
            isinstance(configured_paths, list)
            and bool(configured_paths)
            and all(isinstance(path, str) and path for path in configured_paths)
        )

        for name, text in checklists.items():
            questions, findings = text.split("## Findings", maxsplit=1)
            with self.subTest(path_tree_checklist_enforcement=name):
                assert_terms(
                    questions,
                    (
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
                    ),
                )
                assert_terms(
                    findings,
                    (
                        "a missing or malformed required path tree",
                        "missing complete repository-relative tree segments",
                        "unsplit large trees",
                        "tree metadata separated from its owning tree",
                        "table-cell or HTML-simulated trees",
                        "duplicated full paths or common prefixes",
                    ),
                )

        hld_create_rule = line_containing(hld_create, "ordered sequence")
        assert_terms(
            hld_create_rule, ("dependent implementation steps", "complete sequence alone")
        )
        hld_review_rule = line_containing(hld_review, "ordered sequence")
        assert_terms(
            hld_review_rule,
            ("dependent implementation steps", "response-adequacy finding"),
        )
        hld_template = templates["high-level-design-template.md"]
        implementation_rule = line_containing(
            hld_template, "ordered or dependent implementation actions"
        )
        assert_terms(implementation_rule, ("verification gates", "complete sequence only"))
        verification_rule = line_containing(
            hld_template, "dependency order and required verification gates"
        )
        self.assertIn("Implementation Sequence Diagram", verification_rule)
        hld_questions, hld_findings = checklists["high-level-design"].split(
            "## Findings", maxsplit=1
        )
        assert_terms(
            line_containing(hld_questions, "ordered sequence"),
            ("dependent implementation steps", "Mermaid sequence, state, or flow diagram"),
        )
        self.assertIn("Does Implementation Order give a credible sequence", hld_questions)
        self.assertIn(
            "an ordered action sequence left only in prose, a numbered list, or a table",
            hld_findings,
        )

    def test_hld_data_anchors_are_actionable_for_downstream_design(self) -> None:
        """Keep HLD anchors concrete, owned, and reusable by later designs."""
        template_text = (
            SKILLS_ROOT
            / "route-documentation-work"
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
            / "route-documentation-work"
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
            / "route-documentation-work"
            / "assets"
            / "templates"
            / "high-level-design-template.md"
        ).read_text(encoding="utf-8")
        self.assertIn("exact route variant or supporting UI action", hld_template)
        self.assertIn(
            "anonymous, authenticated, administrator, service, or background actor",
            hld_template,
        )

    def test_functional_spec_interface_examples_are_proportionate(self) -> None:
        """Require interface-specific examples without imposing universal UI mockups."""
        surfaces = (
            (SKILLS_ROOT / "create-functional-spec" / "SKILL.md").read_text(
                encoding="utf-8"
            ),
            (
                SKILLS_ROOT
                / "route-documentation-work"
                / "assets"
                / "templates"
                / "functional-spec-template.md"
            ).read_text(encoding="utf-8"),
            (
                SKILLS_ROOT
                / "review-functional-spec"
                / "references"
                / "review-checklist-functional-spec.md"
            ).read_text(encoding="utf-8"),
        )

        required_contracts = (
            "mockup, wireframe, or interaction diagram",
            "spatial placement, ordering, grouping, relative prominence",
            "two or more view states that must be compared",
            "responsive or conditional layout",
            "method, path, query parameters, headers, authentication, and request body",
            "response status, headers, and body",
            "validation, authentication, and conflict cases",
            "representative payload and a producer-consumer sequence",
            "representative invocation, output, and failure",
            "concrete no-example rationale",
            "only when no required interface example",
            "why an additional example would add no contract information",
            "exact prose, table, or verification block",
            "distinct inputs, outcomes, and failures",
        )
        for text in surfaces:
            with self.subTest(surface=text[:80]):
                for contract in required_contracts:
                    self.assertIn(contract, text)

        for guidance_text in surfaces[:2]:
            self.assertIn(
                "does not require HTML or a UI mockup for every functional specification",
                guidance_text,
            )
        self.assertIn(
            "select proportionate examples from the documented interface type and behavior",
            surfaces[2],
        )

    def test_project_configuration_routes_to_template_and_verifier(self) -> None:
        development_methodology_text = (
            SKILLS_ROOT / "route-documentation-work" / "SKILL.md"
        ).read_text(encoding="utf-8")
        skill_path = SKILLS_ROOT / PROJECT_CONFIGURATION_SKILL / "SKILL.md"
        template_path = (
            SKILLS_ROOT
            / "route-documentation-work"
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
        self.assertIn("verify-documentation-page", skill_text)
        self.assertIn("customer-safe examples", skill_text)
        self.assertIn("schema: project", template_text)
        self.assertIn("proprietary_validation_notes:", template_text)
        self.assertIn("nested_agents_files:", template_text)
        self.assertIn("resource_coordination:", template_text)
        self.assertIn("selected: \"TODO: none or resource-claim", template_text)
        self.assertIn("agent_claim_transport:", template_text)
        self.assertIn("selected: \"TODO: mcp or command", template_text)
        self.assertIn("claim helper from target-runtime evidence", template_text)
        self.assertIn(
            "verifies the selected claim helper",
            template_text,
        )
        self.assertNotIn("claim-helper interface", template_text)
        self.assertIn("This required project-wide setting has no folder overrides", skill_text)
        self.assertIn(
            "The PROJECT.yaml field agent_claim_transport selects the claim helper",
            skill_text,
        )
        self.assertIn("When resource-claim is selected, add resource_coordination.deadline_policy", skill_text)
        self.assertIn("For resource-claim, include only the selected claim helper", skill_text)
        self.assertIn(
            "For none, include no claim skill, helper, procedure, or evidence",
            skill_text,
        )
        self.assertIn("workflow_selection:", template_text)
        self.assertIn("project_skill_extensions: []", template_text)
        self.assertIn("file, github, gitlab, azure-devops, jira, none, or UNSET", template_text)
        self.assertIn("main-branch, feature-branch, or UNSET", template_text)
        self.assertIn("simple-workitem to main-branch", skill_text)
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
        self.assertIn("Generated workflow guidance references selected skills by name", skill_text)
        self.assertIn("record explicit UNSET rather than omitting a deferred decision", skill_text)
        self.assertIn("one exact folder pattern may appear only once", skill_text)
        self.assertIn("one exact folder pattern may appear only once", template_text)
        self.assertNotIn("nested_project_files:", template_text)

        self.assertIn("Create exactly one PROJECT.yaml", skill_text)
        self.assertIn("Do not create nested PROJECT.yaml files", skill_text)
        self.assertIn("intermediate, reviewable intent log", skill_text)
        self.assertIn("treat them as requested configuration intent", skill_text)
        self.assertIn("Project Configurator owns the setup process", modularization_text)
        self.assertIn(
            "Resource-claim requires one verified claim helper",
            modularization_text,
        )
        self.assertIn(
            "For none, confirm there is no claim skill, helper, worktree requirement, or claim evidence",
            modularization_text,
        )
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
            "repositoryMutation belongs to conceptual agent definitions and does not select claim behavior",
            skill_text,
        )
        self.assertIn(
            "Generated AGENTS.md references resource-claim and includes only the selected claim helper's instructions",
            skill_text,
        )
        self.assertIn(
            "AGENTS.md references resource-claim and includes only the selected helper provider",
            skill_text,
        )
        self.assertNotIn("selected helper by reference", skill_text)
        self.assertIn("Keep workflow configuration selector-only", skill_text)
        self.assertIn("Do not infer either selector", skill_text)
        development_methodology_text = (
            SKILLS_ROOT / "route-documentation-work" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("ordered project-level skill extensions", development_methodology_text)
        readme_text = (REPOSITORY_ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("ordered project_skill_extensions list", readme_text)
        self.assertIn("final root-only section", readme_text)
        self.assertIn(
            "Treat a missing definition, skill, helper operation, or helper field as BLOCKED",
            skill_text,
        )
        self.assertIn("resource-claim", skill_text)
        self.assertIn("exact anchored /.worktrees/ entry", skill_text)
        self.assertIn("Do not store a machine-specific absolute worktree path", skill_text)
        self.assertIn(
            "When resource_coordination selects resource-claim, the .worktrees directory is ignored operational state immediately beneath the primary worktree",
            template_text,
        )
        self.assertIn(
            "When resource-claim is selected, contains the anchored /.worktrees/ entry",
            template_text,
        )
        self.assertIn("worktree ignore behavior", modularization_text)
        self.assertIn("thin CLAUDE.md", skill_text)
        self.assertIn(PROJECT_CONFIGURATION_SKILL, development_methodology_text)
        self.assertIn(PROJECT_TEMPLATE, development_methodology_text)
        self.assertIn("verify-documentation-page", development_methodology_text)

    def test_project_and_template_publish_initial_resource_deadline_defaults(self) -> None:
        """Keep setup defaults observable and editable through the project policy path."""

        expected = {
            "backlog-mutation": {
                "maximum_duration_seconds": 600,
                "cleanup_grace_seconds": 120,
            },
            "main-integration": {
                "maximum_duration_seconds": 2700,
                "cleanup_grace_seconds": 600,
            },
            "browser-server": {
                "maximum_duration_seconds": 3600,
                "cleanup_grace_seconds": 600,
            },
            "database-port": {
                "maximum_duration_seconds": 1800,
                "cleanup_grace_seconds": 300,
            },
            "live-model-evaluation": {
                "maximum_duration_seconds": 14400,
                "cleanup_grace_seconds": 1800,
            },
        }
        template_path = (
            SKILLS_ROOT
            / "route-documentation-work"
            / "assets"
            / "templates"
            / PROJECT_TEMPLATE
        )
        for path in (REPOSITORY_ROOT / "PROJECT.yaml", template_path):
            with self.subTest(path=path):
                project = load_yaml_object(path)
                policy = project["resource_coordination"]["deadline_policy"]
                self.assertEqual(expected, policy["resource_classes"])
                self.assertEqual({}, policy["resource_overrides"])

    def test_artifact_review_skills_have_checklists_and_metadata(self) -> None:
        development_methodology_text = (
            SKILLS_ROOT / "route-documentation-work" / "SKILL.md"
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
                self.assertIn("verify-documentation-page", skill_text)
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
                legacy_evidence = "Quoted evidence:" in checklist_text
                typed_evidence = all(
                    field in checklist_text
                    for field in (
                        "Evidence type:",
                        "Evidence source:",
                        "Evidence:",
                    )
                )
                self.assertTrue(legacy_evidence or typed_evidence)
                self.assertIn("Assessment:", checklist_text)
                self.assertIn("?", checklist_text)

    def test_typed_review_evidence_covers_each_completion_case(self) -> None:
        """Keep typed review evidence honest when literal source text is unavailable."""
        for skill_name, review_target in (
            ("review-architecture", "architecture"),
            ("review-functional-spec", "functional-spec"),
            ("review-high-level-design", "high-level-design"),
        ):
            skill_text = (SKILLS_ROOT / skill_name / "SKILL.md").read_text(
                encoding="utf-8"
            )
            checklist_text = (
                SKILLS_ROOT
                / skill_name
                / "references"
                / review_checklist_name(review_target)
            ).read_text(encoding="utf-8")

            for text in (skill_text, checklist_text):
                for field in (
                    "Status:",
                    "Question:",
                    "Evidence type:",
                    "Evidence source:",
                    "Evidence:",
                    "Assessment:",
                ):
                    with self.subTest(skill_name=skill_name, field=field):
                        self.assertIn(field, text)

                cases = {
                    "mode-dependent n/a": (
                        "mode-dependent n/a",
                        "Evidence type: not applicable",
                        "rather than fabricating a quotation",
                    ),
                    "missing contract": (
                        "required contract is missing",
                        "summary or assessment evidence",
                        "mark the item fail",
                    ),
                    "literal quotation": (
                        "exact quotation only for literal source text",
                        "occurs in the named evidence source",
                    ),
                }
                for case_name, phrases in cases.items():
                    with self.subTest(skill_name=skill_name, case=case_name):
                        for phrase in phrases:
                            self.assertIn(phrase, text)

            self.assertNotIn("- Quoted evidence:", checklist_text)

    def test_review_unit_test_plan_uses_shared_typed_evidence_contract(self) -> None:
        skill_text = (
            SKILLS_ROOT / "review-unit-test-plan" / "SKILL.md"
        ).read_text(encoding="utf-8")
        checklist_text = (
            SKILLS_ROOT
            / "review-unit-test-plan"
            / "references"
            / "review-checklist-unit-test-plan.md"
        ).read_text(encoding="utf-8")

        for field in (
            "Status:",
            "Question:",
            "Evidence type:",
            "Evidence source:",
            "Evidence:",
            "Assessment:",
        ):
            with self.subTest(field=field):
                self.assertIn(field, checklist_text)

        self.assertNotIn("- Quoted evidence:", checklist_text)
        self.assertIn("source conflict or required text is absent", checklist_text)
        self.assertIn("assessment or summary", checklist_text)
        self.assertIn("not applicable with a reason", checklist_text)
        self.assertIn("Every exact quotation must occur in the named source", checklist_text)
        self.assertIn("summary for paraphrased source meaning", skill_text)
        self.assertIn("assessment for a derived finding", skill_text)
        self.assertIn("not applicable with a reason", skill_text)
        self.assertIn("Resolve every exact quotation", skill_text)

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
                        "skip any leading retained explanatory note or notes",
                        "scope-bearing qualifier",
                    )
                    if skill_name == "review-module-design"
                    else ()
                ):
                    self.assertIn(phrase, checklist_text)

    def test_documentation_page_verifier_uses_completed_checklist_evidence(self) -> None:
        skill_text = (
            SKILLS_ROOT / "verify-documentation-page" / "SKILL.md"
        ).read_text(encoding="utf-8")

        for phrase in DOCUMENTATION_PAGE_VERIFIER_REVIEW_PHRASES:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, skill_text)

    def test_document_reviews_apply_three_checks_to_every_sentence(self) -> None:
        verifier_text = (
            SKILLS_ROOT / "verify-documentation-page" / "SKILL.md"
        ).read_text(encoding="utf-8")
        reviewer_text = (
            SKILLS_ROOT / "review-structured-artifact" / "SKILL.md"
        ).read_text(encoding="utf-8")
        checklist_text = (
            SKILLS_ROOT
            / "review-structured-artifact"
            / "references"
            / "review-checklist-structured.md"
        ).read_text(encoding="utf-8")

        for text in (verifier_text, checklist_text):
            with self.subTest(document="sentence review contract"):
                self.assertIn("Needed:", text)
                self.assertIn("Clear:", text)
                self.assertIn("Definite reference:", text)
                self.assertIn("every prose sentence", text)
                self.assertIn("table row or list item", text)
                self.assertIn("uses “the” before a common noun", text)

        self.assertIn("Use verify-documentation-page", reviewer_text)
        self.assertIn("three sentence checks", reviewer_text)
        self.assertIn("completed checklist", reviewer_text)

    def test_documentation_writing_skills_require_lists_for_enumerated_prose(
        self,
    ) -> None:
        writer_phrases = (
            "Do not pack a sequence or enumeration into a long paragraph.",
            "Treat three or more distinct steps or items in one paragraph as a list-structure trigger.",
            "use a numbered list for ordered steps and a bulleted list for unordered items",
            "keep one coherent step or item in each entry",
        )
        verifier_phrases = (
            "Flag a long paragraph that carries a sequence or enumeration",
            "Treat three or more distinct steps or items in one paragraph as a finding.",
            "Require a numbered list for ordered steps and a bulleted list for unordered items",
        )

        for skill_name in DOCUMENTATION_LIST_WRITER_SKILLS:
            skill_text = (SKILLS_ROOT / skill_name / "SKILL.md").read_text(
                encoding="utf-8"
            )
            for phrase in writer_phrases:
                with self.subTest(skill_name=skill_name, phrase=phrase):
                    self.assertIn(phrase, skill_text)

        for skill_name in DOCUMENTATION_LIST_VERIFIER_SKILLS:
            skill_text = (SKILLS_ROOT / skill_name / "SKILL.md").read_text(
                encoding="utf-8"
            )
            for phrase in verifier_phrases:
                with self.subTest(skill_name=skill_name, phrase=phrase):
                    self.assertIn(phrase, skill_text)

    def test_example_project_skill_packs_are_packaged(self) -> None:
        for skill_name in EXAMPLE_PROJECT_SKILL_PACKS:
            with self.subTest(skill_name=skill_name):
                skill_path = SKILLS_ROOT / skill_name / "SKILL.md"
                self.assertTrue(skill_path.is_file())
                self.assertTrue(openai_metadata_path(skill_name).is_file())

    def test_dev_backlog_steward_requires_starting_blocked_work_resumption(self) -> None:
        """The suite preserves the staged Blocked resumption contract."""
        suite_root = AGENT_TEST_SUITES_ROOT / "dev-backlog-steward"
        manage_file_text = (
            SKILLS_ROOT / "manage-work-items-file" / "SKILL.md"
        ).read_text(encoding="utf-8")
        coordination_text = (
            SKILLS_ROOT / "coordinate-work-items" / "SKILL.md"
        ).read_text(encoding="utf-8")
        role = load_yaml_object(
            ROLES_ROOT / "dev-activities" / "dev-backlog-steward.role.yaml"
        )
        role_text = (
            ROLES_ROOT / "dev-activities" / "dev-backlog-steward.role.yaml"
        ).read_text(encoding="utf-8")
        self.assertIn("provider-wide backlog inventory", role_text)
        self.assertIn(
            "ordinary lifecycle\n  operations remain with the authorized Coordinator or Orchestrator",
            role_text,
        )
        workflow_text = "\n".join(role["instructions"]["workflow"])
        self.assertIn(
            "return its separate result without entering ordinary lifecycle management",
            workflow_text.lower(),
        )
        boundaries_text = "\n".join(role["instructions"]["boundaries"])
        self.assertIn(
            "The authorized Dev Backlog Coordinator or Dev Orchestrator applies",
            boundaries_text,
        )
        self.assertNotIn("user action brief", role_text.lower())

        for required_phrase in (
            "## Blocked Handoff And Resumption",
            "Set Status to Blocked and Owner to Unowned",
            "restore Status: Ready with Owner: Unowned",
            "When the parent Dev Backlog Coordinator authorizes Ready -> Starting",
            "When the root Dev Orchestrator authorizes Starting -> Running",
            "restore the byte-for-byte pre-attempt Blocked item",
            "Provider mutation protection cannot substitute for delivery ownership.",
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
                self.assertIn("manage-work-items-file", target_skills)
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
        judge_text = (suite_root / "agents" / "judge.toml").read_text(
            encoding="utf-8"
        )
        self.assertIn("reject direct unowned Blocked to Running", judge_text)
        self.assertIn("byte-for-byte pre-attempt Blocked item", judge_text)

    def test_file_future_idea_skills_have_non_overlapping_ownership(self) -> None:
        """Future Ideas and file transactions have dedicated peer contracts."""
        suite_root = AGENT_TEST_SUITES_ROOT / "dev-backlog-steward"
        create_file_text = (
            SKILLS_ROOT / "create-work-item-file" / "SKILL.md"
        ).read_text(encoding="utf-8")
        manage_file_text = (
            SKILLS_ROOT / "manage-work-items-file" / "SKILL.md"
        ).read_text(encoding="utf-8")
        future_ideas_text = (
            SKILLS_ROOT / "manage-future-ideas" / "SKILL.md"
        ).read_text(encoding="utf-8")
        transaction_text = (
            SKILLS_ROOT / "commit-file-provider-transaction" / "SKILL.md"
        ).read_text(encoding="utf-8")
        role = load_yaml_object(
            ROLES_ROOT / "dev-activities" / "dev-backlog-steward.role.yaml"
        )
        role_text = (
            ROLES_ROOT / "dev-activities" / "dev-backlog-steward.role.yaml"
        ).read_text(encoding="utf-8")
        suite = load_yaml_object(suite_root / "suite.yaml")
        probes = load_yaml_object(REPOSITORY_ROOT / "evals" / "skill-probes.yaml")
        cases = load_yaml_object(REPOSITORY_ROOT / "evals" / "cases.yaml")

        self.assertIn("## Future Ideas Boundary", create_file_text)
        self.assertIn("manage-future-ideas", create_file_text)
        self.assertIn("commit-file-provider-transaction", create_file_text)
        self.assertNotIn("## Future Ideas Capture", create_file_text)
        self.assertNotIn("## Future Idea Promotion", create_file_text)
        self.assertNotIn("## Exact Backlog Creation Transaction", create_file_text)

        self.assertIn("## Future Ideas Exclusion", manage_file_text)
        self.assertIn("manage-future-ideas", manage_file_text)
        self.assertNotIn("## Future Ideas Workflow", manage_file_text)
        self.assertNotIn("Validate only a title, Synopsis", manage_file_text)

        for required_phrase in (
            "## Future Ideas Definition",
            "## Capture Future Idea",
            "## Inventory And Validate Future Ideas",
            "## Promote Future Idea",
            "## Result",
            "file-provider-only",
            "not work items or lifecycle",
            "selects Future Ideas",
            "resolved regular files",
            "free text",
            "Promoted To",
            "reciprocal Source Evidence",
            "commit-file-provider-transaction",
            "For capture and promotion, also return the transaction commit",
        ):
            with self.subTest(future_ideas_contract=required_phrase):
                self.assertIn(required_phrase, future_ideas_text)

        for required_phrase in (
            "## Commit File Provider Transaction",
            "ordinary-creation",
            "future-idea-promotion",
            "exact full Git index file bytes and existence",
            "exclusive-create",
            "git commit --only",
            "immutable commit object",
            "unrelated staged",
            "Rollback",
            "After every applicable source and destination path claim",
            "Re-read and re-resolve every manifest path",
            "Current source bytes, file type, canonical containment, and authority.",
            "Continued destination absence and canonical destination containment and authority.",
            "captured HEAD, exact Git index bytes and existence",
            "Return zero-mutation BLOCKED",
            "Do not create a destination, write a source, stage, or commit",
        ):
            with self.subTest(transaction_contract=required_phrase):
                self.assertIn(required_phrase, " ".join(transaction_text.split()))

        role_skills = {
            skill_name: metadata
            for entry in role["skills"]
            for skill_name, metadata in entry.items()
        }
        self.assertIn("manage-future-ideas", role_skills)
        self.assertIn("condition", role_skills["manage-future-ideas"])
        self.assertIn(
            "bounded exception for explicitly requested Future Ideas",
            " ".join(role_text.split()),
        )
        self.assertNotIn("commit-file-provider-transaction", role_text)
        self.assertIn(
            "preserve and report the recovery result from manage-future-ideas",
            " ".join(role_text.split()).lower(),
        )
        self.assertIn("backlog item, Future Idea, or status update", {
            next(iter(entry)) for entry in role["outputContract"]
        })

        scenarios = load_yaml_object(suite_root / "scenarios.yaml")["scenarios"]
        by_id = {scenario["id"]: scenario for scenario in scenarios}
        future_scenario = by_id["future-ideas-capture-and-promotion"]
        self.assertEqual("PASS", future_scenario["expectedTerminalStatus"])
        self.assertIn("manage-future-ideas", future_scenario["targetSkills"])
        self.assertIn(
            "commit-file-provider-transaction", future_scenario["targetSkills"]
        )
        self.assertNotIn("manage-work-items-file", future_scenario["targetSkills"])
        inventory_scenario = by_id["future-ideas-inventory-and-validation"]
        self.assertEqual("executable", inventory_scenario["status"])
        self.assertEqual(
            "fixtures/cases.yaml", inventory_scenario["executableCase"]
        )
        self.assertIn("manage-future-ideas", inventory_scenario["targetSkills"])
        self.assertNotIn(
            "commit-file-provider-transaction", inventory_scenario["targetSkills"]
        )
        self.assertNotIn("create-work-item-file", inventory_scenario["targetSkills"])
        self.assertEqual(
            ["skills/dev-backlog-steward-suite-contract/SKILL.md"],
            suite["projectSkills"]["suite"],
        )
        self.assertEqual(
            "contract_harness.py",
            suite["execution"]["deterministicSimulator"],
        )
        self.assertEqual(
            "test_contract.py",
            suite["execution"]["deterministicTests"],
        )

        probes_by_id = {probe["id"]: probe for probe in probes["probes"]}
        cases_by_id = {case["id"]: case for case in cases["cases"]}
        case_id = "file-work-item-template-contract"
        for probe_id in (
            "probe-manage-future-ideas",
            "probe-commit-file-provider-transaction",
        ):
            with self.subTest(declared_probe=probe_id):
                self.assertEqual([], probes_by_id[probe_id]["executableCases"])
                self.assertEqual("declared", probes_by_id[probe_id]["coverageStatus"])
                self.assertNotIn(probe_id, cases_by_id[case_id]["skillProbes"])
                self.assertNotIn(
                    probe_id, cases_by_id[case_id]["fixtureBackedProbeClaims"]
                )
        self.assertTrue((suite_root / "contract_harness.py").is_file())

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

    def test_terminology_standard_family_is_positive_first_and_role_routed(self) -> None:
        skill_names = (
            "terminology-standard",
            "terminology-standard-review",
            "terminology-standard-update",
        )
        skill_texts = {
            skill_name: (SKILLS_ROOT / skill_name / "SKILL.md").read_text(
                encoding="utf-8"
            )
            for skill_name in skill_names
        }

        for skill_name, skill_text in skill_texts.items():
            with self.subTest(skill=skill_name):
                metadata = yaml.safe_load(skill_text.split("---", maxsplit=2)[1])
                self.assertEqual(skill_name, metadata["name"])
                self.assertEqual(
                    "documentation-methodology",
                    metadata["metadata"]["category"],
                )
                self.assertTrue(skill_name.startswith("terminology-standard"))

        base_text = skill_texts["terminology-standard"]
        self.assertIn("exact filename terminology.md", base_text)
        self.assertIn("provider-neutral operation is Load Terminology Standards", base_text)
        self.assertIn("mcp-agent-ops reference_load", base_text)
        self.assertIn("names set to a one-item list containing terminology.md", base_text)
        self.assertIn("MCP_AGENT_OPS_REFERENCE_ROOTS", base_text)
        self.assertIn("MCP_AGENT_OPS_REFERENCE_NAMES", base_text)
        self.assertIn("TERMINOLOGY STANDARDS LOADED", base_text)
        self.assertIn("TERMINOLOGY STANDARD SCOPE UNAVAILABLE", base_text)
        self.assertIn("Do not reinterpret UNAVAILABLE as ABSENT", base_text)
        self.assertIn("cannot support TERMINOLOGY REVIEW: PASS", base_text)
        self.assertIn("TERMINOLOGY APPLICATION: PARTIAL", base_text)
        self.assertIn("TERMINOLOGY APPLICATION: BLOCKED", base_text)
        self.assertIn("process-local and immutable", base_text)
        self.assertIn("provider-neutral operation is Refresh Terminology Standards", base_text)
        self.assertIn("mcp-agent-ops reference_refresh with no arguments", base_text)
        self.assertIn("rebuilds every allowlisted reference", base_text)
        self.assertIn("TERMINOLOGY REFERENCE SNAPSHOT REFRESHED", base_text)
        self.assertIn("TERMINOLOGY STANDARD PUBLICATION INCOMPLETE", base_text)
        self.assertIn("catalog_revision to equal the refresh revision", base_text)
        self.assertIn("validated SHA-256 digest of the selected target file", base_text)
        self.assertIn(
            "Load the active configured reference snapshot through Load Terminology Standards",
            base_text,
        )
        self.assertIn("first matching project entry governs", base_text)
        self.assertIn("The Avoid section is optional", base_text)
        self.assertIn("Do not populate Avoid as a speculative synonym list", base_text)

        review_text = skill_texts["terminology-standard-review"]
        self.assertIn("Apply terminology-standard", review_text)
        self.assertIn("even when that term is not yet listed under Avoid", review_text)
        self.assertIn("A review never adds a preferred or avoided term", review_text)
        self.assertIn("TERMINOLOGY REVIEW: BLOCKED", review_text)
        self.assertIn("Bind PASS to the returned catalog revision and source labels", review_text)

        update_text = skill_texts["terminology-standard-update"]
        self.assertIn("project terminology.md by default", update_text)
        self.assertIn("shared user standard only when the user explicitly selects", update_text)
        self.assertIn("Omit Avoid for the initial entry", update_text)
        self.assertIn("retained evidence", update_text)
        self.assertIn("TERMINOLOGY STANDARD UPDATE: BLOCKED", update_text)
        self.assertIn(
            "Refresh Terminology Standards operation once before the initial load",
            update_text,
        )
        self.assertIn("Invoke Refresh Terminology Standards a second time", update_text)
        self.assertIn(
            "Invoke Load Terminology Standards once against the refreshed snapshot",
            update_text,
        )
        self.assertIn("TERMINOLOGY STANDARD UPDATE: PUBLICATION INCOMPLETE", update_text)
        self.assertIn("make no mutation", update_text)
        self.assertIn("caller-supplied authorized target path", update_text)
        self.assertIn("pre-mutation and published revisions", update_text)
        self.assertIn("does not assert coverage of an unlisted physical root", update_text)
        self.assertIn("required physical-scope coverage evidence is absent", update_text)
        self.assertIn("Do not report zero mutation or revert a valid file", update_text)
        self.assertEqual(1, update_text.count("Load Terminology Standards result"))

        for skill_name in skill_names:
            with self.subTest(skill_dependency=skill_name):
                openai_metadata = load_yaml_object(
                    SKILLS_ROOT / skill_name / "agents" / "openai.yaml"
                )
                tool_dependencies = openai_metadata["dependencies"]["tools"]
                self.assertEqual("mcp-agent-ops", tool_dependencies[0]["value"])
                self.assertIn("reference_load", tool_dependencies[0]["description"])

        for skill_name in ("terminology-standard", "terminology-standard-update"):
            with self.subTest(refresh_dependency=skill_name):
                openai_metadata = load_yaml_object(
                    SKILLS_ROOT / skill_name / "agents" / "openai.yaml"
                )
                self.assertIn(
                    "reference_refresh",
                    openai_metadata["dependencies"]["tools"][0]["description"],
                )

        routed_agents = {skill_name: set() for skill_name in skill_names}
        for role_path in sorted(ROLES_ROOT.glob("*/*.role.yaml")):
            role = load_yaml_object(role_path)
            for entry in role["skills"]:
                skill_name = next(iter(entry))
                if skill_name in routed_agents:
                    self.assertIn("condition", entry[skill_name])
                    routed_agents[skill_name].add(role["name"])

        self.assertEqual(
            {
                "dev-coder",
                "dev-documentation-writer",
                "methodology-maintainer",
                "wiki-architect",
                "wiki-ingester",
                "wiki-writer",
            },
            routed_agents["terminology-standard"],
        )
        self.assertEqual(
            {
                "dev-artifact-reviewer",
                "dev-code-reviewer",
                "dev-prompt-reviewer",
                "dev-ux-specialist",
                "methodology-artifact-reviewer",
                "wiki-artifact-reviewer",
                "wiki-topic-verifier",
            },
            routed_agents["terminology-standard-review"],
        )
        self.assertEqual(
            {"dev-documentation-writer", "methodology-maintainer"},
            routed_agents["terminology-standard-update"],
        )

        group_design = (
            REPOSITORY_ROOT / "design" / "agents" / "terminology-standard.md"
        ).read_text(encoding="utf-8")
        for skill_name in skill_names:
            self.assertIn(skill_name, group_design)
        self.assertIn("The exact artifact name is terminology.md", group_design)

        group_registry = (
            REPOSITORY_ROOT / "design" / "object-oriented-skill-group-models.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "| Terminology Standard | terminology-standard; terminology-standard-review; terminology-standard-update | None | 3 |",
            group_registry,
        )
        self.assertIn("complete fifty-five-skill inventory", group_registry)
        self.assertIn("used in nine methodology topics", group_registry)
        agent_design_links = group_registry.split(
            "## 4. Agent-Oriented Designs", maxsplit=1
        )[1].split("## 5. Definition Of Good", maxsplit=1)[0]
        self.assertEqual(9, agent_design_links.count("- ["))

        documentation_router = (
            SKILLS_ROOT / "route-documentation-work" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Terminology Standard artifact:", documentation_router)
        self.assertIn("It has no reusable template", documentation_router)
        self.assertIn("does not apply to terminology.md", documentation_router)
        self.assertIn("base terminology-standard skill owns", documentation_router)
        self.assertIn("terminology-standard-update owns", documentation_router)

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

        self.assertNotIn("organise-project-files", role_skill_names)
        self.assertIn("structured-design", role_skill_names)
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
                self.assertNotIn("organise-project-files", adapter_text)
                self.assertIn("structured-design", adapter_text)
                self.assertNotIn("BEGIN INLINED CORE SKILL", adapter_text)
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
        create_text = (SKILLS_ROOT / "create-work-item-file" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        manage_text = (SKILLS_ROOT / "manage-work-items-file" / "SKILL.md").read_text(
            encoding="utf-8"
        )

        for skill_name, skill_text in (
            ("create-work-item-file", create_text),
            ("manage-work-items-file", manage_text),
        ):
            with self.subTest(skill=skill_name):
                self.assertIn("backlog/user-action-required", skill_text)
                self.assertNotIn("docs/user-action-required", skill_text)
                self.assertIn("user action required", skill_text.lower())
        self.assertIn(
            "Structured claim outcomes and technical claim cleanup or recovery remain agent-owned",
            create_text,
        )

        for required_guidance in (
            "User Action Required",
            "Question for the User",
            "Why User Input Is Required",
            "Do not place an item in backlog/user-action-required merely because",
            "synthetic evaluation boundary",
            "Status: Ready only when dependency resolution proves",
            "without manufacturing a",
            "an agent independently identifies definite work",
            "Route an explicit Future Ideas, ideation, or promotion request",
            "the user has not requested or authorized that new work",
            "After creation, route a user-requested item",
            "the original request did not resolve",
        ):
            with self.subTest(create_guidance=required_guidance):
                self.assertIn(required_guidance, create_text)

        for required_guidance in (
            "Do not own, dispatch, implement, or resolve user-action-required work",
            "Ask one plain-language question",
            "Explain why the user owns the answer",
            "State the practical consequence of each option",
            "State the unattended-work boundary",
            "Move an approved or answered item into its typed active backlog folder",
            "set Status: Ready before any Running transition",
            "intentionally deferred recognized work",
        ):
            with self.subTest(manage_guidance=required_guidance):
                self.assertIn(required_guidance, manage_text)
        self.assertNotIn("set its active status according to project convention", manage_text)

    def test_file_backlog_dependency_lifecycle_is_canonical_before_dispatch(self) -> None:
        """Creation, mutation, and coordination enforce one Ready meaning."""
        create_text = (SKILLS_ROOT / "create-work-item-file" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        manage_text = (SKILLS_ROOT / "manage-work-items-file" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        coordinate_text = (
            SKILLS_ROOT / "coordinate-work-items" / "SKILL.md"
        ).read_text(encoding="utf-8")

        self.assertIn("Before assigning Ready", create_text)
        self.assertIn("Status: Blocked", create_text)
        self.assertIn("observable Blocked -> Ready condition", create_text)
        self.assertIn("hard dependency", create_text)

        self.assertIn(
            "Before any transition that would write Status: Ready",
            manage_text,
        )
        self.assertIn("Status: Blocked", manage_text)
        self.assertIn("observable unblock", manage_text)
        self.assertIn("hard dependency", manage_text)

        self.assertIn("Canonical Status: Ready means", coordinate_text)
        self.assertIn("reject dispatch", coordinate_text)
        self.assertIn("provider reconcile that invalid lifecycle to Blocked", coordinate_text)
        self.assertIn("effective lifecycle beside the provider record", coordinate_text)

    def test_file_work_item_template_and_approval_boundary_are_complete(self) -> None:
        """The real fixture enforces item shape and approval behavior."""
        create_text = (SKILLS_ROOT / "create-work-item-file" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        methodology_text = (
            SKILLS_ROOT / "route-documentation-work" / "SKILL.md"
        ).read_text(encoding="utf-8")
        template_name = "file-work-item-template.md"
        template_path = (
            SKILLS_ROOT
            / "route-documentation-work"
            / "assets"
            / "templates"
            / template_name
        )
        template_text = template_path.read_text(encoding="utf-8")

        self.assertIn(template_name, DOCUMENTATION_TEMPLATE_FILENAMES)
        self.assertIn(template_name, create_text)
        self.assertIn(template_name, methodology_text)

        ordered_markers = (
            "Status: TODO Ready, Blocked, User Action Required, or Holding",
            "Type: TODO Defect, Feature, Analysis, Investigation, or Holding",
            "Provider: file",
            "Work Item ID: TODO immutable filename stem without .md",
            "Completion: TODO main-branch, feature-branch, or UNSET",
            "## Summary",
            "## Context",
            "## Source Evidence",
            "## Requirements",
            "## Acceptance Criteria",
            "## Dependencies",
            "## Verification",
            "## Open Questions",
            "## Notes",
        )
        positions = [template_text.index(marker) for marker in ordered_markers]
        self.assertEqual(sorted(positions), positions)
        for optional_comment in (
            "<!-- OPTIONAL: Series child metadata",
            "<!-- OPTIONAL: User Action Required",
            "<!-- OPTIONAL: Governed Definition Approval",
            "<!-- OPTIONAL: Notes",
        ):
            self.assertIn(optional_comment, template_text)
        self.assertLess(
            template_text.index("### Governed Canonical Sources"),
            template_text.index("### Question for the User"),
        )
        self.assertLess(
            template_text.index("### Allowed Dependent Artifacts"),
            template_text.index("### Question for the User"),
        )
        self.assertNotIn("Open Decisions", template_text)
        self.assertNotIn("Design Principles", template_text)

        for required_contract in (
            "Ready items",
            "User Action Required items",
            "Holding items",
            "series children",
            "See the conversation above",
            "May I continue designing?",
            "invalid User Action Required classification",
            "exact canonical-path manifest",
            "exact user-message provenance",
            "They are approval evidence, not design rules.",
            "Keep change-control manifests out of Design Principles",
        ):
            with self.subTest(required_contract=required_contract):
                self.assertIn(required_contract, create_text)

        case_id = "file-work-item-template-contract"
        probe_id = "probe-create-work-item-file"
        cases = load_yaml_object(REPOSITORY_ROOT / "evals" / "cases.yaml")
        probes = load_yaml_object(REPOSITORY_ROOT / "evals" / "skill-probes.yaml")
        scenarios = load_yaml_object(REPOSITORY_ROOT / "evals" / "agent-scenarios.yaml")
        workflows = load_yaml_object(REPOSITORY_ROOT / "evals" / "workflow-packs.yaml")
        case = next(entry for entry in cases["cases"] if entry["id"] == case_id)
        probe = next(entry for entry in probes["probes"] if entry["id"] == probe_id)
        steward = next(
            entry for entry in scenarios["agents"] if entry["id"] == "dev-backlog-steward"
        )
        happy_scenario = next(
            entry
            for entry in steward["scenarios"]
            if entry["id"] == "dev-backlog-steward-happy"
        )
        backlog_workflow = next(
            entry for entry in workflows["packs"] if entry["id"] == "backlog"
        )
        backlog_fixture = next(
            entry
            for entry in scenarios["fixtureProfiles"]
            if entry["id"] == "backlog-state-machine"
        )

        self.assertEqual("fixture-backed", probe["coverageStatus"])
        self.assertEqual([case_id], probe["executableCases"])
        self.assertEqual({probe_id}, set(case["fixtureBackedProbeClaims"]))
        self.assertIn(probe_id, case["skillProbes"])
        self.assertIn(case_id, happy_scenario["executableCases"])
        self.assertIn(case_id, backlog_workflow["executableCases"])
        self.assertIn(case_id, backlog_fixture["executableCases"])
        self.assertEqual("artifact-contract", probe["evaluationKind"])
        self.assertEqual("artifact-contract", case["judgePlan"]["modelRubric"])

        fixture_root = REPOSITORY_ROOT / case["project"]
        for fixture_name in (
            "TASK.md",
            "requests.md",
            "verify.py",
            "checker-approval.yaml",
        ):
            self.assertTrue((fixture_root / fixture_name).is_file())
        verifier = subprocess.run(
            [sys.executable, str(fixture_root / "verify.py"), "--self-test"],
            cwd=fixture_root,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, verifier.returncode, verifier.stdout + verifier.stderr)

        requests_text = (fixture_root / "requests.md").read_text(encoding="utf-8")
        for governed_source in (
            "skills/create-work-item-file/SKILL.md",
            "agents/roles/dev-activities/dev-coder.role.yaml",
            "agents/role-schema.yaml",
            "agents/model-profiles.yaml",
            "adapters/codex/model-profiles.yaml",
            "skills/create-work-item-file/agents/openai.yaml",
            "adapters/codex/skills/codex-harness-directives/SKILL.md",
            "adapters/codex/skills/codex-harness-directives/agents/openai.yaml",
        ):
            with self.subTest(governed_source=governed_source):
                self.assertIn(governed_source, requests_text)
        self.assertIn("cannot create or widen approval", requests_text)
        self.assertIn("checker-approval.yaml", requests_text)

    def test_file_work_item_skills_own_behavior_after_legacy_retirement(self) -> None:
        primary_root = resolve_primary_repository_root()
        canonical_contracts = {
            "create-work-item-file": (
                "Only the primary worktree on main may create canonical files under backlog.",
                "Do not create another queue elsewhere.",
                "Before writing, search every active typed folder",
                "Source Evidence",
                "applicable coordination evidence",
            ),
            "manage-work-items-file": (
                "Only the primary worktree on main may change canonical files under backlog.",
                "must not create, transition, or archive an item",
                "Each startup or terminal transition remains its own short primary-main provider transaction.",
                "AWAITING_REVIEW",
                "same delivery identity remains lifecycle AWAITING_REVIEW",
                "Do not change lifecycle back to RUNNING for same-delivery corrections.",
                "Only a later Commit READY permits the distinct terminal COMPLETED update.",
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
                if skill_name == "create-work-item-file":
                    self.assertIn("atomic no-overwrite creation", frontmatter["description"])
                else:
                    self.assertNotIn("claim", frontmatter["description"])
                for required_contract in required_contracts:
                    self.assertIn(required_contract, skill_text)

        readme_text = README_PATH.read_text(encoding="utf-8")
        self.assertIn(
            "creation provider delegates its exact commit to commit-file-provider-transaction",
            readme_text,
        )
        self.assertNotIn("needs no claim", readme_text)

        for retired_name in (
            "create-backlog",
            "manage-backlog",
            "file-based-backlog",
        ):
            with self.subTest(retired=retired_name):
                self.assertFalse((SKILLS_ROOT / retired_name).exists())

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

    def test_answered_user_action_enters_ready_before_running(self) -> None:
        manage_text = (SKILLS_ROOT / "manage-work-items-file" / "SKILL.md").read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "set Status: Ready before any Running transition",
            manage_text,
        )
        self.assertNotIn(
            "set its active status according to project convention",
            manage_text,
        )

    def test_manage_file_work_items_archives_terminal_series(self) -> None:
        """The file provider defines recoverable terminal-series archival."""
        manage_text = (SKILLS_ROOT / "manage-work-items-file" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        normalized = " ".join(manage_text.split()).lower()

        for required_contract in (
            "preserve the stable series slug and index.md filename",
            "backlog/completed-backlog/type/series-slug/index.md",
            "backlog/failed-backlog/type/series-slug/index.md",
            "do not add an independent status field to the series index",
            "two serialized provider transactions",
            "every explicit child series reference",
            "without changing any child's terminal status, outcome, or evidence",
            "claim the exact active index path, archive destination, and every child",
            "mixed nonterminal child-state inventory",
            "retry the series transaction from the preserved terminal child evidence",
        ):
            with self.subTest(required_contract=required_contract):
                self.assertIn(required_contract, normalized)

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

    def test_skill_html_hides_complete_comments_only_outside_code_fences(self) -> None:
        """Hide source comments from browser HTML without changing fenced examples or raw tags."""

        build_skill_docs = load_build_skill_docs_module()
        rendered = build_skill_docs.render_markdown(
            """Visible before.

<!--
hidden provenance
-->

<section>raw HTML remains ordinary escaped text</section>

```markdown
<!-- fenced comment example -->
```

Visible after.
""",
            SKILLS_ROOT / "document-provenance",
        )
        document_provenance_html = build_skill_docs.build_payload()["skills"][
            "document-provenance"
        ]["html"]
        incomplete_comment = build_skill_docs.render_markdown(
            "<!-- incomplete comment",
            SKILLS_ROOT / "document-provenance",
        )

        self.assertIn("Visible before.", rendered)
        self.assertIn("Visible after.", rendered)
        self.assertNotIn("hidden provenance", rendered)
        self.assertIn(
            "&lt;section&gt;raw HTML remains ordinary escaped text&lt;/section&gt;",
            rendered,
        )
        self.assertIn("&lt;!-- fenced comment example --&gt;", rendered)
        self.assertIn("&lt;!-- incomplete comment", incomplete_comment)
        self.assertNotIn(
            "Artifact-ID: f633e99c-ffc4-4bc9-9c11-75e8dc070914",
            document_provenance_html,
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
        self.assertEqual(8, role_schema["version"])
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
        shared_role_skills = [
            next(iter(entry))
            for entry in role_schema["fixedBehavior"]["sharedSkills"]
        ]
        self.assertEqual(
            ["effective-communication", "ste-technical-writing"],
            shared_role_skills,
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
        self.assertEqual(5, generation_manifest["version"])
        self.assertEqual(
            {"coreSkillDelivery": "by-reference", "inlineCoreSkills": False},
            generation_manifest["generationOptions"],
        )
        self.assertEqual(len(roles), generation_manifest["canonicalRoleCount"])
        roles_by_name = {role.name: role for role in roles}
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
                    self.assertEqual(
                        list(build_skill_docs._referenced_fixed_role_skills(
                            roles_by_name[agent["name"]],
                            adapter_name,
                            False,
                        )),
                        agent["referencedFixedSkills"],
                    )

        skill_names = set(skill_payload["skills"])
        role_payload = build_skill_docs.build_role_payload(roles)
        for role in roles:
            with self.subTest(role=role.name):
                self.assertTrue(set(role.skills).issubset(skill_names))
                role_source = yaml.safe_load(role.yaml)
                self.assertNotIn("skillComments", role_source)
                self.assertNotIn("outputComments", role_source)
                declared_role_skills = [
                    next(iter(entry)) for entry in role_source["skills"]
                ]
                self.assertTrue(set(shared_role_skills).isdisjoint(declared_role_skills))
                self.assertEqual(
                    list(role.skills),
                    shared_role_skills + declared_role_skills,
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
                        set(next(iter(entry.values())))
                        in ({"purpose"}, {"purpose", "schema"})
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
                self.assertEqual(
                    role.output_schema,
                    role_payload["roles"][role.name]["outputSchema"],
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
                        role.skill_conditions["verify-documentation-page"],
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
                        inline_core_skills=False,
                        model_profiles=build_skill_docs.load_adapter_model_profiles(
                            "codex",
                            set(build_skill_docs.load_model_profiles()),
                        ),
                    ),
                    tomllib.loads(codex_agent_text)["developer_instructions"],
                )
                self.assertIn(
                    "Before acting, load these definition-owned skills completely; they govern the work:",
                    codex_agent_text,
                )
                for skill in build_skill_docs.fixed_role_skills(role):
                    self.assertNotIn(f"BEGIN INLINED CORE SKILL: {skill}", codex_agent_text)
                codex_payload = tomllib.loads(codex_agent_text)
                configured_skills = codex_payload.get("skills", {}).get("config", [])
                if role.repository_mutation == "never":
                    self.assertNotIn(CODEX_HARNESS_SKILL_NAME, codex_agent_text)
                    self.assertNotIn(
                        CODEX_HARNESS_SKILL_NAME,
                        [item.get("name") for item in configured_skills],
                    )
                else:
                    self.assertNotIn(f"BEGIN INLINED CORE SKILL: {CODEX_HARNESS_SKILL_NAME}", codex_agent_text)
                    self.assertIn(CODEX_HARNESS_SKILL_NAME, [item.get("name") for item in configured_skills])
                fixed_skills = list(build_skill_docs.fixed_role_skills(role))
                if fixed_skills:
                    self.assertIn(
                        "Before acting, load these definition-owned skills completely; they govern the work: "
                        + ", ".join(fixed_skills)
                        + ".",
                        codex_agent_text,
                    )
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
                self.assertEqual(list(build_skill_docs.fixed_role_skills(role)), claude_frontmatter["skills"])
                self.assertIn("These definition-owned skills are preloaded and govern the work", claude_agent_text)
                for skill in build_skill_docs.fixed_role_skills(role):
                    self.assertNotIn(f"BEGIN INLINED CORE SKILL: {skill}", claude_agent_text)
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
                self.assertIn("Before acting, load these definition-owned skills completely", gemini_agent_text)
                for skill in build_skill_docs.fixed_role_skills(role):
                    self.assertNotIn(f"BEGIN INLINED CORE SKILL: {skill}", gemini_agent_text)
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
                self.assertEqual(list(build_skill_docs.fixed_role_skills(role)), junie_frontmatter["skills"])
                self.assertIn("reasoningLevel", junie_frontmatter)
                self.assertIn("These definition-owned skills are preloaded and govern the work", junie_agent_text)
                for skill in build_skill_docs.fixed_role_skills(role):
                    self.assertNotIn(f"BEGIN INLINED CORE SKILL: {skill}", junie_agent_text)
                for skill, condition in role.skill_conditions.items():
                    self.assertIn(f"Use the {skill} skill {condition}.", junie_agent_text)

        non_setup_roles = [
            role for role in roles
            if role.name != "project-configurator"
        ]
        self.assertTrue(all("detect-technology-skills" not in role.skills for role in non_setup_roles))
        setup_role = next(role for role in roles if role.name == "project-configurator")
        self.assertIn("detect-technology-skills", setup_role.skills)

    def test_native_rendering_helpers_reference_core_skills_by_default_and_can_inline(self) -> None:
        build_skill_docs = load_build_skill_docs_module()
        skill_payload = build_skill_docs.build_payload()
        role = next(
            role
            for role in build_skill_docs.load_role_definitions(set(skill_payload["skills"]))
            if role.name == "dev-coder"
        )
        profile_ids = set(build_skill_docs.load_model_profiles())

        claude_profiles = build_skill_docs.load_adapter_model_profiles("claude", profile_ids)
        referenced = build_skill_docs.render_claude_agent(role, claude_profiles)
        referenced_frontmatter = yaml.safe_load(referenced.split("---", 2)[1])
        self.assertEqual(
            list(build_skill_docs.fixed_role_skills(role)),
            referenced_frontmatter["skills"],
        )
        self.assertNotIn("BEGIN INLINED CORE SKILL", referenced)
        self.assertIn(
            "These definition-owned skills are preloaded and govern the work",
            referenced,
        )
        inlined = build_skill_docs.render_claude_agent(
            role,
            claude_profiles,
            inline_core_skills=True,
        )
        self.assertNotIn("skills", yaml.safe_load(inlined.split("---", 2)[1]))
        for skill in build_skill_docs.fixed_role_skills(role):
            self.assertIn(f"BEGIN INLINED CORE SKILL: {skill}", inlined)

        codex_profiles = build_skill_docs.load_adapter_model_profiles("codex", profile_ids)
        codex_referenced = tomllib.loads(
            build_skill_docs.render_codex_agent(role, codex_profiles)
        )
        self.assertIn(
            {"name": CODEX_HARNESS_SKILL_NAME, "enabled": True},
            codex_referenced["skills"]["config"],
        )
        self.assertNotIn(
            "BEGIN INLINED CORE SKILL",
            codex_referenced["developer_instructions"],
        )
        codex_inlined = tomllib.loads(
            build_skill_docs.render_codex_agent(
                role,
                codex_profiles,
                inline_core_skills=True,
            )
        )
        self.assertIn(
            f"BEGIN INLINED CORE SKILL: {CODEX_HARNESS_SKILL_NAME}",
            codex_inlined["developer_instructions"],
        )

        gemini_profiles = build_skill_docs.load_adapter_model_profiles("gemini", profile_ids)
        gemini_referenced = build_skill_docs.render_gemini_agent(role, gemini_profiles)
        self.assertIn(
            "Before acting, load these definition-owned skills completely",
            gemini_referenced,
        )
        self.assertNotIn("BEGIN INLINED CORE SKILL", gemini_referenced)
        gemini_inlined = build_skill_docs.render_gemini_agent(
            role,
            gemini_profiles,
            inline_core_skills=True,
        )
        self.assertIn("BEGIN INLINED CORE SKILL", gemini_inlined)

        junie_profiles = build_skill_docs.load_adapter_model_profiles("junie", profile_ids)
        junie_referenced = build_skill_docs.render_junie_agent(role, junie_profiles)
        self.assertEqual(
            list(build_skill_docs.fixed_role_skills(role)),
            yaml.safe_load(junie_referenced.split("---", 2)[1])["skills"],
        )
        self.assertNotIn("BEGIN INLINED CORE SKILL", junie_referenced)
        junie_inlined = build_skill_docs.render_junie_agent(
            role,
            junie_profiles,
            inline_core_skills=True,
        )
        self.assertNotIn("skills", yaml.safe_load(junie_inlined.split("---", 2)[1]))
        self.assertIn("BEGIN INLINED CORE SKILL", junie_inlined)

        self.assertNotIn("BEGIN INLINED CORE SKILL", build_skill_docs.role_instruction_text(
            role,
            adapter_name="codex",
        ))
        self.assertNotIn("BEGIN INLINED CORE SKILL", build_skill_docs.codex_role_instruction_text(role))
        self.assertIn(
            {"name": CODEX_HARNESS_SKILL_NAME, "enabled": True},
            build_skill_docs.codex_skill_availability(role),
        )

    def test_adapter_generator_cli_defaults_to_referenced_core_skills(self) -> None:
        current = subprocess.run(
            [sys.executable, str(BUILD_SKILL_DOCS_PATH), "--check"],
            cwd=REPOSITORY_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, current.returncode, current.stdout + current.stderr)

        inline = subprocess.run(
            [
                sys.executable,
                str(BUILD_SKILL_DOCS_PATH),
                "--check",
                "--inline-core-skills",
                "true",
            ],
            cwd=REPOSITORY_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(1, inline.returncode)
        self.assertIn("stale", inline.stdout)

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

    def test_resource_claim_is_the_single_source_for_claim_rules(self) -> None:
        claim_text = (SKILLS_ROOT / "resource-claim" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        readme_text = README_PATH.read_text(encoding="utf-8")
        lifecycle_text = (
            REPOSITORY_ROOT / "design" / "orchestrated-development-lifecycle.html"
        ).read_text(encoding="utf-8")

        for required_contract in (
            "Acquire a claim only for an event in this table.",
            "Acquire it immediately before starting that event.",
            "| No. | Event | Claim | Release |",
            "| 1 | Edit or move an existing backlog item in the primary worktree | Each current backlog path and each destination path.",
            "| 2 | Perform any non-backlog work in the primary worktree | project-files: every path in the primary worktree except backlog.",
            "browser-test:&lt;id&gt;",
            "database:&lt;id&gt;",
            "port:&lt;number&gt;",
            "live-model:&lt;provider&gt;:&lt;suite&gt;",
            "shared-install:&lt;target&gt;",
            "deployment:&lt;environment&gt;",
            "After the backlog mutation event ends or ownership is handed off.",
            "After the claimed deployment or rollback reaches a verified final state.",
            "Apply the exclusive OS lock directly to agent-claims.json.",
            "Release is claim cleanup only.",
            "Release does not inspect or gate on worktree cleanliness",
            "The claim system tracks declared ownership and scope overlap only.",
            "status, and release do not inspect or gate on staged, unstaged, untracked, renamed, or deleted",
            "Git owns dirty-worktree protection",
            "Claim scope is the file, set of files, or shared resource that a claim protects.",
            "Every claim request must specify a scope.",
            "An overlapping request returns CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED",
            "Treat every live claim as valid.",
            "A configured watchdog decides whether a live claim is stale.",
        ):
            with self.subTest(claim_contract=required_contract):
                self.assertIn(required_contract, claim_text)

        for duplicated_contract in (
            "needs no claim",
            "claim-free",
            "Interrupted private-worktree changes",
            "Before finish, release, or handoff",
        ):
            with self.subTest(duplicated_contract=duplicated_contract):
                self.assertNotIn(duplicated_contract, claim_text)

        for required_contract in (
            "Resource Claim](skills/resource-claim/SKILL.md) is the only source",
            "events that require claims",
            "the scope for each event",
            "release timing",
            "Skills that apply claims refer to that table instead of copying its rules.",
        ):
            with self.subTest(readme_contract=required_contract):
                self.assertIn(required_contract, readme_text)

        for required_contract in (
            "Resource Claim skill defines every event that requires a claim",
            "Resource Claim</a> is the only source for claim events, scopes, conflicts, deadlines, recovery, and release timing.",
            "command-line provider</a> and",
            "MCP provider</a> describe only how to invoke that contract.",
        ):
            with self.subTest(lifecycle_contract=required_contract):
                self.assertIn(required_contract, lifecycle_text)
        self.assertNotIn("Complete Event-To-Claim Contract", lifecycle_text)
        self.assertNotIn("<tr><td>1</td><td>Update an existing work item</td>", lifecycle_text)
        self.assertNotIn("needs no claim", lifecycle_text)
        self.assertNotIn("claim-free", lifecycle_text)

    def test_resource_coordination_skills_expose_aligned_operations(self) -> None:
        """Separate policy, interface, and provider operations without overstating MCP support."""
        claim_text = (SKILLS_ROOT / "resource-claim" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        interface_text = (SKILLS_ROOT / "resource-claim-helper" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        command_text = (
            SKILLS_ROOT / "resource-claim-helper-command" / "SKILL.md"
        ).read_text(encoding="utf-8")
        mcp_text = (SKILLS_ROOT / "resource-claim-helper-mcp" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        probes = load_yaml_object(REPOSITORY_ROOT / "evals" / "skill-probes.yaml")
        probes_by_skill = {probe["skill"]: probe for probe in probes["probes"]}

        policy_operations = (
            "Coordinate Shared Resource",
            "Acquire Claim",
            "Extend Claim",
            "Extend Claim Deadline",
            "Heartbeat Claim",
            "Read Claim Status",
            "Release Claim",
        )
        helper_operations = (
            "Read Claim Status",
            "Acquire Claim",
            "Extend Claim",
            "Extend Claim Deadline",
            "Heartbeat Claim",
            "Release Claim",
            "Reset Claim Registry",
            "Maintain Claim Journal",
            "Report Claim Contention",
        )
        for operation in policy_operations:
            with self.subTest(skill="resource-claim", operation=operation):
                self.assertIn(f"## {operation}", claim_text)
        for skill, text in (
            ("resource-claim-helper-command", command_text),
            ("resource-claim-helper-mcp", mcp_text),
        ):
            for operation in helper_operations:
                with self.subTest(skill=skill, operation=operation):
                    self.assertIn(f"## {operation}", text)
                    self.assertIn(operation, interface_text)

        dispatching_and_delivery = (
            REPOSITORY_ROOT
            / "design"
            / "agents"
            / "work-item-dispatching-and-delivery.md"
        ).read_text(encoding="utf-8")
        expected_members = {
            "resource-claim-helper": (
                "Operation Contract",
                *helper_operations,
                "Structured Outcomes",
                "Reconcile an Uncertain Outcome",
                "Provider Realization Contract",
            ),
            "resource-claim-helper-command": helper_operations,
            "resource-claim-helper-mcp": ("Current Availability", *helper_operations),
        }
        for skill, expected in expected_members.items():
            with self.subTest(skill_group_member=skill):
                row = next(
                    line
                    for line in dispatching_and_delivery.splitlines()
                    if line.startswith(f"| Resource Coordination | {skill} |")
                )
                actual = tuple(
                    member.strip()
                    for member in row.strip("|").split("|")[2].split(";")
                )
                self.assertEqual(expected, actual)

        expected_class_operations = (
            "+read-claim-status()",
            "+acquire-claim(scope)",
            "+extend-claim(scope)",
            "+extend-claim-deadline(claimId)",
            "+heartbeat-claim(claimId)",
            "+release-claim(claimId)",
            "+reset-claim-registry()",
            "+maintain-claim-journal()",
            "+report-claim-contention()",
        )
        class_markers = {
            "resource-claim-helper": 'class ClaimHelper["resource-claim-helper"] {',
            "resource-claim-helper-command": "class resource-claim-helper-command {",
            "resource-claim-helper-mcp": "class resource-claim-helper-mcp {",
        }
        for skill, marker in class_markers.items():
            with self.subTest(skill_group_class=skill):
                start = dispatching_and_delivery.index(marker)
                end = dispatching_and_delivery.index("\n    }", start)
                class_body = dispatching_and_delivery[start:end]
                actual = tuple(
                    line.strip()
                    for line in class_body.splitlines()
                    if line.strip().startswith("+")
                )
                self.assertEqual(expected_class_operations, actual)

        self.assertIn("## Claim Events", claim_text)
        self.assertIn("Apply resource-claim for policy and resource-claim-helper", command_text)
        self.assertIn("Apply resource-claim for policy and resource-claim-helper", mcp_text)
        self.assertIn("## Operation Contract", interface_text)
        self.assertIn("## Structured Outcomes", interface_text)
        self.assertIn("## Reconcile an Uncertain Outcome", interface_text)
        self.assertIn("Read `outcome`", command_text)
        self.assertIn("Read result.outcome", mcp_text)
        self.assertIn("same script", command_text)
        self.assertIn("same server", mcp_text)
        self.assertIn("## Current Availability", mcp_text)
        self.assertIn("Do not configure the current mcp-agent-ops provider", mcp_text)

        expected_probe_terms = {
            "resource-claim": (
                "status",
                "acquire",
                "scope extension",
                "deadline extension",
                "heartbeat",
                "release",
                "uncertain",
            ),
            "resource-claim-helper": (
                "repository",
                "scope",
                "deadline",
                "release",
                "journal",
                "report",
                "structured outcomes",
                "uncertain",
            ),
            "resource-claim-helper-command": (
                "status",
                "acquire",
                "scope extension",
                "deadline extension",
                "heartbeat",
                "release",
                "journal maintenance",
                "contention reporting",
                "uncertain",
            ),
            "resource-claim-helper-mcp": (
                "status",
                "acquire",
                "scope extension",
                "deadline extension",
                "heartbeat",
                "release",
                "journal maintenance",
                "contention reporting",
                "uncertain",
                "unavailable",
            ),
        }
        for skill, required_terms in expected_probe_terms.items():
            behavior = probes_by_skill[skill]["expectedBehavior"].casefold()
            for term in required_terms:
                with self.subTest(skill=skill, probe_term=term):
                    self.assertIn(term, behavior)

    def test_coordinator_and_providers_require_exact_work_item_lifecycle_claims(self) -> None:
        coordination_text = (
            SKILLS_ROOT / "coordinate-work-items" / "SKILL.md"
        ).read_text(encoding="utf-8")
        provider_texts = {
            skill_name: (SKILLS_ROOT / skill_name / "SKILL.md").read_text(
                encoding="utf-8"
            )
            for skill_name in (
                "manage-work-items-file",
                "manage-work-items-github",
                "manage-work-items-gitlab",
                "manage-work-items-azure-devops",
                "manage-work-items-jira",
            )
        }
        required_contracts = (
            "Acquire the exact opaque Work Item ID before any work or provider mutation.",
            "Use activity work for outcome work and activity update for provider mutation.",
            "Release the work-item claim with disposition done, blocked, or handoff at the activity boundary.",
            "Blocked may include a bounded blocker reference; when present, it must be canonical, non-empty, single-line, and at most 200 characters.",
            "Path and resource claims remain independently applicable.",
            "The provider remains the lifecycle authority.",
        )
        for source_name, text in provider_texts.items():
            for required_contract in required_contracts:
                with self.subTest(
                    source=source_name,
                    required_contract=required_contract,
                ):
                    self.assertIn(required_contract, text)

        for required_contract in (
            "When resource-claim is loaded, use its Claim Events table and supporting rules.",
            "Acquire the exact opaque Work Item ID only when an applicable Claim Event requires it.",
            "Use activity work for outcome work and activity update for provider mutation.",
            "Release the work-item claim with disposition done, blocked, or handoff at the activity boundary.",
            "Path and resource claims remain independently applicable.",
            "The provider remains the lifecycle authority.",
        ):
            with self.subTest(source="coordinate-work-items", required_contract=required_contract):
                self.assertIn(required_contract, coordination_text)

    def test_roles_keep_mutation_independent_from_resource_coordination(self) -> None:
        build_skill_docs = load_build_skill_docs_module()
        skill_payload = build_skill_docs.build_payload()
        roles = build_skill_docs.load_role_definitions(set(skill_payload["skills"]))
        for role in roles:
            with self.subTest(role=role.name, mutation_policy=role.repository_mutation):
                self.assertNotIn("resource-claim", build_skill_docs.fixed_role_skills(role))
                self.assertNotIn("resource-claim", role.skill_conditions)

        claim_skill = (SKILLS_ROOT / "resource-claim" / "SKILL.md").read_text(encoding="utf-8")
        helper_skill = (SKILLS_ROOT / "resource-claim-helper" / "SKILL.md").read_text(encoding="utf-8")
        mcp_skill = (SKILLS_ROOT / "resource-claim-helper-mcp" / "SKILL.md").read_text(encoding="utf-8")
        command_skill = (SKILLS_ROOT / "resource-claim-helper-command" / "SKILL.md").read_text(encoding="utf-8")
        merge_skill = (SKILLS_ROOT / "integrate-agent-work" / "SKILL.md").read_text(encoding="utf-8")
        claim_script = SKILLS_ROOT / "resource-claim-helper-command" / "scripts" / "claim.py"
        self.assertTrue(claim_script.is_file())
        self.assertFalse((SKILLS_ROOT / "resource-claim" / "scripts" / "claim.py").exists())
        self.assertNotIn("CLAIM_SCRIPT", claim_skill)
        self.assertIn("## Claim Events", claim_skill)
        for tool_name in (
            "claim_status",
            "claim_acquire",
            "claim_extend",
            "claim_heartbeat",
            "claim_release",
            "claim_reset",
            "claim_maintain_journal",
            "claim_report",
        ):
            self.assertIn(tool_name, mcp_skill)
            self.assertNotIn(tool_name, claim_skill)
        self.assertIn(
            'CLAIM_SCRIPT="${HOME}/.agents/skills/resource-claim-helper-command/scripts/claim.py"',
            command_skill,
        )
        self.assertIn("skills/resource-claim-helper-command/scripts/claim.py", command_skill)
        self.assertNotIn("resource-claim-helper-command", mcp_skill)
        self.assertNotIn("resource-claim-helper-mcp", command_skill)
        self.assertNotIn("ISOLATED_CHECKOUT_SETUP_REQUIRED", command_skill)
        self.assertNotIn("DIRTY_CHECKOUT_RECOVERY_AUTHORIZATION_REQUIRED", command_skill)
        self.assertNotIn("--no-change", command_skill)
        self.assertNotIn("no_change", mcp_skill)
        self.assertIn("## Operation Contract", helper_skill)
        self.assertIn("## Structured Outcomes", helper_skill)
        self.assertIn("exclusive OS lock directly to agent-claims.json", claim_skill)
        self.assertIn("maintain-journal --hot-days 2", command_skill)
        self.assertIn("report --since 2d", command_skill)
        self.assertNotIn("git:commit", claim_skill)
        self.assertNotIn("merge:integration:main", claim_skill)
        self.assertNotIn("merge:integration:main", merge_skill)
        readme_text = README_PATH.read_text(encoding="utf-8")
        self.assertIn("Resource Claims And Worktrees", readme_text)
        self.assertIn("Resource Claim](skills/resource-claim/SKILL.md) is the only source", readme_text)
        self.assertNotIn("needs no claim", readme_text)
        self.assertNotIn("claim-free", readme_text)
        self.assertNotIn("Resource Claims And Worktrees", AGENTS_PATH.read_text(encoding="utf-8"))
        self.assertIn("/.worktrees/", GITIGNORE_PATH.read_text(encoding="utf-8").splitlines())

    def test_event_driven_claim_and_current_main_reconciliation_contracts(self) -> None:
        """Protect event ownership and ancestry-bounded integration guidance."""
        claim_text = (SKILLS_ROOT / "resource-claim" / "SKILL.md").read_text(encoding="utf-8")
        command_text = (
            SKILLS_ROOT / "resource-claim-helper-command" / "SKILL.md"
        ).read_text(encoding="utf-8")
        mcp_text = (SKILLS_ROOT / "resource-claim-helper-mcp" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        merge_text = (SKILLS_ROOT / "integrate-agent-work" / "SKILL.md").read_text(encoding="utf-8")
        coordination_text = (
            SKILLS_ROOT / "coordinate-work-items" / "SKILL.md"
        ).read_text(encoding="utf-8")
        design_text = (
            REPOSITORY_ROOT / "design" / "orchestrated-development-lifecycle.html"
        ).read_text(encoding="utf-8")
        probe_text = (
            REPOSITORY_ROOT / "evals" / "skill-probes.yaml"
        ).read_text(encoding="utf-8")
        renderer_text = (
            REPOSITORY_ROOT / "scripts" / "render-agents-technology-skills.py"
        ).read_text(encoding="utf-8")

        event_contract = claim_text.split("## Claim Events", 1)[1].split(
            "## Shared Claim Records", 1
        )[0]
        self.assertIn(
            "Acquire a claim only for an event in this table.",
            event_contract,
        )
        event_rows = [
            line
            for line in event_contract.splitlines()
            if re.match(r"^\| [1-9] \|", line)
        ]
        self.assertEqual(9, len(event_rows))
        self.assertEqual(
            [f"| {number} |" for number in range(1, 10)],
            ["|".join(row.split("|")[:2]) + "|" for row in event_rows],
        )
        for provider_text in (command_text, mcp_text):
            self.assertIn("Apply resource-claim for policy and resource-claim-helper", provider_text)
            self.assertNotIn("needs no claim", provider_text)
            self.assertNotIn("claim-free", provider_text)
            self.assertNotIn("ISOLATED_CHECKOUT_SETUP_REQUIRED", provider_text)
            self.assertNotIn("DIRTY_CHECKOUT_RECOVERY_AUTHORIZATION_REQUIRED", provider_text)

        for required_contract in (
            "Claims prevent two agents from changing the same shared file or resource at the same time.",
            "A claim and its release do not prove that work is complete.",
            "The claim system tracks declared ownership and scope overlap only.",
            "status, and release do not inspect or gate on staged, unstaged, untracked, renamed, or deleted",
            "Git owns dirty-worktree protection",
            "Every claim request must specify a scope.",
            "An overlapping request returns CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED",
            "Ask its owner for a release or recovery notification.",
            "Treat every live claim as valid.",
            "A configured watchdog decides whether a live claim is stale.",
            "A heartbeat does not extend a deadline.",
            "Release is claim cleanup only.",
            "Keep completion, delivery, provider lifecycle, and claim cleanup as separate operations.",
        ):
            with self.subTest(claim_contract=required_contract):
                self.assertIn(required_contract, claim_text)

        for required_contract in (
            "fresh branch based on current main",
            "applying only the accepted file content or explicitly selected commits",
            "Do not merge unrelated branch history merely to preserve it.",
            "Record the source commit IDs and accepted files",
            "Use a full-history merge only when that complete ancestry is intentional",
            "Run the smallest post-integration tests that prove the merged behavior.",
        ):
            with self.subTest(merge_contract=required_contract):
                self.assertIn(required_contract, merge_text)

        for required_contract in (
            "When resource-claim is loaded, use its Claim Events table and supporting rules.",
            "Structured claim outcomes and technical claim cleanup or recovery remain agent-owned",
            "designate this fresh branch as the Work-item integration and cleanup branch",
            "Do not import cumulative branch ancestry merely to preserve provenance",
            "Apply or resume the effective Commit-selected skill only after candidate review and source verification accept the direct or combined commit",
            "Preserve AWAITING_REVIEW with the same delivery identity",
            "Only after the effective Commit-selected skill returns READY",
            "Keep claim release, Commit delivery, and Persistence closure as distinct operations.",
            "a claim owner sends a release or recovery notification",
            "the Watchdog reports an actionable condition",
            "fresh Work-item integration branch is fully merged",
            "prior candidate branch used only as a non-ancestral content source is not the Work-item cleanup branch",
            "GitHub and GitLab closure use their own provider identities",
            "Provider none records terminal evidence only in the task result",
        ):
            with self.subTest(coordination_contract=required_contract):
                self.assertIn(required_contract, coordination_text)

        self.assertNotIn("Retry at five", coordination_text)
        self.assertNotIn(
            "one initial attempt plus no more than six retries",
            coordination_text,
        )
        self.assertIn("Resource Claim</a> is the only source for claim events", design_text)
        for active_term in (
            "MCP helper",
            "configured script",
            "same script",
            "probe-resource-claim-helper",
        ):
            self.assertIn(active_term, probe_text)
        self.assertIn("claim helper Provider Skill is embedded only", renderer_text)

        for required_contract in (
            "fresh reconciliation branch from that exact commit",
            "do not import unrelated ancestry merely to preserve history",
            "this becomes the work-item Thread's integration and cleanup branch",
            "older candidate branch retained only as a non-ancestral content source is handled separately",
            "Before handoff, commit completed work and prove the applicable worktree clean.",
        ):
            with self.subTest(design_contract=required_contract):
                self.assertIn(required_contract, design_text)

        for prohibited_contract in (
            "Administrative Reset Of Inactive Entries",
            "Administrative Cleanup",
            "Dirty unclaimed state",
            "anonymous dirty state",
        ):
            with self.subTest(prohibited_contract=prohibited_contract):
                self.assertNotIn(prohibited_contract, claim_text)
                self.assertNotIn(prohibited_contract, coordination_text)
                for source_root in (SKILLS_ROOT, REPOSITORY_ROOT / "agents" / "roles"):
                    for source_path in source_root.rglob("*"):
                        if source_path.is_file() and source_path.suffix in {".md", ".yaml"}:
                            self.assertNotIn(
                                prohibited_contract,
                                source_path.read_text(encoding="utf-8"),
                                str(source_path.relative_to(REPOSITORY_ROOT)),
                            )
                self.assertNotIn(prohibited_contract, design_text)

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
            {
                "dev-backlog-watchdog",
                "methodology-design-system-checklist-runner",
                "methodology-design-system-review-coordinator",
                "wiki-query-responder",
                "wiki-topic-verifier",
            },
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
                "detect-technology-skills",
                "create-project-configuration",
                "skill-authoring",
                "maintain-methodology-documentation",
                "verify-documentation-page",
                "route-documentation-work",
            )
        }
        for skill, text in skill_texts.items():
            with self.subTest(skill=skill):
                self.assertIn("mcp-agent-ops", text)
                self.assertIn("rejection", text)

        claim_mcp_text = (SKILLS_ROOT / "resource-claim-helper-mcp" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("mcp-agent-ops", claim_mcp_text)
        self.assertIn(
            "Do not configure the current mcp-agent-ops provider as the claim helper.",
            claim_mcp_text,
        )
        for missing_tool in ("claim_extend_deadline", "claim_reset"):
            with self.subTest(missing_tool=missing_tool):
                self.assertIn(f"`{missing_tool}`", claim_mcp_text)

        shared_claim_text = (SKILLS_ROOT / "resource-claim" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("mcp-agent-ops", shared_claim_text)
        self.assertIn("one skill_load call", skill_texts["route-documentation-work"])
        self.assertIn("skill_resource_load", skill_texts["route-documentation-work"])
        self.assertIn("Do not reread a skill through MCP", skill_texts["route-documentation-work"])
        self.assertIn("detect_technology_skills", skill_texts["detect-technology-skills"])
        self.assertIn("skill_list plus detect_technology_skills", skill_texts["create-project-configuration"])
        self.assertIn("skill_validate", skill_texts["skill-authoring"])
        self.assertIn("verify_markdown_links", skill_texts["verify-documentation-page"])
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
                parsed = tomllib.loads(rendered)
                instructions = parsed["developer_instructions"]
                configured = parsed.get("skills", {}).get("config", [])
                if role.repository_mutation == "never":
                    self.assertNotIn(CODEX_HARNESS_SKILL_NAME, instructions)
                    self.assertNotIn(
                        CODEX_HARNESS_SKILL_NAME,
                        [item.get("name") for item in configured],
                    )
                else:
                    self.assertNotIn("BEGIN INLINED CORE SKILL", instructions)
                    self.assertIn(
                        CODEX_HARNESS_SKILL_NAME,
                        [item.get("name") for item in configured],
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
                "dev-backlog-watchdog",
                "dev-orchestrator",
                "dev-backlog-steward",
            ),
            "dev-orchestrator": (
                "dev-coder",
                "dev-code-reviewer",
                "dev-verifier",
                "dev-merge-coordinator",
            ),
            "methodology-maintainer": (
                "dev-skill-lint-reviewer",
                "methodology-artifact-reviewer",
                "dev-verifier",
            ),
            "methodology-design-system-review-coordinator": (
                "methodology-design-system-checklist-runner",
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
                if role_name == "methodology-design-system-review-coordinator":
                    self.assertEqual("never", role.repository_mutation)
                    self.assertEqual("read-only", role.optional_fields["isolation"])
                    self.assertIn(
                        "Invoke methodology-design-system-checklist-runner once for each required assignment",
                        role.instructions,
                    )
                    self.assertIn(
                        "Retry one malformed report once",
                        role.instructions,
                    )
                    self.assertIn(
                        "After one malformed-report retry, return BLOCKED",
                        role.instructions,
                    )
                    continue
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
        self.assertNotIn("integrate-agent-work", orchestrator.skills)
        self.assertNotIn("review-structured-artifact", orchestrator.skills)

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
                normalized_response = " ".join(response.split())
                self.assertIn("GOOD pre-move verdict", normalized_response)
                self.assertIn("GOOD post-move verdict", normalized_response)
                self.assertIn("commit closeout", normalized_response)
                self.assertIn("enabled resource-coordination evidence", normalized_response)
                self.assertNotIn("released the ingest claim", normalized_response)

    def test_topic_writer_hands_verification_to_the_owning_role(self) -> None:
        """Topic writing preserves edits and evidence without owning verifier dispatch."""
        topic_write_skill = (
            SKILLS_ROOT / "project-wiki-topic-write" / "SKILL.md"
        ).read_text(encoding="utf-8")
        topic_write_metadata = load_yaml_object(
            SKILLS_ROOT
            / "project-wiki-topic-write"
            / "agents"
            / "openai.yaml"
        )
        normalized_skill = " ".join(topic_write_skill.split())
        default_prompt = topic_write_metadata["interface"]["default_prompt"]
        writer_role = load_yaml_object(
            ROLES_ROOT / "wiki-activities" / "wiki-writer.role.yaml"
        )
        verifier_role = load_yaml_object(
            ROLES_ROOT / "wiki-activities" / "wiki-topic-verifier.role.yaml"
        )

        for prohibited in (
            "Spawn a fresh subagent",
            "invoke a fresh verifier again",
            "count one correction attempt",
            "at most two corrected resubmissions",
            "governing cap is exhausted",
            "return BLOCKED",
        ):
            with self.subTest(prohibited_skill_orchestration=prohibited):
                self.assertNotIn(prohibited, topic_write_skill)
        for required in (
            "The skill does not spawn or invoke the verifier",
            "Return the handoff to the owning conceptual role",
            "Leave the writer edits intact",
            "before-and-after no-mutation evidence",
            "role-owned BLOCKED evidence",
            "complete created, updated, and deleted page inventory",
            "lint, OKF validation, and leaf-link results",
        ):
            with self.subTest(required_writer_handoff=required):
                self.assertIn(required, normalized_skill)
        self.assertIn("role-owned independent verification", default_prompt)
        for prohibited in (
            "retry cap",
            "two-attempt default",
            "return BLOCKED",
        ):
            with self.subTest(prohibited_metadata_orchestration=prohibited):
                self.assertNotIn(prohibited, default_prompt)

        writer_instructions = writer_role["instructions"]
        boundary_text = " ".join(writer_instructions["boundaries"])
        delegation_text = " ".join(writer_instructions["delegation"])
        failure_text = " ".join(writer_instructions["failureHandling"])
        completion_text = " ".join(writer_instructions["completion"])
        self.assertIn("Invoke wiki-topic-verifier", delegation_text)
        self.assertIn(
            "Report BLOCKED when wiki-topic-verifier is unavailable",
            failure_text,
        )
        self.assertIn(
            "Capture the verifier invocation and returned receipt",
            delegation_text,
        )
        self.assertIn(
            "writer-owned page scope immediately before and after",
            delegation_text,
        )
        self.assertIn("attempted verifier write", boundary_text)
        self.assertIn("Preserve the current unverified writer edits", failure_text)
        self.assertIn("do not invent verifier findings", failure_text)
        self.assertIn("intentionally leave the worktree dirty", completion_text)
        self.assertIn(
            "Report BLOCKED only with the reviewed page inventory",
            completion_text,
        )
        self.assertEqual("never", verifier_role["repositoryMutation"])
        writer_scenarios = load_yaml_object(
            AGENT_TEST_SUITES_ROOT / "wiki-writer" / "scenarios.yaml"
        )["scenarios"]
        interruption = next(
            scenario
            for scenario in writer_scenarios
            if scenario["id"] == "verifier-interruption"
        )
        interruption_contract = " ".join(
            [
                *interruption["requiredBehaviors"],
                *interruption["forbiddenBehaviors"],
            ]
        )
        known_checks = {
            check["id"]
            for check in load_yaml_object(REPOSITORY_ROOT / "evals" / "judges.yaml")[
                "checks"
            ]
        }
        writer_fixtures = load_yaml_object(
            AGENT_TEST_SUITES_ROOT / "wiki-writer" / "fixtures" / "cases.yaml"
        )["cases"]
        self.assertEqual("BLOCKED", interruption["expectedTerminalStatus"])
        self.assertLessEqual(set(interruption["deterministicChecks"]), known_checks)
        self.assertIn("verifier-interruption", writer_fixtures)
        self.assertEqual(
            "executable_harness.py",
            interruption["offlineHarness"],
        )
        self.assertTrue(
            (
                AGENT_TEST_SUITES_ROOT
                / "wiki-writer"
                / interruption["offlineHarness"]
            ).is_file()
        )
        for required in (
            "Preserve writer edits",
            "Keep Wiki Topic Verifier read-only",
            "before-and-after state",
            "role-owned BLOCKED evidence",
            "Do not let project-wiki-topic-write invoke the verifier",
        ):
            with self.subTest(interruption_contract=required):
                self.assertIn(required, interruption_contract)

    def test_dev_orchestrator_disposes_every_confirmed_review_issue_before_closeout(self) -> None:
        """Source and native roles require correction or deliberate exclusion before closeout."""

        role_path = (
            ROLES_ROOT / "dev-activities" / "dev-orchestrator.role.yaml"
        )
        role = load_yaml_object(role_path)
        normalized_source = " ".join(role_path.read_text(encoding="utf-8").split())
        instruction_sections = role["instructions"]
        normalized_boundaries = " ".join(" ".join(instruction_sections["boundaries"]).split())
        normalized_decisions = " ".join(
            " ".join(instruction_sections["decisions"]).split()
        )
        normalized_workflow = " ".join(
            " ".join(instruction_sections["workflow"]).split()
        )
        self.assertIn(
            "Give every issue confirmed by an independent reviewer or verifier exactly one "
            "of two dispositions before delivery closeout.",
            normalized_boundaries,
        )
        self.assertIn(
            "Return the confirmed issue to the original producing agent when it will be "
            "corrected in the current delivery",
            normalized_decisions,
        )
        self.assertIn(
            "Deliberately exclude the confirmed issue from the current delivery only when it "
            "will not be corrected there",
            normalized_decisions,
        )
        self.assertIn(
            "apply create-work-item and the effective Persistence-selected provider "
            "implementation before closeout",
            normalized_workflow,
        )
        self.assertIn(
            "Never merely report a confirmed issue as a warning and close the delivery.",
            normalized_workflow,
        )
        required_policy = (
            "exactly one of two dispositions before delivery closeout",
            "original producing agent",
            "fresh-context re-review",
            "reverification",
            "deliberately exclude",
            "create-work-item and the effective Persistence-selected provider implementation",
            "sporadic confirmed issues",
            "Never merely report a confirmed issue as a warning and close",
        )
        for phrase in required_policy:
            with self.subTest(source_policy=phrase):
                self.assertIn(phrase.lower(), normalized_source.lower())

        for prohibited_policy in (
            "unconfirmed observation",
            "baseline warning",
            "reconcile duplicates",
            "duplicate-reconciliation",
            "If provider none, UNSET, an unsupported provider",
        ):
            with self.subTest(prohibited_policy=prohibited_policy):
                self.assertNotIn(prohibited_policy.lower(), normalized_source.lower())

        self.assertIn(
            "every confirmed reviewer or verifier issue has completed exactly one of the two "
            "required dispositions",
            " ".join(" ".join(instruction_sections["completion"]).split()),
        )
        output_names = {next(iter(entry)) for entry in role["outputContract"]}
        self.assertIn("confirmed issue dispositions", output_names)
        defect_example = next(
            example
            for example in role["examples"]
            if "confirmed verifier issue" in example["purpose"]
        )
        normalized_example = " ".join(
            defect_example["plausibleResponse"].split()
        ).lower()
        for phrase in (
            "original dev-coder corrected the issue",
            "fresh re-review passed",
            "reverification passed",
            "same delivery",
        ):
            with self.subTest(example_evidence=phrase):
                self.assertIn(phrase, normalized_example)

        adapter_paths = {
            "codex": GENERATED_ADAPTERS_ROOT
            / "codex"
            / "agents"
            / "dev-orchestrator.toml",
            "claude": GENERATED_ADAPTERS_ROOT
            / "claude"
            / "agents"
            / "dev-orchestrator.md",
            "gemini": GENERATED_ADAPTERS_ROOT
            / "gemini"
            / "agents"
            / "dev-orchestrator.md",
            "junie": GENERATED_ADAPTERS_ROOT
            / "junie"
            / "agents"
            / "dev-orchestrator.md",
        }
        for adapter, adapter_path in adapter_paths.items():
            normalized_adapter = " ".join(
                adapter_path.read_text(encoding="utf-8").split()
            ).lower()
            for phrase in required_policy:
                with self.subTest(adapter=adapter, rendered_policy=phrase):
                    self.assertIn(phrase.lower(), normalized_adapter)
            for prohibited_policy in (
                "unconfirmed observation",
                "baseline warning",
                "reconcile duplicates",
                "duplicate-reconciliation",
                "if provider none, unset, an unsupported provider",
            ):
                with self.subTest(adapter=adapter, prohibited_policy=prohibited_policy):
                    self.assertNotIn(prohibited_policy, normalized_adapter)
            self.assertIn("confirmed issue dispositions", normalized_adapter)

        scenarios = load_yaml_object(
            AGENT_TEST_SUITES_ROOT / "dev-orchestrator" / "scenarios.yaml"
        )["scenarios"]
        bounded = next(item for item in scenarios if item["id"] == "bounded-correction")
        correction = next(
            item for item in scenarios if item["id"] == "confirmed-issue-correction"
        )
        exclusion = next(
            item for item in scenarios if item["id"] == "skill-under-test-defect-routing"
        )
        self.assertEqual("BLOCKED", bounded["expectedTerminalStatus"])
        self.assertIn("Stop after two failed corrections", bounded["requiredBehaviors"])
        self.assertNotIn(
            "Complete correction, fresh re-review, and reverification before closeout",
            bounded["requiredBehaviors"],
        )
        self.assertIn(
            "Complete correction, fresh re-review, and reverification before closeout",
            correction["requiredBehaviors"],
        )
        self.assertEqual("READY", correction["expectedRoleStatus"])
        self.assertEqual(
            ["dev-code-reviewer", "dev-coder", "dev-code-reviewer", "dev-verifier"],
            correction["requiredDependencyOrder"],
        )
        self.assertIn(
            "Deliberately exclude the confirmed issue from the current delivery",
            exclusion["requiredBehaviors"],
        )
        self.assertIn(
            "Invoke the effective file-provider work-item creation procedure before closeout",
            exclusion["requiredBehaviors"],
        )
        self.assertIn(
            "Warn and close without either disposition",
            exclusion["forbiddenBehaviors"],
        )
        self.assertEqual(
            ["dev-verifier"],
            exclusion["requiredDependencyOrder"],
        )
        self.assertNotIn(
            "dev-backlog-steward",
            exclusion["allowedAgentDependencies"],
        )
        self.assertEqual(
            ["confirmation", "finding"],
            exclusion["requiredHandoffReceiptLanes"],
        )
        self.assertIn(
            "Treat the issue as confirmed without an independent reviewer or verifier receipt",
            exclusion["forbiddenBehaviors"],
        )

    def test_dev_backlog_coordinator_uses_selected_provider_and_completion_routes(self) -> None:
        """The coordinator should supervise provider-neutral state and selected delivery."""
        role = yaml.safe_load(
            (
                ROLES_ROOT
                / "dev-activities"
                / "dev-backlog-coordinator.role.yaml"
            ).read_text(encoding="utf-8")
        )
        role_text = json.dumps(role, sort_keys=True)

        for required_contract in (
            "effective Persistence-selected management skill",
            "Provider file",
            "Provider github",
            "Provider gitlab",
            "Provider azure-devops or jira",
            "Provider none",
            "Provider UNSET or an unavailable selected skill",
            "effective Commit-selected skill",
            "Do not reproduce provider or Commit procedures",
            "active queue defined by coordinate-work-items",
            "Retry only when that notification arrives",
            "Only the watchdog investigates stale claim ownership",
            "Every fifteen minutes",
            "canonical execution identity",
            "When coordinate-codex-tasks is active, also retain its canonical Codex task and conversation identifiers",
            "remove the clean worktree",
        ):
            with self.subTest(contract=required_contract):
                self.assertIn(required_contract, role_text)

        for obsolete_contract in (
            "file-backed work-item queue",
            "Count Status Running from the file-backed backlog",
            "canonical backlog path",
            "direct integration",
            "file-backed queue snapshot",
        ):
            with self.subTest(contract=obsolete_contract):
                self.assertNotIn(obsolete_contract, role_text)
        for retired_wait_contract in (
            "six five-minute retries",
            "thirty-minute retry window",
            "delivery-resource wait that reached thirty minutes",
        ):
            with self.subTest(retired_wait_contract=retired_wait_contract):
                self.assertNotIn(retired_wait_contract, role_text)
        self.assertNotIn("ten actively eligible Starting or Running items", role_text)

    def test_dev_backlog_coordinator_snapshot_includes_stalled_state(self) -> None:
        """Source and generated role outputs must expose Stalled inventory."""

        role_path = (
            ROLES_ROOT
            / "dev-activities"
            / "dev-backlog-coordinator.role.yaml"
        )
        role = load_yaml_object(role_path)
        lifecycle_snapshot = next(
            entry["provider lifecycle snapshot"]["purpose"]
            for entry in role["outputContract"]
            if "provider lifecycle snapshot" in entry
        )
        self.assertIn("STALLED", lifecycle_snapshot)

        generated_paths = (
            GENERATED_ADAPTERS_ROOT
            / "claude"
            / "agents"
            / "dev-backlog-coordinator.md",
            GENERATED_ADAPTERS_ROOT
            / "codex"
            / "agents"
            / "dev-backlog-coordinator.toml",
            GENERATED_ADAPTERS_ROOT
            / "gemini"
            / "agents"
            / "dev-backlog-coordinator.md",
            GENERATED_ADAPTERS_ROOT
            / "junie"
            / "agents"
            / "dev-backlog-coordinator.md",
        )
        for generated_path in generated_paths:
            with self.subTest(generated_path=generated_path):
                rendered = generated_path.read_text(encoding="utf-8")
                self.assertIn("provider lifecycle snapshot", rendered)
                self.assertIn("STALLED", rendered)

    def test_backlog_roles_reconcile_active_evidence_before_refilling_capacity(
        self,
    ) -> None:
        """Roles select the central contract without restating its mechanics."""

        coordinator_path = (
            ROLES_ROOT
            / "dev-activities"
            / "dev-backlog-coordinator.role.yaml"
        )
        watchdog_path = (
            ROLES_ROOT
            / "dev-activities"
            / "dev-backlog-watchdog.role.yaml"
        )
        coordinator_role = load_yaml_object(coordinator_path)
        watchdog_role = load_yaml_object(watchdog_path)
        central_section = "Active Execution And Capacity"
        prohibited_mechanics = (
            "exactly 60 seconds",
            "60-second",
            "Starting-plus-Running",
            "Active Execution Evidence",
            "Reservation Started At",
            "Settlement Deadline",
        )

        for role in (coordinator_role, watchdog_role):
            role_text = json.dumps(role, sort_keys=True)
            selected = {next(iter(entry)) for entry in role["skills"]}
            self.assertIn("coordinate-work-items", selected)
            self.assertIn("coordinate-codex-tasks", selected)
            self.assertIn(central_section, role_text)
            for phrase in prohibited_mechanics:
                self.assertNotIn(phrase, role_text)

        self.assertIn(
            "A failed, stopped, or missing canonical execution triggers the central "
            "coordination section.",
            " ".join(coordinator_role["instructions"]["decisions"]),
        )
        self.assertIn(
            "For a failed, stopped, or missing canonical execution, report the "
            "portable reconciliation trigger",
            " ".join(watchdog_role["instructions"]["workflow"]),
        )
        self.assertIn(
            "dev-backlog-watchdog",
            coordinator_role["agentDependencies"],
        )

        generated_roots = ("claude", "codex", "gemini", "junie")
        generated_suffixes = {
            "claude": "dev-backlog-coordinator.md",
            "codex": "dev-backlog-coordinator.toml",
            "gemini": "dev-backlog-coordinator.md",
            "junie": "dev-backlog-coordinator.md",
        }
        for runtime in generated_roots:
            coordinator_generated = (
                GENERATED_ADAPTERS_ROOT
                / runtime
                / "agents"
                / generated_suffixes[runtime]
            ).read_text(encoding="utf-8")
            watchdog_generated = (
                GENERATED_ADAPTERS_ROOT
                / runtime
                / "agents"
                / generated_suffixes[runtime].replace(
                    "dev-backlog-coordinator",
                    "dev-backlog-watchdog",
                )
            ).read_text(encoding="utf-8")
            with self.subTest(runtime=runtime):
                self.assertIn("coordinate-work-items", coordinator_generated)
                self.assertIn("coordinate-codex-tasks", coordinator_generated)
                self.assertIn("coordinate-work-items", watchdog_generated)
                self.assertIn("coordinate-codex-tasks", watchdog_generated)
                for phrase in prohibited_mechanics:
                    self.assertNotIn(phrase, coordinator_generated)
                    self.assertNotIn(phrase, watchdog_generated)

    def test_claim_related_skills_do_not_copy_claim_events_or_polling_rules(
        self,
    ) -> None:
        """Only resource-claim defines claim events, scopes, and release timing."""
        dependent_skills = (
            "resource-claim-helper",
            "resource-claim-helper-command",
            "resource-claim-helper-mcp",
            "integrate-agent-work",
            "coordinate-work-items",
            "deliver-work-item-main-branch",
            "deliver-work-item-feature-branch",
            "create-work-item-file",
            "create-project-configuration",
            "verify-end-to-end-workflow",
            "manage-work-items-file",
        )
        for skill_name in dependent_skills:
            text = (SKILLS_ROOT / skill_name / "SKILL.md").read_text(encoding="utf-8")
            with self.subTest(skill=skill_name):
                self.assertNotIn("| No. | Event | Claim | Release |", text)
                self.assertNotIn("needs no claim", text)
                self.assertNotIn("claim-free", text)
                self.assertNotIn("six five-minute", text)
                self.assertNotIn("retries at five", text)
                self.assertNotIn("adaptive backoff", text)

    def test_wiki_ingester_blocks_with_role_owned_verifier_interruption_evidence(
        self,
    ) -> None:
        """Verifier interruption preserves the applicable gate state and returns BLOCKED."""
        build_skill_docs = load_build_skill_docs_module()
        skill_payload = build_skill_docs.build_payload()
        roles = build_skill_docs.load_role_definitions(set(skill_payload["skills"]))
        role = next(role for role in roles if role.name == "wiki-ingester")

        boundary_text = " ".join(role.instruction_sections["boundaries"])
        workflow_text = " ".join(role.instruction_sections["workflow"])
        delegation_text = " ".join(role.instruction_sections["delegation"])
        review_text = " ".join(role.instruction_sections["review"])
        failure_text = " ".join(role.instruction_sections["failureHandling"])
        completion_text = " ".join(role.instruction_sections["completion"])
        skill_text = (
            SKILLS_ROOT / "project-wiki" / "SKILL.md"
        ).read_text(encoding="utf-8")
        operations_text = (
            SKILLS_ROOT / "project-wiki" / "references" / "operations.md"
        ).read_text(encoding="utf-8")
        verifier_payload = (
            "Provide the repository root, verification gate, page inventory, source "
            "evidence path, current validation output, and correction-attempt count and cap."
        )
        interruption_examples = [
            example
            for example in role.examples
            if "interruption" in example["purpose"].lower()
            or "interrupted" in example["purpose"].lower()
        ]

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
        self.assertIn("do not restore substantiated content", failure_text)
        self.assertNotIn("restore the source and its page links", failure_text)
        self.assertIn("Own fresh wiki-topic-verifier routing", boundary_text)
        self.assertIn("does not authorize a source move", boundary_text)
        self.assertIn("Capture the invocation and returned receipt", delegation_text)
        for surface, text in (
            ("skill", skill_text),
            ("operations", operations_text),
            ("role", delegation_text),
        ):
            with self.subTest(verifier_payload_surface=surface):
                self.assertIn(verifier_payload, " ".join(text.split()))
        self.assertIn("report role-owned BLOCKED evidence", workflow_text)
        self.assertIn("At the pre-move gate, keep the source in raw", workflow_text)
        self.assertIn("At the post-move gate, retain the already-processed source", workflow_text)
        self.assertIn("verification gate, invocation and receipt evidence", failure_text)
        self.assertIn("page and source inventories", failure_text)
        self.assertIn("completed correction attempts and governing cap", failure_text)
        self.assertIn("current source location", failure_text)
        self.assertIn("exact unresolved interruption", failure_text)
        self.assertIn("Report READY only after every assigned source passes", completion_text)
        self.assertNotIn("completes the verifier interruption workflow", completion_text)
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
        self.assertEqual(2, len(interruption_examples))
        pre_move_example = next(
            example
            for example in interruption_examples
            if "pre-move" in example["purpose"].lower()
        )
        post_move_example = next(
            example
            for example in interruption_examples
            if "post-move" in example["purpose"].lower()
        )
        for example in interruption_examples:
            response = example["plausibleResponse"]
            normalized_response = " ".join(response.split())
            with self.subTest(interruption_example=example["purpose"]):
                self.assertIn("STATUS: BLOCKED", normalized_response)
                self.assertNotIn("STATUS: READY", normalized_response)
                self.assertIn("OPEN QUESTIONS:", normalized_response)
                self.assertIn("page and source inventories", normalized_response)
                self.assertIn("validation output", normalized_response)
                self.assertIn("cap", normalized_response)
                self.assertIn("exact unresolved interruption", normalized_response)
                self.assertIn(
                    "Committed the retained in-scope wiki result",
                    normalized_response,
                )
                self.assertIn("confirmed a clean worktree", normalized_response)
                self.assertIn(
                    "resource-coordination release or handoff",
                    normalized_response,
                )
                self.assertIn("recorded the final queue recheck", normalized_response)
        pre_move_response = " ".join(pre_move_example["plausibleResponse"].split())
        self.assertIn("source remains at raw/retry-policy.md", pre_move_response)
        self.assertNotIn("raw/processed/retry-policy.md", pre_move_response)
        post_move_response = " ".join(post_move_example["plausibleResponse"].split())
        self.assertIn("returned GOOD", post_move_response)
        self.assertIn("raw/processed/retry-policy.md", post_move_response)
        self.assertIn("GOOD pre-move receipt", post_move_response)
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
                    r"(?i)(?:exhausted.{0,180}reports? BLOCKED|"
                    r"reports? BLOCKED.{0,180}exhausted)",
                )
                self.assertRegex(
                    normalized_text,
                    r"(?i)correction-attempt cap (?:governs each verification "
                    r"gate|to the pre-move verification gate)",
                )
                self.assertRegex(
                    normalized_text,
                    r"(?i)(?:correction-attempt|governing) cap.{0,120}"
                    r"post-move(?: verification)? gate",
                )
                self.assertRegex(
                    normalized_text,
                    r"(?i)(?:bounded default.{0,120}post-move(?: verification)? gate|"
                    r"post-move(?: verification)? gate.{0,320}at most two corrected "
                    r"resubmissions after the initial post-move verdict)",
                )
                self.assertRegex(
                    normalized_text,
                    r"(?i)(?:BLOCKED stop rule.{0,120}post-move(?: verification)? gate|"
                    r"post-move(?: verification)? gate.{0,760}exhausted.{0,180}"
                    r"reports? BLOCKED)",
                )
                self.assertNotRegex(
                    normalized_text,
                    r"(?i)repeat(?: lint plus verification)? until "
                    r"(?:the verifier|it) returns GOOD",
                )

    def test_lifecycle_reconciles_active_execution_before_refilling_capacity(self) -> None:
        """The state map must make active eligibility evidence explicit."""

        lifecycle_text = (
            REPOSITORY_ROOT / "design" / "orchestrated-development-lifecycle.html"
        ).read_text(encoding="utf-8")
        backlog_section = lifecycle_text[
            lifecycle_text.index('<section class="section" id="backlog"') :
            lifecycle_text.index('<section class="section" id="file-provider"')
        ]

        reconciliation_label = (
            '<h3 id="task-execution-anomaly-title">Active execution reconciliation '
            "<span>One central contract</span></h3>"
        )
        self.assertIn(reconciliation_label, backlog_section)
        self.assertLess(
            backlog_section.index(reconciliation_label),
            backlog_section.index("<strong>Stalled</strong>"),
        )
        self.assertLess(
            backlog_section.index(reconciliation_label),
            backlog_section.index("<strong>Blocked</strong>"),
        )

        state_map_match = re.search(
            r'<div class="state-map" role="img" aria-label="([^"]+)">',
            backlog_section,
        )
        self.assertIsNotNone(state_map_match)
        state_map_label = state_map_match.group(1)
        for clause in (
            "The Coordinator commits Ready to Starting under one exact provider claim, "
            "releases it, launches one root execution, and ends its handoff.",
            "The new execution independently commits Starting to Running under its own exact "
            "provider claim before implementation.",
            "When coordinate-codex-tasks is active, the root execution maps to one Codex task.",
            "A failed or missing launch remains Starting until the Watchdog reports it "
            "and the Coordinator performs recovery.",
            "Running is active only while both its finite condition deadline and "
            "next-reconciliation boundary remain in the future.",
            "Missing or expired evidence moves the item to a truthful non-active "
            "state before capacity is refilled.",
            "Stalled and Blocked are non-active recovery states.",
        ):
            with self.subTest(aria_clause=clause):
                self.assertIn(clause, state_map_label)

        anomaly_section = backlog_section[
            backlog_section.index(
                '<aside class="task-execution-anomaly"'
            ) :
            backlog_section.index('<div class="state-branches">')
        ]
        self.assertIn(
            '<ol class="task-anomaly-flow" '
            'aria-label="Active execution reconciliation flow">',
            anomaly_section,
        )
        self.assertIn(
            ".task-anomaly-flow { grid-template-columns: 1fr; }",
            lifecycle_text,
        )
        flow_steps = (
            "Recover Starting",
            "Prove Running",
            "Reconcile inactive work",
        )
        flow_positions = tuple(
            anomaly_section.index(f"<strong>{step}</strong>")
            for step in flow_steps
        )
        self.assertEqual(tuple(sorted(flow_positions)), flow_positions)
        for clause in (
            "The Coordinator commits Ready to Starting, releases its claim, launches one root execution, and ends its handoff.",
            "The new execution commits Starting to Running through its own claim.",
            "When coordinate-codex-tasks is active, that execution maps to one Codex task.",
            "Failed or missing launches stay Starting until Watchdog evidence triggers Coordinator recovery.",
            "Observed and started times are history.",
            "Keep both future boundaries current",
            "Expiry of either boundary invalidates active eligibility.",
            "A failed launch remains Starting until Coordinator recovery.",
            "Absent, invalid, or expired evidence cannot preserve Running.",
            "The Coordinator directly records its selected lifecycle transition through the effective Persistence manager before filling the vacancy.",
        ):
            with self.subTest(visible_clause=clause):
                self.assertIn(clause, anomaly_section)

        retired_shortcuts = (
            "Preserve its current state and Starting-plus-Running capacity",
            "The anomaly alone authorizes neither Stalled, Blocked",
            "The anomaly alone does not release Starting-plus-Running capacity",
        )
        for clause in retired_shortcuts:
            with self.subTest(retired_clause=clause):
                self.assertNotIn(clause, state_map_label)
                self.assertNotIn(clause, anomaly_section)

    def test_lifecycle_documents_simplified_coordination_and_delivery_sequences(self) -> None:
        """The lifecycle should teach concepts progressively without runtime-specific clutter."""
        lifecycle_path = (
            REPOSITORY_ROOT / "design" / "orchestrated-development-lifecycle.html"
        )
        lifecycle_text = lifecycle_path.read_text(encoding="utf-8")

        ordered_headings = (
            ("backlog-title", "Work-Item Backlog"),
            ("file-provider-title", "File-Backed Work Items"),
            ("agents-title", "Agent Roles"),
            ("runtime-section-title", "Runtime Coordination"),
            ("private-work-title", "Private Workspaces"),
            ("coordination-title", "Shared-Resource Coordination"),
            ("delivery-title", "Delivery Stages"),
            ("blocker-recovery-title", "Blocker Recovery"),
            ("decisions-title", "User Decision Gates"),
            ("evidence-title", "Delivery Evidence"),
            ("design-work-title", "Design And Documentation Workflows"),
        )
        heading_positions = tuple(
            lifecycle_text.index(f'<h2 id="{heading_id}">{heading}</h2>')
            for heading_id, heading in ordered_headings
        )
        self.assertEqual(tuple(sorted(heading_positions)), heading_positions)

        agents_section = lifecycle_text[
            lifecycle_text.index('<section class="section" id="agents"') :
            lifecycle_text.index(
                '<section class="section" id="runtime-coordination"'
            )
        ]
        runtime_section = lifecycle_text[
            lifecycle_text.index(
                '<section class="section" id="runtime-coordination"'
            ) :
            lifecycle_text.index('<section class="section" id="private-work"')
        ]
        delivery_section = lifecycle_text[
            lifecycle_text.index('<section class="section" id="delivery"') :
            lifecycle_text.index('<section class="section" id="blocker-recovery"')
        ]
        commit_to_persistence_handoff = delivery_section[
            delivery_section.index('<li><span class="number">8</span>') :
            delivery_section.index('<li><span class="number">9</span>')
        ]
        blocker_section = lifecycle_text[
            lifecycle_text.index('<section class="section" id="blocker-recovery"') :
            lifecycle_text.index('<section class="section" id="decisions"')
        ]
        backlog_section = lifecycle_text[
            lifecycle_text.index('<section class="section" id="backlog"') :
            lifecycle_text.index('<section class="section" id="file-provider"')
        ]
        self.assertIn('<h2 id="agents-title">Agent Roles</h2>', agents_section)
        self.assertNotIn("Agents And Handoffs", agents_section)
        self.assertNotIn("Lifecycle Handoffs", agents_section)
        self.assertIn(
            '<figcaption id="delivery-sequence-title">Lifecycle Handoffs',
            delivery_section,
        )
        self.assertIn(
            "A Handoff transfers evidence and the next action",
            delivery_section,
        )
        self.assertIn("<h3>Stalled Dispositions</h3>", backlog_section)
        self.assertIn('<ol class="stalled-dispositions">', backlog_section)
        stalled_dispositions = (
            "Restore Running",
            "Restore Ready",
            "Record Blocked",
            "Record User Action Required",
            "Select Terminal Outcome",
        )
        stalled_positions = tuple(
            backlog_section.index(f"<strong>{disposition}</strong>")
            for disposition in stalled_dispositions
        )
        self.assertEqual(tuple(sorted(stalled_positions)), stalled_positions)
        self.assertIn(
            "<strong>Select Terminal Outcome</strong> only from sufficient "
            "evidence for Completed, Failed, or Abandoned.",
            backlog_section,
        )
        for heading in (
            "Orchestrator Blocker Steps",
            "Blocker Notification Fields",
            "Coordinator Sequence",
        ):
            with self.subTest(blocker_handoff_heading=heading):
                self.assertIn(f"<h4>{heading}</h4>", blocker_section)
        self.assertIn(
            "An Assignment is bounded work sent to an Agent; it does not create another work-item Thread.",
            agents_section,
        )
        self.assertIn(
            "Dev Backlog Steward is optional and limited to provider-wide inventory, normalization, archival audits, and recovery.",
            agents_section,
        )
        self.assertIn(
            '<figcaption id="thread-model-title">Threads Contain Agents',
            agents_section,
        )
        self.assertIn(
            '<figcaption id="steward-sequence-title">Provider-Wide Steward Assignments Are Sequential',
            runtime_section,
        )
        self.assertIn(
            "only one provider-wide maintenance assignment may be active or queued at a time",
            runtime_section,
        )
        self.assertIn(
            "A final assignment result proves only that assignment finished.",
            runtime_section,
        )
        self.assertIn(
            'class="thread-model-figure" aria-labelledby="thread-model-title"',
            agents_section,
        )
        self.assertIn(
            'class="steward-sequence-figure" aria-labelledby="steward-sequence-title"',
            runtime_section,
        )
        self.assertIn(
            'role="img" aria-label="A parent coordination Thread contains a Coordinator Agent',
            agents_section,
        )
        self.assertIn(
            'role="img" aria-label="Assignment A performs one provider-wide maintenance operation.',
            runtime_section,
        )
        self.assertIn(
            '<figcaption id="watchdog-cycle-title">Watchdog Observation Is Read-Only',
            runtime_section,
        )
        self.assertIn(
            "<h3>Backlog Blockage Recovery And Dispatch Mode</h3>",
            runtime_section,
        )
        self.assertIn(
            'aria-label="Lifecycle terminology"',
            agents_section,
        )
        terminology = (
            ("Thread", "The retained execution context."),
            ("Agent", "A running actor inside a Thread."),
            ("Role", "The reusable responsibility and authority contract."),
            ("Assignment", "Bounded work sent to an Agent."),
            (
                "Claim",
                "Conditional temporary protection when resource-claim is selected.",
            ),
        )
        for term, definition in terminology:
            with self.subTest(lifecycle_term=term):
                self.assertIn(f"<dt>{term}</dt><dd>{definition}</dd>", agents_section)

        assignment_steps = (
            "Assignment A",
            "Commit And Finish",
            "Confirm Idle",
            "Assignment B",
        )
        assignment_positions = tuple(
            runtime_section.index(f"<strong>{step}</strong>")
            for step in assignment_steps
        )
        self.assertEqual(
            tuple(sorted(assignment_positions)),
            assignment_positions,
        )
        self.assertIn(
            ".thread-map { grid-template-columns: 1fr; }",
            lifecycle_text,
        )
        self.assertIn(
            ".assignment-flow { grid-template-columns: 1fr; }",
            lifecycle_text,
        )
        self.assertNotIn("Conditional Claim A", runtime_section)
        self.assertNotIn("Conditional Claim B", runtime_section)
        provider_none_delivery_markers = (
            "task-local AWAITING_REVIEW",
            "delivery evidence",
            "without provider mutation",
            "Commit READY",
            "task-local COMPLETED finalization",
            "terminal evidence",
            "without provider mutation",
        )
        marker_offset = 0
        for marker in provider_none_delivery_markers:
            with self.subTest(provider_none_delivery_marker=marker):
                marker_position = commit_to_persistence_handoff.index(
                    marker,
                    marker_offset,
                )
                marker_offset = marker_position + len(marker)
        self.assertEqual(
            2,
            commit_to_persistence_handoff.lower().count("provider none"),
        )
        self.assertIn(
            '<span class="actor">Root Orchestrator</span>'
            '<span class="direction" role="img" aria-label="sends to">'
            '&rarr;</span><span class="actor">Persistence Manager</span>',
            commit_to_persistence_handoff,
        )

        title_like_labels = (
            "Work-Item Continuity",
            "Lifecycle Overview",
            "Work-Item Types",
            "Work-Item Readiness",
            "Work-Item Status",
            "Lifecycle Roles",
            "Production And Implementation Agents",
            "Independent Reviewers",
            "Integration Specialists",
            "Threads Contain Agents",
            "Execution Contexts",
            "Provider-Wide Steward Assignments Are Sequential",
            "Parallel Workspaces",
            "Shared Resource Gate",
            "Claim Cleanup",
            "Claim Limits",
            "Lifecycle Handoffs",
            "Execution Safeguards",
            "1 · Recorded State",
            "2 · Clear Question",
            "3 · Consequences And Boundary",
            "4 · Decision Record",
            "5 · Same-Thread Resume",
            "Evidence Boundaries",
            "Thread Evidence Boundary:",
            "Integration Cleanup",
            "Planned Development",
            "Whole-Project Reverse Engineering",
        )
        for label in title_like_labels:
            with self.subTest(title_like_label=label):
                self.assertIn(f">{label}<", lifecycle_text)

        self.assertEqual(
            (
                "Intake",
                "Selection",
                "Private Work",
                "Independent Review",
                "Delivery",
                "Closeout",
            ),
            tuple(
                re.findall(
                    r'<li><span class="station">\d{2}</span><strong>([^<]+)</strong>',
                    lifecycle_text,
                )
            ),
        )

        self.assertEqual(1, lifecycle_text.count('class="lifecycle-rail"'))
        self.assertEqual(1, lifecycle_text.count('class="status-figure"'))
        self.assertEqual(3, lifecycle_text.count('class="sequence-figure"'))
        self.assertEqual(1, lifecycle_text.count('class="thread-model-figure"'))
        self.assertEqual(1, lifecycle_text.count('class="steward-sequence-figure"'))
        self.assertEqual(1, lifecycle_text.count('class="branch-figure"'))
        self.assertEqual(1, lifecycle_text.count('class="resource-figure"'))
        self.assertEqual(1, lifecycle_text.count('class="evidence-table"'))
        self.assertEqual(1, lifecycle_text.count("<table"))
        self.assertGreater(lifecycle_text.count('aria-label="sends to"'), 0)

        overview_text = re.sub(
            r"<details>.*?</details>",
            "",
            lifecycle_text,
            flags=re.DOTALL,
        )
        paragraphs = re.findall(r"<p(?:\s[^>]*)?>(.*?)</p>", overview_text, re.DOTALL)
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
            "Stalled",
            "Blocked",
            "Completed",
            "Awaiting Review",
            "Archive placement is not another lifecycle status",
            "The Work item is the only durable provider record",
            "Backlog Coordinator",
            "Backlog Watchdog",
            "Backlog Steward",
            "Dev Orchestrator",
            "Independent Reviewers",
            "Verifier",
            "Merge Coordinator",
            "Starting and Running Work items use separate worktrees",
            "Main-branch delivery",
            "Feature-branch delivery",
            "temporary shared-mutation protection",
            "it does not prove review, delivery, or completion",
            "one cheapest representative first",
            "A user answer resolves the decision gate",
            "Thread Evidence Boundary",
            "When coordinate-codex-tasks is active, the root execution maps to one Codex task.",
        ):
            with self.subTest(lifecycle_phrase=phrase):
                self.assertIn(phrase, lifecycle_text)

        for obsolete_phrase in (
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

    def test_completed_work_items_are_reflected_in_human_facing_documentation(self) -> None:
        """Document Persistence, notification, blockage, mode, and claim behavior."""

        lifecycle_text = (
            REPOSITORY_ROOT / "design" / "orchestrated-development-lifecycle.html"
        ).read_text(encoding="utf-8")
        configuration_text = (
            REPOSITORY_ROOT / "design" / "agentic-configuration.html"
        ).read_text(encoding="utf-8")
        readme_text = README_PATH.read_text(encoding="utf-8")

        for phrase in (
            "After a new work item is persisted",
            "It does not reserve capacity, change lifecycle state, create a delivery execution, or start implementation.",
            "Resolve Backlog Blockage owns diagnosis and one-item-at-a-time recovery",
            "Set Solo Mode disables only new secondary-thread dispatch",
            "Set Multitask Mode enables new dispatch only after every blockage item is terminal",
            "Repeated transitions preserve the effective setting",
            "Release removes the named live claim while the registry is locked",
            "reset creates an empty claim registry before new work is dispatched.",
        ):
            with self.subTest(lifecycle_phrase=phrase):
                self.assertIn(phrase, lifecycle_text)

        for text in (readme_text, configuration_text):
            with self.subTest(persistence_document=text[:40]):
                self.assertIn("durable work-item management is first requested", text)
                self.assertIn("AGENTS.md.candidate", text)
                self.assertIn("Deferral leaves Persistence", text)

        for phrase in (
            "After a new file-backed work item is committed",
            "Resolve Backlog Blockage",
            "Set Solo Mode",
            "Set Multitask Mode",
        ):
            with self.subTest(readme_phrase=phrase):
                self.assertIn(phrase, readme_text)

    def test_lifecycle_routes_main_branch_and_pull_request_completion_paths(self) -> None:
        """The lifecycle should distinguish main-branch and feature-branch delivery."""
        lifecycle_path = (
            REPOSITORY_ROOT / "design" / "orchestrated-development-lifecycle.html"
        )
        lifecycle_text = lifecycle_path.read_text(encoding="utf-8")

        for phrase in (
            "Main-branch delivery",
            "fresh reconciliation branch from that exact commit",
            "Apply only the accepted paths",
            "Follow <a href=\"../skills/resource-claim/SKILL.md\">Resource Claim</a>",
            "Feature-branch delivery",
            "GitHub pull request or GitLab merge request",
            "Commit AWAITING_REVIEW without Persistence mutation",
            "Dev Orchestrator directly applies the effective Persistence manager exactly once for the nonterminal AWAITING_REVIEW update",
            "until Commit READY",
            "directly apply the manager exactly once for the distinct terminal Persistence closure",
            "Conditional integration role",
            "nested Merge Coordinator",
            "inside the same work item",
            "Re-review reconciled content when integration changes meaning",
            "delete the merged branch",
            "refill queue capacity",
        ):
            with self.subTest(delivery_phrase=phrase):
                self.assertIn(phrase, lifecycle_text)

        main_branch = lifecycle_text[
            lifecycle_text.index(">Main-branch delivery<") :
            lifecycle_text.index(">Feature-branch delivery<")
        ]
        main_branch_steps = (
            "Review and verify the private candidate",
            "Follow <a href=\"../skills/resource-claim/SKILL.md\">Resource Claim</a>",
            "Refresh current main",
            "Apply only the accepted paths",
        )
        main_branch_positions = tuple(
            main_branch.index(step) for step in main_branch_steps
        )
        self.assertEqual(tuple(sorted(main_branch_positions)), main_branch_positions)

        self.assertIn('table class="evidence-table" aria-labelledby=', lifecycle_text)
        self.assertIn("<caption id=", lifecycle_text)
        self.assertEqual(3, lifecycle_text.count('<th scope="col">'))
        self.assertGreater(lifecycle_text.count('role="img" aria-label="sends to"'), 0)
        self.assertIn("position: static; flex-wrap: wrap", lifecycle_text)

        private_index = lifecycle_text.index(">Private Workspaces<")
        coordination_index = lifecycle_text.index(">Shared-Resource Coordination<")
        delivery_index = lifecycle_text.index(">Delivery Stages<")
        self.assertLess(private_index, coordination_index)
        self.assertLess(coordination_index, delivery_index)

    def test_lifecycle_documents_planned_design_progression(self) -> None:
        lifecycle_text = (
            REPOSITORY_ROOT / "design" / "orchestrated-development-lifecycle.html"
        ).read_text(encoding="utf-8")

        self.assertEqual(
            1,
            lifecycle_text.count(">Design And Documentation Workflows<"),
        )
        ordered_stages = (
            "Functional intent",
            "Architecture",
            "High-level design",
            "Module design",
            "Implementation",
        )
        planned_text = lifecycle_text[
            lifecycle_text.index(">Design And Documentation Workflows<") :
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
        self.assertIn("enabled resource-coordination closeout", direct_response.lower())

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
        self.assertIn("enabled resource-coordination closeout", integrated_response.lower())

        no_coordination_example = next(
            example
            for example in role.examples
            if "resource coordination was none" in example["plausibleResponse"].lower()
        )
        self.assertIn(
            "no coordination lifecycle or evidence",
            no_coordination_example["plausibleResponse"].lower(),
        )

    def test_project_bootstrapper_has_separate_setup_and_documentation_branches(self) -> None:
        """Keep every later documentation gate out of the ordinary setup branch."""

        role = load_yaml_object(
            ROLES_ROOT / "project-setup" / "project-bootstrapper.role.yaml"
        )
        instructions = role["instructions"]
        workflow = instructions["workflow"]
        ordinary_steps = [
            step for step in workflow if "ordinary setup terminal path" in step.lower()
        ]
        self.assertEqual(1, len(ordinary_steps))
        ordinary_step = ordinary_steps[0]
        for phrase in (
            "selected empty documentation roots",
            "setup-specific validation",
            "commit",
            "clean",
            "release",
            "stop",
        ):
            with self.subTest(ordinary_phrase=phrase):
                self.assertIn(phrase, ordinary_step.lower())
        for forbidden in (
            "reverse engineering",
            "module design",
            "independent review",
            "dev-verifier",
        ):
            with self.subTest(forbidden_ordinary_phrase=forbidden):
                self.assertNotIn(forbidden, ordinary_step.lower())

        later_steps = [
            step for step in workflow
            if step.lower().startswith(
                "for the separately requested reverse-engineering/documentation workflow:"
            ) and "require dev-documentation-writer" in step.lower()
            and "coverage manifest" in step.lower()
        ]
        self.assertEqual(1, len(later_steps))
        self.assertIn("coverage manifest", later_steps[0].lower())

        later_prefix = "for the separately requested reverse-engineering/documentation workflow:"
        later_gate_terms = (
            "coverage manifest",
            "path coverage ledger",
            "module design",
            "higher-level design",
            "architecture",
            "functional specifications",
            "independent reviewer",
            "artifact review",
            "dev-verifier",
            "direct commit",
            "multi-contribution",
            "dev-merge-coordinator",
        )
        for section_name in ("workflow", "review", "completion"):
            for clause in instructions[section_name]:
                normalized = clause.lower()
                if normalized.startswith("ordinary setup"):
                    continue
                if any(term in normalized for term in later_gate_terms):
                    with self.subTest(section=section_name, clause=clause):
                        self.assertTrue(normalized.startswith(later_prefix), clause)

        ordinary_review = [
            clause for clause in instructions["review"]
            if clause.lower().startswith("ordinary setup review branch:")
        ]
        ordinary_completion = [
            clause for clause in instructions["completion"]
            if clause.lower().startswith("ordinary setup completion branch:")
        ]
        self.assertEqual(1, len(ordinary_review))
        self.assertEqual(1, len(ordinary_completion))
        self.assertIn("without artifact review or dev-verifier", ordinary_review[0].lower())
        self.assertIn("report ready", ordinary_completion[0].lower())

        configuration_only_example = next(
            example for example in role["examples"]
            if "repair an invalid project configuration" in example["purpose"].lower()
        )
        configuration_only_response = configuration_only_example["plausibleResponse"].lower()
        for phrase in (
            "selected empty documentation roots",
            "setup-specific validation",
            "bounded setup commit",
            "clean status",
            "released enabled setup resource ownership",
        ):
            with self.subTest(configuration_only_evidence=phrase):
                self.assertIn(phrase, configuration_only_response)
        for forbidden in (
            "dev-artifact-reviewer",
            "dev-merge-coordinator",
            "dev-verifier",
            "independent review",
            "final integration commit",
        ):
            with self.subTest(configuration_only_forbidden=forbidden):
                self.assertNotIn(forbidden, configuration_only_response)

    def test_project_configurator_new_scenarios_link_executable_coverage(self) -> None:
        """Keep simplified setup and role-exclusion scenarios tied to runnable evidence."""

        catalog = load_yaml_object(REPOSITORY_ROOT / "evals" / "agent-scenarios.yaml")
        configurator = next(entry for entry in catalog["agents"] if entry["id"] == "project-configurator")
        scenarios = {scenario["id"]: scenario for scenario in configurator["scenarios"]}
        required = {
            "project-configurator-basic-setup",
            "project-configurator-advanced-setup",
            "project-configurator-documentation-roots",
            "project-configurator-persisted-technology-confirmation",
            "project-configurator-conceptual-role-technology-exclusion",
            "project-configurator-dev-coder-provider-dependency-exclusion",
        }
        self.assertTrue(required.issubset(scenarios))
        for scenario_id in required:
            with self.subTest(scenario=scenario_id):
                self.assertEqual([], scenarios[scenario_id]["executableCases"])
                self.assertEqual("declared", scenarios[scenario_id]["coverageStatus"])

    def test_project_setup_skills_expose_reviewed_public_procedures(self) -> None:
        """Keep public setup procedures and execute their routing-output boundary."""

        detection_text = (
            SKILLS_ROOT / "detect-technology-skills" / "SKILL.md"
        ).read_text(encoding="utf-8")
        configuration_text = (
            SKILLS_ROOT / "create-project-configuration" / "SKILL.md"
        ).read_text(encoding="utf-8")

        self.assertIn("## Detect Technology Skills", detection_text)
        self.assertNotIn("## Workflow", detection_text)
        for heading in (
            "## Configure Project Agents And Skills",
            "## Render Project Guidance",
            "## Verify Project Configuration",
        ):
            with self.subTest(configuration_heading=heading):
                self.assertIn(heading, configuration_text)
        self.assertNotIn("## Workflow", configuration_text)
        self.assertNotIn("## Verification", configuration_text)

        probes = load_yaml_object(REPOSITORY_ROOT / "evals" / "skill-probes.yaml")
        probes_by_id = {probe["id"]: probe for probe in probes["probes"]}
        detection_probe = probes_by_id["probe-detect-technology-skills"]
        configuration_probe = probes_by_id["probe-create-project-configuration"]
        self.assertIn("Detect Technology Skills", detection_probe["expectedBehavior"])
        for procedure in (
            "Configure Project Agents And Skills",
            "Render Project Guidance",
            "Verify Project Configuration",
        ):
            with self.subTest(probe_procedure=procedure):
                self.assertIn(procedure, configuration_probe["expectedBehavior"])
        configurator_tests = load_python_module(
            AGENT_TEST_SUITES_ROOT / "project-configurator" / "test_fixtures.py",
            "project_configurator_fixture_contract",
        )
        bootstrapper_evaluator = load_python_module(
            AGENT_TEST_SUITES_ROOT / "project-bootstrapper" / "scripted_orchestration.py",
            "project_bootstrapper_routing_contract",
        )
        composed_routes = {
            "folder_routing": [
                {
                    "pattern": "service/**",
                    "required_skills": ["fastapi", "python"],
                },
            ]
        }
        aggregate_output = {
            "aggregate interface": {
                "selected-skill-set": ["python", "typescript"],
            }
        }
        confirmed_skills = {"fastapi", "python"}
        for evaluator in (
            configurator_tests._evaluate_technology_routing_output,
            bootstrapper_evaluator._evaluate_project_configuration_output,
        ):
            with self.subTest(evaluator=evaluator.__name__):
                self.assertEqual("PASS", evaluator(composed_routes, confirmed_skills))
                self.assertEqual("FAIL", evaluator(aggregate_output, confirmed_skills))
                for invalid_skills in (
                    [""],
                    [" "],
                    ["python", " python"],
                    ["python", "python"],
                    ["unknown-skill"],
                    ["selected-skill-set"],
                ):
                    invalid = {
                        "folder_routing": [
                            {
                                "pattern": "service/**",
                                "required_skills": invalid_skills,
                            }
                        ]
                    }
                    self.assertEqual(
                        "FAIL", evaluator(invalid, confirmed_skills)
                    )

    def test_project_configuration_documents_confirmation_reference_boundary(self) -> None:
        """Require an auditable reference without inventing one cross-project format."""

        skill_text = (
            SKILLS_ROOT / "create-project-configuration" / "SKILL.md"
        ).read_text(encoding="utf-8")
        template_text = (
            SKILLS_ROOT
            / "route-documentation-work"
            / "assets"
            / "templates"
            / "project-template.yaml"
        ).read_text(encoding="utf-8")
        for text in (skill_text, template_text):
            self.assertIn("non-empty auditable reference", text)
            self.assertIn("project-defined", text)

    def test_project_bootstrapper_owns_complete_setup_and_review_loop(self) -> None:
        build_skill_docs = load_build_skill_docs_module()
        skill_payload = build_skill_docs.build_payload()
        roles = build_skill_docs.load_role_definitions(set(skill_payload["skills"]))
        role = next(role for role in roles if role.name == "project-bootstrapper")

        self.assertNotIn("reverse-engineer-project-documentation", build_skill_docs.fixed_role_skills(role))
        self.assertNotIn("reverse-engineer-project-documentation", role.skill_conditions)
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
            "reverse-engineer-project-documentation",
            build_skill_docs.fixed_role_skills(role),
        )
        self.assertNotIn(
            "review-prompt-contracts",
            build_skill_docs.fixed_role_skills(role),
        )
        self.assertNotIn("reverse-engineer-project-documentation", role.skill_conditions)
        self.assertIn("review-prompt-contracts", role.skill_conditions)
        self.assertIn("model-facing evaluator", role.skill_conditions["review-prompt-contracts"])
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
                "review-architecture",
                "review-functional-spec",
                "review-high-level-design",
                "review-module-design",
                "review-unit-test-plan",
                "terminology-standard-review",
            } | set(CORE_PATTERN_SKILLS),
            set(role.skill_conditions),
        )
        self.assertNotIn("resource-claim", role.skill_conditions)

    def test_dev_skill_lint_reviewer_reports_only_critical_skill_issues(self) -> None:
        build_skill_docs = load_build_skill_docs_module()
        skill_payload = build_skill_docs.build_payload()
        roles = build_skill_docs.load_role_definitions(set(skill_payload["skills"]))
        role = next(role for role in roles if role.name == "dev-skill-lint-reviewer")

        self.assertEqual("intermediate", role.model_profile)
        self.assertEqual(
            {
                "skill-authoring",
                "review-structured-artifact",
            },
            set(build_skill_docs.fixed_role_skills(role))
            - {"effective-communication", "ste-technical-writing"},
        )
        self.assertEqual(set(), set(role.skill_conditions))
        self.assertNotIn("resource-claim", role.skill_conditions)
        self.assertIn("Report only critical skill issues", role.instructions)
        self.assertIn("Do not report minor grammar", role.instructions)
        self.assertIn("material STE clarity failure", role.instructions)
        self.assertIn("significant redundancy", role.instructions)
        self.assertIn("wrong harness boundary", role.instructions)
        self.assertIn("no-critical-findings result", role.output_contract)

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

    def test_backlog_management_catalog_group_preserves_conceptual_role_identity(self) -> None:
        build_skill_docs = load_build_skill_docs_module()
        skill_payload = build_skill_docs.build_payload()
        roles = build_skill_docs.load_role_definitions(set(skill_payload["skills"]))
        payload = build_skill_docs.build_role_payload(roles)

        self.assertEqual(
            [
                "dev-activities",
                "backlog-management",
                "wiki-activities",
                "project-setup",
                "methodology-maintenance",
            ],
            [group["id"] for group in payload["catalogGroups"]],
        )
        backlog_roles = {
            role["name"]
            for role in payload["roles"].values()
            if role["catalogGroup"] == "backlog-management"
        }
        self.assertEqual(
            {
                "dev-backlog-coordinator",
                "dev-backlog-steward",
                "dev-backlog-watchdog",
            },
            backlog_roles,
        )
        for role_name in backlog_roles:
            with self.subTest(role=role_name):
                role = payload["roles"][role_name]
                self.assertEqual("dev-activities", role["group"])
                self.assertEqual("Dev Activities", role["groupLabel"])
                self.assertEqual("Backlog Management", role["catalogGroupLabel"])
                self.assertEqual(
                    f"agents/roles/dev-activities/{role_name}.role.yaml",
                    role["sourcePath"],
                )
        self.assertEqual(
            "dev-activities",
            payload["roles"]["dev-orchestrator"]["catalogGroup"],
        )

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
                {"name": CODEX_HARNESS_SKILL_NAME, "enabled": True},
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
            {"simple", "coordination", "default", "documentation", "advanced", "advanced-long", "intermediate"},
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
                "coordination": "gpt-5.6-terra",
                "default": "gpt-5.6-terra",
                "documentation": "gpt-5.5",
                "advanced": "gpt-5.6-sol",
                "advanced-long": "gpt-5.6-sol",
                "intermediate": "gpt-5.6-luna",
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

    def test_documentation_design_system_roles_and_checklists_are_complete(self) -> None:
        """The bounded runner and coordinator must retain their distinct skill and evidence contracts."""
        build_skill_docs = load_build_skill_docs_module()
        skill_names = set(build_skill_docs.build_payload()["skills"])
        loaded_roles = {
            role.name: role
            for role in build_skill_docs.load_role_definitions(skill_names)
        }
        runner_source = load_yaml_object(
            ROLES_ROOT
            / "methodology-maintenance"
            / "methodology-design-system-checklist-runner.role.yaml"
        )
        coordinator_source = load_yaml_object(
            ROLES_ROOT
            / "methodology-maintenance"
            / "methodology-design-system-review-coordinator.role.yaml"
        )

        self.assertEqual(
            ["review-documentation-design-system"],
            [next(iter(entry)) for entry in runner_source["skills"]],
        )
        self.assertEqual([], coordinator_source["skills"])
        self.assertEqual(
            ["methodology-design-system-checklist-runner"],
            coordinator_source["agentDependencies"],
        )
        self.assertEqual("simple", loaded_roles[runner_source["name"]].model_profile)
        self.assertEqual(
            "coordination",
            loaded_roles[coordinator_source["name"]].model_profile,
        )

        for source, role_name in (
            (runner_source, runner_source["name"]),
            (coordinator_source, coordinator_source["name"]),
        ):
            with self.subTest(schema_role=role_name):
                metadata = [next(iter(entry.values())) for entry in source["outputContract"]]
                self.assertTrue(all(set(item) == {"purpose", "schema"} for item in metadata))
                output_schema = loaded_roles[role_name].output_schema
                self.assertEqual("object", output_schema["type"])
                self.assertFalse(output_schema["additionalProperties"])
                self.assertEqual(
                    [next(iter(entry)) for entry in source["outputContract"]],
                    output_schema["required"],
                )
                for adapter, suffix in (
                    ("codex", ".toml"),
                    ("claude", ".md"),
                    ("gemini", ".md"),
                    ("junie", ".md"),
                ):
                    adapter_text = (
                        GENERATED_ADAPTERS_ROOT
                        / adapter
                        / "agents"
                        / f"{role_name}{suffix}"
                    ).read_text(encoding="utf-8")
                    schema_text = (
                        tomllib.loads(adapter_text)["developer_instructions"]
                        if adapter == "codex"
                        else adapter_text
                    )
                    self.assertIn("Strict output JSON Schema:", schema_text)
                    self.assertIn('"additionalProperties": false', schema_text)

        for role_name in (runner_source["name"], coordinator_source["name"]):
            codex_payload = tomllib.loads(
                (
                    GENERATED_ADAPTERS_ROOT
                    / "codex"
                    / "agents"
                    / f"{role_name}.toml"
                ).read_text(encoding="utf-8")
            )
            self.assertEqual("read-only", codex_payload["sandbox_mode"])
            claude_text = (
                GENERATED_ADAPTERS_ROOT / "claude" / "agents" / f"{role_name}.md"
            ).read_text(encoding="utf-8")
            claude_frontmatter = yaml.safe_load(claude_text.split("---", 2)[1])
            self.assertEqual(["Read", "Grep", "Glob"], claude_frontmatter["tools"])
            for adapter in ("gemini", "junie"):
                text = (
                    GENERATED_ADAPTERS_ROOT / adapter / "agents" / f"{role_name}.md"
                ).read_text(encoding="utf-8")
                self.assertIn(
                    "does not prevent repository mutation for this role",
                    text,
                )

        references = sorted(
            (SKILLS_ROOT / "review-documentation-design-system" / "references").glob(
                "review-checklist-documentation-design-system-*.md"
            )
        )
        checklist_ids = [
            check_id
            for path in references
            for check_id in re.findall(r"\bDDS-[A-Z]{3}-\d{3}\b", path.read_text(encoding="utf-8"))
        ]
        self.assertEqual(11, len(references))
        self.assertEqual(91, len(checklist_ids))
        self.assertEqual(91, len(set(checklist_ids)))

    def test_role_output_json_schema_subset_fails_closed(self) -> None:
        """Reject incompatible, type-mismatched, or silently discarded schema content."""

        build_skill_docs = load_build_skill_docs_module()
        source_path = (
            ROLES_ROOT
            / "methodology-maintenance"
            / "methodology-design-system-review-coordinator.role.yaml"
        )
        valid = {
            "type": ["string", "null"],
            "enum": ["PASS", None],
            "minLength": 1,
            "default": None,
            "examples": ["PASS", None],
        }
        self.assertEqual(
            valid,
            build_skill_docs.validate_json_schema(valid, "output", source_path),
        )

        invalid_schemas = (
            {
                "type": "string",
                "properties": {"value": {"type": "string"}},
                "required": ["value"],
                "additionalProperties": False,
            },
            {"type": "array", "items": {"type": "string"}, "minLength": 1},
            {"type": "object", "items": {"type": "string"}},
            {"type": "string", "enum": [1]},
            {"type": "number", "default": "1"},
            {"type": "integer", "examples": [True]},
            {
                "type": "object",
                "properties": {"value": []},
                "required": ["value"],
                "additionalProperties": False,
            },
            {"type": "array", "items": []},
        )
        for schema in invalid_schemas:
            with self.subTest(schema=schema), self.assertRaises(ValueError):
                build_skill_docs.validate_json_schema(schema, "output", source_path)

    def test_context_budget_percent_defaults_overrides_and_validation(self) -> None:
        build_skill_docs = load_build_skill_docs_module()
        skill_names = set(build_skill_docs.build_payload()["skills"])
        required, allowed, groups = build_skill_docs.load_role_schema()
        model_profiles = set(build_skill_docs.load_model_profiles())
        source_path = ROLES_ROOT / "dev-activities" / "dev-coder.role.yaml"
        source_role = load_yaml_object(source_path)

        self.assertNotIn("contextBudgetPercent", required)
        self.assertEqual(
            "percentage-integer",
            load_yaml_object(ROLE_SCHEMA_PATH)["properties"]["contextBudgetPercent"],
        )
        self.assertEqual(
            75,
            load_yaml_object(ROLE_SCHEMA_PATH)["defaults"]["contextBudgetPercent"],
        )
        self.assertEqual(75, build_skill_docs.load_default_context_budget_percent())
        context_budget_overrides = {
            "dev-backlog-coordinator": 35,
            "dev-backlog-watchdog": 50,
            "dev-documentation-writer": 50,
        }
        loaded_role_list = build_skill_docs.load_role_definitions(skill_names)
        loaded_roles = {role.name: role for role in loaded_role_list}
        generated_role_data = build_skill_docs.build_role_payload(loaded_role_list)[
            "roles"
        ]
        for role_path in sorted(ROLES_ROOT.glob("*/*.role.yaml")):
            with self.subTest(role=role_path.stem):
                role = load_yaml_object(role_path)
                expected_percent = context_budget_overrides.get(role["name"], 75)
                self.assertEqual(
                    role["name"] in context_budget_overrides,
                    "contextBudgetPercent" in role,
                )
                self.assertEqual(
                    expected_percent,
                    role.get("contextBudgetPercent", 75),
                )
                self.assertEqual(
                    expected_percent,
                    loaded_roles[role["name"]].context_budget_percent,
                )
                self.assertEqual(
                    expected_percent,
                    generated_role_data[role["name"]]["contextBudgetPercent"],
                )

        invalid_values = (None, 75.5, 0, -1, 101, True)
        for invalid_value in invalid_values:
            with self.subTest(invalid_value=invalid_value), tempfile.TemporaryDirectory() as directory:
                invalid_role = dict(source_role)
                invalid_role["contextBudgetPercent"] = invalid_value
                path = Path(directory) / "dev-activities" / source_path.name
                path.parent.mkdir()
                path.write_text(yaml.safe_dump(invalid_role, sort_keys=False), encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "contextBudgetPercent"):
                    build_skill_docs.load_role_definition(
                        path,
                        required,
                        allowed,
                        groups,
                        skill_names,
                        model_profiles,
                        default_context_budget_percent=75,
                    )

    def test_adapter_context_budget_metadata_is_complete_and_validated(self) -> None:
        build_skill_docs = load_build_skill_docs_module()
        profile_ids = set(build_skill_docs.load_model_profiles())
        expected_capacities = {
            "codex": {1_050_000},
            "claude": {1_000_000},
            "gemini": {1_048_576},
            "junie": {1_000_000, 1_048_576, 1_050_000},
        }

        for adapter, capacities in expected_capacities.items():
            with self.subTest(adapter=adapter):
                source = load_yaml_object(ADAPTER_MODEL_PROFILE_PATHS[adapter])
                self.assertEqual(2, source["version"])
                profiles = build_skill_docs.load_adapter_model_profiles(adapter, profile_ids)
                self.assertEqual(capacities, {profile.context_capacity_tokens for profile in profiles.values()})
                for profile in profiles.values():
                    self.assertEqual("instruction", profile.context_budget_mechanism)
                    self.assertTrue(profile.context_capacity_evidence)
                    self.assertTrue(
                        all(
                            evidence.startswith("https://")
                            for evidence in profile.context_capacity_evidence
                        )
                    )
                    self.assertTrue(profile.context_budget_mechanism_evidence.startswith("https://"))

        valid_payload = load_yaml_object(ADAPTER_MODEL_PROFILE_PATHS["codex"])
        invalid_payloads = []
        for field_name in ("contextCapacityTokens", "contextBudgetMechanism"):
            payload = json.loads(json.dumps(valid_payload))
            payload["profiles"]["simple"].pop(field_name)
            invalid_payloads.append((payload, field_name))
        payload = json.loads(json.dumps(valid_payload))
        payload["profiles"]["simple"]["contextBudgetMechanism"] = "unsupported"
        invalid_payloads.append((payload, "unsupported context budget mechanism"))
        for field_name, expected_error in (
            (
                "contextCapacityEvidence",
                "contextCapacityEvidence must be a non-empty list of HTTPS URLs",
            ),
            (
                "contextBudgetMechanismEvidence",
                "contextBudgetMechanismEvidence must be an HTTPS URL",
            ),
        ):
            payload = json.loads(json.dumps(valid_payload))
            payload["profiles"]["simple"].pop(field_name)
            invalid_payloads.append((payload, expected_error))
        for invalid_evidence in ([], ["http://example.com/model"]):
            payload = json.loads(json.dumps(valid_payload))
            payload["profiles"]["simple"]["contextCapacityEvidence"] = invalid_evidence
            invalid_payloads.append(
                (
                    payload,
                    "contextCapacityEvidence must be a non-empty list of HTTPS URLs",
                )
            )
        for invalid_evidence in ("", "http://example.com/subagents"):
            payload = json.loads(json.dumps(valid_payload))
            payload["profiles"]["simple"][
                "contextBudgetMechanismEvidence"
            ] = invalid_evidence
            invalid_payloads.append(
                (payload, "contextBudgetMechanismEvidence must be an HTTPS URL")
            )

        for payload, expected_error in invalid_payloads:
            with self.subTest(expected_error=expected_error), patch.object(
                build_skill_docs,
                "read_yaml_object",
                return_value=payload,
            ):
                with self.assertRaisesRegex(ValueError, expected_error):
                    build_skill_docs.load_adapter_model_profiles("codex", profile_ids)

    def test_context_budget_derivation_rounds_down_and_rejects_overflow(self) -> None:
        build_skill_docs = load_build_skill_docs_module()

        self.assertEqual(786_432, build_skill_docs.derive_context_budget(1_048_576, 75))
        self.assertEqual(1, build_skill_docs.derive_context_budget(101, 1))
        with self.assertRaisesRegex(ValueError, "exceeds model context capacity"):
            build_skill_docs.derive_context_budget(1_000_000, 101)

    def test_all_adapters_generate_context_instructions_and_stage_results(self) -> None:
        build_skill_docs = load_build_skill_docs_module()
        skill_names = set(build_skill_docs.build_payload()["skills"])
        roles = build_skill_docs.load_role_definitions(skill_names)
        role = next(role for role in roles if role.name == "dev-code-reviewer")
        profile_ids = set(build_skill_docs.load_model_profiles())
        outputs = build_skill_docs.expected_role_outputs(roles)
        manifest = json.loads(
            build_skill_docs.render_agent_generation_manifest(roles, outputs, False)
        )
        expected_profile_budgets = {
            "codex": {
                profile_id: 787_500
                for profile_id in profile_ids
            },
            "claude": {
                profile_id: 750_000
                for profile_id in profile_ids
            },
            "gemini": {
                profile_id: 786_432
                for profile_id in profile_ids
            },
            "junie": {
                "simple": 786_432,
                "coordination": 750_000,
                "default": 750_000,
                "documentation": 787_500,
                "advanced": 750_000,
                "advanced-long": 750_000,
                "intermediate": 750_000,
            },
        }

        for adapter in ("codex", "claude", "gemini", "junie"):
            profiles = build_skill_docs.load_adapter_model_profiles(adapter, profile_ids)
            self.assertEqual(
                expected_profile_budgets[adapter],
                {
                    profile_id: build_skill_docs.resolve_context_budget(
                        profile_id,
                        75,
                        profiles,
                    )["contextBudgetTokens"]
                    for profile_id in profile_ids
                },
            )
            expected_primary = build_skill_docs.resolve_context_budget(
                role.model_profile,
                role.context_budget_percent,
                profiles,
            )
            expected_instruction = build_skill_docs.context_budget_instruction(
                role,
                profiles,
            )
            renderer = getattr(build_skill_docs, f"render_{adapter}_agent")
            rendered = renderer(role, profiles)
            with self.subTest(adapter=adapter):
                self.assertIn(expected_instruction, rendered)
                agent_manifest = next(
                    agent
                    for agent in manifest["adapters"][adapter]["agents"]
                    if agent["name"] == role.name
                )
                allocation = agent_manifest["contextAllocation"]
                self.assertEqual(75, allocation["contextBudgetPercent"])
                self.assertEqual(expected_primary, allocation["primary"])
                self.assertEqual(
                    set(role.model_stages),
                    set(allocation["modelStages"]),
                )
                for stage, profile_id in role.model_stages.items():
                    self.assertEqual(
                        build_skill_docs.resolve_context_budget(
                            profile_id,
                            role.context_budget_percent,
                            profiles,
                        ),
                        allocation["modelStages"][stage],
                    )

                for role_name, expected_percent in (
                    ("dev-backlog-coordinator", 35),
                    ("dev-backlog-watchdog", 50),
                    ("dev-documentation-writer", 50),
                ):
                    override_role = next(
                        candidate
                        for candidate in roles
                        if candidate.name == role_name
                    )
                    override_manifest = next(
                        agent
                        for agent in manifest["adapters"][adapter]["agents"]
                        if agent["name"] == role_name
                    )
                    self.assertEqual(
                        expected_percent,
                        override_manifest["contextAllocation"]["contextBudgetPercent"],
                    )
                    self.assertEqual(
                        build_skill_docs.resolve_context_budget(
                            override_role.model_profile,
                            expected_percent,
                            profiles,
                        ),
                        override_manifest["contextAllocation"]["primary"],
                    )

    def test_context_budget_changes_preserve_unrelated_generated_fields(self) -> None:
        build_skill_docs = load_build_skill_docs_module()
        skill_names = set(build_skill_docs.build_payload()["skills"])
        role = next(
            role
            for role in build_skill_docs.load_role_definitions(skill_names)
            if role.name == "dev-coder"
        )
        profile_ids = set(build_skill_docs.load_model_profiles())

        def without_context_instruction(
            rendered: str,
            context_instruction: str,
        ) -> str:
            return rendered.replace(context_instruction + "\n\n", "", 1)

        for adapter in ("codex", "claude", "gemini", "junie"):
            profiles = build_skill_docs.load_adapter_model_profiles(adapter, profile_ids)
            renderer = getattr(build_skill_docs, f"render_{adapter}_agent")
            changed_role = replace(role, context_budget_percent=74)
            original = renderer(role, profiles)
            changed = renderer(changed_role, profiles)
            with self.subTest(adapter=adapter, change="percentage"):
                self.assertNotEqual(original, changed)
                self.assertEqual(
                    without_context_instruction(
                        original,
                        build_skill_docs.context_budget_instruction(role, profiles),
                    ),
                    without_context_instruction(
                        changed,
                        build_skill_docs.context_budget_instruction(changed_role, profiles),
                    ),
                )

            changed_profiles = dict(profiles)
            original_profile = changed_profiles[role.model_profile]
            changed_profiles[role.model_profile] = replace(
                original_profile,
                context_capacity_tokens=original_profile.context_capacity_tokens - 1,
            )
            capacity_changed = renderer(role, changed_profiles)
            with self.subTest(adapter=adapter, change="capacity"):
                self.assertNotEqual(original, capacity_changed)
                self.assertEqual(75, role.context_budget_percent)
                self.assertEqual(
                    without_context_instruction(
                        original,
                        build_skill_docs.context_budget_instruction(role, profiles),
                    ),
                    without_context_instruction(
                        capacity_changed,
                        build_skill_docs.context_budget_instruction(role, changed_profiles),
                    ),
                )

    def test_context_budget_ownership_and_runtime_evidence_are_documented(self) -> None:
        readme = README_PATH.read_text(encoding="utf-8")
        source_design = (
            REPOSITORY_ROOT / "design" / "generic-agent-definitions-source.html"
        ).read_text(encoding="utf-8")
        catalog_design = (
            REPOSITORY_ROOT / "design" / "agent-and-skill-definitions.html"
        ).read_text(encoding="utf-8")

        for expected in (
            "contextBudgetPercent",
            "defaults.contextBudgetPercent",
            "sets it to 75",
            "explicit override",
            "floor(contextCapacityTokens * contextBudgetPercent / 100)",
            "zero additional token reserve",
            "agent-generation-manifest.json",
        ):
            with self.subTest(readme_contract=expected):
                self.assertIn(expected, readme)
        for expected in (
            "schema default of 75",
            "explicit role value before the default",
            "resolved effective percentage",
            "contextCapacityTokens",
            "contextBudgetMechanism",
            "Codex CLI 0.144.1",
            "Claude Code 2.1.104",
            "Gemini CLI 0.39.1",
            "dated 05 August 2026",
            "separately dated July 2026 subagent page",
            "https://developers.openai.com/codex/subagents",
            "https://code.claude.com/docs/en/sub-agents",
            "https://geminicli.com/docs/core/subagents/",
            "https://junie.jetbrains.com/docs/junie-cli-subagents.html",
        ):
            with self.subTest(design_contract=expected):
                self.assertIn(expected, source_design)
        self.assertNotIn("installed wrapper", source_design)
        self.assertIn("Context budget", catalog_design)
        self.assertIn("schema-owned default", catalog_design)
        self.assertIn("role.contextBudgetPercent", catalog_design)

    def test_dev_documentation_writer_uses_dedicated_model_profile(self) -> None:
        build_skill_docs = load_build_skill_docs_module()
        skill_names = set(build_skill_docs.build_payload()["skills"])
        roles = build_skill_docs.load_role_definitions(skill_names)
        writer = next(role for role in roles if role.name == "dev-documentation-writer")
        source_profile_ids = set(build_skill_docs.load_model_profiles())

        self.assertEqual("documentation", writer.model_profile)
        self.assertEqual(
            {
                "dev-artifact-reviewer",
                "dev-document-topic-editor",
                "dev-documentation-writer",
                "wiki-architect",
                "wiki-ingester",
                "wiki-researcher",
                "wiki-source-collector",
                "wiki-writer",
            },
            {
                role.name
                for role in roles
                if role.model_profile == "documentation"
            },
        )

        expected_profiles = {
            "codex": {
                "simple": ("gpt-5.6-luna", "medium"),
                "coordination": ("gpt-5.6-terra", "low"),
                "default": ("gpt-5.6-terra", "medium"),
                "documentation": ("gpt-5.5", "high"),
                "advanced": ("gpt-5.6-sol", "high"),
                "advanced-long": ("gpt-5.6-sol", "high"),
                "intermediate": ("gpt-5.6-luna", "high"),
            },
            "claude": {
                "simple": ("fable-5", None),
                "coordination": ("sonnet-5", None),
                "default": ("sonnet-5", None),
                "documentation": ("fable-5", None),
                "advanced": ("opus-4.8", None),
                "advanced-long": ("opus-4.8", None),
                "intermediate": ("opus-4.8", None),
            },
            "gemini": {
                "simple": ("flash", None),
                "coordination": ("auto", None),
                "default": ("auto", None),
                "documentation": ("auto", None),
                "advanced": ("pro", None),
                "advanced-long": ("pro", None),
                "intermediate": ("pro", None),
            },
            "junie": {
                "simple": ("gemini-flash", "low"),
                "coordination": ("sonnet", "medium"),
                "default": ("sonnet", "medium"),
                "documentation": ("gpt-5.6-sol", "high"),
                "advanced": ("opus", "high"),
                "advanced-long": ("opus", "high"),
                "intermediate": ("opus", "high"),
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
        self.assertIn('model = "gpt-5.5"', codex_text)
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
        code_implementation_cases = [
            case
            for case in by_id.values()
            if case.get("requiredAgents") == ["dev-coder"]
        ]
        for case in code_implementation_cases:
            with self.subTest(code_comments_case=case["id"]):
                self.assertIn("code-comments", case["requiredSkills"])

        delivery_case = by_id["main-branch-unrelated-dirty-contract"]
        self.assertEqual(["dev-orchestrator"], delivery_case["requiredAgents"])
        self.assertEqual(
            {
                "manage-work-items",
                "structured-design",
                "structured-explanation",
                "deliver-work-item",
                "deliver-work-item-main-branch",
                "resource-claim",
            },
            set(delivery_case["requiredSkills"]),
        )
        self.assertNotIn("code-comments", delivery_case["requiredSkills"])

        review_case = by_id["typescript-code-review"]
        self.assertTrue(review_case["expectVerifyFailure"])
        self.assertIn("code-comments", review_case["requiredSkills"])
        self.assertIn("review-code-with-evidence", review_case["requiredSkills"])
        self.assertEqual(3, len(review_case["requiredFindings"]))

        file_boundary_case = by_id["file-work-item-no-mutation"]
        self.assertEqual(
            ["dev-backlog-steward-provider-boundary"],
            file_boundary_case["agentScenarios"],
        )
        self.assertEqual([], file_boundary_case["fixtureBackedProbeClaims"])
        self.assertEqual(["eval-result.md"], file_boundary_case["allowedWritePaths"])
        self.assertEqual(
            {
                "manage-work-items",
                "create-work-item-file",
                "manage-work-items-file",
            },
            set(file_boundary_case["requiredSkills"]) - {"structured-explanation"},
        )

        probes = load_yaml_object(REPOSITORY_ROOT / "evals" / "skill-probes.yaml")
        probes_by_id = {probe["id"]: probe for probe in probes["probes"]}
        self.assertEqual(
            "fixture-backed",
            probes_by_id["probe-create-work-item-file"]["coverageStatus"],
        )
        self.assertEqual(
            ["file-work-item-template-contract"],
            probes_by_id["probe-create-work-item-file"]["executableCases"],
        )
        self.assertEqual(
            ["backlog-lifecycle", "work-item-management-provider-operations"],
            probes_by_id["probe-manage-work-items-file"]["executableCases"],
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
            "dev-backlog-watchdog",
            "dev-document-topic-editor",
            "dev-skill-lint-reviewer",
            "methodology-design-system-checklist-runner",
            "methodology-design-system-review-coordinator",
        ]
        suite_entries = index["suites"]
        self.assertEqual(expected_suites, [entry["id"] for entry in suite_entries])
        self.assertEqual(list(range(1, 33)), [entry["priority"] for entry in suite_entries])
        suite_directories = {
            path.name
            for path in AGENT_TEST_SUITES_ROOT.iterdir()
            if path.is_dir()
            and (path / "suite.yaml").is_file()
            and path.name not in {"results", "skills"}
            and not path.name.startswith("__")
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
            scenario_statuses = {
                scenario["status"] for scenario in scenarios["scenarios"]
            }
            declared_only = scenario_statuses == {"declared"}

            with self.subTest(suite=entry["id"]):
                self.assertEqual(entry["id"], suite["id"])
                self.assertEqual(entry["id"], role["filename"])
                self.assertTrue((REPOSITORY_ROOT / target["nativeAgent"]).is_file())
                self.assertEqual(1, suite["execution"]["maximumActiveChildren"])
                self.assertTrue(suite["execution"]["requireCodexIdentityEvidence"])
                self.assertEqual(
                    {"supervisor", "judge"},
                    set(suite["projectAgents"]),
                )
                if entry["id"] == "dev-backlog-coordinator":
                    self.assertEqual(
                        ["dev-orchestrator", "dev-backlog-steward"],
                        target["allowedAgentDependencies"],
                    )
                    self.assertEqual(
                        ["dev-backlog-watchdog"],
                        [
                            dependency
                            for dependency in role.get("agentDependencies", [])
                            if dependency not in target["allowedAgentDependencies"]
                        ],
                    )
                else:
                    self.assertEqual(
                        role.get("agentDependencies", []),
                        target["allowedAgentDependencies"],
                    )
                self.assertEqual(entry["id"], scenarios["suite"])
                if declared_only:
                    self.assertEqual(1, len(scenarios["scenarios"]))
                elif entry["id"] == "dev-code-reviewer":
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
                    self.assertEqual(8, len(scenarios["scenarios"]))
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
                elif entry["id"] == "wiki-writer":
                    self.assertEqual(4, len(scenarios["scenarios"]))
                    self.assertEqual(
                        {
                            "durable-topic-creation",
                            "code-aware-maintenance",
                            "insufficient-sources",
                            "verifier-interruption",
                        },
                        {
                            scenario["id"]
                            for scenario in scenarios["scenarios"]
                        },
                    )
                elif entry["id"] == "dev-backlog-coordinator":
                    self.assertEqual(9, len(scenarios["scenarios"]))
                elif entry["id"] == "dev-backlog-watchdog":
                    self.assertEqual(14, len(scenarios["scenarios"]))
                elif entry["id"] == "dev-orchestrator":
                    self.assertEqual(5, len(scenarios["scenarios"]))
                else:
                    self.assertEqual(3, len(scenarios["scenarios"]))

            for scenario in scenarios["scenarios"]:
                executable_case = scenario.get("executableCase")
                with self.subTest(
                    suite=entry["id"],
                    executable_scenario=scenario["id"],
                ):
                    if declared_only:
                        self.assertEqual("declared", scenario["status"])
                        self.assertIsNone(executable_case)
                    else:
                        self.assertIn(
                            scenario["status"],
                            {"executable", "fixture-backed"},
                        )
                        self.assertIsInstance(executable_case, str)
                        self.assertTrue(
                            (suite_root / executable_case).exists()
                            or executable_case in legacy_case_ids
                        )

            project_agents = () if declared_only else suite["projectAgents"].items()
            for agent_kind, relative_path in project_agents:
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

    def test_watchdog_suite_disables_nested_agents_without_dependencies(self) -> None:
        """A read-only Watchdog target cannot reserve an unusable child-agent slot."""

        suite_root = AGENT_TEST_SUITES_ROOT / "dev-backlog-watchdog"
        suite = load_yaml_object(suite_root / "suite.yaml")
        role = load_yaml_object(
            REPOSITORY_ROOT / suite["target"]["conceptualRole"]
        )
        supervisor = tomllib.loads(
            (suite_root / suite["projectAgents"]["supervisor"]).read_text(
                encoding="utf-8"
            )
        )

        self.assertEqual([], suite["target"]["allowedAgentDependencies"])
        self.assertEqual([], role.get("agentDependencies", []))
        self.assertEqual(0, suite["execution"]["nestedAgentLimit"])
        self.assertIn(
            "permit no child agents",
            supervisor["developer_instructions"],
        )

    def test_coordinator_happy_scenario_counts_starting_plus_running_capacity(
        self,
    ) -> None:
        """The Coordinator scenario must use the same active-capacity contract."""

        catalog = load_yaml_object(
            REPOSITORY_ROOT / "evals" / "agent-scenarios.yaml"
        )
        coordinator = next(
            entry
            for entry in catalog["agents"]
            if entry["id"] == "dev-backlog-coordinator"
        )
        scenario = next(
            entry
            for entry in coordinator["scenarios"]
            if entry["id"] == "dev-backlog-coordinator-happy"
        )

        self.assertIn(
            "restore ten Starting or Running work items",
            scenario["promptIntent"],
        )
        self.assertIn(
            "Ten provider-backed Starting or Running items",
            scenario["expectedOutcome"],
        )
        for clause in (
            "Count only lifecycle STARTING and RUNNING items returned by the "
            "effective Persistence-selected management skill.",
            "Use one canonical Dev Orchestrator execution for each Starting or "
            "Running work item.",
            "Recount and refill Starting-plus-Running capacity toward ten "
            "after every terminal cleanup.",
        ):
            with self.subTest(required_behavior=clause):
                self.assertIn(clause, scenario["requiredBehaviors"])
        self.assertIn(
            "Count Stalled, Blocked, User Action Required, Holding, Awaiting "
            "Review, terminal items, or pure waiting tasks as "
            "Starting-plus-Running capacity.",
            scenario["forbiddenBehaviors"],
        )
        self.assertNotIn(
            "Count only lifecycle RUNNING items returned by the effective "
            "Persistence-selected management skill.",
            scenario["requiredBehaviors"],
        )

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

        declared_skills = {
            str(probe["skill"])
            for probe in load_yaml_object(
                REPOSITORY_ROOT / "evals" / "skill-probes.yaml"
            )["probes"]
        }
        for skill_path in skill_paths:
            skill_name = load_yaml_object_from_frontmatter(skill_path)["name"]
            with self.subTest(skill=skill_name):
                declaration = "[x]" if skill_name in declared_skills else "[ ]"
                self.assertIn(
                    f"| {skill_name} | [x] | {declaration} ",
                    skill_section,
                )


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
        maintenance_skill_text = REPOSITORY_MAINTENANCE_SKILL_PATH.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "AGENTS.md references the repository-local maintenance skill at "
            ".agents/skills/dev-methodology-repository-maintenance/SKILL.md.",
            readme_text,
        )
        self.assertIn("- dev-methodology-repository-maintenance", agents_text)
        for phrase in REPOSITORY_MAINTENANCE_REQUIRED_PHRASES:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, maintenance_skill_text)
                self.assertNotIn(phrase, agents_text)

    def test_revise_document_topics_preserves_honest_scores(self) -> None:
        skill_text = REVISE_DOCUMENT_TOPICS_SKILL_PATH.read_text(encoding="utf-8")
        normalized_skill_text = " ".join(skill_text.split())
        skill_metadata = load_yaml_object_from_frontmatter(
            REVISE_DOCUMENT_TOPICS_SKILL_PATH
        )

        self.assertEqual("revise-document-topics", skill_metadata["name"])
        self.assertIn("without gaming alignment scores", skill_metadata["description"])

        for phrase in (
            "[Analyze Document Topics](../analyze-document-topics/SKILL.md)",
            "Prefer a more truthful structure over a higher percentage.",
            "Recalculate the moved topic and every sibling whose predecessor changes.",
            "Reject a reorder that merely transfers a partial score",
            "a one-child parent created only to remove a sequence score",
            "Move the explanation, not merely its outline label.",
            "Keep a partial sequence score",
            "probable wrong-document topics",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, normalized_skill_text)

    def test_analyze_document_topics_justifications_are_source_grounded(self) -> None:
        skill_text = ANALYZE_DOCUMENT_TOPICS_SKILL_PATH.read_text(encoding="utf-8")
        skill_metadata = load_yaml_object_from_frontmatter(
            ANALYZE_DOCUMENT_TOPICS_SKILL_PATH
        )

        self.assertEqual("analyze-document-topics", skill_metadata["name"])
        for phrase in (
            "Treat every why clause as an evidence claim",
            "the source blocks represented by those topics",
            "Do not introduce an unstated purpose, outcome, chronology, dependency,",
            "Confirm that the current topic clearly enunciates every constituent",
            "The why must explain the topic that",
            "is actually written, not a broader",
            "prefer the narrowest source-supported transition",
            "reject a why clause that is not entailed",
            "every topic and why clause describe the same scope",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, skill_text)

    def test_development_methodology_guides_skill_rename_cleanup(self) -> None:
        skill_text = (
            SKILLS_ROOT / "route-documentation-work" / "SKILL.md"
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
            "Core Skill Categories and Ownership",
            "Skill Lifecycle and Runtime Delivery",
            "Technology Extension Skill Catalog",
            "Skill Selection Ownership and Technology Boundaries",
            "Skill Instruction Delivery and Inlining",
            "Technology Extension Configuration Process",
            "Setup-Time Technology Detection",
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
        wiki_context_text = page_text["wiki-skills-and-project-context.html"]
        self.assertEqual(
            1,
            wiki_context_text.count(
                '<h1 id="page-title">Wiki Skills And Project Context</h1>'
            ),
        )
        wiki_context_h2_order = tuple(
            re.findall(r"<h2[^>]*>([^<]+)</h2>", wiki_context_text)
        )
        self.assertEqual(
            DOCUMENT_INFORMATION_OWNERS["wiki-skills-and-project-context.html"][1:],
            wiki_context_h2_order,
        )

        wiki_context_section_topics = {
            "flow-title": (
                "Raw evidence producers",
                "Wiki Ingester",
                "Independent acceptance",
            ),
            "roles-title": (
                "Wiki Architect",
                "Wiki Source Collector",
                "Wiki Researcher",
                "Wiki Ingester",
                "Wiki Writer",
                "Wiki Topic Verifier",
                "Wiki Query Responder",
                "Wiki Artifact Reviewer",
            ),
            "federation-title": (
                "Upstream entity ownership",
                "Downstream project context",
                "Shared and conflicting coverage",
                "Source and feed routing",
            ),
            "verification-title": (
                "Raw ingest before movement",
                "Processed links after movement",
                "Direct page maintenance",
                "Methodology artifacts",
            ),
        }
        for section_id, expected_h3_topics in wiki_context_section_topics.items():
            with self.subTest(wiki_context_section=section_id):
                section = wiki_context_text.split(
                    f'<section class="section" aria-labelledby="{section_id}">',
                    maxsplit=1,
                )[1].split("</section>", maxsplit=1)[0]
                actual_h3_topics = tuple(
                    re.sub(r"<[^>]+>", "", heading).strip()
                    for heading in re.findall(
                        r"<h3[^>]*>(.*?)</h3>",
                        section,
                        flags=re.DOTALL,
                    )
                )
                self.assertEqual(expected_h3_topics, actual_h3_topics)

        for source_derived_contract in (
            "whole-project reverse-engineering audit mode",
            "mutation-capable direct use saves a raw query fragment only if mutation is allowed",
            "Only GOOD authorizes moving the source to raw/processed",
            "becomes an open question about routing",
        ):
            with self.subTest(source_derived_contract=source_derived_contract):
                self.assertEqual(
                    1,
                    wiki_context_text.count(source_derived_contract),
                )

        wiki_context_hrefs = set(
            re.findall(
                r'href="([^"]+)"',
                wiki_context_text,
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
        for filename in DOCUMENT_NAVIGATION_ORDER:
            with self.subTest(index_link=filename):
                self.assertIn(f'href="design/{filename}"', index_text)
        expected_index_owners = (
            "catalog",
            "evaluations",
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
        self.assertEqual(DOCUMENT_NAVIGATION_ORDER, index_pages)

        for position, filename in enumerate(index_pages):
            text = (design_root / filename).read_text(encoding="utf-8")
            with self.subTest(document_navigation=filename):
                self.assertEqual(
                    1,
                    text.count(
                        '<nav class="document-nav" '
                        'aria-label="Documentation navigation">'
                    ),
                )
                self.assertIn(
                    '<a class="site-brand" href="../index.html">',
                    text,
                )
                self.assertIn(
                    "<span>AI-Assisted Coding Toolkit Index</span>",
                    text,
                )
                self.assertNotIn("Back to Documentation Index", text)
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
                expected_sequence_link_count = int(position > 0) + int(
                    position < len(index_pages) - 1
                )
                self.assertEqual(
                    expected_sequence_link_count,
                    sequence.count("<a "),
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
        self.assertIn("<h3>Agent Skill Architecture</h3>", index_text)

        expected_gradient = (
            "linear-gradient(180deg, rgba(232, 240, 255, 0.9), "
            "rgba(246, 248, 251, 0) 340px)"
        )

        def css_rule_declarations(text: str, selector: str) -> dict[str, str]:
            rule_match = re.search(
                rf"{re.escape(selector)}\s*\{{(?P<body>[^}}]*)\}}",
                text,
            )
            self.assertIsNotNone(rule_match, f"Missing CSS rule for {selector}")
            assert rule_match is not None
            return {
                name.strip(): value.strip()
                for declaration in rule_match.group("body").split(";")
                if ":" in declaration
                for name, value in (declaration.split(":", maxsplit=1),)
            }

        html_pages = {"index.html": index_text, **page_text}
        for filename, text in html_pages.items():
            with self.subTest(site_chrome=filename):
                self.assertEqual(1, text.count('<header class="site-header">'))
                self.assertEqual(1, text.count('<footer class="site-footer">'))
                self.assertIn("AI-Assisted Coding Toolkit", text)
                self.assertEqual(1, text.count(expected_gradient))
                if filename == "index.html":
                    self.assertIn(
                        '<a class="site-brand" href="index.html">',
                        text,
                    )
                    self.assertIn('src="logo.png"', text)
                    self.assertIn('href="LICENSE">MIT License</a>', text)
                else:
                    self.assertIn('src="../logo.png"', text)
                    self.assertIn('href="../LICENSE">MIT License</a>', text)

        settings_consumer_text = {}
        for page_path in sorted(design_root.glob("*.html")):
            text = page_path.read_text(encoding="utf-8")
            if '<script src="documentation-settings.js"></script>' in text:
                settings_consumer_text[page_path.name] = text
        self.assertFalse(
            set(DOCUMENT_NAVIGATION_ORDER) - settings_consumer_text.keys()
        )
        settings_site_chrome_pages = {
            "index.html": index_text,
            **settings_consumer_text,
        }
        for filename, text in settings_site_chrome_pages.items():
            with self.subTest(settings_site_chrome=filename):
                site_header = css_rule_declarations(text, ".site-header")
                self.assertEqual("flex", site_header.get("display"))
                self.assertEqual("center", site_header.get("align-items"))
                self.assertTrue(site_header.get("gap"))

                site_brand = css_rule_declarations(text, ".site-brand")
                self.assertEqual("inline-flex", site_brand.get("display"))
                self.assertEqual("0", site_brand.get("min-width"))

        license_text = (REPOSITORY_ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("MIT License", license_text)
        self.assertIn(
            "Copyright (c) 2026 Martin.Bechard@DevConsult.ca",
            license_text,
        )
        self.assertNotIn('class="summary"', index_text)
        self.assertNotIn('class="pill"', index_text)
        index_indicators = tuple(
            re.findall(
                r'<span class="icon" aria-hidden="true">(\d{2})</span>',
                index_text,
            )
        )
        self.assertEqual(
            tuple(f"{position:02d}" for position in range(1, len(index_pages) + 1)),
            index_indicators,
        )
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
            ".documentation-settings {\n      margin-left: auto;",
            'const header = document.querySelector(".site-header");',
            "header.appendChild(container);",
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

    def test_work_item_delivery_responsibilities_expose_multi_item_rules_as_lists(
        self,
    ) -> None:
        page_text = (
            REPOSITORY_ROOT / "design" / "agent-and-skill-definitions.html"
        ).read_text(encoding="utf-8")
        delivery_responsibilities = page_text.split(
            '<section class="section" aria-labelledby="delivery-responsibilities-title">',
            maxsplit=1,
        )[1].split("</section>", maxsplit=1)[0]

        def tag_containers(section: str, tag: str) -> list[str]:
            return re.findall(
                rf"<{tag}(?:\s[^>]*)?>.*?</{tag}>",
                section,
                flags=re.DOTALL,
            )

        def list_item_texts(container: str, expected_count: int) -> list[str]:
            fragments = re.findall(
                r"<li(?:\s[^>]*)?>.*?</li>",
                container,
                flags=re.DOTALL,
            )
            self.assertEqual(expected_count, len(fragments))
            items = [visible_prose_from_html(fragment) for fragment in fragments]
            self.assertTrue(all(len(item) == 1 and item[0] for item in items))
            return [item[0] for item in items]

        def paragraph_texts(section: str) -> list[str]:
            fragments = re.findall(
                r"<p(?:\s[^>]*)?>.*?</p>",
                section,
                flags=re.DOTALL,
            )
            self.assertGreater(len(fragments), 0)
            paragraphs = [visible_prose_from_html(fragment) for fragment in fragments]
            self.assertTrue(
                all(len(paragraph) == 1 and paragraph[0] for paragraph in paragraphs)
            )
            return [paragraph[0] for paragraph in paragraphs]

        def assert_catalog_structure(catalog: str) -> None:
            for heading in (
                "Delivery Workflow",
                "Persistence Selection",
                "Work-Item Coordination",
            ):
                self.assertIn(f"<h3>{heading}</h3>", catalog)

            self.assertNotIn(
                "Dev Coder returns a clean verified candidate commit without applying terminal delivery. Dev Orchestrator obtains",
                catalog,
            )

            delivery_section = catalog.split(
                "<h3>Delivery Workflow</h3>",
                maxsplit=1,
            )[1].split("<h3>Persistence Selection</h3>", maxsplit=1)[0]
            delivery_ordered = tag_containers(delivery_section, "ol")
            self.assertEqual(1, len(delivery_ordered))
            self.assertEqual([], tag_containers(delivery_section, "ul"))
            delivery_items = list_item_texts(delivery_ordered[0], 6)
            self.assertEqual(
                [
                    "Dev Coder returns a clean verified candidate commit without applying terminal delivery.",
                    "Dev Orchestrator obtains fresh independent review and source verification, combines accepted candidates when needed, then applies or resumes the effective Commit-selected skill referenced by applicable AGENTS.md guidance.",
                    "The deliver-work-item-feature-branch completion contract consumes the accepted candidate without modifying source and preserves one delivery identity through host review and corrections.",
                    "Every source correction returns through Dev Orchestrator to the original Dev Coder for a replacement candidate, fresh independent review, and verification before delivery resumes.",
                    "The completion contract loads create-pull-request only as its subordinate GitHub publication capability and returns AWAITING_REVIEW until required review, checks, dependency order, merge, and configured base-branch reachability are observed.",
                    "Persistence closure begins only after Commit returns READY.",
                ],
                delivery_items,
            )
            delivery_paragraphs = paragraph_texts(delivery_section)
            self.assertIn(
                "Candidate creation and terminal delivery are separate responsibilities:",
                delivery_paragraphs,
            )
            self.assertIn(
                "Publication is therefore a resumable handoff rather than completion. Focused pull requests separate shared foundations from independently reviewable changes.",
                delivery_paragraphs,
            )

            persistence_section = catalog.split(
                "<h3>Persistence Selection</h3>",
                maxsplit=1,
            )[1].split("<h3>Work-Item Coordination</h3>", maxsplit=1)[0]
            self.assertEqual([], tag_containers(persistence_section, "ol"))
            persistence_unordered = tag_containers(persistence_section, "ul")
            self.assertEqual(1, len(persistence_unordered))
            persistence_items = list_item_texts(persistence_unordered[0], 2)
            self.assertCountEqual(
                [
                    "Dev Backlog Coordinator and Dev Orchestrator directly apply the effective Persistence-selected manager for lifecycle operations they own; Dev Backlog Steward uses it only for provider-wide inventory, normalization, archival audit, and recovery.",
                    "An UNSET selection requires a decision instead of fallback or shadow persistence.",
                ],
                persistence_items,
            )
            self.assertIn(
                "Work-item Persistence is an independent project selection:",
                paragraph_texts(persistence_section),
            )

            coordination_section = catalog.split(
                "<h3>Work-Item Coordination</h3>",
                maxsplit=1,
            )[1]
            coordination_ordered = tag_containers(coordination_section, "ol")
            coordination_unordered = tag_containers(coordination_section, "ul")
            self.assertEqual(1, len(coordination_ordered))
            self.assertEqual(1, len(coordination_unordered))
            self.assertEqual(
                [
                    "Dev Backlog Coordinator loads coordinate-work-items for sustained multi-item queues and coordinate-codex-tasks only when those executions use Codex tasks.",
                    "It reads inventory and lifecycle through the effective Persistence-selected manager.",
                    "It directly applies the effective Persistence-selected manager for authorized Coordinator lifecycle operations.",
                    "It sends active delivery to Dev Orchestrator with the effective Commit-selected skill.",
                ],
                list_item_texts(coordination_ordered[0], 4),
            )
            self.assertCountEqual(
                [
                    "Provider none has no durable queue or capacity target.",
                    "UNSET, unavailable selected skills, and provider placeholders stop without fallback.",
                    "The coordinator preserves capacity, retry, watchdog, identity, and cleanup semantics without copying provider or completion procedures.",
                    "The orchestrated development lifecycle owns the communication flows.",
                ],
                list_item_texts(coordination_unordered[0], 4),
            )
            self.assertIn(
                "Portable work-item coordination is provider-neutral; Codex task control is an optional runtime mapping:",
                paragraph_texts(coordination_section),
            )

            for paragraph in paragraph_texts(catalog):
                self.assertLess(
                    len(paragraph.split()),
                    80,
                    msg=f"Delivery responsibilities paragraph should be split into a list: {paragraph}",
                )

        assert_catalog_structure(delivery_responsibilities)

        def empty_expected_lists(match: re.Match[str]) -> str:
            tag = match.group(1)
            return f"<{tag}></{tag}><menu>{match.group(2)}</menu>"

        empty_container_mutant = re.sub(
            r"<(ol|ul)>(.*?)</\1>",
            empty_expected_lists,
            delivery_responsibilities,
            flags=re.DOTALL,
        )
        with self.subTest(mutant="empty expected list containers"):
            with self.assertRaises(AssertionError):
                assert_catalog_structure(empty_container_mutant)

        ordered_coordination_item = (
            "<li>It reads inventory and lifecycle through the effective "
            "Persistence-selected manager.</li>"
        )
        unordered_coordination_item = (
            "<li>Provider none has no durable queue or capacity target.</li>"
        )
        swapped_list_mutant = delivery_responsibilities.replace(
            ordered_coordination_item,
            "__ORDERED_COORDINATION_ITEM__",
            1,
        ).replace(
            unordered_coordination_item,
            ordered_coordination_item,
            1,
        ).replace(
            "__ORDERED_COORDINATION_ITEM__",
            unordered_coordination_item,
            1,
        )
        with self.subTest(mutant="ordered and unordered coordination items swapped"):
            with self.assertRaises(AssertionError):
                assert_catalog_structure(swapped_list_mutant)

        first_delivery_item = (
            "<li>Dev Coder returns a clean verified candidate commit without "
            "applying terminal delivery.</li>"
        )
        last_delivery_item = (
            "<li>Persistence closure begins only after Commit returns READY.</li>"
        )
        reordered_delivery_mutant = delivery_responsibilities.replace(
            first_delivery_item,
            "__FIRST_DELIVERY_ITEM__",
            1,
        ).replace(
            last_delivery_item,
            first_delivery_item,
            1,
        ).replace(
            "__FIRST_DELIVERY_ITEM__",
            last_delivery_item,
            1,
        )
        with self.subTest(mutant="ordered delivery items swapped"):
            with self.assertRaises(AssertionError):
                assert_catalog_structure(reordered_delivery_mutant)

        missing_commit_clause_mutant = delivery_responsibilities.replace(
            "<li>Dev Orchestrator obtains fresh independent review and source verification, combines accepted candidates when needed, then applies or resumes the effective Commit-selected skill referenced by applicable AGENTS.md guidance.</li>",
            "<li>Dev Orchestrator obtains fresh independent review and source verification.</li>",
            1,
        )
        with self.subTest(mutant="delivery Commit-routing clause removed"):
            with self.assertRaises(AssertionError):
                assert_catalog_structure(missing_commit_clause_mutant)

        paragraph_to_item_mutant = delivery_responsibilities
        paragraph_moves = (
            (
                "<p>Candidate creation and terminal delivery are separate responsibilities:</p>",
                "Dev Coder returns a clean verified candidate commit without applying terminal delivery.",
                "Candidate creation and terminal delivery are separate responsibilities:",
            ),
            (
                "<p>Publication is therefore a resumable handoff rather than completion. Focused pull requests separate shared foundations from independently reviewable changes.</p>",
                "Persistence closure begins only after Commit returns READY.",
                "Publication is therefore a resumable handoff rather than completion. Focused pull requests separate shared foundations from independently reviewable changes.",
            ),
            (
                "<p>Work-item Persistence is an independent project selection:</p>",
                "Dev Backlog Coordinator and Dev Orchestrator directly apply the effective Persistence-selected manager for lifecycle operations they own; Dev Backlog Steward uses it only for provider-wide inventory, normalization, archival audit, and recovery.",
                "Work-item Persistence is an independent project selection:",
            ),
            (
                "<p>Portable work-item coordination is provider-neutral; Codex task control is an optional runtime mapping:</p>",
                "Dev Backlog Coordinator loads coordinate-work-items for sustained multi-item queues and coordinate-codex-tasks only when those executions use Codex tasks.",
                "Portable work-item coordination is provider-neutral; Codex task control is an optional runtime mapping:",
            ),
        )
        for paragraph_html, item_text, paragraph_text in paragraph_moves:
            paragraph_to_item_mutant = paragraph_to_item_mutant.replace(
                paragraph_html,
                "<p>Structure.</p>",
                1,
            ).replace(
                f"<li>{item_text}</li>",
                f"<li>{item_text} {paragraph_text}</li>",
                1,
            )
        with self.subTest(mutant="intended paragraphs moved into list items"):
            with self.assertRaises(AssertionError):
                assert_catalog_structure(paragraph_to_item_mutant)

    def test_agent_and_skill_definition_page_preserves_topic_hierarchy(self) -> None:
        page_text = (
            REPOSITORY_ROOT / "design" / "agent-and-skill-definitions.html"
        ).read_text(encoding="utf-8")
        outline_text = (
            REPOSITORY_ROOT / "design" / "agent-and-skill-definitions.outline.md"
        ).read_text(encoding="utf-8")
        self.assertEqual(
            [
                ("definition-scope-title", "Conceptual Definition Scope"),
                ("relationships-title", "Agent-Skill Relationships"),
                ("agent-definitions-title", "Conceptual Agent Definitions"),
                ("skills-title", "Skill Definitions"),
                (
                    "project-bindings-title",
                    "Project-Selected Delivery and Technology Bindings",
                ),
                (
                    "provider-independence-title",
                    "Provider-Independent Dev Coder Inputs",
                ),
                (
                    "delivery-responsibilities-title",
                    "Work-Item Delivery Responsibilities",
                ),
            ],
            re.findall(r'<h2 id="([^"]+)">([^<]+)</h2>', page_text),
        )

        outline_coordination_heading = re.search(
            r"    └── ([^\n]+)\n```",
            outline_text,
        )
        self.assertIsNotNone(outline_coordination_heading)
        delivery_section = page_text.split(
            '<section class="section" aria-labelledby="delivery-responsibilities-title">',
            maxsplit=1,
        )[1].split("</section>", maxsplit=1)[0]
        self.assertEqual(
            outline_coordination_heading.group(1),
            re.findall(r"<h3>([^<]+)</h3>", delivery_section)[-1],
        )

        agent_section = page_text.split(
            '<section class="section" aria-labelledby="agent-definitions-title">',
            maxsplit=1,
        )[1].split("</section>", maxsplit=1)[0]
        self.assertIn('<div id="agent-catalog"></div>', agent_section)

        skill_section = page_text.split(
            '<section class="section" aria-labelledby="skills-title">',
            maxsplit=1,
        )[1].split("</section>", maxsplit=1)[0]
        self.assertLess(
            skill_section.index("<h3>Generated Skill Catalog</h3>"),
            skill_section.index('<div class="wide-grid" id="skill-catalog"></div>'),
        )

        role_card_renderer = page_text.split(
            "function createRoleCard(role) {",
            maxsplit=1,
        )[1].split("function renderRoleCatalog()", maxsplit=1)[0]
        self.assertIn('document.createElement("h4")', role_card_renderer)

        role_catalog_renderer = page_text.split(
            "function renderRoleCatalog() {",
            maxsplit=1,
        )[1].split("function renderSkillCatalog()", maxsplit=1)[0]
        self.assertIn('document.createElement("h3")', role_catalog_renderer)

        category_renderer = page_text.split(
            "const createCategoryPanel = (category) => {",
            maxsplit=1,
        )[1].split("skillData.categories.forEach", maxsplit=1)[0]
        self.assertIn('document.createElement("h4")', category_renderer)

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
        self.assertIn(
            '<tr class="format-heading" data-harness-format="claude gemini junie copilot">',
            locations_section,
        )
        self.assertIn("Markdown Agent Definition Files", locations_section)
        self.assertNotIn("Standalone TOML Agent Definition", locations_section)
        self.assertIsNone(re.search(r"\bnative\b", configuration_text, re.IGNORECASE))
        self.assertNotIn(".claude/rules", configuration_text)
        self.assertNotIn("&lt;project-root&gt;/.claude/CLAUDE.md", configuration_text)

    def test_agentic_configuration_topics_follow_primary_document_ownership(self) -> None:
        configuration_text = (
            REPOSITORY_ROOT / "design" / "agentic-configuration.html"
        ).read_text(encoding="utf-8")
        lifecycle_text = (
            REPOSITORY_ROOT / "design" / "orchestrated-development-lifecycle.html"
        ).read_text(encoding="utf-8")

        section_headings = (
            "Runtime Configuration File Locations",
            "Bundle Deployment And Runtime Setup",
            "Cross-Harness Evaluation Environment, Permission Profiles, And Audit Evidence",
        )
        section_positions = [
            configuration_text.index(f">{heading}</h2>")
            for heading in section_headings
        ]
        self.assertEqual(sorted(section_positions), section_positions)

        evaluation_section = configuration_text.split(
            '<section class="section" aria-labelledby="evaluation-title">', maxsplit=1
        )[1].split("</section>", maxsplit=1)[0]
        evaluation_subheadings = (
            "Evaluation Environment And Retained Evidence",
            "Permission Profiles And Containment Limits",
            "Audit Validity And Protection Limits",
        )
        evaluation_subheading_positions = [
            evaluation_section.index(
                f'<h3 class="boundary-heading">{heading}</h3>'
            )
            for heading in evaluation_subheadings
        ]
        self.assertEqual(
            sorted(evaluation_subheading_positions),
            evaluation_subheading_positions,
        )

        helper_path = (
            "${HOME}/.agents/skills/resource-claim-helper-command/scripts/claim.py"
        )
        root_guidance_end = configuration_text.index(
            "<h4>Nested Project Instruction Files</h4>"
        )
        self.assertIn(helper_path, configuration_text[:root_guidance_end])
        self.assertEqual(1, configuration_text.count(helper_path))

        nested_group = configuration_text.split(
            '<th colspan="4" scope="rowgroup">Nested Project Instruction Files',
            maxsplit=1,
        )[1].split("</tbody>", maxsplit=1)[0]
        nested_harnesses = re.findall(
            r'<tr data-harness-row data-harness="([^"]+)">',
            nested_group,
        )
        self.assertEqual(
            ["codex", "claude", "gemini", "copilot", "junie"],
            nested_harnesses,
        )

        self.assertNotIn(">Coordination Surfaces</h3>", configuration_text)
        self.assertIn(
            '<h3 id="runtime-coordination-title">Runtime Coordination Surfaces</h3>',
            lifecycle_text,
        )
        self.assertIn(
            "The stable task and conversation identities remain distinct from display text.",
            lifecycle_text,
        )
        self.assertIn(
            'href="orchestrated-development-lifecycle.html#runtime-coordination-title"',
            configuration_text,
        )

    def test_reverse_engineering_uses_structural_code_discovery(self) -> None:
        skill_text = (
            SKILLS_ROOT / "reverse-engineer-project-documentation" / "SKILL.md"
        ).read_text(encoding="utf-8")

        for phrase in REVERSE_ENGINEERING_DISCOVERY_PHRASES:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, skill_text)

    def test_reverse_engineering_requires_full_gated_coverage(self) -> None:
        reverse_skill_text = (
            SKILLS_ROOT / "reverse-engineer-project-documentation" / "SKILL.md"
        ).read_text(encoding="utf-8")
        bootstrap_skill_text = (
            SKILLS_ROOT / "bootstrap-project-documentation" / "SKILL.md"
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
            SKILLS_ROOT / "route-documentation-work" / "SKILL.md"
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
                / "reverse-engineer-project-documentation"
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
        def first_authored_line_after_notes(
            document_text: str, heading: str
        ) -> tuple[int, str]:
            section_text = document_text.split(heading, maxsplit=1)[1]
            section_text = section_text.split("\n## ", maxsplit=1)[0]
            lines = section_text.splitlines()
            index = 0
            note_count = 0

            while index < len(lines):
                while index < len(lines) and not lines[index].strip():
                    index += 1
                if index >= len(lines) or not lines[index].startswith(">"):
                    break
                note_count += 1
                while index < len(lines) and lines[index].startswith(">"):
                    index += 1

            self.assertLess(index, len(lines), f"{heading} has no authored content")
            return note_count, lines[index]

        def assert_decision_section_order(document_text: str) -> None:
            level_two_headings = [
                line for line in document_text.splitlines() if line.startswith("## ")
            ]
            acceptance_index = level_two_headings.index(
                "## Documentation Acceptance"
            )
            self.assertEqual(
                "## Implementation Readiness",
                level_two_headings[acceptance_index + 1],
            )

        synthetic_note_count, synthetic_decision = first_authored_line_after_notes(
            (
                "## Documentation Acceptance\n\n"
                "> First retained explanatory note.\n\n"
                "> Second retained explanatory note.\n\n"
                "ACCEPTED. Authored decision."
            ),
            "## Documentation Acceptance",
        )
        self.assertEqual(2, synthetic_note_count)
        self.assertEqual("ACCEPTED. Authored decision.", synthetic_decision)

        reverse_text = (
            SKILLS_ROOT / "reverse-engineer-project-documentation" / "SKILL.md"
        ).read_text(encoding="utf-8")
        bootstrap_text = (
            SKILLS_ROOT / "bootstrap-project-documentation" / "SKILL.md"
        ).read_text(encoding="utf-8")
        configuration_text = (
            SKILLS_ROOT / "create-project-configuration" / "SKILL.md"
        ).read_text(encoding="utf-8")
        project_template_text = (
            SKILLS_ROOT
            / "route-documentation-work"
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

        self.assertNotIn("\ndocumentation_mode:", project_template_text)
        self.assertIn(
            "Ordinary setup omits documentation_mode",
            project_template_text,
        )

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
                / "route-documentation-work"
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
            assert_decision_section_order(template_text)
            acceptance_start = template_text.index("## Documentation Acceptance")
            readiness_start = template_text.index("## Implementation Readiness")
            verification_start = template_text.index("## Verification", readiness_start)
            swapped_decision_sections = (
                template_text[:acceptance_start]
                + template_text[readiness_start:verification_start]
                + template_text[acceptance_start:readiness_start]
                + template_text[verification_start:]
            )
            with self.assertRaises(AssertionError):
                assert_decision_section_order(swapped_decision_sections)
            acceptance_note_count, acceptance_decision_instruction = (
                first_authored_line_after_notes(
                    template_text, "## Documentation Acceptance"
                )
            )
            readiness_note_count, readiness_decision_instruction = (
                first_authored_line_after_notes(
                    template_text, "## Implementation Readiness"
                )
            )
            self.assertGreaterEqual(acceptance_note_count, 1)
            self.assertGreaterEqual(readiness_note_count, 1)
            self.assertTrue(
                acceptance_decision_instruction.startswith(
                    "TODO: After any leading retained explanatory note or notes, "
                    "begin the first authored decision with **ACCEPTED.** or **BLOCKED.**"
                )
            )
            self.assertTrue(
                readiness_decision_instruction.startswith(
                    "TODO: After any leading retained explanatory note or notes, "
                    "begin the first authored decision with **READY.** or **BLOCKED.**"
                )
            )
            self.assertNotIn("**READY.**", acceptance_decision_instruction)
            self.assertNotIn("**ACCEPTED.**", readiness_decision_instruction)
            self.assertIn(
                "skip any leading retained explanatory note or notes",
                create_text,
            )
            self.assertIn(
                "skip any leading retained explanatory note or notes",
                checklist_text,
            )
            self.assertEqual(
                1,
                checklist_text.count(
                    "skip any leading retained explanatory note or notes"
                ),
            )
            self.assertNotIn(
                "Does Documentation Acceptance begin with ACCEPTED or BLOCKED",
                checklist_text,
            )
            self.assertIn(
                "documentation acceptance separate from implementation readiness",
                checklist_text.lower(),
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
            SKILLS_ROOT / "route-documentation-work" / "assets" / "templates" / "project-template.yaml"
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
