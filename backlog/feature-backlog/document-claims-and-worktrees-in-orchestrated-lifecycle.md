# Document Claims And Worktrees In The Orchestrated Development Lifecycle

Status: Ready

Type: Feature

## Summary

Add a source-backed explanation of the repository claim and isolated-worktree mechanisms to design/orchestrated-development-lifecycle.html so readers can understand how orchestrated agents acquire ownership, separate concurrent work, integrate accepted contributions, update the backlog, and release cleanly.

## Context

The lifecycle page already names the claim gate, narrow ownership, isolated checkouts, integration resources, and clean release. It does not yet give readers one coherent explanation of the complete mechanism or show how the MCP server, distributed Agent Skill, claim engine, Git worktrees, and conceptual development agents cooperate.

The explanation must be verified against implemented source rather than reconstructed from examples or prior conversation. The primary sources include skills/agent-claim/SKILL.md, skills/agent-claim/scripts/claim.py, its focused tests, the current mcp-agent-ops tool schemas and behavior, README.md, and the conceptual definitions for Dev Orchestrator, Dev Backlog Steward, modifying agents, Dev Merge Coordinator, reviewers, and Dev Verifier. The sibling backlog item separate-project-and-backlog-claim-scopes changes the public scope model and must stabilize before this page describes the steady-state contract.

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
- Use a compact table, flow, or diagram only where it materially clarifies ownership transitions and concurrency. Preserve the page's current visual language, accessibility behavior, navigation, and relative-link conventions.
- Avoid duplicating the complete agent-claim procedure in HTML. Link to the authoritative skill and relevant generated agent catalog while explaining the system at the design level.
- Update other maintained source documentation only when verification finds a factual contradiction that must be resolved for the lifecycle page to be truthful. Regenerate derived artifacts from their owning sources rather than editing them manually.

## Acceptance Criteria

- A reader can identify which component owns claim policy, which interface executes claim operations, where authoritative coordination state lives, and when Git isolation is or is not allowed.
- The page correctly distinguishes narrow ownership, backlog-only lifecycle work, isolated contribution branches, shared-target integration, and final cleanup.
- Every named agent responsibility agrees with its current conceptual role definition and does not assign backlog, review, verification, or integration ownership to the wrong agent.
- Every named MCP operation, claim outcome, scope, worktree rule, and fallback boundary is supported by current source, current published tool schemas, or an explicitly labeled portability path.
- The page does not conflate a Codex task worktree with an acquired repository claim or imply that isolation resolves overlapping ownership.
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
- Record the implementation commit, independent documentation review, verification evidence, and any MCP version or capability limitation that affected the result.

## Notes

- Keep the explanation portable. Do not include local absolute paths, active claim identifiers, transient thread identifiers, or one machine's worktree names.
- Treat the MCP server as an execution interface and the agent-claim skill plus claim engine as the portable behavior contract; verify the exact boundary from current source before publishing that wording.
- Preserve the distinction between coordination evidence and agent transcripts. The claim registry and event journal do not become a store for prompts, reasoning, or arbitrary tool output.
