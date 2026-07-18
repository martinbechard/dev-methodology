# Split Hibernate ORM With Panache From Quarkus Persistence

Status: Proposed

Type: Feature

## Summary

Create a focused Hibernate ORM with Panache skill and reduce Quarkus Persistence to a concise shared foundation for persistence-stack selection, schema alignment, persistence units, and common database verification.

## Context

skills/quarkus-persistence currently combines standard Hibernate ORM, Hibernate Reactive, Panache active record and repository styles, entity mapping, queries, pagination, locking, transaction models, schema ownership, and database verification. That scope is too broad for routine blocking Hibernate ORM with Panache work and loads reactive guidance when it is not pertinent.

Blocking Hibernate ORM with Panache has a distinct contract: active record versus repository style, PanacheEntity and PanacheEntityBase identifiers, PanacheQuery paging and range state, projections, named queries, transaction boundaries, locking, persistence units, generated accessors, and test verification. Reactive APIs and reactive transaction behavior must remain outside this new skill.

Authoritative starting point: [Hibernate ORM with Panache Guide](https://quarkus.io/guides/hibernate-orm-panache).

Parent series: [Technology Skill Expansion](index.md).

## Requirements

- Create skills/hibernate-orm-panache/SKILL.md with matching frontmatter name and a blocking Hibernate ORM with Panache boundary.
- Move Panache-specific active record, repository, query, paging, range, projection, identifier, transaction, flush, and lock guidance out of quarkus-persistence into the focused skill.
- Keep skills/quarkus-persistence concise and limited to shared stack selection, ORM versus reactive boundary recognition, persistence-unit and schema alignment, database fidelity, and routing to specialized companions.
- Remove reactive-specific instructions from hibernate-orm-panache and avoid implying that reactive REST requires Hibernate Reactive.
- Update the Quarkus Persistence reference and review checklist so they do not retain duplicate Panache implementation rules.
- Add skills/hibernate-orm-panache/detection.yaml using Java source plus owning quarkus-hibernate-orm-panache extension evidence.
- Keep quarkus-persistence detection for the broader Quarkus ORM and Hibernate Reactive persistence families.
- Ensure quarkus-hibernate-reactive-panache does not activate hibernate-orm-panache.
- Generate skills/hibernate-orm-panache/agents/openai.yaml from the source skill metadata.
- Update README.md, design/skills-modularization.html, generated skill definitions, technology detection registries, explorer data, support checklist, and regression tests.

## Acceptance Criteria

- A Java scope owned by quarkus-hibernate-orm-panache receives hibernate-orm-panache, quarkus-persistence, quarkus, java, and sql through composition.
- A scope owned only by quarkus-hibernate-reactive-panache does not receive hibernate-orm-panache.
- The new skill contains no reactive session, reactive transaction, or reactive return-type instructions.
- Quarkus Persistence is materially shorter and no longer duplicates detailed Panache query or repository guidance.
- Existing Quarkus persistence detection remains valid for standard and reactive ORM scopes.
- Codex metadata, generated catalog artifacts, and repository tests are current.

## Dependencies

None.

## Verification

- Add positive detection coverage for quarkus-hibernate-orm-panache.
- Add negative detection coverage for quarkus-hibernate-reactive-panache and unrelated Quarkus source.
- Assert the focused skill boundary and the reduced Quarkus Persistence boundary in bundle-content tests.
- Run scripts/validate-agent-skills.py for skills and scripts/openai_metadata.py in check mode.
- Run every generated-output freshness check required by AGENTS.md.
- Run the repository script test suite, the project-wiki script test suite, and git diff validation.

## Notes

- A separate Hibernate Reactive with Panache skill may be proposed later; it is not part of this item.
- Preserve stable quarkus-persistence consumers while narrowing its content rather than renaming or deleting the existing skill.
