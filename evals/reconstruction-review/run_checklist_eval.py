#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Scores repeated checklist-review results against a sealed reconstruction corpus.
# Governing design: skills/documentation-reverse-engineer/SKILL.md
# Governing test plan: scripts/test_reconstruction_review_eval.py

"""Validate and compare candidate and reference reconstruction checklist reviews."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from statistics import median
from typing import Mapping, Sequence


__all__ = ("EvaluationError", "evaluate_results", "load_corpus", "main")


class EvaluationError(RuntimeError):
    """Report an invalid corpus, invocation record, or comparison contract.

    Evaluation callers catch this error at the CLI or orchestration boundary and preserve its
    message as a failed evidence result. For example, load_corpus raises EvaluationError when a
    referenced artifact digest differs from corpus.json; no partial score is returned.
    """


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _canonical_digest(payload: object) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _load_object(path: Path, label: str) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or not payload:
        raise EvaluationError(f"{label} must contain a non-empty JSON object")
    return payload


def _required_string(payload: Mapping[str, object], key: str, label: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        raise EvaluationError(f"{label} {key} must be a non-empty string")
    return value


def _resolve_corpus_file(corpus_root: Path, value: object, label: str) -> Path:
    if not isinstance(value, str) or not value:
        raise EvaluationError(f"{label} path must be a non-empty string")
    relative_path = Path(value)
    if relative_path.is_absolute() or ".." in relative_path.parts:
        raise EvaluationError(f"{label} path must stay inside the corpus: {value}")
    path = corpus_root / relative_path
    if path.is_symlink() or not path.is_file():
        raise EvaluationError(f"{label} file is missing or symbolic: {value}")
    return path


def load_corpus(path: Path) -> dict[str, object]:
    """Load and validate one immutable checklist evaluation corpus.

    path identifies corpus.json. The function verifies schema, referenced artifact and
    adjudication bytes, stable case identity inputs, checklist questions, and the corpus ID
    derived from source baseline, artifact digest, checklist version, and adjudicated defect
    set. It returns the validated corpus payload with no filesystem mutation. Invalid JSON,
    paths, digests, or identity data raise EvaluationError or preserve the owning I/O error.
    """
    path = path.expanduser().resolve(strict=True)
    corpus_root = path.parent
    corpus = _load_object(path, "Corpus")
    if corpus.get("schemaVersion") != 1:
        raise EvaluationError("Corpus schemaVersion must be 1")
    policy = corpus.get("promotionPolicy")
    if not isinstance(policy, dict) or policy.get("minimumRunsPerReviewer") != 3:
        raise EvaluationError("Corpus promotion policy must require three runs per reviewer")
    cases = corpus.get("cases")
    if not isinstance(cases, list) or not cases:
        raise EvaluationError("Corpus cases must be a non-empty list")

    case_ids: set[str] = set()
    identity_rows: list[dict[str, str]] = []
    for raw_case in cases:
        if not isinstance(raw_case, dict):
            raise EvaluationError("Corpus case must be an object")
        case_id = _required_string(raw_case, "id", "Corpus case")
        if case_id in case_ids:
            raise EvaluationError(f"Duplicate corpus case ID: {case_id}")
        case_ids.add(case_id)
        source_baseline = _required_string(raw_case, "sourceBaseline", f"Case {case_id}")
        checklist_version = _required_string(raw_case, "checklistVersion", f"Case {case_id}")
        for prefix in ("artifact", "checklist", "sourceEvidence", "adjudication"):
            file_path = _resolve_corpus_file(
                corpus_root,
                raw_case.get(f"{prefix}Path"),
                f"Case {case_id} {prefix}",
            )
            expected_digest = _required_string(
                raw_case,
                f"{prefix}Sha256",
                f"Case {case_id}",
            )
            if _sha256(file_path) != expected_digest:
                raise EvaluationError(f"Case {case_id} {prefix} digest mismatch")
        checklist = _load_object(
            _resolve_corpus_file(corpus_root, raw_case["checklistPath"], "Checklist"),
            f"Case {case_id} checklist",
        )
        questions = checklist.get("questions")
        if not isinstance(questions, list) or not questions:
            raise EvaluationError(f"Case {case_id} checklist has no questions")
        question_ids = [
            _required_string(question, "id", f"Case {case_id} checklist question")
            if isinstance(question, dict)
            else ""
            for question in questions
        ]
        if "" in question_ids or len(question_ids) != len(set(question_ids)):
            raise EvaluationError(f"Case {case_id} checklist question IDs are invalid")
        if checklist.get("version") != checklist_version:
            raise EvaluationError(f"Case {case_id} checklist version mismatch")
        adjudication = _load_object(
            _resolve_corpus_file(corpus_root, raw_case["adjudicationPath"], "Adjudication"),
            f"Case {case_id} adjudication",
        )
        defects = adjudication.get("defects")
        if not isinstance(defects, list) or not defects:
            raise EvaluationError(f"Case {case_id} adjudication has no defects")
        defect_ids = [
            _required_string(defect, "id", f"Case {case_id} adjudicated defect")
            if isinstance(defect, dict)
            else ""
            for defect in defects
        ]
        if "" in defect_ids or len(defect_ids) != len(set(defect_ids)):
            raise EvaluationError(f"Case {case_id} adjudicated defect IDs are invalid")
        identity_rows.append(
            {
                "adjudicatedDefectSetSha256": str(raw_case["adjudicationSha256"]),
                "artifactSha256": str(raw_case["artifactSha256"]),
                "checklistVersion": checklist_version,
                "sourceBaseline": source_baseline,
            }
        )
    if corpus.get("corpusId") != _canonical_digest(identity_rows):
        raise EvaluationError("Corpus ID does not match its sealed identity inputs")
    return corpus


def _load_results(path: Path, reviewer_class: str) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for line_number, line in enumerate(
        path.expanduser().resolve(strict=True).read_text(encoding="utf-8").splitlines(),
        start=1,
    ):
        if not line.strip():
            continue
        record = json.loads(line)
        if not isinstance(record, dict) or not record:
            raise EvaluationError(f"{reviewer_class} result line {line_number} is invalid")
        if record.get("reviewerClass") != reviewer_class:
            raise EvaluationError(
                f"{reviewer_class} result line {line_number} has the wrong reviewerClass"
            )
        records.append(record)
    if not records:
        raise EvaluationError(f"{reviewer_class} results are empty")
    return records


def _score_reviewer(
    reviewer_class: str,
    records: Sequence[Mapping[str, object]],
    corpus: Mapping[str, object],
) -> dict[str, object]:
    cases = {
        str(case["id"]): case
        for case in corpus["cases"]
        if isinstance(case, dict)
    }
    corpus_root = Path(str(corpus["_corpusRoot"]))
    minimum_runs = int(corpus["promotionPolicy"]["minimumRunsPerReviewer"])
    runs_by_case: dict[str, list[Mapping[str, object]]] = {case_id: [] for case_id in cases}
    model_profiles: set[str] = set()
    invocation_ids: set[str] = set()
    scored_runs: list[dict[str, object]] = []
    for record in records:
        case_id = _required_string(record, "caseId", f"{reviewer_class} result")
        if case_id not in cases:
            raise EvaluationError(f"{reviewer_class} result has unknown caseId: {case_id}")
        if record.get("corpusId") != corpus.get("corpusId"):
            raise EvaluationError(f"{reviewer_class} result is bound to another corpus")
        case = cases[case_id]
        for result_key, case_key in (
            ("artifactSha256", "artifactSha256"),
            ("checklistVersion", "checklistVersion"),
            ("adjudicationSha256", "adjudicationSha256"),
        ):
            if record.get(result_key) != case.get(case_key):
                raise EvaluationError(
                    f"{reviewer_class} result {case_id} used different evaluation inputs"
                )
        invocation_id = _required_string(record, "invocationId", f"{reviewer_class} result")
        if invocation_id in invocation_ids:
            raise EvaluationError(f"Duplicate {reviewer_class} invocationId: {invocation_id}")
        invocation_ids.add(invocation_id)
        model_profiles.add(_required_string(record, "modelProfile", f"{reviewer_class} result"))
        elapsed_seconds = record.get("elapsedSeconds")
        input_tokens = record.get("inputTokens")
        output_tokens = record.get("outputTokens")
        if not isinstance(elapsed_seconds, (int, float)) or elapsed_seconds <= 0:
            raise EvaluationError(f"{reviewer_class} result elapsedSeconds must be positive")
        if not isinstance(input_tokens, int) or input_tokens < 0:
            raise EvaluationError(f"{reviewer_class} result inputTokens must be non-negative")
        if not isinstance(output_tokens, int) or output_tokens < 0:
            raise EvaluationError(f"{reviewer_class} result outputTokens must be non-negative")
        if input_tokens + output_tokens == 0:
            raise EvaluationError(f"{reviewer_class} result must record nonzero model tokens")
        if "costValue" in record:
            if not isinstance(record["costValue"], (int, float)) or record["costValue"] < 0:
                raise EvaluationError(f"{reviewer_class} result costValue is invalid")
            _required_string(record, "costCurrency", f"{reviewer_class} result")
        elif record.get("costStatus") != "UNAVAILABLE":
            raise EvaluationError(
                f"{reviewer_class} result must record costValue or costStatus UNAVAILABLE"
            )

        checklist = _load_object(
            corpus_root / str(case["checklistPath"]),
            f"Case {case_id} checklist",
        )
        adjudication = _load_object(
            corpus_root / str(case["adjudicationPath"]),
            f"Case {case_id} adjudication",
        )
        question_ids = {str(question["id"]) for question in checklist["questions"]}
        defect_ids = {str(defect["id"]) for defect in adjudication["defects"]}
        blocking_ids = {
            str(defect["id"])
            for defect in adjudication["defects"]
            if defect.get("blocking") is True
        }
        reported_ids = record.get("reportedDefectIds")
        answered_ids = record.get("answeredQuestionIds")
        citations = record.get("citations")
        if not isinstance(reported_ids, list) or not all(isinstance(value, str) for value in reported_ids):
            raise EvaluationError(f"{reviewer_class} result reportedDefectIds is invalid")
        if not isinstance(answered_ids, list) or not all(isinstance(value, str) for value in answered_ids):
            raise EvaluationError(f"{reviewer_class} result answeredQuestionIds is invalid")
        if not isinstance(citations, list):
            raise EvaluationError(f"{reviewer_class} result citations must be a list")
        citation_question_ids: set[str] = set()
        for citation in citations:
            if not isinstance(citation, dict):
                raise EvaluationError(f"{reviewer_class} result citation must be an object")
            citation_question_ids.add(
                _required_string(citation, "questionId", f"{reviewer_class} citation")
            )
            _required_string(citation, "sourcePath", f"{reviewer_class} citation")
            _required_string(citation, "quote", f"{reviewer_class} citation")
        reported_set = set(reported_ids)
        answered_set = set(answered_ids)
        scored_runs.append(
            {
                "blockingRecall": (
                    len(blocking_ids & reported_set) / len(blocking_ids)
                    if blocking_ids
                    else 1.0
                ),
                "checklistCompleteness": len(question_ids & answered_set) / len(question_ids),
                "citationCompleteness": len(question_ids & citation_question_ids) / len(question_ids),
                "costValue": record.get("costValue"),
                "defectRecall": len(defect_ids & reported_set) / len(defect_ids),
                "elapsedSeconds": float(elapsed_seconds),
                "falsePositives": len(reported_set - defect_ids),
                "tokenCount": input_tokens + output_tokens,
            }
        )
        runs_by_case[case_id].append(record)
    if len(model_profiles) != 1:
        raise EvaluationError(f"{reviewer_class} results must use one model profile")
    for case_id, case_runs in runs_by_case.items():
        if len(case_runs) < minimum_runs:
            raise EvaluationError(
                f"{reviewer_class} case {case_id} has fewer than {minimum_runs} runs"
            )
    available_costs = [
        float(run["costValue"])
        for run in scored_runs
        if run["costValue"] is not None
    ]
    return {
        "allBlockingDefectsFound": all(run["blockingRecall"] == 1.0 for run in scored_runs),
        "allChecklistQuestionsAnswered": all(
            run["checklistCompleteness"] == 1.0 for run in scored_runs
        ),
        "allVerdictsCited": all(run["citationCompleteness"] == 1.0 for run in scored_runs),
        "medianCost": median(available_costs) if available_costs else None,
        "medianDefectRecall": median(run["defectRecall"] for run in scored_runs),
        "medianElapsedSeconds": median(run["elapsedSeconds"] for run in scored_runs),
        "medianFalsePositives": median(run["falsePositives"] for run in scored_runs),
        "medianTokenCount": median(run["tokenCount"] for run in scored_runs),
        "modelProfile": next(iter(model_profiles)),
        "runCount": len(scored_runs),
    }


def evaluate_results(
    corpus_path: Path,
    candidate_results_path: Path,
    reference_results_path: Path,
) -> dict[str, object]:
    """Evaluate repeated candidate and reference reviews under one sealed corpus.

    The three paths identify the immutable corpus and separately captured JSONL invocation
    records. Every invocation must bind to identical artifact, checklist, and adjudication
    inputs. The function derives recall, false positives, checklist and citation completeness,
    elapsed time, token use, and available cost, then applies the corpus promotion policy. It
    returns PROMOTE only when all quality gates pass and median time or tokens improve by at
    least twenty percent without increasing the other measure. It never invokes a model or
    writes a result file. Invalid evidence raises EvaluationError or the owning parse/I/O error.
    """
    corpus = load_corpus(corpus_path)
    corpus["_corpusRoot"] = str(corpus_path.expanduser().resolve(strict=True).parent)
    candidate = _score_reviewer(
        "candidate",
        _load_results(candidate_results_path, "candidate"),
        corpus,
    )
    reference = _score_reviewer(
        "reference",
        _load_results(reference_results_path, "reference"),
        corpus,
    )
    quality_pass = bool(
        candidate["allBlockingDefectsFound"]
        and candidate["allChecklistQuestionsAnswered"]
        and candidate["allVerdictsCited"]
    )
    false_positive_pass = (
        candidate["medianFalsePositives"] <= reference["medianFalsePositives"]
    )
    time_ratio = candidate["medianElapsedSeconds"] / reference["medianElapsedSeconds"]
    token_ratio = candidate["medianTokenCount"] / reference["medianTokenCount"]
    efficiency_pass = (time_ratio <= 0.8 and token_ratio <= 1.0) or (
        token_ratio <= 0.8 and time_ratio <= 1.0
    )
    promote = quality_pass and false_positive_pass and efficiency_pass
    return {
        "candidate": candidate,
        "corpusId": corpus["corpusId"],
        "gates": {
            "efficiency": efficiency_pass,
            "falsePositives": false_positive_pass,
            "quality": quality_pass,
            "timeRatio": time_ratio,
            "tokenRatio": token_ratio,
        },
        "recommendation": "PROMOTE" if promote else "RETAIN_REFERENCE",
        "reference": reference,
        "schemaVersion": 1,
    }


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compare repeated checklist-review results without invoking a model."
    )
    parser.add_argument("--corpus", required=True, type=Path)
    parser.add_argument("--candidate-results", required=True, type=Path)
    parser.add_argument("--reference-results", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run checklist evaluation and return a process exit status.

    argv contains optional command arguments and defaults to process arguments. Success prints
    the derived comparison as JSON and optionally writes the same bytes to the explicit output
    path. Invalid corpus or invocation evidence is written to standard error and returns one.
    The recommendation is evidence, not an automatic model-routing mutation.
    """
    arguments = _build_parser().parse_args(argv)
    try:
        result = evaluate_results(
            arguments.corpus,
            arguments.candidate_results,
            arguments.reference_results,
        )
    except (EvaluationError, json.JSONDecodeError, OSError, ZeroDivisionError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    output = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if arguments.output is not None:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(output, encoding="utf-8")
    print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
