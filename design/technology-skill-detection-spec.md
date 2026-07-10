# Technology Skill Detection

## Purpose

Technology detection is a project-setup operation. It converts repository evidence for known folders or tiers into durable technology-skill bindings in AGENTS-PLAN.yaml and AGENTS.md.

Normal coding, review, verification, diagnosis, security, interface, prompt, and documentation agents do not rerun detection. They load their canonical fixed-role skills and the technology skills declared by the nearest AGENTS.md.

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
- File, path, manifest, dependency, or content evidence.
- Companion specialized skills.
- Optional exclusive group and priority.
- Required-when-detected policy.

Generic fixed-role skills and optional environment tools are not detection definitions.

## Output

The detector returns one proposed loadout per analyzed scope:

- Scope and path pattern.
- Detected specialized skills.
- Evidence for each skill.
- Missing required skills.
- Exclusive conflicts.
- Explicit no-variant result when nothing bundled matches.

Project Agent Setup records accepted loadouts in AGENTS-PLAN.yaml with their source evidence. It then generates AGENTS.md instructions that require every agent working under the matching path to load those technology skills before acting.

## Fixed-Role Skills

Canonical role definitions remain technology-neutral and declare their fixed generic skills.

- Adapters with a native skills property generate that property.
- Adapters without a native skills property generate unconditional skill-loading instructions.
- Fixed-role loading does not depend on detector output.

## Script Ownership

The canonical detector implementation lives at scripts/detect-technology-skills.py with the other repository build and validation scripts.

The detector skill contains a generated runtime mirror only so a standalone installed skill can execute the same implementation. The build verifies that the mirror matches the canonical script. Detector logic is never maintained independently inside the skill.

## Workflow

1. Project Agent Setup inventories project tiers, ownership boundaries, manifests, source roots, and tests.
2. It chooses representative folder scopes.
3. It runs detection once for those scopes.
4. It reviews conflicts, missing skills, and unsupported technologies.
5. It writes source-backed loadouts into AGENTS-PLAN.yaml.
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
- A mixed repository produces separate loadouts for separate analyzed scopes.
- A child package does not inherit unrelated root workspace dependencies.
- Equal-priority exclusive matches block setup.
- A detected but unavailable required skill blocks setup.
- Generated AGENTS.md tells every agent in a matching folder to load the detected technology skills without rerunning detection.
