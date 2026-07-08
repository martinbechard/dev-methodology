# Project Wiki Source Priority

Use this priority order when reconciling wiki content:

1. Code and tests describe actual behavior.
2. Functional specifications and requirements describe intended behavior.
3. AGENTS.md, README files, and procedure files describe workflow obligations.
4. Defect and feature backlog files describe tracked work. Status headings or explicit status fields determine whether an item is open, fixed, completed, or otherwise closed.
5. Architecture and plan documents describe design intent.
6. Help, RAG, or generated documentation describes the current documentation and retrieval surface.
7. docs/wiki pages summarize and navigate the above sources.

## Conflict Handling

- If the wiki conflicts with a higher-priority source, update the wiki.
- If code conflicts with a specification, record the conflict in Open Questions and treat it as implementation drift.
- If backlog file presence conflicts with an internal status heading or status field, trust the internal status.
- If source documents disagree and the correct answer is unclear, preserve the contradiction in Open Questions instead of inventing a resolution.
