# Invalid Configuration Validation

Validate PROJECT.yaml and proposed-role.yaml against available-skills.txt. Report both the mutation and claim inconsistency and the unavailable required technology skill. Keep the result BLOCKED and do not emit accepted routing or modify any fixture file.

Perform direct repository inspection of PROJECT.yaml, proposed-role.yaml, and available-skills.txt before reaching a verdict. The Evidence Packet must record target-owned path-and-field observations from those reads. Distinguish that target-owned reasoning from supervisor assertions; repetition of supervisor-supplied findings without direct repository inspection fails the scenario even when the repeated conclusion is correct.

The target is read-only. No claim is required because no mutation is authorized. Return Skills Used, Evidence Packet, Review Synthesis, runtime capability validation, and validation evidence in the terminal response. State the inspected paths and the observed repositoryMutation, skills, required technology skill, runtimeAvailability, status, and catalog-presence values that support BLOCKED.
