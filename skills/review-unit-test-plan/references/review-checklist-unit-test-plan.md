# Unit Test Plan Review Checklist

## Completion Format

For every question record:

- Status: pass, fail, question, or n/a.
- Question: copy the objective question being answered.
- Evidence type: exact quotation, summary, assessment, or not applicable.
- Evidence source: name the plan, authority source, checklist, or retained response used.
- Evidence: record exact source text for an exact quotation, or clearly labeled summary or derived assessment text.
- Assessment: explain why the evidence passes, fails, is unclear, or is not applicable.

Do not mark pass without evidence. Every exact quotation must occur in the named source after CRLF and LF normalization. The literal [omitted] marker may replace intervening text only when the retained segments occur exactly and in order. When a source conflict or required text is absent, use assessment or summary evidence with the named sources instead of fabricating a quotation. Label paraphrased source meaning as summary and a derived absence, conflict, duplicate-test, or coverage finding as assessment. For n/a, record not applicable with a reason instead of inventing quoted evidence.

## Source And Scope

- Question: Does the plan identify the unit boundary and authoritative behavior, design, code, defect, and existing-test sources?
- Question: Are source conflicts recorded instead of silently resolved?
- Question: Does the plan avoid claiming exhaustive coverage when runtime or dependency behavior is unknown?
- Question: When source, test, fixture, snapshot, or configuration placement names three or more repository paths that share a prefix, or paths spanning two or more folders, does the plan present their placement in one or more fenced text trees with complete repository-relative root and package segments?
- Question: When a path tree would become large or separate test groups need different metadata, is it split into named component or ownership subsections with one small fenced text tree and adjacent metadata in each, without multiline table cells, simulated HTML breaks, repeated common-prefix lists, or one row per full path?

## Scenario Quality

- Question: Does every scenario state setup, action, observable expected result, and source traceability?
- Question: Do scenarios cover responsibilities, invariants, meaningful boundaries, state transitions, and errors?
- Question: Are non-applicable failure cases marked with a reason?
- Question: Are duplicate or implementation-detail tests avoided?

## Boundaries And Traceability

- Question: Are test doubles described by external boundary contract and purpose rather than a mandated library?
- Question: Does the coverage map connect every important responsibility and risk to scenarios or an explicit gap?
- Question: Does the plan identify relevant integration or end-to-end coverage that should not be duplicated as a unit test?

## Findings

Report findings first. Treat missing authority, vague expected results, untraceable scenarios, unjustified doubles, a missing or malformed required path tree, missing complete repository-relative tree segments, unsplit large trees, tree metadata separated from its owning tree, table-cell or HTML-simulated trees, duplicated full paths or common prefixes, and material coverage gaps as findings.
