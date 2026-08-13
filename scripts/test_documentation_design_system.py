"""
Copyright (c) 2026 Martin.Bechard@DevConsult.ca
AI attribution: Generated with AI assistance.
Responsibility: Verifies the static Documentation Design System, its review checklist discovery, and its source-boundary contracts.
Design: design/documentation-design-system/index.html
Tests: scripts/test_documentation_design_system.py
"""

from __future__ import annotations

from html import unescape
from html.parser import HTMLParser
import hashlib
from pathlib import Path
import re
import unittest
from urllib.parse import urlsplit


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DESIGN_ROOT = REPOSITORY_ROOT / "design" / "documentation-design-system"
SKILL_ROOT = REPOSITORY_ROOT / "skills" / "review-documentation-design-system"
VERSION = "1.0.0"
PAGE_NAMES = (
    "index.html",
    "foundations.html",
    "page-shell.html",
    "content.html",
    "data-display.html",
    "forms-and-actions.html",
    "diagrams.html",
    "accessibility.html",
    "variations.html",
    "source-inventory.html",
)
CHECKLIST_NAMES = (
    "review-checklist-documentation-design-system-accessibility.md",
    "review-checklist-documentation-design-system-content.md",
    "review-checklist-documentation-design-system-data-display.md",
    "review-checklist-documentation-design-system-diagrams.md",
    "review-checklist-documentation-design-system-forms-and-actions.md",
    "review-checklist-documentation-design-system-foundations.md",
    "review-checklist-documentation-design-system-index.md",
    "review-checklist-documentation-design-system-page-shell.md",
    "review-checklist-documentation-design-system-shared.md",
    "review-checklist-documentation-design-system-source-inventory.md",
    "review-checklist-documentation-design-system-variations.md",
)
CHECKLIST_ID_PATTERN = re.compile(r"DDS-[A-Z]+-[0-9]{3}")
LIFECYCLE_NAVIGATION = (
    ("Agent And Skill Definitions", "agent-and-skill-definitions.html"),
    ("Agent And Skill Evaluations", "agent-and-skill-evaluations.html"),
    ("Agent-Owned Evaluation Suites", "agent-owned-evaluation-suites.html"),
    ("Agentic Configuration", "agentic-configuration.html"),
    ("Skills Modularization", "skills-modularization.html"),
    ("Generic Agent Definitions Source", "generic-agent-definitions-source.html"),
    (
        "Agent And Skill Specialization Examples",
        "agent-skill-specialization-examples.html",
    ),
    ("Orchestrated Development Lifecycle", "orchestrated-development-lifecycle.html"),
    ("Documentation Templates", "documentation-templates.html"),
    ("Wiki Skills And Project Context", "wiki-skills-and-project-context.html"),
)
LIFECYCLE_BASELINE_SEMANTIC_SHA256 = (
    "42271356d892a26fe0b8467c266cc2e0fb8099928a1214d8b1d167d8ea7b2b96"
)


class _PageParser(HTMLParser):
    """Collect the identifiers, links, metadata, and suite navigation from one page."""

    def __init__(self) -> None:
        """Initialize empty collections for one source document."""

        super().__init__()
        self.ids: list[str] = []
        self.hrefs: list[str] = []
        self.in_suite_nav = False
        self.suite_nav_seen = False
        self.suite_hrefs: list[str] = []
        self.version_meta: list[str] = []
        self.stylesheets: list[str] = []
        self.scripts: list[str] = []
        self.h1_count = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        """Record relevant attributes while preserving the parser's current nav scope."""

        attributes = dict(attrs)
        element_id = attributes.get("id")
        if element_id:
            self.ids.append(element_id)
        href = attributes.get("href")
        if href:
            self.hrefs.append(href)
        if tag == "nav":
            classes = set((attributes.get("class") or "").split())
            if "suite-nav" in classes and not self.suite_nav_seen:
                self.in_suite_nav = True
                self.suite_nav_seen = True
            else:
                self.in_suite_nav = False
        if tag == "a" and href and self.in_suite_nav:
            self.suite_hrefs.append(href)
        if tag == "meta" and attributes.get("name") == "design-system-version":
            self.version_meta.append(attributes.get("content") or "")
        if tag == "link" and attributes.get("rel") == "stylesheet":
            self.stylesheets.append(href or "")
        if tag == "script" and attributes.get("src"):
            self.scripts.append(attributes["src"] or "")
        if tag == "h1":
            self.h1_count += 1

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        """Process a self-closing tag without changing the element stack."""

        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag: str) -> None:
        """Leave the current element scope after an end tag."""

        if tag == "nav":
            self.in_suite_nav = False


def _parse_page(path: Path) -> tuple[str, _PageParser]:
    """Return source text and parsed static-navigation evidence for one page."""

    text = path.read_text(encoding="utf-8")
    parser = _PageParser()
    parser.feed(text)
    return text, parser


def _lifecycle_semantic_text(source: str) -> str:
    """Return accepted lifecycle prose after removing enumerated shell additions."""

    without_additions = re.sub(
        r'<a class="skip-link".*?</a>',
        "",
        source,
        flags=re.DOTALL,
    )
    without_additions = re.sub(
        r'<nav class="suite-nav".*?</nav>',
        "",
        without_additions,
        flags=re.DOTALL,
    )
    without_additions = re.sub(
        r'<a href="#top">Top</a>',
        "",
        without_additions,
    )
    without_additions = re.sub(
        r'<span class="ds-version">Design system v[^<]+</span>\s*[·-]?\s*',
        "",
        without_additions,
    )
    visible_markup = re.sub(
        r"<(?:style|script)\b.*?</(?:style|script)>",
        "",
        without_additions,
        flags=re.DOTALL,
    )
    visible_text = re.sub(r"<[^>]+>", " ", visible_markup)
    return " ".join(unescape(visible_text).split())


class DocumentationDesignSystemTests(unittest.TestCase):
    """Protect the approved static pages, checklist catalog, and interaction contracts."""

    def test_pages_share_version_assets_navigation_and_valid_fragments(self) -> None:
        """Every page must expose the same versioned ten-page navigation contract."""

        self.assertEqual(VERSION, (DESIGN_ROOT / "VERSION").read_text(encoding="utf-8").strip())
        expected_navigation = list(PAGE_NAMES)
        for page_name in PAGE_NAMES:
            with self.subTest(page=page_name):
                path = DESIGN_ROOT / page_name
                text, parser = _parse_page(path)
                self.assertTrue(text.startswith("<!doctype html>\n<!--\nCopyright"))
                self.assertEqual([VERSION], parser.version_meta)
                self.assertEqual(["assets/design-system.css"], parser.stylesheets)
                self.assertEqual(expected_navigation, parser.suite_hrefs)
                self.assertEqual(1, parser.h1_count)
                self.assertEqual(len(parser.ids), len(set(parser.ids)))
                self.assertIn(f"Design system v{VERSION}", text)
                for href in parser.hrefs:
                    parts = urlsplit(href)
                    if parts.scheme or parts.netloc:
                        continue
                    target = path if not parts.path else path.parent / parts.path
                    self.assertTrue(target.is_file(), href)
                    if parts.fragment:
                        _, target_parser = _parse_page(target)
                        self.assertIn(parts.fragment, target_parser.ids, href)

    def test_index_discovers_every_detail_page_and_assets_exist(self) -> None:
        """The single entry page must discover every concern and required static asset."""

        index_text, _ = _parse_page(DESIGN_ROOT / "index.html")
        for page_name in PAGE_NAMES[1:]:
            self.assertIn(f'href="{page_name}"', index_text)
        self.assertEqual(9, index_text.count('class="card card--link"'))
        for asset in ("design-system.css", "design-system.js", "dev-methodology-logo.png"):
            self.assertTrue((DESIGN_ROOT / "assets" / asset).is_file())

    def test_skill_discovers_eleven_checklists_with_91_unique_ids(self) -> None:
        """The review skill must expose every checklist and one unique occurrence of every ID."""

        skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        all_ids: list[str] = []
        for checklist_name in CHECKLIST_NAMES:
            self.assertIn(f"references/{checklist_name}", skill_text)
            checklist_path = SKILL_ROOT / "references" / checklist_name
            self.assertTrue(checklist_path.is_file())
            all_ids.extend(CHECKLIST_ID_PATTERN.findall(checklist_path.read_text(encoding="utf-8")))
        self.assertEqual(91, len(all_ids))
        self.assertEqual(91, len(set(all_ids)))
        self.assertIn("Open exactly the checklist supplied for this invocation", skill_text)
        self.assertIn("caller schedules separate invocations", skill_text)
        self.assertIn("caller supplies a strict output contract", skill_text)
        self.assertIn("standalone fallback", skill_text)
        self.assertIn("caller-owned pre-dispatch BLOCKED condition", skill_text)
        self.assertIn("NOT TESTED only after", skill_text)
        self.assertNotIn("and the one page-type checklist", skill_text)

    def test_shared_checklist_requires_target_navigation_inventory(self) -> None:
        """Shared review must validate the reviewed suite's real navigation contract."""

        skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        checklist_text = (
            SKILL_ROOT
            / "references"
            / "review-checklist-documentation-design-system-shared.md"
        ).read_text(encoding="utf-8")

        self.assertIn("Documentation Design System v1.0.0", skill_text)
        self.assertIn("expected suite-navigation inventory", skill_text)
        self.assertIn("visible label and href in exact order", skill_text)
        self.assertIn("current-page href", skill_text)
        self.assertIn("caller-supplied expected navigation inventory", checklist_text)
        self.assertIn("visible labels, href values, order", checklist_text)
        self.assertNotIn("the same ten destinations", checklist_text)

    def test_page_type_checklists_require_complete_contract_adoption(self) -> None:
        """Consuming pages must not receive partial page-type checklist reviews."""

        skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn(
            "Page-type checklists review the corresponding Documentation Design System "
            "contract and specimen pages by default.",
            skill_text,
        )
        self.assertIn(
            "only when that page intentionally adopts the complete page-type contract "
            "and every checklist criterion applies",
            skill_text,
        )
        self.assertIn(
            "Never assign or evaluate only part of a page-type checklist.", skill_text
        )
        self.assertIn(
            "complete Shared checklist plus independent artifact review and "
            "browser-based user-experience verification",
            skill_text,
        )

    def test_page_shell_labels_navigation_specimens_as_illustrative(self) -> None:
        """Navigation specimens must not masquerade as a target suite inventory."""

        page_text = (DESIGN_ROOT / "page-shell.html").read_text(encoding="utf-8")
        checklist_text = (
            SKILL_ROOT
            / "references"
            / "review-checklist-documentation-design-system-page-shell.md"
        ).read_text(encoding="utf-8")

        self.assertIn("Illustrative navigation specimen", page_text)
        self.assertIn("labels and destinations are examples", page_text)
        self.assertIn("target suite's authoritative navigation inventory", page_text)
        self.assertIn("illustrative labels and destinations", checklist_text)
        self.assertIn("target suite's authoritative navigation inventory", checklist_text)

    def test_version_one_declares_a_stable_contract(self) -> None:
        """The versioning guidance must describe the 1.0.0 compatibility boundary."""

        page_text = (DESIGN_ROOT / "page-shell.html").read_text(encoding="utf-8")

        self.assertIn("first stable contract release", page_text)
        self.assertNotIn("before 1.0.0", page_text)

    def test_lifecycle_uses_versioned_shell_and_real_navigation(self) -> None:
        """The lifecycle page must use its real suite inventory and shared shell."""

        lifecycle_path = (
            REPOSITORY_ROOT / "design" / "orchestrated-development-lifecycle.html"
        )
        lifecycle_text, lifecycle_parser = _parse_page(lifecycle_path)
        suite_nav = lifecycle_text.split(
            '<nav class="suite-nav" aria-label="Documentation pages">',
            1,
        )[1].split("</nav>", 1)[0]
        navigation_links = re.findall(
            r'<a href="([^"]+)"(?: aria-current="page")?>([^<]+)</a>',
            suite_nav,
        )

        self.assertEqual([VERSION], lifecycle_parser.version_meta)
        self.assertEqual(
            ["documentation-design-system/assets/design-system.css"],
            lifecycle_parser.stylesheets,
        )
        self.assertIn('<body id="top">', lifecycle_text)
        self.assertIn(
            '<a class="skip-link" href="#main-content">Skip to main content</a>',
            lifecycle_text,
        )
        self.assertIn('<main id="main-content">', lifecycle_text)
        self.assertEqual(
            [(href, label) for label, href in LIFECYCLE_NAVIGATION],
            navigation_links,
        )
        for _, href in LIFECYCLE_NAVIGATION:
            with self.subTest(navigation_target=href):
                self.assertTrue((lifecycle_path.parent / href).is_file())
        self.assertEqual(1, suite_nav.count('aria-current="page"'))
        self.assertIn(
            '<a href="orchestrated-development-lifecycle.html" aria-current="page">'
            "Orchestrated Development Lifecycle</a>",
            suite_nav,
        )
        self.assertIn(
            '<section class="hero" aria-labelledby="page-title">', lifecycle_text
        )
        self.assertIn(
            '<h1 id="page-title">Orchestrated Development Lifecycle</h1>',
            lifecycle_text,
        )
        self.assertIn(
            '<nav class="chapter-nav" aria-label="Lifecycle chapters">\n    <a href="#top">Top</a>',
            lifecycle_text,
        )
        self.assertIn(
            '<div class="table-wrap" tabindex="0" role="region" '
            'aria-labelledby="evidence-table-caption"><table class="evidence-table"',
            lifecycle_text,
        )
        self.assertIn(
            ".table-wrap:focus-visible {\n      outline: 3px solid var(--amber);",
            lifecycle_text,
        )
        self.assertIn(f'<span class="ds-version">Design system v{VERSION}</span>', lifecycle_text)
        self.assertEqual(
            LIFECYCLE_BASELINE_SEMANTIC_SHA256,
            hashlib.sha256(
                _lifecycle_semantic_text(lifecycle_text).encode("utf-8")
            ).hexdigest(),
        )

    def test_forms_expose_result_count_and_complete_dialog_keyboard_contract(self) -> None:
        """Form demonstrations must expose results and a real modal focus loop."""

        page_text = (DESIGN_ROOT / "forms-and-actions.html").read_text(encoding="utf-8")
        script_text = (DESIGN_ROOT / "assets" / "design-system.js").read_text(encoding="utf-8")
        self.assertIn("data-filter-form", page_text)
        self.assertIn('role="status" data-result-count', page_text)
        for token in (
            "data-result-count",
            'event.key === "Tab"',
            "focusableElements",
            "event.shiftKey",
            'event.key === "Escape"',
            "activeTrigger.focus()",
        ):
            self.assertIn(token, script_text)

    def test_print_css_hides_demo_controls_but_not_results(self) -> None:
        """Printed documentation omits interactive specimens while retaining explanations and results."""

        css = (DESIGN_ROOT / "assets" / "design-system.css").read_text(encoding="utf-8")
        print_rules = css.split("@media print", 1)[1].split("{", 1)[1]
        hidden_selectors = {
            selector.strip()
            for selector in print_rules.split("{", 1)[0].split(",")
        }
        for selector in (
            ".filters",
            ".field",
            ".check-field",
            "input",
            "select",
            "button",
            ".dialog-backdrop",
        ):
            self.assertIn(selector, hidden_selectors)
        for preserved in (
            "form",
            "[data-demo-form]",
            ".demo-status",
            ".demo-alert",
            "[data-result-count]",
        ):
            self.assertNotIn(preserved, hidden_selectors)
        forms_text = (DESIGN_ROOT / "forms-and-actions.html").read_text(encoding="utf-8")
        self.assertIn('form class="panel" data-demo-form', forms_text)
        self.assertIn('class="demo-alert" role="alert"', forms_text)
        self.assertIn('class="demo-status" role="status"', forms_text)

    def test_every_variation_has_visible_status_and_source_attribution(self) -> None:
        """All 21 comparisons must expose one inline standardization status and source evidence."""

        text = (DESIGN_ROOT / "variations.html").read_text(encoding="utf-8")
        articles = re.findall(
            r'<article class="variation-section"[^>]*>(.*?)</article>',
            text,
            flags=re.DOTALL,
        )
        self.assertEqual(21, len(articles))
        for number, article in enumerate(articles, start=1):
            with self.subTest(variation=number):
                self.assertIn(f">08.{number}<", article)
                header = article.split("</header>", 1)[0]
                self.assertEqual(1, header.count('class="pattern-decision__status"'))
                status = re.search(
                    r'class="pattern-decision__status">([^<]+)</span>',
                    header,
                )
                self.assertIsNotNone(status)
                if number == 3:
                    expected_status = "Partly classified"
                elif number == 4:
                    expected_status = "Resolved in the design system"
                else:
                    expected_status = "Unresolved source variation"
                self.assertEqual(expected_status, status.group(1) if status else None)
                self.assertIn('class="variant-source"', article)

        meaningful_svg = re.search(r"<svg[^>]*role=\"img\"[^>]*>.*?</svg>", text, flags=re.DOTALL)
        self.assertIsNotNone(meaningful_svg)
        svg_text = meaningful_svg.group(0) if meaningful_svg else ""
        self.assertIn('aria-labelledby="variation-hero-svg-title variation-hero-svg-desc"', svg_text)
        self.assertIn('<title id="variation-hero-svg-title">', svg_text)
        self.assertIn('<desc id="variation-hero-svg-desc">', svg_text)

    def test_foundations_spacing_specimen_covers_every_documented_step(self) -> None:
        """The visible specimen must contain all seven documented spacing values."""

        text = (DESIGN_ROOT / "foundations.html").read_text(encoding="utf-8")
        section = text.split('id="space"', 1)[1].split("</section>", 1)[0]
        for value in (".5", ".75", "1", "1.25", "1.5", "2", "2.5"):
            self.assertIn(f"<small>{value}</small>", section)

    def test_diagrams_preserve_accessible_short_stem_geometry(self) -> None:
        """Reusable arrows and correct fan flows must retain the approved geometry and names."""

        text = (DESIGN_ROOT / "diagrams.html").read_text(encoding="utf-8")
        for token in (
            '<symbol id="blockEntryArrow" viewBox="0 0 14 18">',
            '<symbol id="strongBlockEntryArrow" viewBox="0 0 28 18">',
            "9-unit stem",
            "9-unit arrowhead",
            "connector end <code>B - 18</code>",
            "tip at <code>B</code>",
        ):
            self.assertIn(token, text)
        for figure_id in ("geometry", "fanout-do", "fanout-dont", "fanin-do", "fanin-dont"):
            suffix = "-svg" if figure_id == "geometry" else ""
            self.assertIn(f'<title id="{figure_id}{suffix}-title"', text)
            self.assertIn(f'<desc id="{figure_id}{suffix}-desc"', text)
        fanout_do = text.split('id="fanout-do-title"', 1)[1].split("</svg>", 1)[0]
        fanin_do = text.split('id="fanin-do-title"', 1)[1].split("</svg>", 1)[0]
        self.assertEqual(3, fanout_do.count('href="#blockEntryArrow"'))
        self.assertEqual(1, fanin_do.count('href="#strongBlockEntryArrow"'))
        self.assertNotIn("marker-end", fanout_do)
        self.assertNotIn("marker-end", fanin_do)

    def test_source_inventory_declares_the_design_relevant_boundary(self) -> None:
        """The audit must distinguish its 16 inputs from the extra tracked provenance fixture."""

        text = (DESIGN_ROOT / "source-inventory.html").read_text(encoding="utf-8")
        for phrase in (
            "17 tracked HTML files",
            "16 design-relevant sources",
            "11 primary documentation pages",
            "one styled report example",
            "four interaction fixtures",
            "skills/document-provenance/fixtures/valid/maintained.html",
            "excluded",
            "36f8c1be6d04c865c4e718917c5812dc3fdf0363",
        ):
            self.assertIn(phrase, text)

        self.assertIn("audited snapshot", text.lower())
        self.assertIn("were not migrated", text)
        self.assertIn("Generated evaluation data was refreshed", text)

    def test_page_shell_separates_abbreviated_specimen_from_production_navigation(self) -> None:
        """Only real suite navigation carries all ten stable links."""

        text = (DESIGN_ROOT / "page-shell.html").read_text(encoding="utf-8")
        self.assertIn(
            '<div class="suite-nav suite-nav--non-production-specimen"',
            text,
        )
        self.assertNotIn(
            '<nav class="suite-nav suite-nav--non-production-specimen"',
            text,
        )
        self.assertEqual(1, text.count('class="suite-nav" aria-label="Design system pages"'))
        css = (DESIGN_ROOT / "assets" / "design-system.css").read_text(encoding="utf-8")
        compact_rule = css.split(".suite-nav--non-production-specimen {", 1)[1].split("}", 1)[0]
        self.assertIn("width: 100%", compact_rule)
        self.assertIn("margin: 0", compact_rule)
        self.assertIn("padding-top: 0", compact_rule)

    def test_diagram_tree_uses_the_adopted_design_system_path(self) -> None:
        """The folder-tree specimen must enumerate the complete adopted source tree."""

        text = (DESIGN_ROOT / "diagrams.html").read_text(encoding="utf-8")
        tree = text.split('<pre class="folder-tree"', 1)[1].split("</pre>", 1)[0]
        for path_name in (
            "VERSION",
            *PAGE_NAMES,
            "assets/",
            "design-system.css",
            "design-system.js",
            "dev-methodology-logo.png",
        ):
            self.assertIn(path_name, tree)

    def test_readme_states_bounded_coordination_and_portability_evidence(self) -> None:
        """README scope must distinguish tested Codex coordination from untested mappings."""

        text = (REPOSITORY_ROOT / "README.md").read_text(encoding="utf-8")
        for phrase in (
            "bounded page-checklist coordination",
            "Codex tournament-backed evidence",
            "non-Codex portability mappings remain untested",
            "Existing hand-authored HTML pages were not migrated",
            "simple, coordination, default, documentation, advanced, and advanced-long",
        ):
            self.assertIn(phrase, text)

    def test_catalog_precedence_and_predispatch_identity_boundary_are_consistent(self) -> None:
        """Incomplete evidence precedes failure, while malformed identity blocks before dispatch."""

        catalog = (
            REPOSITORY_ROOT / "evals" / "agent-scenarios.yaml"
        ).read_text(encoding="utf-8")
        runner = catalog.split(
            "  - id: methodology-design-system-checklist-runner\n",
            1,
        )[1].split(
            "  - id: methodology-design-system-review-coordinator\n",
            1,
        )[0]
        coordinator = catalog.split(
            "  - id: methodology-design-system-review-coordinator\n",
            1,
        )[1]
        self.assertIn("Derive NOT TESTED before FAIL", runner)
        self.assertIn("exact page, checklist, and expected-ID inventory", runner)
        self.assertIn("malformed assignment identity before dispatch", coordinator)
        self.assertIn("BLOCKED", coordinator)


if __name__ == "__main__":
    unittest.main()
