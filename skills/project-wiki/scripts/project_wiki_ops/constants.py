# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Modified with AI assistance.
# Summary: Defines paths, templates, and command constants for project-wiki operations.

"""Constants for opinionated project wiki operations."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path.cwd().resolve()
WIKI_DIR = PROJECT_ROOT / "docs" / "wiki"
DIGESTS_DIR_NAME = "digests"
REQUIRED_WIKI_FILES = (
    "README.md",
    "schema.md",
    "topic-index.md",
    "glossary.md",
    "open-decisions.md",
    "known-defects.md",
    "maintenance-log.md",
)
INDEX_PAGE_NAME = "index.md"
MARKDOWN_FILE_PATTERN = "*.md"
MARKDOWN_FILE_SUFFIX = ".md"
TOPIC_REQUIRED_HEADINGS = (
    "## Current Understanding",
    "## Authoritative Sources",
    "## Related Code",
    "## Related Tests",
    "## Related Backlog Items",
    "## Related Wiki Pages",
    "## Open Questions",
    "## Maintenance Notes",
)
EXEMPT_SCHEMA_FILES = {
    "README.md",
    "schema.md",
    "topic-index.md",
    "glossary.md",
    "open-decisions.md",
    "known-defects.md",
    "maintenance-log.md",
}
SOURCE_TO_WIKI_PATTERNS = (
    ("backlog/defect-backlog/", "docs/wiki/known-defects.md"),
    ("backlog/feature-backlog/", "docs/wiki/topic-index.md"),
    ("backlog/", "docs/wiki/topic-index.md"),
    ("docs/architecture/", "docs/wiki/topic-index.md"),
    ("docs/plans/", "docs/wiki/topic-index.md"),
    ("docs/requirements/", "docs/wiki/topic-index.md"),
    ("docs/spec", "docs/wiki/topic-index.md"),
    ("docs/rag/", "docs/wiki/topic-index.md"),
    ("docs/help/", "docs/wiki/topic-index.md"),
    ("procedure-", "docs/wiki/topic-index.md"),
    ("AGENTS.md", "docs/wiki/topic-index.md"),
    ("README.md", "docs/wiki/topic-index.md"),
)
ROOT_RELATIVE_PREFIXES = (
    ".agents/",
    "AGENTS.md",
    "README.md",
    "backlog/",
    "docs/",
    "procedure-",
    "src/",
    "tests/",
)
RAW_SOURCE_PATH_SEGMENT = "raw"
GIT_CHANGED_COMMAND = ("git", "status", "--porcelain")
RIPGREP_SEARCH_COMMAND = (
    "rg",
    "--files-with-matches",
    "--fixed-strings",
    "--ignore-case",
    "--glob",
    MARKDOWN_FILE_PATTERN,
)
GREP_SEARCH_COMMAND = (
    "grep",
    "--recursive",
    "--ignore-case",
    "--files-with-matches",
    "--fixed-strings",
    f"--include={MARKDOWN_FILE_PATTERN}",
)
MAX_DISPLAY_ITEMS = 80
MIN_LEAF_TITLE_ALNUM_COUNT = 3
OPEN_QUESTIONS_HEADING = "## Open Questions"
SECTION_HEADING_PREFIX = "## "
MARKDOWN_HEADING_PREFIX = "#"
CODE_FENCE_MARKER = "```"
LIST_ITEM_PREFIX = "- "
CONTINUATION_PREFIX = "  "
NO_OPEN_QUESTIONS_PREFIX = "No open wiki questions are recorded"
TEXT_FORMAT = "text"
JSON_FORMAT = "json"
OUTPUT_FORMATS = (TEXT_FORMAT, JSON_FORMAT)
OKF_VERSION = "0.1"
OKF_RESERVED_FILE_NAMES = {
    "index.md",
    "log.md",
}
OKF_REQUIRED_FRONTMATTER_FIELD = "type"
OKF_FRONTMATTER_DELIMITER = "---"
OKF_DESCRIPTION_MAX_LENGTH = 180
OKF_DEFAULT_TYPE = "Topic"
OKF_PATH_TYPES = {
    "agentic-frameworks": "Agentic Framework",
    "application-patterns": "Application Pattern",
    "adoption-and-operating-model": "Adoption And Operating Model",
    "coding-practices": "Coding Practice",
    "companies": "Company",
    "context-architecture": "Context Architecture",
    "developer-tools": "Developer Tool",
    "digests": "Digest",
    "governance-and-risk": "Governance And Risk",
    "mcp-servers": "MCP Server",
    "model-file-formats": "Model File Format",
    "models": "Model",
    "products": "Product",
    "prompt-and-instructions": "Prompt And Instructions",
    "retrieval-and-tools": "Retrieval And Tools",
    "source-workflows": "Source Workflow",
    "subsystems": "Subsystem",
    "techniques": "Technique",
    "verification-and-evals": "Verification And Eval",
}
OKF_ROOT_FILE_TYPES = {
    "README.md": "Project Wiki",
    "schema.md": "Wiki Schema",
    "topic-index.md": "Topic Index",
    "glossary.md": "Glossary",
    "open-decisions.md": "Decision Log",
    "known-defects.md": "Defect Summary",
    "maintenance-log.md": "Maintenance Log",
}
OKF_DESCRIPTION_STOP_SUFFIXES = (".", "!", "?")
