from __future__ import annotations

import importlib.util
import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout
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

    def create_manifest(self, destination: Path, skill_names: list[str]) -> None:
        manifest = {
            "schema_version": MANIFEST_SCHEMA_VERSION,
            "bundle_id": BUNDLE_ID,
            "adapter": "generic",
            "source": "test-source",
            "artifacts": [
                {
                    "type": SKILL_ARTIFACT_TYPE,
                    "name": skill_name,
                    "path": skill_name,
                }
                for skill_name in skill_names
            ],
        }
        destination.mkdir(parents=True, exist_ok=True)
        (destination / ".dev-methodology-install.json").write_text(
            json.dumps(manifest, sort_keys=True),
            encoding="utf-8",
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

    def test_adapter_default_destinations_use_agent_claude_and_junie_homes(self) -> None:
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            agents_home = root / "agent-home"
            claude_home = root / "claude-home"
            user_home = root / "user-home"
            environment = {
                "AGENTS_HOME": str(agents_home),
                "CLAUDE_HOME": str(claude_home),
                "HOME": str(user_home),
            }

            with patch.dict(os.environ, environment, clear=True):
                self.assertEqual(agents_home / "skills", installer.default_destination("generic"))
                self.assertEqual(agents_home / "skills", installer.default_destination("codex"))
                self.assertEqual(agents_home / "skills", installer.default_destination("gemini"))
                self.assertEqual(claude_home / "skills", installer.default_destination("claude"))
                self.assertEqual(user_home / ".junie" / "skills", installer.default_destination("junie"))

    def test_dest_overrides_adapter_default(self) -> None:
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

    def test_prune_owned_removes_deleted_skill_but_preserves_unowned_skill(self) -> None:
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
                        "--prune-owned",
                    ]
                )

            self.assertEqual(exit_code, installer.SUCCESS_EXIT_CODE)
            self.assertFalse((destination / "obsolete").exists())
            self.assertTrue((destination / "local-only" / "SKILL.md").is_file())
            self.assertEqual(["alpha"], self.read_manifest_skill_names(destination))
            self.assertIn("pruned obsolete obsolete", output.getvalue())

    def test_prune_owned_bootstraps_manifest_without_deleting_unknown_destination(self) -> None:
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
                        "--prune-owned",
                    ]
                )

            self.assertEqual(exit_code, installer.SUCCESS_EXIT_CODE)
            self.assertTrue((destination / "legacy" / "SKILL.md").is_file())
            self.assertEqual(["alpha"], self.read_manifest_skill_names(destination))
            self.assertIn("prune skipped; no ownership manifest", output.getvalue())

    def test_dry_run_prune_owned_reports_without_deleting_or_rewriting_manifest(self) -> None:
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
                        "--prune-owned",
                        "--dry-run",
                    ]
                )

            self.assertEqual(exit_code, installer.SUCCESS_EXIT_CODE)
            self.assertTrue((destination / "obsolete" / "SKILL.md").is_file())
            self.assertEqual(
                before_manifest,
                (destination / ".dev-methodology-install.json").read_text(encoding="utf-8"),
            )
            self.assertIn("would prune obsolete obsolete", output.getvalue())


if __name__ == "__main__":
    unittest.main()
