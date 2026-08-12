# Related-worktree mergeability review

Ten Luna/medium reviewers reassessed the 49 worktrees with related work against current main. Each reviewer inspected branch history and diffs and used a non-mutating merge or applicability analysis.

- Current-main review baseline: `24ddc738b74b75fe6f26fa0a1f30cc78be018821`
- Merge as-is candidates: 6
- No merge needed because the work is already represented on main: 7
- Create or reuse a work item: 36

`MERGE_AS_IS` means the branch is suitable for deliberate integration after the ordinary gate. `NO_MERGE_NEEDED` means the work is already represented and the branch should not be replayed. `CREATE_WORK_ITEM` means direct merging is unsafe or semantically ambiguous because current main has materially diverged.

## Merge as-is candidates

### 1. codex/enforce-documentation-template-conformance-b948-correction3

- Original v2 position: 61
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/enforce-documentation-template-conformance-b948-correction3`
- HEAD: `6fd28466768643c05d1332a101df994089e2b3cb`
- Synopsis: Refines the documentation-template parser across multiple corrections, especially container boundaries and context grammar. It expands fixture validation and regression tests.
- Assessment: The candidate remains applicable as-is. Its affected documentation-writer fixture, validator, scenario, contract, and fixture tests have no main-side changes after the branch base, and the merge is conflict-free.
- Applicability evidence: git merge-base is 4ef3ec159c1d8d4c438b635e868d3a72e68ee774; main has no diff on the five affected paths after that base; git merge-tree reports no conflicts; git diff --check is clean; the focused documentation-writer fixture suite passes 36 tests.
- Main-overlap risk: Low
- Confidence: High
>APPROVED

### 2. codex/runnable-type-unblock-019f77f4

- Original v2 position: 74
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/runnable-type-unblock-019f77f4`
- HEAD: `eacd47c2d241ee7abe1834b5309d2de970c67e9d`
- Synopsis: Backlog report dependency parsing preserves qualified Markdown links as manual prerequisites.
- Assessment: Although current main has related changes in the same two report files, the candidate is a distinct commit and the three-way merge is clean. No main-drift reconciliation is required before normal integration review.
- Applicability evidence: ['main=c335db58b5fdb551277af78963f0ae69d428c89a; candidate=eacd47c2d241ee7abe1834b5309d2de970c67e9d', "merge-base=353273d2806b7109033ec3954e7a7394126d4db5; main...candidate=2252/1; git cherry reports candidate as '+'", 'candidate changes scripts/generate-backlog-report.py and scripts/test_generate_backlog_report.py; both overlap current-main changes', 'git merge-tree main candidate exits 0 and produces a merged tree']
- Main-overlap risk: Medium
- Confidence: High
>APPROVED
>
### 3. codex/verify-offline-staging-482f85a

- Original v2 position: 77
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/verify-offline-staging-482f85a`
- HEAD: `482f85afb3f301319392c0e02c51d969d706d056`
- Synopsis: Stages offline dependency behavior in the agent-test runner and adds regression tests. The branch commit remains unique, while main contains adjacent runner lifecycle-receipt and claim-coordination changes.
- Assessment: The offline dependency fallback is still absent from current main and applies cleanly without overlapping current runner hardening. The intended behavior remains narrowly scoped and its focused regression tests are preserved.
- Applicability evidence: HEAD 482f85af, merge-base 353273d2, and git cherry main HEAD show one unique commit. git merge-tree --write-tree main HEAD succeeds with no conflicts; the resulting tree differs from main only in evals/agent-tests/runner.py and evals/agent-tests/test_runner.py, matching the branch patch (50 runner lines and 113 test lines). Current main's offline staging function still lacks canonical-primary-worktree fallback.
- Main-overlap risk: Low
- Confidence: High
>QUESTION: What is the "offline dependency behavior" and why is it staged?

**Answer:** The evaluation runner creates a disposable workspace before executing a scenario. JavaScript dependencies such as `node_modules` are ignored by Git, so a linked worktree may not contain them and an offline run cannot reinstall them. This branch makes the runner check the selected worktree first and, when the dependencies are absent, copy them from the repository's canonical primary worktree into the disposable evaluation workspace. It still validates the selected worktree's tracked lockfile, the installed TypeScript version, directory containment, and symlink safety. Here, “staged” means copied into the disposable evaluation workspace; it does not mean `git add`.

**Recommendation:** This behavior is useful for running evaluations offline from linked worktrees. Preserve the later item 4 branch instead because it contains this behavior plus stricter safety and schema checks.
>AGREED THEREFORE DISCARD THIS ITEM

### 4. codex/runner-offline-schema-correction-019f77f4

- Original v2 position: 79
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/runner-offline-schema-correction-019f77f4`
- HEAD: `276ce9c0efd583bda9505e3823f59cbfd8e12271`
- Synopsis: Offline dependency staging fallback and strict receipt/schema corrections.
- Assessment: The branch supplies a focused offline dependency staging fallback and strict schema regression checks. Its two changed files merge cleanly into main under the non-mutating merge-tree check, and main still has the corresponding staging function and coordinator schema that the patch extends.
- Applicability evidence: git diff main...branch changes only evals/agent-tests/runner.py and evals/agent-tests/test_runner.py (198 insertions, 7 deletions); git merge-tree main branch reports no conflicts; current main contains _stage_offline_project_dependencies and the handoffReceipts coordinator schema, while the branch adds canonical-primary-worktree fallback, symlink safety, lock evidence, and strict-object tests.
- Main-overlap risk: Low
- Confidence: High
>QUESTION: What is the "offline dependency behavior" and why is it staged? Is this related to item 3?

**Answer:** Yes. This is the same line of work as item 3 and is its stricter successor. It retains primary-worktree fallback, selected-lockfile validation, version checking, diagnostics, and escaping-symlink rejection. It additionally rejects absolute symlinks even when they currently resolve inside the dependency tree, preserves safe relative internal symlinks, validates strict coordinator-result object schemas, and adds the missing `handoffReceipts` required-field declaration.

**Recommendation:** Merge item 4 after the normal integration gate and discard item 3 as superseded.
>AGREED MERGE THIS ITEM

### 5. codex/baton-10-project-configurator-verdict

- Original v2 position: 84
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/baton-10-project-configurator-verdict`
- HEAD: `ce6e0a49313a949e50e168e1796e85bf8d5d0d9c`
- Synopsis: Project Configurator evaluation receipts were strengthened against contaminated or mixed inspection traces and incomplete verdict evidence.
- Assessment: The candidate remains applicable as-is. Project Configurator judge, supervisor, fixtures, scenario, runner, and tests have no main-side changes after the branch base, and the candidate merges without conflicts.
- Applicability evidence: git merge-base is 901a21169abd5ad5f3f06cec4115219f935bd465; main has no diff on the affected Project Configurator and runner paths after that base; git merge-tree reports no conflicts; git diff --check is clean; the focused Project Configurator fixture suite passes 16 tests.
- Main-overlap risk: Low
- Confidence: High
  >APPROVED

### 6. codex/structured-commit-recovery-20260726

- Original v2 position: 124
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/structured-commit-recovery-coder`
- HEAD: `13277e498868e7e2e6f2b9bb40159982112bfd73`
- Synopsis: Dev Orchestrator dependency-routing evaluations were aligned with disposition-aware Commit and provider evidence ordering.
- Assessment: The candidate remains applicable as-is. Its Dev Orchestrator dependency-routing files have no main-side changes after the branch base, and the merge is conflict-free. Focused tests for the new disposition and provider-order behavior pass.
- Applicability evidence: git merge-base is e3d3fac8fb721729de4c395ac87f3b2c95d53eb5; main has no diff on the affected Dev Orchestrator and runner paths after that base; git merge-tree reports no conflicts; git diff --check is clean; the focused dependency-routing test selection passes 4 tests with 29 deselected.
- Main-overlap risk: Low
- Confidence: High

>QUESTION: Find out more specifically what these changes are 

**Answer:** This is a large three-commit Dev Orchestrator evaluation expansion, not a narrow recovery patch. It verifies that the configured Commit method runs only after pre-Commit verification and that `READY`, `AWAITING_REVIEW`, and `BLOCKED` lead to different valid dependency and persistence sequences. It checks direct-main delivery using configured branch, reachability, mapping, and remote evidence; feature-branch delivery using publication, checks, approvals, merge state, final commit, and provider mapping; exact provider Git blobs and YAML-frontmatter status; active-versus-archive paths; and the required order of outer verification and provider updates. It rejects manufactured, incomplete, selector-inconsistent, or improperly ordered evidence. The branch changes ten heavily evolved runner, fixture, Judge, supervisor, contract, and test files and adds about 3,700 lines.

**Recommendation:** Do not merge this branch directly. Create a fresh Commit-disposition audit work item to identify which checks remain absent from current main and port only confirmed gaps.
> DISCARD THIS ITEM - THINKING HAS EVOLVED
> 
## No merge needed

### 1. codex/verify-mysql-source-858062cc

- Original v2 position: 40
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/verify-mysql-source-858062cc`
- HEAD: `858062cc149d7dcb81d14980bfa791423057b25b`
- Synopsis: Adds a MySQL/InnoDB technology skill and detection registry, then tightens source-based activation tests. Detection requires pertinent source plus owning dependency or configuration evidence and avoids documentation, sibling-scope, and sample contamination.
- Assessment: Current main already contains the MySQL skill and the tightened source-based activation contract. The candidate's detection restrictions, documentation/sample exclusions, sibling-scope isolation, and InnoDB guidance are superseded by the accepted main implementation; do not replay the stale branch.
- Applicability evidence: Candidate 858062cc has the same Tighten MySQL detection evidence change as main commit 65c8c2e7. Current main contains skills/mysql/SKILL.md, detection.yaml, and the corresponding test cases (including configuration removal, documentation/sample exclusion, root-scope isolation, and sibling-module non-contamination). A read-only merge-tree reports add/add/content conflicts because those paths have since advanced, but the behavior is already present.
- Main-overlap risk: High
- Confidence: High

### 2. codex/reporting-terminal-uniqueness-verify

- Original v2 position: 44
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/reporting-terminal-uniqueness-verify`
- HEAD: `fd01292f4bdd4d0579f00faeb6c2d4eecf1b05d1`
- Synopsis: Parallel agent reporting gained durable evidence and unique Judge terminal-response diagnostics.
- Assessment: The branch's seven reporting commits are superseded by the accepted reporting history on main. Main contains the same durable Judge provenance, unique terminal-response validation, and malformed-input diagnostic retention, with later hardening and integration changes.
- Applicability evidence: ['main evals/agent-tests/suite_reporting.py contains _judge_rollout_binding_error and exactly-one eligible terminal-response validation.', 'main history contains 6fe1a821 (Reject duplicate Judge terminal responses), a66cc51e (Bound malformed reporting metadata), and 90c937a4 (Prepare accepted parallel reporting integration).', "The branch's only cherry-unique commits, 4941935c and fd01292f, modify the same reporting files and their behavior is present in the current main tree."]
- Main-overlap risk: High
- Confidence: High

### 3. codex/add-quartz-technology-skill-source-correction-1

- Original v2 position: 50
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/add-quartz-technology-skill-source-correction-1`
- HEAD: `9c726cfab21e69989a9e624736a42f72965eb8ca`
- Synopsis: Adds Quartz Scheduler technology guidance, metadata, and Java dependency detection. The skill covers job identity, misfires, concurrency, persistence, clustering, recovery, lifecycle, and verification, with security/testing routing.
- Assessment: The candidate is already represented on current main. Its merge is clean and produces the exact current-main tree, and all three Quartz source and metadata files are byte-identical on main.
- Applicability evidence: Candidate 9c726cfab21e69989a9e624736a42f72965eb8ca has merge-base e040695e8d91f9dc0fe1554e3ddf66371ae61b92 and two unique Quartz commits. git merge-tree --write-tree main candidate succeeds, and its tree d32d094c263db379ecdd3ea1193e39848951fca1 equals main's tree. skills/quartz/SKILL.md, skills/quartz/agents/openai.yaml, and skills/quartz/detection.yaml resolve to identical blobs on both refs.
- Main-overlap risk: Low
- Confidence: High

### 4. codex/enforce-documentation-template-conformance-0483-correction2

- Original v2 position: 60
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/enforce-documentation-template-conformance-0483-correction2`
- HEAD: `b9483a3997c720352edcfa2e98e87f894ae34bcc`
- Synopsis: Hardens the dev-documentation-writer template-conformance fixture and parser across three correction commits. It adds context-aware heading/readiness parsing, command inventory and path resolution, contradiction checks, and updated deterministic gates.
- Assessment: The context-aware documentation-template parser and its deterministic regression coverage are already present in current main, with later additions on the same validator and fixture surfaces. The stale candidate should not be replayed.
- Applicability evidence: Candidate b9483a39 changes five documentation-writer fixture/parser files. Current main has the same parser symbols for hidden-context heading parsing, readiness validation, command inventory, path resolution, and contradiction checks, plus the candidate's corresponding test cases and additional hardening. Merge-tree reports content conflicts in the validator and tests, confirming overlap rather than a missing implementation.
- Main-overlap risk: High
- Confidence: High

### 5. codex/runnable-type-browser-verify-00724e3-resume

- Original v2 position: 65
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/runnable-type-browser-verify-00724e3-resume`
- HEAD: `00724e3b499fe44a9d24e081519d0c1e7d59bb21`
- Synopsis: Preserves manually declared backlog dependencies in runnable-type reporting and adds focused tests. The exact patch is absent, but current main has continued related backlog-report generator work.
- Assessment: The branch preserves compact embedded Markdown dependency declarations. Main already contains the equivalent guard and the expanded qualified-link/manual-prerequisite test coverage, so the branch adds no missing behavior.
- Applicability evidence: ['main scripts/generate-backlog-report.py checks DEPENDENCY_LINK_PATTERN before normalizing compact dependency text.', 'main scripts/test_generate_backlog_report.py contains the equivalent embedded-link, punctuation, query/fragment, and path-escape cases (including tests beginning at the current embedded-link coverage).', 'The branch has one cherry-unique commit, 00724e3b, and merge-tree reports overlap in both scripts/generate-backlog-report.py and its tests.']
- Main-overlap risk: High
- Confidence: High

### 6. codex/hibernate-panache-metadata-dependency-repair

- Original v2 position: 105
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/hibernate-panache-metadata-dependency-repair`
- HEAD: `e0e0d50d910a36fa333b4a792c6a85dec7ae28a9`
- Synopsis: Splits Hibernate ORM Panache guidance from Quarkus persistence and aligns metadata and references with the narrowed scope. Current main contains later completion of that same skill split, but not these exact commits.
- Assessment: The Hibernate ORM Panache split is already finalized on main. The affected skill, metadata, Quarkus persistence guidance, and review checklist have the same tree content as the branch.
- Applicability evidence: ['main history contains 7840fb3e (Finalize Hibernate ORM Panache skill split).', 'git diff between branch e0e0d50d and main is empty for skills/hibernate-orm-panache and skills/quarkus-persistence.', 'Read-only merge-tree succeeds with no conflict for the affected paths.']
- Main-overlap risk: Low
- Confidence: High

### 7. codex/future-ideas-correction-1-current-main-20260722

- Original v2 position: 110
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/future-ideas-correction-1-current-main-20260722`
- HEAD: `e3b605bf6e285833ea3b51ed3f3a71217bf7d2eb`
- Synopsis: Corrects the Future Ideas workflow so lightweight ideas are file-provider records outside ordinary work-item lifecycle, capacity, and dispatch counts. It adds explicit capture/list/validation/promotion rules, reciprocal provenance fixtures, report opt-in handling, and regenerated steward contracts/adapters.
- Assessment: Do not merge the preserved branch as-is. The Future Ideas correction objective is already represented by the later completed current-main delivery and the dedicated manage-future-ideas boundary. The preserved e3b605bf branch is an earlier blocked current-main correction candidate, not an additional applicable patch, so it needs an audit/close disposition rather than a direct merge.
- Applicability evidence: The branch is one unique commit from an old 0ac3b572 base and conflicts broadly with current main. Current main contains the file-only, non-dispatchable Future Ideas role boundary, explicit opt-in report flag, reciprocal promotion handling, and manage-future-ideas separation. scripts/test_generate_backlog_report.py passed all 63 tests. The branch's own historical record identifies a recurring provider-boundary finding that was resolved by the later delivery chain; no branch bytes should be cherry-picked.
- Main-overlap risk: High
- Confidence: High

## Create or reuse a work item

### 1. codex/align-project-organiser-filename-selection-oracle-correction

- Original v2 position: 31
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/align-project-organiser-filename-selection-oracle-correction`
- HEAD: `41343b0327705504b1f9d50600b031dc5a8dbbed`
- Synopsis: Strengthens the Project Organiser filename-selection regression oracle in bundle-content tests. The added assertions cover required and forbidden selection markers.
- Assessment: The branch changes the same bundle-content test file that current main rewrote extensively. Its assertions and surrounding constants are based on an older bundle contract and require deliberate reconciliation, not an AS-IS merge.
- Applicability evidence: HEAD 41343b03, merge-base ddd3d227, and git cherry main HEAD show one unique commit. git merge-tree main HEAD reports a content conflict in scripts/test_bundle_content.py. The branch patch is 84 insertions and 8 deletions, while current main has materially different skill names, generated-bundle expectations, and test structure in that file.
- Recommended work-item scope: Reconcile the filename-selection oracle against the current scripts/test_bundle_content.py contract, then regenerate or update only the required assertions and tests.
- Main-overlap risk: High
- Confidence: High

### 2. codex/align-project-organiser-filename-selection-oracle-review-correction-1

- Original v2 position: 34
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/align-project-organiser-filename-selection-oracle-review-correction-1`
- HEAD: `517679cec2b1fd0288b0dea803ada3838ef83844`
- Synopsis: Project Organiser bundle-content regression oracles were hardened to recognize structured forbidden markers and path omissions.
- Assessment: The branch adds a two-commit rewrite of scripts/test_bundle_content.py, but main already contains a later, materially evolved forbidden-marker oracle in the same test area. The non-mutating merge-tree check reports a content conflict, so this branch cannot be applied as-is without reconciling the newer oracle contract.
- Applicability evidence: git diff main...branch is limited to scripts/test_bundle_content.py (183 insertions, 8 deletions); git merge-tree main branch reports a content conflict in that file; main contains the later structured_field_prefix, forbidden_success_marker_families, and selected_path_pattern implementation at scripts/test_bundle_content.py around lines 7211-7650.
- Recommended work-item scope: Create a bounded test-oracle review item. Compare the branch's additional marker cases with the current main implementation, retain only demonstrably missing coverage, and update the current oracle contract with focused tests.
- Main-overlap risk: High
- Confidence: High
>AGREE
>
### 3. codex/align-project-organiser-filename-selection-oracle-omission-correction-2

- Original v2 position: 35
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/align-project-organiser-filename-selection-oracle-omission-correction-2`
- HEAD: `6e7eb7460a7e133b6a7d7ce37a262a41eefce019`
- Synopsis: Hardens Project Organiser filename-selection regression oracles and omission sentinels. Current main contains related Project Organiser filename-oracle and completion work, but not these exact three patches.
- Assessment: The candidate cannot merge as-is because it rewrites the same Project Organiser oracle region that current main later expanded. Current main already contains the candidate's forbidden-marker and omission-sentinel behavior, plus broader path-label, punctuation, and continuation coverage.
- Applicability evidence: ['main=c335db58b5fdb551277af78963f0ae69d428c89a; candidate=6e7eb7460a7e133b6a7d7ce37a262a41eefce019', 'merge-base=ddd3d2274471e1fdd08a656bcdc37c0f6b17fc1a; main...candidate=2306/3; git cherry reports the three candidate commits as unique (+)', 'git diff main...candidate changes only scripts/test_bundle_content.py (212 insertions, 8 deletions)', 'git merge-tree main candidate exits with a content conflict in scripts/test_bundle_content.py', 'current main contains forbidden_success_marker_families, selected_path_pattern, sentinel-prefixed paths, and additional omission/continuation cases in the same oracle']
- Recommended work-item scope: Do not port the candidate wholesale. If provenance or residual coverage is required, create a bounded oracle-audit item and retain only cases demonstrably absent from current main.
- Main-overlap risk: High
- Confidence: High
>INCLUDE WITH PREVIOUS ITEM

### 4. codex/align-project-organiser-filename-selection-complete-field-correction-3

- Original v2 position: 41
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/align-project-organiser-filename-selection-complete-field-correction-3`
- HEAD: `971bad6bc8a5ffe4b1aeafc49d49c88e48dc8da3`
- Synopsis: Extends the Project Organiser omission-boundary oracle through several follow-up corrections. It adds sentinel and container-boundary checks to bundle-content validation.
- Assessment: The candidate is not appropriate for direct merge onto current main. Current main has substantially rewritten scripts/test_bundle_content.py and already contains the Project Organiser omission oracle area, including the sentinel and punctuation-boundary cases. The branch adds a stale, non-equivalent test expansion against the pre-rewrite layout. Re-derive any remaining omission-boundary gaps from current main in a fresh work item.
- Applicability evidence: git merge-base is ddd3d2274471e1fdd08a656bcdc37c0f6b17fc1a; main changed scripts/test_bundle_content.py by 13,551 insertions and 3,193 deletions after that base. Current main contains the relevant oracle at lines 7225-7645, including sentinel_prefixed_paths, punctuation_continued_paths, recognized-name continuations, and folded-field checks. Branch test_bundle_content.py passes its 86-test suite, but that does not establish applicability to the current rewritten file.
- Recommended work-item scope: Create a fresh, narrowly scoped Project Organiser oracle work item. Compare current main's omission tests with the intended defect, add only demonstrably missing cases, and run the current focused bundle-content suite.
- Main-overlap risk: High
- Confidence: High
>INCLUDE WITH PREVIOUS ITEM

### 5. codex/deterministic-orchestrator-routing-resume-correction2

- Original v2 position: 45
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/deterministic-orchestrator-routing-resume-correction2`
- HEAD: `6c598418892e784c9ea3a145f4e8307f93d85147`
- Synopsis: Adds deterministic orchestrator dependency-routing fixtures and tightens producer, receipt, and fallback evidence. One final patch is equivalent on main; the other four are distinct but concern the same routing contract.
- Assessment: Do not merge the preserved branch as-is. Main already contains the accepted dependency-routing fixture delivery (48e6d614 and the completed work-item record), while this five-commit branch retains superseded harness content and its final source correction is marked cherry-equivalent only for the fallback patch. The preserved completion record documents unresolved linked-worktree, malformed-receipt, and literal-producer-identity findings that require an explicitly authorized fresh correction, not a blind merge.
- Applicability evidence: git cherry main 6c598418 reports four unique commits and one patch-equivalent commit; git merge-tree reports conflicts in the fixture agents, cases, guidance, contract, scenarios, and tests. Current-main PYTHONPATH=evals/agent-tests python -m unittest discover -s evals/agent-tests/dev-orchestrator -p test_fixtures.py passed 32 tests. Direct validate_fixture.py is intentionally not runnable before the documentation lane creates docs/operator-runbook.md and reports that missing input.
- Recommended work-item scope: Create or reuse one narrowly scoped dependency-routing correction work item for the three preserved findings, starting from current main and the accepted 48e6d614 behavior. Do not create a duplicate of the completed fixture item; link this branch as superseded evidence.
- Main-overlap risk: High
- Confidence: High
>MORE DETAIL NEEDED

**Answer:** This five-commit branch originally introduced the deterministic Dev Orchestrator dependency-routing fixture: a small dependency-status project, source and documentation lanes, independent review and verification lanes, structured handoff receipts, exact producer and commit evidence, claim-release evidence, and runner tests. Most of that fixture is now integrated or superseded on main. Its final correction adds three narrower protections: release-journal directories and files cannot escape fixture Git metadata through symlinks; malformed `handoffReceipts` must be rejected when they are not arrays of objects or have missing/non-string lane names; and missing required receipt lanes must fail explicitly while bounded evidence remains available for diagnosis. Earlier review identified three intentions worth checking on current main: linked-worktree behavior, retained evidence after malformed receipts, and exact producer-identity validation.

**Recommendation:** Do not merge the five-commit branch. Create or reuse one narrowly scoped dependency-routing residual-gap work item to test those three behaviors against current main and implement only confirmed gaps.
### 6. codex/runnable-type-browser-verify-00724e3

- Original v2 position: 47
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/runnable-type-browser-verify-00724e3`
- HEAD: `00724e3b499fe44a9d24e081519d0c1e7d59bb21`
- Synopsis: Preserves manual backlog dependency declarations and adds report-generation tests. The branch commit remains unique, while main contains adjacent backlog-report lifecycle and validation changes.
- Assessment: Current main has advanced changes in both touched backlog-report files, and the three-way merge has a content conflict in the test file. The candidate cannot be merged as-is without reconciling the dependency-preservation behavior with current report semantics.
- Applicability evidence: ['main=c335db58b5fdb551277af78963f0ae69d428c89a; candidate=00724e3b499fe44a9d24e081519d0c1e7d59bb21', "merge-base=c1b551f0874dae1a6bda0b3d306880f634af2d6c; main...candidate=2291/1; git cherry reports candidate as '+'", 'candidate changes scripts/generate-backlog-report.py and scripts/test_generate_backlog_report.py; both overlap current-main changes', 'git merge-tree main candidate exits 1 with a content conflict in scripts/test_generate_backlog_report.py']
- Recommended work-item scope: Create a fresh work item to reapply and retest manual backlog-dependency preservation against current main; retain 00724e3b as historical evidence.
- Main-overlap risk: High
- Confidence: High
>DISCARD ITEM

### 7. codex/enforce-documentation-template-conformance-dev-writer

- Original v2 position: 51
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/enforce-documentation-template-conformance-dev-writer`
- HEAD: `f016c8619d68d535e274b4bba8d6b9c0284a3c07`
- Synopsis: Hardens the documentation-writer module-design template fixture validator. It adds parsing, conformance, and fixture-test coverage for template structure and runnable evidence.
- Assessment: The candidate is not safe to merge as-is. Current main contains later documentation-validator corrections on the same files, and a read-only three-way merge reports content conflicts in validate_fixture.py and test_fixtures.py. The branch has one non-equivalent commit relative to main, so its intended parser and runnable-evidence behavior must be reconciled rather than cherry-picked.
- Applicability evidence: git merge-base is 4ef3ec159c1d8d4c438b635e868d3a72e68ee774; git rev-list --left-right --count main...branch is 2262/1; git cherry main branch reports f016c861 as unique; git merge-tree --write-tree main branch reports conflicts in evals/agent-tests/dev-documentation-writer/fixtures/module-design-template-conformance/validate_fixture.py and evals/agent-tests/dev-documentation-writer/test_fixtures.py. Main history has subsequent commits c72b35ff, eaf148d4, c1b551f0, and accepted integration/correction heads touching the same validator surface.
- Recommended work-item scope: Create a narrowly scoped follow-up to audit f016c861's remaining behavioral intent against current main, port only missing conformance/runnable-evidence cases into the current validator, regenerate no unrelated outputs, and run the focused dev-documentation-writer fixture tests.
- Main-overlap risk: High
- Confidence: High
>DISCARD ITEM

### 8. codex/unsupported-review-structured-evaluator-recovery

- Original v2 position: 54
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/unsupported-review-structured-evaluator-recovery`
- HEAD: `08a35a16c1680886610851ea31be18bebe7ec1a6`
- Synopsis: Dev Code Reviewer fixture evaluation was extended to evaluate structured authority, contradiction, and uncertainty semantics.
- Assessment: The structured-evaluator additions are not mergeable AS IS because current main changed both the reviewer fixture evaluator and its fixture tests. The branch also removes existing tests that main still structures differently, so a fresh implementation must preserve current authority and uncertainty coverage.
- Applicability evidence: HEAD 08a35a16, merge-base 32c74af6, and git cherry main HEAD show one unique commit. git merge-tree main HEAD reports add/add conflict for evaluate_synthesis.py and content conflict for test_fixtures.py. Current main contains the authority-boundary fixture inputs byte-for-byte but has different evaluator/test organization; the branch adds 361 lines across three files.
- Recommended work-item scope: Rebase the structured authority, contradiction, and uncertainty evaluator behavior onto current reviewer fixtures and restore or revise the current fixture-boundary tests without dropping main coverage.
- Main-overlap risk: High
- Confidence: High
>DISCARD ITEM

### 9. codex/verify-codex-skill-activation-live

- Original v2 position: 56
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/verify-codex-skill-activation-live`
- HEAD: `f9c94244f991cd2893d7ad29a944eb72633c8929`
- Synopsis: Updates live Codex skill-activation evaluation fixtures and assertions to a newer MCP runtime identity/version.
- Assessment: The branch only changes the old mcp-agent-ops runtime version and digest assertions, while current main has substantially evolved the activation/evaluation catalog and no longer contains the referenced requiredVersion/requiredRuntimeDigest contract at the same location. The non-mutating merge-tree check reports conflicts in both changed files.
- Applicability evidence: git diff main...branch changes evals/cases.yaml and scripts/test_agent_skill_evals.py by four lines total; git merge-tree main branch reports content conflicts in both files; current main has no 0.2.3/0.3.0 requiredVersion or requiredRuntimeDigest entries in those paths, and the repository history records the 0.3.0 activation integration separately.
- Recommended work-item scope: Create a current-main activation-evaluation identity item. Re-establish the runtime identity contract at its present schema location, verify the installed runtime evidence, and update only the current fixtures and assertions.
- Main-overlap risk: High
- Confidence: High
  >DISCARD ITEM

### 10. codex/review-authority-boundary-executable-correction

- Original v2 position: 57
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/review-authority-boundary-executable-correction`
- HEAD: `f4cf12978aed9be10ae7d9bc579f2f44df6c3071`
- Synopsis: Adds executable review-authority-boundary fixtures and evaluation wiring for the code reviewer. The branch commit remains unique, while main contains adjacent code-reviewer suite integration and hardening.
- Assessment: The candidate's authority-boundary scenario is already present in current main, but current main has a stricter staged-workspace, oracle-isolation, evaluator-handoff, and binding-verification contract. The older candidate conflicts with those evolved fixtures and cannot be merged as-is.
- Applicability evidence: ['main=c335db58b5fdb551277af78963f0ae69d428c89a; candidate=f4cf12978aed9be10ae7d9bc579f2f44df6c3071', 'merge-base=32c74af6c8fef1c1681e0b5315c93ac92129c5e7; main...candidate=2261/1; git cherry reports the candidate as unique (+)', 'git diff main...candidate changes 14 reviewer-suite paths, including the fixture, evaluator, scenarios, supervisor/judge instructions, and fixture tests', 'git merge-tree main candidate reports content conflicts in judge.toml, supervisor.toml, scenarios.yaml, suite contract, test_fixtures.py, and scripts/test_bundle_content.py, plus add/add conflicts for fixture files', 'current main history includes ba86db77 (accepted integration candidate), and current scenario/test content adds candidate-oracle isolation, staged roots, evaluation handoff binding, and stronger structured findings']
- Recommended work-item scope: No direct port is indicated. If a missing behavior is identified, create a fresh reviewer-suite item against the current staged/evaluator contract and preserve the candidate only as historical evidence.
- Main-overlap risk: High
- Confidence: High
>DISCARD ITEM
>
### 11. codex/process-backlog-scheduler-correction

- Original v2 position: 73
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/process-backlog-scheduler-correction`
- HEAD: `a734b7fbca75dec87b91f20d891691d047c26f96`
- Synopsis: Scheduler handoff-routing additions to the former Codex work-item coordination skill; current main has the renamed coordination skill and related canonical-task handoff rules, but not the candidate text verbatim.
- Assessment: The branch edits retired skills/codex-workitem-coordination and its generated projection. Current main uses skills/coordinate-codex-tasks, so the scheduler handoff additions cannot be merged as-is. Current main has canonical identity, wake, and archival rules but not the branch's immediate stopped-task handoff ingestion and same-cycle routing requirements.
- Applicability evidence: The branch is one commit ahead of merge-base 353273d2; git merge-tree shows a conflict in the generated catalog and the old skill is removed on the current-main side. A current-main codex task-control contract run passed 16 tests, confirming the existing replacement skill is executable; the branch-specific scheduler wording is absent from skills/coordinate-codex-tasks/SKILL.md. Index 87 contains this commit plus the broader baton series and should be the single scope owner.
- Recommended work-item scope: Fold this entry into one new current-main work item owned by the broader index-87 baton/liveness scope. Port only the still-applicable scheduler rules to coordinate-codex-tasks and regenerate supported projections; do not create a standalone duplicate.
- Main-overlap risk: Medium
- Confidence: High
>DISCARD ITEM

### 12. codex/restore-wiki-ingester-target-boundary-resume

- Original v2 position: 75
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/restore-wiki-ingester-target-boundary-resume`
- HEAD: `1e113a276ca379b521a7bb0537daa3ba1b3ec7d2`
- Synopsis: Builds an executable Wiki Ingester interruption-boundary harness and contract tests. Current main contains subsequent Wiki Ingester interruption completion and reconciliation work, but not these exact patches.
- Assessment: The candidate's Wiki Ingester harness and contract files conflict with newer current-main versions. The branch cannot be applied as-is; its interruption-boundary evidence must be reconciled with the expanded current test contract.
- Applicability evidence: Candidate 1e113a276ca379b521a7bb0537daa3ba1b3ec7d2 has merge-base 353273d2806b7109033ec3954e7a7394126d4db5 and four unique commits. git merge-tree --write-tree main candidate reports add/add conflicts in evals/agent-tests/wiki-ingester/executable_harness.py and test_contract.py. Current main has different blobs for both files and additional Wiki Ingester boundary, neighbor, receipt, and claim-contract tests.
- Recommended work-item scope: Create a Wiki Ingester interruption-contract reconciliation item. Compare the candidate's preserved-target and live interruption assertions with current main, retain any missing evidence, and update the current harness and focused tests without dropping newer coverage.
- Main-overlap risk: High
- Confidence: High

>DISCARD ITEM

### 13. codex/process-backlog-scheduler-baton-refinement

- Original v2 position: 76
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/process-backlog-scheduler-baton-refinement`
- HEAD: `5a17e23f0fb2956ff3c54f3db3327d0b9c59beec`
- Synopsis: Refines Codex work-item coordination around claim-scope batons, parent scheduler audits, wake ownership, and adaptive concurrency.
- Assessment: The candidate cannot merge as-is because it edits the obsolete skills/codex-workitem-coordination/SKILL.md, which main deleted when the coordination skill was renamed, and it conflicts in the generated skill definitions. The claim-scope and scheduler-audit ideas may still be useful, but they require a current-policy review and adaptation to coordinate-work-items/coordinate-codex-tasks.
- Applicability evidence: git merge-base is 353273d2806b7109033ec3954e7a7394126d4db5; git rev-list --left-right --count main...branch is 2252/2; git cherry reports unique commits a734b7fb and 5a17e23f; git merge-tree --write-tree reports a content conflict in design/generated/skill-definitions.js and a modify/delete conflict because main deleted skills/codex-workitem-coordination/SKILL.md. Current main has skills/coordinate-work-items/SKILL.md and skills/coordinate-codex-tasks/SKILL.md instead.
- Recommended work-item scope: Create a follow-up to extract and review only the still-required claim-scope baton, immediate handoff-ingestion, parent scheduler-audit, and adaptive-concurrency requirements against current coordinate-work-items and coordinate-codex-tasks policy; update generated outputs only through the supported generator and run focused coordination contract tests.
- Main-overlap risk: High
- Confidence: Medium
>DISCARD ITEM
>
### 14. codex/preserve-canonical-review-checklists

- Original v2 position: 80
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/preserve-canonical-review-checklists-artifact`
- HEAD: `d7164c2c634433a1988f7dcac4cddac26075974c`
- Synopsis: Adds a canonical checklist contract validator for dev-artifact-reviewer evaluations. It requires generic and applicable specialized checklists to preserve every source question and completion field in order, and binds retained evidence with SHA-256 digests and critical judge gates.
- Assessment: The candidate introduces canonical-checklist validation from an older checklist snapshot, but current main already contains the validator and stronger generated-suite contract. Its test file is an add/add conflict and the candidate's expected functional checklist count is stale, so an AS-IS merge is unsafe and redundant.
- Applicability evidence: ['main=c335db58b5fdb551277af78963f0ae69d428c89a; candidate=d7164c2c634433a1988f7dcac4cddac26075974c', 'merge-base=901a21169abd5ad5f3f06cec4115219f935bd465; main...candidate=2250/1; git cherry reports the candidate as unique (+)', 'git diff main...candidate changes seven artifact-reviewer/catalog paths and adds 528 lines of validator code/tests', 'git merge-tree main candidate reports an add/add conflict for evals/agent-tests/dev-artifact-reviewer/test_checklist_contract.py and auto-merges other touched paths', "current main history includes 2978cb23 (canonical checklist contract preparation), and current main's validator test expects the current functional checklist count (43 rather than the candidate's 25)"]
- Recommended work-item scope: Do not merge the stale snapshot. Create a bounded checklist-contract review item only if current-main coverage has a specific gap; otherwise mark this candidate superseded and retain its commit as evidence.
- Main-overlap risk: High
- Confidence: High
>DISCARD ITEM
>
### 15. codex/restore-wiki-ingester-pre-move-2

- Original v2 position: 83
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/restore-wiki-ingester-pre-move-2`
- HEAD: `85404131f8cafce252e4be837e4dbdacc1058c71`
- Synopsis: Wiki Ingester interruption harness correction retaining the first live failure; current main completed related interruption work but does not contain this test patch verbatim.
- Assessment: Current main contains related Wiki Ingester interruption and restoration behavior, but not the candidate's first-failure evidence-retention assertion and complete bounded evidence selection. The patch cannot be applied as-is to the evolved harness and contract tests.
- Applicability evidence: Candidate 85404131 adds owned-tree digest/result-text/committed-path observation and sequential first-assertion retention helpers across executable_harness.py and test_contract.py. Current main has some digest and gate-preservation fields, but no _retain_evidence/_bounded_evidence/_validate_control_result equivalent; merge-tree reports add/add conflicts in both changed files. Main history includes related interruption commits (including 577627d6), not this complete patch.
- Recommended work-item scope: Create a focused Wiki Ingester interruption-evidence work item. Port only first-failure retention and complete owned-tree/result evidence to the current harness, preserve current interruption contracts, and add focused tests without replaying obsolete fixture scaffolding.
- Main-overlap risk: High
- Confidence: High
>DISCARD ITEM

### 16. codex/baton-8-canonical-checklists-verifier

- Original v2 position: 85
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/baton-8-canonical-checklists-verifier`
- HEAD: `276ce9c0efd583bda9505e3823f59cbfd8e12271`
- Synopsis: Corrects offline staging and strict receipt-schema handling in the agent-test runner. The exact patch is absent, while current main has substantial subsequent runner receipt and verification changes.
- Assessment: The branch contains a distinct offline Node dependency fallback from a linked checkout to the canonical primary worktree, plus absolute-symlink rejection. That behavior is absent from current main. Its coordinator-schema portion is already present on main and should not be recreated.
- Applicability evidence: ['Branch commit 276ce9c0 adds _canonical_primary_worktree, selected-checkout/primary-worktree fallback, absolute-symlink rejection, and focused tests.', 'Current main _stage_offline_project_dependencies only reads repository_root/evals/projects/<case>/node_modules and raises when that directory is absent; no _canonical_primary_worktree or primary-worktree fallback exists.', 'Current main already requires handoffReceipts in the coordinator schema, so that branch change is redundant.', 'Read-only merge-tree succeeds, but the patch still changes the active runner/test implementation and is not an already-integrated behavior.']
- Recommended work-item scope: Create one focused work item to port only canonical-primary-worktree fallback and offline dependency symlink/lock validation into current runner.py, with focused test_runner.py coverage. Exclude the already-present coordinator-schema change.
- Main-overlap risk: High
- Confidence: High
>DISCARD ITEM
>
### 17. codex/baton-9-one-minute-liveness-addendum

- Original v2 position: 87
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/baton-9-one-minute-liveness-addendum`
- HEAD: `3a5f1095977ff14f15190f4164c5b8f1b55af11a`
- Synopsis: Adds one-minute baton liveness checks and scheduler baton routing definitions. The four branch commits remain unique, while main contains adjacent backlog-dispatcher and watchdog scheduling work.
- Assessment: Do not merge the four-commit branch as-is. It modifies the retired codex-workitem-coordination skill, while current main has renamed and substantially rewritten the Codex task-control surface. The branch adds potentially applicable baton/liveness semantics, but those semantics need a fresh translation and review against coordinate-work-items and coordinate-codex-tasks.
- Applicability evidence: git cherry main 3a5f1095 reports all four commits unique; git merge-tree shows conflicts in the generated catalog and old skill path. Current-main scripts/test_codex_task_control.py passed 16 tests. Current coordinate-codex-tasks contains canonical identity, follow-up, Watchdog wake, and archival rules, but no explicit one-minute baton liveness, stopped-handoff age defect, or continuous productive-floor restoration clauses from this branch.
- Recommended work-item scope: Create one fresh current-main work item for semantic porting of the baton/liveness contract, with index 73 folded into the same scope. Require focused coordination-contract tests and supported generated-output refresh; preserve both branches as historical evidence.
- Main-overlap risk: High
- Confidence: High
>DISCARD ITEM
>
### 18. codex/baton-3-current-main-integration-prep

- Original v2 position: 90
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/baton-3-current-main-integration-prep`
- HEAD: `507cde80e1f4ca41181d105d070387de29b34b98`
- Synopsis: Prepares an agent-skill lifecycle current-main integration candidate with generated explorer assets and lifecycle documentation. It adds the explorer UI/script, support-checklist logic, and focused tests for explorer, bundle, coverage, and lifecycle documentation.
- Assessment: The large lifecycle/documentation candidate overlaps ten files changed on current main and has multiple three-way conflicts, including a modify/delete conflict for generated explorer data and an add/add test conflict. It requires deliberate reconciliation rather than an as-is merge.
- Applicability evidence: ['main=c335db58b5fdb551277af78963f0ae69d428c89a; candidate=507cde80e1f4ca41181d105d070387de29b34b98', "merge-base=08bbfa045a1b91e338412304f5926fd328f71166; main...candidate=2245/1; git cherry reports candidate as '+'", 'candidate changes 13 files with 6036 insertions, including README/design/generator/test surfaces; ten changed paths overlap current main', 'git merge-tree main candidate exits 1 with conflicts in README, design pages, generators, tests, plus a modify/delete conflict for design/generated/agent-skill-explorer-data.js']
- Recommended work-item scope: Create a fresh integration work item for the explorer/lifecycle feature, rebase or reimplement against current main, regenerate outputs, and rerun focused documentation and bundle checks.
- Main-overlap risk: High
- Confidence: High
>DISCARD ITEM
>
### 19. codex/baton-7-wiki-ingester-prerequisite

- Original v2 position: 91
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/baton-7-wiki-ingester-prerequisite`
- HEAD: `aa3046c93d3a5505d84b707d538fc117381e22b3`
- Synopsis: Assembles an executable Wiki Ingester prerequisite harness and contract tests. The harness exercises ingestion behavior and validates the agent contract.
- Assessment: The prerequisite Wiki Ingester harness is based on an older contract and conflicts with current-main implementations of the same files. Direct merging would require choosing between competing harness and test definitions.
- Applicability evidence: Candidate aa3046c93d3a5505d84b707d538fc117381e22b3 has merge-base 08bbfa045a1b91e338412304f5926fd328f71166 and one unique commit. git merge-tree --write-tree main candidate reports add/add conflicts in evals/agent-tests/wiki-ingester/executable_harness.py and test_contract.py. Current main contains later Wiki Ingester interruption, neighbor, retained-evidence, and runtime-boundary coverage with different blobs.
- Recommended work-item scope: Create a bounded prerequisite-reconciliation item. Reassess the candidate's executable staging and interruption assertions against current main, port only demonstrably missing cases, and preserve the current target-boundary and live-neighbor tests.
- Main-overlap risk: High
- Confidence: High
>DISCARD ITEM
>
### 20. codex/baton-10-judge-catalog

- Original v2 position: 94
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/baton-10-judge-catalog`
- HEAD: `c5a50e47f1d6d697e1cc2efc4ccbf96b2547879d`
- Synopsis: Dev Orchestrator dependency-routing judge checks were required to come from the critical deterministic-check catalog.
- Assessment: The exact candidate is not mergeable as-is: the read-only three-way merge conflicts in evals/judges.yaml. Main already contains the four intended critical check IDs, with evolved descriptions and broader catalog coverage, while the branch's dedicated fixture assertion is not present in the same form. Reconcile whether that assertion is still a coverage gap before adding anything.
- Applicability evidence: git merge-base is 5514063bb51a56cbd8b667bcf49aa34fca329d06; git rev-list --left-right --count main...branch is 2243/1; git cherry reports c5a50e47 as unique; git merge-tree --write-tree reports a content conflict in evals/judges.yaml but auto-merges evals/agent-tests/dev-orchestrator/test_fixtures.py. Current main evals/judges.yaml already defines one-nested-dependency-at-a-time, committed-handoffs, structured-handoff-receipts, and post-integration-reviews as critical checks, and runner.py centrally validates the deterministic catalog.
- Recommended work-item scope: Create a narrowly scoped verification/follow-up item only if direct dependency-routing coverage is still required: compare the current scenario's deterministicChecks with the current catalog and generic runner assertions, then add one current-main fixture test if a concrete gap remains. Otherwise record this candidate as superseded/no-op without importing its patch.
- Main-overlap risk: High
- Confidence: Medium
>DISCARD ITEM
### 21. codex/baton-9-current-main-reconcile

- Original v2 position: 97
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/baton-9-current-main-reconcile`
- HEAD: `30d7d1e84e758330d786b4aee233100584b0c0ab`
- Synopsis: Reconciles scheduler baton liveness in the Codex coordination skill. The branch commit remains unique, while main contains adjacent scheduler, dispatcher, and watchdog changes.
- Assessment: The branch modifies a coordination skill that current main deleted or replaced and also changes its generated projection. Applying it AS IS would resurrect stale content and conflict with the current coordination model.
- Applicability evidence: HEAD 30d7d1e8, merge-base 5514063b, and git cherry main HEAD show one unique commit. git merge-tree main HEAD reports content conflict in design/generated/skill-definitions.js and modify/delete conflict for skills/codex-workitem-coordination/SKILL.md, which current main deletes. The branch's two-file patch is therefore not applicable to the current source/projection layout.
- Recommended work-item scope: Re-express scheduler baton liveness in the current coordination skill and generation sources, then regenerate projections and add focused tests for the current model.
- Main-overlap risk: High
- Confidence: High
>DISCARD ITEM
### 22. codex/baton-2-runner-receipts-timeout

- Original v2 position: 99
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/baton-2-runner-receipts-timeout`
- HEAD: `999fcd9da4adbea7ba67e1dc6d3fba0b3f17a9f0`
- Synopsis: Preservation of duplicate runner receipts and timeout handling.
- Assessment: The branch combines an older Project Configurator candidate with a duplicate-receipt fix. Main has since substantially evolved the runner and removed or relocated the targeted audit implementation. The non-mutating merge-tree check reports conflicts across the Project Configurator fixtures and the branch's shared runner changes.
- Applicability evidence: git diff main...branch spans nine files and 1,350 changed lines; git merge-tree main branch reports content conflicts in seven files; current main has no pending_calls/duplicate-receipt implementation at the branch's target audit location, indicating that the patch needs architectural revalidation rather than direct application.
- Recommended work-item scope: Create a runner-audit recovery item. Identify the current receipt/audit contract, reproduce the duplicate-call scenario against current main, and implement a narrowly scoped correction with updated fixtures if the defect still exists.
- Main-overlap risk: High
- Confidence: High
>DISCARD ITEM
### 23. codex/baton-10-judge-catalog-current-main

- Original v2 position: 100
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/baton-10-judge-catalog-current-main`
- HEAD: `ccf29acdf83ee812b93b2b18fe34c12be335dc96`
- Synopsis: Adds a deterministic judge-catalog entry for replaying dependency-routing checks. The isolated candidate consists solely of the corresponding evals/judges.yaml change.
- Assessment: The candidate adds four deterministic judge-catalog entries, but current main already contains all four IDs with evolved descriptions. The candidate's single-file patch conflicts with the current catalog and adds no net behavior that can be merged as-is.
- Applicability evidence: ['main=c335db58b5fdb551277af78963f0ae69d428c89a; candidate=ccf29acdf83ee812b93b2b18fe34c12be335dc96', 'merge-base=5b02b9e683bba0193c178ce976bded2b4a194d12; main...candidate=2238/1; git cherry reports the candidate as unique (+)', 'git diff main...candidate changes only evals/judges.yaml (16 added lines)', 'git merge-tree main candidate exits with a content conflict in evals/judges.yaml', 'current main contains one-nested-dependency-at-a-time, committed-handoffs, structured-handoff-receipts, and post-integration-reviews with stronger current-main wording']
- Recommended work-item scope: No implementation port is needed. Create only a reconciliation/audit item if catalog provenance must be recorded; preserve current-main descriptions and do not replace them with the older text.
- Main-overlap risk: High
- Confidence: High
>DISCARD ITEM
### 24. codex/baton-2-runner-current-main-prep

- Original v2 position: 101
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/baton-2-runner-current-main-prep`
- HEAD: `45604ced9da9005cef80ac624f4a51562cd9d50b`
- Synopsis: Prepares the agent-suite runner for current-main integration and adds broad runner regression coverage. It stages dependency and coordinator-schema behavior for integration.
- Assessment: The candidate contains still-missing runner behavior, not only superseded regression coverage. Current main lacks the canonical-primary-worktree offline Node fallback and the Project Configurator exact-read audit added by this branch, so a clean textual merge would conceal a required semantic port.
- Applicability evidence: Candidate 45604ced adds _canonical_primary_worktree, offline dependency fallback/symlink/lock checks, rollout event/read-command auditing, and matching tests. Current main runner.py has no _canonical_primary_worktree or _audit_project_configurator_repository_reads, and current test_runner.py lacks the offline-primary-worktree and exact-read audit tests. Merge-tree happens to succeed, but the runner/test files have extensive later changes and the behavior is not already integrated.
- Recommended work-item scope: Create one bounded runner-integration work item. Reimplement the missing primary-worktree dependency fallback and exact Project Configurator read/audit checks against current main, then add focused runner tests; exclude redundant coordinator-schema coverage already present.
- Main-overlap risk: Medium
- Confidence: High
>DISCARD ITEM
### 25. codex/baton-2-project-configurator-current-main-2

- Original v2 position: 104
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/baton-2-project-configurator-current-main-2`
- HEAD: `975a498d82f5e4e4e1e560b62e9120802524342c`
- Synopsis: Project Configurator current-main candidate handling rejected unpaired reads and completed Codex skill activation bookkeeping.
- Assessment: The candidate cannot be merged safely as-is. It conflicts with current main on the moved completed-backlog record: main records Status: Completed while the branch records Status: Blocked. The branch also overlaps the Project Configurator files changed by index 84, so its intent must be revalidated and rebased rather than applied as a second competing candidate.
- Applicability evidence: git merge-base is 290ca87194be9b6829d992b7fb70aa76dbd5b468; git merge-tree reports an 'added in both' conflict at backlog/completed-backlog/features/verify-codex-skill-activation.md and 'changed in both' conflicts across Project Configurator judge/supervisor/fixture/scenario/contract files. The branch's focused Project Configurator fixture suite passes 16 tests, but the durable backlog status conflict remains unresolved.
- Recommended work-item scope: Create a fresh work item to rebase the desired unpaired-read changes onto current main, resolve the completed-record status from authoritative provider evidence, and reconcile overlap with index 84 before integration.
- Main-overlap risk: High
- Confidence: High
>DISCARD ITEM
### 26. codex/future-ideas-correction-2-current-main-20260722

- Original v2 position: 111
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/future-ideas-correction-2-current-main-20260722`
- HEAD: `abbc76d03d3fdb8675de561c91342228cd22ea8a`
- Synopsis: Adds a file-backed Future Ideas workflow and updates the steward role, generated adapters, reporting script, skills, and evaluation fixtures. It separates Future Ideas records from ordinary backlog handling.
- Assessment: Current main already contains related Future Ideas workflow and projection changes, while this distinct implementation overlaps 23 paths. The three-way merge has broad content and add/add conflicts, so the candidate needs semantic reconciliation.
- Applicability evidence: ['main=c335db58b5fdb551277af78963f0ae69d428c89a; candidate=abbc76d03d3fdb8675de561c91342228cd22ea8a', "merge-base=73e0bdf960488bac78b94eb8ae883947cd79360e; main...candidate=1974/1; git cherry reports candidate as '+'", 'candidate changes 23 paths across the steward role, generated adapters, Future Ideas skills, report generator, and evaluations; all 23 overlap current main', 'git merge-tree main candidate exits 1 with conflicts across README, role/projection/evaluation files, report generator/tests, and related skills']
- Recommended work-item scope: Create a fresh Future Ideas reconciliation work item, preserve abbc76d0 as evidence, and revalidate file-provider-only separation against the current contracts and generated outputs.
- Main-overlap risk: High
- Confidence: High
>DISCARD ITEM
### 27. codex/decouple-dev-orchestrator-eval-correction2-019f96ce

- Original v2 position: 113
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/decouple-dev-orchestrator-eval-correction2-019f96ce`
- HEAD: `2be3274a869355a9078d81b918700909006db652`
- Synopsis: Orchestrator evaluation companion change to use real claims; current main evolved the same dependency-routing fixture to explicit none/resource-claim cases rather than retaining this patch.
- Assessment: The real-claim orchestrator evaluation patch conflicts with current dependency-routing fixtures, runner behavior, and tests. Current main intentionally models explicit none and resource-claim cases, so the branch's real-claim assertions require a fresh applicability decision rather than an as-is merge.
- Applicability evidence: Candidate 2be3274a869355a9078d81b918700909006db652 has merge-base cdf4cd3199d65fceb67dde2a9083d219abcf37df and one unique commit. git merge-tree --write-tree main candidate reports content conflicts in evals/agent-tests/dev-orchestrator/fixtures/dependency-routing/fixture-contract.yaml, evals/agent-tests/dev-orchestrator/test_fixtures.py, and evals/agent-tests/runner.py. The current fixture contract uses explicit none/resource-claim cases instead of the branch's real-claim assertions.
- Recommended work-item scope: Create a dependency-routing evaluation reconciliation item. Decide whether real-claim coverage remains required, then implement it against the current none/resource-claim contract and runner APIs with focused fixture tests.
- Main-overlap risk: High
- Confidence: High
>DISCARD ITEM
### 28. codex/durable-defect-creation-coder-019f96cf

- Original v2 position: 114
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/durable-defect-creation-coder-019f96cf`
- HEAD: `503de4bc4cfd28155f6f4e2c020581889a24687e`
- Synopsis: Durable confirmed-defect recording and terminal-closure ordering were enforced for Dev Orchestrator.
- Assessment: The complete candidate is not safe to merge as-is. The branch's role, generated adapters, manifest, and bundle tests all conflict with current main in a read-only three-way merge. Main does not contain the branch's confirmed-defect recording policy, duplicate reconciliation, provider-none/UNSET blocking, same-delivery correction rule, or corresponding approval-record fixtures; these require deliberate reimplementation on current sources. The branch also includes merge-history noise and older provider/skill topology that must not be replayed.
- Applicability evidence: git merge-base is f58290fac280b58d2ef7aa6a8338b28e5ba5781d; git rev-list --left-right --count main...branch is 1556/8; git cherry reports two equivalent commits (-) and two unique commits (+); git merge-tree --write-tree reports conflicts in agents/roles/dev-activities/dev-orchestrator.role.yaml, design/generated/role-definitions.js, generated/adapters/agent-generation-manifest.json, all four dev-orchestrator adapters, and scripts/test_bundle_content.py. The two approval-record YAML files exist on the branch but not on main. Current main role search shows no equivalent durable-confirmed-defect policy.
- Recommended work-item scope: Create a new focused work item for current-main durable confirmed-defect routing: define confirmation and evidence boundaries, exactly-once provider recording with duplicate reconciliation, provider-none/UNSET blocking, same-delivery correction without a second task, terminal-closure ordering, approval fixtures if still required, source tests, and supported adapter regeneration. Preserve the branch commits as historical evidence only.
- Main-overlap risk: High
- Confidence: High
>DISCARD ITEM
### 29. codex/architecture-assisted-unblocking

- Original v2 position: 117
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/architecture-assisted-unblocking-019f973a`
- HEAD: `6b329e8626316a33656346a296db4d9acee919f3`
- Synopsis: Adds architecture-assisted unblocking behavior to the backlog coordinator and regenerates related projections. The branch commit remains unique, while main contains adjacent coordinator dispatch and recovery work.
- Assessment: The architecture-assisted-unblocking branch is a broad generated bundle from an older coordinator contract. Current main changed the coordinator role, generated adapters, diagrams, and hierarchy sources in overlapping areas, so the branch cannot be accepted AS IS.
- Applicability evidence: HEAD 6b329e86, merge-base 0ce29d03, and git cherry main HEAD show one unique commit. git merge-tree main HEAD reports content conflicts in the coordinator role, multiple generated adapters and design files, plus modify/delete conflicts for generated files removed by current main. The branch touches 13 files and current main has subsequent coordinator dispatch, recovery, and generated-layout changes across those same paths.
- Recommended work-item scope: Reassess architecture-assisted unblocking against the current coordinator role and source-of-truth generation pipeline, then implement and regenerate only the still-required projections with focused contract tests.
- Main-overlap risk: High
- Confidence: High
>DISCARD ITEM
### 30. codex/campaign-candidate-integration-correction1-019f96cf

- Original v2 position: 120
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/campaign-candidate-integration-correction1-019f96cf`
- HEAD: `21737be5b9c804b65c18b388aeff514ae881eeb3`
- Synopsis: Refreshes generated campaign-finalizer contracts after accepted lifecycle source changes. It updates coordinator/orchestrator roles and all supported adapters, adds campaign-candidate integration tests, and binds bundle tests to generated lifecycle output.
- Assessment: This three-commit candidate rewrites generated role/adaptor outputs, lifecycle tests, and workflow skills, but current main has advanced beyond its source set. The non-mutating merge-tree check reports conflicts across nearly every generated and source file, including modify/delete conflicts for skills and tests that main intentionally removed.
- Applicability evidence: git diff main...branch changes 20 files (about 1,190 lines); git merge-tree main branch reports conflicts in README.md, both role sources, generated outputs, lifecycle HTML, and scripts/test_bundle_content.py, plus modify/delete conflicts for scripts/test_codex_workitem_coordination.py, skills/agent-work-merge/SKILL.md, and skills/codex-workitem-coordination/SKILL.md; those latter files are absent on current main.
- Recommended work-item scope: Create a lifecycle-contract reconciliation item. Re-evaluate the accepted source changes against current main, update canonical sources first, regenerate adapters, and add only still-required integration coverage; do not cherry-pick generated outputs directly.
- Main-overlap risk: High
- Confidence: High
>DISCARD ITEM
### 31. codex/campaign-candidate-integration-correction2-019f96cf

- Original v2 position: 121
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/campaign-candidate-integration-correction2-019f96cf`
- HEAD: `6ab5976a3fe74c6bc9b0ab8e4faa80e4471c8f2f`
- Synopsis: Corrects the campaign finalizer transaction model and refreshes coordinator/orchestrator generated contracts. It adds a dedicated campaign-candidate integration test suite and lifecycle wording fixes.
- Assessment: The candidate contains a broad campaign-finalizer transaction model, but it targets obsolete skill names and surfaces that current main later renamed or removed. It cannot be merged as-is; restoring this capability would require a fresh architecture and generated-contract review rather than replaying the old commit.
- Applicability evidence: ['main=c335db58b5fdb551277af78963f0ae69d428c89a; candidate=6ab5976a3fe74c6bc9b0ab8e4faa80e4471c8f2f', 'merge-base=dfbd1542ade8bd8a705ea0396562146fbaa21af6; main...candidate=1795/4; git cherry reports four candidate commits as unique (+)', 'git diff main...candidate changes 20 paths, including README, roles, generated adapters, lifecycle design, coordination skills, and a 1,100-line campaign integration test', 'git merge-tree main candidate reports broad content conflicts, plus modify/delete conflicts for scripts/test_codex_workitem_coordination.py, skills/agent-work-merge/SKILL.md, and skills/codex-workitem-coordination/SKILL.md', 'current main renamed agent-work-merge to integrate-agent-work (e283f805) and codex-workitem-coordination to coordinate-codex-tasks (84eb9937), and current main has no scripts/test_campaign_candidate_integration.py']
- Recommended work-item scope: Create a new architecture/design work item only if coordinated campaign finalization is still an authorized requirement. Re-specify it against current skill names, provider authority, generated outputs, and current lifecycle contracts; do not resurrect deleted files by merging this branch.
- Main-overlap risk: High
- Confidence: High
>DISCARD ITEM
### 32. codex/uar-examples-current-main-recovery

- Original v2 position: 123
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/uar-examples-current-main-recovery`
- HEAD: `aec92b112e4730d2ffe309d322a52f4a079043dd`
- Synopsis: User Action envelope integer, normalization, and state-invariant hardening; current main retains generic User Action routing but no matching envelope contract implementation was found.
- Assessment: The user-action envelope invariant hardening is not present in current main in the candidate's canonical form. The branch also edits generated projections and files that current main removed, so it cannot be merged as-is.
- Applicability evidence: Candidate aec92b11 changes the orchestrator role, generated adapters/metadata, test_codex_workitem_coordination.py, and manage-file-work-items/SKILL.md. Current main lacks the candidate's exact uar.v1 serializer bounds, Unicode/whitespace normalization, canonical byte encoding, digest/replay/stale/conflict rules, and associated test file; merge-tree reports conflicts across role/generated files plus modify/delete conflicts for the test and skill paths.
- Recommended work-item scope: Create a focused User Action envelope contract work item. Revalidate the invariant requirements against current orchestrator and provider naming, update canonical sources first, regenerate projections, and add current-main tests; do not restore deleted files or cherry-pick generated outputs.
- Main-overlap risk: High
- Confidence: High
>DISCARD ITEM
### 33. codex/decouple-orchestrator-current-main-correction-019f96ce

- Original v2 position: 125
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/decouple-orchestrator-current-main-correction-019f96ce`
- HEAD: `06f4c34b8e438833086359c682aa4be6063889b1`
- Synopsis: Binds orchestrator claim-audit evidence to staged helper authority, runtime rollouts, and adapter results. Current main has related orchestrator claim-audit remediation, but none of these three exact patches.
- Assessment: The branch adds stronger runner-owned claim-process evidence: exact staged helper path and digest, immutable rollout binding, canonical argv/result checks, and candidate PROJECT resource-coordination agreement. Current main has related resource-claim lifecycle auditing but not these safeguards, and the branch uses the obsolete agent-claim naming.
- Applicability evidence: ['Branch commits 1bb5695e, a9eefd7d, and 06f4c34b add adapter-result binding, rollout process-evidence auditing, and staged helper authority checks across runner.py and the dependency-routing fixture/tests.', 'Current main has _audit_claim_lifecycle and _session_resource_claim_invocations, but no claimHelperAuthority/processEvidence contract or exact helper SHA-256 enforcement.', 'Current main uses resource-claim/resource-claim-helper terminology after the provider rename; the branch patch targets agent-claim-command and therefore cannot be merged as-is without semantic adaptation.', 'Read-only merge-tree reports conflicts in dependency-routing fixture guidance/contract/tests and runner.py.']
- Recommended work-item scope: Create one focused work item to adapt the branch's runner-owned process-evidence and exact staged-helper authority requirements to current resource-claim naming and contracts. Preserve current resource-claim lifecycle checks, add fixture/test coverage for rollout identity, canonical helper path/digest, unexpected attempts, and committed PROJECT selection, then run the focused orchestrator fixture tests.
- Main-overlap risk: High
- Confidence: High
>DISCARD ITEM
### 34. codex/establish-ste-technical-documentation-standard

- Original v2 position: 127
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/establish-ste-technical-documentation-standard`
- HEAD: `a4165c21f464e0cf74d72c6f81b7a64d49c90f62`
- Synopsis: Establishes the STE technical-documentation standard and updates roles, adapters, generated projections, and verification coverage. The five branch commits remain unique, while main contains adjacent terminology, documentation, and generated-definition work.
- Assessment: Do not merge the preserved five-commit STE branch as-is. Current main already contains the original STE delivery and its semantic-preservation defect closure, but the preserved feature item was explicitly reopened on 2026-08-12 for a fresh current-main reconciliation after cleanup and a clarified scope. The branch must therefore be handled by that existing lifecycle, with fresh review and verification.
- Applicability evidence: git cherry main a4165c21 reports all five commits unique; git merge-tree shows conflicts across README, model profiles, roles, generated mirrors, and tests. Current main has skills/ste-technical-writing/SKILL.md and generated projections. scripts/test_ste_technical_writing.py ran 14 tests with one current-main contract failure: conceptual agents omit terminology-standard from the expected shared skill list. The feature backlog record names the preserved candidate and requires current-main reapplication, regeneration, fresh review, and verification.
- Recommended work-item scope: Reuse the existing Ready work item establish-ste-technical-documentation-standard; do not create a duplicate. Start from current main, selectively reconcile the accepted STE content, resolve the terminology-standard contract finding, regenerate supported projections, and obtain fresh independent review and verification.
- Main-overlap risk: High
- Confidence: High
>DISCARD ITEM
### 35. codex/eliminate-standalone-definition-approval-records-integration-019faeef

- Original v2 position: 130
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/eliminate-standalone-definition-approval-records-integration-019faeef`
- HEAD: `7cca88fee05db053e452729fcc094cc8309623ed`
- Synopsis: Integrates accepted source changes to eliminate standalone definition-approval records while preserving current-main lifecycle semantics. It removes the approval-record files, regenerates skill-definition output, and updates configuration, rendering, and technology-detection tests.
- Assessment: The approval-record removal candidate has broad overlap with current main and cannot merge as-is. The three-way merge reports conflicts in project guidance, generated outputs, scripts, and skills, plus modify/delete conflicts where current main removed files that the candidate still edits.
- Applicability evidence: ['main=c335db58b5fdb551277af78963f0ae69d428c89a; candidate=7cca88fee05db053e452729fcc094cc8309623ed', "merge-base=d855b53031ecdc7fa98d99dd8faa911b3da5222c; main...candidate=1151/1; git cherry reports candidate as '+'", 'candidate changes 129 paths, including deletion of 100+ approval-record files; all 129 paths overlap current main', 'git merge-tree main candidate exits 1 with conflicts in AGENTS.md, PROJECT.yaml, README.md, generated/script/test surfaces, and modify/delete conflicts for scripts/test_codex_workitem_coordination.py and two skills']
- Recommended work-item scope: Create a fresh approval-record cleanup integration work item and reconcile the candidate with current generated/configuration and skill sources; do not replay the broad deletion as an as-is merge.
- Main-overlap risk: High
- Confidence: High
> APPROVED
> 
### 36. codex/align-orchestrated-development-lifecycle-design-system-019ff2f9

- Original v2 position: 134
- Worktree: `/Users/martinbechard/dev/dev-methodology/.worktrees/align-orchestrated-lifecycle-work-019ff2f9`
- HEAD: `ce7002bf2794c62cdbd7ebf58ff217aeb5e55935`
- Synopsis: The orchestrated-development lifecycle documentation was aligned to the design system, refreshed, and made keyboard-scrollable.
- Assessment: The lifecycle/design-system candidate is not applicable as-is to current main. It changes a broad documentation and test surface, while current main has reverted or reshaped the candidate's v1.0 shell, navigation, and keyboard-scroll assumptions.
- Applicability evidence: Candidate ce7002bf2794c62cdbd7ebf58ff217aeb5e55935 has merge-base f1490b80e856df9cc08d24027acd3252734aac18 and four unique commits. git merge-tree --write-tree main candidate reports a content conflict in design/agent-and-skill-evaluations.html; the candidate changes 20 paths and 280 insertions/50 deletions. Current main's orchestrated-development-lifecycle.html and scripts/test_documentation_design_system.py use the v0.1.0 shell and lack the candidate's v1.0 navigation, focusable table wrapper, and semantic-baseline assertions.
- Recommended work-item scope: Create a lifecycle design-system reconciliation item. Revalidate the desired shell and accessibility changes against current v0.1.0 sources, update canonical documentation and tests first, then regenerate affected projections and run focused design-system checks.
- Main-overlap risk: High
- Confidence: High
>DISCARD ITEM
