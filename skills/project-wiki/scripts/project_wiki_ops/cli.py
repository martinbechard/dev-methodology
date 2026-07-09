"""Command-line interface for project wiki operations."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .constants import JSON_FORMAT, MAX_DISPLAY_ITEMS, OUTPUT_FORMATS, TEXT_FORMAT, WIKI_DIR
from .core import (
    changed_files,
    extract_open_questions,
    extract_local_paths,
    init_wiki,
    link_leaf_mentions,
    lint_wiki,
    read_text,
    relative_path,
    stable_path_key,
    suggested_pages,
    wiki_pages,
)
from .models import LintResult
from .okf import (
    migrate_wiki_to_okf,
    okf_summary,
    validate_okf_wiki,
)


def print_init() -> int:
    created = init_wiki()
    if not created:
        print("Project wiki already has the standard scaffold.")
        return 0
    print("Project wiki scaffold created")
    for path in created:
        print(f"- {relative_path(path)}")
    return 0


def print_status() -> int:
    findings = lint_wiki()
    print("Project wiki status")
    print(f"Wiki directory: {relative_path(WIKI_DIR)}")
    print(f"Page count: {len(wiki_pages())}")
    print(f"Missing required files: {missing_count(findings)}")
    print(f"Lint findings: {len(findings)}")
    if findings:
        print("")
        print_lint_findings(findings)
    return 1 if findings else 0


def missing_count(findings: list[LintResult]) -> int:
    return sum(1 for finding in findings if finding.message == "required wiki file is missing")


def print_lint() -> int:
    findings = lint_wiki()
    if not findings:
        print("Project wiki lint passed.")
        return 0
    print_lint_findings(findings)
    return 1


def print_okf_validate() -> int:
    findings = validate_okf_wiki()
    if not findings:
        print("OKF validation passed.")
        return 0
    print_lint_findings(findings)
    return 1


def print_okf_migrate(dry_run: bool) -> int:
    results = migrate_wiki_to_okf(dry_run=dry_run)
    changed_count, concept_count = okf_summary(results)
    action = "would update" if dry_run else "updated"
    print(f"OKF migration {action} {changed_count} of {concept_count} concept documents.")
    if changed_count:
        for result in [item for item in results if item.changed][:MAX_DISPLAY_ITEMS]:
            print(f"- {relative_path(result.path)}")
        if changed_count > MAX_DISPLAY_ITEMS:
            remaining_count = changed_count - MAX_DISPLAY_ITEMS
            print(f"- ... {remaining_count} more documents")
    return 0


def print_lint_findings(findings: list[LintResult]) -> None:
    for finding in findings[:MAX_DISPLAY_ITEMS]:
        print(f"- {stable_path_key(finding.path)}: {finding.message}")
    if len(findings) > MAX_DISPLAY_ITEMS:
        remaining_count = len(findings) - MAX_DISPLAY_ITEMS
        print(f"- ... {remaining_count} more findings")


def print_suggest(use_changed: bool, paths: list[str]) -> int:
    source_paths = changed_files() if use_changed else paths
    suggestions = suggested_pages(source_paths)
    if not source_paths:
        print("No source paths provided or detected.")
        return 0
    print("Project wiki suggestions")
    for source_path in source_paths:
        print(f"- source: {source_path}")
    if not suggestions:
        print("")
        print("No mapped wiki pages found. Consider docs/wiki/topic-index.md or a new topic page.")
        return 0
    print("")
    print("Likely wiki updates")
    for wiki_page, sources in sorted(suggestions.items()):
        print(f"- {wiki_page}")
        for source in sorted(sources):
            print(f"  source: {source}")
    return 0


def print_sources(page_path: str) -> int:
    page = WIKI_DIR.parent.parent / page_path
    if not page.exists():
        print(f"Wiki page not found: {page_path}", file=sys.stderr)
        return 1
    paths = extract_local_paths(read_text(page))
    if not paths:
        print("No local source paths found.")
        return 0
    for source_path in paths:
        print(source_path)
    return 0


def print_questions(output_format: str) -> int:
    questions = extract_open_questions()
    if output_format == JSON_FORMAT:
        print(
            json.dumps(
                [
                    {
                        "file": relative_path(question.path),
                        "line": question.line,
                        "question": question.question,
                    }
                    for question in questions
                ],
                indent=2,
            )
        )
        return 0

    if not questions:
        print("No open wiki questions found.")
        return 0

    print(f"Open wiki questions: {len(questions)}")
    current_path = ""
    for question in questions:
        question_path = relative_path(question.path)
        if question_path != current_path:
            current_path = question_path
            print("")
            print(question_path)
        print(f"  line {question.line}: {question.question}")
    return 0


def print_link_leaves(dry_run: bool, leaves: list[str]) -> int:
    changes = link_leaf_mentions(leaves or None, dry_run)
    title = "Leaf link candidates" if dry_run else "Leaf link updates"
    print(title)
    if not changes:
        print("No leaf links to add.")
        return 0

    for change in changes[:MAX_DISPLAY_ITEMS]:
        print(
            f"- {relative_path(change.target_path)} -> {relative_path(change.leaf_path)} "
            f"({change.title})"
        )
    if len(changes) > MAX_DISPLAY_ITEMS:
        remaining_count = len(changes) - MAX_DISPLAY_ITEMS
        print(f"- ... {remaining_count} more changes")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Project wiki operations")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("init", help="Create the standard docs/wiki scaffold if missing")
    subparsers.add_parser("status", help="Report wiki status and lint findings")
    subparsers.add_parser("lint", help="Run wiki lint checks")
    okf_validate_parser = subparsers.add_parser("okf-validate", help="Validate OKF frontmatter conformance")
    okf_validate_parser.set_defaults(command="okf-validate")
    okf_migrate_parser = subparsers.add_parser("okf-migrate", help="Add or refresh OKF frontmatter")
    okf_migrate_parser.add_argument("--dry-run", action="store_true", help="Show documents that would change")
    suggest_parser = subparsers.add_parser("suggest", help="Suggest wiki pages for source paths")
    suggest_parser.add_argument("paths", nargs="*", help="Source paths to map to wiki pages")
    suggest_parser.add_argument("--changed", action="store_true", help="Use files changed since HEAD")
    sources_parser = subparsers.add_parser("sources", help="Extract local source paths from a wiki page")
    sources_parser.add_argument("page", help="Wiki page path")
    questions_parser = subparsers.add_parser("questions", help="Extract open wiki questions with file and line")
    questions_parser.add_argument("--format", choices=OUTPUT_FORMATS, default=TEXT_FORMAT, help="Output format")
    link_leaves_parser = subparsers.add_parser(
        "link-leaves",
        help="Link existing wiki mentions to durable leaf pages",
    )
    link_leaves_parser.add_argument("leaves", nargs="*", help="Leaf page paths to link; defaults to all wiki leaves")
    link_leaves_parser.add_argument("--dry-run", action="store_true", help="Show link candidates without editing pages")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "init":
        return print_init()
    if args.command == "status":
        return print_status()
    if args.command == "lint":
        return print_lint()
    if args.command == "okf-validate":
        return print_okf_validate()
    if args.command == "okf-migrate":
        return print_okf_migrate(args.dry_run)
    if args.command == "suggest":
        return print_suggest(args.changed, args.paths)
    if args.command == "sources":
        return print_sources(args.page)
    if args.command == "questions":
        return print_questions(args.format)
    if args.command == "link-leaves":
        return print_link_leaves(args.dry_run, args.leaves)
    parser.error(f"unknown command: {args.command}")
    return 1
