from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path
from types import ModuleType

import yaml

SCRIPT_PATH = Path(__file__).with_name("openai_metadata.py")
SKILL_FILE_CONTENT = """---
name: careful-coding
description: Use when making focused, verified code changes.
---

# Careful Coding
"""
EXISTING_METADATA = """interface:
  display_name: Old Name
  short_description: Old description
  default_prompt: Keep this custom prompt.
policy:
  allow_implicit_invocation: false
dependencies:
  tools:
    - type: mcp
      value: docs
"""


def load_script() -> ModuleType:
    spec = importlib.util.spec_from_file_location("openai_metadata", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load openai_metadata.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class OpenAiMetadataTests(unittest.TestCase):
    def create_skill(self, root: Path) -> Path:
        skill = root / "careful-coding"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text(SKILL_FILE_CONTENT, encoding="utf-8")
        return skill

    def test_sync_updates_derived_fields_and_preserves_manual_sections(self) -> None:
        script = load_script()
        with tempfile.TemporaryDirectory() as temp_dir:
            skill = self.create_skill(Path(temp_dir))
            metadata = skill / "agents" / "openai.yaml"
            metadata.parent.mkdir()
            metadata.write_text(EXISTING_METADATA, encoding="utf-8")
            exit_code = script.main([str(skill)])
            parsed = yaml.safe_load(metadata.read_text(encoding="utf-8"))
        self.assertEqual(script.SUCCESS_EXIT_CODE, exit_code)
        self.assertEqual("Careful Coding", parsed["interface"]["display_name"])
        self.assertEqual("Use when making focused, verified code changes.", parsed["interface"]["short_description"])
        self.assertEqual("Keep this custom prompt.", parsed["interface"]["default_prompt"])
        self.assertFalse(parsed["policy"]["allow_implicit_invocation"])
        self.assertEqual("docs", parsed["dependencies"]["tools"][0]["value"])

    def test_check_reports_stale_metadata_without_rewriting(self) -> None:
        script = load_script()
        with tempfile.TemporaryDirectory() as temp_dir:
            skill = self.create_skill(Path(temp_dir))
            metadata = skill / "agents" / "openai.yaml"
            metadata.parent.mkdir()
            metadata.write_text(EXISTING_METADATA, encoding="utf-8")
            original = metadata.read_text(encoding="utf-8")
            exit_code = script.main([str(skill), "--check"])
            self.assertEqual(original, metadata.read_text(encoding="utf-8"))
        self.assertEqual(script.ERROR_EXIT_CODE, exit_code)


if __name__ == "__main__":
    unittest.main()
