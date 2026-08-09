<!--
Copyright (c) 2026 Martin.Bechard@DevConsult.ca
Artifact-ID: 62e153bc-db4b-460f-af13-60ae0de9b9c3
Created-UTC: 2026-08-09T00:26:37Z
Creating-Agent: Dev Coder
Runtime: Codex
Dispatched-Model: gpt-5.6-sol
Reasoning-Effort: high
Task-ID: 019fe3cd-577c-76b1-965c-06fb8793ae42
Artifact-ID-Evidence: runtime-supplied
Created-UTC-Evidence: runtime-supplied
Creating-Agent-Evidence: runtime-supplied
Runtime-Evidence: runtime-supplied
Dispatched-Model-Evidence: runtime-supplied
Reasoning-Effort-Evidence: runtime-supplied
Task-ID-Evidence: runtime-supplied
-->

# Forms And Actions Page Checklist

| ID | Observable pass criterion | Required evidence |
| --- | --- | --- |
| DDS-FRM-001 | Every input, select, checkbox, and file input has a persistent visible label; every button has an explicit type and an action-specific accessible name. | Form-control/name inventory from source and accessibility tree. |
| DDS-FRM-002 | Catalog filters include labeled search, evidence-state select, harness select, and submit action; applying filters updates the result count as readable text. | DOM evidence and before/after interaction trace including result text. |
| DDS-FRM-003 | Text/email, file, checkbox, primary, secondary, and quiet-button examples render as the documented control families without using placeholders as labels. | Control-type/class inventory and screenshot. |
| DDS-FRM-004 | Invalid email submission identifies the field, exposes a specific correction through aria-describedby and role="alert", and does not reveal the alert while valid/inactive. | Invalid and valid interaction traces with DOM state and announced text. |
| DDS-FRM-005 | Successful completion exposes a role="status" message and programmatically moves focus to it when immediate announcement is required. | Keyboard interaction and active-element/live-region evidence. |
| DDS-FRM-006 | Every settings trigger exposes dialog semantics and expanded state; opening moves focus inside the named modal, Tab stays within it, Escape/Close closes it, and focus returns to the invoking trigger. | Full keyboard trace plus aria-haspopup, aria-controls, aria-expanded, dialog role, modal state, and label evidence. |
| DDS-FRM-007 | With JavaScript unavailable, a visible noscript warning states that static examples remain readable and interactive demonstrations do not run. | No-script render or source evidence plus static-content inspection. |
| DDS-FRM-008 | Fixture documentation distinguishes production patterns from four test-only sources and explicitly marks accessibility-defects.html as a negative example that must not be copied. | Visible fixture list, purposes, and warning text. |
| DDS-FRM-009 | The page does not send, persist, or upload entered demonstration data, and the footer states this boundary. | Network/storage observation during interactions plus exact footer text. |
