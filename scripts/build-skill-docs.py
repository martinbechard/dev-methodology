#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Modified with AI assistance.
# Summary: Generates skill and template documentation data, conceptual agent definition views, runtime agent adapters, and their deterministic inventory.

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence
from urllib.parse import urlsplit, urlunsplit

import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPOSITORY_ROOT / "skills"
CATEGORIES_PATH = REPOSITORY_ROOT / "design" / "skill-categories.yaml"
OUTPUT_PATH = REPOSITORY_ROOT / "design" / "generated" / "skill-definitions.js"
TEMPLATE_ROOT = SKILLS_ROOT / "development-methodology" / "assets" / "templates"
TEMPLATE_OUTPUT_PATH = REPOSITORY_ROOT / "design" / "generated" / "template-definitions.js"
ROLE_SCHEMA_PATH = REPOSITORY_ROOT / "agents" / "role-schema.yaml"
MODEL_PROFILES_PATH = REPOSITORY_ROOT / "agents" / "model-profiles.yaml"
ROLES_ROOT = REPOSITORY_ROOT / "agents" / "roles"
ROLE_OUTPUT_PATH = REPOSITORY_ROOT / "design" / "generated" / "role-definitions.js"
GENERATED_ADAPTERS_ROOT = REPOSITORY_ROOT / "generated" / "adapters"
AGENT_GENERATION_MANIFEST_PATH = GENERATED_ADAPTERS_ROOT / "agent-generation-manifest.json"
CODEX_AGENT_OUTPUT_ROOT = GENERATED_ADAPTERS_ROOT / "codex" / "agents"
CLAUDE_AGENT_OUTPUT_ROOT = GENERATED_ADAPTERS_ROOT / "claude" / "agents"
GEMINI_AGENT_OUTPUT_ROOT = GENERATED_ADAPTERS_ROOT / "gemini" / "agents"
JUNIE_AGENT_OUTPUT_ROOT = GENERATED_ADAPTERS_ROOT / "junie" / "agents"
ADAPTERS_ROOT = REPOSITORY_ROOT / "adapters"
ADAPTER_SKILLS_FOLDER_NAME = "skills"
SKILL_FILE_NAME = "SKILL.md"
AGENTS_FOLDER_NAME = "agents"
OPENAI_METADATA_FILE_NAME = "openai.yaml"
FRONTMATTER_DELIMITER = "---"
METADATA_SECTION_KEY = "metadata"
CATEGORY_FIELD_NAME = "category"
CATEGORIES_FIELD_NAME = "categories"
CATEGORY_ID_FIELD_NAME = "id"
CATEGORY_LABEL_FIELD_NAME = "label"
INTERFACE_SECTION_KEY = "interface"
DISPLAY_NAME_FIELD_NAME = "display_name"
SHORT_DESCRIPTION_FIELD_NAME = "short_description"
NAME_FIELD_NAME = "name"
DESCRIPTION_FIELD_NAME = "description"
CODE_FENCE_MARKER = "```"
HEADING_LEVEL_OFFSET = 1
MAX_HEADING_LEVEL = 6
EMPTY_INDEX = 0
NEXT_INDEX = 1
SUCCESS_EXIT_CODE = 0
ERROR_EXIT_CODE = 1
GENERATOR_RELATIVE_PATH = "scripts/build-skill-docs.py"
OUTPUT_GLOBAL_NAME = "DEV_METHODOLOGY_SKILL_DEFINITIONS"
TEMPLATE_OUTPUT_GLOBAL_NAME = "DEV_METHODOLOGY_TEMPLATE_DEFINITIONS"
ROLE_OUTPUT_GLOBAL_NAME = "DEV_METHODOLOGY_ROLE_DEFINITIONS"
ROLE_FILE_SUFFIX = ".role.yaml"
ROLE_SCHEMA_REQUIRED_KEY = "required"
ROLE_SCHEMA_PROPERTIES_KEY = "properties"
ROLE_SCHEMA_GROUPS_KEY = "roleGroups"
ROLE_NAME_FIELD_NAME = "name"
ROLE_FILENAME_FIELD_NAME = "filename"
ROLE_DESCRIPTION_FIELD_NAME = "description"
ROLE_INSTRUCTIONS_FIELD_NAME = "instructions"
ROLE_INSTRUCTION_SECTIONS_PAYLOAD_FIELD_NAME = "instructionSections"
ROLE_REPOSITORY_MUTATION_FIELD_NAME = "repositoryMutation"
ROLE_SKILLS_FIELD_NAME = "skills"
ROLE_AGENT_DEPENDENCIES_FIELD_NAME = "agentDependencies"
ROLE_OUTPUT_CONTRACT_FIELD_NAME = "outputContract"
ROLE_SKILL_JUSTIFICATION_FIELD_NAME = "justification"
ROLE_SKILL_CONDITION_FIELD_NAME = "condition"
ROLE_OUTPUT_PURPOSE_FIELD_NAME = "purpose"
ROLE_EXAMPLES_FIELD_NAME = "examples"
ROLE_MODEL_PROFILE_FIELD_NAME = "modelProfile"
ROLE_MODEL_STAGES_FIELD_NAME = "modelStages"
ROLE_DYNAMIC_FOLDER_SKILLS_FIELD_NAME = "dynamicFolderSkills"
ROLE_SKILL_AVAILABILITY_FIELD_NAME = "skillAvailability"
ROLE_EXAMPLE_RUNTIME_INVOCATIONS_FIELD_NAME = "runtimeInvocations"
ROLE_EXAMPLE_REQUIRED_FIELDS = (
    "purpose",
    ROLE_EXAMPLE_RUNTIME_INVOCATIONS_FIELD_NAME,
    "plausibleResponse",
)
ROLE_EXAMPLE_RUNTIME_IDS = ("codex", "claude-code")
ROLE_LIST_FIELDS = (
    ROLE_AGENT_DEPENDENCIES_FIELD_NAME,
    "tools",
    "disallowedTools",
    "mcpServers",
)
ROLE_STRING_FIELDS = (
    ROLE_NAME_FIELD_NAME,
    ROLE_FILENAME_FIELD_NAME,
    ROLE_DESCRIPTION_FIELD_NAME,
    ROLE_REPOSITORY_MUTATION_FIELD_NAME,
    ROLE_MODEL_PROFILE_FIELD_NAME,
    "permissionMode",
    "isolation",
    "memory",
)
ROLE_INSTRUCTION_SECTION_SPECS = (
    ("objective", "Objective", "string"),
    ("boundaries", "Boundaries", "list"),
    ("decisions", "Decisions", "list"),
    ("workflow", "Workflow", "ordered-list"),
    ("delegation", "Delegation", "list"),
    ("review", "Review", "list"),
    ("failureHandling", "Failure Handling", "list"),
    ("completion", "Completion", "list"),
)
ROLE_REQUIRED_INSTRUCTION_SECTIONS = {"objective", "workflow", "completion"}
ROLE_INTEGER_FIELDS = ("maxTurns", "timeout")
ROLE_BOOLEAN_FIELDS = (ROLE_DYNAMIC_FOLDER_SKILLS_FIELD_NAME,)
ROLE_REPOSITORY_MUTATION_VALUES = {"required", "conditional", "never"}
ROLE_READ_ONLY_ISOLATION = "read-only"
ROLE_GROUP_LABELS = {
    "methodology-maintenance": "Methodology Maintenance",
    "project-setup": "Project Setup",
    "wiki-activities": "Wiki Activities",
    "dev-activities": "Dev Activities",
}
ROLE_GROUP_PREFIXES = {
    "methodology-maintenance": "methodology",
    "project-setup": "project",
    "wiki-activities": "wiki",
    "dev-activities": "dev",
}
ROLE_ACTOR_SUFFIXES = {
    "architect",
    "bootstrapper",
    "coder",
    "collector",
    "configurator",
    "coordinator",
    "diagnostician",
    "ingester",
    "maintainer",
    "operator",
    "orchestrator",
    "organiser",
    "researcher",
    "responder",
    "reviewer",
    "specialist",
    "steward",
    "verifier",
    "writer",
}
SKILL_ACTOR_SUFFIXES = {
    "collector",
    "maintainer",
    "organiser",
    "researcher",
    "reviewer",
    "verifier",
    "writer",
}
CODEX_ADAPTER_NAME = "codex"
CLAUDE_ADAPTER_NAME = "claude"
GEMINI_ADAPTER_NAME = "gemini"
JUNIE_ADAPTER_NAME = "junie"
CODEX_HARNESS_DIRECTIVES_SKILL_NAME = "codex-harness-directives"
CODEX_AGENT_EXTENSION = ".toml"
CLAUDE_AGENT_EXTENSION = ".md"
GEMINI_AGENT_EXTENSION = ".md"
JUNIE_AGENT_EXTENSION = ".md"
CODEX_REASONING_FIELD_NAME = "model_reasoning_effort"
CODEX_SANDBOX_FIELD_NAME = "sandbox_mode"
TOML_MULTILINE_BASIC_STRING_DELIMITER = '"""'
GENERATED_FILE_HEADER = "Generated by scripts/build-skill-docs.py. Do not edit by hand."
GENERATED_JAVASCRIPT_HEADER = "\n".join((
    "// Copyright (c) 2026 Martin.Bechard@DevConsult.ca",
    "// AI attribution: Generated with AI assistance.",
    "// Summary: Provides deterministic generated methodology data to the static design pages.",
))
ROLE_SKILL_INSTRUCTION_PREFIX = "Before acting, load these definition-owned skills completely; they govern the work:"
ROLE_OUTPUT_INSTRUCTION_PREFIX = "Return:"
ROLE_DISPLAY_ACRONYMS = {"e2e": "E2E", "qa": "QA", "ux": "UX"}
MINIMUM_POSITIVE_INTEGER = 1
CATEGORY_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]*$")
MODEL_PROFILE_PATTERN = CATEGORY_PATTERN
HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.*)$")
BULLET_PATTERN = re.compile(r"^\s*-\s+(.*)$")
ORDERED_PATTERN = re.compile(r"^\s*\d+\.\s+(.*)$")
MARKDOWN_LINK_PATTERN = re.compile(r"\[([^\]]+)]\(([^)]+)\)")
STRONG_PATTERN = re.compile(r"\*\*([^*]+)\*\*")
EMPHASIS_PATTERN = re.compile(r"\*([^*]+)\*")
TEMPLATE_LANGUAGE_BY_SUFFIX = {
    ".md": "Markdown",
    ".yaml": "YAML",
}


@dataclass(frozen=True)
class Category:
    id: str
    label: str


@dataclass(frozen=True)
class SkillDefinition:
    name: str
    display_name: str
    description: str
    short_description: str
    category: str
    category_label: str
    source_path: str
    markdown: str
    html: str


@dataclass(frozen=True)
class RoleDefinition:
    name: str
    filename: str
    display_name: str
    description: str
    instructions: str
    instruction_sections: dict[str, object]
    repository_mutation: str
    skills: tuple[str, ...]
    agent_dependencies: tuple[str, ...]
    skill_justifications: dict[str, str]
    skill_conditions: dict[str, str]
    output_contract: tuple[str, ...]
    output_purposes: dict[str, str]
    examples: tuple[dict[str, object], ...]
    group: str
    group_label: str
    source_path: str
    yaml: str
    model_profile: str
    model_stages: dict[str, str]
    optional_fields: dict[str, object]


@dataclass(frozen=True)
class AdapterModelProfile:
    model: str
    effort: str | None
    context: str | None


def split_frontmatter(text: str, source_path: Path) -> tuple[dict[str, object], str]:
    lines = text.splitlines()
    if not lines or lines[EMPTY_INDEX] != FRONTMATTER_DELIMITER:
        raise ValueError(f"Missing YAML frontmatter: {source_path}")

    for index, line in enumerate(lines[NEXT_INDEX:], start=NEXT_INDEX):
        if line == FRONTMATTER_DELIMITER:
            frontmatter = yaml.safe_load("\n".join(lines[NEXT_INDEX:index]))
            if not isinstance(frontmatter, dict):
                raise ValueError(f"Frontmatter must be a YAML object: {source_path}")
            return frontmatter, "\n".join(lines[index + NEXT_INDEX :]).lstrip()

    raise ValueError(f"Missing closing frontmatter delimiter: {source_path}")


def parse_boolean(value: str) -> bool:
    """Parse an explicit true-or-false command-line value."""

    normalized = value.lower()
    if normalized == "true":
        return True
    if normalized == "false":
        return False
    raise argparse.ArgumentTypeError("expected true or false")


def read_yaml_object(path: Path) -> dict[str, object]:
    parsed = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(parsed, dict):
        raise ValueError(f"YAML file must contain an object: {path}")
    return parsed


def load_model_profiles() -> dict[str, str]:
    parsed = read_yaml_object(MODEL_PROFILES_PATH)
    profiles = parsed.get("profiles")
    if not isinstance(profiles, dict) or not profiles:
        raise ValueError("model-profiles.yaml must define a profiles mapping.")
    normalized: dict[str, str] = {}
    for profile_id, profile in profiles.items():
        if not isinstance(profile_id, str) or not MODEL_PROFILE_PATTERN.fullmatch(profile_id):
            raise ValueError(f"Invalid model profile id: {profile_id}")
        if not isinstance(profile, dict):
            raise ValueError(f"Model profile {profile_id} must be an object.")
        purpose = profile.get("purpose")
        if not isinstance(purpose, str) or not purpose.strip():
            raise ValueError(f"Model profile {profile_id} must define a purpose.")
        normalized[profile_id] = purpose.strip()
    return normalized


def load_adapter_model_profiles(
    adapter_name: str,
    source_profile_ids: set[str],
) -> dict[str, AdapterModelProfile]:
    path = ADAPTERS_ROOT / adapter_name / "model-profiles.yaml"
    parsed = read_yaml_object(path)
    if parsed.get("adapter") != adapter_name:
        raise ValueError(f"Adapter model profile name must be {adapter_name}: {path}")
    profiles = parsed.get("profiles")
    if not isinstance(profiles, dict):
        raise ValueError(f"Adapter model profiles must be a mapping: {path}")
    if set(profiles) != source_profile_ids:
        raise ValueError(
            f"Adapter {adapter_name} model profiles must match source profiles: {path}"
        )
    normalized: dict[str, AdapterModelProfile] = {}
    for profile_id, profile in profiles.items():
        if not isinstance(profile, dict):
            raise ValueError(f"Adapter model profile {profile_id} must be an object: {path}")
        unknown_fields = sorted(set(profile) - {"model", "effort", "context"})
        if unknown_fields:
            raise ValueError(
                f"Adapter model profile {profile_id} has unknown fields {unknown_fields}: {path}"
            )
        model = profile.get("model")
        effort = profile.get("effort")
        context = profile.get("context")
        if not isinstance(model, str) or not model.strip():
            raise ValueError(f"Adapter model profile {profile_id} must define model: {path}")
        for field_name, value in (("effort", effort), ("context", context)):
            if value is not None and (not isinstance(value, str) or not value.strip()):
                raise ValueError(
                    f"Adapter model profile {profile_id} {field_name} must be a string: {path}"
                )
        normalized[profile_id] = AdapterModelProfile(
            model.strip(),
            effort.strip() if isinstance(effort, str) else None,
            context.strip() if isinstance(context, str) else None,
        )
    return normalized


def load_categories() -> list[Category]:
    parsed = read_yaml_object(CATEGORIES_PATH)
    category_items = parsed.get(CATEGORIES_FIELD_NAME)
    if not isinstance(category_items, list):
        raise ValueError("skill-categories.yaml must define a categories list.")

    categories: list[Category] = []
    seen_ids: set[str] = set()
    for item in category_items:
        if not isinstance(item, dict):
            raise ValueError("Each category must be an object.")
        category_id = item.get(CATEGORY_ID_FIELD_NAME)
        label = item.get(CATEGORY_LABEL_FIELD_NAME)
        if not isinstance(category_id, str) or not CATEGORY_PATTERN.fullmatch(category_id):
            raise ValueError(f"Invalid category id: {category_id}")
        if category_id in seen_ids:
            raise ValueError(f"Duplicate category id: {category_id}")
        if not isinstance(label, str) or not label.strip():
            raise ValueError(f"Missing category label for {category_id}")
        categories.append(Category(category_id, label.strip()))
        seen_ids.add(category_id)

    return categories


def category_from_frontmatter(frontmatter: dict[str, object], source_path: Path) -> str:
    metadata = frontmatter.get(METADATA_SECTION_KEY)
    if not isinstance(metadata, dict):
        raise ValueError(f"Skill metadata must define category: {source_path}")
    category = metadata.get(CATEGORY_FIELD_NAME)
    if not isinstance(category, str) or not category.strip():
        raise ValueError(f"Skill metadata category is missing: {source_path}")
    if not CATEGORY_PATTERN.fullmatch(category):
        raise ValueError(f"Skill metadata category is invalid: {source_path}")
    return category


def load_openai_interface(skill_directory: Path) -> dict[str, object]:
    metadata_path = skill_directory / AGENTS_FOLDER_NAME / OPENAI_METADATA_FILE_NAME
    if not metadata_path.is_file():
        return {}
    parsed = read_yaml_object(metadata_path)
    interface = parsed.get(INTERFACE_SECTION_KEY)
    return interface if isinstance(interface, dict) else {}


def display_name_from_skill_name(skill_name: str) -> str:
    return re.sub(r"[-_]+", " ", skill_name).title()


def first_sentence(description: str) -> str:
    return re.split(r"(?<=[.!?])\s+", description.strip(), maxsplit=NEXT_INDEX)[EMPTY_INDEX]


def _design_href_for_skill_link(href: str, skill_directory: Path) -> str:
    """Return a skill Markdown link that resolves correctly from a design page."""

    parsed = urlsplit(href)
    if parsed.scheme or parsed.netloc or not parsed.path or parsed.path.startswith("/"):
        return href

    target = (skill_directory / parsed.path).resolve()
    try:
        repository_path = target.relative_to(REPOSITORY_ROOT)
    except ValueError as error:
        raise ValueError(f"Skill link resolves outside the repository: {href}") from error

    design_path = f"../{repository_path.as_posix()}"
    return urlunsplit(("", "", design_path, parsed.query, parsed.fragment))


def format_inline(text: str, skill_directory: Path) -> str:
    escaped = html.escape(text, quote=True)

    def replace_link(match: re.Match[str]) -> str:
        label = html.escape(match.group(NEXT_INDEX), quote=True)
        href = html.escape(
            _design_href_for_skill_link(match.group(2), skill_directory),
            quote=True,
        )
        return f'<a href="{href}">{label}</a>'

    escaped = MARKDOWN_LINK_PATTERN.sub(replace_link, escaped)
    escaped = STRONG_PATTERN.sub(r"<strong>\1</strong>", escaped)
    return EMPHASIS_PATTERN.sub(r"<em>\1</em>", escaped)


def render_markdown(markdown: str, skill_directory: Path) -> str:
    lines = markdown.splitlines()
    parts: list[str] = []
    paragraph_lines: list[str] = []
    list_items: list[str] = []
    list_tag = ""
    code_lines: list[str] = []
    in_code_block = False

    def close_paragraph() -> None:
        if paragraph_lines:
            parts.append(
                f"<p>{format_inline(' '.join(paragraph_lines), skill_directory)}</p>"
            )
            paragraph_lines.clear()

    def close_list() -> None:
        nonlocal list_tag
        if list_items:
            parts.append(f"<{list_tag}>{''.join(list_items)}</{list_tag}>")
            list_items.clear()
            list_tag = ""

    def close_code_block() -> None:
        nonlocal in_code_block
        parts.append(f"<pre><code>{html.escape(chr(10).join(code_lines))}</code></pre>")
        code_lines.clear()
        in_code_block = False

    for line in lines:
        trimmed = line.strip()
        if trimmed.startswith(CODE_FENCE_MARKER):
            if in_code_block:
                close_code_block()
            else:
                close_paragraph()
                close_list()
                in_code_block = True
            continue

        if in_code_block:
            code_lines.append(line)
            continue

        if not trimmed:
            close_paragraph()
            close_list()
            continue

        heading_match = HEADING_PATTERN.match(trimmed)
        if heading_match:
            close_paragraph()
            close_list()
            heading_level = min(len(heading_match.group(NEXT_INDEX)) + HEADING_LEVEL_OFFSET, MAX_HEADING_LEVEL)
            parts.append(
                f"<h{heading_level}>{format_inline(heading_match.group(2), skill_directory)}</h{heading_level}>"
            )
            continue

        bullet_match = BULLET_PATTERN.match(line)
        if bullet_match:
            close_paragraph()
            if list_tag and list_tag != "ul":
                close_list()
            list_tag = "ul"
            list_items.append(
                f"<li>{format_inline(bullet_match.group(NEXT_INDEX), skill_directory)}</li>"
            )
            continue

        ordered_match = ORDERED_PATTERN.match(line)
        if ordered_match:
            close_paragraph()
            if list_tag and list_tag != "ol":
                close_list()
            list_tag = "ol"
            list_items.append(
                f"<li>{format_inline(ordered_match.group(NEXT_INDEX), skill_directory)}</li>"
            )
            continue

        close_list()
        paragraph_lines.append(trimmed)

    if in_code_block:
        close_code_block()
    close_paragraph()
    close_list()
    return "\n".join(parts)


def load_skill_definition(skill_directory: Path, categories_by_id: dict[str, Category]) -> SkillDefinition:
    skill_path = skill_directory / SKILL_FILE_NAME
    raw_markdown = skill_path.read_text(encoding="utf-8")
    frontmatter, body_markdown = split_frontmatter(raw_markdown, skill_path)
    name = frontmatter.get(NAME_FIELD_NAME)
    description = frontmatter.get(DESCRIPTION_FIELD_NAME)
    if not isinstance(name, str) or not isinstance(description, str):
        raise ValueError(f"Skill frontmatter must define name and description: {skill_path}")

    category_id = category_from_frontmatter(frontmatter, skill_path)
    category = categories_by_id.get(category_id)
    if category is None:
        raise ValueError(f"Unknown category {category_id}: {skill_path}")
    if name != skill_directory.name:
        raise ValueError(f"Skill name must match its directory: {skill_path}")
    if name.split("-")[-1] in SKILL_ACTOR_SUFFIXES:
        raise ValueError(f"Skill operations must use verbs instead of actor nouns: {skill_path}")
    if category_id == "artifact-creation" and not name.startswith("create-"):
        raise ValueError(f"Artifact creation skills must start with create: {skill_path}")
    if category_id == "artifact-review" and not name.startswith("review-"):
        raise ValueError(f"Artifact review skills must start with review: {skill_path}")
    if category_id == "wiki-and-knowledge" and not (
        name.startswith("project-wiki") or name == "code-project-wiki"
    ):
        raise ValueError(f"Wiki skills must use the project-wiki object prefix: {skill_path}")

    interface = load_openai_interface(skill_directory)
    display_name = interface.get(DISPLAY_NAME_FIELD_NAME)
    short_description = interface.get(SHORT_DESCRIPTION_FIELD_NAME)
    return SkillDefinition(
        name=name,
        display_name=display_name if isinstance(display_name, str) else display_name_from_skill_name(name),
        description=description.strip(),
        short_description=short_description if isinstance(short_description, str) else first_sentence(description),
        category=category.id,
        category_label=category.label,
        source_path=str(skill_path.relative_to(REPOSITORY_ROOT)),
        markdown=raw_markdown,
        html=render_markdown(body_markdown, skill_directory),
    )


def skill_directories() -> list[Path]:
    return sorted(path.parent for path in SKILLS_ROOT.glob(f"*/{SKILL_FILE_NAME}"))


def adapter_skill_directories(adapter_name: str) -> list[Path]:
    """Return validated harness-specific skill directories for one adapter."""

    skills_root = ADAPTERS_ROOT / adapter_name / ADAPTER_SKILLS_FOLDER_NAME
    if not skills_root.exists():
        return []
    if not skills_root.is_dir() or skills_root.is_symlink():
        raise ValueError(f"Adapter skills root must be a non-symlink directory: {skills_root}")

    directories = sorted(path.parent for path in skills_root.glob(f"*/{SKILL_FILE_NAME}"))
    names: set[str] = set()
    for directory in directories:
        skill_path = directory / SKILL_FILE_NAME
        if directory.is_symlink() or skill_path.is_symlink():
            raise ValueError(f"Adapter skill must not be a symlink: {skill_path}")
        frontmatter, _ = split_frontmatter(skill_path.read_text(encoding="utf-8"), skill_path)
        name = frontmatter.get(NAME_FIELD_NAME)
        description = frontmatter.get(DESCRIPTION_FIELD_NAME)
        if not isinstance(name, str) or not name.strip() or not isinstance(description, str) or not description.strip():
            raise ValueError(f"Adapter skill frontmatter must define name and description: {skill_path}")
        if name != directory.name:
            raise ValueError(f"Adapter skill name must match its directory: {skill_path}")
        if name in names:
            raise ValueError(f"Duplicate adapter skill name {name}: {skills_root}")
        names.add(name)
    return directories


def adapter_skill_names(adapter_name: str) -> tuple[str, ...]:
    """Return the stable names of skills owned only by one runtime adapter."""

    return tuple(directory.name for directory in adapter_skill_directories(adapter_name))


def role_display_name(role_name: str) -> str:
    words = []
    for word in role_name.split("-"):
        words.append(ROLE_DISPLAY_ACRONYMS.get(word, word.title()))
    return " ".join(words)


def validate_string_list(value: object, field_name: str, source_path: Path) -> tuple[str, ...]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"Conceptual agent definition {field_name} must be a non-empty list: {source_path}")
    if any(not isinstance(item, str) or not item.strip() for item in value):
        raise ValueError(f"Conceptual agent definition {field_name} must contain non-empty strings: {source_path}")
    normalized = tuple(item.strip() for item in value)
    if len(normalized) != len(set(normalized)):
        raise ValueError(f"Conceptual agent definition {field_name} contains duplicates: {source_path}")
    return normalized


def validate_role_examples(value: object, source_path: Path) -> tuple[dict[str, object], ...]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"Conceptual agent definition {ROLE_EXAMPLES_FIELD_NAME} must be a non-empty list: {source_path}")

    examples: list[dict[str, object]] = []
    for index, example in enumerate(value, start=MINIMUM_POSITIVE_INTEGER):
        if not isinstance(example, dict):
            raise ValueError(f"Conceptual agent definition example {index} must be an object: {source_path}")
        unknown_fields = sorted(set(example) - set(ROLE_EXAMPLE_REQUIRED_FIELDS))
        missing_fields = sorted(set(ROLE_EXAMPLE_REQUIRED_FIELDS) - set(example))
        if unknown_fields or missing_fields:
            raise ValueError(
                f"Conceptual agent definition example {index} must contain only {ROLE_EXAMPLE_REQUIRED_FIELDS}: {source_path}"
            )
        normalized: dict[str, object] = {}
        for field_name in ROLE_EXAMPLE_REQUIRED_FIELDS:
            field_value = example[field_name]
            if field_name == ROLE_EXAMPLE_RUNTIME_INVOCATIONS_FIELD_NAME:
                if not isinstance(field_value, dict) or set(field_value) != set(ROLE_EXAMPLE_RUNTIME_IDS):
                    raise ValueError(
                        f"Conceptual agent definition example {index} {field_name} keys must match {ROLE_EXAMPLE_RUNTIME_IDS}: {source_path}"
                    )
                invocations: dict[str, str] = {}
                for runtime_id in ROLE_EXAMPLE_RUNTIME_IDS:
                    invocation = field_value[runtime_id]
                    if not isinstance(invocation, str) or not invocation.strip():
                        raise ValueError(
                            f"Conceptual agent definition example {index} {field_name} {runtime_id} must be a non-empty string: {source_path}"
                        )
                    invocations[runtime_id] = invocation.strip()
                normalized[field_name] = invocations
                continue
            if not isinstance(field_value, str) or not field_value.strip():
                raise ValueError(
                    f"Conceptual agent definition example {index} {field_name} must be a non-empty string: {source_path}"
                )
            normalized[field_name] = field_value.strip()
        examples.append(normalized)

    return tuple(examples)


def validate_role_instructions(
    value: object,
    source_path: Path,
) -> tuple[str, dict[str, object]]:
    if isinstance(value, str):
        if not value.strip():
            raise ValueError(f"Conceptual agent definition instructions must be a non-empty string: {source_path}")
        return value.strip(), {}

    if not isinstance(value, dict) or not value:
        raise ValueError(
            f"Conceptual agent definition instructions must be a non-empty string or structured mapping: {source_path}"
        )

    known_sections = {name for name, _, _ in ROLE_INSTRUCTION_SECTION_SPECS}
    unknown_sections = sorted(set(value) - known_sections)
    missing_sections = sorted(ROLE_REQUIRED_INSTRUCTION_SECTIONS - set(value))
    if unknown_sections or missing_sections:
        raise ValueError(
            "Conceptual agent definition structured instructions have "
            f"unknown sections {unknown_sections} or missing sections {missing_sections}: {source_path}"
        )

    normalized: dict[str, object] = {}
    rendered_sections: list[str] = []
    for section_name, section_label, section_type in ROLE_INSTRUCTION_SECTION_SPECS:
        if section_name not in value:
            continue
        section_value = value[section_name]
        if section_type == "string":
            if not isinstance(section_value, str) or not section_value.strip():
                raise ValueError(
                    f"Conceptual agent definition instructions {section_name} must be a non-empty string: {source_path}"
                )
            normalized_value: object = section_value.strip()
            section_body = normalized_value
        else:
            items = validate_string_list(section_value, f"instructions.{section_name}", source_path)
            normalized_value = list(items)
            if section_type == "ordered-list":
                section_body = "\n".join(
                    f"{index}. {item}"
                    for index, item in enumerate(items, start=MINIMUM_POSITIVE_INTEGER)
                )
            else:
                section_body = "\n".join(f"- {item}" for item in items)
        normalized[section_name] = normalized_value
        rendered_sections.append(f"## {section_label}\n\n{section_body}")
    return "\n\n".join(rendered_sections), normalized


def validate_annotated_list(
    value: object,
    field_name: str,
    annotation_field_name: str,
    source_path: Path,
) -> tuple[tuple[str, ...], dict[str, str]]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"Conceptual agent definition {field_name} must be a non-empty list: {source_path}")

    names: list[str] = []
    annotations: dict[str, str] = {}
    for item in value:
        if not isinstance(item, dict) or len(item) != 1:
            raise ValueError(
                f"Conceptual agent definition {field_name} entries must contain exactly one named mapping: {source_path}"
            )
        name, metadata = next(iter(item.items()))
        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"Conceptual agent definition {field_name} entry names must be non-empty strings: {source_path}")
        normalized_name = name.strip()
        if normalized_name in annotations:
            raise ValueError(f"Conceptual agent definition {field_name} contains duplicate {normalized_name}: {source_path}")
        if not isinstance(metadata, dict) or set(metadata) != {annotation_field_name}:
            raise ValueError(
                f"Conceptual agent definition {field_name} {normalized_name} must contain only {annotation_field_name}: {source_path}"
            )
        annotation = metadata[annotation_field_name]
        if not isinstance(annotation, str) or not annotation.strip():
            raise ValueError(
                f"Conceptual agent definition {field_name} {normalized_name} {annotation_field_name} must be a non-empty string: {source_path}"
            )
        names.append(normalized_name)
        annotations[normalized_name] = annotation.strip()
    return tuple(names), annotations


def validate_role_skills(
    value: object,
    source_path: Path,
) -> tuple[tuple[str, ...], dict[str, str], dict[str, str]]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"Conceptual agent definition {ROLE_SKILLS_FIELD_NAME} must be a non-empty list: {source_path}")

    names: list[str] = []
    justifications: dict[str, str] = {}
    conditions: dict[str, str] = {}
    for item in value:
        if not isinstance(item, dict) or len(item) != 1:
            raise ValueError(
                f"Conceptual agent definition {ROLE_SKILLS_FIELD_NAME} entries must contain exactly one named mapping: {source_path}"
            )
        name, metadata = next(iter(item.items()))
        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"Conceptual agent definition {ROLE_SKILLS_FIELD_NAME} entry names must be non-empty strings: {source_path}")
        normalized_name = name.strip()
        if normalized_name in justifications:
            raise ValueError(f"Conceptual agent definition {ROLE_SKILLS_FIELD_NAME} contains duplicate {normalized_name}: {source_path}")
        if not isinstance(metadata, dict) or set(metadata) not in (
            {ROLE_SKILL_JUSTIFICATION_FIELD_NAME},
            {ROLE_SKILL_JUSTIFICATION_FIELD_NAME, ROLE_SKILL_CONDITION_FIELD_NAME},
        ):
            raise ValueError(
                f"Conceptual agent definition {ROLE_SKILLS_FIELD_NAME} {normalized_name} must contain justification and optional condition only: {source_path}"
            )
        justification = metadata[ROLE_SKILL_JUSTIFICATION_FIELD_NAME]
        if not isinstance(justification, str) or not justification.strip():
            raise ValueError(
                f"Conceptual agent definition {ROLE_SKILLS_FIELD_NAME} {normalized_name} justification must be a non-empty string: {source_path}"
            )
        justifications[normalized_name] = justification.strip()
        condition = metadata.get(ROLE_SKILL_CONDITION_FIELD_NAME)
        if condition is not None:
            if not isinstance(condition, str) or not condition.strip().startswith("when "):
                raise ValueError(
                    f"Conceptual agent definition {ROLE_SKILLS_FIELD_NAME} {normalized_name} condition must be a non-empty fragment beginning with when: {source_path}"
                )
            conditions[normalized_name] = condition.strip().rstrip(".")
        names.append(normalized_name)
    return tuple(names), justifications, conditions


def load_role_schema() -> tuple[set[str], set[str], set[str]]:
    schema = read_yaml_object(ROLE_SCHEMA_PATH)
    required = validate_string_list(
        schema.get(ROLE_SCHEMA_REQUIRED_KEY),
        ROLE_SCHEMA_REQUIRED_KEY,
        ROLE_SCHEMA_PATH,
    )
    properties = schema.get(ROLE_SCHEMA_PROPERTIES_KEY)
    if not isinstance(properties, dict) or not properties:
        raise ValueError("role-schema.yaml must define properties.")
    groups = validate_string_list(
        schema.get(ROLE_SCHEMA_GROUPS_KEY),
        ROLE_SCHEMA_GROUPS_KEY,
        ROLE_SCHEMA_PATH,
    )
    if set(groups) != set(ROLE_GROUP_LABELS) or set(groups) != set(ROLE_GROUP_PREFIXES):
        raise ValueError(
            "role-schema.yaml conceptual definition groups must match the generated documentation groups."
        )
    category_words = [label.split()[0].lower() for label in ROLE_GROUP_LABELS.values()]
    if len(category_words) != len(set(category_words)):
        raise ValueError("Conceptual agent definition category labels must start with unique words.")
    for group, label in ROLE_GROUP_LABELS.items():
        if label.split()[0].lower() != ROLE_GROUP_PREFIXES[group]:
            raise ValueError(f"Conceptual agent definition category {group} must start with its definition prefix.")
    return set(required), set(properties), set(groups)


def role_source_paths() -> list[Path]:
    return sorted(ROLES_ROOT.glob(f"*/*{ROLE_FILE_SUFFIX}"))


def load_role_definition(
    source_path: Path,
    required_fields: set[str],
    allowed_fields: set[str],
    allowed_groups: set[str],
    skill_names: set[str],
    model_profile_ids: set[str],
) -> RoleDefinition:
    parsed = read_yaml_object(source_path)
    missing_fields = sorted(required_fields - set(parsed))
    if missing_fields:
        raise ValueError(f"Conceptual agent definition is missing required fields {missing_fields}: {source_path}")
    unknown_fields = sorted(set(parsed) - allowed_fields)
    if unknown_fields:
        raise ValueError(f"Conceptual agent definition has unknown fields {unknown_fields}: {source_path}")

    for field_name in ROLE_STRING_FIELDS:
        value = parsed.get(field_name)
        if value is not None and (not isinstance(value, str) or not value.strip()):
            raise ValueError(f"Conceptual agent definition {field_name} must be a non-empty string: {source_path}")
    for field_name in ROLE_INTEGER_FIELDS:
        value = parsed.get(field_name)
        if value is not None and (
            not isinstance(value, int) or isinstance(value, bool) or value < MINIMUM_POSITIVE_INTEGER
        ):
            raise ValueError(f"Conceptual agent definition {field_name} must be a positive integer: {source_path}")
    for field_name in ROLE_BOOLEAN_FIELDS:
        value = parsed.get(field_name)
        if value is not None and not isinstance(value, bool):
            raise ValueError(f"Conceptual agent definition {field_name} must be a boolean: {source_path}")

    skill_availability = parsed.get(ROLE_SKILL_AVAILABILITY_FIELD_NAME)
    if skill_availability is not None:
        if not isinstance(skill_availability, list):
            raise ValueError(f"Conceptual agent definition skillAvailability must be a list: {source_path}")
        selectors: set[tuple[str, str]] = set()
        for item in skill_availability:
            if not isinstance(item, dict) or set(item) not in ({"name", "enabled"}, {"path", "enabled"}):
                raise ValueError(
                    f"Conceptual agent definition skillAvailability entries need enabled and exactly one of name or path: {source_path}"
                )
            selector = "name" if "name" in item else "path"
            if not isinstance(item[selector], str) or not item[selector].strip() or not isinstance(item["enabled"], bool):
                raise ValueError(f"Conceptual agent definition skillAvailability entry is invalid: {source_path}")
            key = (selector, item[selector])
            if key in selectors:
                raise ValueError(f"Conceptual agent definition skillAvailability repeats {selector} {item[selector]}: {source_path}")
            selectors.add(key)

    dynamic_folder_skills = parsed.get(ROLE_DYNAMIC_FOLDER_SKILLS_FIELD_NAME, False)
    tools = parsed.get("tools")
    if dynamic_folder_skills and tools is not None and "Skill" not in tools:
        raise ValueError(
            f"Conceptual agent definition with dynamic folder skills and a restrictive Claude tools allowlist must include Skill: {source_path}"
        )

    model_profile = parsed.get(ROLE_MODEL_PROFILE_FIELD_NAME)
    if model_profile not in model_profile_ids:
        raise ValueError(f"Conceptual agent definition has unknown model profile {model_profile}: {source_path}")
    model_stages = parsed.get(ROLE_MODEL_STAGES_FIELD_NAME)
    if model_stages is not None:
        if not isinstance(model_stages, dict) or not model_stages:
            raise ValueError(f"Conceptual agent definition modelStages must be a non-empty mapping: {source_path}")
        for stage_name, stage_profile in model_stages.items():
            if not isinstance(stage_name, str) or not CATEGORY_PATTERN.fullmatch(stage_name):
                raise ValueError(f"Conceptual agent definition modelStages has invalid stage {stage_name}: {source_path}")
            if stage_profile not in model_profile_ids:
                raise ValueError(
                    f"Conceptual agent definition modelStages {stage_name} has unknown profile {stage_profile}: {source_path}"
                )

    role_name = parsed[ROLE_NAME_FIELD_NAME]
    filename = parsed[ROLE_FILENAME_FIELD_NAME]
    if not isinstance(role_name, str) or not CATEGORY_PATTERN.fullmatch(role_name):
        raise ValueError(f"Invalid conceptual agent definition name: {source_path}")
    if not isinstance(filename, str) or not CATEGORY_PATTERN.fullmatch(filename):
        raise ValueError(f"Invalid conceptual agent definition filename: {source_path}")
    expected_filename = source_path.name.removesuffix(ROLE_FILE_SUFFIX)
    if filename != expected_filename:
        raise ValueError(f"Conceptual agent definition filename must match its source file: {source_path}")
    if role_name != filename:
        raise ValueError(f"Conceptual agent definition name must match its filename: {source_path}")

    group = source_path.parent.name
    if group not in allowed_groups:
        raise ValueError(f"Unknown conceptual agent definition group {group}: {source_path}")
    role_segments = role_name.split("-")
    if "agent" in role_segments:
        raise ValueError(f"Conceptual agent definition name must not contain the word agent: {source_path}")
    if role_segments[0] != ROLE_GROUP_PREFIXES[group]:
        raise ValueError(f"Conceptual agent definition name must start with the {ROLE_GROUP_PREFIXES[group]} prefix: {source_path}")
    if role_segments[-1] not in ROLE_ACTOR_SUFFIXES:
        raise ValueError(f"Conceptual agent definition name must end with an actor noun: {source_path}")

    list_values: dict[str, tuple[str, ...]] = {}
    for field_name in ROLE_LIST_FIELDS:
        value = parsed.get(field_name)
        if value is not None:
            list_values[field_name] = validate_string_list(value, field_name, source_path)

    examples = ()
    if ROLE_EXAMPLES_FIELD_NAME in parsed:
        examples = validate_role_examples(parsed[ROLE_EXAMPLES_FIELD_NAME], source_path)

    role_skills, skill_justifications, skill_conditions = validate_role_skills(
        parsed[ROLE_SKILLS_FIELD_NAME],
        source_path,
    )
    unknown_skills = sorted(set(role_skills) - skill_names)
    if unknown_skills:
        raise ValueError(f"Conceptual agent definition references unknown skills {unknown_skills}: {source_path}")

    repository_mutation = parsed[ROLE_REPOSITORY_MUTATION_FIELD_NAME]
    if repository_mutation not in ROLE_REPOSITORY_MUTATION_VALUES:
        raise ValueError(
            f"Conceptual agent definition {ROLE_REPOSITORY_MUTATION_FIELD_NAME} must be required, conditional, or never: {source_path}"
        )
    fixed_claim = "agent-claim" in role_skills and "agent-claim" not in skill_conditions
    conditional_claim = "agent-claim" in skill_conditions
    if repository_mutation == "required" and not fixed_claim:
        raise ValueError(f"Conceptual agent definition with required repository mutation must load agent-claim as a definition-owned skill: {source_path}")
    if repository_mutation == "conditional" and not conditional_claim:
        raise ValueError(f"Conceptual agent definition with conditional repository mutation must conditionally load agent-claim: {source_path}")
    if repository_mutation == "never" and "agent-claim" in role_skills:
        raise ValueError(f"Read-only conceptual agent definition must not load agent-claim: {source_path}")
    if (
        parsed.get("isolation") == ROLE_READ_ONLY_ISOLATION
        and repository_mutation != "never"
    ):
        raise ValueError(
            "Conceptual agent definition with read-only isolation must declare "
            f"repositoryMutation never: {source_path}"
        )

    output_contract, output_purposes = validate_annotated_list(
        parsed[ROLE_OUTPUT_CONTRACT_FIELD_NAME],
        ROLE_OUTPUT_CONTRACT_FIELD_NAME,
        ROLE_OUTPUT_PURPOSE_FIELD_NAME,
        source_path,
    )

    agent_dependencies = list_values.get(ROLE_AGENT_DEPENDENCIES_FIELD_NAME, ())
    optional_fields = {
        field_name: parsed[field_name]
        for field_name in sorted(
            set(parsed)
            - required_fields
            - {ROLE_EXAMPLES_FIELD_NAME, ROLE_AGENT_DEPENDENCIES_FIELD_NAME}
        )
    }
    for field_name, values in list_values.items():
        if field_name in optional_fields:
            optional_fields[field_name] = list(values)

    description = parsed[ROLE_DESCRIPTION_FIELD_NAME]
    if not isinstance(description, str):
        raise ValueError(f"Conceptual agent definition description must be a string: {source_path}")
    instructions, instruction_sections = validate_role_instructions(
        parsed[ROLE_INSTRUCTIONS_FIELD_NAME],
        source_path,
    )
    return RoleDefinition(
        name=role_name,
        filename=filename,
        display_name=role_display_name(role_name),
        description=description.strip(),
        instructions=instructions.strip(),
        instruction_sections=instruction_sections,
        repository_mutation=repository_mutation,
        skills=role_skills,
        agent_dependencies=agent_dependencies,
        skill_justifications=skill_justifications,
        skill_conditions=skill_conditions,
        output_contract=output_contract,
        output_purposes=output_purposes,
        examples=examples,
        group=group,
        group_label=ROLE_GROUP_LABELS[group],
        source_path=str(source_path.relative_to(REPOSITORY_ROOT)),
        yaml=source_path.read_text(encoding="utf-8"),
        model_profile=model_profile,
        model_stages=dict(model_stages) if isinstance(model_stages, dict) else {},
        optional_fields=optional_fields,
    )


def load_role_definitions(skill_names: set[str]) -> list[RoleDefinition]:
    required_fields, allowed_fields, allowed_groups = load_role_schema()
    model_profile_ids = set(load_model_profiles())
    roles = [
        load_role_definition(
            source_path,
            required_fields,
            allowed_fields,
            allowed_groups,
            skill_names,
            model_profile_ids,
        )
        for source_path in role_source_paths()
    ]
    role_names = [role.name for role in roles]
    filenames = [role.filename for role in roles]
    if len(role_names) != len(set(role_names)):
        raise ValueError("Conceptual agent definition names must be unique.")
    if len(filenames) != len(set(filenames)):
        raise ValueError("Conceptual agent definition filenames must be unique.")
    known_role_names = set(role_names)
    for role in roles:
        unknown_dependencies = sorted(set(role.agent_dependencies) - known_role_names)
        if unknown_dependencies:
            raise ValueError(
                f"Conceptual agent definition {role.name} references unknown agent dependencies {unknown_dependencies}."
            )
        if role.name in role.agent_dependencies:
            raise ValueError(f"Conceptual agent definition {role.name} cannot depend on itself.")
    return roles


def build_payload() -> dict[str, object]:
    categories = load_categories()
    categories_by_id = {category.id: category for category in categories}
    skills = [load_skill_definition(skill_directory, categories_by_id) for skill_directory in skill_directories()]
    skill_categories = {skill.category for skill in skills}
    missing_categories = sorted(skill_categories - set(categories_by_id))
    if missing_categories:
        raise ValueError("Unknown skill categories: " + ", ".join(missing_categories))

    return {
        "categories": [category.__dict__ for category in categories],
        "skills": {
            skill.name: {
                "name": skill.name,
                "displayName": skill.display_name,
                "description": skill.description,
                "shortDescription": skill.short_description,
                "category": skill.category,
                "categoryLabel": skill.category_label,
                "sourcePath": skill.source_path,
                "markdown": skill.markdown,
                "html": skill.html,
            }
            for skill in skills
        },
    }


def render_javascript(payload: dict[str, object]) -> str:
    serialized = json.dumps(payload, indent=2, sort_keys=True)
    return (
        f"{GENERATED_JAVASCRIPT_HEADER}\n"
        f"// Generated by {GENERATOR_RELATIVE_PATH}. Do not edit by hand.\n"
        f"window.{OUTPUT_GLOBAL_NAME} = {serialized};\n"
    )


def build_template_payload() -> dict[str, object]:
    """Build deterministic browser data from the distributed template sources."""

    templates: dict[str, object] = {}
    for template_path in sorted(TEMPLATE_ROOT.iterdir()):
        language = TEMPLATE_LANGUAGE_BY_SUFFIX.get(template_path.suffix)
        if not template_path.is_file() or language is None:
            continue
        templates[template_path.name] = {
            "content": template_path.read_text(encoding="utf-8"),
            "language": language,
            "name": template_path.name,
            "sourcePath": str(template_path.relative_to(REPOSITORY_ROOT)),
        }

    if not templates:
        raise ValueError(f"No documentation templates found: {TEMPLATE_ROOT}")
    return {"templates": templates}


def render_template_javascript(payload: dict[str, object]) -> str:
    """Render template browser data as a deterministic static JavaScript payload."""

    serialized = json.dumps(payload, indent=2, sort_keys=True)
    return (
        f"{GENERATED_JAVASCRIPT_HEADER}\n"
        f"// {GENERATED_FILE_HEADER}\n"
        f"window.{TEMPLATE_OUTPUT_GLOBAL_NAME} = {serialized};\n"
    )


def build_role_payload(roles: Sequence[RoleDefinition]) -> dict[str, object]:
    return {
        "groups": [
            {"id": group_id, "label": group_label}
            for group_id, group_label in ROLE_GROUP_LABELS.items()
        ],
        "roles": {
            role.name: {
                "name": role.name,
                "filename": role.filename,
                "displayName": role.display_name,
                "description": role.description,
                "instructions": role.instructions,
                ROLE_INSTRUCTION_SECTIONS_PAYLOAD_FIELD_NAME: role.instruction_sections,
                ROLE_REPOSITORY_MUTATION_FIELD_NAME: role.repository_mutation,
                "skills": list(role.skills),
                ROLE_AGENT_DEPENDENCIES_FIELD_NAME: list(role.agent_dependencies),
                "skillJustifications": role.skill_justifications,
                "skillConditions": role.skill_conditions,
                "outputs": list(role.output_contract),
                "outputPurposes": role.output_purposes,
                "examples": list(role.examples),
                "group": role.group,
                "groupLabel": role.group_label,
                "sourcePath": role.source_path,
                "yaml": role.yaml,
                ROLE_MODEL_PROFILE_FIELD_NAME: role.model_profile,
                ROLE_MODEL_STAGES_FIELD_NAME: role.model_stages,
                **role.optional_fields,
            }
            for role in roles
        },
    }


def render_role_javascript(roles: Sequence[RoleDefinition]) -> str:
    serialized = json.dumps(build_role_payload(roles), indent=2, sort_keys=True)
    return (
        f"{GENERATED_JAVASCRIPT_HEADER}\n"
        f"// {GENERATED_FILE_HEADER}\n"
        f"window.{ROLE_OUTPUT_GLOBAL_NAME} = {serialized};\n"
    )


def fixed_role_skills(role: RoleDefinition) -> tuple[str, ...]:
    return tuple(skill for skill in role.skills if skill not in role.skill_conditions)


def conditional_role_skills(role: RoleDefinition) -> tuple[str, ...]:
    return tuple(skill for skill in role.skills if skill in role.skill_conditions)


def role_loading_instruction_text(
    role: RoleDefinition,
    fixed_skills_preloaded: bool = False,
    include_fixed_skills: bool = True,
) -> str:
    sections: list[str] = []
    fixed_skills = fixed_role_skills(role)
    conditional_skills = conditional_role_skills(role)
    if fixed_skills and include_fixed_skills:
        fixed_prefix = (
            "These definition-owned skills are preloaded and govern the work:"
            if fixed_skills_preloaded
            else ROLE_SKILL_INSTRUCTION_PREFIX
        )
        sections.append(f"{fixed_prefix} {', '.join(fixed_skills)}.")
    if conditional_skills:
        route_lines = [
            "Load request-specific skills only when their conditions apply. Use judgment when the request is ambiguous: inspect the requested outcome and available evidence, and ask for clarification only when choosing a route would materially change the result and the intent cannot be inferred.",
        ]
        route_lines.extend(
            f"- Use the {skill} skill {role.skill_conditions[skill]}."
            for skill in conditional_skills
        )
        sections.append("\n".join(route_lines))
    return "\n\n".join(sections)


def inlined_skill_body(skill_name: str, adapter_name: str | None = None) -> str:
    """Return one validated skill body for static adapter embedding."""

    skill_directory = (
        ADAPTERS_ROOT / adapter_name / ADAPTER_SKILLS_FOLDER_NAME / skill_name
        if adapter_name is not None
        else SKILLS_ROOT / skill_name
    )
    skill_path = skill_directory / SKILL_FILE_NAME
    frontmatter, body = split_frontmatter(
        skill_path.read_text(encoding="utf-8"),
        skill_path,
    )
    if frontmatter.get(NAME_FIELD_NAME) != skill_name:
        raise ValueError(f"Skill name must match its directory: {skill_path}")
    return body.rstrip()


def render_inlined_core_skills(
    role: RoleDefinition,
    adapter_name: str,
) -> str:
    """Render the role's unconditional skills as static instruction content."""

    skill_sources = [(skill, None) for skill in fixed_role_skills(role)]
    if adapter_name == CODEX_ADAPTER_NAME and role.repository_mutation != "never":
        skill_sources.append((CODEX_HARNESS_DIRECTIVES_SKILL_NAME, CODEX_ADAPTER_NAME))
    if not skill_sources:
        return ""
    sections = [
        "## Inlined Core Skills",
        "",
        "Apply the following core skill instructions as part of this agent definition. Do not load these core skills dynamically.",
    ]
    for skill_name, source_adapter in skill_sources:
        sections.extend([
            "",
            f"----- BEGIN INLINED CORE SKILL: {skill_name} -----",
            inlined_skill_body(skill_name, source_adapter),
            f"----- END INLINED CORE SKILL: {skill_name} -----",
        ])
    return "\n".join(sections)


def role_instruction_text(
    role: RoleDefinition,
    *,
    adapter_name: str,
    inline_core_skills: bool = True,
) -> str:
    output_text = "; ".join(role.output_contract)
    sections = [role.instructions]
    loading_instructions = role_loading_instruction_text(
        role,
        include_fixed_skills=not inline_core_skills,
    )
    if loading_instructions:
        sections.append(loading_instructions)
    sections.append(f"{ROLE_OUTPUT_INSTRUCTION_PREFIX} {output_text}.")
    if inline_core_skills:
        inlined_skills = render_inlined_core_skills(role, adapter_name)
        if inlined_skills:
            sections.append(inlined_skills)
    return "\n\n".join(sections)


def markdown_role_instruction_text(
    role: RoleDefinition,
    adapter_name: str,
    inline_core_skills: bool,
) -> str:
    """Render one Markdown adapter instruction body without empty sections."""

    sections = [role.instructions]
    loading_instructions = role_loading_instruction_text(
        role,
        fixed_skills_preloaded=adapter_name in {
            CLAUDE_ADAPTER_NAME,
            JUNIE_ADAPTER_NAME,
        },
        include_fixed_skills=not inline_core_skills,
    )
    if loading_instructions:
        sections.append(loading_instructions)
    output_lines = "\n".join(f"- {item}" for item in role.output_contract)
    sections.append(f"Return:\n\n{output_lines}")
    if inline_core_skills:
        inlined_skills = render_inlined_core_skills(role, adapter_name)
        if inlined_skills:
            sections.append(inlined_skills)
    return "\n\n".join(sections) + "\n"


def codex_role_instruction_text(
    role: RoleDefinition,
    inline_core_skills: bool = True,
) -> str:
    """Add the Codex harness skill at generation time without changing portable roles."""

    if inline_core_skills:
        return role_instruction_text(
            role,
            adapter_name=CODEX_ADAPTER_NAME,
            inline_core_skills=True,
        )
    if role.repository_mutation == "never":
        return role_instruction_text(
            role,
            adapter_name=CODEX_ADAPTER_NAME,
            inline_core_skills=False,
        )
    output_text = "; ".join(role.output_contract)
    harness_instruction = (
        f"Before acting, load the {CODEX_HARNESS_DIRECTIVES_SKILL_NAME} skill completely; "
        "it governs Codex-specific directives for this mutation-capable agent."
    )
    return (
        f"{role.instructions}\n\n"
        f"{harness_instruction}\n\n"
        f"{role_loading_instruction_text(role)}\n\n"
        f"{ROLE_OUTPUT_INSTRUCTION_PREFIX} {output_text}."
    )


def codex_skill_availability(
    role: RoleDefinition,
    inline_core_skills: bool = True,
) -> list[dict[str, object]]:
    """Enable the Codex harness skill and retain explicit role-level overrides."""

    configured = [dict(item) for item in role.optional_fields.get(ROLE_SKILL_AVAILABILITY_FIELD_NAME, [])]
    if inline_core_skills or role.repository_mutation == "never":
        return configured
    if any(item.get("name") == CODEX_HARNESS_DIRECTIVES_SKILL_NAME for item in configured):
        raise ValueError(
            f"Conceptual role must not override generated Codex harness skill {CODEX_HARNESS_DIRECTIVES_SKILL_NAME}: {role.source_path}"
        )
    return [{"name": CODEX_HARNESS_DIRECTIVES_SKILL_NAME, "enabled": True}, *configured]


def role_adapter_comments(
    role: RoleDefinition,
    prefix: str,
    adapter_profile: AdapterModelProfile,
) -> str:
    model_profile = role.model_profile
    lines = [
        f"{prefix}Model profile: {model_profile} -> {adapter_profile.model}",
    ]
    model_stages = role.model_stages
    if model_stages:
        lines.append(f"{prefix}Stage model profiles:")
        lines.extend(f"{prefix}- {stage}: {profile}" for stage, profile in model_stages.items())
    lines.append(f"{prefix}Skill justifications:")
    lines.extend(
        f"{prefix}- {skill}: {role.skill_justifications[skill]}" for skill in role.skills
    )
    if role.skill_conditions:
        lines.append(f"{prefix}Request-specific skill conditions:")
        lines.extend(
            f"{prefix}- {skill}: {role.skill_conditions[skill]}"
            for skill in conditional_role_skills(role)
        )
    lines.append(f"{prefix}Output purposes:")
    lines.extend(
        f"{prefix}- {output}: {role.output_purposes[output]}"
        for output in role.output_contract
    )
    return "\n".join(lines)


def render_toml_multiline_basic_string(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return (
        f"{TOML_MULTILINE_BASIC_STRING_DELIMITER}\n"
        f"{escaped}{TOML_MULTILINE_BASIC_STRING_DELIMITER}"
    )


def codex_agent_name(role_name: str) -> str:
    """Convert a portable hyphenated role ID to a Codex runtime-safe name."""

    return role_name.replace("-", "_")


def render_codex_agent(
    role: RoleDefinition,
    model_profiles: dict[str, AdapterModelProfile],
    inline_core_skills: bool = True,
) -> str:
    profile_id = role.model_profile
    adapter_profile = model_profiles[profile_id]
    fields = [
        f"# {GENERATED_FILE_HEADER}",
        role_adapter_comments(role, "# ", adapter_profile),
        f"name = {json.dumps(codex_agent_name(role.name))}",
        f"description = {json.dumps(role.description)}",
        "developer_instructions = "
        + render_toml_multiline_basic_string(
            codex_role_instruction_text(role, inline_core_skills)
        ),
    ]
    fields.append(f"model = {json.dumps(adapter_profile.model)}")
    if adapter_profile.effort is not None:
        fields.append(f"{CODEX_REASONING_FIELD_NAME} = {json.dumps(adapter_profile.effort)}")
    isolation = role.optional_fields.get("isolation")
    if isolation == ROLE_READ_ONLY_ISOLATION:
        fields.append(f"{CODEX_SANDBOX_FIELD_NAME} = {json.dumps(isolation)}")
    for item in codex_skill_availability(role, inline_core_skills):
        fields.extend([
            "",
            "[[skills.config]]",
            f"{('name' if 'name' in item else 'path')} = {json.dumps(item.get('name', item.get('path')))}",
            f"enabled = {str(item['enabled']).lower()}",
        ])
    return "\n".join(fields) + "\n"


def render_claude_agent(
    role: RoleDefinition,
    model_profiles: dict[str, AdapterModelProfile],
    inline_core_skills: bool = True,
) -> str:
    profile_id = role.model_profile
    adapter_profile = model_profiles[profile_id]
    frontmatter: dict[str, object] = {
        ROLE_NAME_FIELD_NAME: role.name,
        ROLE_DESCRIPTION_FIELD_NAME: role.description,
    }
    if not inline_core_skills:
        frontmatter[ROLE_SKILLS_FIELD_NAME] = list(fixed_role_skills(role))
    frontmatter["model"] = adapter_profile.model
    for field_name in (
        "tools",
        "disallowedTools",
        "mcpServers",
        "maxTurns",
        "permissionMode",
        "isolation",
        "memory",
    ):
        if field_name in role.optional_fields:
            frontmatter[field_name] = role.optional_fields[field_name]
    frontmatter_text = yaml.safe_dump(frontmatter, sort_keys=False).strip()
    return (
        f"<!-- {GENERATED_FILE_HEADER}\n{role_adapter_comments(role, '', adapter_profile)}\n-->\n"
        f"---\n{frontmatter_text}\n---\n\n"
        + markdown_role_instruction_text(
            role,
            CLAUDE_ADAPTER_NAME,
            inline_core_skills,
        )
    )


def render_gemini_agent(
    role: RoleDefinition,
    model_profiles: dict[str, AdapterModelProfile],
    inline_core_skills: bool = True,
) -> str:
    profile_id = role.model_profile
    adapter_profile = model_profiles[profile_id]
    frontmatter: dict[str, object] = {
        ROLE_NAME_FIELD_NAME: role.name,
        ROLE_DESCRIPTION_FIELD_NAME: role.description,
        "kind": "local",
        "model": adapter_profile.model,
    }
    for source_field, native_field in (
        ("tools", "tools"),
        ("maxTurns", "max_turns"),
        ("timeout", "timeout_mins"),
    ):
        if source_field in role.optional_fields:
            frontmatter[native_field] = role.optional_fields[source_field]
    frontmatter_text = yaml.safe_dump(frontmatter, sort_keys=False).strip()
    return (
        f"---\n{frontmatter_text}\n---\n\n"
        f"<!-- {GENERATED_FILE_HEADER}\n{role_adapter_comments(role, '', adapter_profile)}\n-->\n\n"
        + markdown_role_instruction_text(
            role,
            GEMINI_ADAPTER_NAME,
            inline_core_skills,
        )
    )


def render_junie_agent(
    role: RoleDefinition,
    model_profiles: dict[str, AdapterModelProfile],
    inline_core_skills: bool = True,
) -> str:
    profile_id = role.model_profile
    adapter_profile = model_profiles[profile_id]
    frontmatter: dict[str, object] = {
        ROLE_NAME_FIELD_NAME: role.name,
        ROLE_DESCRIPTION_FIELD_NAME: role.description,
    }
    if not inline_core_skills:
        frontmatter[ROLE_SKILLS_FIELD_NAME] = list(fixed_role_skills(role))
    frontmatter["model"] = adapter_profile.model
    if adapter_profile.effort is not None:
        frontmatter["reasoningLevel"] = adapter_profile.effort
    for field_name in (
        "tools",
        "disallowedTools",
        "mcpServers",
        "maxTurns",
    ):
        if field_name in role.optional_fields:
            frontmatter[field_name] = role.optional_fields[field_name]
    frontmatter_text = yaml.safe_dump(frontmatter, sort_keys=False).strip()
    return (
        f"---\n{frontmatter_text}\n---\n\n"
        f"<!-- {GENERATED_FILE_HEADER}\n{role_adapter_comments(role, '', adapter_profile)}\n-->\n\n"
        + markdown_role_instruction_text(
            role,
            JUNIE_ADAPTER_NAME,
            inline_core_skills,
        )
    )


def render_agent_generation_manifest(
    roles: Sequence[RoleDefinition],
    outputs: dict[Path, str],
    inline_core_skills: bool,
) -> str:
    """Return a deterministic conceptual-definition-to-adapter inventory with expected digests."""
    adapter_specs = {
        CODEX_ADAPTER_NAME: (CODEX_AGENT_OUTPUT_ROOT, CODEX_AGENT_EXTENSION, "toml"),
        CLAUDE_ADAPTER_NAME: (CLAUDE_AGENT_OUTPUT_ROOT, CLAUDE_AGENT_EXTENSION, "markdown"),
        GEMINI_ADAPTER_NAME: (GEMINI_AGENT_OUTPUT_ROOT, GEMINI_AGENT_EXTENSION, "markdown"),
        JUNIE_ADAPTER_NAME: (JUNIE_AGENT_OUTPUT_ROOT, JUNIE_AGENT_EXTENSION, "markdown"),
    }
    adapters: dict[str, object] = {}
    for adapter_name, (output_root, extension, output_format) in adapter_specs.items():
        harness_skills = []
        for directory in adapter_skill_directories(adapter_name):
            digest = hashlib.sha256()
            for source_file in sorted(path for path in directory.rglob("*") if path.is_file()):
                if source_file.is_symlink():
                    raise ValueError(f"Adapter skill file must not be a symlink: {source_file}")
                relative = source_file.relative_to(directory).as_posix().encode("utf-8")
                payload = source_file.read_bytes()
                digest.update(len(relative).to_bytes(4, "big"))
                digest.update(relative)
                digest.update(len(payload).to_bytes(8, "big"))
                digest.update(payload)
            harness_skills.append(
                {
                    "name": directory.name,
                    "sha256": digest.hexdigest(),
                    "source": str(directory.relative_to(REPOSITORY_ROOT)),
                }
            )
        agents = []
        for role in roles:
            output_path = output_root / f"{role.filename}{extension}"
            content = outputs[output_path]
            agents.append(
                {
                    "name": role.name,
                    "output": str(output_path.relative_to(REPOSITORY_ROOT)),
                    "sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
                    "source": role.source_path,
                }
            )
        adapters[adapter_name] = {
            "agentCount": len(agents),
            "agents": agents,
            "format": output_format,
            "harnessSkills": harness_skills,
            "outputRoot": str(output_root.relative_to(REPOSITORY_ROOT)),
        }

    manifest = {
        "schema": "dev-methodology-agent-generation-manifest",
        "version": 3,
        "generator": GENERATOR_RELATIVE_PATH,
        "generationOptions": {"inlineCoreSkills": inline_core_skills},
        "canonicalRoleCount": len(roles),
        "adapters": adapters,
    }
    return json.dumps(manifest, indent=2, sort_keys=True) + "\n"


def expected_role_outputs(
    roles: Sequence[RoleDefinition],
    inline_core_skills: bool = True,
) -> dict[Path, str]:
    codex_harness_skills = set(adapter_skill_names(CODEX_ADAPTER_NAME))
    if CODEX_HARNESS_DIRECTIVES_SKILL_NAME not in codex_harness_skills:
        raise ValueError(
            f"Codex generation requires adapter skill {CODEX_HARNESS_DIRECTIVES_SKILL_NAME}"
        )
    source_profile_ids = set(load_model_profiles())
    codex_profiles = load_adapter_model_profiles(CODEX_ADAPTER_NAME, source_profile_ids)
    claude_profiles = load_adapter_model_profiles(CLAUDE_ADAPTER_NAME, source_profile_ids)
    gemini_profiles = load_adapter_model_profiles(GEMINI_ADAPTER_NAME, source_profile_ids)
    junie_profiles = load_adapter_model_profiles(JUNIE_ADAPTER_NAME, source_profile_ids)
    outputs = {ROLE_OUTPUT_PATH: render_role_javascript(roles)}
    for role in roles:
        outputs[CODEX_AGENT_OUTPUT_ROOT / f"{role.filename}{CODEX_AGENT_EXTENSION}"] = render_codex_agent(
            role, codex_profiles, inline_core_skills
        )
        outputs[CLAUDE_AGENT_OUTPUT_ROOT / f"{role.filename}{CLAUDE_AGENT_EXTENSION}"] = render_claude_agent(
            role, claude_profiles, inline_core_skills
        )
        outputs[GEMINI_AGENT_OUTPUT_ROOT / f"{role.filename}{GEMINI_AGENT_EXTENSION}"] = render_gemini_agent(
            role, gemini_profiles, inline_core_skills
        )
        outputs[JUNIE_AGENT_OUTPUT_ROOT / f"{role.filename}{JUNIE_AGENT_EXTENSION}"] = render_junie_agent(
            role, junie_profiles, inline_core_skills
        )
    outputs[AGENT_GENERATION_MANIFEST_PATH] = render_agent_generation_manifest(
        roles,
        outputs,
        inline_core_skills,
    )
    return outputs


def stale_generated_adapter_paths(expected_paths: set[Path]) -> list[Path]:
    generated_paths: set[Path] = set()
    for output_root, extension in (
        (CODEX_AGENT_OUTPUT_ROOT, CODEX_AGENT_EXTENSION),
        (CLAUDE_AGENT_OUTPUT_ROOT, CLAUDE_AGENT_EXTENSION),
        (GEMINI_AGENT_OUTPUT_ROOT, GEMINI_AGENT_EXTENSION),
        (JUNIE_AGENT_OUTPUT_ROOT, JUNIE_AGENT_EXTENSION),
    ):
        if output_root.is_dir():
            generated_paths.update(output_root.glob(f"*{extension}"))
    return sorted(generated_paths - expected_paths)


def write_role_outputs(
    roles: Sequence[RoleDefinition],
    check: bool,
    inline_core_skills: bool = True,
) -> list[Path]:
    expected_outputs = expected_role_outputs(roles, inline_core_skills)
    changed_paths = [
        path
        for path, content in expected_outputs.items()
        if not path.is_file() or path.read_text(encoding="utf-8") != content
    ]
    stale_paths = stale_generated_adapter_paths(set(expected_outputs))
    if check:
        return sorted(changed_paths + stale_paths)

    for path in stale_paths:
        path.unlink()
    for path in changed_paths:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(expected_outputs[path], encoding="utf-8")
    return sorted(changed_paths + stale_paths)


def write_output(check: bool) -> bool:
    rendered = render_javascript(build_payload())
    current = OUTPUT_PATH.read_text(encoding="utf-8") if OUTPUT_PATH.is_file() else None
    if current == rendered:
        return False
    if check:
        return True
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(rendered, encoding="utf-8")
    return True


def write_template_output(check: bool) -> bool:
    """Write generated template browser data, or report whether it is stale."""

    rendered = render_template_javascript(build_template_payload())
    current = (
        TEMPLATE_OUTPUT_PATH.read_text(encoding="utf-8")
        if TEMPLATE_OUTPUT_PATH.is_file()
        else None
    )
    if current == rendered:
        return False
    if check:
        return True
    TEMPLATE_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    TEMPLATE_OUTPUT_PATH.write_text(rendered, encoding="utf-8")
    return True


def main(arguments: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate skill, template, conceptual agent definition, adapter, and HTML documentation data."
    )
    parser.add_argument("--check", action="store_true", help="Fail when generated methodology data is stale.")
    parser.add_argument(
        "--inline-core-skills",
        type=parse_boolean,
        default=True,
        metavar="true|false",
        help="Statically append core skills to agent instructions instead of native skill properties. Defaults to true.",
    )
    args = parser.parse_args(arguments)

    try:
        skill_payload = build_payload()
        changed = write_output(args.check)
        template_changed = write_template_output(args.check)
        roles = load_role_definitions(set(skill_payload["skills"]))
        changed_role_paths = write_role_outputs(
            roles,
            args.check,
            args.inline_core_skills,
        )
    except (OSError, ValueError, yaml.YAMLError) as error:
        print(error, file=sys.stderr)
        return ERROR_EXIT_CODE

    if args.check and (changed or template_changed or changed_role_paths):
        if changed:
            print(f"stale {OUTPUT_PATH}")
        if template_changed:
            print(f"stale {TEMPLATE_OUTPUT_PATH}")
        for path in changed_role_paths:
            print(f"stale {path}")
        return ERROR_EXIT_CODE
    if changed:
        print(f"generated {OUTPUT_PATH}")
    if template_changed:
        print(f"generated {TEMPLATE_OUTPUT_PATH}")
    for path in changed_role_paths:
        print(f"generated {path}")
    if not changed and not template_changed and not changed_role_paths:
        print("Methodology documentation data is current.")
    return SUCCESS_EXIT_CODE


if __name__ == "__main__":
    raise SystemExit(main())
