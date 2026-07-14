# Technology Skill Detection

## Purpose

Technology detection is a project-setup operation. It converts repository evidence for known folders or tiers into durable technology-skill bindings in PROJECT.yaml and AGENTS.md.

Normal coding, review, verification, diagnosis, security, interface, prompt, and documentation agents do not rerun detection. The harness supplies their fixed-role skills and the technology skills routed for the active folder.

## Inputs

- Project root.
- One or more folders or tiers identified during project analysis.
- Generated technology detection registry.
- Installed bundled skills used to validate availability.

Prompt wording and agent role are not detection inputs.

## Detection Metadata

Only specialized technology and domain skills have detection metadata.

Each definition contains:

- Skill identifier.
- Kind and label.
- Capabilities for documentation and exploration.
- An any-of activation root containing atomic evidence or all-of clauses.
- File extension, file glob, same-file path and extension, owning manifest, dependency, content, or parsed source-import predicates.
- Companion specialized skills.
- Optional exclusive group and priority.
- Required-when-detected policy.

The skill identifier is explicit even though the source file also sits beside that skill. The duplication lets examples, generated registries, validation errors, and evidence rows identify the selection outcome without relying on a filesystem path.

An any-of branch succeeds when its atomic predicate succeeds or every predicate in its all-of clause succeeds. The detector selects the named skill when at least one complete branch succeeds. It records the concrete files, manifests, dependencies, or imports from satisfied branches as evidence.

FileMatch binds its glob and extensions to one file. This prevents an unrelated source file from supplying the extension for a documentation file whose name happens to match a domain pattern. SourceImport parses Python syntax and does not treat comments or string literals as imports. Globstar path segments match zero or more directories, including root-level app and pages folders.

Example:

```yaml
schema: dev-methodology-technology-detection
version: 2
skill: fastapi
kind: technology
label: FastAPI
capabilities:
  - web-application-framework
activation:
  anyOf:
    - allOf:
        - fileExtension: .py
        - owningDependency: fastapi
    - sourceImport:
        module: fastapi
        extensions:
          - .py
companions:
  - python
```

Generic fixed-role skills and optional environment tools are not detection definitions.

## Output

The detector returns one proposed loadout per analyzed scope:

- Scope and path pattern.
- Detected specialized skills.
- Evidence for each skill.
- Missing required skills.
- Exclusive conflicts.
- Explicit no-variant result when nothing bundled matches.

Project Agent Setup records accepted loadouts in PROJECT.yaml with their source evidence. It then generates AGENTS.md routing so the harness supplies those technology skills to every agent working under the matching path.

## Fixed-Role Skills

Role definitions remain technology-neutral and declare their fixed generic skills.

- Adapters with a native skills property generate that property.
- Adapters without a native skills property generate unconditional skill-loading instructions.
- Fixed-role loading does not depend on detector output.

## Script Ownership

The detector source lives at scripts/detect-technology-skills.py with the other repository build and validation scripts.

The detector skill contains a generated runtime mirror only so a standalone installed skill can execute the same implementation. The build verifies that the mirror matches the repository source script. Detector logic is never maintained independently inside the skill.

## Workflow

1. Project Agent Setup inventories project tiers, ownership boundaries, manifests, source roots, and tests.
2. It chooses representative folder scopes.
3. It runs detection once for those scopes.
4. It reviews conflicts, missing skills, and unsupported technologies.
5. It writes source-backed loadouts into PROJECT.yaml.
6. It generates root or nested AGENTS.md technology-loading instructions.
7. It verifies that every named skill is installed.
8. It reruns detection only when project setup or technology boundaries change.

## Non-Goals

- Per-task skill selection.
- Agent-role filtering.
- Skill-read receipts for ordinary work.
- Prompt-keyword routing.
- Detecting optional command-line tools from the current machine.
- Replacing generic fixed-role skills.
- Claiming support for technologies without a bundled skill.

## Acceptance Cases

- A TypeScript folder produces TypeScript skills and no Java skills.
- A Spring Boot folder produces Java and Spring Boot skills.
- A FastAPI folder produces Python and FastAPI skills.
- A parsed FastAPI import activates FastAPI, while the same text in a comment or string does not.
- Every detection definition explicitly names the skill selected by its activation clauses.
- A Node-owned JavaScript or TypeScript CLI path produces Node CLI skills.
- A Python cli.py path produces Python skills without Node CLI.
- A Next.js API route requires a JavaScript or TypeScript route file and the owning Next.js dependency.
- Domain-oriented path names in documentation and configuration files do not activate product implementation skills.
- Root-level paths satisfy leading globstar patterns.
- A mixed repository produces separate loadouts for separate analyzed scopes.
- A child package does not inherit unrelated root workspace dependencies.
- Equal-priority exclusive matches block setup.
- A detected but unavailable required skill blocks setup.
- Generated AGENTS.md gives the harness the detected technology skills for every matching folder without rerunning detection.
