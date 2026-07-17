# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Modified with AI assistance.
# Summary: Verifies bundle deployment, MCP configuration, ownership, cleanup, and removal.

from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from types import ModuleType
from unittest.mock import patch


INSTALLER_PATH = Path(__file__).with_name("install-skills.py")
SKILL_FILE_CONTENT = "---\nname: alpha\ndescription: Alpha skill.\n---\n"
UPDATED_SKILL_FILE_CONTENT = "---\nname: alpha\ndescription: Updated alpha skill.\n---\n"
SECOND_SKILL_FILE_CONTENT = "---\nname: beta\ndescription: Beta skill.\n---\n"
SYMLINK_TARGET_SKILL_FILE_CONTENT = "---\nname: alpha\ndescription: Symlink target skill.\n---\n"
CACHE_FILE_CONTENT = "compiled"
SOURCE_OPENAI_METADATA = "display_name: Source Alpha\n"
MANIFEST_SCHEMA_VERSION = 1
BUNDLE_ID = "dev-methodology"
SKILL_ARTIFACT_TYPE = "skill"
AGENT_ARTIFACT_TYPE = "agent"
AGENT_FILE_CONTENT = 'name = "reviewer"\ndescription = "Review."\ndeveloper_instructions = "Review."\n'


def load_installer() -> ModuleType:
    spec = importlib.util.spec_from_file_location("install_skills", INSTALLER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load install-skills.py")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class InstallSkillsTests(unittest.TestCase):
    def create_skill(self, root: Path, name: str, content: str = SKILL_FILE_CONTENT) -> Path:
        skill = root / name
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text(content, encoding="utf-8")
        return skill

    def artifact_digest(self, path: Path) -> str:
        digest = hashlib.sha256()
        paths = (
            [path]
            if path.is_file()
            else sorted(item for item in path.rglob("*") if item.is_file())
        )
        for item in paths:
            relative_path = (
                item.name if path.is_file() else item.relative_to(path).as_posix()
            )
            digest.update(relative_path.encode("utf-8"))
            digest.update(item.read_bytes())
        return digest.hexdigest()

    def write_manifest(
        self,
        destination: Path,
        adapter: str,
        artifacts: list[dict[str, str]],
    ) -> None:
        manifest = {
            "schema_version": MANIFEST_SCHEMA_VERSION,
            "bundle_id": BUNDLE_ID,
            "adapter": adapter,
            "source": "test-source",
            "updated_at": "2026-01-01T00:00:00+00:00",
            "artifacts": artifacts,
        }
        destination.mkdir(parents=True, exist_ok=True)
        (destination / ".dev-methodology-install.json").write_text(
            json.dumps(manifest, sort_keys=True),
            encoding="utf-8",
        )

    def create_manifest(
        self,
        destination: Path,
        skill_names: list[str],
        *,
        adapter: str = "generic",
    ) -> None:
        self.write_manifest(
            destination,
            adapter,
            [
                {
                    "type": SKILL_ARTIFACT_TYPE,
                    "name": skill_name,
                    "path": skill_name,
                    "sha256": self.artifact_digest(destination / skill_name),
                }
                for skill_name in skill_names
            ],
        )

    def create_agent_manifest(
        self,
        destination: Path,
        agent_names: list[str],
        *,
        adapter: str = "codex",
        extension: str = ".toml",
    ) -> None:
        self.write_manifest(
            destination,
            adapter,
            [
                {
                    "type": AGENT_ARTIFACT_TYPE,
                    "name": agent_name,
                    "path": f"{agent_name}{extension}",
                    "sha256": self.artifact_digest(destination / f"{agent_name}{extension}"),
                }
                for agent_name in agent_names
            ],
        )

    def read_manifest_skill_names(self, destination: Path) -> list[str]:
        manifest = json.loads(
            (destination / ".dev-methodology-install.json").read_text(encoding="utf-8")
        )
        return [
            artifact["name"]
            for artifact in manifest["artifacts"]
            if artifact["type"] == SKILL_ARTIFACT_TYPE
        ]

    def read_manifest_agent_names(self, destination: Path) -> list[str]:
        manifest = json.loads(
            (destination / ".dev-methodology-install.json").read_text(encoding="utf-8")
        )
        return [
            artifact["name"]
            for artifact in manifest["artifacts"]
            if artifact["type"] == AGENT_ARTIFACT_TYPE
        ]

    def _tree_snapshot(self, root: Path) -> tuple[tuple[str, str, bytes], ...]:
        if not root.exists():
            return ()
        return tuple(
            (
                path.relative_to(root).as_posix(),
                "directory" if path.is_dir() else "file",
                b"" if path.is_dir() else path.read_bytes(),
            )
            for path in sorted(root.rglob("*"))
        )

    def test_installs_skill_directories_and_ignores_generated_cache(self) -> None:
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            destination = root / "dest"
            alpha = self.create_skill(source, "alpha")
            self.create_skill(source, "beta", SECOND_SKILL_FILE_CONTENT)
            cache = alpha / "__pycache__"
            cache.mkdir()
            (cache / "ignored.pyc").write_text(CACHE_FILE_CONTENT, encoding="utf-8")

            output = io.StringIO()
            with redirect_stdout(output):
                exit_code = installer.main(["--source", str(source), "--dest", str(destination)])

            self.assertEqual(exit_code, installer.SUCCESS_EXIT_CODE)
            self.assertEqual((destination / "alpha" / "SKILL.md").read_text(encoding="utf-8"), SKILL_FILE_CONTENT)
            self.assertEqual((destination / "beta" / "SKILL.md").read_text(encoding="utf-8"), SECOND_SKILL_FILE_CONTENT)
            self.assertFalse((destination / "alpha" / "__pycache__").exists())

    def test_skips_existing_skills_unless_replace_is_requested(self) -> None:
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            destination = root / "dest"
            alpha = self.create_skill(source, "alpha")

            first_output = io.StringIO()
            with redirect_stdout(first_output):
                first_exit_code = installer.main(["--source", str(source), "--dest", str(destination)])
            (alpha / "SKILL.md").write_text(UPDATED_SKILL_FILE_CONTENT, encoding="utf-8")

            output = io.StringIO()
            with redirect_stdout(output):
                second_exit_code = installer.main(["--source", str(source), "--dest", str(destination)])

            self.assertEqual(first_exit_code, installer.SUCCESS_EXIT_CODE)
            self.assertEqual(second_exit_code, installer.SUCCESS_EXIT_CODE)
            self.assertIn("skipped alpha", output.getvalue())
            self.assertEqual((destination / "alpha" / "SKILL.md").read_text(encoding="utf-8"), SKILL_FILE_CONTENT)

            replace_output = io.StringIO()
            with redirect_stdout(replace_output):
                replace_exit_code = installer.main(["--source", str(source), "--dest", str(destination), "--replace"])

            self.assertEqual(replace_exit_code, installer.SUCCESS_EXIT_CODE)
            self.assertEqual((destination / "alpha" / "SKILL.md").read_text(encoding="utf-8"), UPDATED_SKILL_FILE_CONTENT)

    def test_owned_customization_requires_discrepancy_analysis_override(self) -> None:
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            destination = root / "dest"
            alpha = self.create_skill(source, "alpha")

            with redirect_stdout(io.StringIO()):
                first_exit_code = installer.main(["--source", str(source), "--dest", str(destination)])
            self.assertEqual(installer.SUCCESS_EXIT_CODE, first_exit_code)

            customized_content = "---\nname: alpha\ndescription: Customer customization.\n---\n"
            (destination / "alpha" / "SKILL.md").write_text(customized_content, encoding="utf-8")
            (alpha / "SKILL.md").write_text(UPDATED_SKILL_FILE_CONTENT, encoding="utf-8")

            error_output = io.StringIO()
            with redirect_stdout(io.StringIO()), redirect_stderr(error_output):
                protected_exit_code = installer.main(
                    ["--source", str(source), "--dest", str(destination), "--replace"]
                )

            self.assertEqual(installer.ERROR_EXIT_CODE, protected_exit_code)
            self.assertIn("require discrepancy analysis", error_output.getvalue())
            self.assertEqual(
                customized_content,
                (destination / "alpha" / "SKILL.md").read_text(encoding="utf-8"),
            )

            with redirect_stdout(io.StringIO()):
                approved_exit_code = installer.main(
                    [
                        "--source",
                        str(source),
                        "--dest",
                        str(destination),
                        "--replace",
                        "--replace-customized",
                    ]
                )

            self.assertEqual(installer.SUCCESS_EXIT_CODE, approved_exit_code)
            self.assertEqual(
                UPDATED_SKILL_FILE_CONTENT,
                (destination / "alpha" / "SKILL.md").read_text(encoding="utf-8"),
            )

    def test_scope_defaults_destinations_for_each_adapter(self) -> None:
        installer = load_installer()

        home = Path("/home/example")
        project = Path("/workspace/example")
        expected = {
            "generic": (Path(".agents/skills"), None),
            "codex": (Path(".agents/skills"), Path(".codex/agents")),
            "claude": (Path(".claude/skills"), Path(".claude/agents")),
            "gemini": (Path(".gemini/skills"), Path(".gemini/agents")),
            "junie": (Path(".junie/skills"), Path(".junie/agents")),
        }
        for adapter_name, (skills_path, agents_path) in expected.items():
            with self.subTest(adapter=adapter_name):
                adapter = installer.ADAPTERS[adapter_name]
                self.assertEqual(
                    (home / skills_path, home / agents_path if agents_path is not None else None),
                    installer.default_destinations(adapter, "user", home=home),
                )
                self.assertEqual(
                    (
                        project / skills_path,
                        project / agents_path if agents_path is not None else None,
                    ),
                    installer.default_destinations(adapter, "project", project_root=project),
                )

    def test_main_installs_to_user_and_project_scope_destinations(self) -> None:
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            for scope, base_method in (("user", "home"), ("project", "cwd")):
                with self.subTest(scope=scope):
                    case_root = root / scope
                    base = case_root / "base"
                    source = case_root / "source"
                    agents_source = case_root / "agents-source"
                    self.create_skill(source, "alpha")
                    agents_source.mkdir(parents=True)
                    (agents_source / "reviewer.toml").write_text(
                        AGENT_FILE_CONTENT,
                        encoding="utf-8",
                    )

                    with patch.object(installer.Path, base_method, return_value=base):
                        exit_code = installer.main(
                            [
                                "--adapter",
                                "codex",
                                "--source",
                                str(source),
                                "--scope",
                                scope,
                                "--configure-mcp",
                                "false",
                                "--install-agents",
                                "--agents-source",
                                str(agents_source),
                            ]
                        )

                    self.assertEqual(installer.SUCCESS_EXIT_CODE, exit_code)
                    self.assertTrue((base / ".agents/skills/alpha/SKILL.md").is_file())
                    self.assertTrue((base / ".codex/agents/reviewer.toml").is_file())

    def test_codex_project_deployment_creates_mcp_config_when_none_exists(self) -> None:
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            project = root / "project"
            source = root / "source"
            executable = root / "bin" / "mcp-agent-ops"
            self.create_skill(source, "alpha")
            project.mkdir()
            executable.parent.mkdir()
            executable.write_text("server", encoding="utf-8")

            with patch.object(installer.Path, "cwd", return_value=project):
                exit_code = installer.main(
                    [
                        "--adapter",
                        "codex",
                        "--source",
                        str(source),
                        "--scope",
                        "project",
                        "--mcp-agent-ops-executable",
                        str(executable),
                    ]
                )

            self.assertEqual(installer.SUCCESS_EXIT_CODE, exit_code)
            config_path = project / ".codex/config.toml"
            config = config_path.read_text(encoding="utf-8")
            self.assertIn("[mcp_servers.mcp-agent-ops]", config)
            self.assertIn(f'command = "{executable.resolve()}"', config)
            self.assertIn(
                f'MCP_AGENT_OPS_SKILL_ROOTS = "{(project / ".agents/skills").resolve()}"',
                config,
            )
            self.assertIn(
                f'MCP_AGENT_OPS_WORKSPACE_ROOTS = "{project.resolve()}"',
                config,
            )
            self.assertFalse(config_path.with_suffix(".toml.bak").exists())

    def test_codex_deployment_updates_config_without_mcp_servers_and_saves_backup(self) -> None:
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            project = root / "project"
            source = root / "source"
            executable = root / "mcp-agent-ops"
            config_path = project / ".codex/config.toml"
            self.create_skill(source, "alpha")
            project.mkdir()
            executable.write_text("server", encoding="utf-8")
            config_path.parent.mkdir()
            original = 'model = "gpt-5"\n'
            config_path.write_text(original, encoding="utf-8")

            with patch.object(installer.Path, "cwd", return_value=project):
                exit_code = installer.main(
                    [
                        "--adapter",
                        "codex",
                        "--source",
                        str(source),
                        "--scope",
                        "project",
                        "--mcp-agent-ops-executable",
                        str(executable),
                    ]
                )

            self.assertEqual(installer.SUCCESS_EXIT_CODE, exit_code)
            self.assertEqual(
                original,
                config_path.with_suffix(".toml.bak").read_text(encoding="utf-8"),
            )
            active_config = config_path.read_text(encoding="utf-8")
            self.assertIn(original, active_config)
            self.assertIn("[mcp_servers.mcp-agent-ops]", active_config)

    def test_codex_deployment_keeps_existing_mcp_agent_ops_config_without_rediscovery(self) -> None:
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            project = root / "project"
            source = root / "source"
            config_path = project / ".codex/config.toml"
            self.create_skill(source, "alpha")
            project.mkdir()
            config_path.parent.mkdir()
            original = '[mcp_servers.mcp-agent-ops]\ncommand = "/installed/server"\n'
            config_path.write_text(original, encoding="utf-8")

            with (
                patch.object(installer.Path, "cwd", return_value=project),
                patch.object(installer.shutil, "which", return_value=None),
                redirect_stdout(io.StringIO()),
            ):
                exit_code = installer.main(
                    [
                        "--adapter",
                        "codex",
                        "--source",
                        str(source),
                        "--scope",
                        "project",
                    ]
                )

            self.assertEqual(installer.SUCCESS_EXIT_CODE, exit_code)
            self.assertEqual(original, config_path.read_text(encoding="utf-8"))
            self.assertFalse(config_path.with_suffix(".toml.bak").exists())

    def test_codex_deployment_preserves_other_servers_until_candidate_is_accepted(self) -> None:
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            project = root / "project"
            source = root / "source"
            executable = root / "mcp-agent-ops"
            config_path = project / ".codex/config.toml"
            self.create_skill(source, "alpha")
            project.mkdir()
            executable.write_text("server", encoding="utf-8")
            config_path.parent.mkdir(parents=True)
            original = '[mcp_servers.github]\ncommand = "github-mcp"\n'
            config_path.write_text(original, encoding="utf-8")

            output = io.StringIO()
            with (
                patch.object(installer.Path, "cwd", return_value=project),
                patch.object(installer.sys.stdin, "isatty", return_value=True),
                patch("builtins.input", return_value="n"),
                redirect_stdout(output),
            ):
                declined_exit_code = installer.main(
                    [
                        "--adapter",
                        "codex",
                        "--source",
                        str(source),
                        "--scope",
                        "project",
                        "--mcp-agent-ops-executable",
                        str(executable),
                    ]
                )

            candidate_path = project / ".codex/config.mcp-agent-ops.toml"
            self.assertEqual(installer.SUCCESS_EXIT_CODE, declined_exit_code)
            self.assertEqual(original, config_path.read_text(encoding="utf-8"))
            self.assertIn("[mcp_servers.github]", candidate_path.read_text(encoding="utf-8"))
            self.assertIn(
                "[mcp_servers.mcp-agent-ops]",
                candidate_path.read_text(encoding="utf-8"),
            )
            self.assertFalse(config_path.with_suffix(".toml.bak").exists())
            self.assertIn("kept active MCP config", output.getvalue())

            with (
                patch.object(installer.Path, "cwd", return_value=project),
                patch.object(installer.sys.stdin, "isatty", return_value=True),
                patch("builtins.input", return_value="y"),
                redirect_stdout(io.StringIO()),
            ):
                accepted_exit_code = installer.main(
                    [
                        "--adapter",
                        "codex",
                        "--source",
                        str(source),
                        "--scope",
                        "project",
                        "--mcp-agent-ops-executable",
                        str(executable),
                    ]
                )

            self.assertEqual(installer.SUCCESS_EXIT_CODE, accepted_exit_code)
            self.assertEqual(
                original,
                config_path.with_suffix(".toml.bak").read_text(encoding="utf-8"),
            )
            self.assertIn("[mcp_servers.github]", config_path.read_text(encoding="utf-8"))
            self.assertIn("[mcp_servers.mcp-agent-ops]", config_path.read_text(encoding="utf-8"))
            self.assertFalse(candidate_path.exists())

    def test_junie_project_deployment_adds_server_to_empty_mcp_catalog(self) -> None:
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            project = root / "project"
            source = root / "source"
            executable = root / "mcp-agent-ops"
            config_path = project / ".junie/mcp.json"
            self.create_skill(source, "alpha")
            project.mkdir()
            executable.write_text("server", encoding="utf-8")
            config_path.parent.mkdir(parents=True)
            config_path.write_text('{"mcpServers": {}}\n', encoding="utf-8")

            with patch.object(installer.Path, "cwd", return_value=project):
                exit_code = installer.main(
                    [
                        "--adapter",
                        "junie",
                        "--source",
                        str(source),
                        "--scope",
                        "project",
                        "--mcp-agent-ops-executable",
                        str(executable),
                    ]
                )

            self.assertEqual(installer.SUCCESS_EXIT_CODE, exit_code)
            config = json.loads(config_path.read_text(encoding="utf-8"))
            self.assertEqual(
                str(executable.resolve()),
                config["mcpServers"]["mcp-agent-ops"]["command"],
            )
            self.assertEqual(
                str(project.resolve()),
                config["mcpServers"]["mcp-agent-ops"]["env"][
                    "MCP_AGENT_OPS_WORKSPACE_ROOTS"
                ],
            )
            self.assertEqual(
                '{"mcpServers": {}}\n',
                config_path.with_suffix(".json.bak").read_text(encoding="utf-8"),
            )

    def test_explicit_destinations_override_scope_defaults_in_main(self) -> None:
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            home = root / "home"
            source = root / "source"
            agents_source = root / "agents-source"
            skills_destination = root / "custom-skills"
            agents_destination = root / "custom-agents"
            self.create_skill(source, "alpha")
            agents_source.mkdir()
            (agents_source / "reviewer.toml").write_text(
                AGENT_FILE_CONTENT,
                encoding="utf-8",
            )

            with patch.object(installer.Path, "home", return_value=home):
                exit_code = installer.main(
                    [
                        "--adapter",
                        "codex",
                        "--source",
                        str(source),
                        "--scope",
                        "user",
                        "--configure-mcp",
                        "false",
                        "--dest",
                        str(skills_destination),
                        "--install-agents",
                        "--agents-source",
                        str(agents_source),
                        "--agents-dest",
                        str(agents_destination),
                    ]
                )

            self.assertEqual(installer.SUCCESS_EXIT_CODE, exit_code)
            self.assertTrue((skills_destination / "alpha/SKILL.md").is_file())
            self.assertTrue((agents_destination / "reviewer.toml").is_file())
            self.assertFalse((home / ".agents/skills").exists())
            self.assertFalse((home / ".codex/agents").exists())

    def test_destination_or_scope_is_required(self) -> None:
        installer = load_installer()

        error_output = io.StringIO()
        with redirect_stdout(io.StringIO()), redirect_stderr(error_output):
            exit_code = installer.main(["--adapter", "codex"])

        self.assertEqual(installer.ERROR_EXIT_CODE, exit_code)
        self.assertIn("provide --dest or --scope", error_output.getvalue())

    def test_cleanup_defaults_true_and_accepts_explicit_false(self) -> None:
        installer = load_installer()

        self.assertTrue(installer.parse_args(["--dest", "target"]).cleanup)
        self.assertFalse(
            installer.parse_args(["--dest", "target", "--cleanup", "false"]).cleanup
        )
        with self.assertRaises(SystemExit), redirect_stderr(io.StringIO()):
            installer.parse_args(["--dest", "target", "--cleanup", "sometimes"])

    def test_explicit_destination_is_used(self) -> None:
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            destination = root / "custom-dest"
            self.create_skill(source, "alpha")

            output = io.StringIO()
            with redirect_stdout(output):
                exit_code = installer.main(
                    ["--adapter", "claude", "--source", str(source), "--dest", str(destination)]
                )

            self.assertEqual(exit_code, installer.SUCCESS_EXIT_CODE)
            self.assertTrue((destination / "alpha" / "SKILL.md").is_file())

    def test_codex_install_merges_only_its_harness_specific_skills(self) -> None:
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            adapter_source = root / "codex-skills"
            destination = root / "dest"
            self.create_skill(source, "alpha")
            self.create_skill(
                adapter_source,
                "codex-harness-directives",
                "---\nname: codex-harness-directives\ndescription: Codex directives.\n---\n",
            )

            exit_code = installer.main(
                [
                    "--adapter",
                    "codex",
                    "--source",
                    str(source),
                    "--adapter-skills-source",
                    str(adapter_source),
                    "--dest",
                    str(destination),
                ]
            )

            self.assertEqual(installer.SUCCESS_EXIT_CODE, exit_code)
            self.assertEqual(
                ["alpha", "codex-harness-directives"],
                self.read_manifest_skill_names(destination),
            )
            self.assertTrue((destination / "codex-harness-directives" / "SKILL.md").is_file())

    def test_default_codex_install_discovers_repository_adapter_skill(self) -> None:
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            destination = Path(temp_dir) / "dest"
            output = io.StringIO()
            with redirect_stdout(output):
                exit_code = installer.main(
                    ["--adapter", "codex", "--dest", str(destination), "--dry-run"]
                )

            self.assertEqual(installer.SUCCESS_EXIT_CODE, exit_code)
            self.assertIn("would install codex-harness-directives", output.getvalue())
            self.assertFalse(destination.exists())

    def test_non_codex_default_installs_exclude_codex_harness_skill(self) -> None:
        installer = load_installer()

        for adapter_name in ("claude", "gemini", "junie"):
            with self.subTest(adapter=adapter_name), tempfile.TemporaryDirectory() as temp_dir:
                destination = Path(temp_dir) / "dest"
                output = io.StringIO()
                with redirect_stdout(output):
                    exit_code = installer.main(
                        ["--adapter", adapter_name, "--dest", str(destination), "--dry-run"]
                    )

                self.assertEqual(installer.SUCCESS_EXIT_CODE, exit_code)
                self.assertNotIn("codex-harness-directives", output.getvalue())
                self.assertFalse(destination.exists())

    def test_duplicate_generic_and_adapter_skill_names_fail_closed(self) -> None:
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            adapter_source = root / "adapter-source"
            destination = root / "dest"
            self.create_skill(source, "alpha")
            self.create_skill(adapter_source, "alpha")
            errors = io.StringIO()
            with redirect_stderr(errors):
                exit_code = installer.main(
                    [
                        "--adapter",
                        "codex",
                        "--source",
                        str(source),
                        "--adapter-skills-source",
                        str(adapter_source),
                        "--dest",
                        str(destination),
                    ]
                )

            self.assertEqual(installer.ERROR_EXIT_CODE, exit_code)
            self.assertIn("duplicate names: alpha", errors.getvalue())
            self.assertFalse(destination.exists())

    def test_replace_existing_symlink_skill(self) -> None:
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            destination = root / "dest"
            symlink_target = root / "symlink-target"
            self.create_skill(source, "alpha", UPDATED_SKILL_FILE_CONTENT)
            self.create_skill(symlink_target, "alpha", SYMLINK_TARGET_SKILL_FILE_CONTENT)
            destination.mkdir()
            (destination / "alpha").symlink_to(symlink_target / "alpha", target_is_directory=True)

            output = io.StringIO()
            with redirect_stdout(output):
                exit_code = installer.main(["--source", str(source), "--dest", str(destination), "--replace"])

            self.assertEqual(exit_code, installer.SUCCESS_EXIT_CODE)
            self.assertFalse((destination / "alpha").is_symlink())
            self.assertEqual(
                UPDATED_SKILL_FILE_CONTENT,
                (destination / "alpha" / "SKILL.md").read_text(encoding="utf-8"),
            )

    def test_replace_dangling_skill_symlink_after_cleanup(self) -> None:
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            destination = root / "dest"
            self.create_skill(source, "alpha")
            self.create_skill(destination, "obsolete", SECOND_SKILL_FILE_CONTENT)
            (destination / "alpha").symlink_to(
                root / "missing-alpha",
                target_is_directory=True,
            )
            self.create_manifest(destination, ["alpha", "obsolete"])

            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                exit_code = installer.main(
                    ["--source", str(source), "--dest", str(destination), "--replace"]
                )

            self.assertEqual(installer.SUCCESS_EXIT_CODE, exit_code)
            self.assertFalse((destination / "alpha").is_symlink())
            self.assertTrue((destination / "alpha/SKILL.md").is_file())
            self.assertFalse((destination / "obsolete").exists())

    def test_install_keeps_openai_metadata_with_source_skill(self) -> None:
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            destination = root / "dest"
            alpha = self.create_skill(source, "alpha")
            metadata = alpha / "agents" / "openai.yaml"
            metadata.parent.mkdir()
            metadata.write_text(SOURCE_OPENAI_METADATA, encoding="utf-8")

            output = io.StringIO()
            with redirect_stdout(output):
                exit_code = installer.main(["--source", str(source), "--dest", str(destination)])

            self.assertEqual(exit_code, installer.SUCCESS_EXIT_CODE)
            self.assertEqual(
                SOURCE_OPENAI_METADATA,
                (destination / "alpha" / "agents" / "openai.yaml").read_text(encoding="utf-8"),
            )

    def test_codex_install_keeps_openai_metadata_with_source_skill(self) -> None:
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            destination = root / "dest"
            alpha = self.create_skill(source, "alpha")
            source_metadata = alpha / "agents" / "openai.yaml"
            source_metadata.parent.mkdir()
            source_metadata.write_text(SOURCE_OPENAI_METADATA, encoding="utf-8")
            output = io.StringIO()
            with redirect_stdout(output):
                exit_code = installer.main(["--adapter", "codex", "--source", str(source), "--dest", str(destination)])

            self.assertEqual(exit_code, installer.SUCCESS_EXIT_CODE)
            self.assertEqual(
                SOURCE_OPENAI_METADATA,
                (destination / "alpha" / "agents" / "openai.yaml").read_text(encoding="utf-8"),
            )

    def test_dry_run_reports_adapter_and_destination(self) -> None:
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            destination = root / "dest"
            self.create_skill(source, "alpha")

            output = io.StringIO()
            with redirect_stdout(output):
                exit_code = installer.main(
                    ["--adapter", "junie", "--source", str(source), "--dest", str(destination), "--dry-run"]
                )

            self.assertEqual(exit_code, installer.SUCCESS_EXIT_CODE)
            self.assertIn(f"adapter junie", output.getvalue())
            self.assertIn(f"destination {destination}", output.getvalue())
            self.assertIn("would install alpha", output.getvalue())
            self.assertFalse(destination.exists())

    def test_installs_generated_codex_agents_with_separate_ownership_manifest(self) -> None:
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            destination = root / "skills-dest"
            agents_source = root / "agents-source"
            agents_destination = root / "agents-dest"
            self.create_skill(source, "alpha")
            agents_source.mkdir()
            (agents_source / "reviewer.toml").write_text(AGENT_FILE_CONTENT, encoding="utf-8")

            output = io.StringIO()
            with redirect_stdout(output):
                exit_code = installer.main(
                    [
                        "--adapter",
                        "codex",
                        "--source",
                        str(source),
                        "--dest",
                        str(destination),
                        "--install-agents",
                        "--agents-source",
                        str(agents_source),
                        "--agents-dest",
                        str(agents_destination),
                    ]
                )

            self.assertEqual(installer.SUCCESS_EXIT_CODE, exit_code)
            self.assertEqual(
                AGENT_FILE_CONTENT,
                (agents_destination / "reviewer.toml").read_text(encoding="utf-8"),
            )
            self.assertEqual(["reviewer"], self.read_manifest_agent_names(agents_destination))
            self.assertIn(f"agents destination {agents_destination}", output.getvalue())

    def test_installs_generated_markdown_agents_for_gemini_claude_and_junie(self) -> None:
        installer = load_installer()

        for adapter_name in ("gemini", "claude", "junie"):
            with self.subTest(adapter=adapter_name), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                source = root / "source"
                destination = root / "skills-dest"
                agents_source = root / "agents-source"
                agents_destination = root / "agents-dest"
                self.create_skill(source, "alpha")
                agents_source.mkdir()
                (agents_source / "reviewer.md").write_text(AGENT_FILE_CONTENT, encoding="utf-8")

                exit_code = installer.main(
                    [
                        "--adapter",
                        adapter_name,
                        "--source",
                        str(source),
                        "--dest",
                        str(destination),
                        "--install-agents",
                        "--agents-source",
                        str(agents_source),
                        "--agents-dest",
                        str(agents_destination),
                    ]
                )

                self.assertEqual(installer.SUCCESS_EXIT_CODE, exit_code)
                self.assertEqual(
                    AGENT_FILE_CONTENT,
                    (agents_destination / "reviewer.md").read_text(encoding="utf-8"),
                )
                self.assertEqual(["reviewer"], self.read_manifest_agent_names(agents_destination))

    def test_agent_install_requires_destination_or_scope_before_copying_skills(self) -> None:
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            destination = root / "skills-dest"
            self.create_skill(source, "alpha")

            error_output = io.StringIO()
            with redirect_stdout(io.StringIO()), redirect_stderr(error_output):
                exit_code = installer.main(
                    [
                        "--adapter",
                        "codex",
                        "--source",
                        str(source),
                        "--dest",
                        str(destination),
                        "--install-agents",
                    ]
                )

            self.assertEqual(installer.ERROR_EXIT_CODE, exit_code)
            self.assertFalse(destination.exists())
            self.assertIn("requires --agents-dest or --scope", error_output.getvalue())

    def test_remove_owned_cleans_skills_and_agents_but_preserves_unowned_content(self) -> None:
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            destination = root / "skills-dest"
            agents_source = root / "agents-source"
            agents_destination = root / "agents-dest"
            self.create_skill(source, "alpha")
            agents_source.mkdir()
            (agents_source / "reviewer.toml").write_text(AGENT_FILE_CONTENT, encoding="utf-8")

            with redirect_stdout(io.StringIO()):
                install_exit_code = installer.main(
                    [
                        "--adapter",
                        "codex",
                        "--source",
                        str(source),
                        "--dest",
                        str(destination),
                        "--install-agents",
                        "--agents-source",
                        str(agents_source),
                        "--agents-dest",
                        str(agents_destination),
                    ]
                )
            self.create_skill(destination, "local-only", SECOND_SKILL_FILE_CONTENT)
            (agents_destination / "local-only.toml").write_text(AGENT_FILE_CONTENT, encoding="utf-8")

            output = io.StringIO()
            with redirect_stdout(output):
                remove_exit_code = installer.main(
                    [
                        "--adapter",
                        "codex",
                        "--dest",
                        str(destination),
                        "--agents-dest",
                        str(agents_destination),
                        "--remove-owned",
                    ]
                )

            self.assertEqual(installer.SUCCESS_EXIT_CODE, install_exit_code)
            self.assertEqual(installer.SUCCESS_EXIT_CODE, remove_exit_code)
            self.assertFalse((destination / "alpha").exists())
            self.assertFalse((agents_destination / "reviewer.toml").exists())
            self.assertFalse((destination / installer.INSTALL_MANIFEST_FILE_NAME).exists())
            self.assertFalse((agents_destination / installer.INSTALL_MANIFEST_FILE_NAME).exists())
            self.assertTrue((destination / "local-only" / "SKILL.md").is_file())
            self.assertTrue((agents_destination / "local-only.toml").is_file())
            self.assertIn("removed owned skill alpha", output.getvalue())
            self.assertIn("removed owned agent reviewer", output.getvalue())

    def test_remove_owned_refuses_to_delete_customized_content(self) -> None:
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            destination = root / "dest"
            self.create_skill(source, "alpha")
            with redirect_stdout(io.StringIO()):
                install_exit_code = installer.main(
                    ["--source", str(source), "--dest", str(destination)]
                )
            customized = "---\nname: alpha\ndescription: Customized.\n---\n"
            (destination / "alpha" / "SKILL.md").write_text(customized, encoding="utf-8")

            error_output = io.StringIO()
            with redirect_stdout(io.StringIO()), redirect_stderr(error_output):
                remove_exit_code = installer.main(
                    ["--dest", str(destination), "--remove-owned"]
                )

            self.assertEqual(installer.SUCCESS_EXIT_CODE, install_exit_code)
            self.assertEqual(installer.ERROR_EXIT_CODE, remove_exit_code)
            self.assertTrue((destination / "alpha" / "SKILL.md").is_file())
            self.assertIn("customized owned skills require discrepancy analysis", error_output.getvalue())

    def test_cleanup_removes_deleted_skill_but_preserves_unowned_skill(self) -> None:
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            destination = root / "dest"
            self.create_skill(source, "alpha")
            self.create_skill(destination, "alpha", UPDATED_SKILL_FILE_CONTENT)
            self.create_skill(destination, "obsolete", SECOND_SKILL_FILE_CONTENT)
            self.create_skill(destination, "local-only", SECOND_SKILL_FILE_CONTENT)
            self.create_manifest(destination, ["alpha", "obsolete"])

            output = io.StringIO()
            with redirect_stdout(output):
                exit_code = installer.main(
                    [
                        "--source",
                        str(source),
                        "--dest",
                        str(destination),
                        "--replace",
                    ]
                )

            self.assertEqual(exit_code, installer.SUCCESS_EXIT_CODE)
            self.assertFalse((destination / "obsolete").exists())
            self.assertTrue((destination / "local-only" / "SKILL.md").is_file())
            self.assertEqual(["alpha"], self.read_manifest_skill_names(destination))
            self.assertIn("cleaned up obsolete obsolete", output.getvalue())

    def test_cleanup_bootstraps_manifest_without_deleting_unknown_destination(self) -> None:
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            destination = root / "dest"
            self.create_skill(source, "alpha")
            self.create_skill(destination, "legacy", SECOND_SKILL_FILE_CONTENT)

            output = io.StringIO()
            with redirect_stdout(output):
                exit_code = installer.main(
                    [
                        "--source",
                        str(source),
                        "--dest",
                        str(destination),
                        "--replace",
                    ]
                )

            self.assertEqual(exit_code, installer.SUCCESS_EXIT_CODE)
            self.assertTrue((destination / "legacy" / "SKILL.md").is_file())
            self.assertEqual(["alpha"], self.read_manifest_skill_names(destination))
            self.assertIn("cleanup skipped; no ownership manifest", output.getvalue())

    def test_cleanup_false_preserves_obsolete_owned_skill_for_later_cleanup(self) -> None:
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            destination = root / "dest"
            self.create_skill(source, "alpha")
            self.create_skill(destination, "alpha", UPDATED_SKILL_FILE_CONTENT)
            self.create_skill(destination, "obsolete", SECOND_SKILL_FILE_CONTENT)
            self.create_manifest(destination, ["alpha", "obsolete"])

            with redirect_stdout(io.StringIO()):
                exit_code = installer.main(
                    [
                        "--source",
                        str(source),
                        "--dest",
                        str(destination),
                        "--replace",
                        "--cleanup",
                        "false",
                    ]
                )

            self.assertEqual(installer.SUCCESS_EXIT_CODE, exit_code)
            self.assertTrue((destination / "obsolete" / "SKILL.md").is_file())
            self.assertEqual(
                ["alpha", "obsolete"],
                self.read_manifest_skill_names(destination),
            )

    def test_dry_run_cleanup_reports_without_deleting_or_rewriting_manifest(self) -> None:
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            destination = root / "dest"
            self.create_skill(source, "alpha")
            self.create_skill(destination, "alpha", UPDATED_SKILL_FILE_CONTENT)
            self.create_skill(destination, "obsolete", SECOND_SKILL_FILE_CONTENT)
            self.create_manifest(destination, ["alpha", "obsolete"])

            before_manifest = (destination / ".dev-methodology-install.json").read_text(
                encoding="utf-8"
            )
            output = io.StringIO()
            with redirect_stdout(output):
                exit_code = installer.main(
                    [
                        "--source",
                        str(source),
                        "--dest",
                        str(destination),
                        "--replace",
                        "--dry-run",
                    ]
                )

            self.assertEqual(exit_code, installer.SUCCESS_EXIT_CODE)
            self.assertTrue((destination / "obsolete" / "SKILL.md").is_file())
            self.assertEqual(
                before_manifest,
                (destination / ".dev-methodology-install.json").read_text(encoding="utf-8"),
            )
            self.assertIn("would clean up obsolete obsolete", output.getvalue())

    def test_manifest_schema_and_adapter_are_validated_before_cleanup(self) -> None:
        installer = load_installer()

        invalid_values = (
            ("schema_version", 999),
            ("schema_version", True),
            ("adapter", "codex"),
        )
        for invalid_field, invalid_value in invalid_values:
            with (
                self.subTest(invalid_field=invalid_field),
                tempfile.TemporaryDirectory() as temp_dir,
            ):
                root = Path(temp_dir)
                source = root / "source"
                destination = root / "dest"
                self.create_skill(source, "alpha", UPDATED_SKILL_FILE_CONTENT)
                self.create_skill(destination, "alpha")
                self.create_skill(destination, "obsolete", SECOND_SKILL_FILE_CONTENT)
                self.create_manifest(destination, ["alpha", "obsolete"])
                manifest_path = destination / ".dev-methodology-install.json"
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                manifest[invalid_field] = invalid_value
                manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

                error_output = io.StringIO()
                with redirect_stdout(io.StringIO()), redirect_stderr(error_output):
                    exit_code = installer.main(
                        ["--source", str(source), "--dest", str(destination), "--replace"]
                    )

                self.assertEqual(installer.ERROR_EXIT_CODE, exit_code)
                self.assertEqual(
                    SKILL_FILE_CONTENT,
                    (destination / "alpha/SKILL.md").read_text(encoding="utf-8"),
                )
                self.assertTrue((destination / "obsolete/SKILL.md").is_file())
                self.assertIn("install manifest", error_output.getvalue())

    def test_manifest_artifacts_are_fully_validated_before_cleanup(self) -> None:
        installer = load_installer()

        for invalid_artifact in ("missing_digest", "unsupported_type", "duplicate_path"):
            with (
                self.subTest(invalid_artifact=invalid_artifact),
                tempfile.TemporaryDirectory() as temp_dir,
            ):
                root = Path(temp_dir)
                source = root / "source"
                destination = root / "dest"
                self.create_skill(source, "alpha", UPDATED_SKILL_FILE_CONTENT)
                self.create_skill(destination, "alpha")
                self.create_skill(destination, "obsolete", SECOND_SKILL_FILE_CONTENT)
                self.create_manifest(destination, ["alpha", "obsolete"])
                manifest_path = destination / ".dev-methodology-install.json"
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                if invalid_artifact == "missing_digest":
                    manifest["artifacts"][1].pop("sha256")
                elif invalid_artifact == "unsupported_type":
                    manifest["artifacts"][1]["type"] = "unknown"
                else:
                    duplicate = dict(manifest["artifacts"][1])
                    duplicate["name"] = "duplicate"
                    manifest["artifacts"].append(duplicate)
                manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

                error_output = io.StringIO()
                with redirect_stdout(io.StringIO()), redirect_stderr(error_output):
                    exit_code = installer.main(
                        ["--source", str(source), "--dest", str(destination), "--replace"]
                    )

                self.assertEqual(installer.ERROR_EXIT_CODE, exit_code)
                self.assertEqual(
                    SKILL_FILE_CONTENT,
                    (destination / "alpha/SKILL.md").read_text(encoding="utf-8"),
                )
                self.assertTrue((destination / "obsolete/SKILL.md").is_file())
                self.assertIn("artifact", error_output.getvalue())

    def test_manifest_artifact_paths_cannot_escape_destination(self) -> None:
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            destination = root / "dest"
            outside = root / "outside"
            self.create_skill(destination, "alpha")
            self.create_skill(outside, "sentinel", SECOND_SKILL_FILE_CONTENT)
            self.create_manifest(destination, ["alpha"])
            manifest_path = destination / ".dev-methodology-install.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["artifacts"].append(
                {
                    "type": SKILL_ARTIFACT_TYPE,
                    "name": "outside",
                    "path": "../outside",
                    "sha256": self.artifact_digest(outside),
                }
            )
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            error_output = io.StringIO()
            with redirect_stdout(io.StringIO()), redirect_stderr(error_output):
                exit_code = installer.main(
                    ["--dest", str(destination), "--remove-owned"]
                )

            self.assertEqual(installer.ERROR_EXIT_CODE, exit_code)
            self.assertTrue((outside / "sentinel/SKILL.md").is_file())
            self.assertIn("path", error_output.getvalue())

    def test_skill_manifest_symlink_is_rejected_without_writing_outside(self) -> None:
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            destination = root / "dest"
            outside_manifest = root / "outside-manifest.json"
            self.create_skill(source, "alpha")
            destination.mkdir()
            (destination / ".dev-methodology-install.json").symlink_to(outside_manifest)

            error_output = io.StringIO()
            with redirect_stdout(io.StringIO()), redirect_stderr(error_output):
                exit_code = installer.main(
                    ["--source", str(source), "--dest", str(destination)]
                )

            self.assertEqual(installer.ERROR_EXIT_CODE, exit_code)
            self.assertFalse(outside_manifest.exists())
            self.assertFalse((destination / "alpha").exists())
            self.assertIn("manifest", error_output.getvalue())

    def test_agent_manifest_symlink_is_rejected_before_skill_install(self) -> None:
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            destination = root / "skills-dest"
            agents_source = root / "agents-source"
            agents_destination = root / "agents-dest"
            outside_manifest = root / "outside-agent-manifest.json"
            self.create_skill(source, "alpha", UPDATED_SKILL_FILE_CONTENT)
            self.create_skill(destination, "alpha")
            self.create_manifest(destination, ["alpha"], adapter="codex")
            agents_source.mkdir()
            (agents_source / "reviewer.toml").write_text(
                AGENT_FILE_CONTENT,
                encoding="utf-8",
            )
            agents_destination.mkdir()
            (agents_destination / ".dev-methodology-install.json").symlink_to(
                outside_manifest
            )

            error_output = io.StringIO()
            with redirect_stdout(io.StringIO()), redirect_stderr(error_output):
                exit_code = installer.main(
                    [
                        "--adapter",
                        "codex",
                        "--source",
                        str(source),
                        "--dest",
                        str(destination),
                        "--replace",
                        "--install-agents",
                        "--agents-source",
                        str(agents_source),
                        "--agents-dest",
                        str(agents_destination),
                    ]
                )

            self.assertEqual(installer.ERROR_EXIT_CODE, exit_code)
            self.assertFalse(outside_manifest.exists())
            self.assertEqual(
                SKILL_FILE_CONTENT,
                (destination / "alpha/SKILL.md").read_text(encoding="utf-8"),
            )
            self.assertFalse((agents_destination / "reviewer.toml").exists())
            self.assertIn("manifest", error_output.getvalue())

    def test_install_prevalidates_skill_and_agent_plans_before_mutation(self) -> None:
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            destination = root / "skills-dest"
            agents_source = root / "agents-source"
            agents_destination = root / "agents-dest"
            self.create_skill(source, "alpha", UPDATED_SKILL_FILE_CONTENT)
            self.create_skill(destination, "alpha")
            self.create_manifest(destination, ["alpha"], adapter="codex")
            agents_source.mkdir()
            agents_destination.mkdir()
            (agents_source / "reviewer.toml").write_text(
                'name = "reviewer"\ndescription = "Updated."\n',
                encoding="utf-8",
            )
            (agents_destination / "reviewer.toml").write_text(
                AGENT_FILE_CONTENT,
                encoding="utf-8",
            )
            self.create_agent_manifest(agents_destination, ["reviewer"])
            agent_manifest_path = agents_destination / ".dev-methodology-install.json"
            agent_manifest = json.loads(agent_manifest_path.read_text(encoding="utf-8"))
            agent_manifest["schema_version"] = 999
            agent_manifest_path.write_text(json.dumps(agent_manifest), encoding="utf-8")

            error_output = io.StringIO()
            with redirect_stdout(io.StringIO()), redirect_stderr(error_output):
                exit_code = installer.main(
                    [
                        "--adapter",
                        "codex",
                        "--source",
                        str(source),
                        "--dest",
                        str(destination),
                        "--replace",
                        "--install-agents",
                        "--agents-source",
                        str(agents_source),
                        "--agents-dest",
                        str(agents_destination),
                    ]
                )

            self.assertEqual(installer.ERROR_EXIT_CODE, exit_code)
            self.assertEqual(
                SKILL_FILE_CONTENT,
                (destination / "alpha/SKILL.md").read_text(encoding="utf-8"),
            )
            self.assertEqual(
                AGENT_FILE_CONTENT,
                (agents_destination / "reviewer.toml").read_text(encoding="utf-8"),
            )

    def test_remove_owned_prevalidates_all_manifests_before_mutation(self) -> None:
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            destination = root / "skills-dest"
            agents_destination = root / "agents-dest"
            self.create_skill(destination, "alpha")
            self.create_manifest(destination, ["alpha"], adapter="codex")
            agents_destination.mkdir()
            (agents_destination / "reviewer.toml").write_text(
                AGENT_FILE_CONTENT,
                encoding="utf-8",
            )
            self.create_agent_manifest(agents_destination, ["reviewer"])
            agent_manifest_path = agents_destination / ".dev-methodology-install.json"
            agent_manifest = json.loads(agent_manifest_path.read_text(encoding="utf-8"))
            agent_manifest["schema_version"] = 999
            agent_manifest_path.write_text(json.dumps(agent_manifest), encoding="utf-8")

            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                exit_code = installer.main(
                    [
                        "--adapter",
                        "codex",
                        "--dest",
                        str(destination),
                        "--agents-dest",
                        str(agents_destination),
                        "--remove-owned",
                    ]
                )

            self.assertEqual(installer.ERROR_EXIT_CODE, exit_code)
            self.assertTrue((destination / "alpha/SKILL.md").is_file())
            self.assertTrue((agents_destination / "reviewer.toml").is_file())

    def test_empty_or_incomplete_skill_source_fails_closed(self) -> None:
        installer = load_installer()

        for source_state in ("empty", "incomplete", "mixed"):
            with (
                self.subTest(source_state=source_state),
                tempfile.TemporaryDirectory() as temp_dir,
            ):
                root = Path(temp_dir)
                source = root / "source"
                destination = root / "dest"
                source.mkdir()
                if source_state == "mixed":
                    self.create_skill(source, "alpha", UPDATED_SKILL_FILE_CONTENT)
                if source_state != "empty":
                    (source / "incomplete").mkdir()
                self.create_skill(destination, "alpha")
                self.create_manifest(destination, ["alpha"])

                error_output = io.StringIO()
                with redirect_stdout(io.StringIO()), redirect_stderr(error_output):
                    exit_code = installer.main(
                        ["--source", str(source), "--dest", str(destination), "--replace"]
                    )

                self.assertEqual(installer.ERROR_EXIT_CODE, exit_code)
                self.assertEqual(
                    SKILL_FILE_CONTENT,
                    (destination / "alpha/SKILL.md").read_text(encoding="utf-8"),
                )
                self.assertIn("skill source", error_output.getvalue())

    def test_unexpected_skill_source_file_fails_before_cleanup(self) -> None:
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            destination = root / "dest"
            self.create_skill(source, "retained")
            source.mkdir(exist_ok=True)
            (source / "alpha").write_text(SKILL_FILE_CONTENT, encoding="utf-8")
            self.create_skill(destination, "alpha")
            self.create_manifest(destination, ["alpha"])

            error_output = io.StringIO()
            with redirect_stdout(io.StringIO()), redirect_stderr(error_output):
                exit_code = installer.main(
                    ["--source", str(source), "--dest", str(destination), "--replace"]
                )

            self.assertEqual(installer.ERROR_EXIT_CODE, exit_code)
            self.assertTrue((destination / "alpha/SKILL.md").is_file())
            self.assertFalse((destination / "retained").exists())
            self.assertIn("alpha", error_output.getvalue())

    def test_reserved_manifest_name_is_rejected_as_a_source_skill(self) -> None:
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            destination = root / "dest"
            self.create_skill(source, ".dev-methodology-install.json")

            error_output = io.StringIO()
            with redirect_stdout(io.StringIO()), redirect_stderr(error_output):
                exit_code = installer.main(
                    ["--source", str(source), "--dest", str(destination)]
                )

            self.assertEqual(installer.ERROR_EXIT_CODE, exit_code)
            self.assertFalse(destination.exists())
            self.assertIn("reserved", error_output.getvalue())

    def test_unexpected_agent_source_entry_fails_before_any_install(self) -> None:
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            destination = root / "skills-dest"
            agents_source = root / "agents-source"
            agents_destination = root / "agents-dest"
            self.create_skill(source, "alpha", UPDATED_SKILL_FILE_CONTENT)
            self.create_skill(destination, "alpha")
            self.create_manifest(destination, ["alpha"], adapter="codex")
            agents_source.mkdir()
            (agents_source / "retained.toml").write_text(
                AGENT_FILE_CONTENT,
                encoding="utf-8",
            )
            (agents_source / "reviewer.md").write_text(
                AGENT_FILE_CONTENT,
                encoding="utf-8",
            )
            agents_destination.mkdir()
            (agents_destination / "reviewer.toml").write_text(
                AGENT_FILE_CONTENT,
                encoding="utf-8",
            )
            self.create_agent_manifest(agents_destination, ["reviewer"])

            error_output = io.StringIO()
            with redirect_stdout(io.StringIO()), redirect_stderr(error_output):
                exit_code = installer.main(
                    [
                        "--adapter",
                        "codex",
                        "--source",
                        str(source),
                        "--dest",
                        str(destination),
                        "--replace",
                        "--install-agents",
                        "--agents-source",
                        str(agents_source),
                        "--agents-dest",
                        str(agents_destination),
                    ]
                )

            self.assertEqual(installer.ERROR_EXIT_CODE, exit_code)
            self.assertEqual(
                SKILL_FILE_CONTENT,
                (destination / "alpha/SKILL.md").read_text(encoding="utf-8"),
            )
            self.assertTrue((agents_destination / "reviewer.toml").is_file())
            self.assertFalse((agents_destination / "retained.toml").exists())
            self.assertIn("reviewer.md", error_output.getvalue())

    def test_ignored_source_metadata_does_not_block_skill_or_agent_install(self) -> None:
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            destination = root / "skills-dest"
            agents_source = root / "agents-source"
            agents_destination = root / "agents-dest"
            self.create_skill(source, "alpha")
            agents_source.mkdir()
            (agents_source / "reviewer.toml").write_text(
                AGENT_FILE_CONTENT,
                encoding="utf-8",
            )
            for source_root in (source, agents_source):
                (source_root / ".DS_Store").write_text("metadata", encoding="utf-8")
                (source_root / "ignored.pyc").write_bytes(b"compiled")
                (source_root / "__pycache__").mkdir()

            with redirect_stdout(io.StringIO()):
                exit_code = installer.main(
                    [
                        "--adapter",
                        "codex",
                        "--source",
                        str(source),
                        "--dest",
                        str(destination),
                        "--install-agents",
                        "--agents-source",
                        str(agents_source),
                        "--agents-dest",
                        str(agents_destination),
                    ]
                )

            self.assertEqual(installer.SUCCESS_EXIT_CODE, exit_code)
            self.assertTrue((destination / "alpha/SKILL.md").is_file())
            self.assertTrue((agents_destination / "reviewer.toml").is_file())

    def test_empty_agent_source_fails_before_skill_install(self) -> None:
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            destination = root / "skills-dest"
            agents_source = root / "agents-source"
            agents_destination = root / "agents-dest"
            self.create_skill(source, "alpha", UPDATED_SKILL_FILE_CONTENT)
            self.create_skill(destination, "alpha")
            self.create_manifest(destination, ["alpha"], adapter="codex")
            agents_source.mkdir()
            agents_destination.mkdir()
            (agents_destination / "reviewer.toml").write_text(
                AGENT_FILE_CONTENT,
                encoding="utf-8",
            )
            self.create_agent_manifest(agents_destination, ["reviewer"])

            error_output = io.StringIO()
            with redirect_stdout(io.StringIO()), redirect_stderr(error_output):
                exit_code = installer.main(
                    [
                        "--adapter",
                        "codex",
                        "--source",
                        str(source),
                        "--dest",
                        str(destination),
                        "--replace",
                        "--install-agents",
                        "--agents-source",
                        str(agents_source),
                        "--agents-dest",
                        str(agents_destination),
                    ]
                )

            self.assertEqual(installer.ERROR_EXIT_CODE, exit_code)
            self.assertEqual(
                SKILL_FILE_CONTENT,
                (destination / "alpha/SKILL.md").read_text(encoding="utf-8"),
            )
            self.assertTrue((agents_destination / "reviewer.toml").is_file())
            self.assertIn("agent source", error_output.getvalue())

    def test_skill_source_and_destination_overlap_is_rejected_before_deletion(self) -> None:
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            source_and_destination = Path(temp_dir) / "skills"
            self.create_skill(source_and_destination, "alpha")

            error_output = io.StringIO()
            with redirect_stdout(io.StringIO()), redirect_stderr(error_output):
                exit_code = installer.main(
                    [
                        "--source",
                        str(source_and_destination),
                        "--dest",
                        str(source_and_destination),
                        "--replace",
                    ]
                )

            self.assertEqual(installer.ERROR_EXIT_CODE, exit_code)
            self.assertTrue((source_and_destination / "alpha/SKILL.md").is_file())
            self.assertFalse(
                (source_and_destination / ".dev-methodology-install.json").exists()
            )
            self.assertIn("overlap", error_output.getvalue())

    def test_skill_source_symlinks_are_rejected_before_target_deletion(self) -> None:
        installer = load_installer()

        for symlink_kind in ("skill_directory", "skill_manifest"):
            with (
                self.subTest(symlink_kind=symlink_kind),
                tempfile.TemporaryDirectory() as temp_dir,
            ):
                root = Path(temp_dir)
                source = root / "source"
                destination = root / "dest"
                source.mkdir()
                self.create_skill(destination, "alpha")
                if symlink_kind == "skill_directory":
                    (source / "alpha").symlink_to(
                        destination / "alpha",
                        target_is_directory=True,
                    )
                else:
                    (source / "alpha").mkdir()
                    (source / "alpha/SKILL.md").symlink_to(
                        destination / "alpha/SKILL.md"
                    )

                error_output = io.StringIO()
                with redirect_stdout(io.StringIO()), redirect_stderr(error_output):
                    exit_code = installer.main(
                        [
                            "--source",
                            str(source),
                            "--dest",
                            str(destination),
                            "--replace",
                        ]
                    )

                self.assertEqual(installer.ERROR_EXIT_CODE, exit_code)
                self.assertEqual(
                    SKILL_FILE_CONTENT,
                    (destination / "alpha/SKILL.md").read_text(encoding="utf-8"),
                )
                self.assertIn("symlink", error_output.getvalue())

    def test_agent_source_and_destination_overlap_is_rejected_before_skill_install(self) -> None:
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            destination = root / "skills-dest"
            agents_source_and_destination = root / "agents"
            self.create_skill(source, "alpha", UPDATED_SKILL_FILE_CONTENT)
            self.create_skill(destination, "alpha")
            self.create_manifest(destination, ["alpha"], adapter="codex")
            agents_source_and_destination.mkdir()
            (agents_source_and_destination / "reviewer.toml").write_text(
                AGENT_FILE_CONTENT,
                encoding="utf-8",
            )

            error_output = io.StringIO()
            with redirect_stdout(io.StringIO()), redirect_stderr(error_output):
                exit_code = installer.main(
                    [
                        "--adapter",
                        "codex",
                        "--source",
                        str(source),
                        "--dest",
                        str(destination),
                        "--replace",
                        "--install-agents",
                        "--agents-source",
                        str(agents_source_and_destination),
                        "--agents-dest",
                        str(agents_source_and_destination),
                    ]
                )

            self.assertEqual(installer.ERROR_EXIT_CODE, exit_code)
            self.assertTrue((agents_source_and_destination / "reviewer.toml").is_file())
            self.assertEqual(
                SKILL_FILE_CONTENT,
                (destination / "alpha/SKILL.md").read_text(encoding="utf-8"),
            )
            self.assertIn("overlap", error_output.getvalue())

    def test_invalid_agent_destination_root_is_rejected_before_skill_install(self) -> None:
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            destination = root / "skills-dest"
            agents_source = root / "agents-source"
            agents_destination = root / "agents-dest"
            self.create_skill(source, "alpha", UPDATED_SKILL_FILE_CONTENT)
            self.create_skill(destination, "alpha")
            self.create_manifest(destination, ["alpha"], adapter="codex")
            agents_source.mkdir()
            (agents_source / "reviewer.toml").write_text(
                AGENT_FILE_CONTENT,
                encoding="utf-8",
            )
            agents_destination.write_text("not a directory", encoding="utf-8")

            error_output = io.StringIO()
            with redirect_stdout(io.StringIO()), redirect_stderr(error_output):
                exit_code = installer.main(
                    [
                        "--adapter",
                        "codex",
                        "--source",
                        str(source),
                        "--dest",
                        str(destination),
                        "--replace",
                        "--install-agents",
                        "--agents-source",
                        str(agents_source),
                        "--agents-dest",
                        str(agents_destination),
                    ]
                )

            self.assertEqual(installer.ERROR_EXIT_CODE, exit_code)
            self.assertEqual(
                SKILL_FILE_CONTENT,
                (destination / "alpha/SKILL.md").read_text(encoding="utf-8"),
            )
            self.assertEqual(
                "not a directory",
                agents_destination.read_text(encoding="utf-8"),
            )
            self.assertIn("destination", error_output.getvalue())

    def test_combined_install_rejects_every_cross_boundary_overlap(self) -> None:
        installer = load_installer()

        for overlap_kind in (
            "destinations",
            "skill_source_agent_destination",
            "agent_source_skill_destination",
        ):
            with (
                self.subTest(overlap_kind=overlap_kind),
                tempfile.TemporaryDirectory() as temp_dir,
            ):
                root = Path(temp_dir)
                source = root / "source"
                agents_source = root / "agents-source"
                self.create_skill(source, "alpha")
                agents_source.mkdir()
                (agents_source / "reviewer.toml").write_text(
                    AGENT_FILE_CONTENT,
                    encoding="utf-8",
                )
                if overlap_kind == "destinations":
                    destination = root / "shared-destination"
                    agents_destination = destination
                elif overlap_kind == "skill_source_agent_destination":
                    destination = root / "skills-destination"
                    agents_destination = source
                else:
                    destination = agents_source
                    agents_destination = root / "agents-destination"

                error_output = io.StringIO()
                with redirect_stdout(io.StringIO()), redirect_stderr(error_output):
                    exit_code = installer.main(
                        [
                            "--adapter",
                            "codex",
                            "--source",
                            str(source),
                            "--dest",
                            str(destination),
                            "--install-agents",
                            "--agents-source",
                            str(agents_source),
                            "--agents-dest",
                            str(agents_destination),
                        ]
                    )

                self.assertEqual(installer.ERROR_EXIT_CODE, exit_code)
                self.assertTrue((source / "alpha/SKILL.md").is_file())
                self.assertTrue((agents_source / "reviewer.toml").is_file())
                if destination != source:
                    self.assertFalse((destination / "alpha/SKILL.md").exists())
                if agents_destination != agents_source:
                    self.assertFalse(
                        (agents_destination / "reviewer.toml").exists()
                    )
                self.assertIn("overlap", error_output.getvalue())

    def test_agent_source_symlink_is_rejected_before_target_deletion(self) -> None:
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            destination = root / "skills-dest"
            agents_source = root / "agents-source"
            agents_destination = root / "agents-dest"
            self.create_skill(source, "alpha", UPDATED_SKILL_FILE_CONTENT)
            self.create_skill(destination, "alpha")
            self.create_manifest(destination, ["alpha"], adapter="codex")
            agents_source.mkdir()
            agents_destination.mkdir()
            (agents_destination / "reviewer.toml").write_text(
                AGENT_FILE_CONTENT,
                encoding="utf-8",
            )
            (agents_source / "reviewer.toml").symlink_to(
                agents_destination / "reviewer.toml"
            )

            error_output = io.StringIO()
            with redirect_stdout(io.StringIO()), redirect_stderr(error_output):
                exit_code = installer.main(
                    [
                        "--adapter",
                        "codex",
                        "--source",
                        str(source),
                        "--dest",
                        str(destination),
                        "--replace",
                        "--install-agents",
                        "--agents-source",
                        str(agents_source),
                        "--agents-dest",
                        str(agents_destination),
                    ]
                )

            self.assertEqual(installer.ERROR_EXIT_CODE, exit_code)
            self.assertEqual(
                SKILL_FILE_CONTENT,
                (destination / "alpha/SKILL.md").read_text(encoding="utf-8"),
            )
            self.assertEqual(
                AGENT_FILE_CONTENT,
                (agents_destination / "reviewer.toml").read_text(encoding="utf-8"),
            )
            self.assertIn("symlink", error_output.getvalue())

    def test_agent_cleanup_can_be_enabled_or_disabled(self) -> None:
        installer = load_installer()

        for cleanup_enabled in (True, False):
            with (
                self.subTest(cleanup_enabled=cleanup_enabled),
                tempfile.TemporaryDirectory() as temp_dir,
            ):
                root = Path(temp_dir)
                source = root / "source"
                destination = root / "skills-dest"
                agents_source = root / "agents-source"
                agents_destination = root / "agents-dest"
                self.create_skill(source, "alpha")
                agents_source.mkdir()
                for agent_name in ("reviewer", "obsolete"):
                    (agents_source / f"{agent_name}.toml").write_text(
                        AGENT_FILE_CONTENT,
                        encoding="utf-8",
                    )
                with redirect_stdout(io.StringIO()):
                    first_exit_code = installer.main(
                        [
                            "--adapter",
                            "codex",
                            "--source",
                            str(source),
                            "--dest",
                            str(destination),
                            "--install-agents",
                            "--agents-source",
                            str(agents_source),
                            "--agents-dest",
                            str(agents_destination),
                        ]
                    )
                (agents_source / "obsolete.toml").unlink()
                second_args = [
                    "--adapter",
                    "codex",
                    "--source",
                    str(source),
                    "--dest",
                    str(destination),
                    "--replace",
                    "--install-agents",
                    "--agents-source",
                    str(agents_source),
                    "--agents-dest",
                    str(agents_destination),
                ]
                if not cleanup_enabled:
                    second_args.extend(["--cleanup", "false"])
                with redirect_stdout(io.StringIO()):
                    second_exit_code = installer.main(second_args)

                self.assertEqual(installer.SUCCESS_EXIT_CODE, first_exit_code)
                self.assertEqual(installer.SUCCESS_EXIT_CODE, second_exit_code)
                self.assertEqual(
                    not cleanup_enabled,
                    (agents_destination / "obsolete.toml").exists(),
                )
                expected_agents = (
                    ["reviewer"] if cleanup_enabled else ["obsolete", "reviewer"]
                )
                self.assertEqual(
                    expected_agents,
                    self.read_manifest_agent_names(agents_destination),
                )

    def test_prune_owned_remains_a_compatible_cleanup_alias(self) -> None:
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            destination = root / "dest"
            self.create_skill(source, "alpha")
            self.create_skill(destination, "alpha")
            self.create_skill(destination, "obsolete", SECOND_SKILL_FILE_CONTENT)
            self.create_manifest(destination, ["alpha", "obsolete"])

            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                exit_code = installer.main(
                    [
                        "--source",
                        str(source),
                        "--dest",
                        str(destination),
                        "--replace",
                        "--prune-owned",
                    ]
                )

            self.assertEqual(installer.SUCCESS_EXIT_CODE, exit_code)
            self.assertFalse((destination / "obsolete").exists())

    def test_skill_copy_failure_preserves_complete_existing_installation(self) -> None:
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            destination = root / "skills-dest"
            self.create_skill(source, "alpha")
            self.create_skill(source, "obsolete", SECOND_SKILL_FILE_CONTENT)
            with redirect_stdout(io.StringIO()):
                first_exit_code = installer.main(
                    ["--source", str(source), "--dest", str(destination)]
                )
            before = self._tree_snapshot(destination)
            (source / "alpha" / "SKILL.md").write_text(
                UPDATED_SKILL_FILE_CONTENT,
                encoding="utf-8",
            )
            installer.shutil.rmtree(source / "obsolete")
            real_copytree = installer.shutil.copytree

            def fail_source_skill_copy(
                source_path: Path,
                destination_path: Path,
                *args: object,
                **kwargs: object,
            ) -> Path:
                if Path(source_path).resolve() == (source / "alpha").resolve():
                    raise OSError("injected skill copy failure")
                return real_copytree(source_path, destination_path, *args, **kwargs)

            error_output = io.StringIO()
            with patch.object(
                installer.shutil,
                "copytree",
                side_effect=fail_source_skill_copy,
            ), redirect_stdout(io.StringIO()), redirect_stderr(error_output):
                exit_code = installer.main(
                    [
                        "--source",
                        str(source),
                        "--dest",
                        str(destination),
                        "--replace",
                    ]
                )

            self.assertEqual(installer.SUCCESS_EXIT_CODE, first_exit_code)
            self.assertEqual(installer.ERROR_EXIT_CODE, exit_code)
            self.assertEqual(before, self._tree_snapshot(destination))
            self.assertIn("injected skill copy failure", error_output.getvalue())

    def test_agent_copy_failure_rolls_back_skill_and_agent_installations(self) -> None:
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            destination = root / "skills-dest"
            agents_source = root / "agents-source"
            agents_destination = root / "agents-dest"
            self.create_skill(source, "alpha")
            agents_source.mkdir()
            reviewer_source = agents_source / "reviewer.toml"
            reviewer_source.write_text(AGENT_FILE_CONTENT, encoding="utf-8")
            (agents_source / "obsolete.toml").write_text(
                AGENT_FILE_CONTENT,
                encoding="utf-8",
            )
            install_args = [
                "--adapter",
                "codex",
                "--source",
                str(source),
                "--dest",
                str(destination),
                "--install-agents",
                "--agents-source",
                str(agents_source),
                "--agents-dest",
                str(agents_destination),
            ]
            with redirect_stdout(io.StringIO()):
                first_exit_code = installer.main(install_args)
            before_skills = self._tree_snapshot(destination)
            before_agents = self._tree_snapshot(agents_destination)
            (source / "alpha" / "SKILL.md").write_text(
                UPDATED_SKILL_FILE_CONTENT,
                encoding="utf-8",
            )
            reviewer_source.write_text(
                AGENT_FILE_CONTENT.replace("Review.", "Updated review."),
                encoding="utf-8",
            )
            (agents_source / "obsolete.toml").unlink()
            real_copy2 = installer.shutil.copy2

            def fail_source_agent_copy(
                source_path: Path,
                destination_path: Path,
                *args: object,
                **kwargs: object,
            ) -> Path:
                if Path(source_path).resolve() == reviewer_source.resolve():
                    raise OSError("injected agent copy failure")
                return real_copy2(source_path, destination_path, *args, **kwargs)

            error_output = io.StringIO()
            with patch.object(
                installer.shutil,
                "copy2",
                side_effect=fail_source_agent_copy,
            ), redirect_stdout(io.StringIO()), redirect_stderr(error_output):
                exit_code = installer.main(install_args + ["--replace"])

            self.assertEqual(installer.SUCCESS_EXIT_CODE, first_exit_code)
            self.assertEqual(installer.ERROR_EXIT_CODE, exit_code)
            self.assertEqual(before_skills, self._tree_snapshot(destination))
            self.assertEqual(before_agents, self._tree_snapshot(agents_destination))
            self.assertIn("injected agent copy failure", error_output.getvalue())

    def test_manifest_replacement_failure_preserves_complete_existing_installation(self) -> None:
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            destination = root / "skills-dest"
            self.create_skill(source, "alpha")
            self.create_skill(source, "obsolete", SECOND_SKILL_FILE_CONTENT)
            with redirect_stdout(io.StringIO()):
                first_exit_code = installer.main(
                    ["--source", str(source), "--dest", str(destination)]
                )
            before = self._tree_snapshot(destination)
            (source / "alpha" / "SKILL.md").write_text(
                UPDATED_SKILL_FILE_CONTENT,
                encoding="utf-8",
            )
            installer.shutil.rmtree(source / "obsolete")
            real_replace = installer.os.replace

            def fail_manifest_replace(source_path: Path, destination_path: Path) -> None:
                if Path(destination_path).name == installer.INSTALL_MANIFEST_FILE_NAME:
                    raise OSError("injected manifest replacement failure")
                real_replace(source_path, destination_path)

            error_output = io.StringIO()
            with patch.object(
                installer.os,
                "replace",
                side_effect=fail_manifest_replace,
            ), redirect_stdout(io.StringIO()), redirect_stderr(error_output):
                exit_code = installer.main(
                    [
                        "--source",
                        str(source),
                        "--dest",
                        str(destination),
                        "--replace",
                    ]
                )

            self.assertEqual(installer.SUCCESS_EXIT_CODE, first_exit_code)
            self.assertEqual(installer.ERROR_EXIT_CODE, exit_code)
            self.assertEqual(before, self._tree_snapshot(destination))
            self.assertIn(
                "injected manifest replacement failure",
                error_output.getvalue(),
            )

    def test_second_destination_swap_failure_rolls_back_first_destination(self) -> None:
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            destination = root / "skills-dest"
            agents_source = root / "agents-source"
            agents_destination = root / "agents-dest"
            self.create_skill(source, "alpha")
            agents_source.mkdir()
            reviewer_source = agents_source / "reviewer.toml"
            reviewer_source.write_text(AGENT_FILE_CONTENT, encoding="utf-8")
            install_args = [
                "--adapter",
                "codex",
                "--source",
                str(source),
                "--dest",
                str(destination),
                "--install-agents",
                "--agents-source",
                str(agents_source),
                "--agents-dest",
                str(agents_destination),
            ]
            with redirect_stdout(io.StringIO()):
                first_exit_code = installer.main(install_args)
            before_skills = self._tree_snapshot(destination)
            before_agents = self._tree_snapshot(agents_destination)
            (source / "alpha" / "SKILL.md").write_text(
                UPDATED_SKILL_FILE_CONTENT,
                encoding="utf-8",
            )
            reviewer_source.write_text(
                AGENT_FILE_CONTENT.replace("Review.", "Updated review."),
                encoding="utf-8",
            )
            real_replace = installer.os.replace
            swap_failed = False

            def fail_agent_destination_swap(
                source_path: Path,
                destination_path: Path,
            ) -> None:
                nonlocal swap_failed
                if (
                    not swap_failed
                    and Path(destination_path) == agents_destination.resolve()
                    and Path(source_path).is_dir()
                ):
                    swap_failed = True
                    raise OSError("injected destination swap failure")
                real_replace(source_path, destination_path)

            error_output = io.StringIO()
            with patch.object(
                installer.os,
                "replace",
                side_effect=fail_agent_destination_swap,
            ), redirect_stdout(io.StringIO()), redirect_stderr(error_output):
                exit_code = installer.main(install_args + ["--replace"])

            self.assertEqual(installer.SUCCESS_EXIT_CODE, first_exit_code)
            self.assertEqual(installer.ERROR_EXIT_CODE, exit_code)
            self.assertEqual(before_skills, self._tree_snapshot(destination))
            self.assertEqual(before_agents, self._tree_snapshot(agents_destination))
            self.assertIn("injected destination swap failure", error_output.getvalue())

    def test_keyboard_interrupt_after_backup_restores_the_original_destination(self) -> None:
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            destination = root / "skills-dest"
            self.create_skill(source, "alpha")
            with redirect_stdout(io.StringIO()):
                first_exit_code = installer.main(
                    ["--source", str(source), "--dest", str(destination)]
                )
            before = self._tree_snapshot(destination)
            (source / "alpha" / "SKILL.md").write_text(
                UPDATED_SKILL_FILE_CONTENT,
                encoding="utf-8",
            )
            real_replace = installer.os.replace
            interruption_raised = False

            def interrupt_staged_destination_swap(
                source_path: Path,
                destination_path: Path,
            ) -> None:
                nonlocal interruption_raised
                if (
                    not interruption_raised
                    and Path(source_path).name == "staged"
                    and Path(destination_path) == destination.resolve()
                ):
                    interruption_raised = True
                    raise KeyboardInterrupt("injected transaction interruption")
                real_replace(source_path, destination_path)

            with patch.object(
                installer.os,
                "replace",
                side_effect=interrupt_staged_destination_swap,
            ), redirect_stdout(io.StringIO()), self.assertRaisesRegex(
                KeyboardInterrupt,
                "injected transaction interruption",
            ):
                installer.main(
                    [
                        "--source",
                        str(source),
                        "--dest",
                        str(destination),
                        "--replace",
                    ]
                )

            self.assertEqual(installer.SUCCESS_EXIT_CODE, first_exit_code)
            self.assertEqual(before, self._tree_snapshot(destination))
            self.assertEqual(
                [],
                list(
                    destination.parent.glob(
                        f"{installer.INSTALL_MANIFEST_FILE_NAME}.skills-transaction-*"
                    )
                ),
            )

    def test_rollback_failure_preserves_backup_and_reports_recovery_location(self) -> None:
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            destination = root / "skills-dest"
            self.create_skill(source, "alpha")
            with redirect_stdout(io.StringIO()):
                first_exit_code = installer.main(
                    ["--source", str(source), "--dest", str(destination)]
                )
            before = self._tree_snapshot(destination)
            (source / "alpha" / "SKILL.md").write_text(
                UPDATED_SKILL_FILE_CONTENT,
                encoding="utf-8",
            )
            real_replace = installer.os.replace
            commit_failure_raised = False

            def fail_commit_and_rollback(
                source_path: Path,
                destination_path: Path,
            ) -> None:
                nonlocal commit_failure_raised
                source_name = Path(source_path).name
                if (
                    not commit_failure_raised
                    and source_name == "staged"
                    and Path(destination_path) == destination.resolve()
                ):
                    commit_failure_raised = True
                    raise OSError("injected staged destination failure")
                if (
                    commit_failure_raised
                    and source_name == "backup"
                    and Path(destination_path) == destination.resolve()
                ):
                    raise OSError("injected backup restore failure")
                real_replace(source_path, destination_path)

            error_output = io.StringIO()
            with patch.object(
                installer.os,
                "replace",
                side_effect=fail_commit_and_rollback,
            ), redirect_stdout(io.StringIO()), redirect_stderr(error_output):
                exit_code = installer.main(
                    [
                        "--source",
                        str(source),
                        "--dest",
                        str(destination),
                        "--replace",
                    ]
                )

            recovery_roots = list(
                destination.parent.glob(
                    f"{installer.INSTALL_MANIFEST_FILE_NAME}.skills-transaction-*"
                )
            )
            self.assertEqual(installer.SUCCESS_EXIT_CODE, first_exit_code)
            self.assertEqual(installer.ERROR_EXIT_CODE, exit_code)
            self.assertEqual(1, len(recovery_roots))
            self.assertEqual(before, self._tree_snapshot(recovery_roots[0] / "backup"))
            self.assertFalse(destination.exists())
            self.assertIn("injected staged destination failure", error_output.getvalue())
            self.assertIn("injected backup restore failure", error_output.getvalue())
            self.assertIn("manual recovery", error_output.getvalue().lower())
            self.assertIn(str(recovery_roots[0]), error_output.getvalue())


if __name__ == "__main__":
    unittest.main()
