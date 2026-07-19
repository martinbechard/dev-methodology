# Technology Skill Expansion

## Goal

Add focused technology skills for MySQL, Quartz Scheduler, Hibernate ORM with Panache, and MapStruct while keeping existing SQL, Java, framework, persistence, and testing guidance composable and non-duplicative.

## Purpose

Project setup should detect these technologies from owning repository evidence and route concise, technology-specific guidance to affected folders. Each skill should own only behavior that differs materially from its companion skills. Catalog documentation, generated registries, Codex metadata, support data, and regression tests must remain synchronized with every addition.

## Design Anchors

- Distributed skill sources live under skills and use matching directory and frontmatter names.
- Specialized technology skills require detection.yaml metadata and source-backed folder activation.
- Detection uses repository evidence rather than task wording, prompt keywords, or installed-skill availability alone.
- SQL remains the vendor-neutral query and schema foundation.
- Java and framework skills remain the language and application foundations.
- Generated documentation and adapters are refreshed from their source files rather than edited manually.
- README.md and design/skills-modularization.html remain aligned with the public technology-skill catalog.

## Non-Goals

- Loading every database, scheduler, mapper, or persistence skill into every agent.
- Repeating general SQL, Java, Spring Boot, Quarkus, test-strategy, or migration guidance in each new skill.
- Adding Hibernate Reactive with Panache guidance to the blocking Hibernate ORM with Panache skill.
- Treating dependency presence at an unrelated owning boundary as proof that every nested folder uses the technology.

## Recommended Order

1. [Split Hibernate ORM with Panache from Quarkus Persistence](split-hibernate-orm-panache-technology-skill.md).
2. [Add the MySQL technology skill](add-mysql-technology-skill.md).
3. [Add the Quartz Scheduler technology skill](add-quartz-scheduler-technology-skill.md).
4. [Add the MapStruct technology skill](add-mapstruct-technology-skill.md).

The Panache split comes first because it corrects an existing oversized skill boundary. The remaining items are independent and may be dispatched in any order after confirming non-overlapping repository claims.

## Definition Of Good

- Every skill has a narrow, explicit ownership boundary and named companion skills.
- Setup-time detection selects each skill only from pertinent owning evidence.
- Negative detection tests prevent documentation, examples, or unrelated sibling modules from activating a skill.
- Source skills, metadata, README inventory, design documentation, generated registries, support data, and regression tests agree.
- Repository validation passes and each completed item is committed as coherent maintenance work.
