# Document Claims And Worktrees In The Orchestrated Development Lifecycle

Status: Completed

Type: Feature

## Running Ownership

- Owner: Dev Orchestrator root task 019f77f4-c4bd-7c91-b197-c987a7beb838.
- Lifecycle agent: Dev Backlog Steward.
- Lifecycle claim: claims-worktrees-lifecycle-docs-start.
- Claim evidence: PRIMARY backlog-domain ownership acquired at event 2219ef6c-3d26-4861-a753-d5dacd76b6c5 from clean baseline commit 8a791b095e569dc82aa445ee0c6e5929a862439e.
- Resume evidence: the earlier WAIT event f22d7daa-3980-47b1-a47d-d9cc603cb1bb was resolved by direct release event 2f64856c-f22e-4da2-a1fd-6c65a6db494b and an evidence-bearing wake-up from the parent coordinator.
- Scope boundary: this claim owns only the Running transition and is released after its clean commit. Documentation, tests, browser resources, review, verification, integration, and terminal backlog archival require separate ownership.

## Completion Evidence

- Running lifecycle: Dev Backlog Steward committed the Running transition as 5dff3ae0d89856db6f33b03f7fce47e6efc35065 and released claim claims-worktrees-lifecycle-docs-start normally at event 91be7391-07bc-40ee-a33e-10ee7ebe1d80.
- Accepted source handoff: archive-reference contribution 9e74c89709769e5f786e1091f54de045eba39b1e was integrated as the distinct provenance-bearing commit 9543d3ba0ef89431ab04bce1bd3a4937b1da65cf. Its existing archive assertion method and the new lifecycle assertion method do not overlap.
- Documentation artifact: commits 2c78978, e18727a, ae268ef, and faba3cd added the ownership topology, three communication sequences, responsive theme behavior, accessible directions, exact child-claim lineage, optional isolation base behavior, recovery checkpoints, and long-work heartbeat semantics. The final tree is byte-identical to the independently reviewed and verified pre-release tree fc42169fd43f14314f7ea6947c3bfb2d3b86ad29.
- Governed claim release: artifact claim claims-worktrees-lifecycle-docs-artifact acquired canonical isolation at event 9b6e4ad6-433a-4ec3-9086-529459d2514f. Release audit event 6f85a5c1-59aa-4fe4-9f69-1d315a72ba20 correctly rejected merge ancestry that exposed out-of-domain backlog commits; the contribution chain was rebuilt from baseline 3929018b136fb093e9633c2394448f7e122f48b4 without content changes, then released normally at event fdd80030-d537-44d9-be5d-d38b294d1361. Resource-only root claim claims-worktrees-lifecycle-docs-root released without repository changes at event 631165c8-d44b-459a-a7f3-25155958c390.
- Browser and accessibility verification: the lifecycle page rendered without page or section overflow at 1220, 820, 375, and 320 CSS pixels. Four labelled figures, three ordered sequences, 33 message rows, 26 sends-to labels, seven exchanges-with labels, unique identifiers, ordered headings, named links, dark-mode tokens, reduced-motion handling, and console-clean rendering were verified. Relevant light and dark text pairs met WCAG AA contrast, with a measured minimum of 5.17:1 in the independent verifier pass.
- Independent review: fresh methodology and visual/accessibility reviewers accepted the corrected contribution and again accepted integrated main with no findings. The review confirmed that the ownership topology and three communication sequences have distinct purposes and agree with the claim skill, claim engine, README, conceptual role contracts, and live MCP schemas.
- Final verification: focused lifecycle, archive-reference, ownership, and claim-engine checks passed; all 450 scripts tests passed on the contribution and again on integrated main. Static HTML verification resolved all 13 local links and fragments with no duplicate identifiers or missing accessible labels. Final post-integration Dev Verifier result was PASS with no findings.
- Integration and cleanup: Dev Merge Coordinator integrated the accepted chain on main as c50233b73a9097872cae9760037895e6f404a715, removed only the clean released and fully integrated claims-worktrees lifecycle worktree, and released claim claims-worktrees-lifecycle-docs-main-integration normally at event 75f5cdce-51ca-4d76-9d6d-7378a3abe93b.
- Terminal lifecycle ownership: Dev Backlog Steward acquired PRIMARY claim claims-worktrees-lifecycle-docs-terminal at event 8a3aa7e6-5cd7-4b7e-9674-4e9e86a7dca8 from clean baseline c50233b73a9097872cae9760037895e6f404a715. The claim is released immediately after this completed-feature archive commit is validated and clean.

## Summary

Add a source-backed explanation of the repository claim and isolated-worktree mechanisms to design/orchestrated-development-lifecycle.html so readers can understand how orchestrated agents acquire ownership, separate concurrent work, integrate accepted contributions, update the backlog, and release cleanly.

## Context

The lifecycle page already names the claim gate, narrow ownership, isolated checkouts, integration resources, and clean release. It does not yet give readers one coherent explanation of the complete mechanism or show how the MCP server, distributed Agent Skill, claim engine, Git worktrees, and conceptual development agents cooperate.

The explanation must be verified against implemented source rather than reconstructed from examples or prior conversation. The primary sources include skills/agent-claim/SKILL.md, skills/agent-claim/scripts/claim.py, its focused tests, the current mcp-agent-ops tool schemas and behavior, README.md, and the conceptual definitions for Parent Backlog Coordinator, Dev Orchestrator, Dev Backlog Steward, modifying agents, Dev Merge Coordinator, reviewers, and Dev Verifier. The sibling backlog item separate-project-and-backlog-claim-scopes stabilized the public scope model and completed at commit db82749e28b51f2cb9281e52b4d3ec587888e70a. The accepted codex-workitem-coordination skill and backlog-agent role contract provide the source for Codex task communication and wake-up behavior when that work is authorized and available.

## Requirements

- Add a dedicated claims and worktrees section to design/orchestrated-development-lifecycle.html and keep the existing lifecycle table consistent with it.
- Explain that repository-global claim state is authoritative across linked Git worktrees and identify the live registry and event journal concept without embedding machine-specific paths.
- Describe the supported ownership forms, atomic acquisition and extension, contention, recovery, heartbeat, clean committed release, and explicit no-change release using the exact names and outcomes implemented at completion time.
- Explain that Codex and Junie use the mcp-agent-ops claim tools as the preferred deterministic interface when available, while the agent-claim skill owns the portable workflow and its bundled command is a fallback only for the transport and capability cases permitted by that skill.
- State that structured coordination outcomes such as PRIMARY, ISOLATE, WAIT, PRIMARY_REQUIRED, ISOLATE_REQUIRED, and RECOVERY_REQUIRED are workflow states rather than generic tool failures, using only outcomes still present in the verified implementation.
- Explain how eligible non-overlapping concurrent writers receive isolated Git worktrees beneath the primary worktree's ignored .worktrees directory, how the claim identifier determines the checkout directory, how sparse checkout treats the primary-only backlog, and why conflicting scopes still wait instead of using isolation to bypass overlap.
- Distinguish claim-created isolated worktrees from any runtime or application-level task worktree so the page does not imply that thread creation alone grants repository ownership.
- Explain that separate worktrees can commit independently, while integration into a shared target branch requires a target-specific integration resource and deliberate ownership.
- Describe the agent responsibilities from the current conceptual definitions: Dev Orchestrator coordinates root ownership and handoffs; producing agents own their narrow mutation lanes; Dev Merge Coordinator owns multi-contribution integration; Dev Backlog Steward owns brief lifecycle mutations through the configured backend; reviewers remain read-only unless mutation is separately authorized; and Dev Verifier owns verification resources required by its checks.
- Make the backlog boundary explicit: backlog lifecycle ownership is primary-worktree-only, must remain separate from project-artifact ownership, and must be released immediately after the narrow lifecycle update so it does not block project claims.
- Show the successful lifecycle from inspection through claim, isolated contribution when required, review, verification, integration, backlog finalization, claim release, and safe clean-worktree removal. Also show the stop conditions for overlap, dirty anonymous state, missing authority, and incomplete handoff evidence.
- Add an accessible communication sequence for normal backlog intake through READ-ONLY PREFLIGHT, LIFECYCLE START, a brief primary claim and release, ARTIFACT GO, isolated production, independent review, Dev Verifier, direct completion or Dev Merge Coordinator target-specific integration, and the terminal Dev Backlog Steward claim.
- Add an accessible communication sequence for WAIT or PRIMARY_REQUIRED through ARTIFACT WAIT, current-owner commit and release notice, the parent coordinator's evidence-bearing baton handoff, and ARTIFACT RESUME. Show that the waiting task stops without polling and that Codex task status is not delivery evidence.
- Add an accessible communication sequence showing several serialized primary-only backlog batons followed by concurrent non-overlapping isolated artifact lanes. Keep generators, browsers and ports, verification, target integration, and claim contention behind explicit resources and adaptive parent dispatch.
- Include Parent Backlog Coordinator, Dev Orchestrator task, Dev Backlog Steward, artifact producer, independent reviewer, Dev Verifier, Dev Merge Coordinator, the claim MCP server and repository-global registry, and Codex task wake-up messaging as distinct actors where they participate.
- Keep these communication sequences on this lifecycle page rather than duplicating them in the codex-workitem-coordination skill documentation.
- Use a compact table, flow, or diagram only where it materially clarifies ownership transitions and concurrency. Preserve the page's current visual language, accessibility behavior, navigation, and relative-link conventions.
- Avoid duplicating the complete agent-claim procedure in HTML. Link to the authoritative skill and relevant generated agent catalog while explaining the system at the design level.
- Update other maintained source documentation only when verification finds a factual contradiction that must be resolved for the lifecycle page to be truthful. Regenerate derived artifacts from their owning sources rather than editing them manually.

## Acceptance Criteria

- A reader can identify which component owns claim policy, which interface executes claim operations, where authoritative coordination state lives, and when Git isolation is or is not allowed.
- The page correctly distinguishes narrow ownership, backlog-only lifecycle work, isolated contribution branches, shared-target integration, and final cleanup.
- Every named agent responsibility agrees with its current conceptual role definition and does not assign backlog, review, verification, or integration ownership to the wrong agent.
- Every named MCP operation, claim outcome, scope, worktree rule, and fallback boundary is supported by current source, current published tool schemas, or an explicitly labeled portability path.
- The page does not conflate a Codex task worktree with an acquired repository claim or imply that isolation resolves overlapping ownership.
- The three communication sequences use the exact implemented claim outcomes and coordination phases, expose the evidence carried by every baton and wake-up, and remain understandable through accessible text alternatives without color or animation.
- Existing lifecycle content contains no contradictory or stale claim and worktree statements after the new section is added.
- Relative links resolve, the HTML remains usable at narrow and wide viewport sizes, and its heading, table, focus, contrast, and reduced-motion behavior remain accessible.
- Repository validation and focused claim-engine tests pass from the required Python version, and any unavailable live MCP verification is reported explicitly rather than inferred.

## Dependencies

- separate-project-and-backlog-claim-scopes

## Verification

- Compare every factual statement with skills/agent-claim/SKILL.md, the claim engine implementation, focused claim tests, README.md, and the applicable conceptual agent definitions.
- Inspect the live or published mcp-agent-ops claim tool descriptions and schemas. Exercise representative operations in a disposable Git repository when the verification boundary permits it, including primary ownership, eligible isolation, overlap waiting, primary-only backlog behavior, recovery, release, and clean worktree removal.
- Run the focused claim-engine and bundle-content tests before the full repository validation commands required by AGENTS.md.
- Run the repository checks for generated documentation and adapters so the maintained page agrees with source-owned representations.
- Run the HTML page verification workflow, resolve every relative link, and inspect the rendered page at representative desktop and narrow viewport sizes.
- Inspect the three communication sequences at narrow, standard, and desktop widths, in light and dark presentation, with keyboard navigation, zoom, reduced motion, readable labels, and accessible alternatives.
- Record the implementation commit, independent documentation review, verification evidence, and any MCP version or capability limitation that affected the result.

## Notes

- Keep the explanation portable. Do not include local absolute paths, active claim identifiers, transient thread identifiers, or one machine's worktree names.
- Treat the MCP server as an execution interface and the agent-claim skill plus claim engine as the portable behavior contract; verify the exact boundary from current source before publishing that wording.
- Preserve the distinction between coordination evidence and agent transcripts. The claim registry and event journal do not become a store for prompts, reasoning, or arbitrary tool output.
