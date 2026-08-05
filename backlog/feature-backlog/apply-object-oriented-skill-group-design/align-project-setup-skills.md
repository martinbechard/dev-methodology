# Align Project Setup Skills

Status: Blocked

Type: Feature

Provider: file

Provider Reference: backlog/feature-backlog/apply-object-oriented-skill-group-design/align-project-setup-skills.md

Completion: direct-main

Series: backlog/feature-backlog/apply-object-oriented-skill-group-design/index.md

## Current Dispatch Reservation

Transition: Ready -> Starting.
Parent Coordination Thread: /root/apply_skill_group_design_backlog.
Launch Reservation: One distinct bounded launch reservation for this provider record.
Normalized Objective: Align Project Setup skills with the approved object-oriented design and update their individual evaluations.
Dispatch Time: 2026-08-05T03:43:25Z.
Intended Root Dev Orchestrator Role: Dev Orchestrator.
Owner: Unowned pending accepted root.
Current Launch Evidence: Parent Coordinator authorized this exact reservation; exact-file backlog claim reserve-align-project-setup-skills acquired with outcome SHARED_CHECKOUT_ACQUIRED and event 709aa785-38fb-4ecf-8964-3576c879aa80. Runtime Thread creation and root acceptance have not occurred.
Required Next Lifecycle Transition: The root Dev Orchestrator must separately accept Starting -> Running before repository mutation.
Reconciliation: Root acceptance recorded separately below; the parent reservation remains preserved.

## Current Running Acceptance

Transition: Starting -> Running.
Canonical Thread: /root/apply_skill_group_design_backlog/align_project_setup_skills.
Root Agent Task: /root/apply_skill_group_design_backlog/align_project_setup_skills.
Owner: Dev Orchestrator.
Branch: codex/align-project-setup-skills.
Worktree: /Users/martinbechard/dev/dev-methodology/.worktrees/align-project-setup-skills.
Phase: Accepted ownership / implementation preparation.
Started At: 2026-08-05T03:47:58Z.
Claim Evidence: The private delivery lane is claim-free because private-worktree implementation triggers no Event Contract claim. This exact primary-main backlog mutation is protected by exact-file claim running-align-project-setup-skills, acquired with outcome SHARED_CHECKOUT_ACQUIRED and event c8a908b3-a99d-44ce-9e04-b148c75cf1f3.
Preserved Coordination: Parent Coordination Thread /root/apply_skill_group_design_backlog and its Ready -> Starting launch reservation remain canonical.

## Summary

Give detect-technology-skills and create-project-configuration explicit public procedure headings while preserving direct exact-name loading and per-skill technology selection in AGENTS.md.

## Context

The reviewed Project Setup design rejects a synthetic selected-skill-set interface because generated AGENTS.md names each confirmed technology skill independently. The two direct Project Setup skills keep their current names and gain Detect Technology Skills and Create Or Update Project Configuration procedure headings.

## Source Evidence

The user directed in the active Codex task on 2026-08-04: "create separate work items to update skills according to the new design, and update individual evals." The exact approved design is design/skill-groups/project-setup.md at reviewed baseline commit c426c970153948f9d5d2d92f1b7b718613a8d4f7.

## Confirmed Defect Record

Fresh Dev Code Reviewer task /root/apply_skill_group_design_backlog/align_project_setup_skills/review_candidate confirmed a Medium defect in candidate 49e8616b1c00b0e241a5fd5e4cd1a498562e2c2a. evals/agent-tests/project-configurator/test_fixtures.py around line 165 and scripts/test_bundle_content.py around line 8705 only assert aggregate-interface or selected-skill-set prose. Project Bootstrapper scenarios.yaml around line 80 only declares the forbidden behavior. The tests still pass if an evaluator accepts a synthetic aggregate node, so the negative acceptance criterion is unproved.

Runnable next action: correction attempt 1 remains assigned to the original coder in this delivery. Add adversarial Project Configurator and Project Bootstrapper verdict cases that reject synthetic aggregate or selected-skill-set output and accept exact per-skill routing. Run the new targeted methods through the two existing test files, then obtain fresh independent review and verification. This is evidence attached to this provider record, not a separate delivery.

Fresh re-review task /root/apply_skill_group_design_backlog/align_project_setup_skills/rereview_correction confirmed a second Medium defect in replacement candidate e27b51e8d885b30bf195198c116d79817b219dee. Project Configurator test_fixtures.py around line 26 and Project Bootstrapper scripted_orchestration.py around line 72 require len(required_skills) == 1, which rejects valid composed exact-name folder routes. Canonical PROJECT.yaml around line 447 validly routes [fastapi, python], and the production renderer around line 1709 iterates every listed skill. A reproduction using one folder with required_skills [fastapi, python] returns configurator=FAIL and bootstrapper=FAIL.

Correction attempt 1 failed. Correction attempt 2 is assigned to the original coder in this delivery: accept any non-empty list of non-empty exact skill identifiers in both evaluators; add the [fastapi, python] one-folder positive control; retain exact FAIL for aggregate-interface or selected-skill-set output; and rerun the three focused methods. This remains evidence attached to this provider record, not a separate delivery.

## Requirements

- Rename the generic Workflow headings to the two proposed public procedure headings.
- Preserve all current evidence, configuration, authority, and generated-guidance boundaries.
- Do not introduce one interface node or aggregate procedure for the selected technology-skill set.
- Update individual evaluations so each procedure is invoked by its public vocabulary and its important negative boundaries remain covered.

## Acceptance Criteria

- Both SKILL.md files expose the proposed procedure heading without changing their exact skill names.
- Project setup still records and renders each confirmed technology skill by exact name.
- Project Configurator and Project Bootstrapper evaluations exercise the revised public procedure wording and reject unsupported technology-selection shortcuts.
- Generated mirrors and focused tests are fresh and passing.

## Dependencies

None.

## Verification

- Run the supported definition-change precheck for both governed paths.
- Run focused Project Configurator, Project Bootstrapper, technology-detection, project-configuration, and skill-probe evaluations.
- Run scripts/test_agent_skill_evals.py, scripts/test_eval_coverage_catalog.py, scripts/test_bundle_content.py, and renderer freshness checks.
- Run git diff --check and obtain independent methodology review and verification.

## Open Questions

None.

## Blocked Handoff

Transition: Running -> Blocked.
Coordinator Decision: The fresh independent methodology-artifact review confirmed that the same acceptance criterion remains unresolved after the two permitted correction attempts. No third correction attempt is authorized.
Canonical Thread: /root/apply_skill_group_design_backlog/align_project_setup_skills.
Canonical Root Agent Task: /root/apply_skill_group_design_backlog/align_project_setup_skills.
Owner: Unowned.
Preserved Clean Candidates:

- 49e8616b1c00b0e241a5fd5e4cd1a498562e2c2a
- e27b51e8d885b30bf195198c116d79817b219dee
- 1ef05295

Blocker: The Project Configurator and Project Bootstrapper evaluators still accept whitespace-only identifiers and a well-shaped synthetic selected-skill-set. They validate only non-empty strings and container shape, rather than identifiers from an explicit confirmed repository/runtime catalog.
Blocker Owner: Dev Backlog Coordinator.
Attempt History: The first fresh code review passed after correction attempt 2. A subsequent independent methodology-artifact review confirmed the unresolved criterion. The first and second correction attempts are therefore exhausted.
Requested Recovery Action: Preserve this evidence and candidate history. Do not mutate the implementation or integrate it while Blocked.
Unblock Condition: A later parent-authorized recovery must retain this same canonical task, record Blocked -> Ready -> Starting -> Running through the normal provider boundaries, then validate stripped identifiers against an explicit confirmed catalog. It must reject empty, whitespace-only, duplicate, unknown, and synthetic identifiers including selected-skill-set; preserve valid single identifiers and the composed [fastapi, python] route; add executable FAIL controls in both agents; and obtain fresh source review, artifact review, and verifier acceptance. If any material finding remains, keep this item Blocked.
Evidence: Candidate 1ef05295 passed fresh source review. The independent artifact review found the catalog-validation gap described above. No delivery or main-integration claim was acquired.

## Governed Definition Approval

### Governed Canonical Sources

- skills/detect-technology-skills/SKILL.md
- skills/create-project-configuration/SKILL.md

### Allowed Dependent Artifacts

- approval-record-align-project-setup-skills.yaml
- evals/skill-probes.yaml
- evals/cases.yaml
- evals/workflow-packs.yaml
- evals/agent-tests/project-configurator
- evals/agent-tests/project-bootstrapper
- evals/projects/project-configuration-routing
- scripts/test_technology_detection.py
- scripts/test_agent_skill_evals.py
- scripts/test_eval_coverage_catalog.py
- scripts/test_bundle_content.py
- README.md
- design/agent-and-skill-definitions.html
- design/agent-and-skill-evaluations.html
- design/generated/skill-definitions.js
- generated/adapters files regenerated from only the approved canonical sources
- Directly related non-governed documentation and focused tests required to keep these approved definitions coherent

### Approval Resolution

Approved at creation on 2026-08-04 by the user statement in the active Codex task: "create separate work items to update skills according to the new design, and update individual evals." Approval is limited to the two governed canonical paths listed above. Any additional governed definition requires new explicit user approval recorded in this item.
