# Project Wiki Review Checklist

## Purpose

Use this review checklist with project-wiki-review to verify a project wiki artifact created from the methodology templates.

## Completion Format

For every question record:

- Status: pass, fail, question, or n/a.
- Question: copy the objective question being answered.
- Evidence type: exact quotation, summary, assessment, or not applicable.
- Evidence source: name the artifact, authority source, checklist, or retained response used.
- Evidence: record exact source text for an exact quotation, or clearly labeled summary or derived assessment text.
- Assessment: explain why the evidence passes, fails, is unclear, or is not applicable.

Do not mark pass without evidence. The label Quoted evidence: is not an additional checklist field; use Evidence with Evidence type: exact quotation. Every exact quotation must occur in the named source after CRLF and LF normalization. The literal [omitted] marker may replace intervening text only when the retained segments occur exactly and in order. Label paraphrases as summaries and derived judgments as assessments. For n/a, record not applicable with a reason instead of inventing quoted evidence.

## Skill Workflow Checks

- Question: Does the review identify the wiki page type, source scope, and intended maintenance role before assessment?
- Question: Does the completed review checklist name this checklist as review-checklist-project-wiki.md?
- Question: Does the completed review checklist save next to the artifact using artifact-name.review-checklist-project-wiki.md?
- Question: Does the review use documentation-page-verify with the artifact, source evidence, and completed review checklist?
- Question: Does the final assessment derive findings or pass status from the completed review checklist rather than memory?
- Question: Does the output lead with findings ordered by severity when problems exist?

## Shared Contract Questions

- Question: Does the artifact start with Current Understanding, Authoritative Sources, Related Code, Related Tests, Related Backlog Items, Related Wiki Pages, Open Questions, and Maintenance Notes?
- Question: Does Current Understanding summarize durable project knowledge instead of narrating edit history?
- Question: Does Authoritative Sources identify which source wins when sources disagree?
- Question: Do Related Code and Related Tests link project-relative evidence or say Not yet identified after a real search?
- Question: Do Open Questions record unresolved authority, ownership, sync cadence, automation, source-link, or page granularity issues?
- Question: Do Maintenance Notes explain what future maintainers must recheck?

## Artifact-Specific Questions

- Question: Does Wiki Root confirm docs/wiki or explain the project-specific exception?
- Question: Does Authority Order include code, tests, functional specs, procedures, architecture, high-level designs, module designs, backlog, and generated documentation as applicable?
- Question: Does Base Page Contract name the shared sections and apply them to durable wiki pages and specialized documentation pages?
- Question: Does Page Subclassing explain how specialized documents extend the base contract without changing it?
- Question: Does Diagram Policy allow diagrams only for real sequence, ownership, dependency, lifecycle, state, data flow, or coverage relationships?
- Question: Do Topic Pages define broad topic pages, folder indexes, leaf pages, and links to specialized documents?
- Question: Do Code Pages map source folders, test folders, scripts, configuration, migrations, and generated artifact sources when those are meaningful?
- Question: Does Local Source Link describe whether a local source link exists, how it is ignored by git, and why durable links remain project-relative?
- Question: Does Daily Commit Sync define range source, raw scan location, file classification, skip recording, and the rule that commit messages are discovery hints?
- Question: Does Update Workflow include status, changed-file suggestion, source reading, page update, related code update, related test update, open question handling, lint, and maintenance log update?
- Question: Does Automation name scheduled or manual maintenance flows and what each may write?
- Question: Does Verification list wiki status, lint, page review, link checks, and sample sync checks?

## Findings

Report findings first. Treat missing source authority, missing Related Code, missing Related Tests, unresolved TODO markers, unsupported exact quotations, and unsourced automation claims as review findings. Preserve an otherwise complete review when a link is broken, record the unresolved link in Open Questions, and make it a blocking evidence failure only when that exact source is indispensable to the claimed conclusion.
