# Remove installed-agent integrity checks from project setup

Status: Ready
Type: Defect
Provider: file
Work Item ID: remove-setup-agent-install-integrity-checks
Completion: main-branch

## Summary

Remove responsibility for validating generated native-agent manifests, ownership metadata, runtime compatibility, and installed agent bytes from Project Bootstrapper, Project Configurator, and the create-project-configuration skill. Keep project setup focused on consuming configuration inputs that a deployment or installation boundary has already established.

## Context

The current Project Bootstrapper role, Project Configurator role, and create-project-configuration skill require project setup to compare installed native-agent ownership metadata, the generation manifest, and installed agent bytes. They also require setup to block and instruct the user to regenerate and reinstall agents when that evidence is missing, invalid, inconsistent, byte-mismatched, or runtime-incompatible.

Those integrity and compatibility checks do not belong to repository configuration. They couple ordinary project setup to deployment verification and make setup responsible for diagnosing or remediating an installed methodology bundle. A dev-methodology deployment or installation workflow may own such verification, but this item does not require adding a replacement check unless an existing deployer-owned contract needs alignment to preserve an already intended guarantee.

Current canonical statements are in:

- agents/roles/project-setup/project-bootstrapper.role.yaml
- agents/roles/project-setup/project-configurator.role.yaml
- skills/create-project-configuration/SKILL.md

## Source Evidence

On 2026-08-13, the user reported a defect: “The Project Bootstrapper role, Project Configurator role, and project-configuration skill all effectively say: Before configuring a repository, verify that the installed harness-specific agents match the metadata and manifest from which they were generated. If those installed files are missing, incompatible, or byte-different from the manifest, stop configuration and instruct the user to regenerate and reinstall them. However, it's not their responsibility to verify that. At best it's a dev-methodology deployer concern. We need an item to clear up this confusion and remove this checking.” This user message explicitly authorizes creation of this defect and changes to the named role and skill definitions within the exact manifest below.

## Requirements

- Remove installed native-agent byte, manifest-consistency, ownership-metadata integrity, and runtime-compatibility verification duties from Project Bootstrapper.
- Remove the same verification and regeneration-or-reinstallation blocking duties from Project Configurator.
- Remove the same verification and blocking duties from create-project-configuration.
- Preserve project setup's ability to consume the effective core-skill delivery mode without making setup prove the integrity of the installation that supplied it.
- Keep deployment and installation integrity verification outside project-setup ownership. Align an existing deployer-owned contract only if discovery proves that a current canonical deployment boundary must be updated to avoid losing an intended check.
- Regenerate supported role, skill, documentation-data, native-adapter, and manifest projections from canonical sources; do not hand-edit generated outputs.
- Add or update focused regression coverage so setup no longer blocks on missing, incompatible, inconsistent, or byte-different installed-agent evidence.

## Acceptance Criteria

- Project Bootstrapper contains no instruction to compare installed agent bytes with ownership metadata or an agent-generation manifest before configuration.
- Project Configurator contains no instruction to perform those comparisons or direct regeneration and reinstallation as a project-setup blocking remediation.
- create-project-configuration contains no instruction to perform those comparisons or classify their failure as a project-configuration BLOCKED outcome.
- Project setup can still obtain and persist the effective core-skill delivery mode through a clearly defined input contract without claiming to verify installation integrity.
- Any retained installation-integrity check is demonstrably owned by an existing deployment or installation workflow and is not invoked as a prerequisite owned by Project Bootstrapper, Project Configurator, or create-project-configuration.
- Supported generated artifacts are fresh and contain no stale copies of the removed setup responsibility.
- Focused tests cover the corrected ownership boundary and pass.

## Dependencies

None.

## Verification

- Run targeted contract tests for Project Bootstrapper, Project Configurator, and create-project-configuration statements, including the affected assertions in scripts/test_bundle_content.py and any more specific discovered consumers.
- Run the supported generator and freshness checks for the two role definitions and the skill definition.
- Validate the changed canonical role and skill definitions with the repository's applicable definition validators.
- Search canonical and generated project-setup surfaces for stale byte-comparison, manifest-integrity, runtime-compatibility, and regenerate-or-reinstall blocking language.
- Run git diff --check.
- Obtain independent code review and verification of the ownership boundary and generated-output consistency.

## Open Questions

- Which existing deployment or installation contract, if any, already owns this integrity check and needs wording alignment? Resolve through source discovery; do not create a new project-setup dependency.
- What is the narrowest trustworthy input from which project setup should consume the effective installed core-skill delivery mode after the integrity checks are removed?

## Governed Definition Approval

### Governed Canonical Sources

- agents/roles/project-setup/project-bootstrapper.role.yaml
- agents/roles/project-setup/project-configurator.role.yaml
- skills/create-project-configuration/SKILL.md

### Allowed Dependent Artifacts

- design/generated/role-definitions.js
- design/generated/skill-definitions.js
- generated/adapters/agent-generation-manifest.json
- generated/adapters/claude/agents/project-bootstrapper.md
- generated/adapters/claude/agents/project-configurator.md
- generated/adapters/codex/agents/project-bootstrapper.toml
- generated/adapters/codex/agents/project-configurator.toml
- generated/adapters/gemini/agents/project-bootstrapper.md
- generated/adapters/gemini/agents/project-configurator.md
- generated/adapters/junie/agents/project-bootstrapper.md
- generated/adapters/junie/agents/project-configurator.md
- Focused tests and maintained documentation that directly encode the corrected project-setup ownership boundary, subject to exact path discovery before mutation.

### Approval Resolution

Approved at creation from the user's 2026-08-13 request naming the Project Bootstrapper role, Project Configurator role, and project-configuration skill and asking for an item to remove this checking. This approval covers only the three exact governed canonical sources listed above and their supported generated or directly dependent artifacts. Any additional governed definition requires separate scope-specific approval.

## Notes

- Do not remove deployment-time integrity validation merely because project setup should not own it.
- Do not make Project Bootstrapper or Project Configurator call a deployer as a substitute prerequisite unless a separately authorized design explicitly requires that interaction.
