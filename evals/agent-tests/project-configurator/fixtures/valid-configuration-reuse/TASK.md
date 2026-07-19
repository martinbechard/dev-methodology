# Valid Configuration Reuse

Reconcile the existing PROJECT.yaml and harness guidance after worker-old moved to worker.

Preserve the existing project summary, Project Configurator role selection, Python loadout, most-specific route precedence, verification command, privacy boundary, and thin Claude bridges. Update stale project-relative worker-old paths to worker. Move the nested AGENTS.md and CLAUDE.md guidance to worker and remove the stale copies.

The permitted output paths are PROJECT.yaml, AGENTS.md, CLAUDE.md, worker/AGENTS.md, worker/CLAUDE.md, worker-old/AGENTS.md, worker-old/CLAUDE.md, and eval-result.md. Keep README.md, available-skills.txt, worker/main.py, and worker/test_main.py unchanged.

Use available-skills.txt as the complete runtime-exposed skill catalog. Save eval-result.md with Skills Used, Evidence Packet, and Review Synthesis sections. Validate YAML, Markdown links, Python detection, tests, claims, the final diff, and the clean committed state.
