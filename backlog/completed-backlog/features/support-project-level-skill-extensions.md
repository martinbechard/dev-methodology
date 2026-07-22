# Support Project-Level Skill Extensions

Status: Completed

Type: Feature

Provider: file

Provider Reference: backlog/completed-backlog/features/support-project-level-skill-extensions.md

Completion: direct-main

## Discovery Execution

- Owner: Unowned
- Claim: None
- Canonical task: 019f85c8-62c2-71d0-bab4-861e863d03ed
- Worktree: /Users/martinbechard/.codex/worktrees/9052/dev-methodology
- Branch: codex/support-project-level-skill-extensions
- Starting main: 2624b5b25ba6e5548051d7b9953933b1e57b3f87
- Phase: Bounded schema, renderer, and exact governed-scope discovery completed; the recorded exact approval permits Ready-state dispatch within the stated scope.
- Started: 2026-07-21
- Running-record claim: start-project-skill-extensions-019f85c8, acquired event 294844ff-d66c-4452-bb44-9d6d1be019de.
- Open issues: No user-action issue remains. Implementation must stay within the approved exact scope.
- Accepted candidate: Pending.

## Delivery Execution / Ownership

- Owner: Dev Orchestrator
- Canonical task: /root/process_backlog/orch_project_skill_extensions
- Artifact claim: project-skill-extensions-20260722
- Branch: codex/project-skill-extensions-20260722
- Canonical worktree: /Users/martinbechard/dev/dev-methodology/.worktrees/project-skill-extensions-20260722
- Starting main: 13ea3ffe92fe7a8352f33b4f618f39f212322ba3
- Phase: Completed and archived after direct-main integration, independent review, and focused verification.
- Candidate: Original candidate 318b9b5; accepted replacement a51047d38bde667aafbf9332a5b74023fe9226b0.
- Accepted commit: a51047d38bde667aafbf9332a5b74023fe9226b0.
- Integration: Main commit b1bfab01eba64640987f912bb61f1655fc64415d, with first parent 922c07b5 and second parent a51047d38bde667aafbf9332a5b74023fe9226b0.
- Delivery claim: project-skill-extensions-20260722 released at event d6ed3f0d-195f-42b7-ba74-287c0ab045bf.
- Correction claim and release: 8b75233a-b60a-4de9-93de-4e37fb39a752 / 57fc94bb-ae9a-4925-bb29-67433de710b9.
- Integration claim and release: 4a7d1ce2-f101-4921-a0d7-e99adb92d4af / 5cf58d0f-4730-4d0e-b21d-97a160b7f4e0.
- Review: Original code PASS; original methodology CHANGES REQUIRED because a nested output was generated at the root-only boundary. The correction code and methodology reviews both PASS. Post-integration code and methodology reviews both PASS, including exact 31-path/blob identity and no merge drift.
- Verification: Candidate VERIFIED-PASS: 94 renderer tests, five verbose acceptance checks, bundle contract, validation, freshness, diff, manifest SHA, and clean state. Integration-focused verification on current main VERIFIED-PASS: 31 exact blobs, no later project-path changes, five focused checks plus bundle, validation, freshness, diff, and clean state. Full campaign, project-wiki, and live catalog checks were skipped under bounded Tier 2 and the identical-byte post-integration rule. System Python 3.9 tomllib boundary was recorded; supported Python 3.11 passed.
- Deployment: No customized user packages were deployed.
- Completion wait started at: None.
- Completion wait attempts: 0.
- Terminal lifecycle claim: complete-project-skill-extensions-20260722, acquired event 7c867b43-c101-4034-b5c9-6e99656a6e91 for only the active item and completed-feature destination.

## Completion Evidence — 2026-07-22

- Completion authority: Explicit completion GO from parent coordinator /root/process_backlog/orch_project_skill_extensions.
- Direct-main observation: b1bfab01eba64640987f912bb61f1655fc64415d is reachable from main; no later project-level skill-extension paths changed before terminal closure.
- Archive: This record moved from backlog/feature-backlog/support-project-level-skill-extensions.md to backlog/completed-backlog/features/support-project-level-skill-extensions.md.
- Terminal verification: Focused lifecycle and file/report validation, plus git diff --check, are recorded with the terminal archive commit.

## User Action Required

### Question For The User

Do you approve changing exactly skills/create-project-configuration/SKILL.md and skills/development-methodology/SKILL.md, together with their supported generated skill mirrors and the directly related non-governed project template, renderer, focused validation and bundle tests, README, and skills-modularization design documentation, to implement backlog/feature-backlog/support-project-level-skill-extensions.md?

### Why User Input Is Required

The evidence-backed design requires changes to two governed skill definitions. Repository policy requires exact path-specific approval before mutation.

### Options And Tradeoffs

- Approve the exact two-skill scope: implement the ordered project-level extension mechanism and its directly related surfaces.
- Narrow the scope by naming allowed paths: preserve excluded behavior as blocked follow-up work.
- Defer: retain the discovery result without implementation.

### Resolution

Approved on 2026-07-22. The user answered "ok authorized" immediately after the exact Question For The User recorded above in the parent conversation. Provenance: parent coordination conversation for this backlog transition. The approval covers exactly skills/create-project-configuration/SKILL.md and skills/development-methodology/SKILL.md, their supported generated skill mirrors, and the directly related non-governed surfaces named in that question.

### Unattended Work Boundary

Ready-state work may proceed only within the exact approved scope. Any governed path or related surface outside the recorded question requires separate scope-specific approval. Preserve the resolved ordered-list schema and root-only reference rendering contract.

### Discovery Evidence

- Canonical task: 019f85c8-62c2-71d0-bab4-861e863d03ed.
- Clean branch/worktree: codex/support-project-level-skill-extensions at /Users/martinbechard/.codex/worktrees/9052/dev-methodology, based on 2624b5b25ba6e5548051d7b9953933b1e57b3f87.
- Schema decision: one ordered project_skill_extensions list accepts bundled identifiers and explicit registered-skill mapping entries; normalized skill id controls duplicate, availability, unknown, and definition-owned conflict checks.
- Rendering decision: one final Project Skill Extensions reference-only section is rendered in root AGENTS.md only; nested AGENTS.md files, technology loadouts, and workflow selectors remain independent.
- Exact governed manifest: skills/create-project-configuration/SKILL.md and skills/development-methodology/SKILL.md.
- Directly related non-governed surfaces: skills/development-methodology/assets/templates/project-template.yaml, scripts/render-agents-technology-skills.py, scripts/test_technology_detection.py, scripts/test_bundle_content.py, README.md, and design/skills-modularization.html.
- UAR routing claim: route-project-skill-extensions-approval, acquired event bf5b9715-7427-4e1d-b290-1e865248ecfb.

Creation Claim: capture-resource-coordination-dialogue-20260721

## Summary

Add an explicit PROJECT.yaml extension mechanism for project-selected skills whose references are appended to root AGENTS.md guidance.

## Context

The user proposed this capability during the resource-coordination dialogue on 2026-07-21. Current PROJECT.yaml configuration selects conceptual agents, workflow provider and completion skills, and folder technology skillsets, but it has no general project-level skill extension list.

Resource coordination is one consumer, but the extension mechanism must be generic rather than encoded as a coordination-only workaround.

## Source Evidence

- On 2026-07-21, the user proposed an extensions property in PROJECT.yaml that lets users add skills appended to project-level AGENTS.md guidance.
- The reviewed dialogue agreed to track its exact shape separately from the resource-coordination selector.
- On 2026-07-21, the user explicitly requested creation of work items based on those conversations.

## Requirements

- Define a documented PROJECT.yaml property for project-level skill extensions.
- Accept bundled skill identifiers and any explicitly supported registered-skill form.
- Validate duplicates, unknown identifiers, unavailable skills, and conflicts deterministically.
- Preserve declared order when order affects generated guidance; otherwise define stable canonical ordering.
- Render concise skill references at the end of root AGENTS.md without copying complete skill procedures.
- Keep folder technology-skill inlining and workflow selectors independent from this extension mechanism.
- Define how extensions interact with definition-owned skills so the same skill is not loaded twice.
- Update the project template, Project Configurator procedure, renderer, validation, documentation, and focused tests together.
- Obtain exact, scope-specific approval before changing governed skill definitions.

## Acceptance Criteria

- A project can declare one or more project-level extension skills in PROJECT.yaml.
- Generated root AGENTS.md contains deterministic reference-only guidance for each valid extension.
- Unknown, unavailable, duplicate, and conflicting entries fail with exact field paths and correction guidance.
- Nested AGENTS.md and folder technology skillsets are unchanged unless explicitly configured through their existing mechanisms.
- Existing definition-owned skills are not duplicated in generated instructions.

## Dependencies

None.

## Verification

- Design the exact YAML shape from existing PROJECT.yaml conventions.
- Test empty, single, multiple, duplicate, unknown, unavailable, and definition-owned-duplicate cases.
- Verify generated AGENTS.md placement and stable ordering.
- Run applicable project configuration, renderer, template, bundle, and documentation checks.
- Run Git diff validation and independent methodology review.

## Open Questions

- Should extensions be one ordered list or a mapping that can later carry setup-time validation metadata?
- Are project-level extensions inherited by nested AGENTS.md files or referenced only from the root-loaded contract?

## Delivery Evidence Update — 2026-07-22

- Current phase: Implementation active; candidate pending.
- Artifact claim: project-skill-extensions-20260722 acquired, event b48a3841-ac00-4585-8589-a7ae89be5540.
- Governed approval checks: Both exact pre-mutation checks returned ALLOWED before mutation.
- Scope extension: Atomic exact extension succeeded, event 1728aec3-e0c8-4d45-81b7-59f32aa72fc9, for proven README.md, scripts/test_bundle_content.py, generated outputs, and 20 adapter outputs.
- Candidate commit: Pending.
- Integration wait started at: None.
- Integration wait attempts: 0.
- Completion wait started at: None.
- Completion wait attempts: 0.
- Delivery evidence: Implementation in progress.
- Next owner: Dev Orchestrator.

## Parent Cleanup Evidence — 2026-07-22

- Task worktrees: Both project-skill-extension worktrees were already removed and clean before parent cleanup.
- Original branch: codex/project-skill-extensions-20260722 at 318b9b5 was verified as an ancestor of main and safely deleted with git branch -d.
- Correction branch: codex/project-skill-extensions-correction-1-20260722 at a51047d was verified as an ancestor of main and safely deleted with git branch -d.
- Worktree metadata: git worktree prune completed.
- Cleanup resource claim: coordinator-cleanup-project-skill-extensions-20260722 acquired, event e77ff382-7ecd-4328-a572-704887da26c8.
- Cleanup resource release: Released as no-change, event f0bf0a6a-5f2b-4278-8261-325d423cbcbb.
- Lifecycle result: The work item and collaboration task are terminal completed.
- Harness limitation: Task title and archive mutation is unavailable in this collaboration harness; UI archival is not claimed.
