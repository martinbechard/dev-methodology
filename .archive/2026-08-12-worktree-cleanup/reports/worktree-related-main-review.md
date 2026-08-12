# Remaining worktrees with related work on main

This focused review list contains only surviving worktrees classified as having related, but not clearly identical, work on main. Entries preserve the oldest-to-newest order from the version 2 audit.

- Worktrees to review: 49
- Original main comparison baseline: `ef5039e1acfbf6a6fe1645066f9ad655ea0a6783`

## Review list

### 1. codex/align-project-organiser-filename-selection-oracle-correction

- Original v2 position: 31
- Created: 2026-07-19T18:23:28.332393Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/align-project-organiser-filename-selection-oracle-correction`
- HEAD: `41343b0327705504b1f9d50600b031dc5a8dbbed`
- Synopsis: Strengthens the Project Organiser filename-selection regression oracle in bundle-content tests. The added assertions cover required and forbidden selection markers.
- Related work on main: Current main already maintains scripts/test_bundle_content.py and related architecture/oracle tests, but the 41343b03 patch is not patch-equivalent and its new omission assertions are not present as the same change.
- Confidence: High

### 2. codex/align-project-organiser-filename-selection-oracle-review-correction-1

- Original v2 position: 34
- Created: 2026-07-19T18:45:43.352651Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/align-project-organiser-filename-selection-oracle-review-correction-1`
- HEAD: `517679cec2b1fd0288b0dea803ada3838ef83844`
- Synopsis: Project Organiser bundle-content regression oracles were hardened to recognize structured forbidden markers and path omissions.
- Related work on main: The work changes scripts/test_bundle_content.py, and current main contains the same structured forbidden-marker oracle area, but both branch commits remain non-equivalent additions (git cherry: 2 plus).
- Confidence: High

### 3. codex/align-project-organiser-filename-selection-oracle-omission-correction-2

- Original v2 position: 35
- Created: 2026-07-19T19:12:18.786101Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/align-project-organiser-filename-selection-oracle-omission-correction-2`
- HEAD: `6e7eb7460a7e133b6a7d7ce37a262a41eefce019`
- Synopsis: Hardens Project Organiser filename-selection regression oracles and omission sentinels. Current main contains related Project Organiser filename-oracle and completion work, but not these exact three patches.
- Related work on main: Branch 6e7eb746 changes scripts/test_bundle_content.py; main history includes ddd3d227, a28b0681, and 28dcbda1 for the same Project Organiser filename-oracle area; cherry marks all branch commits '+'.
- Confidence: High

### 4. codex/verify-mysql-source-858062cc

- Original v2 position: 40
- Created: 2026-07-19T20:01:17.436656Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/verify-mysql-source-858062cc`
- HEAD: `858062cc149d7dcb81d14980bfa791423057b25b`
- Synopsis: Adds a MySQL/InnoDB technology skill and detection registry, then tightens source-based activation tests. Detection requires pertinent source plus owning dependency or configuration evidence and avoids documentation, sibling-scope, and sample contamination.
- Related work on main: HEAD 858062cc; merge-base 8cb5b93e; main...HEAD counts 2291 behind / 2 ahead; two commits add skills/mysql and extend technology-detection tests (349 lines).
- Confidence: High

### 5. codex/align-project-organiser-filename-selection-complete-field-correction-3

- Original v2 position: 41
- Created: 2026-07-19T20:07:30.588418Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/align-project-organiser-filename-selection-complete-field-correction-3`
- HEAD: `971bad6bc8a5ffe4b1aeafc49d49c88e48dc8da3`
- Synopsis: Extends the Project Organiser omission-boundary oracle through several follow-up corrections. It adds sentinel and container-boundary checks to bundle-content validation.
- Related work on main: Current main contains the same scripts/test_bundle_content.py oracle area and earlier bundle-content review commits, but the four worktree commits remain non-equivalent additions.
- Confidence: High

### 6. codex/reporting-terminal-uniqueness-verify

- Original v2 position: 44
- Created: 2026-07-19T20:22:28.921390Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/reporting-terminal-uniqueness-verify`
- HEAD: `fd01292f4bdd4d0579f00faeb6c2d4eecf1b05d1`
- Synopsis: Parallel agent reporting gained durable evidence and unique Judge terminal-response diagnostics.
- Related work on main: The branch shares the reporting runner, suite reporter, tests, and docs with main; its five reporting commits are equivalent in main, while the two uniqueness/diagnostic commits are not (git cherry: 5 minus, 2 plus).
- Confidence: High

### 7. codex/deterministic-orchestrator-routing-resume-correction2

- Original v2 position: 45
- Created: 2026-07-19T20:46:13.085359Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/deterministic-orchestrator-routing-resume-correction2`
- HEAD: `6c598418892e784c9ea3a145f4e8307f93d85147`
- Synopsis: Adds deterministic orchestrator dependency-routing fixtures and tightens producer, receipt, and fallback evidence. One final patch is equivalent on main; the other four are distinct but concern the same routing contract.
- Related work on main: Branch 6c598418 has five commits; cherry marks only the final Bound routing fallback evidence '='; main also contains dependency-routing commits 48e6d614 and 2e92b255.
- Confidence: High

### 8. codex/runnable-type-browser-verify-00724e3

- Original v2 position: 47
- Created: 2026-07-19T21:10:42.269855Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/runnable-type-browser-verify-00724e3`
- HEAD: `00724e3b499fe44a9d24e081519d0c1e7d59bb21`
- Synopsis: Preserves manual backlog dependency declarations and adds report-generation tests. The branch commit remains unique, while main contains adjacent backlog-report lifecycle and validation changes.
- Related work on main: HEAD 00724e3b; merge-base c1b551f0; 2287/1 ahead-behind; git cherry reports '+'; main history for the changed report files includes terminal-series, dependency-aware lifecycle, and provider-ID work.
- Confidence: High

### 9. codex/add-quartz-technology-skill-source-correction-1

- Original v2 position: 50
- Created: 2026-07-19T22:11:56.624955Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/add-quartz-technology-skill-source-correction-1`
- HEAD: `9c726cfab21e69989a9e624736a42f72965eb8ca`
- Synopsis: Adds Quartz Scheduler technology guidance, metadata, and Java dependency detection. The skill covers job identity, misfires, concurrency, persistence, clustering, recovery, lifecycle, and verification, with security/testing routing.
- Related work on main: HEAD 9c726cfa; merge-base e040695e; main...HEAD counts 2264 behind / 2 ahead; two commits add skills/quartz source, adapter, and detection files (82 lines).
- Confidence: High

### 10. codex/enforce-documentation-template-conformance-dev-writer

- Original v2 position: 51
- Created: 2026-07-19T22:27:53.071169Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/enforce-documentation-template-conformance-dev-writer`
- HEAD: `f016c8619d68d535e274b4bba8d6b9c0284a3c07`
- Synopsis: Hardens the documentation-writer module-design template fixture validator. It adds parsing, conformance, and fixture-test coverage for template structure and runnable evidence.
- Related work on main: Current main has the documentation-writer fixture, contract, and prior conformance integration commits; the f016c861 patch changes the same validator/test surfaces but is not patch-equivalent.
- Confidence: High

### 11. codex/unsupported-review-structured-evaluator-recovery

- Original v2 position: 54
- Created: 2026-07-19T22:39:16.790801Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/unsupported-review-structured-evaluator-recovery`
- HEAD: `08a35a16c1680886610851ea31be18bebe7ec1a6`
- Synopsis: Dev Code Reviewer fixture evaluation was extended to evaluate structured authority, contradiction, and uncertainty semantics.
- Related work on main: Main contains one of the three changed fixture files byte-for-byte and has the agent-suite rollout in its history; the evaluator and fixture-test additions remain unique to this branch (git cherry: 1 plus).
- Confidence: Medium

### 12. codex/verify-codex-skill-activation-live

- Original v2 position: 56
- Created: 2026-07-19T22:56:54.200889Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/verify-codex-skill-activation-live`
- HEAD: `f9c94244f991cd2893d7ad29a944eb72633c8929`
- Synopsis: Updates live Codex skill-activation evaluation fixtures and assertions to a newer MCP runtime identity/version.
- Related work on main: Main has an extensive, later-evolved activation/evaluation framework in evals/cases.yaml and scripts/test_agent_skill_evals.py, but the branch's exact runtime-identity assertion patch is not present as the same current contract; main has since changed the evaluation catalog and provider/runtime boundaries.
- Confidence: Medium

### 13. codex/review-authority-boundary-executable-correction

- Original v2 position: 57
- Created: 2026-07-19T22:57:11.976694Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/review-authority-boundary-executable-correction`
- HEAD: `f4cf12978aed9be10ae7d9bc579f2f44df6c3071`
- Synopsis: Adds executable review-authority-boundary fixtures and evaluation wiring for the code reviewer. The branch commit remains unique, while main contains adjacent code-reviewer suite integration and hardening.
- Related work on main: HEAD f4cf1297; merge-base 32c74af6; 2257/1 ahead-behind; git cherry reports '+'; main history for changed reviewer fixtures includes accepted integration and agent-suite execution hardening.
- Confidence: High

### 14. codex/enforce-documentation-template-conformance-0483-correction2

- Original v2 position: 60
- Created: 2026-07-19T23:15:29.554332Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/enforce-documentation-template-conformance-0483-correction2`
- HEAD: `b9483a3997c720352edcfa2e98e87f894ae34bcc`
- Synopsis: Hardens the dev-documentation-writer template-conformance fixture and parser across three correction commits. It adds context-aware heading/readiness parsing, command inventory and path resolution, contradiction checks, and updated deterministic gates.
- Related work on main: HEAD b9483a39; merge-base 4ef3ec15; main...HEAD counts 2258 behind / 3 ahead; three commits modify five documentation-writer eval files (969-line net patch).
- Confidence: High

### 15. codex/enforce-documentation-template-conformance-b948-correction3

- Original v2 position: 61
- Created: 2026-07-19T23:25:29.047420Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/enforce-documentation-template-conformance-b948-correction3`
- HEAD: `6fd28466768643c05d1332a101df994089e2b3cb`
- Synopsis: Refines the documentation-template parser across multiple corrections, especially container boundaries and context grammar. It expands fixture validation and regression tests.
- Related work on main: Current main contains the documentation-writer fixture and conformance history, while the four branch commits add different parser-boundary behavior and are not patch-equivalent.
- Confidence: High

### 16. codex/runnable-type-browser-verify-00724e3-resume

- Original v2 position: 65
- Created: 2026-07-19T23:50:34.206616Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/runnable-type-browser-verify-00724e3-resume`
- HEAD: `00724e3b499fe44a9d24e081519d0c1e7d59bb21`
- Synopsis: Preserves manually declared backlog dependencies in runnable-type reporting and adds focused tests. The exact patch is absent, but current main has continued related backlog-report generator work.
- Related work on main: Branch 00724e3b changes scripts/generate-backlog-report.py and its tests; cherry marks '+'; main history continues dependency/reporting changes including 15c7c781 and 0b467696.
- Confidence: Medium

### 17. codex/process-backlog-scheduler-correction

- Original v2 position: 73
- Created: 2026-07-20T00:32:33.544805Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/process-backlog-scheduler-correction`
- HEAD: `a734b7fbca75dec87b91f20d891691d047c26f96`
- Synopsis: Scheduler handoff-routing additions to the former Codex work-item coordination skill; current main has the renamed coordination skill and related canonical-task handoff rules, but not the candidate text verbatim.
- Related work on main: The branch modifies skills/codex-workitem-coordination and its generated definition; current main uses skills/coordinate-codex-tasks and contains canonical-task handoff, wake, and stopped/archival reconciliation rules, while the branch-specific scheduler wording is absent.
- Confidence: Medium

### 18. codex/runnable-type-unblock-019f77f4

- Original v2 position: 74
- Created: 2026-07-20T00:40:10.119580Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/runnable-type-unblock-019f77f4`
- HEAD: `eacd47c2d241ee7abe1834b5309d2de970c67e9d`
- Synopsis: Backlog report dependency parsing preserves qualified Markdown links as manual prerequisites.
- Related work on main: Current main actively contains the same backlog-report generator and tests, while this prerequisite-preservation commit is not patch-equivalent to main (git cherry: 1 plus).
- Confidence: High

### 19. codex/restore-wiki-ingester-target-boundary-resume

- Original v2 position: 75
- Created: 2026-07-20T00:41:13.310055Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/restore-wiki-ingester-target-boundary-resume`
- HEAD: `1e113a276ca379b521a7bb0537daa3ba1b3ec7d2`
- Synopsis: Builds an executable Wiki Ingester interruption-boundary harness and contract tests. Current main contains subsequent Wiki Ingester interruption completion and reconciliation work, but not these exact patches.
- Related work on main: Branch 1e113a27 has four unique harness commits; main history includes a96a4c8f Complete Wiki Ingester interruption work item and ce35967e interruption reconciliation.
- Confidence: High

### 20. codex/process-backlog-scheduler-baton-refinement

- Original v2 position: 76
- Created: 2026-07-20T00:43:39.490455Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/process-backlog-scheduler-baton-refinement`
- HEAD: `5a17e23f0fb2956ff3c54f3db3327d0b9c59beec`
- Synopsis: Refines Codex work-item coordination around claim-scope batons, parent scheduler audits, wake ownership, and adaptive concurrency.
- Related work on main: Main retains the renamed coordinate-work-items coordination skill and lifecycle-baton evaluation checks, but the branch's dedicated Claim-Scope Batons and Parent Scheduler Audit text is not present in the current skills/coordinate-work-items/SKILL.md; the coordination model has materially evolved.
- Confidence: Medium

### 21. codex/verify-offline-staging-482f85a

- Original v2 position: 77
- Created: 2026-07-20T00:50:03.207877Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/verify-offline-staging-482f85a`
- HEAD: `482f85afb3f301319392c0e02c51d969d706d056`
- Synopsis: Stages offline dependency behavior in the agent-test runner and adds regression tests. The branch commit remains unique, while main contains adjacent runner lifecycle-receipt and claim-coordination changes.
- Related work on main: HEAD 482f85af; merge-base 353273d2; 2248/1 ahead-behind; git cherry reports '+'; main history for runner files includes lifecycle receipt, claim, and worktree-boundary hardening.
- Confidence: High

### 22. codex/runner-offline-schema-correction-019f77f4

- Original v2 position: 79
- Created: 2026-07-20T00:57:48.339172Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/runner-offline-schema-correction-019f77f4`
- HEAD: `276ce9c0efd583bda9505e3823f59cbfd8e12271`
- Synopsis: Offline dependency staging fallback and strict receipt/schema corrections.
- Related work on main: main retains the offline Node/Maven staging and receipt validation framework in evals/agent-tests/runner.py and test_runner.py, but the branch's canonical-primary-worktree fallback is not present verbatim.
- Confidence: Medium

### 23. codex/preserve-canonical-review-checklists

- Original v2 position: 80
- Created: 2026-07-20T00:58:11.236960Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/preserve-canonical-review-checklists-artifact`
- HEAD: `d7164c2c634433a1988f7dcac4cddac26075974c`
- Synopsis: Adds a canonical checklist contract validator for dev-artifact-reviewer evaluations. It requires generic and applicable specialized checklists to preserve every source question and completion field in order, and binds retained evidence with SHA-256 digests and critical judge gates.
- Related work on main: HEAD d7164c2c; merge-base 901a2116; main...HEAD counts 2246 behind / 1 ahead; one commit changes seven evaluation/catalog files and adds 528 lines of validator tests/code.
- Confidence: High

### 24. codex/restore-wiki-ingester-pre-move-2

- Original v2 position: 83
- Created: 2026-07-20T01:26:27.874326Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/restore-wiki-ingester-pre-move-2`
- HEAD: `85404131f8cafce252e4be837e4dbdacc1058c71`
- Synopsis: Wiki Ingester interruption harness correction retaining the first live failure; current main completed related interruption work but does not contain this test patch verbatim.
- Related work on main: Main contains Wiki Ingester interruption completion and reconciliation commits (including a96a4c8f and ffea17a0) and later test-contract updates, but the branch's executable_harness.py/test_contract.py change is not patch-equivalent.
- Confidence: Medium

### 25. codex/baton-10-project-configurator-verdict

- Original v2 position: 84
- Created: 2026-07-20T01:26:35.169619Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/baton-10-project-configurator-verdict`
- HEAD: `ce6e0a49313a949e50e168e1796e85bf8d5d0d9c`
- Synopsis: Project Configurator evaluation receipts were strengthened against contaminated or mixed inspection traces and incomplete verdict evidence.
- Related work on main: Main history includes Project Configurator verdict-integrity and runtime-bridge work in the same judge/supervisor/scenario/runner files; six branch commits remain non-equivalent (git cherry: 1 minus, 6 plus).
- Confidence: High

### 26. codex/baton-8-canonical-checklists-verifier

- Original v2 position: 85
- Created: 2026-07-20T01:26:57.414795Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/baton-8-canonical-checklists-verifier`
- HEAD: `276ce9c0efd583bda9505e3823f59cbfd8e12271`
- Synopsis: Corrects offline staging and strict receipt-schema handling in the agent-test runner. The exact patch is absent, while current main has substantial subsequent runner receipt and verification changes.
- Related work on main: Branch 276ce9c0 changes evals/agent-tests/runner.py and test_runner.py; cherry marks '+'; main includes 6133d116 and 86cf8825 in those runner/test paths.
- Confidence: Medium

### 27. codex/baton-9-one-minute-liveness-addendum

- Original v2 position: 87
- Created: 2026-07-20T01:37:16.846360Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/baton-9-one-minute-liveness-addendum`
- HEAD: `3a5f1095977ff14f15190f4164c5b8f1b55af11a`
- Synopsis: Adds one-minute baton liveness checks and scheduler baton routing definitions. The four branch commits remain unique, while main contains adjacent backlog-dispatcher and watchdog scheduling work.
- Related work on main: HEAD 3a5f1095; merge-base 353273d2; 2248/4 ahead-behind; git cherry reports '+' for all four commits; main history for the changed coordination artifacts includes dispatcher and watchdog wakeup changes.
- Confidence: High

### 28. codex/baton-3-current-main-integration-prep

- Original v2 position: 90
- Created: 2026-07-20T01:44:46.813310Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/baton-3-current-main-integration-prep`
- HEAD: `507cde80e1f4ca41181d105d070387de29b34b98`
- Synopsis: Prepares an agent-skill lifecycle current-main integration candidate with generated explorer assets and lifecycle documentation. It adds the explorer UI/script, support-checklist logic, and focused tests for explorer, bundle, coverage, and lifecycle documentation.
- Related work on main: HEAD 507cde80; merge-base 08bbfa04; main...HEAD counts 2241 behind / 1 ahead; one commit changes 13 design, README, generator, and test files (6036 insertions).
- Confidence: High

### 29. codex/baton-7-wiki-ingester-prerequisite

- Original v2 position: 91
- Created: 2026-07-20T01:55:55.734344Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/baton-7-wiki-ingester-prerequisite`
- HEAD: `aa3046c93d3a5505d84b707d538fc117381e22b3`
- Synopsis: Assembles an executable Wiki Ingester prerequisite harness and contract tests. The harness exercises ingestion behavior and validates the agent contract.
- Related work on main: Current main includes both wiki-ingester files and a long sequence of Wiki Ingester contract/reconciliation commits, but their current blobs differ from aa3046c9 and no exact patch-equivalent commit is present.
- Confidence: High

### 30. codex/baton-10-judge-catalog

- Original v2 position: 94
- Created: 2026-07-20T02:10:50.456573Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/baton-10-judge-catalog`
- HEAD: `c5a50e47f1d6d697e1cc2efc4ccbf96b2547879d`
- Synopsis: Dev Orchestrator dependency-routing judge checks were required to come from the critical deterministic-check catalog.
- Related work on main: The branch changes the orchestrator fixture test and judges catalog, and main has adjacent orchestrator deterministic-gate/catalog integration, but this commit is unique (git cherry: 1 plus).
- Confidence: Medium

### 31. codex/baton-9-current-main-reconcile

- Original v2 position: 97
- Created: 2026-07-20T02:17:18.090237Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/baton-9-current-main-reconcile`
- HEAD: `30d7d1e84e758330d786b4aee233100584b0c0ab`
- Synopsis: Reconciles scheduler baton liveness in the Codex coordination skill. The branch commit remains unique, while main contains adjacent scheduler, dispatcher, and watchdog changes.
- Related work on main: HEAD 30d7d1e8; merge-base 5514063b; 2239/1 ahead-behind; git cherry reports '+'; main history for the changed skill and generated definition includes dispatcher and watchdog updates.
- Confidence: High

### 32. codex/baton-2-runner-receipts-timeout

- Original v2 position: 99
- Created: 2026-07-20T02:20:10.303478Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/baton-2-runner-receipts-timeout`
- HEAD: `999fcd9da4adbea7ba67e1dc6d3fba0b3f17a9f0`
- Synopsis: Preservation of duplicate runner receipts and timeout handling.
- Related work on main: main has the evolved runner receipt/audit and timeout machinery in evals/agent-tests/runner.py and test_runner.py, but the branch's duplicate-call-ID audit implementation is no longer present as the same function.
- Confidence: Medium

### 33. codex/baton-10-judge-catalog-current-main

- Original v2 position: 100
- Created: 2026-07-20T02:33:27.323957Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/baton-10-judge-catalog-current-main`
- HEAD: `ccf29acdf83ee812b93b2b18fe34c12be335dc96`
- Synopsis: Adds a deterministic judge-catalog entry for replaying dependency-routing checks. The isolated candidate consists solely of the corresponding evals/judges.yaml change.
- Related work on main: HEAD ccf29acd; merge-base 5b02b9e6; main...HEAD counts 2234 behind / 1 ahead; one commit adds 16 lines to evals/judges.yaml.
- Confidence: High

### 34. codex/baton-2-runner-current-main-prep

- Original v2 position: 101
- Created: 2026-07-20T02:34:23.902977Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/baton-2-runner-current-main-prep`
- HEAD: `45604ced9da9005cef80ac624f4a51562cd9d50b`
- Synopsis: Prepares the agent-suite runner for current-main integration and adds broad runner regression coverage. It stages dependency and coordinator-schema behavior for integration.
- Related work on main: Current main has the same evals/agent-tests/runner.py and test_runner.py integration surface with later runner fixes, but 45604ced is not patch-equivalent to the current blobs.
- Confidence: High

### 35. codex/baton-2-project-configurator-current-main-2

- Original v2 position: 104
- Created: 2026-07-20T02:51:30.176881Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/baton-2-project-configurator-current-main-2`
- HEAD: `975a498d82f5e4e4e1e560b62e9120802524342c`
- Synopsis: Project Configurator current-main candidate handling rejected unpaired reads and completed Codex skill activation bookkeeping.
- Related work on main: Main history contains the same Project Configurator receipt/verdict and activation areas, but all three branch commits remain unique (git cherry: 3 plus); one branch file is a moved backlog record.
- Confidence: High

### 36. codex/hibernate-panache-metadata-dependency-repair

- Original v2 position: 105
- Created: 2026-07-20T03:01:24.662819Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/hibernate-panache-metadata-dependency-repair`
- HEAD: `e0e0d50d910a36fa333b4a792c6a85dec7ae28a9`
- Synopsis: Splits Hibernate ORM Panache guidance from Quarkus persistence and aligns metadata and references with the narrowed scope. Current main contains later completion of that same skill split, but not these exact commits.
- Related work on main: Branch e0e0d50d has three unique commits adding skills/hibernate-orm-panache and editing Quarkus persistence; main history includes 7840fb3e and ac0ddc09 completing the split.
- Confidence: High

### 37. codex/future-ideas-correction-1-current-main-20260722

- Original v2 position: 110
- Created: 2026-07-22T16:17:47.796231Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/future-ideas-correction-1-current-main-20260722`
- HEAD: `e3b605bf6e285833ea3b51ed3f3a71217bf7d2eb`
- Synopsis: Corrects the Future Ideas workflow so lightweight ideas are file-provider records outside ordinary work-item lifecycle, capacity, and dispatch counts. It adds explicit capture/list/validation/promotion rules, reciprocal provenance fixtures, report opt-in handling, and regenerated steward contracts/adapters.
- Related work on main: HEAD e3b605bf; merge-base 0ac3b572; main...HEAD counts 1971 behind / 1 ahead; one commit spans 24 role/skill/report/evaluation/generated files (967-line net patch).
- Confidence: High

### 38. codex/future-ideas-correction-2-current-main-20260722

- Original v2 position: 111
- Created: 2026-07-22T16:47:45.888313Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/future-ideas-correction-2-current-main-20260722`
- HEAD: `abbc76d03d3fdb8675de561c91342228cd22ea8a`
- Synopsis: Adds a file-backed Future Ideas workflow and updates the steward role, generated adapters, reporting script, skills, and evaluation fixtures. It separates Future Ideas records from ordinary backlog handling.
- Related work on main: Current main already contains Future Ideas workflow and projection commits across the steward role, work-item contracts, report script, and evaluations, but abbc76d0 remains a distinct non-equivalent implementation.
- Confidence: High

### 39. codex/decouple-dev-orchestrator-eval-correction2-019f96ce

- Original v2 position: 113
- Created: 2026-07-25T02:12:54.277992Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/decouple-dev-orchestrator-eval-correction2-019f96ce`
- HEAD: `2be3274a869355a9078d81b918700909006db652`
- Synopsis: Orchestrator evaluation companion change to use real claims; current main evolved the same dependency-routing fixture to explicit none/resource-claim cases rather than retaining this patch.
- Related work on main: Current main's dependency-routing fixture and tests are maintained through event-driven claim-contract commits, but fixture-contract.yaml now declares selected none/resource-claim cases and does not contain the branch's real-claim assertions verbatim.
- Confidence: Medium

### 40. codex/durable-defect-creation-coder-019f96cf

- Original v2 position: 114
- Created: 2026-07-25T02:40:44.703052Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/durable-defect-creation-coder-019f96cf`
- HEAD: `503de4bc4cfd28155f6f4e2c020581889a24687e`
- Synopsis: Durable confirmed-defect recording and terminal-closure ordering were enforced for Dev Orchestrator.
- Related work on main: Main contains related orchestrator role and generated-adapter changes; two branch commits are patch-equivalent and two are unique (git cherry: 2 minus, 2 plus), so the complete branch work is not present.
- Confidence: High

### 41. codex/architecture-assisted-unblocking

- Original v2 position: 117
- Created: 2026-07-25T03:06:24.797670Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/architecture-assisted-unblocking-019f973a`
- HEAD: `6b329e8626316a33656346a296db4d9acee919f3`
- Synopsis: Adds architecture-assisted unblocking behavior to the backlog coordinator and regenerates related projections. The branch commit remains unique, while main contains adjacent coordinator dispatch and recovery work.
- Related work on main: HEAD 6b329e86; merge-base 0ce29d03; 1801/1 ahead-behind; git cherry reports '+'; main history for coordinator role and generated projections includes caller-owned dispatch and recovery updates.
- Confidence: High

### 42. codex/campaign-candidate-integration-correction1-019f96cf

- Original v2 position: 120
- Created: 2026-07-25T03:30:42.347779Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/campaign-candidate-integration-correction1-019f96cf`
- HEAD: `21737be5b9c804b65c18b388aeff514ae881eeb3`
- Synopsis: Refreshes generated campaign-finalizer contracts after accepted lifecycle source changes. It updates coordinator/orchestrator roles and all supported adapters, adds campaign-candidate integration tests, and binds bundle tests to generated lifecycle output.
- Related work on main: HEAD 21737be5; merge-base dfbd1542; main...HEAD counts 1791 behind / 3 ahead; three commits modify generated role/skill adapters and add scripts/test_campaign_candidate_integration.py (approximately 1,100 lines changed).
- Confidence: High

### 43. codex/campaign-candidate-integration-correction2-019f96cf

- Original v2 position: 121
- Created: 2026-07-25T04:25:54.930666Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/campaign-candidate-integration-correction2-019f96cf`
- HEAD: `6ab5976a3fe74c6bc9b0ab8e4faa80e4471c8f2f`
- Synopsis: Corrects the campaign finalizer transaction model and refreshes coordinator/orchestrator generated contracts. It adds a dedicated campaign-candidate integration test suite and lifecycle wording fixes.
- Related work on main: Current main contains the affected coordinator/orchestrator, generated-adapter, lifecycle, and work-item skill surfaces, but the campaign integration test and 6ab5976a transaction-model patch are not present equivalently.
- Confidence: Medium

### 44. codex/uar-examples-current-main-recovery

- Original v2 position: 123
- Created: 2026-07-26T07:29:14.244090Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/uar-examples-current-main-recovery`
- HEAD: `aec92b112e4730d2ffe309d322a52f4a079043dd`
- Synopsis: User Action envelope integer, normalization, and state-invariant hardening; current main retains generic User Action routing but no matching envelope contract implementation was found.
- Related work on main: Current main's Dev Orchestrator role still defines User Action routing and lifecycle handling, but searches found no 9007199254740991, payload_digest, or recorded-not-presented envelope contract in the current skill tree; the specific invariant patch is absent.
- Confidence: Medium

### 45. codex/structured-commit-recovery-20260726

- Original v2 position: 124
- Created: 2026-07-26T07:38:49.533780Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/structured-commit-recovery-coder`
- HEAD: `13277e498868e7e2e6f2b9bb40159982112bfd73`
- Synopsis: Dev Orchestrator dependency-routing evaluations were aligned with disposition-aware Commit and provider evidence ordering.
- Related work on main: Main has adjacent orchestrator Commit/provider-routing integrations in the same evaluation fixtures and runner, but all three branch commits remain unique (git cherry: 3 plus).
- Confidence: High

### 46. codex/decouple-orchestrator-current-main-correction-019f96ce

- Original v2 position: 125
- Created: 2026-07-26T09:37:25.639051Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/decouple-orchestrator-current-main-correction-019f96ce`
- HEAD: `06f4c34b8e438833086359c682aa4be6063889b1`
- Synopsis: Binds orchestrator claim-audit evidence to staged helper authority, runtime rollouts, and adapter results. Current main has related orchestrator claim-audit remediation, but none of these three exact patches.
- Related work on main: Branch 06f4c34b has three unique commits; main history includes fb7ee1f5 Close orchestrator eval claim audit gaps and adjacent resource-claim corrections.
- Confidence: High

### 47. codex/establish-ste-technical-documentation-standard

- Original v2 position: 127
- Created: 2026-07-28T16:32:09.119303Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/establish-ste-technical-documentation-standard`
- HEAD: `a4165c21f464e0cf74d72c6f81b7a64d49c90f62`
- Synopsis: Establishes the STE technical-documentation standard and updates roles, adapters, generated projections, and verification coverage. The five branch commits remain unique, while main contains adjacent terminology, documentation, and generated-definition work.
- Related work on main: HEAD a4165c21; merge-base 6affa81c; 1439/5 ahead-behind; git cherry reports '+' for all five commits; main history for changed files includes STE, documentation-methodology, and generated-definition updates.
- Confidence: High

### 48. codex/eliminate-standalone-definition-approval-records-integration-019faeef

- Original v2 position: 130
- Created: 2026-07-29T18:53:38.442552Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/eliminate-standalone-definition-approval-records-integration-019faeef`
- HEAD: `7cca88fee05db053e452729fcc094cc8309623ed`
- Synopsis: Integrates accepted source changes to eliminate standalone definition-approval records while preserving current-main lifecycle semantics. It removes the approval-record files, regenerates skill-definition output, and updates configuration, rendering, and technology-detection tests.
- Related work on main: HEAD 7cca88fe; merge-base d855b530; main...HEAD counts 1147 behind / 1 ahead; one commit removes 100+ approval-record files and updates AGENTS.md, PROJECT.yaml, render/tests, and coordination skills.
- Confidence: High

### 49. codex/align-orchestrated-development-lifecycle-design-system-019ff2f9

- Original v2 position: 134
- Created: 2026-08-11T22:38:18.295790Z
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/align-orchestrated-lifecycle-work-019ff2f9`
- HEAD: `ce7002bf2794c62cdbd7ebf58ff217aeb5e55935`
- Synopsis: The orchestrated-development lifecycle documentation was aligned to the design system, refreshed, and made keyboard-scrollable.
- Related work on main: Main contains nearby lifecycle/design-system documentation refreshes and generated artifacts, while all four branch commits are unique (git cherry: 4 plus); only three changed paths overlap the current main delta.
- Confidence: High
