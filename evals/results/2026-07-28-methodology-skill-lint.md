# Methodology Skill Lint Review

## Result

The root-launched read-only lint batches covered all 127 authoritative methodology skill sources. Their raw outputs contain 19 CRITICAL outcomes and 108 NO_CRITICAL outcomes.

Independent reconciliation accepted 27 CONFIRMED_CRITICAL dispositions and 100 NO_CRITICAL dispositions. The accepted set retains 18 original critical skill classifications, rejects the provisional documentation-bootstrap and Liquibase classifications, and adds nine independently confirmed omissions.

Every accepted critical skill has one authoritative file-provider record below. Provider references resolve against primary commit f11b3c67b3a033fe9669608b2f8920937d57bc22. Lifecycle state may advance after that commit; the provider reference remains the durable identity.

## Work Identity

- Canonical work-item Thread and root task: 019fa9be-0083-7542-973f-af35557b2393
- Parent Coordinator Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758
- Branch: codex/run-skill-lint-across-methodology-019f
- Worktree: /Users/martinbechard/dev/dev-methodology/.worktrees/run-skill-lint-across-methodology-019f
- Reserved base: 6affa81cccc7fca4b8ce8ed4045a5139c18a7654

## Scope

The authoritative inventory contains:

- Distributed skill sources matching skills/[skill-name]/SKILL.md.
- Adapter-owned skill sources matching adapters/[adapter]/skills/[skill-name]/SKILL.md.

The excluded-source rule omits generated mirrors, vendored files, build output, evaluation fixtures, archived or linked worktrees, report artifacts, and any nested SKILL.md that is not an authoritative distributed or adapter-owned source at one of those two exact path shapes.

A fresh find inventory under skills and adapters produced 127 unique authoritative paths. The raw batch outputs and the final outcome table contain those same 127 paths exactly once.

## Batch Execution Evidence

The root launched all nine successful batches with configured model gpt-5.6-luna and high reasoning effort. All nine retained final outputs self-report gpt-5.6-luna. Eight outputs explicitly self-report high reasoning effort; skill-lint-g5 omits high from its final text.

The generated Codex adapter records gpt-5.6-luna and high as the reviewer configuration. That adapter proves configuration, not runtime execution. Runtime identity remains self-reported by the retained batch outputs.

| Batch task | Skill outcomes | Retained identity evidence |
| --- | ---: | --- |
| skill-lint-g1 | 15 | Self-reports gpt-5.6-luna and high |
| skill-lint-g2 | 15 | Self-reports gpt-5.6-luna and high |
| skill-lint-g3 | 15 | Self-reports gpt-5.6-luna and high |
| skill-lint-g4 | 15 | Self-reports gpt-5.6-luna and high |
| skill-lint-g5 | 15 | Self-reports gpt-5.6-luna; final text omits high |
| skill-lint-g6 | 15 | Self-reports gpt-5.6-luna and high |
| skill-lint-g7 | 15 | Self-reports gpt-5.6-luna and high |
| skill-lint-g8 | 15 | Self-reports gpt-5.6-luna and high |
| skill-lint-g9 | 7 | Self-reports gpt-5.6-luna and high |

Only the successful retained outputs contribute raw outcomes. Failed or abandoned attempts are excluded. No durable conclusion about the Codex CLI version is made from the batch evidence.

The root-executed focused MySQL adjudication ran under canonical task 019fa9be-0083-7542-973f-af35557b2393 with resource evidence label skill-lint-mysql-adjudication-019fa9be. Its retained output explicitly self-reports gpt-5.6-luna, high reasoning effort, and CRITICAL.

## Independent Reconciliation Evidence

| Reviewer task | Reconciliation responsibility |
| --- | --- |
| /root/confirm_critical_a | Confirmed agent-claim-command, backlog-crisis-mode, and end-to-end-verification; rejected documentation-bootstrap |
| /root/confirm_critical_b | Confirmed detect-technology-skills, fix-explanation, and Jest; rejected Liquibase |
| /root/confirm_critical_c | Confirmed maintain-methodology-documentation, manage-file-work-items, MySQL, and project-wiki-create; rejected two provisional subfindings |
| /root/confirm_critical_d | Confirmed project-wiki-topic-verify, project-wiki-topic-write, project-wiki, and React Server Components |
| /root/confirm_critical_e | Confirmed structured-design, test-strategy, tool-runtime, and TypeScript ESM |
| /root/confirm_create_module_design | Confirmed the omitted create-module-design contradiction |
| /root/confirm_new_routing_findings | Confirmed the omitted user-experience-review, quarkus-persistence, and Tailwind routing defects |
| /root/confirm_review_evidence_findings | Confirmed the five omitted review-package evidence-contract defects |
| /root/audit_no_critical_2 | Independently audited 35 raw NO_CRITICAL paths and found no new critical candidate |
| /root/audit_no_critical_3 | Independently audited 32 raw NO_CRITICAL paths and identified eight later-confirmed omissions |
| /root/review_lint_report_candidate | Independently reviewed the first report candidate and required evidence qualification and raw-versus-accepted separation |

## Provider Creation Evidence

- Batch 1 creation commit 24a7a102c9267fd302712b48f90cb935409643d5 created eight provider records. Correction commit 1ef9018bf859607f161ff9a275c336c145b73b9a corrected those records, and a fresh exact-record review returned GOOD.
- Batch 2 creation commit cb36a746af875ea0ad9d5c5fbb83b8342d6dc6b6 created eight provider records. The corrected records are present at commit 79a7be438ed51f503dd33f01f0c8e97b56d60709, and a fresh exact-record review returned GOOD.
- Final batch creation commit f11b3c67b3a033fe9669608b2f8920937d57bc22 created the remaining eleven provider records. Fresh exact-commit review returned GOOD: all 11 records were eligible and schema-complete, with no collisions, anomalies, or dependencies; source, routing, governance, approval, and acceptance checks passed; Markdown links were OK; and the review reported no Future Ideas.
- At commit f11b3c67b3a033fe9669608b2f8920937d57bc22, all 27 references below resolve to unique records with Type: Defect, Provider: file, exact self-referencing Provider Reference, and Completion: direct-main.

## Rejected Provisional Findings

### skills/documentation-bootstrap/SKILL.md

- Raw batch outcome: CRITICAL.
- Accepted disposition: NO_CRITICAL.
- Independent reviewer: /root/confirm_critical_a.
- Rejection rationale: Line 56 describes grouping wiki changes after Commit authority exists. It does not select a Commit workflow, execute Git, or override an UNSET decision. No concrete contradictory execution path was established.

### skills/liquibase/SKILL.md

- Raw batch outcome: CRITICAL.
- Accepted disposition: NO_CRITICAL.
- Independent reviewer: /root/confirm_critical_b.
- Rejection rationale: Line 25 is bounded by generated-SQL inspection, recovery expectations, data-loss reporting, repeat execution, and deployment-risk reporting. It does not authorize live production mutation. Reading representative pre-change database as production was hypothetical.

### Rejected subfindings within accepted critical skills

- skills/manage-file-work-items/SKILL.md remains CONFIRMED_CRITICAL for unconditional claim-event directions under resource_coordination: none. Its provisional UNSET lifecycle finding was rejected because provider selection before mutation and an existing item’s User Action Required transition are distinct workflows.
- skills/project-wiki-create/SKILL.md remains CONFIRMED_CRITICAL for its non-portable template path. Its provisional review-routing finding was rejected because the skill explicitly names the review skills and does not promise fresh independent review; absent preloading alone does not establish a critical dependency defect.

## Accepted Critical Defect Records

Every record in this section has independently accepted disposition CONFIRMED_CRITICAL and one authoritative provider reference. No record authorizes a skill or agent definition mutation.

### skills/agent-claim-command/SKILL.md

- Independent reviewer: /root/confirm_critical_a.
- Accepted defect title: Make agent-claim reset recover invalid JSON registry shapes.
- Accepted defect slug: agent-claim-reset-invalid-json-shapes.
- Provider reference: backlog/defect-backlog/agent-claim-reset-invalid-json-shapes.md
- Location: skills/agent-claim-command/SKILL.md:153; confirming implementation at skills/agent-claim-command/scripts/claim.py:1999-2008.
- Criterion: Unsupported validation claim.
- Source-backed rationale: Reset promises recovery from malformed contents, but valid non-object JSON reaches a get call and can raise AttributeError outside the documented recovery path.
- Smallest correction: Treat every non-object parsed value as an invalid registry shape, or narrow the documented recovery guarantee.
- Verification: Exercise missing, malformed, non-object, and invalid claims-shape registries and require a valid empty registry after every supported reset.

### skills/backlog-crisis-mode/SKILL.md

- Independent reviewer: /root/confirm_critical_a.
- Accepted defect title: Preserve agent-claim ownership during backlog crisis delivery.
- Accepted defect slug: backlog-crisis-retain-agent-claim.
- Provider reference: backlog/defect-backlog/backlog-crisis-retain-agent-claim.md
- Location: skills/backlog-crisis-mode/SKILL.md:32,44; owning claim rules at skills/agent-claim/SKILL.md:20-21,69-75.
- Criterion: Contradiction and unsafe permission.
- Source-backed rationale: The crisis skill stops claim operations while continuing delivery around unrelated changes, bypassing the owning claim contract for shared-path mutation and overlap handling.
- Smallest correction: Retain agent-claim acquisition and conflict handling during crisis delivery.
- Verification: Run crisis guidance against an overlapping claim and require the owning wait or recovery outcome.

### skills/create-module-design/SKILL.md

- Independent reviewer: /root/confirm_create_module_design.
- Accepted defect title: Align module-design optional-section instructions with the mandatory heading contract.
- Accepted defect slug: align-module-design-mandatory-heading-contract.
- Provider reference: backlog/defect-backlog/align-module-design-mandatory-heading-contract.md
- Location: skills/create-module-design/SKILL.md:20,85; module-design-template.md:285,295,303; skills/review-module-design/SKILL.md:28; skills/development-methodology/SKILL.md:123.
- Criterion: Contradiction.
- Source-backed rationale: The creation and review gates require every level-two heading, while the template directs authors to remove Configuration, External Interfaces, and UI And Notification Behavior when inapplicable. Following the template creates an artifact the required gates reject.
- Smallest correction: Preserve the three mandatory headings and record why each is not applicable; make artifact-specific heading contracts override the generic section-removal rule.
- Verification: Cover all three headings with a module that has no applicable content and require creation and review gates to accept retained not-applicable sections.

### skills/detect-technology-skills/SKILL.md

- Independent reviewer: /root/confirm_critical_b.
- Accepted defect title: Make the technology detector fallback prerequisites executable.
- Accepted defect slug: make-technology-detector-fallback-prerequisites-executable.
- Provider reference: backlog/defect-backlog/make-technology-detector-fallback-prerequisites-executable.md
- Location: skills/detect-technology-skills/SKILL.md:16,31-40; imports at skills/detect-technology-skills/scripts/detect.py:15,18.
- Criterion: Missing dependency.
- Source-backed rationale: The documented python3 fallback imports tomllib and PyYAML without declaring a compatible runtime, so an available Python 3.9 runtime can fail before returning a detection outcome.
- Smallest correction: Declare executable runtime and package prerequisites or provide a compatible fallback.
- Verification: Run the exact fallback under every declared supported runtime and cover READY, BLOCKED, and NO_VARIANT.

### skills/end-to-end-verification/SKILL.md

- Independent reviewer: /root/confirm_critical_a.
- Accepted defect title: Route E2E evidence delivery through Commit authority.
- Accepted defect slug: end-to-end-verification-commit-authority.
- Provider reference: backlog/defect-backlog/end-to-end-verification-commit-authority.md
- Location: skills/end-to-end-verification/SKILL.md:22.
- Criterion: Unsafe permission and missing authority or ownership.
- Source-backed rationale: The verifier unconditionally requires a commit before handoff, even when the selected Commit workflow or request grants evidence-only authority.
- Smallest correction: Route delivery through the selected Commit workflow and preserve read-only verification when mutation authority is absent.
- Verification: Exercise direct-main, feature-branch, UNSET, and evidence-only contexts and require only the selected workflow to create commits.

### skills/fix-explanation/SKILL.md

- Independent reviewer: /root/confirm_critical_b.
- Accepted defect title: Align fix-explanation relationship examples with the six-type explanation model.
- Accepted defect slug: align-fix-explanation-item-taxonomy.
- Provider reference: backlog/defect-backlog/align-fix-explanation-item-taxonomy.md
- Location: skills/fix-explanation/SKILL.md:152,191-196; item-type authority at skills/structured-explanation/SKILL.md:30-37.
- Criterion: Output contract defect.
- Source-backed rationale: Relationship examples use TEST, FIX, PROBLEM, and BENEFIT as item types even though structured-explanation permits only six named item types.
- Smallest correction: Express the examples with permitted item types or label the words as ordinary concepts.
- Verification: Produce a representative fix explanation and assert that every structured item uses the declared six-type model.

### skills/jest/SKILL.md

- Independent reviewer: /root/confirm_critical_b.
- Accepted defect title: Bound Jest failure ownership to the current change.
- Accepted defect slug: bound-jest-failure-ownership-to-current-change.
- Provider reference: backlog/defect-backlog/bound-jest-failure-ownership-to-current-change.md
- Location: skills/jest/SKILL.md:32.
- Criterion: Missing authority or ownership.
- Source-backed rationale: Treating every failing test as the current task expands ownership to unrelated failures and can block an otherwise complete scoped change.
- Smallest correction: Own only failures attributable to the current change and record unrelated failures separately.
- Verification: Present one attributable and one pre-existing failure and require repair ownership only for the attributable failure.

### skills/maintain-methodology-documentation/SKILL.md

- Independent reviewer: /root/confirm_critical_c.
- Accepted defect title: Separate distributed methodology guidance from repository maintenance procedures.
- Accepted defect slug: separate-distributed-methodology-from-repository-maintenance.
- Provider reference: backlog/defect-backlog/separate-distributed-methodology-from-repository-maintenance.md
- Location: skills/maintain-methodology-documentation/SKILL.md:3,14-23,33-63; repository-only boundary at .agents/skills/dev-methodology-repository-maintenance/SKILL.md:24-40.
- Criterion: Wrong harness boundary and significant redundancy.
- Source-backed rationale: A distributed skill embeds dev-methodology source-checkout paths and repository procedure already owned by the project-maintenance skill.
- Smallest correction: Keep repository procedure in the project skill and retain only portable methodology-documentation guidance in the distributed skill.
- Verification: Validate the distributed package and assert that it requires no dev-methodology-only source path or command.

### skills/manage-file-work-items/SKILL.md

- Independent reviewer: /root/confirm_critical_c.
- Accepted defect title: Make file-provider claim events conditional on configured resource coordination.
- Accepted defect slug: respect-resource-coordination-none-in-manage-file-work-items.
- Provider reference: backlog/defect-backlog/respect-resource-coordination-none-in-manage-file-work-items.md
- Location: skills/manage-file-work-items/SKILL.md:28,150,244.
- Criterion: Missing dependency and wrong harness boundary.
- Source-backed rationale: The clauses require agent-claim even when a valid project selects resource_coordination: none, leaving no enabled claim procedure for the mandated operation.
- Smallest correction: Make provider claim directions conditional on the configured coordination implementation and define the no-claim path for none.
- Verification: Exercise identical provider transitions under agent-claim and none configurations and require a valid route in both.

### skills/mysql/SKILL.md

- Independent reviewer: /root/confirm_critical_c plus root-executed focused MySQL adjudication.
- Accepted defect title: Bound MySQL production verification to safe test environments.
- Accepted defect slug: bound-mysql-production-verification-to-safe-targets.
- Provider reference: backlog/defect-backlog/bound-mysql-production-verification-to-safe-targets.md
- Location: skills/mysql/SKILL.md:44.
- Criterion: Unsafe permission.
- Source-backed rationale: Correctness and concurrency checks can write data, hold locks, or create load when production-like is interpreted as production.
- Smallest correction: Require a production-like non-production engine and limit explicitly approved production work to bounded read-only diagnostics.
- Verification: Reject direct production mutation, lock, or load testing while permitting approved bounded read-only diagnostics.
- Reconciliation note: skill-lint-g5 raw summary says NO_CRITICAL despite its detailed critical finding. The focused MySQL adjudication under canonical task 019fa9be-0083-7542-973f-af35557b2393 used evidence label skill-lint-mysql-adjudication-019fa9be, self-reported gpt-5.6-luna and high, and returned CRITICAL.

### skills/project-wiki-create/SKILL.md

- Independent reviewer: /root/confirm_critical_c.
- Accepted defect title: Resolve the project-wiki template from the installed skill catalog.
- Accepted defect slug: make-project-wiki-template-resolution-install-portable.
- Provider reference: backlog/defect-backlog/make-project-wiki-template-resolution-install-portable.md
- Location: skills/project-wiki-create/SKILL.md:14.
- Criterion: Missing dependency.
- Source-backed rationale: The template path is expressed relative to the dev-methodology source checkout, but installed skills reside under a configured skill root.
- Smallest correction: Resolve the installed development-methodology asset explicitly or package the template with project-wiki-create.
- Verification: Install into a clean target and prove template discovery and copying work without the source checkout.

### skills/project-wiki-topic-verify/SKILL.md

- Independent reviewer: /root/confirm_critical_d.
- Accepted defect title: Keep topic verification read-only and make helper checks executable.
- Accepted defect slug: project-wiki-topic-verify-read-only-helper-resolution.
- Provider reference: backlog/defect-backlog/project-wiki-topic-verify-read-only-helper-resolution.md
- Location: skills/project-wiki-topic-verify/SKILL.md:10,50-52.
- Criterion: Contradiction, unsafe permission, missing dependency, and unsupported validation claim.
- Source-backed rationale: The read-only verifier permits mutating okf-migrate repair, and its required commands depend on unresolved project-wiki-skill-root path text.
- Smallest correction: Return stale frontmatter as writer-owned correction and define one executable installed helper-root resolution.
- Verification: Invoke stale-frontmatter verification from a clean installed target and require no mutation plus successful runnable checks.

### skills/project-wiki-topic-write/SKILL.md

- Independent reviewer: /root/confirm_critical_d.
- Accepted defect title: Defer verifier orchestration to conceptual roles and resolve writer helper commands.
- Accepted defect slug: project-wiki-topic-write-role-owned-verification.
- Provider reference: backlog/defect-backlog/project-wiki-topic-write-role-owned-verification.md
- Location: skills/project-wiki-topic-write/SKILL.md:64-76.
- Criterion: Wrong harness boundary, output contract defect, missing dependency, and unsupported validation claim.
- Source-backed rationale: The skill owns fresh-subagent dispatch and interruption policy that belong to the conceptual role, while its mandatory helper commands use unresolved project-wiki-skill-root text.
- Smallest correction: Let the owning role orchestrate verification and define portable executable helper resolution.
- Verification: Run writer checks from a clean installation and simulate verifier interruption; require executable commands, preserved edits, no verifier mutation, and BLOCKED evidence.

### skills/project-wiki/SKILL.md

- Independent reviewer: /root/confirm_critical_d.
- Accepted defect title: Restore role-owned wiki verification routing and portable operation paths.
- Accepted defect slug: project-wiki-role-routing-and-operation-paths.
- Provider reference: backlog/defect-backlog/project-wiki-role-routing-and-operation-paths.md
- Location: skills/project-wiki/SKILL.md:145-149,231-245; ingester interruption authority in the configured conceptual role.
- Criterion: Wrong harness boundary, output contract defect, missing dependency, and unsupported validation claim.
- Source-backed rationale: The generic skill owns verifier dispatch, requires GOOD before move without aligning interrupted-verifier handling with the ingester role, and lists operations through unresolved project-wiki-skill-root text.
- Smallest correction: Restore role-owned verification and interruption handling and define portable operation paths.
- Verification: Exercise pre-move and post-move verification interruption plus every listed operation from a clean installed target.

### skills/quarkus-persistence/SKILL.md

- Independent reviewer: /root/confirm_new_routing_findings.
- Accepted defect title: Keep Quarkus persistence companion selection setup-owned.
- Accepted defect slug: keep-quarkus-persistence-companion-selection-setup-owned.
- Provider reference: backlog/defect-backlog/keep-quarkus-persistence-companion-selection-setup-owned.md
- Location: skills/quarkus-persistence/SKILL.md:16; references/persistence-guidelines-quarkus.md:20; references/review-checklist-quarkus-persistence.md:4.
- Criterion: Missing authority or ownership, wrong harness boundary, and significant duplicated authority.
- Source-backed rationale: The package repeatedly directs ordinary runtime actors to select a blocking persistence companion from source evidence even though setup-time detection owns that decision and intentionally distinguishes blocking from reactive Panache.
- Smallest correction: Consume only an active-scope companion already supplied by setup and report missing or stale routing.
- Verification: Preserve blocking and reactive detector cases and assert that runtime work never invents a companion.

### skills/react-server-components/SKILL.md

- Independent reviewer: /root/confirm_critical_d.
- Accepted defect title: Require Server Components evidence before activating the RSC skill.
- Accepted defect slug: react-server-components-detection-boundary.
- Provider reference: backlog/defect-backlog/react-server-components-detection-boundary.md
- Location: skills/react-server-components/detection.yaml:8-11; claimed scope at skills/react-server-components/SKILL.md:3,10.
- Criterion: Missing dependency.
- Source-backed rationale: Any app subtree containing TSX or JSX activates Server Components guidance without Next.js or React Server Components evidence.
- Smallest correction: Require Next.js or another explicit React Server Components marker in detection.yaml.
- Verification: Prove a client-only React app is excluded and valid Server Components projects are selected.
- Governance boundary: The smallest accepted correction is detection.yaml-only under the current governed-source list. This report grants no definition mutation authority.

### skills/review-architecture/SKILL.md

- Independent reviewer: /root/confirm_review_evidence_findings.
- Accepted defect title: Allow typed evidence in architecture review checklists.
- Accepted defect slug: allow-typed-evidence-review-architecture.
- Provider reference: backlog/defect-backlog/allow-typed-evidence-review-architecture.md
- Location: skills/review-architecture/SKILL.md:30; references/review-checklist-architecture.md:9-16; conflicting shared evidence authority at skills/documentation-page-verify/SKILL.md:58-60,67-70 and skills/review-structured-artifact/SKILL.md:95-122.
- Criterion: Contradiction and output contract defect.
- Source-backed rationale: The package requires exact quotation for every applicable result, including absence-based and derived structural conclusions that have no literal target text.
- Smallest correction: Use the shared typed-evidence model and allow explained not-applicable results without quotation.
- Verification: Cover a literal quotation, an absence-based failure, and a conditional not-applicable result.

### skills/review-functional-spec/SKILL.md

- Independent reviewer: /root/confirm_review_evidence_findings.
- Accepted defect title: Allow typed evidence in functional-specification review checklists.
- Accepted defect slug: allow-typed-evidence-review-functional-spec.
- Provider reference: backlog/defect-backlog/allow-typed-evidence-review-functional-spec.md
- Location: skills/review-functional-spec/SKILL.md:30; references/review-checklist-functional-spec.md:9-16,47-68; shared evidence authority at skills/documentation-page-verify/SKILL.md:58-60,67-70 and skills/review-structured-artifact/SKILL.md:95-122.
- Criterion: Contradiction and output contract defect.
- Source-backed rationale: Quote-only evidence cannot truthfully represent missing behavior, absent examples, derived inventory reconciliation, or non-applicable interface conditions.
- Smallest correction: Use typed evidence and require literal resolution only when the evidence type is exact quotation.
- Verification: Cover quotation-backed evidence, an absence-based failure, and a conditional not-applicable result.

### skills/review-high-level-design/SKILL.md

- Independent reviewer: /root/confirm_review_evidence_findings.
- Accepted defect title: Allow typed evidence in high-level-design review checklists.
- Accepted defect slug: allow-typed-evidence-review-high-level-design.
- Provider reference: backlog/defect-backlog/allow-typed-evidence-review-high-level-design.md
- Location: skills/review-high-level-design/SKILL.md:30; references/review-checklist-high-level-design.md:9-16,32-47,71-85; shared evidence authority at skills/documentation-page-verify/SKILL.md:58-60,67-70 and skills/review-structured-artifact/SKILL.md:95-122.
- Criterion: Contradiction and output contract defect.
- Source-backed rationale: The package forces quotation for derived coverage, missing contracts, diagram-trigger analysis, and mode-dependent not-applicable questions.
- Smallest correction: Align the skill and checklist with typed evidence and explanation-backed not-applicable results.
- Verification: Cover a mode-dependent not-applicable result, a missing-contract failure, and a literal quotation.

### skills/review-module-design/SKILL.md

- Independent reviewer: /root/confirm_review_evidence_findings.
- Accepted defect title: Allow typed evidence in module-design review checklists.
- Accepted defect slug: allow-typed-evidence-review-module-design.
- Provider reference: backlog/defect-backlog/allow-typed-evidence-review-module-design.md
- Location: skills/review-module-design/SKILL.md:31; references/review-checklist-module-design.md:9-16,42-103; shared evidence authority at skills/documentation-page-verify/SKILL.md:58-60,67-70 and skills/review-structured-artifact/SKILL.md:95-122.
- Criterion: Contradiction and output contract defect.
- Source-backed rationale: Conditional, operation-reconciliation, omission, and structural checks cannot all be supported by literal source quotations.
- Smallest correction: Use typed evidence in both the skill and direct checklist.
- Verification: Cover an omitted operation, a non-applicable asynchronous boundary, and a resolved exact quotation.

### skills/review-unit-test-plan/SKILL.md

- Independent reviewer: /root/confirm_review_evidence_findings.
- Accepted defect title: Allow typed evidence in unit-test-plan review checklists.
- Accepted defect slug: allow-typed-evidence-review-unit-test-plan.
- Provider reference: backlog/defect-backlog/allow-typed-evidence-review-unit-test-plan.md
- Location: skills/review-unit-test-plan/SKILL.md:14; references/review-checklist-unit-test-plan.md:5-10,15-31; shared evidence authority at skills/documentation-page-verify/SKILL.md:58-60,67-70 and skills/review-structured-artifact/SKILL.md:95-122.
- Criterion: Contradiction and output contract defect.
- Source-backed rationale: Conflict absence, coverage gaps, duplicate-test assessment, and non-applicable failure cases require derived or not-applicable evidence, but the package requires quotations for every result.
- Smallest correction: Apply the shared typed-evidence model across the skill and checklist.
- Verification: Cover a missing source conflict, a non-applicable failure case, and a quotation-backed scenario.

### skills/structured-design/SKILL.md

- Independent reviewer: /root/confirm_critical_e.
- Accepted defect title: Replace the structured-design chain-of-thought output contract.
- Accepted defect slug: replace-structured-design-chain-of-thought-output-contract.
- Provider reference: backlog/defect-backlog/replace-structured-design-chain-of-thought-output-contract.md
- Location: skills/structured-design/SKILL.md:9-10,172,196-198,546,584,602.
- Criterion: Wrong harness boundary.
- Source-backed rationale: CHAIN-OF-THOUGHT is part of the declared output vocabulary, examples, and self-review contract, requiring disclosure of private reasoning.
- Smallest correction: Replace it with an externally useful rationale or bridge field throughout.
- Verification: Validate examples and self-review rules and assert that no output contract requires private reasoning disclosure.

### skills/tailwind-design-system/SKILL.md

- Independent reviewer: /root/confirm_new_routing_findings.
- Accepted defect title: Make Tailwind companion guidance conditional on active-scope routing.
- Accepted defect slug: make-tailwind-companion-guidance-route-aware.
- Provider reference: backlog/defect-backlog/make-tailwind-companion-guidance-route-aware.md
- Location: skills/tailwind-design-system/SKILL.md:16; independently activated companion metadata for React Server Components, React Vite Renderer, Next.js App Router, Jest, and Playwright.
- Criterion: Material clarity failure, missing dependency, and wrong harness boundary.
- Source-backed rationale: The unconditional five-skill combination can require unavailable tools and combine alternative Next.js and Vite runtime models even though Tailwind detection declares no companions.
- Smallest correction: Use only framework, renderer, and test guidance supplied for the active scope.
- Verification: Cover Tailwind with Vite and Next.js plus a negative case where an un-routed test skill is not loaded.

### skills/test-strategy/SKILL.md

- Independent reviewer: /root/confirm_critical_e.
- Accepted defect title: Stop test-strategy from rerunning technology-skill routing.
- Accepted defect slug: stop-test-strategy-from-rerunning-technology-routing.
- Provider reference: backlog/defect-backlog/stop-test-strategy-from-rerunning-technology-routing.md
- Location: skills/test-strategy/SKILL.md:10,16; Project Configurator routing authority in AGENTS.md.
- Criterion: Contradiction and missing authority or ownership.
- Source-backed rationale: The skill first says to use already-routed guidance, then tells ordinary agents to route specialized skills from repository evidence.
- Smallest correction: Consume the recorded active-scope skillset and prohibit ordinary rerouting or detection.
- Verification: Run in a configured folder and require use of the recorded skillset without technology detection.

### skills/tool-runtime/SKILL.md

- Independent reviewer: /root/confirm_critical_e.
- Accepted defect title: Prevent sensitive data retention in tool-runtime logs and traces.
- Accepted defect slug: prevent-sensitive-tool-runtime-log-and-trace-retention.
- Provider reference: backlog/defect-backlog/prevent-sensitive-tool-runtime-log-and-trace-retention.md
- Location: skills/tool-runtime/SKILL.md:20-23.
- Criterion: Unsafe permission.
- Source-backed rationale: The execution-trace requirement lacks a redaction boundary, so logs can retain secrets, tokens, personally identifiable information, private payloads, or protected file contents.
- Smallest correction: Require sensitive-data exclusion and redaction for logs and traces.
- Verification: Cover sensitive values across successful, denied, malformed, partial, and retried calls and assert redacted retained evidence.

### skills/typescript-esm/SKILL.md

- Independent reviewer: /root/confirm_critical_e.
- Accepted defect title: Detect TypeScript ESM in bundler-only projects.
- Accepted defect slug: detect-typescript-esm-in-bundler-only-projects.
- Provider reference: backlog/defect-backlog/detect-typescript-esm-in-bundler-only-projects.md
- Location: skills/typescript-esm/SKILL.md:3; skills/typescript-esm/detection.yaml:9-18.
- Criterion: Missing dependency.
- Source-backed rationale: The skill claims bundler ESM coverage, but activation requires package module mode or NodeNext and misses module: ESNext or moduleResolution: bundler projects.
- Smallest correction: Add a detection.yaml branch for bundler and ESNext TypeScript configurations.
- Verification: Require both typescript-esm and typescript for a bundler-only detector fixture.
- Governance boundary: The smallest accepted correction is detection.yaml-only under the current governed-source list. The definition-change checker’s policy for detection paths is a separate ambiguity; this report grants no mutation authority.

### skills/user-experience-review/SKILL.md

- Independent reviewer: /root/confirm_new_routing_findings.
- Accepted defect title: Stop UX review from performing runtime technology routing.
- Accepted defect slug: stop-ux-review-runtime-technology-routing.
- Provider reference: backlog/defect-backlog/stop-ux-review-runtime-technology-routing.md
- Location: skills/user-experience-review/SKILL.md:15; agents/roles/dev-activities/dev-ux-specialist.role.yaml:6,64.
- Criterion: Missing authority or ownership, wrong harness boundary, and contradiction.
- Source-backed rationale: The skill tells an ordinary UX reviewer to route specialized guidance from repository evidence even though Project Configurator owns setup routing and Dev UX Specialist consumes supplied active-scope guidance.
- Smallest correction: Use only technology guidance already supplied for the active folder and report a routing gap when required guidance is missing.
- Verification: Provide repository evidence for an un-routed skill and require no ad hoc load.

## Complete Outcome Inventory

| Authoritative skill source | Batch task | Raw batch outcome | Independently accepted disposition | Provider reference |
| --- | --- | --- | --- | --- |
| adapters/codex/skills/codex-harness-directives/SKILL.md | skill-lint-g1 | NO_CRITICAL | NO_CRITICAL |  |
| skills/agent-claim-command/SKILL.md | skill-lint-g1 | CRITICAL | CONFIRMED_CRITICAL | backlog/defect-backlog/agent-claim-reset-invalid-json-shapes.md |
| skills/agent-claim-mcp/SKILL.md | skill-lint-g1 | NO_CRITICAL | NO_CRITICAL |  |
| skills/agent-claim/SKILL.md | skill-lint-g1 | NO_CRITICAL | NO_CRITICAL |  |
| skills/agent-harness/SKILL.md | skill-lint-g1 | NO_CRITICAL | NO_CRITICAL |  |
| skills/agent-role-authoring/SKILL.md | skill-lint-g1 | NO_CRITICAL | NO_CRITICAL |  |
| skills/agent-work-merge/SKILL.md | skill-lint-g1 | NO_CRITICAL | NO_CRITICAL |  |
| skills/api-routes/SKILL.md | skill-lint-g1 | NO_CRITICAL | NO_CRITICAL |  |
| skills/application-security/SKILL.md | skill-lint-g1 | NO_CRITICAL | NO_CRITICAL |  |
| skills/ast-grep/SKILL.md | skill-lint-g1 | NO_CRITICAL | NO_CRITICAL |  |
| skills/backlog-crisis-mode/SKILL.md | skill-lint-g1 | CRITICAL | CONFIRMED_CRITICAL | backlog/defect-backlog/backlog-crisis-retain-agent-claim.md |
| skills/careful-coding/SKILL.md | skill-lint-g1 | NO_CRITICAL | NO_CRITICAL |  |
| skills/clerk-auth/SKILL.md | skill-lint-g1 | NO_CRITICAL | NO_CRITICAL |  |
| skills/code-comments/SKILL.md | skill-lint-g1 | NO_CRITICAL | NO_CRITICAL |  |
| skills/code-discovery/SKILL.md | skill-lint-g1 | NO_CRITICAL | NO_CRITICAL |  |
| skills/code-execution-tracing/SKILL.md | skill-lint-g2 | NO_CRITICAL | NO_CRITICAL |  |
| skills/code-project-wiki/SKILL.md | skill-lint-g2 | NO_CRITICAL | NO_CRITICAL |  |
| skills/code-review-evidence/SKILL.md | skill-lint-g2 | NO_CRITICAL | NO_CRITICAL |  |
| skills/codex-workitem-coordination/SKILL.md | skill-lint-g2 | NO_CRITICAL | NO_CRITICAL |  |
| skills/collaboration-patterns/SKILL.md | skill-lint-g2 | NO_CRITICAL | NO_CRITICAL |  |
| skills/complete-work-item-direct-main/SKILL.md | skill-lint-g2 | NO_CRITICAL | NO_CRITICAL |  |
| skills/complete-work-item-feature-branch/SKILL.md | skill-lint-g2 | NO_CRITICAL | NO_CRITICAL |  |
| skills/composition-patterns/SKILL.md | skill-lint-g2 | NO_CRITICAL | NO_CRITICAL |  |
| skills/create-architecture/SKILL.md | skill-lint-g2 | NO_CRITICAL | NO_CRITICAL |  |
| skills/create-azure-devops-work-item/SKILL.md | skill-lint-g2 | NO_CRITICAL | NO_CRITICAL |  |
| skills/create-file-work-item/SKILL.md | skill-lint-g2 | NO_CRITICAL | NO_CRITICAL |  |
| skills/create-functional-spec/SKILL.md | skill-lint-g2 | NO_CRITICAL | NO_CRITICAL |  |
| skills/create-github-work-item/SKILL.md | skill-lint-g2 | NO_CRITICAL | NO_CRITICAL |  |
| skills/create-gitlab-work-item/SKILL.md | skill-lint-g2 | NO_CRITICAL | NO_CRITICAL |  |
| skills/create-high-level-design/SKILL.md | skill-lint-g2 | NO_CRITICAL | NO_CRITICAL |  |
| skills/create-jira-work-item/SKILL.md | skill-lint-g3 | NO_CRITICAL | NO_CRITICAL |  |
| skills/create-module-design/SKILL.md | skill-lint-g3 | NO_CRITICAL | CONFIRMED_CRITICAL | backlog/defect-backlog/align-module-design-mandatory-heading-contract.md |
| skills/create-project-configuration/SKILL.md | skill-lint-g3 | NO_CRITICAL | NO_CRITICAL |  |
| skills/create-pull-request/SKILL.md | skill-lint-g3 | NO_CRITICAL | NO_CRITICAL |  |
| skills/create-unit-test-plan/SKILL.md | skill-lint-g3 | NO_CRITICAL | NO_CRITICAL |  |
| skills/detect-technology-skills/SKILL.md | skill-lint-g3 | CRITICAL | CONFIRMED_CRITICAL | backlog/defect-backlog/make-technology-detector-fallback-prerequisites-executable.md |
| skills/development-methodology/SKILL.md | skill-lint-g3 | NO_CRITICAL | NO_CRITICAL |  |
| skills/documentation-bootstrap/SKILL.md | skill-lint-g3 | CRITICAL | NO_CRITICAL |  |
| skills/documentation-page-verify/SKILL.md | skill-lint-g3 | NO_CRITICAL | NO_CRITICAL |  |
| skills/documentation-reverse-engineer/SKILL.md | skill-lint-g3 | NO_CRITICAL | NO_CRITICAL |  |
| skills/effective-communication/SKILL.md | skill-lint-g3 | NO_CRITICAL | NO_CRITICAL |  |
| skills/electron-main/SKILL.md | skill-lint-g3 | NO_CRITICAL | NO_CRITICAL |  |
| skills/electron-preload/SKILL.md | skill-lint-g3 | NO_CRITICAL | NO_CRITICAL |  |
| skills/end-to-end-verification/SKILL.md | skill-lint-g3 | CRITICAL | CONFIRMED_CRITICAL | backlog/defect-backlog/end-to-end-verification-commit-authority.md |
| skills/fastapi/SKILL.md | skill-lint-g3 | NO_CRITICAL | NO_CRITICAL |  |
| skills/fix-explanation/SKILL.md | skill-lint-g4 | CRITICAL | CONFIRMED_CRITICAL | backlog/defect-backlog/align-fix-explanation-item-taxonomy.md |
| skills/hibernate-orm-panache/SKILL.md | skill-lint-g4 | NO_CRITICAL | NO_CRITICAL |  |
| skills/interface-patterns/SKILL.md | skill-lint-g4 | NO_CRITICAL | NO_CRITICAL |  |
| skills/interpreter-pattern/SKILL.md | skill-lint-g4 | NO_CRITICAL | NO_CRITICAL |  |
| skills/java-comment/SKILL.md | skill-lint-g4 | NO_CRITICAL | NO_CRITICAL |  |
| skills/java-design-pattern-examples/SKILL.md | skill-lint-g4 | NO_CRITICAL | NO_CRITICAL |  |
| skills/java-design/SKILL.md | skill-lint-g4 | NO_CRITICAL | NO_CRITICAL |  |
| skills/java/SKILL.md | skill-lint-g4 | NO_CRITICAL | NO_CRITICAL |  |
| skills/jest/SKILL.md | skill-lint-g4 | CRITICAL | CONFIRMED_CRITICAL | backlog/defect-backlog/bound-jest-failure-ownership-to-current-change.md |
| skills/jhipster-domain-modeling/SKILL.md | skill-lint-g4 | NO_CRITICAL | NO_CRITICAL |  |
| skills/jhipster-persistence/SKILL.md | skill-lint-g4 | NO_CRITICAL | NO_CRITICAL |  |
| skills/jhipster-project/SKILL.md | skill-lint-g4 | NO_CRITICAL | NO_CRITICAL |  |
| skills/jhipster-security/SKILL.md | skill-lint-g4 | NO_CRITICAL | NO_CRITICAL |  |
| skills/jhipster-testing/SKILL.md | skill-lint-g4 | NO_CRITICAL | NO_CRITICAL |  |
| skills/junit/SKILL.md | skill-lint-g4 | NO_CRITICAL | NO_CRITICAL |  |
| skills/langgraph/SKILL.md | skill-lint-g5 | NO_CRITICAL | NO_CRITICAL |  |
| skills/liquibase/SKILL.md | skill-lint-g5 | CRITICAL | NO_CRITICAL |  |
| skills/local-model-integration/SKILL.md | skill-lint-g5 | NO_CRITICAL | NO_CRITICAL |  |
| skills/maintain-methodology-documentation/SKILL.md | skill-lint-g5 | CRITICAL | CONFIRMED_CRITICAL | backlog/defect-backlog/separate-distributed-methodology-from-repository-maintenance.md |
| skills/manage-azure-devops-work-items/SKILL.md | skill-lint-g5 | NO_CRITICAL | NO_CRITICAL |  |
| skills/manage-file-work-items/SKILL.md | skill-lint-g5 | CRITICAL | CONFIRMED_CRITICAL | backlog/defect-backlog/respect-resource-coordination-none-in-manage-file-work-items.md |
| skills/manage-github-work-items/SKILL.md | skill-lint-g5 | NO_CRITICAL | NO_CRITICAL |  |
| skills/manage-gitlab-work-items/SKILL.md | skill-lint-g5 | NO_CRITICAL | NO_CRITICAL |  |
| skills/manage-jira-work-items/SKILL.md | skill-lint-g5 | NO_CRITICAL | NO_CRITICAL |  |
| skills/mapstruct/SKILL.md | skill-lint-g5 | NO_CRITICAL | NO_CRITICAL |  |
| skills/mockito/SKILL.md | skill-lint-g5 | NO_CRITICAL | NO_CRITICAL |  |
| skills/mysql/SKILL.md | skill-lint-g5 | NO_CRITICAL | CONFIRMED_CRITICAL | backlog/defect-backlog/bound-mysql-production-verification-to-safe-targets.md |
| skills/name-methodology-artifacts/SKILL.md | skill-lint-g5 | NO_CRITICAL | NO_CRITICAL |  |
| skills/nextjs-app-router/SKILL.md | skill-lint-g5 | NO_CRITICAL | NO_CRITICAL |  |
| skills/node-cli/SKILL.md | skill-lint-g5 | NO_CRITICAL | NO_CRITICAL |  |
| skills/object-creation-patterns/SKILL.md | skill-lint-g6 | NO_CRITICAL | NO_CRITICAL |  |
| skills/organise-project-files/SKILL.md | skill-lint-g6 | NO_CRITICAL | NO_CRITICAL |  |
| skills/plan-engine/SKILL.md | skill-lint-g6 | NO_CRITICAL | NO_CRITICAL |  |
| skills/playwright/SKILL.md | skill-lint-g6 | NO_CRITICAL | NO_CRITICAL |  |
| skills/postgres-drizzle/SKILL.md | skill-lint-g6 | NO_CRITICAL | NO_CRITICAL |  |
| skills/project-wiki-create/SKILL.md | skill-lint-g6 | CRITICAL | CONFIRMED_CRITICAL | backlog/defect-backlog/make-project-wiki-template-resolution-install-portable.md |
| skills/project-wiki-query/SKILL.md | skill-lint-g6 | NO_CRITICAL | NO_CRITICAL |  |
| skills/project-wiki-research/SKILL.md | skill-lint-g6 | NO_CRITICAL | NO_CRITICAL |  |
| skills/project-wiki-review/SKILL.md | skill-lint-g6 | NO_CRITICAL | NO_CRITICAL |  |
| skills/project-wiki-topic-verify/SKILL.md | skill-lint-g6 | CRITICAL | CONFIRMED_CRITICAL | backlog/defect-backlog/project-wiki-topic-verify-read-only-helper-resolution.md |
| skills/project-wiki-topic-write/SKILL.md | skill-lint-g6 | CRITICAL | CONFIRMED_CRITICAL | backlog/defect-backlog/project-wiki-topic-write-role-owned-verification.md |
| skills/project-wiki/SKILL.md | skill-lint-g6 | CRITICAL | CONFIRMED_CRITICAL | backlog/defect-backlog/project-wiki-role-routing-and-operation-paths.md |
| skills/prompt-contracts/SKILL.md | skill-lint-g6 | NO_CRITICAL | NO_CRITICAL |  |
| skills/python-design-pattern-examples/SKILL.md | skill-lint-g6 | NO_CRITICAL | NO_CRITICAL |  |
| skills/python/SKILL.md | skill-lint-g6 | NO_CRITICAL | NO_CRITICAL |  |
| skills/quarkus-design/SKILL.md | skill-lint-g7 | NO_CRITICAL | NO_CRITICAL |  |
| skills/quarkus-persistence/SKILL.md | skill-lint-g7 | NO_CRITICAL | CONFIRMED_CRITICAL | backlog/defect-backlog/keep-quarkus-persistence-companion-selection-setup-owned.md |
| skills/quarkus-testing/SKILL.md | skill-lint-g7 | NO_CRITICAL | NO_CRITICAL |  |
| skills/quarkus/SKILL.md | skill-lint-g7 | NO_CRITICAL | NO_CRITICAL |  |
| skills/quartz/SKILL.md | skill-lint-g7 | NO_CRITICAL | NO_CRITICAL |  |
| skills/react-server-components/SKILL.md | skill-lint-g7 | CRITICAL | CONFIRMED_CRITICAL | backlog/defect-backlog/react-server-components-detection-boundary.md |
| skills/react-vite-renderer/SKILL.md | skill-lint-g7 | NO_CRITICAL | NO_CRITICAL |  |
| skills/request-patterns/SKILL.md | skill-lint-g7 | NO_CRITICAL | NO_CRITICAL |  |
| skills/review-architecture/SKILL.md | skill-lint-g7 | NO_CRITICAL | CONFIRMED_CRITICAL | backlog/defect-backlog/allow-typed-evidence-review-architecture.md |
| skills/review-functional-spec/SKILL.md | skill-lint-g7 | NO_CRITICAL | CONFIRMED_CRITICAL | backlog/defect-backlog/allow-typed-evidence-review-functional-spec.md |
| skills/review-high-level-design/SKILL.md | skill-lint-g7 | NO_CRITICAL | CONFIRMED_CRITICAL | backlog/defect-backlog/allow-typed-evidence-review-high-level-design.md |
| skills/review-module-design/SKILL.md | skill-lint-g7 | NO_CRITICAL | CONFIRMED_CRITICAL | backlog/defect-backlog/allow-typed-evidence-review-module-design.md |
| skills/review-structured-artifact/SKILL.md | skill-lint-g7 | NO_CRITICAL | NO_CRITICAL |  |
| skills/review-unit-test-plan/SKILL.md | skill-lint-g7 | NO_CRITICAL | CONFIRMED_CRITICAL | backlog/defect-backlog/allow-typed-evidence-review-unit-test-plan.md |
| skills/root-cause-analysis/SKILL.md | skill-lint-g7 | NO_CRITICAL | NO_CRITICAL |  |
| skills/runtime-evidence-collection/SKILL.md | skill-lint-g8 | NO_CRITICAL | NO_CRITICAL |  |
| skills/singleton-pattern/SKILL.md | skill-lint-g8 | NO_CRITICAL | NO_CRITICAL |  |
| skills/skill-authoring/SKILL.md | skill-lint-g8 | NO_CRITICAL | NO_CRITICAL |  |
| skills/spring-boot-design/SKILL.md | skill-lint-g8 | NO_CRITICAL | NO_CRITICAL |  |
| skills/spring-boot-testing/SKILL.md | skill-lint-g8 | NO_CRITICAL | NO_CRITICAL |  |
| skills/spring-boot/SKILL.md | skill-lint-g8 | NO_CRITICAL | NO_CRITICAL |  |
| skills/spring-data-jpa/SKILL.md | skill-lint-g8 | NO_CRITICAL | NO_CRITICAL |  |
| skills/sql/SKILL.md | skill-lint-g8 | NO_CRITICAL | NO_CRITICAL |  |
| skills/state-strategy-patterns/SKILL.md | skill-lint-g8 | NO_CRITICAL | NO_CRITICAL |  |
| skills/structured-design/SKILL.md | skill-lint-g8 | CRITICAL | CONFIRMED_CRITICAL | backlog/defect-backlog/replace-structured-design-chain-of-thought-output-contract.md |
| skills/structured-explanation/SKILL.md | skill-lint-g8 | NO_CRITICAL | NO_CRITICAL |  |
| skills/tailwind-design-system/SKILL.md | skill-lint-g8 | NO_CRITICAL | CONFIRMED_CRITICAL | backlog/defect-backlog/make-tailwind-companion-guidance-route-aware.md |
| skills/test-driven-development/SKILL.md | skill-lint-g8 | NO_CRITICAL | NO_CRITICAL |  |
| skills/test-strategy/SKILL.md | skill-lint-g8 | CRITICAL | CONFIRMED_CRITICAL | backlog/defect-backlog/stop-test-strategy-from-rerunning-technology-routing.md |
| skills/tool-runtime/SKILL.md | skill-lint-g8 | CRITICAL | CONFIRMED_CRITICAL | backlog/defect-backlog/prevent-sensitive-tool-runtime-log-and-trace-retention.md |
| skills/traversal-patterns/SKILL.md | skill-lint-g9 | NO_CRITICAL | NO_CRITICAL |  |
| skills/typescript-design-pattern-examples/SKILL.md | skill-lint-g9 | NO_CRITICAL | NO_CRITICAL |  |
| skills/typescript-esm/SKILL.md | skill-lint-g9 | CRITICAL | CONFIRMED_CRITICAL | backlog/defect-backlog/detect-typescript-esm-in-bundler-only-projects.md |
| skills/typescript-strict/SKILL.md | skill-lint-g9 | NO_CRITICAL | NO_CRITICAL |  |
| skills/typescript/SKILL.md | skill-lint-g9 | NO_CRITICAL | NO_CRITICAL |  |
| skills/user-experience-review/SKILL.md | skill-lint-g9 | NO_CRITICAL | CONFIRMED_CRITICAL | backlog/defect-backlog/stop-ux-review-runtime-technology-routing.md |
| skills/vitest/SKILL.md | skill-lint-g9 | NO_CRITICAL | NO_CRITICAL |  |

## Validation And Review Limits

- A fresh authoritative find inventory contains 127 unique paths and matches the final table exactly, including batch identity, raw outcome, and accepted disposition.
- The 27 accepted critical table rows match the 27 accepted defect sections exactly. All 27 accepted titles and slugs are present, and the slugs are unique.
- scripts/validate-agent-skills.py passed when invoked with all 127 authoritative SKILL.md paths.
- Raw output totals are 19 CRITICAL and 108 NO_CRITICAL. Accepted totals are 27 CONFIRMED_CRITICAL and 100 NO_CRITICAL.
- Every raw batch output returned READY, and no target was reported blocked or unreadable.
- skill-lint-g1 and skill-lint-g2 say validation passed; skill-lint-g3 reports targeted skill validation; skill-lint-g6 reports exact-target validation; skill-lint-g7 reports Agent Skill validation; skill-lint-g8 reports read-only validation for its 15 targets; skill-lint-g9 reports validate-agent-skills passed. skill-lint-g4 and skill-lint-g5 do not report exact-target validation.
- skill-lint-g1, skill-lint-g2, skill-lint-g4, skill-lint-g5, skill-lint-g7, and skill-lint-g9 explicitly report no provider-record mutation. skill-lint-g3, skill-lint-g6, and skill-lint-g8 do not explicitly make that provider statement; skill-lint-g6 reports a clean worktree and skill-lint-g8 reports read-only validation plus a clean worktree.
- skill-lint-g2 and skill-lint-g9 report temporary-directory limitations. skill-lint-g9 also reports a Python 3.9 tomllib limitation for broader tests.
- The independently accepted findings are source-contract judgments. This report does not reproduce every behavioral scenario named in their verification expectations.
- Provider references are authoritative record identities. The report does not treat any then-current Ready, Starting, Running, or User Action Required state as a durable final lifecycle conclusion.

## Definition Change Boundary

This report changes no skill definition, agent definition, metadata, detection source, reference, generated mirror, or provider record. It grants no mutation authority.

Any later change to a governed definition requires explicit scope-specific user approval and the repository pre-mutation check. Supported generated mirrors may be regenerated only from an approved canonical source and must never be edited directly. Detection-only corrections for React Server Components and TypeScript ESM remain outside this report’s mutation authority, including any separate policy decision about applying the definition checker to detection paths.
