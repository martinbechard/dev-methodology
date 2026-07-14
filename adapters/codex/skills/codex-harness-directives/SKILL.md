---
name: codex-harness-directives
description: Apply Codex-specific safeguard and routing directives. Use when a generated Codex agent may create or modify repository files, launch subagents, or route work through Codex model profiles.
---

# Codex Harness Directives

This skill owns directives that apply to Codex-generated agents but do not belong in portable conceptual roles or cross-harness skills.

## Safeguard Routing

- Do not generate, delegate, retry, or split a prompt that asks a Sol-, Terra-, or Luna-backed Codex agent to perform cybersecurity work.
- If the current task or a planned delegation crosses that boundary, preserve completed work and return the routing requirement to the parent agent or user so a supported route can be selected.
- Treat an additional automated-safeguard check as a stop signal for that dispatch. Do not try to bypass it by rephrasing, fragmenting, or moving the same request to another affected agent.
- Do not infer or state that the safeguard notice itself means the user violated a policy. Report only the observed stop and the required routing change.

## Scope

- Apply these directives only in the Codex harness.
- Keep project instructions, role authority, skill procedures, and verification requirements unchanged.
- Do not copy these directives into provider-neutral role definitions or generated agents for other harnesses.
