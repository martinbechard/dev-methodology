# Eliminate Standalone Definition Approval Records

Status: Ready

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/eliminate-standalone-definition-approval-records.md

Completion: direct-main

## Summary

Remove the manually invoked definition-change approval checker and its duplicate standalone YAML inputs. Keep exact-scope user authorization durably in the canonical work item, and remove approval-record files from the repository root and the ignored `.codex/approval-records` directory.

## Context

The repository currently tracks 113 root files matching `approval-record-*.yaml`. Seven additional local records exist under the ignored `.codex/approval-records` directory. These files duplicate authorization evidence that the work-item contract already requires.

The command implemented by `scripts/render-agents-technology-skills.py` accepts `--check-definition-change`, `--approval-record`, and `--regenerated-from`. It validates a separately supplied YAML mapping but does not create approval, enforce filesystem mutation, authenticate provenance, own retention, archive records, or delete them. No repository contract defines a durable location or cleanup lifecycle for the standalone files. The README example passes a root-relative `approval-record.yaml`, and completed implementation commits have accumulated the inputs in the repository root.

The durable authority boundary remains necessary: changes to governed agent and skill definitions require explicit user direction for exact canonical paths, and additional governed paths require additional approval. The defect is the duplicate standalone-file and manually invoked checker mechanism, not the exact-scope authorization rule.

## Source Evidence

Direct user direction in Codex task `019faec9-c3ea-7d92-b350-6b21f091cb60` on 2026-07-29:

> "ok let's get rid of this garbage and delete the files in the root in the corresponding .codex subfolder. create a workitem to get rid of this and Record it in the workitem."

The direction followed a discussion in the same canonical task establishing that the checker is manually invoked by an implementation agent, is not a Git hook or CI enforcement mechanism, and duplicates approval evidence that belongs in the work item.

## Requirements

- Remove the standalone definition-change checker interface from `scripts/render-agents-technology-skills.py`, including `--check-definition-change`, `--approval-record`, and `--regenerated-from`, together with implementation that exists only to support those command paths.
- Remove instructions that require agents to create or pass standalone approval-record YAML files.
- Make the canonical work item's `Governed Definition Approval` section the durable record of exact approved governed paths, exact user wording, date, and user-message provenance.
- Preserve the rule that authorization is exact-path and explicit, and that any additional governed definition outside the work item's approved manifest requires additional user approval recorded in that work item before mutation.
- Preserve generated-mirror ownership rules and the prohibition against direct generated-definition edits.
- Delete every tracked root file matching `approval-record-*.yaml`.
- Delete every local file under `.codex/approval-records` and remove the empty directory when deletion is safe.
- Do not migrate the standalone YAML files elsewhere. Retain historical evidence through Git history and completed work-item records.
- Update `PROJECT.yaml`, generated `AGENTS.md` guidance, README documentation, templates, design output, and focused tests so they describe and enforce the work-item-native authority contract without referring to a standalone approval record or pre-mutation checker command.
- Add regression coverage that fails when a root `approval-record-*.yaml` file is tracked or when maintained guidance instructs agents to create standalone approval-record YAML.
- Keep approval evidence out of design principles and generated mirrors except where those outputs reproduce the approved steady-state work-item contract.

## Acceptance Criteria

- `git ls-files 'approval-record-*.yaml'` returns no paths.
- `.codex/approval-records` contains no files and is removed when empty.
- The renderer exposes none of `--check-definition-change`, `--approval-record`, or `--regenerated-from`.
- Maintained repository guidance contains no command or instruction requiring a standalone approval-record YAML file.
- A canonical work item can record exact governed-definition approval without creating a second approval artifact.
- The work-item contract still requires exact canonical governed paths, exact user direction, date, and provenance, and still blocks scope expansion without additional recorded user approval.
- Direct editing of generated definition mirrors remains prohibited and supported regeneration remains source-owned.
- Focused tests cover removal of the command interface, root-file hygiene, work-item-native approval evidence, additional-scope handling, and generated-mirror ownership.
- Relevant generated outputs are fresh and consistent with the two approved skill-definition sources.
- Independent review confirms that removal of the checker does not weaken the explicit exact-scope user-authorization boundary.

## Dependencies

None.

## Verification

- Run focused renderer tests proving that the removed command-line options are unavailable and ordinary rendering still works.
- Run focused work-item creation and coordination tests for exact-path approval recorded in the canonical item and additional-scope rejection.
- Run a repository-tree assertion that no tracked root path matches `approval-record-*.yaml`.
- Inspect `.codex/approval-records` and require zero remaining files after cleanup.
- Search maintained sources for `--approval-record`, `--check-definition-change`, standalone approval-record creation instructions, and obsolete checker outcomes.
- Regenerate only the supported outputs owned by the approved skill-definition sources and run their freshness checks.
- Run the directly affected bundle-content and technology-renderer tests.
- Run `git diff --check`.
- Obtain fresh independent code and methodology review of the exact-scope authorization boundary.

## Open Questions

None.

## Governed Definition Approval

### Governed Canonical Sources

- `skills/codex-workitem-coordination/SKILL.md`
- `skills/create-file-work-item/SKILL.md`

### Allowed Dependent Artifacts

- `PROJECT.yaml`
- `AGENTS.md`
- `README.md`
- `skills/development-methodology/assets/templates/file-work-item-template.md`
- `scripts/render-agents-technology-skills.py`
- `scripts/test_technology_detection.py`
- `scripts/test_codex_workitem_coordination.py`
- `scripts/test_bundle_content.py`
- `design/generated/skill-definitions.js`
- `generated/adapters/agent-generation-manifest.json`
- Generator-owned runtime adapter files whose conceptual agent definitions consume `codex-workitem-coordination` or `create-file-work-item`, but only when supported regeneration from either approved canonical skill source changes their generated bytes.
- Deletion of tracked root files matching `approval-record-*.yaml`.
- Deletion of local ignored files under `.codex/approval-records` and removal of that directory when empty.

### Approval Resolution

Approved at creation on 2026-07-29 by the direct user request in Codex task `019faec9-c3ea-7d92-b350-6b21f091cb60`: "ok let's get rid of this garbage and delete the files in the root in the corresponding .codex subfolder. create a workitem to get rid of this and Record it in the workitem."

This approval is limited to the two governed canonical skill-definition paths listed above and the dependent cleanup artifacts listed separately. It does not authorize changes to conceptual agent definitions, schemas, model profiles, skill metadata, adapter-owned skill definitions, or any additional distributed skill definition. Discovery of another governed canonical path requires new explicit user approval recorded in this work item before that path is mutated.

## Notes

This item authorizes cleanup delivery but does not perform it during work-item creation. Preserve unrelated working-tree and backlog state.
