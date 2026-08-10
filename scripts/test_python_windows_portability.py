# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Inventories every tracked Python file and verifies the repository's native Windows portability contract.

from __future__ import annotations

import argparse
import contextlib
import importlib.util
import io
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
from typing import Iterable, NamedTuple, Sequence
from unittest import mock


_ROOT = Path(__file__).resolve().parents[1]
_SELF = "scripts/test_python_windows_portability.py"
_PORTABLE = "portable and exercised"
_CORRECTED = "corrected by this item"
_MIXED = "portable surface exercised with bounded Windows exclusions"
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
    "evals/agent-tests/project-bootstrapper/scripted_orchestration.py": (
        "The worker launcher unconditionally requested a POSIX session and called os.killpg. "
        "It now uses a Windows process group plus taskkill tree cleanup while retaining the "
        "existing POSIX session and signal behavior."
    ),
    "scripts/agent_skill_evals/commands.py": (
        "The evaluation command runner unconditionally requested a POSIX session and called "
        "os.killpg. It now creates a Windows process group and uses discovered taskkill tree "
        "cleanup, with direct-process termination only when taskkill is unavailable."
    ),
    "scripts/test_resource_claim.py": (
        "The crash fixture imported fcntl directly and skipped Windows. It now drives the "
        "cross-platform _lock_file abstraction, proves contention, terminates the holder, and "
        "proves crash release; symbolic-link setup remains capability-gated."
    ),
    "skills/resource-claim-helper-command/scripts/claim.py": (
        "The module imported fcntl unconditionally and called flock directly. It now keeps "
        "same-descriptor blocking locks through fcntl on POSIX and msvcrt on Windows."
    ),
}

_MIXED_PLATFORM_PATHS = _paths(
    """
evals/agent-tests/dev-backlog-steward/contract_harness.py
evals/agent-tests/dev-backlog-steward/test_contract.py
evals/agent-tests/dev-code-reviewer/test_fixtures.py
evals/agent-tests/dev-runtime-diagnostician/test_fixtures.py
evals/agent-tests/project-bootstrapper/test_scripted_orchestration.py
evals/agent-tests/runner.py
evals/agent-tests/test_runner.py
evals/agent-tests/test_workspace_inventory.py
evals/agent-tests/wiki-ingester/executable_harness.py
evals/agent-tests/wiki-ingester/test_contract.py
evals/agent-tests/wiki-writer/executable_harness.py
evals/agent-tests/wiki-writer/test_contract.py
evals/agent-tests/workspace_inventory.py
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

# A mixed file is not a whole-file exclusion. Its portable cases or safe command surface run on
# Windows, while every unsupported case is named separately below.
_PLATFORM_SPECIFIC_PATHS = frozenset()


class _BaselineFailure(NamedTuple):
    """Record one inherited failing test entry point without accepting new failure identities."""

    owner: str
    failure_ids: tuple[str, ...]
    status: str = "failing on current main"


_MIXED_PLATFORM_COVERAGE = {
    "evals/agent-tests/dev-backlog-steward/contract_harness.py": "evals/agent-tests/dev-backlog-steward/test_contract.py",
    "evals/agent-tests/dev-backlog-steward/test_contract.py": "evals/agent-tests/dev-backlog-steward/test_contract.py",
    "evals/agent-tests/dev-code-reviewer/test_fixtures.py": "evals/agent-tests/dev-code-reviewer/test_fixtures.py",
    "evals/agent-tests/dev-runtime-diagnostician/test_fixtures.py": "evals/agent-tests/dev-runtime-diagnostician/test_fixtures.py",
    "evals/agent-tests/project-bootstrapper/scripted_orchestration.py": "evals/agent-tests/project-bootstrapper/test_scripted_orchestration.py",
    "evals/agent-tests/project-bootstrapper/test_scripted_orchestration.py": "evals/agent-tests/project-bootstrapper/test_scripted_orchestration.py",
    "evals/agent-tests/runner.py": "command:agent-suite catalog list and validation",
    "evals/agent-tests/test_runner.py": "evals/agent-tests/test_runner.py",
    "evals/agent-tests/test_workspace_inventory.py": "evals/agent-tests/test_workspace_inventory.py",
    "evals/agent-tests/wiki-ingester/executable_harness.py": "evals/agent-tests/wiki-ingester/test_contract.py",
    "evals/agent-tests/wiki-ingester/test_contract.py": "evals/agent-tests/wiki-ingester/test_contract.py",
    "evals/agent-tests/wiki-writer/executable_harness.py": "evals/agent-tests/wiki-writer/test_contract.py",
    "evals/agent-tests/wiki-writer/test_contract.py": "evals/agent-tests/wiki-writer/test_contract.py",
    "evals/agent-tests/workspace_inventory.py": "evals/agent-tests/test_workspace_inventory.py",
    "scripts/agent_skill_evals/commands.py": "scripts/test_agent_skill_evals.py",
    "scripts/agent_skill_evals/invocations.py": "scripts/test_agent_skill_evals.py",
    "scripts/agent_skill_evals/staging.py": "scripts/test_agent_skill_evals.py",
    "scripts/agent_skill_evals/workspace.py": "scripts/test_agent_skill_evals.py",
    "scripts/run-agent-skill-evals.py": "command:catalog validation and trusted fixture regression",
    "scripts/test_agent_skill_evals.py": "scripts/test_agent_skill_evals.py",
    "scripts/test_agent_skill_evaluation_docs.py": "scripts/test_agent_skill_evaluation_docs.py",
    "scripts/test_generate_backlog_report.py": "scripts/test_generate_backlog_report.py",
    "scripts/test_install_skills.py": "scripts/test_install_skills.py",
}

# These cases assert POSIX-only process-group or permission semantics. All other cases in each
# mixed suite remain selected on Windows. The key is repository path, test class, and method.
_WINDOWS_UNSUPPORTED_TEST_CASES = {
    "evals/agent-tests/dev-backlog-steward/test_contract.py::DevBacklogStewardContractTests.test_success_and_safe_rollback_preserve_dirty_bytes_modes_and_index": "asserts POSIX mode-bit preservation",
    "evals/agent-tests/dev-code-reviewer/test_fixtures.py::DevCodeReviewerFixtureTests.test_candidate_staging_enforces_oracle_boundary": "asserts POSIX read-only directory mode bits",
    "evals/agent-tests/dev-runtime-diagnostician/test_fixtures.py::DevRuntimeDiagnosticianFixtureTests.test_retained_process_reproduction_cleans_its_child": "requires lsof and POSIX signal inspection",
    "evals/agent-tests/project-bootstrapper/test_scripted_orchestration.py::ScriptedBootstrapperTests.test_timeout_kills_the_owned_process_group_and_cleans_workspace": "asserts POSIX process-group teardown",
    "evals/agent-tests/test_runner.py::AgentSuiteRunnerTests.test_runtime_uses_current_app_bundled_codex": "asserts the macOS application-bundled Codex path",
    "evals/agent-tests/test_runner.py::AgentSuiteRunnerTests.test_offline_typescript_launcher_uses_bundled_node": "asserts a POSIX executable shell launcher and mode bit",
    "evals/agent-tests/test_runner.py::AgentSuiteRunnerTests.test_playwright_preflight_timeout_reaps_a_hung_process_tree": "asserts POSIX detached-process-group recovery",
    "evals/agent-tests/test_runner.py::AgentSuiteRunnerTests.test_timeout_retains_output_and_stops_the_process_group": "asserts POSIX process-group teardown",
    "evals/agent-tests/test_runner.py::AgentSuiteRunnerTests.test_timeout_stops_detached_descendant": "asserts POSIX detached-session recovery",
    "evals/agent-tests/test_runner.py::AgentSuiteRunnerTests.test_containment_stops_fast_detached_descendant_with_sanitized_environment": "asserts POSIX detached-session inspection",
    "evals/agent-tests/test_workspace_inventory.py::WorkspaceInventoryTests.test_file_modes_and_git_index_changes_are_detected": "asserts POSIX mode-bit changes",
    "evals/agent-tests/wiki-writer/test_contract.py::WikiWriterOfflineInterruptionTests.test_mode_only_change_updates_preserved_state_digest": "asserts POSIX execute-bit changes",
    "scripts/test_agent_skill_evals.py::PreparedWorkspaceTests.test_fixture_key_tracks_modes_empty_directories_and_command_environment_policy": "asserts POSIX mode-bit identity",
    "scripts/test_agent_skill_evals.py::PreparedWorkspaceTests.test_successful_command_terminates_remaining_process_group_members": "asserts POSIX process-group teardown",
}

# Symlink security tests run when the Windows host grants symbolic-link creation. The exact cases
# remain visible here and become classified runtime exclusions only when the capability probe fails.
_SYMLINK_CAPABILITY_TEST_CASES = frozenset(
    {
        "evals/agent-tests/dev-backlog-steward/test_contract.py::DevBacklogStewardContractTests.test_future_ideas_inventory_reads_real_files_and_reports_invalid_entries",
        "evals/agent-tests/dev-backlog-steward/test_contract.py::DevBacklogStewardContractTests.test_post_claim_transaction_drift_stops_before_every_promotion_mutation",
        "evals/agent-tests/dev-backlog-steward/test_contract.py::DevBacklogStewardContractTests.test_absent_destination_with_external_parent_stops_before_claims",
        "evals/agent-tests/dev-backlog-steward/test_contract.py::DevBacklogStewardContractTests.test_post_claim_destination_authority_escape_releases_claims",
        "evals/agent-tests/test_runner.py::AgentSuiteRunnerTests.test_release_journal_paths_cannot_symlink_outside_contained_common_directory",
        "evals/agent-tests/test_runner.py::AgentSuiteRunnerTests.test_catalog_rejects_suite_symlink_escape_before_loading_declared_files",
        "evals/agent-tests/test_runner.py::AgentSuiteRunnerTests.test_catalog_rejects_linked_yaml_files_before_loading_either_file",
        "evals/agent-tests/test_runner.py::AgentSuiteRunnerTests.test_post_execution_scenario_root_validation_rejects_symlink_before_git_probe",
        "evals/agent-tests/test_runner.py::AgentSuiteRunnerTests.test_live_runner_revalidates_scenario_root_after_process_before_git_audit",
        "evals/agent-tests/test_runner.py::AgentSuiteRunnerTests.test_junie_runner_revalidates_scenario_root_after_process_before_git_audit",
        "evals/agent-tests/test_runner.py::AgentSuiteRunnerTests.test_handoff_audit_rejects_sibling_and_symlink_escape_before_git_probe",
        "evals/agent-tests/test_runner.py::AgentSuiteRunnerTests.test_offline_fixture_rejects_escaping_dependency_symlink",
        "evals/agent-tests/test_runner.py::AgentSuiteRunnerTests.test_playwright_broker_rejects_fixture_root_swap_after_startup",
        "evals/agent-tests/test_runner.py::AgentSuiteRunnerTests.test_fixture_server_rejects_file_and_directory_symlink_escapes",
        "scripts/test_generate_backlog_report.py::BacklogReportTest.test_outward_symlinked_idea_and_promotion_target_are_not_read",
        "scripts/test_generate_backlog_report.py::BacklogReportTest.test_series_index_reports_escaped_child_without_reading_target",
        "scripts/test_generate_backlog_report.py::BacklogReportTest.test_symlinked_parent_escape_prevents_terminal_diagnosis",
        "scripts/test_generate_backlog_report.py::BacklogReportTest.test_output_cannot_overwrite_scanned_source_or_guidance",
        "scripts/test_generate_backlog_report.py::BacklogReportTest.test_default_output_cannot_resolve_inside_future_ideas",
        "scripts/test_generate_backlog_report.py::BacklogReportTest.test_lexical_output_inside_future_ideas_cannot_follow_symlink_outward",
        "scripts/test_install_skills.py::InstallSkillsTests.test_project_root_replace_configures_final_in_project_detection_registry",
        "scripts/test_install_skills.py::InstallSkillsTests.test_project_root_external_detection_registry_requires_replace_before_mutation",
        "scripts/test_install_skills.py::InstallSkillsTests.test_project_default_destinations_reject_symlink_escape_before_manifest_read",
        "scripts/test_install_skills.py::InstallSkillsTests.test_project_default_mcp_config_rejects_symlink_escape_before_read",
        "scripts/test_install_skills.py::InstallSkillsTests.test_replace_existing_symlink_skill",
        "scripts/test_install_skills.py::InstallSkillsTests.test_replace_dangling_skill_symlink_after_cleanup",
        "scripts/test_install_skills.py::InstallSkillsTests.test_skill_manifest_symlink_is_rejected_without_writing_outside",
        "scripts/test_install_skills.py::InstallSkillsTests.test_agent_manifest_symlink_is_rejected_before_skill_install",
        "scripts/test_install_skills.py::InstallSkillsTests.test_skill_source_symlinks_are_rejected_before_target_deletion",
        "scripts/test_install_skills.py::InstallSkillsTests.test_agent_source_symlink_is_rejected_before_target_deletion",
        "scripts/test_agent_skill_evals.py::HarnessAndJudgeTests.test_model_visible_inventory_rejects_file_and_directory_symlinks",
    }
)

_CHILD_PROCESS_INSPECTION_TEST_CASES = frozenset(
    {
        "evals/agent-tests/dev-runtime-diagnostician/test_fixtures.py::DevRuntimeDiagnosticianFixtureTests.test_clean_shutdown_supports_repeated_restarts",
        "evals/agent-tests/dev-runtime-diagnostician/test_fixtures.py::DevRuntimeDiagnosticianFixtureTests.test_retained_process_reproduction_cleans_its_child",
        "evals/agent-tests/test_runner.py::AgentSuiteRunnerTests.test_containment_stops_fast_detached_descendant_with_sanitized_environment",
        "evals/agent-tests/test_runner.py::AgentSuiteRunnerTests.test_playwright_preflight_timeout_reaps_a_hung_process_tree",
        "evals/agent-tests/test_runner.py::AgentSuiteRunnerTests.test_timeout_retains_output_and_stops_the_process_group",
        "evals/agent-tests/test_runner.py::AgentSuiteRunnerTests.test_timeout_stops_detached_descendant",
    }
)

_PLAYWRIGHT_RUNTIME_TEST_CASES = frozenset(
    {
        "evals/agent-tests/test_runner.py::AgentSuiteRunnerTests.test_accessibility_interaction_can_observe_focus_label_and_recovery_state",
        "evals/agent-tests/test_runner.py::AgentSuiteRunnerTests.test_concurrent_playwright_clients_keep_browser_and_port_identity_isolated",
        "evals/agent-tests/test_runner.py::AgentSuiteRunnerTests.test_ephemeral_broker_token_is_absent_from_commands_and_retained_evidence",
        "evals/agent-tests/test_runner.py::AgentSuiteRunnerTests.test_failed_target_validation_does_not_consume_the_one_shot_broker",
        "evals/agent-tests/test_runner.py::AgentSuiteRunnerTests.test_fixture_server_rejects_file_and_directory_symlink_escapes",
        "evals/agent-tests/test_runner.py::AgentSuiteRunnerTests.test_playwright_broker_rejects_fixture_root_swap_after_startup",
        "evals/agent-tests/test_runner.py::AgentSuiteRunnerTests.test_playwright_broker_rejects_interaction_path_outside_its_scenario",
        "evals/agent-tests/test_runner.py::AgentSuiteRunnerTests.test_playwright_broker_rejects_wrong_authentication_without_launching_browser",
        "evals/agent-tests/test_runner.py::AgentSuiteRunnerTests.test_playwright_brokers_use_unique_loopback_ports_and_close_when_unused",
        "evals/agent-tests/test_runner.py::AgentSuiteRunnerTests.test_playwright_interaction_validation_rejects_external_navigation",
        "evals/agent-tests/test_runner.py::AgentSuiteRunnerTests.test_playwright_target_client_reaches_runner_broker_and_closes_real_browser",
        "evals/agent-tests/test_runner.py::AgentSuiteRunnerTests.test_same_broker_concurrent_valid_clients_consume_exactly_one_launch",
        "evals/agent-tests/test_runner.py::AgentSuiteRunnerTests.test_upload_interaction_separates_visible_label_from_synthetic_filename",
    }
)

# This exact case needs one tracked presentation fixture. A sparse developer checkout may omit it;
# the full native-Windows checkout must contain it and execute the case.
_TRACKED_FIXTURE_CAPABILITY_TEST_CASES = {
    (
        "scripts/test_generate_backlog_report.py::"
        "BacklogReportTest.test_committed_example_remains_a_curated_semantic_reference"
    ): "backlog/examples/styled-backlog-report.html",
}

# The original candidate inherited twelve unrelated failing test entry points. Expanding mixed
# suites exposed additional failures in a full-history clone of current main. Current main fixed
# test_bundle_content.py; retaining it here makes that improvement observable without shrinking the
# accepted sixteen-path baseline. Every remaining failure identity is compared exactly.
def _failure_ids(raw: str) -> tuple[str, ...]:
    """Parse a duplicate-free baseline identity list."""
    values = tuple(line.strip() for line in raw.splitlines() if line.strip())
    if len(values) != len(set(values)):
        raise _InventoryError("The OS-independent failure baseline contains a duplicate identity.")
    return values


_OS_INDEPENDENT_FAILURE_BASELINE = {
    "evals/agent-tests/dev-artifact-reviewer/test_checklist_contract.py": _BaselineFailure(
        "Dev Artifact Reviewer",
        _failure_ids(
            """
failure:test_checklist_contract.ChecklistContractTests.test_current_canonical_sources_have_stable_unique_question_sequences
"""
        ),
    ),
    "evals/agent-tests/dev-documentation-writer/test_fixtures.py": _BaselineFailure(
        "Dev Documentation Writer",
        _failure_ids(
            """
failure:test_fixtures.DocumentationWriterFixtureTests.test_final_validator_accepts_canonical_bold_readiness_markers
failure:test_fixtures.DocumentationWriterFixtureTests.test_final_validator_accepts_complete_source_faithful_artifact
failure:test_fixtures.DocumentationWriterFixtureTests.test_final_validator_accepts_explanatory_node_prose
failure:test_fixtures.DocumentationWriterFixtureTests.test_final_validator_accepts_local_reference_style_destinations
failure:test_fixtures.DocumentationWriterFixtureTests.test_final_validator_accepts_local_shortcut_reference_destinations
failure:test_fixtures.DocumentationWriterFixtureTests.test_final_validator_accepts_nonanaphoric_that_coverage_claim
failure:test_fixtures.DocumentationWriterFixtureTests.test_final_validator_excludes_html_comments_from_visible_evidence
failure:test_fixtures.DocumentationWriterFixtureTests.test_final_validator_ignores_unrelated_external_reference_destination
failure:test_fixtures.DocumentationWriterFixtureTests.test_final_validator_treats_html_comment_markers_in_fences_as_literal
failure:test_fixtures.DocumentationWriterFixtureTests.test_final_validator_treats_html_comments_in_nested_fences_as_literal
failure:test_fixtures.DocumentationWriterFixtureTests.test_final_validator_treats_nested_blockquotes_as_visible_prose
"""
        ),
    ),
    "evals/agent-tests/dev-orchestrator/test_fixtures.py": _BaselineFailure(
        "Dev Orchestrator",
        _failure_ids(
            """
error:test_fixtures.DependencyRoutingFixtureTests.test_committed_fixture_contract_is_complete
error:test_fixtures.DependencyRoutingFixtureTests.test_coordinator_prompt_exposes_none_coordination_boundary
error:test_fixtures.DependencyRoutingFixtureTests.test_delivery_result_controls_provider_closeout
error:test_fixtures.DependencyRoutingFixtureTests.test_dirty_receipt_repository_matrix_is_rejected (drift='tracked')
error:test_fixtures.DependencyRoutingFixtureTests.test_dirty_receipt_repository_matrix_is_rejected (drift='untracked')
error:test_fixtures.DependencyRoutingFixtureTests.test_every_handoff_field_has_an_exact_omission_diagnostic
error:test_fixtures.DependencyRoutingFixtureTests.test_every_handoff_lane_has_an_exact_omission_diagnostic
error:test_fixtures.DependencyRoutingFixtureTests.test_evidence_audit_preserves_missing_and_duplicate_lane_errors (case='duplicate')
error:test_fixtures.DependencyRoutingFixtureTests.test_evidence_audit_preserves_missing_and_duplicate_lane_errors (case='missing')
error:test_fixtures.DependencyRoutingFixtureTests.test_evidence_audit_rejects_extra_lane_with_or_without_claims (claim_release=False)
error:test_fixtures.DependencyRoutingFixtureTests.test_evidence_audit_rejects_extra_lane_with_or_without_claims (claim_release=True)
error:test_fixtures.DependencyRoutingFixtureTests.test_evidence_audit_rejects_receipt_for_empty_lane_set (claim_release=False)
error:test_fixtures.DependencyRoutingFixtureTests.test_evidence_audit_rejects_receipt_for_empty_lane_set (claim_release=True)
error:test_fixtures.DependencyRoutingFixtureTests.test_fabricated_receipt_evidence_matrix_is_rejected
error:test_fixtures.DependencyRoutingFixtureTests.test_hyphenated_producer_alias_does_not_match_registered_invocation
error:test_fixtures.DependencyRoutingFixtureTests.test_none_coordination_evidence_needs_no_claim_journal
error:test_fixtures.DependencyRoutingFixtureTests.test_none_coordination_ignores_pre_existing_claim_files
error:test_fixtures.DependencyRoutingFixtureTests.test_none_coordination_is_not_a_required_target_skill
error:test_fixtures.DependencyRoutingFixtureTests.test_none_coordination_rejects_claim_invocation (session_id='coder')
error:test_fixtures.DependencyRoutingFixtureTests.test_none_coordination_rejects_claim_invocation (session_id='target')
error:test_fixtures.DependencyRoutingFixtureTests.test_none_coordination_report_omits_claim_release_evidence
error:test_fixtures.DependencyRoutingFixtureTests.test_producer_session_evidence_matrix_is_rejected
error:test_fixtures.DependencyRoutingFixtureTests.test_receipt_session_superset_rejects_duplicates_replacements_and_foreign_roles (name='duplicate-review')
error:test_fixtures.DependencyRoutingFixtureTests.test_receipt_session_superset_rejects_duplicates_replacements_and_foreign_roles (name='duplicate-verification')
error:test_fixtures.DependencyRoutingFixtureTests.test_receipt_session_superset_rejects_duplicates_replacements_and_foreign_roles (name='foreign-review')
error:test_fixtures.DependencyRoutingFixtureTests.test_receipt_session_superset_rejects_duplicates_replacements_and_foreign_roles (name='foreign-verification')
error:test_fixtures.DependencyRoutingFixtureTests.test_receipt_session_superset_rejects_duplicates_replacements_and_foreign_roles (name='replacement-review')
error:test_fixtures.DependencyRoutingFixtureTests.test_receipt_session_superset_rejects_duplicates_replacements_and_foreign_roles (name='replacement-verification')
error:test_fixtures.DependencyRoutingFixtureTests.test_receipts_may_retain_additional_same_role_review_and_verification_sessions
error:test_fixtures.DependencyRoutingFixtureTests.test_report_rejects_extra_lane_with_or_without_claims (claim_release=False)
error:test_fixtures.DependencyRoutingFixtureTests.test_report_rejects_extra_lane_with_or_without_claims (claim_release=True)
error:test_fixtures.DependencyRoutingFixtureTests.test_report_rejects_receipt_for_empty_lane_set (claim_release=False)
error:test_fixtures.DependencyRoutingFixtureTests.test_report_rejects_receipt_for_empty_lane_set (claim_release=True)
error:test_fixtures.DependencyRoutingFixtureTests.test_resource_claim_companion_accepts_exact_legacy_markers
error:test_fixtures.DependencyRoutingFixtureTests.test_resource_claim_companion_allows_released_named_resource_event
error:test_fixtures.DependencyRoutingFixtureTests.test_resource_claim_companion_executes_and_audits_complete_lifecycle
error:test_fixtures.DependencyRoutingFixtureTests.test_resource_claim_companion_reads_legacy_state_as_fallback
error:test_fixtures.DependencyRoutingFixtureTests.test_resource_claim_companion_rejects_contradictory_dual_state
error:test_fixtures.DependencyRoutingFixtureTests.test_resource_claim_companion_rejects_lifecycle_breaks (case='acquire-after-mutation')
error:test_fixtures.DependencyRoutingFixtureTests.test_resource_claim_companion_rejects_lifecycle_breaks (case='acquire-after-release')
error:test_fixtures.DependencyRoutingFixtureTests.test_resource_claim_companion_rejects_lifecycle_breaks (case='active-registry')
error:test_fixtures.DependencyRoutingFixtureTests.test_resource_claim_companion_rejects_lifecycle_breaks (case='duplicate-claim-id-across-repositories')
error:test_fixtures.DependencyRoutingFixtureTests.test_resource_claim_companion_rejects_lifecycle_breaks (case='duplicate-release-event-ids')
error:test_fixtures.DependencyRoutingFixtureTests.test_resource_claim_companion_rejects_lifecycle_breaks (case='early-integration-claim')
error:test_fixtures.DependencyRoutingFixtureTests.test_resource_claim_companion_rejects_lifecycle_breaks (case='isolated-integration-acquire')
error:test_fixtures.DependencyRoutingFixtureTests.test_resource_claim_companion_rejects_lifecycle_breaks (case='malformed-journal-json')
error:test_fixtures.DependencyRoutingFixtureTests.test_resource_claim_companion_rejects_lifecycle_breaks (case='missing-acquire')
error:test_fixtures.DependencyRoutingFixtureTests.test_resource_claim_companion_rejects_lifecycle_breaks (case='multiple-release-event-ids')
error:test_fixtures.DependencyRoutingFixtureTests.test_resource_claim_companion_rejects_lifecycle_breaks (case='resource-file-domain')
error:test_fixtures.DependencyRoutingFixtureTests.test_resource_claim_companion_rejects_lifecycle_breaks (case='second-repository-surplus-claim')
error:test_fixtures.DependencyRoutingFixtureTests.test_resource_claim_companion_rejects_lifecycle_breaks (case='surplus-bound-successful-release')
error:test_fixtures.DependencyRoutingFixtureTests.test_resource_claim_companion_rejects_lifecycle_breaks (case='surplus-private-file-claim')
error:test_fixtures.DependencyRoutingFixtureTests.test_resource_claim_companion_rejects_lifecycle_breaks (case='unexpected-integration-resource')
error:test_fixtures.DependencyRoutingFixtureTests.test_resource_claim_companion_rejects_lifecycle_breaks (case='unrecognized-named-resource')
error:test_fixtures.DependencyRoutingFixtureTests.test_resource_claim_companion_rejects_lifecycle_breaks (case='unreleased-named-resource')
error:test_fixtures.DependencyRoutingFixtureTests.test_resource_claim_companion_rejects_lifecycle_breaks (case='unsupported-schema')
error:test_fixtures.DependencyRoutingFixtureTests.test_resource_claim_companion_rejects_lifecycle_breaks (case='wrong-integration-scope')
error:test_fixtures.DependencyRoutingFixtureTests.test_resource_claim_companion_rejects_mixed_registry_and_event_layouts
error:test_fixtures.DependencyRoutingFixtureTests.test_scalar_receipt_evidence_matrix_is_rejected
error:test_fixtures.DependencyRoutingFixtureTests.test_skill_under_test_finding_uses_separate_protected_and_provider_boundaries
"""
        ),
    ),
    "evals/agent-tests/project-configurator/test_fixtures.py": _BaselineFailure(
        "Project Configurator",
        _failure_ids(
            """
failure:test_fixtures.ProjectConfiguratorFixtureTests.test_routing_contracts_name_exact_role_ownership_and_bridge_bytes
            """
        ),
    ),
    "evals/agent-tests/project-bootstrapper/test_scripted_orchestration.py": _BaselineFailure(
        "Project Bootstrapper",
        _failure_ids(
            """
failure:test_scripted_orchestration.ScriptedBootstrapperTests.test_both_configuration_outputs_receive_independent_reviews
failure:test_scripted_orchestration.ScriptedBootstrapperTests.test_correction_retries_the_owner_and_stops_at_two
failure:test_scripted_orchestration.ScriptedBootstrapperTests.test_default_trace_is_repeatable_and_complete
failure:test_scripted_orchestration.ScriptedBootstrapperTests.test_integration_review_and_verification_corrections_are_bounded
failure:test_scripted_orchestration.ScriptedBootstrapperTests.test_missing_configuration_uses_primary_claim_free_handoff_then_resumes
failure:test_scripted_orchestration.ScriptedBootstrapperTests.test_resumed_execution_obeys_canonical_solo_and_legacy_selectors
failure:test_scripted_orchestration.ScriptedBootstrapperTests.test_reverse_engineering_audit_blocks_without_coverage_manifest_evidence
failure:test_scripted_orchestration.ScriptedBootstrapperTests.test_reverse_engineering_audit_blocks_without_required_ledger
failure:test_scripted_orchestration.ScriptedBootstrapperTests.test_reverse_engineering_audit_detects_swapped_manifest_mappings
failure:test_scripted_orchestration.ScriptedBootstrapperTests.test_reverse_engineering_audit_owner_corrections_are_bounded
failure:test_scripted_orchestration.ScriptedBootstrapperTests.test_reverse_engineering_audit_parses_the_exact_owner_field
failure:test_scripted_orchestration.ScriptedBootstrapperTests.test_reverse_engineering_audit_rejects_baseline_classification_mismatch
failure:test_scripted_orchestration.ScriptedBootstrapperTests.test_reverse_engineering_audit_rejects_incomplete_path_classifications
failure:test_scripted_orchestration.ScriptedBootstrapperTests.test_reverse_engineering_audit_requires_hashed_baseline_for_every_source
failure:test_scripted_orchestration.ScriptedBootstrapperTests.test_reverse_engineering_audit_routes_corrections_and_reaches_steady_state
failure:test_scripted_orchestration.ScriptedBootstrapperTests.test_reverse_engineering_audit_routes_missing_auditable_artifacts (artifact='docs/module-catalog.md')
failure:test_scripted_orchestration.ScriptedBootstrapperTests.test_reverse_engineering_audit_routes_missing_auditable_artifacts (artifact='docs/wiki/topic-index.md')
failure:test_scripted_orchestration.ScriptedBootstrapperTests.test_terminal_dependency_outcomes_are_reproducible (outcome='FAIL')
failure:test_scripted_orchestration.ScriptedBootstrapperTests.test_terminal_dependency_outcomes_are_reproducible (outcome='BLOCKED')
failure:test_scripted_orchestration.ScriptedBootstrapperTests.test_terminal_dependency_outcomes_are_reproducible
failure:test_scripted_orchestration.ScriptedBootstrapperTests.test_verification_correction_is_reviewed_and_reaudited_before_retry
failure:test_scripted_orchestration.ScriptedBootstrapperTests.test_verification_correction_uses_persistent_owner_for_audit_created_document
error:test_scripted_orchestration.ScriptedBootstrapperTests.test_configuration_dependency_invokes_each_public_setup_procedure
error:test_scripted_orchestration.ScriptedBootstrapperTests.test_isolated_snapshot_contains_only_declared_inputs
"""
        ),
    ),
    "evals/agent-tests/wiki-ingester/test_contract.py": _BaselineFailure(
        "Wiki Ingester",
        _failure_ids(
            """
failure:test_contract.WikiIngesterTargetBoundaryTests.test_retained_evaluator_artifacts_replay_offline
"""
        ),
    ),
    "evals/agent-tests/test_runner.py": _BaselineFailure(
        "agent-suite runner",
        _failure_ids(
            """
failure:test_runner.AgentSuiteRunnerTests.test_cleanup_audit_rejects_active_claim_in_nested_fixture_repository
"""
        ),
    ),
    "scripts/test_bundle_content.py": _BaselineFailure("bundle contract", (), "resolved on current main"),
    "scripts/test_codex_task_control.py": _BaselineFailure(
        "Codex task control",
        _failure_ids(
            """
failure:test_codex_task_control.CodexTaskControlPackageTests.test_archival_waits_for_portable_terminal_closeout (clause='Archive a terminal Codex task only after coordinate-work-items confirms')
failure:test_codex_task_control.CodexTaskControlPackageTests.test_archival_waits_for_portable_terminal_closeout (clause='cleanup eligibility')
failure:test_codex_task_control.CodexTaskControlPackageTests.test_archival_waits_for_portable_terminal_closeout (clause='no unresolved notification remains')
failure:test_codex_task_control.CodexTaskControlPackageTests.test_portable_skill_contains_no_codex_only_vocabulary (phrase='task archival')
failure:test_codex_task_control.CodexTaskControlPackageTests.test_watchdog_prompt_templates_are_canonical_and_render_byte_identically
failure:test_codex_task_control.CodexTaskControlRoleRoutingTests.test_non_codex_generated_agents_do_not_name_portable_policy_as_codex (runtime='claude', role='dev-backlog-watchdog')
failure:test_codex_task_control.CodexTaskControlRoleRoutingTests.test_non_codex_generated_agents_do_not_name_portable_policy_as_codex (runtime='gemini', role='dev-backlog-watchdog')
failure:test_codex_task_control.CodexTaskControlRoleRoutingTests.test_non_codex_generated_agents_do_not_name_portable_policy_as_codex (runtime='junie', role='dev-backlog-watchdog')
"""
        ),
    ),
    "scripts/test_eval_coverage_catalog.py": _BaselineFailure(
        "evaluation coverage catalog",
        _failure_ids(
            """
failure:test_eval_coverage_catalog.RepositoryCoverageCliTests.test_cli_reproduces_structural_and_declared_totals
"""
        ),
    ),
    "scripts/test_agent_skill_evaluation_docs.py": _BaselineFailure(
        "agent-skill evaluation documentation",
        _failure_ids(
            """
failure:test_agent_skill_evaluation_docs.AgentSkillEvaluationDocumentationTests.test_backlog_steward_rows_publish_neutral_resource_coordination_variants
failure:test_agent_skill_evaluation_docs.AgentSkillEvaluationDocumentationTests.test_generator_check_reports_current_output
"""
        ),
    ),
    "scripts/test_resource_claim.py": _BaselineFailure(
        "resource claim",
        _failure_ids(
            """
error:test_resource_claim.ResourceClaimTests.test_report_groups_versioned_work_item_segments_and_diagnostics
"""
        ),
    ),
    "scripts/test_role_mutation_policy.py": _BaselineFailure(
        "role mutation policy",
        _failure_ids(
            """
failure:test_role_mutation_policy.RoleMutationPolicyTests.test_execute_workitem_package_is_retired_without_weakening_delivery_contracts
failure:test_role_mutation_policy.RoleMutationPolicyTests.test_workflow_skills_delegate_claim_rules_to_resource_claim
"""
        ),
    ),
    "scripts/test_ste_technical_writing.py": _BaselineFailure(
        "STE technical writing",
        _failure_ids(
            """
failure:test_ste_technical_writing.SteTechnicalWritingContractTests.test_documentation_roles_and_codex_profile_use_gpt_55_high
"""
        ),
    ),
    "scripts/test_technology_detection.py": _BaselineFailure(
        "technology detection",
        _failure_ids(
            """
failure:test_technology_detection.TechnologyDetectionTests.test_agents_section_preserves_none_unset_and_unsupported_boundaries
failure:test_technology_detection.TechnologyDetectionTests.test_render_docstring_distinguishes_optional_authority_from_required_workflow
"""
        ),
    ),
    "scripts/test_work_item_coordination.py": _BaselineFailure(
        "work-item coordination",
        _failure_ids(
            """
failure:test_work_item_coordination.WorkItemCoordinationPackageTests.test_watchdog_policy_is_read_only_and_provider_neutral (clause='Notify the coordinator only when action is required')
failure:test_work_item_coordination.WorkItemCoordinationPackageTests.test_watchdog_policy_is_read_only_and_provider_neutral (clause='one concise no-action cycle result')
"""
        ),
    ),
}

_OS_INDEPENDENT_COMMAND_FAILURE_BASELINE = {
    "agent-suite catalog list": (
        1,
        "ValueError: dev-runtime-diagnostician native agent does not include required skill structured-explanation",
    ),
    "agent-suite catalog validation": (
        1,
        "ValueError: dev-runtime-diagnostician native agent does not include required skill structured-explanation",
    ),
}

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
        (
            _MIXED_PLATFORM_PATHS,
            _MIXED,
            "The portable cases or safe command surface run on Windows; every unsupported case is named separately.",
        ),
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


def _native_windows_host() -> bool:
    """Return whether this interpreter is running on native Windows."""
    return os.name == "nt"


def _child_process_inspection_capability() -> tuple[bool, str]:
    """Probe the POSIX process table needed by descendant-inspection fixtures."""
    if os.name == "nt":
        return False, "POSIX process-table and signal fixture unavailable on Windows"
    process_table = shutil.which("ps")
    if process_table is None:
        return False, "ps executable is unavailable"
    try:
        completed = _run([process_table, "-axo", "pid=,ppid="])
    except OSError as error:
        return False, f"process-table inspection unavailable: {error}"
    if completed.returncode != 0:
        return False, f"process-table inspection exited {completed.returncode}"
    return True, "process-table inspection available"


def _playwright_runtime_capability() -> tuple[bool, str]:
    """Probe the optional Node and Playwright runtime used by real-browser fixture cases."""
    node = shutil.which("node")
    package = _ROOT / "evals/agent-tests/node_modules/playwright/package.json"
    if node is None:
        return False, "Node.js executable is unavailable"
    if not package.is_file():
        return False, "evals/agent-tests Playwright package is not installed"
    try:
        completed = _run(
            [node, "--input-type=module", "-e", "import('playwright')"],
            cwd=_ROOT / "evals/agent-tests",
        )
    except OSError as error:
        return False, f"Playwright import unavailable: {error}"
    if completed.returncode != 0:
        return False, f"Playwright import exited {completed.returncode}"
    return True, "Node.js and Playwright runtime available"


def _tracked_fixture_capability(relative_path: str) -> tuple[bool, str]:
    """Distinguish a sparse-checkout omission from a missing tracked fixture."""
    fixture = _ROOT / relative_path
    if fixture.is_file():
        return True, f"tracked fixture present: {relative_path}"
    completed = _run(
        [_git_executable(), "-C", str(_ROOT), "ls-files", "-t", "--", relative_path]
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"Cannot inspect tracked fixture {relative_path}: {completed.stderr.strip()}"
        )
    marker = completed.stdout.strip()
    if marker == f"S {relative_path}":
        return False, f"tracked fixture omitted by sparse checkout: {relative_path}"
    if marker:
        raise RuntimeError(
            f"Required tracked fixture is missing outside a sparse checkout: {relative_path}"
        )
    raise RuntimeError(f"Required test fixture is not tracked: {relative_path}")


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

    def test_mixed_platform_tests_are_selected_at_case_granularity(self) -> None:
        mixed_tests = {
            path for path in _MIXED_PLATFORM_PATHS if Path(path).name.startswith("test_")
        }
        self.assertTrue(mixed_tests)
        self.assertTrue(mixed_tests <= set(_supported_test_paths()))
        self.assertFalse(mixed_tests & _PLATFORM_SPECIFIC_PATHS)
        self.assertTrue(_WINDOWS_UNSUPPORTED_TEST_CASES)
        for test_id, reason in _WINDOWS_UNSUPPORTED_TEST_CASES.items():
            relative_path, separator, case_id = test_id.partition("::")
            self.assertEqual("::", separator)
            self.assertIn(relative_path, mixed_tests)
            self.assertTrue(case_id.rpartition(".")[2].startswith("test_"))
            self.assertTrue(reason)

    def test_mixed_platform_commands_have_explicit_safe_entry_points(self) -> None:
        command_paths = {
            argument
            for _label, arguments in _command_smokes()
            for argument in arguments
            if argument.endswith(".py")
        }
        self.assertIn("evals/agent-tests/runner.py", command_paths)
        self.assertIn("scripts/run-agent-skill-evals.py", command_paths)
        self.assertTrue(_MIXED_PLATFORM_PATHS <= (_command_covered_paths() | set(_supported_test_paths())))

    def test_runtime_capability_cases_are_explicit_and_reasoned(self) -> None:
        self.assertTrue(_CHILD_PROCESS_INSPECTION_TEST_CASES)
        self.assertTrue(_PLAYWRIGHT_RUNTIME_TEST_CASES)
        with (
            mock.patch(__name__ + "._child_process_inspection_capability", return_value=(False, "blocked")),
            mock.patch(__name__ + "._playwright_runtime_capability", return_value=(False, "missing")),
        ):
            exclusions = _case_exclusions("evals/agent-tests/test_runner.py")
        self.assertTrue(_CHILD_PROCESS_INSPECTION_TEST_CASES & exclusions.keys())
        self.assertTrue(_PLAYWRIGHT_RUNTIME_TEST_CASES & exclusions.keys())
        for key, reason in exclusions.items():
            self.assertTrue(key.startswith("evals/agent-tests/test_runner.py::"))
            self.assertTrue(reason)

    def test_sparse_checkout_fixture_exclusion_is_exact_and_never_a_baseline(self) -> None:
        case_key = (
            "scripts/test_generate_backlog_report.py::"
            "BacklogReportTest.test_committed_example_remains_a_curated_semantic_reference"
        )
        self.assertEqual(
            {case_key: "backlog/examples/styled-backlog-report.html"},
            _TRACKED_FIXTURE_CAPABILITY_TEST_CASES,
        )
        self.assertNotIn(
            "scripts/test_generate_backlog_report.py",
            _OS_INDEPENDENT_FAILURE_BASELINE,
        )
        with mock.patch(
            __name__ + "._tracked_fixture_capability",
            return_value=(False, "tracked fixture omitted by sparse checkout"),
        ):
            exclusions = _case_exclusions("scripts/test_generate_backlog_report.py")
        self.assertEqual({case_key}, set(exclusions))
        self.assertIn("sparse checkout", exclusions[case_key])

        with (
            mock.patch(
                __name__ + "._tracked_fixture_capability",
                return_value=(False, "tracked fixture omitted by sparse checkout"),
            ),
            mock.patch(__name__ + "._native_windows_host", return_value=True),
            self.assertRaisesRegex(RuntimeError, "full checkout"),
        ):
            _case_exclusions("scripts/test_generate_backlog_report.py")

    def test_os_independent_failure_baseline_retains_all_sixteen_owners(self) -> None:
        self.assertEqual(16, len(_OS_INDEPENDENT_FAILURE_BASELINE))
        self.assertEqual(
            118,
            sum(
                len(baseline.failure_ids)
                for baseline in _OS_INDEPENDENT_FAILURE_BASELINE.values()
            ),
        )
        self.assertEqual(
            "resolved on current main",
            _OS_INDEPENDENT_FAILURE_BASELINE["scripts/test_bundle_content.py"].status,
        )
        self.assertEqual(
            (
                "failure:test_agent_skill_evaluation_docs."
                "AgentSkillEvaluationDocumentationTests."
                "test_backlog_steward_rows_publish_neutral_resource_coordination_variants",
                "failure:test_agent_skill_evaluation_docs."
                "AgentSkillEvaluationDocumentationTests."
                "test_generator_check_reports_current_output",
            ),
            _OS_INDEPENDENT_FAILURE_BASELINE[
                "scripts/test_agent_skill_evaluation_docs.py"
            ].failure_ids,
        )
        for relative_path, expected in _OS_INDEPENDENT_FAILURE_BASELINE.items():
            self.assertTrue(relative_path.endswith(".py"))
            self.assertTrue(expected.owner)
            self.assertTrue(expected.failure_ids or expected.status == "resolved on current main")

    def test_failure_baseline_rejects_new_identity_inside_inherited_red_file(self) -> None:
        observed = {
            path: baseline.failure_ids
            for path, baseline in _OS_INDEPENDENT_FAILURE_BASELINE.items()
            if baseline.failure_ids
        }
        resolved = _compare_supported_test_failures(observed)
        self.assertEqual(
            {"scripts/test_bundle_content.py": ()},
            resolved,
        )
        drifted = dict(observed)
        inherited_path = "scripts/test_technology_detection.py"
        drifted[inherited_path] = (*drifted[inherited_path], "failure:new_windows_regression")
        with self.assertRaisesRegex(RuntimeError, "new_windows_regression"):
            _compare_supported_test_failures(drifted)

    def test_corrected_process_launchers_have_explicit_os_branches(self) -> None:
        for relative_path in (
            "evals/agent-tests/project-bootstrapper/scripted_orchestration.py",
            "scripts/agent_skill_evals/commands.py",
        ):
            source = (_ROOT / relative_path).read_text(encoding="utf-8")
            with self.subTest(path=relative_path):
                self.assertIn('if os.name == "nt"', source)
                self.assertIn("CREATE_NEW_PROCESS_GROUP", source)
                self.assertIn('process_options["start_new_session"] = True', source)
                self.assertIn('shutil.which("taskkill")', source)

    def test_lock_crash_fixture_uses_the_cross_platform_abstraction(self) -> None:
        source = (_ROOT / "scripts/test_resource_claim.py").read_text(encoding="utf-8")
        fixture_start = source.index(
            "    def test_registry_os_lock_is_released_when_holder_process_crashes"
        )
        fixture_end = source.index("\n    def test_", fixture_start + 8)
        fixture = source[fixture_start:fixture_end]
        self.assertIn("_lock_file", fixture)
        self.assertNotIn("fcntl", fixture)
        self.assertNotIn("skipIf(os.name", source[max(0, fixture_start - 160):fixture_start])


def _run_contract_tests() -> None:
    """Run the focused portability contract in the current interpreter."""
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(WindowsPortabilityContractTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        raise RuntimeError("The focused Windows portability contract failed.")


def _supported_test_paths() -> tuple[str, ...]:
    """Return every native test entry point, including mixed suites filtered by case."""
    supported = _PORTABLE_PATHS | frozenset(_CORRECTED_PATHS) | _MIXED_PLATFORM_PATHS
    return tuple(
        path
        for path in sorted(supported)
        if Path(path).name.startswith("test_") and path != _SELF
    )


def _command_covered_paths() -> set[str]:
    """Return mixed source paths exercised by an owning test or safe command surface."""
    supported_tests = set(_supported_test_paths())
    return {
        path
        for path, evidence in _MIXED_PLATFORM_COVERAGE.items()
        if evidence.startswith("command:") or evidence in supported_tests
    }


class _TestOutcome(NamedTuple):
    """Capture stable test identities separately from human-readable diagnostic output."""

    tests_run: int
    failure_ids: tuple[str, ...]
    excluded_cases: tuple[tuple[str, str], ...]
    output: str


def _iter_tests(suite: unittest.TestSuite) -> Iterable[unittest.TestCase]:
    """Flatten nested unittest suites without relying on private loader structure."""
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from _iter_tests(item)
        else:
            yield item


def _configured_case_key(relative_path: str, test: unittest.TestCase) -> str:
    """Return the repository path plus stable class and method identity for one case."""
    identifier = test.id()
    components = identifier.split(".")
    case_id = ".".join(components[-2:]) if len(components) >= 2 else identifier
    return f"{relative_path}::{case_id}"


def _case_exclusions(relative_path: str) -> dict[str, str]:
    """Return exact OS or runtime capability cases unavailable on this host."""
    exclusions: dict[str, str] = {}
    if os.name == "nt":
        exclusions.update(
            {
                key: reason
                for key, reason in _WINDOWS_UNSUPPORTED_TEST_CASES.items()
                if key.startswith(f"{relative_path}::")
            }
        )
    symlink_available, symlink_reason = _symlink_capability()
    if not symlink_available:
        exclusions.update(
            {
                key: f"symbolic-link capability unavailable: {symlink_reason}"
                for key in _SYMLINK_CAPABILITY_TEST_CASES
                if key.startswith(f"{relative_path}::")
            }
        )
    process_cases = {
        key for key in _CHILD_PROCESS_INSPECTION_TEST_CASES if key.startswith(f"{relative_path}::")
    }
    if process_cases:
        process_available, process_reason = _child_process_inspection_capability()
        if not process_available:
            exclusions.update(
                {key: f"child-process inspection unavailable: {process_reason}" for key in process_cases}
            )
    playwright_cases = {
        key for key in _PLAYWRIGHT_RUNTIME_TEST_CASES if key.startswith(f"{relative_path}::")
    }
    if playwright_cases:
        playwright_available, playwright_reason = _playwright_runtime_capability()
        if not playwright_available:
            exclusions.update(
                {key: f"Playwright runtime unavailable: {playwright_reason}" for key in playwright_cases}
            )
    for key, fixture_path in _TRACKED_FIXTURE_CAPABILITY_TEST_CASES.items():
        if not key.startswith(f"{relative_path}::"):
            continue
        fixture_available, fixture_reason = _tracked_fixture_capability(fixture_path)
        if fixture_available:
            continue
        if _native_windows_host():
            raise RuntimeError(
                "Native Windows verification requires a full checkout; " + fixture_reason
            )
        exclusions[key] = f"required tracked fixture unavailable: {fixture_reason}"
    return exclusions


def _collect_test_outcome(relative_path: str) -> _TestOutcome:
    """Run one isolated entry point after selecting only its supported Windows cases."""
    path = _ROOT / relative_path
    discovered = unittest.defaultTestLoader.discover(str(path.parent), pattern=path.name)
    exclusions = _case_exclusions(relative_path)
    selected = unittest.TestSuite()
    observed_keys: set[str] = set()
    for test in _iter_tests(discovered):
        key = _configured_case_key(relative_path, test)
        observed_keys.add(key)
        if key not in exclusions:
            selected.addTest(test)
    missing = set(exclusions) - observed_keys
    if missing:
        raise RuntimeError(
            "Windows case exclusion no longer names a discovered test:\n" + "\n".join(sorted(missing))
        )

    diagnostics = io.StringIO()
    with contextlib.redirect_stdout(diagnostics), contextlib.redirect_stderr(diagnostics):
        result = unittest.TextTestRunner(stream=diagnostics, verbosity=1).run(selected)
    failure_ids = tuple(
        sorted(
            [f"failure:{test.id()}" for test, _traceback in result.failures]
            + [f"error:{test.id()}" for test, _traceback in result.errors]
            + [f"unexpected-success:{test.id()}" for test in result.unexpectedSuccesses]
        )
    )
    return _TestOutcome(
        tests_run=result.testsRun,
        failure_ids=failure_ids,
        excluded_cases=tuple(sorted(exclusions.items())),
        output=diagnostics.getvalue(),
    )


def _encode_test_outcome(outcome: _TestOutcome) -> str:
    """Encode one child outcome as a stable machine-readable line."""
    return json.dumps(
        {
            "tests_run": outcome.tests_run,
            "failure_ids": list(outcome.failure_ids),
            "excluded_cases": dict(outcome.excluded_cases),
            "output": outcome.output,
        },
        sort_keys=True,
    )


def _decode_test_outcome(text: str, relative_path: str) -> _TestOutcome:
    """Decode one child result and reject malformed or ambiguous output."""
    try:
        value = json.loads(text)
        tests_run = value["tests_run"]
        failure_ids = value["failure_ids"]
        excluded_cases = value["excluded_cases"]
        output = value["output"]
    except (KeyError, TypeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"Malformed test outcome for {relative_path}: {text}") from error
    if (
        not isinstance(tests_run, int)
        or not isinstance(failure_ids, list)
        or not all(isinstance(item, str) for item in failure_ids)
        or not isinstance(excluded_cases, dict)
        or not all(
            isinstance(key, str) and isinstance(reason, str)
            for key, reason in excluded_cases.items()
        )
        or not isinstance(output, str)
    ):
        raise RuntimeError(f"Malformed test outcome types for {relative_path}")
    return _TestOutcome(
        tests_run,
        tuple(failure_ids),
        tuple(sorted(excluded_cases.items())),
        output,
    )


def _test_python_path(path: Path, inherited: str) -> str:
    """Build one bounded import path for a nested repository test."""
    ancestors: list[str] = [str(path.parent)]
    for ancestor in path.parent.parents:
        if ancestor == _ROOT:
            break
        ancestors.append(str(ancestor))
    return os.pathsep.join(filter(None, (str(_ROOT), *ancestors, inherited)))


def _compare_supported_test_failures(
    observed_failures: dict[str, tuple[str, ...]],
) -> dict[str, tuple[str, ...]]:
    """Accept inherited identities and return baseline identities that have been resolved."""
    unexpected: list[str] = []
    resolved: dict[str, tuple[str, ...]] = {}
    for relative_path, outcome_ids in observed_failures.items():
        baseline = _OS_INDEPENDENT_FAILURE_BASELINE.get(relative_path)
        if baseline is None:
            unexpected.append(f"{relative_path}: new failing test entry point")
            continue
        additions = set(outcome_ids) - set(baseline.failure_ids)
        if additions:
            unexpected.extend(f"{relative_path}: {item}" for item in sorted(additions))
    for relative_path, baseline in _OS_INDEPENDENT_FAILURE_BASELINE.items():
        missing = set(baseline.failure_ids) - set(observed_failures.get(relative_path, ()))
        if missing or not baseline.failure_ids:
            resolved[relative_path] = tuple(sorted(missing))
    if unexpected:
        raise RuntimeError(
            "New or Windows-specific supported-test regressions:\n" + "\n".join(unexpected)
        )
    return resolved


def _run_supported_tests() -> dict[str, object]:
    """Run supported cases and accept only the exact inherited failure identities."""
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    inherited_python_path = environment.get("PYTHONPATH", "")
    observed_failures: dict[str, tuple[str, ...]] = {}
    excluded_cases: dict[str, dict[str, str]] = {}
    tests_run = 0
    for relative_path in _supported_test_paths():
        path = _ROOT / relative_path
        environment["PYTHONPATH"] = _test_python_path(path, inherited_python_path)
        command = [
            sys.executable,
            str(_ROOT / _SELF),
            "--run-test-file",
            relative_path,
        ]
        completed = _run(command, environment=environment)
        if completed.returncode != 0:
            raise RuntimeError(
                f"Supported test child failed for {relative_path}:\n"
                f"{completed.stdout}{completed.stderr}"
            )
        outcome = _decode_test_outcome(completed.stdout, relative_path)
        tests_run += outcome.tests_run
        if outcome.failure_ids:
            observed_failures[relative_path] = outcome.failure_ids
        if outcome.excluded_cases:
            excluded_cases[relative_path] = dict(outcome.excluded_cases)

    resolved = _compare_supported_test_failures(observed_failures)
    return {
        "tests_run": tests_run,
        "observed_inherited_failures": {
            path: list(identities) for path, identities in sorted(observed_failures.items())
        },
        "resolved_baseline_failures": {
            path: list(identities) for path, identities in sorted(resolved.items())
        },
        "excluded_cases": {
            path: dict(sorted(cases.items())) for path, cases in sorted(excluded_cases.items())
        },
    }


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
        ("agent-skill evaluation runner help", (python, "scripts/run-agent-skill-evals.py", "--help")),
        ("agent-skill catalog validation", (python, "scripts/run-agent-skill-evals.py", "--validate-catalogs")),
        ("agent-suite runner help", (python, "evals/agent-tests/runner.py", "--help")),
        ("agent-suite catalog list", (python, "evals/agent-tests/runner.py", "--harness", "codex", "--list")),
        (
            "agent-suite catalog validation",
            (python, "evals/agent-tests/runner.py", "--harness", "codex", "--validate-only"),
        ),
        ("skill validation", (python, "scripts/validate-agent-skills.py", "skills")),
        ("installed detector help", (python, "skills/detect-technology-skills/scripts/detect.py", "--help")),
        ("document provenance help", (python, "skills/document-provenance/scripts/validate_document_provenance.py", "--help")),
        ("project wiki help", (python, "skills/project-wiki/scripts/wiki_ops.py", "--help")),
        ("resource claim help", (python, "skills/resource-claim-helper-command/scripts/claim.py", "--help")),
    )


def _run_command_smokes() -> dict[str, object]:
    """Run safe command surfaces and distinguish inherited drift from portability failures."""
    inherited_failures: dict[str, dict[str, object]] = {}
    resolved: list[str] = []
    for label, arguments in _command_smokes():
        completed = _run(arguments)
        baseline = _OS_INDEPENDENT_COMMAND_FAILURE_BASELINE.get(label)
        if completed.returncode == 0:
            if baseline is not None:
                resolved.append(label)
            continue
        if baseline is None:
            raise RuntimeError(
                f"{label} failed with {completed.returncode}:\n"
                f"{completed.stdout}{completed.stderr}"
            )
        expected_code, expected_signature = baseline
        diagnostic = f"{completed.stdout}{completed.stderr}"
        if completed.returncode != expected_code or expected_signature not in diagnostic:
            raise RuntimeError(
                f"{label} failure drifted from its OS-independent baseline:\n{diagnostic}"
            )
        inherited_failures[label] = {
            "exit_code": completed.returncode,
            "signature": expected_signature,
        }
    return {
        "inherited_failures": inherited_failures,
        "resolved_baseline_failures": sorted(resolved),
    }


def _report(
    command_results: dict[str, object] | None = None,
    test_results: dict[str, object] | None = None,
) -> dict[str, object]:
    """Return inventory counts, exclusions, runtime, and capability evidence."""
    counts = Counter(disposition for disposition, _reason in _INVENTORY.values())
    symlink_available, symlink_reason = _symlink_capability()
    process_available, process_reason = _child_process_inspection_capability()
    playwright_available, playwright_reason = _playwright_runtime_capability()
    fixture_capabilities = {
        path: _tracked_fixture_capability(path)
        for path in sorted(set(_TRACKED_FIXTURE_CAPABILITY_TEST_CASES.values()))
    }
    native_windows = _native_windows_host()
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
        "mixed_platform_coverage": dict(sorted(_MIXED_PLATFORM_COVERAGE.items())),
        "windows_unsupported_test_cases": dict(sorted(_WINDOWS_UNSUPPORTED_TEST_CASES.items())),
        "capability_gated_test_cases": {
            "child_process_inspection": sorted(_CHILD_PROCESS_INSPECTION_TEST_CASES),
            "playwright_runtime": sorted(_PLAYWRIGHT_RUNTIME_TEST_CASES),
            "symbolic_links": sorted(_SYMLINK_CAPABILITY_TEST_CASES),
            "tracked_fixtures": dict(sorted(_TRACKED_FIXTURE_CAPABILITY_TEST_CASES.items())),
        },
        "os_independent_failure_baseline": {
            path: {
                "owner": baseline.owner,
                "failure_ids": list(baseline.failure_ids),
                "status": baseline.status,
            }
            for path, baseline in sorted(_OS_INDEPENDENT_FAILURE_BASELINE.items())
        },
        "symlink_capability": {
            "available": symlink_available,
            "reason": symlink_reason,
        },
        "child_process_inspection_capability": {
            "available": process_available,
            "reason": process_reason,
        },
        "playwright_runtime_capability": {
            "available": playwright_available,
            "reason": playwright_reason,
        },
        "tracked_fixture_capabilities": {
            path: {"available": available, "reason": reason}
            for path, (available, reason) in fixture_capabilities.items()
        },
        "supported_test_file_count": len(_supported_test_paths()),
        "command_smoke_count": len(_command_smokes()),
        "command_results": command_results,
        "test_results": test_results,
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
    parser.add_argument("--run-test-file", help=argparse.SUPPRESS)
    arguments = parser.parse_args(argv)

    if arguments.run_test_file:
        relative_path = arguments.run_test_file
        if relative_path not in _supported_test_paths():
            parser.error("--run-test-file must name a supported test inventory entry")
        print(_encode_test_outcome(_collect_test_outcome(relative_path)))
        return 0

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
    command_results = _run_command_smokes()
    test_results = None
    if arguments.run_supported_tests:
        test_results = _run_supported_tests()
    print(json.dumps(_report(command_results, test_results), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
