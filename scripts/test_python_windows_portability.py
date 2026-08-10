# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Inventories every tracked Python file and verifies the repository's native Windows portability contract.

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path, PureWindowsPath
from typing import Iterable, Sequence
from unittest import mock


_ROOT = Path(__file__).resolve().parents[1]
_SELF = "scripts/test_python_windows_portability.py"
_PORTABLE = "portable and exercised"
_CORRECTED = "corrected by this item"
_PLATFORM_SPECIFIC = "deliberately platform-specific"
_FIXTURE = "non-entry-point fixture data exercised by an owning test"


class _InventoryError(RuntimeError):
    """Report a tracked-file mismatch in the committed Windows inventory."""


def _paths(raw: str) -> frozenset[str]:
    """Parse one duplicate-free newline inventory into repository-relative paths."""
    values = tuple(line.strip() for line in raw.splitlines() if line.strip())
    if len(values) != len(set(values)):
        raise _InventoryError("A Windows inventory group contains a duplicate path.")
    return frozenset(values)


_PORTABLE_PATHS = _paths(
    """
evals/agent-tests/dev-artifact-reviewer/checklist_contract.py
evals/agent-tests/dev-artifact-reviewer/test_checklist_contract.py
evals/agent-tests/dev-backlog-coordinator/coordination_simulator.py
evals/agent-tests/dev-backlog-coordinator/test_coordination_simulator.py
evals/agent-tests/dev-backlog-watchdog/test_watchdog_simulator.py
evals/agent-tests/dev-backlog-watchdog/watchdog_simulator.py
evals/agent-tests/dev-coder/test_fixtures.py
evals/agent-tests/dev-documentation-writer/test_fixtures.py
evals/agent-tests/dev-merge-coordinator/test_fixtures.py
evals/agent-tests/dev-orchestrator/test_fixtures.py
evals/agent-tests/dev-security-reviewer/route_selection.py
evals/agent-tests/dev-security-reviewer/test_route_selection.py
evals/agent-tests/methodology-design-system-checklist-runner/contract.py
evals/agent-tests/methodology-design-system-checklist-runner/test_contract.py
evals/agent-tests/methodology-design-system-review-coordinator/coordination_simulator.py
evals/agent-tests/methodology-design-system-review-coordinator/test_coordination_simulator.py
evals/agent-tests/project-bootstrapper/live_smoke.py
evals/agent-tests/project-bootstrapper/test_fixtures.py
evals/agent-tests/project-configurator/test_fixtures.py
evals/agent-tests/suite_reporting.py
evals/agent-tests/test_suite_reporting.py
evals/agent-tests/wiki-artifact-reviewer/quotation_traceability.py
evals/agent-tests/wiki-artifact-reviewer/test_quotation_traceability.py
evals/agent-tests/wiki-researcher/test_source_links.py
scripts/agent_skill_evals/__init__.py
scripts/agent_skill_evals/judges.py
scripts/agent_skill_evals/validation.py
scripts/agent_skill_judge_contract.py
scripts/build-agent-skill-evaluation-docs.py
scripts/build-agent-skill-hierarchy.py
scripts/build-skill-docs.py
scripts/build-support-checklist.py
scripts/build-technology-detection.py
scripts/detect-technology-skills.py
scripts/generate-backlog-report.py
scripts/install-skills.py
scripts/openai_metadata.py
scripts/render-agents-technology-skills.py
scripts/skill_sources.py
scripts/test_agent_and_skill_definitions_outline.py
scripts/test_agent_identity_generation.py
scripts/test_agent_skill_hierarchy.py
scripts/test_agent_skill_judge_contract.py
scripts/test_bundle_content.py
scripts/test_codex_agent_names.py
scripts/test_codex_task_control.py
scripts/test_deliver_work_item_feature_branch.py
scripts/test_documentation_design_system.py
scripts/test_effective_communication.py
scripts/test_eval_coverage_catalog.py
scripts/test_eval_workflow_fixtures.py
scripts/test_github_work_item_provider_fixture.py
scripts/test_main_branch_completion_contract.py
scripts/test_openai_metadata.py
scripts/test_optional_resource_coordination_workflow_skills.py
scripts/test_path_limited_backlog_git.py
scripts/test_project_document_provenance.py
scripts/test_project_shared_agent_skills.py
scripts/test_provider_family_naming.py
scripts/test_python_windows_portability.py
scripts/test_resource_claim_helper.py
scripts/test_role_mutation_policy.py
scripts/test_skill_lifecycle_documentation.py
scripts/test_ste_technical_writing.py
scripts/test_tailwind_design_system.py
scripts/test_technology_detection.py
scripts/test_terminology_standard_effect_fixture.py
scripts/test_validate_agent_skills.py
scripts/test_work_item_coordination.py
scripts/validate-agent-skills.py
skills/detect-technology-skills/scripts/detect.py
skills/document-provenance/scripts/test_validate_document_provenance.py
skills/document-provenance/scripts/validate_document_provenance.py
skills/project-wiki/scripts/project_wiki_ops/__init__.py
skills/project-wiki/scripts/project_wiki_ops/cli.py
skills/project-wiki/scripts/project_wiki_ops/constants.py
skills/project-wiki/scripts/project_wiki_ops/core.py
skills/project-wiki/scripts/project_wiki_ops/models.py
skills/project-wiki/scripts/project_wiki_ops/okf.py
skills/project-wiki/scripts/test_leaf_linking.py
skills/project-wiki/scripts/test_okf.py
skills/project-wiki/scripts/test_open_questions.py
skills/project-wiki/scripts/test_raw_source_links.py
skills/project-wiki/scripts/test_setup_guidance.py
skills/project-wiki/scripts/wiki_ops.py
"""
)

_CORRECTED_PATHS = {
    "scripts/test_resource_claim.py": (
        "The direct fcntl crash fixture was POSIX-only, and symbolic-link setup lacked a "
        "capability gate. The file now skips only those unavailable OS-specific fixtures."
    ),
    "skills/resource-claim-helper-command/scripts/claim.py": (
        "The module imported fcntl unconditionally and called flock directly. It now keeps "
        "same-descriptor blocking locks through fcntl on POSIX and msvcrt on Windows."
    ),
}

_PLATFORM_SPECIFIC_PATHS = _paths(
    """
evals/agent-tests/dev-backlog-steward/contract_harness.py
evals/agent-tests/dev-backlog-steward/test_contract.py
evals/agent-tests/dev-code-reviewer/test_fixtures.py
evals/agent-tests/dev-runtime-diagnostician/test_fixtures.py
evals/agent-tests/project-bootstrapper/scripted_orchestration.py
evals/agent-tests/project-bootstrapper/test_scripted_orchestration.py
evals/agent-tests/runner.py
evals/agent-tests/test_runner.py
evals/agent-tests/test_workspace_inventory.py
evals/agent-tests/wiki-ingester/executable_harness.py
evals/agent-tests/wiki-ingester/test_contract.py
evals/agent-tests/wiki-writer/executable_harness.py
evals/agent-tests/wiki-writer/test_contract.py
evals/agent-tests/workspace_inventory.py
scripts/agent_skill_evals/commands.py
scripts/agent_skill_evals/invocations.py
scripts/agent_skill_evals/staging.py
scripts/agent_skill_evals/workspace.py
scripts/run-agent-skill-evals.py
scripts/test_agent_skill_evals.py
scripts/test_agent_skill_evaluation_docs.py
scripts/test_generate_backlog_report.py
scripts/test_install_skills.py
"""
)

_FIXTURE_PATHS = _paths(
    """
evals/agent-tests/dev-code-reviewer/fixtures/header-policy-authority-boundary/evaluate_synthesis.py
evals/agent-tests/dev-code-reviewer/fixtures/header-policy-authority-boundary/stage_candidate.py
evals/agent-tests/dev-code-reviewer/fixtures/incomplete-review-evidence/migration.py
evals/agent-tests/dev-code-reviewer/fixtures/incomplete-review-evidence/test_migration.py
evals/agent-tests/dev-code-reviewer/fixtures/justified-clean-review/retry_policy.py
evals/agent-tests/dev-code-reviewer/fixtures/justified-clean-review/test_retry_policy.py
evals/agent-tests/dev-coder/fixtures/insufficient-contract-authority/pricing.py
evals/agent-tests/dev-coder/fixtures/insufficient-contract-authority/test_pricing.py
evals/agent-tests/dev-documentation-writer/fixtures/module-design-template-conformance/src/inventory.py
evals/agent-tests/dev-documentation-writer/fixtures/module-design-template-conformance/tests/test_inventory.py
evals/agent-tests/dev-documentation-writer/fixtures/module-design-template-conformance/validate_fixture.py
evals/agent-tests/dev-orchestrator/fixtures/dependency-routing/src/dependency_status.py
evals/agent-tests/dev-orchestrator/fixtures/dependency-routing/tests/test_dependency_status.py
evals/agent-tests/dev-orchestrator/fixtures/dependency-routing/validate_fixture.py
evals/agent-tests/dev-runtime-diagnostician/fixtures/retained-process-port/lifecycle_probe.py
evals/agent-tests/dev-runtime-diagnostician/fixtures/retained-process-port/service.py
evals/agent-tests/dev-runtime-diagnostician/fixtures/retained-process-port/socket_child.py
evals/agent-tests/dev-runtime-diagnostician/fixtures/unavailable-runtime-dependency/app.py
evals/agent-tests/dev-runtime-diagnostician/fixtures/unavailable-runtime-dependency/test_app.py
evals/agent-tests/dev-runtime-diagnostician/fixtures/worker-stall-competing-hypotheses/reproduce.py
evals/agent-tests/dev-runtime-diagnostician/fixtures/worker-stall-competing-hypotheses/test_worker.py
evals/agent-tests/dev-runtime-diagnostician/fixtures/worker-stall-competing-hypotheses/worker.py
evals/agent-tests/methodology-design-system-checklist-runner/fixtures/documentation-design-system-review-no-interaction/verify.py
evals/agent-tests/methodology-design-system-checklist-runner/fixtures/documentation-design-system-review/verify.py
evals/agent-tests/methodology-design-system-review-coordinator/fixtures/coordination/verify.py
evals/agent-tests/project-bootstrapper/fixtures/invalid-configuration-no-authority/src/service.py
evals/agent-tests/project-bootstrapper/fixtures/invalid-configuration-no-authority/validate_fixture.py
evals/agent-tests/project-bootstrapper/fixtures/missing-configuration-multi-contribution/src/catalog.py
evals/agent-tests/project-bootstrapper/fixtures/missing-configuration-multi-contribution/src/orders.py
evals/agent-tests/project-bootstrapper/fixtures/missing-configuration-multi-contribution/tests/test_catalog.py
evals/agent-tests/project-bootstrapper/fixtures/missing-configuration-multi-contribution/tests/test_orders.py
evals/agent-tests/project-bootstrapper/fixtures/missing-configuration-multi-contribution/validate_fixture.py
evals/agent-tests/project-bootstrapper/fixtures/valid-configuration-direct-path/src/inventory.py
evals/agent-tests/project-bootstrapper/fixtures/valid-configuration-direct-path/test_inventory.py
evals/agent-tests/project-bootstrapper/fixtures/valid-configuration-direct-path/validate_fixture.py
evals/agent-tests/project-configurator/fixtures/technology-routing/service/main.py
evals/agent-tests/project-configurator/fixtures/valid-configuration-reuse/worker/__init__.py
evals/agent-tests/project-configurator/fixtures/valid-configuration-reuse/worker/main.py
evals/agent-tests/project-configurator/fixtures/valid-configuration-reuse/worker/test_main.py
evals/agent-tests/wiki-ingester/fixtures/scenario-files/final-evidence-audit-read-only/src/catalog.py
evals/agent-tests/wiki-ingester/fixtures/stage_fixture.py
evals/agent-tests/wiki-researcher/fixtures/wiki-research/validate_links.py
evals/projects/documentation-design-system-review/verify.py
evals/projects/fastapi-orders/app/main.py
evals/projects/file-work-item-template-contract/verify.py
evals/projects/github-work-item-provider/mock_github.py
evals/projects/github-work-item-provider/verify.py
evals/projects/java-comment-placement/verify.py
evals/projects/python-inventory/src/inventory.py
evals/projects/terminology-standard-effect/negative-activation/verify.py
"""
)

_PLATFORM_SPECIFIC_REASON = (
    "This evaluation or test boundary intentionally depends on POSIX process groups, signals, "
    "UID or mode-bit security checks, executable bits, or unrestricted symbolic-link creation. "
    "Native Windows verification compiles it and reports the bounded exclusion instead of "
    "weakening those containment semantics."
)
_FIXTURE_REASON = (
    "This file is non-entry-point evaluation data. Native Windows verification compiles it, "
    "while its portable owning fixture test validates the intended use when applicable."
)


def _inventory() -> dict[str, tuple[str, str]]:
    """Return every classified path with its disposition and concrete reason."""
    groups: tuple[tuple[Iterable[str], str, str], ...] = (
        (
            _PORTABLE_PATHS,
            _PORTABLE,
            "The file compiles on every supported runtime and is covered by a native command, test, or owning contract.",
        ),
        (_CORRECTED_PATHS, _CORRECTED, ""),
        (_PLATFORM_SPECIFIC_PATHS, _PLATFORM_SPECIFIC, _PLATFORM_SPECIFIC_REASON),
        (_FIXTURE_PATHS, _FIXTURE, _FIXTURE_REASON),
    )
    result: dict[str, tuple[str, str]] = {}
    for paths, disposition, shared_reason in groups:
        for path in paths:
            if path in result:
                raise _InventoryError(f"Python path has more than one disposition: {path}")
            reason = _CORRECTED_PATHS[path] if disposition == _CORRECTED else shared_reason
            result[path] = (disposition, reason)
    return result


_INVENTORY = _inventory()


def _git_executable() -> str:
    """Return Git through platform-aware executable discovery."""
    executable = shutil.which("git")
    if executable is None:
        raise RuntimeError("Git is required for the tracked Python inventory.")
    return executable


def _run(
    arguments: Sequence[str],
    *,
    cwd: Path = _ROOT,
    environment: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    """Run one shell-free command and return captured text output."""
    return subprocess.run(
        list(arguments),
        cwd=cwd,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
    )


def _tracked_python_files() -> frozenset[str]:
    """Read every tracked Python path from the repository index."""
    completed = _run([_git_executable(), "-C", str(_ROOT), "ls-files", "--", "*.py"])
    if completed.returncode != 0:
        raise RuntimeError(f"Cannot inventory tracked Python files: {completed.stderr.strip()}")
    return frozenset(line for line in completed.stdout.splitlines() if line)


def _validate_inventory(tracked: Iterable[str]) -> None:
    """Reject unclassified tracked paths and stale classifications."""
    tracked_paths = frozenset(tracked)
    classified_paths = frozenset(_INVENTORY)
    unclassified = sorted(tracked_paths - classified_paths)
    stale = sorted(classified_paths - tracked_paths)
    if unclassified or stale:
        details = []
        if unclassified:
            details.append("unclassified=" + ", ".join(unclassified))
        if stale:
            details.append("not-tracked=" + ", ".join(stale))
        raise _InventoryError("Python inventory mismatch: " + "; ".join(details))


def _compile_inventory() -> None:
    """Compile every classified file without creating bytecode artifacts."""
    failures: list[str] = []
    for relative_path in sorted(_INVENTORY):
        path = _ROOT / relative_path
        try:
            compile(path.read_bytes(), relative_path, "exec", dont_inherit=True)
        except (OSError, SyntaxError, UnicodeError) as error:
            failures.append(f"{relative_path}: {error}")
    if failures:
        raise RuntimeError("Python compilation failures:\n" + "\n".join(failures))


def _load_claim_helper() -> object:
    """Import the corrected command helper in its intended repository context."""
    path = _ROOT / "skills/resource-claim-helper-command/scripts/claim.py"
    spec = importlib.util.spec_from_file_location("windows_portability_claim_helper", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot create an import specification for {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _symlink_capability() -> tuple[bool, str]:
    """Probe symbolic-link creation without assuming Windows policy or privilege."""
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        target = root / "target.txt"
        link = root / "link.txt"
        target.write_text("target\n", encoding="utf-8")
        try:
            link.symlink_to(target.name)
        except OSError as error:
            return False, f"symbolic-link creation unavailable: {error}"
        if link.read_text(encoding="utf-8") != "target\n":
            return False, "symbolic-link target did not preserve content"
        link.unlink()
        return True, "symbolic-link creation available"


def _claim_round_trip() -> None:
    """Exercise the platform lock through one isolated acquire, status, and release."""
    git = _git_executable()
    claim_script = _ROOT / "skills/resource-claim-helper-command/scripts/claim.py"
    with tempfile.TemporaryDirectory() as directory:
        repository = Path(directory) / "repository with spaces"
        repository.mkdir()
        (repository / ".gitignore").write_text(
            "/.worktrees/\n/.codex/agent-claim/\n", encoding="utf-8"
        )
        (repository / "README.md").write_text("lock smoke\n", encoding="utf-8")
        for command in (
            [git, "init", "--quiet", str(repository)],
            [git, "-C", str(repository), "config", "user.name", "Portability Test"],
            [git, "-C", str(repository), "config", "user.email", "portability@example.invalid"],
            [git, "-C", str(repository), "add", "."],
            [git, "-C", str(repository), "commit", "--quiet", "-m", "fixture"],
        ):
            completed = _run(command)
            if completed.returncode != 0:
                raise RuntimeError(f"Lock-smoke setup failed: {completed.stderr.strip()}")

        base = [sys.executable, str(claim_script), "--repo", str(repository)]
        acquire = _run(
            [
                *base,
                "acquire",
                "--claim-id",
                "windows-portability-lock-smoke",
                "--agent",
                "windows-portability-verifier",
                "--task",
                "windows-portability-verifier",
                "--root-task-id",
                "windows-portability-verifier",
                "--file",
                "README.md",
            ]
        )
        status = _run([*base, "status"])
        release = _run([*base, "release", "--claim-id", "windows-portability-lock-smoke"])
        outcomes = []
        for completed in (acquire, status, release):
            if completed.returncode != 0:
                raise RuntimeError(
                    "Claim lock smoke failed:\n" + completed.stdout + completed.stderr
                )
            outcomes.append(json.loads(completed.stdout)["outcome"])
        if outcomes != ["SHARED_CHECKOUT_ACQUIRED", "STATUS", "RELEASED"]:
            raise RuntimeError(f"Unexpected claim lock outcomes: {outcomes}")


class WindowsPortabilityContractTests(unittest.TestCase):
    """Verify inventory completeness and OS-sensitive standard-library behavior."""

    def test_every_tracked_python_file_has_one_disposition(self) -> None:
        _validate_inventory(_tracked_python_files())

    def test_an_unclassified_python_file_fails_the_inventory(self) -> None:
        with self.assertRaisesRegex(_InventoryError, "unclassified=unclassified_probe.py"):
            _validate_inventory(_tracked_python_files() | {"unclassified_probe.py"})

    def test_every_inventory_file_compiles(self) -> None:
        _compile_inventory()

    def test_corrected_claim_helper_imports_and_locks(self) -> None:
        module = _load_claim_helper()
        self.assertTrue(callable(getattr(module, "main", None)))
        _claim_round_trip()

    def test_windows_drive_and_unc_paths_remain_structured(self) -> None:
        drive = PureWindowsPath("C:/repository/scripts/tool.py")
        unc = PureWindowsPath("//server/share/repository/scripts/tool.py")
        self.assertEqual("C:", drive.drive)
        self.assertEqual("\\\\server\\share", unc.drive)
        self.assertEqual("tool.py", drive.name)
        self.assertEqual("tool.py", unc.name)

    def test_temporary_root_environment_and_cleanup_are_deterministic(self) -> None:
        previous_tempdir = tempfile.tempdir
        with tempfile.TemporaryDirectory() as directory:
            configured = Path(directory) / "temporary root with spaces"
            configured.mkdir()
            try:
                with mock.patch.dict(
                    os.environ,
                    {"TMPDIR": str(configured), "TEMP": str(configured), "TMP": str(configured)},
                ):
                    tempfile.tempdir = None
                    self.assertEqual(configured.resolve(), Path(tempfile.gettempdir()).resolve())
                    with tempfile.NamedTemporaryFile(dir=configured, delete=False) as temporary:
                        temporary.write(b"temporary bytes")
                        temporary_path = Path(temporary.name)
                    self.assertEqual(b"temporary bytes", temporary_path.read_bytes())
                    temporary_path.unlink()
                    self.assertFalse(temporary_path.exists())
            finally:
                tempfile.tempdir = previous_tempdir

    def test_shell_free_subprocess_preserves_paths_and_environment(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            working_directory = Path(directory) / "working directory with spaces"
            working_directory.mkdir()
            environment = os.environ.copy()
            environment["PORTABILITY_VALUE"] = "native argument vector"
            completed = _run(
                [
                    sys.executable,
                    "-c",
                    "import os, pathlib; print(pathlib.Path.cwd().name); print(os.environ['PORTABILITY_VALUE'])",
                ],
                cwd=working_directory,
                environment=environment,
            )
            self.assertEqual(0, completed.returncode, completed.stderr)
            self.assertEqual(
                ["working directory with spaces", "native argument vector"],
                completed.stdout.splitlines(),
            )

    def test_closed_files_support_atomic_replacement(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            destination = root / "state.json"
            replacement = root / "state.json.tmp"
            destination.write_text("old\n", encoding="utf-8")
            replacement.write_text("new\n", encoding="utf-8")
            os.replace(replacement, destination)
            self.assertEqual("new\n", destination.read_text(encoding="utf-8"))
            self.assertFalse(replacement.exists())

    def test_permissions_use_platform_capabilities(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "permission-probe.txt"
            path.write_text("probe\n", encoding="utf-8")
            if os.name == "nt":
                self.assertTrue(os.access(path, os.R_OK))
            else:
                path.chmod(0o600)
                self.assertEqual(0o600, stat.S_IMODE(path.stat().st_mode))

    def test_process_termination_uses_the_portable_process_api(self) -> None:
        process = subprocess.Popen(
            [sys.executable, "-c", "import time; time.sleep(30)"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        try:
            process.terminate()
            process.wait(timeout=10)
            self.assertIsNotNone(process.returncode)
        finally:
            if process.poll() is None:
                process.kill()
                process.wait(timeout=10)

    def test_symlink_capability_is_observed_explicitly(self) -> None:
        available, reason = _symlink_capability()
        self.assertIsInstance(available, bool)
        self.assertTrue(reason)

    def test_report_distinguishes_native_windows_from_portable_preflight(self) -> None:
        report = _report()
        self.assertEqual(os.name == "nt", report["native_windows"])
        expected = (
            "WINDOWS_PORTABILITY_VERIFIED"
            if os.name == "nt"
            else "PORTABLE_PREFLIGHT_PASSED"
        )
        self.assertEqual(expected, report["outcome"])

    def test_nested_test_import_path_stays_inside_the_repository(self) -> None:
        test_path = _ROOT / "evals/agent-tests/dev-orchestrator/test_fixtures.py"
        entries = _test_python_path(test_path, "inherited").split(os.pathsep)
        self.assertIn(str(_ROOT / "evals/agent-tests"), entries)
        self.assertIn(str(test_path.parent), entries)
        self.assertIn(str(_ROOT), entries)
        self.assertIn("inherited", entries)
        self.assertNotIn(str(_ROOT.parent), entries)


def _run_contract_tests() -> None:
    """Run the focused portability contract in the current interpreter."""
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(WindowsPortabilityContractTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        raise RuntimeError("The focused Windows portability contract failed.")


def _supported_test_paths() -> tuple[str, ...]:
    """Return every native test entry point that is not a fixture or bounded exclusion."""
    supported = _PORTABLE_PATHS | frozenset(_CORRECTED_PATHS)
    return tuple(
        path
        for path in sorted(supported)
        if Path(path).name.startswith("test_") and path != _SELF
    )


def _test_python_path(path: Path, inherited: str) -> str:
    """Build one bounded import path for a nested repository test."""
    ancestors: list[str] = [str(path.parent)]
    for ancestor in path.parent.parents:
        if ancestor == _ROOT:
            break
        ancestors.append(str(ancestor))
    return os.pathsep.join(filter(None, (str(_ROOT), *ancestors, inherited)))


def _run_supported_tests() -> None:
    """Run every test file classified as supported on native Windows."""
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    inherited_python_path = environment.get("PYTHONPATH", "")
    failures: list[str] = []
    for relative_path in _supported_test_paths():
        path = _ROOT / relative_path
        environment["PYTHONPATH"] = _test_python_path(path, inherited_python_path)
        command = [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            str(path.parent),
            "-p",
            path.name,
        ]
        completed = subprocess.run(command, cwd=_ROOT, env=environment, check=False)
        if completed.returncode != 0:
            failures.append(relative_path)
    if failures:
        raise RuntimeError("Supported Windows tests failed:\n" + "\n".join(failures))


def _command_smokes() -> tuple[tuple[str, tuple[str, ...]], ...]:
    """Return supported repository command smokes as shell-free argument vectors."""
    python = sys.executable
    return (
        ("agent-skill Judge contract", (python, "scripts/agent_skill_judge_contract.py", "--help")),
        ("evaluation documentation freshness", (python, "scripts/build-agent-skill-evaluation-docs.py", "--check")),
        ("agent-skill hierarchy freshness", (python, "scripts/build-agent-skill-hierarchy.py", "--check")),
        ("skill documentation freshness", (python, "scripts/build-skill-docs.py", "--check")),
        ("support checklist freshness", (python, "scripts/build-support-checklist.py", "--check")),
        ("technology registry freshness", (python, "scripts/build-technology-detection.py", "--check")),
        ("technology detector help", (python, "scripts/detect-technology-skills.py", "--help")),
        ("backlog report help", (python, "scripts/generate-backlog-report.py", "--help")),
        ("bundle installer help", (python, "scripts/install-skills.py", "--help")),
        ("Codex metadata freshness", (python, "scripts/openai_metadata.py", "skills", "--check")),
        ("project guidance renderer help", (python, "scripts/render-agents-technology-skills.py", "--help")),
        ("agent-skill catalog validation", (python, "scripts/run-agent-skill-evals.py", "--validate-catalogs")),
        ("skill validation", (python, "scripts/validate-agent-skills.py", "skills")),
        ("installed detector help", (python, "skills/detect-technology-skills/scripts/detect.py", "--help")),
        ("document provenance help", (python, "skills/document-provenance/scripts/validate_document_provenance.py", "--help")),
        ("project wiki help", (python, "skills/project-wiki/scripts/wiki_ops.py", "--help")),
        ("resource claim help", (python, "skills/resource-claim-helper-command/scripts/claim.py", "--help")),
    )


def _run_command_smokes() -> None:
    """Run each supported command smoke and preserve its failure output."""
    for label, arguments in _command_smokes():
        completed = _run(arguments)
        if completed.returncode != 0:
            raise RuntimeError(
                f"{label} failed with {completed.returncode}:\n"
                f"{completed.stdout}{completed.stderr}"
            )


def _report() -> dict[str, object]:
    """Return inventory counts, exclusions, runtime, and capability evidence."""
    counts = Counter(disposition for disposition, _reason in _INVENTORY.values())
    symlink_available, symlink_reason = _symlink_capability()
    native_windows = os.name == "nt"
    return {
        "schema_version": 1,
        "outcome": (
            "WINDOWS_PORTABILITY_VERIFIED"
            if native_windows
            else "PORTABLE_PREFLIGHT_PASSED"
        ),
        "native_windows": native_windows,
        "python": sys.version.split()[0],
        "platform": sys.platform,
        "inventory_count": len(_INVENTORY),
        "dispositions": dict(sorted(counts.items())),
        "platform_specific_exclusions": {
            path: _INVENTORY[path][1] for path in sorted(_PLATFORM_SPECIFIC_PATHS)
        },
        "symlink_capability": {
            "available": symlink_available,
            "reason": symlink_reason,
        },
        "supported_test_file_count": len(_supported_test_paths()),
        "command_smoke_count": len(_command_smokes()),
    }


def main(argv: Sequence[str] | None = None) -> int:
    """Run the deterministic portability preflight and optional supported test suite."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--run-supported-tests",
        action="store_true",
        help="also run every test file classified as supported on native Windows",
    )
    parser.add_argument(
        "--prove-unclassified-fails",
        action="store_true",
        help="prove that one synthetic unclassified Python path is rejected",
    )
    arguments = parser.parse_args(argv)

    if arguments.prove_unclassified_fails:
        try:
            _validate_inventory(_tracked_python_files() | {"unclassified_probe.py"})
        except _InventoryError as error:
            if "unclassified=unclassified_probe.py" not in str(error):
                raise
            print("UNCLASSIFIED_PYTHON_REJECTED")
            return 0
        raise RuntimeError("The inventory accepted an unclassified Python file.")

    _run_contract_tests()
    _run_command_smokes()
    if arguments.run_supported_tests:
        _run_supported_tests()
    print(json.dumps(_report(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
