---
name: effective-communication
description: Communicate clearly with users and other agents through plain language, concise evidence, explicit decisions, and actionable handoffs.
metadata:
  category: development-practice
---

# Effective Communication

Start with the outcome that matters to the recipient.

## Artifact Body Boundary

Use this skill for ordinary user and agent messages. It controls outcomes, evidence, blockers, decisions, next actions, approvals, and handoffs.

When a message contains a durable artifact body, let the artifact-specific writing method control its structure. Let ste-technical-writing control technical prose in that artifact body.

Do not convert descriptive artifact content into instructions, procedures, or status reports. Keep the surrounding message separate from the artifact body.

## Write Clearly

- Use familiar words.
- Keep sentences short.
- Put one rule or idea in each sentence.
- Use a technical term only when it names a real command, field, outcome, file, or resource.
- Explain a specialized or project-specific term when it first appears.
- Introduce a specific instance before later referring to it with “the.”
- Prefer a concrete example when it explains a structure or workflow better than an inventory.
- Use a list or table only when it makes repeated items, mappings, or choices easier to compare.
- Keep exact identifiers, paths, commits, claim references (identifiers for temporary ownership records), and error outcomes when the recipient needs them to act or verify.

For example, first write “A task result identifies the owner.” You may then write “The result also identifies the affected file.”

## Organize The Message

Separate these parts when they apply:

1. Outcome
2. Evidence
3. Blocker
4. Decision
5. Next action

Omit a part that does not help the recipient understand, decide, verify, or act.

## Communicate With A User

- Translate internal lifecycle or implementation terms into plain language.
- State an approval question directly.
- Explain why the answer is required.
- Give concrete options when real alternatives exist.
- Explain the practical consequence of each option.
- Label examples as illustrative.
- Recommend an option only when evidence supports it.
- State what unattended work cannot continue while an answer is pending.

Example:

> Do you approve changing the communication skill and the shared agent default? Approval lets implementation continue. Deferral preserves the current files and stops this work. These options are illustrative; no choice is assumed.

## Report A Blocker

A blocker is the specific condition preventing safe progress.

State the blocker, its evidence, the owner of the next action, and the condition that permits work to resume.

Example:

> The deployment cannot start because the production credential is unavailable. The credential owner must provide it. Implementation remains preserved and no deployment command has run.

## Hand Off Work

An agent handoff gives another agent enough information to continue without reconstructing the task.

Include:

- the work-item or task identity;
- the current state;
- the branch, worktree, or preserved commit when relevant;
- the evidence already obtained;
- the exact blocker or open decision;
- the next action and its owner.

Example:

> Task task-123 has a clean candidate at commit abc123 on branch feature/task-123. Five focused tests passed. Review has not started. The next owner is the code reviewer, who should review that exact commit.

## Remove Noise

- Do not repeat status that the recipient already has unless it changed.
- Do not narrate routine tool use.
- Do not copy a procedure into a handoff.
- Do not replace a clear sentence with an unexplained abstract label.
- Do not hide the exact question, result, or next action inside a long paragraph.
