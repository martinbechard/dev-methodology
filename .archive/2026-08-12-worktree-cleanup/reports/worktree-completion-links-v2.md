# Remaining worktree review, version 2

This report contains only worktrees that remained registered after the earlier cleanup. Entries are ordered from oldest to most recent using each worktree directory’s filesystem birth time as the local creation-age proxy.

Main comparison baseline: `ef5039e1acfbf6a6fe1645066f9ad655ea0a6783`.

- Worktrees reviewed: 134
- Same work present on main: 84
- Related work present on main: 49
- No clear related work found on main: 1

## Worktrees

### 1. codex/automate-parallel-agent-test-reporting

- Created: 2026-07-19T01:46:52.495410Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/parallel-agent-test-reporting-impl`
- HEAD: `ea5d39bf6bd549c4417237848e81cebe7cda630c`
- Synopsis: Adds a parallel agent-suite reporting module, runner support, documentation, and tests. It automates collection and validation of per-suite reports.
- Main relationship: **Same work is present on main**
- Evidence: The worktree commit is patch-equivalent to current main's parallel-reporting integration, including c0d4a1d0 and the current evals/agent-tests runner, suite_reporting.py, and tests.
- Confidence: High

### 2. codex/019f77f4-wiki-ingester-correction-2

- Created: 2026-07-19T02:17:29.159185Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/019f77f4-wiki-ingester-correction-2`
- HEAD: `c75c8b1195c7ab9744199960aec1ba7a139632c0`
- Synopsis: Adds Wiki Ingester interruption-control harness/tests and related backlog-claim and generated-agent updates.
- Main relationship: **Same work is present on main**
- Evidence: main contains the Wiki Ingester executable harness and contract tests, plus later reconciliation/completion commits cf79773f and a96a4c8f; the related claimed-resumption work is represented in the current backlog history.
- Confidence: Medium

### 3. codex/automate-parallel-agent-test-reporting-correction-1

- Created: 2026-07-19T02:19:38.215637Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/parallel-agent-test-reporting-correction-1`
- HEAD: `9c01df7ff5160f30b14f845f18064760edbc332f`
- Synopsis: Parallel-agent suite reporting correction; the two branch commits are patch-equivalent to current main's integrated reporting correction.
- Main relationship: **Same work is present on main**
- Evidence: git cherry main..9c01df7 marks both branch commits equivalent; main contains befc0c48 (Correct parallel agent reporting evidence) across the same seven eval/reporting files.
- Confidence: High

### 4. codex/automate-parallel-agent-test-reporting-correction-2

- Created: 2026-07-19T02:43:04.278187Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/parallel-agent-test-reporting-correction-2`
- HEAD: `13f16c0e67b3e0fc69bea621a5ae1c656f58c51d`
- Synopsis: Parallel agent-suite reporting was automated, hardened, and required governed agent evidence.
- Main relationship: **Same work is present on main**
- Evidence: All three worktree commits are patch-equivalent to commits reachable from main (git cherry main: 3 minus, 0 plus); the affected files are the agent-test reporting runner, suite reporter, tests, and evaluation docs.
- Confidence: High

### 5. codex/approval-definition-directive-impl

- Created: 2026-07-19T06:53:48.817830Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/approval-definition-directive-impl`
- HEAD: `f4b8c71f36d6d1ab92ef64c8e8b88ad2d45a1736`
- Synopsis: Adds approval and authority gates for definition regeneration, renderer contracts, adapter metadata, and related regression coverage. All five branch commits have patch-equivalent counterparts on current main.
- Main relationship: **Same work is present on main**
- Evidence: Branch f4b8c71f; five commits; git log --cherry-mark shows all five as '=' on main (including c4911e4f and peers).
- Confidence: High

### 6. codex/enforce-runnable-type-eligibility-in-backlog-report

- Created: 2026-07-19T07:29:38.073095Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/runnable-type-coder`
- HEAD: `c5c796106b5d19f53c0c350e5fa576f7c54fc45e`
- Synopsis: Adds a deterministic styled backlog-report generator and tests, then tightens runnable-type eligibility and user-action classification.
- Main relationship: **Same work is present on main**
- Evidence: Current main contains scripts/generate-backlog-report.py and its tests, including the later main commits 15c7c781, 360ad973, 09070eb0, 7bbbaa75, fd18da91, 0a78e087, 0b467696, and the matching runnable-type correction 82bde3ec.
- Confidence: High

### 7. codex/align-project-organiser-filename-selection-correction

- Created: 2026-07-19T08:54:30.922078Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/align-project-organiser-filename-selection-correction-coder`
- HEAD: `f56ad01f7cbbfdf08be09a855ce0a691a450318c`
- Synopsis: Adds a filename-authority guard to Project Organiser bundle tests. The sole branch commit is already represented in main by equivalent patch content.
- Main relationship: **Same work is present on main**
- Evidence: HEAD f56ad01f; merge-base bd2f4013; 2340/1 ahead-behind versus main ef5039e1; git cherry reports the sole commit as '-' (patch-equivalent in main).
- Confidence: High

### 8. codex/align-project-organiser-filename-selection-correction-verify

- Created: 2026-07-19T09:00:16.845983Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/align-project-organiser-filename-selection-correction-verify`
- HEAD: `f56ad01f7cbbfdf08be09a855ce0a691a450318c`
- Synopsis: Adds a regression test that guards Project Organiser filename authority.
- Main relationship: **Same work is present on main**
- Evidence: Branch commit f56ad01f; main contains equivalent patch as 6426a15c (Guard Project Organiser filename authority). git cherry main HEAD reports '-' for the branch commit.
- Confidence: High

### 9. codex/preserve-authoritative-config-renderer

- Created: 2026-07-19T12:00:57.861022Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/preserve-authoritative-config-renderer`
- HEAD: `a612fe255c96b28582433b5ff0390bed6a621832`
- Synopsis: Renderer source-evidence validation and its technology-detection tests.
- Main relationship: **Same work is present on main**
- Evidence: main contains the renderer change and validation coverage in scripts/render-agents-technology-skills.py and scripts/test_technology_detection.py; commit 4388c51d is the main equivalent.
- Confidence: High

### 10. codex/preserve-authoritative-config-eval

- Created: 2026-07-19T12:01:10.635289Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/preserve-authoritative-config-eval`
- HEAD: `0fc48bdf435983dfc7409eb2f678613d6dca6a92`
- Synopsis: Adds project-configurator evaluation coverage for preserving authoritative configuration evidence during a folder move. The scenario, supervisor/judge contract, and fixtures now require frozen-input digests, scalar detection evidence, and source-faithful generated guidance.
- Main relationship: **Same work is present on main**
- Evidence: HEAD 0fc48bdf; merge-base 2f55e1b4; main...HEAD counts 2319 behind / 1 ahead; one commit changes five project-configurator eval files.
- Confidence: High

### 11. codex/preserve-authoritative-config-renderer-correction-1

- Created: 2026-07-19T12:25:48.576817Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/preserve-authoritative-config-renderer-correction-1`
- HEAD: `6b5390436a03aaede4ec33ac4764f2067d133908`
- Synopsis: Hardens technology-skill rendering against malformed evidence rows and expands detection regression tests. Invalid renderer inputs are rejected instead of being emitted.
- Main relationship: **Same work is present on main**
- Evidence: The commit is patch-equivalent to current main's e2e7a47e renderer correction; scripts/render-agents-technology-skills.py and scripts/test_technology_detection.py contain the corresponding behavior.
- Confidence: High

### 12. codex/preserve-authoritative-config-eval-correction-1

- Created: 2026-07-19T13:45:40.349875Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/preserve-authoritative-config-eval-correction-1`
- HEAD: `c0fcca5ab7d0093f04e98fbe5df490281acaee88`
- Synopsis: Corrects Project Configurator evaluation fixtures, scenario contracts, and judge/supervisor evidence handling.
- Main relationship: **Same work is present on main**
- Evidence: The branch patch is present in main as patch-equivalent commit 5d48cfb8 (same configuration-evidence correction).
- Confidence: High

### 13. codex/automate-parallel-agent-test-reporting-recovery

- Created: 2026-07-19T15:27:34.589938Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/parallel-agent-reporting-recovery-producer-1`
- HEAD: `37141f9557f89bb28cb502c0ad718324d1c7ad72`
- Synopsis: Parallel-agent reporting recovery producer correction; branch commits are patch-equivalent to the current reporting implementation.
- Main relationship: **Same work is present on main**
- Evidence: git cherry marks the branch commits equivalent; main contains befc0c48 (Correct parallel agent reporting evidence) touching the same seven reporting and evaluation files.
- Confidence: High

### 14. codex/automate-parallel-agent-test-reporting-recovery-correction-2

- Created: 2026-07-19T16:14:19.026533Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/parallel-agent-reporting-recovery-producer-2`
- HEAD: `f3ad72eadb750ef6f14adf0dab351540e3ddb9e9`
- Synopsis: Parallel agent reporting was corrected and bound to durable evidence.
- Main relationship: **Same work is present on main**
- Evidence: All five worktree commits are patch-equivalent to commits reachable from main (git cherry main: 5 minus, 0 plus); the same reporting runner, suite reporter, tests, and docs are present in main history.
- Confidence: High

### 15. codex/enforce-runnable-type-eligibility-fresh-correction1

- Created: 2026-07-19T16:27:36.619995Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/runnable-type-fresh-cycle-correction1`
- HEAD: `719c8f334e7c47c6039d8f739ae4bfb2fb7c9c44`
- Synopsis: Corrects backlog dependency-link classification and expands its generator tests. The single branch commit is present on main with an equivalent patch.
- Main relationship: **Same work is present on main**
- Evidence: Branch 719c8f33; main contains equivalent e2d1c0b5; cherry comparison marks the branch commit '='.
- Confidence: High

### 16. codex/align-project-organiser-filename-selection-fresh-regression-correction

- Created: 2026-07-19T16:42:57.771417Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/align-project-organiser-filename-selection-fresh-regression-correction`
- HEAD: `e4bf1ae04627d6196ad392c5660e995ffd6c84c1`
- Synopsis: Strengthens Project Organiser path-selection output contracts, including explicit six-facet classification and mutually exclusive approval versus blocker responses, with generated adapters and regressions.
- Main relationship: **Same work is present on main**
- Evidence: The same eight source/generated/test surfaces are present on main through ddd3d227 (Integrate Project Organiser filename selection correction); current agents/roles/project-setup/project-organiser.role.yaml and scripts/test_bundle_content.py retain the approval/blocker contract.
- Confidence: High

### 17. codex/codex-workitem-coordination-role-2

- Created: 2026-07-19T16:44:55.759045Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/codex-workitem-coordination-role-source-2`
- HEAD: `d46717c1d231d11cf1e2ca57006a8a475216979f`
- Synopsis: Adds the Dev Backlog Coordinator role definition. Its sole branch commit is already represented in main by equivalent patch content.
- Main relationship: **Same work is present on main**
- Evidence: HEAD d46717c1; merge-base 57540b9b; 2305/1 ahead-behind; git cherry reports d46717c1 as '-' against main ef5039e1.
- Confidence: High

### 18. codex/codex-workitem-coordination-skill-2

- Created: 2026-07-19T16:44:57.695226Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/codex-workitem-coordination-skill-source-2`
- HEAD: `49f35ef0894df8439d9330d585b845246e1ad0b2`
- Synopsis: Adds the Codex work-item coordination skill source and Codex adapter metadata.
- Main relationship: **Same work is present on main**
- Evidence: Branch commit 49f35ef0; main contains equivalent work as a15d745f (Add Codex work-item coordination skill). git cherry main HEAD reports '-'.
- Confidence: High

### 19. codex/codex-workitem-coordination-evals-docs-2

- Created: 2026-07-19T16:44:58.446764Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/codex-workitem-coordination-evals-docs-2`
- HEAD: `3ab0ab9b3970f6d0fe618d883880782d4aaf933c`
- Synopsis: Codex work-item coordination evaluation scenarios and documentation.
- Main relationship: **Same work is present on main**
- Evidence: main has the codex-workitem-coordination skill plus the coordinated evaluation/catalog updates; later coordination-split commits (including 3c5b0752) carry the work forward.
- Confidence: High

### 20. codex/enforce-behavioral-regression-provenance-correction-1

- Created: 2026-07-19T17:03:29.352359Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/enforce-behavioral-regression-provenance-correction-1`
- HEAD: `d0ace0d9864c8e24465dcfcd544b761f81faca93`
- Synopsis: Strengthens agent-skill evaluation validation for behavioral-regression command provenance. It resolves phase-marked JSON evidence and rejects missing, duplicated, ambiguous, mismatched, or non-green/green command records.
- Main relationship: **Same work is present on main**
- Evidence: HEAD d0ace0d9; merge-base 57540b9b; main...HEAD counts 2305 behind / 2 ahead; two commits modify validation.py and its tests (409 lines added).
- Confidence: High

### 21. codex/parallel-reporting-duplicate-terminal-fix

- Created: 2026-07-19T17:08:42.104279Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/parallel-reporting-duplicate-terminal-fix`
- HEAD: `be89d695b3911a4437e8838204f9ac9cabbc9603`
- Synopsis: Builds out durable parallel-suite reporting and rejects duplicate Judge terminal responses. It adds reporting contracts, runner validation, and extensive regression coverage.
- Main relationship: **Same work is present on main**
- Evidence: All branch commits are patch-equivalent to current main's reporting sequence (6fe1e821, 4e1b5131, befc0c48, 4f10fa62, 872de683, and 90c937a4) and the same evals/agent-tests files are present.
- Confidence: High

### 22. codex/codex-workitem-coordination-role-correction-1

- Created: 2026-07-19T17:14:51.920143Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/codex-workitem-coordination-role-correction-1`
- HEAD: `aabfdf9693a94e41017400233656b5cd25941cfa`
- Synopsis: Adds and corrects the Dev Backlog Coordinator role definition and its lifecycle boundaries.
- Main relationship: **Same work is present on main**
- Evidence: The branch correction is patch-equivalent to main commit 11b50a6f, and the coordinator role source is present on main.
- Confidence: High

### 23. codex/codex-workitem-coordination-skill-correction-1

- Created: 2026-07-19T17:14:54.003929Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/codex-workitem-coordination-skill-correction-1`
- HEAD: `8d6840487c8f61f80543d9c181c10e98157c27a9`
- Synopsis: Codex work-item coordination baton-authority clarification; the branch change is already represented in main.
- Main relationship: **Same work is present on main**
- Evidence: git cherry marks the branch commits equivalent; main contains 1be95a9d (Clarify Codex coordination baton authority) for the coordination skill surface.
- Confidence: High

### 24. codex/codex-workitem-coordination-evals-correction-1

- Created: 2026-07-19T17:14:55.233390Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/codex-workitem-coordination-evals-correction-1`
- HEAD: `0b8dfe3c385554f8267e3446c108cfd5d57ee7d3`
- Synopsis: Codex work-item coordination evaluation scenarios and executable protocol coverage were added.
- Main relationship: **Same work is present on main**
- Evidence: Both worktree commits are patch-equivalent to commits reachable from main (git cherry main: 2 minus, 0 plus), covering coordination scenarios, simulator, fixtures, generated design, and project guidance.
- Confidence: High

### 25. codex/codex-workitem-coordination-role-correction-2

- Created: 2026-07-19T17:33:35.328338Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/codex-workitem-coordination-role-correction-2`
- HEAD: `7d221f136e2116a4e6a032889daf9e8feec98e07`
- Synopsis: Introduces and then clarifies the Dev Backlog Coordinator role, including baton wake audit and authority boundaries. All three commits are present equivalently on current main.
- Main relationship: **Same work is present on main**
- Evidence: Branch 7d221f13; main contains equivalent commits 92bc09f8, 11b50a6f, and e120d6aa; all cherry-mark '='.
- Confidence: High

### 26. codex/codex-workitem-coordination-evals-correction-2

- Created: 2026-07-19T17:33:38.536033Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/codex-workitem-coordination-evals-correction-2`
- HEAD: `aefd03f546ca5edcce6a2811393ad74d25735b1b`
- Synopsis: Adds executable Dev Backlog Coordinator coordination simulations, fixtures, requirements, and suite coverage, then corrects their evidence contracts.
- Main relationship: **Same work is present on main**
- Evidence: Main contains the coordinator simulator and suite files, with integration/correction history including 4175b8fc (executable coordination coverage) and 913260bf (correct coordination evaluation evidence); current evals/agent-tests/dev-backlog-coordinator files match that work.
- Confidence: High

### 27. codex/parallel-reporting-null-scenario-results-correction-1

- Created: 2026-07-19T17:37:54.338112Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/parallel-reporting-null-scenario-results-correction-1`
- HEAD: `0b590f84e1edaa627a08512dc2a8c3f92a33c3ab`
- Synopsis: Adds malformed-reporting validation and a large parallel-agent reporting test suite. All seven branch commits are already represented in main by equivalent patch content.
- Main relationship: **Same work is present on main**
- Evidence: HEAD 0b590f84; merge-base 57540b9b; 2305/7 ahead-behind; git cherry reports all seven commits as '-' against main ef5039e1.
- Confidence: High

### 28. codex/codex-workitem-coordination-preintegration-verify

- Created: 2026-07-19T17:52:28.235470Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/codex-workitem-coordination-preintegration-verify`
- HEAD: `8470cfe2c6f262cd7129530ec639b7c7beec8c69`
- Synopsis: Pre-integration coordination candidate with skill, role, simulator, fixtures, and evaluation evidence.
- Main relationship: **Same work is present on main**
- Evidence: All eight branch commits, including 8470cfe2, have equivalent '-' entries from git cherry main HEAD; main therefore contains this coordination candidate and its corrections.
- Confidence: High

### 29. codex/codex-workitem-coordination-15-minute-audit-refinement

- Created: 2026-07-19T18:10:16.980330Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/codex-workitem-coordination-15-minute-audit-refinement`
- HEAD: `ecc0d6d0e7bfadd2b60b57e361d7c038fd1f73ad`
- Synopsis: A 15-minute coordination-audit skill and agent adapter.
- Main relationship: **Same work is present on main**
- Evidence: main contains skills/codex-workitem-coordination and its agent adapter, with the 15-minute audit definition and correction commits (80f35ccb and 5683e5c4).
- Confidence: High

### 30. codex/codex-workitem-coordination-15-minute-audit-correction-2

- Created: 2026-07-19T18:21:25.523852Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/codex-workitem-coordination-15-minute-audit-correction-2`
- HEAD: `e3c892cf4dbf10bc011b99f001abea836c10b19e`
- Synopsis: Introduces the codex-workitem-coordination skill and adapter with an explicit 15-minute coordination-audit procedure. The commits define baton authority and classify audit observations without changing unrelated provider lifecycle ownership.
- Main relationship: **Same work is present on main**
- Evidence: HEAD e3c892cf; merge-base 57540b9b; main...HEAD counts 2305 behind / 4 ahead; four commits add the skill and its OpenAI metadata (249 lines).
- Confidence: High

### 31. codex/align-project-organiser-filename-selection-oracle-correction

- Created: 2026-07-19T18:23:28.332393Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/align-project-organiser-filename-selection-oracle-correction`
- HEAD: `41343b0327705504b1f9d50600b031dc5a8dbbed`
- Synopsis: Strengthens the Project Organiser filename-selection regression oracle in bundle-content tests. The added assertions cover required and forbidden selection markers.
- Main relationship: **Related work is present on main**
- Evidence: Current main already maintains scripts/test_bundle_content.py and related architecture/oracle tests, but the 41343b03 patch is not patch-equivalent and its new omission assertions are not present as the same change.
- Confidence: High

### 32. codex/codex-workitem-coordination-global-judge-catalog-2

- Created: 2026-07-19T18:28:32.632474Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/codex-workitem-coordination-global-judge-catalog-2`
- HEAD: `ef8313c63296c644a089e4ba103ad1da4cbde446`
- Synopsis: Adds deterministic judge declarations and the Codex work-item coordination skill/evaluation catalog.
- Main relationship: **Same work is present on main**
- Evidence: The branch's declaration commit is patch-equivalent to main commit 8f80da4b; the coordination skill and judge catalog are present on main.
- Confidence: High

### 33. codex/codex-workitem-coordination-bundle-catalog-correction

- Created: 2026-07-19T18:37:54.987878Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/codex-workitem-coordination-bundle-catalog-correction`
- HEAD: `54213be7b27a7fcef19b3a7a1ad12689d166dd58`
- Synopsis: Coordination-suite catalog assertion update spanning generated definitions, role guidance, fixtures, and tests; all branch commits are equivalent to main history.
- Main relationship: **Same work is present on main**
- Evidence: git cherry marks every branch commit equivalent; main contains 039a0d78 (Update coordination suite catalog assertions) and the resulting catalog/test surfaces.
- Confidence: High

### 34. codex/align-project-organiser-filename-selection-oracle-review-correction-1

- Created: 2026-07-19T18:45:43.352651Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/align-project-organiser-filename-selection-oracle-review-correction-1`
- HEAD: `517679cec2b1fd0288b0dea803ada3838ef83844`
- Synopsis: Project Organiser bundle-content regression oracles were hardened to recognize structured forbidden markers and path omissions.
- Main relationship: **Related work is present on main**
- Evidence: The work changes scripts/test_bundle_content.py, and current main contains the same structured forbidden-marker oracle area, but both branch commits remain non-equivalent additions (git cherry: 2 plus).
- Confidence: High

### 35. codex/align-project-organiser-filename-selection-oracle-omission-correction-2

- Created: 2026-07-19T19:12:18.786101Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/align-project-organiser-filename-selection-oracle-omission-correction-2`
- HEAD: `6e7eb7460a7e133b6a7d7ce37a262a41eefce019`
- Synopsis: Hardens Project Organiser filename-selection regression oracles and omission sentinels. Current main contains related Project Organiser filename-oracle and completion work, but not these exact three patches.
- Main relationship: **Related work is present on main**
- Evidence: Branch 6e7eb746 changes scripts/test_bundle_content.py; main history includes ddd3d227, a28b0681, and 28dcbda1 for the same Project Organiser filename-oracle area; cherry marks all branch commits '+'.
- Confidence: High

### 36. codex/add-mysql-technology-skill-source

- Created: 2026-07-19T19:26:08.003868Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/add-mysql-technology-skill-source`
- HEAD: `858062cc149d7dcb81d14980bfa791423057b25b`
- Synopsis: Introduces the MySQL technology skill source, detection metadata, OpenAI adapter, and detection regressions, then tightens detection evidence.
- Main relationship: **Same work is present on main**
- Evidence: Main contains skills/mysql/SKILL.md, skills/mysql/detection.yaml, skills/mysql/agents/openai.yaml, and test coverage via the integrated  da557bd6 Finalize MySQL, Quartz, and MapStruct skills commit; the later main state retains the MySQL source.
- Confidence: High

### 37. codex/codex-workitem-coordination-cumulative-assembly

- Created: 2026-07-19T19:32:53.839007Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/codex-workitem-coordination-cumulative-assembly`
- HEAD: `34e32614d20a210d1af0b55d40eb07c6ce83bd11`
- Synopsis: Builds cumulative Codex work-item coordination definitions, fixtures, simulators, and evaluation coverage. All thirteen branch commits are already represented in main by equivalent patch content.
- Main relationship: **Same work is present on main**
- Evidence: HEAD 34e32614; merge-base c1b551f0; 2287/13 ahead-behind; git cherry reports all thirteen commits as '-' against main ef5039e1.
- Confidence: High

### 38. codex/codex-workitem-coordination-cumulative-review-correction

- Created: 2026-07-19T19:54:27.905841Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/codex-workitem-coordination-cumulative-review-correction`
- HEAD: `82b8af69b7c0146edcabf6a62ceb92ed7bb7cc47`
- Synopsis: Cumulative coordination review correction enforcing parent-only release-gated wake repair.
- Main relationship: **Same work is present on main**
- Evidence: Every branch commit has an equivalent '-' entry from git cherry main HEAD; main includes the corresponding cumulative work, including 4ab5ff4b (Enforce parent-only release-gated wake repair).
- Confidence: High

### 39. codex/runnable-type-markdown-link-correction1

- Created: 2026-07-19T19:55:42.169705Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/runnable-type-markdown-link-correction1`
- HEAD: `00724e3b499fe44a9d24e081519d0c1e7d59bb21`
- Synopsis: Preservation of manual backlog dependency declarations and tests.
- Main relationship: **Same work is present on main**
- Evidence: main's dependency parser keeps qualified/manual links verbatim and the backlog-report tests cover those cases; commits 634d7f69 and 32c74af6 are the corresponding main corrections.
- Confidence: High

### 40. codex/verify-mysql-source-858062cc

- Created: 2026-07-19T20:01:17.436656Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/verify-mysql-source-858062cc`
- HEAD: `858062cc149d7dcb81d14980bfa791423057b25b`
- Synopsis: Adds a MySQL/InnoDB technology skill and detection registry, then tightens source-based activation tests. Detection requires pertinent source plus owning dependency or configuration evidence and avoids documentation, sibling-scope, and sample contamination.
- Main relationship: **Related work is present on main**
- Evidence: HEAD 858062cc; merge-base 8cb5b93e; main...HEAD counts 2291 behind / 2 ahead; two commits add skills/mysql and extend technology-detection tests (349 lines).
- Confidence: High

### 41. codex/align-project-organiser-filename-selection-complete-field-correction-3

- Created: 2026-07-19T20:07:30.588418Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/align-project-organiser-filename-selection-complete-field-correction-3`
- HEAD: `971bad6bc8a5ffe4b1aeafc49d49c88e48dc8da3`
- Synopsis: Extends the Project Organiser omission-boundary oracle through several follow-up corrections. It adds sentinel and container-boundary checks to bundle-content validation.
- Main relationship: **Related work is present on main**
- Evidence: Current main contains the same scripts/test_bundle_content.py oracle area and earlier bundle-content review commits, but the four worktree commits remain non-equivalent additions.
- Confidence: High

### 42. codex/parallel-reporting-terminal-uniqueness-correction-1

- Created: 2026-07-19T20:10:05.349007Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/parallel-reporting-terminal-uniqueness-correction-1`
- HEAD: `fd01292f4bdd4d0579f00faeb6c2d4eecf1b05d1`
- Synopsis: Builds parallel agent-suite reporting, durable response aggregation, and terminal-response uniqueness checks.
- Main relationship: **Same work is present on main**
- Evidence: main contains suite_reporting.py and the reporting history through 90c937a4, including duplicate-terminal rejection and durable evidence commits.
- Confidence: High

### 43. codex/deterministic-orchestrator-routing-resume-code

- Created: 2026-07-19T20:12:03.218629Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/deterministic-orchestrator-routing-resume-code`
- HEAD: `0be9b5eae932d36b3a724a540e64c54150502f9a`
- Synopsis: Deterministic orchestrator dependency-routing fixture and receipt-evidence correction; current main integrated the same fixture and routing work through follow-on commits.
- Main relationship: **Same work is present on main**
- Evidence: Main contains bc148680 (Add deterministic orchestrator dependency fixture), 269a21ac (Contain orchestrator routing evidence), and 4ef3ec15 (Integrate deterministic orchestrator routing) on the branch's 16-file surface; the branch commits are not patch-identical because main subsequently refined them.
- Confidence: High

### 44. codex/reporting-terminal-uniqueness-verify

- Created: 2026-07-19T20:22:28.921390Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/reporting-terminal-uniqueness-verify`
- HEAD: `fd01292f4bdd4d0579f00faeb6c2d4eecf1b05d1`
- Synopsis: Parallel agent reporting gained durable evidence and unique Judge terminal-response diagnostics.
- Main relationship: **Related work is present on main**
- Evidence: The branch shares the reporting runner, suite reporter, tests, and docs with main; its five reporting commits are equivalent in main, while the two uniqueness/diagnostic commits are not (git cherry: 5 minus, 2 plus).
- Confidence: High

### 45. codex/deterministic-orchestrator-routing-resume-correction2

- Created: 2026-07-19T20:46:13.085359Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/deterministic-orchestrator-routing-resume-correction2`
- HEAD: `6c598418892e784c9ea3a145f4e8307f93d85147`
- Synopsis: Adds deterministic orchestrator dependency-routing fixtures and tightens producer, receipt, and fallback evidence. One final patch is equivalent on main; the other four are distinct but concern the same routing contract.
- Main relationship: **Related work is present on main**
- Evidence: Branch 6c598418 has five commits; cherry marks only the final Bound routing fallback evidence '='; main also contains dependency-routing commits 48e6d614 and 2e92b255.
- Confidence: High

### 46. codex/deterministic-orchestrator-routing-resume-verify

- Created: 2026-07-19T20:51:44.056195Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/deterministic-orchestrator-routing-resume-verify`
- HEAD: `6c598418892e784c9ea3a145f4e8307f93d85147`
- Synopsis: Builds deterministic Dev Orchestrator dependency-routing fixtures and runner tests, then bounds routing fallback evidence.
- Main relationship: **Same work is present on main**
- Evidence: Main contains the dependency-routing fixture tree and runner tests, with the corresponding fallback-evidence correction represented by 22d09c0e; current evals/agent-tests/dev-orchestrator files include the fixture and routing checks.
- Confidence: High

### 47. codex/runnable-type-browser-verify-00724e3

- Created: 2026-07-19T21:10:42.269855Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/runnable-type-browser-verify-00724e3`
- HEAD: `00724e3b499fe44a9d24e081519d0c1e7d59bb21`
- Synopsis: Preserves manual backlog dependency declarations and adds report-generation tests. The branch commit remains unique, while main contains adjacent backlog-report lifecycle and validation changes.
- Main relationship: **Related work is present on main**
- Evidence: HEAD 00724e3b; merge-base c1b551f0; 2287/1 ahead-behind; git cherry reports '+'; main history for the changed report files includes terminal-series, dependency-aware lifecycle, and provider-ID work.
- Confidence: High

### 48. codex/add-quartz-technology-skill-source

- Created: 2026-07-19T22:02:23.167678Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/add-quartz-technology-skill-source`
- HEAD: `707d5fd6e354901e130bb4866a90d3825adcefab`
- Synopsis: Adds the Quartz Scheduler technology skill, adapter metadata, and detection configuration.
- Main relationship: **Same work is present on main**
- Evidence: Main has the Quartz source and later completion commits 2cf9f444 and da557bd6 (Finalize MySQL, Quartz, and MapStruct skills); skills/quartz/SKILL.md is present on main.
- Confidence: High

### 49. codex/add-mapstruct-technology-skill-source

- Created: 2026-07-19T22:03:18.259478Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/add-mapstruct-technology-skill-source`
- HEAD: `bdbd68c49064e34eeeaa636dcca4eb75f22b16a6`
- Synopsis: MapStruct technology skill source, adapter, and detection metadata.
- Main relationship: **Same work is present on main**
- Evidence: main contains skills/mapstruct/SKILL.md, agents/openai.yaml, and detection.yaml, finalized by the MapStruct integration commits da557bd6 and 265bb923.
- Confidence: High

### 50. codex/add-quartz-technology-skill-source-correction-1

- Created: 2026-07-19T22:11:56.624955Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/add-quartz-technology-skill-source-correction-1`
- HEAD: `9c726cfab21e69989a9e624736a42f72965eb8ca`
- Synopsis: Adds Quartz Scheduler technology guidance, metadata, and Java dependency detection. The skill covers job identity, misfires, concurrency, persistence, clustering, recovery, lifecycle, and verification, with security/testing routing.
- Main relationship: **Related work is present on main**
- Evidence: HEAD 9c726cfa; merge-base e040695e; main...HEAD counts 2264 behind / 2 ahead; two commits add skills/quartz source, adapter, and detection files (82 lines).
- Confidence: High

### 51. codex/enforce-documentation-template-conformance-dev-writer

- Created: 2026-07-19T22:27:53.071169Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/enforce-documentation-template-conformance-dev-writer`
- HEAD: `f016c8619d68d535e274b4bba8d6b9c0284a3c07`
- Synopsis: Hardens the documentation-writer module-design template fixture validator. It adds parsing, conformance, and fixture-test coverage for template structure and runnable evidence.
- Main relationship: **Related work is present on main**
- Evidence: Current main has the documentation-writer fixture, contract, and prior conformance integration commits; the f016c861 patch changes the same validator/test surfaces but is not patch-equivalent.
- Confidence: High

### 52. codex/restore-wiki-ingester-target-boundary

- Created: 2026-07-19T22:33:22.241552Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/restore-wiki-ingester-target-boundary`
- HEAD: `e663b43383ddad229180295e4ab17a8d60c56a87`
- Synopsis: Adds Wiki Ingester executable interruption-boundary harness and contract tests.
- Main relationship: **Same work is present on main**
- Evidence: Both harness/test files are present on main, with later Wiki Ingester interruption-routing and reconciliation commits in their path history.
- Confidence: High

### 53. codex/runnable-type-prerequisite-empty-delimiter-correction-1

- Created: 2026-07-19T22:35:31.096417Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/runnable-type-prerequisite-empty-delimiter-correction-1`
- HEAD: `9ee0adf7407a91f9cc29ee972ebc2d4776378a22`
- Synopsis: Backlog-report handling for empty query and fragment qualifiers; current main retains the behavior and tests through later report-validation work.
- Main relationship: **Same work is present on main**
- Evidence: Current main's _lexical_repository_target rejects '?' and '#' targets, and its tests retain the empty-qualified prerequisite cases; git log identifies fd18da91 and 5514063b as later carriers of that behavior.
- Confidence: High

### 54. codex/unsupported-review-structured-evaluator-recovery

- Created: 2026-07-19T22:39:16.790801Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/unsupported-review-structured-evaluator-recovery`
- HEAD: `08a35a16c1680886610851ea31be18bebe7ec1a6`
- Synopsis: Dev Code Reviewer fixture evaluation was extended to evaluate structured authority, contradiction, and uncertainty semantics.
- Main relationship: **Related work is present on main**
- Evidence: Main contains one of the three changed fixture files byte-for-byte and has the agent-suite rollout in its history; the evaluator and fixture-test additions remain unique to this branch (git cherry: 1 plus).
- Confidence: Medium

### 55. codex/parallel-reporting-semantic-integration-prep

- Created: 2026-07-19T22:41:06.721662Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/parallel-reporting-semantic-integration-prep`
- HEAD: `85befed5a0faa466595c39d2dabf1e370ec7ef07`
- Synopsis: Prepares accepted parallel agent-test reporting integration across runner, suite reporting, and tests. The single commit is present equivalently on current main.
- Main relationship: **Same work is present on main**
- Evidence: Branch 85befed5; main contains equivalent 90c937a4; cherry comparison marks '='.
- Confidence: High

### 56. codex/verify-codex-skill-activation-live

- Created: 2026-07-19T22:56:54.200889Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/verify-codex-skill-activation-live`
- HEAD: `f9c94244f991cd2893d7ad29a944eb72633c8929`
- Synopsis: Updates live Codex skill-activation evaluation fixtures and assertions to a newer MCP runtime identity/version.
- Main relationship: **Related work is present on main**
- Evidence: Main has an extensive, later-evolved activation/evaluation framework in evals/cases.yaml and scripts/test_agent_skill_evals.py, but the branch's exact runtime-identity assertion patch is not present as the same current contract; main has since changed the evaluation catalog and provider/runtime boundaries.
- Confidence: Medium

### 57. codex/review-authority-boundary-executable-correction

- Created: 2026-07-19T22:57:11.976694Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/review-authority-boundary-executable-correction`
- HEAD: `f4cf12978aed9be10ae7d9bc579f2f44df6c3071`
- Synopsis: Adds executable review-authority-boundary fixtures and evaluation wiring for the code reviewer. The branch commit remains unique, while main contains adjacent code-reviewer suite integration and hardening.
- Main relationship: **Related work is present on main**
- Evidence: HEAD f4cf1297; merge-base 32c74af6; 2257/1 ahead-behind; git cherry reports '+'; main history for changed reviewer fixtures includes accepted integration and agent-suite execution hardening.
- Confidence: High

### 58. codex/enforce-documentation-template-conformance-f016-correction

- Created: 2026-07-19T23:02:51.152067Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/enforce-documentation-template-conformance-f016-correction`
- HEAD: `0483c6d117503370d4371ba5d8f8ca909538d0b2`
- Synopsis: Corrects documentation-template conformance parser and fixture coverage.
- Main relationship: **Same work is present on main**
- Evidence: Main has the same validator/test paths and completion history, including 8bcbe38c (documentation template conformance) and eaf148d4 (Close documentation validator review gaps).
- Confidence: High

### 59. codex/review-authority-boundary-runtime-binding-correction

- Created: 2026-07-19T23:13:09.913969Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/review-authority-boundary-runtime-binding-correction`
- HEAD: `b76ec8ee437f583a79c8d8a5793eddde3a4735ce`
- Synopsis: Review-authority-boundary runtime-binding evaluation fixtures and evidence checks.
- Main relationship: **Same work is present on main**
- Evidence: main contains the header-policy-authority-boundary fixture, staging/evaluator scripts, scenario, and test coverage in evals/agent-tests/dev-code-reviewer; the integrated evidence commits preserve this work.
- Confidence: High

### 60. codex/enforce-documentation-template-conformance-0483-correction2

- Created: 2026-07-19T23:15:29.554332Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/enforce-documentation-template-conformance-0483-correction2`
- HEAD: `b9483a3997c720352edcfa2e98e87f894ae34bcc`
- Synopsis: Hardens the dev-documentation-writer template-conformance fixture and parser across three correction commits. It adds context-aware heading/readiness parsing, command inventory and path resolution, contradiction checks, and updated deterministic gates.
- Main relationship: **Related work is present on main**
- Evidence: HEAD b9483a39; merge-base 4ef3ec15; main...HEAD counts 2258 behind / 3 ahead; three commits modify five documentation-writer eval files (969-line net patch).
- Confidence: High

### 61. codex/enforce-documentation-template-conformance-b948-correction3

- Created: 2026-07-19T23:25:29.047420Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/enforce-documentation-template-conformance-b948-correction3`
- HEAD: `6fd28466768643c05d1332a101df994089e2b3cb`
- Synopsis: Refines the documentation-template parser across multiple corrections, especially container boundaries and context grammar. It expands fixture validation and regression tests.
- Main relationship: **Related work is present on main**
- Evidence: Current main contains the documentation-writer fixture and conformance history, while the four branch commits add different parser-boundary behavior and are not patch-equivalent.
- Confidence: High

### 62. codex/prevent-unsupported-review-findings-b76-correction

- Created: 2026-07-19T23:33:57.481526Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/prevent-unsupported-review-findings-b76-correction`
- HEAD: `12438b8638bcc58cffe6307c8f5c61389e2c71b4`
- Synopsis: Adds the reviewer header-policy authority-boundary fixture, staging/evaluation helpers, and contract coverage.
- Main relationship: **Same work is present on main**
- Evidence: main contains the header-policy fixture and evaluate_synthesis.py, followed by accepted review-integration candidate commit ba86db77.
- Confidence: High

### 63. codex/verification-tier-correction-019f77f4

- Created: 2026-07-19T23:45:51.542599Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/verification-tier-correction-019f77f4`
- HEAD: `57558659cf6cc84a42ef904f8e47702f0c50d6aa`
- Synopsis: Risk-tiered repository verification guidance; current main carries the same tiered validation policy in updated guidance.
- Main relationship: **Same work is present on main**
- Evidence: Main contains 6756b39a (Use targeted verification tiers), which carries the branch's Tier 1-4 validation model and bounded full-suite escalation guidance in AGENTS.md.
- Confidence: High

### 64. codex/activation-doc-version-correction

- Created: 2026-07-19T23:47:46.031147Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/activation-doc-version-correction`
- HEAD: `cabe6db92cb22b9e1aa086a3884e7993cc3d06c4`
- Synopsis: Agent-skill evaluation activation documentation and runtime identity were kept aligned.
- Main relationship: **Same work is present on main**
- Evidence: Both branch commits are patch-equivalent to commits reachable from main (git cherry main: 2 minus, 0 plus), affecting evals README/cases and the activation evaluation test.
- Confidence: High

### 65. codex/runnable-type-browser-verify-00724e3-resume

- Created: 2026-07-19T23:50:34.206616Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/runnable-type-browser-verify-00724e3-resume`
- HEAD: `00724e3b499fe44a9d24e081519d0c1e7d59bb21`
- Synopsis: Preserves manually declared backlog dependencies in runnable-type reporting and adds focused tests. The exact patch is absent, but current main has continued related backlog-report generator work.
- Main relationship: **Related work is present on main**
- Evidence: Branch 00724e3b changes scripts/generate-backlog-report.py and its tests; cherry marks '+'; main history continues dependency/reporting changes including 15c7c781 and 0b467696.
- Confidence: Medium

### 66. codex/runnable-type-browser-gate-00724e3-fresh

- Created: 2026-07-19T23:57:57.044267Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/runnable-type-browser-gate-00724e3-fresh`
- HEAD: `00724e3b499fe44a9d24e081519d0c1e7d59bb21`
- Synopsis: Preserves compact Markdown-link dependency declarations as manual prerequisites instead of converting them into local dependency identifiers, with regression tests.
- Main relationship: **Same work is present on main**
- Evidence: Current scripts/generate-backlog-report.py contains DEPENDENCY_LINK_PATTERN handling and manual-prerequisite reporting; main's e2d1c0b5 Fix backlog dependency link classification and subsequent dependency commits cover this behavior.
- Confidence: High

### 67. codex/parallel-reporting-current-main-reconciliation

- Created: 2026-07-19T23:59:38.425860Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/parallel-reporting-current-main-reconciliation`
- HEAD: `4bb13e40f0a23e3fba3248396b57a70c476fc104`
- Synopsis: Prepares an accepted parallel-reporting integration candidate with runner and suite-reporting fixes. All branch changes are patch-equivalent in main.
- Main relationship: **Same work is present on main**
- Evidence: HEAD 4bb13e40; merge-base 265bb923; 2253/1 ahead-behind; git cherry reports the commit as '-' against main ef5039e1.
- Confidence: High

### 68. codex/runnable-type-overflow-correction-00724e3

- Created: 2026-07-20T00:06:53.689099Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/runnable-type-overflow-correction-00724e3`
- HEAD: `65d2b56c0af877c8c0a8b741efee40d275042dff`
- Synopsis: Adds narrow-viewport wrapping for backlog report metadata and regression tests.
- Main relationship: **Same work is present on main**
- Evidence: Main's current generator includes overflow-wrap:anywhere and its test suite includes test_long_snapshot_metadata_has_narrow_viewport_wrap_contract; main also has final report commit 8e7abda5.
- Confidence: High

### 69. codex/runnable-type-overflow-browser-65d2b56

- Created: 2026-07-20T00:10:56.675045Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/runnable-type-overflow-browser-65d2b56`
- HEAD: `65d2b56c0af877c8c0a8b741efee40d275042dff`
- Synopsis: Narrow-screen wrapping for backlog report metadata.
- Main relationship: **Same work is present on main**
- Evidence: main's generated report CSS includes overflow-wrap metadata rules and the narrow-viewport tests in scripts/test_generate_backlog_report.py (including the broader accepted correction coverage).
- Confidence: High

### 70. codex/dependency-routing-schema-correction-4bb13e4

- Created: 2026-07-20T00:18:39.305609Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/dependency-routing-schema-correction-4bb13e4`
- HEAD: `f909046372e9688d20539609b845299739a242b9`
- Synopsis: Tightens agent-evaluation coordinator output schema and suite-report diagnostics. Required lane/role/commit/review/verification/claimRelease fields now gate reports, and malformed metadata retains diagnostics and evidence paths.
- Main relationship: **Same work is present on main**
- Evidence: HEAD f9090463; merge-base 265bb923; main...HEAD counts 2253 behind / 2 ahead; two commits modify runner/reporting code and tests (150-line net patch).
- Confidence: High

### 71. codex/verify-dev-coder-ts-019f77f4-live

- Created: 2026-07-20T00:26:49.318767Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/verify-dev-coder-ts-019f77f4-live`
- HEAD: `f909046372e9688d20539609b845299739a242b9`
- Synopsis: Adds a regression for a missing dependency receipt lane in parallel reporting. It updates runner aggregation and tests to preserve dependency evidence.
- Main relationship: **Same work is present on main**
- Evidence: Both branch commits are patch-equivalent to current main's accepted parallel-reporting integration and dependency-receipt regression (including 4d576882); the same four evals/agent-tests files are current.
- Confidence: High

### 72. codex/offline-node-staging-fix-019f77f4

- Created: 2026-07-20T00:32:26.539683Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/offline-node-staging-fix-019f77f4`
- HEAD: `9430332f6179f2dea945e5b734a73ee08e567187`
- Synopsis: Hardens offline Node dependency staging by locating the canonical primary worktree and validating symlink boundaries.
- Main relationship: **Same work is present on main**
- Evidence: main contains the same _canonical_primary_worktree/offline-staging implementation and its focused runner tests; current main is a later refinement of the branch patch.
- Confidence: High

### 73. codex/process-backlog-scheduler-correction

- Created: 2026-07-20T00:32:33.544805Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/process-backlog-scheduler-correction`
- HEAD: `a734b7fbca75dec87b91f20d891691d047c26f96`
- Synopsis: Scheduler handoff-routing additions to the former Codex work-item coordination skill; current main has the renamed coordination skill and related canonical-task handoff rules, but not the candidate text verbatim.
- Main relationship: **Related work is present on main**
- Evidence: The branch modifies skills/codex-workitem-coordination and its generated definition; current main uses skills/coordinate-codex-tasks and contains canonical-task handoff, wake, and stopped/archival reconciliation rules, while the branch-specific scheduler wording is absent.
- Confidence: Medium

### 74. codex/runnable-type-unblock-019f77f4

- Created: 2026-07-20T00:40:10.119580Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/runnable-type-unblock-019f77f4`
- HEAD: `eacd47c2d241ee7abe1834b5309d2de970c67e9d`
- Synopsis: Backlog report dependency parsing preserves qualified Markdown links as manual prerequisites.
- Main relationship: **Related work is present on main**
- Evidence: Current main actively contains the same backlog-report generator and tests, while this prerequisite-preservation commit is not patch-equivalent to main (git cherry: 1 plus).
- Confidence: High

### 75. codex/restore-wiki-ingester-target-boundary-resume

- Created: 2026-07-20T00:41:13.310055Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/restore-wiki-ingester-target-boundary-resume`
- HEAD: `1e113a276ca379b521a7bb0537daa3ba1b3ec7d2`
- Synopsis: Builds an executable Wiki Ingester interruption-boundary harness and contract tests. Current main contains subsequent Wiki Ingester interruption completion and reconciliation work, but not these exact patches.
- Main relationship: **Related work is present on main**
- Evidence: Branch 1e113a27 has four unique harness commits; main history includes a96a4c8f Complete Wiki Ingester interruption work item and ce35967e interruption reconciliation.
- Confidence: High

### 76. codex/process-backlog-scheduler-baton-refinement

- Created: 2026-07-20T00:43:39.490455Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/process-backlog-scheduler-baton-refinement`
- HEAD: `5a17e23f0fb2956ff3c54f3db3327d0b9c59beec`
- Synopsis: Refines Codex work-item coordination around claim-scope batons, parent scheduler audits, wake ownership, and adaptive concurrency.
- Main relationship: **Related work is present on main**
- Evidence: Main retains the renamed coordinate-work-items coordination skill and lifecycle-baton evaluation checks, but the branch's dedicated Claim-Scope Batons and Parent Scheduler Audit text is not present in the current skills/coordinate-work-items/SKILL.md; the coordination model has materially evolved.
- Confidence: Medium

### 77. codex/verify-offline-staging-482f85a

- Created: 2026-07-20T00:50:03.207877Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/verify-offline-staging-482f85a`
- HEAD: `482f85afb3f301319392c0e02c51d969d706d056`
- Synopsis: Stages offline dependency behavior in the agent-test runner and adds regression tests. The branch commit remains unique, while main contains adjacent runner lifecycle-receipt and claim-coordination changes.
- Main relationship: **Related work is present on main**
- Evidence: HEAD 482f85af; merge-base 353273d2; 2248/1 ahead-behind; git cherry reports '+'; main history for runner files includes lifecycle receipt, claim, and worktree-boundary hardening.
- Confidence: High

### 78. codex/fix-claim-scope-primary-resources

- Created: 2026-07-20T00:53:58.539304Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/fix-claim-scope-primary-resources`
- HEAD: `05990a23cdeacb66524dff052d2270e1500a5128`
- Synopsis: Fixes primary resource claim routing and adds claim regression coverage.
- Main relationship: **Same work is present on main**
- Evidence: Branch commit 05990a23; main contains equivalent patch fb85b046 (Fix primary resource claim routing), and git cherry main HEAD reports '-'.
- Confidence: High

### 79. codex/runner-offline-schema-correction-019f77f4

- Created: 2026-07-20T00:57:48.339172Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/runner-offline-schema-correction-019f77f4`
- HEAD: `276ce9c0efd583bda9505e3823f59cbfd8e12271`
- Synopsis: Offline dependency staging fallback and strict receipt/schema corrections.
- Main relationship: **Related work is present on main**
- Evidence: main retains the offline Node/Maven staging and receipt validation framework in evals/agent-tests/runner.py and test_runner.py, but the branch's canonical-primary-worktree fallback is not present verbatim.
- Confidence: Medium

### 80. codex/preserve-canonical-review-checklists

- Created: 2026-07-20T00:58:11.236960Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/preserve-canonical-review-checklists-artifact`
- HEAD: `d7164c2c634433a1988f7dcac4cddac26075974c`
- Synopsis: Adds a canonical checklist contract validator for dev-artifact-reviewer evaluations. It requires generic and applicable specialized checklists to preserve every source question and completion field in order, and binds retained evidence with SHA-256 digests and critical judge gates.
- Main relationship: **Related work is present on main**
- Evidence: HEAD d7164c2c; merge-base 901a2116; main...HEAD counts 2246 behind / 1 ahead; one commit changes seven evaluation/catalog files and adds 528 lines of validator tests/code.
- Confidence: High

### 81. codex/preserve-wiki-research-source-links

- Created: 2026-07-20T01:14:15.262027Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/preserve-wiki-research-source-links-artifact`
- HEAD: `dde9d061c139da880043f57153895faaffd06926`
- Synopsis: Adds executable validation for Wiki Research report source links and wires the scenario and tests into the suite. It checks source-link integrity and malformed links.
- Main relationship: **Same work is present on main**
- Evidence: The worktree patch is equivalent to current main's 3ebf5974 Wiki Research source-link integration; validate_links.py, scenarios.yaml, and test_source_links.py match that main behavior.
- Confidence: High

### 82. codex/baton-9-task-display-refinement

- Created: 2026-07-20T01:25:33.443169Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/baton-9-task-display-refinement`
- HEAD: `59aaa8b2a44b958b6f461ea9b525ad4c60b91f71`
- Synopsis: Refines Codex work-item coordination with numbered baton task displays and claim-scope scheduler handoffs.
- Main relationship: **Same work is present on main**
- Evidence: The branch head commit is present in main (59aaa8b2), and the coordination skill contains the baton-display refinements.
- Confidence: High

### 83. codex/restore-wiki-ingester-pre-move-2

- Created: 2026-07-20T01:26:27.874326Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/restore-wiki-ingester-pre-move-2`
- HEAD: `85404131f8cafce252e4be837e4dbdacc1058c71`
- Synopsis: Wiki Ingester interruption harness correction retaining the first live failure; current main completed related interruption work but does not contain this test patch verbatim.
- Main relationship: **Related work is present on main**
- Evidence: Main contains Wiki Ingester interruption completion and reconciliation commits (including a96a4c8f and ffea17a0) and later test-contract updates, but the branch's executable_harness.py/test_contract.py change is not patch-equivalent.
- Confidence: Medium

### 84. codex/baton-10-project-configurator-verdict

- Created: 2026-07-20T01:26:35.169619Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/baton-10-project-configurator-verdict`
- HEAD: `ce6e0a49313a949e50e168e1796e85bf8d5d0d9c`
- Synopsis: Project Configurator evaluation receipts were strengthened against contaminated or mixed inspection traces and incomplete verdict evidence.
- Main relationship: **Related work is present on main**
- Evidence: Main history includes Project Configurator verdict-integrity and runtime-bridge work in the same judge/supervisor/scenario/runner files; six branch commits remain non-equivalent (git cherry: 1 minus, 6 plus).
- Confidence: High

### 85. codex/baton-8-canonical-checklists-verifier

- Created: 2026-07-20T01:26:57.414795Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/baton-8-canonical-checklists-verifier`
- HEAD: `276ce9c0efd583bda9505e3823f59cbfd8e12271`
- Synopsis: Corrects offline staging and strict receipt-schema handling in the agent-test runner. The exact patch is absent, while current main has substantial subsequent runner receipt and verification changes.
- Main relationship: **Related work is present on main**
- Evidence: Branch 276ce9c0 changes evals/agent-tests/runner.py and test_runner.py; cherry marks '+'; main includes 6133d116 and 86cf8825 in those runner/test paths.
- Confidence: Medium

### 86. codex/baton-6-wiki-research-source-links-integration-prep

- Created: 2026-07-20T01:36:06.715789Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/baton-6-wiki-research-source-links-integration-prep`
- HEAD: `cdd5ef2aa94f9afe5ee9fb3f2de2c5bc4eaff103`
- Synopsis: Adds Wiki Researcher source-link validation and tests for report-relative links, with scenario coverage.
- Main relationship: **Same work is present on main**
- Evidence: Main contains evals/agent-tests/wiki-researcher/fixtures/wiki-research/validate_links.py, test_source_links.py, and the scenario update via 3ebf5974 Prepare Wiki Research source-link integration candidate; current source-link-resolution checks remain enabled.
- Confidence: High

### 87. codex/baton-9-one-minute-liveness-addendum

- Created: 2026-07-20T01:37:16.846360Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/baton-9-one-minute-liveness-addendum`
- HEAD: `3a5f1095977ff14f15190f4164c5b8f1b55af11a`
- Synopsis: Adds one-minute baton liveness checks and scheduler baton routing definitions. The four branch commits remain unique, while main contains adjacent backlog-dispatcher and watchdog scheduling work.
- Main relationship: **Related work is present on main**
- Evidence: HEAD 3a5f1095; merge-base 353273d2; 2248/4 ahead-behind; git cherry reports '+' for all four commits; main history for the changed coordination artifacts includes dispatcher and watchdog wakeup changes.
- Confidence: High

### 88. codex/baton-7-wiki-ingester-fail-fast

- Created: 2026-07-20T01:43:48.194528Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/baton-7-wiki-ingester-fail-fast`
- HEAD: `577627d68d45776be7d2a4db39764ea9c2a1ec69`
- Synopsis: Adds Wiki Ingester fail-fast contract tests that retain the first live failure.
- Main relationship: **Same work is present on main**
- Evidence: Main contains the Wiki Ingester contract path and subsequent completion/reconciliation commits a96a4c8f and 772993f8; the feature is present despite branch test refactoring.
- Confidence: High

### 89. codex/baton-1-bootstrapper-isolated-doubles

- Created: 2026-07-20T01:44:08.468438Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/baton-1-bootstrapper-isolated-doubles-artifact`
- HEAD: `c347031d0be4ee27116fd5402cff6ab1c5175ff1`
- Synopsis: Project Bootstrapper isolated-double scripted protocol tests.
- Main relationship: **Same work is present on main**
- Evidence: main contains the scripted Bootstrapper orchestration, live smoke path, suite, and tests under evals/agent-tests/project-bootstrapper; commit 4967f880 integrated the isolated test doubles.
- Confidence: High

### 90. codex/baton-3-current-main-integration-prep

- Created: 2026-07-20T01:44:46.813310Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/baton-3-current-main-integration-prep`
- HEAD: `507cde80e1f4ca41181d105d070387de29b34b98`
- Synopsis: Prepares an agent-skill lifecycle current-main integration candidate with generated explorer assets and lifecycle documentation. It adds the explorer UI/script, support-checklist logic, and focused tests for explorer, bundle, coverage, and lifecycle documentation.
- Main relationship: **Related work is present on main**
- Evidence: HEAD 507cde80; merge-base 08bbfa04; main...HEAD counts 2241 behind / 1 ahead; one commit changes 13 design, README, generator, and test files (6036 insertions).
- Confidence: High

### 91. codex/baton-7-wiki-ingester-prerequisite

- Created: 2026-07-20T01:55:55.734344Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/baton-7-wiki-ingester-prerequisite`
- HEAD: `aa3046c93d3a5505d84b707d538fc117381e22b3`
- Synopsis: Assembles an executable Wiki Ingester prerequisite harness and contract tests. The harness exercises ingestion behavior and validates the agent contract.
- Main relationship: **Related work is present on main**
- Evidence: Current main includes both wiki-ingester files and a long sequence of Wiki Ingester contract/reconciliation commits, but their current blobs differ from aa3046c9 and no exact patch-equivalent commit is present.
- Confidence: High

### 92. codex/baton-7-wiki-ingester-current-main

- Created: 2026-07-20T02:06:44.935486Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/baton-7-wiki-ingester-current-main`
- HEAD: `4748b1b1552f926075eacc829a3ed2cfd01ff530`
- Synopsis: Assembles the Wiki Ingester executable prerequisite harness and contract test suite.
- Main relationship: **Same work is present on main**
- Evidence: main contains both executable_harness.py and test_contract.py, with subsequent Wiki Ingester contract and result-readback commits.
- Confidence: High

### 93. codex/baton-2-project-configurator-current-main

- Created: 2026-07-20T02:06:55.135195Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/baton-2-project-configurator-current-main`
- HEAD: `effa4bd2ad72e6bffb3bec16c447285ead8944c9`
- Synopsis: Project Configurator current-main integration candidate; current main contains the same nine-file integration surface in later candidate/integration commits.
- Main relationship: **Same work is present on main**
- Evidence: Main contains fc653ad4 (Prepare Project Configurator primary integration) and later runner/current-main candidate work on the same Project Configurator fixtures, scenarios, and runner tests; differences are subsequent refinements.
- Confidence: High

### 94. codex/baton-10-judge-catalog

- Created: 2026-07-20T02:10:50.456573Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/baton-10-judge-catalog`
- HEAD: `c5a50e47f1d6d697e1cc2efc4ccbf96b2547879d`
- Synopsis: Dev Orchestrator dependency-routing judge checks were required to come from the critical deterministic-check catalog.
- Main relationship: **Related work is present on main**
- Evidence: The branch changes the orchestrator fixture test and judges catalog, and main has adjacent orchestrator deterministic-gate/catalog integration, but this commit is unique (git cherry: 1 plus).
- Confidence: Medium

### 95. codex/baton-6-wiki-research-current-main

- Created: 2026-07-20T02:11:07.194491Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/baton-6-wiki-research-current-main`
- HEAD: `a297b0547ed4f4b69c4fdb573d16c6dbdd44602a`
- Synopsis: Adds Wiki Research source-link validation fixtures and tests. The single candidate commit is present equivalently on current main.
- Main relationship: **Same work is present on main**
- Evidence: Branch a297b054; main contains equivalent 3ebf5974; cherry comparison marks '='.
- Confidence: High

### 96. codex/baton-10-judge-catalog-3949bb9

- Created: 2026-07-20T02:17:14.349603Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/baton-10-judge-catalog-3949bb9`
- HEAD: `74f7d68cedd553842781c4cc5c9f525f63d883bf`
- Synopsis: Registers deterministic judge checks for dependency-routing coordination evidence.
- Main relationship: **Same work is present on main**
- Evidence: Current evals/judges.yaml contains the dependency-routing judge checks, including one-nested-dependency-at-a-time, committed-handoffs, structured-handoff-receipts, and post-integration-reviews; the checks are used by current Dev Orchestrator scenarios.
- Confidence: High

### 97. codex/baton-9-current-main-reconcile

- Created: 2026-07-20T02:17:18.090237Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/baton-9-current-main-reconcile`
- HEAD: `30d7d1e84e758330d786b4aee233100584b0c0ab`
- Synopsis: Reconciles scheduler baton liveness in the Codex coordination skill. The branch commit remains unique, while main contains adjacent scheduler, dispatcher, and watchdog changes.
- Main relationship: **Related work is present on main**
- Evidence: HEAD 30d7d1e8; merge-base 5514063b; 2239/1 ahead-behind; git cherry reports '+'; main history for the changed skill and generated definition includes dispatcher and watchdog updates.
- Confidence: High

### 98. codex/baton-3-semantic-current-main

- Created: 2026-07-20T02:19:02.680621Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/baton-3-semantic-current-main`
- HEAD: `af9825660f7a6966efebb86532d79095d2d4c000`
- Synopsis: Documents cross-harness skill lifecycle behavior and updates generated design evidence.
- Main relationship: **Same work is present on main**
- Evidence: Branch commit af982566; main contains equivalent lifecycle documentation as cbd37825 (Document cross-harness skill lifecycle).
- Confidence: High

### 99. codex/baton-2-runner-receipts-timeout

- Created: 2026-07-20T02:20:10.303478Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/baton-2-runner-receipts-timeout`
- HEAD: `999fcd9da4adbea7ba67e1dc6d3fba0b3f17a9f0`
- Synopsis: Preservation of duplicate runner receipts and timeout handling.
- Main relationship: **Related work is present on main**
- Evidence: main has the evolved runner receipt/audit and timeout machinery in evals/agent-tests/runner.py and test_runner.py, but the branch's duplicate-call-ID audit implementation is no longer present as the same function.
- Confidence: Medium

### 100. codex/baton-10-judge-catalog-current-main

- Created: 2026-07-20T02:33:27.323957Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/baton-10-judge-catalog-current-main`
- HEAD: `ccf29acdf83ee812b93b2b18fe34c12be335dc96`
- Synopsis: Adds a deterministic judge-catalog entry for replaying dependency-routing checks. The isolated candidate consists solely of the corresponding evals/judges.yaml change.
- Main relationship: **Related work is present on main**
- Evidence: HEAD ccf29acd; merge-base 5b02b9e6; main...HEAD counts 2234 behind / 1 ahead; one commit adds 16 lines to evals/judges.yaml.
- Confidence: High

### 101. codex/baton-2-runner-current-main-prep

- Created: 2026-07-20T02:34:23.902977Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/baton-2-runner-current-main-prep`
- HEAD: `45604ced9da9005cef80ac624f4a51562cd9d50b`
- Synopsis: Prepares the agent-suite runner for current-main integration and adds broad runner regression coverage. It stages dependency and coordinator-schema behavior for integration.
- Main relationship: **Related work is present on main**
- Evidence: Current main has the same evals/agent-tests/runner.py and test_runner.py integration surface with later runner fixes, but 45604ced is not patch-equivalent to the current blobs.
- Confidence: High

### 102. codex/baton-8-canonical-checklists-current-main-prep

- Created: 2026-07-20T02:37:07.360935Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/baton-8-canonical-checklists-current-main-prep`
- HEAD: `7d858318af68a71791e200828779dbb9a31bc41c`
- Synopsis: Integrates canonical artifact-review checklist contracts, scenarios, tests, and judge catalog entries.
- Main relationship: **Same work is present on main**
- Evidence: main contains the checklist contract/test files and patch-equivalent preparation commit 2978cb23, with later canonical-checklist history.
- Confidence: High

### 103. codex/hibernate-panache-unique-source

- Created: 2026-07-20T02:39:04.528848Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/hibernate-panache-unique-source`
- HEAD: `672f16d3f41a3a86ce35a267f2f6948e027c6caa`
- Synopsis: Quarkus persistence boundary correction paired with the Hibernate ORM Panache split; current main finalized that split and retains the corrected Quarkus description.
- Main relationship: **Same work is present on main**
- Evidence: Main contains 7840fb3e (Finalize Hibernate ORM Panache skill split), and current skills/quarkus-persistence/SKILL.md retains the branch's boundary text with later wording refinement.
- Confidence: High

### 104. codex/baton-2-project-configurator-current-main-2

- Created: 2026-07-20T02:51:30.176881Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/baton-2-project-configurator-current-main-2`
- HEAD: `975a498d82f5e4e4e1e560b62e9120802524342c`
- Synopsis: Project Configurator current-main candidate handling rejected unpaired reads and completed Codex skill activation bookkeeping.
- Main relationship: **Related work is present on main**
- Evidence: Main history contains the same Project Configurator receipt/verdict and activation areas, but all three branch commits remain unique (git cherry: 3 plus); one branch file is a moved backlog record.
- Confidence: High

### 105. codex/hibernate-panache-metadata-dependency-repair

- Created: 2026-07-20T03:01:24.662819Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/hibernate-panache-metadata-dependency-repair`
- HEAD: `e0e0d50d910a36fa333b4a792c6a85dec7ae28a9`
- Synopsis: Splits Hibernate ORM Panache guidance from Quarkus persistence and aligns metadata and references with the narrowed scope. Current main contains later completion of that same skill split, but not these exact commits.
- Main relationship: **Related work is present on main**
- Evidence: Branch e0e0d50d has three unique commits adding skills/hibernate-orm-panache and editing Quarkus persistence; main history includes 7840fb3e and ac0ddc09 completing the split.
- Confidence: High

### 106. codex/baton-2-project-configurator-primary-prep

- Created: 2026-07-20T03:16:05.226854Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/baton-2-project-configurator-primary-prep`
- HEAD: `fc653ad42c954519948ae179bf2192bdb78d67e4`
- Synopsis: Prepares Project Configurator primary integration by extending fixture contracts, scenarios, supervisor/judge inputs, and runner tests.
- Main relationship: **Same work is present on main**
- Evidence: Main contains the Project Configurator fixture/test surfaces and their later corrections (including 5d48cfb8, ded845bf, 88b2a13c, and 9c232add); current project-configurator scenarios and test_fixtures.py retain the prepared integration behavior.
- Confidence: High

### 107. codex/verify-wiki-research-source-links

- Created: 2026-07-20T03:33:06.342653Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/verify-wiki-research-source-links`
- HEAD: `a297b0547ed4f4b69c4fdb573d16c6dbdd44602a`
- Synopsis: Adds Wiki Research source-link validation fixtures and tests. All branch changes are patch-equivalent in main.
- Main relationship: **Same work is present on main**
- Evidence: HEAD a297b054; merge-base 5514063b; 2239/1 ahead-behind; git cherry reports the commit as '-' against main ef5039e1.
- Confidence: High

### 108. codex/add-java-comment-placement-skill

- Created: 2026-07-22T01:52:09.023429Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/add-java-comment-placement-019f8781`
- HEAD: `02cc7215edce2782875998c3074a2a84ce5e441e`
- Synopsis: Adds the Java comment placement technology skill, fixtures, verifier, and generated catalog output.
- Main relationship: **Same work is present on main**
- Evidence: Main contains skills/java-comment/SKILL.md and equivalent source commit 22c1925c, followed by completion c879ed6e.
- Confidence: High

### 109. codex/future-ideas-implementation-20260722

- Created: 2026-07-22T14:14:27.769272Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/future-ideas-implementation-20260722`
- HEAD: `65b94bc05f8745e67c53fb6e7963b32c90e7a2fd`
- Synopsis: Lightweight Future Ideas capture and file-provider workflow.
- Main relationship: **Same work is present on main**
- Evidence: main contains the Future Ideas workflow, atomicity rules, generated projections, and report support; commits 8f6e7120 and 50d00082 carry the feature and hardening.
- Confidence: High

### 110. codex/future-ideas-correction-1-current-main-20260722

- Created: 2026-07-22T16:17:47.796231Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/future-ideas-correction-1-current-main-20260722`
- HEAD: `e3b605bf6e285833ea3b51ed3f3a71217bf7d2eb`
- Synopsis: Corrects the Future Ideas workflow so lightweight ideas are file-provider records outside ordinary work-item lifecycle, capacity, and dispatch counts. It adds explicit capture/list/validation/promotion rules, reciprocal provenance fixtures, report opt-in handling, and regenerated steward contracts/adapters.
- Main relationship: **Related work is present on main**
- Evidence: HEAD e3b605bf; merge-base 0ac3b572; main...HEAD counts 1971 behind / 1 ahead; one commit spans 24 role/skill/report/evaluation/generated files (967-line net patch).
- Confidence: High

### 111. codex/future-ideas-correction-2-current-main-20260722

- Created: 2026-07-22T16:47:45.888313Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/future-ideas-correction-2-current-main-20260722`
- HEAD: `abbc76d03d3fdb8675de561c91342228cd22ea8a`
- Synopsis: Adds a file-backed Future Ideas workflow and updates the steward role, generated adapters, reporting script, skills, and evaluation fixtures. It separates Future Ideas records from ordinary backlog handling.
- Main relationship: **Related work is present on main**
- Evidence: Current main already contains Future Ideas workflow and projection commits across the steward role, work-item contracts, report script, and evaluations, but abbc76d0 remains a distinct non-equivalent implementation.
- Confidence: High

### 112. codex/wiki-karpathy-okf-20260724

- Created: 2026-07-24T17:35:41.197484Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/wiki-karpathy-okf-20260724`
- HEAD: `ea34668a2dd682ac23a7243a0e5f273300382c70`
- Synopsis: Clarifies the Karpathy and OKF wiki model in the project wiki-skills documentation page.
- Main relationship: **Same work is present on main**
- Evidence: The exact branch commit ea34668a is in main history, followed by later wiki source-boundary clarification.
- Confidence: High

### 113. codex/decouple-dev-orchestrator-eval-correction2-019f96ce

- Created: 2026-07-25T02:12:54.277992Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/decouple-dev-orchestrator-eval-correction2-019f96ce`
- HEAD: `2be3274a869355a9078d81b918700909006db652`
- Synopsis: Orchestrator evaluation companion change to use real claims; current main evolved the same dependency-routing fixture to explicit none/resource-claim cases rather than retaining this patch.
- Main relationship: **Related work is present on main**
- Evidence: Current main's dependency-routing fixture and tests are maintained through event-driven claim-contract commits, but fixture-contract.yaml now declares selected none/resource-claim cases and does not contain the branch's real-claim assertions verbatim.
- Confidence: Medium

### 114. codex/durable-defect-creation-coder-019f96cf

- Created: 2026-07-25T02:40:44.703052Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/durable-defect-creation-coder-019f96cf`
- HEAD: `503de4bc4cfd28155f6f4e2c020581889a24687e`
- Synopsis: Durable confirmed-defect recording and terminal-closure ordering were enforced for Dev Orchestrator.
- Main relationship: **Related work is present on main**
- Evidence: Main contains related orchestrator role and generated-adapter changes; two branch commits are patch-equivalent and two are unique (git cherry: 2 minus, 2 plus), so the complete branch work is not present.
- Confidence: High

### 115. codex/campaign-candidate-integration-019f96cf

- Created: 2026-07-25T02:51:59.532815Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/campaign-candidate-integration-019f96cf`
- HEAD: `5931a8f865e2a177f952a4f778cc69ce4be1a08c`
- Synopsis: Adds a campaign-candidate finalizer flow across coordinator/orchestrator roles, generated adapters, merge skills, and integration tests. No matching or clearly related campaign-candidate history is present on current main.
- Main relationship: **No clear related work found on main**
- Evidence: Branch 5931a8f8 is one unique 19-file commit; main log has no campaign-candidate subject and no cherry-equivalent commit.
- Confidence: Medium

### 116. codex/add-structured-commit-disposition-correction1-019f970d

- Created: 2026-07-25T03:01:08.296503Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/structured-commit-disposition-correction1-019f970d`
- HEAD: `3352102081b85c3dcda4c23a22bb238c84b2062b`
- Synopsis: Adds structured orchestrator Commit disposition receipts and binds the receipt to the target commit event, with dependency-routing fixture and runner coverage.
- Main relationship: **Same work is present on main**
- Evidence: Current evals/agent-tests/runner.py explicitly validates successful claim-release event IDs binding the resulting commit and agent to the receipt (for example around line 2523), and current Dev Orchestrator fixture tests enforce structured handoff/commit evidence.
- Confidence: High

### 117. codex/architecture-assisted-unblocking

- Created: 2026-07-25T03:06:24.797670Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/architecture-assisted-unblocking-019f973a`
- HEAD: `6b329e8626316a33656346a296db4d9acee919f3`
- Synopsis: Adds architecture-assisted unblocking behavior to the backlog coordinator and regenerates related projections. The branch commit remains unique, while main contains adjacent coordinator dispatch and recovery work.
- Main relationship: **Related work is present on main**
- Evidence: HEAD 6b329e86; merge-base 0ce29d03; 1801/1 ahead-behind; git cherry reports '+'; main history for coordinator role and generated projections includes caller-owned dispatch and recovery updates.
- Confidence: High

### 118. codex/uar-protocol-019f9722-orchestrator-coder

- Created: 2026-07-25T03:25:25.518861Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/uar-protocol-019f9722-orchestrator-coder`
- HEAD: `59e9938810c9a498f3264f00a75d1424ed1deac4`
- Synopsis: Clarifies User Action Required gates across the orchestrator, file-work-item management, and coordination tests.
- Main relationship: **Same work is present on main**
- Evidence: Main's current Dev Orchestrator role explicitly defines User Action Required acceptance, gate, question, and resumption rules; later main history supersedes the branch's older file-work-item layout.
- Confidence: Medium

### 119. codex/add-structured-commit-disposition-correction2-019f970d

- Created: 2026-07-25T03:28:18.358887Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/structured-commit-disposition-correction2-019f970d`
- HEAD: `9f0aafce2281519b5d35dbffe0cba72561e50ed9`
- Synopsis: Dev Orchestrator workflow receipt and disposition evaluation corrections.
- Main relationship: **Same work is present on main**
- Evidence: main's dev-orchestrator scenarios, fixture contract, suite contract, and test_fixtures.py cover the selected workflow, nonterminal review, and structured receipt semantics from this branch.
- Confidence: High

### 120. codex/campaign-candidate-integration-correction1-019f96cf

- Created: 2026-07-25T03:30:42.347779Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/campaign-candidate-integration-correction1-019f96cf`
- HEAD: `21737be5b9c804b65c18b388aeff514ae881eeb3`
- Synopsis: Refreshes generated campaign-finalizer contracts after accepted lifecycle source changes. It updates coordinator/orchestrator roles and all supported adapters, adds campaign-candidate integration tests, and binds bundle tests to generated lifecycle output.
- Main relationship: **Related work is present on main**
- Evidence: HEAD 21737be5; merge-base dfbd1542; main...HEAD counts 1791 behind / 3 ahead; three commits modify generated role/skill adapters and add scripts/test_campaign_candidate_integration.py (approximately 1,100 lines changed).
- Confidence: High

### 121. codex/campaign-candidate-integration-correction2-019f96cf

- Created: 2026-07-25T04:25:54.930666Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/campaign-candidate-integration-correction2-019f96cf`
- HEAD: `6ab5976a3fe74c6bc9b0ab8e4faa80e4471c8f2f`
- Synopsis: Corrects the campaign finalizer transaction model and refreshes coordinator/orchestrator generated contracts. It adds a dedicated campaign-candidate integration test suite and lifecycle wording fixes.
- Main relationship: **Related work is present on main**
- Evidence: Current main contains the affected coordinator/orchestrator, generated-adapter, lifecycle, and work-item skill surfaces, but the campaign integration test and 6ab5976a transaction-model patch are not present equivalently.
- Confidence: Medium

### 122. codex/claim-release-reconciliation-recovery-019f9783

- Created: 2026-07-25T16:54:21.832447Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/019f9783-claim-release-reconciliation-recovery`
- HEAD: `8a20b9ed067a0b1b976eddf5126d088955d556f6`
- Synopsis: Adds descendant claim reconciliation and updates claim command/claim skill tests and documentation.
- Main relationship: **Same work is present on main**
- Evidence: The branch patch is present in main as patch-equivalent commit d652b0c0; claim helper separation and lifecycle refinements follow it.
- Confidence: High

### 123. codex/uar-examples-current-main-recovery

- Created: 2026-07-26T07:29:14.244090Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/uar-examples-current-main-recovery`
- HEAD: `aec92b112e4730d2ffe309d322a52f4a079043dd`
- Synopsis: User Action envelope integer, normalization, and state-invariant hardening; current main retains generic User Action routing but no matching envelope contract implementation was found.
- Main relationship: **Related work is present on main**
- Evidence: Current main's Dev Orchestrator role still defines User Action routing and lifecycle handling, but searches found no 9007199254740991, payload_digest, or recorded-not-presented envelope contract in the current skill tree; the specific invariant patch is absent.
- Confidence: Medium

### 124. codex/structured-commit-recovery-20260726

- Created: 2026-07-26T07:38:49.533780Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/structured-commit-recovery-coder`
- HEAD: `13277e498868e7e2e6f2b9bb40159982112bfd73`
- Synopsis: Dev Orchestrator dependency-routing evaluations were aligned with disposition-aware Commit and provider evidence ordering.
- Main relationship: **Related work is present on main**
- Evidence: Main has adjacent orchestrator Commit/provider-routing integrations in the same evaluation fixtures and runner, but all three branch commits remain unique (git cherry: 3 plus).
- Confidence: High

### 125. codex/decouple-orchestrator-current-main-correction-019f96ce

- Created: 2026-07-26T09:37:25.639051Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/decouple-orchestrator-current-main-correction-019f96ce`
- HEAD: `06f4c34b8e438833086359c682aa4be6063889b1`
- Synopsis: Binds orchestrator claim-audit evidence to staged helper authority, runtime rollouts, and adapter results. Current main has related orchestrator claim-audit remediation, but none of these three exact patches.
- Main relationship: **Related work is present on main**
- Evidence: Branch 06f4c34b has three unique commits; main history includes fb7ee1f5 Close orchestrator eval claim audit gaps and adjacent resource-claim corrections.
- Confidence: High

### 126. codex/runner-lifecycle-recovery-019f981c

- Created: 2026-07-26T11:09:45.921854Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/runner-lifecycle-recovery-019f981c`
- HEAD: `ac579e7c8d98e00ddc209b20558da5b29d662e30`
- Synopsis: Hardens agent-claim lifecycle evidence and recovery handling across the evaluation runner and its tests.
- Main relationship: **Same work is present on main**
- Evidence: Main's current evals/agent-tests/runner.py and test_runner.py include the later event-driven claim-coordination, lifecycle-receipt, no-claim, and recovery gates (5f537762, ab9489eb, ebcdcf29, 10bf58d4, 63cd4fe1, 572cd8f8); the branch's lifecycle-evidence behavior is retained and further evolved.
- Confidence: High

### 127. codex/establish-ste-technical-documentation-standard

- Created: 2026-07-28T16:32:09.119303Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/establish-ste-technical-documentation-standard`
- HEAD: `a4165c21f464e0cf74d72c6f81b7a64d49c90f62`
- Synopsis: Establishes the STE technical-documentation standard and updates roles, adapters, generated projections, and verification coverage. The five branch commits remain unique, while main contains adjacent terminology, documentation, and generated-definition work.
- Main relationship: **Related work is present on main**
- Evidence: HEAD a4165c21; merge-base 6affa81c; 1439/5 ahead-behind; git cherry reports '+' for all five commits; main history for changed files includes STE, documentation-methodology, and generated-definition updates.
- Confidence: High

### 128. codex/uar-brief-reminder-steward-019fa9be

- Created: 2026-07-28T21:13:43.778939Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/uar-brief-reminder-steward-019fa9be`
- HEAD: `032860972666b609ba436b6d67c76cf59645c944`
- Synopsis: Adds the backlog steward user-action brief reminder and regenerates role adapters.
- Main relationship: **Same work is present on main**
- Evidence: Branch commit 03286097; main contains equivalent commit 12912995 (Require steward user-action brief reminder), and the current steward role retains the rule.
- Confidence: High

### 129. codex/establish-ste-technical-documentation-standard-integration-current-771a7d39

- Created: 2026-07-28T23:57:58.435149Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/establish-ste-technical-documentation-standard-integration-current-771a7d39`
- HEAD: `d756549850bd86ff89d6ab1923a146069417e9bd`
- Synopsis: STE technical documentation standard integration across roles, skills, and adapters.
- Main relationship: **Same work is present on main**
- Evidence: main contains skills/ste-technical-writing, documentation-page-verify integration, approval records, role/adaptor updates, and the established standard commit 0c7784ca.
- Confidence: High

### 130. codex/eliminate-standalone-definition-approval-records-integration-019faeef

- Created: 2026-07-29T18:53:38.442552Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/eliminate-standalone-definition-approval-records-integration-019faeef`
- HEAD: `7cca88fee05db053e452729fcc094cc8309623ed`
- Synopsis: Integrates accepted source changes to eliminate standalone definition-approval records while preserving current-main lifecycle semantics. It removes the approval-record files, regenerates skill-definition output, and updates configuration, rendering, and technology-detection tests.
- Main relationship: **Related work is present on main**
- Evidence: HEAD 7cca88fe; merge-base d855b530; main...HEAD counts 1147 behind / 1 ahead; one commit removes 100+ approval-record files and updates AGENTS.md, PROJECT.yaml, render/tests, and coordination skills.
- Confidence: High

### 131. codex/review-agent-skill-specialization-examples-text

- Created: 2026-08-10T00:48:50.018556Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/review-agent-skill-specialization-examples-text`
- HEAD: `8b93e9867d40a3f808e1662c65ccb824fe7f6bff`
- Synopsis: Corrects the Beacon role specialization example and removes an unsupported role key. The follow-up commits align the example schema and generated HTML text.
- Main relationship: **Same work is present on main**
- Evidence: The branch sequence is patch-equivalent to current main's Beacon example corrections, including d0d6a16d; design/agent-skill-specialization-examples.html has the resulting current text.
- Confidence: High

### 132. detached at 3a2864355fd6

- Created: 2026-08-11T21:13:44.530044Z
- Worktree: `/Users/martinbechard/.codex/worktrees/69b1/dev-methodology`
- HEAD: `3a2864355fd6057fafd14145a6569872f54a4e93`
- Synopsis: Detached worktree snapshot has no changes beyond its recorded head.
- Main relationship: **Same work is present on main**
- Evidence: The detached head 3a286435 is an ancestor of main (main is ahead with zero commits unique to the detached head).
- Confidence: High

### 133. detached at f1490b80e856

- Created: 2026-08-11T22:35:53.396082Z
- Worktree: `/Users/martinbechard/.codex/worktrees/0742/dev-methodology`
- HEAD: `f1490b80e856df9cc08d24027acd3252734aac18`
- Synopsis: Wiki context text-review reservation; this worktree head is an ancestor of current main with no remaining tree difference.
- Main relationship: **Same work is present on main**
- Evidence: git merge-base equals the worktree head f1490b80, and git diff main..head is empty; current main contains the reservation commit.
- Confidence: High

### 134. codex/align-orchestrated-development-lifecycle-design-system-019ff2f9

- Created: 2026-08-11T22:38:18.295790Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/align-orchestrated-lifecycle-work-019ff2f9`
- HEAD: `ce7002bf2794c62cdbd7ebf58ff217aeb5e55935`
- Synopsis: The orchestrated-development lifecycle documentation was aligned to the design system, refreshed, and made keyboard-scrollable.
- Main relationship: **Related work is present on main**
- Evidence: Main contains nearby lifecycle/design-system documentation refreshes and generated artifacts, while all four branch commits are unique (git cherry: 4 plus); only three changed paths overlap the current main delta.
- Confidence: High
