# Add The MapStruct Technology Skill

Status: Proposed

Type: Feature

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

## Notes

- Keep version-sensitive statements grounded in current official MapStruct documentation at implementation time.
- Treat generated mapper implementations as verification evidence, not hand-maintained source artifacts.
