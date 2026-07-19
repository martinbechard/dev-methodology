---
name: mapstruct
description: Implement, review, test, or diagnose MapStruct compile-time mapper contracts, processor configuration, create and update semantics, null handling, conversions, collections, cycles, qualifiers, inheritance, component models, and generated implementations.
metadata:
  category: stack-and-domain
---

# MapStruct

Combine with Java. Use Java Design when the work chooses public source or target types, mapping-layer boundaries, or object ownership. Add API, Application Security, persistence, framework, and test skills only when those concerns are present.

## Mapping Contract

- Identify every mapper, mapping direction, source type, target type, create method, update method, factory, shared configuration, and external conversion involved in the change.
- Treat mapped fields as a data-transfer contract. Review identifiers, credentials, authorization state, personal data, audit fields, relationships, and server-owned values explicitly rather than relying on matching names.
- Choose an explicit unmapped-target policy. Prefer ReportingPolicy.ERROR for production contracts, then ignore or populate individual target properties deliberately instead of accepting silent drift.
- Make conversion selection observable. Resolve competing mapping methods with explicit qualifiers, result types, factories, or dedicated conversion methods, and test lossy numeric, date, locale, enum, and string conversions.
- Keep nested mappings intentional. Confirm whether nested objects are copied, flattened, reused, ignored, or created, and prevent cyclic object graphs with explicit cut points, identity mappings, or context-backed cycle tracking.

## Create And Update Semantics

- Distinguish methods that create a new target from methods that mutate an existing @MappingTarget. Do not infer update behavior from a similarly shaped create mapping.
- Specify null source-argument behavior with NullValueMappingStrategy separately from null or absent source-property behavior. NullValuePropertyMappingStrategy applies to @MappingTarget updates; verify its effect on retained, cleared, and defaulted target state.
- Review collection and map behavior against CollectionMappingStrategy and the target accessors. Confirm replacement, clearing, adder use, element conversion, ordering, mutability, and persistence relationship side effects.
- Treat inverse and inherited configuration as reused policy, not proof of symmetry. Audit InheritConfiguration, InheritInverseConfiguration, and MapperConfig prototype mappings for fields whose create, update, or reverse semantics differ.
- Keep subclass, builder, constructor, record, and object-factory selection aligned with the source and target contracts supported by the configured MapStruct version.

## Mapper Integration

- Centralize genuinely shared policy in MapperConfig, including reporting, null handling, component model, injection strategy, and mapping inheritance. Keep method-specific exceptions close to the mapping method.
- Use named or annotation-based qualifiers when type signatures alone cannot express the intended conversion. Keep qualifier retention and placement compatible with MapStruct discovery.
- Configure the component model and injection strategy to match the owning framework. Compose with Spring Boot or Quarkus guidance for dependency injection and lifecycle behavior instead of duplicating framework policy here.
- Keep decorators, callbacks, context parameters, and expressions small and explicit. Move substantial domain logic to an owned service and test it independently.

## Processor Verification

1. Confirm the MapStruct annotations and compatible annotation processor are configured in the nearest owning Maven or Gradle build.
2. Run the project-native clean command-line compile so the annotation processor executes outside the IDE. IDE-only generated sources or successful editor navigation do not count as verification.
3. Inspect the generated mapper implementation for selected conversion methods, null guards, update assignments, collection handling, nested calls, component annotations, and injection shape. Treat generated files as build evidence rather than maintained source.
4. Test create, update, null, absent-property, collection, nested, cycle, qualifier, and failure cases that are material to the mapper contract.
5. Report the mapper paths, shared configuration, compiler command, processor configuration, generated implementation evidence, focused test results, and remaining contract risk.
