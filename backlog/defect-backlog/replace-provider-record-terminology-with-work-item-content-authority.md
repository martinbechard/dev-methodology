# Replace Provider-Record Terminology with Work-Item Content Authority

Status: Running

Type: Defect

Provider: file

Work Item ID: replace-provider-record-terminology-with-work-item-content-authority

Completion: main-branch

## Summary

Correct the work-item methodology so it consistently states that the work-item content is the work-item authority and that the Persistence provider determines the specific storage format. Stop using provider record or provider records as the generic name for authoritative work-item content.

## Context

Current coordination, lifecycle, role, design, and test text repeatedly calls authoritative work-item content a provider record and sometimes states that the provider record or provider is the lifecycle authority. This wording conflates the provider-specific storage mechanism with the provider-neutral Work item and causes agents and users to call Work items provider records.

The canonical replacement concept is:

> The work-item content is the work-item authority and is stored according to the Persistence provider's specific format.

Initial affected sources include skills/coordinate-work-items/SKILL.md, skills/manage-work-items/SKILL.md, provider-specific create and management skills, skills/resource-claim/SKILL.md, skills/coordinate-codex-tasks/SKILL.md, Dev Backlog role definitions, design/orchestrated-development-lifecycle.html, design/work-item-provider-and-completion-contracts.md, design/documentation-templates.html, and their focused assertions. Generated Agent configuration and other generated artifacts must be updated only through their owning generators.

## Source Evidence

On 2026-08-11 in Codex task 019ff2f9-0863-7133-aac0-ff141cf16a92, the user corrected the terminology and directed: "it should say: \"the work-item content is the work-item authority and is stored according to the persistence provider's specific format\". Add a defect to correct that wording so people will stop calling them provider records".

## Requirements

- Establish the user's sentence as the provider-neutral authority rule, using the repository's canonical capitalization for Work item and Persistence where applicable without changing its meaning.
- Replace provider record and provider records when those phrases generically name authoritative Work-item content, lifecycle authority, durable state, recovery state, or queue state.
- State that the selected Persistence provider owns storage format, provider-native identity and relationships, supported operations, and storage-specific location evidence without making the provider itself or a provider record the Work-item authority.
- Update provider-neutral skills, provider-specific skills, role sources, maintained design documentation, templates, examples, and focused assertions that encode the incorrect terminology.
- Regenerate generator-owned Agent configuration and documentation from authoritative sources; do not edit generated outputs directly.
- Preserve legitimate provider-specific terminology where it describes an actual storage object or provider operation and does not rename the provider-neutral Work item.
- Keep Work Item ID, lifecycle, Commit delivery, Git evidence, resource claims, runtime evidence, and provider-none behavior semantically unchanged.
- Do not rewrite completed or failed historical work-item content solely to modernize terminology.

## Acceptance Criteria

- Provider-neutral methodology explicitly states that the Work-item content is the Work-item authority and is stored according to the Persistence provider's specific format.
- No maintained current source, generated Agent configuration, design page, template, or focused assertion calls authoritative Work-item content a provider record or states that a provider record or provider is the Work-item or lifecycle authority.
- Provider-specific descriptions clearly distinguish storage format and native provider objects from provider-neutral Work-item content.
- Provider none continues to use task-local result evidence without inventing a durable Work item or Persistence storage format.
- Focused negative assertions reject reintroduction of provider record terminology for provider-neutral Work-item authority.
- All affected generators are fresh, relevant skill and role validation passes, and Git diff checks pass.
- Fresh independent review and verification confirm that the terminology correction changes wording and conceptual ownership without changing lifecycle, delivery, claim, or provider behavior.

## Dependencies

None.

## Verification

- Search all maintained current sources and generated outputs for provider record, provider records, and statements assigning Work-item or lifecycle authority to a provider; classify every remaining match as legitimate provider-specific storage terminology or a defect.
- Run focused work-item coordination, bundle-content, role-policy, template, and provider-family tests affected by the corrected statements.
- Run the owning generators and their freshness checks for every changed generated output.
- Validate every changed skill and role source and run Git diff checks.
- Obtain fresh independent terminology, methodology, source, and verification review.

## Open Questions

- Which remaining uses of record describe a genuine provider-native storage object and should be retained with explicit provider-specific qualification?

## Notes

- Historical archived Work items remain evidence of the terminology in use when they were created and are not migration targets.
- This defect changes terminology and conceptual authority only; it does not redesign Persistence providers or lifecycle behavior.

## Starting Handoff Evidence

- Reserved At: 2026-08-13T13:08:59Z.
- Transition: `Ready -> Starting`.
- Runtime Parent Task: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Coordinator Execution: `/root/backlog_coordinator`.
- Baseline: `5a6fd30cc79d12ceedd85f5f08b3091565a844a0` on primary `main`.
- Capacity: Uses one of two available slots after `estimate-agent-work` entered User Action Required and `keep-user-decisions-in-visible-worker-tasks` completed external cleanup. Active usage becomes four of five.
- Dependencies: None. The item is independent of active evaluation-terminology, dependency-routing, and Project Configurator receipt work.
- Overlap: The completed dispatcher correction is already integrated on `main`. The new execution must claim exact approved paths before mutation and reconcile any later shared generated-output overlap rather than acquiring broad ownership.
- Dispatch Architecture: Create one visible Codex task whose initial prompt launches one Dev Orchestrator subagent and states the visible root title-and-messaging responsibility.
- Transition Claims: Work Item `start-replace-provider-record-terminology-work-item`; event `374ca7bf-24e1-4712-b916-b7d6f0219342`. Provider `start-replace-provider-record-terminology-provider`; event `1955c585-35ee-4e91-b08f-7b308df9eed4`.
- Runtime Identity: Pending caller-owned visible task creation. Creation does not imply Running.

## Canonical Runtime Assignment

- Assigned At: 2026-08-13T13:10:38Z.
- Codex Task ID: `019ffb3e-c71d-7593-8cd1-c566b1678667`.
- Conversation ID: `019ffb3e-c71d-7593-8cd1-c566b1678667`.
- Host: `local`.
- Runtime Parent Task: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Requested Title: `Starting — Replace Provider Record Terminology With Work Item Content Authority`.
- Initial Action: The visible root starts one Dev Orchestrator subagent for this authoritative Work Item and owns required Codex title and subagent messaging.
- Creation Outcome: Unique direct `threadId` and host success in the saved dev-methodology project, with no client or pending identity and no retry.
- Lifecycle Boundary: This assignment remains `Starting` until the nested Dev Orchestrator accepts and records `Starting -> Running`.
- Adoption Claims: Work Item `adopt-provider-terminology-task`; event `e37607d1-68cc-4ffb-9a17-2db317889f54`. Provider `adopt-provider-terminology-provider`; event `6e2e03c0-7048-4cbb-a0d4-364f7358fbc5`.

## Running Acceptance Evidence

- Accepted At: 2026-08-13T13:11:48Z.
- Transition: `Starting -> Running`.
- Canonical Codex Task ID: `019ffb3e-c71d-7593-8cd1-c566b1678667`.
- Canonical Conversation ID: `019ffb3e-c71d-7593-8cd1-c566b1678667`.
- Runtime Parent Task: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Coordinator Execution: `/root/backlog_coordinator`.
- Accepted Owner: `/root/replace_provider_record_terminology` acting as Dev Orchestrator.
- Work Item Claim: `replace-provider-record-terminology-running-update`; event `cd6f9199-8b38-4d13-847f-34997d98c3bc`.
