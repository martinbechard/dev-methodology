# Publish Agent And Skill Evaluation HTML

Status: Running

Type: Feature

Provider: file

Provider Reference: backlog/feature-backlog/publish-agent-and-skill-evaluation-html.md

Completion: direct-main

## Delivery Execution / Ownership

- Owner: Dev Orchestrator
- Canonical task: 019f8b05-a1a0-70a1-bda7-0c93d28a28ba
- Artifact claim: Pending fresh artifact claim; the initial claim and both correction claims are released.
- Branch: codex/evaluation-html-resume-20260722
- Canonical worktree: /Users/martinbechard/.codex/worktrees/40a0/dev-methodology
- Starting main: e414fa04307d086321373e6bd090ae38a2d2177b
- Phase: parser normalization correction recovery.
- Candidate: 08d8154fcf14e02a30e749296fb992210e61d000 preserved; not accepted.
- Accepted commit: Pending.
- Claim wait started at: None.
- Claim wait attempts: 0.
- Integration wait started at: None.
- Integration wait attempts: 0.
- Completion wait started at: None.
- Completion wait attempts: 0.
- Open issues: The accepted parser/browser correction condition is now execution work; preserve the exact regression boundary.
- Shared-surface sequencing: Start on new unique evaluation documentation and data-generator surfaces; defer shared bundle and navigation paths until wake-up.
- Next owner: Dev Orchestrator.
- Delivery evidence: Candidate chain preserved; no browser verifier, integration, or completion evidence exists.

## Cold-Start Recovery Execution — 2026-07-22

- Lifecycle transition: Blocked -> Ready after reconciliation confirmed the recorded fresh-owner parser/browser correction condition was accepted for execution -> Running under fresh ownership.
- Canonical task identity: 019f8b05-a1a0-70a1-bda7-0c93d28a28ba.
- Backlog recovery claim: cold-start-backlog-reconcile-2-019f8b00, acquired event 66822334-e85a-41aa-b2ad-6a6c433b6798 from primary main.
- Recovery phase: parser normalization correction recovery.
- The blocker, exact unblock condition, candidate chain, review findings, and verification boundary below remain preserved.

## Phase Evidence Update — 2026-07-22

- Historical phase: Correction attempt 1 was active; acceptance remained pending.
- Candidate: df6911b3179bb82859ae25708ee4b09404a02af1, with a clean candidate worktree.
- Initial implementation claim release: Event b772d85a-b94e-469b-b216-ea7042aea478.
- Fresh review disposition: Both reviews reported CORRECTIONS REQUIRED.
- Review findings: Replace the high-risk ID-only historical/current semantic join and its no-probe abort; prevent duplicate and removed rows; remove the fixed timestamp and hardcoded narrative; correct verdict and Judge semantics; include omitted follow-ups and freshness inputs; and provide browser evidence.
- Correction attempt 1: Was active under claim publish-agent-skill-evaluation-html-correction-1-20260722 for exactly design/agent-and-skill-evaluations.html, design/agent-and-skill-evaluations.js, scripts/build-agent-skill-evaluation-docs.py, and scripts/test_agent_skill_evaluation_docs.py.
- Accepted commit: Pending.
- Next owner at that phase: Dev Orchestrator.

## Blocked Handoff — 2026-07-22

- Blocked reason: The bounded two-attempt correction loop is exhausted. Final methodology re-review found a recurring fail-open parser and completeness class.
- Remaining parser and completeness failure: Valid Markdown follow-up markers using * or + can be silently omitted, reformatted, or duplicated, reducing evidence without failure.
- Remaining priority-normalization failure: Raw YAML priority validation allows mixed scalar 1 and "1" values to pass before they collide after integer normalization.
- Preserved commit chain: df6911b3179bb82859ae25708ee4b09404a02af1 to 71102b36f729d2e3520d0a5575b6ea280cb53b36 to 08d8154fcf14e02a30e749296fb992210e61d000.
- Initial claim release: publish-agent-skill-evaluation-html-20260722 released, event b772d85a-b94e-469b-b216-ea7042aea478.
- Correction attempt 1 release: publish-agent-skill-evaluation-html-correction-1-20260722 released, event 4e75bc61-513f-4c02-9ba5-697aa7bacf3b.
- Correction attempt 2 release: publish-agent-skill-evaluation-html-correction-2-20260722 released, event a7d77293-839e-41e7-9728-c3be2584832e.
- Verification state: No browser verifier was run; no integration or work-item completion occurred.
- User-package mutation: None.
- Exact unblock: A fresh owner must add omission and duplicate regressions for * and + follow-up markers, add mixed-scalar priority duplicate rejection, correct parsing and normalization, then repeat fresh review, browser verification, and focused data reconciliation before integration.
- Owner: Unowned.
- Artifact claim: None.
- Accepted commit: Pending.

Creation Claim: create-eval-html-docs-item-20260722

## Summary

Publish source-backed HTML documentation that explains the skills and agents evaluation methodology, presents skill-by-skill and agent-by-agent results, and summarizes the governed evaluation state with reconciled global statistics.

## Context

The repository already maintains evaluation catalogs, agent-owned suites, runner and reporting code, and dated Markdown results under evals. The current documentation explains the methodology and records campaign results, but readers must navigate multiple source files to understand what was evaluated, how verdicts should be interpreted, and which skills or agents have direct evidence.

The HTML documentation must distinguish structural validation, agent suites, diagnostic skill probes, workflow evidence, deterministic Judges, Model Judges, Human Judge calibration, functional isolation, and security containment. It must not turn an unevaluated skill, a diagnostic probe, a blocked boundary, a manual observation, or an unavailable semantic Judge into a verified pass.

## Source Evidence

- On 2026-07-22, the user directly requested HTML documentation for the skills and agents evaluations, including the methodology, skill-by-skill results, agent-by-agent results, and global statistics.
- evals/README.md defines the evaluation layers, evidence boundaries, privacy controls, verdict distinctions, and catalog validation workflow.
- evals/skill-probes.yaml is the catalog for targeted skill diagnostics and explicitly does not represent exhaustive skill coverage.
- evals/agent-tests/suite-index.yaml and the suite directories define the agent-owned evaluation catalog.
- evals/agent-tests/results and evals/results contain governed reports and older observations with different evidence strength.
- design contains the repository's maintained HTML documentation and shared browser behavior.

## Requirements

- Add a maintained HTML documentation page under design for agent and skill evaluations and link it from the relevant existing design navigation surface.
- Begin with a methodology section that explains the evaluation layers, execution flow, evidence sources, Judge roles, verdict semantics, evidence strength, privacy boundary, disposable workspace model, and freshness rules in plain language.
- Identify the selected result campaign, its execution date or range, harness, source artifacts, and generation time so every displayed statistic has an explicit scope.
- Derive displayed inventories and results from authoritative repository sources rather than manually duplicating catalog entries or outcome totals in HTML.
- Provide global statistics that reconcile with the selected source evidence, including:
  - total bundled skills and total conceptual agents;
  - skills with direct probes or governed result evidence, skills with only indirect agent-suite coverage, and skills with no recorded evaluation evidence;
  - total agent suites and scenarios, with verdict totals and percentages;
  - catalog coverage, missing results, stale results, and result categories that are not eligible to count as verified passes;
  - harness and evidence-level breakdowns when those fields exist in the selected campaign.
- Provide one discoverable skill entry for every bundled skill. Each entry must show the available direct probes, linked cases or scenarios, latest governed outcome, evidence level, source links, and limitations. Show an explicit no direct evaluation evidence state instead of omitting a skill or inferring success from assignment to an agent.
- Provide one discoverable agent entry for every conceptual agent. Each entry must show its suite, scenarios, per-scenario verdicts, aggregate counts, evidence level, execution context, source links, and unresolved findings or follow-up items when recorded.
- Preserve the source meaning of PASS, FAIL, BLOCKED, manual observation, deterministic critical skip, Judge pass, calibration status, containment status, and missing evidence. Display these as separate dimensions where the source model keeps them separate.
- Support quick navigation, text search or filtering, and clear status legends across the methodology, global summary, skill entries, and agent entries.
- Keep the page usable at desktop and narrow viewport widths, with accessible headings, keyboard-operable controls, readable tables or cards, and status meaning that does not depend on color alone.
- Reuse the repository's shared HTML documentation conventions and settings behavior where applicable.
- Add deterministic generation or data-export support when needed, together with freshness validation that fails when the skill catalog, conceptual agent catalog, evaluation catalogs, or selected result schema changes without a corresponding documentation refresh.
- Keep tracked repository evidence authoritative. Do not make temporary directories, local absolute paths, unretained session files, or machine-specific artifacts the only support for a displayed result.
- Keep synthetic evaluation inputs and generated documentation free of personal, customer, company-confidential, credential, and secret material.
- Do not change a governed skill or agent definition as part of this item unless the exact canonical definition paths are separately approved through the repository's definition-change authority process.

## Acceptance Criteria

- A reader can open the HTML documentation and understand the evaluation methodology before interpreting any result.
- The global skill, agent, suite, scenario, and verdict totals reconcile exactly with the authoritative catalogs and selected governed result campaign.
- Every bundled skill has one visible entry, including a truthful explicit state when no direct probe or governed result exists.
- Every conceptual agent has one visible entry with its suite and all governed scenario outcomes, or an explicit missing-result state.
- Aggregate statistics can be traced to the skill and agent detail entries without double-counting indirect coverage or diagnostic probes.
- BLOCKED and unavailable semantic evidence are not presented as FAIL or PASS, and older manual observations are not presented as governed verification.
- The documentation exposes the selected campaign date, harness, evidence level, source references, and freshness state.
- Catalog or result drift causes a focused freshness check to fail rather than silently leaving stale HTML statistics.
- Navigation, filters, and any expandable detail remain keyboard operable and preserve understandable content when JavaScript is unavailable or fails.
- The page passes focused responsive, accessibility, link, generation-freshness, and data-reconciliation checks.

## Dependencies

None.

## Verification

- Validate the generated or embedded data against the complete skill inventory, conceptual agent inventory, skill-probe catalog, agent suite index, and selected result campaign.
- Assert that skill, agent, suite, scenario, and verdict aggregates equal the sum of their visible detail records.
- Test explicit no-evidence, missing-result, stale-result, BLOCKED, FAIL, PASS, manual-observation, and uncalibrated-Judge presentations.
- Run focused generator freshness and repository bundle tests for every changed documentation and evaluation-reporting surface.
- Run browser checks at desktop and narrow viewport widths, including keyboard navigation, filter behavior, JavaScript-disabled content, heading structure, focus visibility, and non-color status cues.
- Validate every tracked source link and confirm that no displayed claim depends only on a temporary or machine-specific artifact.
- Run git diff --check.
- Obtain an independent documentation and methodology review of the completed HTML, its source mapping, and its statistical reconciliation.

## Notes

- Skill probes are diagnostic controls within scenarios, not a requirement for one probe per assigned skill. The HTML must make that limitation visible while still listing every skill.
- The latest complete governed agent campaign is the default summary candidate, but implementation must select campaigns through explicit source metadata rather than filename ordering alone.
- Historical reports may be linked or offered as alternate views, but the global summary must identify one unambiguous selected campaign.
