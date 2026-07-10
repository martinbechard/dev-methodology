from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path
from types import ModuleType


SCRIPT_PATH = Path(__file__).with_name("refresh-shared-skills.py")
EXPECTED_DEFAULT_TARGET_COUNT = 3
EXPECTED_FILTERED_TARGET_COUNT = 1
EXPECTED_FAILED_TARGET_COUNT = 1
FIRST_COMMAND_INDEX = 0
SECOND_COMMAND_INDEX = 1
THIRD_COMMAND_INDEX = 2
ADAPTER_ARGUMENT_START_INDEX = 2
ADAPTER_ARGUMENT_END_INDEX = 4


def load_refresh_script() -> ModuleType:
    spec = importlib.util.spec_from_file_location("refresh_shared_skills", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load refresh-shared-skills.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class RefreshSharedSkillsTests(unittest.TestCase):
    def test_default_run_refreshes_all_shared_targets(self) -> None:
        refresh_script = load_refresh_script()
        commands: list[list[str]] = []

        def capture_runner(command: list[str]) -> int:
            commands.append(command)
            return refresh_script.SUCCESS_EXIT_CODE

        exit_code = refresh_script.main(["--dry-run"], runner=capture_runner)

        self.assertEqual(refresh_script.SUCCESS_EXIT_CODE, exit_code)
        self.assertEqual(EXPECTED_DEFAULT_TARGET_COUNT, len(commands))
        self.assertIn("--dry-run", commands[FIRST_COMMAND_INDEX])
        for command in commands:
            with self.subTest(command=command):
                self.assertIn("--prune-owned", command)
        self.assertNotIn("--install-agents", commands[FIRST_COMMAND_INDEX])
        self.assertIn("--install-agents", commands[SECOND_COMMAND_INDEX])
        self.assertIn("--install-agents", commands[THIRD_COMMAND_INDEX])
        self.assertEqual(
            ["--adapter", "codex"],
            commands[FIRST_COMMAND_INDEX][ADAPTER_ARGUMENT_START_INDEX:ADAPTER_ARGUMENT_END_INDEX],
        )
        self.assertEqual(
            ["--adapter", "codex"],
            commands[SECOND_COMMAND_INDEX][ADAPTER_ARGUMENT_START_INDEX:ADAPTER_ARGUMENT_END_INDEX],
        )
        self.assertIn(str(Path.home() / ".codex" / "skills"), commands[SECOND_COMMAND_INDEX])
        self.assertEqual(
            ["--adapter", "claude"],
            commands[THIRD_COMMAND_INDEX][ADAPTER_ARGUMENT_START_INDEX:ADAPTER_ARGUMENT_END_INDEX],
        )

    def test_target_filter_refreshes_only_selected_target(self) -> None:
        refresh_script = load_refresh_script()
        commands: list[list[str]] = []

        def capture_runner(command: list[str]) -> int:
            commands.append(command)
            return refresh_script.SUCCESS_EXIT_CODE

        exit_code = refresh_script.main(["--target", "claude", "--dry-run"], runner=capture_runner)

        self.assertEqual(refresh_script.SUCCESS_EXIT_CODE, exit_code)
        self.assertEqual(EXPECTED_FILTERED_TARGET_COUNT, len(commands))
        self.assertEqual(
            ["--adapter", "claude"],
            commands[FIRST_COMMAND_INDEX][ADAPTER_ARGUMENT_START_INDEX:ADAPTER_ARGUMENT_END_INDEX],
        )

    def test_stops_on_failed_refresh(self) -> None:
        refresh_script = load_refresh_script()
        commands: list[list[str]] = []

        def failing_runner(command: list[str]) -> int:
            commands.append(command)
            return refresh_script.ERROR_EXIT_CODE

        exit_code = refresh_script.main(["--dry-run"], runner=failing_runner)

        self.assertEqual(refresh_script.ERROR_EXIT_CODE, exit_code)
        self.assertEqual(EXPECTED_FAILED_TARGET_COUNT, len(commands))


if __name__ == "__main__":
    unittest.main()
