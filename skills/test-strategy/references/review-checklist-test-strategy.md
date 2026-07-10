# Test Strategy Review Checklist

- Question: Do the selected checks cover the changed contract and its material risks?
- Question: Are success, invalid, failure, and state-transition paths covered where applicable?
- Question: Are test boundaries chosen from observable behavior rather than implementation arrangement?
- Question: Are doubles limited to owned external or nondeterministic boundaries?
- Question: Are fixtures, clocks, global state, and cleanup controlled?
- Question: Are focused and broader commands reported with their actual outcomes?
- Question: Are skipped checks and environment blockers distinct from passing checks?
- Question: Does the remaining risk match the evidence that was actually collected?
