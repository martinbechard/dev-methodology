# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies the dependency-free workflow evaluation fixtures and their model-input safety.

from __future__ import annotations

import re
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECTS_ROOT = ROOT / "evals" / "projects"
WORKFLOW_FIXTURES = {
    "documentation-functional-spec": (
        "sources/product-requirements.md",
        "sources/http-contract.md",
        "sources/acceptance-evidence.md",
    ),
    "project-configuration-routing": (
        "README.md",
        "available-skills.txt",
        "docs/architecture.md",
        "services/api/pyproject.toml",
        "apps/web/package.json",
        "automation/pipeline.yaml",
    ),
    "wiki-raw-ingest": (
        "raw/2026-07-15-order-cancellation.md",
        "docs/wiki/topic-index.md",
        "docs/wiki/orders/order-lifecycle.md",
        "docs/wiki/digests/2026-07.md",
    ),
    "backlog-lifecycle": (
        "backlog/feature-backlog/retry-policy.md",
        ".backlog-state/claims/retry-policy.yaml",
        ".backlog-state/logs/retry-policy.log",
    ),
}
EXPECTED_AGENT_OUTPUTS = {
    "documentation-functional-spec": (
        "docs/functional-specifications/order-cancellation.md",
        "eval-result.md",
    ),
    "project-configuration-routing": (
        "PROJECT.yaml",
        "AGENTS.md",
        "eval-result.md",
    ),
    "wiki-raw-ingest": (
        "docs/wiki/orders/order-cancellation.md",
        "raw/processed/2026-07-15-order-cancellation.md",
        "eval-result.md",
    ),
    "backlog-lifecycle": (
        "backlog-status.md",
        "eval-result.md",
    ),
}
SENSITIVE_PATTERNS = (
    re.compile(rb"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.IGNORECASE),
    re.compile(rb"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(
        rb"(?:api[_-]?key|access[_-]?token|client[_-]?secret)\s*[:=]",
        re.IGNORECASE,
    ),
    re.compile(
        rb"(?:company|customer)[_ -]?(?:confidential|internal)",
        re.IGNORECASE,
    ),
)


class WorkflowFixtureTests(unittest.TestCase):
    """Protect the source state and privacy boundary of non-code workflow fixtures."""

    def test_fixture_sources_exist_and_agent_outputs_do_not(self) -> None:
        """Each fixture begins with complete evidence and without a precomputed answer."""

        for fixture_name, required_paths in WORKFLOW_FIXTURES.items():
            with self.subTest(fixture=fixture_name):
                fixture_root = PROJECTS_ROOT / fixture_name
                self.assertTrue((fixture_root / "TASK.md").is_file())
                for relative_path in required_paths:
                    self.assertTrue((fixture_root / relative_path).is_file(), relative_path)
                for relative_path in EXPECTED_AGENT_OUTPUTS[fixture_name]:
                    self.assertFalse((fixture_root / relative_path).exists(), relative_path)

    def test_model_visible_fixture_sources_are_synthetic_and_non_sensitive(self) -> None:
        """No staged workflow source contains a credential, private key, or PII pattern."""

        for fixture_name in WORKFLOW_FIXTURES:
            fixture_root = PROJECTS_ROOT / fixture_name
            for path in fixture_root.rglob("*"):
                if not path.is_file():
                    continue
                content = path.read_bytes()
                for pattern in SENSITIVE_PATTERNS:
                    self.assertIsNone(
                        pattern.search(content),
                        f"sensitive model-visible input in {path.relative_to(ROOT)}",
                    )

    def test_workflow_fixtures_contain_no_source_code(self) -> None:
        """The model-visible fixtures avoid code headers that carry personal attribution."""

        source_suffixes = {".c", ".cc", ".go", ".java", ".js", ".py", ".ts", ".tsx"}
        for fixture_name in WORKFLOW_FIXTURES:
            fixture_root = PROJECTS_ROOT / fixture_name
            source_files = [
                path.relative_to(fixture_root).as_posix()
                for path in fixture_root.rglob("*")
                if path.is_file() and path.suffix in source_suffixes
            ]
            self.assertEqual([], source_files, fixture_name)

    def test_wiki_fixture_is_a_valid_pre_ingest_baseline(self) -> None:
        """The wiki task starts from a lint-clean and OKF-valid source state."""

        fixture_root = PROJECTS_ROOT / "wiki-raw-ingest"
        wiki_ops = ROOT / "skills" / "project-wiki" / "scripts" / "wiki_ops.py"
        for operation in ("status", "lint", "okf-validate"):
            completed = subprocess.run(
                [sys.executable, str(wiki_ops), operation],
                cwd=fixture_root,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(
                0,
                completed.returncode,
                f"{operation} failed:\n{completed.stdout}\n{completed.stderr}",
            )

    def test_backlog_fixture_has_no_terminal_delivery_evidence(self) -> None:
        """The interrupted item remains active and cannot be inferred complete."""

        fixture_root = PROJECTS_ROOT / "backlog-lifecycle"
        self.assertTrue((fixture_root / "backlog/feature-backlog/retry-policy.md").is_file())
        self.assertFalse((fixture_root / ".backlog-state/results/retry-policy.yaml").exists())
        self.assertFalse(
            (fixture_root / "backlog/completed-backlog/features/retry-policy.md").exists()
        )


if __name__ == "__main__":
    unittest.main()
