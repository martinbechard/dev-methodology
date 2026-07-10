# Unit Test Plan Review Checklist

## Completion Format

For every question record:

- Status: pass, fail, question, or n/a.
- Question: copy the objective question.
- Quoted evidence: quote the exact artifact or source text.
- Assessment: explain the status from that evidence.

## Source And Scope

- Question: Does the plan identify the unit boundary and authoritative behavior, design, code, defect, and existing-test sources?
- Question: Are source conflicts recorded instead of silently resolved?
- Question: Does the plan avoid claiming exhaustive coverage when runtime or dependency behavior is unknown?

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

Report findings first. Treat missing authority, vague expected results, untraceable scenarios, unjustified doubles, and material coverage gaps as findings.
