from __future__ import annotations

import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from types import ModuleType

import yaml


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "run-agent-skill-evals.py"


def load_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location("run_agent_skill_evals", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load evaluation runner")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class AgentSkillEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_module()
        cls.case = cls.module.load_cases()["typescript-order-pricing"]

    def receipt(self) -> dict[str, object]:
        return {
            "schema": "dev-methodology-eval-evidence",
            "version": 1,
            "case": "typescript-order-pricing",
            "verdict": "verified",
            "captureProvenance": {
                "kind": "human-attested-harness-export",
                "reference": "attestation.json#capture",
            },
            "agent": {
                "id": "coding-agent",
                "harness": "codex",
                "model": "test-model",
                "invocationEvidence": "events.jsonl#invocation",
            },
            "skills": [
                {
                    "id": skill,
                    "contentDigest": digest(ROOT / "skills" / skill / "SKILL.md"),
                    "readEvidence": [{"type": "tool-call", "reference": f"events.jsonl#read-{skill}"}],
                }
                for skill in self.case["requiredSkills"]
            ],
            "behaviorAssertions": [
                {"id": assertion, "verdict": "passed", "evidence": f"assertions.json#{assertion}"}
                for assertion in self.case["requiredEvidence"]
            ],
            "commands": [
                {"command": "npm test", "exitCode": 0, "expectation": "success", "evidence": "commands.log#test"}
            ],
            "independentVerifier": {"kind": "deterministic", "reference": "verifier.json#verdict"},
        }

    def validate(self, receipt: dict[str, object]) -> list[str]:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "evidence.yaml"
            events = [{
                "id": "invocation",
                "type": "invocation",
                "agent": receipt["agent"]["id"],
                "harness": receipt["agent"]["harness"],
                "model": receipt["agent"]["model"],
            }]
            events.extend({
                "id": f"read-{skill}",
                "type": "tool-call",
                "skill": skill,
                "contentDigest": digest(ROOT / "skills" / skill / "SKILL.md"),
            } for skill in self.case["requiredSkills"])
            references = ["test", "verdict"]
            references.extend(str(assertion) for assertion in self.case["requiredEvidence"])
            (root / "events.jsonl").write_text("\n".join(json.dumps(event) for event in events) + "\n", encoding="utf-8")
            (root / "assertions.json").write_text("\n".join(references) + "\n", encoding="utf-8")
            (root / "commands.log").write_text("test\n", encoding="utf-8")
            (root / "verifier.json").write_text("verdict\n", encoding="utf-8")
            (root / "attestation.json").write_text("capture\n", encoding="utf-8")
            path.write_text(yaml.safe_dump(receipt), encoding="utf-8")
            return self.module.validate_evidence(self.case, path)

    def test_complete_receipt_is_accepted(self) -> None:
        self.assertEqual([], self.validate(self.receipt()))

    def test_declared_agent_is_not_enough_without_matching_identity(self) -> None:
        receipt = self.receipt()
        receipt["agent"]["id"] = "code-review-agent"
        self.assertIn("evidence agent id does not match a required agent", self.validate(receipt))

    def test_skill_claim_is_not_enough_without_tool_call_evidence(self) -> None:
        receipt = self.receipt()
        receipt["skills"][0]["readEvidence"] = []
        errors = self.validate(receipt)
        self.assertTrue(any("missing skill read tool evidence" in error for error in errors))

    def test_skill_digest_must_match_the_loaded_source(self) -> None:
        receipt = self.receipt()
        receipt["skills"][0]["contentDigest"] = "wrong"
        errors = self.validate(receipt)
        self.assertTrue(any("skill digest mismatch" in error for error in errors))

    def test_reference_claim_is_not_enough_without_a_captured_artifact(self) -> None:
        receipt = self.receipt()
        receipt["agent"]["invocationEvidence"] = "missing.jsonl#invocation"
        errors = self.validate(receipt)
        self.assertTrue(any("reference target is missing" in error for error in errors))

    def test_plain_marker_is_not_accepted_as_a_harness_event(self) -> None:
        receipt = self.receipt()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "events.jsonl").write_text("invocation\n", encoding="utf-8")
            path = root / "evidence.yaml"
            path.write_text(yaml.safe_dump(receipt), encoding="utf-8")
            errors = self.module.validate_evidence(self.case, path)
        self.assertTrue(any("JSON harness event" in error for error in errors))

    def test_unattested_capture_is_not_accepted(self) -> None:
        receipt = self.receipt()
        receipt.pop("captureProvenance")
        errors = self.validate(receipt)
        self.assertIn("evidence captureProvenance must be a mapping", errors)

    def test_every_behavior_assertion_needs_independent_evidence(self) -> None:
        receipt = self.receipt()
        receipt["behaviorAssertions"][0]["evidence"] = ""
        errors = self.validate(receipt)
        self.assertTrue(any("behavior assertion lacks passed evidence" in error for error in errors))

    def test_read_only_case_requires_unchanged_hash(self) -> None:
        case = self.module.load_cases()["typescript-code-review"]
        receipt = self.receipt()
        receipt["case"] = case["id"]
        receipt["agent"]["id"] = "code-review-agent"
        receipt["skills"] = [
            {
                "id": skill,
                "contentDigest": digest(ROOT / "skills" / skill / "SKILL.md"),
                "readEvidence": [{"type": "tool-call", "reference": f"events.jsonl#read-{skill}"}],
            }
            for skill in case["requiredSkills"]
        ]
        receipt["behaviorAssertions"] = [
            {"id": assertion, "verdict": "passed", "evidence": f"assertions.json#{assertion}"}
            for assertion in case["requiredEvidence"]
        ]
        receipt["findings"] = [
            {"id": finding, "evidence": f"review.md#{finding}"}
            for finding in case["requiredFindings"]
        ]
        receipt["projectHashBefore"] = "before"
        receipt["projectHashAfter"] = "after"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "evidence.yaml"
            path.write_text(yaml.safe_dump(receipt), encoding="utf-8")
            errors = self.module.validate_evidence(case, path)
        self.assertIn("read-only evaluation changed the project hash", errors)


if __name__ == "__main__":
    unittest.main()
