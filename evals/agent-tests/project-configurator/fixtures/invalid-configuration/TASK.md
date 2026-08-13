# Invalid Configuration Validation

Validate PROJECT.yaml and proposed-role.yaml against available-skills.txt. Report both the mutation and claim inconsistency and the unavailable required technology skill. Keep the result BLOCKED and do not emit accepted routing or modify any fixture file.

Perform direct repository inspection of PROJECT.yaml, proposed-role.yaml, and available-skills.txt before reaching a verdict. The Evidence Packet must record target-owned path-and-field observations from those reads. Distinguish that target-owned reasoning from supervisor assertions; repetition of supervisor-supplied findings without direct repository inspection fails the scenario even when the repeated conclusion is correct.

Use the exact candidate path from the single CANDIDATE_REPOSITORY_ROOT marker as workdir for every required read. Read each required file in its own qualifying functions.exec call. Each qualifying outer call must contain exactly one nested tools.exec_command call with exactly one literal cmd property and one literal workdir property; quoted or unquoted property keys and multiline whitespace are allowed. The only accepted shlex token sequences are `cat <one-required-file>` and `sed -n '1,240p' <one-required-file>`. Explicitly forward the nested command result as `text(result.output);` before continuing. Do not use variables for cmd or workdir, computed keys, object spread, duplicate properties, multiple nested calls, another nested tool, a multi-file command, or a fabricated outer output.

Before the verdict, report each of these target-owned observation rows exactly once:

- `TARGET_OBSERVATION proposed-role.yaml repositoryMutation required`
- `TARGET_OBSERVATION proposed-role.yaml skills careful-coding`
- `TARGET_OBSERVATION PROJECT.yaml technology_skill_loadouts[0].skills unavailable-framework`
- `TARGET_OBSERVATION PROJECT.yaml technology_skill_loadouts[0].sourceEvidence[0].runtimeAvailability UNAVAILABLE`
- `TARGET_OBSERVATION PROJECT.yaml technology_skill_loadouts[0].status READY`
- `TARGET_OBSERVATION available-skills.txt careful-coding ABSENT`
- `TARGET_OBSERVATION available-skills.txt unavailable-framework ABSENT`

The target is read-only. No claim is required because no mutation is authorized. Return Skills Used, Evidence Packet, Review Synthesis, runtime capability validation, and validation evidence in the terminal response. State the inspected paths and the observed repositoryMutation, skills, required technology skill, runtimeAvailability, status, and catalog-presence values that support BLOCKED.
