# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies workflow skills respect optional project-selected resource coordination.

from __future__ import annotations

from pathlib import Path
import unittest


_ROOT = Path(__file__).resolve().parents[1]
_WORKFLOWS = {
    "integrate-agent-work": ("integration", "Final Report"),
    "deliver-work-item-feature-branch": ("publication", "Results"),
    "deliver-work-item-main-branch": ("integration", "Result"),
    "verify-end-to-end-workflow": (
        "verification",
        "Evidence Handoff And Commit Authority",
    ),
}
_COORDINATION_START = (
    "Applicable project instructions own resource-coordination selection. "
    "They load the selected procedure, if any."
)
_UNSCOPED_NONE_END = "Do not discover, acquire, heartbeat, or release claims."
_SCOPED_NONE_END = (
    "In that none-selected case, do not discover, acquire, heartbeat, or release "
    "claims."
)
_LOADED_RESULT_EVIDENCE = (
    "Include coordination evidence only when the loaded procedure requires it."
)
_NONE_RESULT_OMISSION = (
    "In the none-selected case, omit claim-specific fields, placeholders, and "
    "not-applicable results."
)


def _normalized(text: str) -> str:
    """Return Markdown prose with formatting whitespace collapsed."""

    return " ".join(text.split())


def _section(text: str, heading: str) -> str:
    """Return one level-two Markdown section by heading."""

    marker = f"## {heading}"
    if marker not in text:
        raise AssertionError(f"missing section: {marker}")
    return text.split(marker, 1)[1].split("\n## ", 1)[0]


def _without_coordination_contract(text: str) -> str:
    """Return normalized skill text with its coordination contract removed."""

    normalized = _normalized(text)
    start = normalized.find(_COORDINATION_START)
    if start < 0:
        raise AssertionError("missing resource-coordination contract start")
    for end_marker in (_SCOPED_NONE_END, _UNSCOPED_NONE_END):
        end = normalized.find(end_marker, start)
        if end >= 0:
            outside_contract = normalized[:start] + normalized[end + len(end_marker) :]
            return outside_contract.replace(_NONE_RESULT_OMISSION, "")
    raise AssertionError("missing resource-coordination contract end")


class OptionalResourceCoordinationWorkflowSkillTests(unittest.TestCase):
    """Protect both configured coordination selections across workflow skills."""

    def test_resource_claim_context_applies_contract_and_reports_evidence(self) -> None:
        """Require enabled procedures to own operations and downstream evidence."""

        for skill_name, (event, handoff_heading) in _WORKFLOWS.items():
            skill_path = _ROOT / "skills" / skill_name / "SKILL.md"
            skill_text = skill_path.read_text(encoding="utf-8")
            normalized = _normalized(skill_text)
            handoff = _normalized(_section(skill_text, handoff_heading))
            with self.subTest(skill=skill_name):
                self.assertIn(_COORDINATION_START, normalized)
                self.assertIn(
                    "Apply the loaded resource-coordination procedure when its event "
                    f"contract requires protection during {event}.",
                    normalized,
                )
                self.assertIn(
                    "Preserve the complete behavior and evidence that the loaded "
                    "procedure requires.",
                    normalized,
                )
                self.assertIn(_LOADED_RESULT_EVIDENCE, handoff)

    def test_none_context_scopes_operations_and_omits_claim_evidence(self) -> None:
        """Require none-selected workflows to omit all claim work and result fields."""

        for skill_name, (_, handoff_heading) in _WORKFLOWS.items():
            skill_path = _ROOT / "skills" / skill_name / "SKILL.md"
            skill_text = skill_path.read_text(encoding="utf-8")
            normalized = _normalized(skill_text)
            handoff = _normalized(_section(skill_text, handoff_heading))
            with self.subTest(skill=skill_name):
                self.assertIn(
                    "When applicable project instructions select none and load no "
                    "resource-coordination procedure, perform no claim procedure and "
                    "no claim-specific evidence handling.",
                    normalized,
                )
                self.assertIn(_SCOPED_NONE_END, normalized)
                self.assertIn(_NONE_RESULT_OMISSION, handoff)

    def test_none_context_has_no_claim_obligation_outside_its_contract(self) -> None:
        """Reject claim-specific operations or evidence anywhere else in a workflow."""

        for skill_name in _WORKFLOWS:
            skill_path = _ROOT / "skills" / skill_name / "SKILL.md"
            outside_contract = _without_coordination_contract(
                skill_path.read_text(encoding="utf-8")
            )
            with self.subTest(skill=skill_name):
                self.assertNotRegex(outside_contract, r"(?i)\bclaims?(?:-specific)?\b")


if __name__ == "__main__":
    unittest.main()
