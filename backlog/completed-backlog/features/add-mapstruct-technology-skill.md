# Add The MapStruct Technology Skill

Status: Completed

Type: Feature

## Approval Resolution

- Decision: Approved on 2026-07-19.
- User-message provenance: after receiving the exact MapStruct definition-scope question, the user answered “Approved” in parent coordination thread 019f77f4-c4bd-7c91-b197-c987a7beb838.
- Approved governed scope: create only skills/mapstruct/SKILL.md and skills/mapstruct/agents/openai.yaml.
- Associated ordinary scope: the detection metadata, tests, documentation, and supported generated catalog mirrors already specified by this item and its read-only preflight.
- Exclusions: no agent-role definition change or change to another governed skill definition is authorized.
- Lifecycle boundary: this transaction records the decision while keeping the item Ready. Running ownership and project-artifact work require separate lifecycle and ARTIFACT GO authority.

## Running Ownership

- Owner: Parent Backlog Coordinator root task 019f77f4-c4bd-7c91-b197-c987a7beb838.
- Lifecycle agent: Dev Backlog Steward.
- Lifecycle claim: add-mapstruct-technology-skill-start.
- Claim evidence: PRIMARY exact-file backlog ownership acquired at 2026-07-19T21:57:34.438526Z from clean baseline commit 9bfd57280164a7648c45b189837d289413d1e89e.
- Task anomaly: archived preflight task 019f7a7e-6fce-7bc2-826b-c613c51ee7a1 remains evidence only; the parent retained lifecycle ownership to avoid another parked or duplicate task.
- Scope boundary: this claim owns only the Running transition and is released after its clean commit. Governed definitions, approval-record files, detection metadata, tests, documentation, generated catalog mirrors, verification, integration, installation, and completion remain gated on a later parent-issued ARTIFACT GO.

## Summary

Add a focused MapStruct skill for compile-time Java mapping contracts, annotation-processor configuration, generated implementation evidence, update mappings, null behavior, cycles, qualifiers, inheritance, and framework component models.

## Context

The bundle has Java and framework guidance but no skill for MapStruct's compile-time mapper contract. MapStruct changes can silently alter data exposure, update semantics, null handling, collection replacement, nested mappings, cycle behavior, dependency injection, and generated implementation shape. Build and IDE annotation-processing configuration are also part of correctness because mapper implementations are generated during compilation.

The skill should own mapping semantics and processor verification. Domain model design, API design, persistence mapping, security review, and framework injection remain companion responsibilities.

Authoritative starting point: [MapStruct Stable Reference Guide](https://mapstruct.org/documentation/stable/reference/html/).

Parent series: [Technology Skill Expansion](index.md).

## Requirements

- Create skills/mapstruct/SKILL.md with matching frontmatter name and a concise MapStruct-specific responsibility boundary.
- Cover source and target contract review, explicit unmapped-target policy, conversion selection, null-value strategies, update methods with MappingTarget, collection behavior, nested mappings, cycles, qualifiers, mapper configuration inheritance, component models, and generated implementation inspection.
- Require the annotation processor to run in project-native command-line builds and keep IDE-only success from counting as verification.
- Compose with java, java-design, API, application-security, persistence, framework, and test skills only where those concerns are present.
- Add skills/mapstruct/detection.yaml using Java source plus owning Maven or Gradle evidence for MapStruct annotations or its annotation processor.
- Reject documentation-only mentions, generated output without owning source configuration, and unrelated sibling-module dependencies.
- Generate skills/mapstruct/agents/openai.yaml from the source skill metadata.
- Add MapStruct to README.md, design/skills-modularization.html, generated skill definitions, technology detection registries, explorer data, and the support checklist.
- Add focused bundle-content and technology-detection regression coverage.

## Acceptance Criteria

- A pertinent Java mapper scope with owning MapStruct configuration receives mapstruct and java together.
- An unrelated folder under the same repository does not receive mapstruct solely because a sibling module owns the processor.
- The skill makes create and update mapping semantics explicit and requires generated implementation evidence.
- The skill requires compile-time treatment of unmapped targets and does not rely on reflection-based assumptions.
- Framework component models compose with existing Spring Boot or Quarkus guidance rather than being duplicated.
- Codex metadata, generated catalog artifacts, and repository tests are current.

## Dependencies

None.

## Verification

- Run positive Maven and Gradle detection fixtures for pertinent Java mapper scopes.
- Run negative fixtures for unrelated sibling modules and documentation-only examples.
- Run scripts/validate-agent-skills.py for skills and scripts/openai_metadata.py in check mode.
- Run every generated-output freshness check required by AGENTS.md.
- Run the repository script test suite, the project-wiki script test suite, and git diff validation.

## Completion Evidence

- Approval: the exact definition checks for skills/mapstruct/SKILL.md and skills/mapstruct/agents/openai.yaml used /private/tmp/mapstruct-skill-approval.yaml and /private/tmp/mapstruct-openai-metadata-approval.yaml; both returned ALLOWED_APPROVED_DEFINITION_CHANGE.
- Accepted source: commit bdbd68c49064e34eeeaa636dcca4eb75f22b16a6, released by event 9d3fb5cb-1497-4241-97e3-6ce4b5b1411b.
- Shared finalization: commit da557bd676edfd064284675d0859f5f1a39b7195, released from the isolated assembly by event f4993b97-2808-4aba-b692-00412db470fe.
- Integration: main fast-forwarded byte-identically to da557bd676edfd064284675d0859f5f1a39b7195 and the primary integration claim released cleanly by event 5ae7a396-97e1-4e53-b45d-655b7db7562f.
- Review: a fresh independent post-integration review reported no findings, confirmed the exact 22-file technology scope, and confirmed that unsupported-review commit 12438b8638bcc58cffe6307c8f5c61389e2c71b4 was not included.
- Focused verification: 5 metadata tests, 73 technology-detection tests, and 87 bundle-content tests passed after integration; all four generated-output freshness checks, skill validation for source and Codex adapter skills, OpenAI metadata synchronization, exact candidate comparison, git diff validation, and clean status passed.
- Full verification: 478 repository script tests and 17 project-wiki script tests passed on the byte-identical accepted candidate; they were not rerun after the exact fast-forward because integration changed no bytes and every focused gate passed.
- Terminal authorization: parent task 019f77f4-c4bd-7c91-b197-c987a7beb838 issued TERMINAL LIFECYCLE GO for this separate archive transaction.

## Notes

- Keep version-sensitive statements grounded in current official MapStruct documentation at implementation time.
- Treat generated mapper implementations as verification evidence, not hand-maintained source artifacts.
