# Add The Quartz Scheduler Technology Skill

Status: Running

Type: Feature

## Approval Resolution

- Decision: Approved on 2026-07-19.
- User-message provenance: after receiving the exact Quartz definition-scope question, the user answered “Approved” in parent coordination thread 019f77f4-c4bd-7c91-b197-c987a7beb838.
- Approved governed scope: create only skills/quartz/SKILL.md and skills/quartz/agents/openai.yaml.
- Associated ordinary scope: the detection metadata, tests, documentation, and supported generated catalog mirrors already specified by this item and its read-only preflight.
- Exclusions: no agent-role definition change or change to another governed skill definition is authorized.
- Lifecycle boundary: this transaction records the decision while keeping the item Ready. Running ownership and project-artifact work require separate lifecycle and ARTIFACT GO authority.

## Running Ownership

- Owner: Parent Backlog Coordinator root task 019f77f4-c4bd-7c91-b197-c987a7beb838.
- Lifecycle agent: Dev Backlog Steward.
- Lifecycle claim: add-quartz-technology-skill-start.
- Claim evidence: PRIMARY exact-file backlog ownership acquired at 2026-07-19T21:56:21.320859Z from clean baseline commit 0fd9ee91d1ab17ff459de0810a88927aa9633005.
- Task anomaly: archived preflight task 019f7a78-6b0d-7cd3-836e-818e4d495c3f could not be resumed because its archived rollout file was missing, so the parent retained lifecycle ownership rather than creating a duplicate task.
- Scope boundary: this claim owns only the Running transition and is released after its clean commit. Governed definitions, approval-record files, detection metadata, tests, documentation, generated catalog mirrors, verification, integration, installation, and completion remain gated on a later parent-issued ARTIFACT GO.

## Summary

Add a focused Quartz Scheduler skill for Java job and trigger contracts, calendars, misfires, concurrency, durable job storage, clustering, recovery, and scheduler verification.

## Context

The bundle has Java, Spring Boot, Quarkus, testing, SQL, and persistence guidance but no scheduler-specific skill for Quartz. Quartz work needs explicit ownership of job identity, trigger identity, cron and timezone semantics, misfire policy, concurrent execution, retries and idempotency, JobDataMap durability, JobStore selection, JDBC schema ownership, clustering, recovery, and operational observability.

The skill must cover Quartz itself without assuming Spring Boot integration. Spring Boot or Quarkus integration rules should remain in their framework skills and compose with Quartz when detected.

Authoritative starting point: [Quartz Scheduler Documentation](https://www.quartz-scheduler.org/documentation/).

Parent series: [Technology Skill Expansion](index.md).

## Requirements

- Create skills/quartz/SKILL.md with matching frontmatter name and a concise Quartz-specific responsibility boundary.
- Cover jobs, triggers, calendars, cron and timezone behavior, explicit misfire policies, disallow-concurrent-execution decisions, idempotency, recovery, JobDataMap compatibility, JobStore choice, JDBC-backed clustering, and scheduler lifecycle evidence.
- Require explicit ownership for retry, duplicate execution, partial failure, and side effects rather than implying exactly-once execution.
- Compose with java, sql, spring-boot, quarkus, testing, and application-security guidance only when the affected scope requires them.
- Add skills/quartz/detection.yaml using Java source plus owning Maven or Gradle evidence for Quartz core or an established framework Quartz integration.
- Reject dependency mentions that are not pertinent to the selected source folder and documentation-only examples.
- Generate skills/quartz/agents/openai.yaml from the source skill metadata.
- Add Quartz to README.md, design/skills-modularization.html, generated skill definitions, technology detection registries, explorer data, and the support checklist.
- Add focused bundle-content and technology-detection regression coverage.

## Acceptance Criteria

- A pertinent Java scope with Quartz ownership receives quartz and java together.
- Spring Boot Quartz ownership composes quartz with the existing Spring Boot skillset rather than creating duplicate framework rules.
- Documentation or an unrelated sibling module containing Quartz text does not activate the skill.
- The skill requires explicit trigger misfire, concurrency, retry, and recovery behavior.
- The skill distinguishes volatile and durable job stores and treats clustering as a database-backed operational contract.
- Codex metadata, generated catalog artifacts, and repository tests are current.

## Dependencies

None.

## Verification

- Run positive detection fixtures for Quartz core and framework integration.
- Run negative fixtures for documentation-only and unrelated sibling evidence.
- Run scripts/validate-agent-skills.py for skills and scripts/openai_metadata.py in check mode.
- Run every generated-output freshness check required by AGENTS.md.
- Run the repository script test suite, the project-wiki script test suite, and git diff validation.

## Notes

- Keep version-sensitive statements grounded in current official Quartz documentation at implementation time.
- Do not promise exactly-once execution; acceptance should be expressed through idempotency and observed recovery behavior.
