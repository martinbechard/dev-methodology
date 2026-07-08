# Agent Neutrality Analysis

Analysis date: 2026-07-08

## Purpose

This repository is intended to support agents from multiple manufacturers. The core guidance should therefore avoid unnecessary vendor or product coupling. Manufacturer names, runtime paths, app-specific tools, and model-specific commands should appear only when the guidance is intentionally about that manufacturer or when an adapter needs to translate the neutral workflow into a concrete runtime.

The desired steady state is:

- Core instructions use neutral terms such as the agent, the verifier, the runtime, and the target agent environment.
- Repository-local coordination and temporary state use .agents by default.
- Product-specific folders such as .codex or .claude are treated as adapter or legacy paths.
- Commands that depend on a runtime are generated or documented through adapter profiles rather than embedded in reusable skills.
- OpenAI, Codex, Claude, Gemini, Copilot, or other provider names appear only in adapter files, examples that are explicitly about those products, or source material where the product identity is the subject.

## Scope

The review covered:

- Root project documents: README.md, documentation-methodology.md, and procedure-reverse-engineer-project-documentation.md.
- Templates under templates.
- Skill packages under skills, including SKILL.md files, references, scripts, and agents/openai.yaml files.
- Installer and tests under scripts.
- Project wiki helper implementation and regression tests under skills/project-wiki/scripts.

Three read-only explorer agents reviewed the root docs and templates, the skill tree, and the scripts/tests lane in parallel. I also ran local searches for vendor-specific terms and inspected the surrounding source.

## Executive Summary

The repository is already conceptually close to vendor-neutral. Most long-form methodology prose says agents rather than naming one product. The remaining coupling is concentrated in four places:

- Public setup language describes the bundle as Codex-specific.
- Installed command paths assume CODEX_HOME or ~/.codex.
- Several reusable skill descriptions and read-first references name Codex or point at an absolute local .codex path.
- Tests lock in Codex command strings and OpenAI example fixtures.

The right fix is not to delete all provider names. The durable fix is to split the package into a vendor-neutral core plus runtime adapters. The core should define the workflow, file conventions, verification expectations, and neutral command intents. Adapters should own install destinations, refresh commands, skill invocation syntax, automation tooling, and runtime-specific metadata.

## Findings

### 1. Root Docs Present The Bundle As Codex-Specific

README.md:37 calls the skills folder a portable Codex skill bundle. README.md:38 says the installer targets CODEX_HOME/skills or ~/.codex/skills. README.md:60 tells the user to restart Codex.

Those lines make the top-level package appear Codex-only even though most of the methodology is generic.

Recommendation:

- Describe the repository as a portable agent methodology or agent capability bundle.
- Describe skill packaging as one supported runtime format rather than the public abstraction.
- Replace the restart instruction with a neutral refresh instruction, then put Codex-specific refresh notes in an adapter section.

### 2. Reusable Templates Carry Codex Provenance

README.md:5, documentation-methodology.md:5, procedure-reverse-engineer-project-documentation.md:5, templates/*:5, and copied template assets under skills/development-methodology carry a GPT-5 Codex credit.

That provenance will be copied into downstream projects and makes neutral templates look vendor-authored.

Recommendation:

- Remove per-template vendor credits, or replace them with neutral repository provenance.
- Keep detailed generation provenance in release notes or repository history rather than reusable templates.

### 3. Installer Defaults To Codex

scripts/install-skills.py:15 defines CODEX_HOME_ENVIRONMENT_VARIABLE. scripts/install-skills.py:26 through scripts/install-skills.py:31 resolve the default destination to CODEX_HOME/skills or ~/.codex/skills. scripts/install-skills.py:36 and scripts/install-skills.py:48 describe the destination as a Codex skills directory.

This is useful for one runtime but should not be the default behavior of a multi-agent bundle.

Recommendation:

- Add a neutral default such as AGENTS_HOME/skills or ~/.agents/skills.
- Add explicit adapter profiles such as generic, codex, claude, and gemini.
- Keep CODEX_HOME support inside the Codex adapter.
- Make installer help text describe the selected adapter, not Codex globally.

### 4. Skill Frontmatter Names Codex Where The Agent Would Do

Reusable skill descriptions name Codex in several places:

- skills/careful-coding/SKILL.md:4
- skills/ast-grep/SKILL.md:4
- skills/fix-explanation/SKILL.md:4
- skills/project-wiki-query/SKILL.md:4
- skills/project-wiki-topic-writer/SKILL.md:4
- skills/project-wiki-topic-verifier/SKILL.md:4

These descriptions are not specifically about Codex behavior. They describe when any capable coding agent should use the skill.

Recommendation:

- Replace Codex with the agent, an agent, or the coding agent in reusable frontmatter.
- Reserve runtime names for adapter metadata or runtime-specific instructions.

### 5. Hard-Coded Skill Paths Assume A Local .codex Layout

The project wiki skill family contains repeated command and reference paths tied to .codex:

- skills/project-wiki/SKILL.md:232 through skills/project-wiki/SKILL.md:241
- skills/project-wiki-query/SKILL.md:15 through skills/project-wiki-query/SKILL.md:17
- skills/project-wiki-topic-writer/SKILL.md:29 through skills/project-wiki-topic-writer/SKILL.md:34
- skills/project-wiki-topic-writer/SKILL.md:57 through skills/project-wiki-topic-writer/SKILL.md:59
- skills/project-wiki-topic-verifier/SKILL.md:26 through skills/project-wiki-topic-verifier/SKILL.md:32
- skills/project-wiki-topic-verifier/SKILL.md:49, skills/project-wiki-topic-verifier/SKILL.md:50, and skills/project-wiki-topic-verifier/SKILL.md:100
- skills/project-wiki/references/page-schema.md:121 through skills/project-wiki/references/page-schema.md:123
- skills/project-wiki/references/topic-page-verification-checklist.md:62 through skills/project-wiki/references/topic-page-verification-checklist.md:64
- skills/project-wiki/references/operations.md:82, skills/project-wiki/references/operations.md:145, and skills/project-wiki/references/operations.md:157

Some references also use an absolute local home path under /Users/martinbechard/.codex, which is not portable to another machine.

Recommendation:

- Use relative references inside the skill package when one skill points to another file in the repository.
- Define a neutral command placeholder such as [agent-skills-home]/project-wiki/scripts/wiki_ops.py in docs, or provide a wrapper command under .agents/bin.
- Keep concrete ~/.codex examples only in Codex adapter documentation.

### 6. Generated Wiki Scaffold Emits Codex Commands

skills/project-wiki/scripts/project_wiki_ops/core.py:53 through skills/project-wiki/scripts/project_wiki_ops/core.py:60 write ~/.codex command examples into generated wiki README content. core.py:137 repeats the same assumption in generated schema content.

This means future generated docs inherit Codex-specific paths even after the source skill prose is neutralized.

Recommendation:

- Centralize command rendering behind a helper or manifest constant.
- Render neutral command intent in the core scaffold.
- Let adapters render concrete commands for each runtime.

### 7. Agent Claim Coordination Defaults To .Codex

skills/agent-claim/SKILL.md:20 sets the default claim file to .Codex/agent-claims.json. skills/project-wiki/scripts/project_wiki_ops/constants.py:56 through skills/project-wiki/scripts/project_wiki_ops/constants.py:59 include both .Codex and .agents as root-relative prefixes. skills/project-wiki/scripts/project_wiki_ops/core.py:39 through skills/project-wiki/scripts/project_wiki_ops/core.py:40 also recognizes .Codex and .agents in bare path extraction.

The user goal explicitly prefers a generic .agents folder when there is no reason to use a manufacturer folder.

Recommendation:

- Make .agents/agent-claims.json the default.
- Treat .Codex, .codex, .Claude, and .claude as adapter or repository-declared legacy locations.
- Make recognized workflow directories configurable rather than hard-coded in the core parser.

### 8. Automation Guidance Is Codex-Specific

skills/project-wiki/SKILL.md:160 and skills/project-wiki/references/operations.md:65 instruct agents running inside the Codex app to use the Codex automation tool for scheduled feeds.

The underlying rule is sensible: use the approved automation facility of the current environment. The current wording embeds one environment into the core skill.

Recommendation:

- Core rule: use the target environment's approved automation facility for scheduled feeds.
- Adapter rules: Codex uses the Codex automation tool; other environments may use their own scheduler, OS cron, GitHub Actions, or a hosted workflow when approved by the repository.

### 9. Subagent And Tool Invocation Syntax Is Not Abstracted

The verifier workflow relies on a useful neutral concept: run an independent read-only verifier context. The implementation language is tied to one style of orchestration:

- skills/project-wiki/SKILL.md:145
- skills/project-wiki-topic-writer/SKILL.md:60
- skills/project-wiki/references/operations.md:106

The $project-wiki-topic-verifier syntax and no-fork subagent wording may not map directly to every agent platform.

Recommendation:

- Core rule: run an independent verifier context with read-only authority and pass only repository root, page list, evidence paths, and lint output.
- Adapter rule: translate that into the runtime's invocation model, such as a subagent call, a separate agent session, a command wrapper, or a manual verification prompt.

### 10. OpenAI Metadata Is Installed As Part Of Every Skill

There are 13 files under skills/*/agents/openai.yaml. The current installer copies each whole skill directory, so OpenAI-shaped metadata is part of the default installed payload.

The files may be useful as runtime adapter metadata, but their location makes OpenAI the only first-class target.

Recommendation:

- Add agents/generic.yaml or a neutral manifest for the core package.
- Move provider-specific metadata under an adapter path, or copy it only when the selected adapter needs it.
- Review $skill-name prompt syntax as adapter-specific unless every supported runtime accepts it.

### 11. Tests Pin Vendor Paths And Examples

Vendor coupling is also present in regression tests:

- skills/project-wiki/scripts/test_setup_guidance.py:31 through skills/project-wiki/scripts/test_setup_guidance.py:44 assert exact ~/.codex command phrases.
- skills/project-wiki/scripts/test_raw_source_links.py:31 through skills/project-wiki/scripts/test_raw_source_links.py:43 uses .codex/automations as a passing fixture.
- skills/project-wiki/scripts/test_leaf_linking.py:22 through skills/project-wiki/scripts/test_leaf_linking.py:51 uses OpenAI and OpenAI Agents SDK fixture content.

The OpenAI fixture is not runtime coupling, but it adds unnecessary manufacturer branding to tests that can use fictional entities.

Recommendation:

- Replace generic fixtures with fictional neutral names.
- Test command intent or shared command rendering rather than exact Codex paths.
- Add adapter-specific tests only for adapter-specific behavior.

## Proposed Target Architecture

### Neutral Core

The core package owns manufacturer-independent concepts:

- Methodology documents and templates.
- Skill or capability instructions written in neutral language.
- Project wiki schema, linting, and helper scripts.
- Agent coordination rules using .agents as the default repository-local state directory.
- Verification contracts such as independent verifier context, read-only review, and full build or test expectations.
- Neutral command intents such as wiki status, wiki lint, link leaves, OKF migrate, and OKF validate.

The core should avoid hard-coded runtime home directories, app names, model names, and provider-specific invocation syntax.

### Runtime Adapters

Adapters translate neutral concepts into a runtime:

- Install destination.
- Environment variables.
- Refresh or restart instructions.
- Skill or command invocation syntax.
- Subagent or verifier invocation strategy.
- Automation scheduler strategy.
- Runtime metadata files.

Suggested initial adapters:

- generic: installs to .agents/skills or AGENTS_HOME/skills and documents neutral commands.
- codex: installs to CODEX_HOME/skills or ~/.codex/skills and includes Codex refresh and automation instructions.
- claude: installs to the appropriate Claude-compatible location once that target convention is chosen.
- gemini or other runtime adapters only when the project has a known install target and invocation contract.

### Adapter Manifest

Add a small adapter manifest so installer behavior and documentation generation are data-driven. The manifest should express:

- Adapter name.
- Skills destination rule.
- Optional environment variable.
- User-home fallback.
- Command prefix for helper scripts.
- Automation facility label.
- Skill invocation syntax.
- Metadata files to include or exclude.

This keeps core scripts from accumulating product-specific branches.

## Implementation Order

1. Define neutral vocabulary and adapter vocabulary.
   Update README wording first so later changes have a public contract to follow.

2. Introduce adapter configuration.
   Add a generic adapter and a Codex adapter. Keep Codex behavior working, but make it explicit.

3. Refactor installer defaults.
   Default to the generic adapter or require an adapter choice. Preserve Codex install behavior through the Codex adapter.

4. Centralize command rendering.
   Replace embedded ~/.codex command strings in skills, references, generated wiki scaffolds, and tests with neutral command intents or adapter-rendered commands.

5. Neutralize skill frontmatter and read-first paths.
   Replace unnecessary Codex mentions with the agent and replace absolute local paths with relative package references.

6. Move coordination state to .agents.
   Change the agent-claim default and parser defaults to .agents. Keep product-specific folders only as configured adapter or legacy paths.

7. Separate provider metadata.
   Add generic manifests or adapter-scoped metadata. Keep agents/openai.yaml only where the OpenAI or Codex adapter needs it.

8. Refresh tests.
   Update tests after the neutral API exists. Tests should verify neutral defaults, Codex adapter behavior, and generated docs without hard-coded vendor paths in the core.

9. Run verification.
   Run the Python regression tests and any repository build or lint command available after code changes. Any test failures should be fixed in the same pass.

## Suggested Worklist By Area

README and methodology docs:

- README.md:37, README.md:38, and README.md:60 need neutral public setup language.
- README.md:5, documentation-methodology.md:5, and procedure-reverse-engineer-project-documentation.md:5 need neutral provenance handling.

Templates:

- templates/*:5 and skills/development-methodology/assets/templates/*:5 need neutral provenance or no provenance.

Installer:

- scripts/install-skills.py:15 through scripts/install-skills.py:48 need adapter-driven destination selection.
- scripts/test_install_skills.py should gain generic default and Codex adapter coverage after installer behavior changes.

Core skill prose:

- The Codex mentions in reusable SKILL.md descriptions should become neutral.
- Read-first paths should become relative package references.
- Project wiki operation commands should become neutral command intents or adapter-rendered examples.

Project wiki scripts:

- skills/project-wiki/scripts/project_wiki_ops/core.py should stop embedding ~/.codex commands in generated scaffolds.
- skills/project-wiki/scripts/project_wiki_ops/constants.py should prefer .agents and load additional workflow prefixes from configuration.

Tests:

- test_setup_guidance.py should stop asserting Codex paths in core guidance.
- test_raw_source_links.py should use .agents for the neutral fixture.
- test_leaf_linking.py should use fictional fixture names unless it is intentionally testing real OpenAI wiki linking.

## Risk Notes

- Do not remove provider names when the subject is genuinely that provider. For example, a future wiki page about OpenAI or Claude should keep the real names.
- Do not replace skill terminology blindly. The repository has actual SKILL.md packages, so skill is still valid when referring to that file format. The public abstraction should be broader when speaking across runtimes.
- Do not create parallel fallback systems. Keep one neutral core and explicit adapters instead of scattered if-Codex checks.
- Treat existing .Codex, .codex, or provider paths as compatibility inputs only when a repository or adapter declares them.

## Conclusion

The project can become manufacturer-neutral without a large conceptual rewrite. The main work is to move runtime facts out of core instructions and into adapters. After that, the same methodology can serve Codex, Claude, Gemini, Copilot-style agents, local command-line agents, and future runtimes without making one provider the default mental model.
