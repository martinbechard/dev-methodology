# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Orders Deterministic and Model Judges and validates calibrated Model Judge records.

from __future__ import annotations

import hashlib
import json
from collections import Counter
from dataclasses import dataclass
from typing import Callable, Mapping, Sequence


JUDGE_TYPES = frozenset({"Deterministic Judge", "Model Judge", "Human Judge"})
_CALIBRATION_DIGEST_FIELDS = (
    "judgePromptSha256",
    "judgeOutputSchemaSha256",
    "instructionEnvelopeSha256",
    "harness",
    "judgeModelIdentity",
    "reasoningProfile",
    "rubricSha256",
    "calibrationSetSha256",
)
_REQUIRED_SAMPLE_CLASSES = frozenset({
    "clear-pass",
    "clear-fail",
    "boundary",
    "incomplete-plausible",
    "adversarially-polished",
})
_MINIMUM_CALIBRATION_EXAMPLES = 25
_MINIMUM_EXAMPLES_PER_CLASS = 5
_MINIMUM_FAILED_EXAMPLES = 2
_MINIMUM_CRITICAL_DEFECTS = 5
_ORDERED_SCORE_MINIMUM = 0
_ORDERED_SCORE_MAXIMUM = 4


@dataclass(frozen=True)
class JudgeResult:
    """Represent one Judge verdict and its independently inspectable evidence reference."""

    judge: str
    verdict: str
    evidence: str
    check_id: str = ""
    critical: bool = True


@dataclass(frozen=True)
class JudgePipelineResult:
    """Report ordered Judge results and whether Model Judge execution was skipped."""

    deterministic_results: tuple[JudgeResult, ...]
    model_result: JudgeResult | None
    model_status: str


def run_judge_pipeline(
    deterministic_judges: Sequence[Callable[[], JudgeResult]],
    model_judge: Callable[[], JudgeResult] | None,
) -> JudgePipelineResult:
    """Run Deterministic Judges first and skip the Model Judge after a deterministic failure."""

    deterministic_results: list[JudgeResult] = []
    for judge in deterministic_judges:
        result = judge()
        deterministic_results.append(result)
    if any(result.critical and result.verdict != "passed" for result in deterministic_results):
        return JudgePipelineResult(
            deterministic_results=tuple(deterministic_results),
            model_result=None,
            model_status="skipped-deterministic-failure",
        )
    if model_judge is None:
        return JudgePipelineResult(tuple(deterministic_results), None, "not-required")
    model_result = model_judge()
    return JudgePipelineResult(tuple(deterministic_results), model_result, model_result.verdict)


def calibration_record_digest(record: Mapping[str, object]) -> str:
    """Digest calibration evidence while excluding its self-referential recordDigest field."""

    payload = {key: value for key, value in record.items() if key != "recordDigest"}
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def calibration_set_digest(samples: Sequence[object]) -> str:
    """Digest the canonical labeled calibration set independently from metrics and status."""

    encoded = json.dumps(samples, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def validate_calibration_record(
    record: Mapping[str, object],
    expected_digests: Mapping[str, str],
    *,
    minimum_binary_f1: float = 0.85,
    minimum_weighted_kappa: float = 0.70,
) -> list[str]:
    """Validate Model Judge calibration quality and invalidate any changed governed digest."""

    errors: list[str] = []
    if record.get("status") != "accepted":
        errors.append("Model Judge calibration status must be accepted")
    if not isinstance(record.get("rubricId"), str) or not record.get("rubricId"):
        errors.append("Model Judge calibration rubricId must be a non-empty string")
    elif expected_digests.get("rubricId") is not None and record.get("rubricId") != expected_digests.get("rubricId"):
        errors.append("Model Judge calibration rubricId is stale")
    if record.get("harness") not in {"codex", "junie"}:
        errors.append("Model Judge calibration harness must be codex or junie")
    for field in _CALIBRATION_DIGEST_FIELDS:
        expected = expected_digests.get(field)
        if not isinstance(expected, str) or not expected:
            errors.append(f"Model Judge calibration expected {field} is missing")
        elif record.get(field) != expected:
            errors.append(f"Model Judge calibration {field} is stale")
    actual_record_digest = record.get("recordDigest")
    if actual_record_digest != calibration_record_digest(record):
        errors.append("Model Judge calibration recordDigest does not match its content")
    metrics = record.get("metrics")
    if not isinstance(metrics, Mapping):
        return errors + ["Model Judge calibration metrics must be a mapping"]
    samples = record.get("samples")
    if not isinstance(samples, list):
        return errors + ["Model Judge calibration samples must be a list"]
    if record.get("calibrationSetSha256") != calibration_set_digest(samples):
        errors.append("Model Judge calibration calibrationSetSha256 does not match samples")
    try:
        computed_metrics = compute_calibration_metrics(samples)
    except ValueError as error:
        return errors + [f"Model Judge calibration samples are invalid: {error}"]
    for field, computed in computed_metrics.items():
        supplied = metrics.get(field)
        if not isinstance(supplied, (int, float)) or abs(float(supplied) - float(computed)) > 1e-9:
            errors.append(f"Model Judge calibration metric does not match samples: {field}")
    binary_f1 = metrics.get("binaryF1")
    weighted_kappa = metrics.get("weightedKappa")
    critical_recall = metrics.get("criticalDefectRecall")
    if not isinstance(binary_f1, (int, float)) or binary_f1 < minimum_binary_f1:
        errors.append(f"Model Judge calibration binaryF1 must be at least {minimum_binary_f1}")
    if not isinstance(weighted_kappa, (int, float)) or weighted_kappa < minimum_weighted_kappa:
        errors.append(f"Model Judge calibration weightedKappa must be at least {minimum_weighted_kappa}")
    if not isinstance(critical_recall, (int, float)) or critical_recall != 1.0:
        errors.append("Model Judge calibration criticalDefectRecall must equal 1.0")
    return errors


def compute_calibration_metrics(samples: Sequence[object]) -> dict[str, float | int]:
    """Compute binary F1, linear weighted kappa, critical recall, and sample count from labels."""

    if len(samples) < _MINIMUM_CALIBRATION_EXAMPLES:
        raise ValueError(f"at least {_MINIMUM_CALIBRATION_EXAMPLES} labeled samples are required")
    human_defects: list[bool] = []
    model_defects: list[bool] = []
    human_scores: list[int] = []
    model_scores: list[int] = []
    critical: list[bool] = []
    seen: set[str] = set()
    observed_classes: set[str] = set()
    class_counts: Counter[str] = Counter()
    for index, item in enumerate(samples):
        if not isinstance(item, Mapping):
            raise ValueError(f"sample {index} must be a mapping")
        sample_id = item.get("id")
        if not isinstance(sample_id, str) or not sample_id or sample_id in seen:
            raise ValueError(f"sample {index} must have a unique non-empty id")
        seen.add(sample_id)
        sample_class = item.get("sampleClass")
        if sample_class not in _REQUIRED_SAMPLE_CLASSES:
            raise ValueError(f"sample {sample_id} must use a declared sampleClass")
        observed_classes.add(str(sample_class))
        class_counts[str(sample_class)] += 1
        human_label = item.get("humanLabel")
        model_label = item.get("modelLabel")
        if human_label not in {"pass", "fail"} or model_label not in {"pass", "fail"}:
            raise ValueError(f"sample {sample_id} labels must be pass or fail")
        human_score = item.get("humanScore")
        model_score = item.get("modelScore")
        if (
            not isinstance(human_score, int)
            or isinstance(human_score, bool)
            or not isinstance(model_score, int)
            or isinstance(model_score, bool)
            or not _ORDERED_SCORE_MINIMUM <= human_score <= _ORDERED_SCORE_MAXIMUM
            or not _ORDERED_SCORE_MINIMUM <= model_score <= _ORDERED_SCORE_MAXIMUM
        ):
            raise ValueError(
                f"sample {sample_id} scores must be integers from "
                f"{_ORDERED_SCORE_MINIMUM} through {_ORDERED_SCORE_MAXIMUM}"
            )
        ambiguous = item.get("ambiguous", False)
        if not isinstance(ambiguous, bool):
            raise ValueError(f"sample {sample_id} ambiguous must be a boolean")
        if sample_class == "boundary" or ambiguous:
            _validate_human_adjudication(item, sample_id, human_label, human_score)
        critical_value = item.get("criticalDefect")
        if not isinstance(critical_value, bool):
            raise ValueError(f"sample {sample_id} criticalDefect must be a boolean")
        human_defects.append(human_label == "fail")
        model_defects.append(model_label == "fail")
        human_scores.append(human_score)
        model_scores.append(model_score)
        critical.append(critical_value)

    missing_classes = sorted(_REQUIRED_SAMPLE_CLASSES - observed_classes)
    if missing_classes:
        raise ValueError(f"calibration samples are missing required classes: {', '.join(missing_classes)}")
    underrepresented = sorted(
        sample_class
        for sample_class in _REQUIRED_SAMPLE_CLASSES
        if class_counts[sample_class] < _MINIMUM_EXAMPLES_PER_CLASS
    )
    if underrepresented:
        raise ValueError(
            f"calibration classes require at least {_MINIMUM_EXAMPLES_PER_CLASS} examples each: "
            f"{', '.join(underrepresented)}"
        )
    if sum(human_defects) < _MINIMUM_FAILED_EXAMPLES:
        raise ValueError(f"at least {_MINIMUM_FAILED_EXAMPLES} Human Judge gold labels must fail")

    true_positive = sum(human and model for human, model in zip(human_defects, model_defects))
    false_positive = sum(not human and model for human, model in zip(human_defects, model_defects))
    false_negative = sum(human and not model for human, model in zip(human_defects, model_defects))
    denominator = 2 * true_positive + false_positive + false_negative
    binary_f1 = 1.0 if denominator == 0 else (2 * true_positive) / denominator
    critical_total = sum(human and critical_value for human, critical_value in zip(human_defects, critical))
    critical_detected = sum(
        human and critical_value and model
        for human, model, critical_value in zip(human_defects, model_defects, critical)
    )
    if critical_total < _MINIMUM_CRITICAL_DEFECTS:
        raise ValueError(
            f"at least {_MINIMUM_CRITICAL_DEFECTS} Human Judge gold failures must be marked as critical defects"
        )
    critical_recall = critical_detected / critical_total
    return {
        "binaryF1": binary_f1,
        "weightedKappa": _linear_weighted_kappa(human_scores, model_scores),
        "criticalDefectRecall": critical_recall,
        "sampleCount": len(samples),
    }


def _linear_weighted_kappa(human_scores: Sequence[int], model_scores: Sequence[int]) -> float:
    categories = tuple(range(_ORDERED_SCORE_MINIMUM, _ORDERED_SCORE_MAXIMUM + 1))
    maximum_distance = _ORDERED_SCORE_MAXIMUM - _ORDERED_SCORE_MINIMUM
    count = len(human_scores)
    observed_disagreement = sum(
        abs(human - model) / maximum_distance
        for human, model in zip(human_scores, model_scores)
    ) / count
    human_counts = Counter(human_scores)
    model_counts = Counter(model_scores)
    expected_disagreement = sum(
        (human_counts[human] / count)
        * (model_counts[model] / count)
        * abs(human - model)
        / maximum_distance
        for human in categories
        for model in categories
    )
    if expected_disagreement == 0:
        return 1.0 if observed_disagreement == 0 else 0.0
    return 1.0 - observed_disagreement / expected_disagreement


def _validate_human_adjudication(
    sample: Mapping[str, object],
    sample_id: str,
    gold_label: object,
    gold_score: object,
) -> None:
    judgments = sample.get("humanJudgments")
    if not isinstance(judgments, list) or len(judgments) < 2:
        raise ValueError(f"ambiguous sample {sample_id} requires two independent Human Judges")
    judge_ids: set[str] = set()
    for index, judgment in enumerate(judgments):
        if not isinstance(judgment, Mapping):
            raise ValueError(f"ambiguous sample {sample_id} Human Judge {index} must be a mapping")
        judge_id = judgment.get("judgeId")
        if not isinstance(judge_id, str) or not judge_id or judge_id in judge_ids:
            raise ValueError(f"ambiguous sample {sample_id} requires unique independent Human Judge ids")
        judge_ids.add(judge_id)
        _validate_label_and_score(judgment, f"ambiguous sample {sample_id} Human Judge {judge_id}")
    adjudication = sample.get("adjudication")
    if not isinstance(adjudication, Mapping):
        raise ValueError(f"ambiguous sample {sample_id} requires adjudicated gold")
    adjudicator_id = adjudication.get("adjudicatorId")
    if not isinstance(adjudicator_id, str) or not adjudicator_id or adjudicator_id in judge_ids:
        raise ValueError(f"ambiguous sample {sample_id} requires an independent adjudicator")
    _validate_label_and_score(adjudication, f"ambiguous sample {sample_id} adjudication")
    if adjudication.get("label") != gold_label or adjudication.get("score") != gold_score:
        raise ValueError(f"ambiguous sample {sample_id} gold label and score must match adjudication")


def _validate_label_and_score(value: Mapping[str, object], label: str) -> None:
    if value.get("label") not in {"pass", "fail"}:
        raise ValueError(f"{label} label must be pass or fail")
    score = value.get("score")
    if (
        not isinstance(score, int)
        or isinstance(score, bool)
        or not _ORDERED_SCORE_MINIMUM <= score <= _ORDERED_SCORE_MAXIMUM
    ):
        raise ValueError(
            f"{label} score must be an integer from "
            f"{_ORDERED_SCORE_MINIMUM} through {_ORDERED_SCORE_MAXIMUM}"
        )
