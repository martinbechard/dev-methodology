# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Builds canonical Model Judge requests and validates bound verdicts and calibration identities.
# Governing contract: evals/judge-prompt-v1.md and evals/judge-output-schema.yaml.

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Sequence

import yaml


ROOT = Path(__file__).resolve().parents[1]
PROMPT_PATH = ROOT / "evals" / "judge-prompt-v1.md"
OUTPUT_SCHEMA_PATH = ROOT / "evals" / "judge-output-schema.yaml"
CONTRACT_VERSION = "model-judge-v1"
SUPPORTED_HARNESSES = frozenset({"codex", "junie"})

_IDENTIFIER = re.compile(r"^[a-z0-9][a-z0-9._-]{0,127}$")
_DOCUMENT_KEYS = frozenset(
    {"id", "mediaType", "sha256", "byteLength", "content", "dataClassification"}
)
_OUTPUT_KEYS = frozenset(
    {
        "schema",
        "version",
        "contractVersion",
        "rubricId",
        "rubricSha256",
        "instructionEnvelopeSha256",
        "inputManifestSha256",
        "dimensionScores",
        "overall",
    }
)
_DIMENSION_SCORE_KEYS = frozenset(
    {"id", "score", "critical", "evidenceReferences", "rationale"}
)
_REFERENCE_KEYS = frozenset({"documentId", "locator"})
_SUPPORTED_PASS_RULES = frozenset(
    {
        "noAggregateCompensation",
        "minimumDimensionScore",
        "minimumDimensionScores",
        "criticalDimensions",
        "criticalCompletenessRequired",
        "readinessMustBeConsistent",
    }
)


class JudgeContractError(ValueError):
    """Report a contract, binding, or untrusted Model Judge output violation.

    Callers should treat this exception as a failed or unusable Judge result. It
    is raised before a verdict can be accepted and has no external side effects.
    """


@dataclass(frozen=True)
class JudgeRequest:
    """Hold the two message payloads and their immutable digest bindings.

    The instruction envelope is trusted evaluator configuration. The input
    manifest is a separate untrusted-data message containing candidate and
    evidence text. A caller sends them in those distinct roles and never
    concatenates the manifest into the instruction envelope.

    A typical caller builds an instance with build_judge_request, sends
    instruction_envelope_bytes as system or developer instructions, sends
    input_manifest_bytes as the user data message, and retains both digest
    fields with the Judge output.
    """

    instruction_envelope_bytes: bytes
    input_manifest_bytes: bytes
    prompt_sha256: str
    output_schema_sha256: str
    rubric_sha256: str
    instruction_envelope_sha256: str
    input_manifest_sha256: str


@dataclass(frozen=True)
class _RubricRules:
    dimension_ids: tuple[str, ...]
    critical_dimensions: frozenset[str]
    minimum_scores: Mapping[str, int]


def canonical_json_bytes(value: object) -> bytes:
    """Encode a JSON-compatible value into deterministic UTF-8 bytes.

    Args:
        value: A JSON-compatible value. Mapping keys must be strings and
            numeric values must be finite.

    Returns:
        Sorted, whitespace-free UTF-8 JSON bytes without a trailing newline.

    Raises:
        JudgeContractError: If the value cannot be represented as strict JSON.
    """

    _validate_json_value(value, "$", set())
    try:
        text = json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
    except (TypeError, ValueError) as error:
        raise JudgeContractError(f"value is not canonical JSON data: {error}") from error
    return text.encode("utf-8")


def build_judge_request(
    *,
    case_id: str,
    harness: str,
    rubric: Mapping[str, object],
    candidate_output: str,
    evidence: Mapping[str, str],
) -> JudgeRequest:
    """Build separate canonical instruction and untrusted-data payloads.

    Args:
        case_id: Stable lowercase evaluation case identifier.
        harness: Either codex or junie. Other harnesses are outside the current
            contract and are rejected.
        rubric: Trusted Model Judge rubric with a fixed 0 through 4 scale and
            explicit non-compensating pass rules.
        candidate_output: UTF-8 candidate text to evaluate as untrusted data.
        evidence: Non-empty mapping from stable document identifiers to UTF-8
            evidence text. Values are untrusted data, never instructions.

    Returns:
        A JudgeRequest with canonical payload bytes and SHA-256 bindings.

    Raises:
        JudgeContractError: If identifiers, harness, rubric, candidate text, or
            evidence cannot satisfy the version-one contract.
    """

    _require_identifier(case_id, "case id")
    _require_harness(harness)
    if not isinstance(candidate_output, str):
        raise JudgeContractError("candidate output must be UTF-8 text")
    if not isinstance(evidence, Mapping) or not evidence:
        raise JudgeContractError("evidence must be a non-empty document mapping")

    instruction_value = _instruction_envelope(rubric)
    instruction_bytes = canonical_json_bytes(instruction_value)
    instruction_digest = _sha256(instruction_bytes)

    evidence_documents: list[dict[str, object]] = []
    for document_id in sorted(evidence):
        _require_identifier(document_id, "evidence document id")
        if document_id == "candidate-output":
            raise JudgeContractError("evidence document id candidate-output is reserved")
        content = evidence[document_id]
        if not isinstance(content, str):
            raise JudgeContractError(f"evidence document {document_id} must be UTF-8 text")
        evidence_documents.append(_document(document_id, content))

    manifest_value: dict[str, object] = {
        "schema": "dev-methodology-model-judge-input-manifest",
        "version": 1,
        "contractVersion": CONTRACT_VERSION,
        "caseId": case_id,
        "harness": harness,
        "rubricId": str(rubric["id"]),
        "rubricSha256": _sha256(canonical_json_bytes(rubric)),
        "instructionEnvelopeSha256": instruction_digest,
        "dataBoundary": "untrusted-data-never-instructions",
        "candidateOutput": _document("candidate-output", candidate_output),
        "evidenceDocuments": evidence_documents,
    }
    manifest_bytes = canonical_json_bytes(manifest_value)
    request = JudgeRequest(
        instruction_envelope_bytes=instruction_bytes,
        input_manifest_bytes=manifest_bytes,
        prompt_sha256=str(instruction_value["judgePromptSha256"]),
        output_schema_sha256=str(instruction_value["judgeOutputSchemaSha256"]),
        rubric_sha256=_sha256(canonical_json_bytes(rubric)),
        instruction_envelope_sha256=instruction_digest,
        input_manifest_sha256=_sha256(manifest_bytes),
    )
    # Reuse the loader as an internal postcondition so builder and persisted
    # artifact validation cannot drift into separate contracts.
    loaded = load_judge_request(request.instruction_envelope_bytes, request.input_manifest_bytes)
    if loaded != request:
        raise JudgeContractError("built Judge request failed its canonical postcondition")
    return request


def load_judge_request(
    instruction_envelope_bytes: bytes,
    input_manifest_bytes: bytes,
) -> JudgeRequest:
    """Load and verify persisted canonical Judge request artifacts.

    Args:
        instruction_envelope_bytes: Trusted instruction artifact bytes produced
            by this contract version.
        input_manifest_bytes: Separate untrusted input-manifest bytes produced
            by this contract version.

    Returns:
        A JudgeRequest whose digests were recomputed from both canonical files.

    Raises:
        JudgeContractError: If either artifact is non-canonical, stale, altered,
            malformed, or bound to an unsupported harness or rubric.
    """

    instruction = _parse_canonical_json_object(
        instruction_envelope_bytes, "Judge instruction envelope"
    )
    manifest = _parse_canonical_json_object(input_manifest_bytes, "Judge input manifest")
    _validate_instruction_envelope(instruction)
    instruction_digest = _sha256(instruction_envelope_bytes)
    rubric = _mapping(instruction.get("rubric"), "instruction rubric")
    rubric_digest = _sha256(canonical_json_bytes(rubric))
    _validate_input_manifest(manifest, instruction_digest, str(rubric["id"]), rubric_digest)
    return JudgeRequest(
        instruction_envelope_bytes=instruction_envelope_bytes,
        input_manifest_bytes=input_manifest_bytes,
        prompt_sha256=str(instruction["judgePromptSha256"]),
        output_schema_sha256=str(instruction["judgeOutputSchemaSha256"]),
        rubric_sha256=rubric_digest,
        instruction_envelope_sha256=instruction_digest,
        input_manifest_sha256=_sha256(input_manifest_bytes),
    )


def validate_judge_output(
    output: Mapping[str, object],
    request: JudgeRequest,
) -> bytes:
    """Validate a Model Judge response and recompute its terminal result.

    Args:
        output: Parsed untrusted JSON object returned by the Model Judge.
        request: The exact request whose rubric, instructions, and evidence
            bindings govern the response.

    Returns:
        Canonical JSON bytes for the accepted response. The returned object has
        the same fields as the input because claimed verdict fields are checked
        against, rather than replaced by, independently recomputed values.

    Raises:
        JudgeContractError: If schema shape, bindings, fixed scores, critical
            flags, evidence references, or recomputed pass rules do not match.
    """

    canonical_request = load_judge_request(
        request.instruction_envelope_bytes,
        request.input_manifest_bytes,
    )
    if canonical_request != request:
        raise JudgeContractError("Judge request digest fields do not match its artifact bytes")
    if not isinstance(output, Mapping):
        raise JudgeContractError("Model Judge output must be a JSON object")
    _require_exact_keys(output, _OUTPUT_KEYS, "Model Judge output")
    if output.get("schema") != "dev-methodology-model-judge-output":
        raise JudgeContractError("Model Judge output schema identifier is invalid")
    if output.get("version") != 1 or output.get("contractVersion") != CONTRACT_VERSION:
        raise JudgeContractError("Model Judge output contract version is invalid")

    instruction = _parse_canonical_json_object(
        request.instruction_envelope_bytes, "Judge instruction envelope"
    )
    manifest = _parse_canonical_json_object(request.input_manifest_bytes, "Judge input manifest")
    rubric = _mapping(instruction.get("rubric"), "instruction rubric")
    rules = _validate_rubric(rubric)
    expected_bindings = {
        "rubricId": rubric["id"],
        "rubricSha256": request.rubric_sha256,
        "instructionEnvelopeSha256": request.instruction_envelope_sha256,
        "inputManifestSha256": request.input_manifest_sha256,
    }
    for field, expected in expected_bindings.items():
        if output.get(field) != expected:
            raise JudgeContractError(f"Model Judge output {field} binding is stale or invalid")

    documents = {"candidate-output"}
    evidence_documents = manifest.get("evidenceDocuments")
    if isinstance(evidence_documents, list):
        documents.update(
            str(document["id"])
            for document in evidence_documents
            if isinstance(document, Mapping) and "id" in document
        )
    score_values = output.get("dimensionScores")
    if not isinstance(score_values, list):
        raise JudgeContractError("Model Judge dimensionScores must be a list")
    observed_ids: list[str] = []
    scores: dict[str, int] = {}
    for index, value in enumerate(score_values):
        item = _mapping(value, f"Model Judge dimensionScores[{index}]")
        _require_exact_keys(item, _DIMENSION_SCORE_KEYS, f"dimension score {index}")
        dimension_id = item.get("id")
        if not isinstance(dimension_id, str):
            raise JudgeContractError(f"dimension score {index} id must be text")
        observed_ids.append(dimension_id)
        score = item.get("score")
        if not isinstance(score, int) or isinstance(score, bool) or not 0 <= score <= 4:
            raise JudgeContractError(
                f"Model Judge dimension score must be an integer from 0 through 4: {dimension_id}"
            )
        scores[dimension_id] = score
        expected_critical = dimension_id in rules.critical_dimensions
        if item.get("critical") is not expected_critical:
            raise JudgeContractError(
                f"Model Judge critical flag does not match the trusted rubric: {dimension_id}"
            )
        rationale = item.get("rationale")
        if not isinstance(rationale, str) or not rationale.strip():
            raise JudgeContractError(f"Model Judge rationale is required: {dimension_id}")
        _validate_evidence_references(
            item.get("evidenceReferences"), documents, dimension_id
        )

    if tuple(observed_ids) != rules.dimension_ids:
        raise JudgeContractError(
            "Model Judge dimension score ids and order must exactly match the trusted rubric"
        )
    dimension_pass = {
        dimension_id: score >= rules.minimum_scores[dimension_id]
        for dimension_id, score in scores.items()
    }
    recomputed_verdict = "pass" if all(dimension_pass.values()) else "fail"
    recomputed_critical = any(
        not dimension_pass[dimension_id]
        for dimension_id in rules.critical_dimensions
    )
    overall = _mapping(output.get("overall"), "Model Judge overall")
    _require_exact_keys(overall, {"verdict", "criticalFailure"}, "Model Judge overall")
    if overall.get("verdict") != recomputed_verdict:
        raise JudgeContractError(
            f"Model Judge claimed verdict does not match pass rules; recomputed verdict is {recomputed_verdict}"
        )
    if overall.get("criticalFailure") is not recomputed_critical:
        raise JudgeContractError(
            "Model Judge claimed criticalFailure does not match the trusted rubric"
        )
    return canonical_json_bytes(output)


def build_calibration_binding(
    *,
    rubric: Mapping[str, object],
    calibration_set: Sequence[object],
    harness: str,
    judge_model_identity: str,
    reasoning_profile: str,
) -> bytes:
    """Build the canonical identity that a calibration record must match.

    Args:
        rubric: Trusted rubric used for every labeled calibration example.
        calibration_set: Ordered labeled example objects. The full canonical set
            determines calibrationSetSha256 but is not copied into the binding.
        harness: Either codex or junie; calibrations are not portable across
            harnesses without a separate accepted record.
        judge_model_identity: Concrete provider and model-version identity.
        reasoning_profile: Concrete reasoning-effort or inference profile.

    Returns:
        Canonical JSON bytes binding prompt, output schema, rubric, calibration
        set, harness, model identity, and reasoning profile.

    Raises:
        JudgeContractError: If any governed input is empty, unsupported,
            malformed, or not representable as canonical JSON.
    """

    _require_harness(harness)
    _validate_rubric(rubric)
    if isinstance(calibration_set, (str, bytes)) or not isinstance(calibration_set, Sequence):
        raise JudgeContractError("calibration set must be a non-empty sequence")
    if not calibration_set:
        raise JudgeContractError("calibration set must be a non-empty sequence")
    model_identity = _require_non_empty_text(judge_model_identity, "Judge model identity")
    reasoning = _require_non_empty_text(reasoning_profile, "reasoning profile")
    instruction = _instruction_envelope(rubric)
    value = {
        "schema": "dev-methodology-model-judge-calibration-binding",
        "version": 1,
        "contractVersion": CONTRACT_VERSION,
        "harness": harness,
        "rubricId": rubric["id"],
        "judgePromptSha256": instruction["judgePromptSha256"],
        "judgeOutputSchemaSha256": instruction["judgeOutputSchemaSha256"],
        "rubricSha256": instruction["rubricSha256"],
        "instructionEnvelopeSha256": _sha256(canonical_json_bytes(instruction)),
        "calibrationSetSha256": _sha256(canonical_json_bytes(list(calibration_set))),
        "judgeModelIdentity": model_identity,
        "reasoningProfile": reasoning,
    }
    return canonical_json_bytes(value)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the standalone request builder, output validator, or binding builder.

    Args:
        argv: Optional argument sequence excluding the executable name. When
            omitted, command-line arguments from the current process are used.

    Returns:
        Zero on success and two when an artifact or contract validation fails.
        Argument-parser usage errors retain argparse's standard SystemExit.

    Side effects:
        The build command creates its output directory and writes two canonical
        JSON artifacts. Other commands write canonical JSON only to standard
        output. Validation failures write a concise error to standard error.
    """

    parser = _argument_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "build":
            rubric = _load_rubric(args.rubric_file, args.rubric_id)
            evidence = _read_evidence_assignments(args.evidence)
            request = build_judge_request(
                case_id=args.case_id,
                harness=args.harness,
                rubric=rubric,
                candidate_output=args.candidate_output.read_text(encoding="utf-8"),
                evidence=evidence,
            )
            args.output_dir.mkdir(parents=True, exist_ok=True)
            instruction_path = args.output_dir / "judge-instructions-v1.json"
            manifest_path = args.output_dir / "judge-input-manifest-v1.json"
            instruction_path.write_bytes(request.instruction_envelope_bytes)
            manifest_path.write_bytes(request.input_manifest_bytes)
            summary = {
                "instructionEnvelope": str(instruction_path),
                "instructionEnvelopeSha256": request.instruction_envelope_sha256,
                "inputManifest": str(manifest_path),
                "inputManifestSha256": request.input_manifest_sha256,
            }
            print(canonical_json_bytes(summary).decode("utf-8"))
            return 0
        if args.command == "validate":
            request = load_judge_request(
                args.instructions.read_bytes(),
                args.manifest.read_bytes(),
            )
            output = json.loads(args.judge_output.read_text(encoding="utf-8"))
            if not isinstance(output, Mapping):
                raise JudgeContractError("Model Judge output must be a JSON object")
            print(validate_judge_output(output, request).decode("utf-8"))
            return 0
        if args.command == "calibration-binding":
            rubric = _load_rubric(args.rubric_file, args.rubric_id)
            calibration_set = yaml.safe_load(args.calibration_set.read_text(encoding="utf-8"))
            if not isinstance(calibration_set, list):
                raise JudgeContractError("calibration set file must contain a list")
            print(
                build_calibration_binding(
                    rubric=rubric,
                    calibration_set=calibration_set,
                    harness=args.harness,
                    judge_model_identity=args.judge_model_identity,
                    reasoning_profile=args.reasoning_profile,
                ).decode("utf-8")
            )
            return 0
    except (JudgeContractError, OSError, UnicodeError, json.JSONDecodeError, yaml.YAMLError) as error:
        print(f"FAIL {error}", file=sys.stderr)
        return 2
    raise JudgeContractError(f"unsupported command: {args.command}")


def _argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build and validate canonical Codex and Junie Model Judge artifacts."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    build = subparsers.add_parser("build", help="Build trusted instructions and an untrusted manifest.")
    _add_rubric_arguments(build)
    build.add_argument("--case-id", required=True)
    build.add_argument("--harness", required=True, choices=sorted(SUPPORTED_HARNESSES))
    build.add_argument("--candidate-output", required=True, type=Path)
    build.add_argument(
        "--evidence",
        action="append",
        default=[],
        metavar="DOCUMENT_ID=PATH",
        help="Add one untrusted evidence document; repeat for multiple documents.",
    )
    build.add_argument("--output-dir", required=True, type=Path)

    validate = subparsers.add_parser("validate", help="Validate one bound Model Judge JSON output.")
    validate.add_argument("--instructions", required=True, type=Path)
    validate.add_argument("--manifest", required=True, type=Path)
    validate.add_argument("--judge-output", required=True, type=Path)

    calibration = subparsers.add_parser(
        "calibration-binding",
        help="Build the governed digest identity for one calibration set.",
    )
    _add_rubric_arguments(calibration)
    calibration.add_argument("--calibration-set", required=True, type=Path)
    calibration.add_argument("--harness", required=True, choices=sorted(SUPPORTED_HARNESSES))
    calibration.add_argument("--judge-model-identity", required=True)
    calibration.add_argument("--reasoning-profile", required=True)
    return parser


def _add_rubric_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--rubric-file", required=True, type=Path)
    parser.add_argument("--rubric-id", required=True)


def _load_rubric(path: Path, rubric_id: str) -> Mapping[str, object]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if isinstance(value, Mapping) and value.get("id") == rubric_id:
        return value
    rubrics = value.get("rubrics") if isinstance(value, Mapping) else None
    if isinstance(rubrics, list):
        for rubric in rubrics:
            if isinstance(rubric, Mapping) and rubric.get("id") == rubric_id:
                return rubric
    raise JudgeContractError(f"rubric file does not define rubric id: {rubric_id}")


def _read_evidence_assignments(assignments: Sequence[str]) -> dict[str, str]:
    evidence: dict[str, str] = {}
    for assignment in assignments:
        document_id, separator, raw_path = assignment.partition("=")
        if not separator or not raw_path:
            raise JudgeContractError(
                f"evidence assignment must use DOCUMENT_ID=PATH: {assignment}"
            )
        if document_id in evidence:
            raise JudgeContractError(f"duplicate evidence document id: {document_id}")
        evidence[document_id] = Path(raw_path).read_text(encoding="utf-8")
    return evidence


def _instruction_envelope(rubric: Mapping[str, object]) -> dict[str, object]:
    _validate_rubric(rubric)
    prompt_bytes = _canonical_prompt_bytes()
    schema = _load_output_schema()
    return {
        "schema": "dev-methodology-model-judge-instruction-envelope",
        "version": 1,
        "contractVersion": CONTRACT_VERSION,
        "judgePrompt": prompt_bytes.decode("utf-8"),
        "judgePromptSha256": _sha256(prompt_bytes),
        "outputSchema": schema,
        "judgeOutputSchemaSha256": _sha256(canonical_json_bytes(schema)),
        "rubric": rubric,
        "rubricSha256": _sha256(canonical_json_bytes(rubric)),
        "responseFormat": "single-json-object",
    }


def _validate_instruction_envelope(value: Mapping[str, object]) -> None:
    expected_keys = {
        "schema",
        "version",
        "contractVersion",
        "judgePrompt",
        "judgePromptSha256",
        "outputSchema",
        "judgeOutputSchemaSha256",
        "rubric",
        "rubricSha256",
        "responseFormat",
    }
    _require_exact_keys(value, expected_keys, "Judge instruction envelope")
    if value.get("schema") != "dev-methodology-model-judge-instruction-envelope":
        raise JudgeContractError("Judge instruction envelope schema identifier is invalid")
    if value.get("version") != 1 or value.get("contractVersion") != CONTRACT_VERSION:
        raise JudgeContractError("Judge instruction envelope contract version is invalid")
    prompt_bytes = _canonical_prompt_bytes()
    if value.get("judgePrompt") != prompt_bytes.decode("utf-8"):
        raise JudgeContractError("Judge instruction envelope prompt does not match the governed prompt")
    if value.get("judgePromptSha256") != _sha256(prompt_bytes):
        raise JudgeContractError("Judge instruction envelope prompt digest is invalid")
    schema = _mapping(value.get("outputSchema"), "Judge output schema")
    expected_schema = _load_output_schema()
    if canonical_json_bytes(schema) != canonical_json_bytes(expected_schema):
        raise JudgeContractError("Judge instruction envelope output schema is stale")
    if value.get("judgeOutputSchemaSha256") != _sha256(canonical_json_bytes(schema)):
        raise JudgeContractError("Judge instruction envelope output schema digest is invalid")
    rubric = _mapping(value.get("rubric"), "Judge instruction rubric")
    _validate_rubric(rubric)
    if value.get("rubricSha256") != _sha256(canonical_json_bytes(rubric)):
        raise JudgeContractError("Judge instruction envelope rubric digest is invalid")
    if value.get("responseFormat") != "single-json-object":
        raise JudgeContractError("Judge instruction response format is invalid")


def _validate_input_manifest(
    manifest: Mapping[str, object],
    instruction_digest: str,
    rubric_id: str,
    rubric_digest: str,
) -> None:
    expected_keys = {
        "schema",
        "version",
        "contractVersion",
        "caseId",
        "harness",
        "rubricId",
        "rubricSha256",
        "instructionEnvelopeSha256",
        "dataBoundary",
        "candidateOutput",
        "evidenceDocuments",
    }
    _require_exact_keys(manifest, expected_keys, "Judge input manifest")
    if manifest.get("schema") != "dev-methodology-model-judge-input-manifest":
        raise JudgeContractError("Judge input manifest schema identifier is invalid")
    if manifest.get("version") != 1 or manifest.get("contractVersion") != CONTRACT_VERSION:
        raise JudgeContractError("Judge input manifest contract version is invalid")
    case_id = manifest.get("caseId")
    if not isinstance(case_id, str):
        raise JudgeContractError("Judge input manifest caseId must be text")
    _require_identifier(case_id, "case id")
    harness = manifest.get("harness")
    if not isinstance(harness, str):
        raise JudgeContractError("Judge input manifest harness must be text")
    _require_harness(harness)
    expected_bindings = {
        "rubricId": rubric_id,
        "rubricSha256": rubric_digest,
        "instructionEnvelopeSha256": instruction_digest,
        "dataBoundary": "untrusted-data-never-instructions",
    }
    for field, expected in expected_bindings.items():
        if manifest.get(field) != expected:
            raise JudgeContractError(f"Judge input manifest {field} binding is invalid")
    candidate = _mapping(manifest.get("candidateOutput"), "candidate output document")
    _validate_document(candidate, expected_id="candidate-output")
    evidence = manifest.get("evidenceDocuments")
    if not isinstance(evidence, list) or not evidence:
        raise JudgeContractError("Judge input manifest evidenceDocuments must be non-empty")
    ids: list[str] = []
    for index, value in enumerate(evidence):
        document = _mapping(value, f"evidence document {index}")
        document_id = _validate_document(document)
        if document_id == "candidate-output":
            raise JudgeContractError("evidence document id candidate-output is reserved")
        ids.append(document_id)
    if ids != sorted(ids) or len(ids) != len(set(ids)):
        raise JudgeContractError("evidence documents must have unique ids in canonical order")


def _document(document_id: str, content: str) -> dict[str, object]:
    content_bytes = content.encode("utf-8")
    return {
        "id": document_id,
        "mediaType": "text/plain; charset=utf-8",
        "sha256": _sha256(content_bytes),
        "byteLength": len(content_bytes),
        "content": content,
        "dataClassification": "untrusted-data",
    }


def _validate_document(document: Mapping[str, object], expected_id: str | None = None) -> str:
    _require_exact_keys(document, _DOCUMENT_KEYS, "manifest document")
    document_id = document.get("id")
    if not isinstance(document_id, str):
        raise JudgeContractError("manifest document id must be text")
    _require_identifier(document_id, "manifest document id")
    if expected_id is not None and document_id != expected_id:
        raise JudgeContractError(f"manifest document id must be {expected_id}")
    if document.get("mediaType") != "text/plain; charset=utf-8":
        raise JudgeContractError(f"manifest document media type is invalid: {document_id}")
    if document.get("dataClassification") != "untrusted-data":
        raise JudgeContractError(f"manifest document must remain untrusted data: {document_id}")
    content = document.get("content")
    if not isinstance(content, str):
        raise JudgeContractError(f"manifest document content must be UTF-8 text: {document_id}")
    content_bytes = content.encode("utf-8")
    if document.get("byteLength") != len(content_bytes):
        raise JudgeContractError(f"manifest document byte length is invalid: {document_id}")
    if document.get("sha256") != _sha256(content_bytes):
        raise JudgeContractError(f"manifest document digest is invalid: {document_id}")
    return document_id


def _validate_rubric(rubric: Mapping[str, object]) -> _RubricRules:
    if not isinstance(rubric, Mapping):
        raise JudgeContractError("Model Judge rubric must be a mapping")
    rubric_id = rubric.get("id")
    if not isinstance(rubric_id, str):
        raise JudgeContractError("Model Judge rubric id must be text")
    _require_identifier(rubric_id, "rubric id")
    if rubric.get("type") not in (None, "model"):
        raise JudgeContractError(f"rubric {rubric_id} must use Model Judge type")
    if rubric.get("scale") not in (None, "0-to-4-per-dimension"):
        raise JudgeContractError(f"rubric {rubric_id} must use the fixed 0 through 4 scale")
    dimensions = rubric.get("dimensions")
    if not isinstance(dimensions, list) or not dimensions:
        raise JudgeContractError(f"rubric {rubric_id} dimensions must be non-empty")
    dimension_ids: list[str] = []
    critical: set[str] = set()
    for index, value in enumerate(dimensions):
        if isinstance(value, str):
            dimension_id = value
        elif isinstance(value, Mapping):
            dimension_value = value.get("id")
            if not isinstance(dimension_value, str):
                raise JudgeContractError(f"rubric {rubric_id} dimension {index} must identify an id")
            dimension_id = dimension_value
            critical_value = value.get("critical", False)
            if not isinstance(critical_value, bool):
                raise JudgeContractError(
                    f"rubric {rubric_id} dimension critical flag must be boolean: {dimension_id}"
                )
            if critical_value:
                critical.add(dimension_id)
        else:
            raise JudgeContractError(f"rubric {rubric_id} dimension {index} is invalid")
        _require_identifier(dimension_id, "rubric dimension id")
        if dimension_id in dimension_ids:
            raise JudgeContractError(f"rubric {rubric_id} repeats dimension: {dimension_id}")
        dimension_ids.append(dimension_id)

    rules = _mapping(rubric.get("passRules"), f"rubric {rubric_id} passRules")
    unknown = sorted(set(rules) - _SUPPORTED_PASS_RULES)
    if unknown:
        raise JudgeContractError(
            f"rubric {rubric_id} uses unsupported pass rules: {', '.join(unknown)}"
        )
    if rules.get("noAggregateCompensation") is not True:
        raise JudgeContractError(
            f"rubric {rubric_id} must forbid aggregate score compensation"
        )
    minimum = rules.get("minimumDimensionScore")
    if not isinstance(minimum, int) or isinstance(minimum, bool) or not 0 <= minimum <= 4:
        raise JudgeContractError(
            f"rubric {rubric_id} minimumDimensionScore must be an integer from 0 through 4"
        )
    minimum_scores = {dimension_id: minimum for dimension_id in dimension_ids}
    declared_minimums = rules.get("minimumDimensionScores", {})
    if not isinstance(declared_minimums, Mapping):
        raise JudgeContractError(f"rubric {rubric_id} minimumDimensionScores must be a mapping")
    for dimension_id, dimension_minimum in declared_minimums.items():
        if not isinstance(dimension_id, str) or dimension_id not in dimension_ids:
            raise JudgeContractError(f"rubric {rubric_id} minimum score names an unknown dimension")
        if (
            not isinstance(dimension_minimum, int)
            or isinstance(dimension_minimum, bool)
            or not 0 <= dimension_minimum <= 4
        ):
            raise JudgeContractError(
                f"rubric {rubric_id} minimum score must be an integer from 0 through 4"
            )
        minimum_scores[dimension_id] = dimension_minimum
    declared_critical = rules.get("criticalDimensions", [])
    if not isinstance(declared_critical, list) or not all(
        isinstance(value, str) for value in declared_critical
    ):
        raise JudgeContractError(f"rubric {rubric_id} criticalDimensions must be a list")
    critical.update(str(value) for value in declared_critical)

    for flag, dimension_id in (
        ("criticalCompletenessRequired", "completeness"),
        ("readinessMustBeConsistent", "readiness"),
    ):
        if flag not in rules:
            continue
        enabled = rules[flag]
        if not isinstance(enabled, bool):
            raise JudgeContractError(f"rubric {rubric_id} {flag} must be boolean")
        if enabled:
            if dimension_id not in dimension_ids:
                raise JudgeContractError(
                    f"rubric {rubric_id} {flag} requires dimension {dimension_id}"
                )
            critical.add(dimension_id)

    unknown_critical = sorted(critical - set(dimension_ids))
    if unknown_critical:
        raise JudgeContractError(
            f"rubric {rubric_id} marks unknown critical dimensions: {', '.join(unknown_critical)}"
        )
    return _RubricRules(
        dimension_ids=tuple(dimension_ids),
        critical_dimensions=frozenset(critical),
        minimum_scores=minimum_scores,
    )


def _validate_evidence_references(
    value: object,
    document_ids: set[str],
    dimension_id: str,
) -> None:
    if not isinstance(value, list) or not value:
        raise JudgeContractError(f"Model Judge evidence references are required: {dimension_id}")
    observed: set[tuple[str, str]] = set()
    for index, raw_reference in enumerate(value):
        reference = _mapping(
            raw_reference,
            f"Model Judge evidence reference {dimension_id}[{index}]",
        )
        _require_exact_keys(reference, _REFERENCE_KEYS, "Model Judge evidence reference")
        document_id = reference.get("documentId")
        locator = reference.get("locator")
        if not isinstance(document_id, str) or document_id not in document_ids:
            raise JudgeContractError(
                f"Model Judge evidence reference names an unknown document: {document_id}"
            )
        if not isinstance(locator, str) or not locator.strip():
            raise JudgeContractError(
                f"Model Judge evidence reference locator is required: {dimension_id}"
            )
        identity = (document_id, locator)
        if identity in observed:
            raise JudgeContractError(
                f"Model Judge evidence reference is duplicated: {dimension_id}"
            )
        observed.add(identity)


def _load_output_schema() -> Mapping[str, object]:
    value = yaml.safe_load(OUTPUT_SCHEMA_PATH.read_text(encoding="utf-8"))
    schema = _mapping(value, "Judge output schema")
    if schema.get("schema") != "dev-methodology-model-judge-output-schema":
        raise JudgeContractError("Judge output schema identifier is invalid")
    if schema.get("version") != 1 or schema.get("contractVersion") != CONTRACT_VERSION:
        raise JudgeContractError("Judge output schema contract version is invalid")
    return schema


def _canonical_prompt_bytes() -> bytes:
    text = PROMPT_PATH.read_text(encoding="utf-8")
    normalized = text.replace("\r\n", "\n").replace("\r", "\n").rstrip("\n") + "\n"
    return normalized.encode("utf-8")


def _parse_canonical_json_object(value: bytes, label: str) -> Mapping[str, object]:
    try:
        parsed = json.loads(value.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as error:
        raise JudgeContractError(f"{label} must be UTF-8 canonical JSON: {error}") from error
    mapping = _mapping(parsed, label)
    if canonical_json_bytes(mapping) != value:
        raise JudgeContractError(f"{label} bytes are not canonical")
    return mapping


def _mapping(value: object, label: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise JudgeContractError(f"{label} must be a mapping")
    if not all(isinstance(key, str) for key in value):
        raise JudgeContractError(f"{label} keys must be strings")
    return value


def _validate_json_value(value: object, path: str, active: set[int]) -> None:
    if value is None or isinstance(value, (str, bool, int)):
        return
    if isinstance(value, float):
        if not math.isfinite(value):
            raise JudgeContractError(f"canonical JSON number must be finite: {path}")
        return
    if isinstance(value, Mapping):
        identity = id(value)
        if identity in active:
            raise JudgeContractError(f"canonical JSON data contains a cycle: {path}")
        active.add(identity)
        for key, child in value.items():
            if not isinstance(key, str):
                raise JudgeContractError(f"canonical JSON mapping key must be text: {path}")
            _validate_json_value(child, f"{path}.{key}", active)
        active.remove(identity)
        return
    if isinstance(value, list):
        identity = id(value)
        if identity in active:
            raise JudgeContractError(f"canonical JSON data contains a cycle: {path}")
        active.add(identity)
        for index, child in enumerate(value):
            _validate_json_value(child, f"{path}[{index}]", active)
        active.remove(identity)
        return
    raise JudgeContractError(f"value is not canonical JSON data at {path}")


def _require_exact_keys(value: Mapping[str, object], expected: set[str] | frozenset[str], label: str) -> None:
    missing = sorted(set(expected) - set(value))
    extra = sorted(set(value) - set(expected))
    if missing or extra:
        details: list[str] = []
        if missing:
            details.append(f"missing {', '.join(missing)}")
        if extra:
            details.append(f"unexpected {', '.join(extra)}")
        raise JudgeContractError(f"{label} fields are invalid: {'; '.join(details)}")


def _require_identifier(value: str, label: str) -> None:
    if not _IDENTIFIER.fullmatch(value):
        raise JudgeContractError(
            f"{label} must use lowercase letters, digits, dots, underscores, or hyphens"
        )


def _require_harness(harness: str) -> None:
    if harness not in SUPPORTED_HARNESSES:
        raise JudgeContractError(
            f"supported harness must be codex or junie, received: {harness}"
        )


def _require_non_empty_text(value: str, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise JudgeContractError(f"{label} must be non-empty text")
    return value.strip()


def _sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
