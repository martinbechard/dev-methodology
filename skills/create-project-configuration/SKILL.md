---
name: create-project-configuration
description: Use when creating or substantially rewriting the root PROJECT.yaml, including setup mode, Persistence, Commit, claim-helper selection, agent definitions, skill selection, generated guidance, and validation.
metadata:
  category: documentation-methodology
---

# Create Project Configuration

Use this skill to create or substantially rewrite a PROJECT.yaml artifact. The artifact records project-owned setup choices and connects conceptual agents and their technology-agnostic core skills, shared conditional Agent skills, project-level skill extensions, independent resource-coordination, Persistence and Commit selection, persisted documentation mode, and folder technology skills through generated root and nested AGENTS.md guidance with validation evidence.

## Setup Contract

Ask Setup mode first, with Basic as the default and Advanced as the alternative. Basic asks whether to create the Wiki, defaulting to Yes, and asks the user to confirm detected technology candidates. Persist Yes as project_setup.documentation wiki and No as project_setup.documentation none so the negative answer creates no documentation root. It displays the hidden resolved choices as Set: Concurrent tasking No, Persistence none, Commit main-branch, the installed core skill delivery mode, and technology skill delivery by-reference. It never displays Concurrent capacity.

Advanced defaults Concurrent tasking to No and asks Concurrent capacity, default 3, only after Yes. It defaults Persistence to file, Commit to main-branch, Documentation to both, and technology skill delivery to by-reference. Documentation choices are exactly wiki, specifications, and both. Show every detected technology candidate with evidence and conflicts. Persist every candidate disposition, the ordered accepted skill list, each rejection and reason, and a durable explicit user-confirmation reference. Require a non-empty auditable reference, but keep its format project-defined because this contract supplies no universal identifier scheme. Reject missing, empty, whitespace-only, or boolean-only confirmation evidence.

Read core skill delivery from the installed native-agent ownership metadata and generation manifest. A default methodology installation records by-reference. Persist the confirmed effective mode in PROJECT.yaml and display it as Set; do not ask it again. Missing, inconsistent, invalid, byte-mismatched, or runtime-incompatible evidence is BLOCKED with an instruction to regenerate and install compatible native agents. A project may change core delivery only through explicit project-scoped regeneration and installation before PROJECT.yaml records the new value.

## Template

Use skills/route-documentation-work/assets/templates/project-template.yaml as the starting asset. When the asset is already staged or directly available through the loaded skill package, read it there. When it is not staged and mcp-agent-ops is available, load it with skill_resource_load. Use the direct skill-relative file as the fallback only when the tool is absent or its server cannot initialize or connect before dispatch; do not bypass a structured policy rejection.

Copy the template only when a local editable artifact is needed. Replace every TODO instruction with source-backed content from the target repository.

## Scope

Create exactly one PROJECT.yaml at the project root when the project needs a reviewable configuration for agents and skills. The root file owns the configuration for the entire project, including every subfolder scope.

Do not create nested PROJECT.yaml files. When a subfolder has distinct technology, runtime ownership, data boundaries, verification commands, or agent skillsets, record that scope in the root PROJECT.yaml and create nested AGENTS.md guidance when normal work in that subtree needs a narrower operational contract.

Create or update PROJECT.yaml before writing AGENTS.md guidance. PROJECT.yaml is the setup and validation artifact that explains what AGENTS.md should contain, why the conceptual agent definitions and skills were chosen, and where project-specific evidence belongs. AGENTS.md is the operational reference that the harness supplies after the configuration has been validated. When the target uses Claude Code, create a thin CLAUDE.md beside each applicable AGENTS.md that imports the colocated guidance instead of duplicating it.

Treat PROJECT.yaml as an intermediate, reviewable intent log between repository inspection and generated operational guidance. A maintainer may edit it to correct a selected conceptual agent definition, folder skillset, route, or guidance placement. On the next setup run, Project Configurator must treat those edits as requested configuration intent, reconcile them with current repository evidence and bundle constraints, preserve valid corrections, and report a blocking conflict or open question instead of silently replacing an unsupported edit.

Set resource_coordination to none or resource-claim. This required project-wide setting has no folder overrides. Report a missing or unsupported value instead of choosing one.

When resource-claim is selected, add resource_coordination.deadline_policy with resource_classes and resource_overrides.

Each resource class has:

- a positive maximum_duration_seconds;
- a non-negative cleanup_grace_seconds.

Use these initial defaults for a new configuration:

| Resource class | Maximum | Cleanup grace |
|---|---:|---:|
| backlog-mutation | 600 | 120 |
| main-integration | 2700 | 600 |
| browser-server | 3600 | 600 |
| database-port | 1800 | 300 |
| live-model-evaluation | 14400 | 1800 |

Preserve valid project-specific values. A resource_overrides entry names one resource ID, its resource class, maximum duration, and cleanup grace. Omit deadline_policy when resource_coordination is none.

The PROJECT.yaml field agent_claim_transport selects the claim helper. The field keeps its historical name for compatibility. Set it to command or mcp only after verifying that helper in the target runtime.

- command requires resource-claim-helper-command, Python, and every resource-claim-helper operation and result.
- mcp requires resource-claim-helper-mcp and every resource-claim-helper operation and result field. The current external provider has not passed this verification.

Record whether the selected helper is AVAILABLE or UNAVAILABLE and include the verification evidence. If neither helper works, report BLOCKED. Omit agent_claim_transport when resource_coordination is none.

Keep workflow configuration selector-only. Always record one Persistence value from file, github, gitlab, azure-devops, jira, none, or UNSET and one independent Commit value from main-branch, feature-branch, or UNSET, plus selector-specific folder overrides. A missing workflow_selection.persistence or workflow_selection.commit mapping is invalid; record explicit UNSET rather than omitting a deferred decision. Within either selector, one exact folder pattern may appear only once. Reject both redundant equal-value duplicates and conflicting duplicates with the indexed patterns and values. Do not copy provider lifecycle, branch, pull-request, merge-request, review-loop, or completion procedures into PROJECT.yaml or AGENTS.md. Generated workflow guidance references selected skills by name and keeps the selected create, manage, and completion skills as references only. Folder technology skills use by-reference delivery by default and remain separate from conceptual agent skill lists.

Record project_skill_extensions as one ordered list. Use a bundled skill identifier string when the skill exists in the bundle. For an explicitly registered non-bundled skill, use one mapping containing exactly skill, registration, availability, and catalog; registration must be registered, availability must be AVAILABLE, and catalog must identify the target runtime catalog that exposes the skill. Use an empty list when no project-level extension is selected.

Record shared_agent_skills as one ordered list of mappings containing exactly skill and condition. Use it for a bundled skill whose condition applies uniformly to every conceptual Agent in the project. Keep the skill out of individual role_agent_set skill lists, and do not use this field for a skill owned by only one Agent or one folder. For project file placement, select organise-project-files with the condition "when an Agent must choose or audit the location of a project file or directory". Use an empty list when the project has no shared conditional Agent skill.

Load resource-claim only through resource_coordination. Verify exactly one resource-claim-helper-command or resource-claim-helper-mcp Provider Skill against resource-claim-helper, then render only that selected provider. Do not add the policy, interface, or providers to project_skill_extensions or technology_skill_loadouts.

Normalize each shared Agent skill and extension identifier by trimming whitespace and converting it to lowercase before validating its lowercase hyphenated form. Use that normalized identifier for duplicate, bundled-availability, registered-availability, unknown-skill, and definition-owned conflict checks. Report every failure with the exact shared_agent_skills or project_skill_extensions index and field plus the correction. Preserve valid declared order. Reject a shared Agent skill that duplicates any fixed or conditional skill in role_agent_set. Reject an extension that duplicates any fixed or conditional skill in role_agent_set or any entry in shared_agent_skills.

Render valid shared Agent skills as one concise root-only Shared Agent Skills section that tells every Agent to load each referenced skill only when its condition applies. Render valid project-level extensions as a separate reference-only Project Skill Extensions section at the end of root AGENTS.md. Do not inline either set of skill bodies. Do not copy the section to nested AGENTS.md files; this applies to both Shared Agent Skills and Project Skill Extensions. Do not merge these project-wide references into workflow selectors or folder technology loadouts.

Preserve Azure DevOps and Jira values as explicit unsupported selections so the matching create and manage placeholder skills can report BLOCKED without mutation. Preserve none as the explicit absence of a durable provider and reject durable provider operations under it. Preserve UNSET until the pertinent agent asks for the provider decision before persistence or the completion decision before implementation or publication. Do not infer either selector from backlog files, remotes, hosting metadata, templates, installed plugins, or available tools.

Migrate legacy workflow_selection.provider to workflow_selection.persistence and workflow_selection.completion to workflow_selection.commit without changing selected values. Also move workflow_selection.workitem to workflow_selection.commit, mapping simple-workitem to main-branch, feature-branch-workitem to feature-branch, and UNSET to UNSET, and workflow_selection.backlog to workflow_selection.persistence, mapping file-based-backlog to file, github-issues-backlog to github, none to none, and UNSET to UNSET. Report mixed legacy and canonical fields with their exact paths; never silently overwrite established intent.

Accept direct-main only as the exact legacy value of workflow_selection.commit, workflow_selection.completion, or project_setup.commit. Normalize that value to main-branch before validation and rendering, including exact Commit folder overrides. Emit main-branch in all new configuration and generated guidance. Do not reinterpret direct-main in another field, repair a malformed selector structure, or accept any other unsupported value.

Persist project_setup.documentation as none or wiki for Basic setup and as wiki, specifications, or both for Advanced setup. Setup creates only the selected empty roots and repository-required placeholders; none creates no documentation root. It never performs reverse engineering, source-derived documentation, or independent review. Add documentation_mode.selected only when a later explicit documentation workflow needs it.

For a legacy PROJECT.yaml without documentation_mode, infer hybrid-specifications-and-wiki only when repository evidence shows both structured specification roots and docs/wiki, or when bootstrap-project-documentation is establishing that full hierarchy. Otherwise ask for the project-owned selection and persist it before downstream documentation work. Downstream agents consume the persisted selection instead of reconstructing it from conversational context. Treat an unsupported documentation mode as BLOCKED. Treat a missing value as a migration requirement rather than silently applying an unrecorded default.

repositoryMutation belongs to conceptual agent definitions and does not select claim behavior. Generated AGENTS.md references resource-claim and includes only the selected claim helper's instructions. It must not copy claim rules into project guidance.

When resource-claim is selected, add /.worktrees/ to the root .gitignore. Describe .worktrees in root AGENTS.md as ignored worktree state under the primary worktree. Do not store a machine-specific absolute worktree path in PROJECT.yaml or AGENTS.md.

## Configure Project Agents And Skills

1. Inspect the target repository before writing. Inspect existing AGENTS.md artifacts, then read README files, package metadata, build configuration, source roots, tests, docs, wiki pages, task-relevant procedures, backlog files, and current worktree status.
2. Classify the project family, application tiers, technology stacks, documentation surfaces, runtime boundaries, data boundaries, and verification commands.
3. For ordinary setup, persist only project_setup.documentation and do not require documentation_mode. When a later explicit documentation workflow begins, select and validate documentation_mode.selected, persist hybrid-specifications-and-wiki for a full hybrid bootstrap, migrate a legacy missing field only from the evidence defined above, and stop on an unsupported value.
4. Identify the conceptual agent definitions needed for the project. Prefer shared reusable definitions such as Development Orchestrator, Project Configurator, Coding Agent, Code Review Agent, QA And Verification Agent, Documentation Writer, Wiki Query Agent, and specialist reviewers only when the project evidence requires them. Copy each selected definition's complete fixed and conditional skill metadata from its canonical definition; do not abridge the skillset or flatten conditional skills into fixed ones. Select resource_coordination independently as none or resource-claim. When resource-claim is selected, record and validate the five resource deadline classes and any resource-ID overrides. Verify one command or MCP claim helper in the target runtime, then record that helper and its verification under agent_claim_transport. Omit the deadline and helper settings when resource_coordination is none.
5. Map each tier, technology, folder, or workflow to the reusable skills it needs. Record project-wide conditional behavior once in shared_agent_skills rather than repeating the same condition in individual Agent definitions. Separately record the ordered project_skill_extensions list, validating bundled identifiers and explicit registered-skill mappings against the target runtime catalog and every selected definition-owned and shared Agent skill.
6. Ask for Persistence and Commit independently in Advanced mode; apply and display the fixed Basic values without controls. Allow source-backed, user-intended folder overrides to change only their matching selector. Do not infer either selector from repository files, remotes, hosting metadata, templates, installed plugins, or available tools. Record UNSET when a decision is intentionally deferred so the pertinent task agent asks at the Persistence or Commit operation boundary.
7. As Project Configurator, inspect the technology skills actually exposed by the target runtime. Prefer skill_list plus detect_technology_skills when mcp-agent-ops is available; the server binds detection to its complete active catalog. Use the loaded detector only when the MCP tools are absent or the server cannot initialize or connect before request dispatch. Never use it to bypass a path, root, authorization, input-policy, or other structured rejection. Pass the complete catalog to the fallback detector with repeated available-skill inputs. Review source paths, owning manifests, configuration, and build evidence. Preserve the catalog source, catalog revision or portable fallback identity, and detector runtime-availability result in PROJECT.yaml.
8. Review each detector candidate for pertinence to the analyzed folder. Reject owning-manifest overreach when the folder's source, configuration, runner, or runtime responsibility belongs to another technology, and record the rejection evidence.
9. Record deterministic technology_skill_loadouts and folder bindings, including source evidence, runtime availability, rejected candidates, missing required skills, exclusive conflicts, and explicit no-variant results. Store repository evidence as project-relative paths and external tool evidence as portable identifiers, versions, digests, or declared variables. Never embed an absolute checkout, user-home, worktree, cache, or temporary-directory path in PROJECT.yaml. For a scope with no pertinent specialized skill, record `NO_VARIANT` plus a general-model-training fallback; do not invent a skill or omit the scope. Keep a detected required-but-unavailable skill `BLOCKED`.
10. Decide which subfolders need nested AGENTS.md guidance and record every decision in the root PROJECT.yaml. Use only real repository-relative paths or valid globs in loadouts and folder routes, never prose labels. Prefer non-overlapping routes. When overlap is unavoidable, record a deterministic most-specific-pattern-wins rule and verify that generated AGENTS.md guidance preserves it.
11. Verify that every selected conceptual agent definition declares repositoryMutation and does not directly list the project-selected resource-coordination implementation. Verify the selected coordination skill is available to the target runtime. When resource-claim is selected, verify every deadline class and resource-ID override. Verify that the selected command or MCP helper supports every required operation and deadline field. Treat a missing definition, skill, helper operation, or helper field as BLOCKED. Do not copy claim rules into project instructions or try another helper.
12. When resource-claim is selected, ensure the root .gitignore contains the exact anchored /.worktrees/ entry before rendering project guidance.
13. Copy the template once to the project root and replace every TODO with source-backed project content.
14. When an existing PROJECT.yaml contains maintainer edits, treat them as requested configuration intent. Preserve valid Persistence, Commit, and selector-specific folder-override corrections exactly. Report an invalid identifier, duplicate override, or incompatible operation with the exact evidence and constraint instead of silently replacing the edit or inferring another selector.
15. Keep proprietary project validation notes inside the target project repository. Do not copy private project names, internal implementation details, customer data, secrets, or non-public workflows into distributable examples.
16. Use fictitious names, synthetic paths, and generic behavior for customer-safe examples.
## Render Project Guidance

1. After validating the configuration, run scripts/render-agents-technology-skills.py with PROJECT.yaml. Create or update the root and nested AGENTS.md files. Reference the selected resource-coordination skill only when enabled. For resource-claim, include only the selected claim helper. For none, include no claim skill, helper, procedure, or evidence. Do not render a worktree requirement. Keep technology skills by reference unless Advanced setup explicitly selected inline delivery. Add Shared Agent Skills and Project Skill Extensions only to the root AGENTS.md. When resource-claim is selected, mention .worktrees as operational state without copying claim procedures.
2. When Claude Code is used, create thin CLAUDE.md bridge files that import the colocated AGENTS.md without copying its rules.
3. Say Not yet identified for related sources, tests, commands, or conceptual agent definitions that do not exist yet.
4. Keep the artifact steady-state. Do not describe it as new, revised, or enhanced unless the document is explicitly a change plan.

## Verify Project Configuration

Before finishing:

1. When mcp-agent-ops is available, run verify_yaml on the created or materially rewritten root PROJECT.yaml before verify-documentation-page. A structured YAML finding is a failed gate, not an MCP connection failure. Use the applicable local YAML check only when the tool is absent or the server cannot initialize or connect before request dispatch. Never use the local check to bypass a path, root, authorization, input-policy, or other structured rejection.
2. Use verify-documentation-page on the created or materially rewritten root PROJECT.yaml file.
3. Search PROJECT.yaml for unresolved TODO markers that are not intentional.
4. Confirm project_setup.documentation matches the chosen Basic or Advanced setup branch. Only when a later explicit documentation workflow is configured, confirm documentation_mode.selected is present, equals a supported value, and records the selection or legacy migration evidence. Reject unsupported values and legacy missing fields before that downstream documentation work.
5. Confirm every conceptual agent definition, complete fixed and conditional definition-owned skillset, shared Agent skill, project-level skill extension, workflow selector, folder route, validation command, and file contract has source evidence or an open question. Validate shared_agent_skills and project_skill_extensions in declared order. Reject duplicate, unknown, unavailable, definition-owned, and cross-list identifiers with exact indexed correction guidance, and confirm each registered extension names its catalog. Validate Persistence and Commit defaults and folder overrides independently against their canonical vocabularies and compatibility matrix. Confirm Azure DevOps and Jira remain placeholder selections, none remains an explicit no-persistence boundary, and UNSET remains an ask boundary. Search for POSIX and Windows user-home paths and replace any workstation-specific evidence location with a project-relative path or portable declared variable.
6. Run setup-time detection for representative folders in every declared tier. Confirm each result matches the planned skillset, every selected skill is exposed by the target runtime, every required skill is available, and every no-variant scope explicitly falls back to general model training.
7. Confirm AGENTS.md names the effective Persistence create and manage skills and Commit skill as reference-only workflow guidance, including selector-specific folder overrides. Confirm it does not reproduce workflow skill bodies or procedure headings. Confirm the root Shared Agent Skills section preserves every shared_agent_skills condition and the final Project Skill Extensions section preserves extension order without inlining either skill body. Confirm no nested AGENTS.md repeats either section. Separately confirm each detected folder technology skill is referenced by default, is inlined only when Advanced setup explicitly selected inline delivery, or records an explicit general-model-training fallback. Confirm ordinary agents are not told to rerun detection and the output matches PROJECT.yaml. Confirm every route is a real path or valid glob, conflicting broad fallbacks were split into non-overlapping scopes where possible, and any remaining overlap uses the same documented precedence in PROJECT.yaml and generated guidance.
8. Confirm resource_coordination is none or resource-claim and has no folder overrides. Confirm every selected conceptual agent definition declares repositoryMutation and does not list resource-claim. For resource-claim, confirm agent_claim_transport selects one verified AVAILABLE helper and AGENTS.md references resource-claim and includes only the selected helper provider. For none, confirm AGENTS.md contains no claim skill, helper, procedure, or evidence. Confirm AGENTS.md does not copy claim rules or instruct agents to try a different helper.
9. When resource-claim is selected, confirm the root .gitignore contains the exact /.worktrees/ line and Git reports a .worktrees probe as ignored.
10. When resource-claim is selected, confirm the root AGENTS.md identifies .worktrees as ignored primary-root operational state, prohibits deriving it from a linked checkout, and contains no machine-specific absolute worktree path.
11. Confirm the project contains exactly one PROJECT.yaml at its root and that it records every nested AGENTS.md placement decision.
12. Confirm every planned AGENTS.md exists and matches the validated routing plan.
13. When Claude Code is used, confirm every applicable AGENTS.md has a thin colocated CLAUDE.md import and that no guidance is duplicated between them.
14. Confirm maintainer edits to PROJECT.yaml were preserved when valid or reported with the exact rejected selector, supported values, migration guidance, evidence, and constraint that blocks them.
15. Confirm customer-shareable examples are fictitious and proprietary examples remain only inside their target repositories.
16. Run project wiki status and lint when docs/wiki exists and the plan references wiki pages.
17. Run the target project build when code, imports, generated artifacts, or project metadata changed.

Do not send private, proprietary, sensitive, PII, or company-internal material to an external service unless the user explicitly authorizes it.
