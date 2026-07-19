# Add The MySQL Technology Skill

Status: Completed

Type: Feature

## Approval Resolution

- Decision: Approved on 2026-07-19.
- User-message provenance: the user said, “MySQL skill is approved,” in parent coordination thread 019f77f4-c4bd-7c91-b197-c987a7beb838.
- Approved governed scope: create only skills/mysql/SKILL.md and skills/mysql/agents/openai.yaml.
- Associated ordinary scope: the detection metadata, tests, documentation, and supported generated catalog mirrors already specified by this item and its read-only preflight.
- Exclusions: no agent-role definition change, replacement of the general SQL skill, installation, or expansion to another governed definition is authorized.
- Lifecycle boundary: the approval-record transaction kept the item Ready. Running ownership and later project-artifact work require their own separate lifecycle and ARTIFACT GO authority.

## Running Ownership

- Owner: Dev Orchestrator root task 019f77f4-c4bd-7c91-b197-c987a7beb838.
- Canonical task: 019f79e6-25ef-7b51-ab3c-39fce2656db4.
- Lifecycle agent: Dev Backlog Steward.
- Lifecycle claim: add-mysql-technology-skill-start.
- Claim evidence: PRIMARY exact-file backlog ownership acquired at 2026-07-19T18:50:56.342798Z from clean baseline commit f8b9ee0c870bb2afc312b64ba0741633b0d0ea4b.
- Scope boundary: this claim owns only the Running transition and is released after its clean commit. Skill definitions, detection metadata, tests, documentation, generated catalog mirrors, verification, integration, installation, and backlog completion remain gated on a later parent-issued ARTIFACT GO.

## Summary

Add a focused MySQL skill that complements vendor-neutral SQL guidance with MySQL and InnoDB behavior for schema design, query plans, transactions, locking, indexes, migrations, and production verification.

## Context

The bundle has a vendor-neutral SQL skill and framework-specific persistence skills, but it does not provide MySQL engine guidance. MySQL-specific work needs explicit treatment of storage engine behavior, clustered and secondary indexes, isolation and locking semantics, deadlock retries, character sets and collations, online schema-change risk, replication implications, and EXPLAIN evidence.

The skill must remain database-specific. It should not duplicate generic query correctness, parameterization, transaction ownership, ORM mapping, or migration-tool rules already owned by SQL and companion skills.

Authoritative starting point: [MySQL 8.4 Reference Manual](https://dev.mysql.com/doc/refman/8.4/en/).

Parent series: [Technology Skill Expansion](index.md).

## Requirements

- Create skills/mysql/SKILL.md with matching frontmatter name and a concise MySQL-specific responsibility boundary.
- Cover InnoDB transaction and locking behavior, clustered and secondary index consequences, query-plan evidence, deadlock handling, charset and collation choices, foreign-key and DDL implications, and production-engine verification.
- Compose with sql and applicable migration, framework, ORM, and testing skills instead of copying their general guidance.
- Add skills/mysql/detection.yaml with evidence-backed activation for supported owning project manifests or MySQL connection configuration plus pertinent source in the selected scope.
- Recognize established MySQL connector or driver evidence across the detector's supported manifest formats where the owning project and selected folder make the skill relevant.
- Reject documentation-only mentions, example configuration outside the owning boundary, and unrelated sibling modules.
- Generate skills/mysql/agents/openai.yaml from the source skill metadata.
- Add MySQL to README.md, design/skills-modularization.html, generated skill definitions, technology detection registries, explorer data, and the support checklist.
- Add focused bundle-content and technology-detection regression coverage.

## Acceptance Criteria

- MySQL work in a pertinent source folder receives mysql and sql together.
- A MySQL dependency or connection example in an unrelated documentation folder does not activate mysql.
- The skill distinguishes MySQL and InnoDB behavior from vendor-neutral SQL rules.
- The skill does not assume one ORM, migration framework, application framework, or test runner.
- Codex metadata and all generated catalog artifacts are current.
- Repository validation passes with no stale generated output.

## Dependencies

None.

## Verification

- Run the focused MySQL detection tests against positive and negative temporary project fixtures.
- Run scripts/validate-agent-skills.py for skills.
- Run scripts/openai_metadata.py in check mode.
- Run every generated-output freshness check required by AGENTS.md.
- Run the repository script test suite, the project-wiki script test suite, and git diff validation.

## Completion Evidence

- Approval: the exact definition checks for skills/mysql/SKILL.md and skills/mysql/agents/openai.yaml used /private/tmp/mysql-skill-approval.yaml and /private/tmp/mysql-openai-metadata-approval.yaml; both returned ALLOWED_APPROVED_DEFINITION_CHANGE.
- Accepted source: commit 050f63bbaa0f4cbd8d4b47742ed9a15f1aa597e1, released by event 0dcc91b6-ab61-46bf-b6b7-160a618135d6.
- Shared finalization: commit da557bd676edfd064284675d0859f5f1a39b7195, released from the isolated assembly by event f4993b97-2808-4aba-b692-00412db470fe.
- Integration: main fast-forwarded byte-identically to da557bd676edfd064284675d0859f5f1a39b7195 and the primary integration claim released cleanly by event 5ae7a396-97e1-4e53-b45d-655b7db7562f.
- Review: a fresh independent post-integration review reported no findings, confirmed the exact 22-file technology scope, and confirmed that unsupported-review commit 12438b8638bcc58cffe6307c8f5c61389e2c71b4 was not included.
- Focused verification: 5 metadata tests, 73 technology-detection tests, and 87 bundle-content tests passed after integration; all four generated-output freshness checks, skill validation for source and Codex adapter skills, OpenAI metadata synchronization, exact candidate comparison, git diff validation, and clean status passed.
- Full verification: 478 repository script tests and 17 project-wiki script tests passed on the byte-identical accepted candidate; they were not rerun after the exact fast-forward because integration changed no bytes and every focused gate passed.
- Terminal authorization: parent task 019f77f4-c4bd-7c91-b197-c987a7beb838 issued TERMINAL LIFECYCLE GO for this separate archive transaction.

## Notes

- Keep version-sensitive statements grounded in current official MySQL documentation at implementation time.
- Do not make mysql an exclusive alternative to sql; it is a database-specific companion.
