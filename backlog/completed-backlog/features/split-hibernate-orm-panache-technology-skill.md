# Split Hibernate ORM With Panache From Quarkus Persistence

Status: Completed

Type: Feature

## Running Ownership

- Owner: Dev Orchestrator root task 019f77f4-c4bd-7c91-b197-c987a7beb838.
- Canonical task: 019f7d90-88e6-7333-b0ef-1e87b061527a.
- Lifecycle agent: Dev Backlog Steward.
- Lifecycle claim: hibernate-panache-split-lifecycle.
- Claim evidence: PRIMARY exact-file backlog ownership acquired at 2026-07-20T02:38:16.677214Z from clean baseline commit ff6c23fc2a5ca789f83e14f45f71f6c08154bd3b.
- Scope boundary: this claim owns only the Running transition and is released after its clean commit. Unique skill sources use a separate canonical isolated claim; shared catalogs, tests, generated outputs, review, verification, and integration remain separately owned.

## Definition Approval

- User direction: “The hibernate split is approved.”
- Approval date: 2026-07-19.
- Provenance: User direction delegated through Codex parent task 019f77f4-c4bd-7c91-b197-c987a7beb838.
- Authorized governed scope: create skills/hibernate-orm-panache/SKILL.md and skills/hibernate-orm-panache/agents/openai.yaml; modify skills/quarkus-persistence/SKILL.md; update its persistence guidance and review-checklist references; update corresponding detection metadata and only the supported generated mirrors.
- Excluded scope: agent-role definition changes, a Hibernate Reactive with Panache skill, and changes to any other governed skill definition.

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

## Completion Evidence

- Accepted source lineage: commits 0e7f07462256c0a843fb768a5ea909b58fdbb333, 672f16d3f41a3a86ce35a267f2f6948e027c6caa, and e0e0d50d910a36fa333b4a792c6a85dec7ae28a9 were preserved byte-for-byte in finalization commit 7840fb3e29e6ece46f291cce2be067e76cbf7c36.
- Source finalization: the exact 16-file contribution was independently accepted and proportionally verified before its claim released cleanly at event 638711f8-f69e-4970-ab3c-bc3c7be2ca80.
- Integration: main fast-forwarded from accepted base 3f75ea58ee38fcba0d6bc6d7515a6d656c3ac037 to 7840fb3e29e6ece46f291cce2be067e76cbf7c36 under exact primary integration claim acquisition d2161df8-8e45-4de7-932f-badf99c3891c; the claim released cleanly at event 24a971a3-3351-4b70-8fe6-c099ec14028f.
- Post-integration review: a fresh independent review on the later clean main lineage reported ACCEPTED with no findings or open questions, confirmed all six governed source blobs remained identical to the accepted commit, and confirmed later generated-catalog updates preserved the Hibernate ORM With Panache records.
- Focused verification: the Dev Verifier reran the complete bounded gate on clean main at ded845bf39f8f21c1cb9a2b250141a38ab8c5c5c. Three Hibernate detection regressions, seven affected bundle-content tests, two evaluation-catalog tests, both affected skill validations, path-scoped OpenAI metadata synchronization, all three relevant generated-output freshness checks, ancestry, git diff validation, and clean status passed.
- Concurrency reconciliation: main later advanced through unrelated backlog, evaluation, and wiki-candidate commits to terminal-claim baseline 3ebf5974a43466936ea9f1e803e34ed199d947e5. The accepted commit remained an ancestor and none of the exact 16 Hibernate/Panache paths changed after the fresh verifier.
- Verification scope: broad repository, project-wiki, live, and browser suites were intentionally omitted by terminal direction. An unrelated stale coordination-skill metadata warning was excluded from this item.
- Terminal authorization: parent task 019f77f4-c4bd-7c91-b197-c987a7beb838 issued POST-INTEGRATION / TERMINAL GO and TERMINAL CLAIM RETRY GO for this separate archive transaction.

## Notes

- A separate Hibernate Reactive with Panache skill may be proposed later; it is not part of this item.
- Preserve stable quarkus-persistence consumers while narrowing its content rather than renaming or deleting the existing skill.
