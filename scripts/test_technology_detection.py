# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Modified with AI assistance.
# Summary: Verifies setup-time technology detection, folder ownership, generated mirrors, and AGENTS.md rendering.

from __future__ import annotations

import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
BUILD_SCRIPT = ROOT / "scripts" / "build-technology-detection.py"
DETECT_SCRIPT = ROOT / "scripts" / "detect-technology-skills.py"
INSTALLED_DETECT_SCRIPT = ROOT / "skills" / "detect-technology-skills" / "scripts" / "detect.py"
RENDER_SCRIPT = ROOT / "scripts" / "render-agents-technology-skills.py"
REGISTRY = ROOT / "skills" / "detect-technology-skills" / "references" / "technology-skill-detection-registry.yaml"
TOML_PYTHON_ENV = "TECHNOLOGY_DETECTOR_TOML_PYTHON"
PARSER_FREE_PYTHON_ENV = "TECHNOLOGY_DETECTOR_PARSER_FREE_PYTHON"


def load_renderer_module():
    """Load the renderer script so policy decisions can be tested at its Python boundary."""
    spec = importlib.util.spec_from_file_location("render_agents_technology_skills", RENDER_SCRIPT)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load renderer: {RENDER_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_detection_builder_module():
    """Load the detection builder so source-schema behavior can be tested directly."""
    spec = importlib.util.spec_from_file_location("build_technology_detection", BUILD_SCRIPT)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load detection builder: {BUILD_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_source_detection_registry(path: Path) -> None:
    """Write a temporary registry from source detection definitions for focused source tests."""
    module = load_detection_builder_module()
    path.write_text(
        yaml.safe_dump(module.registry(module.load_detection_entries()), sort_keys=False),
        encoding="utf-8",
    )




def with_unset_workflows(value: dict[str, object]) -> dict[str, object]:
    """Add one verified claim-helper interface and deferred workflow selectors."""

    return {
        **with_claim_transport({}),
        "workflow_selection": {
            "persistence": {"default": "UNSET"},
            "commit": {"default": "UNSET"},
        },
        **value,
    }


def with_claim_transport(value: dict[str, object]) -> dict[str, object]:
    """Add one available command adapter selection to a renderer fixture."""

    return {
        "resource_coordination": {
            "selected": "agent-claim",
            "deadline_policy": {
                "resource_classes": {
                    "backlog-mutation": {
                        "maximum_duration_seconds": 600,
                        "cleanup_grace_seconds": 120,
                    },
                    "main-integration": {
                        "maximum_duration_seconds": 2700,
                        "cleanup_grace_seconds": 600,
                    },
                    "browser-server": {
                        "maximum_duration_seconds": 3600,
                        "cleanup_grace_seconds": 600,
                    },
                    "database-port": {
                        "maximum_duration_seconds": 1800,
                        "cleanup_grace_seconds": 300,
                    },
                    "live-model-evaluation": {
                        "maximum_duration_seconds": 14400,
                        "cleanup_grace_seconds": 1800,
                    },
                },
                "resource_overrides": {},
            },
        },
        "agent_claim_transport": {
            "selected": "command",
            "availability": "AVAILABLE",
            "verification": ["bundled command fixture"],
        },
        **value,
    }


def confirmed_technology_selection() -> dict[str, object]:
    """Return persisted candidate and explicit user-confirmation evidence."""

    return {
        "candidates": [
            {
                "scope": "src/**",
                "skill": "python",
                "evidence": ["Python source evidence: src/app.py"],
                "conflicts": [],
                "disposition": "accepted",
            }
        ],
        "accepted_skills": ["python"],
        "rejections": [],
        "confirmation": {
            "status": "confirmed",
            "evidence": "user-message: confirmed python for src/**",
        },
    }


def detector_test_interpreter(environment_name: str, *, require_toml: bool) -> Path:
    """Resolve a PyYAML-capable detector runtime with the requested TOML parser state."""
    configured = os.environ.get(environment_name)
    candidates = [configured] if configured else [
        sys.executable,
        "python3.13",
        "python3.12",
        "python3.11",
        "python3.10",
        "python3.9",
        "python3",
    ]
    checked: set[Path] = set()
    probe = (
        "import importlib.util; "
        "has_toml = bool(importlib.util.find_spec('tomllib') or importlib.util.find_spec('tomli')); "
        "has_yaml = bool(importlib.util.find_spec('yaml')); "
        f"raise SystemExit(0 if has_yaml and has_toml is {require_toml!r} else 1)"
    )
    for candidate in candidates:
        if not candidate:
            continue
        located = shutil.which(candidate)
        path = Path(located or candidate).expanduser().resolve()
        if path in checked or not path.is_file():
            continue
        checked.add(path)
        completed = subprocess.run([str(path), "-c", probe], check=False, capture_output=True, text=True)
        if completed.returncode == 0:
            return path
    requirement = "with" if require_toml else "without"
    if configured:
        raise AssertionError(
            f"{environment_name}={configured!r} is not a Python runtime {requirement} tomllib/tomli and with PyYAML"
        )
    raise unittest.SkipTest(
        f"host matrix has no Python runtime {requirement} tomllib/tomli and with PyYAML; "
        f"set {environment_name} to provide one"
    )


def toml_capable_interpreter() -> Path:
    """Return the configured or discovered runtime for tests that interpret pyproject.toml."""
    return detector_test_interpreter(TOML_PYTHON_ENV, require_toml=True)


def parser_free_interpreter() -> Path:
    """Return the configured or discovered runtime for the missing-TOML-parser boundary."""
    return detector_test_interpreter(PARSER_FREE_PYTHON_ENV, require_toml=False)


def run_detection(
    project: Path,
    *scopes: str,
    expected_code: int = 0,
    detector: Path = DETECT_SCRIPT,
    extra: list[str] | None = None,
    interpreter: Path | str = sys.executable,
    isolated: bool = False,
) -> dict[str, object]:
    """Run one detector implementation and return its parsed result at the expected exit boundary."""
    arguments = [str(interpreter)]
    if isolated:
        arguments.append("-S")
    arguments.extend([str(detector), "--project-root", str(project)])
    for scope in scopes:
        arguments.extend(["--scope", scope])
    arguments.extend(extra or [])
    completed = subprocess.run(arguments, cwd=ROOT, check=False, capture_output=True, text=True)
    if completed.returncode != expected_code:
        raise AssertionError(f"expected {expected_code}, got {completed.returncode}: {completed.stderr}\n{completed.stdout}")
    return json.loads(completed.stdout)


class TechnologyDetectionTests(unittest.TestCase):
    """Verify detector clauses, ownership isolation, generated mirrors, and routing output."""

    def test_basic_setup_renders_resolved_values_without_hidden_controls(self) -> None:
        """Keep Basic setup inspectable while hiding fixed decisions."""

        renderer = load_renderer_module()
        project = with_claim_transport({
            "project_setup": {
                "mode": "basic",
                "concurrent_tasking": False,
                "persistence": "none",
                "commit": "direct-main",
                "documentation": "wiki",
                "core_skill_delivery": {
                    "mode": "by-reference",
                    "source": "installed-agent-metadata",
                },
                "technology_skill_delivery": "by-reference",
                "technology_confirmation_required": True,
            },
            "workflow_selection": {
                "persistence": {"default": "none"},
                "commit": {"default": "direct-main"},
            },
            "technology_confirmation": confirmed_technology_selection(),
            "technology_skill_loadouts": [{
                "pathPattern": "src/**",
                "skills": ["python"],
            }],
        })
        rendered = renderer.render(project)

        for expected in (
            "Setup mode: Basic",
            "Set: Concurrent tasking No",
            "Set: Persistence none",
            "Set: Commit direct-main",
            "Documentation question: Create the Wiki? Yes (default Yes)",
            "Set: Core skill delivery by-reference",
            "Set: Technology skill delivery by-reference",
            "Technology confirmation: required",
        ):
            self.assertIn(expected, rendered)
        self.assertNotIn("Concurrent capacity", rendered)

        no_wiki_project = {
            **project,
            "project_setup": {
                **project["project_setup"],
                "documentation": "none",
            },
        }
        no_wiki_rendered = renderer.render(no_wiki_project)
        self.assertIn(
            "Documentation question: Create the Wiki? No (default Yes)",
            no_wiki_rendered,
        )

    def test_advanced_setup_requires_capacity_only_for_concurrent_tasking(self) -> None:
        """Expose Advanced concurrent capacity only after tasking is enabled."""

        renderer = load_renderer_module()
        project = with_claim_transport({
            "project_setup": {
                "mode": "advanced",
                "concurrent_tasking": True,
                "concurrent_capacity": 3,
                "persistence": "file",
                "commit": "direct-main",
                "documentation": "both",
                "core_skill_delivery": {
                    "mode": "by-reference",
                    "source": "installed-agent-metadata",
                },
                "technology_skill_delivery": "inline",
                "technology_confirmation_required": True,
            },
            "workflow_selection": {
                "persistence": {"default": "file"},
                "commit": {"default": "direct-main"},
            },
            "technology_confirmation": confirmed_technology_selection(),
            "technology_skill_loadouts": [{
                "pathPattern": "src/**",
                "skills": ["python"],
            }],
        })

        rendered = renderer.render(project)
        self.assertIn("Setup mode: Advanced", rendered)
        self.assertIn("Concurrent capacity: 3", rendered)
        self.assertIn("Technology skill delivery: inline", rendered)
        self.assertIn("BEGIN INLINED TECHNOLOGY SKILL: python", rendered)

        no_documentation_project = {
            **project,
            "project_setup": {
                **project["project_setup"],
                "documentation": "none",
            },
        }
        with self.assertRaisesRegex(
            ValueError,
            "project_setup.documentation must be wiki, specifications, or both in Advanced mode",
        ):
            renderer.render(no_documentation_project)

        with self.assertRaisesRegex(
            ValueError,
            "explicit technology delivery by-reference conflicts with project_setup.technology_skill_delivery 'inline'",
        ):
            renderer.render(project, inline_tech_skills=False)

        project["project_setup"]["concurrent_tasking"] = False
        with self.assertRaisesRegex(
            ValueError,
            "project_setup.concurrent_capacity is allowed only when concurrent_tasking is true",
        ):
            renderer.render(project)

    def test_setup_selectors_reconcile_with_canonical_and_legacy_workflow_paths(self) -> None:
        """Reject selector divergence before setup text and canonical routing can disagree."""

        renderer = load_renderer_module()
        project = with_claim_transport({
            "project_setup": {
                "mode": "basic",
                "concurrent_tasking": False,
                "persistence": "none",
                "commit": "direct-main",
                "documentation": "wiki",
                "core_skill_delivery": {
                    "mode": "by-reference",
                    "source": "installed-agent-metadata",
                },
                "technology_skill_delivery": "by-reference",
                "technology_confirmation_required": True,
            },
            "technology_confirmation": confirmed_technology_selection(),
            "workflow_selection": {
                "provider": {"default": "file"},
                "completion": {"default": "feature-branch"},
            },
            "technology_skill_loadouts": [{
                "pathPattern": "src/**",
                "skills": ["python"],
            }],
        })

        with self.assertRaisesRegex(
            ValueError,
            "^project_setup.persistence 'none' conflicts with workflow_selection.persistence.default 'file'$",
        ):
            renderer.render(project)

        project["workflow_selection"] = {
            "provider": {"default": "none"},
            "completion": {"default": "direct-main"},
        }
        rendered = renderer.render(project)
        self.assertIn("Set: Persistence none", rendered)
        self.assertIn("Default persistence none", rendered)
        self.assertIn(
            "Normalized workflow_selection.provider to workflow_selection.persistence",
            rendered,
        )
        self.assertIn(
            "Normalized workflow_selection.completion to workflow_selection.commit",
            rendered,
        )
        self.assertNotIn("Default provider", rendered)
        self.assertNotIn("Default completion", rendered)
        self.assertNotIn("feature-branch", rendered)

    def test_legacy_selector_families_normalize_directly_to_persistence_and_commit(self) -> None:
        """Preserve compatibility values while rendering canonical labels and routes only."""

        renderer = load_renderer_module()
        rendered = renderer.render(with_claim_transport({
            "workflow_selection": {
                "backlog": {
                    "default": "file-based-backlog",
                    "folder_overrides": [{
                        "pattern": "services/**",
                        "process": "github-issues-backlog",
                    }],
                },
                "workitem": {
                    "default": "simple-workitem",
                    "folder_overrides": [{
                        "pattern": "release/**",
                        "process": "feature-branch-workitem",
                    }],
                },
            },
        }))

        self.assertIn("Default persistence file: create with create-work-item-file", rendered)
        self.assertIn("services/** persistence github: create with create-work-item-github", rendered)
        self.assertIn("Default commit direct-main: use deliver-work-item-direct-main", rendered)
        self.assertIn("release/** commit feature-branch: use deliver-work-item-feature-branch", rendered)
        self.assertIn(
            "Normalized workflow_selection.backlog to workflow_selection.persistence",
            rendered,
        )
        self.assertIn(
            "Normalized workflow_selection.workitem to workflow_selection.commit",
            rendered,
        )
        self.assertNotIn("Default provider", rendered)
        self.assertNotIn("Default completion", rendered)

        with self.assertRaisesRegex(
            ValueError,
            "^workflow_selection.provider collides with workflow_selection.persistence; "
            "replace workflow_selection.provider with workflow_selection.persistence and keep exactly one selector family$",
        ):
            renderer.render(with_claim_transport({
                "workflow_selection": {
                    "persistence": {"default": "file"},
                    "provider": {"default": "file"},
                    "commit": {"default": "direct-main"},
                },
            }))

    def test_setup_requires_structured_technology_confirmation_evidence(self) -> None:
        """Reject missing, boolean-only, empty, or internally inconsistent confirmations."""

        renderer = load_renderer_module()
        project = with_claim_transport({
            "project_setup": {
                "mode": "basic",
                "concurrent_tasking": False,
                "persistence": "none",
                "commit": "direct-main",
                "documentation": "wiki",
                "core_skill_delivery": {
                    "mode": "by-reference",
                    "source": "installed-agent-metadata",
                },
                "technology_skill_delivery": "by-reference",
                "technology_confirmation_required": True,
            },
            "workflow_selection": {
                "persistence": {"default": "none"},
                "commit": {"default": "direct-main"},
            },
            "technology_skill_loadouts": [{
                "pathPattern": "src/**",
                "skills": ["python"],
            }],
        })

        invalid_values = (
            (None, "technology_confirmation must be a mapping"),
            (True, "technology_confirmation must be a mapping"),
            ({}, "technology_confirmation keys must be exactly"),
            (
                {
                    **confirmed_technology_selection(),
                    "confirmation": True,
                },
                "technology_confirmation.confirmation must be a mapping",
            ),
            (
                {
                    **confirmed_technology_selection(),
                    "confirmation": {"status": "confirmed", "evidence": ""},
                },
                "technology_confirmation.confirmation.evidence must be a non-empty auditable reference",
            ),
            (
                {
                    **confirmed_technology_selection(),
                    "confirmation": {"status": "confirmed", "evidence": "   "},
                },
                "technology_confirmation.confirmation.evidence must be a non-empty auditable reference",
            ),
        )
        for confirmation, expected in invalid_values:
            candidate = dict(project)
            if confirmation is not None:
                candidate["technology_confirmation"] = confirmation
            with self.subTest(expected=expected), self.assertRaisesRegex(
                ValueError,
                re.escape(expected),
            ):
                renderer.render(candidate)

        project["technology_confirmation"] = confirmed_technology_selection()
        rendered = renderer.render(project)
        self.assertIn("Technology candidates: 1", rendered)
        self.assertIn("Accepted technology skills: python", rendered)
        self.assertIn("Confirmation evidence: user-message: confirmed python for src/**", rendered)

    def test_technology_confirmation_binds_each_skill_to_its_confirmed_scope(self) -> None:
        """Reject scope-swapped routing and allow the same skill on distinct confirmed scopes."""

        renderer = load_renderer_module()
        project = with_claim_transport({
            "project_setup": {
                "mode": "basic",
                "concurrent_tasking": False,
                "persistence": "none",
                "commit": "direct-main",
                "documentation": "wiki",
                "core_skill_delivery": {
                    "mode": "by-reference",
                    "source": "installed-agent-metadata",
                },
                "technology_skill_delivery": "by-reference",
                "technology_confirmation_required": True,
            },
            "workflow_selection": {
                "persistence": {"default": "none"},
                "commit": {"default": "direct-main"},
            },
            "technology_confirmation": confirmed_technology_selection(),
            "technology_skill_loadouts": [{
                "pathPattern": "tests/**",
                "skills": ["python"],
            }],
        })
        with self.assertRaisesRegex(
            ValueError,
            "accepted scope and skill bindings must match technology_skill_loadouts in order",
        ):
            renderer.render(project)

        project["technology_confirmation"] = {
            "candidates": [
                {
                    "scope": "src/**",
                    "skill": "python",
                    "evidence": ["Python source evidence: src/app.py"],
                    "conflicts": [],
                    "disposition": "accepted",
                },
                {
                    "scope": "tests/**",
                    "skill": "python",
                    "evidence": ["Python test evidence: tests/test_app.py"],
                    "conflicts": [],
                    "disposition": "accepted",
                },
            ],
            "accepted_skills": ["python", "python"],
            "rejections": [],
            "confirmation": {
                "status": "confirmed",
                "evidence": "project-review: python confirmed for source and tests",
            },
        }
        project["technology_skill_loadouts"] = [
            {"pathPattern": "src/**", "skills": ["python"]},
            {"pathPattern": "tests/**", "skills": ["python"]},
        ]
        rendered = renderer.render(project)
        self.assertIn("Accepted technology skills: python, python", rendered)

    def test_technology_skill_ids_are_validated_before_by_reference_rendering(self) -> None:
        """Reject instruction-shaped skill identifiers on every persisted routing surface."""

        renderer = load_renderer_module()
        project = with_claim_transport({
            "project_setup": {
                "mode": "basic",
                "concurrent_tasking": False,
                "persistence": "none",
                "commit": "direct-main",
                "documentation": "wiki",
                "core_skill_delivery": {
                    "mode": "by-reference",
                    "source": "installed-agent-metadata",
                },
                "technology_skill_delivery": "by-reference",
                "technology_confirmation_required": True,
            },
            "workflow_selection": {
                "persistence": {"default": "none"},
                "commit": {"default": "direct-main"},
            },
            "technology_confirmation": confirmed_technology_selection(),
            "technology_skill_loadouts": [{
                "pathPattern": "src/**",
                "skills": ["python"],
                "sourceEvidence": [{
                    "skill": "python",
                    "evidence": ["Python source evidence: src/app.py"],
                }],
            }],
        })
        mutations = (
            ("accepted", lambda value: value["technology_confirmation"]["accepted_skills"].__setitem__(0, "python\n## injected")),
            ("candidate", lambda value: value["technology_confirmation"]["candidates"][0].__setitem__("skill", "python\n## injected")),
            ("evidence", lambda value: value["technology_skill_loadouts"][0]["sourceEvidence"][0].__setitem__("skill", "python\n## injected")),
            ("loadout", lambda value: value["technology_skill_loadouts"][0]["skills"].__setitem__(0, "python\n## injected")),
        )
        for surface, mutate in mutations:
            with self.subTest(surface=surface):
                candidate = deepcopy(project)
                mutate(candidate)
                with self.assertRaisesRegex(ValueError, "lowercase hyphenated skill id"):
                    renderer.render(candidate)

        rejected = deepcopy(project)
        rejected["technology_confirmation"] = {
            "candidates": [{
                "scope": "src/**",
                "skill": "python",
                "evidence": ["Python source evidence: src/app.py"],
                "conflicts": ["not selected"],
                "disposition": "rejected",
            }],
            "accepted_skills": [],
            "rejections": [{"skill": "python\n## injected", "reason": "not selected"}],
            "confirmation": {
                "status": "confirmed",
                "evidence": "user-message: no technology skills accepted",
            },
        }
        rejected["technology_skill_loadouts"] = []
        with self.assertRaisesRegex(ValueError, "lowercase hyphenated skill id"):
            renderer.render(rejected)

    def test_technology_free_text_cannot_inject_generated_guidance(self) -> None:
        """Reject multiline or control-bearing text before rendering AGENTS.md."""

        renderer = load_renderer_module()
        project = with_claim_transport({
            "project_setup": {
                "mode": "basic",
                "concurrent_tasking": False,
                "persistence": "none",
                "commit": "direct-main",
                "documentation": "wiki",
                "core_skill_delivery": {
                    "mode": "by-reference",
                    "source": "installed-agent-metadata",
                },
                "technology_skill_delivery": "by-reference",
                "technology_confirmation_required": True,
            },
            "workflow_selection": {
                "persistence": {"default": "none"},
                "commit": {"default": "direct-main"},
            },
            "technology_confirmation": confirmed_technology_selection(),
            "technology_skill_loadouts": [{
                "pathPattern": "src/**",
                "skills": ["python"],
                "sourceEvidence": [{
                    "skill": "python",
                    "evidence": ["Python source evidence: src/app.py"],
                }],
            }],
        })
        mutations = (
            ("candidate evidence", lambda value: value["technology_confirmation"]["candidates"][0]["evidence"].__setitem__(0, "fact\n## injected")),
            ("candidate conflict", lambda value: value["technology_confirmation"]["candidates"][0].__setitem__("conflicts", ["conflict\r## injected"])),
            ("confirmation evidence", lambda value: value["technology_confirmation"]["confirmation"].__setitem__("evidence", "reference\n## injected")),
            ("source evidence", lambda value: value["technology_skill_loadouts"][0]["sourceEvidence"][0]["evidence"].__setitem__(0, "fact\twith control")),
            ("unicode next line", lambda value: value["technology_confirmation"]["candidates"][0]["evidence"].__setitem__(0, "fact\u0085## injected")),
            ("unicode line separator", lambda value: value["technology_confirmation"]["candidates"][0]["evidence"].__setitem__(0, "fact\u2028## injected")),
            ("unicode paragraph separator", lambda value: value["technology_confirmation"]["candidates"][0]["evidence"].__setitem__(0, "fact\u2029## injected")),
        )
        for surface, mutate in mutations:
            with self.subTest(surface=surface):
                candidate = deepcopy(project)
                mutate(candidate)
                with self.assertRaisesRegex(ValueError, "single-line text without control characters"):
                    renderer.render(candidate)

        rejected = deepcopy(project)
        rejected["technology_confirmation"] = {
            "candidates": [{
                "scope": "src/**",
                "skill": "python",
                "evidence": ["Python source evidence: src/app.py"],
                "conflicts": ["not selected"],
                "disposition": "rejected",
            }],
            "accepted_skills": [],
            "rejections": [{"skill": "python", "reason": "reason\n## injected"}],
            "confirmation": {
                "status": "confirmed",
                "evidence": "user-message: no technology skills accepted",
            },
        }
        rejected["technology_skill_loadouts"] = []
        with self.assertRaisesRegex(ValueError, "single-line text without control characters"):
            renderer.render(rejected)

        no_variant = with_unset_workflows({
            "technology_skill_loadouts": [{
                "pathPattern": "config/**",
                "skills": [],
                "status": "NO_VARIANT",
                "fallback": "general model training\n## injected",
            }],
        })
        with self.assertRaisesRegex(ValueError, "single-line text without control characters"):
            renderer.render(no_variant)

    def test_explicit_activation_clause_requires_every_condition(self) -> None:
        toml_python = toml_capable_interpreter()
        for dependencies, expected in (([], False), (["example-framework"], True)):
            with self.subTest(dependencies=dependencies):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    project = root / "project"
                    skills = root / "skills"
                    project.mkdir()
                    (project / "main.py").write_text("value = 1\n", encoding="utf-8")
                    dependency_line = f"dependencies = {json.dumps(dependencies)}\n" if dependencies else ""
                    (project / "pyproject.toml").write_text(
                        '[project]\nname = "example"\nversion = "1"\n' + dependency_line,
                        encoding="utf-8",
                    )
                    skill_root = skills / "example-framework"
                    skill_root.mkdir(parents=True)
                    (skill_root / "SKILL.md").write_text(
                        "---\nname: example-framework\ndescription: Test framework.\n---\n",
                        encoding="utf-8",
                    )
                    registry = root / "registry.yaml"
                    registry.write_text(yaml.safe_dump({"skills": [{
                        "skill": "example-framework",
                        "kind": "technology",
                        "capabilities": ["application-framework"],
                        "activation": {"anyOf": [{"allOf": [
                            {"fileExtension": ".py"},
                            {"owningDependency": "example-framework"},
                        ]}]},
                        "companions": [],
                        "selection": "additive",
                        "priority": 100,
                        "requiredWhenDetected": True,
                    }]}), encoding="utf-8")

                    result = run_detection(
                        project,
                        "main.py",
                        interpreter=toml_python,
                        extra=["--registry", str(registry), "--skills-root", str(skills)],
                    )

                    self.assertEqual(expected, "example-framework" in result["loadouts"][0]["skills"])

    def test_compiler_option_predicate_schema_requires_exact_string_fields(self) -> None:
        builder = load_detection_builder_module()
        path = ROOT / "skills" / "typescript-esm" / "detection.yaml"
        predicate = {
            "glob": "tsconfig*.json",
            "name": "moduleResolution",
            "equals": "bundler",
        }

        self.assertEqual(
            predicate,
            builder.validate_mapping_predicate(
                "compilerOption",
                predicate,
                "activation.anyOf",
                path,
            ),
        )
        with self.assertRaisesRegex(ValueError, "requires"):
            builder.validate_mapping_predicate(
                "compilerOption",
                {"glob": "tsconfig*.json", "name": "moduleResolution"},
                "activation.anyOf",
                path,
            )
        with self.assertRaisesRegex(ValueError, "must be a non-empty string"):
            builder.validate_mapping_predicate(
                "compilerOption",
                {**predicate, "equals": ["bundler"]},
                "activation.anyOf",
                path,
            )

    def test_source_import_is_code_evidence_not_comment_or_string_text(self) -> None:
        cases = (
            ("from fastapi import FastAPI\n", True),
            ("# from fastapi import FastAPI\n", False),
            ('EXAMPLE = "from fastapi import FastAPI"\n', False),
        )
        for source, expected in cases:
            with self.subTest(source=source):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    project = root / "project"
                    skills = root / "skills"
                    project.mkdir()
                    (project / "main.py").write_text(source, encoding="utf-8")
                    skill_root = skills / "example-framework"
                    skill_root.mkdir(parents=True)
                    (skill_root / "SKILL.md").write_text(
                        "---\nname: example-framework\ndescription: Test framework.\n---\n",
                        encoding="utf-8",
                    )
                    registry = root / "registry.yaml"
                    registry.write_text(yaml.safe_dump({"skills": [{
                        "skill": "example-framework",
                        "kind": "technology",
                        "capabilities": ["application-framework"],
                        "activation": {"anyOf": [{"sourceImport": {
                            "module": "fastapi",
                            "extensions": [".py"],
                        }}]},
                        "companions": [],
                        "selection": "additive",
                        "priority": 100,
                        "requiredWhenDetected": True,
                    }]}), encoding="utf-8")

                    result = run_detection(
                        project,
                        "main.py",
                        extra=["--registry", str(registry), "--skills-root", str(skills)],
                    )

                    self.assertEqual(expected, "example-framework" in result["loadouts"][0]["skills"])

    def test_root_level_globstar_path_matches(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = root / "project"
            skills = root / "skills"
            route = project / "app" / "api" / "users" / "route.ts"
            route.parent.mkdir(parents=True)
            route.write_text("export const GET = () => new Response();\n", encoding="utf-8")
            skill_root = skills / "example-routes"
            skill_root.mkdir(parents=True)
            (skill_root / "SKILL.md").write_text(
                "---\nname: example-routes\ndescription: Test routes.\n---\n",
                encoding="utf-8",
            )
            registry = root / "registry.yaml"
            registry.write_text(yaml.safe_dump({"skills": [{
                "skill": "example-routes",
                "kind": "technology",
                "capabilities": ["http-api"],
                "activation": {"anyOf": [{"fileGlob": "**/app/api/**/route.ts"}]},
                "companions": [],
                "selection": "additive",
                "priority": 100,
                "requiredWhenDetected": True,
            }]}), encoding="utf-8")

            result = run_detection(
                project,
                "app/api",
                extra=["--registry", str(registry), "--skills-root", str(skills)],
            )

            self.assertEqual(["example-routes"], result["loadouts"][0]["skills"])

    def test_generated_registry_and_installed_detector_are_current(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(BUILD_SCRIPT), "--check"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)
        self.assertEqual(DETECT_SCRIPT.read_text(encoding="utf-8"), INSTALLED_DETECT_SCRIPT.read_text(encoding="utf-8"))

    def test_typescript_scope_has_exact_loadout(self) -> None:
        for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
            with self.subTest(detector=detector):
                result = run_detection(ROOT / "evals" / "projects" / "typescript-order-pricing", "src", detector=detector)
                self.assertEqual(["typescript", "typescript-esm", "typescript-strict"], result["loadouts"][0]["skills"])

    def test_typescript_es_module_configuration_is_jsonc_aware_and_case_insensitive(self) -> None:
        cases = (
            ("compact-esnext", '{"compilerOptions":{"module":"ESNext"}}', True),
            ("lowercase-esnext", '{"compilerOptions": { "module" : "esnext" }}', True),
            ("compact-bundler", '{"compilerOptions":{"moduleResolution":"bundler"}}', True),
            (
                "capitalized-bundler-with-trailing-commas",
                '{"compilerOptions": {"moduleResolution": "Bundler",},}',
                True,
            ),
            (
                "commented-out-bundler",
                '{"compilerOptions": {// "moduleResolution": "bundler"\n"noEmit": true}}',
                False,
            ),
            ("malformed-bundler", '{"compilerOptions":{"moduleResolution":"bundler"', False),
        )
        for name, configuration, expected in cases:
            with self.subTest(case=name), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                source = root / "src" / "main.ts"
                source.parent.mkdir()
                source.write_text("export const main = true;\n", encoding="utf-8")
                (root / "tsconfig.json").write_text(
                    configuration,
                    encoding="utf-8",
                )
                (root / "package.json").write_text(
                    '{"devDependencies":{"typescript":"1"}}\n',
                    encoding="utf-8",
                )
                registry = root / "source-registry.yaml"
                write_source_detection_registry(registry)

                for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                    with self.subTest(case=name, detector=detector):
                        result = run_detection(
                            root,
                            "src",
                            detector=detector,
                            extra=["--registry", str(registry)],
                        )

                        expected_skills = ["typescript", "typescript-esm"] if expected else ["typescript"]
                        self.assertEqual(expected_skills, result["loadouts"][0]["skills"])

    def test_typescript_es_module_detection_preserves_existing_activation_paths(self) -> None:
        cases = (
            (
                "package-module",
                '{"compilerOptions": {}}',
                '{"type": "module", "devDependencies": {"typescript": "1"}}',
            ),
            (
                "nodenext",
                '{"compilerOptions":{"module":"NodeNext"}}',
                '{"devDependencies":{"typescript":"1"}}',
            ),
        )
        for name, configuration, package in cases:
            with self.subTest(case=name), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                source = root / "src" / "main.ts"
                source.parent.mkdir()
                source.write_text("export const main = true;\n", encoding="utf-8")
                (root / "tsconfig.json").write_text(configuration, encoding="utf-8")
                (root / "package.json").write_text(package, encoding="utf-8")
                registry = root / "source-registry.yaml"
                write_source_detection_registry(registry)

                for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                    with self.subTest(case=name, detector=detector):
                        result = run_detection(
                            root,
                            "src",
                            detector=detector,
                            extra=["--registry", str(registry)],
                        )
                        self.assertEqual(
                            ["typescript", "typescript-esm"],
                            result["loadouts"][0]["skills"],
                        )

    def test_spring_boot_scope_has_exact_loadout(self) -> None:
        for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
            with self.subTest(detector=detector):
                result = run_detection(ROOT / "evals" / "projects" / "spring-boot-order-cancellation", "src/main", detector=detector)
                self.assertEqual(
                    ["java", "java-comment", "java-design", "spring-boot", "spring-boot-design", "sql"],
                    result["loadouts"][0]["skills"],
                )

    def test_java_source_selects_java_comment_additively_with_java(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "src" / "main" / "java" / "example"
            source.mkdir(parents=True)
            (source / "Order.java").write_text("class Order {}\n", encoding="utf-8")

            expected = ["java", "java-comment", "java-design"]
            for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                with self.subTest(detector=detector):
                    result = run_detection(root, "src/main", detector=detector)
                    self.assertEqual(expected, result["loadouts"][0]["skills"])

    def test_spring_data_jpa_composes_with_spring_design_and_sql(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "src" / "main" / "java" / "example"
            source.mkdir(parents=True)
            (source / "Order.java").write_text("class Order {}\n", encoding="utf-8")
            (root / "pom.xml").write_text(
                "<artifactId>spring-boot</artifactId>\n"
                "<artifactId>spring-boot-starter-data-jpa</artifactId>\n",
                encoding="utf-8",
            )

            expected = [
                "java",
                "java-comment",
                "java-design",
                "spring-boot",
                "spring-boot-design",
                "spring-data-jpa",
                "sql",
            ]
            for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                with self.subTest(detector=detector):
                    result = run_detection(root, "src/main", detector=detector)
                    self.assertEqual(expected, result["loadouts"][0]["skills"])

    def test_spring_boot_testing_requires_test_source_and_test_starter(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tests = root / "src" / "test" / "java" / "example"
            tests.mkdir(parents=True)
            (tests / "OrderTest.java").write_text("class OrderTest {}\n", encoding="utf-8")
            (root / "pom.xml").write_text(
                "<artifactId>spring-boot</artifactId>\n"
                "<artifactId>spring-boot-starter-test</artifactId>\n",
                encoding="utf-8",
            )

            expected = [
                "java",
                "java-comment",
                "java-design",
                "junit",
                "mockito",
                "spring-boot",
                "spring-boot-design",
                "spring-boot-testing",
            ]
            for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                with self.subTest(detector=detector):
                    result = run_detection(root, "src/test", detector=detector)
                    self.assertEqual(expected, result["loadouts"][0]["skills"])

    def test_blocking_quarkus_panache_composes_with_shared_persistence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "src" / "main" / "java" / "example"
            source.mkdir(parents=True)
            (source / "Order.java").write_text("class Order {}\n", encoding="utf-8")
            (root / "pom.xml").write_text(
                "<artifactId>quarkus-maven-plugin</artifactId>\n"
                "<artifactId>quarkus-hibernate-orm-panache</artifactId>\n",
                encoding="utf-8",
            )

            expected = [
                "hibernate-orm-panache",
                "java",
                "java-comment",
                "java-design",
                "quarkus",
                "quarkus-design",
                "quarkus-persistence",
                "sql",
            ]
            for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                with self.subTest(detector=detector):
                    result = run_detection(root, "src/main", detector=detector)
                    self.assertEqual(expected, result["loadouts"][0]["skills"])

    def test_reactive_quarkus_panache_does_not_select_blocking_panache(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "src" / "main" / "java" / "example"
            source.mkdir(parents=True)
            (source / "Order.java").write_text("class Order {}\n", encoding="utf-8")
            (root / "pom.xml").write_text(
                "<artifactId>quarkus-maven-plugin</artifactId>\n"
                "<artifactId>quarkus-hibernate-reactive-panache</artifactId>\n",
                encoding="utf-8",
            )

            expected = [
                "java",
                "java-comment",
                "java-design",
                "quarkus",
                "quarkus-design",
                "quarkus-persistence",
                "sql",
            ]
            for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                with self.subTest(detector=detector):
                    result = run_detection(root, "src/main", detector=detector)
                    self.assertEqual(expected, result["loadouts"][0]["skills"])

    def test_unrelated_quarkus_source_does_not_select_blocking_panache(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "src" / "main" / "java" / "example"
            source.mkdir(parents=True)
            (source / "GreetingResource.java").write_text("class GreetingResource {}\n", encoding="utf-8")
            (root / "pom.xml").write_text(
                "<artifactId>quarkus-maven-plugin</artifactId>\n"
                "<artifactId>quarkus-rest</artifactId>\n",
                encoding="utf-8",
            )

            expected = [
                "java",
                "java-comment",
                "java-design",
                "quarkus",
                "quarkus-design",
            ]
            for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                with self.subTest(detector=detector):
                    result = run_detection(root, "src/main", detector=detector)
                    self.assertEqual(expected, result["loadouts"][0]["skills"])

    def test_quarkus_testing_requires_test_source_and_test_dependency(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tests = root / "src" / "test" / "java" / "example"
            tests.mkdir(parents=True)
            (tests / "OrderTest.java").write_text("class OrderTest {}\n", encoding="utf-8")
            (root / "pom.xml").write_text(
                "<artifactId>quarkus-maven-plugin</artifactId>\n"
                "<artifactId>quarkus-junit</artifactId>\n",
                encoding="utf-8",
            )

            expected = [
                "java",
                "java-comment",
                "java-design",
                "junit",
                "quarkus",
                "quarkus-design",
                "quarkus-testing",
            ]
            for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                with self.subTest(detector=detector):
                    result = run_detection(root, "src/test", detector=detector)
                    self.assertEqual(expected, result["loadouts"][0]["skills"])

    def test_junit_and_mockito_compose_for_java_tests(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tests = root / "src" / "test" / "java" / "example"
            tests.mkdir(parents=True)
            (tests / "OrderTest.java").write_text(
                "import org.junit.jupiter.api.Test;\n"
                "import org.mockito.Mock;\n"
                "class OrderTest {}\n",
                encoding="utf-8",
            )
            (root / "pom.xml").write_text(
                "<artifactId>junit-jupiter</artifactId>\n"
                "<artifactId>mockito-core</artifactId>\n",
                encoding="utf-8",
            )

            expected = ["java", "java-comment", "java-design", "junit", "mockito"]
            for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                with self.subTest(detector=detector):
                    result = run_detection(root, "src/test", detector=detector)
                    self.assertEqual(expected, result["loadouts"][0]["skills"])

    def test_explicit_java_pattern_types_load_java_examples(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "src" / "main" / "java" / "example"
            source.mkdir(parents=True)
            for filename in (
                "OrderFactory.java",
                "RegistrySingleton.java",
                "GatewayAdapter.java",
                "MenuComposite.java",
                "StyleFlyweight.java",
                "PricingStrategy.java",
                "SubmitCommand.java",
                "EditorMemento.java",
                "StatusObserver.java",
                "TreeVisitor.java",
                "ExpressionInterpreter.java",
            ):
                (source / filename).write_text("class Example {}\n", encoding="utf-8")

            expected = [
                "java",
                "java-comment",
                "java-design",
                "java-design-pattern-examples",
            ]
            for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                with self.subTest(detector=detector):
                    result = run_detection(root, "src/main", detector=detector)
                    self.assertEqual(expected, result["loadouts"][0]["skills"])

    def test_ordinary_state_type_does_not_infer_state_pattern(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "src" / "main" / "java" / "example"
            source.mkdir(parents=True)
            (source / "OrderState.java").write_text("class OrderState {}\n", encoding="utf-8")

            expected = ["java", "java-comment", "java-design"]
            for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                with self.subTest(detector=detector):
                    result = run_detection(root, "src/main", detector=detector)
                    self.assertEqual(expected, result["loadouts"][0]["skills"])

    def test_explicit_typescript_pattern_types_load_typescript_examples(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "src"
            source.mkdir(parents=True)
            for filename in ("PricingStrategy.ts", "StyleFlyweight.ts", "ExpressionInterpreter.ts"):
                (source / filename).write_text("export class Example {}\n", encoding="utf-8")

            expected = [
                "typescript",
                "typescript-design-pattern-examples",
            ]
            for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                with self.subTest(detector=detector):
                    result = run_detection(root, "src", detector=detector)
                    self.assertEqual(expected, result["loadouts"][0]["skills"])

    def test_explicit_python_pattern_modules_load_python_examples(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "src"
            source.mkdir(parents=True)
            for filename in ("pricing_strategy_pattern.py", "style_flyweight_pattern.py", "expression_interpreter_pattern.py"):
                (source / filename).write_text("class Example:\n    pass\n", encoding="utf-8")

            expected = [
                "python",
                "python-design-pattern-examples",
            ]
            for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                with self.subTest(detector=detector):
                    result = run_detection(root, "src", detector=detector)
                    self.assertEqual(expected, result["loadouts"][0]["skills"])

    def test_liquibase_scope_composes_with_sql_without_jhipster(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            changelog = root / "src" / "main" / "resources" / "db" / "changelog"
            changelog.mkdir(parents=True)
            (root / "pom.xml").write_text(
                "<dependency><artifactId>liquibase-core</artifactId></dependency>\n",
                encoding="utf-8",
            )
            (changelog / "db.changelog-master.xml").write_text(
                "<databaseChangeLog/>\n",
                encoding="utf-8",
            )

            for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                with self.subTest(detector=detector):
                    result = run_detection(root, changelog.relative_to(root).as_posix(), detector=detector)
                    self.assertEqual(["liquibase", "sql"], result["loadouts"][0]["skills"])

    def test_liquibase_documentation_folder_does_not_activate_skill(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            notes = root / "docs" / "liquibase"
            notes.mkdir(parents=True)
            (root / "pom.xml").write_text(
                "<dependency><artifactId>liquibase-core</artifactId></dependency>\n",
                encoding="utf-8",
            )
            (notes / "example.xml").write_text("<databaseChangeLog/>\n", encoding="utf-8")

            for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                with self.subTest(detector=detector):
                    result = run_detection(root, notes.relative_to(root).as_posix(), detector=detector)
                    self.assertNotIn("liquibase", result["loadouts"][0]["skills"])

    def test_mysql_connector_manifests_compose_with_sql(self) -> None:
        cases = (
            (
                "maven",
                "pom.xml",
                "<dependency><groupId>com.mysql</groupId><artifactId>mysql-connector-j</artifactId></dependency>\n",
                "src/main/java/example/Application.java",
                "class Application {}\n",
                ["java", "java-comment", "java-design", "mysql", "sql"],
            ),
            (
                "gradle",
                "build.gradle.kts",
                'dependencies { runtimeOnly("com.mysql:mysql-connector-j:1") }\n',
                "src/main/kotlin/example/Application.kt",
                "class Application\n",
                ["mysql", "sql"],
            ),
            (
                "node",
                "package.json",
                '{"dependencies":{"mysql2":"1"}}\n',
                "src/database.ts",
                "export const database = {};\n",
                ["mysql", "sql", "typescript"],
            ),
            (
                "python",
                "pyproject.toml",
                '[project]\nname="orders"\nversion="1"\ndependencies=["mysql-connector-python>=1"]\n',
                "src/orders/database.py",
                "DATABASE = {}\n",
                ["mysql", "python", "sql"],
            ),
            (
                "python-requirements",
                "requirements-prod.txt",
                "PyMySQL==1\n",
                "src/orders/database.py",
                "DATABASE = {}\n",
                ["mysql", "python", "sql"],
            ),
        )
        for name, manifest_name, manifest, source_name, source, expected in cases:
            with self.subTest(case=name), tempfile.TemporaryDirectory() as directory:
                interpreter = toml_capable_interpreter() if manifest_name == "pyproject.toml" else sys.executable
                root = Path(directory) / "project"
                source_path = root / source_name
                source_path.parent.mkdir(parents=True)
                source_path.write_text(source, encoding="utf-8")
                (root / manifest_name).write_text(manifest, encoding="utf-8")
                registry = root.parent / "source-registry.yaml"
                write_source_detection_registry(registry)

                for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                    with self.subTest(case=name, detector=detector):
                        result = run_detection(
                            root,
                            "src",
                            detector=detector,
                            interpreter=interpreter,
                            extra=["--registry", str(registry)],
                        )
                        self.assertEqual(expected, result["loadouts"][0]["skills"])

    def test_mysql_connection_configuration_requires_pertinent_source(self) -> None:
        cases = (
            (
                "connection-uri",
                "src/main.ts",
                "export const start = () => true;\n",
                "src/config/database.yaml",
                "url: mysql://db.example/orders\n",
                "package.json",
                '{"dependencies":{}}\n',
                ["mysql", "sql", "typescript"],
            ),
            (
                "jdbc-url",
                "src/main/java/example/Application.java",
                "class Application {}\n",
                "src/main/resources/application.properties",
                "datasource.url=jdbc:mysql://db.example/orders\n",
                "pom.xml",
                "<project/>\n",
                ["java", "java-comment", "java-design", "mysql", "sql"],
            ),
        )
        for name, source_name, source, config_name, config, manifest_name, manifest, expected in cases:
            with self.subTest(case=name), tempfile.TemporaryDirectory() as directory:
                root = Path(directory) / "project"
                source_path = root / source_name
                configuration = root / config_name
                source_path.parent.mkdir(parents=True)
                configuration.parent.mkdir(parents=True)
                source_path.write_text(source, encoding="utf-8")
                configuration.write_text(config, encoding="utf-8")
                (root / manifest_name).write_text(manifest, encoding="utf-8")
                registry = root.parent / "source-registry.yaml"
                write_source_detection_registry(registry)

                for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                    with self.subTest(case=name, detector=detector):
                        result = run_detection(
                            root,
                            "src",
                            detector=detector,
                            extra=["--registry", str(registry)],
                        )
                        self.assertEqual(expected, result["loadouts"][0]["skills"])

                configuration.unlink()
                expected_without_configuration = [
                    skill for skill in expected if skill not in {"mysql", "sql"}
                ]
                for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                    with self.subTest(case=name, detector=detector, configuration="removed"):
                        result = run_detection(
                            root,
                            "src",
                            detector=detector,
                            extra=["--registry", str(registry)],
                        )
                        self.assertEqual(expected_without_configuration, result["loadouts"][0]["skills"])

    def test_mysql_documentation_and_sample_configuration_do_not_activate(self) -> None:
        cases = (
            ("docs", "README.md", "Use mysql-connector-j with jdbc:mysql://db.example/orders.\n"),
            ("examples", "application-example.yaml", "url: mysql://db.example/orders\n"),
        )
        for scope, filename, content in cases:
            with self.subTest(scope=scope), tempfile.TemporaryDirectory() as directory:
                root = Path(directory) / "project"
                evidence = root / scope / filename
                evidence.parent.mkdir(parents=True)
                evidence.write_text(content, encoding="utf-8")
                (root / "package.json").write_text(
                    '{"dependencies":{"mysql2":"1"}}\n',
                    encoding="utf-8",
                )
                registry = root.parent / "source-registry.yaml"
                write_source_detection_registry(registry)

                for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                    with self.subTest(scope=scope, detector=detector):
                        result = run_detection(
                            root,
                            scope,
                            detector=detector,
                            extra=["--registry", str(registry)],
                        )
                        self.assertNotIn("mysql", result["loadouts"][0]["skills"])

    def test_mysql_root_scope_does_not_pair_source_with_documentation_config(self) -> None:
        cases = (
            ("docs", "docs/mysql.properties", "datasource.url=jdbc:mysql://db.example/orders\n"),
            ("examples", "examples/application-example.yaml", "url: mysql://db.example/orders\n"),
            ("env-example", ".env.example", "DATABASE_URL=mysql://db.example/orders\n"),
        )
        for name, evidence_name, content in cases:
            with self.subTest(case=name), tempfile.TemporaryDirectory() as directory:
                root = Path(directory) / "project"
                source = root / "src" / "main.ts"
                evidence = root / evidence_name
                source.parent.mkdir(parents=True)
                evidence.parent.mkdir(parents=True, exist_ok=True)
                source.write_text("export const start = () => true;\n", encoding="utf-8")
                evidence.write_text(content, encoding="utf-8")
                (root / "package.json").write_text('{"dependencies":{}}\n', encoding="utf-8")
                registry = root.parent / "source-registry.yaml"
                write_source_detection_registry(registry)

                for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                    with self.subTest(case=name, detector=detector):
                        result = run_detection(
                            root,
                            ".",
                            detector=detector,
                            extra=["--registry", str(registry)],
                        )
                        self.assertEqual(["typescript"], result["loadouts"][0]["skills"])

    def test_mysql_sibling_module_does_not_contaminate_selected_scope(self) -> None:
        toml_python = toml_capable_interpreter()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "project"
            service_source = root / "service" / "src" / "main.py"
            example_source = root / "example" / "src" / "database.ts"
            service_source.parent.mkdir(parents=True)
            example_source.parent.mkdir(parents=True)
            service_source.write_text("value = 1\n", encoding="utf-8")
            example_source.write_text("export const database = {};\n", encoding="utf-8")
            (root / "service" / "pyproject.toml").write_text(
                '[project]\nname="service"\nversion="1"\n',
                encoding="utf-8",
            )
            (root / "example" / "package.json").write_text(
                '{"dependencies":{"mysql2":"1"}}\n',
                encoding="utf-8",
            )
            registry = root.parent / "source-registry.yaml"
            write_source_detection_registry(registry)

            for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                with self.subTest(detector=detector):
                    result = run_detection(
                        root,
                        "service/src",
                        detector=detector,
                        interpreter=toml_python,
                        extra=["--registry", str(registry)],
                    )
                    self.assertEqual(["python"], result["loadouts"][0]["skills"])

    def test_quartz_maven_and_gradle_evidence_composes_with_java(self) -> None:
        cases = (
            (
                "maven",
                "pom.xml",
                "<dependency><groupId>org.quartz-scheduler</groupId><artifactId>quartz</artifactId></dependency>\n",
            ),
            (
                "gradle",
                "build.gradle.kts",
                'dependencies { implementation("org.quartz-scheduler:quartz:2.5.0") }\n',
            ),
        )
        for name, manifest_name, manifest in cases:
            with self.subTest(case=name), tempfile.TemporaryDirectory() as directory:
                root = Path(directory) / "project"
                source = root / "src" / "main" / "java" / "example" / "CleanupJob.java"
                source.parent.mkdir(parents=True)
                source.write_text("class CleanupJob {}\n", encoding="utf-8")
                (root / manifest_name).write_text(manifest, encoding="utf-8")
                registry = root.parent / "source-registry.yaml"
                write_source_detection_registry(registry)

                for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                    with self.subTest(case=name, detector=detector):
                        result = run_detection(
                            root,
                            "src/main",
                            detector=detector,
                            extra=["--registry", str(registry)],
                        )
                        skills = result["loadouts"][0]["skills"]
                        self.assertIn("java", skills)
                        self.assertIn("quartz", skills)

    def test_quartz_documentation_and_sibling_dependency_do_not_activate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "project"
            service = root / "service"
            source = service / "src" / "main" / "java" / "example" / "Application.java"
            source.parent.mkdir(parents=True)
            source.write_text("class Application {}\n", encoding="utf-8")
            (service / "pom.xml").write_text("<project/>\n", encoding="utf-8")
            sibling = root / "examples"
            sibling.mkdir()
            (sibling / "pom.xml").write_text(
                "<dependency><groupId>org.quartz-scheduler</groupId><artifactId>quartz</artifactId></dependency>\n",
                encoding="utf-8",
            )
            (service / "README.md").write_text("Use Quartz Scheduler jobs.\n", encoding="utf-8")
            registry = root.parent / "source-registry.yaml"
            write_source_detection_registry(registry)

            for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                with self.subTest(detector=detector):
                    result = run_detection(
                        root,
                        "service/src",
                        detector=detector,
                        extra=["--registry", str(registry)],
                    )
                    self.assertNotIn("quartz", result["loadouts"][0]["skills"])

    def test_mapstruct_maven_and_gradle_evidence_composes_with_java(self) -> None:
        cases = (
            (
                "maven",
                "pom.xml",
                "<dependency><groupId>org.mapstruct</groupId><artifactId>mapstruct</artifactId></dependency>\n",
            ),
            (
                "gradle",
                "build.gradle.kts",
                'dependencies { annotationProcessor("org.mapstruct:mapstruct-processor:1.6.3") }\n',
            ),
        )
        for name, manifest_name, manifest in cases:
            with self.subTest(case=name), tempfile.TemporaryDirectory() as directory:
                root = Path(directory) / "project"
                source = root / "src" / "main" / "java" / "example" / "OrderMapper.java"
                source.parent.mkdir(parents=True)
                source.write_text(
                    "import org.mapstruct.Mapper;\n@Mapper interface OrderMapper {}\n",
                    encoding="utf-8",
                )
                (root / manifest_name).write_text(manifest, encoding="utf-8")
                registry = root.parent / "source-registry.yaml"
                write_source_detection_registry(registry)

                for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                    with self.subTest(case=name, detector=detector):
                        result = run_detection(
                            root,
                            "src/main",
                            detector=detector,
                            extra=["--registry", str(registry)],
                        )
                        skills = result["loadouts"][0]["skills"]
                        self.assertIn("java", skills)
                        self.assertIn("mapstruct", skills)

    def test_mapstruct_generated_output_and_sibling_dependency_do_not_activate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "project"
            service = root / "service"
            generated = service / "src" / "generated" / "java" / "example" / "OrderMapperImpl.java"
            generated.parent.mkdir(parents=True)
            generated.write_text("class OrderMapperImpl {}\n", encoding="utf-8")
            (service / "pom.xml").write_text("<project/>\n", encoding="utf-8")
            sibling = root / "other"
            sibling.mkdir()
            (sibling / "pom.xml").write_text(
                "<dependency><artifactId>mapstruct-processor</artifactId></dependency>\n",
                encoding="utf-8",
            )
            registry = root.parent / "source-registry.yaml"
            write_source_detection_registry(registry)

            for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                with self.subTest(detector=detector):
                    result = run_detection(
                        root,
                        "service/src",
                        detector=detector,
                        extra=["--registry", str(registry)],
                    )
                    self.assertNotIn("mapstruct", result["loadouts"][0]["skills"])

    def test_jhipster_scope_composes_focused_skills_with_java_and_spring_boot(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".jhipster").mkdir()
            (root / "src" / "main" / "java" / "example" / "config").mkdir(parents=True)
            (root / "src" / "main" / "resources" / "config" / "liquibase").mkdir(parents=True)
            (root / "src" / "test" / "java" / "example").mkdir(parents=True)
            (root / ".yo-rc.json").write_text(
                '{"generator-jhipster":{"baseName":"sample","jhipsterVersion":"9.1.0"}}\n',
                encoding="utf-8",
            )
            (root / "pom.xml").write_text(
                "<artifactId>spring-boot</artifactId>\n<artifactId>archunit-junit5</artifactId>\n",
                encoding="utf-8",
            )
            (root / ".jhipster" / "Order.json").write_text("{}\n", encoding="utf-8")
            (root / "src" / "main" / "java" / "example" / "Application.java").write_text(
                "class Application {}\n",
                encoding="utf-8",
            )
            (root / "src" / "main" / "java" / "example" / "config" / "SecurityConfiguration.java").write_text(
                "class SecurityConfiguration {}\n",
                encoding="utf-8",
            )
            (root / "src" / "main" / "resources" / "config" / "liquibase" / "master.xml").write_text(
                "<databaseChangeLog/>\n",
                encoding="utf-8",
            )
            (root / "src" / "test" / "java" / "example" / "TechnicalStructureTest.java").write_text(
                "class TechnicalStructureTest {}\n",
                encoding="utf-8",
            )

            expected = [
                "java",
                "java-comment",
                "java-design",
                "jhipster-domain-modeling",
                "jhipster-persistence",
                "jhipster-project",
                "jhipster-security",
                "jhipster-testing",
                "liquibase",
                "spring-boot",
                "spring-boot-design",
                "sql",
            ]
            for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                with self.subTest(detector=detector):
                    result = run_detection(root, ".", detector=detector)
                    self.assertEqual(expected, result["loadouts"][0]["skills"])

    def test_jhipster_concern_paths_do_not_activate_without_an_owning_marker(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "src" / "main" / "java" / "example" / "config"
            tests = root / "src" / "test" / "java" / "example"
            liquibase = root / "src" / "main" / "resources" / "config" / "liquibase"
            source.mkdir(parents=True)
            tests.mkdir(parents=True)
            liquibase.mkdir(parents=True)
            (root / ".jhipster").mkdir()
            (root / "pom.xml").write_text("<artifactId>spring-boot</artifactId>\n", encoding="utf-8")
            (source / "Application.java").write_text("class Application {}\n", encoding="utf-8")
            (source / "SecurityConfiguration.java").write_text("class SecurityConfiguration {}\n", encoding="utf-8")
            (tests / "ApplicationTest.java").write_text("class ApplicationTest {}\n", encoding="utf-8")
            (liquibase / "master.xml").write_text("<databaseChangeLog/>\n", encoding="utf-8")
            (root / ".jhipster" / "Order.json").write_text("{}\n", encoding="utf-8")

            for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                with self.subTest(detector=detector):
                    result = run_detection(root, ".", detector=detector)
                    self.assertFalse(any(skill.startswith("jhipster-") for skill in result["loadouts"][0]["skills"]))

    def test_jhipster_generator_config_requires_a_version(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "src" / "main" / "java" / "example"
            source.mkdir(parents=True)
            (root / ".yo-rc.json").write_text(
                '{"generator-jhipster":{"baseName":"sample"}}\n',
                encoding="utf-8",
            )
            (root / "pom.xml").write_text("<artifactId>spring-boot</artifactId>\n", encoding="utf-8")
            (source / "Application.java").write_text("class Application {}\n", encoding="utf-8")

            for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                with self.subTest(detector=detector):
                    result = run_detection(root, ".", detector=detector)
                    self.assertNotIn("jhipster-project", result["loadouts"][0]["skills"])

    def test_nested_jhipster_example_does_not_supply_the_owning_marker(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "src" / "main" / "java" / "example"
            example = root / "docs" / "jhipster-example"
            source.mkdir(parents=True)
            example.mkdir(parents=True)
            (root / "pom.xml").write_text("<artifactId>spring-boot</artifactId>\n", encoding="utf-8")
            (source / "Application.java").write_text("class Application {}\n", encoding="utf-8")
            (example / ".yo-rc.json").write_text(
                '{"generator-jhipster":{"jhipsterVersion":"9.1.0"}}\n',
                encoding="utf-8",
            )

            for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                with self.subTest(detector=detector):
                    result = run_detection(root, ".", detector=detector)
                    self.assertNotIn("jhipster-project", result["loadouts"][0]["skills"])

    def test_jhipster_gradle_runtime_marker_works_without_generator_config(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "src" / "main" / "java" / "example"
            source.mkdir(parents=True)
            (root / "build.gradle.kts").write_text(
                'plugins { id("org.springframework.boot") }\n'
                'dependencies { implementation("tech.jhipster:jhipster-framework:9.1.0") }\n',
                encoding="utf-8",
            )
            (source / "GatewayApplication.java").write_text("class GatewayApplication {}\n", encoding="utf-8")

            for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                with self.subTest(detector=detector):
                    result = run_detection(root, ".", detector=detector)
                    self.assertIn("jhipster-project", result["loadouts"][0]["skills"])

    def test_non_java_jhipster_generator_scope_is_no_variant(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "package.json").write_text(
                '{"devDependencies":{"generator-jhipster":"9.1.0"}}\n',
                encoding="utf-8",
            )
            (root / ".yo-rc.json").write_text(
                '{"generator-jhipster":{"jhipsterVersion":"9.1.0"}}\n',
                encoding="utf-8",
            )

            for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                with self.subTest(detector=detector):
                    result = run_detection(root, ".yo-rc.json", detector=detector)
                    self.assertEqual("NO_VARIANT", result["loadouts"][0]["status"])
                    self.assertEqual([], result["loadouts"][0]["skills"])

    def test_python_scope_has_exact_loadout(self) -> None:
        toml_python = toml_capable_interpreter()
        for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
            with self.subTest(detector=detector):
                result = run_detection(
                    ROOT / "evals" / "projects" / "python-inventory",
                    "src",
                    detector=detector,
                    interpreter=toml_python,
                )
                self.assertEqual(["python"], result["loadouts"][0]["skills"])

    def test_python_cli_filename_does_not_activate_node_cli(self) -> None:
        toml_python = toml_capable_interpreter()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "src").mkdir()
            (root / "src" / "cli.py").write_text("def main():\n    return 0\n", encoding="utf-8")
            (root / "pyproject.toml").write_text(
                '[project]\nname="python-cli"\nversion="1"\n',
                encoding="utf-8",
            )
            for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                with self.subTest(detector=detector):
                    result = run_detection(root, "src", detector=detector, interpreter=toml_python)
                    self.assertEqual(["python"], result["loadouts"][0]["skills"])

    def test_node_cli_requires_a_javascript_or_typescript_cli_path(self) -> None:
        cases = (
            ("tool-cli.js", ["node-cli"]),
            ("tool-cli.ts", ["node-cli", "typescript"]),
            ("client.ts", ["typescript"]),
        )
        for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
            for file_name, expected in cases:
                with self.subTest(detector=detector, file_name=file_name):
                    with tempfile.TemporaryDirectory() as directory:
                        root = Path(directory)
                        (root / "src").mkdir()
                        (root / "src" / file_name).write_text("export const run = () => 0;\n", encoding="utf-8")
                        (root / "package.json").write_text(
                            '{"name":"node-cli","version":"1","bin":{"tool":"src/tool-cli.js"}}\n',
                            encoding="utf-8",
                        )
                        result = run_detection(root, "src", detector=detector)
                        self.assertEqual(expected, result["loadouts"][0]["skills"])

    def test_fastapi_scope_composes_with_python(self) -> None:
        toml_python = toml_capable_interpreter()
        for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
            with self.subTest(detector=detector):
                result = run_detection(
                    ROOT / "evals" / "projects" / "fastapi-orders",
                    "app",
                    detector=detector,
                    interpreter=toml_python,
                )
                self.assertEqual(["fastapi", "python"], result["loadouts"][0]["skills"])
                evidence = {row["skill"]: row["evidence"] for row in result["loadouts"][0]["sourceEvidence"]}
                self.assertTrue(any("fastapi" in value.lower() for value in evidence["fastapi"]))

    def test_fastapi_import_text_in_detector_tests_does_not_activate_fastapi(self) -> None:
        result = run_detection(ROOT, "scripts")
        self.assertEqual(["python"], result["loadouts"][0]["skills"])

    def test_next_api_routes_require_code_and_the_owning_next_dependency(self) -> None:
        cases = (
            ("route.py", {"next": "1"}, ["python"]),
            ("route.ts", {}, ["typescript"]),
            ("route.ts", {"next": "1"}, ["api-routes", "nextjs-app-router", "typescript"]),
        )
        for file_name, dependencies, expected in cases:
            with self.subTest(file_name=file_name, dependencies=dependencies):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    route = root / "app" / "api" / "users" / file_name
                    route.parent.mkdir(parents=True)
                    route.write_text("value = 1\n", encoding="utf-8")
                    (root / "package.json").write_text(
                        json.dumps({"dependencies": dependencies}) + "\n",
                        encoding="utf-8",
                    )
                    result = run_detection(root, "app")
                    self.assertEqual(expected, result["loadouts"][0]["skills"])

    def test_react_server_components_requires_next_app_router_evidence(self) -> None:
        cases = (
            ("App.tsx", {"react": "1"}, False),
            ("page.tsx", {"next": "1"}, True),
        )
        for file_name, dependencies, expected in cases:
            with self.subTest(file_name=file_name, dependencies=dependencies):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    component = root / "app" / file_name
                    component.parent.mkdir(parents=True)
                    component.write_text("export default function Component() { return null; }\n", encoding="utf-8")
                    (root / "package.json").write_text(
                        json.dumps({"dependencies": dependencies}) + "\n",
                        encoding="utf-8",
                    )
                    result = run_detection(root, "app")
                    self.assertEqual(
                        expected,
                        "react-server-components" in result["loadouts"][0]["skills"],
                    )

    def test_domain_detector_names_in_non_code_files_do_not_activate_product_skills(self) -> None:
        cases = (
            ("docs/harness-design.md", "agent harness\n"),
            ("docs/tool-runtime.md", "tool runtime\n"),
            ("docs/plan-engine.md", "plan engine\n"),
            ("docs/local-model.md", "localModel\n"),
            ("plans/example.yaml", "steps: []\n"),
        )
        for file_name, content in cases:
            with self.subTest(file_name=file_name):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    path = root / file_name
                    path.parent.mkdir(parents=True)
                    path.write_text(content, encoding="utf-8")
                    result = run_detection(root, path.parent.relative_to(root).as_posix())
                    self.assertEqual([], result["loadouts"][0]["skills"])

    def test_domain_detectors_accept_matching_code_artifacts(self) -> None:
        cases = (
            ("agent-harness.ts", "export const value = 1;\n", ["agent-harness", "typescript"]),
            ("tool-runtime.py", "value = 1\n", ["python", "tool-runtime"]),
            ("plan-engine.go", "package plan\n", ["plan-engine"]),
            ("local-model.ts", "export const localModel = true;\n", ["local-model-integration", "typescript"]),
        )
        for file_name, content, expected in cases:
            with self.subTest(file_name=file_name):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    (root / "src").mkdir()
                    (root / "src" / file_name).write_text(content, encoding="utf-8")
                    result = run_detection(root, "src")
                    self.assertEqual(expected, result["loadouts"][0]["skills"])

    def test_mixed_repository_produces_separate_scope_loadouts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "web" / "src").mkdir(parents=True)
            (root / "api" / "app").mkdir(parents=True)
            (root / "web" / "src" / "main.ts").write_text("export const value = 1;\n", encoding="utf-8")
            (root / "web" / "package.json").write_text('{"devDependencies":{"typescript":"1"}}\n', encoding="utf-8")
            (root / "api" / "app" / "main.py").write_text("from fastapi import FastAPI\n", encoding="utf-8")
            (root / "api" / "requirements.txt").write_text("fastapi==1.0\n", encoding="utf-8")
            for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                with self.subTest(detector=detector):
                    result = run_detection(root, "web/src", "api/app", detector=detector)
                    self.assertEqual(["typescript"], result["loadouts"][0]["skills"])
                    self.assertEqual(["fastapi", "python"], result["loadouts"][1]["skills"])

    def test_root_workspace_dependencies_do_not_contaminate_owned_child(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "packages" / "core" / "src").mkdir(parents=True)
            (root / "packages" / "core" / "src" / "entry.ts").write_text("export const value = 1;\n", encoding="utf-8")
            (root / "package.json").write_text('{"dependencies":{"next":"1","@clerk/nextjs":"1"}}\n', encoding="utf-8")
            (root / "packages" / "core" / "package.json").write_text('{"dependencies":{}}\n', encoding="utf-8")
            result = run_detection(root, "packages/core/src")
            self.assertEqual(["typescript"], result["loadouts"][0]["skills"])

    def test_sibling_spring_module_does_not_contaminate_python_scope(self) -> None:
        toml_python = toml_capable_interpreter()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "python" / "src").mkdir(parents=True)
            (root / "java" / "src").mkdir(parents=True)
            (root / "python" / "src" / "main.py").write_text("value = 1\n", encoding="utf-8")
            (root / "python" / "pyproject.toml").write_text('[project]\nname="python"\nversion="1"\n', encoding="utf-8")
            (root / "java" / "src" / "Main.java").write_text("class Main {}\n", encoding="utf-8")
            (root / "java" / "pom.xml").write_text("<artifactId>spring-boot</artifactId>\n", encoding="utf-8")
            result = run_detection(root, "python/src", interpreter=toml_python)
            self.assertEqual(["python"], result["loadouts"][0]["skills"])

    def test_missing_detected_required_skill_blocks_setup(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = root / "project"
            skills = root / "skills"
            project.mkdir()
            skills.mkdir()
            (project / "main.py").write_text("value = 1\n", encoding="utf-8")
            registry = root / "registry.yaml"
            registry.write_text(yaml.safe_dump({"skills": [{
                "skill": "missing-python",
                "kind": "technology",
                "capabilities": ["language-coding"],
                "activation": {"anyOf": [{"fileExtension": ".py"}]},
                "companions": [],
                "selection": "additive",
                "priority": 100,
                "requiredWhenDetected": True,
            }]}), encoding="utf-8")
            for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                with self.subTest(detector=detector):
                    result = run_detection(
                        project,
                        "main.py",
                        expected_code=2,
                        detector=detector,
                        extra=["--registry", str(registry), "--skills-root", str(skills)],
                    )
                    self.assertEqual("BLOCKED", result["loadouts"][0]["status"])
                    self.assertEqual("missing-python", result["loadouts"][0]["missingRequiredSkills"][0]["skill"])

    def test_explicit_runtime_catalog_overrides_methodology_source_skills(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = root / "project"
            skills = root / "skills"
            project.mkdir()
            skill_root = skills / "example-python"
            skill_root.mkdir(parents=True)
            (skill_root / "SKILL.md").write_text(
                "---\nname: example-python\ndescription: Test runtime catalog.\n---\n",
                encoding="utf-8",
            )
            (project / "main.py").write_text("value = 1\n", encoding="utf-8")
            registry = root / "registry.yaml"
            registry.write_text(yaml.safe_dump({"skills": [{
                "skill": "example-python",
                "kind": "technology",
                "capabilities": ["language-coding"],
                "activation": {"anyOf": [{"fileExtension": ".py"}]},
                "companions": [],
                "selection": "additive",
                "priority": 100,
                "requiredWhenDetected": True,
            }]}), encoding="utf-8")

            blocked = run_detection(
                project,
                "main.py",
                expected_code=2,
                extra=[
                    "--registry", str(registry),
                    "--skills-root", str(skills),
                    "--available-skill", "another-skill",
                ],
            )
            self.assertEqual("BLOCKED", blocked["loadouts"][0]["status"])
            self.assertEqual(
                "UNAVAILABLE",
                blocked["loadouts"][0]["sourceEvidence"][0]["runtimeAvailability"],
            )
            self.assertEqual(
                ["another-skill"],
                blocked["runtimeSkillCatalog"]["availableSkills"],
            )

            ready = run_detection(
                project,
                "main.py",
                extra=[
                    "--registry", str(registry),
                    "--skills-root", str(skills),
                    "--available-skill", "example-python",
                ],
            )
            self.assertEqual("READY", ready["loadouts"][0]["status"])
            self.assertEqual(
                "AVAILABLE",
                ready["loadouts"][0]["sourceEvidence"][0]["runtimeAvailability"],
            )

    def test_equal_priority_exclusive_matches_block_setup(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = root / "project"
            skills = root / "skills"
            project.mkdir()
            (project / "example.mix").write_text("mixed\n", encoding="utf-8")
            entries = []
            for skill in ("variant-one", "variant-two"):
                skill_root = skills / skill
                skill_root.mkdir(parents=True)
                (skill_root / "SKILL.md").write_text(f"---\nname: {skill}\ndescription: Test variant.\n---\n", encoding="utf-8")
                entries.append({
                    "skill": skill,
                    "kind": "technology",
                    "capabilities": ["language-coding"],
                    "activation": {"anyOf": [{"fileExtension": ".mix"}]},
                    "companions": [],
                    "selection": "exclusive",
                    "exclusiveGroup": "mixed-language",
                    "priority": 10,
                    "requiredWhenDetected": True,
                })
            registry = root / "registry.yaml"
            registry.write_text(yaml.safe_dump({"skills": entries}), encoding="utf-8")
            for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                with self.subTest(detector=detector):
                    result = run_detection(
                        project,
                        "example.mix",
                        expected_code=2,
                        detector=detector,
                        extra=["--registry", str(registry), "--skills-root", str(skills)],
                    )
                    self.assertEqual(["variant-one", "variant-two"], result["loadouts"][0]["exclusiveConflicts"][0]["skills"])

    def test_no_variant_is_explicit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.txt").write_text("plain\n", encoding="utf-8")
            result = run_detection(root, "README.txt")
            self.assertEqual("NO_VARIANT", result["loadouts"][0]["status"])
            self.assertEqual([], result["loadouts"][0]["skills"])

    def test_parser_free_runtime_blocks_only_pyproject_scopes(self) -> None:
        """Block pyproject scopes while preserving detection on a parser-free runtime."""
        python = parser_free_interpreter()

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            pyproject_project = root / "pyproject-project"
            plain_project = root / "plain-project"
            skills = root / "skills"
            pyproject_project.mkdir()
            plain_project.mkdir()
            (pyproject_project / "main.py").write_text("value = 1\n", encoding="utf-8")
            (pyproject_project / "pyproject.toml").write_text(
                "[project]\n"
                'name = "example"\n'
                'dependencies = ["FastAPI>=0.115"]\n',
                encoding="utf-8",
            )
            (plain_project / "main.py").write_text("value = 1\n", encoding="utf-8")
            (plain_project / "README.txt").write_text("plain\n", encoding="utf-8")
            for skill in ("example-fastapi", "example-python"):
                skill_root = skills / skill
                skill_root.mkdir(parents=True)
                (skill_root / "SKILL.md").write_text(
                    f"---\nname: {skill}\ndescription: Test Python 3.9 prerequisites.\n---\n",
                    encoding="utf-8",
                )
            registry = root / "registry.yaml"
            registry.write_text(yaml.safe_dump({"skills": [
                {
                    "skill": "example-fastapi",
                    "kind": "technology",
                    "capabilities": ["web-framework"],
                    "activation": {"anyOf": [{"owningDependency": "fastapi"}]},
                    "companions": [],
                    "selection": "additive",
                    "priority": 100,
                    "requiredWhenDetected": True,
                },
                {
                    "skill": "example-python",
                    "kind": "technology",
                    "capabilities": ["language-coding"],
                    "activation": {"anyOf": [{"fileExtension": ".py"}]},
                    "companions": [],
                    "selection": "additive",
                    "priority": 110,
                    "requiredWhenDetected": True,
                },
            ]}), encoding="utf-8")

            for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                with self.subTest(detector=detector, outcome="BLOCKED_PREREQUISITE"):
                    blocked_prerequisite = run_detection(
                        pyproject_project,
                        "main.py",
                        expected_code=2,
                        detector=detector,
                        interpreter=python,
                        extra=["--registry", str(registry), "--skills-root", str(skills)],
                    )
                    self.assertEqual("BLOCKED", blocked_prerequisite["loadouts"][0]["status"])
                    self.assertEqual([], blocked_prerequisite["loadouts"][0]["skills"])
                    self.assertEqual(
                        ["missing runtime prerequisite: install tomli or use Python 3.11+ to read pyproject.toml"],
                        blocked_prerequisite["loadouts"][0]["scopeErrors"],
                    )

                with self.subTest(detector=detector, outcome="READY"):
                    ready = run_detection(
                        plain_project,
                        "main.py",
                        detector=detector,
                        interpreter=python,
                        extra=["--registry", str(registry), "--skills-root", str(skills)],
                    )
                    self.assertEqual("READY", ready["loadouts"][0]["status"])
                    self.assertEqual(["example-python"], ready["loadouts"][0]["skills"])

                with self.subTest(detector=detector, outcome="BLOCKED"):
                    blocked = run_detection(
                        plain_project,
                        "main.py",
                        expected_code=2,
                        detector=detector,
                        interpreter=python,
                        extra=[
                            "--registry", str(registry),
                            "--skills-root", str(skills),
                            "--available-skill", "unrelated-skill",
                        ],
                    )
                    self.assertEqual("BLOCKED", blocked["loadouts"][0]["status"])

                with self.subTest(detector=detector, outcome="NO_VARIANT"):
                    no_variant = run_detection(
                        plain_project,
                        "README.txt",
                        detector=detector,
                        interpreter=python,
                        extra=["--registry", str(registry), "--skills-root", str(skills)],
                    )
                    self.assertEqual("NO_VARIANT", no_variant["loadouts"][0]["status"])

    def test_tomllib_parses_quoted_optional_dependency_table(self) -> None:
        """Keep valid quoted TOML table syntax on the standard parser path."""
        python = toml_capable_interpreter()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = root / "project"
            skills = root / "skills"
            project.mkdir()
            (project / "main.py").write_text("value = 1\n", encoding="utf-8")
            (project / "pyproject.toml").write_text(
                '["project"."optional-dependencies"]\n'
                'web = ["FastAPI>=0.115"]\n',
                encoding="utf-8",
            )
            skill_root = skills / "example-fastapi"
            skill_root.mkdir(parents=True)
            (skill_root / "SKILL.md").write_text(
                "---\nname: example-fastapi\ndescription: Test quoted TOML tables.\n---\n",
                encoding="utf-8",
            )
            registry = root / "registry.yaml"
            registry.write_text(yaml.safe_dump({"skills": [{
                "skill": "example-fastapi",
                "kind": "technology",
                "capabilities": ["web-framework"],
                "activation": {"anyOf": [{"owningDependency": "fastapi"}]},
                "companions": [],
                "selection": "additive",
                "priority": 100,
                "requiredWhenDetected": True,
            }]}), encoding="utf-8")

            for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                with self.subTest(detector=detector):
                    result = run_detection(
                        project,
                        "main.py",
                        detector=detector,
                        interpreter=python,
                        extra=["--registry", str(registry), "--skills-root", str(skills)],
                    )
                    self.assertEqual(["example-fastapi"], result["loadouts"][0]["skills"])

    def test_malformed_pyproject_never_yields_false_dependency_detection(self) -> None:
        """Reject partial dependency evidence from a malformed pyproject document."""
        parser_free_python = parser_free_interpreter()
        toml_python = toml_capable_interpreter()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = root / "project"
            skills = root / "skills"
            project.mkdir()
            (project / "main.py").write_text("value = 1\n", encoding="utf-8")
            (project / "pyproject.toml").write_text(
                "[project]\n"
                'dependencies = ["FastAPI>=0.115"]\n'
                "this is not valid TOML\n",
                encoding="utf-8",
            )
            skill_root = skills / "example-fastapi"
            skill_root.mkdir(parents=True)
            (skill_root / "SKILL.md").write_text(
                "---\nname: example-fastapi\ndescription: Test malformed TOML.\n---\n",
                encoding="utf-8",
            )
            registry = root / "registry.yaml"
            registry.write_text(yaml.safe_dump({"skills": [{
                "skill": "example-fastapi",
                "kind": "technology",
                "capabilities": ["web-framework"],
                "activation": {"anyOf": [{"owningDependency": "fastapi"}]},
                "companions": [],
                "selection": "additive",
                "priority": 100,
                "requiredWhenDetected": True,
            }]}), encoding="utf-8")

            for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                with self.subTest(detector=detector, interpreter="toml-capable"):
                    parsed = run_detection(
                        project,
                        "main.py",
                        detector=detector,
                        interpreter=toml_python,
                        extra=["--registry", str(registry), "--skills-root", str(skills)],
                    )
                    self.assertEqual("NO_VARIANT", parsed["loadouts"][0]["status"])
                    self.assertEqual([], parsed["loadouts"][0]["skills"])

                with self.subTest(detector=detector, interpreter="parser-free"):
                    blocked = run_detection(
                        project,
                        "main.py",
                        expected_code=2,
                        detector=detector,
                        interpreter=parser_free_python,
                        extra=["--registry", str(registry), "--skills-root", str(skills)],
                    )
                    self.assertEqual("BLOCKED", blocked["loadouts"][0]["status"])
                    self.assertEqual([], blocked["loadouts"][0]["skills"])

    def test_missing_pyyaml_blocks_each_scope_before_registry_load(self) -> None:
        """Return structured blockers before a missing PyYAML runtime can touch the registry."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "one.py").write_text("value = 1\n", encoding="utf-8")
            (root / "two.py").write_text("value = 2\n", encoding="utf-8")
            missing_registry = root / "does-not-exist.yaml"

            for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                with self.subTest(detector=detector):
                    result = run_detection(
                        root,
                        "one.py",
                        "two.py",
                        expected_code=2,
                        detector=detector,
                        isolated=True,
                        extra=["--registry", str(missing_registry)],
                    )
                    self.assertEqual("BLOCKED", result["status"])
                    self.assertEqual(["one.py", "two.py"], [item["scope"] for item in result["loadouts"]])
                    for loadout in result["loadouts"]:
                        self.assertEqual("BLOCKED", loadout["status"])
                        self.assertEqual(
                            ["missing runtime prerequisite: PyYAML"],
                            loadout["scopeErrors"],
                        )

    def test_missing_scope_blocks_instead_of_reporting_no_variant(self) -> None:
        project = ROOT / "evals" / "projects" / "fastapi-orders"
        for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
            with self.subTest(detector=detector):
                result = run_detection(project, "does-not-exist", expected_code=2, detector=detector)
                self.assertEqual("BLOCKED", result["status"])
                self.assertEqual(["scope does not exist"], result["loadouts"][0]["scopeErrors"])

    def test_broad_scope_spanning_multiple_owners_blocks_partitioning(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "packages" / "web" / "src").mkdir(parents=True)
            (root / "packages" / "api" / "src").mkdir(parents=True)
            (root / "packages" / "web" / "src" / "main.ts").write_text("export const value = 1;\n", encoding="utf-8")
            (root / "packages" / "web" / "package.json").write_text('{"dependencies":{"next":"1"}}\n', encoding="utf-8")
            (root / "packages" / "api" / "src" / "main.py").write_text("value = 1\n", encoding="utf-8")
            (root / "packages" / "api" / "pyproject.toml").write_text('[project]\nname="api"\nversion="1"\n', encoding="utf-8")
            for detector in (DETECT_SCRIPT, INSTALLED_DETECT_SCRIPT):
                with self.subTest(detector=detector):
                    result = run_detection(root, "packages", expected_code=2, detector=detector)
                    self.assertEqual("BLOCKED", result["status"])
                    self.assertIn("analyze each owner separately", result["loadouts"][0]["scopeErrors"][0])

    def test_installed_detector_matches_source_behavior(self) -> None:
        project = ROOT / "evals" / "projects" / "fastapi-orders"
        toml_python = toml_capable_interpreter()
        source_result = run_detection(project, "app", interpreter=toml_python)
        installed = run_detection(project, "app", detector=INSTALLED_DETECT_SCRIPT, interpreter=toml_python)
        self.assertEqual(source_result, installed)

    def test_detector_has_no_task_time_options(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(DETECT_SCRIPT), "--help"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        for obsolete in ("--role", "--confirm-read", "--require-confirmed"):
            self.assertNotIn(obsolete, completed.stdout)

    def test_agents_section_requires_unconditional_loading_without_redetection(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            plan = Path(directory) / "PROJECT.yaml"
            plan.write_text(yaml.safe_dump(with_unset_workflows({
                "technology_skill_loadouts": [{
                    "pathPattern": "api/**",
                    "skills": ["fastapi", "python"],
                    "sourceEvidence": [{"skill": "fastapi", "evidence": ["owning manifest dependency fastapi"]}],
                }],
            })), encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, str(RENDER_SCRIPT), "--project", str(plan), "--inline-tech-skills", "true"],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertIn(
                "api/**: apply the inlined fastapi, python skills instructions before acting",
                completed.stdout,
            )
            self.assertIn("BEGIN INLINED TECHNOLOGY SKILL: fastapi", completed.stdout)
            self.assertIn("BEGIN INLINED TECHNOLOGY SKILL: python", completed.stdout)
            self.assertIn("Do not rerun detection during ordinary work", completed.stdout)
            self.assertIn("most-specific matching pattern wins", completed.stdout)
            self.assertNotIn("Agent Claims And Worktrees", completed.stdout)
            self.assertIn(
                "BEGIN INLINED CLAIM HELPER SKILL: agent-claim-command",
                completed.stdout,
            )
            self.assertNotIn(
                "BEGIN INLINED CLAIM HELPER SKILL: agent-claim-mcp",
                completed.stdout,
            )

    def test_agents_section_preserves_scalar_source_evidence_verbatim(self) -> None:
        renderer = load_renderer_module()
        for evidence_key in ("sourceEvidence", "source_evidence"):
            with self.subTest(evidence_key=evidence_key):
                project = with_unset_workflows({
                    "technology_skill_loadouts": [{
                        "pathPattern": "worker/**",
                        "skills": ["python"],
                        evidence_key: [{
                            "skill": "python",
                            "evidence": ["  Python source evidence: worker/main.py  "],
                        }],
                    }],
                })

                rendered = renderer.render(project, inline_tech_skills=False)

                self.assertIn(
                    "  - python evidence:   Python source evidence: worker/main.py  \n",
                    rendered,
                )

    def test_agents_section_rejects_invalid_source_evidence_structure(self) -> None:
        renderer = load_renderer_module()
        invalid_values = (
            ({"sourceEvidence": {}}, "technology_skill_loadouts[0].sourceEvidence must be a list"),
            ({"sourceEvidence": ["python"]}, "technology_skill_loadouts[0].sourceEvidence[0] must be a mapping"),
            (
                {"sourceEvidence": [{"evidence": ["worker/main.py"]}]},
                "technology_skill_loadouts[0].sourceEvidence[0].skill must normalize to a lowercase hyphenated skill id",
            ),
            (
                {"source_evidence": [{"skill": 42, "evidence": ["worker/main.py"]}]},
                "technology_skill_loadouts[0].source_evidence[0].skill must normalize to a lowercase hyphenated skill id",
            ),
        )

        for evidence_value, expected in invalid_values:
            with self.subTest(evidence_value=evidence_value):
                project = with_unset_workflows({
                    "technology_skill_loadouts": [{
                        "pathPattern": "worker/**",
                        "skills": ["python"],
                        **evidence_value,
                    }],
                })

                with self.assertRaises(ValueError) as raised:
                    renderer.render(project, inline_tech_skills=False)
                self.assertEqual(expected, str(raised.exception))

    def test_agents_section_cli_rejects_invalid_source_evidence_structure(self) -> None:
        invalid_values = (
            ({"sourceEvidence": {}}, "technology_skill_loadouts[0].sourceEvidence must be a list"),
            ({"sourceEvidence": ["python"]}, "technology_skill_loadouts[0].sourceEvidence[0] must be a mapping"),
            (
                {"sourceEvidence": [{"evidence": ["worker/main.py"]}]},
                "technology_skill_loadouts[0].sourceEvidence[0].skill must normalize to a lowercase hyphenated skill id",
            ),
            (
                {"source_evidence": [{"skill": 42, "evidence": ["worker/main.py"]}]},
                "technology_skill_loadouts[0].source_evidence[0].skill must normalize to a lowercase hyphenated skill id",
            ),
        )

        with tempfile.TemporaryDirectory() as directory:
            plan = Path(directory) / "PROJECT.yaml"
            for evidence_value, expected in invalid_values:
                with self.subTest(evidence_value=evidence_value):
                    plan.write_text(yaml.safe_dump(with_unset_workflows({
                        "technology_skill_loadouts": [{
                            "pathPattern": "worker/**",
                            "skills": ["python"],
                            **evidence_value,
                        }],
                    })), encoding="utf-8")

                    completed = subprocess.run(
                        [sys.executable, str(RENDER_SCRIPT), "--project", str(plan)],
                        cwd=ROOT,
                        check=False,
                        capture_output=True,
                        text=True,
                    )

                    self.assertEqual(1, completed.returncode)
                    self.assertEqual(expected, completed.stderr.strip())

    def test_agents_section_validates_source_evidence_before_skipping_empty_loadout(self) -> None:
        renderer = load_renderer_module()
        project = with_unset_workflows({
            "technology_skill_loadouts": [{
                "pathPattern": "worker/**",
                "skills": [],
                "sourceEvidence": ["python"],
                "status": "NO_VARIANT",
            }],
        })

        with self.assertRaises(ValueError) as raised:
            renderer.render(project, inline_tech_skills=False)
        self.assertEqual(
            "technology_skill_loadouts[0].sourceEvidence[0] must be a mapping",
            str(raised.exception),
        )

    def test_agents_section_rejects_non_string_source_evidence_facts(self) -> None:
        renderer = load_renderer_module()
        invalid_facts = (
            {"path": "worker/main.py"},
            ["worker/main.py"],
            42,
        )

        for invalid_fact in invalid_facts:
            with self.subTest(invalid_fact=invalid_fact):
                project = with_unset_workflows({
                    "technology_skill_loadouts": [{
                        "pathPattern": "worker/**",
                        "skills": ["python"],
                        "sourceEvidence": [{
                            "skill": "python",
                            "evidence": [invalid_fact],
                        }],
                    }],
                })

                with self.assertRaisesRegex(
                    ValueError,
                    r"^technology_skill_loadouts\[0\]\.sourceEvidence\[0\]\.evidence\[0\] must be a string$",
                ):
                    renderer.render(project, inline_tech_skills=False)

    def test_agents_section_rejects_non_list_source_evidence(self) -> None:
        renderer = load_renderer_module()
        project = with_unset_workflows({
            "technology_skill_loadouts": [{
                "pathPattern": "worker/**",
                "skills": ["python"],
                "sourceEvidence": [{
                    "skill": "python",
                    "evidence": {"path": "worker/main.py"},
                }],
            }],
        })

        with self.assertRaisesRegex(
            ValueError,
            r"^technology_skill_loadouts\[0\]\.sourceEvidence\[0\]\.evidence must be a list of strings$",
        ):
            renderer.render(project, inline_tech_skills=False)

    def test_agents_section_requires_explicit_persistence_and_commit_selectors(self) -> None:
        renderer = load_renderer_module()
        invalid_projects = (
            (
                {},
                "workflow_selection is required; record workflow_selection.persistence.default and workflow_selection.commit.default explicitly, using UNSET when either decision is deferred",
            ),
            (
                {
                    "workflow_selection": {
                        "commit": {"default": "UNSET"},
                    },
                },
                "workflow_selection.persistence must be a mapping; record workflow_selection.persistence.default: UNSET when the persistence decision is deferred",
            ),
            (
                {
                    "workflow_selection": {
                        "persistence": {"default": "UNSET"},
                    },
                },
                "workflow_selection.commit must be a mapping; record workflow_selection.commit.default: UNSET when the commit decision is deferred",
            ),
            (
                {
                    "workflow_selection": {
                        "persistence": {},
                        "commit": {"default": "UNSET"},
                    },
                },
                "workflow_selection.persistence.default is required; record workflow_selection.persistence.default: UNSET when the persistence decision is deferred",
            ),
            (
                {
                    "workflow_selection": {
                        "persistence": {"default": "UNSET"},
                        "commit": {},
                    },
                },
                "workflow_selection.commit.default is required; record workflow_selection.commit.default: UNSET when the commit decision is deferred",
            ),
        )

        for project, expected in invalid_projects:
            with self.subTest(expected=expected):
                with self.assertRaisesRegex(ValueError, f"^{re.escape(expected)}$"):
                    renderer.render(project)

    def test_agents_section_rejects_duplicate_provider_and_completion_patterns(self) -> None:
        renderer = load_renderer_module()
        invalid_projects = (
            (
                {
                    "workflow_selection": {
                        "provider": {
                            "default": "file",
                            "folder_overrides": [
                                {"pattern": "services/**", "provider": "file"},
                                {"pattern": "services/**", "provider": "github"},
                            ],
                        },
                        "completion": {"default": "direct-main"},
                    },
                },
                "workflow_selection.provider.folder_overrides[1].pattern 'services/**' conflicts with workflow_selection.provider.folder_overrides[0].pattern using values 'file' and 'github'",
            ),
            (
                {
                    "workflow_selection": {
                        "provider": {
                            "default": "file",
                            "folder_overrides": [
                                {"pattern": "services/**", "provider": "github"},
                                {"pattern": "services/**", "provider": "github"},
                            ],
                        },
                        "completion": {"default": "direct-main"},
                    },
                },
                "workflow_selection.provider.folder_overrides[1].pattern 'services/**' duplicates workflow_selection.provider.folder_overrides[0].pattern with value 'github'; duplicate patterns are not allowed",
            ),
            (
                {
                    "workflow_selection": {
                        "provider": {"default": "file"},
                        "completion": {
                            "default": "direct-main",
                            "folder_overrides": [
                                {"pattern": "services/**", "completion": "direct-main"},
                                {"pattern": "services/**", "completion": "feature-branch"},
                            ],
                        },
                    },
                },
                "workflow_selection.completion.folder_overrides[1].pattern 'services/**' conflicts with workflow_selection.completion.folder_overrides[0].pattern using values 'direct-main' and 'feature-branch'",
            ),
            (
                {
                    "workflow_selection": {
                        "provider": {"default": "file"},
                        "completion": {
                            "default": "direct-main",
                            "folder_overrides": [
                                {"pattern": "services/**", "completion": "feature-branch"},
                                {"pattern": "services/**", "completion": "feature-branch"},
                            ],
                        },
                    },
                },
                "workflow_selection.completion.folder_overrides[1].pattern 'services/**' duplicates workflow_selection.completion.folder_overrides[0].pattern with value 'feature-branch'; duplicate patterns are not allowed",
            ),
        )

        for project, expected in invalid_projects:
            with self.subTest(expected=expected):
                with self.assertRaisesRegex(ValueError, f"^{re.escape(expected)}$"):
                    renderer.render(project)

    def test_agents_section_accepts_boundary_persistence_overrides_without_inference(self) -> None:
        renderer = load_renderer_module()
        rendered = renderer.render(with_claim_transport({
            "workflow_selection": {
                "persistence": {
                    "default": "file",
                    "folder_overrides": [
                        {"pattern": "interactive/**", "persistence": "none"},
                        {"pattern": "deferred/**", "persistence": "UNSET"},
                        {"pattern": "jira/**", "persistence": "jira"},
                        {"pattern": "ado/**", "persistence": "azure-devops"},
                    ],
                },
                "commit": {"default": "direct-main"},
            },
        }))

        self.assertIn("interactive/** persistence none: no durable persistence skill", rendered)
        self.assertIn(
            "deferred/** persistence UNSET: when durable work-item management is first requested",
            rendered,
        )
        self.assertIn("jira/** persistence jira: create with create-work-item-jira", rendered)
        self.assertIn("ado/** persistence azure-devops: create with create-work-item-azure-devops", rendered)
        self.assertEqual(2, rendered.count("unsupported placeholder remains selected and reports BLOCKED"))
        self.assertIn("does not infer either value", rendered)

    def test_agents_section_renders_every_persistence_as_reference_only_skill_guidance(self) -> None:
        renderer = load_renderer_module()
        persistence_guidance = {
            "file": "Default persistence file: create with create-work-item-file; manage with manage-work-items-file.",
            "github": "Default persistence github: create with create-work-item-github; manage with manage-work-items-github.",
            "gitlab": "Default persistence gitlab: create with create-work-item-gitlab; manage with manage-work-items-gitlab.",
            "azure-devops": "Default persistence azure-devops: create with create-work-item-azure-devops; manage with manage-work-items-azure-devops.",
            "jira": "Default persistence jira: create with create-work-item-jira; manage with manage-work-items-jira.",
            "none": "Default persistence none: no durable persistence skill; durable create and manage operations are invalid.",
            "UNSET": "Default persistence UNSET: when durable work-item management is first requested, ask whether to select the available file provider.",
        }
        commit_guidance = {
            "direct-main": "Default commit direct-main: use deliver-work-item-direct-main.",
            "feature-branch": "Default commit feature-branch: use deliver-work-item-feature-branch.",
            "UNSET": "Default commit UNSET: the pertinent agent asks for the Commit decision before implementation or publication.",
        }

        for persistence, expected_persistence in persistence_guidance.items():
            for commit, expected_commit in commit_guidance.items():
                with self.subTest(persistence=persistence, commit=commit):
                    rendered = renderer.render(with_claim_transport({
                        "workflow_selection": {
                            "persistence": {"default": persistence},
                            "commit": {"default": commit},
                        },
                        "technology_skill_loadouts": [],
                    }))

                    self.assertIn("## Work-Item Workflow Skill References", rendered)
                    self.assertIn(expected_persistence, rendered)
                    self.assertIn(expected_commit, rendered)
                    self.assertNotIn("Default provider", rendered)
                    self.assertNotIn("Default completion", rendered)
                    self.assertNotIn("# Create File Work Item", rendered)
                    self.assertNotIn("# Complete Work Item Direct Main", rendered)

    def test_agents_section_resolves_persistence_and_commit_overrides_independently(self) -> None:
        renderer = load_renderer_module()
        rendered = renderer.render(with_claim_transport({
            "workflow_selection": {
                "persistence": {
                    "default": "file",
                    "folder_overrides": [{
                        "pattern": "services/**",
                        "persistence": "github",
                    }],
                },
                "commit": {
                    "default": "feature-branch",
                    "folder_overrides": [{
                        "pattern": "services/**",
                        "commit": "direct-main",
                    }],
                },
            },
            "technology_skill_loadouts": [],
        }))

        self.assertIn(
            "Default persistence file: create with create-work-item-file; manage with manage-work-items-file.",
            rendered,
        )
        self.assertIn(
            "services/** persistence github: create with create-work-item-github; manage with manage-work-items-github.",
            rendered,
        )
        self.assertIn(
            "Default commit feature-branch: use deliver-work-item-feature-branch.",
            rendered,
        )
        self.assertIn(
            "services/** commit direct-main: use deliver-work-item-direct-main.",
            rendered,
        )
        self.assertIn("Most-specific matching folder pattern wins independently", rendered)

    def test_agents_section_preserves_none_unset_and_unsupported_boundaries(self) -> None:
        renderer = load_renderer_module()
        none_rendered = renderer.render(with_claim_transport({
            "workflow_selection": {
                "persistence": {"default": "none"},
                "commit": {"default": "feature-branch"},
            },
        }))
        unset_rendered = renderer.render(with_claim_transport({
            "workflow_selection": {
                "persistence": {"default": "UNSET"},
                "commit": {"default": "UNSET"},
            },
        }))
        placeholder_rendered = renderer.render(with_claim_transport({
            "workflow_selection": {
                "persistence": {"default": "azure-devops"},
                "commit": {"default": "direct-main"},
            },
        }))

        self.assertIn(
            "Default persistence none: no durable persistence skill; durable create and manage operations are invalid.",
            none_rendered,
        )
        self.assertIn("asks for the Persistence decision before a persistence operation", unset_rendered)
        self.assertIn("asks for the Commit decision before implementation or publication", unset_rendered)
        self.assertIn("does not infer either value from repository or hosting evidence", unset_rendered)
        self.assertIn("create-work-item-azure-devops", placeholder_rendered)
        self.assertIn("manage-work-items-azure-devops", placeholder_rendered)
        self.assertIn("unsupported placeholder remains selected and reports BLOCKED", placeholder_rendered)

    def test_agents_section_keeps_workflow_references_distinct_from_inlined_technology(self) -> None:
        renderer = load_renderer_module()
        rendered = renderer.render(with_claim_transport({
            "workflow_selection": {
                "persistence": {"default": "github"},
                "commit": {"default": "feature-branch"},
            },
            "technology_skill_loadouts": [{
                "pathPattern": "services/**",
                "skills": ["python"],
            }],
        }), inline_tech_skills=True)

        self.assertIn("Workflow skills are referenced by name only", rendered)
        self.assertIn("## Technology Skills", rendered)
        self.assertIn("----- BEGIN INLINED TECHNOLOGY SKILL: python -----", rendered)
        self.assertIn(renderer.inlined_skill_body("python"), rendered)
        self.assertNotIn("# Create GitHub Work Item", rendered)
        self.assertNotIn("# Complete Work Item Feature Branch", rendered)

    def test_project_skill_extensions_accept_empty_bundled_and_registered_entries_in_order(self) -> None:
        renderer = load_renderer_module()

        empty = renderer.render(with_unset_workflows({"project_skill_extensions": []}))
        self.assertNotIn("## Project Skill Extensions", empty)

        single = renderer.render(with_unset_workflows({
            "project_skill_extensions": ["python"],
        }))
        self.assertEqual(1, single.count("## Project Skill Extensions"))
        self.assertTrue(single.rstrip().endswith("- python"))

        rendered = renderer.render(with_unset_workflows({
            "project_skill_extensions": [
                "sql",
                {
                    "skill": "project-local-review",
                    "registration": "registered",
                    "availability": "AVAILABLE",
                    "catalog": "target runtime skill catalog",
                },
                "python",
            ],
            "technology_skill_loadouts": [],
        }))

        self.assertEqual(1, rendered.count("## Project Skill Extensions"))
        self.assertNotIn("BEGIN INLINED PROJECT SKILL", rendered)
        ordered_positions = [
            rendered.index("- sql"),
            rendered.index("- project-local-review"),
            rendered.index("- python"),
        ]
        self.assertEqual(sorted(ordered_positions), ordered_positions)
        self.assertGreater(
            rendered.index("## Project Skill Extensions"),
            rendered.index("## Technology Skills"),
        )
        self.assertTrue(rendered.rstrip().endswith("- python"))

    def test_project_skill_extensions_reject_invalid_duplicate_unknown_and_unavailable_entries(self) -> None:
        renderer = load_renderer_module()
        invalid_projects = (
            (
                {"project_skill_extensions": "python"},
                "project_skill_extensions must be a list; use [] when no project-level extension is selected",
            ),
            (
                {"project_skill_extensions": [None]},
                "project_skill_extensions[0] must be a bundled skill id string or a registered-skill mapping",
            ),
            (
                {"project_skill_extensions": ["python", " Python "]},
                "project_skill_extensions[1] skill id 'python' duplicates project_skill_extensions[0]; remove the duplicate entry",
            ),
            (
                {"project_skill_extensions": ["not-a-bundled-skill"]},
                "project_skill_extensions[0] unknown bundled skill id 'not-a-bundled-skill'; use a bundled skill id or a registered-skill mapping",
            ),
            (
                {
                    "project_skill_extensions": [{
                        "skill": "project-local-review",
                        "registration": "registered",
                        "availability": "UNAVAILABLE",
                        "catalog": "target runtime skill catalog",
                    }],
                },
                "project_skill_extensions[0].availability is UNAVAILABLE for skill 'project-local-review'; install or expose the registered skill, then set project_skill_extensions[0].availability to AVAILABLE",
            ),
        )

        for extension_config, expected in invalid_projects:
            with self.subTest(expected=expected):
                with self.assertRaisesRegex(ValueError, f"^{re.escape(expected)}$"):
                    renderer.render(with_unset_workflows(extension_config))

    def test_project_skill_extensions_validate_registered_mapping_fields(self) -> None:
        renderer = load_renderer_module()
        invalid_entries = (
            (
                {},
                "project_skill_extensions[0] keys must be exactly: skill, registration, availability, catalog",
            ),
            (
                {
                    "skill": "project-local-review",
                    "registration": "discovered",
                    "availability": "AVAILABLE",
                    "catalog": "target runtime skill catalog",
                },
                "project_skill_extensions[0].registration must be registered; use a bundled skill id string for bundled skills",
            ),
            (
                {
                    "skill": "Project Local Review",
                    "registration": "registered",
                    "availability": "AVAILABLE",
                    "catalog": "target runtime skill catalog",
                },
                "project_skill_extensions[0].skill must normalize to a lowercase hyphenated skill id",
            ),
            (
                {
                    "skill": "project-local-review",
                    "registration": "registered",
                    "availability": "AVAILABLE",
                    "catalog": "",
                },
                "project_skill_extensions[0].catalog must be a non-empty registered catalog identifier",
            ),
        )

        for entry, expected in invalid_entries:
            with self.subTest(expected=expected):
                with self.assertRaisesRegex(ValueError, f"^{re.escape(expected)}$"):
                    renderer.render(with_unset_workflows({"project_skill_extensions": [entry]}))

    def test_project_skill_extensions_reject_definition_owned_duplicates_and_do_not_propagate_to_nested_guidance(self) -> None:
        renderer = load_renderer_module()
        project = with_unset_workflows({
            "project_skill_extensions": ["python"],
            "role_agent_set": [{
                "role": "example-coder",
                "skills": ["python"],
                "conditional_skills": [{"skill": "sql", "condition": "when needed"}],
            }],
        })

        with self.assertRaisesRegex(
            ValueError,
            "^project_skill_extensions\\[0\\] skill id 'python' duplicates definition-owned skill role_agent_set\\[0\\].skills\\[0\\]; remove it from project_skill_extensions$",
        ):
            renderer.render(project)

        project["project_skill_extensions"] = ["sql"]
        with self.assertRaisesRegex(
            ValueError,
            "^project_skill_extensions\\[0\\] skill id 'sql' duplicates definition-owned skill role_agent_set\\[0\\].conditional_skills\\[0\\].skill; remove it from project_skill_extensions$",
        ):
            renderer.render(project)

        nested = renderer.render(with_unset_workflows({
            "project_skill_extensions": ["python"],
            "nested_agents_files": [{
                "path": "services/AGENTS.md",
                "needed": True,
            }],
        }))
        extension_section = nested.split("## Project Skill Extensions", maxsplit=1)[1]
        self.assertNotIn("services/AGENTS.md", extension_section)
        self.assertIn("root AGENTS.md", extension_section)

    def test_agents_section_rejects_invalid_workflow_values_and_combined_overrides(self) -> None:
        renderer = load_renderer_module()
        invalid_projects = (
            (
                {
                    "workflow_selection": {
                        "provider": {"default": "bitbucket"},
                        "completion": {"default": "direct-main"},
                    },
                },
                "workflow_selection.provider.default rejects 'bitbucket'; supported values: file, github, gitlab, azure-devops, jira, none, UNSET",
            ),
            (
                {
                    "workflow_selection": {
                        "provider": {"default": "file"},
                        "completion": {"default": "merge-when-green"},
                    },
                },
                "workflow_selection.completion.default rejects 'merge-when-green'; supported values: direct-main, feature-branch, UNSET",
            ),
            (
                {
                    "workflow_selection": {
                        "provider": {
                            "default": "file",
                            "folder_overrides": [{
                                "pattern": "services/**",
                                "process": "github+feature-branch",
                            }],
                        },
                        "completion": {"default": "direct-main"},
                    },
                },
                "workflow_selection.provider.folder_overrides[0].process rejects combined value 'github+feature-branch'; supported provider values: file, github, gitlab, azure-devops, jira, none, UNSET; split it into workflow_selection.provider.folder_overrides[0].provider and a workflow_selection.completion.folder_overrides entry with the same pattern",
            ),
            (
                {
                    "workflow_selection": {
                        "provider": {"default": "file"},
                        "completion": {
                            "default": "direct-main",
                            "folder_overrides": [{
                                "pattern": "services/**",
                                "process": "github+feature-branch",
                            }],
                        },
                    },
                },
                "workflow_selection.completion.folder_overrides[0].process rejects combined value 'github+feature-branch'; supported completion values: direct-main, feature-branch, UNSET; split it into workflow_selection.completion.folder_overrides[0].completion and a workflow_selection.provider.folder_overrides entry with the same pattern",
            ),
            (
                {
                    "workflow_selection": {
                        "provider": {
                            "default": "file",
                            "folder_overrides": [{"pattern": "", "provider": "github"}],
                        },
                        "completion": {"default": "direct-main"},
                    },
                },
                "workflow_selection.provider.folder_overrides[0].pattern must be a non-empty project-relative path pattern",
            ),
            (
                {
                    "workflow_selection": {
                        "provider": {"default": "file"},
                        "completion": {
                            "default": "direct-main",
                            "folder_overrides": [{
                                "pattern": "services/**",
                                "completion": "merge-when-green",
                            }],
                        },
                    },
                },
                "workflow_selection.completion.folder_overrides[0].completion rejects 'merge-when-green'; supported values: direct-main, feature-branch, UNSET",
            ),
        )

        for project, expected in invalid_projects:
            with self.subTest(expected=expected):
                with self.assertRaisesRegex(ValueError, f"^{re.escape(expected)}$"):
                    renderer.render(project)

    def test_agents_section_collision_checks_mixed_legacy_and_canonical_defaults(self) -> None:
        renderer = load_renderer_module()
        cases = (
            (
                "workitem",
                "commit",
                "workflow_selection.workitem collides with workflow_selection.commit; replace workflow_selection.workitem with workflow_selection.commit and keep exactly one selector family",
            ),
            (
                "completion",
                "commit",
                "workflow_selection.completion collides with workflow_selection.commit; replace workflow_selection.completion with workflow_selection.commit and keep exactly one selector family",
            ),
            (
                "backlog",
                "persistence",
                "workflow_selection.backlog collides with workflow_selection.persistence; replace workflow_selection.backlog with workflow_selection.persistence and keep exactly one selector family",
            ),
            (
                "provider",
                "persistence",
                "workflow_selection.provider collides with workflow_selection.persistence; replace workflow_selection.provider with workflow_selection.persistence and keep exactly one selector family",
            ),
        )

        for legacy_key, canonical_key, expected in cases:
            with self.subTest(legacy_key=legacy_key):
                legacy_default = (
                    "simple-workitem" if legacy_key == "workitem"
                    else "file-based-backlog" if legacy_key == "backlog"
                    else "direct-main" if legacy_key == "completion"
                    else "file"
                )
                canonical_default = "direct-main" if canonical_key == "commit" else "file"
                project = {
                    "workflow_selection": {
                        legacy_key: {"default": legacy_default},
                        canonical_key: {"default": canonical_default},
                    },
                }
                with self.assertRaisesRegex(ValueError, f"^{re.escape(expected)}$"):
                    renderer.render(project)
                self.assertEqual(
                    {"default": canonical_default},
                    project["workflow_selection"][canonical_key],
                )

    def test_agents_section_collision_checks_mixed_legacy_and_canonical_overrides(self) -> None:
        renderer = load_renderer_module()
        cases = (
            (
                "workitem",
                "feature-branch-workitem",
                "commit",
                "feature-branch",
                "workflow_selection.workitem collides with workflow_selection.commit; replace workflow_selection.workitem with workflow_selection.commit and keep exactly one selector family",
            ),
            (
                "backlog",
                "github-issues-backlog",
                "persistence",
                "github",
                "workflow_selection.backlog collides with workflow_selection.persistence; replace workflow_selection.backlog with workflow_selection.persistence and keep exactly one selector family",
            ),
        )

        for legacy_key, legacy_value, canonical_key, canonical_value, expected in cases:
            with self.subTest(legacy_key=legacy_key, expected=expected):
                legacy_default = "simple-workitem" if legacy_key == "workitem" else "file-based-backlog"
                canonical_default = "direct-main" if canonical_key == "commit" else "file"
                project = {
                    "workflow_selection": {
                        legacy_key: {
                            "default": legacy_default,
                            "folder_overrides": [{
                                "pattern": "services/**",
                                "process": legacy_value,
                            }],
                        },
                        canonical_key: {
                            "default": canonical_default,
                            "folder_overrides": [{
                                "pattern": "services/**",
                                canonical_key: canonical_value,
                            }],
                        },
                    },
                }
                with self.assertRaisesRegex(ValueError, f"^{re.escape(expected)}$"):
                    renderer.render(project)
                self.assertEqual(
                    canonical_value,
                    project["workflow_selection"][canonical_key]["folder_overrides"][0][canonical_key],
                )

    def test_render_docstring_distinguishes_optional_authority_from_required_workflow(self) -> None:
        renderer = load_renderer_module()

        self.assertIn("Optional definition authority", renderer.render.__doc__)
        self.assertIn("workflow_selection and resource_coordination are required", renderer.render.__doc__)
        self.assertIn(
            "agent_claim_transport is required only when resource_coordination selects agent-claim",
            renderer.render.__doc__,
        )
        self.assertNotIn("Optional authority and workflow", renderer.render.__doc__)

    def test_agents_section_reports_deterministic_legacy_selector_migrations(self) -> None:
        renderer = load_renderer_module()
        legacy_values = (
            ("workitem", "simple-workitem", "Default commit direct-main"),
            ("workitem", "feature-branch-workitem", "Default commit feature-branch"),
            ("backlog", "file-based-backlog", "Default persistence file"),
            ("backlog", "github-issues-backlog", "Default persistence github"),
            ("backlog", "none", "Default persistence none"),
            ("backlog", "UNSET", "Default persistence UNSET"),
        )

        for selector, legacy_value, expected_target in legacy_values:
            with self.subTest(selector=selector, legacy_value=legacy_value):
                other = (
                    {"persistence": {"default": "file"}}
                    if selector == "workitem"
                    else {"commit": {"default": "direct-main"}}
                )
                rendered = renderer.render(with_claim_transport({
                    "workflow_selection": {
                        selector: {"default": legacy_value},
                        **other,
                    },
                }))
                canonical_key = "commit" if selector == "workitem" else "persistence"
                self.assertIn(
                    f"Normalized workflow_selection.{selector} to workflow_selection.{canonical_key}",
                    rendered,
                )
                self.assertIn(expected_target, rendered)

    def test_agents_section_validates_every_legacy_selector_field_before_migration(self) -> None:
        renderer = load_renderer_module()
        completion_guidance = (
            "; supported legacy values and canonical replacements: simple-workitem -> direct-main, "
            "feature-branch-workitem -> feature-branch, UNSET -> UNSET"
        )
        provider_guidance = (
            "; supported legacy values and canonical replacements: file-based-backlog -> file, "
            "github-issues-backlog -> github, none -> none, UNSET -> UNSET"
        )
        invalid_projects = (
            (
                {"workflow_selection": {"workitem": "simple-workitem"}},
                "workflow_selection.workitem must be a mapping; canonical replacement: workflow_selection.commit"
                + completion_guidance,
            ),
            (
                {"workflow_selection": {"workitem": {"default": "invented"}}},
                "workflow_selection.workitem.default rejects 'invented'; supported legacy values and canonical replacements: simple-workitem -> direct-main, feature-branch-workitem -> feature-branch, UNSET -> UNSET",
            ),
            (
                {"workflow_selection": {"backlog": {}}},
                "workflow_selection.backlog.default rejects None; supported legacy values and canonical replacements: file-based-backlog -> file, github-issues-backlog -> github, none -> none, UNSET -> UNSET",
            ),
            (
                {
                    "workflow_selection": {
                        "workitem": {
                            "default": "simple-workitem",
                            "folder_overrides": "services/**",
                        },
                    },
                },
                "workflow_selection.workitem.folder_overrides must be a list" + completion_guidance,
            ),
            (
                {
                    "workflow_selection": {
                        "backlog": {
                            "default": "file-based-backlog",
                            "folder_overrides": ["not-a-mapping"],
                        },
                    },
                },
                "workflow_selection.backlog.folder_overrides[0] must be a mapping with pattern and process" + provider_guidance,
            ),
            (
                {
                    "workflow_selection": {
                        "workitem": {
                            "default": "simple-workitem",
                            "folder_overrides": [{"process": "feature-branch-workitem"}],
                        },
                    },
                },
                "workflow_selection.workitem.folder_overrides[0].pattern must be a non-empty project-relative path pattern" + completion_guidance,
            ),
            (
                {
                    "workflow_selection": {
                        "backlog": {
                            "default": "file-based-backlog",
                            "folder_overrides": [{"pattern": "services/**"}],
                        },
                    },
                },
                "workflow_selection.backlog.folder_overrides[0] keys must be exactly: pattern, process"
                + provider_guidance,
            ),
            (
                {
                    "workflow_selection": {
                        "workitem": {
                            "default": "simple-workitem",
                            "folder_overrides": [{
                                "pattern": "",
                                "process": "feature-branch-workitem",
                            }],
                        },
                    },
                },
                "workflow_selection.workitem.folder_overrides[0].pattern must be a non-empty project-relative path pattern" + completion_guidance,
            ),
            (
                {
                    "workflow_selection": {
                        "backlog": {
                            "default": "file-based-backlog",
                            "folder_overrides": [{
                                "pattern": "services/**",
                                "process": "jira",
                            }],
                        },
                    },
                },
                "workflow_selection.backlog.folder_overrides[0].process rejects 'jira'; supported legacy values and canonical replacements: file-based-backlog -> file, github-issues-backlog -> github, none -> none, UNSET -> UNSET",
            ),
            (
                {
                    "workflow_selection": {
                        "backlog": {
                            "default": "file-based-backlog",
                            "folder_overrides": [
                                {"pattern": "services/**", "process": "none"},
                                {"pattern": "services/**", "process": "UNSET"},
                            ],
                        },
                    },
                },
                "workflow_selection.backlog.folder_overrides[1].pattern 'services/**' conflicts with workflow_selection.backlog.folder_overrides[0].pattern using values 'none' and 'UNSET'" + provider_guidance,
            ),
            (
                {
                    "workflow_selection": {
                        "workitem": {
                            "default": "simple-workitem",
                            "folder_overrides": [
                                {"pattern": "services/**", "process": "feature-branch-workitem"},
                                {"pattern": "services/**", "process": "feature-branch-workitem"},
                            ],
                        },
                    },
                },
                "workflow_selection.workitem.folder_overrides[1].pattern 'services/**' duplicates workflow_selection.workitem.folder_overrides[0].pattern with value 'feature-branch-workitem'; duplicate patterns are not allowed" + completion_guidance,
            ),
        )

        for project, expected in invalid_projects:
            with self.subTest(expected=expected):
                with self.assertRaisesRegex(ValueError, f"^{re.escape(expected)}$"):
                    renderer.render(project)

    def test_agents_section_rejects_legacy_values_under_canonical_selector_keys(self) -> None:
        renderer = load_renderer_module()
        projects = (
            (
                {
                    "workflow_selection": {
                        "provider": {"default": "file-based-backlog"},
                        "completion": {"default": "direct-main"},
                    },
                },
                "workflow_selection.provider.default uses legacy value 'file-based-backlog'; migrate to 'file'",
            ),
            (
                {
                    "workflow_selection": {
                        "provider": {"default": "github"},
                        "completion": {"default": "simple-workitem"},
                    },
                },
                "workflow_selection.completion.default uses legacy value 'simple-workitem'; migrate to 'direct-main'",
            ),
        )

        for project, expected in projects:
            with self.subTest(expected=expected):
                with self.assertRaisesRegex(ValueError, f"^{re.escape(expected)}$"):
                    renderer.render(project)

    def test_agents_section_preserves_valid_maintainer_selected_values(self) -> None:
        renderer = load_renderer_module()
        workflow_selection = {
            "provider": {"default": "gitlab"},
            "completion": {"default": "direct-main"},
            "selection_policy": "Maintainer-selected values are authoritative.",
        }

        rendered = renderer.render(with_claim_transport({"workflow_selection": workflow_selection}))

        self.assertEqual("gitlab", workflow_selection["provider"]["default"])
        self.assertEqual("direct-main", workflow_selection["completion"]["default"])
        self.assertIn("create-work-item-gitlab", rendered)
        self.assertIn("deliver-work-item-direct-main", rendered)

    def test_agents_section_references_technology_skills_by_default_with_inline_override(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            plan = Path(directory) / "PROJECT.yaml"
            plan.write_text(yaml.safe_dump(with_unset_workflows({
                "technology_skill_loadouts": [{
                    "pathPattern": "src/**",
                    "skills": ["python"],
                }],
            })), encoding="utf-8")

            dynamically_loaded = subprocess.run(
                [sys.executable, str(RENDER_SCRIPT), "--project", str(plan)],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            ).stdout
            self.assertIn("src/**: load python before acting", dynamically_loaded)
            self.assertNotIn("BEGIN INLINED TECHNOLOGY SKILL", dynamically_loaded)

            inlined = subprocess.run(
                [
                    sys.executable,
                    str(RENDER_SCRIPT),
                    "--project",
                    str(plan),
                    "--inline-tech-skills",
                    "true",
                ],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            ).stdout
            self.assertIn("src/**: apply the inlined python skill instructions", inlined)
            self.assertIn("BEGIN INLINED TECHNOLOGY SKILL: python", inlined)
            self.assertIn("# Python", inlined)

            invalid = subprocess.run(
                [
                    sys.executable,
                    str(RENDER_SCRIPT),
                    "--project",
                    str(plan),
                    "--inline-tech-skills",
                    "yes",
                ],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(2, invalid.returncode)
            self.assertIn("expected true or false", invalid.stderr)

    def test_agents_section_output_requires_explicit_replace(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plan = root / "PROJECT.yaml"
            output = root / "AGENTS.md"
            plan.write_text(yaml.safe_dump(with_unset_workflows({
                "technology_skill_loadouts": [{
                    "pathPattern": "src/**",
                    "skills": ["python"],
                }],
            })), encoding="utf-8")

            created = subprocess.run(
                [
                    sys.executable,
                    str(RENDER_SCRIPT),
                    "--project",
                    str(plan),
                    "--output",
                    str(output),
                    "--inline-tech-skills",
                    "true",
                ],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(0, created.returncode, created.stderr)
            self.assertIn(
                "BEGIN INLINED TECHNOLOGY SKILL: python",
                output.read_text(encoding="utf-8"),
            )

            original = "existing project instructions\n"
            output.write_text(original, encoding="utf-8")
            protected = subprocess.run(
                [
                    sys.executable,
                    str(RENDER_SCRIPT),
                    "--project",
                    str(plan),
                    "--output",
                    str(output),
                ],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(1, protected.returncode)
            self.assertIn(f"output file already exists: {output}", protected.stderr)
            self.assertIn("--replace", protected.stderr)
            self.assertEqual(original, output.read_text(encoding="utf-8"))

            replaced = subprocess.run(
                [
                    sys.executable,
                    str(RENDER_SCRIPT),
                    "--project",
                    str(plan),
                    "--output",
                    str(output),
                    "--replace",
                    "--inline-tech-skills",
                    "true",
                ],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(0, replaced.returncode, replaced.stderr)
            self.assertIn(
                "BEGIN INLINED TECHNOLOGY SKILL: python",
                output.read_text(encoding="utf-8"),
            )

    def test_agents_section_omits_project_skill_extensions_from_nested_output(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plan = root / "PROJECT.yaml"
            root_output = root / "AGENTS.md"
            output = root / "services" / "AGENTS.md"
            output.parent.mkdir()
            plan.write_text(yaml.safe_dump(with_unset_workflows({
                "project_skill_extensions": ["python"],
                "technology_skill_loadouts": [],
            })), encoding="utf-8")

            root_completed = subprocess.run(
                [
                    sys.executable,
                    str(RENDER_SCRIPT),
                    "--project",
                    str(plan),
                    "--output",
                    str(root_output),
                ],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            completed = subprocess.run(
                [
                    sys.executable,
                    str(RENDER_SCRIPT),
                    "--project",
                    str(plan),
                    "--output",
                    str(output),
                ],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(0, root_completed.returncode, root_completed.stderr)
            self.assertIn(
                "## Project Skill Extensions",
                root_output.read_text(encoding="utf-8"),
            )
            self.assertEqual(0, completed.returncode, completed.stderr)
            rendered = output.read_text(encoding="utf-8")
            self.assertIn("## Technology Skills", rendered)
            self.assertNotIn("## Project Skill Extensions", rendered)
            self.assertNotIn("- python", rendered)

    def test_renderer_stays_single_purpose_and_rejects_retired_policy_options(self) -> None:
        """Keep the renderer limited to project guidance and technology skill routing."""

        with tempfile.TemporaryDirectory() as directory:
            plan = Path(directory) / "PROJECT.yaml"
            plan.write_text(
                yaml.safe_dump(
                    with_unset_workflows(
                        {
                            "technology_skill_loadouts": [
                                {
                                    "pathPattern": "scripts/**",
                                    "skills": ["python"],
                                }
                            ]
                        }
                    )
                ),
                encoding="utf-8",
            )

            rendered = subprocess.run(
                [sys.executable, str(RENDER_SCRIPT), "--project", str(plan)],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(0, rendered.returncode, rendered.stderr)
            self.assertIn("## Technology Skills", rendered.stdout)
            self.assertIn("- scripts/**: load python before acting.", rendered.stdout)
            self.assertNotIn("Agent And Skill Definition Approval", rendered.stdout)
            self.assertNotIn("definition_change_authority", rendered.stdout)

            retired_options = (
                ("--check-definition-change", "skills/example/SKILL.md"),
                ("--approval-record", "approval-record.yaml"),
                ("--regenerated-from", "skills/example/SKILL.md"),
                ("--update-authority-directive",),
            )
            for option in retired_options:
                with self.subTest(option=option[0]):
                    rejected = subprocess.run(
                        [
                            sys.executable,
                            str(RENDER_SCRIPT),
                            "--project",
                            str(plan),
                            *option,
                        ],
                        cwd=ROOT,
                        check=False,
                        capture_output=True,
                        text=True,
                    )
                    self.assertEqual(2, rejected.returncode)
                    self.assertIn("unrecognized arguments", rejected.stderr)

        project_text = (ROOT / "PROJECT.yaml").read_text(encoding="utf-8")
        agents_text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        for retired_text in (
            "definition_change_authority",
            "--check-definition-change",
            "--approval-record",
            "--regenerated-from",
            "Agent And Skill Definition Approval",
        ):
            with self.subTest(retired_text=retired_text):
                self.assertNotIn(retired_text, project_text)
                self.assertNotIn(retired_text, agents_text)



    def test_agents_section_rejects_invalid_inlined_skill_names(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            plan = Path(directory) / "PROJECT.yaml"
            plan.write_text(yaml.safe_dump(with_unset_workflows({
                "technology_skill_loadouts": [{
                    "pathPattern": "src/**",
                    "skills": ["../../private"],
                }],
            })), encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, str(RENDER_SCRIPT), "--project", str(plan), "--inline-tech-skills", "true"],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(1, completed.returncode)
            self.assertIn(
                "technology_skill_loadouts[0].skills[0] must normalize to a lowercase hyphenated skill id",
                completed.stderr,
            )

    def test_agents_section_preserves_no_variant_general_training_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            plan = Path(directory) / "PROJECT.yaml"
            plan.write_text(yaml.safe_dump(with_unset_workflows({
                "technology_skill_loadouts": [
                    {
                        "pathPattern": "src/main/**",
                        "skills": ["python"],
                        "status": "READY",
                    },
                    {
                        "pathPattern": "config/**",
                        "skills": [],
                        "status": "NO_VARIANT",
                        "fallback": "general model training",
                    },
                ],
            })), encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, str(RENDER_SCRIPT), "--project", str(plan), "--inline-tech-skills", "true"],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertIn(
                "src/main/**: apply the inlined python skill instructions before acting",
                completed.stdout,
            )
            self.assertIn(
                "config/**: no pertinent specialized technology skill is available; use general model training and continue full scope coverage",
                completed.stdout,
            )
            self.assertIn("most-specific matching pattern wins", completed.stdout)

    def test_registry_contains_only_specialized_skills(self) -> None:
        registry = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
        self.assertEqual(2, registry["version"])
        self.assertTrue(registry["skills"])
        self.assertEqual({"technology", "domain"}, {entry["kind"] for entry in registry["skills"]})
        self.assertTrue(all(entry.get("skill") for entry in registry["skills"]))
        self.assertTrue(all(set(entry["activation"]) == {"anyOf"} for entry in registry["skills"]))
        self.assertFalse({"careful-coding", "test-strategy", "detect-technology-skills"} & {entry["skill"] for entry in registry["skills"]})


if __name__ == "__main__":
    unittest.main()
