# Migration Review: Creating Procedure Rules Documents

## Source

[Legacy procedure](../procedure-create-procedure.md) defines how to create project procedure-rule documents. This review compares it with the live skill catalog, canonical roles, and repository maintenance contract.

## Durable Guidance

- Ground a procedure in identified primary inputs and do not invent requirements.
- State one concrete rule at a time in direct language; preserve the reason that supports the exact assertion.
- Select the document shape from the user request and existing project conventions, keep Markdown readable, and link supporting sources where claims depend on them.
- Review a custom procedure from its evidence before treating it as complete.

## Mapping And Coverage

| Legacy point | Live destination | Coverage | Action |
| --- | --- | --- | --- |
| Identify inputs and extract only supported rules | [development-methodology](../../skills/development-methodology/SKILL.md) workflow; [documentation-page-verifier](../../skills/documentation-page-verifier/SKILL.md) source checks | Covered | Keep current source-backed workflow. |
| Direct, atomic rules and reasons tied to their immediate parent | [structured-design](../../skills/structured-design/SKILL.md) required discipline | Covered | Keep; it is clearer and less prescriptive than the legacy tree syntax. |
| Markdown structure, selected format, links, and useful examples | development-methodology workflow and documentation-page-verifier format checks | Covered | Keep format selection authoritative rather than imposing one procedure layout. |
| Review and iterate with evidence | [review-structured](../../skills/review-structured/SKILL.md) and documentation-page-verifier | Covered | Use the verifier for custom procedure documents. |
| Consistent meaning of MUST, SHOULD, and MAY | structured-design | Missing | Add the narrow rule below. |
| Record the authoritative inputs used to create a standalone rules document | structured-design | Partly covered | Add the narrow rule below. |
| Where repo-local procedures belong | [AGENTS.md](../../AGENTS.md) | Covered | Keep long repo-local guidance in a root procedure file linked from AGENTS.md; do not make it a distributed skill. |

## Exact Suggested Additions

Add these two bullets under Structured Design, Required Discipline:

- For a rules document, use MUST or MUST NOT only for unconditional obligations, SHOULD or SHOULD NOT for recommendations with contextual exceptions, and MAY for permission.
- When writing a standalone procedure or rules document, name the authoritative inputs or link them at the point where the rule set depends on them.

These additions are reusable outside this repository, compact, and compatible with the existing source-link and immediate-BECAUSE discipline.

## Omits

Do not retain the mandatory RULE prefix, sequential rule numbering, mandatory BECAUSE for every rule, mandatory five-level reasoning, ASCII tree characters, fixed procedure-topic-rules filename, or wiki-link syntax. The current catalog correctly lets the selected artifact format govern these presentation choices; Structured Design already limits rationale to what is useful and directly supportive.

Do not create a procedure-authoring skill or agent. A repository procedure is normally local guidance under AGENTS.md, while portable documentation work is already routed by development-methodology and verified by documentation-page-verifier.

## Conclusion

Keep the legacy procedure as historical input only. Retain its evidence, atomicity, and rationale principles through the existing skills; make the two small Structured Design additions above. No new skill or canonical agent is recommended.
