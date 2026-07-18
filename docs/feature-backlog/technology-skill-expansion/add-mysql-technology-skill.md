# Add The MySQL Technology Skill

Status: Proposed

Type: Feature

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

## Notes

- Keep version-sensitive statements grounded in current official MySQL documentation at implementation time.
- Do not make mysql an exclusive alternative to sql; it is a database-specific companion.
