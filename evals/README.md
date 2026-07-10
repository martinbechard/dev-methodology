# Agent And Skill Evaluations

These synthetic projects exercise the canonical Coding Agent, Code Review Agent, model stages, and technology skills without customer data.

Each case contains:

- A small buildable project.
- A bounded implementation task.
- Required skill routing.
- Review-evidence identifiers.
- Baseline verification commands.

Run fixture verification with:

```bash
python3 scripts/run-agent-skill-evals.py --install
```

To evaluate an agent, copy one project to a disposable working directory, give the agent its TASK.md, and ask it to save eval-result.md. Then run:

```bash
python3 scripts/run-agent-skill-evals.py --case typescript-order-pricing --project-root /path/to/working-copy --result /path/to/working-copy/eval-result.md
```

The result must name the skills used, contain an evidence packet, contain review synthesis, and include every required evidence identifier from evals/cases.yaml. Review cases may also require specific findings and an intentionally failing verification command.

The checked evaluation record is in results/2026-07-09-live-agent-evaluations.md. Keep generated implementations in disposable working directories; retain only the reusable fixtures, evaluation contract, and result summary in this repository.
