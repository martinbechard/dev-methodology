# Replace Provider-Record Terminology with Work-Item Content Authority

Status: Ready

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
