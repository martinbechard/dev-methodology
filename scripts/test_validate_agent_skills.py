from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from types import ModuleType


VALIDATOR_PATH = Path(__file__).with_name("validate-agent-skills.py")


def load_validator() -> ModuleType:
    spec = importlib.util.spec_from_file_location("validate_agent_skills", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load validate-agent-skills.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ValidateAgentSkillsTests(unittest.TestCase):
    def create_skill(self, root: Path, name: str, frontmatter: str) -> Path:
        skill_dir = root / name
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(frontmatter + "\n\n# " + name.title() + "\n", encoding="utf-8")
        return skill_dir

    def test_accepts_agent_skill_frontmatter(self) -> None:
        validator = load_validator()

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill_dir = self.create_skill(
                root,
                "careful-coding",
                "---\nname: careful-coding\ndescription: Use when coding carefully.\n---",
            )

            findings = validator.validate_skill_paths([skill_dir])

        self.assertEqual([], findings)

    def test_rejects_okf_type_frontmatter(self) -> None:
        validator = load_validator()

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill_dir = self.create_skill(
                root,
                "careful-coding",
                "---\ntype: Skill\nname: careful-coding\ndescription: Use when coding carefully.\n---",
            )

            findings = validator.validate_skill_paths([skill_dir])

        self.assertEqual(1, len(findings))
        self.assertIn("unexpected frontmatter keys: type", findings[0].message)

    def test_accepts_source_side_openai_metadata(self) -> None:
        validator = load_validator()

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill_dir = self.create_skill(
                root,
                "careful-coding",
                "---\nname: careful-coding\ndescription: Use when coding carefully.\n---",
            )
            metadata = skill_dir / "agents" / "openai.yaml"
            metadata.parent.mkdir()
            metadata.write_text("interface:\n  display_name: Careful Coding\n", encoding="utf-8")

            findings = validator.validate_skill_paths([root])

        self.assertEqual([], findings)

    def test_rejects_invalid_openai_metadata_policy(self) -> None:
        validator = load_validator()

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill_dir = self.create_skill(
                root,
                "careful-coding",
                "---\nname: careful-coding\ndescription: Use when coding carefully.\n---",
            )
            metadata = skill_dir / "agents" / "openai.yaml"
            metadata.parent.mkdir()
            metadata.write_text(
                "policy:\n  allow_implicit_invocation: maybe\n",
                encoding="utf-8",
            )

            findings = validator.validate_skill_paths([root])

        self.assertEqual(1, len(findings))
        self.assertIn("policy allow_implicit_invocation must be a boolean", findings[0].message)

    def test_rejects_name_that_does_not_match_directory(self) -> None:
        validator = load_validator()

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill_dir = self.create_skill(
                root,
                "careful-coding",
                "---\nname: other-name\ndescription: Use when coding carefully.\n---",
            )

            findings = validator.validate_skill_paths([skill_dir])

        self.assertEqual(1, len(findings))
        self.assertIn("frontmatter name must match the skill directory name", findings[0].message)

    def test_cli_returns_success_for_valid_skill_root(self) -> None:
        validator = load_validator()

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.create_skill(
                root,
                "careful-coding",
                "---\nname: careful-coding\ndescription: Use when coding carefully.\n---",
            )

            exit_code = validator.main([str(root)])

        self.assertEqual(validator.SUCCESS_EXIT_CODE, exit_code)


if __name__ == "__main__":
    unittest.main()
