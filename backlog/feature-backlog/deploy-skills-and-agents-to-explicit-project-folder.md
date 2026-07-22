# Deploy Skills And Agents To An Explicit Project Folder

Status: Ready

Type: Feature

Provider: file

Provider Reference: backlog/feature-backlog/deploy-skills-and-agents-to-explicit-project-folder.md

Completion: direct-main

Creation Claim: create-explicit-project-deployment-item-20260721

## Summary

Allow the skills and agents installer to accept an explicit project folder and deploy the selected adapter bundle there instead of using user-level destinations or requiring the caller to change the current working directory.

## Context

The installer currently supports user and project scopes. User scope derives destinations from the user home directory. Project scope derives skill, agent, MCP configuration, and workspace-root paths from the current working directory. The internal destination helper can already accept a project root, but the command-line interface does not expose that choice and other project-scoped path derivation still reads the current working directory directly.

This makes deployment to another project awkward and error-prone: callers must change directories before invoking the installer, and a partial implementation could send skills, agents, MCP configuration, ownership manifests, or allowed workspace roots to different projects.

The user directly requested a backlog item to let the skills and agents deployer specify a project folder instead of deploying at user level.

## Source Evidence

- scripts/install-skills.py defines user and project scopes, but project scope defaults to Path.cwd() at the command boundary.
- scripts/install-skills.py already has an internal project_root parameter in default_destinations, showing that explicit-root destination derivation is compatible with the current design.
- README.md documents project deployment only for the current project.
- scripts/test_install_skills.py covers project-scope deployment by mocking Path.cwd(), not by passing a project folder through the public command interface.

## Requirements

- Add an explicit project-folder command option for project-scoped skill and agent deployment. Prefer the name --project-root unless repository CLI conventions establish a clearer name during implementation.
- Require project scope when the explicit project folder is supplied, and reject combinations whose destination ownership would be ambiguous.
- Preserve current project-scope behavior when the option is omitted: the current working directory remains the project root.
- Resolve the selected project folder once and use that same canonical root for every project-scoped default.
- Derive adapter-specific skill and native-agent destinations beneath the selected project folder.
- Derive the scoped Codex or Junie MCP configuration path beneath the selected project folder when installer-managed MCP configuration is enabled.
- Use the selected project folder as the default MCP workspace root unless the caller supplies explicit workspace roots.
- Keep explicit skill, agent, and MCP configuration destinations authoritative where the existing command contract permits them, while retaining one unambiguous project identity for remaining scoped defaults.
- Apply the same selected project root to install, replace, cleanup, ownership-manifest, remove-owned, dry-run, and rollback behavior.
- Validate that the selected project root exists and is a directory before staging or mutating any destination.
- Do not fall back to user-level destinations when an explicit project root was requested or when its validation fails.
- Support every adapter whose project-scope destinations are currently supported.
- Update command help, README deployment examples, and directly related installer documentation so a caller can deploy to a different project without changing directories.
- Before changing any governed skill or agent definition discovered during implementation, identify the exact canonical paths and obtain separate scope-specific user approval. The backlog request itself does not authorize governed-definition mutation.

## Acceptance Criteria

- A caller can invoke the installer from the methodology repository, specify another existing project folder, and install both skills and native agents into that project's adapter-specific directories.
- The resulting MCP configuration, catalog paths, detection-registry path, and default allowed workspace root all refer to the selected project rather than the invocation directory or user home.
- The destination ownership manifests record the deployed artifacts under the selected project directories and retain the durable methodology source identity.
- Omitting the explicit project folder with project scope preserves current-working-directory behavior.
- Supplying the project folder with user scope, an invalid scope combination, a missing path, or a non-directory path fails before any destination or configuration is changed.
- Explicit destination overrides retain their documented precedence without causing the remaining generated paths to switch to another project root.
- Dry-run reports the same resolved project paths that a real deployment would use and performs no mutation.
- Refresh, cleanup, remove-owned, staging failure, and rollback operate only within the selected project and preserve unowned or customized content according to the existing installer contract.
- Focused tests cover Codex, Junie, Claude, Gemini, and generic adapter destination derivation where applicable, plus MCP configuration behavior for Codex and Junie.
- User-level deployment behavior remains unchanged.

## Dependencies

None.

## Verification

- Add command-parser and destination-resolution tests for an explicit absolute and relative project root.
- Add focused install and dry-run tests proving the invocation directory remains untouched while the selected project receives skills and agents.
- Add Codex and Junie tests for MCP configuration path, installed skill root, detection registry, and default workspace root under the selected project.
- Add rejection tests for user scope, missing paths, non-directory paths, and ambiguous explicit-destination combinations, asserting zero mutation.
- Re-run focused ownership, cleanup, remove-owned, staged transaction, and rollback tests against an explicit project root.
- Run the installer help and README content assertions affected by the new option.
- Run the applicable installer regression suite, Python compilation or static checks required by the repository, and git diff --check.
- Obtain an independent review of the command contract, path containment, rollback safety, documentation, and focused tests before direct-main completion.

## Notes

- This item exposes a project root through the public deployment interface; it does not change the adapter-specific directory names.
- This item does not make project deployment the default and does not authorize automatic deployment during ordinary repository maintenance.
- Project-scoped installation should remain an explicit caller action with a caller-supplied target.
