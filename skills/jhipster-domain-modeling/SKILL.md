---
name: jhipster-domain-modeling
description: Use when creating, changing, reviewing, or regenerating JHipster JDL, entities, fields, validations, relationships, DTOs, service layers, filtering, or pagination in a Java and Spring Boot application.
metadata:
  category: stack-and-domain
---

# JHipster Domain Modeling

Combine with JHipster Project. Load JHipster Persistence when an SQL model change requires a database migration.

## Model Ownership

- Use the established JDL files as the primary model source when the project maintains them. Otherwise keep the .jhipster entity definitions aligned with generated code.
- Model requiredness, validation, ownership, display fields, and delete behavior deliberately. Do not infer cascade semantics from the generated user interface.
- Keep relationship direction no broader than the use case requires. Review both sides of bidirectional and many-to-many relationships for serialization, equality, and query costs.
- Add a service layer when business orchestration or transaction ownership does not belong in a REST resource.
- Use DTOs when the API contract must differ from persistence entities, aggregate data, or limit exposed relationships. Keep MapStruct mappings explicit for non-trivial transformations.
- Choose filtering and pagination from expected query behavior and client needs rather than enabling every generator option.

## Generation Workflow

1. Change the model source and review the generated plan before overwriting files.
2. Regenerate only the affected entities unless a complete regeneration is intentional.
3. Inspect server, client, migration, and test changes together because one model change spans all of them.
4. Update generated test values when new validation rules make generic fixtures invalid.

## Verification

- Compile the backend and run affected entity integration tests.
- Verify relationship create, update, read, delete, and authorization behavior at the API boundary.
- Verify validation on both server and client when the same rule is generated into both stacks.
- Confirm that the resulting migration preserves existing data and matches the domain model.
