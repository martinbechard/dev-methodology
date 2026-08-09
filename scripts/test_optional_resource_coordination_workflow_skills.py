# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies workflow skills respect optional project-selected resource coordination.

from __future__ import annotations

from pathlib import Path
import unittest


_ROOT = Path(__file__).resolve().parents[1]
_WORKFLOWS = {
    "integrate-agent-work": "integration",
    "deliver-work-item-feature-branch": "publication",
    "deliver-work-item-main-branch": "integration",
    "verify-end-to-end-workflow": "verification",
}
_CURRENT_UNCONDITIONAL_PHRASES = (
    "Follow the Claim Events table in resource-claim during integration.",
    "Follow the Claim Events table in resource-claim during publication.",
    "Apply resource-claim when verification triggers a claim event.",
)


class OptionalResourceCoordinationWorkflowSkillTests(unittest.TestCase):
    """Protect both configured coordination selections across workflow skills."""

    def test_workflows_follow_each_project_selected_coordination_mode(self) -> None:
        """Require complete loaded-procedure behavior and no procedure for none."""

        for skill_name, event in _WORKFLOWS.items():
            skill_path = _ROOT / "skills" / skill_name / "SKILL.md"
            normalized = " ".join(skill_path.read_text(encoding="utf-8").split())

            for selection in ("resource-claim", "none"):
                with self.subTest(skill=skill_name, selection=selection):
                    self.assertIn(
                        "Applicable project instructions own resource-coordination "
                        "selection. They load the selected procedure, if any.",
                        normalized,
                    )
                    if selection == "resource-claim":
                        self.assertIn(
                            "Apply the loaded resource-coordination procedure when its "
                            f"event contract requires protection during {event}.",
                            normalized,
                        )
                        self.assertIn(
                            "Preserve the complete behavior and evidence that the loaded "
                            "procedure requires.",
                            normalized,
                        )
                    else:
                        self.assertIn(
                            "When applicable project instructions select none and load no "
                            "resource-coordination procedure, perform no claim procedure "
                            "and no claim-specific evidence handling.",
                            normalized,
                        )
                        self.assertIn(
                            "Do not discover, acquire, heartbeat, or release claims.",
                            normalized,
                        )

    def test_workflows_reject_unconditional_resource_claim_instructions(self) -> None:
        """Reject the exact hard-coded instructions that bypass project selection."""

        for skill_name in _WORKFLOWS:
            skill_path = _ROOT / "skills" / skill_name / "SKILL.md"
            skill_text = skill_path.read_text(encoding="utf-8")
            for phrase in _CURRENT_UNCONDITIONAL_PHRASES:
                with self.subTest(skill=skill_name, phrase=phrase):
                    self.assertNotIn(phrase, skill_text)


if __name__ == "__main__":
    unittest.main()
