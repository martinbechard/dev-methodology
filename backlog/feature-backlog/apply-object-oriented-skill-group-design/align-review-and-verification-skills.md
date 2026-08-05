# Align Review And Verification Skills

Status: Blocked

Type: Feature

Provider: file

Provider Reference: backlog/feature-backlog/apply-object-oriented-skill-group-design/align-review-and-verification-skills.md

Completion: direct-main

Series: backlog/feature-backlog/apply-object-oriented-skill-group-design/index.md

## Summary

Apply the six canonical Review And Verification skill renames, give test-strategy an explicit Select And Run Tests procedure, and update every affected Agent suite and individual skill evaluation.

## Context

The approved names are review-code-with-evidence, verify-end-to-end-workflow, analyze-root-cause, collect-runtime-evidence, trace-code-execution, and review-prompt-contracts. test-strategy remains a multi-concept subject package and exposes Select And Run Tests. These skills are loaded by distinct review, browser, verification, diagnosis, UX, and prompt-review Agents; their role boundaries must remain intact.

## Source Evidence

The user directed in the active Codex task on 2026-08-04: "create separate work items to update skills according to the new design, and update individual evals." The exact names, procedures, and Agent relationships are in design/skill-groups/review-and-verification.md and the proposal registry at reviewed baseline commit c426c970153948f9d5d2d92f1b7b718613a8d4f7.

## Requirements

- Apply all six canonical renames, including frontmatter, metadata, exact Agent references, catalogs, fixtures, and generated mirrors.
- Rename test-strategy Workflow to Select And Run Tests without changing its technology-routing or coverage authority boundaries.
- Preserve separation among evidence-first review, test selection, end-to-end verification, root-cause analysis, runtime evidence, execution tracing, and prompt-contract review.
- Keep code-discovery as an external two-procedure dependency rather than absorbing it into diagnosis skills.
- Update every affected Agent suite and add or update an individual behavioral evaluation for all seven skills.
- Preserve historical result records and classify old-name occurrences before retaining them.

## Acceptance Criteria

- The six proposed names are the only maintained live identities for their responsibilities.
- test-strategy exposes Select And Run Tests and still does not rerun setup-time technology detection.
- Each Agent definition loads the correct renamed skill and retains its read-only, mutation, runtime, and delivery boundaries.
- Each skill has focused behavioral evidence for its public procedure and important negative boundary.
- Generated mirrors, catalogs, affected suites, and full evaluation coverage validation pass.

## Dependencies

- backlog/feature-backlog/apply-object-oriented-skill-group-design/align-integration-and-delivery-skills.md

## Verification

- Run the supported definition-change precheck for every governed canonical path below.
- Run individual skill probes and focused suites for Dev Code Reviewer, Dev Browser Operator, Dev UX Specialist, Dev Verifier, Dev Runtime Diagnostician, and Dev Prompt Reviewer.
- Run scripts/test_agent_skill_evals.py, scripts/test_eval_coverage_catalog.py, scripts/test_bundle_content.py, relevant runtime and prompt contract tests, and generated-output freshness checks.
- Search maintained sources for all six former identities and classify any retained historical evidence.
- Run git diff --check and obtain independent methodology review and verification.

## Open Questions

Resolve whether any generic Workflow heading contains more than one independent public procedure; add another heading only when the source instructions establish a separate invocation boundary.

## Crisis Dependency Reclassification

Reclassified At: 2026-08-05T17:10:30Z.

Transition: Ready -> Blocked.

Owner: Unowned.

Exact Blocker: Required dependency backlog/feature-backlog/apply-object-oriented-skill-group-design/align-integration-and-delivery-skills.md is Blocked.

Blocker Owner: Dev Backlog Coordinator resolving the named dependency chain in Backlog Crisis Mode.

Unblock Condition: Align Integration And Delivery Skills reaches a terminal successful disposition and its delivered integration and delivery identities are available on current main.

Coordinator Next Action: Keep this item in the crisis dependency set and do not dispatch it. After the unblock condition is satisfied, reconcile it through Blocked -> Ready under the normal lifecycle.

## Governed Definition Approval

### Governed Canonical Sources

- skills/code-review-evidence/SKILL.md
- skills/code-review-evidence/agents/openai.yaml
- skills/review-code-with-evidence/SKILL.md
- skills/review-code-with-evidence/agents/openai.yaml
- skills/test-strategy/SKILL.md
- skills/end-to-end-verification/SKILL.md
- skills/end-to-end-verification/agents/openai.yaml
- skills/verify-end-to-end-workflow/SKILL.md
- skills/verify-end-to-end-workflow/agents/openai.yaml
- skills/root-cause-analysis/SKILL.md
- skills/root-cause-analysis/agents/openai.yaml
- skills/analyze-root-cause/SKILL.md
- skills/analyze-root-cause/agents/openai.yaml
- skills/runtime-evidence-collection/SKILL.md
- skills/runtime-evidence-collection/agents/openai.yaml
- skills/collect-runtime-evidence/SKILL.md
- skills/collect-runtime-evidence/agents/openai.yaml
- skills/code-execution-tracing/SKILL.md
- skills/code-execution-tracing/agents/openai.yaml
- skills/trace-code-execution/SKILL.md
- skills/trace-code-execution/agents/openai.yaml
- skills/prompt-contracts/SKILL.md
- skills/prompt-contracts/agents/openai.yaml
- skills/review-prompt-contracts/SKILL.md
- skills/review-prompt-contracts/agents/openai.yaml
- agents/roles/dev-activities/dev-code-reviewer.role.yaml
- agents/roles/dev-activities/dev-browser-operator.role.yaml
- agents/roles/dev-activities/dev-ux-specialist.role.yaml
- agents/roles/dev-activities/dev-verifier.role.yaml
- agents/roles/dev-activities/dev-runtime-diagnostician.role.yaml
- agents/roles/dev-activities/dev-prompt-reviewer.role.yaml

### Allowed Dependent Artifacts

- approval-record-align-review-and-verification-skills.yaml
- evals/skill-probes.yaml
- evals/cases.yaml
- evals/workflow-packs.yaml
- evals/agent-tests/dev-code-reviewer
- evals/agent-tests/dev-browser-operator
- evals/agent-tests/dev-ux-specialist
- evals/agent-tests/dev-verifier
- evals/agent-tests/dev-runtime-diagnostician
- evals/agent-tests/dev-prompt-reviewer
- scripts/test_agent_skill_evals.py
- scripts/test_eval_coverage_catalog.py
- scripts/test_bundle_content.py
- README.md
- design/agent-and-skill-definitions.html
- design/agent-and-skill-evaluations.html
- design/generated/skill-definitions.js
- design/generated/role-definitions.js
- generated/adapters files regenerated from only the approved canonical sources
- Directly related non-governed documentation, fixtures, and focused tests required to keep these approved definitions coherent

### Approval Resolution

Approved at creation on 2026-08-04 by the user statement in the active Codex task: "create separate work items to update skills according to the new design, and update individual evals." The reviewed Review And Verification diagram shows the exact skill identities and six exact Agent definitions covered here. Approval is limited to the governed canonical paths listed above. Any additional governed definition requires new explicit user approval recorded in this item.
